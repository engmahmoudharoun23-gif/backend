import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime, timezone

load_dotenv()

async def restore_missing_data():
    mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
    db_name = os.environ.get("DB_NAME", "wfm_reports")
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        print("[INFO] Starting restoration process...")
        
        # 1. Restore Projects from Project Cards
        print("\n--- Project Restoration ---")
        pc_cursor = db.project_cards.find({})
        added_count = 0
        async for pc in pc_cursor:
            project_name = pc.get("project")
            if not project_name:
                continue
                
            # Check if project exists
            existing = await db.projects.find_one({"name": project_name})
            if not existing:
                print(f"[+] Adding missing project: {project_name}")
                new_project = {
                    "id": str(uuid.uuid4()),
                    "name": project_name,
                    "description": f"Restored from project cards: {project_name}",
                    "created_at": datetime.now(timezone.utc),
                    "is_deleted": False
                }
                await db.projects.insert_one(new_project)
                added_count += 1
        print(f"[OK] Restored {added_count} projects.")

        # 2. Restore Governorates from Project Governorates
        print("\n--- Governorate Restoration ---")
        pg_cursor = db.project_governorates.find({})
        gov_added = 0
        gov_names = set()
        async for pg in pg_cursor:
            # Assuming project_governorates has governorate info
            gov_name = pg.get("name") or pg.get("governorate")
            if gov_name and gov_name not in gov_names:
                gov_names.add(gov_name)
                existing = await db.governorates.find_one({"name": gov_name})
                if not existing:
                    print(f"[+] Adding missing governorate: {gov_name}")
                    await db.governorates.insert_one({
                        "id": str(uuid.uuid4()),
                        "name": gov_name,
                        "created_at": datetime.now(timezone.utc),
                        "is_deleted": False
                    })
                    gov_added += 1
        print(f"[OK] Restored {gov_added} governorates.")

        # 3. Fix 'is_deleted' field in all collections
        print("\n--- Field Integrity Fix ---")
        collections_to_fix = ['reports', 'projects', 'users', 'invoices', 'extracts', 'governorates']
        for col_name in collections_to_fix:
            print(f"[FIX] Fixing {col_name}...")
            # Set is_deleted: False where it's missing
            result = await db[col_name].update_many(
                {"is_deleted": {"$exists": False}},
                {"$set": {"is_deleted": False}}
            )
            print(f"   Updated {result.modified_count} documents.")

        # 3. Check for users that might be missing
        # (Usually hard to tell without a reference, but we can check if admin is okay)
        admin = await db.users.find_one({"username": "admin"})
        if not admin:
            print("[WARN] Admin user missing! Should we recreate it?")
            # Not recreating automatically yet, but noted.
        else:
            print(f"[OK] Admin user found: {admin.get('full_name')}")

    except Exception as e:
        print(f"[ERROR] Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(restore_missing_data())
