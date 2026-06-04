import os

endpoints = """
# ========== Work Permits API ==========
@api_router.get("/work-permits")
async def get_work_permits(
    project: Optional[str] = None,
    governorate: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    user_doc = current_user if isinstance(current_user, dict) else current_user.dict()
    user_perms = set(user_doc.get("permissions", []))
    pp = user_doc.get("project_permissions", {})
    for plist in pp.values():
        user_perms.update(plist or [])
        
    if user_doc.get("role") != "admin" and "work_permits" not in user_perms:
        raise HTTPException(status_code=403, detail="لا تملك صلاحية عرض تصاريح العمل")
        
    query = {"is_deleted": {"$ne": True}}
    
    if user_doc.get("role") != "admin":
        user_govs = user_doc.get("governorates", [])
        user_projs = user_doc.get("projects", [])
        
        if governorate:
            gov_query = get_flexible_in_query([governorate], "governorate")
            query.update(gov_query)
        elif user_govs and "الكل" not in user_govs and "جميع المحافظات" not in user_govs:
            gov_query = get_flexible_in_query(user_govs, "governorate")
            query.update(gov_query)
            
        if project:
            proj_query = get_flexible_in_query([project], "project")
            query.update(proj_query)
        elif user_projs and "الكل" not in user_projs and "جميع المشاريع" not in user_projs:
            proj_query = get_flexible_in_query(user_projs, "project")
            query.update(proj_query)
            
    else:
        if governorate: query.update(get_flexible_in_query([governorate], "governorate"))
        if project: query.update(get_flexible_in_query([project], "project"))

    reports = await db.work_permits.find(query, {"_id": 0}).to_list(1000)
    # Reverse sort by created_at assuming natural insertion order
    reports.reverse()
    return reports

@api_router.post("/work-permits")
async def create_work_permit(data: dict, current_user: User = Depends(get_current_user)):
    user_doc = current_user if isinstance(current_user, dict) else current_user.dict()
    user_perms = set(user_doc.get("permissions", []))
    pp = user_doc.get("project_permissions", {})
    for plist in pp.values():
        user_perms.update(plist or [])
        
    if user_doc.get("role") != "admin" and "work_permits" not in user_perms:
        raise HTTPException(status_code=403, detail="لا تملك صلاحية اضافة تصاريح العمل")
        
    report_id = str(uuid.uuid4())
    data["id"] = report_id
    data["created_by"] = user_doc.get("name", "Unknown")
    data["created_at"] = datetime.now(timezone.utc).isoformat()
    data["status"] = "قيد المراجعة"
    data["is_deleted"] = False
    
    await db.work_permits.insert_one(data)
    return {"message": "Success", "id": report_id}

@api_router.put("/work-permits/{report_id}")
async def update_work_permit(report_id: str, data: dict, current_user: User = Depends(get_current_user)):
    user_doc = current_user if isinstance(current_user, dict) else current_user.dict()
    user_perms = set(user_doc.get("permissions", []))
    pp = user_doc.get("project_permissions", {})
    for plist in pp.values():
        user_perms.update(plist or [])
        
    is_admin = user_doc.get("role") == "admin"
    can_edit = "work_permits_edit" in user_perms
    can_review = user_doc.get("can_create_subusers") == True # Manager
    
    if not is_admin and not can_edit and not can_review and "work_permits" not in user_perms:
        raise HTTPException(status_code=403, detail="لا تملك الصلاحية")
        
    update_data = {k: v for k, v in data.items() if k not in ["id", "_id", "created_by", "created_at"]}
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    await db.work_permits.update_one({"id": report_id}, {"$set": update_data})
    return {"message": "Success"}

@api_router.delete("/work-permits/{report_id}")
async def delete_work_permit(report_id: str, current_user: User = Depends(get_current_user)):
    user_doc = current_user if isinstance(current_user, dict) else current_user.dict()
    user_perms = set(user_doc.get("permissions", []))
    pp = user_doc.get("project_permissions", {})
    for plist in pp.values():
        user_perms.update(plist or [])
        
    if user_doc.get("role") != "admin" and "work_permits_delete" not in user_perms and "work_permits" not in user_perms:
        raise HTTPException(status_code=403, detail="لا تملك الصلاحية")
        
    result = await db.work_permits.update_one(
        {"id": report_id},
        {"$set": {
            "is_deleted": True,
            "deleted_at": datetime.now(timezone.utc).isoformat(),
            "deleted_by": current_user.id
        }}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="غير موجود")
    return {"message": "Success"}

"""

def main():
    target = '    return {"message": "Success"}\n\n\n# ========== Trash Endpoints for Reports =========='
    
    with open('server.py', 'r', encoding='utf-8') as f:
        content = f.read()
        
    if "@api_router.get(\"/work-permits\")" not in content:
        content = content.replace(target, '    return {"message": "Success"}\n\n' + endpoints + '\n# ========== Trash Endpoints for Reports ==========')
        with open('server.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Injected endpoints successfully!")
    else:
        print("Endpoints already exist!")
        
    import shutil
    if os.path.exists('server_recovered.py'):
        shutil.copy('server.py', 'server_recovered.py')

if __name__ == "__main__":
    main()
