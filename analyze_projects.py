import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def analyze_projects():
    mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
    db_name = os.environ.get("DB_NAME", "wfm_reports")
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        pipeline = [
            {"$group": {"_id": "$project", "count": {"$sum": 1}}}
        ]
        results = await db.reports.aggregate(pipeline).to_list(100)
        for res in results:
            name = res["_id"]
            print(f"Project: {repr(name)} | Count: {res['count']}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(analyze_projects())
