#!/usr/bin/env python3
"""
Entry point for Sodh - Solana Blockchain Explorer with Health Check
"""
import os
import sys
import time
import signal
import subprocess
import threading
import uvicorn
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable to track Streamlit process
streamlit_process = None

@app.get("/healthz")
async def health_check():
    """Health check endpoint"""
    if streamlit_process and streamlit_process.poll() is None:
        return Response(status_code=status.HTTP_200_OK, content="OK")
    return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content="Streamlit not running")

def run_streamlit():
    """Run Streamlit in a subprocess"""
    global streamlit_process
    
    app_path = str(Path(__file__).parent / "sodh" / "app.py")
    port = os.getenv("PORT", "8501")
    
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "--server.port", port,
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false",
        "--server.maxUploadSize", "200",
        "--server.fileWatcherType", "none",
        "--server.runOnSave", "false",
        "--browser.serverAddress", "0.0.0.0",
        "--browser.serverPort", port,
        "--theme.base", "dark",
        "--theme.primaryColor", "#14F195",
        "--theme.backgroundColor", "#131313",
        "--theme.secondaryBackgroundColor", "#1E1E1E",
        "--server.enableWebsocketCompression", "true",
        app_path
    ]
    
    env = os.environ.copy()
    streamlit_process = subprocess.Popen(cmd, env=env)
    return streamlit_process.wait()

def signal_handler(signum, frame):
    """Handle termination signals"""
    global streamlit_process
    if streamlit_process:
        streamlit_process.terminate()
        streamlit_process.wait()
    sys.exit(0)

def main():
    """Main entry point"""
    # Set up signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start Streamlit in a separate thread
    streamlit_thread = threading.Thread(target=run_streamlit, daemon=True)
    streamlit_thread.start()
    
    # Wait a moment for Streamlit to start
    time.sleep(2)
    
    # Start the FastAPI server for health checks
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info",
        access_log=False
    )

if __name__ == "__main__":
    main()
