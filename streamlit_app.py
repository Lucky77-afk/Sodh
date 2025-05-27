"""
Streamlit entry point for Sodh - Solana Blockchain Explorer
"""
import os
import sys
import streamlit as st

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Try to import from the root directory first
    from app import main
except ImportError:
    try:
        # Fall back to main package if root import fails
        from main.app import main
    except ImportError as e:
        st.error(f"Failed to import app: {e}")
        raise

# Run the app
if __name__ == "__main__":
    main()
