#!/usr/bin/env python3
"""
Entry point for Sodh - Solana Blockchain Explorer
"""
import os
import sys
from pathlib import Path

def main():
    # Set environment variables for Streamlit
    os.environ["STREAMLIT_SERVER_ENABLE_STATIC_SERVING"] = "false"
    os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = "false"
    os.environ["STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION"] = "false"
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    
    # Get the path to the app
    app_path = str(Path(__file__).parent / "sodh" / "app.py")
    port = os.getenv("PORT", "8501")
    
    # Run Streamlit
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
    
    print(f"Starting Streamlit on port {port}")
    os.execvp(cmd[0], cmd)

if __name__ == "__main__":
    main()
