import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Import the main app
from sodh.app import main

if __name__ == "__main__":
    # Set Streamlit config
    import streamlit as st
    
    # Set page config
    st.set_page_config(
        page_title="Sodh - Solana Blockchain Explorer",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Run the main app
    main()
