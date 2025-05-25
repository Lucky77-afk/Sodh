#!/usr/bin/env python3

"""
Entry point for running the Streamlit application on Streamlit Cloud.
"""
import os
import sys
from pathlib import Path

if __name__ == "__main__":
    # Add the project root to the Python path
    project_root = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_root))
    
    # Path to the app
    app_path = str(project_root / "sodh" / "app.py")
    
    # Set environment variables
    os.environ["STREAMLIT_SERVER_PORT"] = os.getenv("PORT", "8501")
    os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    
    # Import streamlit here to ensure environment is set first
    from streamlit.web import cli as st_cli
    
    # Run the Streamlit app directly
    sys.argv = ["streamlit", "run", app_path]
    sys.exit(st_cli.main())
