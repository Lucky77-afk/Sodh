"""
Entry point for running the Streamlit application.
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Import the app from the sodh package
from sodh import app

if __name__ == "__main__":
    # Run the Streamlit app
    import streamlit.web.bootstrap
    from streamlit.web import cli as st_cli
    
    # Set the config file path
    config_path = project_root / ".streamlit" / "config.toml"
    
    # Run the Streamlit app
    streamlit.web.bootstrap.run(
        str(project_root / "sodh" / "app.py"),
        "",
        [],
        flag_options={
            "server.headless": True,
            "global.developmentMode": False,
            "server.port": 8501,
            "server.address": "0.0.0.0",
            "browser.serverAddress": "localhost",
            "theme.base": "dark",
            "theme.primaryColor": "#14F195",
            "theme.backgroundColor": "#131313",
            "theme.secondaryBackgroundColor": "#1E1E1E",
            "theme.textColor": "#FFFFFF"
        }
    )
