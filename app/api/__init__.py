# API Routes Package
from fastapi import APIRouter

# Import route modules
# Note: These are the new modular routes, the old server.py still handles most endpoints
# Gradually, endpoints will be moved here

# Main API router
api_router = APIRouter()

# Include route modules (uncomment as routes are migrated)
from .routes.auth import router as auth_router
from .routes.users import router as users_router
from .routes.reports import router as reports_router
from .routes.projects import router as projects_router
from .routes.governorates import router as governorates_router
from .routes.invoices import router as invoices_router
from .routes.connections import router as connections_router
from .routes.employee_requests import router as employee_requests_router
from .routes.dashboard import router as dashboard_router

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(reports_router)
api_router.include_router(projects_router)
api_router.include_router(governorates_router)
api_router.include_router(invoices_router)
api_router.include_router(connections_router)
api_router.include_router(employee_requests_router)
api_router.include_router(dashboard_router)

__all__ = ["api_router"]
