import streamlit as st
import asyncio
import os
from config import GROQ_API_KEY, get_model_info
from cv_extractor import create_cv_extraction_ui
from job_parser import create_job_parser_ui
from email_generator import create_email_generator_ui
from vector_store import get_vector_store

# Configure page
st.set_page_config(
    page_title="CV Extractor & Cold Email Generator",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to make primary buttons green
st.markdown("""
<style>
    /* Target Streamlit primary buttons specifically */
    .stButton > button[kind="primary"] {
        background-color: #28a745 !important;
        color: white !important;
        border-color: #28a745 !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #218838 !important;
        border-color: #1e7e34 !important;
    }
    .stButton > button[kind="primary"]:active {
        background-color: #1e7e34 !important;
        border-color: #1c7430 !important;
    }
    
    /* Alternative selector for primary buttons */
    .stButton > button[data-testid="baseButton-primary"] {
        background-color: #28a745 !important;
        color: white !important;
        border-color: #28a745 !important;
    }
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background-color: #218838 !important;
        border-color: #1e7e34 !important;
    }
    .stButton > button[data-testid="baseButton-primary"]:active {
        background-color: #1e7e34 !important;
        border-color: #1c7430 !important;
    }
</style>
""", unsafe_allow_html=True)

# Check for API key
def check_api_key():
    if not GROQ_API_KEY:
        st.error("⚠️ GROQ_API_KEY not found in environment variables!")
        st.info("Please create a .env file with your GROQ_API_KEY")
        st.code("GROQ_API_KEY=your_api_key_here")
        return False
    return True

def main():
    # Check API key
    if not check_api_key():
        return
    
    # Initialize vector store
    vector_store = get_vector_store()
    
    # Sidebar navigation
    st.sidebar.title("Personalized Cold Email Generator")
    
    # Check data availability for navigation hints
    cv_data = vector_store.get_cv_data()
    job_data = vector_store.get_job_data()
    
    # Navigation with status indicators
    page = st.sidebar.selectbox(
        "Choose a page",
        ["CV Extractor", "Job Parser", "Email Generator"]
    )
    
    # Show data status in sidebar
    st.sidebar.subheader("📊 Data Status")
    
    if cv_data:
        st.sidebar.success("✅ CV Data Available")
        with st.sidebar.expander("CV Summary"):
            st.write(f"**Name:** {cv_data.get('name', 'N/A')}")
            st.write(f"**Skills:** {len(cv_data.get('skills', []))} skills")
            st.write(f"**Experience:** {len(cv_data.get('experience', []))} positions")
    else:
        st.sidebar.warning("⚠️ No CV Data")
    
    if job_data:
        st.sidebar.success("✅ Job Data Available")
        with st.sidebar.expander("Job Summary"):
            # Handle both Pydantic model and dictionary
            if hasattr(job_data, 'job_title'):
                # Pydantic model
                st.write(f"**Position:** {job_data.job_title}")
                st.write(f"**Company:** {job_data.company_name}")
                st.write(f"**Skills:** {len(job_data.required_skills)} required")
            else:
                # Dictionary
                st.write(f"**Position:** {job_data.get('job_title', 'N/A')}")
                st.write(f"**Company:** {job_data.get('company_name', 'N/A')}")
                st.write(f"**Skills:** {len(job_data.get('required_skills', []))} required")
    else:
        st.sidebar.warning("⚠️ No Job Data")
    
    # Show workflow progress
    st.sidebar.subheader("🔄 Workflow Progress")
    steps = [
        ("CV Extractor", cv_data is not None),
        ("Job Parser", job_data is not None),
        ("Email Generator", cv_data is not None and job_data is not None)
    ]
    
    for step_name, completed in steps:
        if completed:
            st.sidebar.success(f"✅ {step_name}")
        else:
            st.sidebar.info(f"⏳ {step_name}")
    
    # Quick actions
    st.sidebar.subheader("⚡ Quick Actions")
    
    if cv_data and job_data:
        if st.sidebar.button("🚀 Generate Email Now", type="primary"):
            st.session_state.auto_navigate = "Email Generator"
            st.rerun()
    
    if st.sidebar.button("🗑️ Clear All Data", type="primary"):
        vector_store.clear_user_data()
        st.rerun()
    
    # Auto-navigation
    if st.session_state.get('auto_navigate'):
        page = st.session_state.auto_navigate
        del st.session_state.auto_navigate
    
    if page == "CV Extractor":
        # Use the updated CV extraction UI
        cv_data, manual_links = create_cv_extraction_ui()
        
        # Store in session state for use in other pages
        if cv_data:
            st.session_state.cv_data = cv_data
        if manual_links:
            st.session_state.manual_links = manual_links
    
    elif page == "Job Parser":
        # Use the job parser UI
        job_data = create_job_parser_ui()
        
        # Store in session state for use in other pages
        if job_data:
            st.session_state.current_job_data = job_data
    
    elif page == "Email Generator":
        # Use the email generator UI
        generated_email = create_email_generator_ui()
        
        # Store in session state
        if generated_email:
            st.session_state.current_email = generated_email
    


if __name__ == "__main__":
    main() 