import re

def main():
    with open('server.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Add permissions
    if '"work_permits"' not in content:
        perm_target = '{"key": "business_reports_delete", "label": "حذف تقرير الأعمال", "group": "التقارير"},'
        perm_replacement = perm_target + '''
    {"key": "work_permits", "label": "تصاريح العمل", "group": "التقارير"},
    {"key": "work_permits_edit", "label": "تعديل تصريح العمل", "group": "التقارير"},
    {"key": "work_permits_delete", "label": "حذف تصريح العمل", "group": "التقارير"},'''
        content = content.replace(perm_target, perm_replacement)
        
        # Add to SUPER_ADMIN_PERMISSIONS list (usually around line 513)
        super_admin_target = '\"business_reports_delete\", \"business_reports_review\", \"consultant_close\"'
        if super_admin_target in content:
            super_admin_replacement = super_admin_target + ', "work_permits", "work_permits_edit", "work_permits_delete"'
            content = content.replace(super_admin_target, super_admin_replacement)

    # 2. Add Endpoints by duplicating safety_reports
    # We will find the safety_reports block from get_safety_reports to delete_safety_report
    # and duplicate it for work_permits
    
    if 'def get_work_permits' not in content:
        # Regex to capture the block
        # Look for @api_router.get("/safety-reports") and end at the end of delete_safety_report
        # Actually it's safer to just inject a new block of code.
        
        injection_point = "def get_safety_reports_trash"
        
        work_permits_code = """
# ==========================================
# WORK PERMITS
# ==========================================

@api_router.get("/work-permits")
async def get_work_permits(
    project: str = Query(None),
    governorate: str = Query(None),
    date: str = Query(None),
    current_user: User = Depends(get_current_user)
):
    user_doc = await db.users.find_one({"id": current_user.id})
    user_perms = user_doc.get("permissions", [])
    if user_doc.get("role") != "admin" and "work_permits" not in user_perms:
        raise HTTPException(status_code=403, detail="لا تملك صلاحية عرض تصاريح العمل")

    query = {"is_deleted": {"$ne": True}}
    
    if project: query["project"] = project
    if governorate: query["governorate"] = governorate
    if date: query["date"] = date

    if user_doc.get("role") != "admin":
        allowed_projects = get_projects_with_permission(current_user, "work_permits")
        if not allowed_projects: return []
        if allowed_projects[0] != "all":
            if "project" in query and query["project"] not in allowed_projects:
                return []
            if "project" not in query:
                query["project"] = {"$in": allowed_projects}

    records = await db.work_permits.find(query, {"_id": 0}).sort("date", -1).to_list(500)
    return records

@api_router.post("/work-permits")
async def create_work_permit(request: Request, current_user: User = Depends(get_current_user)):
    user_doc = await db.users.find_one({"id": current_user.id})
    user_perms = user_doc.get("permissions", [])
    if user_doc.get("role") != "admin" and "work_permits" not in user_perms:
        raise HTTPException(status_code=403, detail="لا تملك صلاحية الإضافة")

    data = await request.json()
    record = {
        "id": str(uuid.uuid4()),
        "date": data.get("date"),
        "governorate": data.get("governorate"),
        "project": data.get("project"),
        "notes": data.get("notes", ""),
        "file_url": data.get("file_url", ""),
        "added_by": current_user.id,
        "added_by_name": current_user.full_name or current_user.username,
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    await db.work_permits.insert_one(record)
    return record

@api_router.put("/work-permits/{permit_id}")
async def update_work_permit(permit_id: str, request: Request, current_user: User = Depends(get_current_user)):
    user_doc = await db.users.find_one({"id": current_user.id})
    user_perms = user_doc.get("permissions", [])
    if user_doc.get("role") != "admin" and "work_permits" not in user_perms:
        raise HTTPException(status_code=403, detail="لا تملك صلاحية التعديل")

    data = await request.json()
    update_data = {}
    if "date" in data: update_data["date"] = data["date"]
    if "governorate" in data: update_data["governorate"] = data["governorate"]
    if "project" in data: update_data["project"] = data["project"]
    if "notes" in data: update_data["notes"] = data["notes"]
    if "file_url" in data: update_data["file_url"] = data["file_url"]

    if update_data:
        await db.work_permits.update_one({"id": permit_id}, {"$set": update_data})
    
    return {"status": "success"}

@api_router.delete("/work-permits/{permit_id}")
async def delete_work_permit(permit_id: str, current_user: User = Depends(get_current_user)):
    user_doc = await db.users.find_one({"id": current_user.id})
    user_perms = user_doc.get("permissions", [])
    if user_doc.get("role") != "admin" and "work_permits" not in user_perms:
        raise HTTPException(status_code=403, detail="لا تملك صلاحية الحذف")

    result = await db.work_permits.update_one(
        {"id": permit_id}, 
        {"$set": {"is_deleted": True, "deleted_by": current_user.id, "deleted_at": datetime.datetime.utcnow().isoformat()}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="غير موجود")
    return {"status": "deleted"}

@api_router.get("/trash/work-permits")
"""
        content = content.replace("@api_router.get(\"/trash/safety-reports\")", work_permits_code + "\n@api_router.get(\"/trash/safety-reports\")")

    # Add work_permits to Trash routes
    if 'def get_work_permits_trash' not in content:
        trash_code = """
@api_router.get("/trash/work-permits")
async def get_work_permits_trash(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin": raise HTTPException(status_code=403)
    return await db.work_permits.find({"is_deleted": True}, {"_id": 0}).sort("deleted_at", -1).to_list(500)

@api_router.put("/trash/work-permits/{permit_id}/restore")
async def restore_work_permits_trash(permit_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin": raise HTTPException(status_code=403)
    await db.work_permits.update_one({"id": permit_id}, {"$unset": {"is_deleted": "", "deleted_by": "", "deleted_at": ""}})
    return {"status": "restored"}

@api_router.delete("/trash/work-permits/{permit_id}/permanent")
async def permanent_work_permits_trash(permit_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin": raise HTTPException(status_code=403)
    await db.work_permits.delete_one({"id": permit_id, "is_deleted": True})
    return {"status": "deleted"}
"""
        content = content.replace("async def get_safety_reports_trash", trash_code + "\nasync def get_safety_reports_trash")

    # Inject into get_all_trash mapping
    if '"work_permit": (db.work_permits' not in content:
        target1 = '"safety_report": (db.safety_reports, "safety_report", "تقرير سلامة"),'
        content = content.replace(target1, target1 + '\n            "work_permit": (db.work_permits, "work_permit", "تصريح عمل"),')

        target2 = '"safety_report": db.safety_reports,'
        content = content.replace(target2, target2 + '\n        "work_permit": db.work_permits,')

    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(content)

    print("server.py updated successfully.")

if __name__ == "__main__":
    main()
