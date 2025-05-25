"""
FastAPI application to serve Streamlit app with health checks.
"""
import os
import sys
import subprocess
import threading
import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse
from pathlib import Path

app = FastAPI()
STREAMLIT_PORT = 8501

# Start Streamlit in a subprocess
def start_streamlit():
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "sodh/app.py",
        "--server.port", str(STREAMLIT_PORT),
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false",
        "--server.maxUploadSize", "200",
        "--server.fileWatcherType", "none",
        "--server.runOnSave", "false",
        "--browser.serverAddress", "0.0.0.0",
        "--browser.serverPort", str(STREAMLIT_PORT)
    ]
    subprocess.Popen(cmd, env=os.environ)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Root endpoint redirects to Streamlit
@app.get("/")
async def root():
    return RedirectResponse(url=f"http://localhost:{STREAMLIT_PORT}")

if __name__ == "__main__":
    # Start Streamlit in a separate thread
    streamlit_thread = threading.Thread(target=start_streamlit, daemon=True)
    streamlit_thread.start()
    
    # Start FastAPI server
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
