from fastapi import APIRouter
from storage import list_files_in_s3

router = APIRouter()


@router.get("/api/documents")
async def get_documents():
    try:
        files = list_files_in_s3()
        return {"status": "success", "documents": files}
    except Exception as e:
        return {"status": "error", "message": str(e)}
