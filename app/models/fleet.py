"""
Fleet Models (Cars and Maintenance)
نماذج السيارات والصيانة
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime, timezone
import uuid


class CarBase(BaseModel):
    """Base car fields"""
    plate_number: str
    brand: Optional[str] = ""
    model: Optional[str] = ""
    year: Optional[str] = ""
    color: Optional[str] = ""
    chassis_number: Optional[str] = ""
    driver_name: Optional[str] = ""
    driver_phone: Optional[str] = ""
    project: Optional[str] = ""
    notes: Optional[str] = ""
    images: List[str] = []


class CarCreate(CarBase):
    """Create car request"""
    pass


class CarUpdate(BaseModel):
    """Update car request"""
    plate_number: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[str] = None
    color: Optional[str] = None
    chassis_number: Optional[str] = None
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    project: Optional[str] = None
    notes: Optional[str] = None
    images: Optional[List[str]] = None


class Car(CarBase):
    """Full car model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None


class MaintenanceRecordBase(BaseModel):
    """Base maintenance record fields"""
    car_id: str
    maintenance_type: str
    description: Optional[str] = ""
    cost: Optional[float] = 0
    mileage: Optional[str] = ""
    workshop: Optional[str] = ""
    notes: Optional[str] = ""
    images: List[str] = []
    maintenance_date: Optional[str] = ""


class MaintenanceRecordCreate(MaintenanceRecordBase):
    """Create maintenance record request"""
    pass


class MaintenanceRecordUpdate(BaseModel):
    """Update maintenance record request"""
    maintenance_type: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[float] = None
    mileage: Optional[str] = None
    workshop: Optional[str] = None
    notes: Optional[str] = None
    images: Optional[List[str]] = None
    maintenance_date: Optional[str] = None


class MaintenanceRecord(MaintenanceRecordBase):
    """Full maintenance record model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    created_by_name: Optional[str] = None
