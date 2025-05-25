import streamlit as st
import os
from pathlib import Path

def render_header():
    """Render the application header with logo and navigation."""
    # Directly embed the SVG content
    logo_svg = '''
    <svg width="200" height="50" viewBox="0 0 200 50" xmlns="http://www.w3.org/2000/svg">
      <style>
        .logo-text { font-family: Arial, sans-serif; font-size: 24px; font-weight: bold; fill: #14F195; }
        .logo-subtext { font-family: Arial, sans-serif; font-size: 14px; fill: #FFFFFF; }
      </style>
      <rect width="200" height="50" fill="#131313" rx="5"/>
      <text x="10" y="32" class="logo-text">Sodh</text>
      <text x="80" y="32" class="logo-subtext">Solana Explorer</text>
      <line x1="10" y1="35" x2="190" y2="35" stroke="#14F195" stroke-width="2"/>
    </svg>
    '''
    
    # Encode the SVG for URL embedding
    import urllib.parse
    encoded_svg = urllib.parse.quote(logo_svg.strip())
    data_url = f"data:image/svg+xml,{encoded_svg}"
    
    # Custom CSS for the header
    st.markdown(f"""
    <style>
    /* Header Container */
    .sodh-header {{
        width: 100%;
        padding: 1rem 0;
        margin-bottom: 1rem;
        background: transparent;
    }}
    
    /* Header Content */
    .sodh-header-content {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1.5rem;
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 1rem;
    }}
    
    /* Logo Container */
    .sodh-logo-container {{
        display: flex;
        align-items: center;
        text-decoration: none;
    }}
    
    /* Logo Image */
    .sodh-logo {{
        height: 40px;
        width: auto;
    }}
    
    /* Navigation */
    .sodh-nav {{
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
    }}
    
    /* Navigation Buttons */
    .sodh-nav-button {{
        padding: 0.5rem 1rem;
        border: 1px solid #14F195;
        border-radius: 6px;
        background: transparent;
        color: #14F195;
        font-family: 'Arial', sans-serif;
        font-size: 0.9rem;
        font-weight: 500;
        text-decoration: none;
        transition: all 0.2s ease;
        white-space: nowrap;
    }}
    
    .sodh-nav-button:hover {{
        background: rgba(20, 241, 149, 0.1);
        transform: translateY(-1px);
    }}
    
    /* Divider */
    .sodh-divider {{
        width: 100%;
        height: 1px;
        background: #2D2D2D;
        margin: 1rem 0;
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .sodh-header-content {{
            flex-direction: column;
            align-items: stretch;
            gap: 1rem;
        }}
        
        .sodh-nav {{
            flex-direction: column;
            width: 100%;
        }}
        
        .sodh-nav-button {{
            text-align: center;
            width: 100%;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Header HTML with embedded SVG
    header_html = f"""
    <header class="sodh-header">
        <div class="sodh-header-content">
            <div class="sodh-logo-container">
                {logo_svg.strip()}
            </div>
            <nav class="sodh-nav">
                <a href="app.py" class="sodh-nav-button">📊 Dashboard</a>
                <a href="pages/transactions.py" class="sodh-nav-button">🔄 Transactions</a>
                <a href="pages/account.py" class="sodh-nav-button">👤 Account</a>
                <a href="pages/smart_contract.py" class="sodh-nav-button">📝 Smart Contract</a>
                <a href="pages/whitepaper.py" class="sodh-nav-button">📄 Whitepaper</a>
            </nav>
        </div>
        <div class="sodh-divider"></div>
    </header>
    """
    
    # Render the header
    st.markdown(header_html, unsafe_allow_html=True)
