#!/usr/bin/env python3
"""
Entry point for Sodh - Solana Blockchain Explorer

This script serves as the main entry point for the Streamlit application.
"""
import os
import sys
import subprocess

def main():
    """Main function to start the Streamlit server."""
    # Get port from environment variable or use default
    port = os.environ.get("PORT", "8501")
    
    # Get the absolute path to the app.py file
    app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "app.py"))
    
    # Print debug information
    print(f"🚀 Starting Streamlit on port {port}...")
    print(f"📂 App path: {app_path}")
    print(f"📦 Current working directory: {os.getcwd()}")
    print(f"📝 Directory contents: {os.listdir('.')}")
    
    # Start Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "--server.port", port,
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.fileWatcherType", "none",
        app_path
    ]
    
    print(f"🚀 Command: {' '.join(cmd)}")
    
    # Start the process
    process = subprocess.Popen(
        cmd,
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    
    # Wait for the process to complete
    try:
        process.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        process.terminate()
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
