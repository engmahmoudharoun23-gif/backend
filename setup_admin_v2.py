import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from datetime import datetime, timezone
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_admin():
    mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    db_name = os.getenv("DB_NAME", "wfm_reports")
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Check if admin already exists
    existing_admin = await db.users.find_one({"username": "admin"})
    if existing_admin:
        print("Admin user already exists. Skipping creation.")
        client.close()
        return

    admin = {
        "id": str(uuid.uuid4()),
        "username": "admin",
        "email": "admin@wfm.com",
        "full_name": "المسؤول",
        "role": "admin",
        "governorates": [],  # Empty = Access to all governorates
        "hashed_password": pwd_context.hash("admin123"),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "is_active": True
    }
    
    await db.users.insert_one(admin)
    print("✅ Created admin user:")
    print("   Username: admin")
    print("   Password: admin123")
    client.close()

if __name__ == "__main__":
    asyncio.run(create_admin())
