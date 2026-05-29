# User Service
from datetime import datetime, timezone
from typing import List, Optional
import uuid

from ..database.mongodb import db
from ..models.user import User, UserCreate, UserUpdate, UserResponse
from .auth_service import get_password_hash

async def get_all_users(current_user: User) -> List[dict]:
    # Admin sees all users, others see only their sub-users
    query = {} if current_user.role == "admin" else {"created_by": current_user.id}
    
    users = await db.users.find(
        query, 
        {"_id": 0, "profile_picture": 0}
    ).to_list(1000)
    
    for user in users:
        if isinstance(user.get('created_at'), str):
            user['created_at'] = datetime.fromisoformat(user['created_at'])
        # Backward compatibility
        if 'projects' not in user:
            user['projects'] = []
        if 'governorates' not in user:
            user['governorates'] = []
        if 'title' not in user:
            user['title'] = None
        if 'created_by' not in user:
            user['created_by'] = None
        if 'can_create_subusers' not in user:
            user['can_create_subusers'] = user.get('role') == 'admin'
    
    return users

async def get_user_by_id(user_id: str) -> Optional[dict]:
    """Get a user by ID"""
    return await db.users.find_one({"id": user_id}, {"_id": 0})

async def get_user_by_username(username: str) -> Optional[dict]:
    """Get a user by username"""
    return await db.users.find_one({"username": username}, {"_id": 0})

async def create_user(user_data: UserCreate, created_by: str) -> dict:
    """Create a new user"""
    # Check if username exists
    existing = await db.users.find_one({"username": user_data.username})
    if existing:
        raise ValueError("اسم المستخدم موجود مسبقاً")
    
    new_user = {
        "id": str(uuid.uuid4()),
        "username": user_data.username,
        "full_name": user_data.full_name,
        "title": user_data.title,
        "hashed_password": get_password_hash(user_data.password),
        "role": user_data.role,
        "projects": user_data.projects,
        "governorates": user_data.governorates,
        "permissions": user_data.permissions,
        "can_create_subusers": user_data.can_create_subusers,
        "is_active": True,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "created_by": created_by,
    }
    
    await db.users.insert_one(new_user)
    del new_user["hashed_password"]
    return new_user

async def update_user(user_id: str, user_data: UserUpdate) -> Optional[dict]:
    """Update a user"""
    update_data = {}
    
    if user_data.username is not None:
        update_data["username"] = user_data.username
    if user_data.full_name is not None:
        update_data["full_name"] = user_data.full_name
    if user_data.title is not None:
        update_data["title"] = user_data.title
    if user_data.password is not None:
        update_data["hashed_password"] = get_password_hash(user_data.password)
    if user_data.governorates is not None:
        update_data["governorates"] = user_data.governorates
    if user_data.projects is not None:
        update_data["projects"] = user_data.projects
    if user_data.permissions is not None:
        update_data["permissions"] = user_data.permissions
    
    if update_data:
        await db.users.update_one({"id": user_id}, {"$set": update_data})
    
    return await get_user_by_id(user_id)

async def delete_user(user_id: str) -> bool:
    """Delete a user"""
    result = await db.users.delete_one({"id": user_id})
    return result.deleted_count > 0

async def toggle_user_active(user_id: str) -> Optional[dict]:
    """Toggle user active status"""
    user = await get_user_by_id(user_id)
    if not user:
        return None
    
    new_status = not user.get("is_active", True)
    await db.users.update_one({"id": user_id}, {"$set": {"is_active": new_status}})
    return await get_user_by_id(user_id)

async def update_user_permissions(user_id: str, permissions_data: dict) -> Optional[dict]:
    """Update user permissions"""
    update_data = {
        "permissions": permissions_data.get("permissions", [])
    }
    if "project_permissions" in permissions_data:
        update_data["project_permissions"] = permissions_data["project_permissions"]
    if "connection_permissions" in permissions_data:
        update_data["connection_permissions"] = permissions_data["connection_permissions"]
    if "projects" in permissions_data:
        update_data["projects"] = permissions_data["projects"]
        
    await db.users.update_one({"id": user_id}, {"$set": update_data})
    return await get_user_by_id(user_id)
