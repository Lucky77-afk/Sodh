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
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(20, 241, 149, 0.05) 0%, rgba(153, 69, 255, 0.05) 100%);
            border: 1px solid rgba(20, 241, 149, 0.2);
            border-radius: 20px;
            padding: 25px;
            margin: 20px 0;
        ">
            <h3 style="
                color: #14F195; 
                font-size: 1.6rem; 
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 12px;
            ">
                <span style="font-size: 1.4rem;">🚀</span>
                Getting Started with DAPPR
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Step-by-step guide
        st.markdown("""
        <div style="
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 25px 0;
        ">
            <div style="
                background: linear-gradient(135deg, rgba(20, 241, 149, 0.05) 0%, rgba(0, 255, 163, 0.05) 100%);
                border: 1px solid rgba(20, 241, 149, 0.3);
                border-radius: 15px;
                padding: 25px;
                position: relative;
            ">
                <div style="
                    position: absolute;
                    top: -10px;
                    left: 20px;
                    background: #14F195;
                    color: #000;
                    padding: 5px 15px;
                    border-radius: 15px;
                    font-size: 0.9rem;
                    font-weight: 600;
                ">STEP 1</div>
                
                <h4 style="color: #14F195; margin: 20px 0 15px 0; font-size: 1.2rem;">💼 Connect Your Wallet</h4>
                <p style="color: #CCCCCC; margin-bottom: 15px; line-height: 1.5;">
                    Choose from supported Solana wallets:
                </p>
                <div style="margin: 15px 0;">
                    <div style="color: #FFFFFF; margin: 8px 0; display: flex; align-items: center; gap: 10px;">
                        <span style="color: #14F195;">•</span> Phantom Wallet (Recommended)
                    </div>
                    <div style="color: #FFFFFF; margin: 8px 0; display: flex; align-items: center; gap: 10px;">
                        <span style="color: #14F195;">•</span> Solflare
                    </div>
                    <div style="color: #FFFFFF; margin: 8px 0; display: flex; align-items: center; gap: 10px;">
                        <span style="color: #14F195;">•</span> Binance Wallet
                    </div>
                </div>
            </div>
            
            <div style="
                background: linear-gradient(135deg, rgba(153, 69, 255, 0.05) 0%, rgba(20, 241, 149, 0.05) 100%);
                border: 1px solid rgba(153, 69, 255, 0.3);
                border-radius: 15px;
                padding: 25px;
                position: relative;
            ">
                <div style="
                    position: absolute;
                    top: -10px;
                    left: 20px;
                    background: #9945FF;
                    color: #FFF;
                    padding: 5px 15px;
                    border-radius: 15px;
                    font-size: 0.9rem;
                    font-weight: 600;
                ">STEP 2</div>
                
                <h4 style="color: #9945FF; margin: 20px 0 15px 0; font-size: 1.2rem;">🔍 Explore Platform</h4>
                <p style="color: #CCCCCC; margin-bottom: 15px; line-height: 1.5;">
                    Navigate through sections:
                </p>
                <div style="margin: 15px 0;">
                    <div style="color: #FFFFFF; margin: 8px 0; display: flex; align-items: center; gap: 10px;">
                        <span style="color: #9945FF;">•</span> Dashboard - Blockchain metrics
                    </div>
                    <div style="color: #FFFFFF; margin: 8px 0; display: flex; align-items: center; gap: 10px;">
                        <span style="color: #9945FF;">•</span> Smart Contract - Collaborations
                    </div>
                </div>
            </div>
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