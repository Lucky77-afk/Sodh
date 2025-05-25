#!/usr/bin/env python3
"""
Main entry point for Sodh - Solana Blockchain Explorer
"""
import os
import sys
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

def ensure_import_path():
    """Ensure the project root is in the Python path."""
    project_root = Path(__file__).parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    return project_root

def run_streamlit():
    """Run the Streamlit application."""
    try:
        import streamlit.web.cli as st_cli
        
        # Set up paths
        project_root = ensure_import_path()
        app_path = project_root / "sodh" / "app.py"
        
        if not app_path.exists():
            logger.error(f"Application not found at: {app_path}")
            return 1
            
        logger.info(f"Starting Streamlit with app at: {app_path}")
        
        # Configure Streamlit arguments
        sys.argv = [
            "streamlit", "run", str(app_path),
            "--server.port", os.getenv("PORT", "8501"),
            "--server.address", "0.0.0.0",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false",
            "--server.maxUploadSize", "200",
            "--server.fileWatcherType", "none",
            "--logger.level", "info",
            "--server.headless", "true"
        ]
        
        # Run Streamlit
        return st_cli.main()
        
    except Exception as e:
        logger.error(f"Failed to start Streamlit: {str(e)}", exc_info=True)
        return 1

def main():
    """Main entry point."""
    # Handle health check
    if os.environ.get('HEALTH_CHECK') == 'true':
        print("Health check passed")
        return 0
        
    # Run the Streamlit app
    return run_streamlit()

if __name__ == "__main__":
    sys.exit(main())
