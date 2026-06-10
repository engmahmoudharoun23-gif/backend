import re

path = r"d:\sery17-main\sery17-main\backend\server.py"

with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update headers in ALL export functions that match this pattern
old_headers = '''    headers = [
        "رقم", "المحافظة", "المشروع", "رقم البلاغ", "رقم الرخصة",
        "حالة المعالجة", "الحالة", "نوع البلاغ", "العمق (سم)", "القطر (ملم)",
        "اسم المقاول", "خط العرض", "خط الطول", "رخصة أسفلت",
        "الملاحظات", "تاريخ الاستلام", "تاريخ الإغلاق", "عدد الصور", "مراقب الاستشاري"
    ]'''

new_headers = '''    headers = [
        "رقم", "المحافظة", "المشروع", "رقم البلاغ", "رقم الرخصة",
        "حالة المعالجة", "الحالة", "نوع البلاغ", "العمق (سم)", "القطر (ملم)",
        "اسم المقاول", "خط العرض", "خط الطول", "رخصة أسفلت",
        "الملاحظات", "تاريخ الاستلام", "تاريخ المباشرة", "تاريخ الإغلاق", "عدد الصور", "مراقب الاستشاري"
    ]'''

code = code.replace(old_headers, new_headers)

# 2. Add start_date extraction in the loops
# The loops start with:
#         created_at = report.get('created_at')

old_date_extraction = '''        created_at = report.get('created_at')
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        elif not isinstance(created_at, datetime):
            created_at = None
        
        closed_at = report.get('closed_at')
        if isinstance(closed_at, str):
            closed_at = datetime.fromisoformat(closed_at)
        elif not isinstance(closed_at, datetime):
            closed_at = None'''

new_date_extraction = '''        created_at = report.get('created_at')
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        elif not isinstance(created_at, datetime):
            created_at = None
        
        start_date = report.get('start_date')
        if isinstance(start_date, str):
            try:
                start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            except:
                start_date = None
        elif not isinstance(start_date, datetime):
            start_date = None
            
        closed_at = report.get('closed_at')
        if isinstance(closed_at, str):
            try:
                closed_at = datetime.fromisoformat(closed_at.replace('Z', '+00:00'))
            except:
                closed_at = None
        elif not isinstance(closed_at, datetime):
            closed_at = None'''

code = code.replace(old_date_extraction, new_date_extraction)

# 3. Add start_date to row_data
# In row_data, we have:
#             report.get('notes', ''),  # الملاحظات
#             created_at.strftime('%Y-%m-%d %H:%M') if created_at else '',
#             closed_at.strftime('%Y-%m-%d %H:%M') if closed_at else '',

old_row_data = '''            report.get('notes', ''),  # الملاحظات
            created_at.strftime('%Y-%m-%d %H:%M') if created_at else '',
            closed_at.strftime('%Y-%m-%d %H:%M') if closed_at else '','''

new_row_data = '''            report.get('notes', ''),  # الملاحظات
            created_at.strftime('%Y-%m-%d %H:%M') if created_at else '',
            start_date.strftime('%Y-%m-%d') if start_date else '',
            closed_at.strftime('%Y-%m-%d %H:%M') if closed_at else '','''

# Some might not have `# الملاحظات` comment, let's use regex
import re
code = re.sub(
    r"(report\.get\('notes',\s*''\),.*?\n\s+)(created_at\.strftime\('%Y-%m-%d %H:%M'\)\s+if\s+created_at\s+else\s+'',\n\s+)(closed_at\.strftime\('%Y-%m-%d %H:%M'\)\s+if\s+closed_at\s+else\s+'',)",
    r"\1\2start_date.strftime('%Y-%m-%d') if start_date else '',\n            \3",
    code
)

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("Done updating export columns in backend!")
