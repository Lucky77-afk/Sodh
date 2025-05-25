import streamlit as st
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

def get_account_data(address):
    """Get complete account data using direct RPC calls"""
    try:
        # Validate address format
        from utils.wallet_validator import get_valid_pubkey
        pubkey, address_type, error_msg = get_valid_pubkey(address)
        
        if error_msg:
            return None, f"Invalid address: {error_msg}"
        
        address_str = str(pubkey)
        
        # Get balance
        balance_result = make_rpc_call("getBalance", [address_str])
        if not balance_result or 'result' not in balance_result:
            return None, "Could not fetch balance"
        
        balance_lamports = balance_result['result']['value']
        balance_sol = balance_lamports / 1_000_000_000
        
        # Get transaction signatures
        tx_count = 0
        recent_transactions = []
        try:
            sigs_result = make_rpc_call("getSignaturesForAddress", [address_str, {"limit": 5}])
            if sigs_result and 'result' in sigs_result:
                tx_count = len(sigs_result['result'])
                recent_transactions = sigs_result['result']
        except:
            pass
        
        # Get USDT balance
        usdt_balance = 0.0
        try:
            token_result = make_rpc_call("getTokenAccountsByOwner", [
                address_str,
                {"mint": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"},
                {"encoding": "jsonParsed"}
            ])
            
            if token_result and 'result' in token_result:
                token_accounts = token_result['result']['value']
                if token_accounts:
                    token_account = token_accounts[0]['account']['data']['parsed']['info']
                    usdt_balance = float(token_account['tokenAmount']['uiAmount'] or 0)
        except:
            pass
        
        return {
            'address': address_str,
            'balance_sol': balance_sol,
            'balance_lamports': balance_lamports,
            'transaction_count': tx_count,
            'usdt_balance': usdt_balance,
            'address_type': address_type,
            'recent_transactions': recent_transactions
        }, None
        
    except Exception as e:
        return None, f"Error: {str(e)}"

def render_account():
    """Renders the account/wallet page with balance and transactions"""
    st.markdown('<h2>Account Explorer</h2>', unsafe_allow_html=True)
    st.markdown("Enter a Solana wallet address to explore")
    
    # Input field for wallet address
    wallet_address = st.text_input(
        "Wallet Address", 
        value=st.session_state.get('wallet_address', ''),
        placeholder="Solana wallet address",
        key="account_wallet_input",
        label_visibility="collapsed"
    )
    
    # Wallet provider selection
    provider_options = [
        "Select Wallet Provider",
        "Phantom",
        "Solflare", 
        "Sollet",
        "Slope",
        "Trust Wallet",
        "Binance Wallet",
        "CoinDCX Wallet",
        "Custom"
    ]
    
    selected_provider = st.selectbox(
        "Wallet Provider",
        provider_options,
        index=provider_options.index(st.session_state.get('wallet_provider', 'Solflare'))
    )
    
    # Store in session state
    if wallet_address:
        st.session_state['wallet_address'] = wallet_address
    if selected_provider != "Select Wallet Provider":
        st.session_state['wallet_provider'] = selected_provider

    # If wallet address is provided
    if wallet_address:
        with st.spinner("Loading account information..."):
            # Get account information
            account_data, error_msg = get_account_data(wallet_address)
            
            if error_msg:
                st.error(error_msg)
                return
            
            if not account_data:
                st.warning("Could not retrieve account information")
                return
        
        # Account overview section
        st.markdown("### Account Overview")
        
        # Display account information in a card format
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%);
                border: 1px solid #14F195;
                border-radius: 15px;
                padding: 20px;
                margin: 10px 0;
                box-shadow: 0 4px 15px rgba(20, 241, 149, 0.1);
            ">
                <h4 style="color: #14F195; margin: 0 0 15px 0;">🔥 {selected_provider.upper() if selected_provider else 'WALLET'} WALLET ADDRESS</h4>
                <p style="
                    color: #FFFFFF; 
                    font-family: 'Courier New', monospace; 
                    font-size: 14px; 
                    word-break: break-all;
                    background: #0a0a0a;
                    padding: 10px;
                    border-radius: 8px;
                    border: 1px solid #333;
                    margin: 0;
                ">{wallet_address}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Display balance and transaction info
            balance_sol = account_data['balance_sol']
            balance_lamports = account_data['balance_lamports']
            tx_count = account_data['transaction_count']
            usdt_balance = account_data['usdt_balance']
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%);
                border: 1px solid #9945FF;
                border-radius: 15px;
                padding: 20px;
                margin: 10px 0;
                box-shadow: 0 4px 15px rgba(153, 69, 255, 0.1);
            ">
                <h4 style="color: #9945FF; margin: 0 0 15px 0;">💰 Balance Information</h4>
                <p style="color: #FFFFFF; margin: 5px 0;">
                    <strong>SOL Balance:</strong> 
                    <span style="color: #14F195; font-family: monospace;">{balance_sol:.9f} SOL</span>
                </p>
                <p style="color: #FFFFFF; margin: 5px 0;">
                    <strong>Lamports:</strong> 
                    <span style="color: #14F195; font-family: monospace;">{balance_lamports:,}</span>
                </p>
                <p style="color: #FFFFFF; margin: 5px 0;">
                    <strong>Recent Transactions:</strong> 
                    <span style="color: #14F195; font-family: monospace;">{tx_count}</span>
                </p>
                {f'<p style="color: #FFFFFF; margin: 5px 0;"><strong>USDT Balance:</strong> <span style="color: #14F195; font-family: monospace;">{usdt_balance:.6f} USDT</span></p>' if usdt_balance > 0 else ''}
            </div>
            """, unsafe_allow_html=True)
        
        # Show recent transactions if available
        recent_transactions = account_data.get('recent_transactions', [])
        if recent_transactions:
            st.markdown("### Recent Transactions")
            
            for i, tx_info in enumerate(recent_transactions):
                signature = tx_info['signature']
                slot = tx_info.get('slot', 0)
                status = 'Success' if not tx_info.get('err') else 'Failed'
                block_time = tx_info.get('blockTime')
                
                # Format timestamp
                if block_time:
                    tx_time = datetime.fromtimestamp(block_time).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    tx_time = 'Unknown'
                
                # Color based on status
                status_color = "#14F195" if status == "Success" else "#FF6B6B"
                
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #1a1a1a 0%, #252525 100%);
                    border: 1px solid #333;
                    border-radius: 10px;
                    padding: 15px;
                    margin: 10px 0;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <h5 style="color: #14F195; margin: 0;">Transaction #{i+1}</h5>
                        <span style="
                            background: {status_color}; 
                            color: #000; 
                            padding: 4px 8px; 
                            border-radius: 12px; 
                            font-size: 12px; 
                            font-weight: bold;
                        ">{status}</span>
                    </div>
                    
                    <p style="color: #CCCCCC; margin: 5px 0; font-size: 12px;">
                        <strong>Signature:</strong> 
                        <span style="font-family: monospace; word-break: break-all;">{signature[:20]}...{signature[-20:]}</span>
                    </p>
                    
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #AAAAAA; font-size: 12px;">Slot: {slot:,}</span>
                        <span style="color: #AAAAAA; font-size: 12px;">{tx_time}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("### Recent Transactions")
            st.info("No recent transactions found for this address")
            
    else:
        st.info("Enter a wallet address above to view account details")