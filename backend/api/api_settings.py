from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Any
from database.database import get_swarm_settings, update_swarm_settings

router = APIRouter()


class SettingsUpdateRequest(BaseModel):
    session_id: Optional[str] = None
    sessionId: Optional[str] = None
    is_swarm_active: Optional[bool] = None
    isSwarmActive: Optional[bool] = None
    swarm_mode: Optional[str] = None
    swarmMode: Optional[str] = None
    max_steps: Optional[int] = None
    maxSteps: Optional[int] = None
    supervisor_model: Optional[str] = None
    model: Optional[str] = None
    selectedModel: Optional[str] = None
    custom_model_id: Optional[str] = None
    customModelId: Optional[str] = None
    temperature: Optional[float] = None
    embedding_model: Optional[str] = None
    embeddingModel: Optional[str] = None
    active_agents: Optional[Any] = None
    agents: Optional[Any] = None


@router.get("/api/settings")
@router.get("/api/settings/{session_id}")
async def get_settings(session_id: Optional[str] = None):
    """Retrieve the swarm settings for the specified session_id (defaults to 'default')."""
    try:
        sid = session_id or "default"
        settings = get_swarm_settings(session_id=sid)
        return {
            "status": "success",
            "session_id": sid,
            "data": settings
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/settings")
@router.put("/api/settings")
@router.post("/api/settings/{session_id}")
@router.put("/api/settings/{session_id}")
async def update_settings(payload: SettingsUpdateRequest, session_id: Optional[str] = None):
    """Update swarm configuration settings for the specified session_id in the database."""
    try:
        # Determine target session_id from body or path/query
        sid = payload.session_id or payload.sessionId or session_id or "default"

        # Resolve snake_case vs camelCase field aliases
        is_swarm_active = payload.is_swarm_active if payload.is_swarm_active is not None else payload.isSwarmActive
        swarm_mode = payload.swarm_mode if payload.swarm_mode is not None else payload.swarmMode
        max_steps = payload.max_steps if payload.max_steps is not None else payload.maxSteps
        
        supervisor_model = None
        if payload.supervisor_model is not None:
            supervisor_model = payload.supervisor_model
        elif payload.model is not None:
            supervisor_model = payload.model
        elif payload.selectedModel is not None:
            supervisor_model = payload.selectedModel

        custom_model_id = payload.custom_model_id if payload.custom_model_id is not None else payload.customModelId
        temperature = payload.temperature
        embedding_model = payload.embedding_model if payload.embedding_model is not None else payload.embeddingModel
        
        active_agents = payload.active_agents if payload.active_agents is not None else payload.agents

        updated = update_swarm_settings(
            session_id=sid,
            is_swarm_active=is_swarm_active,
            swarm_mode=swarm_mode,
            max_steps=max_steps,
            supervisor_model=supervisor_model,
            custom_model_id=custom_model_id,
            temperature=temperature,
            embedding_model=embedding_model,
            active_agents=active_agents
        )

        return {
            "status": "success",
            "message": f"Swarm settings updated successfully for session '{sid}'",
            "session_id": sid,
            "data": updated
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
