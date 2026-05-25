# Reports Routes
from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File, Form
from typing import List, Optional
from datetime import datetime, timezone
import uuid
import os

from ...models.report import Report, ReportResponse, ReportCreate, ReportUpdate
from ...services.auth_service import get_current_user
from ...database.mongodb import db, reports_collection

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("", response_model=List[ReportResponse])
async def list_reports(
    project: Optional[str] = None,
    governorate: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 1000,
    current_user = Depends(get_current_user)
):
    """جلب قائمة البلاغات"""
    query = {"is_deleted": {"$ne": True}}
    if project:
        query["project"] = project
    if governorate:
        query["governorate"] = governorate
    if status:
        query["status"] = status
        
    # User permissions filter
    if current_user.role != "admin" and "all_projects" not in current_user.permissions:
        if current_user.projects:
            query["project"] = {"$in": current_user.projects}
        if current_user.governorates:
            query["governorate"] = {"$in": current_user.governorates}
            
    reports = await reports_collection.find(query).sort("created_at", -1).to_list(limit)
    return reports

@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(report_id: str, current_user = Depends(get_current_user)):
    """جلب بيانات بلاغ معين"""
    report = await reports_collection.find_one({"id": report_id, "is_deleted": {"$ne": True}})
    if not report:
        raise HTTPException(status_code=404, detail="البلاغ غير موجود")
    return report

@router.post("", response_model=ReportResponse)
async def create_report(
    project: str = Form(...),
    governorate: str = Form(...),
    report_type: str = Form(...),
    area: Optional[str] = Form(None),
    description: Optional[str] = Form(""),
    notes: Optional[str] = Form(""),
    latitude: Optional[str] = Form(None),
    longitude: Optional[str] = Form(None),
    images: List[UploadFile] = File([]),
    current_user = Depends(get_current_user)
):
    """إنشاء بلاغ جديد"""
    # Simple image saving (mocked for now)
    image_paths = []
    # In a real app, we'd save the files to disk/S3
    
    report_dict = {
        "id": str(uuid.uuid4()),
        "project": project,
        "governorate": governorate,
        "report_type": report_type,
        "area": area,
        "description": description,
        "notes": notes,
        "latitude": latitude,
        "longitude": longitude,
        "images": image_paths,
        "status": "pending",
        "created_at": datetime.now(timezone.utc),
        "created_by": current_user.id,
        "created_by_name": current_user.full_name,
        "is_deleted": False,
        "seen_by": [current_user.id]
    }
    
    await reports_collection.insert_one(report_dict)
    return report_dict

@router.delete("/{report_id}")
async def delete_report(report_id: str, current_user = Depends(get_current_user)):
    """حذف بلاغ (Soft Delete)"""
    result = await reports_collection.update_one(
        {"id": report_id},
        {"$set": {
            "is_deleted": True,
            "deleted_at": datetime.now(timezone.utc),
            "deleted_by": current_user.id
        }}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="البلاغ غير موجود")
    return {"message": "تم حذف البلاغ بنجاح"}

@router.get("/stats")
async def get_report_stats(
    project: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """إحصائيات البلاغات"""
    query = {"is_deleted": False}
    if project:
        query["project"] = project
        
    pipeline = [
        {"$match": query},
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]
    
    stats = await reports_collection.aggregate(pipeline).to_list(None)
    result = {s["_id"]: s["count"] for s in stats}
    return result
