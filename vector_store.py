#!/usr/bin/env python3
"""
Vector Database for CV and Job Data Storage
Uses ChromaDB for efficient storage and retrieval of structured data
"""

import chromadb
from chromadb.config import Settings
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from pydantic import BaseModel
import streamlit as st


class DataRecord(BaseModel):
    """Base model for data records in vector store"""
    id: str
    type: str  # 'cv' or 'job'
    data: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]


class VectorStore:
    """Vector database for storing CV and job data"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Initialize collections
        self.cv_collection = self.client.get_or_create_collection(
            name="cv_data",
            metadata={"description": "CV/Resume data storage"}
        )
        
        self.job_collection = self.client.get_or_create_collection(
            name="job_data",
            metadata={"description": "Job description data storage"}
        )
        
        self.email_collection = self.client.get_or_create_collection(
            name="email_records",
            metadata={"description": "Email tracking records"}
        )
    
    def _generate_embedding_text(self, data: Dict[str, Any], data_type: str) -> str:
        """Generate text for embedding from structured data"""
        if data_type == "cv":
            # Create embedding text from CV data
            text_parts = []
            
            if "name" in data:
                text_parts.append(f"Name: {data['name']}")
            
            if "skills" in data and data["skills"]:
                text_parts.append(f"Skills: {', '.join(data['skills'])}")
            
            if "experience" in data and data["experience"]:
                exp_text = []
                for exp in data["experience"][:3]:  # Top 3 experiences
                    if isinstance(exp, dict):
                        exp_text.append(f"{exp.get('title', '')} at {exp.get('company', '')}")
                    else:
                        exp_text.append(str(exp))
                text_parts.append(f"Experience: {'; '.join(exp_text)}")
            
            if "education" in data and data["education"]:
                edu_text = []
                for edu in data["education"][:2]:  # Top 2 education entries
                    if isinstance(edu, dict):
                        edu_text.append(f"{edu.get('degree', '')} from {edu.get('institution', '')}")
                    else:
                        edu_text.append(str(edu))
                text_parts.append(f"Education: {'; '.join(edu_text)}")
            
            if "summary" in data:
                text_parts.append(f"Summary: {data['summary']}")
            
            return " | ".join(text_parts)
        
        elif data_type == "job":
            # Create embedding text from job data
            text_parts = []
            
            if "job_title" in data:
                text_parts.append(f"Job Title: {data['job_title']}")
            
            if "company_name" in data:
                text_parts.append(f"Company: {data['company_name']}")
            
            if "required_skills" in data and data["required_skills"]:
                text_parts.append(f"Required Skills: {', '.join(data['required_skills'])}")
            
            if "preferred_skills" in data and data["preferred_skills"]:
                text_parts.append(f"Preferred Skills: {', '.join(data['preferred_skills'])}")
            
            if "responsibilities" in data and data["responsibilities"]:
                resp_text = "; ".join(data["responsibilities"][:3])  # Top 3 responsibilities
                text_parts.append(f"Responsibilities: {resp_text}")
            
            if "summary" in data:
                text_parts.append(f"Summary: {data['summary']}")
            
            return " | ".join(text_parts)
        
        return str(data)
    
    def store_cv_data(self, cv_data: Dict[str, Any], user_id: str = "default") -> str:
        """Store CV data in vector database"""
        try:
            record_id = str(uuid.uuid4())
            embedding_text = self._generate_embedding_text(cv_data, "cv")
            
            # Store in ChromaDB
            self.cv_collection.add(
                documents=[embedding_text],
                metadatas=[{
                    "user_id": user_id,
                    "type": "cv",
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                    "data_keys": ",".join(list(cv_data.keys()))  # Convert list to string
                }],
                ids=[record_id]
            )
            
            # Also store full data in session state for immediate access
            if 'cv_data' not in st.session_state:
                st.session_state.cv_data = {}
            
            st.session_state.cv_data = cv_data
            st.session_state.cv_record_id = record_id
            
            return record_id
            
        except Exception as e:
            st.error(f"Error storing CV data: {e}")
            return None
    
    def store_job_data(self, job_data: Dict[str, Any], user_id: str = "default") -> str:
        """Store job data in vector database"""
        try:
            record_id = str(uuid.uuid4())
            embedding_text = self._generate_embedding_text(job_data, "job")
            
            # Store in ChromaDB
            self.job_collection.add(
                documents=[embedding_text],
                metadatas=[{
                    "user_id": user_id,
                    "type": "job",
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                    "data_keys": ",".join(list(job_data.keys()))  # Convert list to string
                }],
                ids=[record_id]
            )
            
            # Also store full data in session state for immediate access
            if 'current_job_data' not in st.session_state:
                st.session_state.current_job_data = {}
            
            st.session_state.current_job_data = job_data
            st.session_state.job_record_id = record_id
            
            return record_id
            
        except Exception as e:
            st.error(f"Error storing job data: {e}")
            return None
    
    def store_email_record(self, email_record: Dict[str, Any], user_id: str = "default") -> str:
        """Store email record in vector database"""
        try:
            record_id = str(uuid.uuid4())
            
            # Create embedding text from email record
            email_text = f"Job: {email_record.get('job_title', '')} at {email_record.get('company_name', '')} | Type: {email_record.get('email_type', '')} | Status: {email_record.get('status', '')}"
            
            # Store in ChromaDB
            self.email_collection.add(
                documents=[email_text],
                metadatas=[{
                    "user_id": user_id,
                    "type": "email",
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                    "sent_date": email_record.get('sent_date', datetime.now().isoformat()),
                    "job_title": email_record.get('job_title', ''),
                    "company_name": email_record.get('company_name', ''),
                    "status": email_record.get('status', '')
                }],
                ids=[record_id]
            )
            
            return record_id
            
        except Exception as e:
            st.error(f"Error storing email record: {e}")
            return None
    
    def get_cv_data(self, user_id: str = "default") -> Optional[Dict[str, Any]]:
        """Retrieve CV data from vector database"""
        try:
            # First check session state
            if 'cv_data' in st.session_state and st.session_state.cv_data:
                return st.session_state.cv_data
            
            # Query ChromaDB
            results = self.cv_collection.query(
                query_texts=["CV data"],
                n_results=1,
                where={"user_id": user_id, "type": "cv"}
            )
            
            if results['ids'] and results['ids'][0]:
                # For now, return session state data
                # In a full implementation, you'd reconstruct from stored data
                return st.session_state.get('cv_data')
            
            return None
            
        except Exception as e:
            st.error(f"Error retrieving CV data: {e}")
            return None
    
    def get_job_data(self, user_id: str = "default") -> Optional[Dict[str, Any]]:
        """Retrieve job data from vector database"""
        try:
            # First check session state
            if 'current_job_data' in st.session_state and st.session_state.current_job_data:
                return st.session_state.current_job_data
            
            # Query ChromaDB
            results = self.job_collection.query(
                query_texts=["job data"],
                n_results=1,
                where={"user_id": user_id, "type": "job"}
            )
            
            if results['ids'] and results['ids'][0]:
                # For now, return session state data
                return st.session_state.get('current_job_data')
            
            return None
            
        except Exception as e:
            st.error(f"Error retrieving job data: {e}")
            return None
    
    def get_email_records(self, user_id: str = "default", days: int = 30) -> List[Dict[str, Any]]:
        """Retrieve email records from vector database"""
        try:
            from datetime import datetime, timedelta
            
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Query ChromaDB for recent emails
            results = self.email_collection.query(
                query_texts=["email records"],
                n_results=50,
                where={
                    "user_id": user_id,
                    "type": "email",
                    "sent_date": {"$gte": cutoff_date.isoformat()}
                }
            )
            
            # Convert results to list of records
            records = []
            if results['metadatas']:
                for i, metadata in enumerate(results['metadatas'][0]):
                    records.append({
                        "id": results['ids'][0][i],
                        "job_title": metadata.get('job_title', ''),
                        "company_name": metadata.get('company_name', ''),
                        "status": metadata.get('status', ''),
                        "sent_date": metadata.get('sent_date', ''),
                        "created_at": metadata.get('created_at', '')
                    })
            
            return records
            
        except Exception as e:
            st.error(f"Error retrieving email records: {e}")
            return []
    
    def search_similar_jobs(self, query: str, user_id: str = "default", n_results: int = 5) -> List[Dict[str, Any]]:
        """Search for similar jobs based on query"""
        try:
            results = self.job_collection.query(
                query_texts=[query],
                n_results=n_results,
                where={"user_id": user_id, "type": "job"}
            )
            
            similar_jobs = []
            if results['metadatas']:
                for i, metadata in enumerate(results['metadatas'][0]):
                    similar_jobs.append({
                        "id": results['ids'][0][i],
                        "job_title": metadata.get('job_title', ''),
                        "company_name": metadata.get('company_name', ''),
                        "created_at": metadata.get('created_at', ''),
                        "similarity": results['distances'][0][i] if results['distances'] else 0
                    })
            
            return similar_jobs
            
        except Exception as e:
            st.error(f"Error searching similar jobs: {e}")
            return []
    
    def get_statistics(self, user_id: str = "default") -> Dict[str, Any]:
        """Get statistics from vector database"""
        try:
            # Count CV records by querying and counting results
            cv_results = self.cv_collection.query(
                query_texts=["CV data"],
                n_results=1000,
                where={"user_id": user_id, "type": "cv"}
            )
            cv_count = len(cv_results['ids'][0]) if cv_results['ids'] else 0
            
            # Count job records by querying and counting results
            job_results = self.job_collection.query(
                query_texts=["job data"],
                n_results=1000,
                where={"user_id": user_id, "type": "job"}
            )
            job_count = len(job_results['ids'][0]) if job_results['ids'] else 0
            
            # Count email records by querying and counting results
            email_results = self.email_collection.query(
                query_texts=["email records"],
                n_results=1000,
                where={"user_id": user_id, "type": "email"}
            )
            email_count = len(email_results['ids'][0]) if email_results['ids'] else 0
            
            # Get recent email records for success rate calculation
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
            # Delete from ChromaDB collections
            self.cv_collection.delete(where={"user_id": user_id})
            self.job_collection.delete(where={"user_id": user_id})
            self.email_collection.delete(where={"user_id": user_id})
            
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


# Global vector store instance
vector_store = None

def get_vector_store():
    """Get or create vector store instance with fallback to JSON storage"""
    global vector_store
    if vector_store is None:
        try:
            # Try to use ChromaDB first
            vector_store = VectorStore()
        except Exception as e:
            # If ChromaDB fails (e.g., SQLite compatibility), use fallback storage
            st.warning(f"⚠️ ChromaDB not available ({e}), using fallback storage")
            from fallback_storage import get_fallback_storage
            vector_store = get_fallback_storage()
    return vector_store 