import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import bcrypt
from datetime import datetime, timezone
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

async def create_admin():
    mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
    db_name = os.environ.get("DB_NAME", "wfm_reports")
    
    print(f"Connecting to {mongo_url}...")
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        # Check if admin already exists
        existing_admin = await db.users.find_one({"username": "admin"})
        if existing_admin:
            print("Admin user already exists. Updating password to admin123...")
            await db.users.update_one(
                {"username": "admin"},
                {"$set": {"hashed_password": hash_password("admin123")}}
            )
        else:
            admin = {
                "id": str(uuid.uuid4()),
                "username": "admin",
                "email": "admin@wfm.com",
                "full_name": "Admin User",
                "role": "admin",
                "governorates": [],
                "projects": [],
                "hashed_password": hash_password("admin123"),
                "created_at": datetime.now(timezone.utc).isoformat(),
                "is_active": True,
                "permissions": ["dashboard", "users_manage", "projects", "settings"]
            }
            await db.users.insert_one(admin)
            print("Admin user created: admin / admin123")
            
        # Ensure projects exist
        projects = ["Medina", "Mecca"]
        for proj_name in projects:
            exists = await db.projects.find_one({"name": proj_name})
            if not exists:
                await db.projects.insert_one({
                    "id": str(uuid.uuid4()),
                    "name": proj_name,
                    "created_at": datetime.now(timezone.utc).isoformat()
                })
                print(f"Project created: {proj_name}")
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(create_admin())
