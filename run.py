#!/usr/bin/env python3

"""
Entry point for running the Streamlit application on Streamlit Cloud.
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

def main():
    """Main entry point for the application."""
    # Path to the app
    app_path = str(project_root / "sodh" / "app.py")
    
    # Import streamlit here to ensure environment is set first
    import streamlit.web.bootstrap
    
    # Configure streamlit arguments
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--server.port=$PORT",
        "--server.address=0.0.0.0",
        "--server.enableCORS=true",
        "--server.enableXsrfProtection=true",
        "--logger.level=error"
    ]
    
    # Run the Streamlit app
    sys.exit(streamlit.web.bootstrap.main())

if __name__ == "__main__":
    main()
