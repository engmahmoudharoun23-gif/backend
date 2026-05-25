"""
Image Processing Utilities
أدوات معالجة الصور
"""
import io
import base64
import logging
from PIL import Image
from typing import Optional, List
from ..config import get_settings

logger = logging.getLogger(__name__)


def compress_image(image_data: str, max_size: int = None, quality: int = None) -> str:
    """
    Compress base64 image
    ضغط صورة base64
    """
    settings = get_settings()
    max_size = max_size or settings.MAX_IMAGE_DIMENSION
    quality = quality or settings.IMAGE_COMPRESSION_QUALITY
    
    try:
        # Extract base64 data
        if ',' in image_data:
            header, data = image_data.split(',', 1)
        else:
            header = 'data:image/jpeg;base64'
            data = image_data
        
        # Decode image
        image_bytes = base64.b64decode(data)
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'RGBA':
                background.paste(img, mask=img.split()[3])
            else:
                background.paste(img)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if too large
        if img.width > max_size or img.height > max_size:
            ratio = min(max_size / img.width, max_size / img.height)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Compress
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        compressed_data = base64.b64encode(output.getvalue()).decode()
        
        return f"data:image/jpeg;base64,{compressed_data}"
    
    except Exception as e:
        logger.error(f"Image compression error: {e}")
        return image_data  # Return original on error


def compress_images(images: List[str], max_size: int = None, quality: int = None) -> List[str]:
    """
    Compress multiple images
    ضغط عدة صور
    """
    return [compress_image(img, max_size, quality) for img in images if img]


def get_image_size(image_data: str) -> tuple:
    """
    Get image dimensions
    جلب أبعاد الصورة
    """
    try:
        if ',' in image_data:
            _, data = image_data.split(',', 1)
        else:
            data = image_data
        
        image_bytes = base64.b64decode(data)
        img = Image.open(io.BytesIO(image_bytes))
        return img.size
    except Exception as e:
        logger.error(f"Error getting image size: {e}")
        return (0, 0)


def validate_image(image_data: str, max_size_bytes: int = None) -> bool:
    """
    Validate image data
    التحقق من صحة الصورة
    """
    settings = get_settings()
    max_size_bytes = max_size_bytes or settings.MAX_UPLOAD_SIZE
    
    try:
        if ',' in image_data:
            _, data = image_data.split(',', 1)
        else:
            data = image_data
        
        image_bytes = base64.b64decode(data)
        
        # Check size
        if len(image_bytes) > max_size_bytes:
            return False
        
        # Try to open as image
        img = Image.open(io.BytesIO(image_bytes))
        img.verify()
        
        return True
    except Exception:
        return False
