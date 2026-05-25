import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
import json
from dotenv import load_dotenv

load_dotenv()
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

async def inspect():
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    users = await db.users.find({}).to_list(100)
    for u in users:
        u.pop("_id", None)
        u.pop("hashed_password", None)
        print(json.dumps(u, ensure_ascii=False, indent=2))
        
    client.close()

asyncio.run(inspect())
