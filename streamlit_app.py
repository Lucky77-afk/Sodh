"""
Streamlit entry point for Sodh - Solana Blockchain Explorer

This file serves as the main entry point for Streamlit Cloud deployment.
It simply imports and runs the main app from app.py
"""
import os
import sys
import streamlit as st

# Add the current directory to the path so we can import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the main function from app
from app import main

# Run the app
if __name__ == "__main__":
    # Set environment variables for Streamlit Cloud
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = "false"
    os.environ["STREAMLIT_SERVER_PORT"] = os.environ.get("PORT", "8501")
    
    # Run the main function
    main()
