from api.api_chat import router as chat_router
from api.api_history import router as history_router
from api.human_approve_reject import router as approve_router
from api.clear_memory import router as memory_router
from api.model_region_status import router as status_router
from api.document_upload import router as upload_router
from api.fetch_uploaded_docs import router as documents_router
from api.clear_vector_db import router as reset_vector_db
from api.get_vectordb_stats import router as vectordb_stats_router
from api.api_settings import router as settings_router
from api.telemetry import router as get_live_telemetry
from api.predict import router as get_live_prediction
from api.auto_plant_agent import router as run_palnt_agent
from api.api_emergency_stop_resume import router as emergency_stop
from api.api_emergency_stop_resume import router as resume_plant
from api.auth import router as register
from api.auth import router as login


__all__ = [
    "chat_router",
    "history_router",
    "approve_router",
    "memory_router",
    "status_router",
    "upload_router",
    "documents_router",
    "reset_vector_db",
    "vectordb_stats_router",
    "settings_router",
    "get_live_telemetry",
    "get_live_prediction",
    "run_palnt_agent",
    "emergency_stop",
    "resume_plant",
    "register",
    "login"
]
