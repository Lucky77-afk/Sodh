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
    tabs = st.tabs(["Getting Started", "Smart Contract Basics", "Creating Projects", "Managing Collaborations", "Funding & Payments"])
    
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
        
        # Step-by-step guide with enhanced styling
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
                    Choose from supported Solana wallets to interact with the DAPPR platform:
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
                    <div style="color: #FFFFFF; margin: 8px 0; display: flex; align-items: center; gap: 10px;">
                        <span style="color: #14F195;">•</span> CoinDCX Wallet
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
                
                <h4 style="color: #9945FF; margin: 20px 0 15px 0; font-size: 1.2rem;">🔍 Explore the Platform</h4>
                <p style="color: #CCCCCC; margin-bottom: 15px; line-height: 1.5;">
                    Navigate through the main sections to understand platform capabilities:
                </p>
                <div style="margin: 15px 0;">
                    <div style="color: #FFFFFF; margin: 8px 0; display: flex; align-items: center; gap: 10px;">
                        <span style="color: #9945FF;">•</span> Dashboard - View blockchain metrics
                    </div>
                    <div style="color: #FFFFFF; margin: 8px 0; display: flex; align-items: center; gap: 10px;">
                        <span style="color: #9945FF;">•</span> Transactions - Monitor activity
                    </div>
                    <div style="color: #FFFFFF; margin: 8px 0; display: flex; align-items: center; gap: 10px;">
                        <span style="color: #9945FF;">•</span> Smart Contract - Manage collaborations
                    </div>
                    <div style="color: #FFFFFF; margin: 8px 0; display: flex; align-items: center; gap: 10px;">
                        <span style="color: #9945FF;">•</span> Account - Check wallet details
                    </div>
                </div>
            </div>
            
            <div style="
                background: linear-gradient(135deg, rgba(255, 215, 0, 0.05) 0%, rgba(255, 107, 107, 0.05) 100%);
                border: 1px solid rgba(255, 215, 0, 0.3);
                border-radius: 15px;
                padding: 25px;
                position: relative;
            ">
                <div style="
                    position: absolute;
                    top: -10px;
                    left: 20px;
                    background: #FFD700;
                    color: #000;
                    padding: 5px 15px;
                    border-radius: 15px;
                    font-size: 0.9rem;
                    font-weight: 600;
                ">STEP 3</div>
                
                <h4 style="color: #FFD700; margin: 20px 0 15px 0; font-size: 1.2rem;">🤝 Start Collaborating</h4>
                <p style="color: #CCCCCC; margin-bottom: 15px; line-height: 1.5;">
                    Begin your research collaboration journey:
                </p>
                <div style="margin: 15px 0;">
                    <div style="color: #FFFFFF; margin: 8px 0; display: flex; align-items: center; gap: 10px;">
                        <span style="color: #FFD700;">•</span> Create research projects
                    </div>
                    <div style="color: #FFFFFF; margin: 8px 0; display: flex; align-items: center; gap: 10px;">
                        <span style="color: #FFD700;">•</span> Set collaboration terms
                    </div>
                    <div style="color: #FFFFFF; margin: 8px 0; display: flex; align-items: center; gap: 10px;">
                        <span style="color: #FFD700;">•</span> Add team members
                    </div>
                    <div style="color: #FFFFFF; margin: 8px 0; display: flex; align-items: center; gap: 10px;">
                        <span style="color: #FFD700;">•</span> Track project progress
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Additional guidance section
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.02);
            border-radius: 15px;
            padding: 20px;
            margin: 25px 0;
            text-align: center;
        ">
            <p style="
                color: #CCCCCC; 
                font-size: 1.1rem; 
                line-height: 1.6; 
                margin: 0;
            ">
                💡 <strong style="color: #14F195;">Pro Tip:</strong> Start by exploring the Account page to understand wallet connections, then move to Smart Contract to see collaboration features in action.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="stCard">
            <h4 style="color: #14F195; margin-top: 0;">Step 2: Explore the Platform</h4>
            <p>
                Navigate through the different sections of DAPPR:
            </p>
            <ul>
                <li><strong>Dashboard:</strong> View Solana network statistics and performance metrics</li>
                <li><strong>Transactions:</strong> Explore and search blockchain transactions</li>
                <li><strong>Account:</strong> View wallet details, balance, and transaction history</li>
                <li><strong>Smart Contract:</strong> Interact with the collaboration agreement contract</li>
                <li><strong>Whitepaper:</strong> Learn about DAPPR's architecture and economic model</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Step 3: Fund your wallet
        st.markdown("""
        <div class="stCard">
            <h4 style="color: #14F195; margin-top: 0;">Step 3: Fund Your Wallet</h4>
            <p>
                To interact with the smart contract, you'll need SOL for transaction fees and USDC for funding projects.
            </p>
            <p>
                For this demo, you can use Solana's devnet and request funds from a faucet:
            </p>
            <div style="background-color: #272727; padding: 12px; border-radius: 6px; font-family: 'Roboto Mono', monospace; font-size: 0.9rem;">
                <span style="color: #9945FF;">solana</span> airdrop 2 <span style="color: #14F195;">[YOUR_WALLET_ADDRESS]</span> --url https://api.devnet.solana.com
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown("### Smart Contract Basics")
        
        # Contract overview
        st.markdown("""
        <div class="stCard">
            <h4 style="color: #14F195; margin-top: 0;">DAPPR Collaboration Contract</h4>
            <p>
                The DAPPR platform is powered by a Solana smart contract written using Anchor framework. 
                This contract manages collaborative projects between academia and industry partners.
            </p>
            <p>
                <strong>Contract Address:</strong> <span class="wallet-address">Coll1ABbXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxX</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Main contract functions
        st.markdown("#### Core Functions")
        
        functions = [
            {
                "name": "initialize_project",
                "description": "Creates a new collaboration project with name, description, and IP terms",
                "parameters": "name (string), description (string), ip_terms (string)",
                "permissions": "Anyone can create a project"
            },
            {
                "name": "add_participant",
                "description": "Adds a participant to a project with a defined role and contribution percentage",
                "parameters": "name (string), role (string), contribution_percentage (u8), confidential_details (bytes)",
                "permissions": "Only project admin"
            },
            {
                "name": "add_milestone",
                "description": "Creates a milestone for the project with a deadline and payment amount",
                "parameters": "title (string), description (string), deadline (i64), payment_amount (u64), deliverables (string)",
                "permissions": "Only project admin"
            },
            {
                "name": "fund_milestone",
                "description": "Funds a milestone with USDC tokens",
                "parameters": "amount (u64)",
                "permissions": "Anyone (typically funders)"
            }
        ]
        
        for function in functions:
            st.markdown(f"""
            <div style="background-color: #1E1E1E; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 3px solid #14F195;">
                <div style="font-family: 'Roboto Mono', monospace; color: #14F195; margin-bottom: 8px;">
                    {function["name"]}({function["parameters"]})
                </div>
                <p style="margin-bottom: 5px; color: #FFFFFF;">{function["description"]}</p>
                <p style="font-size: 0.9rem; color: #AAA; margin-bottom: 0;">
                    <strong>Permissions:</strong> {function["permissions"]}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown("### Creating Projects")
        
        # Project creation guide
        st.markdown("""
        <div class="stCard">
            <h4 style="color: #14F195; margin-top: 0;">How to Create a New Project</h4>
            <p>
                Follow these steps to create a new collaboration project:
            </p>
            <ol>
                <li>Navigate to the "Smart Contract" page</li>
                <li>Expand the "Create New Project" form</li>
                <li>Enter project details:
                    <ul>
                        <li><strong>Project Name:</strong> A concise title for your collaboration</li>
                        <li><strong>Project Description:</strong> Details about the research objectives</li>
                        <li><strong>IP Terms:</strong> Intellectual property ownership and distribution terms</li>
                    </ul>
                </li>
                <li>Click "Create Project" to submit the transaction</li>
            </ol>
            <p>
                When creating a project, you will automatically become the project admin 
                with permissions to add participants and milestones.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Project structure visualization
        st.markdown("""
        <div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; margin-top: 15px;">
            <div style="color: #14F195; margin-bottom: 15px; font-weight: bold; text-align: center;">PROJECT STRUCTURE</div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
                <div style="width: 45%; background-color: #272727; padding: 15px; border-radius: 8px; border: 1px solid #333;">
                    <div style="color: #14F195; font-weight: bold; margin-bottom: 10px;">Project Account</div>
                    <div style="color: #AAA; font-size: 0.9rem; margin-bottom: 5px;">- name: string</div>
                    <div style="color: #AAA; font-size: 0.9rem; margin-bottom: 5px;">- description: string</div>
                    <div style="color: #AAA; font-size: 0.9rem; margin-bottom: 5px;">- ip_terms: string</div>
                    <div style="color: #AAA; font-size: 0.9rem; margin-bottom: 5px;">- admin: PublicKey</div>
                    <div style="color: #AAA; font-size: 0.9rem; margin-bottom: 5px;">- active: boolean</div>
                    <div style="color: #AAA; font-size: 0.9rem; margin-bottom: 5px;">- created_at: i64</div>
                    <div style="color: #AAA; font-size: 0.9rem; margin-bottom: 5px;">- participant_count: u8</div>
                    <div style="color: #AAA; font-size: 0.9rem; margin-bottom: 5px;">- milestone_count: u8</div>
                </div>
                <div style="width: 45%; background-color: #272727; padding: 15px; border-radius: 8px; border: 1px solid #333;">
                    <div style="color: #9945FF; font-weight: bold; margin-bottom: 10px;">Project PDAs</div>
                    <div style="color: #AAA; font-size: 0.9rem; margin-bottom: 5px;">- Participants (up to 10)</div>
                    <div style="color: #AAA; font-size: 0.9rem; margin-bottom: 5px;">- Milestones (up to 20)</div>
                    <div style="color: #AAA; font-size: 0.9rem; margin-bottom: 5px;">- Escrow Account (USDC)</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Example project transaction
        st.markdown("#### Example Project Creation Transaction")
        
        st.code("""
// Example of project creation transaction structure
{
  "transaction": {
    "message": {
      "accountKeys": [
        "AdminWallet111111111111111111111111111111",
        "ProjectAccount111111111111111111111111111",
        "TokenMint1111111111111111111111111111111",
        "EscrowAccount11111111111111111111111111111",
        "TokenProgram11111111111111111111111111111",
        "SystemProgram1111111111111111111111111111"
      ],
      "instructions": [
        {
          "programId": "Coll1ABbXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxX",
          "accounts": [
            { "name": "admin", "pubkey": "AdminWallet111111111111111111111111111111" },
            { "name": "project", "pubkey": "ProjectAccount111111111111111111111111111" },
            { "name": "usdcMint", "pubkey": "TokenMint1111111111111111111111111111111" },
            { "name": "escrowAccount", "pubkey": "EscrowAccount11111111111111111111111111111" },
            { "name": "tokenProgram", "pubkey": "TokenProgram11111111111111111111111111111" },
            { "name": "systemProgram", "pubkey": "SystemProgram1111111111111111111111111111" }
          ],
          "data": "initialize_project",
          "args": [
            "Quantum Research Collaboration",
            "A collaborative project to research quantum computing applications in bioinformatics",
            "All intellectual property developed through this collaboration will be jointly owned..."
          ]
        }
      ]
    }
  }
}
        """, language="javascript")
    
    with tabs[3]:
        st.markdown("### Managing Collaborations")
        
        # Adding participants guide
        st.markdown("""
        <div class="stCard">
            <h4 style="color: #14F195; margin-top: 0;">Adding Participants</h4>
            <p>
                As a project admin, you can add up to 10 participants to each collaboration project:
            </p>
            <ol>
                <li>Go to the "Smart Contract" page and select your project</li>
                <li>Navigate to the "Participants" tab</li>
                <li>Click "Add Participant" and fill in:
                    <ul>
                        <li><strong>Name:</strong> The participant's name</li>
                        <li><strong>Role:</strong> Their role in the project</li>
                        <li><strong>Contribution Percentage:</strong> Their share of the project (1-100%)</li>
                        <li><strong>Wallet Address:</strong> Their Solana wallet address</li>
                        <li><strong>Confidential Details:</strong> Optional encrypted information</li>
                    </ul>
                </li>
            </ol>
            <p>
                Note: The sum of all contribution percentages must not exceed 100%.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Creating milestones guide
        st.markdown("""
        <div class="stCard">
            <h4 style="color: #14F195; margin-top: 0;">Creating Milestones</h4>
            <p>
                Break down your project into manageable milestones with clear deliverables:
            </p>
            <ol>
                <li>Go to the "Smart Contract" page and select your project</li>
                <li>Navigate to the "Milestones" tab</li>
                <li>Click "Add Milestone" and fill in:
                    <ul>
                        <li><strong>Title:</strong> Brief name for the milestone</li>
                        <li><strong>Description:</strong> Detailed explanation of the work</li>
                        <li><strong>Deadline:</strong> Target completion date</li>
                        <li><strong>Payment Amount:</strong> Amount in USDC to be paid upon completion</li>
                        <li><strong>Deliverables:</strong> Specific outputs expected</li>
                    </ul>
                </li>
            </ol>
            <p>
                Each milestone can be funded separately, allowing for flexible project financing.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Milestone workflow diagram
        st.markdown("""
        <div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; margin-top: 15px; text-align: center;">
            <div style="color: #14F195; margin-bottom: 15px; font-weight: bold;">MILESTONE WORKFLOW</div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="width: 18%; background-color: #272727; padding: 10px; border-radius: 8px; border: 1px solid #333;">
                    <div style="color: #FFFFFF; font-weight: bold;">Created</div>
                </div>
                <div style="width: 5%; color: #666;">→</div>
                <div style="width: 18%; background-color: #272727; padding: 10px; border-radius: 8px; border: 1px solid #333;">
                    <div style="color: #FFFFFF; font-weight: bold;">Funded</div>
                </div>
                <div style="width: 5%; color: #666;">→</div>
                <div style="width: 18%; background-color: #272727; padding: 10px; border-radius: 8px; border: 1px solid #333;">
                    <div style="color: #FFFFFF; font-weight: bold;">Completed</div>
                </div>
                <div style="width: 5%; color: #666;">→</div>
                <div style="width: 18%; background-color: #272727; padding: 10px; border-radius: 8px; border: 1px solid #333;">
                    <div style="color: #FFFFFF; font-weight: bold;">Approved</div>
                </div>
                <div style="width: 5%; color: #666;">→</div>
                <div style="width: 18%; background-color: #272727; padding: 10px; border-radius: 8px; border: 1px solid #333;">
                    <div style="color: #FFFFFF; font-weight: bold;">Paid</div>
                </div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                <div style="width: 18%; text-align: center; font-size: 0.8rem; color: #AAA;">Admin</div>
                <div style="width: 5%;"></div>
                <div style="width: 18%; text-align: center; font-size: 0.8rem; color: #AAA;">Funder</div>
                <div style="width: 5%;"></div>
                <div style="width: 18%; text-align: center; font-size: 0.8rem; color: #AAA;">Participant</div>
                <div style="width: 5%;"></div>
                <div style="width: 18%; text-align: center; font-size: 0.8rem; color: #AAA;">Admin</div>
                <div style="width: 5%;"></div>
                <div style="width: 18%; text-align: center; font-size: 0.8rem; color: #AAA;">Contract</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[4]:
        st.markdown("### Funding & Payments")
        
        # Funding projects guide
        st.markdown("""
        <div class="stCard">
            <h4 style="color: #14F195; margin-top: 0;">Funding Projects</h4>
            <p>
                Projects are funded on a milestone-by-milestone basis through USDC:
            </p>
            <ol>
                <li>Navigate to the "Smart Contract" page and select a project</li>
                <li>Go to the "Milestones" tab and find the milestone you want to fund</li>
                <li>Click "Fund Milestone" and enter the amount (must match the milestone payment amount)</li>
                <li>Confirm the transaction in your wallet</li>
            </ol>
            <p>
                Funds are held in escrow until the milestone is completed and approved by the admin.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Payment distribution guide
        st.markdown("""
        <div class="stCard">
            <h4 style="color: #14F195; margin-top: 0;">Payment Distribution</h4>
            <p>
                When a milestone is completed and approved, payments are automatically distributed:
            </p>
            <ol>
                <li>Participants mark a milestone as completed with evidence</li>
                <li>Project admin reviews and approves the milestone</li>
                <li>Admin triggers the payment distribution</li>
                <li>Smart contract automatically distributes funds to each participant based on their contribution percentage</li>
            </ol>
            <p>
                The distribution is trustless and transparent, with all transactions recorded on the Solana blockchain.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Payment calculation example
        st.markdown("#### Example Payment Calculation")
        
        st.markdown("""
        <div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; margin-top: 15px;">
            <div style="color: #14F195; margin-bottom: 15px; font-weight: bold; text-align: center;">MILESTONE PAYMENT DISTRIBUTION</div>
            <div style="margin-bottom: 15px;">
                <div style="color: #FFFFFF; margin-bottom: 5px;"><strong>Milestone Payment:</strong> 1,000 USDC</div>
                <div style="height: 20px; background-color: #272727; border-radius: 10px; overflow: hidden; margin-top: 10px;">
                    <div style="width: 40%; height: 100%; background-color: #14F195; float: left;"></div>
                    <div style="width: 35%; height: 100%; background-color: #9945FF; float: left;"></div>
                    <div style="width: 25%; height: 100%; background-color: #00FFA3; float: left;"></div>
                </div>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <div style="width: 30%;">
                    <div style="color: #14F195; font-weight: bold; margin-bottom: 5px;">Dr. Alice Johnson</div>
                    <div style="color: #FFFFFF; margin-bottom: 5px;">40% contribution</div>
                    <div style="color: #AAA; font-size: 0.9rem;">Payment: 400 USDC</div>
                </div>
                <div style="width: 30%;">
                    <div style="color: #9945FF; font-weight: bold; margin-bottom: 5px;">Dr. Bob Smith</div>
                    <div style="color: #FFFFFF; margin-bottom: 5px;">35% contribution</div>
                    <div style="color: #AAA; font-size: 0.9rem;">Payment: 350 USDC</div>
                </div>
                <div style="width: 30%;">
                    <div style="color: #00FFA3; font-weight: bold; margin-bottom: 5px;">Dr. Carol Williams</div>
                    <div style="color: #FFFFFF; margin-bottom: 5px;">25% contribution</div>
                    <div style="color: #AAA; font-size: 0.9rem;">Payment: 250 USDC</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Advanced topics and resources
    st.markdown("### Additional Resources")
    
    with st.expander("Solana Developer Resources"):
        st.markdown("""
        - [Solana Documentation](https://docs.solana.com/)
        - [Anchor Framework](https://project-serum.github.io/anchor/getting-started/introduction.html)
        - [Solana Cookbook](https://solanacookbook.com/)
        - [Solana Playground](https://beta.solpg.io/)
        """)
    
    with st.expander("DAPPR Technical Documentation"):
        st.markdown("""
        - Full Smart Contract Specification
        - API Documentation
        - Integration Guides
        - Security Audits
        """)
        
    # Call-to-action
    st.markdown("""
    <div style="background: linear-gradient(90deg, rgba(20,241,149,0.2) 0%, rgba(153,69,255,0.2) 100%); 
                padding: 20px; border-radius: 10px; margin-top: 30px; text-align: center;">
        <h3 style="margin-top: 0; margin-bottom: 15px;">Ready to Start Collaborating?</h3>
        <p style="margin-bottom: 20px;">
            Create your first project on DAPPR and transform how you collaborate on research.
        </p>
        <div style="background-color: #9945FF; color: white; display: inline-block; padding: 10px 20px; border-radius: 5px; font-weight: bold;">
            Get Started
        </div>
    </div>
    """, unsafe_allow_html=True)