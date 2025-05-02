import streamlit as st
import base64
import os

def render_header():
    """Renders the application header with logo and title"""
    col1, col2 = st.columns([1, 5])
    
    with col1:
        # Try to load JPEG logo first
        logo_path_jpeg = os.path.join("assets", "logo.jpeg")
        logo_path_svg = os.path.join("assets", "logo.svg")
        
        if os.path.exists(logo_path_jpeg):
            # Use the JPEG logo file with proper encoding
            with open(logo_path_jpeg, "rb") as f:
                logo_bytes = f.read()
                encoded_logo = base64.b64encode(logo_bytes).decode()
                st.markdown(f"""
                <div style="width: 90px; height: 90px; display: flex; align-items: center; justify-content: center;">
                    <img src="data:image/jpeg;base64,{encoded_logo}" style="max-width: 100%; max-height: 100%; border-radius: 50%;">
                </div>
                """, unsafe_allow_html=True)
        elif os.path.exists(logo_path_svg):
            # Fallback to SVG if JPEG not found
            with open(logo_path_svg, "r") as f:
                svg_content = f.read()
                st.markdown(f"""
                <div style="width: 60px; height: 60px;">
                    {svg_content}
                </div>
                """, unsafe_allow_html=True)
        else:
            # Fallback to inline SVG if no logo files found
            st.markdown("""
            <svg width="60" height="60" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="30" cy="30" r="28" fill="#131313" stroke="#14F195" stroke-width="2"/>
                <path d="M17 30.5C17 25.2533 21.2533 21 26.5 21H33.5C38.7467 21 43 25.2533 43 30.5C43 35.7467 38.7467 40 33.5 40H26.5C21.2533 40 17 35.7467 17 30.5Z" fill="#131313" stroke="#9945FF" stroke-width="2"/>
                <path d="M25 30.5C25 29.1193 26.1193 28 27.5 28H32.5C33.8807 28 35 29.1193 35 30.5C35 31.8807 33.8807 33 32.5 33H27.5C26.1193 33 25 31.8807 25 30.5Z" fill="#14F195"/>
                <path d="M27 25L33 36" stroke="#00FFA3" stroke-width="1.5" stroke-linecap="round"/>
                <path d="M33 25L27 36" stroke="#00FFA3" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <h1 style="margin-bottom: 0px; margin-top: 5px;">
            <span class="gradient-text">SODH</span>
            <span style="font-size: 1rem; color: #AAAAAA; font-weight: normal; margin-left: 8px;">
                Solana Blockchain Explorer
            </span>
        </h1>
        <div style="font-size: 0.9rem; color: #666; margin-top: 2px;">
            Powered by DAPPR - Decentralized Autonomous Platform for Propagation of Research
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin-top: 10px; margin-bottom: 16px; border-color: #333;'>", unsafe_allow_html=True)
