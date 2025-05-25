#!/usr/bin/env python3
"""
Minimal Streamlit Cloud entry point.
"""
import os
import sys
from pathlib import Path

def main():
    try:
        # Set up paths
        project_root = Path(__file__).parent
        app_path = str(project_root / "sodh" / "app.py")
        
        # Set environment variables
        os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
        os.environ["STREAMLIT_SERVER_PORT"] = os.getenv("PORT", "8501")
        os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
        
        # Add the project root to the Python path
        sys.path.append(str(project_root))
        
        # Import streamlit components
        from streamlit import config as _config
        from streamlit.web import cli as st_cli
        from streamlit.runtime.runtime import Runtime
        
        # Check if a runtime instance already exists
        if not Runtime._instance:
            # Configure Streamlit
            _config.set_option("server.port", int(os.getenv("PORT", "8501")))
            _config.set_option("server.address", "0.0.0.0")
            _config.set_option("server.enableCORS", True)
            _config.set_option("server.enableXsrfProtection", True)
            _config.set_option("browser.gatherUsageStats", False)
            
            # Run the app
            sys.argv = ["streamlit", "run", app_path]
            st_cli.main()
        else:
            print("Streamlit runtime already exists. Skipping new instance creation.")
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
