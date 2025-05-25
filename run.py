#!/usr/bin/env python3
"""
Streamlit Cloud entry point.
"""
import os
import sys
from pathlib import Path

def main():
    # Set up paths
    project_root = Path(__file__).parent
    app_path = str(project_root / "sodh" / "app.py")
    
    # Set environment variables
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    os.environ["STREAMLIT_SERVER_PORT"] = os.getenv("PORT", "8501")
    
    # Add the project root to the Python path
    sys.path.append(str(project_root))
    
    # Import and run the app directly
    from streamlit.web import cli as st_cli
    
    # Prepare command line arguments
    streamlit_args = [
        "run",
        app_path,
        "--server.port", os.getenv("PORT", "8501"),
        "--server.address", "0.0.0.0",
        "--server.enableCORS", "true",
        "--server.enableXsrfProtection", "true",
        "--browser.gatherUsageStats", "false"
    ]
    
    # Run the app
    sys.exit(st_cli.main(streamlit_args))

if __name__ == "__main__":
    main()
