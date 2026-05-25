"""
Water/Sewage Connection Models
نماذج توصيلات المياه والصرف الصحي
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime, timezone
import uuid


class WaterConnectionBase(BaseModel):
    """Base water connection fields"""
    project: str
    contractor: str
    account_number: Optional[str] = ""
    request_number: Optional[str] = ""
    restriction_number: Optional[str] = ""
    ccb_report_number: Optional[str] = ""
    customer_name: Optional[str] = ""
    phone_number: Optional[str] = ""
    area: Optional[str] = ""
    work_order_date: Optional[str] = ""
    diameter: Optional[str] = ""
    connection_length: Optional[str] = ""
    notes: Optional[str] = ""
    latitude: Optional[str] = ""
    longitude: Optional[str] = ""
    commissioning_date: Optional[str] = ""
    permit_number: Optional[str] = ""
    publication_date: Optional[str] = ""
    issue_date: Optional[str] = ""
    expected_execution_date: Optional[str] = ""
    connection_type: Optional[str] = ""  # نوع التوصيلة
    connections_count: Optional[str] = ""
    connection_length_without_extra: Optional[str] = ""
    connections_length_without_main: Optional[str] = ""
    network_diameter_63: Optional[str] = ""
    network_line_length: Optional[str] = ""
    network_diameter_16: Optional[str] = ""
    meter_number: Optional[str] = ""
    meter_type: Optional[str] = ""
    meter_removal_installation: Optional[str] = ""  # إزالة عداد وتركيب عداد جديد
    execution_date: Optional[str] = ""
    system_closing_date: Optional[str] = ""
    request_status: Optional[str] = "جديد"
    cancellation_date: Optional[str] = ""
    cancellation_reason: Optional[str] = ""
    images: List[str] = []


class WaterConnectionCreate(WaterConnectionBase):
    """Create water connection request"""
    pass


class WaterConnection(WaterConnectionBase):
    """Full water connection model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    created_by_name: Optional[str] = None


class SewageConnectionBase(BaseModel):
    """Base sewage connection fields"""
    project: str
    contractors: List[str] = []
    account_number: Optional[str] = ""
    request_number: Optional[str] = ""
    ccb_report_number: Optional[str] = ""
    customer_name: Optional[str] = ""
    phone_number: Optional[str] = ""
    area: Optional[str] = ""
    work_order_date: Optional[str] = ""
    connection_length: Optional[str] = ""
    notes: Optional[str] = ""
    latitude: Optional[str] = ""
    longitude: Optional[str] = ""
    commissioning_date: Optional[str] = ""
    permit_number: Optional[str] = ""
    publication_date: Optional[str] = ""
    issue_date: Optional[str] = ""
    expected_execution_date: Optional[str] = ""
    execution_date: Optional[str] = ""
    system_closing_date: Optional[str] = ""
    request_status: Optional[str] = "جديد"
    cancellation_date: Optional[str] = ""
    cancellation_reason: Optional[str] = ""
    images: List[str] = []


class SewageConnectionCreate(SewageConnectionBase):
    """Create sewage connection request"""
    pass


class SewageConnection(SewageConnectionBase):
    """Full sewage connection model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    created_by_name: Optional[str] = None
