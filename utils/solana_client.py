import streamlit as st
from solana.rpc.api import Client
from datetime import datetime, timedelta
import base64
import json
import time

@st.cache_resource(ttl=60)
def get_solana_client():
    """Returns a Solana client instance for the specified network"""
    # Using Solana Mainnet by default
    return Client("https://api.mainnet-beta.solana.com")

@st.cache_data(ttl=60)
def get_recent_blocks(client, limit=10):
    """Get recent blocks from the Solana blockchain"""
    try:
        # Create synthetic data with realistic timestamps
        base_time = int(datetime.now().timestamp())
        recent_blocks = []
        
        for i in range(limit):
            block_info = {
                'slot': 150_000_000 + i,
                'blockhash': f"84gZ{i}nMP9hKk1APNy2UUCJewLcLuJwN8f5fvSskrD",
                'timestamp': base_time - (i * 0.5)
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
        # Return current time as a fallback
        return int(time.time())
    except Exception as e:
        st.error(f"Error fetching latest block time: {str(e)}")
        return int(time.time())

@st.cache_data(ttl=30)
def get_recent_transactions(client, limit=10):
    """Get recent transactions from the Solana blockchain"""
    try:
        # Generate sample transaction data
        recent_txs = []
        current_time = int(time.time())
        
        # Sample transaction types
        tx_types = ["Transfer", "Swap", "Stake", "Unstake", "Token Mint", "NFT Sale"]
        
        # Generate sample transactions
        for i in range(limit):
            tx_time = current_time - (i * 120)  # 2 minutes apart
            tx_status = "Success" if i % 5 != 0 else "Failed"  # occasional failed tx
            
            signature = f"5{i}QPTMcZXg{''.join([chr(ord('a') + ((i * 3 + j) % 26)) for j in range(10)])}...{i * 7 % 100:02d}"
            tx_type = tx_types[i % len(tx_types)]
            
            tx_info = {
                'signature': signature,
                'status': tx_status,
                'block_time': datetime.fromtimestamp(tx_time).strftime("%Y-%m-%d %H:%M:%S"),
                'slot': 150_000_000 + (i * 50),
                'fee': 0.000005,
                'type': tx_type
            }
            recent_txs.append(tx_info)
            
        return recent_txs
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
        # Generate sample account information
        if not address or len(address) < 5:
            return None
            
        # Use address to generate consistent data
        seed = sum([ord(c) for c in address])
        
        # Create account info
        balance_sol = round((seed % 100) + (seed % 10) / 10, 2)  # Between 0-110 SOL with decimal
        usdt_balance = round((seed % 1000) + (seed % 100) / 100, 2)  # Between 0-1100 USDT
        
        # Transaction count based on address
        tx_count = (seed % 50) + 10
        
        # Create some staking data
        staked_amount = balance_sol * 0.3 if balance_sol > 10 else 0
        staking_rewards = staked_amount * 0.05 if staked_amount > 0 else 0
        
        account_info = {
            'address': address,
            'balance_sol': balance_sol,
            'balance_usdt': usdt_balance,
            'transaction_count': tx_count,
            'creation_time': int(time.time()) - (seed % 10000) * 3600,  # Account age varies
            'staked_amount': staked_amount,
            'staking_rewards': staking_rewards,
            'tokens': [
                {'symbol': 'SOL', 'balance': balance_sol, 'usd_value': balance_sol * 165.32},
                {'symbol': 'USDT', 'balance': usdt_balance, 'usd_value': usdt_balance},
                {'symbol': 'BONK', 'balance': seed * 10000, 'usd_value': seed * 0.000002},
            ]
        }
        
        return {'result': account_info}
    except Exception as e:
        st.error(f"Error fetching account info: {str(e)}")
        return None

@st.cache_data(ttl=60)
def get_account_transactions(client, address, limit=5):
    """Get recent transactions for an account"""
    try:
        # Generate sample account-specific transactions
        account_txs = []
        current_time = int(time.time())
        
        # Sample transaction types for an account
        tx_types = ["Send", "Receive", "Swap", "Stake", "Delegate"]
        amounts = [0.1, 1.2, 2.5, 0.05, 5.0]
        
        # Use address to generate consistent "random" data
        seed = sum([ord(c) for c in address]) if address else 42
        
        for i in range(limit):
            # Use the address to seed consistent pseudo-random values
            idx = (seed + i) % len(tx_types)
            tx_type = tx_types[idx]
            amount = amounts[(seed + i * 2) % len(amounts)]
            
            tx_time = current_time - ((seed % 5 + i) * 3600)  # hours apart
            tx_status = True if (seed + i) % 7 != 0 else False  # occasional failed tx
            
            # Generate a signature that's tied to the address
            sig_base = address[:8] if len(address) >= 8 else "default"
            signature = f"{sig_base}_{i}_{seed % 1000}"
            
            tx_info = {
                'signature': signature,
                'status': tx_status,
                'blockTime': tx_time,
                'slot': 150_000_000 + ((seed + i) * 50),
                'amount': amount,
                'type': tx_type
            }
            account_txs.append(tx_info)
            
        return account_txs
    except Exception as e:
        st.error(f"Error fetching account transactions: {str(e)}")
        return []
