"""
Common Utilities
أدوات مشتركة
"""
import uuid
import logging
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def generate_id() -> str:
    """Generate unique ID"""
    return str(uuid.uuid4())


def get_utc_now() -> datetime:
    """Get current UTC datetime"""
    return datetime.now(timezone.utc)


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime to string"""
    if dt is None:
        return ""
    return dt.strftime(format_str)


def parse_datetime(date_str: str, format_str: str = "%Y-%m-%d") -> Optional[datetime]:
    """Parse string to datetime"""
    try:
        return datetime.strptime(date_str, format_str)
    except (ValueError, TypeError):
        return None


def sanitize_mongodb_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove MongoDB _id and convert ObjectId to string
    تنظيف المستند من _id
    """
    if doc is None:
        return {}
    
    # Create a copy to avoid modifying original
    cleaned = dict(doc)
    
    # Remove _id
    cleaned.pop("_id", None)
    
    return cleaned


def calculate_date_range(period: str) -> tuple:
    """
    Calculate date range based on period
    حساب نطاق التاريخ
    
    Periods: day, week, month, quarter, year
    """
    now = get_utc_now()
    end_date = now
    
    if period == "day":
        start_date = now - timedelta(days=1)
    elif period == "week":
        start_date = now - timedelta(weeks=1)
    elif period == "month":
        start_date = now - timedelta(days=30)
    elif period == "quarter":
        start_date = now - timedelta(days=90)
    elif period == "year":
        start_date = now - timedelta(days=365)
    else:
        start_date = now - timedelta(days=30)
    
    return (start_date, end_date)


def build_date_filter(date_from: str = None, date_to: str = None, field: str = "created_at") -> dict:
    """
    Build MongoDB date filter
    بناء فلتر التاريخ
    """
    if not date_from and not date_to:
        return {}
    
    date_filter = {}
    
    if date_from:
        from_dt = parse_datetime(date_from)
        if from_dt:
            date_filter["$gte"] = from_dt
    
    if date_to:
        to_dt = parse_datetime(date_to)
        if to_dt:
            # Add one day to include the end date
            date_filter["$lt"] = to_dt + timedelta(days=1)
    
    if date_filter:
        return {field: date_filter}
    
    return {}


def paginate_query(skip: int = 0, limit: int = 100) -> dict:
    """
    Create pagination parameters
    إنشاء معاملات التصفح
    """
    return {
        "skip": max(0, skip),
        "limit": min(max(1, limit), 1000)  # Max 1000 items per page
    }
