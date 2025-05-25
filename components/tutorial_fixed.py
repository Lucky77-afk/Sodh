import streamlit as st

def render_tutorial():
    """Renders the tutorial section with enhanced visual design and comprehensive guidance"""
    # Hero section for tutorial
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 25%, #2a2a2a 50%, #1a1a1a 75%, #0a0a0a 100%);
        border: 1px solid rgba(20, 241, 149, 0.3);
        border-radius: 25px;
        padding: 40px;
        margin: 20px 0;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    ">
        <div style="position: relative; z-index: 1;">
            <h1 style="
                color: #FFFFFF; 
                font-size: 2.5rem; 
                font-weight: 700; 
                margin-bottom: 16px;
                background: linear-gradient(135deg, #14F195 0%, #9945FF 50%, #00FFA3 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">DAPPR Platform Tutorial</h1>
            <h2 style="
                color: #AAAAAA; 
                font-size: 1.4rem; 
                font-weight: 400; 
                margin-bottom: 20px;
                line-height: 1.4;
            ">Master Decentralized Research Collaboration on Solana</h2>
            <div style="
                width: 100px;
                height: 4px;
                background: linear-gradient(90deg, #14F195 0%, #9945FF 100%);
                margin: 0 auto;
                border-radius: 2px;
            "></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced introduction
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(20, 241, 149, 0.05) 0%, rgba(153, 69, 255, 0.05) 100%);
        border: 1px solid rgba(20, 241, 149, 0.2);
        border-radius: 20px;
        padding: 25px;
        margin: 25px 0;
        text-align: center;
    ">
        <p style="
            color: #FFFFFF; 
            font-size: 1.2rem; 
            line-height: 1.6; 
            margin: 0;
        ">
            Welcome to the comprehensive DAPPR platform tutorial. This guide will empower you to leverage blockchain technology for revolutionary research collaboration, smart contract interactions, and decentralized innovation on the Solana network.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tutorial sections
    tabs = st.tabs(["🚀 Getting Started", "📋 Smart Contracts", "🔬 Creating Projects", "🤝 Collaborations", "💰 Funding"])
    
    with tabs[0]:
        st.markdown("### 🚀 Getting Started with DAPPR")
        
        # Step 1
        st.markdown("""
        <div style="
            background: rgba(20, 241, 149, 0.05);
            border: 1px solid rgba(20, 241, 149, 0.3);
            border-radius: 15px;
            padding: 20px;
            margin: 15px 0;
        ">
            <h4 style="color: #14F195;">💼 Step 1: Connect Your Wallet</h4>
            <p style="color: #CCCCCC;">Choose from supported Solana wallets:</p>
            <ul style="color: #FFFFFF;">
                <li>Phantom Wallet (Recommended)</li>
                <li>Solflare</li>
                <li>Binance Wallet</li>
                <li>CoinDCX Wallet</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Step 2
        st.markdown("""
        <div style="
            background: rgba(153, 69, 255, 0.05);
            border: 1px solid rgba(153, 69, 255, 0.3);
            border-radius: 15px;
            padding: 20px;
            margin: 15px 0;
        ">
            <h4 style="color: #9945FF;">🔍 Step 2: Explore the Platform</h4>
            <p style="color: #CCCCCC;">Navigate through the main sections:</p>
            <ul style="color: #FFFFFF;">
                <li>Dashboard - View blockchain metrics</li>
                <li>Transactions - Monitor activity</li>
                <li>Smart Contract - Manage collaborations</li>
                <li>Account - Check wallet details</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Step 3
        st.markdown("""
        <div style="
            background: rgba(255, 215, 0, 0.05);
            border: 1px solid rgba(255, 215, 0, 0.3);
            border-radius: 15px;
            padding: 20px;
            margin: 15px 0;
        ">
            <h4 style="color: #FFD700;">🤝 Step 3: Start Collaborating</h4>
            <p style="color: #CCCCCC;">Begin your research collaboration journey:</p>
            <ul style="color: #FFFFFF;">
                <li>Create research projects</li>
                <li>Set collaboration terms</li>
                <li>Add team members</li>
                <li>Track project progress</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown("### 📋 Smart Contract Basics")
        st.markdown("""
        Learn how DAPPR's smart contracts enable transparent research collaboration:
        
        **Key Features:**
        - 🔒 Immutable project agreements
        - 💰 Automated milestone payments  
        - 🤝 Multi-party collaboration tracking
        - 📊 Transparent progress monitoring
        """)
    
    with tabs[2]:
        st.markdown("### 🔬 Creating Research Projects")
        st.markdown("""
        Step-by-step guide to creating your first research project:
        
        1. **Project Setup** - Define research objectives and scope
        2. **Team Assembly** - Add collaborators and define roles
        3. **Milestone Planning** - Break work into manageable phases
        4. **Agreement Terms** - Set IP sharing and compensation rules
        """)
    
    with tabs[3]:
        st.markdown("### 🤝 Managing Collaborations")
        st.markdown("""
        Effective collaboration management on DAPPR:
        
        - **Real-time Updates** - Track project progress instantly
        - **Dispute Resolution** - Built-in mediation mechanisms
        - **Attribution Tracking** - Permanent contribution records
        - **Cross-institutional** - Seamless university-industry partnerships
        """)
    
    with tabs[4]:
        st.markdown("### 💰 Funding & Payments")
        st.markdown("""
        Understanding the DAPPR funding ecosystem:
        
        **Funding Sources:**
        - Research grants and institutional funding
        - Industry partnership investments
        - Milestone-based payments
        - Performance bonuses
        
        **Payment Features:**
        - Automated escrow systems
        - Multi-signature approvals
        - Transparent fund tracking
        - Instant settlement upon milestone completion
        """)
    
    # Call to action
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(20, 241, 149, 0.1) 0%, rgba(153, 69, 255, 0.1) 100%);
        border: 1px solid rgba(20, 241, 149, 0.3);
        border-radius: 20px;
        padding: 30px;
        margin: 30px 0;
        text-align: center;
    ">
        <h3 style="color: #14F195; margin-bottom: 20px;">Ready to Start?</h3>
        <p style="color: #FFFFFF; margin-bottom: 20px; font-size: 1.1rem;">
            Create your first project on DAPPR and transform how you collaborate on research.
        </p>
        <div style="
            background: rgba(20, 241, 149, 0.1);
            border: 1px solid #14F195;
            border-radius: 15px;
            padding: 15px 30px;
            color: #14F195;
            font-weight: 600;
            display: inline-block;
            cursor: pointer;
        ">🚀 Get Started Now</div>
    </div>
    """, unsafe_allow_html=True)