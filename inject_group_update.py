import os

SERVER_PATH = "d:/sery17-main/sery17-main/backend/server.py"

with open(SERVER_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update get_chat_contacts return dictionary to include members and created_by
old_return = '        "is_group": c.get("is_group", False)\n    } for c in unique_contacts]'
new_return = '        "is_group": c.get("is_group", False),\n        "members": c.get("members", []),\n        "created_by": c.get("created_by")\n    } for c in unique_contacts]'

if '"members": c.get("members", [])' not in content:
    content = content.replace(old_return, new_return)

# 2. Add PUT /chat/v2/groups/{group_id} endpoint
if "@api_router.put(\"/chat/v2/groups/{group_id}\")" not in content:
    put_endpoint = """
@api_router.put("/chat/v2/groups/{group_id}")
async def update_chat_group(group_id: str, payload: dict, current_user: User = Depends(get_current_user)):
    group = await db.chat_groups.find_one({"id": group_id})
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
        
    # Only creator or admin can update
    if group.get("created_by") != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to edit this group")
        
    update_data = {}
    if payload.get("name"):
        update_data["name"] = payload.get("name")
    if payload.get("members") is not None:
        members = payload.get("members")
        if current_user.id not in members:
            members.append(current_user.id)
        update_data["members"] = members
        
    if update_data:
        await db.chat_groups.update_one({"id": group_id}, {"$set": update_data})
        
    return {"message": "Group updated"}
"""
    content = content.replace('@api_router.post("/chat/v2/groups")', put_endpoint + '\n@api_router.post("/chat/v2/groups")')

with open(SERVER_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Group update endpoints injected successfully")
