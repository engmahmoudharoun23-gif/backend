import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def check():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.wfm_reports
    
    print("Simulating notification count for Admin...")
    
    # Admin Count (from server.py logic)
    pending_requests = await db.employee_requests.count_documents({
        "$or": [
            {"status": "approved_by_manager"},
            {"request_type": {"$in": ["advance_request", "advance"]}, "status": "pending"}
        ],
        "is_deleted": {"$ne": True}
    })
    
    print(f"Admin Pending Requests Count: {pending_requests}")
    
    # List them
    cursor = db.employee_requests.find({
        "$or": [
            {"status": "approved_by_manager"},
            {"request_type": {"$in": ["advance_request", "advance"]}, "status": "pending"}
        ],
        "is_deleted": {"$ne": True}
    })
    async for doc in cursor:
        print(f"Req ID: {doc.get('id')}, Type: {doc.get('request_type')}, Status: {doc.get('status')}, By: {doc.get('uploaded_by_name')}")

if __name__ == "__main__":
    asyncio.run(check())
