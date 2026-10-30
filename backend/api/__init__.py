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
    "settings_router"
]
