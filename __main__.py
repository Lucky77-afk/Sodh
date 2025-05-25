"""
Sodh - Solana Blockchain Explorer
"""
import streamlit.cli as stcli
import sys

def main():
    """Run the Streamlit app."""
    sys.argv = ["streamlit", "run", "main/app.py"] + sys.argv[1:]
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()
