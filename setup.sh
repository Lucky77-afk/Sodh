#!/bin/bash
# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p .streamlit

# Create a default config.toml if it doesn't exist
if [ ! -f .streamlit/config.toml ]; then
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

echo "Setup complete. Run 'streamlit run app.py' to start the application."
