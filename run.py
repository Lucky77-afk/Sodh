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
    
    # Set environment variables
    os.environ["STREAMLIT_SERVER_PORT"] = os.getenv("PORT", "8501")
    os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    
    # Import streamlit here to ensure environment is set first
    import streamlit.web.bootstrap
    import streamlit.config as config
    
    # Configure streamlit
    config.set_option("server.port", int(os.getenv("PORT", "8501")))
    config.set_option("server.address", "0.0.0.0")
    config.set_option("server.enableCORS", True)
    config.set_option("server.enableXsrfProtection", True)
    config.set_option("server.fileWatcherType", "none")
    config.set_option("browser.gatherUsageStats", False)
    
    # Set theme configuration
    config.set_option("theme.base", "dark")
    config.set_option("theme.primaryColor", "#14F195")
    config.set_option("theme.backgroundColor", "#131313")
    config.set_option("theme.secondaryBackgroundColor", "#1E1E1E")
    config.set_option("theme.textColor", "#FFFFFF")
    config.set_option("theme.font", "sans serif")
    
    # Run the Streamlit app
    sys.exit(
        streamlit.web.bootstrap.run(
            app_path,
            "",
            [],
            flag_options={
                "server.port": int(os.getenv("PORT", "8501")),
                "server.address": "0.0.0.0",
                "server.enableCORS": True,
                "server.enableXsrfProtection": True,
                "server.fileWatcherType": "none",
                "browser.gatherUsageStats": False,
            },
        )
    )

if __name__ == "__main__":
    main()
