import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def run():
    db = AsyncIOMotorClient('mongodb+srv://omergehad345_db_user:Test123456789@cluster0.op68vs9.mongodb.net/?appName=Cluster0')['wfm_reports']
    u = await db.users.find_one({'username': {'$regex': 'mahmoud', '$options': 'i'}})
    if not u:
        async for x in db.users.find({}):
            if 'mahmoud' in str(x.get('username')).lower() or 'هارون' in str(x.get('full_name')):
                u = x
                break
                
    if u:
        print("Found:", u['full_name'])
        # Add his ID to seen_by and deleted_notifications for all reports in "الشمالية"
        res = await db.reports.update_many(
            {'project': {'$regex': 'الشمالية'}}, 
            {'$addToSet': {'seen_by': u['_id'], 'deleted_notifications': u['_id']}}
        )
        print('Fixed reports:', res.modified_count)
    else:
        print('User not found')

asyncio.run(run())
