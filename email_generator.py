#!/usr/bin/env python3
"""
Cold Email Generator Agent
Generates personalized cold emails using CV data and job data
"""

from pydantic_ai import Agent
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import streamlit as st
import uuid
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_tracker import EmailRecord, EmailTracker
from config import GROQ_MODEL, validate_config, EMAIL_ADDRESS, EMAIL_PASSWORD, SENDER_NAME
from vector_store import get_vector_store
from error_handler import handle_groq_api_error


class EmailGenerationInput(BaseModel):
    cv_data: Dict[str, Any] = Field(
        description="CV data including personal info, skills, experience, etc."
    )
    job_data: Dict[str, Any] = Field(
        description="Job data including title, company, requirements, etc."
    )
    email_type: str = Field(
        description="Type of email to generate (academic, industry, freelance, networking)"
    )
    tone: str = Field(
        description="Email tone (professional, friendly, confident, enthusiastic)"
    )
    recipient_name: Optional[str] = Field(
        description="Recipient name if known"
    )
    recipient_email: Optional[str] = Field(
        description="Recipient email address"
    )


class GeneratedEmail(BaseModel):
    """Generated email content"""
    subject_line: str = Field(
        description="Compelling email subject line"
    )
    greeting: str = Field(
        description="Personalized greeting"
    )
    introduction: str = Field(
        description="Opening paragraph introducing yourself and purpose"
    )
    body: str = Field(
        description="Main body with relevant experience and skills"
    )
    call_to_action: str = Field(
        description="Clear call to action"
    )
    closing: str = Field(
        description="Professional closing"
    )
    full_email: str = Field(
        description="Complete email content"
    )
    personalization_score: int = Field(
        description="Score indicating how personalized the email is (1-10)"
    )


class EmailGeneratorAgent:
    """Cold Email Generator Agent using PydanticAI"""
    
    def __init__(self):
        validate_config()
        self.agent = Agent(
            model=GROQ_MODEL,
            deps_type=EmailGenerationInput,
            result_type=GeneratedEmail,
            system_prompt="""You are a specialized Cold Email Generator that creates highly personalized, compelling emails for job applications.

CRITICAL INSTRUCTIONS:
- Create emails that are highly personalized to the specific job and company
- Use specific details from the CV and job description
- Match skills and experience to job requirements
- Create compelling & catchy subject lines that stand out
- Write in a professional and engaging tone
- Keep emails concise but impactful (150-300 words)
- Avoid generic templates - make each email unique
- Use the recipient's name if provided
- Reference specific company details and job requirements

Email Structure:
1. Subject Line: Compelling, specific, and relevant
2. TLDR Hook: 2-3 line compelling personal narrative (gritty, humble, focused)
3. Personalized Compliment: Specific about their company/product/mission
4. Credibility Through Experience: 2-sentence impact summary with verifiable links
5. Value-First: What you can do for them (map skills to their pain points)
6. Signal of Fit: Show adaptability and experience
7. Strong Call-to-Action: Ownership-focused, not just job-seeking

Subject Line Variations (use these patterns for catchy, personalized subject lines):
- "Ex [Previous Company] [Role] interested in [Target Role] at [Target Company]"
- "Former [Previous Company] [Role] from [University] interested in [Target Company]"
- "[University] [Degree] grad with [X] years at [Previous Company] - [Target Role]"
- "[Previous Company] [Role] → [Target Company] [Target Role]"
- "[University] alum with [X] years [Industry] experience - [Target Role]"
- "From [Previous Company] to [Target Company] - [Target Role] application"
- "[Previous Company] [Role] seeking [Target Role] at [Target Company]"
- "[University] [Degree] + [X] years at [Previous Company] = Perfect for [Target Role]"
- "[Previous Company] experience + [Target Company] opportunity"
- "[University] grad with [Previous Company] background - [Target Role]"

Personalization Techniques:
- Reference specific skills from CV that match job requirements
- Mention relevant projects or achievements
- Connect experience to company's industry or mission
- Use company-specific details when available
- Reference the specific job title and company name
- Avoid excessive jargon, buzzwords, or flattery
- Express both curiosity about {company_name} and the specific value you can provide
- Include relevant social links or portfolio if available
- Use subject line variations that highlight relevant experience and education

Body Strategy (Viral Cold Email Framework):
1. TLDR Hook: Start with 2-3 lines of compelling personal narrative - gritty, humble, focused tone
2. Personalized Compliment: Open with something specific about their company/product/mission - show you've done research
3. Credibility Through Experience: 2-sentence impact summary with verifiable links to companies/projects
4. Value-First Approach: Shift focus to what you can do for them - map your skills to their pain points
5. Signal of Fit: Demonstrate adaptability and early-stage experience - show you thrive in chaos
6. Strong CTA: Ownership-focused closing - show you want to co-build, not just get a job

Key Principles:
- Make it feel 1:1, not mass-blasted
- Lead with energy and specificity
- Show, don't tell - link to verifiable work
- Think like a founder - solve their problems, not yours
- Make it frictionless to say yes
- Keep it conversational and founder-to-founder, not corporate
- Always sprinkle the URLs from socials in the body to build more credibility 
- Always maintain proper email formatting with clear paragraphs and structure

Tone Guidelines:
- Professional: Formal, business-like, respectful
- Friendly: Warm, approachable, conversational
- Confident: Assured, self-assured, positive
- Enthusiastic: Energetic, passionate, excited
- Authentic: Gritty, humble, founder-to-founder (preferred for startups)
- Conversational: Human, not recruiter-y, personal Gmail style

Remember: Each email should feel like it was written specifically for this job and company. The subject line should immediately grab attention and show relevant experience. The body should follow the viral cold email framework: TLDR hook → personalized compliment → credibility → value-first → fit signal → strong CTA. Make it feel like a founder-to-founder conversation, not a corporate application."""
        )
    
    async def generate_email(self, cv_data: Dict, job_data: Dict, email_type: str, 
                           tone: str, recipient_name: str = None, 
                           recipient_email: str = None) -> GeneratedEmail:
        """Generate personalized cold email"""
        try:
            # Convert Pydantic models to dictionaries if needed
            if hasattr(cv_data, 'model_dump'):
                cv_data_dict = cv_data.model_dump()
            else:
                cv_data_dict = cv_data
                
            if hasattr(job_data, 'model_dump'):
                job_data_dict = job_data.model_dump()
            else:
                job_data_dict = job_data
            
            # Create personalized prompt
            prompt = f"""Generate a personalized cold email for a {email_type} position.

CV DATA:
{json.dumps(cv_data_dict, indent=2)}

JOB DATA:
{json.dumps(job_data_dict, indent=2)}

EMAIL TYPE: {email_type}
TONE: {tone}
RECIPIENT NAME: {recipient_name or 'Hiring Manager'}
RECIPIENT EMAIL: {recipient_email or 'Not specified'}

INSTRUCTIONS:
- Create a highly personalized email using specific details from the CV and job
- Focus on quality over quantity, making every word count
- Match the candidate's skills and experience to the job requirements
- Use the specified tone throughout the email
- Follow the viral cold email framework: TLDR hook → personalized compliment → credibility → value-first → fit signal → strong CTA. Make it feel like a founder-to-founder conversation, not a corporate application.
- Make the email specific to this company and position
- Include relevant social links or portfolio if available in CV data (make sure to include the URLs in the body of the email)
- Create a clear call to action
- Keep the email professional and engaging

Please generate a personalized cold email."""

            result = await self.agent.run(
                prompt,
                deps=EmailGenerationInput(
                    cv_data=cv_data_dict,
                    job_data=job_data_dict,
                    email_type=email_type,
                    tone=tone,
                    recipient_name=recipient_name,
                    recipient_email=recipient_email
                )
            )
            
            return result.data
        except Exception as e:
            handle_groq_api_error(e, "email generation")
            return None


def test_smtp_connection(sender_email: str, sender_password: str, smtp_server: str = "smtp.gmail.com", 
                         smtp_port: int = 587) -> bool:
    """Test SMTP connection without sending an email"""
    try:
        st.info(f"🧪 Testing connection to {smtp_server}:{smtp_port}...")
        
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
        server.starttls()
        server.login(sender_email, sender_password)
        server.quit()
        
        st.success("✅ SMTP connection test successful!")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        st.error(f"❌ Authentication failed: {e}")
        st.info("💡 Make sure you're using an App Password, not your regular password")
        return False
    except Exception as e:
        st.error(f"❌ Connection test failed: {e}")
        return False


def send_email_via_smtp(sender_email: str, sender_password: str, recipient_email: str, 
                        subject: str, body: str, smtp_server: str = "smtp.gmail.com", 
                        smtp_port: int = 587) -> bool:
    """Send email via SMTP"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'plain'))
        
        # Create SMTP session with better error handling
        st.info(f"🔗 Connecting to {smtp_server}:{smtp_port}...")
        
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
        
        # Enable TLS
        st.info("🔒 Enabling TLS encryption...")
        server.starttls()
        
        # Login
        st.info("🔐 Authenticating...")
        server.login(sender_email, sender_password)
        
        # Send email
        st.info("📤 Sending email...")
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        
        # Close connection
        server.quit()
        
        st.success("✅ Email sent successfully!")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        st.error(f"❌ Authentication failed: {e}")
        st.info("💡 Make sure you're using an App Password, not your regular password")
        return False
    except smtplib.SMTPConnectError as e:
        st.error(f"❌ Connection failed: {e}")
        st.info("💡 Check your internet connection and SMTP server settings")
        return False
    except smtplib.SMTPRecipientsRefused as e:
        st.error(f"❌ Recipient email rejected: {e}")
        st.info("💡 Check the recipient email address")
        return False
    except smtplib.SMTPServerDisconnected as e:
        st.error(f"❌ Server disconnected: {e}")
        st.info("💡 Try again or check your email provider settings")
        return False
    except Exception as e:
        st.error(f"❌ Error sending email: {e}")
        st.info("💡 Check your email credentials and try again")
        return False


def create_email_generator_ui():
    """Create Streamlit UI for email generation"""
    st.title("📧 Cold Email Generator")
    st.write("Generate personalized cold emails using your CV data and job information")
    
    # Initialize vector store
    vector_store = get_vector_store()
    
    # Load data from vector store
    cv_data = vector_store.get_cv_data()
    job_data = vector_store.get_job_data()
    
    # Check if required data is available
    if not cv_data:
        st.warning("⚠️ Please extract your CV data first using the CV Extractor page.")
        st.info("💡 Navigate to 'CV Extractor' in the sidebar to get started")
        return None
    
    if not job_data:
        st.warning("⚠️ Please parse a job description first using the Job Parser page.")
        st.info("💡 Navigate to 'Job Parser' in the sidebar to parse a job")
        return None
    
    # Display success message
    st.success("✅ All data loaded successfully! Ready to generate personalized emails.")
    
    # Initialize components
    if 'email_generator' not in st.session_state:
        st.session_state.email_generator = EmailGeneratorAgent()
    
    if 'email_tracker' not in st.session_state:
        st.session_state.email_tracker = EmailTracker()
    
    # Initialize send email interface state
    if 'show_send_email' not in st.session_state:
        st.session_state.show_send_email = False
    
    # Display data summary
    st.subheader("📊 Data Summary")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**👤 Your Profile:**")
        # Handle both Pydantic model and dictionary for CV data
        if hasattr(cv_data, 'name'):
            # Pydantic model
            st.write(f"• Name: {cv_data.name}")
            st.write(f"• Skills: {', '.join(cv_data.skills[:5])}...")
            st.write(f"• Experience: {len(cv_data.experience)} positions")
            st.write(f"• Projects: {len(cv_data.projects)} projects")
        else:
            # Dictionary
            st.write(f"• Name: {cv_data.get('name', 'N/A')}")
            st.write(f"• Skills: {', '.join(cv_data.get('skills', [])[:5])}...")
            st.write(f"• Experience: {len(cv_data.get('experience', []))} positions")
            st.write(f"• Projects: {len(cv_data.get('projects', []))} projects")
    
    with col2:
        st.write("**💼 Target Job:**")
        # Handle both Pydantic model and dictionary for job data
        if hasattr(job_data, 'job_title'):
            # Pydantic model
            st.write(f"• Position: {job_data.job_title}")
            st.write(f"• Company: {job_data.company_name}")
            st.write(f"• Required Skills: {', '.join(job_data.required_skills[:5])}...")
            st.write(f"• Experience Level: {job_data.experience_level or 'Not specified'}")
        else:
            # Dictionary
            st.write(f"• Position: {job_data.get('job_title', 'N/A')}")
            st.write(f"• Company: {job_data.get('company_name', 'N/A')}")
            st.write(f"• Required Skills: {', '.join(job_data.get('required_skills', [])[:5])}...")
            st.write(f"• Experience Level: {job_data.get('experience_level', 'Not specified')}")
    
    # Email generation form
    st.subheader("📝 Email Generation Settings")
    
    # Email type selection
    email_type = st.selectbox(
        "Email Type",
        ["Industry Position", "Academic Research", "Freelance/Consulting", "Networking"],
        help="Choose the type of position you're applying for"
    )
    
    # Tone selection
    tone = st.selectbox(
        "Email Tone",
        ["Professional", "Friendly", "Confident", "Enthusiastic"],
        help="Choose the tone for your email"
    )
    
    # Recipient information
    col1, col2 = st.columns(2)
    with col1:
        recipient_name = st.text_input(
            "Recipient Name", 
            placeholder="John Smith",
            help="Hiring manager or recruiter name (optional)"
        )
    
    with col2:
        recipient_email = st.text_input(
            "Recipient Email",
            placeholder="john.smith@company.com",
            help="Recipient email address (optional)"
        )
    
    # Generate email button
    if st.button("🚀 Generate Personalized Email", type="primary", use_container_width=True):
        with st.spinner("Generating personalized email..."):
            import asyncio
            try:
                generated_email = asyncio.run(
                    st.session_state.email_generator.generate_email(
                        cv_data=cv_data,
                        job_data=job_data,
                        email_type=email_type,
                        tone=tone,
                        recipient_name=recipient_name,
                        recipient_email=recipient_email
                    )
                )
                
                if generated_email:
                    # Store generated email
                    st.session_state.current_email = generated_email
                    st.session_state.current_email_type = email_type
                    st.session_state.current_tone = tone
                    st.session_state.current_recipient_name = recipient_name
                    st.session_state.current_recipient_email = recipient_email
                    
                    # Display generated email
                    st.success("Email generated successfully!")
                    st.rerun()
                else:
                    st.error("Failed to generate email")
                    
            except Exception as e:
                st.error(f"Error during email generation: {e}")
    
    # Show message if no email has been generated yet
    if not st.session_state.get('current_email'):
        st.info("💡 Click 'Generate Personalized Email' above to create your first email")
    
    # Display generated email if it exists in session state
    if st.session_state.get('current_email'):
        generated_email = st.session_state.current_email
        email_type = st.session_state.get('current_email_type', 'Industry Position')
        tone = st.session_state.get('current_tone', 'Professional')
        recipient_name = st.session_state.get('current_recipient_name', '')
        recipient_email = st.session_state.get('current_recipient_email', '')
        
        # Email preview
        st.subheader("📧 Generated Email")
        
        # Subject line
        st.write(f"**Subject:** {generated_email.subject_line}")
        
        # Email content
        st.text_area(
            "Email Content",
            value=generated_email.full_email,
            height=400,
            help="Copy this email content to send"
        )
        
        # Personalization score
        st.metric("Personalization Score", f"{generated_email.personalization_score}/10")
        
        # Email sections breakdown
        with st.expander("📋 Email Breakdown"):
            st.write("**Greeting:**")
            st.write(generated_email.greeting)
            
            st.write("**Introduction:**")
            st.write(generated_email.introduction)
            
            st.write("**Body:**")
            st.write(generated_email.body)
            
            st.write("**Call to Action:**")
            st.write(generated_email.call_to_action)
            
            st.write("**Closing:**")
            st.write(generated_email.closing)
        
        # Email actions
        st.subheader("📤 Email Actions")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("📋 Copy Email", type="primary", key="copy_email_btn"):
                st.write("Email content copied to clipboard!")
                st.code(generated_email.full_email)
        
        with col2:
            if st.button("📥 Download Email", key="download_email_btn"):
                # Convert Pydantic models to dictionaries for JSON serialization
                cv_data_dict = cv_data.model_dump() if hasattr(cv_data, 'model_dump') else cv_data
                job_data_dict = job_data.model_dump() if hasattr(job_data, 'model_dump') else job_data
                
                email_data = {
                    "subject": generated_email.subject_line,
                    "content": generated_email.full_email,
                    "generated_at": datetime.now().isoformat(),
                    "cv_data_used": cv_data_dict,
                    "job_data_used": job_data_dict,
                    "email_type": email_type,
                    "tone": tone
                }
                st.download_button(
                    label="Download as JSON",
                    data=json.dumps(email_data, indent=2),
                    file_name=f"cold_email_{job_data.company_name if hasattr(job_data, 'company_name') else job_data.get('company_name', 'company')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col3:
            if st.button("📧 Mark as Sent", type="primary", key="mark_sent_btn"):
                # Convert Pydantic models to dictionaries for storage
                cv_data_dict = cv_data.model_dump() if hasattr(cv_data, 'model_dump') else cv_data
                job_data_dict = job_data.model_dump() if hasattr(job_data, 'model_dump') else job_data
                
                # Create email record
                email_record = EmailRecord(
                    id=str(uuid.uuid4()),
                    job_title=job_data.job_title if hasattr(job_data, 'job_title') else job_data.get('job_title', ''),
                    company_name=job_data.company_name if hasattr(job_data, 'company_name') else job_data.get('company_name', ''),
                    recipient_email=recipient_email,
                    recipient_name=recipient_name,
                    sent_date=datetime.now(),
                    email_type=email_type,
                    status="sent",
                    cv_data_used=cv_data_dict,
                    job_data_used=job_data_dict,
                    email_content=generated_email.full_email,
                    notes=f"Generated with {tone} tone"
                )
                
                # Add to tracker
                st.session_state.email_tracker.add_record(email_record)
                
                # Store in vector database
                vector_store.store_email_record(email_record.model_dump())
                
                st.success("✅ Email marked as sent and tracked!")
        
        with col4:
            if st.button("📤 Send Email", type="primary", key="send_email_btn"):
                st.session_state.show_send_email = True
                st.rerun()
            
            # Show hint if send email interface is not visible
            if not st.session_state.show_send_email:
                st.info("💡 Click 'Send Email' to configure SMTP and send directly")
            else:
                st.success("✅ Send email interface is active")
        
        with col5:
            if st.button("🗑️ Clear Email", type="secondary", key="clear_email_btn"):
                # Clear all email-related session state
                if 'current_email' in st.session_state:
                    del st.session_state.current_email
                if 'current_email_type' in st.session_state:
                    del st.session_state.current_email_type
                if 'current_tone' in st.session_state:
                    del st.session_state.current_tone
                if 'current_recipient_name' in st.session_state:
                    del st.session_state.current_recipient_name
                if 'current_recipient_email' in st.session_state:
                    del st.session_state.current_recipient_email
                if 'show_send_email' in st.session_state:
                    st.session_state.show_send_email = False
                st.rerun()
        
        # Debug information (only show if there are issues)
        if st.checkbox("🐛 Show Debug Info", key="debug_checkbox"):
            st.write("**Debug Information:**")
            st.write(f"• show_send_email: {st.session_state.show_send_email}")
            st.write(f"• current_email exists: {st.session_state.get('current_email') is not None}")
            st.write(f"• email_tracker exists: {st.session_state.get('email_tracker') is not None}")
        
        # Email sending interface
        if st.session_state.show_send_email:
            st.subheader("📤 Send Email via SMTP")
            
            # Check if email credentials are configured
            if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
                st.error("❌ Email credentials not configured!")
                st.info("""
                Please add your email credentials to the .env file:
                
                ```
                EMAIL_ADDRESS=your.email@gmail.com
                EMAIL_PASSWORD=your_app_password
                SENDER_NAME=Your Name
                ```
                
                Then restart the application.
                """)
                return
            
            st.success(f"✅ Using configured email: {EMAIL_ADDRESS}")
            
            # Quick setup guide
            with st.expander("📋 Quick Setup Guide", expanded=False):
                st.write("""
                **For Gmail:**
                1. Enable 2-factor authentication
                2. Generate an App Password (Google Account → Security → App Passwords)
                3. Use your Gmail address and the app password (not your regular password)
                
                **For Outlook/Office365:**
                1. Enable 2-factor authentication
                2. Generate an App Password (Account Settings → Security → App Passwords)
                3. Use your Outlook email and the app password
                
                **For Yahoo:**
                1. Enable 2-factor authentication
                2. Generate an App Password (Account Security → App Passwords)
                3. Use your Yahoo email and the app password
                """)
            
            # SMTP Configuration (read-only since using env vars)
            with st.expander("⚙️ SMTP Configuration", expanded=True):
                st.write("**Step 1: Email provider settings (configured via environment variables)**")
                st.write("---")
                col1, col2 = st.columns(2)
                with col1:
                    smtp_server = st.selectbox(
                        "SMTP Server",
                        ["smtp.gmail.com", "smtp.outlook.com", "smtp.yahoo.com", "smtp.office365.com"],
                        help="Choose your email provider's SMTP server",
                        key="smtp_server_select"
                    )
                    smtp_port = st.number_input(
                        "SMTP Port",
                        value=587,
                        min_value=25,
                        max_value=587,
                        help="SMTP port (usually 587 for TLS)",
                        key="smtp_port_input"
                    )
                
                with col2:
                    st.text_input(
                        "Your Email Address",
                        value=EMAIL_ADDRESS,
                        disabled=True,
                        help="Configured via EMAIL_ADDRESS environment variable"
                    )
                    st.text_input(
                        "App Password",
                        value="••••••••••••••••" if EMAIL_PASSWORD else "",
                        disabled=True,
                        help="Configured via EMAIL_PASSWORD environment variable"
                    )
                
                # Test connection button
                if st.button("🧪 Test Connection", type="secondary", key="test_connection_btn"):
                    test_smtp_connection(EMAIL_ADDRESS, EMAIL_PASSWORD, smtp_server, smtp_port)
            
            # Email preview
            st.subheader("📧 Email Preview")
            st.write("**Step 2: Review your email before sending**")
            st.write("---")
            st.write(f"**From:** {SENDER_NAME} <{EMAIL_ADDRESS}>")
            st.write(f"**To:** {recipient_email or 'Not specified'}")
            st.write(f"**Subject:** {generated_email.subject_line}")
            st.write("**Content:**")
            st.text_area(
                "Email Content",
                value=generated_email.full_email,
                height=300,
                disabled=True,
                key="email_preview_area"
            )
            
            # Send button
            st.write("**Step 3: Send your email**")
            st.write("---")
            if st.button("🚀 Send Email Now", type="primary", use_container_width=True, key="send_email_now_btn"):
                if not recipient_email:
                    st.error("❌ Please specify a recipient email address")
                else:
                    with st.spinner("Sending email..."):
                        try:
                            success = send_email_via_smtp(
                                sender_email=EMAIL_ADDRESS,
                                sender_password=EMAIL_PASSWORD,
                                recipient_email=recipient_email,
                                subject=generated_email.subject_line,
                                body=generated_email.full_email,
                                smtp_server=smtp_server,
                                smtp_port=smtp_port
                            )
                            
                            if success:
                                st.success("✅ Email sent successfully!")
                                
                                # Create email record
                                cv_data_dict = cv_data.model_dump() if hasattr(cv_data, 'model_dump') else cv_data
                                job_data_dict = job_data.model_dump() if hasattr(job_data, 'model_dump') else job_data
                                
                                email_record = EmailRecord(
                                    id=str(uuid.uuid4()),
                                    job_title=job_data.job_title if hasattr(job_data, 'job_title') else job_data.get('job_title', ''),
                                    company_name=job_data.company_name if hasattr(job_data, 'company_name') else job_data.get('company_name', ''),
                                    recipient_email=recipient_email,
                                    recipient_name=recipient_name,
                                    sent_date=datetime.now(),
                                    email_type=email_type,
                                    status="delivered",
                                    cv_data_used=cv_data_dict,
                                    job_data_used=job_data_dict,
                                    email_content=generated_email.full_email,
                                    notes=f"Sent via SMTP with {tone} tone"
                                )
                                
                                # Add to tracker
                                st.session_state.email_tracker.add_record(email_record)
                                
                                # Store in vector database
                                vector_store.store_email_record(email_record.model_dump())
                                
                                # Hide the send interface
                                st.session_state.show_send_email = False
                                st.rerun()
                            else:
                                st.error("❌ Failed to send email. Please check your credentials and try again.")
                        except Exception as e:
                            st.error(f"❌ Error sending email: {str(e)}")
                            st.info("💡 Common issues: Check your app password, enable 2FA, or try a different SMTP server")
            
            # Cancel button
            if st.button("❌ Cancel", use_container_width=True, key="cancel_send_btn"):
                st.session_state.show_send_email = False
                st.rerun()
                
    # Email tracking section
    st.subheader("📊 Email Tracking")
    
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
    
    # Navigation hint
    st.info("💡 Use the sidebar to navigate between different pages and manage your data")
    
    return st.session_state.get('current_email')


if __name__ == "__main__":
    create_email_generator_ui() 