"""
Models Package
تصدير جميع النماذج
"""
from .user import (
    User, UserCreate, UserUpdate, UserResponse, UserBase,
    Token, TokenData, LoginRequest,
    ChangePasswordRequest, ResetPasswordRequest, VerifyResetCodeRequest
)
from .report import (
    Report, ReportCreate, ReportUpdate, ReportResponse, ReportBase,
    ReportType, ReportTypeCreate
)
from .invoice import (
    Invoice, InvoiceCreate, InvoiceUpdate, InvoiceResponse, InvoiceBase,
    RejectRequest, CancelRequest
)
from .employee_request import (
    EmployeeRequest, EmployeeRequestCreate, EmployeeRequestUpdate, EmployeeRequestResponse, EmployeeRequestBase
)
from .connection import (
    WaterConnection, WaterConnectionCreate, WaterConnectionBase,
    SewageConnection, SewageConnectionCreate, SewageConnectionBase
)
from .extract import (
    Extract, ExtractCreate, ExtractUpdate, ExtractResponse, ExtractBase
)
from .fleet import (
    Car, CarCreate, CarUpdate, CarBase,
    MaintenanceRecord, MaintenanceRecordCreate, MaintenanceRecordUpdate, MaintenanceRecordBase
)
from .common import (
    Contractor, ContractorCreate, ContractorBase,
    Governorate, GovernorateCreate, GovernorateBase,
    Area, AreaCreate, AreaBase,
    Project, ProjectCreate, ProjectBase,
    SupportMessage, ChatMessage
)

__all__ = [
    # User models
    "User", "UserCreate", "UserUpdate", "UserResponse", "UserBase",
    "Token", "TokenData", "LoginRequest",
    "ChangePasswordRequest", "ResetPasswordRequest", "VerifyResetCodeRequest",
    
    # Report models
    "Report", "ReportCreate", "ReportUpdate", "ReportResponse", "ReportBase",
    "ReportType", "ReportTypeCreate",
    
    # Invoice models
    "Invoice", "InvoiceCreate", "InvoiceUpdate", "InvoiceResponse", "InvoiceBase",
    "RejectRequest", "CancelRequest",
    
    # Employee request models
    "EmployeeRequest", "EmployeeRequestCreate", "EmployeeRequestUpdate", "EmployeeRequestResponse", "EmployeeRequestBase",
    
    # Connection models
    "WaterConnection", "WaterConnectionCreate", "WaterConnectionBase",
    "SewageConnection", "SewageConnectionCreate", "SewageConnectionBase",
    
    # Extract models
    "Extract", "ExtractCreate", "ExtractUpdate", "ExtractResponse", "ExtractBase",
    
    # Fleet models
    "Car", "CarCreate", "CarUpdate", "CarBase",
    "MaintenanceRecord", "MaintenanceRecordCreate", "MaintenanceRecordUpdate", "MaintenanceRecordBase",
    
    # Common models
    "Contractor", "ContractorCreate", "ContractorBase",
    "Governorate", "GovernorateCreate", "GovernorateBase",
    "Area", "AreaCreate", "AreaBase",
    "Project", "ProjectCreate", "ProjectBase",
    "SupportMessage", "ChatMessage",
]
