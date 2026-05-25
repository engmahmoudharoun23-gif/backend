import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def check():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.wfm_reports
    
    medhat_id = "b3cbc848-273b-40e1-8cda-5e1c45619e1a"
    print(f"Simulating notification count for Medhat ({medhat_id})...")
    
    # Simulate get_sub_user_ids_recursive
    # (Assuming it checks reports_to or similar)
    sub_user_ids = []
    cursor = db.users.find({"manager_id": medhat_id})
    async for doc in cursor:
        sub_user_ids.append(doc.get('id'))
    
    print(f"Sub-users found: {sub_user_ids}")
    
    # Manager Count
    sub_req_query = {
        "uploaded_by": {"$in": sub_user_ids},
        "status": "pending",
        "request_type": {"$nin": ["advance_request", "advance"]},
        "is_deleted": {"$ne": True}
    }
    manager_count = await db.employee_requests.count_documents(sub_req_query)
    print(f"Manager Count (Pending Subs): {manager_count}")
    
    # Delegated Reviewer Count
    review_req_query = {
        "status": "approved_by_manager",
        "is_deleted": {"$ne": True},
        "reviewed_by_manager": {"$ne": medhat_id}
    }
    review_count = await db.employee_requests.count_documents(review_req_query)
    print(f"Review Count (Approved by others): {review_count}")

if __name__ == "__main__":
    asyncio.run(check())
