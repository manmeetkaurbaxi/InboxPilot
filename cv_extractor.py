#!/usr/bin/env python3
"""
CV/Resume Data Extractor
Extracts structured data from PDF resumes using AI and allows manual input of social links
"""

from pydantic_ai import Agent
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import streamlit as st
import asyncio
import json
import PyPDF2
import io
from config import GROQ_MODEL, validate_config
from vector_store import get_vector_store
from error_handler import handle_groq_api_error


class CVExtractionInput(BaseModel):
    cv_text: str = Field(
        description="Raw text extracted from the CV/Resume PDF"
    )

class CVExtractionResult(BaseModel):
    name: str = Field(
        description="Full name of the person from the CV (leave empty if not found)"
    )
    email: str = Field(
        description="Email address from the CV (leave empty if not found)"
    )
    phone: Optional[str] = Field(
        description="Phone number from the CV (leave empty if not found)"
    )
    education: List[str] = Field(
        description="List of educational qualifications and institutions with years and GPA (leave empty if not found)"
    )
    experience: List[str] = Field(
        description="List of work experience and job titles with years (leave empty if not found)"
    )
    volunteer: List[str] = Field(
        description="List of volunteer experience, community service, and unpaid work with years (leave empty if not found)"
    )
    skills: List[str] = Field(
        description="List of technical and professional skills (leave empty if not found)"
    )
    projects: List[str] = Field(
        description="List of notable projects and achievements with years (leave empty if not found)"
    )
    awards: List[str] = Field(
        description="List of awards, honors, scholarships, and recognitions with years (leave empty if not found)"
    )
    publications: List[str] = Field(
        description="List of research publications, papers, articles, and presentations with years (leave empty if not found)"
    )
    summary: str = Field(
        description="Professional summary or objective from the CV (leave empty if not found)"
    )
    
    def sort_by_year(self):
        """Sort all time-based fields from latest to oldest by year"""
        import re
        
        def extract_year(text):
            """Extract year from text, return 0 if no year found"""
            if not text:
                return 0
            # Look for 4-digit years
            years = re.findall(r'\b(19|20)\d{2}\b', text)
            if years:
                return max(int(year) for year in years)
            return 0
        
        def sort_list_by_year(items):
            """Sort list by extracted year, latest first"""
            if not items:
                return items
            return sorted(items, key=extract_year, reverse=True)
        
        # Sort all time-based fields
        self.education = sort_list_by_year(self.education)
        self.experience = sort_list_by_year(self.experience)
        self.volunteer = sort_list_by_year(self.volunteer)
        self.projects = sort_list_by_year(self.projects)
        self.awards = sort_list_by_year(self.awards)
        self.publications = sort_list_by_year(self.publications)
        
        return self
    
    def validate_extraction(self):
        """Validate that the extraction contains real data, not placeholder data"""
        placeholder_indicators = [
            "john doe", "jane doe", "sample", "example", "placeholder", 
            "test", "demo", "lorem ipsum", "your name", "your email"
        ]
        
        # Check name
        if self.name.lower() in placeholder_indicators:
            return False, f"Name appears to be placeholder: {self.name}"
        
        # Check email
        if self.email.lower() in placeholder_indicators or "@example.com" in self.email.lower():
            return False, f"Email appears to be placeholder: {self.email}"
        
        # Check if all fields are empty (might indicate extraction failure)
        if not any([self.name, self.email, self.education, self.experience, self.volunteer, self.skills, self.awards, self.publications]):
            return False, "No meaningful data was extracted from the CV"
        
        return True, "Extraction appears to contain real data"


def create_cv_extraction_agent():
    """Create CV extraction agent with proper API key configuration"""
    # Validate configuration
    validate_config()
    
    return Agent(
        model=GROQ_MODEL,
        deps_type=CVExtractionInput,
        result_type=CVExtractionResult,
        system_prompt="""You are a specialized CV/Resume parser that extracts ONLY the actual information present in the provided CV text. 

CRITICAL INSTRUCTIONS:
- Extract ONLY information that is explicitly stated in the CV text
- DO NOT generate, invent, or assume any information
- If a field is not present in the CV, use empty string or empty list
- If you cannot find specific information, leave it blank rather than guessing
- Be precise and accurate with the actual content
- Focus on extracting real data, not creating sample data
- ALWAYS include years and dates when available
- For education, include GPA if mentioned
- Pay special attention to volunteer work, community service, and unpaid positions
- Look for sections like "Volunteer", "Community Service", "Awards", "Honors", "Publications", "Research", "Papers", etc.

Extraction tasks:
1. Personal Information: Extract name, email, phone ONLY if they appear in the text
2. Education: List actual degrees, institutions, years, and GPA if mentioned
3. Experience: Extract real job titles, companies, and years/durations
4. Volunteer: Extract volunteer work, community service, unpaid positions with years
5. Skills: List only skills explicitly mentioned in the CV
6. Projects: Extract only projects that are actually described with years
7. Awards: Extract awards, honors, scholarships, recognitions, certificates, and achievements with years
8. Publications: Extract research papers, journal articles, conference presentations, books, reports, and publications with years
9. Summary: Use the actual summary/objective if present, otherwise leave blank

Remember: Extract what's there, don't create what's not there."""
    )


def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if page_text.strip():  # Only add non-empty pages
                text += f"\n--- Page {page_num + 1} ---\n"
                text += page_text
                text += "\n"
        
        # Clean up the text
        text = text.strip()
        
        # Remove excessive whitespace
        import re
        text = re.sub(r'\n\s*\n', '\n\n', text)  # Remove multiple empty lines
        text = re.sub(r' +', ' ', text)  # Remove multiple spaces
        
        if not text.strip():
            st.error("No text could be extracted from the PDF. The PDF might be image-based or corrupted.")
            return None
            
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None


async def extract_cv_data(cv_text: str) -> CVExtractionResult:
    """Extract structured data from CV text using PydanticAI agent"""
    try:
        # Create agent dynamically
        agent = create_cv_extraction_agent()
        
        # Create a more specific prompt with the actual CV text
        prompt = f"""Please extract ONLY the actual information from this CV text. Do not generate or invent any information.

CV TEXT TO ANALYZE:
{cv_text}

INSTRUCTIONS:
- Extract ONLY information that is explicitly present in the text above
- If information is missing, use empty strings or empty lists
- Do not create sample data like "John Doe" or placeholder information
- Be precise and accurate with the actual content
- ALWAYS include years and dates when available
- For education entries, include GPA if mentioned
- Pay special attention to volunteer work, community service, and unpaid positions
- Look for sections like "Volunteer", "Community Service", "Awards", "Honors", "Publications", "Research", "Papers", etc.

Please extract the structured information from this CV."""
        
        result = await agent.run(
            prompt,
            deps=CVExtractionInput(cv_text=cv_text)
        )
        
        # Sort the extracted data by year (latest first)
        if result.data:
            result.data.sort_by_year()
            
        return result.data
    except Exception as e:
        handle_groq_api_error(e, "CV extraction")
        return None


def create_manual_links_section():
    """Create manual input section for social links and GitHub repositories"""
    st.subheader("🔗 Social Links & GitHub Repositories")
    st.write("Enter your usernames for social platforms and GitHub repositories:")
    
    links = {}
    
    # Social Media Links - Username inputs
    st.write("**Social Media Usernames:**")
    col1, col2 = st.columns(2)
    
    with col1:
        linkedin_username = st.text_input("LinkedIn Username", placeholder="john-doe", help="Your LinkedIn profile username (e.g., john-doe)")
        if linkedin_username:
            links["LinkedIn"] = f"https://linkedin.com/in/{linkedin_username.strip()}"
            
        twitter_username = st.text_input("Twitter/X Username", placeholder="johndoe", help="Your Twitter/X username (e.g., johndoe)")
        if twitter_username:
            links["Twitter"] = f"https://twitter.com/{twitter_username.strip()}"
            
        github_username = st.text_input("GitHub Username", placeholder="johndoe", help="Your GitHub username (e.g., johndoe)")
        if github_username:
            links["GitHub"] = f"https://github.com/{github_username.strip()}"
    
    with col2:
        medium_username = st.text_input("Medium Username", placeholder="@johndoe", help="Your Medium username (e.g., @johndoe)")
        if medium_username:
            # Remove @ if user includes it
            clean_username = medium_username.strip().lstrip('@')
            links["Medium"] = f"https://medium.com/@{clean_username}"
            
        # Portfolio website (still full URL since it's custom)
        portfolio_url = st.text_input("Portfolio Website", placeholder="https://johndoe.dev", help="Your personal portfolio website URL")
        if portfolio_url:
            links["Portfolio"] = portfolio_url.strip()
    
    # GitHub Repositories - Username + repository names
    st.write("**GitHub Repositories:**")
    st.write("Enter your GitHub username and repository names (one per line):")
    
    if github_username:
        st.info(f"GitHub Username: {github_username}")
        repo_input = st.text_area(
            "Repository Names", 
            placeholder="my-awesome-project\nportfolio-website\nmachine-learning-project",
            help="Enter repository names only (one per line). URLs will be automatically generated using your GitHub username."
        )
        
        if repo_input:
            repos = [repo.strip() for repo in repo_input.split('\n') if repo.strip()]
            for i, repo in enumerate(repos, 1):
                # Clean repository name (remove any URLs or extra characters)
                clean_repo = repo.strip().split('/')[-1]  # Take last part if full path given
                links[f"GitHub Repo {i}"] = f"https://github.com/{github_username.strip()}/{clean_repo}"
    else:
        st.warning("Please enter your GitHub username above to add repositories.")
    
    # Show preview of generated links
    if links:
        st.subheader("📋 Generated Links Preview")
        with st.expander("Click to see generated URLs"):
            for label, url in links.items():
                st.write(f"• **{label}**: [{url}]({url})")
    
    return links


def create_cv_extraction_ui():
    """Create Streamlit UI for CV extraction with stepwise approach"""
    st.title("📄 CV/Resume Data Extractor")
    st.write("Step-by-step data collection for personalized emails")
    
    # Initialize vector store
    vector_store = get_vector_store()
    
    # Initialize session state for step tracking
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'manual_links' not in st.session_state:
        st.session_state.manual_links = {}
    
    if 'cv_data' not in st.session_state:
        st.session_state.cv_data = None
    
    # Step indicator
    st.subheader(f"Step {st.session_state.current_step} of 3")
    
    if st.session_state.current_step == 1:
        # Step 1: Social Links Collection
        st.write("**Step 1: Add your social media links and GitHub repositories**")
        st.write("This information will be used to personalize your emails.")
        
        manual_links = create_manual_links_section()
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", disabled=True):
                st.session_state.current_step = 1
        
        with col2:
            if st.button("Next → Upload CV/Resume", type="primary", use_container_width=True):
                # Store the manual links
                st.session_state.manual_links = manual_links
                st.session_state.current_step = 2
                st.rerun()
        
        # Show current progress
        if manual_links:
            st.success(f"✅ {len(manual_links)} links collected")
            with st.expander("📋 Collected Links"):
                for label, url in manual_links.items():
                    st.write(f"• **{label}**: {url}")
    
    elif st.session_state.current_step == 2:
        # Step 2: CV/Resume Upload and Extraction
        st.write("**Step 2: Upload and extract data from your CV/Resume**")
        st.write("Upload your CV/Resume PDF to extract structured information.")
        
        # Show collected links from step 1
        if st.session_state.manual_links:
            st.info("📋 Links from Step 1:")
            for label, url in st.session_state.manual_links.items():
                st.write(f"• **{label}**: {url}")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload your CV/Resume in PDF format"
        )
        
        cv_data = None
        
        if uploaded_file is not None:
            # Display file info
            st.success(f"File uploaded: {uploaded_file.name}")
            
            # Extract text from PDF
            with st.spinner("Extracting text from PDF..."):
                cv_text = extract_text_from_pdf(uploaded_file)
            
            if cv_text:
                # Display raw text
                with st.expander("Raw CV Text"):
                    st.text_area("Extracted Text", cv_text, height=200)
                
                # Extract structured data
                if st.button("Extract Structured Data", type="primary", use_container_width=True):
                    with st.spinner("Extracting structured data..."):
                        # Run async function properly
                        try:
                            cv_data = asyncio.run(extract_cv_data(cv_text))
                        except Exception as e:
                            st.error(f"Error during extraction: {e}")
                            cv_data = None
                    
                    if cv_data:
                        # Validate the extraction
                        is_valid, message = cv_data.validate_extraction()
                        
                        if is_valid:
                            # Store CV data in session state as dictionary
                            cv_dict = cv_data.model_dump()
                            st.session_state.cv_data = cv_dict
                            
                            # Store in vector database
                            record_id = vector_store.store_cv_data(cv_dict)
                            
                            if record_id:
                                st.success("✅ CV data extracted and stored successfully!")
                            else:
                                st.warning("⚠️ CV data extracted but failed to store in vector database")
                            
                            # Display extracted data
                            st.success("Data extraction completed!")
                            
                            # Personal Information
                            st.subheader("👤 Personal Information")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Name", cv_data.name)
                            with col2:
                                st.metric("Email", cv_data.email)
                            with col3:
                                st.metric("Phone", cv_data.phone or "Not provided")
                            
                            # Education
                            st.subheader("🎓 Education")
                            for edu in cv_data.education:
                                st.write(f"• {edu}")
                            
                            # Experience
                            st.subheader("💼 Work Experience")
                            for exp in cv_data.experience:
                                st.write(f"• {exp}")
                            
                            # Volunteer Experience
                            if cv_data.volunteer:
                                st.subheader("🤝 Volunteer Experience")
                                for vol in cv_data.volunteer:
                                    st.write(f"• {vol}")
                            
                            # Skills
                            st.subheader("🛠️ Skills")
                            skills_text = ", ".join(cv_data.skills)
                            st.write(skills_text)
                            
                            # Projects
                            st.subheader("🚀 Projects & Achievements")
                            for project in cv_data.projects:
                                st.write(f"• {project}")
                            
                            # Awards
                            if cv_data.awards:
                                st.subheader("🏆 Awards & Honors")
                                for award in cv_data.awards:
                                    st.write(f"• {award}")
                            
                            # Publications
                            if cv_data.publications:
                                st.subheader("📚 Publications")
                                for pub in cv_data.publications:
                                    st.write(f"• {pub}")
                            
                            # Summary
                            if cv_data.summary:
                                st.subheader("📝 Professional Summary")
                                st.write(cv_data.summary)
                        else:
                            st.error(f"❌ {message}")
                            st.write("**Extracted Data (for debugging):**")
                            st.json(cv_data.model_dump())
                    else:
                        st.error("Failed to extract structured data from CV")
            else:
                st.error("Failed to extract text from PDF")
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back to Social Links"):
                st.session_state.current_step = 1
                st.rerun()
        
        with col2:
            if st.button("Next → Download Data", type="primary", use_container_width=True, disabled=not st.session_state.cv_data):
                st.session_state.current_step = 3
                st.rerun()
    
    elif st.session_state.current_step == 3:
        # Step 3: Data Review and Download
        st.write("**Step 3: Review and download your collected data**")
        st.write("Review all collected information before downloading/cold-emailing.")
        
        # Display all collected data
        st.subheader("📊 Collected Data Summary")
        
        # CV Data Summary
        if st.session_state.cv_data:
            cv_data = st.session_state.cv_data
            st.write("**👤 CV Data:**")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"• Name: {cv_data.get('name', 'N/A')}")
                st.write(f"• Email: {cv_data.get('email', 'N/A')}")
                st.write(f"• Education: {len(cv_data.get('education', []))} entries")
                st.write(f"• Experience: {len(cv_data.get('experience', []))} positions")
            with col2:
                st.write(f"• Skills: {len(cv_data.get('skills', []))} skills")
                st.write(f"• Projects: {len(cv_data.get('projects', []))} projects")
                st.write(f"• Awards: {len(cv_data.get('awards', []))} awards")
                st.write(f"• Publications: {len(cv_data.get('publications', []))} publications")
        
        # Manual Links Summary
        if st.session_state.manual_links:
            st.write("**🔗 Social Links:**")
            for label, url in st.session_state.manual_links.items():
                st.write(f"• {label}: {url}")
        
        # Download section
        st.subheader("💾 Download Combined Data")
        
        # Create combined data structure
        combined_data = {}
        if st.session_state.cv_data:
            combined_data.update(st.session_state.cv_data)
        if st.session_state.manual_links:
            combined_data["manual_links"] = st.session_state.manual_links
        
        # Download button
        json_data = json.dumps(combined_data, indent=2)
        st.download_button(
            label="📥 Download as JSON",
            data=json_data,
            file_name="cv_extracted_data.json",
            mime="application/json"
        )
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back to CV Upload"):
                st.session_state.current_step = 2
                st.rerun()
        
        with col2:
            if st.button("🚀 Continue to Job Parser", type="primary", use_container_width=True):
                st.success("✅ Data collection completed! Navigate to the Job Parser page to continue.")
                st.info("💡 Use the sidebar to navigate to 'Job Parser' page")
                st.balloons()
        
        # Success message
        st.success("🎉 Data collection completed! You can now use this data for email generation.")
    
    # Return the collected data for use in other parts of the application
    return st.session_state.cv_data, st.session_state.manual_links


if __name__ == "__main__":
    create_cv_extraction_ui() 