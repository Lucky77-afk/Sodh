import streamlit as st
import pandas as pd
from datetime import datetime
from utils.solana_client import get_solana_client, get_recent_transactions, get_transaction_details

def format_timestamp(timestamp):
    """Format timestamp from different formats to human-readable"""
    if not timestamp:
        return "Unknown"
    try:
        if isinstance(timestamp, (int, float)):
            # Handle Unix timestamp
            return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(timestamp, str):
            # Try to parse if it's a string timestamp
            try:
                return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                return timestamp
        return str(timestamp)
    except Exception:
        return str(timestamp)

def render_transaction_card(tx):
    """Renders a transaction card with details"""
    # Handle both dict and object access
    if hasattr(tx, 'get'):
        signature = tx.get('signature', 'Unknown')
        status = tx.get('status', 'Unknown')
        block_time = tx.get('block_time', tx.get('blockTime', 'Unknown'))
        fee = tx.get('fee', 0)
    else:
        signature = getattr(tx, 'signature', 'Unknown')
        status = getattr(tx, 'status', 'Unknown')
        block_time = getattr(tx, 'block_time', getattr(tx, 'blockTime', 'Unknown'))
        fee = getattr(tx, 'fee', 0)
    
    # Format the signature if it's a full signature
    if isinstance(signature, str) and len(signature) > 16:
        signature_display = f"{signature[:8]}...{signature[-8:]}"
    else:
        signature_display = str(signature)
    
    # Format the block time
    formatted_time = format_timestamp(block_time)
    
    # Format fee if it's a number
    try:
        fee = float(fee) if fee is not None else 0
        fee_display = f"{fee:.9f} SOL"
    except (TypeError, ValueError):
        fee_display = f"{fee} SOL"
    
    # Format the card
    st.markdown(f"""
    <div class="transaction-row">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div class="transaction-hash">{signature_display}</div>
                <div style="font-size: 0.8rem; color: #AAAAAA;">{formatted_time}</div>
            </div>
            <div>
                <span style="color: {'#14F195' if str(status).lower() == 'success' else '#FF5C5C'}; font-size: 0.9rem;">
                    {status}
                </span>
            </div>
        </div>
        <div style="margin-top: 8px; display: flex; justify-content: space-between;">
            <div style="font-size: 0.8rem; color: #AAAAAA;">Fee: {fee_display}</div>
            <div>
                <a href="https://explorer.solana.com/tx/{signature}" target="_blank" style="color: #9945FF; text-decoration: none; font-size: 0.8rem;">
                    View on Solana Explorer
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_transactions():
    """Renders the transactions page with search and list of recent transactions"""
    st.markdown('<h2>Transaction Explorer</h2>', unsafe_allow_html=True)
    
    # Add search box
    tx_search = st.text_input("Search by transaction signature", placeholder="Enter transaction signature...")
    
    # If search is performed
    if tx_search:
        st.markdown("### Transaction Details")
        try:
            client = get_solana_client()
            tx_details = get_transaction_details(client, tx_search)
            
            if tx_details:
                # Status indicator - handle both dict and object access
                meta = tx_details.get('meta', {}) if hasattr(tx_details, 'get') else {}
                status = "Success" if (hasattr(meta, 'err') and meta.err is None) or (hasattr(meta, 'get') and meta.get('err') is None) else "Failed"
                status_color = "#14F195" if status == "Success" else "#FF5C5C"
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="stCard">
                        <div style="font-size: 0.9rem; color: #AAA;">STATUS</div>
                        <div style="font-size: 1.2rem; color: {status_color};">{status}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    block_time = getattr(tx_details, 'blockTime', 0) if hasattr(tx_details, 'blockTime') else tx_details.get('blockTime', 0)
                    formatted_time = format_timestamp(block_time)
                    st.markdown(f"""
                    <div class="stCard">
                        <div style="font-size: 0.9rem; color: #AAA;">TIMESTAMP</div>
                        <div style="font-size: 1.2rem; color: #FFFFFF;">{formatted_time}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    slot = getattr(tx_details, 'slot', 'Unknown') if hasattr(tx_details, 'slot') else tx_details.get('slot', 'Unknown')
                    st.markdown(f"""
                    <div class="stCard">
                        <div style="font-size: 0.9rem; color: #AAA;">SLOT</div>
                        <div style="font-size: 1.2rem; color: #FFFFFF;">{slot}</div>
                    </div>
                    """, unsafe_include_html=True)
                
                # Transaction signature
                st.markdown("#### Signature")
                st.code(tx_search, language="text")
                
                # Fee - handle both dict and object access
                try:
                    meta = tx_details.get('meta', {}) if hasattr(tx_details, 'get') else {}
                    fee_lamports = getattr(meta, 'fee', 0) if hasattr(meta, 'fee') else meta.get('fee', 0)
                    fee = float(fee_lamports) / 1_000_000_000  # Convert lamports to SOL
                    st.markdown(f"#### Fee: {fee:.9f} SOL")
                except (TypeError, AttributeError) as e:
                    st.warning(f"Could not determine transaction fee: {str(e)}")
                
                # Instructions
                st.markdown("#### Instructions")
                try:
                    # Handle both dict and object access patterns
                    transaction = tx_details.get('transaction', {}) if hasattr(tx_details, 'get') else {}
                    message = transaction.get('message', {}) if hasattr(transaction, 'get') else {}
                    instructions = message.get('instructions', []) if hasattr(message, 'get') else []
                    
                    if not instructions and hasattr(message, 'instructions'):
                        instructions = message.instructions
                    
                    if instructions:
                        for i, instruction in enumerate(instructions):
                            with st.expander(f"Instruction {i+1}"):
                                # Convert to dict if it's an object
                                if hasattr(instruction, '__dict__'):
                                    instruction = instruction.__dict__
                                st.json(instruction)
                    else:
                        st.info("No instruction data available")
                except Exception as e:
                    st.error(f"Error displaying instructions: {str(e)}")
                
                # Log messages
                try:
                    meta = tx_details.get('meta', {}) if hasattr(tx_details, 'get') else {}
                    log_messages = getattr(meta, 'logMessages', []) if hasattr(meta, 'logMessages') else meta.get('logMessages', [])
                    
                    if log_messages:
                        with st.expander("Log Messages"):
                            for msg in log_messages:
                                st.text(msg)
                except Exception as e:
                    st.error(f"Error displaying log messages: {str(e)}")
            else:
                st.warning("Transaction not found")
        except Exception as e:
            st.error(f"Error retrieving transaction details: {str(e)}")
    
    # Recent transactions section
    st.markdown("### Recent Transactions")
    
    # Try to get transactions from database first
    from utils.database import get_recent_transactions as get_db_transactions
    
    try:
        # Get database transactions
        db_txs = get_db_transactions(limit=10)
        
        if db_txs:
            # Format database transactions to match expected format
            for tx in db_txs:
                # Convert Unix timestamp to datetime if available
                block_time = "Unknown"
                if tx.get("blocktime"):
                    from datetime import datetime
                    block_time = datetime.fromtimestamp(tx["blocktime"]).strftime("%Y-%m-%d %H:%M:%S")
                elif tx.get("created_at"):
                    block_time = tx["created_at"]
                
                # Create a transaction object with the required fields
                tx_obj = {
                    "signature": tx["signature"],
                    "status": "Success" if tx["status"] == "Confirmed" else "Failed",
                    "block_time": block_time,
                    "fee": "0.000005"  # Default fee
                }
                render_transaction_card(tx_obj)
        else:
            # Fallback to Solana blockchain transactions if no database transactions
            try:
                client = get_solana_client()
                recent_txs = get_recent_transactions(_client=client)
                
                if recent_txs:
                    for tx in recent_txs:
                        render_transaction_card(tx)
                else:
                    st.info("No recent transactions found")
            except Exception as e:
                st.error(f"Error retrieving recent transactions from blockchain: {str(e)}")
    except Exception as e:
        st.error(f"Error retrieving recent transactions: {str(e)}")
        
# No need for datetime import as it's now at the top
