import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import time
from utils.solana_client import get_solana_client, get_latest_block_time
from utils.database import get_recent_transactions
from solders.rpc.responses import Blockhash, GetBlockHeightResp, GetEpochInfoResp, GetVoteAccountsResp, RpcBlockhashResp, RpcContext, RpcResponse, RpcResultWithContext, RpcVersionInfo, RpcVoteAccountInfo, RpcVoteAccountStatus

def _get_supply_info(client):
    """Helper function to get supply info from client"""
    try:
        supply_info = client.get_supply()
        
        # Handle solders response
        if hasattr(supply_info, 'value'):
            supply_value = supply_info.value
            if hasattr(supply_value, 'value') and hasattr(supply_value.value, 'total'):
                return supply_value.value.total / 1_000_000_000
        return 580.0  # Fallback value
    except Exception as e:
        st.warning(f"Could not retrieve SOL supply data: {str(e)}")
        return 580.0

def _get_epoch_info(client):
    """Helper function to get epoch info from client"""
    try:
        epoch_info = client.get_epoch_info()
        
        # Handle solders response
        if hasattr(epoch_info, 'value'):
            value = epoch_info.value
            if hasattr(value, 'epoch') and hasattr(value, 'slot_index') and hasattr(value, 'slots_in_epoch'):
                epoch = value.epoch
                slot_index = value.slot_index
                slots_in_epoch = value.slots_in_epoch or 1
                progress = (slot_index / slots_in_epoch) * 100 if slots_in_epoch > 0 else 0
                return epoch, progress
        return 0, 0
    except Exception as e:
        st.warning(f"Could not retrieve epoch data: {str(e)}")
        return 0, 0

def render_dashboard():
    """Renders the dashboard with blockchain metrics and visualizations"""
    st.markdown('<h2>Solana Network Dashboard</h2>', unsafe_allow_html=True)
    
    # Load Solana client
    client = get_solana_client()
    
    # Get network stats with better error handling
    try:
        # Get supply info
        supply = _get_supply_info(client)
        
        # Get epoch info
        current_epoch, epoch_progress = _get_epoch_info(client)
        
        # Get validator count
        active_validators = 0
        try:
            validators_response = client.get_vote_accounts()
            
            # Handle solders response
            if hasattr(validators_response, 'value'):
                value = validators_response.value
                current_validators = getattr(value, 'current', None) or []
                delinquent_validators = getattr(value, 'delinquent', None) or []
                active_validators = len(current_validators) + len(delinquent_validators)
            elif isinstance(validators_response, dict) and 'result' in validators_response:
                result = validators_response['result']
                if isinstance(result, dict):
                    current_validators = result.get('current', [])
                    delinquent_validators = result.get('delinquent', [])
                    active_validators = len(current_validators) + len(delinquent_validators)
            else:
                st.warning("Could not parse validator data")
        except Exception as e:
            st.warning(f"Could not retrieve validator data: {str(e)}")
            active_validators = 1000  # Fallback value
        
        # Get transaction count
        try:
            tx_count_response = client.get_transaction_count()
            if hasattr(tx_count_response, 'value'):
                tx_count = tx_count_response.value
            elif isinstance(tx_count_response, dict) and 'result' in tx_count_response:
                tx_count = tx_count_response['result']
            else:
                tx_count = 0
                st.warning("Failed to parse transaction count response")
        except Exception as e:
            tx_count = 0
            st.warning(f"Could not retrieve transaction count: {str(e)}")
        
        # Set health status based on network connection
        health_status = "✅ Operational"
        try:
            # Get recent blockhash as a way to check network health
            blockhash_response = client.get_latest_blockhash()
            if not blockhash_response or not hasattr(blockhash_response, 'value'):
                health_status = "⚠️ Degraded"
        except Exception as e:
            health_status = "⚠️ Degraded"
            st.warning(f"Could not check network health: {str(e)}")
        
        # Create dashboard metrics in three columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="stCard">
                <div style="font-size: 0.9rem; color: #AAA;">SOLANA PRICE</div>
                <div class="metric-value" style="font-size: 1.8rem;">$165.32</div>
                <div style="font-size: 0.8rem; color: #00FFA3;">+2.4% (24h)</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="stCard">
                <div style="font-size: 0.9rem; color: #AAA;">CURRENT EPOCH</div>
                <div class="metric-value" style="font-size: 1.8rem;">{}</div>
                <div style="font-size: 0.8rem; color: #AAA;">Progress: {:.1f}%</div>
            </div>
            """.format(current_epoch, epoch_progress), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="stCard">
                <div style="font-size: 0.9rem; color: #AAA;">TRANSACTIONS</div>
                <div class="metric-value" style="font-size: 1.8rem;">{:,}</div>
                <div style="font-size: 0.8rem; color: #AAA;">All-time count</div>
            </div>
            """.format(tx_count), unsafe_allow_html=True)
            
            st.markdown("""
            <div class="stCard">
                <div style="font-size: 0.9rem; color: #AAA;">TOTAL SUPPLY</div>
                <div class="metric-value" style="font-size: 1.8rem;">{:,.2f} SOL</div>
                <div style="font-size: 0.8rem; color: #AAA;">Circulating</div>
            </div>
            """.format(supply), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="stCard">
                <div style="font-size: 0.9rem; color: #AAA;">NETWORK STATUS</div>
                <div class="metric-value" style="font-size: 1.8rem;">{}</div>
                <div style="font-size: 0.8rem; color: #AAA;">Current status</div>
            </div>
            """.format(health_status), unsafe_allow_html=True)
            
            st.markdown("""
            <div class="stCard">
                <div style="font-size: 0.9rem; color: #AAA;">VALIDATORS</div>
                <div class="metric-value" style="font-size: 1.8rem;">{}</div>
                <div style="font-size: 0.8rem; color: #AAA;">Active nodes</div>
            </div>
            """.format(active_validators), unsafe_allow_html=True)
        
        # Performance metrics
        st.markdown("### Network Performance", unsafe_allow_html=True)
        perf_col1, perf_col2 = st.columns(2)
        
        with perf_col1:
            # Transaction per second chart
            now = datetime.now()
            times = [(now - timedelta(minutes=i)).strftime("%H:%M") for i in range(20, 0, -1)]
            
            # Calculate realistic TPS values based on Solana's capabilities
            base_tps = 2500
            variation = 500
            tps_values = [max(0, base_tps + random.randint(-variation, variation)) for _ in range(20)]
            
            tps_df = pd.DataFrame({
                'Time': times,
                'TPS': tps_values
            })
            
            fig = px.line(tps_df, x='Time', y='TPS', title='Transactions Per Second (Sample Data)')
            fig.update_layout(
                plot_bgcolor='#1E1E1E',
                paper_bgcolor='#1E1E1E',
                font=dict(color='#FFFFFF'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#333333'),
                margin=dict(l=10, r=10, t=40, b=10),
                height=300
            )
            fig.update_traces(line=dict(color='#14F195', width=3))
            st.plotly_chart(fig, use_container_width=True)
            
            with perf_col2:
                # Block time chart with sample data
                now = datetime.now()
                times = [(now - timedelta(minutes=i)).strftime("%H:%M") for i in range(20, 0, -1)]
                block_times = [random.uniform(0.4, 0.6) for _ in range(20)]  # Sample block times in seconds
                
                block_time_df = pd.DataFrame({
                    'Time': times,
                    'Block Time (s)': block_times
                })
                
                fig = px.line(block_time_df, x='Time', y='Block Time (s)', title='Block Times (Sample Data)')
                fig.update_layout(
                    plot_bgcolor='#1E1E1E',
                    paper_bgcolor='#1E1E1E',
                    font=dict(color='#FFFFFF'),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor='#333333'),
                    margin=dict(l=10, r=10, t=40, b=10),
                    height=300
                )
                fig.update_traces(line=dict(color='#9945FF', width=3))
                st.plotly_chart(fig, use_container_width=True)
        
        # Local database transactions
        st.markdown("### Local Database Transactions", unsafe_allow_html=True)
        
        # Get database transactions
        db_transactions = get_recent_transactions(limit=5)
        
        if db_transactions and len(db_transactions) > 0:
            # Format transaction data for display
            tx_disp_data = {
                'Signature': [],
                'Type': [],
                'Status': [],
                'Timestamp': []
            }
            
            for tx in db_transactions:
                # Format signature for display (truncate)
                sig = tx['signature']
                short_sig = f"{sig[:8]}...{sig[-8:]}" if len(sig) > 16 else sig
                
                # Format timestamp
                timestamp = tx.get('created_at', 'N/A')
                
                # Add to display data
                tx_disp_data['Signature'].append(short_sig)
                tx_disp_data['Type'].append(tx.get('tx_type', 'Unknown'))
                tx_disp_data['Status'].append(tx.get('status', 'Unknown'))
                tx_disp_data['Timestamp'].append(timestamp)
            
            # Create dataframe
            tx_df = pd.DataFrame(tx_disp_data)
            
            # Add color styling to status column
            def color_status(val):
                color = '#14F195' if val == 'Confirmed' else '#FF5C5C'
                return f'color: {color}'
            
            # Display styled dataframe
            st.dataframe(
                tx_df.style.applymap(color_status, subset=['Status']),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No transactions found in the database. Create a project, milestone, or participant to see transactions here.")
        
        # Token metrics with a tab selection for main view
        st.markdown("### Token Dashboard", unsafe_allow_html=True)
        
        # Create tabs for different token views
        token_tabs = st.tabs(["Top Tokens", "SOL", "USDT"])
        
        with token_tabs[0]:
            # Top tokens tab
            st.markdown("#### Top Solana Tokens", unsafe_allow_html=True)
            
            # Sample token data (in a real app, this would come from an API)
            token_data = {
                'Token': ['SOL', 'USDT', 'USDC', 'BONK', 'JUP', 'RAY', 'ORCA'],
                'Price': ['$165.32', '$1.00', '$1.00', '$0.00002', '$0.82', '$1.23', '$0.57'],
                'Change': ['+2.4%', '+0.0%', '+0.1%', '+15.2%', '-3.1%', '+5.7%', '-1.2%'],
                'Volume': ['$1.2B', '$872M', '$453M', '$112M', '$87M', '$45M', '$23M'],
                'Market Cap': ['$68.9B', '$43.2B', '$24.7B', '$1.2B', '$827M', '$245M', '$115M'],
            }
            
            token_df = pd.DataFrame(token_data)
            
            # Add color styling to change column
            def color_change(val):
                color = '#00FFA3' if '+' in val else ('#FF5C5C' if '-' in val else '#AAAAAA')
                return f'color: {color}'
            
            # Display styled dataframe
            st.dataframe(
                token_df.style.applymap(color_change, subset=['Change']),
                use_container_width=True,
                hide_index=True
            )
            
        with token_tabs[1]:
            # SOL specific tab
            st.markdown("#### SOL Token Details", unsafe_allow_html=True)
            
            # Create two columns for statistics and chart
            sol_col1, sol_col2 = st.columns([1, 2])
            
            with sol_col1:
                # SOL statistics
                st.markdown("""
                <div class="stCard">
                    <div style="font-size: 0.9rem; color: #AAA;">CURRENT PRICE</div>
                    <div class="metric-value" style="font-size: 1.8rem;">$165.32</div>
                    <div style="font-size: 0.8rem; color: #00FFA3;">+2.4% (24h)</div>
                </div>
                
                <div class="stCard">
                    <div style="font-size: 0.9rem; color: #AAA;">MARKET CAP</div>
                    <div class="metric-value" style="font-size: 1.8rem;">$68.9B</div>
                    <div style="font-size: 0.8rem; color: #AAA;">Rank #5</div>
                </div>
                
                <div class="stCard">
                    <div style="font-size: 0.9rem; color: #AAA;">TRADING VOLUME (24H)</div>
                    <div class="metric-value" style="font-size: 1.8rem;">$1.2B</div>
                    <div style="font-size: 0.8rem; color: #00FFA3;">+12.3%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with sol_col2:
                # SOL price chart for the last week
                dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7, 0, -1)]
                
                # Mock price data with a trend
                base_price = 165.32
                price_trend = [
                    base_price * 0.92,  # 7 days ago
                    base_price * 0.95,
                    base_price * 0.99,
                    base_price * 0.96,
                    base_price * 1.02,
                    base_price * 1.05,
                    base_price,         # Today
                ]
                
                # Create dataframe for chart
                sol_price_df = pd.DataFrame({
                    'Date': dates,
                    'Price': price_trend
                })
                
                # Create the chart
                fig = px.line(sol_price_df, x='Date', y='Price', title='SOL Price (7 Day)')
                fig.update_layout(
                    plot_bgcolor='#1E1E1E',
                    paper_bgcolor='#1E1E1E',
                    font=dict(color='#FFFFFF'),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor='#333333', title='Price (USD)'),
                    margin=dict(l=10, r=10, t=40, b=10),
                    height=300
                )
                fig.update_traces(line=dict(color='#14F195', width=3))
                st.plotly_chart(fig, use_container_width=True)
                
        with token_tabs[2]:
            # USDT specific tab
            st.markdown("#### USDT (Tether) Token Details", unsafe_allow_html=True)
            
            # Create two columns for statistics and chart
            usdt_col1, usdt_col2 = st.columns([1, 2])
            
            with usdt_col1:
                # USDT statistics
                st.markdown("""
                <div class="stCard">
                    <div style="font-size: 0.9rem; color: #AAA;">CURRENT PRICE</div>
                    <div class="metric-value" style="font-size: 1.8rem;">$1.00</div>
                    <div style="font-size: 0.8rem; color: #AAAAAA;">+0.0% (24h)</div>
                </div>
                
                <div class="stCard">
                    <div style="font-size: 0.9rem; color: #AAA;">MARKET CAP</div>
                    <div class="metric-value" style="font-size: 1.8rem;">$43.2B</div>
                    <div style="font-size: 0.8rem; color: #AAA;">Rank #3</div>
                </div>
                
                <div class="stCard">
                    <div style="font-size: 0.9rem; color: #AAA;">TRADING VOLUME (24H)</div>
                    <div class="metric-value" style="font-size: 1.8rem;">$872M</div>
                    <div style="font-size: 0.8rem; color: #00FFA3;">+4.1%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with usdt_col2:
                # USDT price chart for the last week (should be stable around $1)
                dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7, 0, -1)]
                
                # Mock price data with very minor fluctuations (stablecoin)
                base_price = 1.00
                price_trend = [
                    base_price * 0.998,  # 7 days ago
                    base_price * 1.001,
                    base_price * 0.999,
                    base_price * 0.997,
                    base_price * 1.002,
                    base_price * 1.001,
                    base_price,         # Today
                ]
                
                # Create dataframe for chart
                usdt_price_df = pd.DataFrame({
                    'Date': dates,
                    'Price': price_trend
                })
                
                # Create the chart with a very narrow y-axis range to show the tiny fluctuations
                fig = px.line(usdt_price_df, x='Date', y='Price', title='USDT Price (7 Day)')
                fig.update_layout(
                    plot_bgcolor='#1E1E1E',
                    paper_bgcolor='#1E1E1E',
                    font=dict(color='#FFFFFF'),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor='#333333',
                        title='Price (USD)',
                        range=[0.995, 1.005]  # Narrow range to show tiny fluctuations
                    ),
                    margin=dict(l=10, r=10, t=40, b=10),
                    height=300
                )
                fig.update_traces(line=dict(color='#26A17B', width=3))  # Tether green color
                st.plotly_chart(fig, use_container_width=True)
                
                # Add info about USDT on Solana and its role in DAPPR platform
                st.markdown("""
                <div class="stCard">
                    <h4 style="margin-top: 0;">USDT in DAPPR Platform</h4>
                    <p>USDT on Solana is a stablecoin token that maintains a 1:1 peg with the US Dollar. The DAPPR platform uses USDT for:</p>
                    <ul>
                        <li><strong>Research Funding</strong>: Collaborators can fund research projects with USDT, providing stability against cryptocurrency volatility</li>
                        <li><strong>Milestone Payments</strong>: Contributors receive payments in USDT when completing project milestones</li>
                        <li><strong>Budget Planning</strong>: Project managers can budget research costs in a stable currency</li>
                    </ul>
                    <p><strong>Technical Details:</strong></p>
                    <ul>
                        <li>SPL Token with 6 decimal places (unlike SOL's 9 decimals)</li>
                        <li>Transactions utilize the SPL token program for transfers</li>
                        <li>Associated Token Accounts (ATAs) required for receiving USDT</li>
                    </ul>
                    <p><strong>Implementation:</strong> DAPPR smart contracts support both SOL and USDT funding through specialized transaction endpoints.</p>
                </div>
                """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error retrieving Solana network data: {str(e)}")
        st.warning("Some dashboard components may not display correctly due to API errors.")
