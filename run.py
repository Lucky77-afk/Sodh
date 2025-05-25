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
    os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = "true"
    os.environ["STREAMLIT_SERVER_ENABLE_XSRF"] = "true"
    
    # Clean up any existing runtime instance
    try:
        # Send SIGTERM to any existing Streamlit process
        os.system("pkill -f 'streamlit run'")
    except Exception as e:
        print(f"Warning: Could not clean up existing Streamlit instances: {e}")
    
    # Set Streamlit configuration using environment variables
    _config.set_option("server.headless", os.getenv("STREAMLIT_SERVER_HEADLESS") == "true")
    _config.set_option("server.port", int(os.getenv("STREAMLIT_SERVER_PORT", "8501")))
    _config.set_option("server.address", os.getenv("STREAMLIT_SERVER_ADDRESS", "0.0.0.0"))
    _config.set_option("server.enableCORS", os.getenv("STREAMLIT_SERVER_ENABLE_CORS") == "true")
    _config.set_option("server.enableXsrfProtection", os.getenv("STREAMLIT_SERVER_ENABLE_XSRF") == "true")
    _config.set_option("browser.gatherUsageStats", os.getenv("STREAMLIT_BROWSER_GATHER_USAGE_STATS") == "true")
    
    # Prepare command line arguments
    streamlit_args = [
        f"--server.port={os.getenv('PORT', '8501')}",
        "--server.address=0.0.0.0",
        "--server.enableCORS=true",
        "--server.enableXsrfProtection=true",
        "--browser.gatherUsageStats=false"
    ]
    
    try:
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
    except Exception as e:
        print(f"Error running Streamlit app: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
