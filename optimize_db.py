"""
تحسين قاعدة البيانات للأداء العالي
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def create_indexes():
    """إنشاء الفهارس لتسريع الاستعلامات"""
    
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    print("🚀 بدء إنشاء الفهارس...")
    
    try:
        # فهارس المستخدمين
        await db.users.create_index("username", background=True)
        await db.users.create_index("role", background=True)
        await db.users.create_index("projects", background=True)
        await db.users.create_index("is_active", background=True)
        print("✅ فهارس users")
    except Exception as e:
        print(f"⚠️ users: {e}")
    
    try:
        # فهارس البلاغات
        await db.reports.create_index("report_number", background=True)
        await db.reports.create_index("project", background=True)
        await db.reports.create_index("governorate", background=True)
        await db.reports.create_index("contractor", background=True)
        await db.reports.create_index("created_at", background=True)
        await db.reports.create_index("status", background=True)
        await db.reports.create_index([("project", 1), ("governorate", 1)], background=True)
        await db.reports.create_index([("project", 1), ("created_at", -1)], background=True)
        print("✅ فهارس reports")
    except Exception as e:
        print(f"⚠️ reports: {e}")
    
    try:
        # فهارس المستخلصات
        await db.extracts.create_index("project", background=True)
        await db.extracts.create_index("status", background=True)
        await db.extracts.create_index("created_by", background=True)
        await db.extracts.create_index("created_at", background=True)
        await db.extracts.create_index("is_deleted", background=True)
        await db.extracts.create_index([("project", 1), ("status", 1)], background=True)
        await db.extracts.create_index([("is_deleted", 1), ("created_at", -1)], background=True)
        await db.extracts.create_index([("created_by", 1), ("created_at", -1)], background=True)
        print("✅ فهارس extracts")
    except Exception as e:
        print(f"⚠️ extracts: {e}")
    
    try:
        # فهارس الفواتير
        await db.invoices.create_index("project", background=True)
        await db.invoices.create_index("status", background=True)
        await db.invoices.create_index("created_at", background=True)
        await db.invoices.create_index("uploaded_by", background=True)
        await db.invoices.create_index([("project", 1), ("status", 1)], background=True)
        await db.invoices.create_index([("project", 1), ("created_at", -1)], background=True)
        print("✅ فهارس invoices")
    except Exception as e:
        print(f"⚠️ invoices: {e}")
    
    try:
        # فهارس طلبات الموظفين
        await db.employee_requests.create_index("status", background=True)
        await db.employee_requests.create_index("created_at", background=True)
        await db.employee_requests.create_index("uploaded_by", background=True)
        await db.employee_requests.create_index("request_type", background=True)
        await db.employee_requests.create_index([("status", 1), ("created_at", -1)], background=True)
        print("✅ فهارس employee_requests")
    except Exception as e:
        print(f"⚠️ employee_requests: {e}")
    
    try:
        # فهارس التوصيلات
        await db.water_connections.create_index("project", background=True)
        await db.water_connections.create_index([("project", 1), ("governorate", 1)], background=True)
        await db.sewage_connections.create_index("project", background=True)
        await db.sewage_connections.create_index([("project", 1), ("governorate", 1)], background=True)
        print("✅ فهارس connections")
    except Exception as e:
        print(f"⚠️ connections: {e}")
    
    try:
        # فهارس المشاريع والمقاولين
        await db.projects.create_index("name", background=True)
        await db.contractors.create_index("name", background=True)
        await db.contractors.create_index("project", background=True)
        await db.cars.create_index("project", background=True)
        print("✅ فهارس أخرى")
    except Exception as e:
        print(f"⚠️ others: {e}")
    
    print("\n🎉 تم إنشاء الفهارس!")
    print("⚡ النظام جاهز للأداء العالي")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_indexes())
