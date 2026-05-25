import motor.motor_asyncio
import asyncio
import json

async def run():
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['wfm_reports']
    # Search for "500" in notes or payment_history.notes
    docs = await db.hr_advances_custodies.find({
        "$or": [
            {"notes": {"$regex": "500"}},
            {"payment_history.notes": {"$regex": "500"}}
        ]
    }).to_list(100)
    for doc in docs:
        doc.pop('_id', None)
        print(json.dumps(doc, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(run())
