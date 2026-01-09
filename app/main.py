import subprocess
import threading
import time
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure the project root is in PYTHONPATH so 'app' module is found
os.environ["PYTHONPATH"] = os.getcwd()

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def run_backend():
    try:
        logger.info("Starting Backend (Uvicorn) on port 9999...")
        # Use sys.executable to ensure we use the same python/venv
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.backend.api:app", 
            "--host", "0.0.0.0", 
            "--port", "9999"
        ], check=True)
    except Exception as e:
        logger.error(f"Backend failed: {e}")
        # In a real app, you might want to trigger a global shutdown here

def run_frontend():
    try:
        logger.info("Starting Frontend (Streamlit)...")
        # Correctly split the flags into separate list items
        subprocess.run([
            sys.executable, "-m", "streamlit", 
            "run", "app/frontend/ui.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0" 
        ], check=True)
    except Exception as e:
        logger.error(f"Frontend failed: {e}")

if __name__ == "__main__":
    try:
        # 1. Start Backend in a background thread
        backend_thread = threading.Thread(target=run_backend, daemon=True)
        backend_thread.start()

        # 2. Wait a moment for the API to initialize
        time.sleep(3)

        # 3. Start Frontend on the main thread
        # (This will block the script until you close Streamlit)
        run_frontend()

    except KeyboardInterrupt:
        logger.info("Shutting down services...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")