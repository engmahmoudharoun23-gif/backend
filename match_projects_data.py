import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def match_projects():
    mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
    db_name = os.environ.get("DB_NAME", "wfm_reports")
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        # Get all projects
        projects = await db.projects.find().to_list(100)
        print("Existing Projects in DB:")
        for p in projects:
            p_name = p.get('name')
            p_id = p.get('id')
            
            # Count reports
            report_count = await db.reports.count_documents({"project": p_name})
            # Count water connections
            water_count = await db.water_connections.count_documents({"project": p_name})
            # Count sewage connections
            sewage_count = await db.sewage_connections.count_documents({"project": p_name})
            
            print(f"ID: {p_id:38} | Name: {repr(p_name):20} | Reports: {report_count:3} | Water: {water_count:3} | Sewage: {sewage_count:3}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(match_projects())
