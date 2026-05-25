with open('server.py', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        if 'get_projects_with_permission' in line:
            print(f"Line {idx}: {line.strip()}")
