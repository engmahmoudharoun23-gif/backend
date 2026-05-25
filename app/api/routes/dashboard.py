# Dashboard and Notifications Routes
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from datetime import datetime, timezone

from ...services.auth_service import get_current_user
from ...database.mongodb import reports_collection, invoices_collection, employee_requests_collection

router = APIRouter(tags=["Dashboard"])

@router.get("/dashboard/stats")
async def get_dashboard_stats(
    project: Optional[str] = None,
    month: Optional[str] = None,
    year: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """إحصائيات لوحة التحكم"""
    query = {"is_deleted": {"$ne": True}}
    if project:
        query["project"] = project
        
    # Basic counts
    reports_count = await reports_collection.count_documents(query)
    
    # Invoices summary
    invoice_query = {}
    if project:
        invoice_query["project"] = project
    invoices_count = await invoices_collection.count_documents(invoice_query)
    
    return {
        "reports_count": reports_count,
        "invoices_count": invoices_count,
        "pending_requests": await employee_requests_collection.count_documents({"status": "pending"})
    }

@router.get("/notifications/pending-count")
async def get_pending_count(current_user = Depends(get_current_user)):
    """عدد الإشعارات المعلقة"""
    # Simply return count of pending invoices and requests if user is admin
    if current_user.role == "admin":
        invoices = await invoices_collection.count_documents({"status": "pending"})
        requests = await employee_requests_collection.count_documents({"status": "pending"})
        return {"count": invoices + requests}
    return {"count": 0}
