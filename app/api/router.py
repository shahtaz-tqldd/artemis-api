from fastapi import APIRouter

from app.api.health.router import router as health_router 
from trading_agent.router import router as trading_agent_router

# Main API router
api_router = APIRouter()

# Endpoint routers
api_router.include_router(
    health_router,
    prefix="/health",
    tags=["Health"],
)
api_router.include_router(
    trading_agent_router,
    prefix="/trading-agent",
    tags=["Trading Agent"],
)
