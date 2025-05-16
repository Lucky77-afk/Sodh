import streamlit as st
import time
import json
from utils.database import record_transaction
from utils.solana_client_new import get_solana_client

def create_and_submit_transaction(tx_type, tx_data):
    """
    Creates and submits a real Solana transaction based on transaction type and data
    """
    try:
        # Initialize UI elements for progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Get Solana client
        client = get_solana_client()
        
        # Convert input data to JSON for database storage
        tx_json = json.dumps(tx_data, indent=2)
        
        # Update status
        status_text.text("Preparing transaction...")
        progress_bar.progress(20)
        
        # Create transaction based on type
        if tx_type == "initialize_project":
            # Create project initialization transaction
            from solders.instruction import Instruction
            from solders.keypair import Keypair
            from solders.pubkey import Pubkey
            from solders.system_program import CreateAccountParams, create_account
            from solders.transaction import Transaction
            
            # Generate project PDA
            project_pda = Pubkey.find_program_address(
                [b"project", bytes(tx_data["args"]["name"], "utf-8")],
                Pubkey.from_string("YourProgramAddressHere")
            )[0]
            
            # Create account instruction
            create_acc_ix = create_account(
                CreateAccountParams(
                    from_pubkey=st.session_state.connected_wallet,
                    to_pubkey=project_pda,
                    lamports=1000000000,  # 1 SOL
                    space=8 + 256 + 256 + 1024,  # Account data size
                    owner=Pubkey.from_string("YourProgramAddressHere")
                )
            )
            
            # Initialize project instruction
            init_ix = Instruction(
                program_id=Pubkey.from_string("YourProgramAddressHere"),
                data=bytes([0]),  # Instruction discriminator
                accounts=[
                    {"pubkey": st.session_state.connected_wallet, "is_signer": True, "is_writable": False},
                    {"pubkey": project_pda, "is_signer": False, "is_writable": True},
                    {"pubkey": Pubkey.from_string("11111111111111111111111111111111"), "is_signer": False, "is_writable": False},
                ]
            )
            
            # Create and send transaction
            tx = Transaction().add(create_acc_ix).add(init_ix)
            response = client.send_transaction(tx)
            
            # Extract signature
            tx_signature = response.value
            
            # Record transaction in database
            record_transaction(
                signature=tx_signature,
                tx_type=tx_type,
                status="Confirmed",
                blocktime=int(time.time()),
                slot=response.context.slot,
                data=tx_json
            )
            
            return {
                "success": True,
                "signature": tx_signature,
                "blocktime": int(time.time()),
                "slot": response.context.slot,
                "tx_type": tx_type,
                "data": tx_data
            }
        
        # Add other transaction types here
        elif tx_type == "add_participant":
            # Implement participant addition
            pass
        elif tx_type == "add_milestone":
            # Implement milestone addition
            pass
        elif tx_type == "fund_milestone_sol":
            # Implement SOL funding
            pass
        elif tx_type == "fund_milestone_usdt":
            # Implement USDT funding
            pass
        elif tx_type == "complete_milestone":
            # Implement milestone completion
            pass
        elif tx_type == "approve_milestone":
            # Implement milestone approval
            pass
        elif tx_type == "distribute_milestone_payment":
            # Implement payment distribution
            pass
            
        return {
            "success": False,
            "error": f"Unsupported transaction type: {tx_type}"
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def render_transaction_submitter(tx_type, tx_data):
    """
    Renders a transaction submission form with transaction simulation
    
    Parameters:
    - tx_type: Type of transaction (e.g., 'create_project', 'add_milestone')
    - tx_data: Dictionary of transaction data
    """
    with st.expander(f"Transaction Details ({tx_type})"):
        st.json(tx_data)
        
        # Use a unique key for the button to avoid conflicts
        if st.button("Sign and Submit Transaction", 
                    type="primary",
                    key=f"submit_{tx_type}_{hash(str(tx_data))}"):
            with st.spinner("Processing transaction..."):
                # Create and submit transaction
                result = create_and_submit_transaction(tx_type, tx_data)
                
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
                    st.error(f"Transaction failed: {result.get('error', 'Unknown error')}")
                    return False, result
                    
        return None, None  # No transaction submitted yet

def render_project_submission_form():
    """Renders a form to create a new collaboration project with transaction simulation"""
    st.markdown("### Create New Project")
    
    # Use session state to track form submission
    if 'project_form_submitted' not in st.session_state:
        st.session_state.project_form_submitted = False
    
    # Use columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        project_name = st.text_input("Project Name", 
                                   placeholder="Enter a name for your research collaboration",
                                   key="project_name")
    
    # Project description takes full width
    project_description = st.text_area("Project Description", 
                                     placeholder="Describe the goals and scope of this project",
                                     key="project_description")
    
    # Add currency preference for the project
    st.markdown("#### Project Funding Options")
    col1, col2 = st.columns(2)
    with col1:
        default_currency = st.selectbox("Default Currency", 
                                      options=["SOL", "USDT"],
                                      key="default_currency")
    with col2:
        accept_multiple = st.checkbox("Accept multiple currencies", 
                                    value=True,
                                    key="accept_multiple")
        
    ip_terms = st.text_area("IP Terms", 
                         value="All intellectual property developed through this collaboration will be jointly owned by participants proportional to their contribution percentage.",
                         key="ip_terms")
    
    # Submit button outside of form
    if st.button("Prepare Transaction", type="primary"):
        if not st.session_state.project_name or not st.session_state.project_description:
            st.error("Please fill in all required fields")
            return None, None
            
        st.session_state.project_form_submitted = True
        
    # Process form submission
    if st.session_state.project_form_submitted:
        # Create transaction data with appropriate token information based on selection
        if st.session_state.default_currency == "SOL":
            token_accounts = {
                "admin": "connected_wallet_address",
                "project": "derived_project_pda",
                "system_program": "11111111111111111111111111111111",
            }
            # Add token program accounts if accepting multiple currencies
            if st.session_state.accept_multiple:
                token_accounts.update({
                    "usdt_mint": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",  # USDT on Solana
                    "token_program": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
                })
        else:  # USDT is default
            token_accounts = {
                "admin": "connected_wallet_address",
                "project": "derived_project_pda",
                "usdt_mint": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",  # USDT on Solana
                "escrow_account": "derived_escrow_pda",
                "token_program": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
                "system_program": "11111111111111111111111111111111",
            }
        
        # Create transaction data
        tx_data = {
            "instruction": "initialize_project",
            "accounts": token_accounts,
            "args": {
                "name": st.session_state.project_name,
                "description": st.session_state.project_description,
                "ip_terms": st.session_state.ip_terms,
                "default_currency": st.session_state.default_currency,
                "accept_multiple_currencies": st.session_state.accept_multiple
            }
        }
        
        # Render the transaction submitter
        result = render_transaction_submitter("create_project", tx_data)
        
        # Reset form state if transaction was submitted
        if result[0] is not None:
            st.session_state.project_form_submitted = False
            return result
    
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
            # Currency selection
            currency = st.selectbox("Currency", options=["SOL", "USDT"])
            
            # Use a numeric input for the payment amount
            if currency == "SOL":
                payment_amount = st.number_input(f"Payment Amount ({currency})", min_value=0.1, value=1.0, step=0.1)
                # SOL has 9 decimals
                decimal_multiplier = 1_000_000_000
            else:  # USDT
                payment_amount = st.number_input(f"Payment Amount ({currency})", min_value=1, value=50)
                # USDT has 6 decimals
                decimal_multiplier = 1_000_000
        
        deliverables = st.text_area("Deliverables", placeholder="List the specific outputs expected for this milestone")
        
        # Form submission
        submit_button = st.form_submit_button("Prepare Transaction")
        
        if submit_button:
            if milestone_title and milestone_description and deliverables:
                # Convert deadline to Unix timestamp
                import datetime
                deadline_datetime = datetime.datetime.combine(deadline_date, datetime.datetime.min.time())
                deadline_timestamp = int(deadline_datetime.timestamp())
                
                # Convert payment to proper units (using decimal_multiplier)
                payment_amount_units = int(payment_amount * decimal_multiplier)
                
                # Create transaction data based on selected currency
                if currency == "SOL":
                    # SOL transaction data
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
                            "token_type": "SOL",
                            "deliverables": deliverables
                        }
                    }
                else:
                    # USDT transaction data (add SPL token program accounts)
                    tx_data = {
                        "instruction": "add_milestone",
                        "accounts": {
                            "admin": "connected_wallet_address",
                            "project": project_id,
                            "milestone_account": "derived_milestone_pda",
                            "usdt_mint": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",  # USDT on Solana
                            "token_program": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
                            "system_program": "11111111111111111111111111111111",
                        },
                        "args": {
                            "title": milestone_title,
                            "description": milestone_description,
                            "deadline": deadline_timestamp,
                            "payment_amount": payment_amount_units,
                            "token_type": "USDT",
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
                        "system_program": "11111111111111111111111111111111",
                    },
                    "args": {
                        "name": participant_name,
                        "role": participant_role,
                        "wallet_address": wallet_address,
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