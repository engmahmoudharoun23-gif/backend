# Main Application Entry Point
# This file re-exports from the original server.py to maintain backward compatibility
# During migration, endpoints will be gradually moved to the new structure

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import everything from the original server.py
# This maintains backward compatibility while we migrate
from server import app, api_router, db

# Re-export for gunicorn/uvicorn
__all__ = ["app"]
