#!/usr/bin/env python3
"""
Setup script for Streamlit Cloud deployment
Fixes protobuf compatibility issues
"""

import os
import subprocess
import sys

def fix_protobuf_issues():
    """Fix protobuf compatibility issues"""
    print("🔧 Fixing protobuf compatibility issues...")
    
    # Set environment variable for protobuf
    os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
    
    # Try to upgrade/downgrade protobuf if needed
    try:
        # First, try to install a compatible version
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', 
            'protobuf>=3.20.0,<4.0.0', '--force-reinstall'
        ])
        print("✅ Protobuf version fixed")
    except subprocess.CalledProcessError:
        print("⚠️ Could not fix protobuf version, using environment variable workaround")
    
    # Set additional environment variables
    os.environ['PYTHONPATH'] = os.getcwd()
    
    print("✅ Deployment setup completed")

if __name__ == "__main__":
    fix_protobuf_issues() 