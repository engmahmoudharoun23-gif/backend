import os

SERVER_PATH = "d:/sery17-main/sery17-main/backend/server.py"

with open(SERVER_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add /chat/v2/groups endpoint
if "@api_router.post(\"/chat/v2/groups\")" not in content:
    group_endpoint = """
@api_router.post("/chat/v2/groups")
async def create_chat_group(payload: dict, current_user: User = Depends(get_current_user)):
    if not payload.get("name") or not payload.get("members"):
        raise HTTPException(status_code=400, detail="Name and members are required")
    
    group_id = f"group_{str(uuid.uuid4())[:8]}"
    members = payload.get("members")
    if current_user.id not in members:
        members.append(current_user.id)
        
    new_group = {
        "id": group_id,
        "name": payload.get("name"),
        "created_by": current_user.id,
        "members": members,
        "created_at": datetime.utcnow(),
        "is_group": True
    }
    await db.chat_groups.insert_one(new_group)
    new_group["_id"] = str(new_group["_id"])
    new_group["created_at"] = new_group["created_at"].isoformat()
    return {"message": "Group created", "group": new_group}
"""
    content = content.replace('@api_router.get("/chat/v2/contacts")', group_endpoint + '\n@api_router.get("/chat/v2/contacts")')

# 2. Add groups to get_chat_contacts
if "await db.chat_groups.find" not in content:
    contact_injection = """
    # Fetch groups
    groups = await db.chat_groups.find({"members": current_user.id}).to_list(100)
    for g in groups:
        g["unread_count"] = 0 # simplified for groups
        g["full_name"] = g.get("name")
        g["is_group"] = True
        
        last_msg = await db.chat_messages.find_one({
            "receiver_id": g["id"],
            "is_deleted": False
        }, sort=[("created_at", -1)])
        
        if last_msg:
            sender = await db.users.find_one({"id": last_msg["sender_id"]}, {"full_name": 1, "username": 1})
            sender_name = sender.get("full_name") or sender.get("username") if sender else "Unknown"
            g["last_message"] = f"{sender_name}: {last_msg.get('text', 'مرفق')}"
            g["last_message_time"] = last_msg.get("created_at")
        else:
            g["last_message"] = "بدأت المجموعة"
            g["last_message_time"] = g.get("created_at")
                
        unique_contacts.append(g)
"""
    target_str = '    unique_contacts.sort(key=lambda x: x.get("last_message_time") or datetime.min, reverse=True)'
    content = content.replace(target_str, contact_injection + "\n" + target_str)

    # Need to update the return format to include is_group
    old_return = '        "unread_count": c.get("unread_count", 0)\n    } for c in unique_contacts]'
    new_return = '        "unread_count": c.get("unread_count", 0),\n        "is_group": c.get("is_group", False)\n    } for c in unique_contacts]'
    content = content.replace(old_return, new_return)

# 3. Update get_chat_messages
if "contact_id.startswith(\"group_\")" not in content:
    get_msgs_old = """    messages = await db.chat_messages.find(
        {
            "$or": [
                {"sender_id": current_user.id, "receiver_id": contact_id},
                {"sender_id": contact_id, "receiver_id": current_user.id}
            ],
            "is_deleted": False,
            "cleared_by": {"$ne": current_user.id}
        }
    ).sort("created_at", 1).to_list(500)"""
    
    get_msgs_new = """    if contact_id.startswith("group_"):
        messages = await db.chat_messages.find(
            {
                "receiver_id": contact_id,
                "is_deleted": False,
                "cleared_by": {"$ne": current_user.id}
            }
        ).sort("created_at", 1).to_list(500)
    else:
        messages = await db.chat_messages.find(
            {
                "$or": [
                    {"sender_id": current_user.id, "receiver_id": contact_id},
                    {"sender_id": contact_id, "receiver_id": current_user.id}
                ],
                "is_deleted": False,
                "cleared_by": {"$ne": current_user.id}
            }
        ).sort("created_at", 1).to_list(500)"""
    content = content.replace(get_msgs_old, get_msgs_new)


with open(SERVER_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Backend patched successfully")
