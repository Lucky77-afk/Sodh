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
    
    # Why We Started Building DAPPR section
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(153, 69, 255, 0.05) 0%, rgba(20, 241, 149, 0.05) 100%);
        border: 1px solid rgba(153, 69, 255, 0.2);
        border-radius: 20px;
        padding: 30px;
        margin: 30px 0;
        position: relative;
    ">
        <h3 style="
            color: #9945FF; 
            font-size: 1.8rem; 
            font-weight: 600; 
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 12px;
        ">
            <span style="
                background: linear-gradient(135deg, #9945FF 0%, #14F195 100%);
                border-radius: 10px;
                padding: 8px;
                font-size: 1.2rem;
            ">🔬</span>
            Why We Started Building DAPPR
        </h3>
        <p style="
            color: #FFFFFF; 
            font-size: 1.1rem; 
            line-height: 1.7; 
            margin-bottom: 20px;
            text-align: justify;
        ">
            We created DAPPR in response to a critical observation: despite tremendous advances in both academic research and industry innovation, the bridge between these worlds remains fundamentally broken. Through extensive experience straddling both environments, we identified several systemic problems that effectively trap valuable knowledge in silos.
        </p>
        
        <div style="
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 25px;
        ">
            <div style="
                background: rgba(20, 241, 149, 0.05);
                border: 1px solid rgba(20, 241, 149, 0.2);
                border-radius: 15px;
                padding: 20px;
            ">
                <h4 style="color: #14F195; margin-bottom: 12px; font-size: 1.1rem;">🎯 Incentive Misalignment</h4>
                <p style="color: #CCCCCC; font-size: 0.95rem; line-height: 1.5; margin: 0;">
                    Academic rewards publication metrics while industry prioritizes commercial applications, creating structural disconnects that prevent transformative research from reaching real-world applications.
                </p>
            </div>
            
            <div style="
                background: rgba(255, 107, 107, 0.05);
                border: 1px solid rgba(255, 107, 107, 0.2);
                border-radius: 15px;
                padding: 20px;
            ">
                <h4 style="color: #FF6B6B; margin-bottom: 12px; font-size: 1.1rem;">📋 IP Framework Issues</h4>
                <p style="color: #CCCCCC; font-size: 0.95rem; line-height: 1.5; margin: 0;">
                    Traditional collaboration requires navigating byzantine legal agreements that often take longer to negotiate than the actual research, creating risk-averse environments.
                </p>
            </div>
            
            <div style="
                background: rgba(255, 215, 0, 0.05);
                border: 1px solid rgba(255, 215, 0, 0.2);
                border-radius: 15px;
                padding: 20px;
            ">
                <h4 style="color: #FFD700; margin-bottom: 12px; font-size: 1.1rem;">🤝 Attribution & Trust Deficits</h4>
                <p style="color: #CCCCCC; font-size: 0.95rem; line-height: 1.5; margin: 0;">
                    Researchers fear inadequate recognition while industry struggles with accountability, lacking verifiable systems for permanent attribution and trust building.
                </p>
            </div>
            
            <div style="
                background: rgba(0, 255, 163, 0.05);
                border: 1px solid rgba(0, 255, 163, 0.2);
                border-radius: 15px;
                padding: 20px;
            ">
                <h4 style="color: #00FFA3; margin-bottom: 12px; font-size: 1.1rem;">🔍 Systemic Opacity</h4>
                <p style="color: #CCCCCC; font-size: 0.95rem; line-height: 1.5; margin: 0;">
                    Limited visibility across institutional boundaries leads to redundant work, missed synergies, and inefficient resource allocation, particularly disadvantaging emerging fields.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Market Opportunity section
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.05) 0%, rgba(255, 107, 107, 0.05) 100%);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 20px;
        padding: 30px;
        margin: 30px 0;
        position: relative;
    ">
        <h3 style="
            color: #FFD700; 
            font-size: 1.8rem; 
            font-weight: 600; 
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 12px;
        ">
            <span style="
                background: linear-gradient(135deg, #FFD700 0%, #FF6B6B 100%);
                border-radius: 10px;
                padding: 8px;
                font-size: 1.2rem;
            ">💰</span>
            Market Opportunity
        </h3>
        
        <div style="
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
            margin-top: 25px;
        ">
            <div style="
                background: rgba(20, 241, 149, 0.05);
                border: 1px solid rgba(20, 241, 149, 0.2);
                border-radius: 15px;
                padding: 20px;
                text-align: center;
            ">
                <div style="color: #14F195; font-size: 2.2rem; font-weight: 700; margin-bottom: 8px;">$2.4T</div>
                <div style="color: #FFFFFF; font-size: 1rem; font-weight: 600; margin-bottom: 8px;">Global R&D Investment</div>
                <div style="color: #AAAAAA; font-size: 0.9rem; line-height: 1.4;">
                    Annual worldwide research spending, with 60-80% never translating to practical applications
                </div>
            </div>
            
            <div style="
                background: rgba(153, 69, 255, 0.05);
                border: 1px solid rgba(153, 69, 255, 0.2);
                border-radius: 15px;
                padding: 20px;
                text-align: center;
            ">
                <div style="color: #9945FF; font-size: 2.2rem; font-weight: 700; margin-bottom: 8px;">$1.5T</div>
                <div style="color: #FFFFFF; font-size: 1rem; font-weight: 600; margin-bottom: 8px;">Stranded Innovation Value</div>
                <div style="color: #AAAAAA; font-size: 0.9rem; line-height: 1.4;">
                    Potentially stranded innovation value annually due to collaboration barriers
                </div>
            </div>
            
            <div style="
                background: rgba(255, 215, 0, 0.05);
                border: 1px solid rgba(255, 215, 0, 0.2);
                border-radius: 15px;
                padding: 20px;
                text-align: center;
            ">
                <div style="color: #FFD700; font-size: 2.2rem; font-weight: 700; margin-bottom: 8px;">$250B</div>
                <div style="color: #FFFFFF; font-size: 1rem; font-weight: 600; margin-bottom: 8px;">University Research Budgets</div>
                <div style="color: #AAAAAA; font-size: 0.9rem; line-height: 1.4;">
                    Collective annual budgets capturing less than 5% of commercial value generated
                </div>
            </div>
            
            <div style="
                background: rgba(0, 255, 163, 0.05);
                border: 1px solid rgba(0, 255, 163, 0.2);
                border-radius: 15px;
                padding: 20px;
                text-align: center;
            ">
                <div style="color: #00FFA3; font-size: 2.2rem; font-weight: 700; margin-bottom: 8px;">14mo</div>
                <div style="color: #FFFFFF; font-size: 1rem; font-weight: 600; margin-bottom: 8px;">Legal Process Duration</div>
                <div style="color: #AAAAAA; font-size: 0.9rem; line-height: 1.4;">
                    Average time for industry partners to navigate legal processes before collaboration
                </div>
            </div>
        </div>
        
        <div style="
            background: rgba(255, 255, 255, 0.02);
            border-radius: 15px;
            padding: 20px;
            margin-top: 25px;
            text-align: center;
        ">
            <p style="
                color: #FFFFFF; 
                font-size: 1.1rem; 
                line-height: 1.6; 
                margin: 0;
                font-style: italic;
            ">
                We're targeting <strong style="color: #14F195;">"near-commercial research"</strong> – the estimated $1.2 trillion in annual academic output that could create immediate industry impact if collaboration barriers were removed.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Long-Term Vision section
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(0, 255, 163, 0.05) 0%, rgba(153, 69, 255, 0.05) 100%);
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
                background: linear-gradient(135deg, #00FFA3 0%, #9945FF 100%);
                border-radius: 10px;
                padding: 8px;
                font-size: 1.2rem;
            ">🔮</span>
            Long-Term Vision
        </h3>
        <p style="
            color: #FFFFFF; 
            font-size: 1.1rem; 
            line-height: 1.7; 
            margin-bottom: 25px;
            text-align: justify;
        ">
            Our vision for DAPPR transcends creating just another research platform; we're building the foundation for a new innovation economy where knowledge creation and application function seamlessly across traditional boundaries.
        </p>
        
        <div style="margin: 25px 0;">
            <div style="
                background: rgba(20, 241, 149, 0.03);
                border-left: 4px solid #14F195;
                padding: 20px;
                margin: 15px 0;
                border-radius: 0 15px 15px 0;
            ">
                <h4 style="color: #14F195; margin-bottom: 12px; font-size: 1.1rem;">🆔 Self-Sovereign Research Identity</h4>
                <p style="color: #CCCCCC; font-size: 0.95rem; line-height: 1.5; margin: 0;">
                    Blockchain-verified identity system where researchers' contributions, impact, and reputation become portable assets that transcend institutional boundaries, creating career mobility and shifting power dynamics toward individual contributors.
                </p>
            </div>
            
            <div style="
                background: rgba(153, 69, 255, 0.03);
                border-left: 4px solid #9945FF;
                padding: 20px;
                margin: 15px 0;
                border-radius: 0 15px 15px 0;
            ">
                <h4 style="color: #9945FF; margin-bottom: 12px; font-size: 1.1rem;">⚡ Frictionless Knowledge Markets</h4>
                <p style="color: #CCCCCC; font-size: 0.95rem; line-height: 1.5; margin: 0;">
                    Automated attribution, IP management, and value distribution through smart contracts enable instantaneous research collaborations that would be logistically impossible under current frameworks.
                </p>
            </div>
            
            <div style="
                background: rgba(255, 215, 0, 0.03);
                border-left: 4px solid #FFD700;
                padding: 20px;
                margin: 15px 0;
                border-radius: 0 15px 15px 0;
            ">
                <h4 style="color: #FFD700; margin-bottom: 12px; font-size: 1.1rem;">🌍 Democratized Access to Innovation</h4>
                <p style="color: #CCCCCC; font-size: 0.95rem; line-height: 1.5; margin: 0;">
                    Progressive removal of institutional gatekeepers, allowing individual researchers worldwide to connect directly with industry partners and enabling smaller companies to access cutting-edge research.
                </p>
            </div>
            
            <div style="
                background: rgba(0, 255, 163, 0.03);
                border-left: 4px solid #00FFA3;
                padding: 20px;
                margin: 15px 0;
                border-radius: 0 15px 15px 0;
            ">
                <h4 style="color: #00FFA3; margin-bottom: 12px; font-size: 1.1rem;">🕸️ Cross-boundary Knowledge Graph</h4>
                <p style="color: #CCCCCC; font-size: 0.95rem; line-height: 1.5; margin: 0;">
                    As the platform scales, it generates an unprecedented map of research connections and complementary innovations, creating visibility across traditional silos and enabling AI-suggested collaborations.
                </p>
            </div>
        </div>
        
        <div style="
            background: linear-gradient(135deg, rgba(20, 241, 149, 0.1) 0%, rgba(0, 255, 163, 0.1) 100%);
            border-radius: 15px;
            padding: 25px;
            margin-top: 25px;
            text-align: center;
        ">
            <p style="
                color: #FFFFFF; 
                font-size: 1.2rem; 
                line-height: 1.6; 
                margin: 0;
                font-weight: 500;
            ">
                In its fullest expression, DAPPR will function as <strong style="color: #14F195;">essential infrastructure for human innovation</strong> – as fundamental to knowledge creation as the internet has become to information sharing.
            </p>
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