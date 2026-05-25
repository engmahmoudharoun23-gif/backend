# Employee Requests Routes
from fastapi import APIRouter, HTTPException, Depends, Form
from typing import List, Optional
from datetime import datetime, timezone
import uuid

from ...services.auth_service import get_current_user
from ...database.mongodb import employee_requests_collection

router = APIRouter(prefix="/employee-requests", tags=["Employee Requests"])

@router.get("")
async def list_requests(
    status: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """جلب قائمة طلبات الموظفين"""
    query = {}
    if status:
        query["status"] = status
        
    # Permission filter
    if current_user.role != "admin" and "view_all_employee_requests" not in current_user.permissions:
        query["uploaded_by"] = current_user.id
        
    requests = await employee_requests_collection.find(query).sort("created_at", -1).to_list(1000)
    return requests

@router.post("")
async def create_request(
    request_type: str = Form(...),
    description: str = Form(...),
    current_user = Depends(get_current_user)
):
    """إنشاء طلب جديد"""
    req_dict = {
        "id": str(uuid.uuid4()),
        "request_type": request_type,
        "description": description,
        "status": "pending",
        "uploaded_by": current_user.id,
        "uploaded_by_name": current_user.full_name,
        "created_at": datetime.now(timezone.utc)
    }
    await employee_requests_collection.insert_one(req_dict)
    return req_dict

@router.post("/{request_id}/approve")
async def approve_request(request_id: str, current_user = Depends(get_current_user)):
    """اعتماد طلب"""
    if current_user.role != "admin" and "review_employee_requests" not in current_user.permissions:
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية")
        
    result = await employee_requests_collection.update_one(
        {"id": request_id},
        {"$set": {"status": "approved", "approved_by": current_user.id, "approved_at": datetime.now(timezone.utc)}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="الطلب غير موجود")
    return {"message": "تم اعتماد الطلب بنجاح"}
