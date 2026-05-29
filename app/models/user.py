"""
User Model
نموذج المستخدم
"""
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import List, Optional
from datetime import datetime, timezone
import uuid


class UserBase(BaseModel):
    """Base user fields"""
    username: str
    email: Optional[EmailStr] = None
    full_name: str
    title: Optional[str] = None
    profile_picture: Optional[str] = None
    role: str = "user"
    governorates: List[str] = []
    projects: List[str] = []
    can_create_subusers: bool = True
    permissions: List[str] = []
    project_permissions: Optional[dict] = None
    connection_permissions: Optional[dict] = None
    is_active: bool = True


class UserCreate(UserBase):
    """Create user request"""
    password: str


class UserUpdate(BaseModel):
    """Update user request"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    title: Optional[str] = None
    profile_picture: Optional[str] = None
    governorates: Optional[List[str]] = None
    projects: Optional[List[str]] = None
    can_create_subusers: Optional[bool] = None
    permissions: Optional[List[str]] = None
    project_permissions: Optional[dict] = None
    connection_permissions: Optional[dict] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class User(UserBase):
    """Full user model with ID and timestamps"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    hashed_password: str
    created_by: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserResponse(BaseModel):
    """User response without sensitive data"""
    id: str
    username: str
    email: Optional[str] = None
    full_name: str
    title: Optional[str] = None
    profile_picture: Optional[str] = None
    role: str
    governorates: List[str] = []
    projects: List[str] = []
    can_create_subusers: bool = True
    permissions: List[str] = []
    project_permissions: Optional[dict] = None
    connection_permissions: Optional[dict] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    created_by: Optional[str] = None


class Token(BaseModel):
    """JWT Token response"""
    access_token: str
    token_type: str = "bearer"


class TokenResponse(BaseModel):
    """Token response with user data"""
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    """JWT Token payload"""
    sub: Optional[str] = None
    exp: Optional[datetime] = None


class LoginRequest(BaseModel):
    """Login request"""
    username: str
    password: str


class ChangePasswordRequest(BaseModel):
    """Change password request"""
    current_password: str
    new_password: str


class ResetPasswordRequest(BaseModel):
    """Reset password request"""
    email: EmailStr


class VerifyResetCodeRequest(BaseModel):
    """Verify reset code request"""
    email: EmailStr
    code: str
    new_password: str


class PermissionsUpdate(BaseModel):
    """Permissions update request"""
    permissions: List[str]
    project_permissions: Optional[dict] = None
    connection_permissions: Optional[dict] = None
    projects: Optional[List[str]] = None
