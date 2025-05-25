"""
Solana wallet address validation utilities.
"""
import re
from solders.pubkey import Pubkey

def is_valid_solana_address(address: str) -> bool:
    """
    Check if a string is a valid Solana wallet address.
    
    Args:
        address (str): The address to validate
        
    Returns:
        bool: True if the address is valid, False otherwise
    """
    if not address or not isinstance(address, str):
        return False
    
    # Basic length check (Solana addresses are 43-44 base58 chars)
    if len(address) < 32 or len(address) > 44:
        return False
    
    # Check if it's a base58 string
    if not re.match(r'^[1-9A-HJ-NP-Za-km-z]+$', address):
        return False
    
    # Try to create a Pubkey from the address
    try:
        Pubkey.from_string(address)
        return True
    except:
        return False
