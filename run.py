#!/usr/bin/env python3

"""
Entry point for running the Streamlit application on Streamlit Cloud.
"""
#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def main():
    # Add the project root to the Python path
    project_root = Path(__file__).parent
    sys.path.append(str(project_root))
    
    # Set up paths
    app_path = str(project_root / "sodh" / "app.py")
    
    # Set environment variables
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    os.environ["STREAMLIT_SERVER_PORT"] = os.getenv("PORT", "8501")
    os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
    os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = "true"
    os.environ["STREAMLIT_SERVER_ENABLE_XSRF"] = "true"
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    
    # Import streamlit here after setting environment variables
    from streamlit.web import cli as st_cli
    
    # Prepare command line arguments
    streamlit_args = [
        "run",
        app_path,
        "--server.port", os.getenv("PORT", "8501"),
        "--server.address", "0.0.0.0",
        "--server.enableCORS", "true",
        "--server.enableXsrfProtection", "true",
        "--browser.gatherUsageStats", "false"
    ]
    
    try:
        # Run the app using the CLI
        sys.exit(st_cli.main(streamlit_args))
    except Exception as e:
        print(f"Error running Streamlit app: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
