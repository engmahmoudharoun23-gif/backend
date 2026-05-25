"""
Report Model
نموذج البلاغات
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime, timezone
import uuid


class ReportBase(BaseModel):
    """Base report fields"""
    project: str
    governorate: str
    area: Optional[str] = None
    report_type: str
    contractor: Optional[str] = None
    images: List[str] = []
    description: Optional[str] = ""
    notes: Optional[str] = ""
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    status: str = "pending"


class ReportCreate(ReportBase):
    """Create report request"""
    pass


class ReportUpdate(BaseModel):
    """Update report request"""
    project: Optional[str] = None
    governorate: Optional[str] = None
    area: Optional[str] = None
    report_type: Optional[str] = None
    contractor: Optional[str] = None
    images: Optional[List[str]] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    status: Optional[str] = None


class Report(ReportBase):
    """Full report model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    created_by_name: Optional[str] = None
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[str] = None
    seen_by: List[str] = []


class ReportResponse(BaseModel):
    """Report response"""
    id: str
    project: str
    governorate: str
    area: Optional[str] = None
    report_type: str
    contractor: Optional[str] = None
    images: List[str] = []
    description: Optional[str] = ""
    notes: Optional[str] = ""
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    created_by_name: Optional[str] = None


class ReportType(BaseModel):
    """Report type model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    project: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ReportTypeCreate(BaseModel):
    """Create report type request"""
    name: str
    project: str
