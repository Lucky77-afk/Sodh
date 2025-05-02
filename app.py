import streamlit as st
import socket
import datetime
import os
import base64
from datetime import datetime
from components.header import render_header
from components.dashboard import render_dashboard
from components.transactions import render_transactions
from components.account import render_account
from components.smart_contract import render_smart_contract
from components.whitepaper import render_whitepaper
from components.tutorial import render_tutorial
from utils.database import init_db

# Initialize database with error handling
db_initialized = init_db()
if not db_initialized:
    print("Warning: Database initialization failed, using in-memory mode")

# Print connection information for debugging
hostname = socket.gethostname()
try:
    # Try to get the server's IP address
    ip_address = socket.gethostbyname(hostname)
    print(f"Server hostname: {hostname}")
    print(f"Server IP address: {ip_address}")
    print(f"Server running on http://0.0.0.0:5000")
except Exception as e:
    print(f"Error getting server info: {e}")
    print(f"Server hostname: {hostname}")
    print(f"Server running on http://0.0.0.0:5000")

# Check for logo to use as icon

logo_path = os.path.join("assets", "logo.jpeg")
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        logo_bytes = f.read()
    encoded_logo = base64.b64encode(logo_bytes).decode()
    page_icon = f"data:image/jpeg;base64,{encoded_logo}"
else:
    page_icon = "🔍"

# Set page configuration
st.set_page_config(
    page_title="Sodh - Solana Blockchain Explorer",
    page_icon=page_icon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.solana.com/docs',
        'Report a bug': None,
        'About': "Sodh Explorer - A Solana Blockchain Explorer built with Streamlit"
    }
)

# Add custom styling with improved UI
st.markdown("""
    <style>
    /* Base Styles */
    .main {
        background-color: #131313;
        color: #FFFFFF;
    }
    
    /* Enhanced Card Design with Glow Effect */
    .stCard {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1.2rem;
        border: 1px solid rgba(20, 241, 149, 0.1);
        box-shadow: 0 4px 12px rgba(20, 241, 149, 0.05);
        transition: all 0.3s ease;
    }
    
    .stCard:hover {
        box-shadow: 0 8px 20px rgba(20, 241, 149, 0.1);
        transform: translateY(-2px);
    }
    
    /* Typography */
    h1, h2, h3 {
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        letter-spacing: -0.01em;
    }
    
    h1 {
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
    }
    
    h2 {
        font-size: 1.8rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(153, 69, 255, 0.3);
        padding-bottom: 0.5rem;
    }
    
    h3 {
        font-size: 1.4rem;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
        color: #9945FF;
    }
    
    /* Sidebar Styling */
    div[data-testid="stSidebarNav"] {
        background-color: #1A1A1A;
        padding-top: 2rem;
        padding-left: 1.2rem;
        border-right: 1px solid rgba(20, 241, 149, 0.1);
    }
    
    /* Radio buttons in sidebar */
    div[data-testid="stRadio"] {
        background-color: #1E1E1E;
        border-radius: 8px;
        padding: 0.5rem;
    }
    
    div[data-testid="stRadio"] > div {
        gap: 0.5rem !important;
    }
    
    div[data-testid="stRadio"] label {
        background-color: #1A1A1A;
        border-radius: 6px;
        padding: 0.6rem 1rem;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.2s ease;
        border: 1px solid #252525;
    }
    
    div[data-testid="stRadio"] label:hover {
        background-color: #252525;
        border-color: #14F195;
    }
    
    /* Active element */
    div[data-testid="stRadio"] [data-baseweb="radio"] input:checked + div {
        background-color: rgba(20, 241, 149, 0.2);
        border-color: #14F195;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #9945FF, #14F195);
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        font-size: 0.85rem;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(153, 69, 255, 0.3);
    }
    
    button[kind="primaryFormSubmit"] {
        background-color: #14F195;
        color: #131313;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(30, 30, 30, 0.7);
        padding: 8px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        white-space: pre-wrap;
        background-color: #252525;
        border-radius: 6px;
        color: #EEEEEE;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.85rem;
        border: 1px solid #333;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #2A2A2A;
        border-color: #9945FF;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #14F195, #9945FF) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
    }
    
    /* Metric Values */
    .metric-value {
        color: #14F195;
        font-weight: 600;
        font-family: 'Roboto Mono', monospace;
        font-size: 1.8rem;
        text-shadow: 0 0 10px rgba(20, 241, 149, 0.3);
    }
    
    /* Transaction Elements */
    .transaction-row {
        padding: 14px;
        border-radius: 10px;
        margin-bottom: 10px;
        background-color: #1E1E1E;
        border-left: 3px solid #9945FF;
        transition: all 0.2s ease;
    }
    
    .transaction-row:hover {
        background-color: #252525;
        transform: translateX(3px);
    }
    
    .transaction-hash {
        font-family: 'Roboto Mono', monospace;
        color: #9945FF;
        font-size: 0.9rem;
        background-color: rgba(153, 69, 255, 0.1);
        padding: 4px 8px;
        border-radius: 4px;
    }
    
    .transaction-amount {
        font-family: 'Roboto Mono', monospace;
        color: #00FFA3;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    /* Wallet Address */
    .wallet-address {
        font-family: 'Roboto Mono', monospace;
        color: #FFFFFF;
        background-color: #1E1E1E;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 0.9rem;
        border: 1px solid #333;
        word-break: break-all;
    }
    
    /* Gradient Text */
    .gradient-text {
        background: linear-gradient(90deg, #14F195, #9945FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        letter-spacing: 0.05em;
    }
    
    /* Form Elements */
    div[data-baseweb="input"] {
        background-color: #1A1A1A;
        border: 1px solid #333;
        border-radius: 6px;
    }
    
    div[data-baseweb="input"]:focus-within {
        border-color: #14F195;
        box-shadow: 0 0 0 2px rgba(20, 241, 149, 0.2);
    }
    
    div[data-baseweb="input"] input {
        color: #FFFFFF;
    }
    
    /* Form Card */
    .form-card {
        background-color: #1E1E1E;
        border-radius: 12px;
        padding: 1.8rem;
        margin-bottom: 1.8rem;
        border-left: 4px solid #14F195;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
    }
    
    /* Smart Contract Elements */
    .contract-function {
        font-family: 'Roboto Mono', monospace;
        color: #14F195;
        background-color: rgba(20, 241, 149, 0.1);
        padding: 10px 16px;
        border-radius: 6px;
        margin-bottom: 8px;
        border-left: 3px solid #14F195;
        transition: all 0.2s ease;
    }
    
    .contract-function:hover {
        background-color: rgba(20, 241, 149, 0.15);
        transform: translateX(3px);
    }
    
    .contract-event {
        font-family: 'Roboto Mono', monospace;
        color: #9945FF;
        background-color: rgba(153, 69, 255, 0.1);
        padding: 10px 16px;
        border-radius: 6px;
        margin-bottom: 8px;
        border-left: 3px solid #9945FF;
        transition: all 0.2s ease;
    }
    
    .contract-event:hover {
        background-color: rgba(153, 69, 255, 0.15);
        transform: translateX(3px);
    }
    
    /* Milestone Card */
    .milestone-card {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 16px;
        border-left: 4px solid #9945FF;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .milestone-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(153, 69, 255, 0.2);
    }
    
    /* Data Tables */
    div[data-testid="stDataFrame"] {
        background-color: #1A1A1A;
        border-radius: 8px;
        padding: 8px;
        border: 1px solid #333;
    }
    
    div[data-testid="stDataFrame"] th {
        background-color: #252525;
        color: #14F195;
        font-weight: 600;
        padding: 12px 16px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
    }
    
    div[data-testid="stDataFrame"] td {
        padding: 10px 16px;
        border-bottom: 1px solid #333;
    }
    
    /* Error Messages */
    div[data-testid="stAlert"] {
        background-color: rgba(255, 92, 92, 0.1);
        color: #FF5C5C;
        border: 1px solid rgba(255, 92, 92, 0.3);
        border-radius: 8px;
        padding: 16px;
    }
    
    /* Success Messages */
    div.element-container div[data-testid="stAlert"][kind="success"] {
        background-color: rgba(20, 241, 149, 0.1);
        color: #14F195;
        border: 1px solid rgba(20, 241, 149, 0.3);
    }
    
    /* Mobile Responsive Adjustments */
    @media (max-width: 768px) {
        .stCard {
            padding: 1rem;
        }
        
        h1 {
            font-size: 1.8rem;
        }
        
        h2 {
            font-size: 1.5rem;
        }
        
        .transaction-row {
            padding: 10px;
        }
        
        .metric-value {
            font-size: 1.4rem;
        }
    }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Render the header with logo
render_header()

# Add access information notification
st.toast("📱 For mobile access, use the 'Open in new tab' button in Replit's preview window", icon="🔔")

# Sidebar navigation
with st.sidebar:
    # Add health check access
    if st.button("⚡ Check Server Status"):
        # Use experimental_set_query_params for setting the query parameter
        st.experimental_set_query_params(health_check="true")
        st.experimental_rerun()
    st.markdown('<p class="gradient-text">NAVIGATION</p>', unsafe_allow_html=True)
    page = st.radio(
        "Select a page",
        ["Dashboard", "Transactions", "Account", "Smart Contract", "Whitepaper", "Tutorial"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown('<p class="gradient-text">CONNECT WALLET</p>', unsafe_allow_html=True)
    wallet_address = st.text_input("Wallet Address", placeholder="Enter Solana wallet address")
    if st.button("Connect"):
        st.session_state.wallet_address = wallet_address
        st.experimental_rerun()
    
    # Clear wallet
    if 'wallet_address' in st.session_state and st.session_state.wallet_address:
        if st.button("Disconnect Wallet"):
            del st.session_state.wallet_address
            st.experimental_rerun()
    
    # About section in sidebar
    st.markdown("---")
    st.markdown('<p class="gradient-text">ABOUT DAPPR</p>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 0.85rem; color: #AAA;">
    Decentralized Autonomous Platform for Propagation of Research (DAPPR) leverages Solana blockchain to revolutionize academia-industry collaboration.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.8rem; color: #666;">
        Sodh Explorer v1.0<br>
        Powered by Solana
    </div>
    """, unsafe_allow_html=True)

# Add health check/status page
# Get query params in a way that works across Streamlit versions
query_params = st.experimental_get_query_params()
if 'health_check' in query_params:
    st.success("Server is up and running! 🚀")
    st.write(f"Server Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        st.write(f"Hostname: {socket.gethostname()}")
        st.write(f"IP Address: {socket.gethostbyname(socket.gethostname())}")
    except:
        st.write("Could not determine server details")
    
    st.write("### Database Status")
    try:
        from utils.database import get_projects
        projects = get_projects()
        st.write(f"✅ Database connected successfully")
        st.write(f"Projects count: {len(projects)}")
    except Exception as e:
        st.error(f"❌ Database error: {str(e)}")
    
    st.button("Refresh Status")
    
# Main content based on navigation selection
elif page == "Dashboard":
    render_dashboard()
elif page == "Transactions":
    render_transactions()
elif page == "Account":
    render_account()
elif page == "Smart Contract":
    render_smart_contract()
elif page == "Whitepaper":
    render_whitepaper()
elif page == "Tutorial":
    render_tutorial()
