#!/bin/bash

# Create .streamlit directory if it doesn't exist
mkdir -p .streamlit

# Create config.toml with necessary settings
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
enableStaticServing = false

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

echo "✅ Streamlit configuration complete"
