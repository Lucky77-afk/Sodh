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
    from utils.database import get_projects, get_participants, get_milestones
    
    st.markdown("### Collaborative Projects")
    
    # Example/fallback projects to show if database access fails
    example_projects = [
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
    
    # Initialize projects list
    projects = []
    
    try:
        # Get projects from database
        db_projects = get_projects()
        
        # Process projects from database
        if db_projects:
            for project in db_projects:
                try:
                    # Get related data with error handling
                    try:
                        participants_count = len(get_participants(project_id=project['id']))
                    except:
                        participants_count = 0
                        
                    try:
                        milestones_count = len(get_milestones(project_id=project['id']))
                    except:
                        milestones_count = 0
                    
                    # Format data for display
                    projects.append({
                        "id": project['id'],
                        "name": project['name'],
                        "description": project['description'],
                        "participants": participants_count,
                        "milestones": milestones_count,
                        "created_at": project['created_at'],
                        "status": "Active"  # Default status for now
                    })
                except Exception as e:
                    st.warning(f"Error processing project data: {str(e)}")
    except Exception as e:
        st.warning(f"Error retrieving projects from database: {str(e)}")
        # Use example projects as fallback
        projects = example_projects
        
    # If still no projects, use examples
    if not projects:
        projects = example_projects
    
    for project in projects:
        status_color = "#14F195" if project["status"] == "Active" else "#9945FF"
        
        # Generate a unique key for this project's button
        button_key = f"select_project_{project['id']}_{project['name'].replace(' ', '_')}"
        
        # Create the project card
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div style="background-color: #1E1E1E; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
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
            
            with col2:
                if st.button(f"Select", key=button_key):
                    st.session_state.current_project_id = project['id']
                    st.success(f"Selected project: {project['name']}")
                    st.rerun()

def render_project_form():
    """Renders a form to create a new collaboration project"""
    from components.transaction_submitter_simplified import render_project_submission_form
    from utils.database import create_project
    
    # Render the project submission form and get the result
    success, result = render_project_submission_form()
    
    # Check if we have a successful result
    if success and result and 'signature' in result and 'data' in result and 'args' in result['data']:
        try:
            # Store the project in the database
            project = create_project(
                name=result['data']['args']['name'],
                description=result['data']['args']['description'],
                ip_terms=result['data']['args'].get('ip_terms'),
                transaction_signature=result['signature']
            )
            
            # Store project ID in session state for other components to use
            if project:
                st.session_state.current_project_id = project.id
                
                # Show success message with transaction details
                st.success("Project created successfully!")
                st.markdown(f"""
                <div style="background-color: #1E1E1E; padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span style="color: #AAA;">Transaction Signature:</span>
                        <span class="transaction-hash">{result['signature'][:10]}...{result['signature'][-8:]}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span style="color: #AAA;">Project Name:</span>
                        <span style="color: #FFFFFF;">{result['data']['args']['name']}</span>
                    </div>
                    <div style="color: #14F195; margin-top: 10px;">
                        The project has been created and stored on the blockchain.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Reset form state
                if 'project_form_submitted' in st.session_state:
                    del st.session_state.project_form_submitted
                    
                # Store transaction signature in session state
                st.session_state.latest_tx_signature = result['signature']
                
                # Force a rerun to update the UI
                st.rerun()
                
        except Exception as e:
            st.error(f"Error creating project: {str(e)}")
            # Log the full error for debugging
            import traceback
            st.error(traceback.format_exc())
    elif result is not None and not success:
        # Show error message if the form was submitted but there was an error
        st.error("There was an error processing your request. Please try again.")

def render_smart_contract():
    """Main function to render smart contract interface"""
    st.markdown('<h2>DAPPR Smart Contract</h2>', unsafe_allow_html=True)
    
    # Get current wallet address from session state
    wallet_address = st.session_state.get('connected_wallet')
    
    # Show wallet connection status
    if not wallet_address:
        st.markdown("""
        <div style="background-color: #1E1E1E; padding: 15px; border-radius: 10px; margin: 15px 0;">
            <div style="color: #9945FF; margin-bottom: 10px;">Wallet Status:</div>
            <div style="color: #AAA;">
                <span style="color: #FF5C5C; font-weight: bold;">❌ Not Connected</span>
                <span style="color: #AAA;"> - Connect your wallet to execute smart contract functions</span>
            </div>
            <div style="margin-top: 10px;">
                <a href="https://solana.com/wallet" target="_blank" style="color: #9945FF; text-decoration: none;">
                    Learn more about Solana wallets
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background-color: #1E1E1E; padding: 15px; border-radius: 10px; margin: 15px 0;">
            <div style="color: #9945FF; margin-bottom: 10px;">Wallet Status:</div>
            <div style="color: #AAA;">
                <span style="color: #14F195; font-weight: bold;">✅ Connected</span>
                <span style="color: #AAA;"> - Ready to execute smart contract functions</span>
            </div>
            <div style="margin-top: 10px;">
                <a href="https://solana.com/wallet" target="_blank" style="color: #9945FF; text-decoration: none;">
                    Learn more about Solana wallets
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    tabs = st.tabs(["Projects", "Contract Explorer", "Milestones", "Participants"])
    
    with tabs[0]:
        render_contract_header()
        
        # Project Operations
        st.markdown("### Project Operations")
        
        # Create Project
        if st.button("Create New Project", type="primary"):
            with st.expander("Create Project Details"):
                project_name = st.text_input("Project Name")
                description = st.text_area("Description")
                
                if st.button("Submit Project", type="primary"):
                    if project_name and description:
                        tx_data = {
                            "args": {
                                "name": project_name,
                                "description": description,
                                "admin": wallet_address
                            }
                        }
                        success, result = render_transaction_submitter("initialize_project", tx_data)
                        if success:
                            st.success(f"Project created successfully: {result['signature']}")
                            st.rerun()
                    else:
                        st.error("Please fill in all required fields")
        
        # Add Participant
        if st.button("Add Participant", type="secondary"):
            with st.expander("Add Participant Details"):
                participant_name = st.text_input("Participant Name")
                wallet_address = st.text_input("Participant Wallet Address")
                role = st.text_input("Role")
                
                if st.button("Add Participant", type="primary"):
                    if participant_name and wallet_address and role:
                        tx_data = {
                            "args": {
                                "name": participant_name,
                                "wallet_address": wallet_address,
                                "role": role,
                                "project_id": st.session_state.get('current_project_id')
                            }
                        }
                        success, result = render_transaction_submitter("add_participant", tx_data)
                        if success:
                            st.success(f"Participant added successfully: {result['signature']}")
                            st.rerun()
                    else:
                        st.error("Please fill in all required fields")
        
        # Add Milestone
        if st.button("Add Milestone", type="secondary"):
            with st.expander("Add Milestone Details"):
                title = st.text_input("Milestone Title")
                description = st.text_area("Description")
                deadline = st.date_input("Deadline")
                payment_amount = st.number_input("Payment Amount", min_value=0.0, step=0.001)
                token_type = st.selectbox("Token Type", ["SOL", "USDT"])
                
                if st.button("Add Milestone", type="primary"):
                    if title and description and deadline and payment_amount > 0:
                        tx_data = {
                            "args": {
                                "title": title,
                                "description": description,
                                "deadline": int(deadline.timestamp()),
                                "payment_amount": payment_amount,
                                "token_type": token_type,
                                "project_id": st.session_state.get('current_project_id')
                            }
                        }
                        success, result = render_transaction_submitter("add_milestone", tx_data)
                        if success:
                            st.success(f"Milestone added successfully: {result['signature']}")
                            st.rerun()
                    else:
                        st.error("Please fill in all required fields")
        
        # Fund Milestone
        if st.button("Fund Milestone", type="secondary"):
            with st.expander("Fund Milestone Details"):
                milestone_id = st.text_input("Milestone ID")
                amount = st.number_input("Amount", min_value=0.0, step=0.001)
                token_type = st.selectbox("Token Type", ["SOL", "USDT"])
                
                if st.button("Fund Milestone", type="primary"):
                    if milestone_id and amount > 0:
                        tx_data = {
                            "args": {
                                "milestone_id": milestone_id,
                                "amount": amount,
                                "token_type": token_type
                            }
                        }
                        tx_type = "fund_milestone_sol" if token_type == "SOL" else "fund_milestone_usdt"
                        success, result = render_transaction_submitter(tx_type, tx_data)
                        if success:
                            st.success(f"Milestone funded successfully: {result['signature']}")
                            st.rerun()
                    else:
                        st.error("Please fill in all required fields")
        
        # Complete Milestone
        if st.button("Complete Milestone", type="secondary"):
            with st.expander("Complete Milestone Details"):
                milestone_id = st.text_input("Milestone ID")
                
                if st.button("Complete Milestone", type="primary"):
                    if milestone_id:
                        tx_data = {
                            "args": {
                                "milestone_id": milestone_id
                            }
                        }
                        success, result = render_transaction_submitter("complete_milestone", tx_data)
                        if success:
                            st.success(f"Milestone completed successfully: {result['signature']}")
                            st.rerun()
                    else:
                        st.error("Please enter milestone ID")
        
        # Approve Milestone
        if st.button("Approve Milestone", type="secondary"):
            with st.expander("Approve Milestone Details"):
                milestone_id = st.text_input("Milestone ID")
                
                if st.button("Approve Milestone", type="primary"):
                    if milestone_id:
                        tx_data = {
                            "args": {
                                "milestone_id": milestone_id
                            }
                        }
                        success, result = render_transaction_submitter("approve_milestone", tx_data)
                        if success:
                            st.success(f"Milestone approved successfully: {result['signature']}")
                            st.rerun()
                    else:
                        st.error("Please enter milestone ID")
        
        # Distribute Payment
        if st.button("Distribute Payment", type="secondary"):
            with st.expander("Distribute Payment Details"):
                milestone_id = st.text_input("Milestone ID")
                
                if st.button("Distribute Payment", type="primary"):
                    if milestone_id:
                        tx_data = {
                            "args": {
                                "milestone_id": milestone_id
                            }
                        }
                        success, result = render_transaction_submitter("distribute_milestone_payment", tx_data)
                        if success:
                            st.success(f"Payment distributed successfully: {result['signature']}")
                            st.rerun()
                    else:
                        st.error("Please enter milestone ID")
        
        # Display existing projects
        st.markdown("### Existing Projects")
        render_contract_projects()
        
        # Project creation form
        st.markdown("### Create New Project")
        render_project_form()
        
    with tabs[1]:
        st.markdown("### Smart Contract Functions")
        
        # Create grid layout for functions
        col1, col2 = st.columns(2)
        
        # Project Management Functions
        with col1:
            st.markdown("#### Project Management")
            functions = [
                {"name": "initialize_project", "description": "Creates a new collaboration project", "icon": "📁"},
                {"name": "add_participant", "description": "Adds a participant to a project", "icon": "👥"},
                {"name": "add_milestone", "description": "Creates a milestone for the project", "icon": "🎯"}
            ]
            
            for function in functions:
                st.markdown(f"""
                <div style="background-color: #1E1E1E; padding: 12px; border-radius: 6px; margin-bottom: 8px; cursor: pointer;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="color: #14F195; font-size: 1.2rem;">{function["icon"]}</span>
                        <div>
                            <div style="font-family: 'Roboto Mono', monospace; color: #14F195;">{function["name"]}</div>
                            <div style="font-size: 0.9rem; color: #AAAAAA; margin-top: 4px;">{function["description"]}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Payment Functions
        with col2:
            st.markdown("#### Payment Functions")
            functions = [
                {"name": "fund_milestone_sol", "description": "Funds a milestone with SOL", "icon": "💰"},
                {"name": "fund_milestone_usdt", "description": "Funds a milestone with USDT stablecoin", "icon": "💳"},
                {"name": "distribute_milestone_payment", "description": "Distributes payment to participants", "icon": "🔄"}
            ]
            
            for function in functions:
                st.markdown(f"""
                <div style="background-color: #1E1E1E; padding: 12px; border-radius: 6px; margin-bottom: 8px; cursor: pointer;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="color: #14F195; font-size: 1.2rem;">{function["icon"]}</span>
                        <div>
                            <div style="font-family: 'Roboto Mono', monospace; color: #14F195;">{function["name"]}</div>
                            <div style="font-size: 0.9rem; color: #AAAAAA; margin-top: 4px;">{function["description"]}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Milestone Functions
        st.markdown("### Milestone Functions")
        functions = [
            {"name": "complete_milestone", "description": "Marks a milestone as completed", "icon": "✅"},
            {"name": "approve_milestone", "description": "Approves a completed milestone", "icon": "👍"}
        ]
        
        for function in functions:
            st.markdown(f"""
            <div style="background-color: #1E1E1E; padding: 12px; border-radius: 6px; margin-bottom: 8px; cursor: pointer;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="color: #14F195; font-size: 1.2rem;">{function["icon"]}</span>
                    <div>
                        <div style="font-family: 'Roboto Mono', monospace; color: #14F195;">{function["name"]}</div>
                        <div style="font-size: 0.9rem; color: #AAAAAA; margin-top: 4px;">{function["description"]}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Contract Events
        st.markdown("### Contract Events")
        events = [
            {"name": "ProjectCreatedEvent", "time": "2025-04-15 14:32:11", "transaction": "4ztK...xPq9"},
            {"name": "ParticipantAddedEvent", "time": "2025-04-15 15:10:22", "transaction": "7mnR...vFw2"},
            {"name": "MilestoneAddedEvent", "time": "2025-04-16 09:45:17", "transaction": "2kLp...tR8j"}
        ]
        
        for event in events:
            # Generate a valid Solana transaction URL
            tx_hash = event["transaction"].replace("...", "1" * 32)  # Replace with a valid mock hash
            tx_url = f"https://explorer.solana.com/tx/{tx_hash}"
            
            st.markdown(f"""
            <div style="background-color: #1E1E1E; padding: 12px; border-radius: 6px; margin-bottom: 8px; cursor: pointer;"
                 onclick="window.open('{tx_url}', '_blank')">
                <div style="display: flex; justify-content: space-between;">
                    <div style="font-family: 'Roboto Mono', monospace; color: #9945FF;">{event["name"]}</div>
                    <div style="font-size: 0.8rem; color: #AAAAAA;">{event["time"]}</div>
                </div>
                <div style="font-size: 0.9rem; color: #AAAAAA; margin-top: 4px;">
                    Tx: <span class="transaction-hash">{event["transaction"]}</span>
                </div>
                <div style="font-size: 0.8rem; color: #14F195; margin-top: 6px; text-align: right;">View transaction ↗</div>
            </div>
            """, unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown("### Project Milestones")
        
        # Import transaction forms for adding milestones
        from components.transaction_submitter_simplified import render_milestone_submission_form
        
        # Add milestone form
        from utils.database import create_milestone
        
        # Get current project ID from session state or use a default
        project_id = st.session_state.get('current_project_id', 1)
        
        success, result = render_milestone_submission_form(project_id=project_id)
        
        if success:
            # Store the milestone in the database
            if 'data' in result and 'args' in result['data']:
                # Convert Unix timestamp to datetime
                deadline_timestamp = result['data']['args'].get('deadline')
                deadline_date = datetime.fromtimestamp(deadline_timestamp) if deadline_timestamp else None
                
                milestone = create_milestone(
                    project_id=project_id,
                    title=result['data']['args']['title'],
                    description=result['data']['args']['description'],
                    deadline=deadline_date,
                    payment_amount=result['data']['args']['payment_amount'] / 1_000_000 if 'payment_amount' in result['data']['args'] else 0,
                    deliverables=result['data']['args'].get('deliverables'),
                    transaction_signature=result['signature']
                )
            
            st.success(f"Milestone added successfully with transaction signature: {result['signature'][:7]}...{result['signature'][-4:]}")
            st.session_state.show_milestone_confirmation = True
            st.session_state.latest_milestone_tx = result['signature']
        
        st.markdown("<hr style='margin: 20px 0; border-color: #333;'>", unsafe_allow_html=True)
        
        # Display existing milestones from database
        from utils.database import get_milestones
        
        # Get current project ID from session state or use a default
        project_id = st.session_state.get('current_project_id', 1)
        
        # Get milestones from database
        db_milestones = get_milestones(project_id=project_id)
        
        # Process milestones from database
        milestones = []
        if db_milestones:
            for m in db_milestones:
                milestones.append({
                    "id": m['id'],
                    "title": m['title'],
                    "description": m['description'],
                    "deadline": m['deadline'],
                    "payment": f"{m['payment_amount']} {m.get('token_type', 'USDT')}",
                    "status": m['status']
                })
        
        # Add example milestones if none in database
        if not milestones:
            milestones = [
                {
                    "title": "Initial Quantum Algorithm Design",
                    "description": "Develop the theoretical framework for quantum algorithms targeting protein folding predictions",
                    "deadline": "2025-05-23",
                    "payment": "50 USDT",
                    "status": "Funded"
                },
                {
                    "title": "Prototype Implementation",
                    "description": "Implement prototype of quantum algorithm on simulator and analyze performance",
                    "deadline": "2025-06-23",
                    "payment": "1.5 SOL",
                    "status": "Pending"
                }
            ]
        
        # If we just added a new milestone via a transaction, add it to the display list
        if 'show_milestone_confirmation' in st.session_state and st.session_state.show_milestone_confirmation:
            if 'latest_milestone_tx' in st.session_state:
                # Add the new milestone to the top of the list
                if result and 'data' in result and 'args' in result['data']:
                    # Get token type and calculate correct amount based on decimals
                    token_type = result['data']['args'].get('token_type', 'USDT')  # Default to USDT if not specified
                    
                    if token_type == "SOL":
                        payment_display = result['data']['args']['payment_amount'] / 1_000_000_000  # 9 decimals for SOL
                    else:  # USDT or other tokens with 6 decimals
                        payment_display = result['data']['args']['payment_amount'] / 1_000_000  # 6 decimals
                    
                    new_milestone = {
                        "title": result['data']['args']['title'],
                        "description": result['data']['args']['description'],
                        "deadline": datetime.fromtimestamp(result['data']['args']['deadline']).strftime("%Y-%m-%d"),
                        "payment": f"{payment_display} {token_type}",
                        "status": "Pending"
                    }
                    milestones.insert(0, new_milestone)
                
                # Reset confirmation after displaying
                st.session_state.show_milestone_confirmation = False
        
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
                # For funded milestones, allow completing them
                st.button(f"Mark as Completed: {milestone['title']}", key=f"complete_milestone_{i}", 
                         type="secondary", use_container_width=False)
            elif milestone["status"] == "Pending":
                # For pending milestones, allow funding them
                st.button(f"Fund Milestone: {milestone['title']}", key=f"fund_milestone_{i}", 
                         type="primary", use_container_width=False)
    
    with tabs[3]:
        st.markdown("### Project Participants")
        
        # Import transaction form for adding participants
        from components.transaction_submitter_simplified import render_participant_submission_form
        
        # Add participant form
        from utils.database import create_participant
        
        # Get current project ID from session state or use a default
        project_id = st.session_state.get('current_project_id', 1)
        
        success, result = render_participant_submission_form(project_id=project_id)
        
        if success:
            # Store the participant in the database
            if 'data' in result and 'args' in result['data'] and 'accounts' in result['data']:
                participant = create_participant(
                    project_id=project_id,
                    name=result['data']['args']['name'],
                    role=result['data']['args']['role'],
                    wallet_address=result['data']['accounts']['participant'],
                    contribution_percentage=result['data']['args'].get('contribution_percentage', 0),
                    confidential_details=result['data']['args'].get('confidential_details'),
                    transaction_signature=result['signature']
                )
            
            st.success(f"Participant added successfully with transaction signature: {result['signature'][:7]}...{result['signature'][-4:]}")
            st.session_state.show_participant_confirmation = True
            st.session_state.latest_participant_tx = result['signature']
        
        st.markdown("<hr style='margin: 20px 0; border-color: #333;'>", unsafe_allow_html=True)
        
        # Display existing participants from database
        from utils.database import get_participants
        
        # Get current project ID from session state or use a default
        project_id = st.session_state.get('current_project_id', 1)
        
        # Get participants from database
        db_participants = get_participants(project_id=project_id)
        
        # Process participants from database
        participants = []
        if db_participants:
            for p in db_participants:
                # Format wallet address for display
                wallet_display = p['wallet_address']
                if wallet_display and len(wallet_display) > 10:
                    wallet_display = f"{wallet_display[:4]}...{wallet_display[-4:]}"
                
                participants.append({
                    "id": p['id'],
                    "name": p['name'],
                    "role": p['role'],
                    "contribution": f"{p['contribution_percentage']}%",
                    "joined": p['joined_at'].split()[0] if p['joined_at'] else "N/A",
                    "wallet": wallet_display
                })
        
        # Add example participants if none in database
        if not participants:
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
        
        # If we just added a new participant via a transaction, add it to the display list
        if 'show_participant_confirmation' in st.session_state and st.session_state.show_participant_confirmation:
            if 'latest_participant_tx' in st.session_state:
                # Add the new participant to the top of the list
                if result and 'data' in result and 'args' in result['data']:
                    new_participant = {
                        "name": result['data']['args']['name'],
                        "role": result['data']['args']['role'],
                        "contribution": f"{result['data']['args']['contribution_percentage']}%",
                        "joined": datetime.now().strftime("%Y-%m-%d"),
                        "wallet": f"{result['data']['accounts']['participant'][:4]}...{result['data']['accounts']['participant'][-4:]}"
                    }
                    participants.insert(0, new_participant)
                
                # Reset confirmation after displaying
                st.session_state.show_participant_confirmation = False
        
        # Show all participants in cards
        col1, col2 = st.columns(2)
        
        for i, participant in enumerate(participants):
            # Alternate between columns
            with col1 if i % 2 == 0 else col2:
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