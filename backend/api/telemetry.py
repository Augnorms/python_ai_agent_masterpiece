from modbus_service import get_formatted_telemetry_table
from fastapi import APIRouter

router = APIRouter()

@router.get("/api/telemetry/live")
def get_live_telemetry():
    data, port, connected = get_formatted_telemetry_table()
    if not data:
        return {"status": "error", "message": "Could not connect to PLC"}
    return {"status": "success", "data": data, "modbus_connection":port, "modbus_status": connected}