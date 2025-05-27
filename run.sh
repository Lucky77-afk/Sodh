#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting Sodh - Solana Dashboard Helper..."

# Create .streamlit directory if it doesn't exist
mkdir -p .streamlit

# Create a simple config.toml if it doesn't exist
if [ ! -f .streamlit/config.toml ]; then
    cat > .streamlit/config.toml << 'EOL'
[server]
port = 8501
address = "0.0.0.0"
headless = true
baseUrlPath = "/"
enableCORS = false
enableXsrfProtection = false
maxUploadSize = 200
enableWebsocketCompression = true
fileWatcherType = "none"
runOnSave = false

[browser]
gatherUsageStats = false
serverAddress = "0.0.0.0"
serverPort = 8501

[theme]
base = "dark"
primaryColor = "#14F195"
backgroundColor = "#131313"
secondaryBackgroundColor = "#1E1E1E"
EOL
fi

# Run Streamlit with the app
streamlit run app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --server.fileWatcherType=none \
    --server.runOnSave=false \
    --browser.gatherUsageStats=false
