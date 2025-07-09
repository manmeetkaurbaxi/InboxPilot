# 🚀 Streamlit Cloud Deployment Guide

## Prerequisites

1. **GitHub Repository**: Your code must be in a public GitHub repository
2. **Streamlit Cloud Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **Environment Variables**: Prepare your API keys and credentials

## Step-by-Step Deployment

### 1. **Prepare Your Repository**

Ensure your repository has the following files:

```
my_own/
├── main.py                    # Main Streamlit app
├── requirements.txt           # Dependencies (updated with protobuf fix)
├── runtime.txt               # Python version specification
├── .streamlit/
│   ├── config.toml           # Streamlit configuration
│   └── secrets.toml          # Local secrets template
└── setup_deployment.py       # Deployment setup script
```

### 2. **Set Up Streamlit Cloud**

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub repository
4. Configure the app:
   - **Repository**: `your-username/your-repo-name`
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `my_own/main.py`

### 3. **Configure Streamlit Cloud Secrets**

In Streamlit Cloud, go to your app settings and add these secrets:

1. **Go to your app** in Streamlit Cloud
2. **Click "Settings"** (gear icon)
3. **Go to "Secrets"** tab
4. **Add the following secrets**:

```toml
GROQ_API_KEY = "your_actual_groq_api_key"
EMAIL_ADDRESS = "your.email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
SENDER_NAME = "Your Name"
```

**Important Notes:**
- The app automatically uses Streamlit Cloud secrets when deployed
- For local development, use `.env` file
- The app will automatically use fallback JSON storage if ChromaDB fails due to SQLite compatibility issues

### 4. **Deploy and Test**

1. Click "Deploy" in Streamlit Cloud
2. Wait for the build to complete
3. Test all functionality:
   - CV extraction
   - Job parsing
   - Email generation
   - Email sending

## 🔧 Troubleshooting Protobuf Issues

### If you still get protobuf errors:

1. **Check the build logs** in Streamlit Cloud
2. **Verify requirements.txt** has the correct protobuf version
3. **Ensure environment variables** are set correctly
4. **Try the workaround** by setting `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python`

### Common Issues and Solutions:

#### Issue: "Descriptors cannot be created directly"

**Solution**: The protobuf version fix in `requirements.txt` should resolve this.

#### Issue: "Module not found"

**Solution**: Ensure all dependencies are in `requirements.txt`

#### Issue: "API key not found"

**Solution**: Check that `GROQ_API_KEY` is set in Streamlit Cloud secrets

#### Issue: "Email sending fails"

**Solution**: Verify email credentials and 2FA settings

#### Issue: "SQLite version unsupported"

**Solution**: The app automatically falls back to JSON storage. This is normal and expected on Streamlit Cloud.

## 🛠️ Local Testing Before Deployment

Test your app locally to ensure it works:

```bash
cd my_own
pip install -r requirements.txt
streamlit run main.py
```

## 📊 Monitoring Your Deployment

1. **Check build logs** for any errors
2. **Monitor app performance** in Streamlit Cloud dashboard
3. **Test all features** after deployment
4. **Check error logs** if issues occur

## 🔄 Updating Your Deployment

1. **Push changes** to your GitHub repository
2. **Streamlit Cloud** will automatically redeploy
3. **Monitor the build** for any new issues
4. **Test the updated app**

## 📞 Support

If you encounter issues:

1. **Check the build logs** in Streamlit Cloud
2. **Review the troubleshooting section** above
3. **Check Streamlit Cloud documentation**
4. **Open an issue** in your repository

## 🎯 Best Practices

1. **Keep dependencies updated** in `requirements.txt`
2. **Use environment variables** for sensitive data
3. **Test locally** before deploying
4. **Monitor app performance** regularly
5. **Keep your API keys secure**
 