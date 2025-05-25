import streamlit as st
import requests
import json
from datetime import datetime
import base58
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solana.rpc.api import Client
from solana.rpc.types import TokenAccountOpts
import os

# Define constants for Solana and USDT SPL token program
SYSTEM_PROGRAM_ID = Pubkey.from_string("11111111111111111111111111111111")
TOKEN_PROGRAM_ID = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
USDT_MINT = Pubkey.from_string("Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB")  # USDT on Solana

@st.cache_resource(ttl=60)
def get_solana_client():
    """Returns a Solana client instance for the specified network"""
    # Check if we have a Helius API key for better RPC access
    helius_api_key = os.environ.get('HELIUS_API_KEY')
    
    if helius_api_key:
        # Use Helius mainnet endpoint for authentic data
        rpc_url = f"https://mainnet.helius-rpc.com/?api-key={helius_api_key}"
        st.write("✅ Connected to Helius RPC for authentic blockchain data")
        return Client(rpc_url)
    else:
        # Fallback to public endpoint
        st.write("⚠️ Using public endpoint (limited functionality)")
        return Client("https://api.mainnet-beta.solana.com")

def make_direct_rpc_call(method, params, rpc_url=None):
    """Make direct HTTP RPC calls to avoid library parsing issues"""
    if rpc_url is None:
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

def get_account_info_robust(address):
    """Get account information using robust error handling and direct RPC calls"""
    try:
        # Import our wallet validator
        from ..utils.wallet_validator import is_valid_solana_address
        from solders.pubkey import Pubkey
        
        # Validate the address
        if not is_valid_solana_address(address):
            st.error(f"Invalid Solana wallet address: {address}")
            return None
            
        pubkey = Pubkey.from_string(address)
        st.write(f"🔍 Analyzing address: {str(pubkey)}")
        
        # Get balance using direct RPC call
        balance_result = make_direct_rpc_call("getBalance", [str(pubkey)])
        if not balance_result or 'result' not in balance_result:
            st.warning("Could not fetch balance")
            return None
        
        balance_lamports = balance_result['result']['value']
        balance_sol = balance_lamports / 1_000_000_000  # Convert to SOL
        st.write(f"💰 Balance: {balance_sol:.9f} SOL ({balance_lamports:,} lamports)")
        
        # Get transaction signatures using direct RPC call
        tx_count = 0
        try:
            sigs_result = make_direct_rpc_call("getSignaturesForAddress", [str(pubkey), {"limit": 10}])
            if sigs_result and 'result' in sigs_result:
                tx_count = len(sigs_result['result'])
                st.write(f"📊 Recent transactions: {tx_count}")
            else:
                st.write("📊 No recent transactions found")
        except Exception as tx_error:
            st.write(f"⚠️ Transaction count unavailable: {str(tx_error)}")
        
        # Try to get USDT balance using direct RPC call
        usdt_balance = 0.0
        try:
            token_accounts_result = make_direct_rpc_call("getTokenAccountsByOwner", [
                str(pubkey),
                {"mint": str(USDT_MINT)},
                {"encoding": "jsonParsed"}
            ])
            
            if token_accounts_result and 'result' in token_accounts_result:
                token_accounts = token_accounts_result['result']['value']
                if token_accounts:
                    # Get balance from first USDT token account
                    token_account = token_accounts[0]['account']['data']['parsed']['info']
                    usdt_balance = float(token_account['tokenAmount']['uiAmount'] or 0)
                    st.write(f"💵 USDT Balance: {usdt_balance:.6f} USDT")
                else:
                    st.write("💵 No USDT tokens found")
        except Exception as usdt_error:
            st.write(f"⚠️ USDT balance unavailable: {str(usdt_error)}")
        
        # Return account information
        return {
            'address': str(pubkey),
            'balance_sol': balance_sol,
            'balance_lamports': balance_lamports,
            'transaction_count': tx_count,
            'usdt_balance': usdt_balance,
            'address_type': address_type
        }
        
    except Exception as e:
        st.error(f"Error fetching account info: {str(e)}")
        return None

def get_recent_transactions_robust(address, limit=5):
    """Get recent transactions using robust error handling"""
    try:
        from ..utils.wallet_validator import is_valid_solana_address
        from solders.pubkey import Pubkey
        
        if not is_valid_solana_address(address):
            st.error(f"Invalid Solana wallet address: {address}")
            return []
            
        pubkey = Pubkey.from_string(address)
        
        # Get transaction signatures using direct RPC call
        sigs_result = make_direct_rpc_call("getSignaturesForAddress", [str(pubkey), {"limit": limit}])
        
        if not sigs_result or 'result' not in sigs_result:
            return []
        
        transactions = []
        for sig_info in sigs_result['result']:
            # Get transaction details
            tx_result = make_direct_rpc_call("getTransaction", [
                sig_info['signature'],
                {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}
            ])
            
            if tx_result and 'result' in tx_result and tx_result['result']:
                tx_data = tx_result['result']
                
                # Extract basic transaction info
                transaction = {
                    'signature': sig_info['signature'],
                    'slot': sig_info.get('slot', 0),
                    'block_time': sig_info.get('blockTime'),
                    'status': 'Success' if not sig_info.get('err') else 'Failed',
                    'fee': tx_data.get('meta', {}).get('fee', 0),
                }
                
                transactions.append(transaction)
        
        return transactions
        
    except Exception as e:
        st.error(f"Error fetching transactions: {str(e)}")
        return []

def get_recent_blocks_robust(limit=10):
    """Get recent blocks using direct RPC calls"""
    try:
        # Get current slot
        slot_result = make_direct_rpc_call("getSlot", [])
        if not slot_result or 'result' not in slot_result:
            return []
        
        current_slot = slot_result['result']
        blocks = []
        
        # Get recent blocks
        for i in range(limit):
            slot = current_slot - i
            block_result = make_direct_rpc_call("getBlock", [slot, {"encoding": "jsonParsed"}])
            
            if block_result and 'result' in block_result and block_result['result']:
                block_data = block_result['result']
                
                block = {
                    'slot': slot,
                    'block_time': block_data.get('blockTime'),
                    'transaction_count': len(block_data.get('transactions', [])),
                    'block_hash': block_data.get('blockhash', ''),
                    'parent_slot': block_data.get('parentSlot', 0)
                }
                blocks.append(block)
        
        return blocks
        
    except Exception as e:
        st.error(f"Error fetching blocks: {str(e)}")
        return []

def create_keypair():
    """Creates a keypair for demo purposes"""
    try:
        keypair = Keypair()
        return {
            'public_key': str(keypair.pubkey()),
            'private_key': base58.b58encode(bytes(keypair)).decode('utf-8')
        }
    except Exception as e:
        st.error(f"Error creating keypair: {str(e)}")
        return None

def get_recent_blockhash():
    """Gets a recent blockhash from the Solana blockchain"""
    try:
        result = make_direct_rpc_call("getLatestBlockhash", [])
        if result and 'result' in result:
            return result['result']['value']['blockhash']
        return None
    except Exception as e:
        st.error(f"Error getting recent blockhash: {str(e)}")
        return None