import asyncio, motor.motor_asyncio
async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://omergehad345_db_user:Test123456789@cluster0.op68vs9.mongodb.net/?appName=Cluster0')
    db = client['wfm_reports']
    
    projects = await db.reports.distinct('project')
    for p in projects:
        count = await db.reports.count_documents({'project': p})
        if count == 143:
            await db.reports.update_many({'project': p}, {'': {'project': '\u0627\u0644\u0645\u062d\u0627\u0641\u0638\u0627\u062a \u0627\u0644\u063a\u0631\u0628\u064a\u0629'}})
            print('Updated 143 to Western')
        elif count == 55:
            await db.reports.update_many({'project': p}, {'': {'project': '\u0643\u0634\u0641 \u0627\u0644\u062a\u0633\u0631\u0628\u0627\u062a \u0648\u0625\u0635\u0644\u0627\u062d\u0647\u0627'}})
            print('Updated 55 to Leak')
            
    users = await db.users.find({}).to_list(100)
    for u in users:
        await db.users.update_one({'_id': u['_id']}, {'': {'projects': ['\u0627\u0644\u0645\u062d\u0627\u0641\u0638\u0627\u062a \u0627\u0644\u063a\u0631\u0628\u064a\u0629', '\u0643\u0634\u0641 \u0627\u0644\u062a\u0633\u0631\u0628\u0627\u062a \u0648\u0625\u0635\u0644\u0627\u062d\u0647\u0627', '\u0627\u0644\u062a\u0634\u0648\u0647 \u0627\u0644\u0628\u0635\u0631\u064a']}})
    print('Users projects fixed')

asyncio.run(main())
