"""
DAPPR - Decentralized Academic-Industry Partnership Platform
"""
import streamlit as st
import base58
import json
import asyncio
import time
from pathlib import Path
from solana.rpc.async_api import AsyncClient
from solana.keypair import Keypair
from solana.publickey import PublicKey
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.let_it_rain import rain

# Import our DAPPR client
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from contracts.client import DapprClient

# Constants
PRIMARY_COLOR = "#14F195"
SECONDARY_COLOR = "#9945FF"
BACKGROUND_COLOR = "#0E1117"
TEXT_COLOR = "#FAFAFA"

# Set page config first
st.set_page_config(
    page_title="DAPPR - Decentralized Research Platform",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load custom CSS
local_css("assets/styles.css")

# Initialize session state
if 'wallet' not in st.session_state:
    st.session_state.wallet = None
    st.session_state.client = None
    st.session_state.connected = False
    st.session_state.projects = []  # Store user's projects
    st.session_state.show_success = False
    st.session_state.show_error = False
    st.session_state.error_message = ""
    st.session_state.success_message = ""

# Utility functions
def show_success(message):
    st.session_state.success_message = message
    st.session_state.show_success = True
    st.session_state.show_error = False
    st.experimental_rerun()

def show_error(message):
    st.session_state.error_message = message
    st.session_state.show_error = True
    st.session_state.show_success = False
    st.experimental_rerun()

def clear_messages():
    st.session_state.show_success = False
    st.session_state.show_error = False
    st.session_state.success_message = ""
    st.session_state.error_message = ""

def connect_wallet():
    try:
        with st.spinner("Connecting wallet..."):
            # Simulate wallet connection
            time.sleep(1)
            st.session_state.wallet = Keypair()
            st.session_state.client = DapprClient(
                rpc_url="https://api.devnet.solana.com",
                program_id="DAPPR1111111111111111111111111111111111111",
                wallet=st.session_state.wallet
            )
            st.session_state.connected = True
            show_success("Wallet connected successfully!")
    except Exception as e:
        show_error(f"Failed to connect wallet: {str(e)}")

def disconnect_wallet():
    st.session_state.wallet = None
    st.session_state.client = None
    st.session_state.connected = False
    st.session_state.projects = []
    clear_messages()
    st.experimental_rerun()

# Display success/error messages
if st.session_state.show_success:
    st.success(st.session_state.success_message)
    time.sleep(3)
    clear_messages()
    st.experimental_rerun()

if st.session_state.show_error:
    st.error(st.session_state.error_message)
    time.sleep(3)
    clear_messages()
    st.experimental_rerun()

# Sidebar
with st.sidebar:
    # Logo and title
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("assets/images/logo.png", width=60)
    with col2:
        st.markdown("<h2 style='margin-top: 10px;'>DAPPR</h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Wallet connection
    if not st.session_state.connected:
        if st.button("🔗 Connect Wallet", use_container_width=True, type="primary"):
            connect_wallet()
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        
        # Network info
        with st.expander("🌐 Network Info", expanded=True):
            st.caption("Current Network")
            st.info("Solana Devnet")
            st.caption("RPC Endpoint")
            st.code("https://api.devnet.solana.com", language="bash")
    else:
        # Connected wallet info
        st.success("✅ Wallet Connected")
        
        # Wallet address with copy button
        wallet_col1, wallet_col2 = st.columns([3, 1])
        with wallet_col1:
            st.code(st.session_state.wallet.public_key, language="bash")
        with wallet_col2:
            if st.button("📋", key="copy_wallet"):
                st.session_state.client.clipboard.copy(str(st.session_state.wallet.public_key))
                st.toast("Address copied to clipboard!")
        
        # Network info
        st.markdown("---")
        st.caption("Network")
        st.info("Solana Devnet")
        
        # Disconnect button
        if st.button("🚪 Disconnect Wallet", use_container_width=True, type="secondary"):
            disconnect_wallet()
    
    # Navigation
    st.markdown("---")
    st.markdown("### Navigation")
    nav_option = st.radio(
        "",
        ["🏠 Dashboard", "📝 Create Project", "💰 Fund Research", "📊 My Projects", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6B7280; font-size: 0.8rem;">
        <p>DAPPR v1.0.0</p>
        <p> 2025 All rights reserved</p>
    </div>
    """, unsafe_allow_html=True)

# Main content area
st.markdown("""
    <style>
        .main .block-container {
            padding-top: 2rem;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Navigation based on sidebar selection
if nav_option == "🏠 Dashboard":
    st.title("🔍 Research Dashboard")
    
    if st.session_state.connected:
        # Stats cards
        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container(border=True, height=150):
                st.markdown("### Total Projects")
                st.markdown("<h1 style='color: #14F195; margin-top: 10px;'>12</h1>", unsafe_allow_html=True)
                st.caption("+2 this month")
        
        with col2:
            with st.container(border=True, height=150):
                st.markdown("### Total Funding")
                st.markdown("<h1 style='color: #14F195; margin-top: 10px;'>1,245 SOL</h1>", unsafe_allow_html=True)
                st.caption("+120 SOL this month")
        
        with col3:
            with st.container(border=True, height=150):
                st.markdown("### Active Researchers")
                st.markdown("<h1 style='color: #14F195; margin-top: 10px;'>87</h1>", unsafe_allow_html=True)
                st.caption("+12 this month")
        
        # Recent activity
        st.markdown("### 📈 Recent Activity")
        with st.container(border=True):
            st.markdown("""
            - **Project 'AI for Climate' received 5 SOL from 0x1a...3f**
            - **New project 'Blockchain in Healthcare' created**
            - **Milestone 1 completed for 'Renewable Energy Research'**
            - **3 new researchers joined the platform**
            - **Project 'Quantum Computing' reached 75% of its funding goal**
            """)
        
        # Featured projects
        st.markdown("### 🌟 Featured Projects")
        featured_cols = st.columns(3)
        for i in range(3):
            with featured_cols[i]:
                with st.container(border=True, height=250):
                    st.markdown("#### Project Title")
                    st.caption("Brief description of the project and its goals...")
                    st.progress(0.65)
                    st.caption("65% funded • 15 days left")
                    st.button("View Details", key=f"featured_{i}", use_container_width=True)
    else:
        st.info("🔑 Connect your wallet to view your dashboard")

elif nav_option == "📝 Create Project":
    st.title("🚀 Create New Research Project")
    
    if st.session_state.connected:
        with st.form("create_project_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("Project Title*", placeholder="Enter project title", help="A clear and concise title for your research project")
                funding_goal = st.number_input("Funding Goal (SOL)*", min_value=1.0, step=1.0, format="%.2f", help="Minimum funding required to start the project")
                
                # Categories
                categories = ["AI/ML", "Blockchain", "Climate Change", "Healthcare", "Renewable Energy"]
                category = st.selectbox("Category*", options=categories)
                
                # Tags
                tags = st.text_input("Tags*", placeholder="Enter relevant tags (comma-separated)", help="Tags to help researchers find your project")
                
            with col2:
                description = st.text_area("Project Description*", placeholder="Enter project description", help="A detailed description of your research project")
                license_type = st.selectbox("License Type*", options=["MIT", "Apache 2.0", "GPL-3.0", "Proprietary"])
                commercial_rights = st.checkbox("Allow commercial use")
                
            if st.form_submit_button("Create Project"):
                if not all([title, description, funding_goal]):
                    st.error("Please fill in all required fields")
                else:
                    with st.spinner("Creating project..."):
                        try:
                            # Convert SOL to lamports (1 SOL = 1,000,000,000 lamports)
                            lamports = int(funding_goal * 10**9)
                            
                            # Create IP terms
                            ip_terms = {
                                "ownership_split": [
                                    [str(st.session_state.wallet.public_key), 100]
                                ],
                                "license_type": license_type,
                                "commercial_rights": commercial_rights
                            }
                            
                            # In a real app, this would be an async call
                            # tx_sig = asyncio.run(
                            #     st.session_state.client.create_project(
                            #         title=title,
                            #         description=description,
                            #         funding_goal=lamports,
                            #         ip_terms=ip_terms
                            #     )
                            # )
                            
                            # For demo, just show success
                            st.success(f"Project '{title}' created successfully!")
                            st.balloons()
                            
                        except Exception as e:
                            st.error(f"Failed to create project: {str(e)}")

elif nav_option == "💰 Fund Research":
    st.title("💸 Fund a Research Project")
    st.info("Browse and fund promising research projects")
    
    # In a real app, this would fetch projects from the blockchain
    st.warning("Project listing functionality coming soon!")

elif nav_option == "📊 My Projects":
    st.title("📈 My Research Projects")
    
    if st.session_state.connected:
        # In a real app, this would fetch user's projects from the blockchain
        st.info("No projects found. Create your first project to get started!")
    else:
        st.warning("Please connect your wallet to view your projects")

elif nav_option == "⚙️ Settings":
    st.title("⚙️ Settings")
    st.info("Coming soon!")

# Footer
st.markdown("---")
st.markdown("### About DAPPR")
st.markdown("""
DAPPR is a decentralized platform that bridges the gap between academic research and industry collaboration 
using Solana blockchain technology. Our mission is to accelerate innovation by creating a transparent, 
fair, and efficient ecosystem for research funding and collaboration.

[GitHub](https://github.com/Lucky77-afk/Sodh) | [Whitepaper](/assets/Whitepaper)
""")

# Ensure wallet is connected for protected routes
if nav_option not in ["🏠 Dashboard"] and not st.session_state.connected:
    st.warning("🔑 Please connect your wallet to continue")
    st.stop()

# Footer
st.markdown("---")
st.markdown("### About DAPPR")
st.markdown("""
DAPPR is a decentralized platform that bridges the gap between academic research and industry collaboration 
using Solana blockchain technology. Our mission is to accelerate innovation by creating a transparent, 
fair, and efficient ecosystem for research funding and collaboration.

[GitHub](https://github.com/Lucky77-afk/Sodh) | [Whitepaper](/assets/Whitepaper)
""")
