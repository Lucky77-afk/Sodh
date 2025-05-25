#!/usr/bin/env python3

"""
Entry point for running the Streamlit application.
"""
import os
import sys
import subprocess
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    # Set environment variables
    env = os.environ.copy()
    env["STREAMLIT_SERVER_ENABLE_STATIC_SERVING"] = "true"
    env["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
    env["STREAMLIT_SERVER_HEADLESS"] = "true"
    env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    
    # Path to the app
    app_path = str(project_root / "sodh" / "app.py")
    
    # Build the command to run Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "--server.port", "8501",
        "--server.address", "0.0.0.0",
        "--server.enableCORS", "true",
        "--server.enableXsrfProtection", "true",
        "--theme.base", "dark",
        "--theme.primaryColor", "#14F195",
        "--theme.backgroundColor", "#131313",
        "--theme.secondaryBackgroundColor", "#1E1E1E",
        "--theme.textColor", "#FFFFFF",
        "--theme.font", "sans serif",
        app_path
    ]
    
    # Run the Streamlit app
    subprocess.run(cmd, env=env)
