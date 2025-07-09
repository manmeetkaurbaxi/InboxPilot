#!/usr/bin/env python3
"""
Fallback Storage System
Uses JSON files when ChromaDB is not available due to SQLite compatibility issues
"""

import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
import streamlit as st

class FallbackStorage:
    """JSON-based storage system as fallback for ChromaDB"""
    
    def __init__(self, storage_dir: str = "data"):
        self.storage_dir = storage_dir
        self.ensure_storage_dir()
        
        # File paths
        self.cv_file = os.path.join(storage_dir, "cv_data.json")
        self.job_file = os.path.join(storage_dir, "job_data.json")
        self.email_file = os.path.join(storage_dir, "email_records.json")
        
        # Initialize files if they don't exist
        self.initialize_files()
    
    def ensure_storage_dir(self):
        """Ensure storage directory exists"""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
    
    def initialize_files(self):
        """Initialize JSON files if they don't exist"""
        files = [self.cv_file, self.job_file, self.email_file]
        for file_path in files:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump([], f)
    
    def store_cv_data(self, cv_data: Dict[str, Any], user_id: str = "default") -> str:
        """Store CV data in JSON file"""
        try:
            record_id = str(uuid.uuid4())
            record = {
                "id": record_id,
                "user_id": user_id,
                "type": "cv",
                "data": cv_data,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            # Read existing data
            with open(self.cv_file, 'r') as f:
                data = json.load(f)
            
            # Remove old CV data for this user
            data = [item for item in data if item.get('user_id') != user_id]
            
            # Add new record
            data.append(record)
            
            # Write back to file
            with open(self.cv_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Store in session state for immediate access
            st.session_state.cv_data = cv_data
            st.session_state.cv_record_id = record_id
            
            return record_id
        except Exception as e:
            st.error(f"Error storing CV data: {e}")
            return None
    
    def store_job_data(self, job_data: Dict[str, Any], user_id: str = "default") -> str:
        """Store job data in JSON file"""
        try:
            record_id = str(uuid.uuid4())
            record = {
                "id": record_id,
                "user_id": user_id,
                "type": "job",
                "data": job_data,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            # Read existing data
            with open(self.job_file, 'r') as f:
                data = json.load(f)
            
            # Remove old job data for this user
            data = [item for item in data if item.get('user_id') != user_id]
            
            # Add new record
            data.append(record)
            
            # Write back to file
            with open(self.job_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Store in session state for immediate access
            st.session_state.current_job_data = job_data
            st.session_state.job_record_id = record_id
            
            return record_id
        except Exception as e:
            st.error(f"Error storing job data: {e}")
            return None
    
    def store_email_record(self, email_record: Dict[str, Any], user_id: str = "default") -> str:
        """Store email record in JSON file"""
        try:
            record_id = str(uuid.uuid4())
            record = {
                "id": record_id,
                "user_id": user_id,
                "type": "email",
                "data": email_record,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            # Read existing data
            with open(self.email_file, 'r') as f:
                data = json.load(f)
            
            # Add new record
            data.append(record)
            
            # Write back to file
            with open(self.email_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            return record_id
        except Exception as e:
            st.error(f"Error storing email record: {e}")
            return None
    
    def get_cv_data(self, user_id: str = "default") -> Optional[Dict[str, Any]]:
        """Retrieve CV data from JSON file"""
        try:
            # First check session state
            if 'cv_data' in st.session_state and st.session_state.cv_data:
                return st.session_state.cv_data
            
            # Read from file
            with open(self.cv_file, 'r') as f:
                data = json.load(f)
            
            # Find latest CV data for user
            user_cv_data = [item for item in data if item.get('user_id') == user_id and item.get('type') == 'cv']
            if user_cv_data:
                latest_cv = max(user_cv_data, key=lambda x: x.get('created_at', ''))
                return latest_cv.get('data')
            
            return None
        except Exception as e:
            st.error(f"Error retrieving CV data: {e}")
            return None
    
    def get_job_data(self, user_id: str = "default") -> Optional[Dict[str, Any]]:
        """Retrieve job data from JSON file"""
        try:
            # First check session state
            if 'current_job_data' in st.session_state and st.session_state.current_job_data:
                return st.session_state.current_job_data
            
            # Read from file
            with open(self.job_file, 'r') as f:
                data = json.load(f)
            
            # Find latest job data for user
            user_job_data = [item for item in data if item.get('user_id') == user_id and item.get('type') == 'job']
            if user_job_data:
                latest_job = max(user_job_data, key=lambda x: x.get('created_at', ''))
                return latest_job.get('data')
            
            return None
        except Exception as e:
            st.error(f"Error retrieving job data: {e}")
            return None
    
    def get_email_records(self, user_id: str = "default", days: int = 30) -> List[Dict[str, Any]]:
        """Retrieve email records from JSON file"""
        try:
            from datetime import datetime, timedelta
            
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Read from file
            with open(self.email_file, 'r') as f:
                data = json.load(f)
            
            # Filter recent emails for user
            user_emails = [
                item for item in data 
                if item.get('user_id') == user_id 
                and item.get('type') == 'email'
                and datetime.fromisoformat(item.get('created_at', '1970-01-01')) >= cutoff_date
            ]
            
            # Convert to expected format
            records = []
            for item in user_emails:
                email_data = item.get('data', {})
                records.append({
                    "id": item.get('id', ''),
                    "job_title": email_data.get('job_title', ''),
                    "company_name": email_data.get('company_name', ''),
                    "status": email_data.get('status', ''),
                    "sent_date": email_data.get('sent_date', ''),
                    "created_at": item.get('created_at', '')
                })
            
            return records
        except Exception as e:
            st.error(f"Error retrieving email records: {e}")
            return []
    
    def get_statistics(self, user_id: str = "default") -> Dict[str, Any]:
        """Get statistics from JSON files"""
        try:
            # Count CV records
            with open(self.cv_file, 'r') as f:
                cv_data = json.load(f)
            cv_count = len([item for item in cv_data if item.get('user_id') == user_id])
            
            # Count job records
            with open(self.job_file, 'r') as f:
                job_data = json.load(f)
            job_count = len([item for item in job_data if item.get('user_id') == user_id])
            
            # Count email records
            with open(self.email_file, 'r') as f:
                email_data = json.load(f)
            email_count = len([item for item in email_data if item.get('user_id') == user_id])
            
            # Get recent emails for success rate
            recent_emails = self.get_email_records(user_id, 30)
            successful_emails = len([r for r in recent_emails if r.get('status') in ['delivered', 'opened', 'replied']])
            success_rate = (successful_emails / len(recent_emails)) * 100 if recent_emails else 0
            
            return {
                "cv_records": cv_count,
                "job_records": job_count,
                "email_records": email_count,
                "recent_emails": len(recent_emails),
                "success_rate": round(success_rate, 1)
            }
        except Exception as e:
            st.error(f"Error getting statistics: {e}")
            return {
                "cv_records": 0,
                "job_records": 0,
                "email_records": 0,
                "recent_emails": 0,
                "success_rate": 0
            }
    
    def clear_user_data(self, user_id: str = "default"):
        """Clear all data for a specific user"""
        try:
            # Clear CV data
            with open(self.cv_file, 'r') as f:
                cv_data = json.load(f)
            cv_data = [item for item in cv_data if item.get('user_id') != user_id]
            with open(self.cv_file, 'w') as f:
                json.dump(cv_data, f, indent=2)
            
            # Clear job data
            with open(self.job_file, 'r') as f:
                job_data = json.load(f)
            job_data = [item for item in job_data if item.get('user_id') != user_id]
            with open(self.job_file, 'w') as f:
                json.dump(job_data, f, indent=2)
            
            # Clear email data
            with open(self.email_file, 'r') as f:
                email_data = json.load(f)
            email_data = [item for item in email_data if item.get('user_id') != user_id]
            with open(self.email_file, 'w') as f:
                json.dump(email_data, f, indent=2)
            
            # Clear session state
            if 'cv_data' in st.session_state:
                del st.session_state.cv_data
            if 'current_job_data' in st.session_state:
                del st.session_state.current_job_data
            if 'cv_record_id' in st.session_state:
                del st.session_state.cv_record_id
            if 'job_record_id' in st.session_state:
                del st.session_state.job_record_id
            
            st.success("User data cleared successfully!")
        except Exception as e:
            st.error(f"Error clearing user data: {e}")

def get_fallback_storage():
    """Get fallback storage instance"""
    return FallbackStorage() 