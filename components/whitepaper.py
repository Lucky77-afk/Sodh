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
    
    # Executive Summary with enhanced styling
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(20, 241, 149, 0.05) 0%, rgba(153, 69, 255, 0.05) 100%);
        border: 1px solid rgba(20, 241, 149, 0.2);
        border-radius: 20px;
        padding: 30px;
        margin: 30px 0;
        position: relative;
    ">
        <h3 style="
            color: #14F195; 
            font-size: 1.8rem; 
            font-weight: 600; 
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 12px;
        ">
            <span style="
                background: linear-gradient(135deg, #14F195 0%, #00FFA3 100%);
                border-radius: 10px;
                padding: 8px;
                font-size: 1.2rem;
            ">📋</span>
            Executive Summary
        </h3>
        <p style="
            color: #FFFFFF; 
            font-size: 1.1rem; 
            line-height: 1.7; 
            margin: 0;
            text-align: justify;
        ">
            The Decentralized Autonomous Platform for Propagation of Research (DAPPR) leverages Solana's 
            high-performance blockchain and artificial intelligence to revolutionize collaboration between 
            academia and industry. By addressing challenges such as misaligned incentives, restrictive 
            intellectual property frameworks, and inefficient value distribution, DAPPR fosters transparent, 
            trustless, and scalable partnerships.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Why Solana section
    with st.expander("Why Solana?", expanded=True):
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("""
            Solana is the blockchain of choice for DAPPR due to its unparalleled performance, 
            scalability, and developer-friendly ecosystem, making it a leading platform for 
            decentralized applications in 2025.
            
            #### Key Features:
            
            - **High Throughput**: Thousands of TPS for frequent micropayments
            - **Low Transaction Fees**: Below $0.0025 per transaction
            - **Fast Finality**: PoH consensus for rapid confirmations
            - **Energy Efficiency**: Minimal energy consumption per transaction
            - **Developer-Friendly**: Comprehensive tools and support
            """)
            
        with col2:
            # Enhanced Solana metrics card
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(153, 69, 255, 0.1) 0%, rgba(20, 241, 149, 0.1) 100%);
                border: 1px solid rgba(153, 69, 255, 0.3);
                border-radius: 20px;
                padding: 24px;
                margin: 10px 0;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            ">
                <div style="
                    color: #9945FF; 
                    font-size: 1.1rem; 
                    font-weight: 600; 
                    margin-bottom: 20px;
                    text-align: center;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 8px;
                ">
                    <span style="font-size: 1.2rem;">⚡</span>
                    SOLANA METRICS (2025)
                </div>
                
                <div style="margin-top: 16px;">
                    <div style="
                        display: flex; 
                        justify-content: space-between; 
                        align-items: center;
                        margin-bottom: 12px;
                        padding: 8px 0;
                        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                    ">
                        <span style="color: #CCCCCC; font-size: 0.9rem;">Transactions Per Second:</span>
                        <span style="
                            color: #14F195; 
                            font-weight: 700; 
                            font-family: monospace;
                            font-size: 1rem;
                        ">65,000+</span>
                    </div>
                    <div style="
                        display: flex; 
                        justify-content: space-between; 
                        align-items: center;
                        margin-bottom: 12px;
                        padding: 8px 0;
                        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                    ">
                        <span style="color: #CCCCCC; font-size: 0.9rem;">Average Fee:</span>
                        <span style="
                            color: #14F195; 
                            font-weight: 700; 
                            font-family: monospace;
                            font-size: 1rem;
                        ">$0.00025</span>
                    </div>
                    <div style="
                        display: flex; 
                        justify-content: space-between; 
                        align-items: center;
                        margin-bottom: 12px;
                        padding: 8px 0;
                        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                    ">
                        <span style="color: #CCCCCC; font-size: 0.9rem;">Block Time:</span>
                        <span style="
                            color: #14F195; 
                            font-weight: 700; 
                            font-family: monospace;
                            font-size: 1rem;
                        ">400ms</span>
                    </div>
                    <div style="
                        display: flex; 
                        justify-content: space-between; 
                        align-items: center;
                        padding: 8px 0;
                    ">
                        <span style="color: #CCCCCC; font-size: 0.9rem;">Uptime Since Feb 2023:</span>
                        <span style="
                            color: #14F195; 
                            font-weight: 700; 
                            font-family: monospace;
                            font-size: 1rem;
                        ">100%</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
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
        
        # Architecture diagram
        st.markdown("""
        <div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; text-align: center;">
            <div style="color: #14F195; margin-bottom: 15px; font-weight: bold;">DAPPR ARCHITECTURE</div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
                <div style="width: 30%; background-color: #272727; padding: 15px; border-radius: 8px; border: 1px solid #333;">
                    <div style="color: #9945FF; font-weight: bold; margin-bottom: 10px;">Primary Layer</div>
                    <div style="color: #AAA; font-size: 0.9rem;">Core governance & funding transactions</div>
                </div>
                <div style="width: 30%; background-color: #272727; padding: 15px; border-radius: 8px; border: 1px solid #333;">
                    <div style="color: #9945FF; font-weight: bold; margin-bottom: 10px;">Secondary Layer</div>
                    <div style="color: #AAA; font-size: 0.9rem;">Project-specific collaboration units</div>
                </div>
                <div style="width: 30%; background-color: #272727; padding: 15px; border-radius: 8px; border: 1px solid #333;">
                    <div style="color: #9945FF; font-weight: bold; margin-bottom: 10px;">Entity Layer</div>
                    <div style="color: #AAA; font-size: 0.9rem;">Stakeholder profiles & data</div>
                </div>
            </div>
            <div style="background-color: #272727; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 20px;">
                <div style="color: #14F195; font-weight: bold; margin-bottom: 10px;">Smart Contracts</div>
                <div style="color: #AAA; font-size: 0.9rem;">Agreements, Funding, Distribution, Compliance</div>
            </div>
            <div style="background-color: #272727; padding: 15px; border-radius: 8px; border: 1px solid #333;">
                <div style="color: #14F195; font-weight: bold; margin-bottom: 10px;">Solana Blockchain</div>
                <div style="color: #AAA; font-size: 0.9rem;">High throughput, low fees, fast finality</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
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
        
        # Economic model visualization
        col1, col2 = st.columns(2)
        
        with col1:
            # Token distribution chart
            token_data = pd.DataFrame({
                'Category': ['Research Contribution', 'Platform Development', 'Community Governance', 'Partnership Incentives', 'Reserve'],
                'Percentage': [40, 25, 15, 10, 10]
            })
            
            st.markdown("#### Token Distribution")
            st.bar_chart(token_data.set_index('Category'))
        
        with col2:
            # Revenue streams
            st.markdown("#### Revenue Streams")
            st.markdown("""
            <div class="stCard">
                <div style="margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #FFFFFF;">Transaction Fees:</span>
                        <span class="metric-value">45%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #FFFFFF;">Premium Subscriptions:</span>
                        <span class="metric-value">30%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #FFFFFF;">Value-Added Services:</span>
                        <span class="metric-value">20%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #FFFFFF;">DeFi Integration:</span>
                        <span class="metric-value">5%</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Implementation Framework
    with st.expander("Implementation Framework"):
        st.markdown("""
        DAPPR's development follows a structured six-phase roadmap to ensure scalability,
        reliability, and stakeholder engagement.
        
        #### Development Roadmap
        
        1. **Requirements Analysis (3-6 months)**: Define functional and technical requirements
        2. **Prototype Development (6-9 months)**: Build Solana-based prototype with smart contracts
        3. **Pilot Testing (3-6 months)**: Controlled testing with select institutions
        4. **Beta Launch (6 months)**: Limited public release with core functionality
        5. **Full Deployment (3 months)**: Complete platform release with all features
        6. **Continuous Improvement**: Ongoing development and feature enhancement
        """)
        
        # Timeline visualization
        st.markdown("""
        <div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; margin-top: 15px;">
            <div style="color: #14F195; margin-bottom: 15px; font-weight: bold; text-align: center;">IMPLEMENTATION TIMELINE</div>
            <div style="position: relative; height: 60px; margin-bottom: 30px;">
                <div style="position: absolute; top: 25px; left: 0; right: 0; height: 2px; background-color: #333;"></div>
                <div style="position: absolute; top: 21px; left: 0%; width: 10px; height: 10px; background-color: #14F195; border-radius: 50%;"></div>
                <div style="position: absolute; top: 21px; left: 20%; width: 10px; height: 10px; background-color: #14F195; border-radius: 50%;"></div>
                <div style="position: absolute; top: 21px; left: 40%; width: 10px; height: 10px; background-color: #14F195; border-radius: 50%;"></div>
                <div style="position: absolute; top: 21px; left: 60%; width: 10px; height: 10px; background-color: #9945FF; border-radius: 50%;"></div>
                <div style="position: absolute; top: 21px; left: 80%; width: 10px; height: 10px; background-color: #9945FF; border-radius: 50%;"></div>
                <div style="position: absolute; top: 21px; left: 100%; width: 10px; height: 10px; background-color: #9945FF; border-radius: 50%;"></div>
                
                <div style="position: absolute; top: 0; left: 0%; transform: translateX(-50%); color: #AAA; font-size: 0.8rem;">Start</div>
                <div style="position: absolute; top: 0; left: 20%; transform: translateX(-50%); color: #AAA; font-size: 0.8rem;">Q2 2025</div>
                <div style="position: absolute; top: 0; left: 40%; transform: translateX(-50%); color: #AAA; font-size: 0.8rem;">Q4 2025</div>
                <div style="position: absolute; top: 0; left: 60%; transform: translateX(-50%); color: #AAA; font-size: 0.8rem;">Q2 2026</div>
                <div style="position: absolute; top: 0; left: 80%; transform: translateX(-50%); color: #AAA; font-size: 0.8rem;">Q4 2026</div>
                <div style="position: absolute; top: 0; left: 100%; transform: translateX(-50%); color: #AAA; font-size: 0.8rem;">Q2 2027</div>
                
                <div style="position: absolute; top: 35px; left: 0%; transform: translateX(-50%); color: #14F195; font-size: 0.8rem; text-align: center; width: 100px;">Requirements</div>
                <div style="position: absolute; top: 35px; left: 20%; transform: translateX(-50%); color: #14F195; font-size: 0.8rem; text-align: center; width: 100px;">Prototype</div>
                <div style="position: absolute; top: 35px; left: 40%; transform: translateX(-50%); color: #14F195; font-size: 0.8rem; text-align: center; width: 100px;">Pilot</div>
                <div style="position: absolute; top: 35px; left: 60%; transform: translateX(-50%); color: #9945FF; font-size: 0.8rem; text-align: center; width: 100px;">Beta</div>
                <div style="position: absolute; top: 35px; left: 80%; transform: translateX(-50%); color: #9945FF; font-size: 0.8rem; text-align: center; width: 100px;">Deployment</div>
                <div style="position: absolute; top: 35px; left: 100%; transform: translateX(-50%); color: #9945FF; font-size: 0.8rem; text-align: center; width: 100px;">Continuous</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced Conclusion section
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(0, 255, 163, 0.05) 0%, rgba(20, 241, 149, 0.05) 100%);
        border: 1px solid rgba(0, 255, 163, 0.2);
        border-radius: 20px;
        padding: 30px;
        margin: 30px 0;
        position: relative;
    ">
        <h3 style="
            color: #00FFA3; 
            font-size: 1.8rem; 
            font-weight: 600; 
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 12px;
        ">
            <span style="
                background: linear-gradient(135deg, #00FFA3 0%, #14F195 100%);
                border-radius: 10px;
                padding: 8px;
                font-size: 1.2rem;
            ">🚀</span>
            Conclusion
        </h3>
        <p style="
            color: #FFFFFF; 
            font-size: 1.1rem; 
            line-height: 1.7; 
            margin: 0;
            text-align: justify;
        ">
            DAPPR represents a paradigm shift in academia-industry collaboration, leveraging Solana's 
            blockchain capabilities to create a transparent, efficient, and equitable system. By 
            addressing long-standing challenges in research collaboration, DAPPR has the potential to 
            accelerate innovation and knowledge transfer on a global scale, creating significant value 
            for all stakeholders involved.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Call-to-action section
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
        border: 2px solid transparent;
        background-clip: padding-box;
        border-radius: 25px;
        padding: 40px;
        margin: 40px 0;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    ">
        <!-- Animated gradient border -->
        <div style="
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, #14F195, #9945FF, #00FFA3, #14F195);
            border-radius: 25px;
            z-index: -1;
            background-size: 300% 300%;
            animation: gradientShift 3s ease infinite;
        "></div>
        
        <h3 style="
            color: #FFFFFF; 
            font-size: 2rem; 
            font-weight: 700; 
            margin-bottom: 20px;
            background: linear-gradient(135deg, #14F195 0%, #9945FF 50%, #00FFA3 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        ">Join the DAPPR Ecosystem</h3>
        
        <p style="
            color: #CCCCCC; 
            font-size: 1.2rem; 
            line-height: 1.6; 
            margin-bottom: 30px;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        ">
            Be part of the revolution in academia-industry collaboration. 
            Connect your wallet to explore the platform and start building the future of research.
        </p>
        
        <div style="
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
        ">
            <div style="
                background: rgba(20, 241, 149, 0.1);
                border: 1px solid #14F195;
                border-radius: 15px;
                padding: 15px 25px;
                color: #14F195;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
            ">🔗 Connect Wallet</div>
            
            <div style="
                background: rgba(153, 69, 255, 0.1);
                border: 1px solid #9945FF;
                border-radius: 15px;
                padding: 15px 25px;
                color: #9945FF;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
            ">📚 Explore Platform</div>
        </div>
    </div>
    
    <style>
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
    </style>
    """, unsafe_allow_html=True)