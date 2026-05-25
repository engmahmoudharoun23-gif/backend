"""
Database Connection Module
إدارة الاتصال بقاعدة البيانات MongoDB
"""
import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
from ..config import get_settings

logger = logging.getLogger(__name__)

# Global database instance
_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None


async def get_database() -> AsyncIOMotorDatabase:
    """
    Get database instance
    جلب مثيل قاعدة البيانات
    """
    global _client, _db
    
    if _db is None:
        settings = get_settings()
        _client = AsyncIOMotorClient(
            settings.MONGO_URL,
            maxPoolSize=settings.MONGO_MAX_POOL_SIZE,
            minPoolSize=settings.MONGO_MIN_POOL_SIZE,
            maxIdleTimeMS=settings.MONGO_MAX_IDLE_TIME_MS,
            connectTimeoutMS=settings.MONGO_CONNECT_TIMEOUT_MS,
            serverSelectionTimeoutMS=settings.MONGO_CONNECT_TIMEOUT_MS
        )
        _db = _client[settings.DB_NAME]
        logger.info(f"Connected to MongoDB: {settings.DB_NAME}")
    
    return _db


async def close_database():
    """
    Close database connection
    إغلاق الاتصال بقاعدة البيانات
    """
    global _client, _db
    
    if _client is not None:
        _client.close()
        _client = None
        _db = None
        logger.info("MongoDB connection closed")


def get_db_sync() -> AsyncIOMotorDatabase:
    """
    Get database instance synchronously (for backward compatibility)
    جلب مثيل قاعدة البيانات بشكل متزامن
    """
    global _client, _db
    
    if _db is None:
        settings = get_settings()
        _client = AsyncIOMotorClient(
            settings.MONGO_URL,
            maxPoolSize=settings.MONGO_MAX_POOL_SIZE,
            minPoolSize=settings.MONGO_MIN_POOL_SIZE,
            maxIdleTimeMS=settings.MONGO_MAX_IDLE_TIME_MS,
            connectTimeoutMS=settings.MONGO_CONNECT_TIMEOUT_MS,
            serverSelectionTimeoutMS=settings.MONGO_CONNECT_TIMEOUT_MS
        )
        _db = _client[settings.DB_NAME]
    
    return _db


# Collection names
class Collections:
    """
    Database collection names
    أسماء المجموعات في قاعدة البيانات
    """
    USERS = "users"
    REPORTS = "reports"
    REPORT_TYPES = "report_types"
    CONTRACTORS = "contractors"
    GOVERNORATES = "governorates"
    AREAS = "areas"
    PROJECTS = "projects"
    EXTRACTS = "extracts"
    INVOICES = "invoices"
    EMPLOYEE_REQUESTS = "employee_requests"
    CARS = "cars"
    MAINTENANCE_RECORDS = "maintenance_records"
    WATER_CONNECTIONS = "water_connections"
    SEWAGE_CONNECTIONS = "sewage_connections"
    CHAT_MESSAGES = "chat_messages"
    SUPPORT_MESSAGES = "support_messages"
    TRASH = "trash"
    DELETED_REPORTS = "deleted_reports"
    DELETED_GOVERNORATES = "deleted_governorates"


async def create_indexes():
    """
    Create database indexes for better performance
    إنشاء الفهارس لتحسين الأداء
    """
    db = await get_database()
    
    # Users indexes
    await db[Collections.USERS].create_index("username", unique=True)
    await db[Collections.USERS].create_index("email", sparse=True)
    await db[Collections.USERS].create_index("created_by")
    
    # Reports indexes
    await db[Collections.REPORTS].create_index("project")
    await db[Collections.REPORTS].create_index("governorate")
    await db[Collections.REPORTS].create_index("created_at")
    await db[Collections.REPORTS].create_index("status")
    await db[Collections.REPORTS].create_index("is_deleted")
    await db[Collections.REPORTS].create_index([("project", 1), ("created_at", -1)])
    
    # Invoices indexes
    await db[Collections.INVOICES].create_index("status")
    await db[Collections.INVOICES].create_index("uploaded_by")
    await db[Collections.INVOICES].create_index("manager_id")
    
    # Employee requests indexes
    await db[Collections.EMPLOYEE_REQUESTS].create_index("status")
    await db[Collections.EMPLOYEE_REQUESTS].create_index("uploaded_by")
    await db[Collections.EMPLOYEE_REQUESTS].create_index("manager_id")
    
    # Extracts indexes
    await db[Collections.EXTRACTS].create_index("project")
    await db[Collections.EXTRACTS].create_index("contractor")
    await db[Collections.EXTRACTS].create_index("status")
    
    # Connections indexes
    await db[Collections.WATER_CONNECTIONS].create_index("project")
    await db[Collections.WATER_CONNECTIONS].create_index("request_number")
    await db[Collections.SEWAGE_CONNECTIONS].create_index("project")
    await db[Collections.SEWAGE_CONNECTIONS].create_index("request_number")
    
    # Maintenance records indexes
    await db[Collections.MAINTENANCE_RECORDS].create_index("car_id")
    await db[Collections.MAINTENANCE_RECORDS].create_index("created_at")
    
    logger.info("Database indexes created successfully")
