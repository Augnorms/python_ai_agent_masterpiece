import subprocess
from fastapi import APIRouter

router = APIRouter()

@router.post("/api/plant/emergency-stop")
async def emergency_stop():
    try:
        # Runs the Docker CLI command to stop the simulator container
        subprocess.run(["docker", "stop", "desal-sim"], check=True)
        return {"status": "success", "message": "Emergency Stop Activated. Plant Simulator Halted."}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": f"Failed to stop plant: {str(e)}"}

@router.post("/api/plant/resume")
async def resume_plant():
    try:
        # Runs the Docker CLI command to start the simulator container
        subprocess.run(["docker", "start", "desal-sim"], check=True)
        return {"status": "success", "message": "Plant Resumed. Simulator Started."}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": f"Failed to resume plant: {str(e)}"}