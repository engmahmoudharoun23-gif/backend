import asyncio
import motor.motor_asyncio
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://omergehad345_db_user:Test123456789@cluster0.op68vs9.mongodb.net/?appName=Cluster0')
    db = client['wfm_reports']
    
    hashed_password = get_password_hash("admin123")
    
    await db.users.update_one(
        {"username": "admin"},
        {"$set": {"hashed_password": hashed_password}}
    )
    print("Password reset successfully for admin to 'admin123'")

if __name__ == '__main__':
    asyncio.run(main())
