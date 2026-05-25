import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def check_admin_permissions():
    mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
    db_name = os.environ.get("DB_NAME", "wfm_reports")
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        admin = await db.users.find_one({"username": "admin"})
        if admin:
            print(f"User: {admin.get('username')}")
            print(f"Role: {admin.get('role')}")
            perms = admin.get("permissions", [])
            print(f"Current Permissions: {perms}")
            
            # Ensure all_projects is there
            if "all_projects" not in perms:
                print("[!] Admin is missing 'all_projects' permission. Adding it...")
                await db.users.update_one(
                    {"username": "admin"},
                    {"$addToSet": {"permissions": "all_projects"}}
                )
                print("[OK] Added 'all_projects' permission.")
            
            # Ensure other essential permissions
            essential = ["dashboard", "reports_view", "reports_add", "reports_edit", "reports_export", "trash_view"]
            for p in essential:
                if p not in perms:
                    await db.users.update_one(
                        {"username": "admin"},
                        {"$addToSet": {"permissions": p}}
                    )
            print("[OK] All essential permissions ensured.")
        else:
            print("[ERROR] Admin user not found.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(check_admin_permissions())
