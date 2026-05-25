# Projects Routes
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime, timezone
import uuid

from ...services.auth_service import get_current_user
from ...database.mongodb import projects_collection

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("")
async def list_projects(current_user = Depends(get_current_user)):
    """جلب قائمة المشاريع"""
    projects = await projects_collection.find().to_list(100)
    return projects

@router.post("")
async def create_project(data: dict, current_user = Depends(get_current_user)):
    """إنشاء مشروع جديد"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية")
        
    data["id"] = str(uuid.uuid4())
    data["created_at"] = datetime.now(timezone.utc)
    await projects_collection.insert_one(data)
    return data

@router.delete("/{project_id}")
async def delete_project(project_id: str, current_user = Depends(get_current_user)):
    """حذف مشروع"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية")
        
    result = await projects_collection.delete_one({"id": project_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="المشروع غير موجود")
    return {"message": "تم حذف المشروع بنجاح"}
