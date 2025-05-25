#!/usr/bin/env python3
"""
Entry point for Sodh - Solana Blockchain Explorer

This script handles the Streamlit application startup with proper configuration
for both local development and cloud deployment.
"""
import os
import sys
import signal
import subprocess
import time
from pathlib import Path
from typing import Optional, List


def run_health_check(port: int = 8501, timeout: int = 10) -> bool:
    """Run a health check against the running Streamlit server.
    
    Args:
        port: The port where Streamlit is running
        timeout: Timeout in seconds
        
    Returns:
        bool: True if health check passes, False otherwise
    """
    import requests
    
    url = f"http://localhost:{port}/?health_check=true"
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200 and "Server is up and running" in response.text
    except requests.RequestException:
        return False


def start_streamlit(port: int = 8501) -> subprocess.Popen:
    """Start the Streamlit server as a subprocess.
    
    Args:
        port: Port to run Streamlit on
        
    Returns:
        subprocess.Popen: The running Streamlit process
    """
    # Set environment variables for Streamlit
    env = os.environ.copy()
    env.update({
        "STREAMLIT_SERVER_ENABLE_STATIC_SERVING": "false",
        "STREAMLIT_SERVER_ENABLE_CORS": "false",
        "STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION": "false",
        "STREAMLIT_SERVER_HEADLESS": "true",
        "PORT": str(port)
    })
    
    # Get the path to the app
    app_path = str(Path(__file__).parent / "app.py")
    
    # Build the command
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "--server.port", str(port),
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false",
        "--server.maxUploadSize", "200",
        "--server.fileWatcherType", "none",
        "--server.runOnSave", "false",
        "--browser.serverAddress", "0.0.0.0",
        "--browser.serverPort", str(port),
        "--theme.base", "dark",
        "--theme.primaryColor", "#14F195",
        "--theme.backgroundColor", "#131313",
        "--theme.secondaryBackgroundColor", "#1E1E1E",
        "--server.enableWebsocketCompression", "true",
        app_path
    ]
    
    print(f"Starting Streamlit on port {port}...")
    return subprocess.Popen(
        cmd,
        env=env,
        stdout=sys.stdout,
        stderr=sys.stderr,
        start_new_session=True
    )


def main():
    """Main entry point for the application."""
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run the Sodh Streamlit app')
    parser.add_argument('--port', type=int, default=8501,
                       help='Port to run the server on')
    parser.add_argument('--health-check', action='store_true',
                       help='Run health check and exit')
    args = parser.parse_args()
    
    if args.health_check:
        # Just run a health check and exit
        if run_health_check(port=args.port):
            print("Health check passed")
            sys.exit(0)
        else:
            print("Health check failed")
            sys.exit(1)
    
    # Start the Streamlit server
    process = start_streamlit(port=args.port)
    
    # Set up signal handlers for clean shutdown
    def signal_handler(sig, frame):
        print("Shutting down...")
        process.terminate()
        process.wait()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Wait for the process to complete
    try:
        process.wait()
    except KeyboardInterrupt:
        signal_handler(None, None)


if __name__ == "__main__":
    main()
