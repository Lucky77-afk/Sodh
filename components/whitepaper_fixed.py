import streamlit as st
import pandas as pd

def render_whitepaper():
    """Renders the DAPPR whitepaper content with enhanced visual design"""
    # Hero section with gradient background
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
                background: linear-gradient(135deg, #14F195 0%, #00FFA3 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">DAPPR Whitepaper</h1>
            <h2 style="
                color: #AAAAAA; 
                font-size: 1.4rem; 
                font-weight: 400; 
                margin-bottom: 20px;
                line-height: 1.4;
            ">Decentralized Autonomous Platform for Propagation of Research</h2>
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
    
    # Executive Summary
    st.markdown("## 📋 Executive Summary")
    st.markdown("""
    The Decentralized Autonomous Platform for Propagation of Research (DAPPR) leverages Solana's high-performance blockchain and artificial intelligence to revolutionize collaboration between academia and industry. By addressing challenges such as misaligned incentives, restrictive intellectual property frameworks, and inefficient value distribution, DAPPR fosters transparent, trustless, and scalable partnerships.
    """)
    
    # Why Solana section
    st.markdown("### Why Solana?")
    st.markdown("""
    Solana is the blockchain of choice for DAPPR due to its unparalleled performance, scalability, and developer-friendly ecosystem, making it a leading platform for decentralized applications in 2025.
    """)
    
    # Key Features
    st.markdown("**Key Features:**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("- ⚡ **High Throughput**: Thousands of TPS for frequent micropayments")
        st.markdown("- 💰 **Low Transaction Fees**: Below $0.0025 per transaction")
        st.markdown("- ⚡ **Fast Finality**: PoH consensus for rapid confirmations")
    
    with col2:
        st.markdown("- 🌱 **Energy Efficiency**: Minimal energy consumption per transaction")
        st.markdown("- 👨‍💻 **Developer-Friendly**: Comprehensive tools and support")
    
    # Solana Metrics
    st.markdown("### ⚡ SOLANA METRICS (2025)")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Transactions Per Second", "65,000+")
    with col2:
        st.metric("Average Fee", "$0.00025")
    with col3:
        st.metric("Block Time", "400ms")
    with col4:
        st.metric("Uptime Since Feb 2023", "100%")
    
    # Why We Started Building DAPPR
    st.markdown("## 🔬 Why We Started Building DAPPR")
    st.markdown("""
    We created DAPPR in response to a critical observation: despite tremendous advances in both academic research and industry innovation, the bridge between these worlds remains fundamentally broken. Through extensive experience straddling both environments, we identified several systemic problems that effectively trap valuable knowledge in silos.
    """)
    
    # Problem areas
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="
            background: rgba(20, 241, 149, 0.05);
            border: 1px solid rgba(20, 241, 149, 0.2);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
        ">
            <h4 style="color: #14F195; margin-bottom: 12px;">🎯 Incentive Misalignment</h4>
            <p style="color: #CCCCCC; font-size: 0.9rem; line-height: 1.5;">
                Academic rewards publication metrics while industry prioritizes commercial applications, creating structural disconnects.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="
            background: rgba(255, 215, 0, 0.05);
            border: 1px solid rgba(255, 215, 0, 0.2);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
        ">
            <h4 style="color: #FFD700; margin-bottom: 12px;">🤝 Attribution & Trust Deficits</h4>
            <p style="color: #CCCCCC; font-size: 0.9rem; line-height: 1.5;">
                Researchers fear inadequate recognition while industry struggles with accountability.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: rgba(255, 107, 107, 0.05);
            border: 1px solid rgba(255, 107, 107, 0.2);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
        ">
            <h4 style="color: #FF6B6B; margin-bottom: 12px;">📋 IP Framework Issues</h4>
            <p style="color: #CCCCCC; font-size: 0.9rem; line-height: 1.5;">
                Traditional collaboration requires navigating byzantine legal agreements that often take longer than the research itself.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="
            background: rgba(0, 255, 163, 0.05);
            border: 1px solid rgba(0, 255, 163, 0.2);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
        ">
            <h4 style="color: #00FFA3; margin-bottom: 12px;">🔍 Systemic Opacity</h4>
            <p style="color: #CCCCCC; font-size: 0.9rem; line-height: 1.5;">
                Limited visibility across institutional boundaries leads to redundant work and missed synergies.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Market Opportunity
    st.markdown("## 💰 Market Opportunity")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: rgba(20, 241, 149, 0.05); border-radius: 15px; margin: 10px 0;">
            <div style="color: #14F195; font-size: 2rem; font-weight: 700;">$2.4T</div>
            <div style="color: #FFFFFF; font-weight: 600;">Global R&D Investment</div>
            <div style="color: #AAAAAA; font-size: 0.8rem;">Annual worldwide research spending</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: rgba(153, 69, 255, 0.05); border-radius: 15px; margin: 10px 0;">
            <div style="color: #9945FF; font-size: 2rem; font-weight: 700;">$1.5T</div>
            <div style="color: #FFFFFF; font-weight: 600;">Stranded Innovation</div>
            <div style="color: #AAAAAA; font-size: 0.8rem;">Potentially stranded value annually</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: rgba(255, 215, 0, 0.05); border-radius: 15px; margin: 10px 0;">
            <div style="color: #FFD700; font-size: 2rem; font-weight: 700;">$250B</div>
            <div style="color: #FFFFFF; font-weight: 600;">University Budgets</div>
            <div style="color: #AAAAAA; font-size: 0.8rem;">Collective annual research budgets</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: rgba(0, 255, 163, 0.05); border-radius: 15px; margin: 10px 0;">
            <div style="color: #00FFA3; font-size: 2rem; font-weight: 700;">14mo</div>
            <div style="color: #FFFFFF; font-weight: 600;">Legal Process</div>
            <div style="color: #AAAAAA; font-size: 0.8rem;">Average collaboration setup time</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Long-Term Vision
    st.markdown("## 🔮 Long-Term Vision")
    st.markdown("""
    Our vision for DAPPR transcends creating just another research platform; we're building the foundation for a new innovation economy where knowledge creation and application function seamlessly across traditional boundaries.
    """)
    
    # Vision components
    st.markdown("### Key Vision Components:")
    
    st.markdown("#### 🆔 Self-Sovereign Research Identity")
    st.markdown("""
    Blockchain-verified identity system where researchers' contributions, impact, and reputation become portable assets that transcend institutional boundaries, creating career mobility and shifting power dynamics toward individual contributors.
    """)
    
    st.markdown("#### ⚡ Frictionless Knowledge Markets")
    st.markdown("""
    Automated attribution, IP management, and value distribution through smart contracts enable instantaneous research collaborations that would be logistically impossible under current frameworks.
    """)
    
    st.markdown("#### 🌍 Democratized Access to Innovation")
    st.markdown("""
    Progressive removal of institutional gatekeepers, allowing individual researchers worldwide to connect directly with industry partners and enabling smaller companies to access cutting-edge research.
    """)
    
    st.markdown("#### 🕸️ Cross-boundary Knowledge Graph")
    st.markdown("""
    As the platform scales, it generates an unprecedented map of research connections and complementary innovations, creating visibility across traditional silos and enabling AI-suggested collaborations.
    """)
    
    # Technical Architecture
    with st.expander("Technical Architecture"):
        st.markdown("""
        DAPPR's architecture is designed to leverage Solana's capabilities, ensuring secure, 
        scalable, and efficient operations for industry-academia collaboration.
        
        #### Multi-Layered Blockchain Structure
        
        DAPPR employs a three-tiered blockchain architecture:
        
        - **Primary Layer**: Core transactions (funding, governance)
        - **Secondary Layer**: Individual collaboration units (research projects)
        - **Entity Layer**: Stakeholder-specific data (researcher profiles, institutions)
        
        #### Smart Contracts
        
        Solana's robust smart contract framework automates:
        
        - Collaboration Agreements
        - Funding Disbursements
        - Value Distribution
        - Compliance and Dispute Resolution
        """)
    
    # Economic Model
    with st.expander("Economic Model"):
        st.markdown("""
        DAPPR's economic model aligns stakeholder incentives through token economics, stablecoin 
        integration, and dynamic pricing mechanisms.
        
        #### Token Economics
        
        DAPPR employs a dual-token system:
        
        - **Governance Tokens**: Grant voting rights on platform decisions
        - **Transactional Tokens**: Medium for value exchange, pegged to stablecoins
        
        #### Stablecoin Integration
        
        Stablecoins (USDC, USDT) are integral to DAPPR's monetization, with Solana's stablecoin 
        market cap reaching $12.63 billion in April 2025.
        
        #### Revenue Model
        
        DAPPR generates revenue through:
        
        - Transaction fees (0.5%)
        - Premium subscriptions
        - Value-added services (IP protection, analytics)
        """)
        
        # Token distribution chart
        token_data = pd.DataFrame({
            'Category': ['Research Contribution', 'Platform Development', 'Community Governance', 'Partnership Incentives', 'Reserve'],
            'Percentage': [40, 25, 15, 10, 10]
        })
        
        st.markdown("#### Token Distribution")
        st.bar_chart(token_data.set_index('Category'))
    
    # Implementation Framework
    with st.expander("Implementation Framework"):
        st.markdown("""
        DAPPR's implementation follows a phased approach, ensuring gradual adoption and 
        continuous improvement based on stakeholder feedback.
        
        #### Phase 1: Foundation (Q2 2025)
        - Core smart contract development
        - Basic collaboration framework
        - Pilot partner onboarding
        
        #### Phase 2: Expansion (Q4 2025)
        - Advanced features (AI matching, analytics)
        - Multi-institutional partnerships
        - Token launch
        
        #### Phase 3: Scale (Q2 2026)
        - Global rollout
        - Advanced governance mechanisms
        - Cross-chain interoperability
        
        #### Phase 4: Optimization (Q4 2026+)
        - AI-driven research matching
        - Predictive analytics
        - Self-governing ecosystem
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
        <h3 style="color: #14F195; margin-bottom: 20px;">Join the Research Revolution</h3>
        <p style="color: #FFFFFF; margin-bottom: 20px; font-size: 1.1rem;">
            We're targeting "near-commercial research" – the estimated $1.2 trillion in annual academic output that could create immediate industry impact if collaboration barriers were removed.
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
        ">🚀 Start Collaborating Today</div>
    </div>
    """, unsafe_allow_html=True)