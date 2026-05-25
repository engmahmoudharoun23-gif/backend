"""
Configuration Settings Module
إعدادات التطبيق ومتغيرات البيئة
"""
import os
from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Optional, List

# المسار الجذري للتطبيق
ROOT_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    """
    Application Settings
    يتم تحميل الإعدادات من متغيرات البيئة أو ملف .env
    """
    # Database
    MONGO_URL: str = "mongodb://localhost:27017"
    DB_NAME: str = "test_database"
    
    # JWT Authentication
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 525600  # 365 يوم
    
    # API Keys
    EMERGENT_LLM_KEY: Optional[str] = None
    RESEND_API_KEY: Optional[str] = None
    
    # Server Settings
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # MongoDB Pool Settings
    MONGO_MAX_POOL_SIZE: int = 100
    MONGO_MIN_POOL_SIZE: int = 10
    MONGO_MAX_IDLE_TIME_MS: int = 30000
    MONGO_CONNECT_TIMEOUT_MS: int = 5000
    
    # Upload Settings
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp", "image/gif"]
    IMAGE_COMPRESSION_QUALITY: int = 70
    MAX_IMAGE_DIMENSION: int = 1920
    
    # Cache Settings
    CACHE_TTL: int = 10  # seconds
    
    # Concurrency Limits
    MAX_CONCURRENT_UPLOADS: int = 50
    MAX_CONCURRENT_QUERIES: int = 100
    THREAD_POOL_WORKERS: int = 20
    
    class Config:
        env_file = str(ROOT_DIR / ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    استخدام الكاش لتجنب قراءة الإعدادات في كل طلب
    """
    return Settings()


# Permissions Configuration
ALL_PERMISSIONS = [
    {"key": "dashboard", "label": "لوحة التحكم", "group": "عام"},
    {"key": "reports_view", "label": "عرض البلاغات", "group": "البلاغات"},
    {"key": "reports_add", "label": "إضافة بلاغ", "group": "البلاغات"},
    {"key": "reports_edit", "label": "تعديل البلاغات", "group": "البلاغات"},
    {"key": "reports_delete", "label": "حذف البلاغات", "group": "البلاغات"},
    {"key": "reports_notifications", "label": "إشعارات البلاغات", "group": "البلاغات"},
    {"key": "reports_export", "label": "تصدير البلاغات", "group": "البلاغات"},
    {"key": "trash_view", "label": "عرض سلة المحذوفات", "group": "البلاغات"},
    {"key": "trash_restore", "label": "استعادة من المحذوفات", "group": "البلاغات"},
    {"key": "trash_delete", "label": "حذف نهائي", "group": "البلاغات"},
    {"key": "contractors", "label": "المقاولون", "group": "الإعدادات"},
    {"key": "project_settings", "label": "إعدادات المشاريع", "group": "الإعدادات"},
    {"key": "extracts", "label": "المستخلصات", "group": "المالية"},
    {"key": "fleet", "label": "صيانة الأسطول", "group": "الأسطول"},
    {"key": "cars", "label": "السيارات", "group": "الأسطول"},
    {"key": "custody", "label": "العهد", "group": "المالية"},
    {"key": "invoices", "label": "فواتير العهدة", "group": "المالية"},
    {"key": "review_invoices", "label": "مراجعة الفواتير", "group": "المالية"},
    {"key": "employee_requests", "label": "طلبات الموظفين", "group": "الموارد البشرية"},
    {"key": "view_all_employee_requests", "label": "عرض جميع طلبات الموظفين", "group": "الموارد البشرية"},
    {"key": "review_employee_requests", "label": "مراجعة طلبات الموظفين", "group": "الموارد البشرية"},
    {"key": "team", "label": "فريق العمل", "group": "الموارد البشرية"},
    {"key": "users", "label": "إدارة المستخدمين", "group": "الإدارة"},
    {"key": "settings", "label": "الإعدادات", "group": "الإدارة"},
    {"key": "support", "label": "رسائل الدعم", "group": "الإدارة"},
    {"key": "all_projects", "label": "جميع المشاريع", "group": "الإدارة"},
    {"key": "water_connections", "label": "توصيلات المياه", "group": "مشروع إيصال"},
    {"key": "sewage_connections", "label": "توصيلات الصرف الصحي", "group": "مشروع إيصال"},
    {"key": "chat", "label": "المحادثات", "group": "عام"},
    {"key": "business_reports_review", "label": "مراجعة تقارير الأعمال", "group": "التقارير"},
]

# Request Types for Employee Requests
REQUEST_TYPES = {
    "vacation": "إجازة",
    "sick_leave": "إجازة مرضية",
    "permission": "استئذان",
    "work_from_home": "عمل من المنزل",
    "overtime": "عمل إضافي",
    "advance": "سلفة",
    "family_visit": "زيارة عائلية",
    "other": "أخرى"
}

# Report Statuses
REPORT_STATUSES = {
    "pending": "قيد المعالجة",
    "in_progress": "جاري التنفيذ",
    "completed": "مكتمل",
    "cancelled": "ملغي"
}

# Invoice Statuses
INVOICE_STATUSES = {
    "pending": "قيد المراجعة",
    "approved_by_manager": "معتمدة من المدير",
    "approved_final": "اعتماد نهائي",
    "approved_by_admin": "معتمدة نهائياً",
    "cancelled": "تم إلغاء الاعتماد",
    "rejected": "مرفوضة"
}
