import shutil
import os

src = r"d:\$RECYCLE.BIN\S-1-5-21-2326408567-1304265601-955886391-1001\$R236WSH\sery17-main\backend\server.py"
dst = r"d:\sery17-main\sery17-main\backend\server_recovered.py"

try:
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Successfully copied from {src} to {dst}")
        print(f"Size: {os.path.getsize(dst)} bytes")
    else:
        print(f"Source file not found: {src}")
except Exception as e:
    print(f"Error: {e}")
