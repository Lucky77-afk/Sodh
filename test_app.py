"""
Test script for the Sodh Streamlit application.
Run this script to verify that the app starts correctly.
"""
import subprocess
import sys
import time

def test_app():
    """Test that the Streamlit app starts without errors."""
    try:
        # Start the Streamlit app in a subprocess
        process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless", "true"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment for the app to start
        time.sleep(5)
        
        # Check if the process is still running
        if process.poll() is None:
            print("✅ Streamlit app started successfully")
            process.terminate()
            return True
        else:
            # Get error output if the process failed
            _, stderr = process.communicate()
            print(f"❌ Error starting Streamlit app: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Streamlit app: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Streamlit app...")
    success = test_app()
    sys.exit(0 if success else 1)
