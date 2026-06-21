import asyncio, motor.motor_asyncio
async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://omergehad345_db_user:Test123456789@cluster0.op68vs9.mongodb.net/?appName=Cluster0')
    db = client['wfm_reports']
    
    # 1. Update "شركة الموسي" (76) and "شركة الموسي " (67) -> Total 143 to "مشروع المحافظات الغربية"
    res1 = await db.reports.update_many({'project': 'شركة الموسي'}, {'$set': {'project': 'مشروع المحافظات الغربية'}})
    res2 = await db.reports.update_many({'project': 'شركة الموسي '}, {'$set': {'project': 'مشروع المحافظات الغربية'}})
    
    # 2. Update "جيزة العربية" (55) to "مشروع كشف التسربات وإصلاحها"
    res3 = await db.reports.update_many({'project': 'جيزة العربية'}, {'$set': {'project': 'مشروع كشف التسربات وإصلاحها'}})
    
    print(f"Updated Western: {res1.modified_count + res2.modified_count} reports")
    print(f"Updated Leak: {res3.modified_count} reports")

asyncio.run(main())
