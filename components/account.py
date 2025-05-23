import streamlit as st
import pandas as pd
import re
from datetime import datetime
from utils.solana_client_new import get_solana_client, get_account_info, get_account_transactions

def is_valid_solana_address(address):
    """Check if the address is a valid Solana wallet address"""
    if not address:
        return False
    # Solana addresses are base58 encoded and typically 32-44 characters long
    if not re.match(r'^[1-9A-HJ-NP-Za-km-z]{32,44}$', address):
        return False
    
    # Try to convert to Pubkey to verify validity
    try:
        from solders.pubkey import Pubkey
        Pubkey.from_string(address)
        return True
    except Exception:
        return False

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
        # Validate Solana address format
        if not is_valid_solana_address(wallet_address):
            st.error("❌ Invalid Solana wallet address. Please enter a valid Solana address.")
            st.info("Solana addresses are base58-encoded and typically 32-44 characters long (e.g., '9sQqDyg2mXX2cx3KVaqpCA1JmGhzi2LbfTfptEAjQ2zD')")
            return
            
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
                    st.error(f"Failed to fetch transactions: {str(e)}")
                
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
                # Show a more helpful message for empty accounts
                st.info("This wallet address exists on the Solana network but has no balance or associated data.")
                
                # Add helpful information
                st.markdown("""
                <div style="background-color: #1E1E1E; padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <div style="color: #9945FF; margin-bottom: 10px;">Wallet Status:</div>
                    <div style="color: #AAA;">
                        <div style="margin-bottom: 8px;">
                            <span style="color: #14F195; font-weight: bold;">✅ Valid Address</span>
                            <span style="color: #AAA;"> - This is a valid Solana wallet address</span>
                        </div>
                        <div style="margin-bottom: 8px;">
                            <span style="color: #FF5C5C; font-weight: bold;">❌ No Balance</span>
                            <span style="color: #AAA;"> - This wallet has no SOL balance</span>
                        </div>
                        <div style="margin-bottom: 8px;">
                            <span style="color: #FF5C5C; font-weight: bold;">❌ No Transactions</span>
                            <span style="color: #AAA;"> - This wallet has not made any transactions</span>
                        </div>
                    </div>
                </div>
                
                <div style="background-color: #1E1E1E; padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <div style="color: #9945FF; margin-bottom: 10px;">How to use this wallet:</div>
                    <div style="color: #AAA;">
                        1. To receive SOL: Share this address with others to receive SOL transfers<br>
                        2. To send SOL: Connect this wallet to a Solana wallet app (like Phantom) to send transactions<br>
                        3. To check balance: Connect this wallet to a wallet app or use a Solana explorer
                    </div>
                    <div style="margin-top: 10px;">
                        <a href="https://solana.com/wallet" target="_blank" style="color: #9945FF; text-decoration: none;">
                            Learn more about Solana wallets
                        </a>
                    </div>
                </div>
                
                <div style="background-color: #1E1E1E; padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <div style="color: #9945FF; margin-bottom: 10px;">Next Steps:</div>
                    <div style="color: #AAA;">
                        1. Get some SOL by:<br>
                        &nbsp;&nbsp;• Participating in airdrops<br>
                        &nbsp;&nbsp;• Trading on a DEX<br>
                        &nbsp;&nbsp;• Receiving transfers from others<br>
                        2. Connect to a wallet app to start sending transactions<br>
                        3. Use this address to receive payments and participate in projects
                    </div>
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error retrieving account data: {str(e)}")
    else:
        # Show instructions when no wallet is entered
        st.info("Enter a Solana wallet address to view account details and transactions.")
        
        # Display sample screenshots of the account view
        st.markdown("### Account Explorer Preview")
        st.image("https://images.unsplash.com/photo-1561525155-40a650192479", caption="Account Overview Sample")
