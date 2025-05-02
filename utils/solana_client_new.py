import streamlit as st
import time
import json
import base64
import solders.pubkey
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta

# Use solders.pubkey.Pubkey instead of solana.publickey.PublicKey
SYSTEM_PROGRAM_ID = "11111111111111111111111111111111"
TOKEN_PROGRAM_ID = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
USDT_MINT = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"  # USDT on Solana

@st.cache_resource(ttl=60)
def get_solana_client():
    """Returns a Solana client instance for the specified network"""
    # Import here to avoid module resolution issues
    from solana.rpc.api import Client
    # Using Solana Devnet for development (switch to mainnet for production)
    return Client("https://api.devnet.solana.com")

@st.cache_data(ttl=60)
def get_recent_blocks(client, limit=10):
    """Get recent blocks from the Solana blockchain"""
    try:
        # Get recent confirmed blocks
        response = client.get_recent_blocks(limit=limit)
        
        if 'result' not in response:
            st.error("Failed to get recent blocks from Solana")
            return []
            
        blocks_data = response['result']
        recent_blocks = []
        
        # Get block time information for each block
        for block in blocks_data:
            try:
                # Try to get block time
                slot = block
                block_time_response = client.get_block_time(slot)
                timestamp = block_time_response.get('result', int(time.time()))
                
                # Get block hash
                block_info_response = client.get_block(slot)
                blockhash = block_info_response.get('result', {}).get('blockhash', 'unknown')
                
                block_info = {
                    'slot': slot,
                    'blockhash': blockhash,
                    'timestamp': timestamp
                }
                recent_blocks.append(block_info)
            except Exception as block_error:
                st.error(f"Error processing block {block}: {str(block_error)}")
                
        return recent_blocks
    except Exception as e:
        st.error(f"Error fetching recent blocks: {str(e)}")
        return []

@st.cache_data(ttl=30)
def get_latest_block_time(client):
    """Get the latest block time"""
    try:
        # Get the latest finalized slot
        slot_response = client.get_slot(commitment="finalized")
        if 'result' not in slot_response:
            return int(time.time())
            
        slot = slot_response['result']
        
        # Get the block time for this slot
        block_time_response = client.get_block_time(slot)
        if 'result' not in block_time_response:
            return int(time.time())
            
        return block_time_response['result']
    except Exception as e:
        st.error(f"Error fetching latest block time: {str(e)}")
        return int(time.time())

@st.cache_data(ttl=30)
def get_recent_transactions(client, limit=10):
    """Get recent transactions from the Solana blockchain"""
    try:
        # Get recent confirmed signatures using client
        signatures_response = client.get_signatures_for_address(
            account=SYSTEM_PROGRAM_ID,  # System program gets many transactions
            limit=limit
        )
        
        if 'result' not in signatures_response:
            st.error("Failed to get recent transactions from Solana")
            return []
            
        signatures_data = signatures_response['result']
        recent_txs = []
        
        for tx_info in signatures_data:
            try:
                # Extract the transaction signature
                signature = tx_info.get('signature', '')
                
                # Get full transaction details
                tx_data = get_transaction_details(client, signature)
                
                if not tx_data:
                    continue
                
                # Determine transaction status
                status = "Success" if tx_data.get('meta', {}).get('err') is None else "Failed"
                
                # Get block time
                block_time = tx_data.get('blockTime', 0)
                formatted_time = datetime.fromtimestamp(block_time).strftime("%Y-%m-%d %H:%M:%S") if block_time else "Unknown"
                
                # Get slot
                slot = tx_data.get('slot', 0)
                
                # Try to determine transaction type by examining instructions
                tx_type = "Unknown"
                try:
                    # Program ID of the first instruction can indicate the transaction type
                    program_id = tx_data.get('transaction', {}).get('message', {}).get('instructions', [{}])[0].get('programId', '')
                    
                    # Map program IDs to transaction types
                    program_map = {
                        "11111111111111111111111111111111": "Transfer",
                        "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA": "Token",
                        "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL": "Associated Token",
                        "Stake11111111111111111111111111111111111111": "Stake",
                        "9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin": "Serum DEX",
                    }
                    
                    tx_type = program_map.get(program_id, "Other")
                except Exception:
                    pass
                
                # Calculate fee in SOL
                fee = tx_data.get('meta', {}).get('fee', 0) / 1_000_000_000  # Convert lamports to SOL
                
                # Construct transaction info
                tx_info = {
                    'signature': signature,
                    'status': status,
                    'block_time': formatted_time,
                    'slot': slot,
                    'fee': fee,
                    'type': tx_type
                }
                recent_txs.append(tx_info)
            except Exception as tx_error:
                st.error(f"Error processing transaction: {str(tx_error)}")
                
        return recent_txs
    except Exception as e:
        st.error(f"Error fetching recent transactions: {str(e)}")
        return []

@st.cache_data(ttl=300)
def get_transaction_details(_client, signature):
    """Get detailed information for a specific transaction"""
    try:
        # Import client here to avoid streamlit hashing issues
        from solana.rpc.api import Client
        client = Client("https://api.devnet.solana.com")
        
        tx_response = client.get_transaction(signature)
        if tx_response and 'result' in tx_response:
            return tx_response['result']
        return None
    except Exception as e:
        st.error(f"Error fetching transaction details: {str(e)}")
        return None

@st.cache_data(ttl=60)
def get_account_info(_client, address):
    """Get account information for a wallet address"""
    try:
        # Check if the address is valid
        if not address or len(address) < 32:
            return None
        
        # Import client here to avoid streamlit hashing issues
        from solana.rpc.api import Client
        client = Client("https://api.devnet.solana.com")
        
        # Get SOL balance
        balance_response = client.get_balance(address)
        if 'result' not in balance_response:
            return None
            
        # Convert lamports to SOL
        balance_lamports = balance_response['result']['value']
        balance_sol = balance_lamports / 1_000_000_000  # 1 SOL = 10^9 lamports
        
        # Get transaction count
        tx_signatures = client.get_signatures_for_address(address, limit=100)
        tx_count = len(tx_signatures.get('result', []))
        
        # Try to get USDT token balance if address has associated token account
        usdt_balance = 0.0
        try:
            # Find USDT associated token account for this wallet
            associated_token_response = client.get_token_accounts_by_owner(
                address, 
                {'mint': USDT_MINT}
            )
            
            token_accounts = associated_token_response.get('result', {}).get('value', [])
            
            if token_accounts:
                # Get token account info for the first matching account
                token_account_pubkey = token_accounts[0]['pubkey']
                token_account_info = client.get_token_account_balance(token_account_pubkey)
                
                # Extract USDT balance from account info
                if 'result' in token_account_info:
                    usdt_amount = token_account_info['result'].get('value', {}).get('uiAmount', 0)
                    usdt_balance = float(usdt_amount)
        except Exception as token_error:
            st.warning(f"Could not fetch token balances: {str(token_error)}")
        
        # Current market values (would be fetched from an API in production)
        sol_price_usd = 150.00  # Example price, would come from price feed
        
        # Create account info
        account_info = {
            'address': address,
            'balance_sol': balance_sol,
            'balance_usdt': usdt_balance,
            'transaction_count': tx_count,
            'creation_time': int(time.time()) - (3600 * 24 * 30),  # Placeholder, exact creation time not readily available
            # Token information
            'tokens': [
                {'symbol': 'SOL', 'balance': balance_sol, 'usd_value': balance_sol * sol_price_usd},
                {'symbol': 'USDT', 'balance': usdt_balance, 'usd_value': usdt_balance},
            ]
        }
        
        return {'result': account_info}
    except Exception as e:
        st.error(f"Error fetching account info: {str(e)}")
        return None

@st.cache_data(ttl=60)
def get_account_transactions(_client, address, limit=5):
    """Get recent transactions for an account"""
    try:
        # Check if address is valid
        if not address or len(address) < 32:
            return []
        
        # Import client here to avoid streamlit hashing issues
        from solana.rpc.api import Client
        client = Client("https://api.devnet.solana.com")
        
        # Get recent signatures for this account
        signatures_response = client.get_signatures_for_address(
            address,
            limit=limit
        )
        
        if 'result' not in signatures_response:
            st.error("Failed to get transactions for this account")
            return []
            
        signatures_data = signatures_response['result']
        account_txs = []
        
        # Process each transaction
        for sig_info in signatures_data:
            try:
                # Get signature
                signature = sig_info.get('signature', '')
                
                # Get full transaction details
                tx_data = get_transaction_details(client, signature)
                
                if not tx_data:
                    continue
                    
                # Determine transaction status
                status = True if tx_data.get('meta', {}).get('err') is None else False
                
                # Get block time and slot
                block_time = tx_data.get('blockTime', 0)
                slot = tx_data.get('slot', 0)
                
                # Try to determine transaction amount and direction
                amount = 0.0
                tx_type = "Unknown"
                
                try:
                    # Check transaction message for information about the transfer
                    message = tx_data.get('transaction', {}).get('message', {})
                    instructions = message.get('instructions', [])
                    
                    # Get account keys 
                    account_keys = message.get('accountKeys', [])
                    
                    # Check if this is a system program transfer
                    if instructions and len(instructions) > 0:
                        program_id = instructions[0].get('programId', '')
                        
                        # Handle different transaction types
                        if program_id == "11111111111111111111111111111111":  # System Program
                            # This is likely a SOL transfer
                            tx_type = "Transfer"
                            
                            # Try to determine if it's incoming or outgoing
                            if account_keys and len(account_keys) >= 2:
                                if account_keys[0] == address:
                                    tx_type = "Send"
                                else:
                                    tx_type = "Receive"
                                    
                            # Get pre and post balances to determine amount
                            pre_balances = tx_data.get('meta', {}).get('preBalances', [])
                            post_balances = tx_data.get('meta', {}).get('postBalances', [])
                            
                            if pre_balances and post_balances and len(pre_balances) > 0 and len(post_balances) > 0:
                                # Calculate difference in lamports
                                balance_diff = abs(post_balances[0] - pre_balances[0])
                                amount = balance_diff / 1_000_000_000  # Convert lamports to SOL
                        
                        elif program_id == "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA":  # Token Program
                            # This is an SPL token transaction
                            tx_type = "Token"
                            
                            # More detailed token transaction analysis would go here in a production app
                            
                        elif program_id == "Stake11111111111111111111111111111111111111":  # Stake Program
                            tx_type = "Stake"
                            
                        else:
                            # Other transaction types
                            program_map = {
                                "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL": "Associated Token",
                                "9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin": "Serum DEX",
                            }
                            tx_type = program_map.get(program_id, "Other")
                except Exception as parse_error:
                    st.warning(f"Error parsing transaction data: {str(parse_error)}")
                
                # Create transaction info
                tx_info = {
                    'signature': signature,
                    'status': status,
                    'blockTime': block_time,
                    'slot': slot,
                    'amount': amount,
                    'type': tx_type
                }
                account_txs.append(tx_info)
            except Exception as tx_error:
                st.error(f"Error processing transaction: {str(tx_error)}")
                
        return account_txs
    except Exception as e:
        st.error(f"Error fetching account transactions: {str(e)}")
        return []

# Helper functions to create and submit transactions
def create_keypair():
    """Creates a keypair for demo purposes"""
    # Import here to avoid module resolution issues
    from solana.keypair import Keypair
    return Keypair()

def get_recent_blockhash(client):
    """Gets a recent blockhash from the Solana blockchain"""
    try:
        response = client.get_recent_blockhash()
        if 'result' in response and 'value' in response['result']:
            return response['result']['value']['blockhash']
        return None
    except Exception as e:
        st.error(f"Error getting recent blockhash: {str(e)}")
        return None