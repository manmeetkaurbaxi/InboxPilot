#!/usr/bin/env python3
"""
Email Configuration Checker
Verify that your email settings are configured correctly
"""

import os
from dotenv import load_dotenv
import smtplib

def check_email_config():
    """Check if email configuration is properly set up"""
    print("🔍 Checking Email Configuration")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Check required variables
    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")
    sender_name = os.getenv("SENDER_NAME", "Your Name")
    
    print(f"📧 Email Address: {'✅ Set' if email_address else '❌ Not set'}")
    if email_address:
        print(f"   Value: {email_address}")
    
    print(f"🔑 Email Password: {'✅ Set' if email_password else '❌ Not set'}")
    if email_password:
        print(f"   Value: {'••••••••••••••••' if len(email_password) > 0 else 'Empty'}")
    
    print(f"👤 Sender Name: {'✅ Set' if sender_name else '❌ Not set'}")
    if sender_name:
        print(f"   Value: {sender_name}")
    
    # Check if all required fields are set
    if not email_address or not email_password:
        print("\n❌ Email configuration incomplete!")
        print("\nTo fix this, add the following to your .env file:")
        print("""
EMAIL_ADDRESS=your.email@gmail.com
EMAIL_PASSWORD=your_app_password
SENDER_NAME=Your Name
        """)
        return False
    
    print("\n✅ Email configuration looks good!")
    
    # Test SMTP connection
    print("\n🧪 Testing SMTP connection...")
    
    # Determine SMTP server based on email domain
    if "@gmail.com" in email_address:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
    elif "@outlook.com" in email_address or "@hotmail.com" in email_address:
        smtp_server = "smtp.outlook.com"
        smtp_port = 587
    elif "@yahoo.com" in email_address:
        smtp_server = "smtp.yahoo.com"
        smtp_port = 587
    else:
        smtp_server = "smtp.gmail.com"  # Default
        smtp_port = 587
    
    print(f"   Server: {smtp_server}:{smtp_port}")
    
    try:
        print("   Connecting...")
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
        server.starttls()
        print("   Authenticating...")
        server.login(email_address, email_password)
        server.quit()
        print("   ✅ SMTP connection successful!")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"   ❌ Authentication failed: {e}")
        print("   💡 Make sure you're using an App Password, not your regular password")
        return False
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        print("   💡 Check your internet connection and email provider settings")
        return False

def main():
    """Main function"""
    print("🚀 Email Configuration Checker")
    print("=" * 40)
    
    success = check_email_config()
    
    if success:
        print("\n🎉 Email configuration is ready!")
        print("You can now use the send email functionality in the main application.")
    else:
        print("\n❌ Email configuration needs to be fixed.")
        print("Please update your .env file and run this script again.")
    
    return success

if __name__ == "__main__":
    main() 