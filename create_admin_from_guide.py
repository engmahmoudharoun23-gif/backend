import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from datetime import datetime, timezone
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_admin():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["wfm_reports"]
    
    # حذف المستخدم إذا كان موجوداً
    await db.users.delete_one({"username": "admin"})
    
    admin = {
        "id": str(uuid.uuid4()),
        "username": "admin",
        "email": "admin@wfm.com",
        "full_name": "المسؤول",
        "role": "admin",
        "governorates": [],  # فارغ = الوصول لكل المحافظات
        "hashed_password": pwd_context.hash("admin123"),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "is_active": True
    }
    
    await db.users.insert_one(admin)
    print("✅ تم إنشاء حساب المسؤول:")
    print("   اسم المستخدم: admin")
    print("   كلمة المرور: admin123")
    client.close()

if __name__ == "__main__":
    asyncio.run(create_admin())
