#!/bin/bash
set -e  # Exit on error

echo "Setting up the Solana Explorer application..."

# Install system dependencies
echo "Installing system dependencies..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y $(cat packages.txt)
else
    echo "Skipping apt-get installation (not on a Debian-based system)"
fi

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p .streamlit

# Install Python dependencies with specific versions
echo "Installing Python dependencies..."
python -m pip install --upgrade pip

# Install Solana dependencies in the correct order
echo "Installing Solana dependencies..."
pip install --no-cache-dir \
    base58==2.1.1 \
    construct==2.10.68 \
    construct-typing==0.5.6 \
    jsonalias==0.1.1 \
    solders==0.26.0 \
    solana==0.36.6

# Install the rest of the requirements
echo "Installing remaining dependencies..."
pip install --no-cache-dir -r requirements.txt

# Verify Solana installation
echo "Verifying Solana installation..."
python -c "from solders.pubkey import Pubkey; print('✅ Solana SDK imported successfully')" || echo "❌ Solana SDK import failed"

# Create a default config.toml if it doesn't exist
echo "Configuring Streamlit..."
cat > .streamlit/config.toml <<EOL
[server]
headless = true
port = 8502  # Using a different port to avoid conflicts
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
base = "dark"
primaryColor = "#14F195"
backgroundColor = "#131313"
secondaryBackgroundColor = "#1E1E1E"
textColor = "#FFFFFF"
font = "sans serif"
EOL

# Create a default secrets.toml if it doesn't exist
if [ ! -f .streamlit/secrets.toml ]; then
    echo "Creating default secrets file..."
    cat > .streamlit/secrets.toml <<EOL
# Database configuration
# DATABASE_URL = "postgresql://username:password@host:port/database"

# Solana RPC endpoint (you can use a public one or your own)
SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"

# Other secrets can be added here
# API_KEY = "your_api_key_here"
EOL
fi

echo ""
echo "==============================================="
echo "✅ Setup complete!"
echo "To start the application locally, run:"
echo "  streamlit run app.py --server.port=8502"
echo ""
echo "If port 8502 is in use, you can try a different port:"
echo "  streamlit run app.py --server.port=8503"
echo ""
echo "Make sure to configure your .streamlit/secrets.toml"
echo "with the appropriate database and API settings."
echo "==============================================="
echo ""
