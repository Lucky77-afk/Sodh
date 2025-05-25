import os
import sys
import time
from pathlib import Path
import streamlit as st

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Health check endpoint for Streamlit Cloud
if os.environ.get('HEALTH_CHECK') == 'true':
    print("Health check passed")
    sys.exit(0)

try:
    # Set page config first
    st.set_page_config(
        page_title="Sodh - Solana Blockchain Explorer",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add a simple header
    st.title("Sodh - Solana Blockchain Explorer")
    
    # Import and run the main app
    from sodh.app import main
    main()
    
except Exception as e:
    # Log the full error
    import traceback
    error_msg = f"Error in Streamlit app: {str(e)}\n{traceback.format_exc()}"
    print(error_msg, file=sys.stderr)
    
    # Display a user-friendly error message
    st.error("An error occurred while loading the application.")
    if st.checkbox("Show error details"):
        st.code(error_msg)
    
    # Exit with error code
    sys.exit(1)
