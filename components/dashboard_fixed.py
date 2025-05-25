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
        response = requests.post(rpc_url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"RPC call failed: {str(e)}")
        return None

def get_blockchain_metrics():
    """Get current blockchain metrics"""
    try:
        # Get current slot (latest block)
        slot_result = make_rpc_call("getSlot", [])
        current_slot = slot_result['result'] if slot_result and 'result' in slot_result else 0
        
        # Get block time for current slot
        block_time_result = make_rpc_call("getBlockTime", [current_slot])
        current_block_time = block_time_result['result'] if block_time_result and 'result' in block_time_result else None
        
        # Get epoch info
        epoch_result = make_rpc_call("getEpochInfo", [])
        epoch_info = epoch_result['result'] if epoch_result and 'result' in epoch_result else {}
        
        # Get supply info
        supply_result = make_rpc_call("getSupply", [])
        supply_info = supply_result['result']['value'] if supply_result and 'result' in supply_result else {}
        
        return {
            'current_slot': current_slot,
            'block_time': current_block_time,
            'epoch': epoch_info.get('epoch', 0),
            'slot_index': epoch_info.get('slotIndex', 0),
            'slots_in_epoch': epoch_info.get('slotsInEpoch', 0),
            'total_supply': supply_info.get('total', 0),
            'circulating_supply': supply_info.get('circulating', 0)
        }
    except Exception as e:
        st.error(f"Error fetching blockchain metrics: {str(e)}")
        return {}

def get_recent_blocks_safe(limit=10):
    """Get recent blocks using safe RPC calls"""
    try:
        # Get current slot
        slot_result = make_rpc_call("getSlot", [])
        if not slot_result or 'result' not in slot_result:
            return []
        
        current_slot = slot_result['result']
        blocks = []
        
        # Get recent blocks
        for i in range(limit):
            slot = current_slot - i
            block_result = make_rpc_call("getBlock", [slot, {"encoding": "json", "transactionDetails": "none"}])
            
            if block_result and 'result' in block_result and block_result['result']:
                block_data = block_result['result']
                
                block = {
                    'slot': slot,
                    'block_time': block_data.get('blockTime'),
                    'transaction_count': len(block_data.get('transactions', [])),
                    'block_hash': block_data.get('blockhash', ''),
                    'parent_slot': block_data.get('parentSlot', 0)
                }
                blocks.append(block)
        
        return blocks
        
    except Exception as e:
        st.error(f"Error fetching blocks: {str(e)}")
        return []

def render_dashboard():
    """Renders the dashboard with blockchain metrics and visualizations"""
    st.markdown('<h2>Blockchain Dashboard</h2>', unsafe_allow_html=True)
    
    # Get blockchain metrics
    with st.spinner("Loading blockchain data..."):
        metrics = get_blockchain_metrics()
        recent_blocks = get_recent_blocks_safe(10)
    
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