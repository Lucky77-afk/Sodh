#!/usr/bin/env python3
"""
Main entry point for Sodh - Solana Blockchain Explorer
"""
import os
import sys
import logging
import subprocess
import threading
import time
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

class AppRunner:
    def __init__(self):
        self.process = None
        self.port = int(os.getenv("PORT", 8501))
        self.streamlit_port = self.port + 1  # Use next port for Streamlit
        
    def run_fastapi(self):
        """Run FastAPI server for health checks."""
        import uvicorn
        from fastapi import FastAPI
        from fastapi.responses import RedirectResponse
        
        app = FastAPI()
        
        @app.get("/health")
        async def health_check():
            return {"status": "healthy"}
            
        @app.get("/")
        async def root():
            return RedirectResponse(url=f"http://localhost:{self.streamlit_port}")
            
        uvicorn.run(app, host="0.0.0.0", port=self.port)
    
    def run_streamlit(self):
        """Run Streamlit app."""
        app_path = str(Path(__file__).parent / "sodh" / "app.py")
        if not os.path.exists(app_path):
            logger.error(f"App not found at: {app_path}")
            return
            
        cmd = [
            "streamlit", "run", app_path,
            "--server.port", str(self.streamlit_port),
            "--server.address", "0.0.0.0",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false",
            "--server.maxUploadSize", "200",
            "--server.fileWatcherType", "none",
            "--logger.level", "info"
        ]
        
        self.process = subprocess.Popen(cmd)
        self.process.wait()
    
    def health_check(self):
        """Handle health check and exit if needed."""
        if os.environ.get('HEALTH_CHECK') == 'true':
            print("Health check passed")
            sys.exit(0)
    
    def run(self):
        """Run both FastAPI and Streamlit."""
        self.health_check()
        
        # Start Streamlit in a separate thread
        streamlit_thread = threading.Thread(target=self.run_streamlit)
        streamlit_thread.daemon = True
        streamlit_thread.start()
        
        # Give Streamlit time to start
        time.sleep(2)
        
        # Run FastAPI in the main thread
        self.run_fastapi()

def main():
    """Main entry point."""
    try:
        runner = AppRunner()
        runner.run()
    except Exception as e:
        logger.critical(f"Application failed to start: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
