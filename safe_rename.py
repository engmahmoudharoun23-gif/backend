import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def safe_rename():
    mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
    db_name = os.environ.get("DB_NAME", "wfm_reports")
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Mapping project ID -> New Name
    id_mapping = {
        '06ba487d-616b-49b4-a9ab-87204594f671': 'مشروع المحافظات الغربية',
        '1e17fa92-f1dd-4e31-9a5d-98d492a3b118': 'مشروع ايصال',
        'c9a1bf8d-05b2-4ca5-84b2-110d93329e91': 'مشروع التسربات',
        '9209abe5-213d-44cb-bb20-8348254560de': 'مشروع ايصال الرياض',
        '5b79e186-f92b-4850-b1bd-822449c5f074': 'مشروع ايصال مكة',
        '69539b77-52d9-401a-aa22-443526fc561a': 'مشروع ايصال المدينة',
    }

    collections = [
        'projects', 'reports', 'water_connections', 'sewage_connections', 
        'invoices', 'extracts', 'project_cards', 'activity_logs',
        'report_types', 'report_statuses'
    ]
    
    try:
        for p_id, new_name in id_mapping.items():
            # Get the current garbled name
            project = await db.projects.find_one({"id": p_id})
            if not project:
                continue
                
            old_name = project.get("name")
            print(f"Renaming {repr(old_name)} to {new_name}...")
            
            # Update projects
            await db.projects.update_one({"id": p_id}, {"$set": {"name": new_name}})
            
            # Update other collections
            for col in collections:
                if col == 'projects': continue
                if col == 'project_cards':
                    await db[col].update_many({"project": old_name}, {"$set": {"project": new_name}})
                else:
                    await db[col].update_many({"project": old_name}, {"$set": {"project": new_name}})
                    
            # Update users projects list (requires pulling old and pushing new)
            users = await db.users.find({"projects": old_name}).to_list(1000)
            for u in users:
                await db.users.update_one(
                    {"_id": u["_id"]},
                    {"$set": {"projects.$[elem]": new_name}},
                    array_filters=[{"elem": old_name}]
                )
                    
        print("Renaming completed successfully.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(safe_rename())
