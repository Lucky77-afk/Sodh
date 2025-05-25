import os
import sys
import time
from pathlib import Path
import streamlit as st

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Health check endpoint
if os.environ.get('HEALTH_CHECK'):
    print("Health check passed")
    sys.exit(0)

try:
    # Import the main app
    from sodh.app import main

    # Set page config
    st.set_page_config(
        page_title="Sodh - Solana Blockchain Explorer",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add a simple header
    st.title("Sodh - Solana Blockchain Explorer")
    
    # Run the main app
    main()
    
except Exception as e:
    # Display error to the user
    st.error("An error occurred while loading the application.")
    st.exception(e)
    
    # Log the error
    import traceback
    print(f"Error in Streamlit app: {str(e)}")
    print(traceback.format_exc())
