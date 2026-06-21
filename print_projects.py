import asyncio, motor.motor_asyncio
async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://omergehad345_db_user:Test123456789@cluster0.op68vs9.mongodb.net/?appName=Cluster0')
    db = client['wfm_reports']
    projects = await db.reports.distinct('project')
    for p in projects:
        count = await db.reports.count_documents({'project': p})
        print(f'{repr(p)} -> {count}')
asyncio.run(main())
