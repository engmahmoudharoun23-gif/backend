import asyncio, motor.motor_asyncio, json
async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://omergehad345_db_user:Test123456789@cluster0.op68vs9.mongodb.net/?appName=Cluster0')
    db = client['wfm_reports']
    projects = await db.reports.distinct('project')
    
    result = []
    for p in projects:
        count = await db.reports.count_documents({'project': p})
        result.append({'project': p, 'count': count})
        
    with open('d:/sery17-main/backend/projects_debug.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

asyncio.run(main())
