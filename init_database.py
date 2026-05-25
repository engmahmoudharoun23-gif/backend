#!/usr/bin/env python3
"""
سكريبت تهيئة قاعدة البيانات
يقوم بإنشاء قاعدة البيانات وتعبئتها بالبيانات الأولية من ملف seed_data.json
"""
import os
import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from pathlib import Path

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'test_database')

async def init_database():
    print(f"🔗 الاتصال بقاعدة البيانات: {MONGO_URL}/{DB_NAME}")
    
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # قراءة ملف البيانات
    seed_file = Path(__file__).parent / 'seed_data.json'
    if not seed_file.exists():
        print("❌ ملف seed_data.json غير موجود!")
        return
    
    with open(seed_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("\n📦 بدء تهيئة قاعدة البيانات...")
    
    for collection_name, documents in data.items():
        if not documents:
            print(f"  ⏭️  {collection_name}: فارغ - تخطي")
            continue
        
        # حذف البيانات القديمة
        await db[collection_name].delete_many({})
        
        # تحويل التواريخ من string إلى datetime
        for doc in documents:
            for key, value in doc.items():
                if isinstance(value, str) and 'T' in value and (value.endswith('Z') or '+' in value):
                    try:
                        doc[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    except:
                        pass
        
        # إدخال البيانات الجديدة
        await db[collection_name].insert_many(documents)
        print(f"  ✅ {collection_name}: {len(documents)} سجل")
    
    # إنشاء الفهارس
    print("\n🔧 إنشاء الفهارس...")
    await db.users.create_index("username", unique=True)
    await db.reports.create_index("report_number")
    await db.reports.create_index("project")
    await db.reports.create_index("governorate")
    await db.contractors.create_index("project")
    
    print("\n✅ تم تهيئة قاعدة البيانات بنجاح!")
    print(f"\n📊 ملخص:")
    for col in data.keys():
        count = await db[col].count_documents({})
        print(f"  - {col}: {count}")

if __name__ == "__main__":
    asyncio.run(init_database())
