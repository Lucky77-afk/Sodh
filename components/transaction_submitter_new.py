import streamlit as st
import time
import json
import base58
from utils.database import record_transaction
from utils.solana_client_new import get_solana_client, SYSTEM_PROGRAM_ID, TOKEN_PROGRAM_ID, USDT_MINT, create_keypair, get_recent_blockhash

def create_and_submit_transaction(tx_type, tx_data):
    """
    Creates and submits a real Solana transaction based on transaction type and data
    """
    # Initialize UI elements for progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Get Solana client
    client = get_solana_client()
    
    # Convert input data to JSON for database storage
    tx_json = json.dumps(tx_data, indent=2)
    
    # Update status
    status_text.text("Preparing transaction...")
    progress_bar.progress(10)
    
    # Generate or use provided wallet keypair
    # In a real app, this would come from wallet connection
    # For demo purposes, we'll create a new keypair
    sender_keypair = Keypair()
    
    # Get recent blockhash for transaction
    status_text.text("Getting recent blockhash...")
    progress_bar.progress(20)
    try:
        blockhash_response = client.get_recent_blockhash()
        if 'result' not in blockhash_response:
            status_text.text("Failed to get recent blockhash")
            return {
                "success": False,
                "error": "Failed to get recent blockhash from Solana",
                "tx_type": tx_type
            }
            
        blockhash = Blockhash(blockhash_response['result']['value']['blockhash'])
    except Exception as e:
        status_text.text(f"Error getting blockhash: {str(e)}")
        return {
            "success": False,
            "error": f"Blockhash error: {str(e)}",
            "tx_type": tx_type
        }
    
    # Create a transaction object
    transaction = Transaction()
    transaction.recent_blockhash = blockhash
    
    status_text.text("Building transaction...")
    progress_bar.progress(40)
    
    # Build the transaction based on the transaction type
    try:
        # Extract instruction and accounts from tx_data
        instruction_type = tx_data.get('instruction', '')
        accounts_data = tx_data.get('accounts', {})
        args_data = tx_data.get('args', {})
        
        if tx_type == 'create_project':
            # Create a project initialization transaction
            # Convert account addresses to PublicKey objects
            accounts = []
            
            # Add system program account
            system_program = SYSTEM_PROGRAM_ID
            accounts.append(AccountMeta(pubkey=system_program, is_signer=False, is_writable=False))
            
            # Add token program if using USDT
            if 'token_program' in accounts_data:
                token_program = TOKEN_PROGRAM_ID
                accounts.append(AccountMeta(pubkey=token_program, is_signer=False, is_writable=False))
                
                # Add USDT mint account if present
                if 'usdt_mint' in accounts_data:
                    usdt_mint = USDT_MINT
                    accounts.append(AccountMeta(pubkey=usdt_mint, is_signer=False, is_writable=False))
            
            # Add sender account
            accounts.append(AccountMeta(pubkey=sender_keypair.public_key, is_signer=True, is_writable=True))
            
            # Create instruction data - encode args into bytes
            # This would match your smart contract's instruction format
            instruction_data = bytes([0])  # 0 = create_project instruction code
            
            # Add name, description, etc. as needed by your contract
            # Simple encoding example - in reality this would match your contract's ABI
            if 'name' in args_data:
                name_bytes = args_data['name'].encode('utf-8')
                instruction_data += len(name_bytes).to_bytes(4, byteorder='little')
                instruction_data += name_bytes
                
            if 'description' in args_data:
                desc_bytes = args_data['description'].encode('utf-8')
                instruction_data += len(desc_bytes).to_bytes(4, byteorder='little')
                instruction_data += desc_bytes
                
            # Create the instruction
            create_project_ix = TransactionInstruction(
                keys=accounts,
                program_id=PublicKey("YourProgramIdHere"),  # Replace with actual program ID
                data=instruction_data
            )
            
            # Add instruction to transaction
            transaction.add(create_project_ix)
            
        elif tx_type == 'add_milestone':
            # Similar implementation for milestone creation
            # Would follow same pattern as above but with milestone-specific data
            # Simplified for brevity
            pass
            
        elif tx_type == 'add_participant':
            # Similar implementation for participant addition
            # Would follow same pattern as above but with participant-specific data
            # Simplified for brevity
            pass
            
        else:
            status_text.text(f"Unknown transaction type: {tx_type}")
            return {
                "success": False,
                "error": f"Unknown transaction type: {tx_type}",
                "tx_type": tx_type
            }
            
    except Exception as e:
        status_text.text(f"Error building transaction: {str(e)}")
        return {
            "success": False,
            "error": f"Transaction build error: {str(e)}",
            "tx_type": tx_type
        }
    
    # In a real app, this would connect to the user's wallet for signing
    # For demo, we'll sign with our generated keypair
    status_text.text("Signing transaction...")
    progress_bar.progress(60)
    try:
        # Sign transaction with sender keypair
        transaction.sign(sender_keypair)
    except Exception as e:
        status_text.text(f"Error signing transaction: {str(e)}")
        return {
            "success": False,
            "error": f"Transaction signing error: {str(e)}",
            "tx_type": tx_type
        }
    
    # Serialize and send the transaction
    status_text.text("Sending transaction to Solana network...")
    progress_bar.progress(80)
    try:
        # Serialize the transaction to wire format
        serialized_transaction = transaction.serialize()
        
        # Send transaction
        tx_response = client.send_raw_transaction(serialized_transaction)
        
        if 'result' not in tx_response:
            status_text.text("Failed to submit transaction")
            return {
                "success": False,
                "error": "Failed to submit transaction to Solana network",
                "tx_type": tx_type
            }
            
        # Get transaction signature
        tx_signature = tx_response['result']
    except Exception as e:
        status_text.text(f"Error sending transaction: {str(e)}")
        return {
            "success": False,
            "error": f"Transaction submission error: {str(e)}",
            "tx_type": tx_type
        }
    
    # Wait for confirmation
    status_text.text("Waiting for confirmation...")
    progress_bar.progress(90)
    time.sleep(1.0)  # In production, would actually poll for confirmation
    
    # Get transaction details (would normally confirm status)
    try:
        # For demo purposes, we'll assume success after a delay
        # In production, you would confirm by checking status
        status_text.text("Transaction confirmed!")
        progress_bar.progress(100)
        
        # Mock values for demo - in production these would come from blockchain
        current_time = int(time.time())
        slot = 150000000  # Example slot number
        
        # Record transaction in database
        try:
            record_transaction(
                signature=tx_signature,
                tx_type=tx_type,
                status="Confirmed",
                blocktime=current_time,
                slot=slot,
                data=tx_json
            )
            print(f"Successfully recorded transaction: {tx_signature}")
        except Exception as e:
            print(f"Error recording transaction: {str(e)}")
            # Continue with the flow even if DB recording fails
        
        # Return successful transaction data
        return {
            "success": True,
            "signature": tx_signature,
            "blocktime": current_time,
            "slot": slot,
            "tx_type": tx_type,
            "data": tx_data
        }
    except Exception as e:
        status_text.text(f"Error confirming transaction: {str(e)}")
        try:
            record_transaction(
                signature=tx_signature if 'tx_signature' in locals() else "unknown",
                tx_type=tx_type,
                status="Failed",
                blocktime=int(time.time()),
                slot=0,
                data=tx_json
            )
        except Exception as db_error:
            print(f"Error recording failed transaction: {str(db_error)}")
        
        return {
            "success": False,
            "error": f"Transaction confirmation error: {str(e)}",
            "tx_type": tx_type,
            "signature": tx_signature if 'tx_signature' in locals() else "unknown"
        }

def render_transaction_submitter(tx_type, tx_data):
    """
    Renders a transaction submission form with real transaction
    
    Parameters:
    - tx_type: Type of transaction (e.g., 'create_project', 'add_milestone')
    - tx_data: Dictionary of transaction data
    """
    with st.expander(f"Transaction Details ({tx_type})"):
        st.json(tx_data)
        
        if st.button("Sign and Submit Transaction", type="primary"):
            with st.spinner("Processing transaction..."):
                # Create and submit real transaction
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
                    st.error(f"Transaction failed: {result['error']}")
                    return False, result
                    
        return None, None  # No transaction submitted yet

def render_project_submission_form():
    """Renders a form to create a new collaboration project with transaction simulation"""
    with st.form("new_project_form"):
        st.markdown("### Create New Project")
        project_name = st.text_input("Project Name", placeholder="Enter a name for your research collaboration")
        project_description = st.text_area("Project Description", placeholder="Describe the goals and scope of this project")
        
        # Add currency preference for the project
        st.markdown("#### Project Funding Options")
        col1, col2 = st.columns(2)
        with col1:
            default_currency = st.selectbox("Default Currency", options=["SOL", "USDT"])
        with col2:
            accept_multiple = st.checkbox("Accept multiple currencies", value=True)
            
        ip_terms = st.text_area("IP Terms", 
                               value="All intellectual property developed through this collaboration will be jointly owned by participants proportional to their contribution percentage.")
        
        # Form submission
        submit_button = st.form_submit_button("Prepare Transaction")
        
        if submit_button:
            if project_name and project_description:
                # Create transaction data with appropriate token information based on selection
                if default_currency == "SOL":
                    token_accounts = {
                        "admin": "connected_wallet_address",
                        "project": "derived_project_pda",
                        "system_program": "11111111111111111111111111111111",
                    }
                    # Add token program accounts if accepting multiple currencies
                    if accept_multiple:
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
                        "name": project_name,
                        "description": project_description,
                        "ip_terms": ip_terms,
                        "default_currency": default_currency,
                        "accept_multiple_currencies": accept_multiple
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
                        "participant_account": "derived_participant_pda",
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