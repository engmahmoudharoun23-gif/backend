import asyncio, motor.motor_asyncio, json
async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://omergehad345_db_user:Test123456789@cluster0.op68vs9.mongodb.net/?appName=Cluster0')
    db = client['wfm_reports']
    
    # 1. Restore reports
    res1 = await db.reports.update_many({'project': 'المحافظات الغربية'}, {'$set': {'project': 'مشروع المحافظات الغربية'}})
    res2 = await db.reports.update_many({'project': 'كشف التسربات وإصلاحها'}, {'$set': {'project': 'مشروع كشف التسربات وإصلاحها'}})
    print(f"Restored reports: {res1.modified_count} Western, {res2.modified_count} Leak")

    # 2. Restore users
    with open('d:/sery17-main/frontend/sery17-main/users_atlas_dump.json', 'r', encoding='utf-8') as f:
        users_backup = json.load(f)
    
    restored_users = 0
    for ub in users_backup:
        await db.users.update_one({'username': ub['username']}, {'$set': {'projects': ub['projects'], 'governorates': ub['governorates']}})
        restored_users += 1
    
    print(f"Restored {restored_users} users from backup")

asyncio.run(main())
