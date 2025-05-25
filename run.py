#!/usr/bin/env python3
"""
Entry point for Sodh - Solana Blockchain Explorer
"""
import os
import sys
import time
import signal
import subprocess
from pathlib import Path

def main():
    # Get the path to the app
    app_path = str(Path(__file__).parent / "sodh" / "app.py")
    port = os.getenv("PORT", "8501")
    
    # Set environment variables for Streamlit
    env = os.environ.copy()
    
    # Configure Streamlit to use the health check endpoint
    env["STREAMLIT_SERVER_ENABLE_STATIC_FILE_HANDLING"] = "true"
    env["STREAMLIT_SERVER_ENABLE_CORS"] = "false"
    env["STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION"] = "false"
    env["STREAMLIT_SERVER_HEADLESS"] = "true"
    
    # Run Streamlit in a subprocess
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
        "--server.enableStaticServing", "true",
        app_path
    ]
    
    print(f"Starting Streamlit on port {port}")
    os.execvp(cmd[0], cmd)

if __name__ == "__main__":
    main()
