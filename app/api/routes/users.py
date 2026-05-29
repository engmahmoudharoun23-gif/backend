# User Routes
from fastapi import APIRouter, HTTPException, Depends
from typing import List

from ...models.user import User, UserCreate, UserUpdate, UserResponse, PermissionsUpdate
from ...services.auth_service import get_current_user
from ...services.user_service import (
    get_all_users, get_user_by_id, create_user, update_user, delete_user,
    toggle_user_active, update_user_permissions
)
from ...config.settings import ALL_PERMISSIONS

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=List[UserResponse])
async def list_users(current_user: User = Depends(get_current_user)):
    """جلب قائمة المستخدمين"""
    users = await get_all_users(current_user)
    return [UserResponse(**user) for user in users]

@router.post("", response_model=UserResponse)
async def create_new_user(user_data: UserCreate, current_user: User = Depends(get_current_user)):
    """إنشاء مستخدم جديد"""
    # Check if user can create subusers
    if not current_user.can_create_subusers and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية إنشاء مستخدمين")
    
    try:
        user = await create_user(user_data, current_user.id)
        return UserResponse(**user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, current_user: User = Depends(get_current_user)):
    """جلب بيانات مستخدم معين"""
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    return UserResponse(**user)

@router.put("/{user_id}", response_model=UserResponse)
async def update_existing_user(user_id: str, user_data: UserUpdate, current_user: User = Depends(get_current_user)):
    """تحديث بيانات مستخدم"""
    user = await update_user(user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    return UserResponse(**user)

@router.delete("/{user_id}")
async def delete_existing_user(user_id: str, current_user: User = Depends(get_current_user)):
    """حذف مستخدم"""
    success = await delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    return {"message": "تم حذف المستخدم بنجاح"}

@router.put("/{user_id}/toggle-active")
async def toggle_active(user_id: str, current_user: User = Depends(get_current_user)):
    """تفعيل/تعطيل المستخدم"""
    user = await toggle_user_active(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    return {"message": "تم تحديث حالة المستخدم", "is_active": user.get("is_active")}

@router.put("/{user_id}/permissions")
async def update_permissions(user_id: str, permissions_data: PermissionsUpdate, current_user: User = Depends(get_current_user)):
    """تحديث صلاحيات المستخدم"""
    user = await update_user_permissions(user_id, permissions_data.model_dump(exclude_unset=True))
    if not user:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    return {"message": "تم تحديث الصلاحيات بنجاح"}

@router.get("/permissions/all")
async def get_all_available_permissions(current_user: User = Depends(get_current_user)):
    """جلب قائمة الصلاحيات المتاحة"""
    return ALL_PERMISSIONS
