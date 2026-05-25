"""
Employee Request Model
نموذج طلبات الموظفين
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime, timezone
import uuid


class EmployeeRequestBase(BaseModel):
    """Base employee request fields"""
    request_type: str  # vacation, sick_leave, permission, etc.
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    reason: Optional[str] = ""
    notes: Optional[str] = ""
    project: Optional[str] = None
    images: List[str] = []


class EmployeeRequestCreate(EmployeeRequestBase):
    """Create employee request"""
    pass


class EmployeeRequestUpdate(BaseModel):
    """Update employee request"""
    request_type: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    reason: Optional[str] = None
    notes: Optional[str] = None
    project: Optional[str] = None
    images: Optional[List[str]] = None
    status: Optional[str] = None


class EmployeeRequest(EmployeeRequestBase):
    """Full employee request model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "pending"  # pending, approved_by_manager, approved_by_admin, rejected, cancelled
    
    # Employee info
    uploaded_by: Optional[str] = None
    employee_name: Optional[str] = None
    employee_id: Optional[str] = None
    
    # Manager info
    manager_id: Optional[str] = None
    manager_name: Optional[str] = None
    
    # Approval tracking
    reviewed_by_manager_id: Optional[str] = None
    reviewed_by_manager_name: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    
    approved_by_final_reviewer_id: Optional[str] = None
    approved_by_final_reviewer_name: Optional[str] = None
    approved_at: Optional[datetime] = None
    
    # Rejection tracking
    rejected_by_id: Optional[str] = None
    rejected_by_name: Optional[str] = None
    rejection_notes: Optional[str] = None
    rejected_at: Optional[datetime] = None
    
    # Cancellation tracking
    cancelled_by_id: Optional[str] = None
    cancelled_by_name: Optional[str] = None
    cancellation_notes: Optional[str] = None
    cancelled_at: Optional[datetime] = None
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None


class EmployeeRequestResponse(BaseModel):
    """Employee request response"""
    id: str
    request_type: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    reason: Optional[str] = ""
    notes: Optional[str] = ""
    project: Optional[str] = None
    images: List[str] = []
    status: str
    employee_name: Optional[str] = None
    manager_name: Optional[str] = None
    reviewed_by_manager_name: Optional[str] = None
    approved_by_final_reviewer_name: Optional[str] = None
    rejection_notes: Optional[str] = None
    cancellation_notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
