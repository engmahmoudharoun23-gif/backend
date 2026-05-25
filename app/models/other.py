"""
Other Models - نماذج أخرى
MongoDB schemas for support, invoices, contractors, etc.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# ============= Support Messages =============
class SupportMessage(BaseModel):
    """نموذج رسالة الدعم الفني"""
    id: str
    sender_id: str
    sender_name: str
    receiver_id: str
    message: str
    is_read: bool = False
    is_from_admin: bool = False
    created_at: Optional[datetime] = None


class SupportMessageCreate(BaseModel):
    """نموذج إنشاء رسالة دعم"""
    receiver_id: str
    message: str


class SupportMessageResponse(BaseModel):
    """نموذج استجابة رسالة الدعم"""
    id: str
    sender_id: str
    sender_name: str
    receiver_id: str
    message: str
    is_read: bool
    is_from_admin: bool
    created_at: Optional[datetime] = None


# ============= Invoices (فواتير العهدة) =============
class Invoice(BaseModel):
    """نموذج فاتورة العهدة"""
    id: str
    invoice_number: str
    governorate: str
    project: str
    amount: float
    description: Optional[str] = None
    status: str = "pending"  # pending, paid, cancelled
    due_date: Optional[datetime] = None
    paid_date: Optional[datetime] = None
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    is_deleted: bool = False


class InvoiceCreate(BaseModel):
    """نموذج إنشاء فاتورة"""
    invoice_number: str
    governorate: str
    project: str
    amount: float
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class InvoiceUpdate(BaseModel):
    """نموذج تحديث فاتورة"""
    invoice_number: Optional[str] = None
    governorate: Optional[str] = None
    project: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None
    paid_date: Optional[datetime] = None


# ============= Contractors (المقاولين) =============
class Contractor(BaseModel):
    """نموذج المقاول"""
    id: str
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    is_active: bool = True


class ContractorCreate(BaseModel):
    """نموذج إنشاء مقاول"""
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None


class ContractorResponse(BaseModel):
    """نموذج استجابة المقاول"""
    id: str
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    is_active: bool = True


# ============= Team Members (أعضاء الفريق) =============
class TeamMember(BaseModel):
    """نموذج عضو الفريق"""
    id: str
    name: str
    role: str
    phone: Optional[str] = None
    email: Optional[str] = None
    is_active: bool = True


class TeamMemberCreate(BaseModel):
    """نموذج إنشاء عضو فريق"""
    name: str
    role: str
    phone: Optional[str] = None
    email: Optional[str] = None


class TeamMemberResponse(BaseModel):
    """نموذج استجابة عضو الفريق"""
    id: str
    name: str
    role: str
    phone: Optional[str] = None
    email: Optional[str] = None
    is_active: bool = True


# ============= Cars (السيارات) =============
class CarCreate(BaseModel):
    """نموذج إنشاء سيارة"""
    plate_number: str
    car_type: str
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    status: str = "available"


class CarUpdate(BaseModel):
    """نموذج تحديث سيارة"""
    plate_number: Optional[str] = None
    car_type: Optional[str] = None
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    status: Optional[str] = None


class CarResponse(BaseModel):
    """نموذج استجابة السيارة"""
    id: str
    plate_number: str
    car_type: str
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None


# ============= Project Cards =============
class CardItem(BaseModel):
    """نموذج عنصر البطاقة"""
    id: str
    label: str
    value: str
    color: Optional[str] = None


class ProjectCards(BaseModel):
    """نموذج بطاقات المشروع"""
    project: str
    cards: List[CardItem]


class CardItemCreate(BaseModel):
    """نموذج إنشاء عنصر بطاقة"""
    label: str


class CardItemUpdate(BaseModel):
    """نموذج تحديث عنصر بطاقة"""
    label: str
