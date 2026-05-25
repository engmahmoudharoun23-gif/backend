# Authentication Routes
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone

from ...models.user import LoginRequest, TokenResponse, UserResponse
from ...services.auth_service import authenticate_user, create_access_token, get_current_user
from ...database.mongodb import db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    """تسجيل الدخول"""
    user = await authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="اسم المستخدم أو كلمة المرور غير صحيحة")
    
    # Create token
    access_token = create_access_token(data={"sub": user["username"]})
    
    # Prepare user response (without sensitive data)
    user_response = {
        "id": user.get("id"),
        "username": user.get("username"),
        "full_name": user.get("full_name"),
        "title": user.get("title"),
        "role": user.get("role", "user"),
        "projects": user.get("projects", []),
        "governorates": user.get("governorates", []),
        "permissions": user.get("permissions", []),
        "can_create_subusers": user.get("can_create_subusers", False),
        "is_active": user.get("is_active", True),
        "profile_picture": user.get("profile_picture"),
    }
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_response
    }

@router.get("/me", response_model=UserResponse)
async def get_me(current_user = Depends(get_current_user)):
    """الحصول على بيانات المستخدم الحالي"""
    return UserResponse(**current_user.model_dump())
