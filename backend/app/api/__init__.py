from fastapi import APIRouter
from app.api.v1 import routes_health

def get_v1_router() -> APIRouter:
    """
    Returns an APIRouter with all v1 routers included.
    """
    router = APIRouter()
    router.include_router(routes_health.router, tags=["health"])
    return router
