import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext

async def reset_pwd():
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['wfm_reports']
    await db.users.update_one({'username': 'admin'}, {'$set': {'hashed_password': pwd_context.hash('admin123')}})
    client.close()
    print('Password reset to admin123')

asyncio.run(reset_pwd())
