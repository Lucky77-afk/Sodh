#!/usr/bin/env python3

"""
Entry point for running the Streamlit application.
"""
import os
import sys
import subprocess
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

def find_available_port(start_port=8501, max_attempts=10):
    """Find an available port starting from start_port."""
    import socket
    from contextlib import closing
    
    for port in range(start_port, start_port + max_attempts):
        try:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return start_port  # Fallback to start_port if no port is available

def main():
    """Main entry point for the application."""
    # Set environment variables
    env = os.environ.copy()
    env["STREAMLIT_SERVER_ENABLE_STATIC_SERVING"] = "true"
    env["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
    env["STREAMLIT_SERVER_HEADLESS"] = "true"
    env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    
    # Find an available port
    port = find_available_port(8501)
    if port != 8501:
        print(f"Port 8501 is in use, using port {port} instead")
    
    # Path to the app
    app_path = str(project_root / "sodh" / "app.py")
    
    # Configure environment variables for Streamlit
    os.environ["STREAMLIT_SERVER_PORT"] = str(port)
    os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    
    # Build the command to run Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "--server.port", str(port),
        "--server.address", "0.0.0.0",
        "--server.enableCORS", "true",
        "--server.enableXsrfProtection", "true",
        "--theme.base", "dark",
        "--theme.primaryColor", "#14F195",
        "--theme.backgroundColor", "#131313",
        "--theme.secondaryBackgroundColor", "#1E1E1E",
        "--theme.textColor", "#FFFFFF",
        "--theme.font", "sans serif",
        app_path
    ]
    
    try:
        # Run the Streamlit app
        subprocess.run(cmd, env=env)
    except Exception as e:
        print(f"Error running Streamlit: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
