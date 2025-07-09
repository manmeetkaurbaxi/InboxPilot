#!/usr/bin/env python3
"""
Test script for CV extraction functionality
"""

import asyncio
import json
from cv_extractor import (
    CVExtractionResult, 
    extract_text_from_pdf, 
    extract_cv_data,
    create_manual_links_section
)
import io
from PyPDF2 import PdfWriter, PdfReader


def create_test_pdf():
    """Create a test PDF with sample CV content"""
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    
    # Create a PDF in memory
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    
    # Add test CV content
    can.drawString(100, 750, "John Smith")
    can.drawString(100, 730, "john.smith@email.com")
    can.drawString(100, 710, "Software Engineer")
    can.drawString(100, 690, "EDUCATION:")
    can.drawString(100, 670, "Bachelor of Science in Computer Science, University of Technology, 2020-2024, GPA: 3.8")
    can.drawString(100, 650, "EXPERIENCE:")
    can.drawString(100, 630, "Software Developer at Tech Corp, 2022-2024")
    can.drawString(100, 610, "SKILLS:")
    can.drawString(100, 590, "Python, JavaScript, React, Node.js")
    can.drawString(100, 570, "PROJECTS:")
    can.drawString(100, 550, "E-commerce Platform, 2023")
    can.drawString(100, 530, "AWARDS:")
    can.drawString(100, 510, "Dean's List, 2023")
    can.drawString(100, 490, "PUBLICATIONS:")
    can.drawString(100, 470, "Machine Learning in Web Applications, 2023")
    can.drawString(100, 450, "VOLUNTEER:")
    can.drawString(100, 430, "Code Mentor at Local High School, 2022-2023")
    can.drawString(100, 410, "SUMMARY:")
    can.drawString(100, 390, "Passionate software engineer with expertise in full-stack development")
    
    can.save()
    
    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    return packet


def test_cv_extraction_result():
    """Test CVExtractionResult model"""
    print("Testing CVExtractionResult model...")
    
    # Test basic creation
    cv_data = CVExtractionResult(
        name="John Smith",
        email="john@example.com",
        phone="123-456-7890",
        education=["Bachelor of Science, University of Technology, 2020-2024, GPA: 3.8"],
        experience=["Software Developer at Tech Corp, 2022-2024"],
        volunteer=["Code Mentor at Local High School, 2022-2023"],
        skills=["Python", "JavaScript", "React"],
        projects=["E-commerce Platform, 2023"],
        awards=["Dean's List, 2023"],
        publications=["Machine Learning in Web Applications, 2023"],
        summary="Passionate software engineer"
    )
    
    # Test sorting by year
    cv_data.sort_by_year()
    
    # Test validation
    is_valid, message = cv_data.validate_extraction()
    assert is_valid, f"Validation failed: {message}"
    
    print("✅ CVExtractionResult model tests passed")


def test_text_extraction():
    """Test PDF text extraction"""
    print("Testing PDF text extraction...")
    
    # Create test PDF
    pdf_buffer = create_test_pdf()
    
    # Test text extraction
    text = extract_text_from_pdf(pdf_buffer)
    
    assert text is not None, "Text extraction failed"
    assert "John Smith" in text, "Name not found in extracted text"
    assert "john.smith@email.com" in text, "Email not found in extracted text"
    assert "Software Engineer" in text, "Title not found in extracted text"
    
    print("✅ PDF text extraction tests passed")


async def test_cv_data_extraction():
    """Test CV data extraction with AI"""
    print("Testing CV data extraction with AI...")
    
    # Create test PDF
    pdf_buffer = create_test_pdf()
    
    # Extract text
    text = extract_text_from_pdf(pdf_buffer)
    
    # Extract structured data
    cv_data = await extract_cv_data(text)
    
    assert cv_data is not None, "CV data extraction failed"
    assert cv_data.name == "John Smith", f"Name extraction failed: got {cv_data.name}"
    assert cv_data.email == "john.smith@email.com", f"Email extraction failed: got {cv_data.email}"
    assert len(cv_data.education) > 0, "Education extraction failed"
    assert len(cv_data.experience) > 0, "Experience extraction failed"
    assert len(cv_data.skills) > 0, "Skills extraction failed"
    assert len(cv_data.volunteer) > 0, "Volunteer extraction failed"
    assert len(cv_data.awards) > 0, "Awards extraction failed"
    assert len(cv_data.publications) > 0, "Publications extraction failed"
    
    # Test validation
    is_valid, message = cv_data.validate_extraction()
    assert is_valid, f"Validation failed: {message}"
    
    print("✅ CV data extraction tests passed")


def test_placeholder_detection():
    """Test placeholder data detection"""
    print("Testing placeholder data detection...")
    
    # Test with placeholder data
    placeholder_cv = CVExtractionResult(
        name="John Doe",
        email="john.doe@example.com",
        phone="",
        education=[],
        experience=[],
        volunteer=[],
        skills=[],
        projects=[],
        awards=[],
        publications=[],
        summary=""
    )
    
    is_valid, message = placeholder_cv.validate_extraction()
    assert not is_valid, "Placeholder detection failed"
    assert "placeholder" in message.lower(), "Placeholder message not found"
    
    print("✅ Placeholder detection tests passed")


def test_year_sorting():
    """Test year-based sorting functionality"""
    print("Testing year-based sorting...")
    
    cv_data = CVExtractionResult(
        name="Test User",
        email="test@example.com",
        phone="",
        education=[
            "Bachelor's Degree, University A, 2018-2022",
            "Master's Degree, University B, 2022-2024"
        ],
        experience=[
            "Junior Developer, Company A, 2020-2022",
            "Senior Developer, Company B, 2022-2024",
            "Intern, Company C, 2019-2020"
        ],
        volunteer=[
            "Mentor, Organization A, 2021-2023",
            "Volunteer, Organization B, 2019-2021"
        ],
        skills=["Python", "JavaScript"],
        projects=[
            "Project A, 2023",
            "Project B, 2021",
            "Project C, 2024"
        ],
        awards=[
            "Award A, 2023",
            "Award B, 2020",
            "Award C, 2024"
        ],
        publications=[
            "Paper A, 2022",
            "Paper B, 2024",
            "Paper C, 2021"
        ],
        summary="Test summary"
    )
    
    # Sort by year
    cv_data.sort_by_year()
    
    # Check that items are sorted by year (latest first)
    assert "2024" in cv_data.education[0], "Education not sorted correctly"
    assert "2024" in cv_data.experience[0], "Experience not sorted correctly"
    assert "2023" in cv_data.volunteer[0], "Volunteer not sorted correctly"
    assert "2024" in cv_data.projects[0], "Projects not sorted correctly"
    assert "2024" in cv_data.awards[0], "Awards not sorted correctly"
    assert "2024" in cv_data.publications[0], "Publications not sorted correctly"
    
    print("✅ Year sorting tests passed")


def test_manual_links_structure():
    """Test manual links data structure"""
    print("Testing manual links structure...")
    
    # Simulate manual links input
    manual_links = {
        "LinkedIn": "https://linkedin.com/in/johndoe",
        "GitHub": "https://github.com/johndoe",
        "Twitter": "https://twitter.com/johndoe",
        "Portfolio": "https://johndoe.dev",
        "GitHub Repo 1": "https://github.com/johndoe/project1",
        "GitHub Repo 2": "https://github.com/johndoe/project2"
    }
    
    # Test structure
    assert "LinkedIn" in manual_links, "LinkedIn link missing"
    assert "GitHub" in manual_links, "GitHub link missing"
    assert "GitHub Repo 1" in manual_links, "GitHub repository missing"
    
    # Test URL format
    for label, url in manual_links.items():
        assert url.startswith("http"), f"Invalid URL format for {label}: {url}"
    
    print("✅ Manual links structure tests passed")


async def main():
    """Run all tests"""
    print("🧪 Running CV Extractor Tests...\n")
    
    try:
        # Run tests
        test_cv_extraction_result()
        test_text_extraction()
        await test_cv_data_extraction()
        test_placeholder_detection()
        test_year_sorting()
        test_manual_links_structure()
        
        print("\n🎉 All tests passed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main()) 