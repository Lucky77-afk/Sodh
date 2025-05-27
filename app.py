"""
Sodh - Solana Blockchain Explorer
"""
import os
import streamlit as st
import base58
from solana.rpc.api import Client

def main():
    # Set page configuration (must be the first Streamlit command)
    st.set_page_config(
        page_title="Sodh - Solana Blockchain Explorer",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize Solana client with RPC endpoint from secrets or use default
    @st.cache_resource
    def get_solana_client():
        try:
            rpc_endpoint = st.secrets.get(
                "SOLANA_RPC_ENDPOINT", 
                "https://api.mainnet-beta.solana.com"
            )
            return Client(rpc_endpoint)
        except Exception as e:
            st.error(f"Failed to initialize Solana client: {str(e)}")
            return None

    # Add custom CSS
    st.markdown("""
        <style>
        .main {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        .stButton>button {
            background-color: #14F195;
            color: #000000;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
        }
        .stButton>button:hover {
            background-color: #12D98A;
        }
        .stTextInput>div>div>input {
            background-color: #1E1E1E;
            color: #FAFAFA;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #14F195;
        }
        </style>
    """, unsafe_allow_html=True)

    # Main app content
    st.title("🔍 Sodh - Solana Blockchain Explorer")
    st.markdown("Explore the Solana blockchain with ease. Search for accounts, transactions, and more.")

    # Initialize Solana client
    solana_client = get_solana_client()
    if solana_client is None:
        st.error("Failed to connect to Solana network. Please check your connection and try again.")
        return

    # Search bar
    with st.form("search_form"):
        search_query = st.text_input(
            "Search by Solana address or transaction hash:",
            placeholder="Enter a Solana address or transaction hash",
            key="search_input"
        )
        search_button = st.form_submit_button("Search")

    if search_button and search_query:
        st.session_state.search_query = search_query
        
        # Check if it's a valid Solana address
        try:
            # This will raise an exception if the address is invalid
            decoded = base58.b58decode(search_query)
            if len(decoded) == 32:  # Standard Solana address length
                with st.spinner("Fetching account information..."):
                    try:
                        account_info = solana_client.get_account_info(search_query)
                        if account_info:
                            st.subheader("Account Information")
                            st.json(account_info)
                    except Exception as e:
                        st.error(f"Error fetching account info: {str(e)}")
            else:
                st.error("Invalid Solana address length")
        except Exception as e:
            st.error(f"Invalid Solana address: {str(e)}")

    # Add footer
    st.markdown("---")
    st.markdown("### About Sodh")
    st.markdown("Sodh is an open-source Solana blockchain explorer built with Streamlit.")
    st.markdown("© 2025 Sodh Explorer | [GitHub](https://github.com/Lucky77-afk/Sodh)")

if __name__ == "__main__":
    main()
