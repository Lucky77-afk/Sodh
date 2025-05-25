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
    
    # Clean up any existing runtime instance
    try:
        # Send SIGTERM to any existing Streamlit process
        os.system("pkill -f 'streamlit run'")
    except Exception as e:
        print(f"Warning: Could not clean up existing Streamlit instances: {e}")
    
    # Set Streamlit configuration
    _config.set_option("server.headless", True)
    _config.set_option("server.port", 8501)
    _config.set_option("server.address", "0.0.0.0")
    _config.set_option("server.enableCORS", True)
    _config.set_option("server.enableXsrfProtection", True)
    _config.set_option("browser.gatherUsageStats", False)
    
    # Prepare command line arguments
    streamlit_args = [
        "--server.port=8501",
        "--server.address=0.0.0.0",
        "--server.enableCORS=true",
        "--server.enableXsrfProtection=true",
        "--browser.gatherUsageStats=false"
    ]
    
    # Run the app using the bootstrap module
    sys.exit(
        streamlit.web.bootstrap.run(
            app_path,
            command_line=streamlit_args,
            args=[],
            flag_options={},
            _is_hello=False
        )
    )

if __name__ == "__main__":
    main()
