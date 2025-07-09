#!/usr/bin/env python3
"""
Test script for job scraper functionality
"""

import asyncio
from job_parser import JobScraper, JobParserAgent
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables for local development
load_dotenv()

def test_scraper():
    """Test the job scraper with a sample URL"""
    print("🧪 Testing Job Scraper...")
    
    # Initialize scraper
    scraper = JobScraper()
    
    # Test URL validation
    test_urls = [
        "https://www.linkedin.com/jobs/view/123456",
        "https://indeed.com/viewjob?jk=123456",
        "https://glassdoor.com/Job/jobs.htm?sc.keyword=software+engineer",
        "https://example.com/not-a-job-site",
        "invalid-url"
    ]
    
    print("\n🔍 Testing URL validation:")
    for url in test_urls:
        is_valid = scraper._is_valid_job_url(url)
        print(f"  {url}: {'✅ Valid' if is_valid else '❌ Invalid'}")
    
    # Test with a real job posting URL (you can replace this with an actual URL)
    print("\n🌐 Testing job extraction:")
    test_url = "https://www.linkedin.com/jobs/view/software-engineer-at-google-123456"
    
    try:
        print(f"  🔍 Processing URL: {test_url}")
        job_info = scraper.extract_job_info_from_url(test_url)
        
        if "error" in job_info:
            print(f"  ❌ Error: {job_info['error']}")
        else:
            print(f"  ✅ Job Title: {job_info['job_title']}")
            print(f"  ✅ Company: {job_info['company_name']}")
            print(f"  ✅ Description Length: {len(job_info['job_description'])} characters")
            
            # Show first 200 characters of description
            desc_preview = job_info['job_description'][:200] + "..." if len(job_info['job_description']) > 200 else job_info['job_description']
            print(f"  📝 Description Preview: {desc_preview}")
            
            # Check if description seems valid
            if len(job_info['job_description']) < 50:
                print("  ⚠️  Warning: Job description seems too short")
            elif len(job_info['job_description']) > 1000:
                print("  ✅ Job description length looks good")
            else:
                print("  ℹ️  Job description length is moderate")
                
    except Exception as e:
        print(f"  ❌ Exception: {e}")
        import traceback
        print(f"  📋 Full traceback:")
        traceback.print_exc()
    
    print("\n✅ Scraper test completed!")

def test_parser():
    """Test the job parser with sample data"""
    print("\n🧪 Testing Job Parser...")
    
    # Sample job description
    sample_job_description = """
    Senior Software Engineer
    
    Company: TechCorp Inc.
    Location: San Francisco, CA (Hybrid)
    
    We are looking for a Senior Software Engineer to join our team.
    
    Requirements:
    - 5+ years of experience in software development
    - Proficiency in Python, JavaScript, and React
    - Experience with cloud platforms (AWS, Azure)
    - Strong problem-solving skills
    
    Preferred Skills:
    - Docker and Kubernetes
    - Machine Learning experience
    - Agile development methodologies
    
    Responsibilities:
    - Develop and maintain web applications
    - Collaborate with cross-functional teams
    - Code review and mentoring junior developers
    - Participate in technical architecture decisions
    
    Benefits:
    - Competitive salary
    - Health insurance
    - 401k matching
    - Flexible work arrangements
    
    Salary Range: $120,000 - $150,000
    """
    
    try:
        # Initialize parser
        parser = JobParserAgent()
        
        # Parse the sample job description
        print("  🔍 Parsing sample job description...")
        job_data = asyncio.run(parser.parse_job_description(sample_job_description))
        
        if job_data:
            print(f"  ✅ Job Title: {job_data.job_title}")
            print(f"  ✅ Company: {job_data.company_name}")
            print(f"  ✅ Location: {job_data.location}")
            print(f"  ✅ Required Skills: {len(job_data.required_skills)} skills")
            print(f"  ✅ Preferred Skills: {len(job_data.preferred_skills)} skills")
            print(f"  ✅ Responsibilities: {len(job_data.responsibilities)} items")
            print(f"  ✅ Benefits: {len(job_data.benefits)} benefits")
            print(f"  ✅ Salary Range: {job_data.salary_range}")
        else:
            print("  ❌ Failed to parse job description")
            
    except Exception as e:
        print(f"  ❌ Exception: {e}")
    
    print("\n✅ Parser test completed!")

def main():
    """Run all tests"""
    print("🚀 Starting Job Parser Tests...")
    
    # Check if API key is available
    groq_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("⚠️  GROQ_API_KEY not found. Some tests may fail.")
        print("   Please set your API key in Streamlit secrets or .env file")
    
    # Run tests
    test_scraper()
    test_parser()
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    main() 