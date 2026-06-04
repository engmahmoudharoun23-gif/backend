import os
import shutil

def main():
    # Since I successfully patched server.py, I can just copy server.py to server_recovered.py
    # IF the user is running server_recovered.py, it will pick up the changes.
    src = "server.py"
    dest = "server_recovered.py"
    if os.path.exists(dest):
        shutil.copy(src, dest)
        print("Copied server.py to server_recovered.py")

if __name__ == "__main__":
    main()
