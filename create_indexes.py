import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os

async def create_indexes():
    """إنشاء indexes لتسريع الاستعلامات"""
    mongo_url = os.environ.get('MONGO_URL')
    client = AsyncIOMotorClient(mongo_url)
    db = client.reports_db
    
    print("🚀 إنشاء indexes لتسريع الأداء...")
    
    try:
        # Index لرقم البلاغ (للتحقق من التكرار)
        await db.reports.create_index([("report_number", 1), ("is_deleted", 1)], background=True)
        print("✅ Index created: report_number + is_deleted")
        
        # Index لرقم الرخصة (للتحقق من التكرار)
        await db.reports.create_index([("license_number", 1), ("is_deleted", 1)], background=True)
        print("✅ Index created: license_number + is_deleted")
        
        # Index للمشروع والمحافظة (للفلترة السريعة)
        await db.reports.create_index([("project", 1), ("is_deleted", 1)], background=True)
        print("✅ Index created: project + is_deleted")
        
        # Index للمحافظة
        await db.reports.create_index([("governorate", 1), ("is_deleted", 1)], background=True)
        print("✅ Index created: governorate + is_deleted")
        
        # Index لتاريخ الإنشاء (للترتيب)
        await db.reports.create_index([("created_at", -1)], background=True)
        print("✅ Index created: created_at (descending)")
        
        # Index للمستخدم المنشئ
        await db.reports.create_index([("created_by", 1), ("is_deleted", 1)], background=True)
        print("✅ Index created: created_by + is_deleted")
        
        # Compound index للاستعلامات المعقدة
        await db.reports.create_index([
            ("project", 1), 
            ("governorate", 1), 
            ("is_deleted", 1),
            ("created_at", -1)
        ], background=True)
        print("✅ Index created: compound (project + governorate + is_deleted + created_at)")
        
        # عرض جميع الـ indexes
        indexes = await db.reports.list_indexes().to_list(None)
        print(f"\n📊 إجمالي الـ indexes: {len(indexes)}")
        for idx in indexes:
            print(f"  - {idx.get('name')}")
        
        print("\n✅ تم إنشاء جميع الـ indexes بنجاح!")
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(create_indexes())
