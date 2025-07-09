# 🔐 Secrets Management Guide

This guide explains how to manage secrets (API keys, passwords, etc.) for both local development and Streamlit Cloud deployment.

## 🏠 Local Development

### Option 1: Environment Variables (.env file) - Recommended

1. **Create a `.env` file** in the `my_own/` directory:

```bash
# .env file
GROQ_API_KEY=your_actual_groq_api_key_here
EMAIL_ADDRESS=your.email@gmail.com
EMAIL_PASSWORD=your_app_password_here
SENDER_NAME=Your Name
```

2. **The app automatically loads** these variables using `python-dotenv`

### Option 2: Streamlit Secrets (.streamlit/secrets.toml)

1. **Create `.streamlit/secrets.toml`** file:

```toml
GROQ_API_KEY = "your_actual_groq_api_key_here"
EMAIL_ADDRESS = "your.email@gmail.com"
EMAIL_PASSWORD = "your_app_password_here"
SENDER_NAME = "Your Name"
```

2. **The app automatically detects** and uses these secrets

## ☁️ Streamlit Cloud Deployment

### Setting Up Secrets in Streamlit Cloud

1. **Deploy your app** to Streamlit Cloud
2. **Go to your app** in the Streamlit Cloud dashboard
3. **Click "Settings"** (gear icon) in the top right
4. **Go to "Secrets"** tab
5. **Add your secrets** in TOML format:

```toml
GROQ_API_KEY = "your_actual_groq_api_key_here"
EMAIL_ADDRESS = "your.email@gmail.com"
EMAIL_PASSWORD = "your_app_password_here"
SENDER_NAME = "Your Name"
```

6. **Click "Save"** to apply the secrets
7. **Redeploy your app** if needed

### How the App Detects Secrets

The app uses a **priority-based approach**:

1. **First**: Try to use `st.secrets` (Streamlit Cloud)
2. **Fallback**: Use `os.getenv()` (local .env file)
3. **Default**: Use hardcoded defaults where appropriate

```python
# Example from config.py
try:
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    EMAIL_ADDRESS = st.secrets.get("EMAIL_ADDRESS") or os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = st.secrets.get("EMAIL_PASSWORD") or os.getenv("EMAIL_PASSWORD")
    SENDER_NAME = st.secrets.get("SENDER_NAME") or os.getenv("SENDER_NAME", "Your Name")
except:
    # Fallback to environment variables
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    SENDER_NAME = os.getenv("SENDER_NAME", "Your Name")
```

## 🔑 Required Secrets

### GROQ_API_KEY

- **Purpose**: Access to Groq LLM API for AI processing
- **How to get**: Sign up at [console.groq.com](https://console.groq.com)
- **Format**: String (e.g., "gsk\_...")

### EMAIL_ADDRESS

- **Purpose**: Email address for sending emails
- **Format**: Valid email address (e.g., "your.email@gmail.com")
- **Note**: Must have 2FA enabled and app password generated

### EMAIL_PASSWORD

- **Purpose**: App password for email authentication
- **Format**: App password (not regular password)
- **How to get**: Generate app password in your email provider settings

### SENDER_NAME

- **Purpose**: Name displayed as sender in emails
- **Format**: String (e.g., "Your Name")
- **Default**: "Your Name" if not provided

## 🛡️ Security Best Practices

### ✅ Do's

- Use **App Passwords** for email (not regular passwords)
- Keep secrets **private** and never commit them to git
- Use **different secrets** for development and production
- **Rotate secrets** regularly
- Use **strong, unique passwords**

### ❌ Don'ts

- Never commit `.env` files to git
- Never share secrets in public repositories
- Don't use regular email passwords
- Don't hardcode secrets in your code
- Don't use the same secrets across multiple projects

## 🔧 Testing Your Secrets

### Local Testing

```bash
cd my_own
python check_email_config.py
```

### Streamlit Cloud Testing

1. Deploy with secrets configured
2. Test email functionality in the app
3. Check app logs for any errors

## 🚨 Troubleshooting

### "API key not found" Error

- **Local**: Check your `.env` file exists and has correct format
- **Cloud**: Verify secrets are added in Streamlit Cloud settings

### "Email authentication failed" Error

- Ensure you're using an **App Password**, not regular password
- Verify **2FA is enabled** on your email account
- Check email provider settings

### "Secrets not loading" Error

- **Local**: Restart the Streamlit app after adding `.env` file
- **Cloud**: Redeploy the app after adding secrets

## 📝 Example Files

### .env file (local development)

```bash
GROQ_API_KEY=gsk_your_actual_key_here
EMAIL_ADDRESS=your.email@gmail.com
EMAIL_PASSWORD=your_16_char_app_password
SENDER_NAME=Your Name
```

### Streamlit Cloud Secrets (production)

```toml
GROQ_API_KEY = "gsk_your_actual_key_here"
EMAIL_ADDRESS = "your.email@gmail.com"
EMAIL_PASSWORD = "your_16_char_app_password"
SENDER_NAME = "Your Name"
```

## 🔄 Migration Guide

### From Local to Cloud

1. **Deploy your app** to Streamlit Cloud
2. **Add secrets** in Streamlit Cloud settings
3. **Test functionality** in the deployed app
4. **Remove local secrets** if no longer needed

### From Cloud to Local

1. **Copy secrets** from Streamlit Cloud settings
2. **Create `.env` file** with the same values
3. **Test locally** to ensure everything works
4. **Keep both** for development flexibility
