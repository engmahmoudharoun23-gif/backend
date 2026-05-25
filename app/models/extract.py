"""
Extract Model
نموذج المستخلصات
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime, timezone
import uuid


class ExtractBase(BaseModel):
    """Base extract fields"""
    project: str
    contractor: str
    extract_number: Optional[str] = ""
    description: Optional[str] = ""
    notes: Optional[str] = ""
    expected_value: Optional[float] = 0
    actual_value: Optional[float] = None
    status: str = "pending"  # pending, registered
    images: List[str] = []


class ExtractCreate(ExtractBase):
    """Create extract request"""
    pass


class ExtractUpdate(BaseModel):
    """Update extract request"""
    project: Optional[str] = None
    contractor: Optional[str] = None
    extract_number: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    expected_value: Optional[float] = None
    actual_value: Optional[float] = None
    status: Optional[str] = None
    images: Optional[List[str]] = None


class Extract(ExtractBase):
    """Full extract model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    created_by_name: Optional[str] = None
    is_deleted: bool = False


class ExtractResponse(BaseModel):
    """Extract response"""
    id: str
    project: str
    contractor: str
    extract_number: Optional[str] = ""
    description: Optional[str] = ""
    notes: Optional[str] = ""
    expected_value: Optional[float] = 0
    actual_value: Optional[float] = None
    status: str
    images: List[str] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by_name: Optional[str] = None
