from fastapi import APIRouter, UploadFile, File
from storage import upload_file_to_s3
from inject_rag.ingest_rag_service import process_and_ingest_file
import time

router = APIRouter()


@router.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    start_time = time.perf_counter()
    try:
        # 1. Read the file content
        file_content = await file.read()

        # 2. Upload to MinIO S3
        result = upload_file_to_s3(file_content, file.filename)

        # 3. Process the file for RAG
        rag_result = process_and_ingest_file(file_content, file.filename)

        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 1)

        return {
            "status": "success",
            "message": f"{result} || {rag_result}",
            "filename": file.filename,
            "elapsed_ms": elapsed_ms
        }

    except Exception as e:
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 1)
        return {
            "status": "error",
            "message": str(e),
            "elapsed_ms": elapsed_ms
        }
