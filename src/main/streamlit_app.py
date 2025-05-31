"""
DAPPR - Decentralized Academic-Industry Partnership Platform
"""
import streamlit as st
import base58
import json
import asyncio
import time
import os
from pathlib import Path
from datetime import datetime
from solana.rpc.async_api import AsyncClient
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.commitment import Confirmed
from streamlit_extras.stylable_container import stylable_container

# Add project root to path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

# Try to import DapprClient, but don't fail if it's not available
try:
    from contracts.client import DapprClient
    SMART_CONTRACTS_ENABLED = True
except (ImportError, ModuleNotFoundError):
    SMART_CONTRACTS_ENABLED = False
    st.warning("Smart contract integration is not available. Running in demo mode.")

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
        with st.spinner("🔌 Connecting wallet..."):
            # In a real app, this would connect to a wallet like Phantom
            # For demo purposes, we'll generate a new keypair
            time.sleep(1)  # Simulate connection delay
            
            # Generate a new keypair for the wallet
            st.session_state.wallet = Keypair()
            
            # Initialize the DapprClient if available
            if SMART_CONTRACTS_ENABLED:
                st.session_state.client = DapprClient(
                    rpc_url="https://api.devnet.solana.com",
                    program_id="DAPPR1111111111111111111111111111111111111",
                    wallet=st.session_state.wallet
                )
            
            st.session_state.connected = True
            show_success("✅ Wallet connected successfully!")
    except Exception as e:
        st.error(f"❌ Failed to connect wallet: {str(e)}")
        st.exception(e)  # Log the full exception for debugging

def disconnect_wallet():
    st.session_state.wallet = None
    st.session_state.client = None
    st.session_state.connected = False
    st.session_state.projects = []
    clear_messages()
    st.experimental_rerun()

# Display success/error messages
if st.session_state.show_success:
    st.success(st.session_state.success_message, icon="✅")
    time.sleep(3)
    st.session_state.show_success = False

if st.session_state.show_error:
    st.error(st.session_state.error_message, icon="❌")
    time.sleep(3)
    st.session_state.show_error = False

# Sidebar with custom styling
st.markdown("""
<style>
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        color: white;
    }
    .stRadio > div > label {
        color: white !important;
        padding: 10px;
        margin: 5px 0;
        border-radius: 8px;
        transition: all 0.3s;
    }
    .stRadio > div > label:hover {
        background: rgba(20, 241, 149, 0.1);
    }
    .stRadio > div > div > div {
        margin: 10px 0;
    }
    .wallet-address {
        font-family: monospace;
        background: #1e293b;
        padding: 10px;
        border-radius: 8px;
        margin: 15px 0;
        word-break: break-all;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    # Logo and title
    st.image("assets/logo.svg", width=50)
    st.markdown("<h1 style='color: #14F195; margin-top: 10px;'>DAPPR</h1>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation
    st.markdown("### NAVIGATION")
    nav_options = [
        "📊 Dashboard",
        "🔄 Transactions",
        "👤 Account",
        "📝 Smart Contract",
        "📄 Whitepaper",
        "🎓 Tutorial"
    ]
    nav_option = st.radio("", nav_options, index=0, label_visibility="collapsed")
    
    st.markdown("---")
    
    # Wallet Connection
    st.markdown("### CONNECT WALLET")
    wallet_address = st.text_input("Wallet Address", 
                                 placeholder="Enter Solana wallet address",
                                 label_visibility="collapsed")
    
    if wallet_address:
        st.markdown(f"<div class='wallet-address'>{wallet_address}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # About Section
    st.markdown("### ABOUT DAPPR")
    st.markdown("""
    Decentralized Autonomous Platform for Propagation of Research (DAPPR) 
    leverages Solana blockchain to revolutionize academia-industry collaboration.
    """)
    
    st.markdown("---")
    st.markdown("Sodh Explorer v1.0  ")
    
    st.markdown("---")
    
    # Wallet connection
    if 'wallet' in st.session_state and st.session_state.wallet is not None:
        st.markdown("### Wallet")
        st.markdown(
            f"<div class='wallet-address' title='Click to copy' style='cursor: pointer;' onclick='navigator.clipboard.writeText(\"{st.session_state.wallet.public_key}\")'>{st.session_state.wallet.public_key}</div>",
            unsafe_allow_html=True
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔄 Refresh", use_container_width=True, type="secondary"):
                st.experimental_rerun()
        with col2:
            if st.button("🚪 Disconnect", use_container_width=True):
                disconnect_wallet()
    else:
        if st.button("🔗 Connect Wallet", use_container_width=True):
            connect_wallet()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6B7280; font-size: 0.8rem;">
        <p>DAPPR v1.0.0</p>
        <p>© 2025 All rights reserved</p>
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
        with col3:
            st.metric("Total Funding", "42 SOL")
            
        st.markdown("### Recent Activity")
        st.info("Recent activity will be displayed here.")
    else:
        st.warning("🔒 Please connect your wallet to view your dashboard")
        if st.button("🔗 Connect Wallet", type="primary"):
            connect_wallet()

elif nav_option == "🔄 Transactions":
    st.title("🔄 Transactions")
    st.info("Transaction history will be displayed here.")

elif nav_option == "👤 Account":
    st.title("👤 Account")
    
    if st.session_state.connected:
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.image("assets/logo.svg", width=150)
        
        with col2:
            st.markdown(f"### Wallet Address")
            st.code(str(st.session_state.wallet.public_key))
            
            if st.button("Disconnect Wallet"):
                disconnect_wallet()
    else:
        st.warning("🔒 Please connect your wallet to view account details")
        if st.button("🔗 Connect Wallet", type="primary"):
            connect_wallet()

elif nav_option == "📝 Smart Contract":
    st.title("📝 Smart Contract Manager")
    st.markdown("Deploy and interact with smart contracts on the Solana blockchain.")
    
    if st.session_state.connected:
        tab1, tab2, tab3 = st.tabs(["📜 Deployed Contracts", "🚀 Deploy New", "📚 Documentation"])
        
        with tab1:
            st.header("Your Smart Contracts")
            
            if 'deployed_contracts' not in st.session_state:
                st.session_state.deployed_contracts = []
            
            if not st.session_state.deployed_contracts:
                st.info("You haven't deployed any smart contracts yet.")
            else:
                for contract in st.session_state.deployed_contracts:
                    with st.expander(f"📄 {contract['name']} ({contract['address'][:8]}...{contract['address'][-4:]})"):
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.markdown(f"""
                            **Network:** `{contract['network']}`  
                            **Type:** `{contract['type']}`  
                            **Deployed:** `{contract['deployed_at']}`
                            """)
                        with col2:
                            st.code(contract['address'])
                            
                        if st.button("Interact", key=f"interact_{contract['address']}"):
                            st.session_state.active_contract = contract['address']
                            st.experimental_rerun()
        
        with tab2:
            st.header("Deploy New Contract")
            
            contract_type = st.selectbox(
                "Select Contract Type",
                ["Research Project", "Funding Pool", "IP License", "Custom"]
            )
            
            contract_name = st.text_input("Contract Name")
            
            if contract_type == "Custom":
                contract_code = st.text_area("Contract Code (Rust)", height=300)
                st.info("Note: Custom contracts will be compiled on the client side before deployment.")
            
            if st.button("Deploy Contract", type="primary"):
                if not contract_name:
                    st.error("Please enter a contract name")
                else:
                    with st.spinner("Deploying contract to Solana devnet..."):
                        # Simulate deployment
                        time.sleep(2)
                        new_contract = {
                            "name": contract_name,
                            "type": contract_type,
                            "address": f"{base58.b58encode(os.urandom(32)).decode('utf-8')}",
                            "network": "devnet",
                            "deployed_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "abi": {}
                        }
                        st.session_state.deployed_contracts.append(new_contract)
                        st.success(f"✅ Contract deployed successfully!")
                        st.balloons()
                        st.experimental_rerun()
        
        with tab3:
            st.header("Smart Contract Documentation")
            
            st.markdown("""
            ### Available Contract Types
            
            1. **Research Project**
               - Manages research project lifecycle
               - Handles funding milestones
               - Tracks deliverables
            
            2. **Funding Pool**
               - Manages pooled funding
               - Handles distributions
               - Tracks contributions
            
            3. **IP License**
               - Manages intellectual property rights
               - Handles licensing terms
               - Tracks usage
            
            4. **Custom**
               - Deploy your own Solana program
               - Requires Rust code
            
            ### Interaction Guide
            - Connect your wallet to view deployed contracts
            - Use the "Interact" button to call contract methods
            - All transactions require wallet confirmation
            """)
    else:
        st.warning("🔒 Please connect your wallet to interact with smart contracts")
        if st.button("🔗 Connect Wallet", type="primary"):
            connect_wallet()

elif nav_option == "📄 Whitepaper":
    st.title("📄 Whitepaper")
    st.markdown("""
    ## Decentralized Autonomous Platform for Propagation of Research (DAPPR)
    
    ### Abstract
    DAPPR leverages Solana blockchain to revolutionize academia-industry collaboration by creating a decentralized 
    platform for research funding, intellectual property management, and knowledge sharing.
    
    ### Key Features
    - **Decentralized Funding**: Transparent and secure funding for research projects
    - **IP Management**: Blockchain-based intellectual property rights management
    - **Smart Contracts**: Automated execution of research agreements
    - **Token Economy**: Native token for platform governance and rewards
    
    [Read the full whitepaper here](https://example.com/whitepaper)
    """)

elif nav_option == "🎓 Tutorial":
    st.title("🎓 Tutorial")
    
    st.markdown("### Getting Started with DAPPR")
    
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    
    st.markdown("### Step-by-Step Guide")
    
    steps = [
        "1. Connect your Solana wallet",
        "2. Browse available research projects",
        "3. Fund projects you're interested in",
        "4. Track project progress and milestones",
        "5. Receive rewards and updates"
    ]
    
    for step in steps:
        st.markdown(f"- {step}")
    
    st.download_button(
        label="📥 Download User Guide (PDF)",
        data=b"Sample PDF content",
        file_name="dappr_user_guide.pdf",
        mime="application/pdf"
    )

# Project funding modal
if 'selected_project' in st.session_state and st.session_state.selected_project is not None:
    project = st.session_state.selected_project
    
    # Create a modal
    with st.container():
        st.markdown(f"## 💰 Fund {project['title']}")
        st.markdown(f"**Category:** {project['category']}")
        st.markdown(f"**Project Owner:** `{project['owner']}`")
        
        # Funding amount
        amount = st.number_input("Amount (SOL)", 
                               min_value=0.1, 
                               step=0.1,
                               format="%.1f",
                               help="Minimum funding amount is 0.1 SOL")
        
        # Project progress
        progress = min(100, int((project['funds_raised'] / project['funding_goal']) * 100))
        st.markdown("### Funding Progress")
        st.markdown(f"""
        <div style='margin: 10px 0 20px;'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>
                <span>{project['funds_raised']} SOL raised</span>
                <span>{progress}% of {project['funding_goal']} SOL goal</span>
            </div>
            <div style='height: 8px; background: #2D3748; border-radius: 4px; overflow: hidden;'>
                <div style='width: {progress}%; height: 100%; background: #14F195;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Terms and conditions
        st.markdown("### Terms & Conditions")
        st.markdown("""
        - Your funds will be held in escrow until project completion
        - If funding goal is not met, you will receive a full refund
        - Project milestones must be approved by backers before funds are released
        - A 2% platform fee will be applied to all contributions
        """)
        
        # Action buttons
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("← Back to Projects"):
                del st.session_state.selected_project
                st.experimental_rerun()
        with col2:
            if st.button("Confirm Funding", type="primary"):
                try:
                    # In a real app, this would be an async call to the smart contract
                    # tx_sig = asyncio.run(
                    #     st.session_state.client.fund_project(
                    #         project_id=project['id'],
                    #         amount=int(amount * 1_000_000_000)  # Convert to lamports
                    #     )
                    # )
                    show_success(f"Successfully funded {amount} SOL to {project['title']}!")
                    del st.session_state.selected_project
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"❌ Failed to fund project: {str(e)}")

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
