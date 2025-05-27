"""
Sodh - Solana Blockchain Explorer (Root Entry Point)
"""
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the main app
from src.main.streamlit_app import main

if __name__ == "__main__":
    main()
