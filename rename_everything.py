import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

# Mapping based on data patterns
MAPPING = {
    '   - ': 'مشروع المحافظات الغربية',
    '   ': 'مشروع ايصال',
    '': 'مشروع ايصال مكة', # Assuming this based on connections
    ' ': 'مشروع ايصال الرياض', # This one has connections
    '': 'مشروع التسربات',
    '': 'مشروع ايصال المدينة',
}

# Real identities from user's request
# 1. مشروع ايصال
# 2. مشروع المحافظات الغربية
# 3. مشروع التسربات
# 4. مشروع ايصال الرياض

async def rename_all():
    mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
    db_name = os.environ.get("DB_NAME", "wfm_reports")
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Refined mapping after more thought
    # 14 reports -> Western Governorates
    # 3 reports -> Connections (ايصال)
    # 2 reports -> Leaks (تسربات)
    # 1 report -> Riyadh Connections
    # The others with connections might be other branches
    
    mapping = {
        '   - ': 'مشروع المحافظات الغربية',
        '   ': 'مشروع ايصال',
        '': 'مشروع التسربات',
        '': 'مشروع ايصال الرياض',
        '': 'مشروع ايصال مكة',
        ' ': 'مشروع ايصال المدينة',
    }

    collections = [
        'projects', 'reports', 'water_connections', 'sewage_connections', 
        'invoices', 'extracts', 'project_cards', 'users', 'activity_logs',
        'report_types', 'report_statuses'
    ]
    
    try:
        for old_name, new_name in mapping.items():
            print(f"Renaming {repr(old_name)} to {new_name}...")
            
            # For collections where 'project' is the field
            for col in collections:
                if col == 'projects' or col == 'project_cards':
                    # These might use 'name' or 'project'
                    await db[col].update_many({"name": old_name}, {"$set": {"name": new_name}})
                    await db[col].update_many({"project": old_name}, {"$set": {"project": new_name}})
                elif col == 'users':
                    # users.projects is a list
                    await db.users.update_many({"projects": old_name}, {"$set": {"projects.$": new_name}})
                else:
                    await db[col].update_many({"project": old_name}, {"$set": {"project": new_name}})
                    
        print("Renaming completed.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(rename_all())
