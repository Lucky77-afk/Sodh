# Sodh - Solana Dashboard

A Streamlit-based dashboard for interacting with the Solana blockchain.

## Features

- View Solana account information
- Monitor transactions
- Interact with smart contracts
- Access whitepapers and tutorials

## Prerequisites

- Python 3.10+
- pip (Python package manager)

## Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sodh.git
   cd sodh
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`
   - Add your Helius API key and other secrets

5. Run the application locally:
   ```bash
   streamlit run run.py
   ```

## Deployment

### Streamlit Cloud

1. Fork this repository
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Click "New app" and select your forked repository
4. Set the main file path to `run.py`
5. Add your secrets in the advanced settings
6. Click "Deploy!"

### Other Platforms

For other platforms (Heroku, etc.), make sure to:

1. Set the following environment variables:
   - `HELIUS_API_KEY`: Your Helius API key
   - `PORT`: The port to run the app on (usually set by the platform)

2. The `Procfile` is already configured for most platforms

## Project Structure

```
sodh/
├── .streamlit/
│   ├── config.toml       # Streamlit configuration
│   └── secrets.toml      # Sensitive data (not in version control)
├── sodh/                # Main package
│   ├── components/       # UI components
│   ├── utils/            # Utility functions
│   ├── app.py            # Main application
│   └── __init__.py       # Package initialization
├── .gitignore
├── Procfile             # For Heroku/other platforms
├── README.md            # This file
├── requirements.txt      # Python dependencies
├── runtime.txt          # Python version
└── setup.py             # Package configuration
```

## License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
