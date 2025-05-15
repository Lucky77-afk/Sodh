import streamlit as st
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from solders.pubkey import Pubkey as PublicKey
from solders.transaction import Transaction
from solders.instruction import Instruction as TransactionInstruction, AccountMeta

# Import Blockhash from the correct location for solders 0.26.0
try:
    # Try the most common location first
    from solders.hash import Hash as Blockhash
except ImportError:
    try:
        # Try direct import for solders 0.26.0
        from solders import blockhash as solders_blockhash
        Blockhash = solders_blockhash.Blockhash
    except (ImportError, AttributeError):
        try:
            # Try another possible location
            from solders.rpc.responses import Blockhash
        except ImportError:
            # Last resort - create a simple Blockhash class
            class Blockhash:
                def __init__(self, blockhash_str):
                    self.blockhash = blockhash_str
                    
                def __str__(self):
                    return self.blockhash

from solders.keypair import Keypair
from datetime import datetime, timedelta
import base64
import json
import time
import base58
import struct

# Define constants for Solana and USDT SPL token program
def create_pubkey_from_string(address):
    """Helper function to create a PublicKey from a base58-encoded string"""
    try:
        # First, try to decode the base58 string to bytes
        decoded = base58.b58decode(address)
        # Then create a PublicKey from the decoded bytes
        return PublicKey(decoded)
    except Exception as e:
        st.error(f"Error creating PublicKey from address {address}: {str(e)}")
        raise

# Initialize constants with proper PublicKey objects
SYSTEM_PROGRAM_ID = create_pubkey_from_string("11111111111111111111111111111111")
TOKEN_PROGRAM_ID = create_pubkey_from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
USDT_MINT = create_pubkey_from_string("Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB")  # USDT on Solana

@st.cache_resource(ttl=60)
def get_solana_client():
    """Returns a Solana client instance for the specified network"""
    # Using Solana Devnet for development (switch to mainnet for production)
    return Client("https://api.devnet.solana.com")

@st.cache_data(ttl=60)
def get_recent_blocks(_client, limit=10):
    """Get recent blocks from the Solana blockchain"""
    try:
        # Create a fresh client instance to avoid hashing errors
        client = Client("https://api.devnet.solana.com")
        
        # Get recent confirmed blocks
        response = client.get_recent_blocks(limit=limit)
        
        # Handle solders response
        blocks_data = []
        if hasattr(response, 'value'):
            blocks_data = response.value if hasattr(response.value, '__iter__') else []
        elif isinstance(response, dict) and 'result' in response:
            blocks_data = response.get('result', [])
        
        if not blocks_data:
            st.error("No block data received from Solana")
            return []
            
        recent_blocks = []
        
        # Get block time information for each block
        for block in blocks_data:
            try:
                slot = block
                
                # Get block time
                block_time_response = client.get_block_time(slot)
                timestamp = int(time.time())  # Default to current time
                
                # Handle block time response
                if hasattr(block_time_response, 'value'):
                    timestamp = block_time_response.value
                elif isinstance(block_time_response, dict) and 'result' in block_time_response:
                    timestamp = block_time_response.get('result', timestamp)
                
                # Get block hash and other info
                block_info_response = client.get_block(slot)
                blockhash = 'unknown'
                
                # Handle block info response
                if hasattr(block_info_response, 'value'):
                    block_value = block_info_response.value
                    if hasattr(block_value, 'blockhash'):
                        blockhash = str(block_value.blockhash)
                elif isinstance(block_info_response, dict) and 'result' in block_info_response:
                    result = block_info_response.get('result', {})
                    if isinstance(result, dict):
                        blockhash = result.get('blockhash', 'unknown')
                
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
def get_latest_block_time(_client):
    """Get the latest block time"""
    try:
        # Create a fresh client instance to avoid hashing errors
        client = Client("https://api.devnet.solana.com")
        
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
def get_recent_transactions(_client, limit=10):
    """Get recent transactions from the Solana blockchain"""
    try:
        # Create a fresh client instance to avoid hashing errors
        client = Client("https://api.devnet.solana.com")
        
        # Get recent confirmed signatures using client
        signatures_response = client.get_signatures_for_address(
            account=SYSTEM_PROGRAM_ID,  # System program gets many transactions
            limit=limit
        )
        
        # Handle solders response
        if hasattr(signatures_response, 'value'):
            signatures_data = signatures_response.value
        elif isinstance(signatures_response, dict) and 'result' in signatures_response:
            signatures_data = signatures_response['result']
        else:
            st.error("Unexpected response format from get_signatures_for_address")
            return []
            
        recent_txs = []
        
        for tx_info in signatures_data:
            try:
                # Extract the transaction signature
                if hasattr(tx_info, 'signature'):
                    signature = str(tx_info.signature)
                elif isinstance(tx_info, dict):
                    signature = tx_info.get('signature', '')
                else:
                    continue
                
                # Get full transaction details
                tx_data = get_transaction_details(client, signature)
                
                if not tx_data:
                    continue
                
                # Determine transaction status
                meta = tx_data.get('meta', {}) if hasattr(tx_data, 'get') else {}
                status = "Success" if meta.get('err') is None else "Failed"
                
                # Get block time
                block_time = tx_data.get('blockTime', 0) if hasattr(tx_data, 'get') else 0
                formatted_time = datetime.fromtimestamp(block_time).strftime("%Y-%m-%d %H:%M:%S") if block_time else "Unknown"
                
                # Get slot
                slot = tx_data.get('slot', 0) if hasattr(tx_data, 'get') else 0
                
                # Try to determine transaction type by examining instructions
                tx_type = "Unknown"
                try:
                    # Get transaction and message
                    transaction = tx_data.get('transaction', {}) if hasattr(tx_data, 'get') else {}
                    message = transaction.get('message', {}) if hasattr(transaction, 'get') else {}
                    instructions = message.get('instructions', []) if hasattr(message, 'get') else []
                    
                    # Program ID of the first instruction can indicate the transaction type
                    program_id = ""
                    if instructions and len(instructions) > 0:
                        first_instruction = instructions[0] if hasattr(instructions, '__getitem__') else {}
                        program_id = first_instruction.get('programId', '') if hasattr(first_instruction, 'get') else ''
                    
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

def get_transaction_details(_client, signature):
    """Get detailed information for a specific transaction"""
    try:
        # Create a fresh client instance to avoid hashing errors
        client = Client("https://api.devnet.solana.com")
        
        tx_response = client.get_transaction(signature)
        
        # Handle solders response
        if hasattr(tx_response, 'value'):
            return tx_response.value
        elif isinstance(tx_response, dict) and 'result' in tx_response:
            return tx_response['result']
            
        return None
    except Exception as e:
        st.error(f"Error fetching transaction details: {str(e)}")
        return None

def get_account_info(_client, address):
    """Get account information for a wallet address"""
    try:
        # Create a fresh client instance to avoid hashing errors
        client = Client("https://api.devnet.solana.com")
        
        # Check if the address is valid
        if not address or len(address) < 32:
            return None
            
        try:
            # Convert address string to PublicKey object using our helper function
            pubkey = create_pubkey_from_string(address)
        except Exception as e:
            st.error(f"Invalid Solana address format: {str(e)}")
            return None
        
        # Get SOL balance
        balance_response = client.get_balance(pubkey)
        
        # Handle solders response
        balance_lamports = 0
        if hasattr(balance_response, 'value'):
            balance_lamports = balance_response.value
        elif isinstance(balance_response, dict) and 'result' in balance_response:
            result = balance_response.get('result', {})
            if isinstance(result, dict) and 'value' in result:
                balance_lamports = result['value']
        
        # Convert lamports to SOL
        balance_sol = balance_lamports / 1_000_000_000  # 1 SOL = 10^9 lamports
        
        # Get transaction count
        tx_signatures = client.get_signatures_for_address(pubkey, limit=100)
        
        # Handle solders response for transaction signatures
        tx_count = 0
        if hasattr(tx_signatures, 'value'):
            tx_count = len(tx_signatures.value) if hasattr(tx_signatures.value, '__len__') else 0
        elif isinstance(tx_signatures, dict) and 'result' in tx_signatures:
            result = tx_signatures.get('result', [])
            tx_count = len(result) if hasattr(result, '__len__') else 0
        
        # Try to get USDT token balance if address has associated token account
        usdt_balance = 0.0
        try:
            # Find USDT associated token account for this wallet
            associated_token_response = client.get_token_accounts_by_owner(
                pubkey, 
                {'mint': str(USDT_MINT)}
            )
            
            # Handle solders response for token accounts
            token_accounts = []
            if hasattr(associated_token_response, 'value'):
                token_accounts = associated_token_response.value
            elif isinstance(associated_token_response, dict) and 'result' in associated_token_response:
                result = associated_token_response.get('result', {})
                if hasattr(result, 'get'):
                    token_accounts = result.get('value', [])
            
            if token_accounts and len(token_accounts) > 0:
                # Get the first token account
                token_account = token_accounts[0] if hasattr(token_accounts, '__getitem__') else {}
                
                # Get the token account pubkey
                token_account_pubkey = None
                if hasattr(token_account, 'pubkey'):
                    token_account_pubkey = token_account.pubkey
                elif isinstance(token_account, dict) and 'pubkey' in token_account:
                    token_account_pubkey = token_account['pubkey']
                
                if token_account_pubkey:
                    # Get token account balance
                    token_account_info = client.get_token_account_balance(token_account_pubkey)
                    
                    # Extract USDT balance from account info
                    if hasattr(token_account_info, 'value'):
                        value = token_account_info.value
                        if hasattr(value, 'ui_amount'):
                            usdt_balance = float(value.ui_amount)
                    elif isinstance(token_account_info, dict) and 'result' in token_account_info:
                        result = token_account_info.get('result', {})
                        if hasattr(result, 'get'):
                            value = result.get('value', {})
                            if hasattr(value, 'get'):
                                usdt_amount = value.get('uiAmount', 0)
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

def get_account_transactions(_client, address, limit=5):
    """Get recent transactions for an account"""
    try:
        # Create a fresh client instance to avoid hashing errors
        client = Client("https://api.devnet.solana.com")
        
        # Check if address is valid
        if not address or len(address) < 32:
            return []
            
        try:
            # Convert address string to PublicKey object using our helper function
            pubkey = create_pubkey_from_string(address)
        except Exception as e:
            st.error(f"Invalid Solana address format: {str(e)}")
            return []
        
        # Get recent signatures for this account
        signatures_response = client.get_signatures_for_address(
            pubkey,
            limit=limit
        )
        
        # Handle solders response
        signatures_data = []
        if hasattr(signatures_response, 'value'):
            signatures_data = signatures_response.value
        elif isinstance(signatures_response, dict) and 'result' in signatures_response:
            signatures_data = signatures_response['result']
        else:
            st.error("Unexpected response format from get_signatures_for_address")
            return []
            
        account_txs = []
        
        # Process each transaction
        for sig_info in signatures_data:
            try:
                # Get signature
                if hasattr(sig_info, 'signature'):
                    signature = str(sig_info.signature)
                elif isinstance(sig_info, dict):
                    signature = sig_info.get('signature', '')
                else:
                    continue
                
                # Get full transaction details
                tx_data = get_transaction_details(client, signature)
                
                if not tx_data:
                    continue
                    
                # Determine transaction status
                meta = tx_data.get('meta', {}) if hasattr(tx_data, 'get') else {}
                status = meta.get('err') is None if hasattr(meta, 'get') else False
                
                # Get block time and slot
                block_time = tx_data.get('blockTime', 0) if hasattr(tx_data, 'get') else 0
                slot = tx_data.get('slot', 0) if hasattr(tx_data, 'get') else 0
                
                # Try to determine transaction amount and direction
                amount = 0.0
                tx_type = "Unknown"
                
                try:
                    # Get transaction and message data
                    transaction = tx_data.get('transaction', {}) if hasattr(tx_data, 'get') else {}
                    message = transaction.get('message', {}) if hasattr(transaction, 'get') else {}
                    
                    # Get instructions and account keys
                    instructions = message.get('instructions', []) if hasattr(message, 'get') else []
                    account_keys = message.get('accountKeys', []) if hasattr(message, 'get') else []
                    
                    # Handle both list and attribute access for account_keys
                    if hasattr(account_keys, 'keys'):
                        account_keys = [str(key) for key in account_keys.keys]
                    elif not isinstance(account_keys, list):
                        account_keys = []
                    
                    # Check if this is a system program transfer
                    if instructions and len(instructions) > 0:
                        # Get the first instruction
                        first_instruction = instructions[0] if hasattr(instructions, '__getitem__') else {}
                        
                        # Get program ID
                        program_id = ""
                        if hasattr(first_instruction, 'program_id'):
                            program_id = str(first_instruction.program_id)
                        elif isinstance(first_instruction, dict):
                            program_id = str(first_instruction.get('programId', ''))
                        
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
                            
                            # Get meta data
                            meta = tx_data.get('meta', {}) if hasattr(tx_data, 'get') else {}
                            
                            # Get pre and post balances to determine amount
                            pre_balances = meta.get('preBalances', []) if hasattr(meta, 'get') else []
                            post_balances = meta.get('postBalances', []) if hasattr(meta, 'get') else []
                            
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

# Creates a new keypair for demo purposes
def create_keypair():
    """Creates a keypair for demo purposes"""
    return Keypair()

# Gets a recent blockhash from the Solana blockchain
def get_recent_blockhash(_client):
    """Gets a recent blockhash from the Solana blockchain"""
    try:
        # Create a new client instance to avoid caching issues
        client = Client("https://api.devnet.solana.com")
        
        response = client.get_recent_blockhash()
        
        # Handle solders response
        if hasattr(response, 'value'):
            # Handle the case where response is a GetRecentBlockhashResp object
            if hasattr(response.value, 'value') and hasattr(response.value.value, 'blockhash'):
                return str(response.value.value.blockhash)
        elif isinstance(response, dict) and 'result' in response:
            # Handle the case where response is a dict with 'result' key
            result = response.get('result', {})
            if isinstance(result, dict) and 'value' in result:
                value = result.get('value', {})
                if isinstance(value, dict) and 'blockhash' in value:
                    return value['blockhash']
        
        return None
    except Exception as e:
        st.error(f"Error getting recent blockhash: {str(e)}")
        return None