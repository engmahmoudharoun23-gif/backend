"""
Централизованная система хранения Cloudinary - بديل عن التخزين المحلي
"""
import os
import logging
import cloudinary
import cloudinary.uploader
from typing import Optional
from io import BytesIO

logger = logging.getLogger(__name__)

# إعداد Cloudinary من متغيرات البيئة
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
    secure=True
)

def upload_image(data: bytes, category: str = "reports", ext: str = "jpg", content_type: str = "image/jpeg") -> str:
    """
    رفع صورة أو ملف إلى Cloudinary وإرجاع الـ URL العام.
    """
    try:
        # تحديد نوع الملف (صورة أو فيديو أو ملف عام)
        resource_type = "auto"
        if "video" in content_type:
            resource_type = "video"
        elif "image" not in content_type:
            resource_type = "raw"

        # الرفع إلى Cloudinary
        upload_result = cloudinary.uploader.upload(
            BytesIO(data),
            folder=f"sery17/{category}",
            resource_type=resource_type
        )
        
        # إرجاع URL الملف (نستخدم secure_url للأمان)
        return upload_result.get("secure_url")
    except Exception as e:
        logger.error(f"❌ Cloudinary upload failed: {e}")
        raise RuntimeError(f"فشل الرفع إلى Cloudinary: {str(e)}")

def get_object(path: str):
    """
    تحميل كائن (هذه الدالة لم تعد ضرورية مع Cloudinary لأننا نستخدم الروابط المباشرة، 
    ولكن سنبقيها للتوافق مع الكود القديم إذا لزم الأمر)
    """
    import requests
    resp = requests.get(path)
    resp.raise_for_status()
    return resp.content, resp.headers.get("Content-Type", "application/octet-stream")

def guess_ext(filename: Optional[str], content_type: Optional[str]) -> str:
    """تحديد امتداد الملف من الاسم أو النوع."""
    if filename and "." in filename:
        return filename.rsplit(".", 1)[-1].lower()
    ct = (content_type or "").lower()
    if "png" in ct: return "png"
    if "webp" in ct: return "webp"
    if "gif" in ct: return "gif"
    if "video" in ct: return "mp4"
    if "pdf" in ct: return "pdf"
    return "jpg"

def init_storage():
    """Dummy function for compatibility with server.py"""
    logger.info("Cloudinary storage system initialized (shim)")
    pass
