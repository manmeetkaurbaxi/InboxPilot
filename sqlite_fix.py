#!/usr/bin/env python3
"""
SQLite Compatibility Fix for ChromaDB
Patches the system to use a compatible SQLite version
"""

import os
import sys
import sqlite3

def fix_sqlite():
    """Fix SQLite compatibility issues for ChromaDB"""
    try:
        # Try to import pysqlite3 and patch sqlite3
        import pysqlite3
        sys.modules['sqlite3'] = pysqlite3
        print("✅ Successfully patched sqlite3 with pysqlite3")
    except ImportError:
        print("⚠️ pysqlite3 not available, using system sqlite3")
    
    # Check SQLite version
    try:
        version = sqlite3.sqlite_version
        print(f"📊 SQLite version: {version}")
        
        # Parse version string to check if it's >= 3.35.0
        version_parts = version.split('.')
        major = int(version_parts[0])
        minor = int(version_parts[1])
        
        if major > 3 or (major == 3 and minor >= 35):
            print("✅ SQLite version is compatible with ChromaDB")
            return True
        else:
            print("⚠️ SQLite version may be incompatible with ChromaDB")
            return False
    except Exception as e:
        print(f"❌ Error checking SQLite version: {e}")
        return False

def setup_chroma_compatibility():
    """Setup ChromaDB with SQLite compatibility"""
    try:
        # Apply SQLite fix before importing ChromaDB
        fix_sqlite()
        
        # Import ChromaDB after fixing SQLite
        import chromadb
        print("✅ ChromaDB imported successfully")
        return True
    except Exception as e:
        print(f"❌ Error setting up ChromaDB compatibility: {e}")
        return False

if __name__ == "__main__":
    setup_chroma_compatibility() 