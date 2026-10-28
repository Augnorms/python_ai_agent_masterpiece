from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import (
    chat_router,
    history_router,
    approve_router,
    memory_router,
    status_router,
    upload_router,
    documents_router,
    reset_vector_db,
    vectordb_stats_router
)

app = FastAPI()

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(chat_router)
app.include_router(history_router)
app.include_router(approve_router)
app.include_router(memory_router)
app.include_router(status_router)
app.include_router(upload_router)
app.include_router(documents_router)
app.include_router(reset_vector_db)
app.include_router(vectordb_stats_router)

app.include_router(vectordb_stats_router)