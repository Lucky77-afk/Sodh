"""
DAPPR - Decentralized Academic-Industry Partnership Platform
"""
import streamlit as st
import base58
import json
import asyncio
from pathlib import Path
from solana.rpc.async_api import AsyncClient
from solana.keypair import Keypair
from solana.publickey import PublicKey

# Import our DAPPR client
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from contracts.client import DapprClient

# Set page config
st.set_page_config(
    page_title="DAPPR - Decentralized Research Platform",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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

# Initialize session state
if 'wallet' not in st.session_state:
    st.session_state.wallet = None
    st.session_state.client = None
    st.session_state.connected = False

# Sidebar for logo and wallet connection
with st.sidebar:
    # Add logo at the top
    st.image("assets/images/logo.png", width=200)
    st.markdown("---")
    
    st.title("🔑 Wallet Connection")
    
    if st.button("Connect Wallet" if not st.session_state.connected else "Disconnect Wallet"):
        if not st.session_state.connected:
            try:
                # In a real app, this would connect to a wallet like Phantom
                # For demo, we'll generate a new keypair
                st.session_state.wallet = Keypair()
                st.session_state.client = DapprClient(
                    rpc_url="https://api.devnet.solana.com",
                    program_id="DAPPR1111111111111111111111111111111111111",
                    wallet=st.session_state.wallet
                )
                st.session_state.connected = True
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Failed to connect wallet: {str(e)}")
        else:
            st.session_state.wallet = None
            st.session_state.client = None
            st.session_state.connected = False
            st.experimental_rerun()
    
    if st.session_state.connected:
        st.success("✅ Wallet Connected")
        st.write(f"Address: `{st.session_state.wallet.public_key}`")
        st.write("Network: Devnet")
    else:
        st.warning("🔌 Wallet not connected")

# Main app
st.title("🔬 DAPPR - Decentralized Research Platform")
st.markdown("### Bridge the gap between academic research and industry collaboration")

if not st.session_state.connected:
    st.warning("Please connect your wallet to continue")
    st.stop()

# Tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Create Project", "Fund Project", "My Projects"])

with tab1:
    st.header("Create New Research Project")
    
    with st.form("create_project_form"):
        title = st.text_input("Project Title")
        description = st.text_area("Project Description")
        funding_goal = st.number_input("Funding Goal (SOL)", min_value=0.1, step=0.1)
        
        st.subheader("Intellectual Property Terms")
        col1, col2 = st.columns(2)
        with col1:
            license_type = st.selectbox(
                "License Type",
                ["MIT", "Apache 2.0", "GPL-3.0", "Proprietary"]
            )
        with col2:
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

with tab2:
    st.header("Fund a Research Project")
    st.info("Browse and fund promising research projects")
    
    # In a real app, this would fetch projects from the blockchain
    st.warning("Project listing functionality coming soon!")

with tab3:
    st.header("My Research Projects")
    
    if st.session_state.connected:
        # In a real app, this would fetch user's projects from the blockchain
        st.info("No projects found. Create your first project to get started!")
    else:
        st.warning("Please connect your wallet to view your projects")

# Footer
st.markdown("---")
st.markdown("### About DAPPR")
st.markdown("""
DAPPR is a decentralized platform that bridges the gap between academic research and industry collaboration 
using Solana blockchain technology. Our mission is to accelerate innovation by creating a transparent, 
fair, and efficient ecosystem for research funding and collaboration.

[GitHub](https://github.com/Lucky77-afk/Sodh) | [Whitepaper](/assets/Whitepaper)
""")
