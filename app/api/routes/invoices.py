# Invoices Routes
from fastapi import APIRouter, HTTPException, Depends, Form, File, UploadFile
from typing import List, Optional
from datetime import datetime, timezone
import uuid

from ...services.auth_service import get_current_user
from ...database.mongodb import invoices_collection

router = APIRouter(prefix="/invoices", tags=["Invoices"])

@router.get("")
async def list_invoices(
    project: Optional[str] = None,
    status: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """جلب قائمة الفواتير"""
    query = {}
    if project:
        query["project"] = project
    if status:
        query["status"] = status
        
    # Permission filter
    if current_user.role != "admin" and "view_all_invoices" not in current_user.permissions:
        query["uploaded_by"] = current_user.id
        
    invoices = await invoices_collection.find(query).sort("created_at", -1).to_list(1000)
    return invoices

@router.post("")
async def create_invoice(
    project: str = Form(...),
    amount: float = Form(...),
    description: Optional[str] = Form(""),
    files: List[UploadFile] = File([]),
    current_user = Depends(get_current_user)
):
    """رفع فاتورة جديدة"""
    invoice_dict = {
        "id": str(uuid.uuid4()),
        "project": project,
        "amount": amount,
        "description": description,
        "status": "pending",
        "uploaded_by": current_user.id,
        "uploaded_by_name": current_user.full_name,
        "created_at": datetime.now(timezone.utc),
        "files": [] # In a real app, save files to disk
    }
    await invoices_collection.insert_one(invoice_dict)
    return invoice_dict

@router.post("/{invoice_id}/approve")
async def approve_invoice(invoice_id: str, current_user = Depends(get_current_user)):
    """اعتماد فاتورة"""
    if current_user.role != "admin" and "review_invoices" not in current_user.permissions:
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية")
        
    result = await invoices_collection.update_one(
        {"id": invoice_id},
        {"$set": {"status": "approved", "approved_by": current_user.id, "approved_at": datetime.now(timezone.utc)}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="الفاتورة غير موجودة")
    return {"message": "تم اعتماد الفاتورة بنجاح"}
