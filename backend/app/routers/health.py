# app/routers/health.py
from fastapi import APIRouter
from datetime import datetime
from ..core.config import APP_NAME, APP_ENV

router = APIRouter()

@router.get("/health", tags=["health"])
async def health():
    """
    Basic health check. Returns service name, environment and current server time.
    """
    return {
        "status": "ok",
        "service": APP_NAME,
        "env": APP_ENV,
        "time": datetime.utcnow().isoformat() + "Z",
    }
