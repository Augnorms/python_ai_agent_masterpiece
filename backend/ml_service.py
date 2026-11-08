import os
import joblib
import numpy as np
import time
from modbus_service import get_live_modbus_data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "pred_models")
permeat_flow = joblib.load(os.path.join(MODEL_DIR, "permeate_flowrate_model_rf.pkl"))
permeat_tds = joblib.load(os.path.join(MODEL_DIR, "permeate_flowtds_model_rf.pkl"))

def predict_live_status():
    """Reads live Modbus data and runs both models, returning the exact format the UI needs."""
    
    # 1. Get live data from the PLC
    data, port, connected = get_live_modbus_data()
    
    if not connected or "error" in data:
        return {
            "status": "error",
            "message": "Cannot predict because PLC is disconnected."
        }

    try:
        # 2. Start timer
        start_time = time.time()

        # 3. Extract features in the exact order the model was trained on
        features = np.array([[
            data["feed_flowrate"],
            data["feed_tds"],
            data["feed_salinity"],
            data["feed_temperature"],
            data["recovery"],
            data["flux"],
            data["pressure_drop"]
        ]])

        # 4. Run predictions
        pred_flow = permeat_flow.predict(features)[0]
        pred_tds = permeat_tds.predict(features)[0]

        # 5. Determine TDS Quality Status based on README
        if pred_tds < 50:
            status = "Excellent"
        elif pred_tds < 100:
            status = "Good"
        elif pred_tds < 200:
            status = "Warning"
        else:
            status = "Poor"

        # 6. Calculate Latency
        elapsed_ms = int((time.time() - start_time) * 1000)

        # 7. Return the exact format the Vue frontend expects
        return {
            "status": "success",
            "inputs": data,
            "predictions": {
                "alpha": {
                    "flow": round(pred_flow, 2),
                    "tds": None,           # Alpha only predicts flow
                    "latency_ms": elapsed_ms
                },
                "beta": {
                    "flow": None,          # Beta only predicts TDS
                    "tds": round(pred_tds, 2),
                    "quality_status": status,
                    "latency_ms": elapsed_ms
                }
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }