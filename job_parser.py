#!/usr/bin/env python3
"""
Job Description Parser Agent
Extracts structured job data from job descriptions using PydanticAI and LangChain
"""

from pydantic_ai import Agent
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import streamlit as st
import json
import os
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from config import GROQ_MODEL, validate_config
from vector_store import get_vector_store
from email_tracker import EmailRecord, EmailTracker
from error_handler import handle_groq_api_error


class JobDescriptionInput(BaseModel):
    job_description: str = Field(
        description="Raw job description text to be parsed"
    )


class JobData(BaseModel):
    """Structured job data extracted from job description"""
    job_title: str = Field(
        description="The job title/position name"
    )
    company_name: str = Field(
        description="The company or organization name"
    )
    location: Optional[str] = Field(
        description="Job location (city, state, country, or remote)"
    )
    job_type: Optional[str] = Field(
        description="Type of employment (Full-time, Part-time, Contract, Internship, etc.)"
    )
    experience_level: Optional[str] = Field(
        description="Experience level required (Entry, Mid, Senior, Lead, etc.)"
    )
    required_skills: List[str] = Field(
        description="List of required technical and professional skills"
    )
    preferred_skills: List[str] = Field(
        description="List of preferred or nice-to-have skills"
    )
    responsibilities: List[str] = Field(
        description="List of key responsibilities and duties"
    )
    qualifications: List[str] = Field(
        description="List of required qualifications, education, certifications"
    )
    benefits: List[str] = Field(
        description="List of benefits and perks mentioned"
    )
    salary_range: Optional[str] = Field(
        description="Salary range if mentioned (e.g., $80k-$120k, Competitive, etc.)"
    )
    industry: Optional[str] = Field(
        description="Industry or sector (Technology, Healthcare, Finance, etc.)"
    )
    department: Optional[str] = Field(
        description="Department or team (Engineering, Marketing, Sales, etc.)"
    )
    remote_policy: Optional[str] = Field(
        description="Remote work policy (Remote, Hybrid, On-site, etc.)"
    )
    visa_sponsorship: Optional[bool] = Field(
        description="Whether visa sponsorship is mentioned or available"
    )
    summary: str = Field(
        description="Brief summary of the job role and company"
    )





class JobScraper:
    """Web scraper for job postings"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_job_info_from_url(self, url: str) -> Dict[str, Any]:
        """Extract job information from a job posting URL"""
        try:
            # Validate URL
            if not self._is_valid_job_url(url):
                return {"error": f"Invalid job posting URL for: {url}"}
            
            # Fetch the page
            response = self.session.get(url, timeout=15)  # Increased timeout
            response.raise_for_status()
            
            # Check if we got a valid response
            if response.status_code != 200:
                return {"error": f"HTTP {response.status_code}: {response.reason}"}
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract job information based on common patterns
            job_info = {
                "job_title": self._extract_job_title(soup, url),
                "company_name": self._extract_company_name(soup, url),
                "job_description": self._extract_job_description(soup),
                "source_url": url
            }
            
            # Validate extracted data
            if not job_info["job_description"] or len(job_info["job_description"].strip()) < 50:
                return {"error": "Could not extract sufficient job description from the page"}
            
            return job_info
            
        except requests.RequestException as e:
            return {"error": f"Failed to fetch URL: {str(e)}"}
        except Exception as e:
            return {"error": f"Error extracting job info: {str(e)}"}
    
    def _is_valid_job_url(self, url: str) -> bool:
        """Check if URL is a valid job posting URL"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            path = parsed.path.lower()
            
            # LinkedIn job URLs - more flexible matching
            if 'linkedin.com' in domain and ('/jobs/' in path or '/jobs/view/' in path or '/job/' in path):
                return True
            
            # Indeed job URLs
            if 'indeed.com' in domain and ('/viewjob' in path or '/job/' in path):
                return True
            
            # Glassdoor job URLs
            if 'glassdoor.com' in domain and ('/Job/' in path or '/job/' in path):
                return True
            
            # Other job sites
            job_sites = [
                'monster.com',
                'careerbuilder.com',
                'ziprecruiter.com',
                'dice.com',
                'angel.co',
                'stackoverflow.com',
                'github.com',
                'remote.co',
                'weworkremotely.com',
                'flexjobs.com'
            ]
            
            for site in job_sites:
                if site in domain:
                    return True
            
            return False
        except Exception as e:
            # Log the error for debugging (but don't print in production)
            return False
    
    def _extract_job_title(self, soup: BeautifulSoup, url: str) -> str:
        """Extract job title from the page"""
        # Common selectors for job titles
        selectors = [
            'h1[class*="job-title"]',
            'h1[class*="title"]',
            '.job-title',
            '.title',
            '[data-testid="job-title"]',
            'h1',
            'title'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get_text(strip=True)
                if title and len(title) > 3:
                    return title
        
        # Fallback: extract from URL or page title
        page_title = soup.find('title')
        if page_title:
            title = page_title.get_text(strip=True)
            # Clean up common suffixes
            title = re.sub(r'\s*[-|]\s*(LinkedIn|Indeed|Glassdoor|Monster|CareerBuilder).*', '', title)
            return title
        
        return "Job Title Not Found"
    
    def _extract_company_name(self, soup: BeautifulSoup, url: str) -> str:
        """Extract company name from the page"""
        # Common selectors for company names
        selectors = [
            '[class*="company"]',
            '[class*="employer"]',
            '[data-testid="company"]',
            '.company-name',
            '.employer-name',
            'a[href*="/company/"]',
            'a[href*="/employer/"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                company = element.get_text(strip=True)
                if company and len(company) > 2:
                    return company
        
        # Fallback: try to extract from URL
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Extract company from domain patterns
        if 'linkedin.com' in domain:
            # LinkedIn company pages often have company in path
            path_parts = parsed.path.split('/')
            for part in path_parts:
                if part and part not in ['jobs', 'job', 'company', '']:
                    return part.replace('-', ' ').title()
        
        return "Company Name Not Found"
    
    def _extract_job_description(self, soup: BeautifulSoup) -> str:
        """Extract job description from the page"""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
            script.decompose()
        
        # Common selectors for job descriptions (ordered by specificity)
        selectors = [
            '[class*="job-description"]',
            '[class*="description"]',
            '[class*="details"]',
            '[class*="content"]',
            '[class*="requirements"]',
            '[class*="responsibilities"]',
            '.job-description',
            '.job-details',
            '.description',
            '.content',
            '[data-testid="job-description"]',
            '[data-testid="description"]',
            'main',
            'article',
            '[role="main"]'
        ]
        
        # Try each selector
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(separator='\n', strip=True)
                # Check if this looks like a job description
                if text and len(text) > 200:  # Increased minimum length
                    # Additional validation: check for job-related keywords
                    job_keywords = ['requirements', 'responsibilities', 'experience', 'skills', 'qualifications', 'duties', 'role', 'position']
                    if any(keyword.lower() in text.lower() for keyword in job_keywords):
                        return text
        
        # Fallback: get all text from body and try to extract the main content
        body = soup.find('body')
        if body:
            # Try to find the largest text block that might be the job description
            text_blocks = []
            for element in body.find_all(['div', 'section', 'article', 'main']):
                text = element.get_text(separator='\n', strip=True)
                if text and len(text) > 300:  # Look for substantial text blocks
                    text_blocks.append((len(text), text))
            
            if text_blocks:
                # Sort by length and return the longest
                text_blocks.sort(key=lambda x: x[0], reverse=True)
                longest_text = text_blocks[0][1]
                
                # Clean up the text
                cleaned_text = re.sub(r'\n\s*\n', '\n\n', longest_text)  # Remove excessive newlines
                cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # Normalize whitespace
                return cleaned_text
        
        # Last resort: get all body text
        if body:
            text = body.get_text(separator='\n', strip=True)
            # Clean up the text
            text = re.sub(r'\n\s*\n', '\n\n', text)  # Remove excessive newlines
            text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
            return text
        
        return "Job description not found"


class JobParserAgent:
    """Job Description Parser Agent using PydanticAI"""
    
    def __init__(self):
        validate_config()
        self.agent = Agent(
            model=GROQ_MODEL,
            deps_type=JobDescriptionInput,
            result_type=JobData,
            system_prompt="""You are a specialized Job Description Parser that extracts structured information from job postings.

CRITICAL INSTRUCTIONS:
- Extract ONLY information that is explicitly stated in the job description
- DO NOT generate, invent, or assume any information
- If a field is not present, use empty string or empty list
- Be precise and accurate with the actual content
- Focus on extracting real data, not creating sample data
- For skills, separate required vs preferred skills
- For responsibilities, extract key duties and expectations
- For qualifications, include education, experience, certifications
- For benefits, extract perks, compensation, work arrangements

Extraction tasks:
1. Job Title: Extract the exact job title/position name
2. Company Name: Extract the hiring company or organization
3. Location: Extract job location (city, state, country, remote info)
4. Job Type: Extract employment type (Full-time, Part-time, Contract, etc.)
5. Experience Level: Extract required experience level
6. Required Skills: List skills explicitly marked as required
7. Preferred Skills: List skills marked as preferred or nice-to-have
8. Responsibilities: Extract key duties and responsibilities
9. Qualifications: Extract education, experience, certification requirements
10. Benefits: Extract mentioned benefits, perks, compensation
11. Salary Range: Extract salary information if mentioned
12. Industry: Extract industry or sector information
13. Department: Extract department or team information
14. Remote Policy: Extract remote work policy details
15. Visa Sponsorship: Determine if visa sponsorship is mentioned
16. Summary: Create a brief summary of the role and company

Remember: Extract what's there, don't create what's not there."""
        )
        self.scraper = JobScraper()
    
    async def parse_job_description(self, job_description: str) -> JobData:
        """Parse job description and extract structured data"""
        try:
            result = await self.agent.run(
                f"""Please extract structured information from this job description:

JOB DESCRIPTION:
{job_description}

INSTRUCTIONS:
- Extract ONLY information that is explicitly present in the text above
- If information is missing, use empty strings or empty lists
- Do not create sample data or assume information
- Be precise and accurate with the actual content
- Separate required skills from preferred skills
- Extract all relevant details about the role, company, and requirements

Please extract the structured job information.""",
                deps=JobDescriptionInput(job_description=job_description)
            )
            
            return result.data
        except Exception as e:
            handle_groq_api_error(e, "job parsing")
            return None
    
    def scrape_and_parse_job(self, url: str) -> JobData:
        """Scrape job posting from URL and parse it"""
        try:
            # Debug: Log the URL being processed
            st.info(f"🔍 Processing URL: {url}")
            
            # Extract job info from URL
            job_info = self.scraper.extract_job_info_from_url(url)
            
            # Debug: Log the extracted job info
            if "error" in job_info:
                st.error(f"❌ Error scraping job: {job_info['error']}")
                return None
            
            # Debug: Show what was extracted
            st.success(f"✅ Successfully extracted job info:")
            st.write(f"• Job Title: {job_info.get('job_title', 'Not found')}")
            st.write(f"• Company: {job_info.get('company_name', 'Not found')}")
            st.write(f"• Description Length: {len(job_info.get('job_description', ''))} characters")
            
            # Check if we have a valid job description
            if not job_info.get('job_description') or len(job_info['job_description'].strip()) < 50:
                st.error("❌ Extracted job description is too short or empty")
                st.write("**Raw extracted text:**")
                st.text(job_info.get('job_description', 'No description found'))
                return None
            
            # Parse the extracted job description
            st.info("🤖 Parsing job description with AI...")
            import asyncio
            job_data = asyncio.run(self.parse_job_description(job_info["job_description"]))
            
            if job_data:
                st.success("✅ Job parsing completed successfully!")
                return job_data
            else:
                st.error("❌ Failed to parse job description")
                return None
            
        except Exception as e:
            st.error(f"❌ Error during job scraping: {str(e)}")
            st.info("💡 This might be due to:")
            st.write("• Website blocking automated requests")
            st.write("• Invalid or expired job posting URL")
            st.write("• Network connectivity issues")
            st.write("• Website structure changes")
            handle_groq_api_error(e, "job scraping")
            return None





def create_job_parser_ui():
    """Create Streamlit UI for job description parsing"""
    st.title("🔍 Job Description Parser")
    st.write("Parse job descriptions to extract structured data for email generation")
    
    # Initialize vector store
    vector_store = get_vector_store()
    
    # Check if CV data is available from previous step
    cv_data = vector_store.get_cv_data()
    if cv_data:
        st.success("✅ CV data loaded from previous step!")
        with st.expander("📋 Your CV Summary"):
            col1, col2 = st.columns(2)
            with col1:
                # Handle both Pydantic model and dictionary for CV data
                if hasattr(cv_data, 'name'):
                    # Pydantic model
                    st.write(f"**Name:** {cv_data.name}")
                    st.write(f"**Skills:** {', '.join(cv_data.skills[:5])}...")
                else:
                    # Dictionary
                    st.write(f"**Name:** {cv_data.get('name', 'N/A')}")
                    st.write(f"**Skills:** {', '.join(cv_data.get('skills', [])[:5])}...")
            with col2:
                # Handle both Pydantic model and dictionary for CV data
                if hasattr(cv_data, 'experience'):
                    # Pydantic model
                    st.write(f"**Experience:** {len(cv_data.experience)} positions")
                    st.write(f"**Projects:** {len(cv_data.projects)} projects")
                else:
                    # Dictionary
                    st.write(f"**Experience:** {len(cv_data.get('experience', []))} positions")
                    st.write(f"**Projects:** {len(cv_data.get('projects', []))} projects")
    else:
        st.info("💡 No CV data found. You can still parse job descriptions, but personalized email generation will require CV data.")
    
    # Initialize components
    if 'job_parser' not in st.session_state:
        st.session_state.job_parser = JobParserAgent()
    
    if 'email_tracker' not in st.session_state:
        st.session_state.email_tracker = EmailTracker()
    
    # Input method selection
    st.subheader("📝 Job Information Input")
    input_method = st.radio(
        "Choose input method:",
        ["Manual Text Input", "Job URL Scraping"],
        help="Select how you want to provide job information"
    )
    
    if input_method == "Manual Text Input":
        # Manual job description input
        job_description = st.text_area(
            "Paste Job Description",
            placeholder="Paste the complete job description here...",
            height=300,
            help="Paste the full job description including requirements, responsibilities, and company information"
        )
        
        if st.button("🔍 Parse Job Description", type="primary", use_container_width=True):
            if job_description.strip():
                with st.spinner("Parsing job description..."):
                    import asyncio
                    try:
                        job_data = asyncio.run(st.session_state.job_parser.parse_job_description(job_description))
                        if job_data:
                            # Store in vector database
                            job_dict = job_data.model_dump()
                            record_id = vector_store.store_job_data(job_dict)
                            
                            if record_id:
                                st.session_state.current_job_data = job_data
                                display_job_results(job_data)
                            else:
                                st.error("Failed to store job data")
                        else:
                            st.error("Failed to parse job description")
                    except Exception as e:
                        st.error(f"Error during parsing: {e}")
            else:
                st.warning("Please enter a job description to parse")
    
    else:
        # URL-based job scraping
        st.write("**Supported job sites:** LinkedIn, Indeed, Glassdoor, Monster, CareerBuilder, ZipRecruiter, Dice, Angel.co, Stack Overflow Jobs, GitHub Jobs, Remote.co, WeWorkRemotely, FlexJobs")
        
        col1, col2 = st.columns(2)
        with col1:
            job_title = st.text_input(
                "Job Title",
                placeholder="e.g., Senior Software Engineer",
                help="Enter the job title for reference"
            )
        
        with col2:
            company_name = st.text_input(
                "Company Name",
                placeholder="e.g., Google",
                help="Enter the company name for reference"
            )
        
        job_url = st.text_input(
            "Job Posting URL",
            placeholder="https://www.linkedin.com/jobs/view/...",
            help="Paste the complete URL of the job posting"
        )
        
        if st.button("🌐 Scrape & Parse Job", type="primary", use_container_width=True):
            if job_url.strip():
                with st.spinner("Scraping and parsing job posting..."):
                    try:
                        job_data = st.session_state.job_parser.scrape_and_parse_job(job_url)
                        if job_data:
                            # Override with manual inputs if provided
                            if job_title:
                                job_data.job_title = job_title
                            if company_name:
                                job_data.company_name = company_name
                            
                            # Store in vector database
                            job_dict = job_data.model_dump()
                            record_id = vector_store.store_job_data(job_dict)
                            
                            if record_id:
                                st.session_state.current_job_data = job_data
                                display_job_results(job_data)
                            else:
                                st.error("Failed to store job data")
                        else:
                            st.error("Failed to scrape and parse job posting")
                    except Exception as e:
                        st.error(f"Error during scraping: {e}")
            else:
                st.warning("Please enter a job posting URL")
    
    # Email Tracking Section
    st.subheader("📧 Email Tracking")
    
    # Show statistics
    stats = st.session_state.email_tracker.get_statistics()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Emails", stats["total_emails"])
    with col2:
        st.metric("Companies Contacted", stats["companies_contacted"])
    with col3:
        st.metric("Recent Emails (30d)", stats["recent_emails"])
    with col4:
        st.metric("Success Rate", f"{stats['success_rate']}%")
    
    # Show recent emails
    recent_emails = st.session_state.email_tracker.get_recent_emails(30)
    if recent_emails:
        with st.expander("📋 Recent Email History"):
            for record in recent_emails[-10:]:  # Show last 10
                st.write(f"**{record.job_title}** at **{record.company_name}**")
                st.write(f"Sent: {record.sent_date.strftime('%Y-%m-%d %H:%M')} | Status: {record.status}")
                st.write("---")
    
    # Debug section (only show in development)
    if st.checkbox("🔧 Show Debug Options", help="Enable debug features for troubleshooting"):
        st.subheader("🔧 Debug Tools")
        
        # Test scraper functionality
        if st.button("🧪 Test Scraper", help="Test the scraper with a sample URL"):
            test_url = "https://www.linkedin.com/jobs/view/software-engineer-at-google-123456"
            st.info(f"Testing URL: {test_url}")
            
            try:
                scraper = JobScraper()
                job_info = scraper.extract_job_info_from_url(test_url)
                
                if "error" in job_info:
                    st.error(f"❌ Test failed: {job_info['error']}")
                else:
                    st.success("✅ Test successful!")
                    st.write(f"Title: {job_info.get('job_title')}")
                    st.write(f"Company: {job_info.get('company_name')}")
                    st.write(f"Description Length: {len(job_info.get('job_description', ''))}")
                    
                    # Show description preview
                    desc = job_info.get('job_description', '')
                    if desc:
                        with st.expander("Description Preview"):
                            st.text(desc[:500] + "..." if len(desc) > 500 else desc)
            except Exception as e:
                st.error(f"❌ Test exception: {e}")
        
        # Show session state info
        with st.expander("📊 Session State Info"):
            st.write("Current session state keys:")
            for key in st.session_state.keys():
                st.write(f"• {key}: {type(st.session_state[key]).__name__}")
    
    # Navigation hint
    if cv_data and st.session_state.get('current_job_data'):
        st.success("✅ Ready for email generation! Navigate to the Email Generator page to create personalized emails.")
    
    return st.session_state.get('current_job_data')


def display_job_results(job_data: JobData):
    """Display parsed job results"""
    st.success("Job description parsed successfully!")
    
    # Job Overview
    st.subheader("📋 Job Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Job Title", job_data.job_title)
        st.metric("Company", job_data.company_name)
    with col2:
        st.metric("Location", job_data.location or "Not specified")
        st.metric("Job Type", job_data.job_type or "Not specified")
    with col3:
        st.metric("Experience Level", job_data.experience_level or "Not specified")
        st.metric("Industry", job_data.industry or "Not specified")
    
    # Check for duplicates
    is_duplicate = st.session_state.email_tracker.check_duplicate(
        job_data.job_title, 
        job_data.company_name
    )
    
    if is_duplicate:
        st.warning("⚠️ An email has already been sent for this job/company in the last 30 days!")
    
    # Detailed Information
    with st.expander("📊 Detailed Job Information"):
        # Skills
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Required Skills:**")
            for skill in job_data.required_skills:
                st.write(f"• {skill}")
        
        with col2:
            st.write("**Preferred Skills:**")
            for skill in job_data.preferred_skills:
                st.write(f"• {skill}")
        
        # Responsibilities
        st.write("**Key Responsibilities:**")
        for resp in job_data.responsibilities:
            st.write(f"• {resp}")
        
        # Qualifications
        st.write("**Qualifications:**")
        for qual in job_data.qualifications:
            st.write(f"• {qual}")
        
        # Benefits
        if job_data.benefits:
            st.write("**Benefits:**")
            for benefit in job_data.benefits:
                st.write(f"• {benefit}")
        
        # Additional Info
        if job_data.salary_range:
            st.write(f"**Salary Range:** {job_data.salary_range}")
        if job_data.remote_policy:
            st.write(f"**Remote Policy:** {job_data.remote_policy}")
        if job_data.visa_sponsorship is not None:
            st.write(f"**Visa Sponsorship:** {'Yes' if job_data.visa_sponsorship else 'No'}")
    
    # Summary
    st.subheader("📝 Job Summary")
    st.write(job_data.summary)
    
    # Store for email generation
    st.session_state.job_data_for_email = job_data


if __name__ == "__main__":
    create_job_parser_ui() 