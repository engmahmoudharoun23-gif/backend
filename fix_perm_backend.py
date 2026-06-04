import os

def main():
    target = 'user_perms = user_doc.get("permissions", [])'
    replacement = '''user_perms = set(user_doc.get("permissions", []))
    for plist in user_doc.get("project_permissions", {}).values():
        user_perms.update(plist or [])'''
        
    with open('server.py', 'r', encoding='utf-8') as f:
        content = f.read()
        
    # We only want to replace it inside the work_permits endpoints
    # To do this safely, we will find "def get_work_permits", "def create_work_permit", "def update_work_permit", "def delete_work_permit"
    # and replace the permission lines in those blocks.
    
    # Simple search and replace for the exact strings in work_permits blocks
    content = content.replace(
        'user_perms = user_doc.get("permissions", [])\n    if user_doc.get("role") != "admin" and "work_permits" not in user_perms:',
        'user_perms = set(user_doc.get("permissions", []))\n    for plist in user_doc.get("project_permissions", {}).values():\n        user_perms.update(plist or [])\n    if user_doc.get("role") != "admin" and "work_permits" not in user_perms:'
    )
    
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Patched server.py successfully")

    # Also copy to server_recovered.py
    import shutil
    if os.path.exists('server_recovered.py'):
        shutil.copy('server.py', 'server_recovered.py')

if __name__ == "__main__":
    main()
