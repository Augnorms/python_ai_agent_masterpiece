from fastapi import APIRouter

router = APIRouter()


@router.get("/api/status")
async def get_status():
    # In a real app, you might query the cloud provider here.
    return {
        "status": "active",
        "region": "Ghana-Accra",
        "model": "openai/gpt-oss-20b"
    }
