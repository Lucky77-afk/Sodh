#!/usr/bin/env python3
"""
Entry point for Sodh - Solana Blockchain Explorer

This script serves as the main entry point for the Streamlit application.
"""
import os
import sys
import signal
import subprocess
from pathlib import Path

def start_streamlit():
    """Start the Streamlit server."""
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 8501))
    
    # Set environment variables for Streamlit
    env = os.environ.copy()
    env.update({
        "STREAMLIT_SERVER_PORT": str(port),
        "STREAMLIT_SERVER_HEADLESS": "true",
        "STREAMLIT_SERVER_ENABLE_CORS": "false",
        "STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION": "false",
        "STREAMLIT_SERVER_FILE_WATCHER_TYPE": "none",
        "STREAMLIT_SERVER_ADDRESS": "0.0.0.0",
        "STREAMLIT_BROWSER_GATHER_USAGE_STATS": "false"
    })
    
    # Get the path to the app
    app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "src", "main", "streamlit_app.py"))
    
    # Start Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "--server.port", str(port),
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.fileWatcherType", "none",
        app_path
    ]
    
    print(f"🚀 Starting Streamlit on port {port}...")
    print(f"📂 App path: {app_path}")
    print(f"🔧 Environment: {env}")
    print(f"🚀 Command: {' '.join(cmd)}")
    
    return subprocess.Popen(
        cmd,
        env=env,
        stdout=sys.stdout,
        stderr=sys.stderr,
        start_new_session=True
    )

def main():
    """Main function to start the Streamlit server."""
    process = None
    try:
        process = start_streamlit()
        process.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        if process and process.poll() is None:  # If process is still running
            process.terminate()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
