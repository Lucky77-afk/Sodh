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

# Sidebar
with st.sidebar:
    # Logo and title with animation
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("assets/logo.svg", width=50)
    with col2:
        st.markdown("<h1 style='color: #14F195; margin-top: 10px;'>DAPPR</h1>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation
    nav_options = ["🏠 Dashboard", "📝 Create Project", "🔍 Browse Projects", "📊 My Projects", "⚙️ Settings"]
    nav_option = st.radio("Navigation", nav_options, index=0, label_visibility="collapsed")
    
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
    
    # Add some space at the bottom
    st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
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
                category = st.selectbox("Category *", ["Blockchain", "AI/ML", "Biotech", "Renewable Energy", "Other"])
            
            description = st.text_area("Project Description *", 
                                     placeholder="Describe your research project in detail...", 
                                     height=150)
            
            # Funding goal with SOL conversion
            st.markdown("### 💰 Funding Goal")
            funding_col1, funding_col2 = st.columns([2, 1])
            with funding_col1:
                funding_goal = st.number_input("Amount (SOL) *", 
                                            min_value=1.0, 
                                            step=0.1,
                                            format="%.1f",
                                            help="Minimum funding goal in SOL")
            with funding_col2:
                st.markdown("<div style='margin-top: 30px; color: #A0AEC0;'>≈ $0.00</div>", 
                           unsafe_allow_html=True)
            
            # Milestones
            st.markdown("### 📅 Milestones")
            st.markdown("<div class='caption'>Add key milestones for your project with their respective rewards</div>", 
                       unsafe_allow_html=True)
            
            milestones = []
            for i in range(3):
                with st.expander(f"Milestone {i+1}", expanded=(i==0)):
                    m_col1, m_col2 = st.columns([3, 1])
                    with m_col1:
                        m_title = st.text_input(f"Title *", 
                                             key=f"milestone_title_{i}",
                                             placeholder=f"Milestone {i+1} title")
                    with m_col2:
                        m_reward = st.number_input(f"Reward (SOL) *", 
                                                min_value=0.1, 
                                                step=0.1,
                                                format="%.1f",
                                                key=f"milestone_reward_{i}")
                    m_desc = st.text_area(f"Description *", 
                                         key=f"milestone_desc_{i}",
                                         placeholder=f"Describe what will be delivered in this milestone")
                    
                    if m_title and m_desc and m_reward > 0:
                        milestones.append({
                            "title": m_title,
                            "description": m_desc,
                            "reward": m_reward,
                            "status": "Pending"
                        })
            
            # IP Terms
            st.markdown("### 📜 Intellectual Property Terms")
            ip_terms = st.text_area("Specify how intellectual property will be handled",
                                 placeholder="Describe the IP terms and conditions for this project...",
                                 height=100)
            
            # Form submission
            st.markdown("<div class='caption'>* Required fields</div>", unsafe_allow_html=True)
            
            submitted = st.form_submit_button("🚀 Create Project", type="primary", use_container_width=True)
            
            if submitted:
                if not title or not description or funding_goal <= 0 or not milestones:
                    show_error("Please fill in all required fields and add at least one valid milestone")
                else:
                    try:
                        # Create project object
                        project_id = f"PRJ-{int(time.time())}"
                        new_project = {
                            "id": project_id,
                            "title": title,
                            "category": category,
                            "description": description,
                            "funding_goal": funding_goal,
                            "funds_raised": 0,
                            "milestones": milestones,
                            "ip_terms": ip_terms,
                            "status": "Draft",
                            "created_at": int(time.time()),
                            "owner": str(st.session_state.wallet.public_key)
                        }
                        
                        # Here you would call your smart contract
                        if SMART_CONTRACTS_ENABLED and 'client' in st.session_state:
                            # Convert SOL to lamports (1 SOL = 1,000,000,000 lamports)
                            lamports = int(funding_goal * 1_000_000_000)
                            
                            # Call the smart contract
                            tx_signature = asyncio.run(
                                st.session_state.client.create_project(
                                    title=title,
                                    description=description,
                                    funding_goal=lamports,
                                    ip_terms={"terms": ip_terms}
                                )
                            )
                            new_project["tx_signature"] = tx_signature
                            
                        # Add to session state
                        if 'projects' not in st.session_state:
                            st.session_state.projects = []
                        st.session_state.projects.append(new_project)
                        
                        show_success(f"Project '{title}' created successfully! 🎉")
                        # Reset form
                        st.experimental_rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error creating project: {str(e)}")
                        st.exception(e)  # Log the full exception for debugging
    else:
        st.warning("🔒 Please connect your wallet to create a project")
        if st.button("🔗 Connect Wallet", type="primary"):
            connect_wallet()

elif nav_option == "💰 Fund Research":
    st.title("💸 Fund Research Projects")
    
    if 'wallet' in st.session_state and st.session_state.wallet is not None:
        # Search and filter section
        with st.container():
            st.markdown("### 🔍 Find Projects to Support")
            
            # Search and filter in columns
            col1, col2, col3 = st.columns([3, 2, 2])
            
            with col1:
                search_query = st.text_input("Search projects...", 
                                           placeholder="Search by title, description, or tags")
            
            with col2:
                categories = ["All Categories", "Blockchain", "AI/ML", "Biotech", "Renewable Energy", "Other"]
                selected_category = st.selectbox("Category", categories)
            
            with col3:
                statuses = ["All Statuses", "Active", "Funded", "In Progress", "Completed"]
                selected_status = st.selectbox("Status", statuses)
        
        # Display projects in a grid
        st.markdown("### 🚀 Available Projects")
        
        # Sample project data (in a real app, this would come from your smart contract)
        projects = [
            {
                "id": "PRJ-001",
                "title": "Decentralized Identity Solution",
                "category": "Blockchain",
                "description": "Building a self-sovereign identity solution on Solana that gives users full control over their personal data.",
                "funding_goal": 100,
                "funds_raised": 45,
                "status": "Active",
                "owner": str(st.session_state.wallet.public_key)[:8] + "..." + str(st.session_state.wallet.public_key)[-4:],
                "milestones": 3,
                "created_at": "2023-05-15",
                "tags": ["identity", "privacy", "web3"]
            },
            {
                "id": "PRJ-002",
                "title": "AI for Climate Modeling",
                "category": "AI/ML",
                "description": "Using machine learning to improve climate prediction models and help combat climate change.",
                "funding_goal": 200,
                "funds_raised": 180,
                "status": "Active",
                "owner": "7xYt...9m4n",
                "milestones": 4,
                "created_at": "2023-06-01",
                "tags": ["ai", "climate", "sustainability"]
            }
        ]
        
        # Filter projects
        filtered_projects = projects
        if search_query:
            filtered_projects = [p for p in filtered_projects 
                              if (search_query.lower() in p["title"].lower() 
                                   or search_query.lower() in p["description"].lower()
                                   or any(search_query.lower() in tag.lower() for tag in p.get("tags", [])))]
        
        if selected_category != "All Categories":
            filtered_projects = [p for p in filtered_projects if p["category"] == selected_category]
            
        if selected_status != "All Statuses":
            filtered_projects = [p for p in filtered_projects if p["status"] == selected_status]
        
        # Display projects in a responsive grid
        if not filtered_projects:
            st.info("🌟 No projects found matching your criteria. Try adjusting your filters.")
        else:
            # Create a responsive grid
            cols = st.columns(1)  # Single column for mobile, will be adjusted with CSS
            
            for i, project in enumerate(filtered_projects):
                with cols[0]:
                    with st.container():
                        progress = min(100, int((project['funds_raised'] / project['funding_goal']) * 100))
                        category_color = {
                            'Blockchain': '#9945FF',
                            'AI/ML': '#00C4FF',
                            'Biotech': '#FF6B6B',
                            'Renewable Energy': '#4CAF50',
                            'Other': '#9C27B0'
                        }.get(project['category'], '#666666')
                        
                        # Format description with ellipsis if too long
                        desc = (project['description'][:150] + '...') if len(project['description']) > 150 else project['description']
                        
                        # Get status color
                        status_color = {
                            'Active': '#14F195',
                            'Funded': '#00C4FF',
                            'In Progress': '#FFD700',
                            'Completed': '#4CAF50'
                        }.get(project['status'], '#A0AEC0')
                        
                        # Render the card with proper string formatting
                        card_html = f"""
                        <div class='card' style='margin-bottom: 20px; padding: 15px; border-radius: 8px; background: #1A1E2C;'>
                            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
                                <h3 style='margin: 0; color: white;'>{project['title']}</h3>
                                <span style='background: {category_color}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.8em;'>{project['category']}</span>
                            </div>
                            <p style='color: #A0AEC0; margin-bottom: 15px;'>{desc}</p>
                            
                            <div style='margin-bottom: 15px;'>
                                <div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>
                                    <span style='color: #A0AEC0;'>Progress</span>
                                    <span style='color: white;'>{progress}%</span>
                                </div>
                                <div style='height: 8px; background: #2D3748; border-radius: 4px; overflow: hidden;'>
                                    <div style='width: {progress}%; height: 100%; background: #14F195;'></div>
                                </div>
                                <div style='display: flex; justify-content: space-between; margin-top: 5px;'>
                                    <small style='color: #A0AEC0;'>{project['funds_raised']} SOL raised</small>
                                    <small style='color: #A0AEC0;'>Goal: {project['funding_goal']} SOL</small>
                                </div>
                            </div>
                            
                            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
                                <div>
                                    <small style='color: #A0AEC0;'>👤 {project['owner']}</small> • 
                                    <small style='color: #A0AEC0;'>📅 {project.get('created_at', 'N/A')}</small> • 
                                    <small style='color: #A0AEC0;'>📌 {project.get('milestones', 0)} milestones</small>
                                </div>
                                <span style='color: {status_color}; font-weight: 500;'>{project['status']}</span>
                            </div>
                            
                            <button class='stButton' style='width: 100%; padding: 8px 16px; background: #14F195; color: black; border: none; border-radius: 6px; cursor: pointer; font-weight: 600;'>
                                💰 Fund Project
                            </button>
                        </div>
                        """
                        st.markdown(card_html, unsafe_allow_html=True)
                        
                        # Add fund button handler
                        if st.button(f"Fund {project['title']}", key=f"fund_{project['id']}"):
                            st.session_state.selected_project = project
                            st.experimental_rerun()
    else:
        st.warning("🔒 Please connect your wallet to browse and fund projects")
        if st.button("🔗 Connect Wallet", type="primary"):
            connect_wallet()
            
        # Show some sample projects to encourage signup
        st.markdown("## 🌟 Featured Projects")
        st.markdown("Connect your wallet to see all available projects and start funding research!")
        
        # Sample project cards (hidden until connected)
        sample_projects = [
            {
                "title": "Decentralized Identity",
                "category": "Blockchain",
                "description": "Self-sovereign identity solution giving users control over their personal data.",
                "funding_goal": 100,
                "funds_raised": 45,
                "status": "Active"
            },
            {
                "title": "AI Climate Models",
                "category": "AI/ML",
                "description": "Improving climate prediction accuracy with machine learning.",
                "funding_goal": 200,
                "funds_raised": 180,
                "status": "Active"
            }
        ]
        
        for project in sample_projects:
            with st.container():
                # Get category color for sample project
                sample_category_color = {
                    'Blockchain': '#9945FF',
                    'AI/ML': '#00C4FF',
                    'Biotech': '#FF6B6B',
                    'Renewable Energy': '#4CAF50',
                    'Other': '#9C27B0'
                }.get(project['category'], '#666666')
                
                # Format description for sample project
                sample_desc = (project['description'][:150] + '...') if len(project['description']) > 150 else project['description']
                
                # Sample project card HTML
                sample_card = f"""
                <div class='card' style='margin-bottom: 20px; padding: 15px; border-radius: 8px; background: #1A1E2C; opacity: 0.7; filter: blur(1px); pointer-events: none;'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
                        <h3 style='margin: 0; color: white;'>{title}</h3>
                        <span style='background: {color}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.8em;'>{category}</span>
                    </div>
                    <p style='color: #A0AEC0; margin-bottom: 15px;'>{description}</p>
                    
                    <div style='margin-bottom: 15px;'>
                        <div style='display: flex; justify-content: space-between;'>
                            <small style='color: #A0AEC0;'>Connect wallet to see details</small>
                            <span style='color: #14F195; font-weight: 500;'>{status}</span>
                        </div>
                        <div style='height: 8px; background: #2D3748; border-radius: 4px; margin-top: 10px; overflow: hidden;'>
                            <div style='width: 30%; height: 100%; background: #14F195; opacity: 0.5;'></div>
                        </div>
                    </div>
                </div>
                """.format(
                    title=project['title'],
                    category=project['category'],
                    description=sample_desc,
                    status=project['status'],
                    color=sample_category_color
                )
                st.markdown(sample_card, unsafe_allow_html=True)

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
