# Email Sending Troubleshooting Guide

This guide helps you resolve issues with the send email button and email functionality.

## 🚨 Send Email Button Not Working

### Quick Fixes

1. **Refresh the Page**

   - Sometimes the interface gets stuck
   - Press `Ctrl+F5` (or `Cmd+Shift+R` on Mac) to hard refresh

2. **Check Data Requirements**

   - Ensure you have CV data loaded (from CV Extractor page)
   - Ensure you have job data loaded (from Job Parser page)
   - Both are required before the send email interface appears

3. **Enable Debug Information**
   - Check the "🐛 Show Debug Info" checkbox
   - This will show you the current state of the application

### Step-by-Step Debugging

#### Step 1: Verify Data Loading

1. Go to the **CV Extractor** page
2. Upload and extract your CV data
3. Go to the **Job Parser** page
4. Parse a job description
5. Return to the **Email Generator** page
6. Generate an email

#### Step 2: Check Send Email Button

1. After generating an email, look for the "📤 Send Email" button
2. Click it - this should show the SMTP configuration interface
3. If the interface doesn't appear, check the debug information

#### Step 3: Configure SMTP Settings

1. The application now uses environment variables for email credentials
2. Ensure your `.env` file contains:
   ```
   EMAIL_ADDRESS=your.email@gmail.com
   EMAIL_PASSWORD=your_app_password
   SENDER_NAME=Your Name
   ```
3. Select your email provider from the dropdown
4. Use the "🧪 Test Connection" button to verify settings

## 🔧 Common Email Configuration Issues

### Gmail Setup

```
SMTP Server: smtp.gmail.com
SMTP Port: 587
Email: your.email@gmail.com
Password: [App Password - not your regular password]
```

**To get an App Password:**

1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Click "Security"
3. Enable "2-Step Verification" if not already enabled
4. Click "App passwords"
5. Select "Mail" and generate a password
6. Use this 16-character password in the application

### Outlook/Office365 Setup

```
SMTP Server: smtp.outlook.com
SMTP Port: 587
Email: your.email@outlook.com
Password: [App Password]
```

**To get an App Password:**

1. Go to [Microsoft Account Security](https://account.microsoft.com/security)
2. Enable "Two-step verification"
3. Go to "Advanced security options"
4. Create an "App password"
5. Use this password in the application

### Yahoo Setup

```
SMTP Server: smtp.yahoo.com
SMTP Port: 587
Email: your.email@yahoo.com
Password: [App Password]
```

**To get an App Password:**

1. Go to [Yahoo Account Security](https://login.yahoo.com/account/security)
2. Enable "2-step verification"
3. Go to "App passwords"
4. Generate a new app password
5. Use this password in the application

## 🐛 Debug Information

When you enable "Show Debug Info", you'll see:

- `show_send_email`: Should be `True` when send interface is active
- `current_email exists`: Should be `True` if email was generated
- `email_tracker exists`: Should be `True` if tracking is initialized

### What Each Debug Value Means

- **show_send_email: False** - The send interface is hidden
- **show_send_email: True** - The send interface should be visible
- **current_email exists: False** - No email has been generated yet
- **current_email exists: True** - Email is ready to send
- **email_tracker exists: False** - Email tracking not initialized
- **email_tracker exists: True** - Email tracking is working

## ❌ Error Messages and Solutions

### "Authentication failed"

- **Cause**: Wrong password or 2FA not enabled
- **Solution**: Use App Password, not regular password

### "Connection failed"

- **Cause**: Network issues or wrong SMTP settings
- **Solution**: Check internet connection and SMTP server/port

### "Recipient email rejected"

- **Cause**: Invalid email address or domain issues
- **Solution**: Verify recipient email address

### "Server disconnected"

- **Cause**: Email provider security settings
- **Solution**: Try again or check email provider settings

### "Please specify a recipient email address"

- **Cause**: No recipient email entered
- **Solution**: Enter a valid email address in the recipient field

### "Please provide your email credentials"

- **Cause**: Missing email or password
- **Solution**: Fill in both email and app password fields

## 🧪 Testing Your Setup

Use the test script to verify your email configuration:

```bash
# Option 1: Use the test runner (recommended)
python run_tests.py email

# Option 2: Run directly
streamlit run test_scripts/test_email_functionality.py
```

This will help you:

1. Test SMTP connection without sending emails
2. Send a test email to verify everything works
3. Get detailed error messages if something fails

## 📞 Getting Help

If you're still having issues:

1. **Check the logs**: Look for error messages in the Streamlit output
2. **Test with the test script**: Use `test_email_functionality.py`
3. **Verify your email provider**: Make sure your email provider supports SMTP
4. **Check network**: Ensure your network allows SMTP traffic (port 587)

### Common Network Issues

- **Corporate networks**: May block SMTP traffic
- **Public WiFi**: May have restrictions
- **Firewall**: May block outgoing SMTP connections
- **ISP restrictions**: Some ISPs block SMTP for security

## 🔄 Alternative Solutions

If direct email sending doesn't work:

1. **Copy and paste**: Copy the generated email and send manually
2. **Download email**: Use the download feature to save the email
3. **Mark as sent**: Use the "Mark as Sent" button to track without sending
4. **Use email client**: Import the generated email into your email client

## 📋 Checklist

Before reporting an issue, verify:

- [ ] CV data is loaded
- [ ] Job data is loaded
- [ ] Email is generated successfully
- [ ] 2-factor authentication is enabled
- [ ] App password is generated
- [ ] Correct SMTP server and port
- [ ] Internet connection is working
- [ ] Test connection button works
- [ ] Debug information shows correct values
