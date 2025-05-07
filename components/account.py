import streamlit as st
import pandas as pd
from datetime import datetime
from utils.solana_client_new import get_solana_client, get_account_info, get_account_transactions

def render_account():
    """Renders the account/wallet page with balance and transactions"""
    st.markdown('<h2>Account Explorer</h2>', unsafe_allow_html=True)
    
    # Get wallet address from session state or input
    if 'wallet_address' in st.session_state and st.session_state.wallet_address:
        wallet_address = st.session_state.wallet_address
        
        # Initialize wallet_type in session state if not already present
        if 'wallet_type' not in st.session_state:
            st.session_state['wallet_type'] = "Phantom"
            
        # Display wallet type selection
        wallet_options = ["Phantom", "Solflare", "Trust Wallet", "Binance", "CoinDCX", "Other"]
        wallet_index = wallet_options.index(st.session_state['wallet_type']) if st.session_state['wallet_type'] in wallet_options else 0
        
        wallet_type = st.selectbox(
            "Wallet Provider", 
            wallet_options,
            index=wallet_index
        )
        # Store the selected wallet type in session state
        st.session_state['wallet_type'] = wallet_type
    else:
        wallet_address = st.text_input("Enter a Solana wallet address to explore", placeholder="Solana wallet address...")
        
        # Add wallet provider selection when entering a new address
        if wallet_address:
            wallet_type = st.selectbox(
                "Select Wallet Provider", 
                ["Phantom", "Solflare", "Trust Wallet", "Binance", "CoinDCX", "Other"]
            )
            st.session_state['wallet_type'] = wallet_type

    # If wallet address is provided
    if wallet_address:
        try:
            client = get_solana_client()
            account_info = get_account_info(client, wallet_address)
            
            # Account overview section
            st.markdown("### Account Overview")
            
            # Get wallet type and display appropriate logo
            wallet_type = st.session_state.get('wallet_type', 'Other')
            
            # Determine logo and color based on wallet type
            logo_icon = "🔑"  # Default
            logo_color = "#FFFFFF"  # Default
            
            if wallet_type == "Phantom":
                logo_icon = "👻"
                logo_color = "#AB9FF2"
            elif wallet_type == "Solflare":
                logo_icon = "🔥"
                logo_color = "#FE8F44"
            elif wallet_type == "Trust Wallet":
                logo_icon = "🛡️"
                logo_color = "#3375BB"
            elif wallet_type == "Binance":
                logo_icon = "🔶"
                logo_color = "#F3BA2F"
            elif wallet_type == "CoinDCX":
                logo_icon = "🔷"
                logo_color = "#0052FF"
                
            # Wallet address with logo
            st.markdown(f"""
            <div style="margin-bottom: 16px;">
                <div style="font-size: 0.9rem; color: #AAA; margin-bottom: 4px;">
                    <span style="color: {logo_color}; margin-right: 8px;">{logo_icon}</span>
                    {wallet_type.upper()} WALLET ADDRESS
                </div>
                <div class="wallet-address">{wallet_address}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if account_info and account_info.get("value"):
                # Calculate SOL balance
                lamports = account_info.get("value", {}).get("lamports", 0)
                sol_balance = lamports / 1_000_000_000  # Convert lamports to SOL
                
                executable = account_info.get("value", {}).get("executable", False)
                account_type = "Program" if executable else "Wallet"
                
                # Display account metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="stCard">
                        <div style="font-size: 0.9rem; color: #AAA;">SOL BALANCE</div>
                        <div class="metric-value" style="font-size: 1.8rem;">{sol_balance:.9f}</div>
                        <div style="font-size: 0.8rem; color: #AAA;">≈ ${sol_balance * 165.32:.2f} USD</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    rent_epoch = account_info.get("value", {}).get("rentEpoch", 0)
                    st.markdown(f"""
                    <div class="stCard">
                        <div style="font-size: 0.9rem; color: #AAA;">ACCOUNT TYPE</div>
                        <div class="metric-value" style="font-size: 1.8rem;">{account_type}</div>
                        <div style="font-size: 0.8rem; color: #AAA;">Rent Epoch: {rent_epoch}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    owner = account_info.get("value", {}).get("owner", "Unknown")
                    st.markdown(f"""
                    <div class="stCard">
                        <div style="font-size: 0.9rem; color: #AAA;">OWNER</div>
                        <div class="metric-value" style="font-size: 1.2rem; word-break: break-all;">{owner}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Fetch recent transactions for this account
                st.markdown("### Recent Transactions")
                
                try:
                    account_txs = get_account_transactions(client, wallet_address)
                    
                    if account_txs:
                        for tx in account_txs:
                            signature = tx.get('signature', 'Unknown')
                            status = "Success" if tx.get('status', False) else "Failed"
                            status_class = "success" if status == "Success" else "error"
                            block_time = datetime.fromtimestamp(tx.get('blockTime', 0)).strftime("%Y-%m-%d %H:%M:%S") if tx.get('blockTime') else "Unknown"
                            
                            st.markdown(f"""
                            <div class="transaction-row">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <div>
                                        <div class="transaction-hash">{signature[:16]}...{signature[-8:]}</div>
                                        <div style="font-size: 0.8rem; color: #AAAAAA;">{block_time}</div>
                                    </div>
                                    <div>
                                        <span style="color: {'#14F195' if status == 'Success' else '#FF5C5C'}; font-size: 0.9rem;">
                                            {status}
                                        </span>
                                    </div>
                                </div>
                                <div style="margin-top: 8px; text-align: right;">
                                    <a href="https://explorer.solana.com/tx/{signature}" target="_blank" style="color: #9945FF; text-decoration: none; font-size: 0.8rem;">
                                        View on Solana Explorer
                                    </a>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No recent transactions found for this account")
                
                except Exception as e:
                    st.warning(f"Could not fetch transactions: {str(e)}")
                
                # Token holdings
                st.markdown("### Token Holdings")
                
                # This would normally come from a token balances API
                # For demonstration, we'll show placeholder/sample token data
                token_data = pd.DataFrame({
                    "Token": ["USDC", "RAY", "BONK"],
                    "Balance": ["125.00", "47.25", "15,000,000.00"],
                    "Value (USD)": ["$125.00", "$58.12", "$300.00"]
                })
                
                st.dataframe(token_data, use_container_width=True, hide_index=True)
                st.caption("Note: Token data is a sample representation")
                
            else:
                st.warning("Account not found or empty")
        except Exception as e:
            st.error(f"Error retrieving account data: {str(e)}")
    else:
        # Show instructions when no wallet is entered
        st.info("Enter a Solana wallet address to view account details and transactions.")
        
        # Display supported wallet types with icons
        st.markdown("### Supported Wallet Providers")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="text-align: center; padding: 15px; background-color: #1E1E1E; border-radius: 10px; margin-bottom: 10px;">
                <div style="font-size: 28px; margin-bottom: 8px;">👻</div>
                <div style="color: #AB9FF2; font-weight: bold;">Phantom</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="text-align: center; padding: 15px; background-color: #1E1E1E; border-radius: 10px;">
                <div style="font-size: 28px; margin-bottom: 8px;">🔥</div>
                <div style="color: #FE8F44; font-weight: bold;">Solflare</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 15px; background-color: #1E1E1E; border-radius: 10px; margin-bottom: 10px;">
                <div style="font-size: 28px; margin-bottom: 8px;">🛡️</div>
                <div style="color: #3375BB; font-weight: bold;">Trust Wallet</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="text-align: center; padding: 15px; background-color: #1E1E1E; border-radius: 10px;">
                <div style="font-size: 28px; margin-bottom: 8px;">🔶</div>
                <div style="color: #F3BA2F; font-weight: bold;">Binance</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div style="text-align: center; padding: 15px; background-color: #1E1E1E; border-radius: 10px; margin-bottom: 10px;">
                <div style="font-size: 28px; margin-bottom: 8px;">🔷</div>
                <div style="color: #0052FF; font-weight: bold;">CoinDCX</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="text-align: center; padding: 15px; background-color: #1E1E1E; border-radius: 10px;">
                <div style="font-size: 28px; margin-bottom: 8px;">🔑</div>
                <div style="color: #FFFFFF; font-weight: bold;">Other Wallets</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Display sample screenshots of the account view
        st.markdown("### Account Explorer Preview")
        st.image("https://images.unsplash.com/photo-1561525155-40a650192479", caption="Account Overview Sample")
