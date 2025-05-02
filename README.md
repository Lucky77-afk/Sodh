# SODH - Solana Blockchain Explorer

SODH is a comprehensive Solana blockchain explorer built with Streamlit. It offers a user-friendly interface for interacting with the Solana blockchain, viewing transactions, and working with smart contracts.

## Features

- **Dashboard**: View real-time Solana network metrics and statistics
- **Transactions**: Explore and analyze blockchain transactions
- **Account Explorer**: Check wallet balances, transactions, and stake information
- **Smart Contract**: Interact with the DAPPR smart contract for research collaborations
- **Multiple Token Support**: Handle both SOL and USDT transactions
- **Whitepaper**: Access the DAPPR whitepaper directly within the application
- **Tutorial**: Learn how to use Solana and the DAPPR platform

## Technology Stack

- **Frontend**: Streamlit
- **Blockchain**: Solana
- **Database**: PostgreSQL
- **Data Visualization**: Plotly
- **Token Integration**: SOL and USDT (Tether on Solana)

## Environment Setup

### Prerequisites

- Python 3.8+
- PostgreSQL
- Solana CLI tools (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/sodh-explorer.git
cd sodh-explorer
```

2. Install the dependencies:
```bash
pip install -r requirements.txt
```

3. Set up the PostgreSQL database:
```bash
# Make sure your PostgreSQL server is running
# The application will automatically create necessary tables on startup
```

4. Run the application:
```bash
streamlit run app.py
```

## Usage

Once the application is running, you can:

1. Navigate through different sections using the sidebar
2. Connect your Solana wallet to view account information
3. Explore Solana transactions
4. View token information for SOL and USDT
5. Interact with the DAPPR smart contract for research collaborations

## About DAPPR

DAPPR (Decentralized Autonomous Platform for Propagation of Research) leverages Solana blockchain to revolutionize academia-industry collaboration. It creates a transparent ecosystem for research funding, intellectual property management, and value distribution.

## License

[MIT License](LICENSE)