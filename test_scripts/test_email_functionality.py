#!/usr/bin/env python3
"""
Test script for email functionality
Run this to test if the email sending works correctly
"""

import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_email_functionality():
    """Test email functionality with a simple interface"""
    st.title("🧪 Email Functionality Test")
    st.write("Use this to test if your email settings work correctly")
    
    # Email configuration
    st.subheader("📧 Email Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        smtp_server = st.selectbox(
            "SMTP Server",
            ["smtp.gmail.com", "smtp.outlook.com", "smtp.yahoo.com", "smtp.office365.com"]
        )
        smtp_port = st.number_input("SMTP Port", value=587, min_value=25, max_value=587)
    
    with col2:
        sender_email = st.text_input("Your Email", placeholder="your.email@gmail.com")
        sender_password = st.text_input("App Password", type="password")
    
    # Test recipient
    test_recipient = st.text_input("Test Recipient Email", placeholder="test@example.com")
    
    # Test buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧪 Test Connection", type="primary"):
            if sender_email and sender_password:
                try:
                    st.info(f"Testing connection to {smtp_server}:{smtp_port}...")
                    server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.quit()
                    st.success("✅ Connection test successful!")
                except Exception as e:
                    st.error(f"❌ Connection test failed: {e}")
            else:
                st.warning("Please enter email and password")
    
    with col2:
        if st.button("📧 Send Test Email", type="primary"):
            if sender_email and sender_password and test_recipient:
                try:
                    # Create test message
                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = test_recipient
                    msg['Subject'] = "Test Email from Cold Email Generator"
                    
                    body = """
                    This is a test email from the Cold Email Generator application.
                    
                    If you received this email, your SMTP configuration is working correctly!
                    
                    Best regards,
                    Cold Email Generator
                    """
                    
                    msg.attach(MIMEText(body, 'plain'))
                    
                    # Send email
                    st.info("Sending test email...")
                    server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, test_recipient, msg.as_string())
                    server.quit()
                    
                    st.success("✅ Test email sent successfully!")
                    st.info("Check your recipient's inbox for the test email")
                    
                except Exception as e:
                    st.error(f"❌ Failed to send test email: {e}")
            else:
                st.warning("Please fill in all fields")
    
    # Help section
    with st.expander("📋 Setup Instructions"):
        st.write("""
        **For Gmail:**
        1. Enable 2-factor authentication on your Google account
        2. Go to Google Account → Security → App Passwords
        3. Generate a new app password for "Mail"
        4. Use your Gmail address and the generated app password
        
        **For Outlook/Office365:**
        1. Enable 2-factor authentication
        2. Go to Account Settings → Security → App Passwords
        3. Generate an app password
        4. Use your Outlook email and the app password
        
        **For Yahoo:**
        1. Enable 2-factor authentication
        2. Go to Account Security → App Passwords
        3. Generate an app password
        4. Use your Yahoo email and the app password
        """)

if __name__ == "__main__":
    test_email_functionality() 