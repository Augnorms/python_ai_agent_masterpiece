from fastapi import APIRouter
from ml_service import predict_live_status

router = APIRouter()

@router.get("/api/predict/live")
def get_live_prediction():
    result = predict_live_status()
    return result