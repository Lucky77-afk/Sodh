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
        <div style="
            background: rgba(153, 69, 255, 0.05);
            border: 1px solid rgba(153, 69, 255, 0.3);
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
        ">
            <h4 style="color: #9945FF;">🔧 Understanding DAPPR Smart Contracts</h4>
            <p style="color: #CCCCCC; line-height: 1.6;">
                DAPPR's smart contracts are self-executing digital agreements that automatically enforce collaboration terms without intermediaries. Built on Solana's high-performance blockchain, they ensure transparency, security, and efficiency in research partnerships.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 🏗️ Core Smart Contract Components")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="
                background: rgba(20, 241, 149, 0.05);
                border: 1px solid rgba(20, 241, 149, 0.3);
                border-radius: 12px;
                padding: 20px;
                margin: 10px 0;
            ">
                <h5 style="color: #14F195;">🔒 Project Agreement Contract</h5>
                <ul style="color: #CCCCCC; font-size: 0.9rem;">
                    <li>Defines research objectives and scope</li>
                    <li>Sets intellectual property sharing rules</li>
                    <li>Establishes participant roles and responsibilities</li>
                    <li>Creates immutable collaboration terms</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="
                background: rgba(255, 215, 0, 0.05);
                border: 1px solid rgba(255, 215, 0, 0.3);
                border-radius: 12px;
                padding: 20px;
                margin: 10px 0;
            ">
                <h5 style="color: #FFD700;">⏱️ Milestone Management</h5>
                <ul style="color: #CCCCCC; font-size: 0.9rem;">
                    <li>Breaks projects into measurable phases</li>
                    <li>Tracks deliverable completion status</li>
                    <li>Manages deadline and timeline enforcement</li>
                    <li>Validates milestone achievement criteria</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="
                background: rgba(255, 107, 107, 0.05);
                border: 1px solid rgba(255, 107, 107, 0.3);
                border-radius: 12px;
                padding: 20px;
                margin: 10px 0;
            ">
                <h5 style="color: #FF6B6B;">💰 Payment Escrow System</h5>
                <ul style="color: #CCCCCC; font-size: 0.9rem;">
                    <li>Holds funds securely until milestones complete</li>
                    <li>Automates payment distribution to participants</li>
                    <li>Supports both SOL and USDT transactions</li>
                    <li>Provides transparent fund tracking</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="
                background: rgba(0, 255, 163, 0.05);
                border: 1px solid rgba(0, 255, 163, 0.3);
                border-radius: 12px;
                padding: 20px;
                margin: 10px 0;
            ">
                <h5 style="color: #00FFA3;">📊 Governance & Voting</h5>
                <ul style="color: #CCCCCC; font-size: 0.9rem;">
                    <li>Enables democratic decision-making</li>
                    <li>Manages dispute resolution processes</li>
                    <li>Handles project modification requests</li>
                    <li>Implements weighted voting by contribution</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("#### 🔄 Smart Contract Lifecycle")
        
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.02);
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <div style="text-align: center; flex: 1;">
                    <div style="background: #14F195; color: #000; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px; font-weight: bold;">1</div>
                    <div style="color: #14F195; font-weight: 600;">Initialize</div>
                    <div style="color: #AAAAAA; font-size: 0.8rem;">Deploy contract with project parameters</div>
                </div>
                <div style="color: #666; font-size: 1.5rem;">→</div>
                <div style="text-align: center; flex: 1;">
                    <div style="background: #9945FF; color: #FFF; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px; font-weight: bold;">2</div>
                    <div style="color: #9945FF; font-weight: 600;">Execute</div>
                    <div style="color: #AAAAAA; font-size: 0.8rem;">Participants interact and complete milestones</div>
                </div>
                <div style="color: #666; font-size: 1.5rem;">→</div>
                <div style="text-align: center; flex: 1;">
                    <div style="background: #FFD700; color: #000; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px; font-weight: bold;">3</div>
                    <div style="color: #FFD700; font-weight: 600;">Validate</div>
                    <div style="color: #AAAAAA; font-size: 0.8rem;">Automated verification of deliverables</div>
                </div>
                <div style="color: #666; font-size: 1.5rem;">→</div>
                <div style="text-align: center; flex: 1;">
                    <div style="background: #00FFA3; color: #000; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px; font-weight: bold;">4</div>
                    <div style="color: #00FFA3; font-weight: 600;">Distribute</div>
                    <div style="color: #AAAAAA; font-size: 0.8rem;">Automatic payment and IP allocation</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown("### 🔬 Creating Research Projects")
        
        st.markdown("""
        <div style="
            background: rgba(20, 241, 149, 0.05);
            border: 1px solid rgba(20, 241, 149, 0.3);
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
        ">
            <h4 style="color: #14F195;">🎯 Project Creation Overview</h4>
            <p style="color: #CCCCCC; line-height: 1.6;">
                Creating a research project on DAPPR involves setting up a comprehensive collaboration framework that defines objectives, participants, timelines, and funding mechanisms. Each project becomes a smart contract that automatically manages the entire research lifecycle.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 📋 Detailed Project Setup Process")
        
        # Step 1: Project Definition
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.02);
            border-left: 4px solid #14F195;
            border-radius: 0 12px 12px 0;
            padding: 20px;
            margin: 15px 0;
        ">
            <h5 style="color: #14F195; margin-bottom: 15px;">📝 Step 1: Project Definition & Scope</h5>
            <div style="color: #CCCCCC; line-height: 1.5;">
                <p><strong>Research Objectives:</strong></p>
                <ul>
                    <li>Define clear, measurable research goals</li>
                    <li>Specify expected outcomes and deliverables</li>
                    <li>Set success criteria and validation methods</li>
                    <li>Establish timeline and key milestones</li>
                </ul>
                
                <p><strong>Scope Definition:</strong></p>
                <ul>
                    <li>Technical requirements and methodologies</li>
                    <li>Resource needs (equipment, data, expertise)</li>
                    <li>Regulatory compliance requirements</li>
                    <li>Risk assessment and mitigation strategies</li>
                </ul>
                
                <p><strong>Example Project Template:</strong></p>
                <div style="background: rgba(20, 241, 149, 0.1); padding: 15px; border-radius: 8px; margin: 10px 0;">
                    <em style="color: #00FFA3;">
                    "Development of AI-powered drug discovery platform for rare diseases using machine learning algorithms to analyze molecular structures and predict therapeutic efficacy within 18 months."
                    </em>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Step 2: Team Assembly
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.02);
            border-left: 4px solid #9945FF;
            border-radius: 0 12px 12px 0;
            padding: 20px;
            margin: 15px 0;
        ">
            <h5 style="color: #9945FF; margin-bottom: 15px;">👥 Step 2: Team Assembly & Role Definition</h5>
            <div style="color: #CCCCCC; line-height: 1.5;">
                <p><strong>Participant Categories:</strong></p>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 15px 0;">
                    <div style="background: rgba(153, 69, 255, 0.1); padding: 12px; border-radius: 8px;">
                        <strong style="color: #9945FF;">🎓 Academic Researchers</strong><br>
                        <small>Principal investigators, graduate students, postdocs</small>
                    </div>
                    <div style="background: rgba(20, 241, 149, 0.1); padding: 12px; border-radius: 8px;">
                        <strong style="color: #14F195;">🏢 Industry Partners</strong><br>
                        <small>R&D teams, product managers, technical leads</small>
                    </div>
                    <div style="background: rgba(255, 215, 0, 0.1); padding: 12px; border-radius: 8px;">
                        <strong style="color: #FFD700;">🔬 Subject Matter Experts</strong><br>
                        <small>Consultants, advisors, domain specialists</small>
                    </div>
                    <div style="background: rgba(255, 107, 107, 0.1); padding: 12px; border-radius: 8px;">
                        <strong style="color: #FF6B6B;">💰 Funding Entities</strong><br>
                        <small>Investors, grants, institutional funds</small>
                    </div>
                </div>
                
                <p><strong>Role Definition Process:</strong></p>
                <ul>
                    <li>Specify contribution expectations for each participant</li>
                    <li>Define decision-making authority and voting weights</li>
                    <li>Set communication protocols and reporting requirements</li>
                    <li>Establish intellectual property contribution percentages</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Step 3: Milestone Planning
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.02);
            border-left: 4px solid #FFD700;
            border-radius: 0 12px 12px 0;
            padding: 20px;
            margin: 15px 0;
        ">
            <h5 style="color: #FFD700; margin-bottom: 15px;">⏱️ Step 3: Comprehensive Milestone Planning</h5>
            <div style="color: #CCCCCC; line-height: 1.5;">
                <p><strong>Milestone Structure Framework:</strong></p>
                
                <div style="background: rgba(255, 215, 0, 0.05); padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <strong style="color: #FFD700;">Phase 1: Research & Development (Months 1-6)</strong>
                    <ul style="margin: 10px 0;">
                        <li>Literature review and competitive analysis</li>
                        <li>Technical feasibility studies</li>
                        <li>Prototype development and initial testing</li>
                        <li>Preliminary results validation</li>
                    </ul>
                    <em style="color: #AAAAAA;">Funding Release: 30% of total project budget</em>
                </div>
                
                <div style="background: rgba(153, 69, 255, 0.05); padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <strong style="color: #9945FF;">Phase 2: Implementation & Testing (Months 7-12)</strong>
                    <ul style="margin: 10px 0;">
                        <li>Full-scale development and optimization</li>
                        <li>Comprehensive testing and validation</li>
                        <li>Performance benchmarking</li>
                        <li>Documentation and IP filing</li>
                    </ul>
                    <em style="color: #AAAAAA;">Funding Release: 40% of total project budget</em>
                </div>
                
                <div style="background: rgba(20, 241, 149, 0.05); padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <strong style="color: #14F195;">Phase 3: Commercialization & Deployment (Months 13-18)</strong>
                    <ul style="margin: 10px 0;">
                        <li>Market validation and user testing</li>
                        <li>Regulatory approval processes</li>
                        <li>Production scaling and deployment</li>
                        <li>Final deliverable transfer</li>
                    </ul>
                    <em style="color: #AAAAAA;">Funding Release: 30% of total project budget</em>
                </div>
                
                <p><strong>Milestone Validation Criteria:</strong></p>
                <ul>
                    <li>Objective, measurable deliverables</li>
                    <li>Peer review and validation processes</li>
                    <li>Performance benchmarks and KPIs</li>
                    <li>Documentation and reproducibility requirements</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Step 4: Agreement Terms
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.02);
            border-left: 4px solid #00FFA3;
            border-radius: 0 12px 12px 0;
            padding: 20px;
            margin: 15px 0;
        ">
            <h5 style="color: #00FFA3; margin-bottom: 15px;">📄 Step 4: Smart Contract Agreement Terms</h5>
            <div style="color: #CCCCCC; line-height: 1.5;">
                <p><strong>Intellectual Property Framework:</strong></p>
                <div style="background: rgba(0, 255, 163, 0.05); padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;">
                        <div>
                            <strong style="color: #00FFA3;">Background IP:</strong><br>
                            <small>Pre-existing intellectual property remains with original owners</small>
                        </div>
                        <div>
                            <strong style="color: #00FFA3;">Foreground IP:</strong><br>
                            <small>New IP created during collaboration shared based on contribution</small>
                        </div>
                        <div>
                            <strong style="color: #00FFA3;">Commercial Rights:</strong><br>
                            <small>Usage rights, licensing terms, and revenue sharing agreements</small>
                        </div>
                        <div>
                            <strong style="color: #00FFA3;">Publication Rights:</strong><br>
                            <small>Academic publication protocols and industry disclosure requirements</small>
                        </div>
                    </div>
                </div>
                
                <p><strong>Financial Terms & Distribution:</strong></p>
                <ul>
                    <li>Total project budget and funding sources</li>
                    <li>Milestone-based payment schedules</li>
                    <li>Contribution-weighted profit sharing</li>
                    <li>Expense reimbursement policies</li>
                    <li>Success bonus structures and performance incentives</li>
                </ul>
                
                <p><strong>Governance & Dispute Resolution:</strong></p>
                <ul>
                    <li>Voting mechanisms for project decisions</li>
                    <li>Conflict resolution procedures</li>
                    <li>Project modification and scope change protocols</li>
                    <li>Termination conditions and asset distribution</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Practical Example
        st.markdown("#### 💡 Complete Project Example")
        
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(20, 241, 149, 0.1) 0%, rgba(153, 69, 255, 0.1) 100%);
            border: 1px solid rgba(20, 241, 149, 0.3);
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
        ">
            <h5 style="color: #14F195; margin-bottom: 15px;">🔬 Case Study: "Neural Network Drug Discovery Platform"</h5>
            <div style="color: #CCCCCC; line-height: 1.6;">
                <p><strong>Project Overview:</strong> Develop an AI-powered platform for accelerated drug discovery targeting rare neurological diseases.</p>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0;">
                    <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 8px;">
                        <strong style="color: #9945FF;">📊 Project Metrics:</strong>
                        <ul style="margin: 10px 0;">
                            <li>Duration: 24 months</li>
                            <li>Total Budget: $2.5M</li>
                            <li>Team Size: 12 participants</li>
                            <li>Expected ROI: 300-500%</li>
                        </ul>
                    </div>
                    
                    <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 8px;">
                        <strong style="color: #FFD700;">🎯 Key Deliverables:</strong>
                        <ul style="margin: 10px 0;">
                            <li>AI prediction algorithms</li>
                            <li>Validated drug candidates</li>
                            <li>Clinical trial protocols</li>
                            <li>Regulatory submissions</li>
                        </ul>
                    </div>
                </div>
                
                <p><strong>Participant Structure:</strong></p>
                <ul>
                    <li><strong>Stanford AI Lab</strong> (40% contribution): Machine learning algorithms and model development</li>
                    <li><strong>Pharmaceutical Partner</strong> (35% contribution): Drug synthesis and clinical expertise</li>
                    <li><strong>Biotech Startup</strong> (15% contribution): Platform development and deployment</li>
                    <li><strong>NIH Grant</strong> (10% contribution): Funding and regulatory guidance</li>
                </ul>
                
                <div style="background: rgba(20, 241, 149, 0.1); padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <strong style="color: #14F195;">💰 Smart Contract Automation:</strong>
                    <p style="margin: 10px 0;">
                    The smart contract automatically releases $750K after Phase 1 completion (algorithm validation), 
                    $1.25M after Phase 2 (successful drug candidate identification), and $500K upon final deliverable 
                    transfer. IP ownership is automatically distributed: 40% Stanford, 35% Pharma, 15% Biotech, 10% Public Domain.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[3]:
        st.markdown("### 🤝 Managing Collaborations")
        
        st.markdown("""
        <div style="
            background: rgba(255, 107, 107, 0.05);
            border: 1px solid rgba(255, 107, 107, 0.3);
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
        ">
            <h4 style="color: #FF6B6B;">🎯 Collaboration Management Framework</h4>
            <p style="color: #CCCCCC; line-height: 1.6;">
                DAPPR provides comprehensive tools for managing complex multi-party research collaborations, ensuring transparency, accountability, and efficient coordination throughout the entire project lifecycle.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 📊 Real-Time Project Monitoring")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="
                background: rgba(20, 241, 149, 0.05);
                border: 1px solid rgba(20, 241, 149, 0.3);
                border-radius: 12px;
                padding: 20px;
                margin: 10px 0;
            ">
                <h5 style="color: #14F195;">📈 Progress Tracking Dashboard</h5>
                <ul style="color: #CCCCCC; font-size: 0.9rem;">
                    <li><strong>Milestone Completion:</strong> Visual progress bars and status indicators</li>
                    <li><strong>Task Distribution:</strong> Individual contributor workload monitoring</li>
                    <li><strong>Timeline Adherence:</strong> Deadline tracking and delay alerts</li>
                    <li><strong>Budget Utilization:</strong> Real-time spending and allocation tracking</li>
                    <li><strong>Quality Metrics:</strong> Deliverable assessment and validation scores</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="
                background: rgba(153, 69, 255, 0.05);
                border: 1px solid rgba(153, 69, 255, 0.3);
                border-radius: 12px;
                padding: 20px;
                margin: 10px 0;
            ">
                <h5 style="color: #9945FF;">🔔 Automated Notifications</h5>
                <ul style="color: #CCCCCC; font-size: 0.9rem;">
                    <li><strong>Milestone Alerts:</strong> Upcoming deadlines and completion reminders</li>
                    <li><strong>Payment Notifications:</strong> Funding releases and distribution updates</li>
                    <li><strong>Collaboration Updates:</strong> New participant additions or role changes</li>
                    <li><strong>Governance Events:</strong> Voting opportunities and decision outcomes</li>
                    <li><strong>Issue Escalation:</strong> Conflict detection and resolution triggers</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="
                background: rgba(255, 215, 0, 0.05);
                border: 1px solid rgba(255, 215, 0, 0.3);
                border-radius: 12px;
                padding: 20px;
                margin: 10px 0;
            ">
                <h5 style="color: #FFD700;">📋 Performance Analytics</h5>
                <ul style="color: #CCCCCC; font-size: 0.9rem;">
                    <li><strong>Contribution Metrics:</strong> Individual and team productivity analysis</li>
                    <li><strong>Impact Assessment:</strong> Research output quality and significance</li>
                    <li><strong>Collaboration Efficiency:</strong> Communication and coordination effectiveness</li>
                    <li><strong>Resource Optimization:</strong> Budget and time utilization insights</li>
                    <li><strong>Predictive Analytics:</strong> Project success probability forecasting</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="
                background: rgba(0, 255, 163, 0.05);
                border: 1px solid rgba(0, 255, 163, 0.3);
                border-radius: 12px;
                padding: 20px;
                margin: 10px 0;
            ">
                <h5 style="color: #00FFA3;">🌐 Cross-Platform Integration</h5>
                <ul style="color: #CCCCCC; font-size: 0.9rem;">
                    <li><strong>Research Tools:</strong> Direct integration with lab management systems</li>
                    <li><strong>Publication Platforms:</strong> Automated manuscript and patent filing</li>
                    <li><strong>Communication Channels:</strong> Slack, Teams, and Discord connectivity</li>
                    <li><strong>Version Control:</strong> Git integration for code and document management</li>
                    <li><strong>Calendar Systems:</strong> Meeting scheduling and deadline synchronization</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("#### ⚖️ Advanced Dispute Resolution System")
        
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.02);
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
        ">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
                <div style="text-align: center;">
                    <div style="background: #FF6B6B; color: #000; border-radius: 50%; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-weight: bold; font-size: 1.2rem;">1</div>
                    <h6 style="color: #FF6B6B; margin-bottom: 10px;">Automated Detection</h6>
                    <p style="color: #AAAAAA; font-size: 0.9rem;">AI monitors for potential conflicts in deliverables, timelines, or communications</p>
                </div>
                
                <div style="text-align: center;">
                    <div style="background: #FFD700; color: #000; border-radius: 50%; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-weight: bold; font-size: 1.2rem;">2</div>
                    <h6 style="color: #FFD700; margin-bottom: 10px;">Mediation Process</h6>
                    <p style="color: #AAAAAA; font-size: 0.9rem;">Structured negotiation framework with neutral mediator assignment</p>
                </div>
                
                <div style="text-align: center;">
                    <div style="background: #9945FF; color: #FFF; border-radius: 50%; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-weight: bold; font-size: 1.2rem;">3</div>
                    <h6 style="color: #9945FF; margin-bottom: 10px;">Arbitration Panel</h6>
                    <p style="color: #AAAAAA; font-size: 0.9rem;">Expert arbitrators provide binding decisions when mediation fails</p>
                </div>
                
                <div style="text-align: center;">
                    <div style="background: #14F195; color: #000; border-radius: 50%; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-weight: bold; font-size: 1.2rem;">4</div>
                    <h6 style="color: #14F195; margin-bottom: 10px;">Smart Contract Execution</h6>
                    <p style="color: #AAAAAA; font-size: 0.9rem;">Automatic implementation of resolution decisions and asset redistribution</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 🏆 Attribution & Recognition Framework")
        
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(153, 69, 255, 0.1) 0%, rgba(20, 241, 149, 0.1) 100%);
            border: 1px solid rgba(153, 69, 255, 0.3);
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
        ">
            <h5 style="color: #9945FF; margin-bottom: 20px;">🎖️ Comprehensive Contribution Tracking</h5>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0;">
                <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 8px;">
                    <strong style="color: #14F195;">📊 Quantitative Metrics:</strong>
                    <ul style="margin: 10px 0; color: #CCCCCC;">
                        <li>Code commits and documentation contributions</li>
                        <li>Research hours and experimental work</li>
                        <li>Publication authorship and citation impact</li>
                        <li>Patent filings and IP development</li>
                        <li>Funding acquisition and resource provision</li>
                    </ul>
                </div>
                
                <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 8px;">
                    <strong style="color: #FFD700;">🎯 Qualitative Assessments:</strong>
                    <ul style="margin: 10px 0; color: #CCCCCC;">
                        <li>Peer review scores and feedback quality</li>
                        <li>Leadership and collaboration effectiveness</li>
                        <li>Innovation and creative problem-solving</li>
                        <li>Mentorship and knowledge transfer</li>
                        <li>Strategic vision and project direction</li>
                    </ul>
                </div>
            </div>
            
            <div style="background: rgba(20, 241, 149, 0.1); padding: 15px; border-radius: 8px; margin: 15px 0;">
                <strong style="color: #14F195;">🔗 Blockchain Attribution:</strong>
                <p style="margin: 10px 0; color: #CCCCCC;">
                All contributions are permanently recorded on the Solana blockchain, creating an immutable record of individual and institutional contributions. This enables:
                </p>
                <ul style="color: #CCCCCC;">
                    <li>Portable reputation that follows researchers across institutions</li>
                    <li>Transparent credit allocation for funding and promotion decisions</li>
                    <li>Automatic royalty distribution based on contribution percentages</li>
                    <li>Historical impact tracking for long-term career development</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[4]:
        st.markdown("### 💰 Funding & Payments")
        
        st.markdown("""
        <div style="
            background: rgba(255, 215, 0, 0.05);
            border: 1px solid rgba(255, 215, 0, 0.3);
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
        ">
            <h4 style="color: #FFD700;">💼 DAPPR Financial Ecosystem</h4>
            <p style="color: #CCCCCC; line-height: 1.6;">
                DAPPR's sophisticated funding and payment system leverages Solana's fast, low-cost transactions to create a seamless financial infrastructure for research collaboration, supporting everything from micro-payments to multi-million dollar projects.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 💵 Comprehensive Funding Sources")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="
                background: rgba(20, 241, 149, 0.05);
                border: 1px solid rgba(20, 241, 149, 0.3);
                border-radius: 12px;
                padding: 20px;
                margin: 10px 0;
            ">
                <h5 style="color: #14F195;">🎓 Academic Funding</h5>
                <ul style="color: #CCCCCC; font-size: 0.9rem;">
                    <li><strong>Government Grants:</strong> NSF, NIH, DOE, and international funding agencies</li>
                    <li><strong>University Funds:</strong> Internal research budgets and endowment income</li>
                    <li><strong>Foundation Grants:</strong> Private foundations and charitable organizations</li>
                    <li><strong>Crowdfunding:</strong> Decentralized fundraising from global contributors</li>
                </ul>
                <div style="background: rgba(20, 241, 149, 0.1); padding: 10px; border-radius: 6px; margin-top: 10px;">
                    <small style="color: #00FFA3;"><strong>Typical Range:</strong> $50K - $5M per project</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="
                background: rgba(153, 69, 255, 0.05);
                border: 1px solid rgba(153, 69, 255, 0.3);
                border-radius: 12px;
                padding: 20px;
                margin: 10px 0;
            ">
                <h5 style="color: #9945FF;">🏢 Industry Investment</h5>
                <ul style="color: #CCCCCC; font-size: 0.9rem;">
                    <li><strong>Corporate R&D:</strong> Direct investment from Fortune 500 companies</li>
                    <li><strong>Venture Capital:</strong> Early-stage funding for commercializable research</li>
                    <li><strong>Strategic Partnerships:</strong> Long-term collaboration agreements</li>
                    <li><strong>Innovation Challenges:</strong> Competition-based funding mechanisms</li>
                </ul>
                <div style="background: rgba(153, 69, 255, 0.1); padding: 10px; border-radius: 6px; margin-top: 10px;">
                    <small style="color: #9945FF;"><strong>Typical Range:</strong> $100K - $50M per project</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="
                background: rgba(255, 107, 107, 0.05);
                border: 1px solid rgba(255, 107, 107, 0.3);
                border-radius: 12px;
                padding: 20px;
                margin: 10px 0;
            ">
                <h5 style="color: #FF6B6B;">🌐 Decentralized Funding</h5>
                <ul style="color: #CCCCCC; font-size: 0.9rem;">
                    <li><strong>Token Sales:</strong> Project-specific cryptocurrency offerings</li>
                    <li><strong>DeFi Protocols:</strong> Yield farming and liquidity mining rewards</li>
                    <li><strong>DAO Investments:</strong> Decentralized autonomous organization funding</li>
                    <li><strong>Prediction Markets:</strong> Betting on research outcomes and impact</li>
                </ul>
                <div style="background: rgba(255, 107, 107, 0.1); padding: 10px; border-radius: 6px; margin-top: 10px;">
                    <small style="color: #FF6B6B;"><strong>Typical Range:</strong> $10K - $10M per project</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="
                background: rgba(0, 255, 163, 0.05);
                border: 1px solid rgba(0, 255, 163, 0.3);
                border-radius: 12px;
                padding: 20px;
                margin: 10px 0;
            ">
                <h5 style="color: #00FFA3;">💎 Premium Features</h5>
                <ul style="color: #CCCCCC; font-size: 0.9rem;">
                    <li><strong>Success Bonuses:</strong> Performance-based additional payments</li>
                    <li><strong>IP Licensing:</strong> Revenue sharing from commercialization</li>
                    <li><strong>Royalty Streams:</strong> Ongoing payments from successful products</li>
                    <li><strong>Equity Stakes:</strong> Ownership in spin-off companies</li>
                </ul>
                <div style="background: rgba(0, 255, 163, 0.1); padding: 10px; border-radius: 6px; margin-top: 10px;">
                    <small style="color: #00FFA3;"><strong>Potential Upside:</strong> 10x - 1000x initial investment</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("#### 🔐 Advanced Payment Infrastructure")
        
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.02);
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
        ">
            <h5 style="color: #14F195; margin-bottom: 20px;">🏦 Multi-Asset Escrow System</h5>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin: 20px 0;">
                <div style="background: rgba(20, 241, 149, 0.05); padding: 15px; border-radius: 8px;">
                    <strong style="color: #14F195;">💰 Supported Currencies:</strong>
                    <ul style="margin: 10px 0; color: #CCCCCC;">
                        <li>SOL (Native Solana token)</li>
                        <li>USDC (USD Coin stablecoin)</li>
                        <li>USDT (Tether stablecoin)</li>
                        <li>Custom project tokens</li>
                        <li>Wrapped BTC and ETH</li>
                    </ul>
                </div>
                
                <div style="background: rgba(153, 69, 255, 0.05); padding: 15px; border-radius: 8px;">
                    <strong style="color: #9945FF;">🔒 Security Features:</strong>
                    <ul style="margin: 10px 0; color: #CCCCCC;">
                        <li>Multi-signature wallet protection</li>
                        <li>Time-locked fund releases</li>
                        <li>Dispute resolution freezing</li>
                        <li>Insurance coverage options</li>
                        <li>Audit trail transparency</li>
                    </ul>
                </div>
                
                <div style="background: rgba(255, 215, 0, 0.05); padding: 15px; border-radius: 8px;">
                    <strong style="color: #FFD700;">⚡ Transaction Features:</strong>
                    <ul style="margin: 10px 0; color: #CCCCCC;">
                        <li>Sub-second transaction finality</li>
                        <li>Micro-payment capabilities ($0.01+)</li>
                        <li>Batch processing for efficiency</li>
                        <li>Programmable payment schedules</li>
                        <li>Cross-border settlement</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 📊 Payment Distribution Models")
        
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(255, 215, 0, 0.1) 0%, rgba(255, 107, 107, 0.1) 100%);
            border: 1px solid rgba(255, 215, 0, 0.3);
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
        ">
            <h5 style="color: #FFD700; margin-bottom: 20px;">💡 Flexible Distribution Strategies</h5>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin: 20px 0;">
                <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 8px; text-align: center;">
                    <div style="color: #14F195; font-size: 1.5rem; margin-bottom: 10px;">📈</div>
                    <strong style="color: #14F195;">Equal Distribution</strong>
                    <p style="color: #AAAAAA; font-size: 0.9rem; margin: 8px 0;">
                    All participants receive equal shares regardless of contribution size
                    </p>
                </div>
                
                <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 8px; text-align: center;">
                    <div style="color: #9945FF; font-size: 1.5rem; margin-bottom: 10px;">⚖️</div>
                    <strong style="color: #9945FF;">Contribution-Weighted</strong>
                    <p style="color: #AAAAAA; font-size: 0.9rem; margin: 8px 0;">
                    Payments proportional to individual contribution percentages
                    </p>
                </div>
                
                <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 8px; text-align: center;">
                    <div style="color: #FFD700; font-size: 1.5rem; margin-bottom: 10px;">🎯</div>
                    <strong style="color: #FFD700;">Performance-Based</strong>
                    <p style="color: #AAAAAA; font-size: 0.9rem; margin: 8px 0;">
                    Variable payments based on milestone achievement quality
                    </p>
                </div>
                
                <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 8px; text-align: center;">
                    <div style="color: #FF6B6B; font-size: 1.5rem; margin-bottom: 10px;">🔄</div>
                    <strong style="color: #FF6B6B;">Hybrid Models</strong>
                    <p style="color: #AAAAAA; font-size: 0.9rem; margin: 8px 0;">
                    Combination of fixed and variable payment structures
                    </p>
                </div>
            </div>
            
            <div style="background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 8px; margin: 15px 0;">
                <strong style="color: #FFD700;">💎 Advanced Distribution Example:</strong>
                <p style="margin: 10px 0; color: #CCCCCC;">
                For a $1M project: 60% distributed by contribution weight, 25% equally among all participants, 15% based on peer-reviewed performance scores. Smart contracts automatically calculate and distribute payments within seconds of milestone validation.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 🚀 Real-World Implementation")
        
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.02);
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
        ">
            <h5 style="color: #00FFA3; margin-bottom: 15px;">📱 Step-by-Step Payment Process</h5>
            
            <div style="display: flex; flex-direction: column; gap: 15px;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="background: #14F195; color: #000; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0;">1</div>
                    <div style="color: #CCCCCC;">
                        <strong style="color: #14F195;">Funding Deposit:</strong> Project initiator deposits funds into escrow smart contract
                    </div>
                </div>
                
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="background: #9945FF; color: #FFF; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0;">2</div>
                    <div style="color: #CCCCCC;">
                        <strong style="color: #9945FF;">Milestone Completion:</strong> Participants submit deliverables and request validation
                    </div>
                </div>
                
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="background: #FFD700; color: #000; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0;">3</div>
                    <div style="color: #CCCCCC;">
                        <strong style="color: #FFD700;">Peer Review:</strong> Automated and human validation of milestone achievement
                    </div>
                </div>
                
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="background: #FF6B6B; color: #000; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0;">4</div>
                    <div style="color: #CCCCCC;">
                        <strong style="color: #FF6B6B;">Smart Distribution:</strong> Instant payment calculation and distribution to all participants
                    </div>
                </div>
                
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="background: #00FFA3; color: #000; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0;">5</div>
                    <div style="color: #CCCCCC;">
                        <strong style="color: #00FFA3;">Receipt & Records:</strong> Immutable blockchain records for accounting and tax purposes
                    </div>
                </div>
            </div>
            
            <div style="background: rgba(0, 255, 163, 0.1); padding: 15px; border-radius: 8px; margin: 20px 0; text-align: center;">
                <strong style="color: #00FFA3;">⚡ Average Processing Time: 15 seconds from validation to payment receipt</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
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