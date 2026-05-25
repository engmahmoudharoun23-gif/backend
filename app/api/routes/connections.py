# Connections Routes (Water & Sewage)
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime, timezone
import uuid

from ...services.auth_service import get_current_user
from ...database.mongodb import water_connections_collection, sewage_connections_collection

router = APIRouter(tags=["Connections"])

@router.get("/water-connections")
async def list_water_connections(
    project: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """جلب قائمة توصيلات المياه"""
    query = {}
    if project:
        query["project"] = project
    
    connections = await water_connections_collection.find(query).sort("created_at", -1).to_list(1000)
    return connections

@router.get("/sewage-connections")
async def list_sewage_connections(
    project: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """جلب قائمة توصيلات الصرف الصحي"""
    query = {}
    if project:
        query["project"] = project
    
    connections = await sewage_connections_collection.find(query).sort("created_at", -1).to_list(1000)
    return connections

@router.post("/water-connections")
async def create_water_connection(data: dict, current_user = Depends(get_current_user)):
    """إضافة توصيلة مياه جديدة"""
    data["id"] = str(uuid.uuid4())
    data["created_at"] = datetime.now(timezone.utc)
    data["created_by"] = current_user.id
    await water_connections_collection.insert_one(data)
    return data

@router.post("/sewage-connections")
async def create_sewage_connection(data: dict, current_user = Depends(get_current_user)):
    """إضافة توصيلة صرف صحي جديدة"""
    data["id"] = str(uuid.uuid4())
    data["created_at"] = datetime.now(timezone.utc)
    data["created_by"] = current_user.id
    await sewage_connections_collection.insert_one(data)
    return data
