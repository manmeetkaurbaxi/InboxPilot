#!/usr/bin/env python3
"""
Test script to verify the setup and dependencies
"""

import sys
import os
from dotenv import load_dotenv

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    
    try:
        import streamlit
        print("✅ streamlit imported successfully")
    except ImportError as e:
        print(f"❌ streamlit import failed: {e}")
        return False
    
    try:
        import PyPDF2
        print("✅ PyPDF2 imported successfully")
    except ImportError as e:
        print(f"❌ PyPDF2 import failed: {e}")
        return False
    
    try:
        import pydantic
        print("✅ pydantic imported successfully")
    except ImportError as e:
        print(f"❌ pydantic import failed: {e}")
        return False
    
    try:
        import pydantic_ai
        print("✅ pydantic_ai imported successfully")
    except ImportError as e:
        print(f"❌ pydantic_ai import failed: {e}")
        return False
    
    try:
        import groq
        print("✅ groq imported successfully")
    except ImportError as e:
        print(f"❌ groq import failed: {e}")
        return False
    
    return True

def test_env_vars():
    """Test if environment variables are set"""
    print("\nTesting environment variables...")
    
    try:
        from config import validate_config, get_model_info
        validate_config()
        model_info = get_model_info()
        print("✅ GROQ_API_KEY is set")
        print(f"✅ Using model: {model_info['model']}")
        return True
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_cv_extractor():
    """Test if CV extractor can be imported"""
    print("\nTesting CV extractor...")
    
    try:
        from cv_extractor import extract_text_from_pdf, CVExtractionResult
        print("✅ CV extractor imported successfully")
        return True
    except ImportError as e:
        print(f"❌ CV extractor import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing CV Extractor Setup")
    print("=" * 40)
    
    all_tests_passed = True
    
    # Test imports
    if not test_imports():
        all_tests_passed = False
    
    # Test environment variables
    if not test_env_vars():
        all_tests_passed = False
    
    # Test CV extractor
    if not test_cv_extractor():
        all_tests_passed = False
    
    print("\n" + "=" * 40)
    if all_tests_passed:
        print("🎉 All tests passed! You're ready to run the application.")
        print("\nTo start the application, run:")
        print("streamlit run main.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\nTo install dependencies, run:")
        print("pip install -r requirements.txt")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 