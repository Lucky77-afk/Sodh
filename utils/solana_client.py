import streamlit as st
from solana.rpc.api import Client
from datetime import datetime, timedelta
import base64
import json

@st.cache_resource(ttl=60)
def get_solana_client():
    """Returns a Solana client instance for the specified network"""
    # Using Solana Mainnet by default
    return Client("https://api.mainnet-beta.solana.com")

@st.cache_data(ttl=60)
def get_recent_blocks(client, limit=10):
    """Get recent blocks from the Solana blockchain"""
    try:
        recent_blocks = []
        
        # Get recent block signatures
        signatures_response = client.get_recent_block_signatures_with_config(limit=limit)
        if signatures_response and 'result' in signatures_response:
            recent_signatures = signatures_response['result']
            
            for block in recent_signatures:
                block_info = {
                    'slot': block.get('slot'),
                    'blockhash': block.get('blockhash'),
                    'timestamp': block.get('blockTime')
                }
                recent_blocks.append(block_info)
                
        return recent_blocks
    except Exception as e:
        st.error(f"Error fetching recent blocks: {str(e)}")
        return []

@st.cache_data(ttl=30)
def get_latest_block_time(client):
    """Get the latest block time"""
    try:
        slot_response = client.get_slot()
        if slot_response and 'result' in slot_response:
            latest_slot = slot_response['result']
            
            # Get the block time for this slot
            block_time_response = client.get_block_time(latest_slot)
            if block_time_response and 'result' in block_time_response:
                return block_time_response['result']
                
        return None
    except Exception as e:
        st.error(f"Error fetching latest block time: {str(e)}")
        return None

@st.cache_data(ttl=30)
def get_recent_transactions(client, limit=10):
    """Get recent transactions from the Solana blockchain"""
    try:
        # Get recent transaction signatures
        signatures_response = client.get_signatures_for_address(client.get_genesis_hash()['result'], limit=limit)
        
        if signatures_response and 'result' in signatures_response:
            recent_txs = []
            
            for sig_info in signatures_response['result']:
                signature = sig_info.get('signature')
                status = "Success" if sig_info.get('err') is None else "Failed"
                block_time = datetime.fromtimestamp(sig_info.get('blockTime', 0)).strftime("%Y-%m-%d %H:%M:%S") if sig_info.get('blockTime') else "Unknown"
                slot = sig_info.get('slot', 'Unknown')
                fee = 0.000005  # Approximate fee in SOL (would be calculated from tx details)
                
                tx_info = {
                    'signature': signature,
                    'status': status,
                    'block_time': block_time,
                    'slot': slot,
                    'fee': fee
                }
                recent_txs.append(tx_info)
                
            return recent_txs
        return []
    except Exception as e:
        st.error(f"Error fetching recent transactions: {str(e)}")
        return []

@st.cache_data(ttl=300)
def get_transaction_details(client, signature):
    """Get detailed information for a specific transaction"""
    try:
        tx_response = client.get_transaction(signature)
        if tx_response and 'result' in tx_response:
            return tx_response['result']
        return None
    except Exception as e:
        st.error(f"Error fetching transaction details: {str(e)}")
        return None

@st.cache_data(ttl=60)
def get_account_info(client, address):
    """Get account information for a wallet address"""
    try:
        account_response = client.get_account_info(address)
        return account_response
    except Exception as e:
        st.error(f"Error fetching account info: {str(e)}")
        return None

@st.cache_data(ttl=60)
def get_account_transactions(client, address, limit=5):
    """Get recent transactions for an account"""
    try:
        # Get recent transaction signatures for the address
        signatures_response = client.get_signatures_for_address(address, limit=limit)
        
        if signatures_response and 'result' in signatures_response:
            account_txs = []
            
            for sig_info in signatures_response['result']:
                tx_info = {
                    'signature': sig_info.get('signature'),
                    'status': sig_info.get('err') is None,
                    'blockTime': sig_info.get('blockTime'),
                    'slot': sig_info.get('slot')
                }
                account_txs.append(tx_info)
                
            return account_txs
        return []
    except Exception as e:
        st.error(f"Error fetching account transactions: {str(e)}")
        return []
