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

def configure_environment():
    """Set up environment variables and paths."""
    # Set up paths
    project_root = Path(__file__).parent
    
    # Add project root to Python path
    if str(project_root) not in sys.path:
        sys.path.append(str(project_root))
    
    # Set Streamlit configuration via environment variables
    os.environ.setdefault("STREAMLIT_SERVER_HEADLESS", "true")
    os.environ.setdefault("STREAMLIT_SERVER_PORT", os.getenv("PORT", "8501"))
    os.environ.setdefault("STREAMLIT_SERVER_ADDRESS", "0.0.0.0")
    os.environ.setdefault("STREAMLIT_SERVER_ENABLE_CORS", "true")
    os.environ.setdefault("STREAMLIT_SERVER_ENABLE_XSRF", "true")
    os.environ.setdefault("STREAMLIT_SERVER_MAX_UPLOAD_SIZE", "200")
    os.environ.setdefault("STREAMLIT_BROWSER_GATHER_USAGE_STATS", "false")

def run_streamlit():
    """Run the Streamlit application."""
    try:
        project_root = Path(__file__).parent
        app_path = str(project_root / "sodh" / "app.py")
        
        # Import streamlit components
        import streamlit.web.cli as st_cli
        from streamlit.runtime.runtime import Runtime
        
        # Check if a runtime instance already exists
        if not hasattr(Runtime, '_instance') or not Runtime._instance:
            logger.info("Starting Streamlit application...")
            
            # Configure and run Streamlit
            sys.argv = [
                "streamlit", "run", app_path,
                "--server.port", os.getenv("PORT", "8501"),
                "--server.address", "0.0.0.0",
                "--server.enableCORS", "true",
                "--server.enableXsrfProtection", "true",
                "--server.maxUploadSize", "200"
            ]
            
            # Ensure we have a clean environment
            if '_streamlit_' in sys.modules:
                import importlib
                importlib.reload(sys.modules['_streamlit_'])
                
            st_cli.main()
        else:
            logger.warning("Streamlit runtime already exists. Skipping new instance creation.")
            
    except Exception as e:
        logger.error(f"Failed to start Streamlit application: {str(e)}", exc_info=True)
        sys.exit(1)

def health_check():
    """Simple health check endpoint."""
    if os.environ.get('HEALTH_CHECK'):
        print("Health check passed")
        sys.exit(0)

def main():
    """Main entry point."""
    try:
        # Configure environment
        configure_environment()
        
        # Handle health check
        health_check()
        
        # Run the Streamlit app
        run_streamlit()
        
    except Exception as e:
        logger.critical(f"Application failed to start: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
