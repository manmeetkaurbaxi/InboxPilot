#!/usr/bin/env python3
"""
Email Tracking Module
Handles email records and tracking to prevent duplication
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
import os


class EmailRecord(BaseModel):
    """Record of sent emails to prevent duplication"""
    id: str = Field(description="Unique identifier for the email record")
    job_title: str = Field(description="Job title applied for")
    company_name: str = Field(description="Company name")
    recipient_email: Optional[str] = Field(description="Recipient email address")
    recipient_name: Optional[str] = Field(description="Recipient name")
    sent_date: datetime = Field(description="Date and time when email was sent")
    email_type: str = Field(description="Type of email sent (cold, follow-up, etc.)")
    status: str = Field(description="Email status (sent, delivered, opened, etc.)")
    cv_data_used: Dict[str, Any] = Field(description="CV data used for personalization")
    job_data_used: Dict[str, Any] = Field(description="Job data used for personalization")
    email_content: Optional[str] = Field(description="Email content sent")
    notes: Optional[str] = Field(description="Additional notes or follow-up actions")


class EmailTracker:
    """Track sent emails to prevent duplication"""
    
    def __init__(self, storage_file: str = "email_records.json"):
        self.storage_file = storage_file
        self.records = self._load_records()
    
    def _load_records(self) -> List[EmailRecord]:
        """Load email records from storage"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    return [EmailRecord(**record) for record in data]
            return []
        except Exception as e:
            print(f"Error loading email records: {e}")
            return []
    
    def _save_records(self):
        """Save email records to storage"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump([record.model_dump() for record in self.records], f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving email records: {e}")
    
    def check_duplicate(self, job_title: str, company_name: str, days_threshold: int = 30) -> bool:
        """Check if an email has already been sent for this job/company"""
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days_threshold)
        
        for record in self.records:
            if (record.job_title.lower() == job_title.lower() and 
                record.company_name.lower() == company_name.lower() and
                record.sent_date > cutoff_date):
                return True
        return False
    
    def add_record(self, email_record: EmailRecord):
        """Add a new email record"""
        self.records.append(email_record)
        self._save_records()
    
    def get_recent_emails(self, days: int = 30) -> List[EmailRecord]:
        """Get recent email records"""
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        return [record for record in self.records if record.sent_date > cutoff_date]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get email tracking statistics"""
        total_emails = len(self.records)
        recent_emails = len(self.get_recent_emails(30))
        
        # Count unique companies
        companies = set(record.company_name for record in self.records)
        companies_contacted = len(companies)
        
        # Calculate success rate (emails with positive status)
        successful_emails = len([r for r in self.records 
                               if r.status in ['delivered', 'opened', 'replied']])
        success_rate = (successful_emails / total_emails * 100) if total_emails > 0 else 0
        
        return {
            "total_emails": total_emails,
            "companies_contacted": companies_contacted,
            "recent_emails": recent_emails,
            "success_rate": round(success_rate, 1)
        } 