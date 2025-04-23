import streamlit as st

def render_header():
    """Renders the application header with logo and title"""
    col1, col2 = st.columns([1, 5])
    
    with col1:
        st.markdown("""
        <svg width="60" height="60" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="30" cy="30" r="28" fill="#131313" stroke="#14F195" stroke-width="2"/>
            <path d="M17 30.5C17 25.2533 21.2533 21 26.5 21H33.5C38.7467 21 43 25.2533 43 30.5C43 35.7467 38.7467 40 33.5 40H26.5C21.2533 40 17 35.7467 17 30.5Z" fill="#131313" stroke="#9945FF" stroke-width="2"/>
            <path d="M25 30.5C25 29.1193 26.1193 28 27.5 28H32.5C33.8807 28 35 29.1193 35 30.5C35 31.8807 33.8807 33 32.5 33H27.5C26.1193 33 25 31.8807 25 30.5Z" fill="#14F195"/>
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
        """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin-top: 0; margin-bottom: 16px; border-color: #333;'>", unsafe_allow_html=True)
