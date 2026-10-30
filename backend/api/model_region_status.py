from fastapi import APIRouter
from database.database import get_swarm_settings

router = APIRouter()


@router.get("/api/status")
async def get_status(session_id: str = "default"):
    settings = get_swarm_settings(session_id)
    is_active = settings.get("is_swarm_active", True)
    model = settings.get("custom_model_id") or settings.get("supervisor_model") or "llama-3.3-70b-versatile"

    return {
        "status": "active" if is_active else "standby",
        "is_swarm_active": is_active,
        "region": "Ghana-Accra",
        "model": model,
        "swarm_mode": settings.get("swarm_mode", "autonomous")
    }
