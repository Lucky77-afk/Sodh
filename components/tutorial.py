import streamlit as st

def render_tutorial():
    """Renders the tutorial section with Solana smart contract guidance"""
    st.markdown('<h2>DAPPR Platform Tutorial</h2>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    Welcome to the DAPPR platform tutorial. This guide will help you understand how to use the 
    collaboration smart contract and navigate the Solana blockchain ecosystem.
    """)
    
    # Tutorial sections
    tabs = st.tabs(["Getting Started", "Smart Contract Basics", "Creating Projects", "Managing Collaborations", "Funding & Payments"])
    
    with tabs[0]:
        st.markdown("### Getting Started with DAPPR")
        
        # Step 1: Connect wallet
        st.markdown("""
        <div class="stCard">
            <h4 style="color: #14F195; margin-top: 0;">Step 1: Connect Your Wallet</h4>
            <p>
                To interact with the DAPPR platform, you'll need a Solana wallet. Popular options include:
            </p>
            <ul>
                <li>Phantom Wallet</li>
                <li>Solflare</li>
                <li>Sollet</li>
            </ul>
            <p>
                Once you have a wallet, click on "Connect" in the sidebar and enter your wallet address.
                For production use, the wallet connection would happen automatically through a web3 provider.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Step 2: Explore the platform
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