import streamlit as st
import base58
import pandas as pd
from datetime import datetime

def render_contract_header():
    """Renders the collaborative contract header with details"""
    st.markdown("""
    <h2>Solana Smart Contract</h2>
    <div style="background-color: #1E1E1E; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 4px solid #14F195;">
        <div style="font-size: 0.9rem; color: #AAA;">CONTRACT ADDRESS</div>
        <div class="wallet-address">Coll1ABbXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxX</div>
        <div style="margin-top: 10px; font-size: 0.9rem; color: #AAA;">CONTRACT TYPE</div>
        <div style="color: #FFFFFF;">Collaboration Agreement</div>
    </div>
    """, unsafe_allow_html=True)

def render_contract_projects():
    """Display list of collaborative projects from the contract"""
    st.markdown("### Collaborative Projects")
    
    # Sample project data (would come from contract in production)
    projects = [
        {
            "id": "Proj1",
            "name": "Quantum Research Collaboration",
            "description": "A collaborative project to research quantum computing applications in bioinformatics",
            "participants": 3,
            "milestones": 2,
            "created_at": "2025-04-15",
            "status": "Active"
        },
        {
            "id": "Proj2",
            "name": "Decentralized AI Training Framework",
            "description": "Developing a framework for decentralized AI model training using blockchain validation",
            "participants": 5,
            "milestones": 4,
            "created_at": "2025-03-28",
            "status": "Active"
        },
        {
            "id": "Proj3",
            "name": "Carbon Credit Tokenization System",
            "description": "Building a system to tokenize and trade carbon credits on Solana blockchain",
            "participants": 4,
            "milestones": 3,
            "created_at": "2025-03-10",
            "status": "Completed"
        }
    ]
    
    for project in projects:
        status_color = "#14F195" if project["status"] == "Active" else "#9945FF"
        
        st.markdown(f"""
        <div style="background-color: #1E1E1E; padding: 15px; border-radius: 10px; margin-bottom: 15px; cursor: pointer;" 
             onclick="alert('Project details would open here');">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0; color: #FFFFFF;">{project["name"]}</h3>
                <div style="color: {status_color}; font-size: 0.9rem; font-weight: bold;">
                    {project["status"]}
                </div>
            </div>
            <p style="color: #AAAAAA; margin-top: 8px; margin-bottom: 12px;">
                {project["description"]}
            </p>
            <div style="display: flex; gap: 15px; font-size: 0.8rem;">
                <div style="color: #AAAAAA;">
                    <span style="color: #14F195; font-weight: bold;">{project["participants"]}</span> Participants
                </div>
                <div style="color: #AAAAAA;">
                    <span style="color: #14F195; font-weight: bold;">{project["milestones"]}</span> Milestones
                </div>
                <div style="color: #AAAAAA;">
                    Created: {project["created_at"]}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_project_form():
    """Renders a form to create a new collaboration project"""
    with st.expander("Create New Project"):
        with st.form("new_project_form"):
            project_name = st.text_input("Project Name")
            project_description = st.text_area("Project Description")
            ip_terms = st.text_area("IP Terms", 
                                     value="All intellectual property developed through this collaboration will be jointly owned by participants proportional to their contribution percentage.")
            
            # Form submission
            submit_button = st.form_submit_button("Create Project")
            
            if submit_button:
                if project_name and project_description:
                    st.success(f"Project '{project_name}' would be created on the blockchain")
                else:
                    st.error("Please fill in all required fields")

def render_smart_contract():
    """Main function to render smart contract interface"""
    st.markdown('<h2>DAPPR Smart Contract</h2>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Projects", "Contract Explorer", "Milestones", "Participants"])
    
    with tabs[0]:
        render_contract_header()
        col1, col2 = st.columns([2, 1])
        with col1:
            render_project_form()
        render_contract_projects()
        
    with tabs[1]:
        st.markdown("### Smart Contract Functions")
        functions = [
            {"name": "initialize_project", "description": "Creates a new collaboration project"},
            {"name": "add_participant", "description": "Adds a participant to a project"},
            {"name": "add_milestone", "description": "Creates a milestone for the project"},
            {"name": "fund_milestone", "description": "Funds a milestone with USDC"},
            {"name": "complete_milestone", "description": "Marks a milestone as completed"},
            {"name": "approve_milestone", "description": "Approves a completed milestone"},
            {"name": "distribute_milestone_payment", "description": "Distributes payment to participants"}
        ]
        
        for function in functions:
            st.markdown(f"""
            <div style="background-color: #1E1E1E; padding: 12px; border-radius: 6px; margin-bottom: 8px;">
                <div style="font-family: 'Roboto Mono', monospace; color: #14F195;">{function["name"]}</div>
                <div style="font-size: 0.9rem; color: #AAAAAA; margin-top: 4px;">{function["description"]}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("### Contract Events")
        events = [
            {"name": "ProjectCreatedEvent", "time": "2025-04-15 14:32:11", "transaction": "4ztK...xPq9"},
            {"name": "ParticipantAddedEvent", "time": "2025-04-15 15:10:22", "transaction": "7mnR...vFw2"},
            {"name": "MilestoneAddedEvent", "time": "2025-04-16 09:45:17", "transaction": "2kLp...tR8j"}
        ]
        
        for event in events:
            st.markdown(f"""
            <div style="background-color: #1E1E1E; padding: 12px; border-radius: 6px; margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between;">
                    <div style="font-family: 'Roboto Mono', monospace; color: #9945FF;">{event["name"]}</div>
                    <div style="font-size: 0.8rem; color: #AAAAAA;">{event["time"]}</div>
                </div>
                <div style="font-size: 0.9rem; color: #AAAAAA; margin-top: 4px;">
                    Tx: <span class="transaction-hash">{event["transaction"]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown("### Project Milestones")
        
        milestones = [
            {
                "title": "Initial Quantum Algorithm Design",
                "description": "Develop the theoretical framework for quantum algorithms targeting protein folding predictions",
                "deadline": "2025-05-23",
                "payment": "50 USDC",
                "status": "Funded"
            },
            {
                "title": "Prototype Implementation",
                "description": "Implement prototype of quantum algorithm on simulator and analyze performance",
                "deadline": "2025-06-23",
                "payment": "100 USDC",
                "status": "Pending"
            }
        ]
        
        for i, milestone in enumerate(milestones):
            status_color = "#14F195" if milestone["status"] == "Funded" else "#AAA"
            
            st.markdown(f"""
            <div style="background-color: #1E1E1E; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="margin: 0; color: #FFFFFF;">{milestone["title"]}</h3>
                    <div style="color: {status_color}; font-size: 0.9rem; font-weight: bold;">
                        {milestone["status"]}
                    </div>
                </div>
                <p style="color: #AAAAAA; margin-top: 8px; margin-bottom: 12px;">
                    {milestone["description"]}
                </p>
                <div style="display: flex; gap: 15px; font-size: 0.8rem;">
                    <div style="color: #AAAAAA;">
                        Deadline: <span style="color: #FFFFFF;">{milestone["deadline"]}</span>
                    </div>
                    <div style="color: #AAAAAA;">
                        Payment: <span style="color: #14F195; font-weight: bold;">{milestone["payment"]}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if milestone["status"] == "Funded":
                st.markdown(f"""
                <div style="padding-left: 15px; margin-bottom: 20px;">
                    <button style="background-color: #9945FF; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-family: 'Inter', sans-serif;">
                        Mark as Completed
                    </button>
                </div>
                """, unsafe_allow_html=True)
    
    with tabs[3]:
        st.markdown("### Project Participants")
        
        participants = [
            {
                "name": "Dr. Alice Johnson",
                "role": "Lead Researcher",
                "contribution": "40%",
                "joined": "2025-04-15",
                "wallet": "8ZtK...xBw4"
            },
            {
                "name": "Dr. Bob Smith",
                "role": "Quantum Algorithm Specialist",
                "contribution": "35%",
                "joined": "2025-04-15",
                "wallet": "5RnP...vZq7"
            },
            {
                "name": "Dr. Carol Williams",
                "role": "Bioinformatics Expert",
                "contribution": "25%",
                "joined": "2025-04-16",
                "wallet": "3mLj...tA1s"
            }
        ]
        
        for participant in participants:
            st.markdown(f"""
            <div style="background-color: #1E1E1E; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="margin: 0; color: #FFFFFF;">{participant["name"]}</h3>
                    <div style="color: #14F195; font-size: 0.9rem; font-weight: bold;">
                        {participant["contribution"]}
                    </div>
                </div>
                <p style="color: #AAAAAA; margin-top: 8px; margin-bottom: 12px;">
                    {participant["role"]}
                </p>
                <div style="display: flex; gap: 15px; font-size: 0.8rem;">
                    <div style="color: #AAAAAA;">
                        Joined: <span style="color: #FFFFFF;">{participant["joined"]}</span>
                    </div>
                    <div style="color: #AAAAAA;">
                        Wallet: <span class="transaction-hash">{participant["wallet"]}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)