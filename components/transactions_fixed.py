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
        response = requests.post(rpc_url, json=payload, timeout=30)  # Increased timeout
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        st.warning(f"Request timed out for {method}")
        return None
    except requests.exceptions.RequestException as e:
        st.warning(f"Network error for {method}: {str(e)}")
        return None
    except Exception as e:
        st.warning(f"Error in {method}: {str(e)}")
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
    """Renders an enhanced transaction card with modern design"""
    if not tx:
        return
    
    signature = tx.get('signature', 'Unknown')
    slot = tx.get('slot', 0)
    status = tx.get('status', 'Unknown')
    fee = tx.get('fee', 0)
    block_time = tx.get('block_time')
    compute_units = tx.get('compute_units', 0)
    
    # Format timestamp
    if block_time:
        tx_time = datetime.fromtimestamp(block_time).strftime('%H:%M:%S UTC')
        tx_date = datetime.fromtimestamp(block_time).strftime('%Y-%m-%d')
    else:
        tx_time = 'Unknown'
        tx_date = 'Unknown'
    
    # Status color and icon
    if status == "Success":
        status_color = "#14F195"
        status_bg = "rgba(20, 241, 149, 0.1)"
        status_icon = "✓"
    else:
        status_color = "#FF6B6B"
        status_bg = "rgba(255, 107, 107, 0.1)"
        status_icon = "✗"
    
    # Truncate signature for display
    sig_display = f"{signature[:8]}...{signature[-8:]}" if len(signature) > 16 else signature
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
        border: 1px solid rgba(20, 241, 149, 0.2);
        border-radius: 20px;
        padding: 24px;
        margin: 20px 0;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    ">
        <!-- Gradient overlay -->
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #14F195 0%, #9945FF 50%, #14F195 100%);
        "></div>
        
        <!-- Header with status -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="
                    width: 40px;
                    height: 40px;
                    background: linear-gradient(135deg, #14F195 0%, #00FFA3 100%);
                    border-radius: 12px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 18px;
                    font-weight: bold;
                    color: #000;
                ">📊</div>
                <div>
                    <h4 style="color: #FFFFFF; margin: 0; font-size: 18px; font-weight: 600;">Transaction</h4>
                    <p style="color: #AAAAAA; margin: 0; font-size: 12px;">{tx_date}</p>
                </div>
            </div>
            <div style="
                background: {status_bg};
                border: 1px solid {status_color};
                color: {status_color};
                padding: 8px 16px;
                border-radius: 25px;
                font-size: 12px;
                font-weight: 600;
                display: flex;
                align-items: center;
                gap: 6px;
            ">
                <span style="font-size: 14px;">{status_icon}</span>
                {status}
            </div>
        </div>
        
        <!-- Signature with copy functionality -->
        <div style="margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="color: #14F195; font-size: 14px; font-weight: 600;">Transaction Signature</span>
                <span style="color: #AAAAAA; font-size: 11px;">Click to view full</span>
            </div>
            <div style="
                background: rgba(0, 0, 0, 0.4);
                border: 1px solid rgba(20, 241, 149, 0.3);
                border-radius: 12px;
                padding: 12px 16px;
                font-family: 'Courier New', monospace;
                font-size: 13px;
                color: #FFFFFF;
                word-break: break-all;
                position: relative;
                overflow: hidden;
            ">
                <div style="display: none;" id="full-{signature[:8]}">{signature}</div>
                <div id="short-{signature[:8]}">{sig_display}</div>
            </div>
        </div>
        
        <!-- Transaction details grid -->
        <div style="
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 16px;
            margin-top: 20px;
        ">
            <div style="
                background: rgba(20, 241, 149, 0.05);
                border: 1px solid rgba(20, 241, 149, 0.2);
                border-radius: 12px;
                padding: 12px;
                text-align: center;
            ">
                <div style="color: #14F195; font-size: 11px; font-weight: 600; margin-bottom: 4px;">SLOT</div>
                <div style="color: #FFFFFF; font-size: 16px; font-weight: 700; font-family: monospace;">{slot:,}</div>
            </div>
            
            <div style="
                background: rgba(153, 69, 255, 0.05);
                border: 1px solid rgba(153, 69, 255, 0.2);
                border-radius: 12px;
                padding: 12px;
                text-align: center;
            ">
                <div style="color: #9945FF; font-size: 11px; font-weight: 600; margin-bottom: 4px;">FEE</div>
                <div style="color: #FFFFFF; font-size: 16px; font-weight: 700; font-family: monospace;">{fee/1_000_000_000:.6f} SOL</div>
            </div>
            
            <div style="
                background: rgba(0, 255, 163, 0.05);
                border: 1px solid rgba(0, 255, 163, 0.2);
                border-radius: 12px;
                padding: 12px;
                text-align: center;
            ">
                <div style="color: #00FFA3; font-size: 11px; font-weight: 600; margin-bottom: 4px;">TIME</div>
                <div style="color: #FFFFFF; font-size: 16px; font-weight: 700; font-family: monospace;">{tx_time}</div>
            </div>
            
            <div style="
                background: rgba(255, 215, 0, 0.05);
                border: 1px solid rgba(255, 215, 0, 0.2);
                border-radius: 12px;
                padding: 12px;
                text-align: center;
            ">
                <div style="color: #FFD700; font-size: 11px; font-weight: 600; margin-bottom: 4px;">COMPUTE</div>
                <div style="color: #FFFFFF; font-size: 16px; font-weight: 700; font-family: monospace;">{compute_units:,}</div>
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