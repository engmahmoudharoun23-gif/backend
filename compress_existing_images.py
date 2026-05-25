#!/usr/bin/env python3
"""
Script لضغط الصور الموجودة في قاعدة البيانات
يقوم بضغط جميع صور البلاغات إلى حجم أقصى 3 ميجابايت
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import base64
from PIL import Image
from io import BytesIO

# تحميل المتغيرات من .env
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# الاتصال بقاعدة البيانات
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']


def compress_image_data(image_data: str, max_size_mb: float = 3.0) -> str:
    """
    ضغط الصورة إلى حجم أقصى محدد (بالميجابايت)
    
    Args:
        image_data: بيانات الصورة بصيغة base64 data URL
        max_size_mb: الحجم الأقصى بالميجابايت (افتراضي: 3 MB)
    
    Returns:
        بيانات الصورة المضغوطة بصيغة base64 data URL
    """
    try:
        # استخراج نوع الصورة والبيانات من data URL
        if ',' in image_data:
            header, base64_data = image_data.split(',', 1)
            content_type = header.split(':')[1].split(';')[0] if ':' in header else 'image/jpeg'
        else:
            base64_data = image_data
            content_type = 'image/jpeg'
        
        # تحويل من base64 إلى bytes
        image_bytes = base64.b64decode(base64_data)
        current_size_mb = len(image_bytes) / (1024 * 1024)
        
        # إذا كانت الصورة أصغر من الحد الأقصى، إرجاعها كما هي
        if current_size_mb <= max_size_mb:
            return image_data
        
        # فتح الصورة باستخدام PIL
        img = Image.open(BytesIO(image_bytes))
        
        # تحويل الصور RGBA إلى RGB
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        
        # تحديد جودة الضغط بناءً على الحجم الحالي
        quality = 85
        if current_size_mb > 10:
            quality = 70
        elif current_size_mb > 5:
            quality = 75
        elif current_size_mb > 3:
            quality = 80
        
        # محاولات متعددة لضغط الصورة
        for attempt in range(3):
            output = BytesIO()
            img.save(output, format='JPEG', quality=quality, optimize=True)
            compressed_bytes = output.getvalue()
            compressed_size_mb = len(compressed_bytes) / (1024 * 1024)
            
            if compressed_size_mb <= max_size_mb:
                # نجح الضغط
                compressed_base64 = base64.b64encode(compressed_bytes).decode('utf-8')
                return f"data:image/jpeg;base64,{compressed_base64}"
            
            # تقليل الجودة للمحاولة التالية
            quality -= 10
            
            # إذا كانت الصورة كبيرة جداً، تقليل الدقة
            if compressed_size_mb > max_size_mb * 1.5:
                img = img.resize((int(img.width * 0.8), int(img.height * 0.8)), Image.Resampling.LANCZOS)
        
        # إذا فشلت جميع المحاولات، إرجاع آخر نسخة مضغوطة
        compressed_base64 = base64.b64encode(compressed_bytes).decode('utf-8')
        return f"data:image/jpeg;base64,{compressed_base64}"
        
    except Exception as e:
        print(f"⚠️ خطأ في ضغط الصورة: {str(e)}")
        # في حالة الخطأ، إرجاع الصورة الأصلية
        return image_data


async def compress_all_images():
    """
    ضغط جميع الصور في قاعدة البيانات
    """
    print("=" * 60)
    print("🔄 بدء عملية ضغط الصور الموجودة في قاعدة البيانات")
    print("=" * 60)
    
    # الاتصال بقاعدة البيانات
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        # جلب جميع البلاغات التي تحتوي على صور
        reports = await db.reports.find({"images": {"$exists": True, "$ne": []}}).to_list(None)
        
        total_reports = len(reports)
        print(f"\n📊 عدد البلاغات التي تحتوي على صور: {total_reports}")
        
        if total_reports == 0:
            print("✅ لا توجد صور للضغط")
            return
        
        total_images = 0
        compressed_images = 0
        total_saved_mb = 0.0
        
        for idx, report in enumerate(reports, 1):
            report_id = report.get('id')
            report_number = report.get('report_number', 'غير معروف')
            images = report.get('images', [])
            
            print(f"\n[{idx}/{total_reports}] معالجة البلاغ: {report_number}")
            print(f"    عدد الصور: {len(images)}")
            
            new_images = []
            report_saved_mb = 0.0
            
            for img_idx, image_data in enumerate(images, 1):
                try:
                    # حساب الحجم الأصلي
                    if ',' in image_data:
                        _, base64_data = image_data.split(',', 1)
                    else:
                        base64_data = image_data
                    
                    original_bytes = base64.b64decode(base64_data)
                    original_size_mb = len(original_bytes) / (1024 * 1024)
                    
                    # ضغط الصورة
                    compressed_data = compress_image_data(image_data, max_size_mb=3.0)
                    
                    # حساب الحجم بعد الضغط
                    if ',' in compressed_data:
                        _, compressed_base64 = compressed_data.split(',', 1)
                    else:
                        compressed_base64 = compressed_data
                    
                    compressed_bytes = base64.b64decode(compressed_base64)
                    compressed_size_mb = len(compressed_bytes) / (1024 * 1024)
                    
                    saved_mb = original_size_mb - compressed_size_mb
                    
                    if saved_mb > 0.01:  # إذا تم توفير أكثر من 0.01 MB
                        print(f"    ✓ صورة {img_idx}: {original_size_mb:.2f} MB → {compressed_size_mb:.2f} MB (توفير: {saved_mb:.2f} MB)")
                        compressed_images += 1
                        report_saved_mb += saved_mb
                    else:
                        print(f"    • صورة {img_idx}: {original_size_mb:.2f} MB (لا يوجد ضغط مطلوب)")
                    
                    new_images.append(compressed_data)
                    total_images += 1
                    
                except Exception as e:
                    print(f"    ⚠️ خطأ في معالجة صورة {img_idx}: {str(e)}")
                    new_images.append(image_data)  # الاحتفاظ بالصورة الأصلية
            
            # تحديث البلاغ في قاعدة البيانات
            if new_images != images:
                await db.reports.update_one(
                    {"id": report_id},
                    {"$set": {"images": new_images}}
                )
                total_saved_mb += report_saved_mb
                print(f"    ✅ تم تحديث البلاغ - إجمالي التوفير: {report_saved_mb:.2f} MB")
        
        # طباعة النتائج النهائية
        print("\n" + "=" * 60)
        print("📈 ملخص النتائج:")
        print("=" * 60)
        print(f"✅ إجمالي البلاغات المعالجة: {total_reports}")
        print(f"✅ إجمالي الصور المعالجة: {total_images}")
        print(f"✅ الصور التي تم ضغطها: {compressed_images}")
        print(f"✅ إجمالي المساحة الموفرة: {total_saved_mb:.2f} MB ({total_saved_mb / 1024:.2f} GB)")
        print("=" * 60)
        print("🎉 اكتملت عملية الضغط بنجاح!")
        
    except Exception as e:
        print(f"\n❌ خطأ: {str(e)}")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(compress_all_images())
