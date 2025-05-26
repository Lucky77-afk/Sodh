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
        "STREAMLIT_SERVER_PORT": str(port),
        "STREAMLIT_SERVER_HEADLESS": "true",
        "STREAMLIT_SERVER_ENABLE_CORS": "false",
        "STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION": "false",
        "STREAMLIT_SERVER_FILE_WATCHER_TYPE": "none",
        "STREAMLIT_BROWSER_GATHER_USAGE_STATS": "false",
        "STREAMLIT_SERVER_ADDRESS": "0.0.0.0",
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
    
    print(f"🚀 Starting Streamlit on port {port}...")
    return subprocess.Popen(
        cmd,
        env=env,
        stdout=sys.stdout,
        stderr=sys.stderr,
        start_new_session=True
    )

def main():
    """Main entry point for the application."""
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 8501))
    
    # Check if this is a health check
    if os.environ.get("HEALTH_CHECK") == "true":
        print("🩺 Health check endpoint")
        print("HTTP/1.1 200 OK\nContent-Type: text/plain\n\nServer is up and running")
        sys.exit(0)
    
    print(f"🚀 Starting Sodh - Solana Blockchain Explorer on port {port}")
    
    # Start Streamlit server
    process = start_streamlit(port)
    
    # Set up signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        print("\n🛑 Shutting down...")
        process.terminate()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Wait for the process to complete
    try:
        while True:
            time.sleep(1)
            if process.poll() is not None:
                print(f"\n❌ Streamlit process exited with code {process.returncode}")
                sys.exit(process.returncode)
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()
