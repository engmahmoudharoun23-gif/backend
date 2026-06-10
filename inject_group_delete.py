import os

SERVER_PATH = "d:/sery17-main/sery17-main/backend/server.py"

with open(SERVER_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Add DELETE /chat/v2/groups/{group_id} endpoint
if "@api_router.delete(\"/chat/v2/groups/{group_id}\")" not in content:
    delete_endpoint = """
@api_router.delete("/chat/v2/groups/{group_id}")
async def delete_chat_group(group_id: str, current_user: User = Depends(get_current_user)):
    group = await db.chat_groups.find_one({"id": group_id})
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
        
    # Only creator can delete
    if group.get("created_by") != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this group")
        
    # Delete the group
    await db.chat_groups.delete_one({"id": group_id})
    
    # Optionally delete all messages in this group
    await db.chat_messages.delete_many({"receiver_id": group_id})
        
    return {"message": "Group deleted successfully"}
"""
    content = content.replace('@api_router.post("/chat/v2/groups")', delete_endpoint + '\n@api_router.post("/chat/v2/groups")')

with open(SERVER_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Group delete endpoint injected successfully")
