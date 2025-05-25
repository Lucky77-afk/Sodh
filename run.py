#!/usr/bin/env python3

"""
Minimal entry point for running the Streamlit application on Streamlit Cloud.
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
    
    try:
        # Import streamlit and run the app directly
        import streamlit.web.bootstrap as bootstrap
        from streamlit import config as _config
        
        # Set config options directly
        _config.set_option("server.port", int(os.getenv("PORT", "8501")))
        _config.set_option("server.address", "0.0.0.0")
        _config.set_option("server.enableCORS", True)
        _config.set_option("server.enableXsrfProtection", True)
        _config.set_option("browser.gatherUsageStats", False)
        
        # Run the app
        bootstrap.run(app_path, [], [])
        
    except Exception as e:
        print(f"Error running Streamlit app: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
