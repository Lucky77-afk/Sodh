#!/usr/bin/env python3

"""
Entry point for running the Streamlit application on Streamlit Cloud.
"""
import os
import sys
from pathlib import Path

def main():
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
    from streamlit import config as _config
    import streamlit.web.bootstrap
    
    # Clear any existing runtime
    if hasattr(streamlit, '_is_running_with_streamlit'):
        streamlit._is_running_with_streamlit = False
    
    # Configure Streamlit
    _config.set_option("server.port", int(os.getenv("PORT", "8501")))
    _config.set_option("server.address", "0.0.0.0")
    _config.set_option("server.enableCORS", True)
    _config.set_option("server.enableXsrfProtection", True)
    _config.set_option("browser.gatherUsageStats", False)
    
    # Run the app directly
    streamlit.web.bootstrap.run(
        app_path,
        args=[],
        flag_options={
            "server.port": int(os.getenv("PORT", "8501")),
            "server.address": "0.0.0.0",
            "server.enableCORS": True,
            "server.enableXsrfProtection": True,
            "browser.gatherUsageStats": False,
        }
    )

if __name__ == "__main__":
    main()
