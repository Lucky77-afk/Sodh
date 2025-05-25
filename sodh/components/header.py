import streamlit as st
import os
from pathlib import Path
import base64

def render_header():
    """Render the application header with logo and navigation."""
    import os
    from pathlib import Path
    
    # Ensure assets directory exists
    assets_dir = os.path.join(Path(__file__).parent.parent, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    # Custom CSS for the header
    st.markdown("""
    <style>
    .header {
        display: flex;
        align-items: center;
        padding: 1rem 0;
        margin-bottom: 1rem;
    }
    .logo-container {
        display: flex;
        align-items: center;
        margin-right: 2rem;
    }
    .logo {
        height: 40px;
        margin-right: 1rem;
    }
    .nav-buttons {
        display: flex;
        gap: 0.5rem;
        flex-grow: 1;
    }
    .nav-button {
        padding: 0.5rem 1rem;
        border: 1px solid #14F195;
        border-radius: 4px;
        background: transparent;
        color: #14F195;
        cursor: pointer;
        transition: all 0.3s;
    }
    .nav-button:hover {
        background: rgba(20, 241, 149, 0.1);
    }
    .divider {
        border-top: 1px solid #2D2D2D;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a simple logo using HTML/CSS
    st.markdown("""
    <div class="header">
        <div class="logo-container">
            <div class="logo">
                <span class="logo-text">Sodh</span>
                <span class="logo-subtext">Solana Explorer</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Add logo styles
    st.markdown("""
    <style>
    .logo {
        display: flex;
        flex-direction: column;
        padding: 5px 10px;
        background: #131313;
        border-radius: 5px;
        border-left: 4px solid #14F195;
    }
    .logo-text {
        color: #14F195;
        font-family: Arial, sans-serif;
        font-size: 24px;
        font-weight: bold;
        line-height: 1;
    }
    .logo-subtext {
        color: #FFFFFF;
        font-family: Arial, sans-serif;
        font-size: 12px;
        margin-top: 2px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    st.markdown("""
    <div class="nav-buttons">
        <button class="nav-button" onclick="window.location.href='app.py'">📊 Dashboard</button>
        <button class="nav-button" onclick="window.location.href='pages/transactions.py'">🔄 Transactions</button>
        <button class="nav-button" onclick="window.location.href='pages/account.py'">👤 Account</button>
        <button class="nav-button" onclick="window.location.href='pages/smart_contract.py'">📝 Smart Contract</button>
        <button class="nav-button" onclick="window.location.href='pages/whitepaper.py'">📄 Whitepaper</button>
    </div>
    </div>
    <div class="divider"></div>
    """, unsafe_allow_html=True)
