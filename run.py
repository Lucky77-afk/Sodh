"""
Entry point for running the Streamlit application.
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import the app from the sodh package
from .sodh.app import main

if __name__ == "__main__":
    # Run the Streamlit app
    import streamlit.web.bootstrap
    
    # Set the config file path
    config_path = project_root / ".streamlit" / "config.toml"
    
    # Set environment variables for Streamlit
    os.environ["STREAMLIT_SERVER_PORT"] = "8501"
    os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    
    # Run the Streamlit app
    streamlit.web.bootstrap.run(
        str(project_root / "sodh" / "app.py"),
        args=[],
        flag_options={
            "server.headless": True,
            "global.developmentMode": False,
            "server.port": 8501,
            "server.address": "0.0.0.0",
            "browser.serverAddress": "0.0.0.0",
            "theme.base": "dark",
            "theme.primaryColor": "#14F195",
            "theme.backgroundColor": "#131313",
            "theme.secondaryBackgroundColor": "#1E1E1E",
            "theme.textColor": "#FFFFFF"
        }
    )
