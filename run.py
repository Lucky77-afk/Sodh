#!/usr/bin/env python3
"""
Entry point for Sodh - Solana Blockchain Explorer
"""
import os
import sys
import subprocess
import http.server
import socketserver
import threading
from pathlib import Path

# Health check server configuration
HEALTH_CHECK_PORT = 8080

def run_health_check_server():
    class HealthCheckHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/healthz':
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'OK')
            else:
                self.send_response(404)
                self.end_headers()

    with socketserver.TCPServer(("0.0.0.0", HEALTH_CHECK_PORT), HealthCheckHandler) as httpd:
        print(f"Health check server running on port {HEALTH_CHECK_PORT}")
        httpd.serve_forever()

def main():
    # Start health check server in a separate thread
    health_thread = threading.Thread(target=run_health_check_server, daemon=True)
    health_thread.start()

    # Get the path to the app
    app_path = str(Path(__file__).parent / "sodh" / "app.py")
    
    # Set environment variables for Streamlit
    env = os.environ.copy()
    port = os.getenv("PORT", "8501")
    
    # Run Streamlit in a subprocess
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "--server.port", port,
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false",
        "--server.maxUploadSize", "200",
        "--server.fileWatcherType", "none",
        "--server.runOnSave", "false",
        "--browser.serverAddress", "0.0.0.0",
        "--browser.serverPort", port,
        "--theme.base", "dark",
        "--theme.primaryColor", "#14F195",
        "--theme.backgroundColor", "#131313",
        "--theme.secondaryBackgroundColor", "#1E1E1E",
        app_path
    ]
    
    print(f"Starting Streamlit server on port {port}")
    try:
        return subprocess.call(cmd, env=env)
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        print(f"Error starting Streamlit: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
