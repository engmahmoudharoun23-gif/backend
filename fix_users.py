import asyncio, motor.motor_asyncio
async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://omergehad345_db_user:Test123456789@cluster0.op68vs9.mongodb.net/?appName=Cluster0')
    db = client['wfm_reports']
    
    projects_list = ['المحافظات الغربية', 'كشف التسربات وإصلاحها', 'التشوه البصري']
    await db.users.update_many({}, {'$set': {'projects': projects_list}})
    print('Restored projects for all users')

asyncio.run(main())
