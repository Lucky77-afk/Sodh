import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

def get_blockchain_metrics():
    """Get current blockchain metrics with optimized calls"""
    metrics = {
        'current_slot': 0,
        'block_time': None,
        'epoch': 0,
        'slot_index': 0,
        'slots_in_epoch': 0,
        'total_supply': 0,
        'circulating_supply': 0
    }
    
    try:
        # Get epoch info first (most reliable call)
        epoch_result = make_rpc_call("getEpochInfo", [])
        if epoch_result and 'result' in epoch_result:
            epoch_info = epoch_result['result']
            metrics.update({
                'epoch': epoch_info.get('epoch', 0),
                'slot_index': epoch_info.get('slotIndex', 0),
                'slots_in_epoch': epoch_info.get('slotsInEpoch', 0)
            })
            # Use absolute slot from epoch info
            metrics['current_slot'] = epoch_info.get('absoluteSlot', 0)
        
        # Try to get supply info (may timeout)
        supply_result = make_rpc_call("getSupply", [])
        if supply_result and 'result' in supply_result:
            supply_info = supply_result['result']['value']
            metrics.update({
                'total_supply': supply_info.get('total', 0),
                'circulating_supply': supply_info.get('circulating', 0)
            })
        
        return metrics
        
    except Exception as e:
        st.warning(f"Some blockchain data unavailable: {str(e)}")
        return metrics

def get_recent_blocks_safe(current_slot, limit=5):
    """Get recent blocks using safe RPC calls with reduced limit"""
    blocks = []
    
    try:
        # Get fewer blocks to reduce timeout risk
        for i in range(min(limit, 5)):  # Max 5 blocks
            slot = current_slot - i
            
            # Use minimal encoding to reduce response size
            block_result = make_rpc_call("getBlock", [slot, {
                "encoding": "json", 
                "transactionDetails": "signatures",
                "maxSupportedTransactionVersion": 0
            }])
            
            if block_result and 'result' in block_result and block_result['result']:
                block_data = block_result['result']
                
                # Count signatures instead of full transactions
                signatures = block_data.get('signatures', [])
                
                block = {
                    'slot': slot,
                    'block_time': block_data.get('blockTime'),
                    'transaction_count': len(signatures),
                    'block_hash': block_data.get('blockhash', ''),
                    'parent_slot': block_data.get('parentSlot', 0)
                }
                blocks.append(block)
            else:
                # Add placeholder for failed blocks
                blocks.append({
                    'slot': slot,
                    'block_time': None,
                    'transaction_count': 0,
                    'block_hash': '',
                    'parent_slot': 0
                })
        
        return blocks
        
    except Exception as e:
        st.warning(f"Block data partially unavailable: {str(e)}")
        return blocks

def render_dashboard():
    """Renders the dashboard with blockchain metrics and visualizations"""
    st.markdown('<h2>Blockchain Dashboard</h2>', unsafe_allow_html=True)
    
    # Get blockchain metrics
    with st.spinner("Loading blockchain data..."):
        metrics = get_blockchain_metrics()
        current_slot = metrics.get('current_slot', 0)
        recent_blocks = get_recent_blocks_safe(current_slot, 5) if current_slot > 0 else []
    
    if not metrics:
        st.error("Unable to load blockchain metrics")
        return
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%);
            border: 1px solid #14F195;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(20, 241, 149, 0.1);
        ">
            <h4 style="color: #14F195; margin: 0 0 10px 0;">Current Slot</h4>
            <h2 style="color: #FFFFFF; margin: 0; font-family: monospace;">{metrics.get('current_slot', 0):,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        epoch = metrics.get('epoch', 0)
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%);
            border: 1px solid #9945FF;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(153, 69, 255, 0.1);
        ">
            <h4 style="color: #9945FF; margin: 0 0 10px 0;">Current Epoch</h4>
            <h2 style="color: #FFFFFF; margin: 0; font-family: monospace;">{epoch}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        circulating = metrics.get('circulating_supply', 0) / 1_000_000_000  # Convert to SOL
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%);
            border: 1px solid #00FFA3;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 255, 163, 0.1);
        ">
            <h4 style="color: #00FFA3; margin: 0 0 10px 0;">Circulating Supply</h4>
            <h2 style="color: #FFFFFF; margin: 0; font-family: monospace;">{circulating:,.0f}M</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        progress = (metrics.get('slot_index', 0) / max(metrics.get('slots_in_epoch', 1), 1)) * 100
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%);
            border: 1px solid #FFD700;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(255, 215, 0, 0.1);
        ">
            <h4 style="color: #FFD700; margin: 0 0 10px 0;">Epoch Progress</h4>
            <h2 style="color: #FFFFFF; margin: 0; font-family: monospace;">{progress:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent blocks section
    if recent_blocks:
        st.markdown("### Recent Blocks")
        
        # Create DataFrame for visualization
        df_blocks = pd.DataFrame(recent_blocks)
        
        if not df_blocks.empty and 'block_time' in df_blocks.columns:
            # Convert timestamps to readable format
            df_blocks['timestamp'] = pd.to_datetime(df_blocks['block_time'], unit='s', errors='coerce')
            df_blocks = df_blocks.dropna(subset=['timestamp'])
            
            if not df_blocks.empty:
                # Block times chart
                fig_times = px.line(
                    df_blocks.head(10), 
                    x='slot', 
                    y='transaction_count',
                    title='Transactions per Block',
                    color_discrete_sequence=['#14F195']
                )
                fig_times.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    title_font_color='#14F195'
                )
                st.plotly_chart(fig_times, use_container_width=True)
        
        # Recent blocks table
        st.markdown("### Latest Blocks")
        
        for i, block in enumerate(recent_blocks[:5]):
            slot = block.get('slot', 0)
            tx_count = block.get('transaction_count', 0)
            block_time = block.get('block_time')
            
            if block_time:
                time_str = datetime.fromtimestamp(block_time).strftime('%H:%M:%S UTC')
            else:
                time_str = 'Unknown'
            
            # Color function for transaction count
            def color_count(count):
                if count > 100:
                    return "#14F195"  # Green for high activity
                elif count > 50:
                    return "#FFD700"  # Yellow for medium activity
                else:
                    return "#9945FF"  # Purple for low activity
            
            tx_color = color_count(tx_count)
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #1a1a1a 0%, #252525 100%);
                border: 1px solid #333;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h5 style="color: #14F195; margin: 0;">Block #{slot:,}</h5>
                        <p style="color: #AAAAAA; margin: 5px 0 0 0; font-size: 12px;">Time: {time_str}</p>
                    </div>
                    <div style="text-align: right;">
                        <span style="
                            color: {tx_color}; 
                            font-size: 18px; 
                            font-weight: bold;
                        ">{tx_count} TXs</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Block data not available at the moment")