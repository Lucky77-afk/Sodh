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

## Deployment

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/Lucky77-afk/Sodh.git
   cd Sodh
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

### Deploy to Streamlit Community Cloud

1. Ensure your code is pushed to a GitHub repository
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/)
3. Click on "New app"
4. Select your repository, branch, and main file path (app.py)
5. Click "Deploy!"

### Environment Variables

If your application requires environment variables (like API keys), you'll need to set them in the Streamlit Community Cloud:

1. Go to your app in Streamlit Community Cloud
2. Click on "Advanced settings"
3. Add your environment variables in the "Secrets" section

## Configuration

The application uses a configuration file located at `.streamlit/config.toml`. You can modify this file to change the application's theme and behavior.

## License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

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

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

```
SODH - Solana Blockchain Explorer
Copyright (C) 2025 Your Name or Organization

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```