import streamlit as st
import pandas as pd
from datetime import datetime
import json
from utils.solana_client_robust import get_solana_client, get_account_info_robust, get_recent_transactions_robust

def format_lamports(lamports):
    """Convert lamports to SOL with proper formatting"""
    return lamports / 1_000_000_000

def format_timestamp(timestamp):
    """Format timestamp to human-readable format"""
    if not timestamp:
        return "N/A"
    try:
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except (TypeError, ValueError):
        return str(timestamp)

def get_wallet_icon(wallet_type):
    """Get wallet icon and color based on wallet type"""
    wallet_icons = {
        "Phantom": ("👻", "#AB9FF2"),
        "Solflare": ("🔥", "#FE8F44"),
        "Trust Wallet": ("🛡️", "#3375BB"),
        "Binance": ("🔶", "#F3BA2F"),
        "CoinDCX": ("🔷", "#0052FF"),
    }
    return wallet_icons.get(wallet_type, ("🔑", "#FFFFFF"))

def render_transaction_card(tx):
    """Render a transaction card with consistent styling"""
    with st.container():
        st.markdown("""
        <style>
            .tx-card {
                background-color: #1E1E1E;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 16px;
                border-left: 4px solid #14F195;
            }
            .tx-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12px;
            }
            .tx-title {
                font-size: 16px;
                font-weight: 600;
                color: #FFFFFF;
                margin: 0;
            }
            .tx-status {
                font-size: 14px;
                font-weight: 500;
                padding: 4px 8px;
                border-radius: 4px;
                background-color: rgba(20, 241, 149, 0.2);
                color: #14F195;
            }
            .tx-metric {
                font-size: 14px;
                color: #AAAAAA;
                margin: 4px 0;
            }
            .tx-metric-value {
                font-weight: 600;
                color: #FFFFFF;
            }
            .wallet-address {
                font-family: 'Roboto Mono', monospace;
                background-color: #2A2A2A;
                padding: 8px 12px;
                border-radius: 4px;
                margin: 8px 0;
                word-break: break-all;
                font-size: 14px;
            }
        </style>
        """, unsafe_allow_html=True)
        
        signature = tx.get('signature', 'Unknown')
        short_sig = f"{signature[:8]}...{signature[-8:]}" if len(signature) > 20 else signature
        
        st.markdown(f"""
        <div class="tx-card">
            <div class="tx-header">
                <h3 class="tx-title">Transaction</h3>
                <span class="tx-status">✓ Success</span>
            </div>
            
            <div class="tx-metric">Signature:</div>
            <div class="wallet-address">{short_sig}</div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 16px; margin-top: 12px;">
                <div>
                    <div class="tx-metric">SLOT</div>
                    <div class="tx-metric-value">{slot}</div>
                </div>
                <div>
                    <div class="tx-metric">TIME</div>
                    <div class="tx-metric-value">{time}</div>
                </div>
            </div>
        </div>
        """.format(
            signature=signature,
            short_sig=short_sig,
            slot=tx.get('slot', 'N/A'),
            time=format_timestamp(tx.get('blockTime'))
        ), unsafe_allow_html=True)

def render_account():
    """Renders the account/wallet page with balance and transactions"""
    st.markdown("# 👤 Account Explorer")
    
    # Get wallet address from session state or input
    if 'wallet_address' in st.session_state and st.session_state.wallet_address:
        wallet_address = st.session_state.wallet_address
        
        # Initialize wallet_type in session state if not already present
        if 'wallet_type' not in st.session_state:
            st.session_state['wallet_type'] = "Solflare"
            
        # Display wallet type selection
        wallet_options = ["Solflare", "Phantom", "Trust Wallet", "Binance", "CoinDCX", "Other"]
        wallet_index = wallet_options.index(st.session_state['wallet_type']) if st.session_state['wallet_type'] in wallet_options else 0
        
        wallet_type = st.selectbox(
            "Wallet Provider", 
            wallet_options,
            index=wallet_index,
            key="wallet_type_selector"
        )
        # Store the selected wallet type in session state
        st.session_state['wallet_type'] = wallet_type
    else:
        wallet_address = st.text_input(
            "Enter a Solana wallet address to explore", 
            placeholder="Solana wallet address...",
            key="wallet_address_input"
        )
        
        # Add wallet provider selection when entering a new address
        if wallet_address:
            wallet_type = st.selectbox(
                "Select Wallet Provider", 
                ["Solflare", "Phantom", "Trust Wallet", "Binance", "CoinDCX", "Other"],
                key="wallet_provider_selector"
            )
            st.session_state['wallet_type'] = wallet_type
            st.session_state['wallet_address'] = wallet_address
            st.experimental_rerun()

    # If wallet address is provided
    if wallet_address:
        try:
            # Add custom CSS for the page
            st.markdown("""
            <style>
                .metric-card {
                    background-color: #1E1E1E;
                    border-radius: 8px;
                    padding: 16px;
                    margin-bottom: 16px;
                }
                .metric-label {
                    font-size: 0.9rem;
                    color: #AAAAAA;
                    margin-bottom: 4px;
                }
                .metric-value {
                    font-size: 1.8rem;
                    font-weight: 600;
                    color: #FFFFFF;
                }
                .usd-value {
                    font-size: 0.9rem;
                    color: #888888;
                }
            </style>
            """, unsafe_allow_html=True)
            
            client = get_solana_client()
            account_info = get_account_info_robust(wallet_address)
            
            # Account overview section
            st.markdown("## Account Overview")
            
            # Get wallet type and display appropriate logo
            wallet_type = st.session_state.get('wallet_type', 'Other')
            logo_icon, logo_color = get_wallet_icon(wallet_type)
            
            # Wallet address section
            st.markdown(f"""
            <div style="margin-bottom: 24px;">
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 1.2rem; margin-right: 8px; color: {logo_color};">{logo_icon}</span>
                    <span style="font-size: 0.9rem; color: #AAAAAA; text-transform: uppercase;">{wallet_type} Wallet</span>
                </div>
                <div class="wallet-address">{wallet_address}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if account_info and account_info.get("value"):
                # Calculate SOL balance
                lamports = account_info.get("value", {}).get("lamports", 0)
                sol_balance = format_lamports(lamports)
                
                # Display account metrics in a grid
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">SOL BALANCE</div>
                        <div class="metric-value">{sol_balance:.9f}</div>
                        <div class="usd-value">≈ ${sol_balance * 165.32:,.2f} USD</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    rent_epoch = account_info.get("value", {}).get("rentEpoch", 0)
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">ACCOUNT TYPE</div>
                        <div class="metric-value">{"Wallet" if account_info.get("value", {}).get("executable") == False else "Program"}</div>
                        <div class="usd-value">Rent Epoch: {rent_epoch}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    owner = account_info.get("value", {}).get("owner", "Unknown")
                    short_owner = f"{owner[:6]}...{owner[-4:]}" if len(owner) > 10 else owner
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">OWNER</div>
                        <div class="metric-value" style="font-size: 1.2rem;">{short_owner}</div>
                        <div class="usd-value">
                            <a href="https://explorer.solana.com/address/{owner}" target="_blank" style="color: #9945FF; text-decoration: none;">
                                View on Explorer
                            </a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Fetch recent transactions for this account
                st.markdown("## Recent Transactions")
                
                try:
                    account_txs = get_recent_transactions_robust(wallet_address)
                    
                    if account_txs:
                        for tx in account_txs:
                            # Use our new transaction card component
                            render_transaction_card(tx)
                    else:
                        st.info("No recent transactions found for this account")
                
                except Exception as e:
                    st.warning(f"Could not fetch transactions: {str(e)}")
                
                # Token holdings section
                st.markdown("## Token Holdings")
                
                # Sample token data - in a real app, this would come from an API
                token_data = pd.DataFrame({
                    "Token": ["USDC", "RAY", "BONK"],
                    "Balance": [125.00, 47.25, 15000000.00],
                    "Value (USD)": [125.00, 58.12, 300.00]
                })
                
                # Format the DataFrame for display
                display_data = token_data.copy()
                display_data["Balance"] = display_data["Balance"].apply(lambda x: f"{x:,.2f}" if x < 1000 else f"{x:,.0f}")
                display_data["Value (USD)"] = display_data["Value (USD)"].apply(lambda x: f"${x:,.2f}")
                
                # Display the styled DataFrame
                st.dataframe(
                    display_data,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Token": st.column_config.TextColumn("TOKEN"),
                        "Balance": st.column_config.TextColumn("BALANCE"),
                        "Value (USD)": st.column_config.TextColumn("VALUE (USD)")
                    }
                )
                
                st.caption("Note: Token data is a sample representation. Real-time data coming soon.")
                
            else:
                st.warning("Account not found or empty")
        except Exception as e:
            st.error(f"Error retrieving account data: {str(e)}")
    else:
        # Show instructions when no wallet is entered
        st.info("Enter a Solana wallet address to view account details and transactions.")
        
        # Add custom CSS for the wallet selection cards
        st.markdown("""
        <style>
            .wallet-card {
                text-align: center;
                padding: 20px;
                background-color: #1E1E1E;
                border-radius: 10px;
                margin-bottom: 15px;
                transition: all 0.3s ease;
                border: 1px solid #2A2A2A;
            }
            .wallet-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                border-color: #444;
            }
            .wallet-icon {
                font-size: 32px;
                margin-bottom: 10px;
            }
            .wallet-name {
                font-weight: 600;
                margin-bottom: 5px;
            }
            .wallet-desc {
                font-size: 12px;
                color: #888;
                margin-top: 5px;
            }
            .section-title {
                font-size: 1.25rem;
                font-weight: 600;
                margin: 20px 0 15px 0;
                color: #FFFFFF;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Main content container
        st.markdown("""
        <div style="max-width: 900px; margin: 0 auto;">
            <h2 style="text-align: center; margin-bottom: 30px;">Explore Solana Wallets</h2>
            <p style="text-align: center; color: #AAA; margin-bottom: 30px;">
                Enter a wallet address or connect with one of the supported providers to view account details, 
                transaction history, and token balances.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Wallet cards in a grid
        st.markdown("<div class='section-title'>Connect Your Wallet</div>", unsafe_allow_html=True)
        
        # Wallet provider cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="wallet-card">
                <div class="wallet-icon">👻</div>
                <div class="wallet-name" style="color: #AB9FF2;">Phantom</div>
                <div class="wallet-desc">Most popular Solana wallet</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="wallet-card">
                <div class="wallet-icon">🛡️</div>
                <div class="wallet-name" style="color: #3375BB;">Trust Wallet</div>
                <div class="wallet-desc">Secure multi-chain wallet</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="wallet-card">
                <div class="wallet-icon">🔥</div>
                <div class="wallet-name" style="color: #FE8F44;">Solflare</div>
                <div class="wallet-desc">Lightweight & secure</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="wallet-card">
                <div class="wallet-icon">🔶</div>
                <div class="wallet-name" style="color: #F3BA2F;">Binance</div>
                <div class="wallet-desc">Exchange wallet</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class="wallet-card">
                <div class="wallet-icon">🔷</div>
                <div class="wallet-name" style="color: #0052FF;">CoinDCX</div>
                <div class="wallet-desc">Indian exchange wallet</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="wallet-card">
                <div class="wallet-icon">🔑</div>
                <div class="wallet-name">Other Wallets</div>
                <div class="wallet-desc">Connect any Solana wallet</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Manual address input section
        st.markdown("<div style='margin: 30px 0 15px 0;' class='section-title'>Or Enter Wallet Address Manually</div>", unsafe_allow_html=True)
        
        # Add a form for better UX with the input field
        with st.form("wallet_address_form"):
            wallet_address = st.text_input(
                "Solana Wallet Address",
                placeholder="Enter a Solana wallet address...",
                key="wallet_address_input_manual"
            )
            
            wallet_type = st.selectbox(
                "Select Wallet Provider", 
                ["Solflare", "Phantom", "Trust Wallet", "Binance", "CoinDCX", "Other"],
                key="wallet_provider_manual"
            )
            
            if st.form_submit_button("View Wallet"):
                if wallet_address:
                    st.session_state['wallet_address'] = wallet_address
                    st.session_state['wallet_type'] = wallet_type
                    st.experimental_rerun()
        
        # Add some helpful information
        st.markdown("""
        <div style="margin-top: 40px; padding: 20px; background-color: #1E1E1E; border-radius: 10px;">
            <h3 style="color: #FFFFFF; margin-top: 0;">About Solana Wallets</h3>
            <p style="color: #AAA; margin-bottom: 15px;">
                A Solana wallet is your gateway to the Solana blockchain, allowing you to store, send, 
                and receive SOL and other SPL tokens. Each wallet has a unique address that identifies it on the network.
            </p>
            <div style="display: flex; justify-content: space-between; margin-top: 20px;">
                <div style="flex: 1; padding-right: 15px;">
                    <div style="color: #14F195; font-weight: 600; margin-bottom: 5px;">Secure</div>
                    <div style="font-size: 0.85rem; color: #888;">Your private keys stay on your device</div>
                </div>
                <div style="flex: 1; padding: 0 15px; border-left: 1px solid #2A2A2A;">
                    <div style="color: #14F195; font-weight: 600; margin-bottom: 5px;">Fast</div>
                    <div style="font-size: 0.85rem; color: #888;">Instant transactions with low fees</div>
                </div>
                <div style="flex: 1; padding-left: 15px; border-left: 1px solid #2A2A2A;">
                    <div style="color: #14F195; font-weight: 600; margin-bottom: 5px;">Decentralized</div>
                    <div style="font-size: 0.85rem; color: #888;">You control your funds and data</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
