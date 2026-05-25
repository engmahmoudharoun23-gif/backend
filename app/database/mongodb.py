# Database Configuration
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# MongoDB Configuration
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "reports_db")

# MongoDB Client
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Collections
users_collection = db.users
reports_collection = db.reports
projects_collection = db.projects
governorates_collection = db.governorates
invoices_collection = db.invoices
extracts_collection = db.extracts
employee_requests_collection = db.employee_requests
cars_collection = db.cars
water_connections_collection = db.water_connections
sewage_connections_collection = db.sewage_connections
chat_messages_collection = db.chat_messages
support_tickets_collection = db.support_tickets
work_units_collection = db.work_units

async def create_indexes():
    """إنشاء الفهارس لتحسين الأداء"""
    try:
        # Users indexes
        await db.users.create_index("id", unique=True)
        await db.users.create_index("username", unique=True)
        await db.users.create_index("created_by")
        
        # Reports indexes
        await db.reports.create_index("id", unique=True)
        await db.reports.create_index("report_number")
        await db.reports.create_index("governorate")
        await db.reports.create_index("project")
        await db.reports.create_index("created_by")
        await db.reports.create_index("created_at")
        
        # Projects indexes
        await db.projects.create_index("id", unique=True)
        await db.projects.create_index("name", unique=True)
        
        # Governorates indexes
        await db.governorates.create_index("id", unique=True)
        
        # Invoices indexes
        await db.invoices.create_index("id", unique=True)
        await db.invoices.create_index("status")
        await db.invoices.create_index("project")
        await db.invoices.create_index("uploaded_by")
        
        # Extracts indexes
        await db.extracts.create_index("id", unique=True)
        await db.extracts.create_index("project")
        await db.extracts.create_index("status")
        
        # Cars indexes
        await db.cars.create_index("id", unique=True)
        await db.cars.create_index("project")
        
        # Connections indexes
        await db.water_connections.create_index("id", unique=True)
        await db.water_connections.create_index("project")
        await db.sewage_connections.create_index("id", unique=True)
        await db.sewage_connections.create_index("project")
        
        print("✅ Database indexes created successfully")
    except Exception as e:
        print(f"⚠️ Index creation warning: {e}")
