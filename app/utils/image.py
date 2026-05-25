"""
Image Utilities - أدوات معالجة الصور
Image compression, validation, etc.
"""
import base64
import io
import logging
from typing import Optional
from PIL import Image

logger = logging.getLogger(__name__)


def compress_image_data(image_data: str, max_size_mb: float = 3.0) -> str:
    """
    Compress base64 image data to reduce size
    ضغط بيانات الصورة لتقليل الحجم
    
    Args:
        image_data: Base64 encoded image string
        max_size_mb: Maximum size in megabytes
        
    Returns:
        Compressed base64 image string
    """
    try:
        # Check if already small enough
        current_size_mb = len(image_data) / (1024 * 1024)
        if current_size_mb <= max_size_mb:
            return image_data
        
        # Extract base64 data
        if ',' in image_data:
            header, base64_data = image_data.split(',', 1)
        else:
            header = "data:image/jpeg;base64"
            base64_data = image_data
        
        # Decode and compress
        image_bytes = base64.b64decode(base64_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')
        
        # Calculate compression ratio
        compression_ratio = max_size_mb / current_size_mb
        quality = int(85 * compression_ratio)
        quality = max(20, min(quality, 85))
        
        # Resize if very large
        max_dimension = 1920
        if max(image.size) > max_dimension:
            ratio = max_dimension / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Save compressed
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG', quality=quality, optimize=True)
        compressed_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return f"data:image/jpeg;base64,{compressed_data}"
        
    except Exception as e:
        logger.error(f"Image compression error: {e}")
        return image_data


def validate_image_data(image_data: str) -> bool:
    """
    Validate base64 image data
    التحقق من صحة بيانات الصورة
    """
    try:
        if not image_data:
            return False
        
        # Check for base64 prefix
        if ',' in image_data:
            _, base64_data = image_data.split(',', 1)
        else:
            base64_data = image_data
        
        # Try to decode
        image_bytes = base64.b64decode(base64_data)
        
        # Try to open as image
        image = Image.open(io.BytesIO(image_bytes))
        image.verify()
        
        return True
        
    except Exception as e:
        logger.error(f"Image validation error: {e}")
        return False


def get_image_size_mb(image_data: str) -> float:
    """
    Get image size in megabytes
    الحصول على حجم الصورة بالميجابايت
    """
    return len(image_data) / (1024 * 1024)
