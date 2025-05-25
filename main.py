#!/usr/bin/env python3
"""
Main entry point for Sodh - Solana Blockchain Explorer
"""
import os
import sys
import http.server
import socketserver
import threading
from pathlib import Path

# Configuration
PORT = int(os.getenv("PORT", 8501))
HEALTH_CHECK_PORT = int(os.getenv("HEALTH_CHECK_PORT", 8080))

class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()

def run_health_check():
    """Run a simple HTTP server for health checks"""
    with socketserver.TCPServer(("0.0.0.0", HEALTH_CHECK_PORT), HealthCheckHandler) as httpd:
        print(f"Health check server running on port {HEALTH_CHECK_PORT}")
        httpd.serve_forever()

def main():
    # Start health check server in a separate thread
    health_thread = threading.Thread(target=run_health_check, daemon=True)
    health_thread.start()
    
    # Run Streamlit
    app_path = str(Path(__file__).parent / "sodh" / "app.py")
    
    # Use os.execvp to replace the current process with Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "--server.port", str(PORT),
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false",
        "--server.maxUploadSize", "200",
        "--server.fileWatcherType", "none",
        "--server.runOnSave", "false",
        "--browser.serverAddress", "0.0.0.0",
        "--browser.serverPort", str(PORT),
        "--theme.base", "dark",
        "--theme.primaryColor", "#14F195",
        "--theme.backgroundColor", "#131313",
        "--theme.secondaryBackgroundColor", "#1E1E1E",
        app_path
    ]
    
    print(f"Starting Streamlit on port {PORT}")
    os.execvp(cmd[0], cmd)

if __name__ == "__main__":
    main()
