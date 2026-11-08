import threading
import time
from pymodbus.client import ModbusTcpClient

PLC_IP = "127.0.0.1"
PLC_PORT = 502

_modbus_lock = threading.Lock()
_cache_data = None
_cache_port = f"{PLC_IP}:{PLC_PORT}"
_cache_connected = False
_cache_time = 0
CACHE_TTL = 0.5  # Cache for 500ms to eliminate socket collision between concurrent endpoints

def get_live_modbus_data():
    """Connects to the PLC and reads the live registers with concurrency lock & short TTL cache."""
    global _cache_data, _cache_port, _cache_connected, _cache_time

    now = time.time()
    # If we read the PLC very recently (<500ms ago), reuse it immediately
    if _cache_data and (now - _cache_time) < CACHE_TTL:
        return _cache_data, _cache_port, _cache_connected

    # Acquire lock with a timeout to prevent deadlocks
    acquired = _modbus_lock.acquire(timeout=2.0)
    if not acquired:
        if _cache_data:
            return _cache_data, _cache_port, _cache_connected
        return {"error": "Modbus client lock timeout."}, f"{PLC_IP}:{PLC_PORT}", False

    client = None
    try:
        client = ModbusTcpClient(PLC_IP, port=PLC_PORT, timeout=1.5)
        connected = client.connect() 

        if not connected:
            return {"error": "Could not connect to PLC Modbus server."}, f"{PLC_IP}:{PLC_PORT}", False
        
        # Read holding registers (Address 0 to 10)
        response = client.read_holding_registers(0, count=10)
        
        if response.isError():
            return {"error": "Failed to read Modbus registers."}, f"{PLC_IP}:{PLC_PORT}", False
            
        regs = response.registers
        
        # Scale the data back (as seen in simulator.py)
        data = {
            "feed_flowrate": regs[0] / 10.0,
            "feed_tds": float(regs[1]),
            "feed_temperature": regs[2] / 10.0,
            "feed_salinity": regs[6] / 10.0,
            "recovery": regs[7] / 10.0,
            "flux": regs[8] / 10.0,
            "pressure_drop": regs[9] / 10.0,
        }

        _cache_data = data
        _cache_connected = True
        _cache_time = time.time()

        return data, f"{PLC_IP}:{PLC_PORT}", True
        
    except Exception as e:
        if _cache_data:
            return _cache_data, _cache_port, True
        return {"error": str(e)}, f"{PLC_IP}:{PLC_PORT}", False
    finally:
        if client:
            try:
                client.close()
            except Exception:
                pass
        _modbus_lock.release()



def get_formatted_telemetry_table():
    """Returns the Modbus data formatted for the UI table."""
    data, port, connected = get_live_modbus_data()
    
    if "error" in data:
        return [], port, False

    # Map the live data to the exact rows for the UI
    table_rows = [
        {
            "address": "40001",
            "tag": "Feed Flowrate",
            "type": "INT16 (x10)",
            "raw": int(data["feed_flowrate"] * 10),
            "scaled": round(data["feed_flowrate"], 2),
            "unit": "m3/h",
            "health": "GOOD"
        },
        {
            "address": "40002",
            "tag": "Feed TDS",
            "type": "INT16",
            "raw": int(data["feed_tds"]),
            "scaled": round(data["feed_tds"], 2),
            "unit": "ppm",
            "health": "GOOD"
        },
        {
            "address": "40003",
            "tag": "Feed Temperature",
            "type": "INT16 (x10)",
            "raw": int(data["feed_temperature"] * 10),
            "scaled": round(data["feed_temperature"], 2),
            "unit": "°C",
            "health": "GOOD"
        },
        {
            "address": "40007",
            "tag": "Feed Salinity",
            "type": "INT16 (x10)",
            "raw": int(data["feed_salinity"] * 10),
            "scaled": round(data["feed_salinity"], 2),
            "unit": "g/L",
            "health": "GOOD"
        },
        {
            "address": "40008",
            "tag": "Recovery",
            "type": "INT16 (x10)",
            "raw": int(data["recovery"] * 10),
            "scaled": round(data["recovery"], 2),
            "unit": "%",
            "health": "GOOD"
        },
        {
            "address": "40009",
            "tag": "Flux",
            "type": "INT16 (x10)",
            "raw": int(data["flux"] * 10),
            "scaled": round(data["flux"], 2),
            "unit": "LMH",
            "health": "GOOD"
        },
        {
            "address": "40010",
            "tag": "Pressure Drop",
            "type": "INT16 (x10)",
            "raw": int(data["pressure_drop"] * 10),
            "scaled": round(data["pressure_drop"], 2),
            "unit": "bar",
            "health": "GOOD"
        }
    ]
    
    return table_rows, port, connected


if __name__ == "__main__":
    # This block only runs if you execute this file directly (python modbus_service.py)
    print("Testing Modbus connection...")
    result = get_live_modbus_data()
    print("Result:", result)