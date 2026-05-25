# Governorates Routes
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime, timezone
import uuid

from ...services.auth_service import get_current_user
from ...database.mongodb import governorates_collection

router = APIRouter(prefix="/governorates", tags=["Governorates"])

@router.get("")
async def list_governorates(current_user = Depends(get_current_user)):
    """جلب قائمة المحافظات"""
    govs = await governorates_collection.find().to_list(100)
    return govs

@router.post("")
async def create_governorate(data: dict, current_user = Depends(get_current_user)):
    """إضافة محافظة جديدة"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية")
        
    data["id"] = str(uuid.uuid4())
    data["created_at"] = datetime.now(timezone.utc)
    await governorates_collection.insert_one(data)
    return data

@router.delete("/{gov_id}")
async def delete_governorate(gov_id: str, current_user = Depends(get_current_user)):
    """حذف محافظة"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية")
        
    result = await governorates_collection.delete_one({"id": gov_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="المحافظة غير موجودة")
    return {"message": "تم حذف المحافظة بنجاح"}
