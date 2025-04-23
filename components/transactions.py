import streamlit as st
import pandas as pd
from utils.solana_client import get_solana_client, get_recent_transactions, get_transaction_details

def render_transaction_card(tx):
    """Renders a transaction card with details"""
    signature = tx.get('signature', 'Unknown')
    status = tx.get('status', 'Unknown')
    status_class = "success" if status == "Success" else "error"
    block_time = tx.get('block_time', 'Unknown')
    fee = tx.get('fee', 0)
    
    # Format the card
    st.markdown(f"""
    <div class="transaction-row">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div class="transaction-hash">{signature[:16]}...{signature[-8:]}</div>
                <div style="font-size: 0.8rem; color: #AAAAAA;">{block_time}</div>
            </div>
            <div>
                <span style="color: {'#14F195' if status == 'Success' else '#FF5C5C'}; font-size: 0.9rem;">
                    {status}
                </span>
            </div>
        </div>
        <div style="margin-top: 8px; display: flex; justify-content: space-between;">
            <div style="font-size: 0.8rem; color: #AAAAAA;">Fee: {fee} SOL</div>
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
                # Status indicator
                status = "Success" if tx_details.get("meta", {}).get("err") is None else "Failed"
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
                    block_time = datetime.fromtimestamp(tx_details.get("blockTime", 0)).strftime("%Y-%m-%d %H:%M:%S") if tx_details.get("blockTime") else "Unknown"
                    st.markdown(f"""
                    <div class="stCard">
                        <div style="font-size: 0.9rem; color: #AAA;">TIMESTAMP</div>
                        <div style="font-size: 1.2rem; color: #FFFFFF;">{block_time}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    slot = tx_details.get("slot", "Unknown")
                    st.markdown(f"""
                    <div class="stCard">
                        <div style="font-size: 0.9rem; color: #AAA;">SLOT</div>
                        <div style="font-size: 1.2rem; color: #FFFFFF;">{slot}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Transaction signature
                st.markdown("#### Signature")
                st.code(tx_search, language="text")
                
                # Fee
                fee = tx_details.get("meta", {}).get("fee", 0) / 1_000_000_000  # Convert lamports to SOL
                st.markdown(f"#### Fee: {fee:.9f} SOL")
                
                # Instructions
                st.markdown("#### Instructions")
                instructions = tx_details.get("transaction", {}).get("message", {}).get("instructions", [])
                if instructions:
                    for i, instruction in enumerate(instructions):
                        with st.expander(f"Instruction {i+1}"):
                            st.json(instruction)
                
                # Log messages
                log_messages = tx_details.get("meta", {}).get("logMessages", [])
                if log_messages:
                    with st.expander("Log Messages"):
                        for msg in log_messages:
                            st.text(msg)
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
                recent_txs = get_recent_transactions(client)
                
                if recent_txs:
                    for tx in recent_txs:
                        render_transaction_card(tx)
                else:
                    st.info("No recent transactions found")
            except Exception as e:
                st.error(f"Error retrieving recent transactions from blockchain: {str(e)}")
    except Exception as e:
        st.error(f"Error retrieving recent transactions: {str(e)}")
        
    # Add import for datetime if search is used
    from datetime import datetime
