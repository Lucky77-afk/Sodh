#!/bin/bash
set -e  # Exit on error

echo "Setting up the Solana Explorer application..."

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p .streamlit

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir

# Install Solana dependencies separately to ensure they're installed correctly
echo "Installing Solana dependencies..."
pip install solana==0.36.6 solders==0.26.0 construct==2.10.68 construct-typing==0.5.6 base58==2.1.1

# Install Solana CLI tools (if needed)
# echo "Installing Solana CLI tools..."
# sh -c "$(curl -sSfL https://release.solana.com/v1.16.18/install)"
# export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"

# Create a default config.toml if it doesn't exist
if [ ! -f .streamlit/config.toml ]; then
    echo "Creating default Streamlit configuration..."
    cat > .streamlit/config.toml <<EOL
[server]
headless = true
port = 8501
enableCORS = false

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
fi

# Create a default secrets.toml if it doesn't exist
if [ ! -f .streamlit/secrets.toml ]; then
    echo "Creating default secrets file..."
    cat > .streamlit/secrets.toml <<EOL
# Database configuration
# DATABASE_URL = "postgresql://username:password@host:port/database"

# Solana RPC endpoint (you can use a public one or your own)
# SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"

# Other secrets can be added here
# API_KEY = "your_api_key_here"
EOL
fi

echo ""
echo "==============================================="
echo "Setup complete!"
echo "To start the application locally, run:"
echo "  streamlit run app.py"
echo ""
echo "Make sure to configure your .streamlit/secrets.toml"
echo "with the appropriate database and API settings."
echo "==============================================="
echo ""
