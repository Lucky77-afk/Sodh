import streamlit as st
import re
import base58
from solders.pubkey import Pubkey as PublicKey

def validate_solana_address(address):
    """
    Validates if the provided string is a valid Solana address.
    
    Args:
        address: The Solana address to validate
        
    Returns:
        bool: True if address is valid, False otherwise
    """
    # First check: Basic regex pattern for Solana addresses (Base58 character set)
    pattern = r'^[1-9A-HJ-NP-Za-km-z]{32,44}$'
    if not re.match(pattern, address):
        return False
        
    # Second check: Try to create a PublicKey object
    try:
        # Verify the address can be properly decoded
        decoded = base58.b58decode(address)
        if len(decoded) != 32:
            return False
        
        # Create a PublicKey object
        PublicKey.from_string(address)
        return True
    except (ValueError, TypeError, Exception):
        return False

def validate_ethereum_address(address):
    """
    Validates if the provided string is a valid Ethereum address.
    
    Args:
        address: The Ethereum address to validate (with 0x prefix)
        
    Returns:
        bool: True if address is valid, False otherwise
    """
    # Check basic pattern for Ethereum addresses (0x followed by 40 hex chars)
    pattern = r'^0x[0-9a-fA-F]{40}$'
    if not re.match(pattern, address):
        return False
    
    # Additional checks could be added here, like EIP-55 checksum validation
    return True

def convert_eth_to_solana_pubkey(eth_address):
    """
    Converts an Ethereum address to a Solana PublicKey.
    
    Args:
        eth_address: The Ethereum address to convert (with 0x prefix)
        
    Returns:
        A Solana PublicKey object or None if conversion fails
    """
    try:
        # Remove 0x prefix
        hex_str = eth_address[2:]
        
        # Ethereum addresses are 20 bytes (40 hex chars)
        # Solana needs 32 bytes (64 hex chars)
        if len(hex_str) == 40:  # Standard Ethereum address length
            # Pad to 64 hex chars (32 bytes) by adding zeros at the end
            padded_hex = hex_str + '0' * 24
            
            # Convert to bytes
            hex_bytes = bytes.fromhex(padded_hex)
            
            # Create PublicKey
            return PublicKey(hex_bytes)
        else:
            return None
    except Exception:
        return None

def get_valid_pubkey(address):
    """
    Gets a valid Solana PublicKey from the input address, handling different formats.
    
    Args:
        address: The address string (Solana or Ethereum format)
        
    Returns:
        tuple: (pubkey, address_type, error_message)
            - pubkey: A PublicKey object if successful, None otherwise
            - address_type: "solana", "ethereum", or "invalid"
            - error_message: Error message if validation failed, None otherwise
    """
    if not address:
        return None, "invalid", "Address cannot be empty"
    
    address = str(address).strip()
    
    # Check if this is an Ethereum address
    if address.startswith("0x"):
        if validate_ethereum_address(address):
            pubkey = convert_eth_to_solana_pubkey(address)
            if pubkey:
                return pubkey, "ethereum", None
            else:
                return None, "ethereum", "Failed to convert Ethereum address to Solana format"
        else:
            return None, "invalid", "Invalid Ethereum address format"
    
    # Otherwise, treat as a Solana address
    elif validate_solana_address(address):
        try:
            pubkey = PublicKey.from_string(address)
            return pubkey, "solana", None
        except Exception as e:
            return None, "solana", f"Failed to create PublicKey: {str(e)}"
    else:
        return None, "invalid", "Invalid Solana address format"