#!/usr/bin/env python3
"""
Test script specifically for link extraction functionality
"""

from cv_extractor import extract_links_from_text, extract_keyword_from_context

def test_link_extraction():
    """Test link extraction with various patterns"""
    print("🧪 Testing Link Extraction")
    print("=" * 50)
    
    # Test cases with different patterns
    test_cases = [
        "GitHub: https://github.com/johnsmith",
        "LinkedIn - https://linkedin.com/in/johnsmith",
        "Portfolio=https://johnsmith.dev",
        "Blog | https://johnsmith.medium.com",
        "Project Repository: https://github.com/johnsmith/project",
        "Twitter: https://twitter.com/johnsmith",
        "Stack Overflow: https://stackoverflow.com/users/johnsmith",
        "Medium: https://medium.com/@johnsmith/article",
        "GitLab: https://gitlab.com/johnsmith/repo",
        "Dev.to: https://dev.to/johnsmith/post",
        "Just a plain URL: https://example.com",
        "No label https://github.com/johnsmith",
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case}")
        links = extract_links_from_text(test_case)
        
        if links:
            for key, url in links.items():
                print(f"  ✅ Extracted: {key} -> {url}")
        else:
            print(f"  ❌ No links extracted")
    
    print("\n" + "=" * 50)
    print("Link extraction test completed!")

def test_keyword_extraction():
    """Test keyword extraction from context"""
    print("\n🔍 Testing Keyword Extraction")
    print("=" * 50)
    
    test_contexts = [
        ("GitHub: https://github.com/user", 8),
        ("LinkedIn - https://linkedin.com/in/user", 12),
        ("Portfolio=https://example.com", 10),
        ("Blog | https://medium.com/user", 6),
        ("Project Repository: https://github.com/user/repo", 20),
        ("No label https://github.com/user", 9),
    ]
    
    for context, url_pos in test_contexts:
        keyword = extract_keyword_from_context(context, url_pos)
        print(f"Context: '{context}'")
        print(f"Keyword: {keyword}")
        print()

if __name__ == "__main__":
    test_link_extraction()
    test_keyword_extraction() 