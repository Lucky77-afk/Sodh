#!/usr/bin/env python3
"""
Main entry point for Sodh - Solana Blockchain Explorer
"""
import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

def ensure_package_importable():
    """Ensure the sodh package is importable."""
    project_root = Path(__file__).parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    try:
        import sodh
        logger.info(f"Successfully imported sodh from: {sodh.__file__}")
        return True
    except ImportError as e:
        logger.error(f"Failed to import sodh package: {e}")
        return False

def configure_environment():
    """Set up environment variables and paths."""
    # Set Streamlit configuration via environment variables
    os.environ.update({
        "STREAMLIT_SERVER_HEADLESS": "true",
        "STREAMLIT_SERVER_PORT": os.getenv("PORT", "8501"),
        "STREAMLIT_SERVER_ADDRESS": "0.0.0.0",
        "STREAMLIT_SERVER_ENABLE_CORS": "false",
        "STREAMLIT_SERVER_ENABLE_XSRF": "false",
        "STREAMLIT_SERVER_MAX_UPLOAD_SIZE": "200",
        "STREAMLIT_BROWSER_GATHER_USAGE_STATS": "false",
        "STREAMLIT_SERVER_FILE_WATCHER_TYPE": "none"
    })

def run_streamlit():
    """Run the Streamlit application."""
    try:
        # Import streamlit components
        import streamlit.web.cli as st_cli
        
        # Get the app path
        app_path = str(Path(__file__).parent / "sodh" / "app.py")
        
        if not os.path.exists(app_path):
            logger.error(f"App not found at: {app_path}")
            sys.exit(1)
            
        logger.info(f"Starting Streamlit with app at: {app_path}")
        
        # Configure and run Streamlit
        sys.argv = [
            "streamlit", "run", app_path,
            "--server.port", os.getenv("PORT", "8501"),
            "--server.address", "0.0.0.0",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false",
            "--server.maxUploadSize", "200",
            "--server.fileWatcherType", "none",
            "--logger.level", "info"
        ]
        
        # Run Streamlit
        st_cli.main()
        
    except Exception as e:
        logger.error(f"Failed to start Streamlit application: {str(e)}", exc_info=True)
        sys.exit(1)

def health_check():
    """Simple health check endpoint."""
    if os.environ.get('HEALTH_CHECK') == 'true':
        print("Health check passed")
        sys.exit(0)

def main():
    """Main entry point."""
    try:
        # Handle health check
        health_check()
        
        # Ensure package is importable
        if not ensure_package_importable():
            logger.error("Failed to import sodh package. Check your installation.")
            sys.exit(1)
        
        # Configure environment
        configure_environment()
        
        # Run the Streamlit app
        run_streamlit()
        
    except Exception as e:
        logger.critical(f"Application failed to start: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
