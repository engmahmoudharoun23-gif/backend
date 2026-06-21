import asyncio, motor.motor_asyncio
async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://omergehad345_db_user:Test123456789@cluster0.op68vs9.mongodb.net/?appName=Cluster0')
    db = client['wfm_reports']
    
    projects = await db.reports.distinct('project')
    for p in projects:
        count = await db.reports.count_documents({'project': p})
        if count == 143:
            await db.reports.update_many({'project': p}, {'$set': {'project': 'المحافظات الغربية'}})
            print('Updated 143 to Western')
        elif count == 55:
            await db.reports.update_many({'project': p}, {'$set': {'project': 'كشف التسربات وإصلاحها'}})
            print('Updated 55 to Leak')
            
    users = await db.users.find({}).to_list(100)
    for u in users:
        await db.users.update_one({'_id': u['_id']}, {'$set': {'projects': ['المحافظات الغربية', 'كشف التسربات وإصلاحها', 'التشوه البصري']}})
    print('Users projects fixed')

asyncio.run(main())
