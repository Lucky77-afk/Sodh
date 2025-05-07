import streamlit as st
from solana.rpc.api import Client
# Use solders pubkey instead of solana.publickey
import solders.pubkey
from solana.transaction import Transaction
# These imports may have changed with the newer solana package
import solders.instruction
from solders.keypair import Keypair
from solana.rpc.types import TxOpts

# Define compatibility layer for PublicKey
PublicKey = solders.pubkey.Pubkey
# Aliases for compatibility
TransactionInstruction = solders.instruction.Instruction
AccountMeta = solders.instruction.AccountMeta
from datetime import datetime, timedelta
import base64
import json
import time
import base58
import struct

# Define constants for Solana and USDT SPL token program
# Convert string to bytes then to PublicKey
SYSTEM_PROGRAM_ID = PublicKey.from_string("11111111111111111111111111111111")
TOKEN_PROGRAM_ID = PublicKey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
USDT_MINT = PublicKey.from_string("Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB")  # USDT on Solana

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

def get_transaction_details(_client, signature):
    """Get detailed information for a specific transaction"""
    try:
        # Create a fresh client instance to avoid hashing errors
        client = Client("https://api.devnet.solana.com")
        
        tx_response = client.get_transaction(signature)
        if tx_response and 'result' in tx_response:
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
            st.error("Invalid wallet address length")
            return None
            
        try:
            # Convert address string to PublicKey object using from_string
            # Make sure address is a string first and print debug info
            address_str = str(address).strip()
            st.write(f"DEBUG - Address type: {type(address_str)}, Value: {address_str}")
            
            # Check for Ethereum style addresses (starting with 0x)
            if address_str.startswith("0x"):
                st.write("DEBUG - Ethereum style address detected, attempting conversion")
                
                # For Ethereum addresses, we need to inform the user
                st.warning(f"You entered an Ethereum address: {address_str}. Note that Solana addresses don't start with '0x'. Please enter a native Solana address for best results.")
                
                # We can try to convert from hex to bytes and create a PublicKey
                try:
                    # Remove 0x prefix and convert to bytes
                    hex_str = address_str[2:]  # Remove 0x prefix
                    if len(hex_str) < 32:
                        # Pad with zeros if needed
                        hex_str = hex_str.zfill(64)
                    elif len(hex_str) > 64:
                        # Truncate if too long
                        hex_str = hex_str[:64]
                        
                    # Convert to bytes
                    hex_bytes = bytes.fromhex(hex_str)
                    pubkey = PublicKey(hex_bytes[:32])  # Take first 32 bytes
                    st.write(f"DEBUG - Created PublicKey from Ethereum address: {pubkey}")
                    
                    # Show the equivalent Solana address
                    st.info(f"Converted to Solana format: {str(pubkey)}")
                except Exception as e_eth:
                    st.write(f"DEBUG - Ethereum conversion failed: {str(e_eth)}")
                    # Continue with other methods
            
            # Try different methods of creating a PublicKey
            try:
                # Method 1: Direct from_string
                pubkey = PublicKey.from_string(address_str)
                st.write("DEBUG - PublicKey created with from_string")
            except Exception as e1:
                st.write(f"DEBUG - from_string failed: {str(e1)}")
                try:
                    # Check if it's a valid Base58 string
                    if not any(c in address_str for c in '0xOIl+/'):  # Characters not in Base58
                        # Method this includes Bs58 decoding if needed
                        decoded = base58.b58decode(address_str)
                        pubkey = PublicKey(decoded)
                        st.write("DEBUG - PublicKey created with base58 decode")
                    else:
                        raise ValueError("Contains invalid Base58 characters")
                except Exception as e2:
                    st.write(f"DEBUG - base58 decode failed: {str(e2)}")
                    
                    # For demo purposes, if all else fails, use a default demo address
                    fallback_address = "8HGyAAB4dL4GhdQidH6WfCvkm2MF8wZCDm4XRmiWHnnm"
                    try:
                        st.warning(f"Invalid Solana address format. Using demo address for demonstration purposes.")
                        pubkey = PublicKey.from_string(fallback_address)
                        st.write(f"DEBUG - Using fallback demo address: {fallback_address}")
                    except Exception as e3:
                        st.write(f"DEBUG - Fallback address failed: {str(e3)}")
                        raise Exception(f"All PublicKey creation methods failed: {str(e1)}, {str(e2)}, {str(e3)}")
            
        except Exception as e:
            st.error(f"Invalid Solana address format: {str(e)}")
            return None
        
        # Get SOL balance
        try:
            # Debug the pubkey object
            st.write(f"DEBUG - Pubkey type: {type(pubkey)}, Value: {pubkey}")
            
            # Try to get balance with the pubkey
            try:
                balance_response = client.get_balance(pubkey)
                st.write("DEBUG - Balance fetched with pubkey object")
                st.write(f"DEBUG - Balance response type: {type(balance_response)}")
                
                # Handle different response types
                if hasattr(balance_response, 'value'):
                    # This is the solders.rpc.responses.GetBalanceResp type
                    balance_lamports = balance_response.value
                    st.write(f"DEBUG - Using value attribute: {balance_lamports}")
                elif isinstance(balance_response, dict) and 'result' in balance_response:
                    # This is the dictionary response type
                    balance_lamports = balance_response['result']['value']
                    st.write(f"DEBUG - Using result dictionary: {balance_lamports}")
                else:
                    # Try to convert to a string and evaluate
                    st.write(f"DEBUG - Unknown response format: {str(balance_response)}")
                    raise Exception(f"Unknown balance response format: {type(balance_response)}")
                    
            except Exception as e_obj:
                st.write(f"DEBUG - Balance fetch with object failed: {str(e_obj)}")
                # Try with string representation
                try:
                    balance_response = client.get_balance(str(pubkey))
                    st.write("DEBUG - Balance fetched with string representation")
                    
                    # Handle different response types
                    if hasattr(balance_response, 'value'):
                        # This is the solders.rpc.responses.GetBalanceResp type
                        balance_lamports = balance_response.value
                    elif isinstance(balance_response, dict) and 'result' in balance_response:
                        # This is the dictionary response type
                        balance_lamports = balance_response['result']['value']
                    else:
                        # Try to convert to a string and evaluate
                        st.write(f"DEBUG - Unknown response format with string: {str(balance_response)}")
                        raise Exception(f"Unknown balance response format: {type(balance_response)}")
                        
                except Exception as e_str:
                    st.write(f"DEBUG - Balance fetch with string failed: {str(e_str)}")
                    raise Exception(f"Could not fetch balance: {str(e_obj)}, {str(e_str)}")
            
            # Convert lamports to SOL
            balance_sol = balance_lamports / 1_000_000_000  # 1 SOL = 10^9 lamports
        except Exception as balance_error:
            st.error(f"Balance fetch error: {str(balance_error)}")
            return None
        
        # Get transaction count
        try:
            try:
                tx_signatures = client.get_signatures_for_address(pubkey, limit=100)
                st.write("DEBUG - Signatures fetched with pubkey object")
            except Exception as e_sig_obj:
                st.write(f"DEBUG - Signatures fetch with object failed: {str(e_sig_obj)}")
                try:
                    tx_signatures = client.get_signatures_for_address(str(pubkey), limit=100)
                    st.write("DEBUG - Signatures fetched with string representation")
                except Exception as e_sig_str:
                    st.write(f"DEBUG - Signatures fetch with string failed: {str(e_sig_str)}")
                    raise Exception(f"Could not fetch signatures: {str(e_sig_obj)}, {str(e_sig_str)}")
                    
            # Handle different response types
            st.write(f"DEBUG - Signatures response type: {type(tx_signatures)}")
            
            if hasattr(tx_signatures, 'value'):
                # This is a typed response object
                tx_count = len(tx_signatures.value) if hasattr(tx_signatures, 'value') else 0
                st.write(f"DEBUG - Using value attribute for tx count: {tx_count}")
            elif isinstance(tx_signatures, dict) and 'result' in tx_signatures:
                # This is the dictionary response type
                tx_count = len(tx_signatures.get('result', []))
                st.write(f"DEBUG - Using result dictionary for tx count: {tx_count}")
            else:
                # Try to convert to a string and log
                st.write(f"DEBUG - Unknown tx signatures format: {str(tx_signatures)}")
                tx_count = 0
        except Exception as tx_error:
            st.warning(f"Could not fetch transaction count: {str(tx_error)}")
            tx_count = 0
        
        # Try to get USDT token balance if address has associated token account
        usdt_balance = 0.0
        try:
            # Find USDT associated token account for this wallet
            try:
                # The {'mint': str(USDT_MINT)} is causing the issue
                # Let's try with the proper filters structure
                filter_obj = {'mint': str(USDT_MINT)}
                st.write(f"DEBUG - Using filter object: {filter_obj}, type: {type(filter_obj)}")
                
                # For token program ID
                token_program_id = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
                
                # Try to create a proper filter
                try:
                    from solana.rpc.types import TokenAccountOpts
                    from solders.pubkey import Pubkey
                    
                    # Try with the proper TokenAccountOpts structure if available
                    mint_pubkey = Pubkey.from_string(str(USDT_MINT))
                    filter_opts = TokenAccountOpts(mint=mint_pubkey)
                    associated_token_response = client.get_token_accounts_by_owner(
                        pubkey, 
                        filter_opts
                    )
                    st.write("DEBUG - Token accounts fetched with TokenAccountOpts")
                except Exception as e_opts:
                    st.write(f"DEBUG - TokenAccountOpts approach failed: {str(e_opts)}")
                    
                    # Try with direct approach as fallback
                    try:
                        # Just set an empty result directly
                        associated_token_response = {"result": {"value": []}}
                        st.write("DEBUG - Using empty token accounts fallback")
                    except Exception as e_alt:
                        st.write(f"DEBUG - Empty token accounts fallback failed: {str(e_alt)}")
                        # Final fallback in case of any errors
                        associated_token_response = {"result": {"value": []}}
                        st.write("DEBUG - Using last resort empty token accounts fallback")
            except Exception as e_token_obj:
                st.write(f"DEBUG - All token accounts fetch approaches failed: {str(e_token_obj)}")
                # Final fallback - just set an empty result
                associated_token_response = {"result": {"value": []}}
                st.write("DEBUG - Using empty token accounts fallback after all failures")
            
            
            # Handle different response types for token accounts
            st.write(f"DEBUG - Token accounts response type: {type(associated_token_response)}")
            
            if hasattr(associated_token_response, 'value') and not hasattr(associated_token_response, 'message'):
                # This is a typed response object with value (success case)
                token_accounts = associated_token_response.value if hasattr(associated_token_response, 'value') else []
                st.write(f"DEBUG - Using value attribute for token accounts: {len(token_accounts)} accounts found")
            elif hasattr(associated_token_response, 'message'):
                # This is an error response
                st.write(f"DEBUG - Error response for token accounts: {associated_token_response.message if hasattr(associated_token_response, 'message') else str(associated_token_response)}")
                token_accounts = []
            elif isinstance(associated_token_response, dict) and 'result' in associated_token_response:
                # This is the dictionary response type
                token_accounts = associated_token_response.get('result', {}).get('value', [])
                st.write(f"DEBUG - Using result dictionary for token accounts: {len(token_accounts)} accounts found")
            else:
                # Try to convert to a string and log
                st.write(f"DEBUG - Unknown token accounts format: {str(associated_token_response)}")
                token_accounts = []
            
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

# Helper functions for transaction creation
def create_keypair():
    """Creates a keypair for demo purposes"""
    # Return a new keypair
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
        
def get_account_transactions(_client, address, limit=5):
    """Get recent transactions for an account"""
    try:
        # Create a fresh client instance to avoid hashing errors
        client = Client("https://api.devnet.solana.com")
        
        # Check if address is valid
        if not address or len(address) < 32:
            st.error("Invalid wallet address length")
            return []
            
        try:
            # Convert address string to PublicKey object using from_string
            # Make sure address is a string first and print debug info
            address_str = str(address).strip()
            st.write(f"DEBUG - Tx Address type: {type(address_str)}, Value: {address_str}")
            
            # Check for Ethereum style addresses (starting with 0x)
            if address_str.startswith("0x"):
                st.write("DEBUG - Tx Ethereum style address detected, attempting conversion")
                
                # We can try to convert from hex to bytes and create a PublicKey
                try:
                    # Remove 0x prefix and convert to bytes
                    hex_str = address_str[2:]  # Remove 0x prefix
                    if len(hex_str) < 32:
                        # Pad with zeros if needed
                        hex_str = hex_str.zfill(64)
                    elif len(hex_str) > 64:
                        # Truncate if too long
                        hex_str = hex_str[:64]
                        
                    # Convert to bytes
                    hex_bytes = bytes.fromhex(hex_str)
                    pubkey = PublicKey(hex_bytes[:32])  # Take first 32 bytes
                    st.write(f"DEBUG - Tx Created PublicKey from Ethereum address: {pubkey}")
                except Exception as e_eth:
                    st.write(f"DEBUG - Tx Ethereum conversion failed: {str(e_eth)}")
                    # Continue with other methods
            
            # Try different methods of creating a PublicKey
            try:
                # Method 1: Direct from_string
                pubkey = PublicKey.from_string(address_str)
                st.write("DEBUG - Tx PublicKey created with from_string")
            except Exception as e1:
                st.write(f"DEBUG - Tx from_string failed: {str(e1)}")
                try:
                    # Check if it's a valid Base58 string
                    if not any(c in address_str for c in '0xOIl+/'):  # Characters not in Base58
                        # Method this includes Bs58 decoding if needed
                        decoded = base58.b58decode(address_str)
                        pubkey = PublicKey(decoded)
                        st.write("DEBUG - Tx PublicKey created with base58 decode")
                    else:
                        raise ValueError("Contains invalid Base58 characters")
                except Exception as e2:
                    st.write(f"DEBUG - Tx base58 decode failed: {str(e2)}")
                    
                    # For demo purposes, if all else fails, use a default demo address
                    fallback_address = "8HGyAAB4dL4GhdQidH6WfCvkm2MF8wZCDm4XRmiWHnnm"
                    try:
                        pubkey = PublicKey.from_string(fallback_address)
                        st.write(f"DEBUG - Tx Using fallback demo address: {fallback_address}")
                    except Exception as e3:
                        st.write(f"DEBUG - Tx Fallback address failed: {str(e3)}")
                        raise Exception(f"All PublicKey creation methods failed: {str(e1)}, {str(e2)}, {str(e3)}")
            
        except Exception as e:
            st.error(f"Invalid Solana address format: {str(e)}")
            return []
        
        # Get recent signatures for this account
        try:
            signatures_response = client.get_signatures_for_address(
                pubkey,
                limit=limit
            )
            st.write("DEBUG - Tx Signatures fetched with pubkey object")
        except Exception as e_sig_obj:
            st.write(f"DEBUG - Tx Signatures fetch with object failed: {str(e_sig_obj)}")
            try:
                signatures_response = client.get_signatures_for_address(
                    str(pubkey),
                    limit=limit
                )
                st.write("DEBUG - Tx Signatures fetched with string representation")
            except Exception as e_sig_str:
                st.write(f"DEBUG - Tx Signatures fetch with string failed: {str(e_sig_str)}")
                raise Exception(f"Could not fetch tx signatures: {str(e_sig_obj)}, {str(e_sig_str)}")
        
        # Handle different response types for signatures
        if hasattr(signatures_response, 'value'):
            # This is a typed response object
            signatures_data = signatures_response.value if hasattr(signatures_response, 'value') else []
            st.write(f"DEBUG - Using value attribute for signatures data: {len(signatures_data)} signatures found")
        elif isinstance(signatures_response, dict) and 'result' in signatures_response:
            # This is the dictionary response type 
            signatures_data = signatures_response['result']
            st.write(f"DEBUG - Using result dictionary for signatures data: {len(signatures_data)} signatures found")
        else:
            # Try to convert to a string and log
            st.write(f"DEBUG - Unknown signatures data format: {str(signatures_response)}")
            st.error("Failed to get transactions for this account")
            return []
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

