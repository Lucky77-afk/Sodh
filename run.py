#!/usr/bin/env python3
"""
Entry point for Sodh - Solana Blockchain Explorer
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    # Handle health check
    if os.environ.get('HEALTH_CHECK') == 'true':
        print("Health check passed")
        return 0

    # Get the path to the app
    app_path = str(Path(__file__).parent / "sodh" / "app.py")
    
    # Set environment variables for Streamlit
    env = os.environ.copy()
    env["STREAMLIT_SERVER_PORT"] = os.getenv("PORT", "8501")
    env["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
    env["STREAMLIT_SERVER_HEADLESS"] = "true"
    
    # Run Streamlit in a subprocess
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "--server.port", os.getenv("PORT", "8501"),
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false",
        "--server.maxUploadSize", "200",
        "--server.fileWatcherType", "none",
        app_path
    ]
    
    try:
        return subprocess.call(cmd, env=env)
    except KeyboardInterrupt:
        return 0

if __name__ == "__main__":
    sys.exit(main())
