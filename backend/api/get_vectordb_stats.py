from fastapi import APIRouter
import chromadb

router = APIRouter()

# Connect to Docker ChromaDB
chroma_client = chromadb.HttpClient(host='localhost', port=8001)

@router.get("/api/vector-db/stats")
@router.get("/api/vectordb/stats")
async def get_vector_db_stats():
    """Returns metadata about the ChromaDB collection."""
    try:
        # Check if company_docs exists
        collections = chroma_client.list_collections()
        has_collection = any(
            (c.name if hasattr(c, "name") else str(c)) == "company_docs"
            for c in collections
        )
        if not has_collection:
            return {"total_chunks": 0, "status": "empty"}

        collection = chroma_client.get_collection(name="company_docs")
        total_chunks = collection.count()

        return {
            "total_chunks": total_chunks,
            "status": "active" if total_chunks > 0 else "empty"
        }
    except Exception as e:
        return {"total_chunks": 0, "status": "error", "message": str(e)}
