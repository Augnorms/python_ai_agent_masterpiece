from fastapi import APIRouter
import chromadb

router = APIRouter()

# Connect to Docker ChromaDB
chroma_client = chromadb.HttpClient(host='localhost', port=8001)

@router.post("/api/clear-chroma")
@router.delete("/api/clear-chroma")
@router.post("/api/reset_vector_db")
@router.delete("/api/reset_vector_db")
async def reset_vector_db():
    """Deletes the entire collection from ChromaDB."""
    try:
        try:
            chroma_client.delete_collection(name="company_docs")
        except Exception as del_err:
            if "does not exist" not in str(del_err).lower():
                raise del_err
        # Ensure clean collection is ready for subsequent ingests/queries
        chroma_client.get_or_create_collection(name="company_docs")
        return {"status": "success", "message": "ChromaDB collection 'company_docs' has been completely wiped."}
    except Exception as e:
        return {"status": "error", "message": f"Failed to reset ChromaDB: {str(e)}"}
