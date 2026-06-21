import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def f():
    client = AsyncIOMotorClient('mongodb+srv://omergehad345_db_user:Test123456789@cluster0.op68vs9.mongodb.net/?appName=Cluster0')
    db = client['wfm_reports']
    projects = await db.projects.find().to_list(10)
    with open('projects_out.txt', 'w', encoding='utf-8') as f:
        for p in projects:
            f.write(p.get('name', '') + '\n')

asyncio.run(f())
