import streamlit as st
import pandas as pd
from datetime import datetime
from utils.solana_client import get_solana_client, get_account_info, get_account_transactions

def render_account():
    """Renders the account/wallet page with balance and transactions"""
    st.markdown('<h2>Account Explorer</h2>', unsafe_allow_html=True)
    
    # Get wallet address from session state or input
    if 'wallet_address' in st.session_state and st.session_state.wallet_address:
        wallet_address = st.session_state.wallet_address
    else:
        wallet_address = st.text_input("Enter a Solana wallet address to explore", placeholder="Solana wallet address...")

    # If wallet address is provided
    if wallet_address:
        try:
            client = get_solana_client()
            account_info = get_account_info(client, wallet_address)
            
            # Account overview section
            st.markdown("### Account Overview")
            
            # Wallet address
            st.markdown(f"""
            <div style="margin-bottom: 16px;">
                <div style="font-size: 0.9rem; color: #AAA; margin-bottom: 4px;">WALLET ADDRESS</div>
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
        
        # Display sample screenshots of the account view
        st.markdown("### Account Explorer Preview")
        st.image("https://images.unsplash.com/photo-1561525155-40a650192479", caption="Account Overview Sample")
