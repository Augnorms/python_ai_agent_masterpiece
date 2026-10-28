from fastapi import APIRouter
from database.database import delete_session

router = APIRouter()


@router.delete("/api/memory/{session_id}")
async def clear_memory(session_id: str):
    delete_session(session_id)
    return {"status": "success", "message": "Memory cleared"}
