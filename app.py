import streamlit as st
from components.header import render_header
from components.dashboard import render_dashboard
from components.transactions import render_transactions
from components.account import render_account

# Set page configuration
st.set_page_config(
    page_title="Sodh - Solana Blockchain Explorer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom styling
st.markdown("""
    <style>
    .main {
        background-color: #131313;
        color: #FFFFFF;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 16px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1E1E1E;
        border-radius: 4px;
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #14F195 !important;
        color: #131313 !important;
    }

    div[data-testid="stSidebarNav"] {
        background-color: #1E1E1E;
        padding-top: 2rem;
        padding-left: 1rem;
    }
    
    button[kind="primaryFormSubmit"] {
        background-color: #14F195;
        color: #131313;
    }
    
    .stCard {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    h1, h2, h3 {
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }
    
    .metric-value {
        color: #14F195;
        font-weight: bold;
        font-family: 'Roboto Mono', monospace;
    }
    
    .transaction-row {
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 8px;
        background-color: #1E1E1E;
    }
    
    .transaction-hash {
        font-family: 'Roboto Mono', monospace;
        color: #9945FF;
        font-size: 0.9rem;
    }
    
    .transaction-amount {
        font-family: 'Roboto Mono', monospace;
        color: #00FFA3;
        font-weight: bold;
    }
    
    .wallet-address {
        font-family: 'Roboto Mono', monospace;
        color: #FFFFFF;
        background-color: #1E1E1E;
        padding: 8px;
        border-radius: 4px;
        font-size: 0.9rem;
    }
    
    .gradient-text {
        background: linear-gradient(90deg, #14F195, #9945FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    
    .stButton>button {
        background-color: #9945FF;
        color: white;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-family: 'Inter', sans-serif;
    }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&family=Roboto+Mono&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Render the header with logo
render_header()

# Sidebar navigation
with st.sidebar:
    st.markdown('<p class="gradient-text">NAVIGATION</p>', unsafe_allow_html=True)
    page = st.radio(
        "Select a page",
        ["Dashboard", "Transactions", "Account"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown('<p class="gradient-text">CONNECT WALLET</p>', unsafe_allow_html=True)
    wallet_address = st.text_input("Wallet Address", placeholder="Enter Solana wallet address")
    if st.button("Connect"):
        st.session_state.wallet_address = wallet_address
        st.rerun()
    
    # Clear wallet
    if 'wallet_address' in st.session_state and st.session_state.wallet_address:
        if st.button("Disconnect Wallet"):
            del st.session_state.wallet_address
            st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.8rem; color: #666;">
        Sodh Explorer v1.0<br>
        Powered by Solana
    </div>
    """, unsafe_allow_html=True)

# Main content based on navigation selection
if page == "Dashboard":
    render_dashboard()
elif page == "Transactions":
    render_transactions()
elif page == "Account":
    render_account()
