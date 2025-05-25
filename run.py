#!/usr/bin/env python3
"""
Entry point for Sodh - Solana Blockchain Explorer
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    # Get the path to the app
    app_path = str(Path(__file__).parent / "sodh" / "app.py")
    port = os.getenv("PORT", "8501")
    
    # Set environment variables for Streamlit
    env = os.environ.copy()
    
    # Configure Streamlit to use the health check endpoint
    env["STREAMLIT_SERVER_HEALTH_CHECK_ENABLED"] = "true"
    env["STREAMLIT_SERVER_HEALTH_CHECK_PATH"] = "/healthz"
    
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
        app_path
    ]
    
    print(f"Starting Streamlit server on port {port}")
    try:
        return subprocess.call(cmd, env=env)
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        print(f"Error starting Streamlit: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
