#!/usr/bin/env python3
"""
Debug script for job scraper functionality
"""

import os
import sys
import streamlit as st
from dotenv import load_dotenv

# Load environment variables for local development
load_dotenv()

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from job_parser import JobScraper, JobParserAgent
import asyncio

def debug_scraper():
    """Debug the job scraper functionality"""
    print("🔍 Debugging Job Scraper...")
    
    # Test URL - you can replace this with a real job posting URL
    test_url = "https://www.linkedin.com/jobs/view/software-engineer-at-google-123456"
    
    print(f"Testing URL: {test_url}")
    
    # Initialize scraper
    scraper = JobScraper()
    
    # Test URL validation
    is_valid = scraper._is_valid_job_url(test_url)
    print(f"URL Valid: {is_valid}")
    
    if not is_valid:
        print("❌ URL validation failed")
        return
    
    # Test scraping
    try:
        print("🔍 Extracting job info...")
        job_info = scraper.extract_job_info_from_url(test_url)
        
        if "error" in job_info:
            print(f"❌ Scraping error: {job_info['error']}")
            return
        
        print("✅ Scraping successful!")
        print(f"Job Title: {job_info.get('job_title', 'Not found')}")
        print(f"Company: {job_info.get('company_name', 'Not found')}")
        print(f"Description Length: {len(job_info.get('job_description', ''))} characters")
        
        # Show description preview
        desc = job_info.get('job_description', '')
        if desc:
            preview = desc[:300] + "..." if len(desc) > 300 else desc
            print(f"Description Preview: {preview}")
        
        # Test parsing if we have a description
        if desc and len(desc) > 50:
            print("\n🤖 Testing AI parsing...")
            parser = JobParserAgent()
            
            try:
                job_data = asyncio.run(parser.parse_job_description(desc))
                if job_data:
                    print("✅ AI parsing successful!")
                    print(f"Parsed Job Title: {job_data.job_title}")
                    print(f"Parsed Company: {job_data.company_name}")
                    print(f"Required Skills: {len(job_data.required_skills)}")
                    print(f"Responsibilities: {len(job_data.responsibilities)}")
                else:
                    print("❌ AI parsing failed")
            except Exception as e:
                print(f"❌ AI parsing error: {e}")
        else:
            print("⚠️  Description too short for AI parsing")
            
    except Exception as e:
        print(f"❌ Exception during scraping: {e}")
        import traceback
        traceback.print_exc()

def test_real_url():
    """Test with a real job posting URL"""
    print("\n🌐 Testing with real URL...")
    
    # You can replace this with an actual job posting URL
    real_url = input("Enter a real job posting URL to test (or press Enter to skip): ").strip()
    
    if not real_url:
        print("Skipping real URL test")
        return
    
    scraper = JobScraper()
    
    try:
        print(f"Testing: {real_url}")
        job_info = scraper.extract_job_info_from_url(real_url)
        
        if "error" in job_info:
            print(f"❌ Error: {job_info['error']}")
        else:
            print("✅ Success!")
            print(f"Title: {job_info.get('job_title')}")
            print(f"Company: {job_info.get('company_name')}")
            print(f"Description Length: {len(job_info.get('job_description', ''))}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    print("🚀 Job Scraper Debug Tool")
    print("=" * 50)
    
    # Check environment
    groq_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("⚠️  GROQ_API_KEY not found. AI parsing will not work.")
        print("   Please set your API key in Streamlit secrets or .env file")
    
    debug_scraper()
    test_real_url()
    
    print("\n✅ Debug completed!") 