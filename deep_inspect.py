import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def deep_inspect():
    mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
    client = AsyncIOMotorClient(mongo_url)
    
    try:
        dbs = await client.list_database_names()
        print(f"Databases found: {dbs}")
        
        for db_name in dbs:
            if db_name in ['admin', 'config', 'local']:
                continue
            print(f"\n--- Database: {db_name} ---")
            db = client[db_name]
            colls = await db.list_collection_names()
            for col in colls:
                count = await db[col].count_documents({})
                print(f"  Collection: {col:25} Count: {count}")
                if count > 0:
                    sample = await db[col].find_one()
                    # print(f"    Sample keys: {list(sample.keys())}")
                    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(deep_inspect())
