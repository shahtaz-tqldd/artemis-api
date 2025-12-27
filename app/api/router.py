from fastapi import APIRouter

from app.api.health.router import router as health_router 
from chat.router import router as chat_router

# Main API router
api_router = APIRouter()

# Endpoint routers
api_router.include_router(
    health_router,
    prefix="/health",
    tags=["Health"],
)
api_router.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat Session"],
)
