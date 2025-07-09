#!/usr/bin/env python3
"""
Test runner script
This script helps you run the correct test commands
"""

import subprocess
import sys
import os

def run_test(test_name):
    """Run a specific test"""
    test_scripts_dir = "test_scripts"
    
    if test_name == "email":
        script_path = os.path.join(test_scripts_dir, "test_email_functionality.py")
        if os.path.exists(script_path):
            print("🧪 Running email functionality test...")
            subprocess.run([sys.executable, "-m", "streamlit", "run", script_path])
        else:
            print(f"❌ Test script not found: {script_path}")
    
    elif test_name == "scraper":
        script_path = os.path.join(test_scripts_dir, "test_scraper.py")
        if os.path.exists(script_path):
            print("🌐 Running web scraper test...")
            subprocess.run([sys.executable, script_path])
        else:
            print(f"❌ Test script not found: {script_path}")
    
    elif test_name == "cv":
        script_path = os.path.join(test_scripts_dir, "test_cv_extractor.py")
        if os.path.exists(script_path):
            print("📄 Running CV extractor test...")
            subprocess.run([sys.executable, script_path])
        else:
            print(f"❌ Test script not found: {script_path}")
    
    elif test_name == "setup":
        script_path = os.path.join(test_scripts_dir, "test_setup.py")
        if os.path.exists(script_path):
            print("⚙️ Running setup test...")
            subprocess.run([sys.executable, script_path])
        else:
            print(f"❌ Test script not found: {script_path}")
    
    elif test_name == "email_config":
        script_path = "check_email_config.py"
        if os.path.exists(script_path):
            print("📧 Checking email configuration...")
            subprocess.run([sys.executable, script_path])
        else:
            print(f"❌ Email config checker not found: {script_path}")
    
    else:
        print(f"❌ Unknown test: {test_name}")
        print_help()

def print_help():
    """Print help information"""
    print("""
🧪 Test Runner for Cold Email Generator

Usage: python run_tests.py [test_name]

Available tests:
  email        - Test email functionality (SMTP, sending)
  scraper      - Test web scraping functionality
  cv           - Test CV extraction functionality
  setup        - Test environment setup
  email_config - Check email configuration

Examples:
  python run_tests.py email
  python run_tests.py scraper
  python run_tests.py cv
  python run_tests.py setup
  python run_tests.py email_config
    """)

def main():
    if len(sys.argv) != 2:
        print_help()
        return
    
    test_name = sys.argv[1].lower()
    run_test(test_name)

if __name__ == "__main__":
    main() 