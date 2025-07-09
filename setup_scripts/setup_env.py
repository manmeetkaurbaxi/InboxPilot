#!/usr/bin/env python3
"""
Setup script to help users create their .env file
"""

import os
import sys

def create_env_file():
    """Create .env file with user input"""
    print("🔧 Setting up environment variables")
    print("=" * 40)
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists!")
        overwrite = input("Do you want to overwrite it? (y/N): ").lower().strip()
        if overwrite != 'y':
            print("Setup cancelled.")
            return False
    
    print("\n📝 Please provide your API keys:")
    print("(You can get a GROQ API key from https://console.groq.com/keys)")
    
    # Get GROQ API key
    groq_key = input("\nEnter your GROQ API key: ").strip()
    if not groq_key:
        print("❌ GROQ API key is required!")
        return False
    
    # Optional email settings
    print("\n📧 Optional: Email settings (press Enter to skip)")
    email_address = input("Email address: ").strip()
    email_password = input("Email password (app password): ").strip()
    sender_name = input("Sender name: ").strip()
    
    # Create .env content
    env_content = f"""# Groq API Key - Get from https://console.groq.com/keys
GROQ_API_KEY={groq_key}

# Optional: Email settings for sending emails
"""
    
    if email_address:
        env_content += f"EMAIL_ADDRESS={email_address}\n"
    if email_password:
        env_content += f"EMAIL_PASSWORD={email_password}\n"
    if sender_name:
        env_content += f'SENDER_NAME="{sender_name}"\n'
    
    # Write .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("\n✅ .env file created successfully!")
        print("You can now run: streamlit run main.py")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 CV Extractor Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("❌ Please run this script from the my_own directory")
        print("cd my_own")
        print("python setup_env.py")
        return False
    
    # Create .env file
    success = create_env_file()
    
    if success:
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Test setup: python test_setup.py")
        print("3. Run application: streamlit run main.py")
    else:
        print("\n❌ Setup failed. Please try again.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 