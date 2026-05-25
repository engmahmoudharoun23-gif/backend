"""
Common Models
نماذج مشتركة
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime, timezone
import uuid


class ContractorBase(BaseModel):
    """Base contractor fields"""
    name: str
    phone: Optional[str] = ""
    email: Optional[str] = ""
    address: Optional[str] = ""
    project: Optional[str] = None
    notes: Optional[str] = ""


class ContractorCreate(ContractorBase):
    """Create contractor request"""
    pass


class Contractor(ContractorBase):
    """Full contractor model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class GovernorateBase(BaseModel):
    """Base governorate fields"""
    name: str
    project: str


class GovernorateCreate(GovernorateBase):
    """Create governorate request"""
    pass


class Governorate(GovernorateBase):
    """Full governorate model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AreaBase(BaseModel):
    """Base area fields"""
    name: str
    governorate: str
    project: str


class AreaCreate(AreaBase):
    """Create area request"""
    pass


class Area(AreaBase):
    """Full area model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ProjectBase(BaseModel):
    """Base project fields"""
    name: str
    description: Optional[str] = ""
    location: Optional[str] = ""
    is_active: bool = True


class ProjectCreate(ProjectBase):
    """Create project request"""
    pass


class Project(ProjectBase):
    """Full project model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SupportMessage(BaseModel):
    """Support message model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    user_name: str
    message: str
    is_read: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ChatMessage(BaseModel):
    """Chat message model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str
    sender_name: str
    receiver_id: str
    message: str
    is_read: bool = False
    images: List[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
