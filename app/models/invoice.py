"""
Invoice Model
نموذج فواتير العهدة
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime, timezone
import uuid


class InvoiceBase(BaseModel):
    """Base invoice fields"""
    amount: float
    description: Optional[str] = ""
    notes: Optional[str] = ""
    category: Optional[str] = ""
    project: Optional[str] = None
    images: List[str] = []


class InvoiceCreate(InvoiceBase):
    """Create invoice request"""
    pass


class InvoiceUpdate(BaseModel):
    """Update invoice request"""
    amount: Optional[float] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    category: Optional[str] = None
    project: Optional[str] = None
    images: Optional[List[str]] = None
    status: Optional[str] = None


class Invoice(InvoiceBase):
    """Full invoice model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "pending"  # pending, approved_by_manager, approved_final, rejected, cancelled
    uploaded_by: Optional[str] = None
    uploaded_by_name: Optional[str] = None
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


class InvoiceResponse(BaseModel):
    """Invoice response"""
    id: str
    amount: float
    description: Optional[str] = ""
    notes: Optional[str] = ""
    category: Optional[str] = ""
    project: Optional[str] = None
    images: List[str] = []
    status: str
    uploaded_by: Optional[str] = None
    uploaded_by_name: Optional[str] = None
    manager_name: Optional[str] = None
    reviewed_by_manager_name: Optional[str] = None
    approved_by_final_reviewer_name: Optional[str] = None
    rejection_notes: Optional[str] = None
    cancellation_notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class RejectRequest(BaseModel):
    """Reject request body"""
    rejection_reason: str


class CancelRequest(BaseModel):
    """Cancel request body"""
    cancellation_reason: Optional[str] = None
