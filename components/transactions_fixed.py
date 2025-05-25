import streamlit as st
import pandas as pd
import requests
import json
import os
from datetime import datetime

def make_rpc_call(method, params):
    """Make direct RPC calls to avoid library parsing issues"""
    helius_api_key = os.environ.get('HELIUS_API_KEY')
    if helius_api_key:
        rpc_url = f"https://mainnet.helius-rpc.com/?api-key={helius_api_key}"
    else:
        rpc_url = "https://api.mainnet-beta.solana.com"
    
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params
    }
    
    try:
        response = requests.post(rpc_url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"RPC call failed: {str(e)}")
        return None

def get_recent_transactions_safe(limit=10):
    """Get recent transactions using safe RPC calls"""
    try:
        # Get current slot
        slot_result = make_rpc_call("getSlot", [])
        if not slot_result or 'result' not in slot_result:
            return []
        
        current_slot = slot_result['result']
        transactions = []
        
        # Get recent blocks and their transactions
        for i in range(min(5, limit)):  # Check last 5 blocks
            slot = current_slot - i
            block_result = make_rpc_call("getBlock", [slot, {"encoding": "json", "transactionDetails": "signatures"}])
            
            if block_result and 'result' in block_result and block_result['result']:
                block_data = block_result['result']
                block_time = block_data.get('blockTime')
                
                # Get first few transaction signatures from this block
                signatures = block_data.get('signatures', [])[:2]  # Limit to 2 per block
                
                for sig in signatures:
                    tx_info = {
                        'signature': sig,
                        'slot': slot,
                        'block_time': block_time,
                        'status': 'Success'  # Assume success for signatures in confirmed blocks
                    }
                    transactions.append(tx_info)
                    
                    if len(transactions) >= limit:
                        break
            
            if len(transactions) >= limit:
                break
        
        return transactions[:limit]
        
    except Exception as e:
        st.error(f"Error fetching transactions: {str(e)}")
        return []

def get_transaction_details_safe(signature):
    """Get transaction details using safe RPC calls"""
    try:
        tx_result = make_rpc_call("getTransaction", [
            signature,
            {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}
        ])
        
        if not tx_result or 'result' not in tx_result or not tx_result['result']:
            return None
        
        tx_data = tx_result['result']
        meta = tx_data.get('meta', {})
        
        return {
            'signature': signature,
            'slot': tx_data.get('slot', 0),
            'block_time': tx_data.get('blockTime'),
            'fee': meta.get('fee', 0),
            'status': 'Success' if not meta.get('err') else 'Failed',
            'compute_units': meta.get('computeUnitsConsumed', 0),
            'log_messages': meta.get('logMessages', [])[:5]  # First 5 log messages
        }
        
    except Exception as e:
        st.error(f"Error fetching transaction details: {str(e)}")
        return None

def render_transaction_card(tx):
    """Renders a transaction card with details"""
    if not tx:
        return
    
    signature = tx.get('signature', 'Unknown')
    slot = tx.get('slot', 0)
    status = tx.get('status', 'Unknown')
    fee = tx.get('fee', 0)
    block_time = tx.get('block_time')
    
    # Format timestamp
    if block_time:
        tx_time = datetime.fromtimestamp(block_time).strftime('%Y-%m-%d %H:%M:%S UTC')
    else:
        tx_time = 'Unknown'
    
    # Status color
    status_color = "#14F195" if status == "Success" else "#FF6B6B"
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1a1a1a 0%, #252525 100%);
        border: 1px solid #333;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <h4 style="color: #14F195; margin: 0;">Transaction</h4>
            <span style="
                background: {status_color}; 
                color: #000; 
                padding: 6px 12px; 
                border-radius: 15px; 
                font-size: 12px; 
                font-weight: bold;
            ">{status}</span>
        </div>
        
        <div style="margin: 10px 0;">
            <p style="color: #CCCCCC; margin: 5px 0; font-size: 13px;">
                <strong>Signature:</strong><br>
                <span style="
                    font-family: monospace; 
                    word-break: break-all; 
                    background: #0a0a0a; 
                    padding: 8px; 
                    border-radius: 5px; 
                    display: block; 
                    margin-top: 5px;
                ">{signature}</span>
            </p>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;">
            <div>
                <p style="color: #AAAAAA; margin: 0; font-size: 12px;">
                    <strong>Slot:</strong> {slot:,}
                </p>
                <p style="color: #AAAAAA; margin: 5px 0 0 0; font-size: 12px;">
                    <strong>Fee:</strong> {fee/1_000_000_000:.9f} SOL
                </p>
            </div>
            <div>
                <p style="color: #AAAAAA; margin: 0; font-size: 12px;">
                    <strong>Time:</strong> {tx_time}
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_transactions():
    """Renders the transactions page with search and list of recent transactions"""
    st.markdown('<h2>Transaction Explorer</h2>', unsafe_allow_html=True)
    
    # Search section
    st.markdown("Search by transaction signature")
    search_signature = st.text_input("Transaction Signature", placeholder="Enter transaction signature...", key="tx_search", label_visibility="collapsed")
    
    if search_signature:
        with st.spinner("Loading transaction details..."):
            tx_details = get_transaction_details_safe(search_signature)
            
            if tx_details:
                st.markdown("### Transaction Details")
                render_transaction_card(tx_details)
                
                # Show additional details if available
                if tx_details.get('log_messages'):
                    with st.expander("Transaction Logs"):
                        for i, log in enumerate(tx_details['log_messages']):
                            st.code(f"{i+1}. {log}")
            else:
                st.error("Transaction not found or could not be retrieved")
    
    # Recent transactions section
    st.markdown("### Recent Transactions")
    
    with st.spinner("Loading recent transactions..."):
        recent_txs = get_recent_transactions_safe(limit=10)
        
        if recent_txs:
            for tx in recent_txs:
                render_transaction_card(tx)
        else:
            st.info("No recent transactions available at the moment")