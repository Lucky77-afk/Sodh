import streamlit as st
import time
import random
import json

def simulate_transaction(tx_type, tx_data):
    """
    Simulates a Solana transaction and returns mock information
    In a real implementation, this would actually submit to the blockchain
    """
    # Generate a random transaction signature (mock)
    sig_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    tx_signature = ''.join(random.choice(sig_chars) for _ in range(87))
    
    # Convert input data to JSON
    tx_json = json.dumps(tx_data, indent=2)
    
    # Simulate transaction processing time
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("Preparing transaction...")
    progress_bar.progress(10)
    time.sleep(0.5)
    
    status_text.text("Connecting to wallet...")
    progress_bar.progress(30)
    time.sleep(0.7)
    
    status_text.text("Sending transaction to Solana network...")
    progress_bar.progress(50)
    time.sleep(0.8)
    
    status_text.text("Waiting for confirmation...")
    progress_bar.progress(80)
    time.sleep(1.0)
    
    # Simulate random success with high probability
    success = random.random() < 0.95
    
    if success:
        status_text.text("Transaction confirmed!")
        progress_bar.progress(100)
        
        # Return successful transaction data
        return {
            "success": True,
            "signature": tx_signature,
            "blocktime": int(time.time()),
            "slot": random.randint(150000000, 160000000),
            "tx_type": tx_type,
            "data": tx_data
        }
    else:
        status_text.text("Transaction failed.")
        
        # Return failure data
        return {
            "success": False,
            "error": "Transaction simulation error: Insufficient funds for transaction",
            "tx_type": tx_type
        }

def render_transaction_submitter(tx_type, tx_data):
    """
    Renders a transaction submission form with simulation
    
    Parameters:
    - tx_type: Type of transaction (e.g., 'create_project', 'add_milestone')
    - tx_data: Dictionary of transaction data
    """
    with st.expander(f"Transaction Details ({tx_type})"):
        st.json(tx_data)
        
        if st.button("Sign and Submit Transaction", type="primary"):
            with st.spinner("Processing transaction..."):
                # Simulate transaction
                result = simulate_transaction(tx_type, tx_data)
                
                if result["success"]:
                    st.success("Transaction successful!")
                    
                    # Display transaction details
                    st.markdown(f"""
                    <div style="background-color: #1E1E1E; padding: 15px; border-radius: 10px; margin: 15px 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <span style="color: #AAA;">Transaction Signature:</span>
                            <span class="transaction-hash">{result["signature"][:20]}...{result["signature"][-8:]}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <span style="color: #AAA;">Block Time:</span>
                            <span style="color: #FFFFFF;">{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result["blocktime"]))}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <span style="color: #AAA;">Slot:</span>
                            <span style="color: #FFFFFF;">{result["slot"]}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <span style="color: #AAA;">Type:</span>
                            <span style="color: #14F195;">{result["tx_type"]}</span>
                        </div>
                        <div style="text-align: center; margin-top: 15px;">
                            <a href="javascript:void(0)" style="color: #9945FF; text-decoration: none;">
                                View on Solana Explorer
                            </a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    return True, result
                else:
                    st.error(f"Transaction failed: {result['error']}")
                    return False, result
                    
        return None, None  # No transaction submitted yet

def render_project_submission_form():
    """Renders a form to create a new collaboration project with transaction simulation"""
    with st.form("new_project_form"):
        st.markdown("### Create New Project")
        project_name = st.text_input("Project Name", placeholder="Enter a name for your research collaboration")
        project_description = st.text_area("Project Description", placeholder="Describe the goals and scope of this project")
        ip_terms = st.text_area("IP Terms", 
                                 value="All intellectual property developed through this collaboration will be jointly owned by participants proportional to their contribution percentage.")
        
        # Form submission
        submit_button = st.form_submit_button("Prepare Transaction")
        
        if submit_button:
            if project_name and project_description:
                # Create transaction data
                tx_data = {
                    "instruction": "initialize_project",
                    "accounts": {
                        "admin": "connected_wallet_address",
                        "project": "derived_project_pda",
                        "usdc_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC on Solana
                        "escrow_account": "derived_escrow_pda",
                        "token_program": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
                        "system_program": "11111111111111111111111111111111",
                    },
                    "args": {
                        "name": project_name,
                        "description": project_description,
                        "ip_terms": ip_terms
                    }
                }
                
                # Render the transaction submitter
                return render_transaction_submitter("create_project", tx_data)
            else:
                st.error("Please fill in all required fields")
                return None, None
        
        return None, None  # No submission attempted

def render_milestone_submission_form(project_id="Proj1"):
    """Renders a form to create a new milestone with transaction simulation"""
    with st.form("new_milestone_form"):
        st.markdown("### Add Project Milestone")
        milestone_title = st.text_input("Milestone Title", placeholder="Enter a title for this milestone")
        milestone_description = st.text_area("Description", placeholder="Describe what needs to be accomplished")
        
        col1, col2 = st.columns(2)
        with col1:
            # Use a date input for the deadline
            deadline_date = st.date_input("Deadline Date")
        with col2:
            # Use a numeric input for the payment amount
            payment_amount = st.number_input("Payment Amount (USDC)", min_value=1, value=50)
        
        deliverables = st.text_area("Deliverables", placeholder="List the specific outputs expected for this milestone")
        
        # Form submission
        submit_button = st.form_submit_button("Prepare Transaction")
        
        if submit_button:
            if milestone_title and milestone_description and deliverables:
                # Convert deadline to Unix timestamp
                import datetime
                deadline_datetime = datetime.datetime.combine(deadline_date, datetime.time())
                deadline_timestamp = int(deadline_datetime.timestamp())
                
                # Convert payment to proper units (USDC has 6 decimals)
                payment_amount_units = payment_amount * 1_000_000  # Convert to USDC's smallest unit
                
                # Create transaction data
                tx_data = {
                    "instruction": "add_milestone",
                    "accounts": {
                        "admin": "connected_wallet_address",
                        "project": project_id,
                        "milestone_account": "derived_milestone_pda",
                        "system_program": "11111111111111111111111111111111",
                    },
                    "args": {
                        "title": milestone_title,
                        "description": milestone_description,
                        "deadline": deadline_timestamp,
                        "payment_amount": payment_amount_units,
                        "deliverables": deliverables
                    }
                }
                
                # Render the transaction submitter
                return render_transaction_submitter("add_milestone", tx_data)
            else:
                st.error("Please fill in all required fields")
                return None, None
        
        return None, None  # No submission attempted

def render_participant_submission_form(project_id="Proj1"):
    """Renders a form to add a participant with transaction simulation"""
    with st.form("new_participant_form"):
        st.markdown("### Add Project Participant")
        participant_name = st.text_input("Name", placeholder="Enter participant's name")
        participant_role = st.text_input("Role", placeholder="Enter participant's role in the project")
        
        contribution_percentage = st.slider("Contribution Percentage", min_value=1, max_value=100, value=25, 
                                           help="Percentage of work contribution and payment allocation")
        
        wallet_address = st.text_input("Wallet Address", placeholder="Enter participant's Solana wallet address")
        confidential_details = st.text_area("Confidential Details (Optional)", 
                                           placeholder="Additional confidential information (will be encrypted)")
        
        # Form submission
        submit_button = st.form_submit_button("Prepare Transaction")
        
        if submit_button:
            if participant_name and participant_role and wallet_address:
                # Create transaction data
                tx_data = {
                    "instruction": "add_participant",
                    "accounts": {
                        "admin": "connected_wallet_address",
                        "project": project_id,
                        "participant": wallet_address,
                        "participant_account": "derived_participant_pda",
                        "system_program": "11111111111111111111111111111111",
                    },
                    "args": {
                        "name": participant_name,
                        "role": participant_role,
                        "contribution_percentage": contribution_percentage,
                        "confidential_details": confidential_details if confidential_details else ""
                    }
                }
                
                # Render the transaction submitter
                return render_transaction_submitter("add_participant", tx_data)
            else:
                st.error("Please fill in all required fields")
                return None, None
        
        return None, None  # No submission attempted