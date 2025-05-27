#!/bin/bash

# Exit on error
set -e

echo "🚀 Setting up Sodh - Solana Dashboard Helper"
echo "===================================="

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p .streamlit

# Create a simple app.py if it doesn't exist
if [ ! -f app.py ]; then
    echo "📄 Creating default app.py..."
    cat > app.py << 'EOL'
import streamlit as st

def main():
    st.set_page_config(
        page_title="Sodh - Solana Dashboard Helper",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 Sodh - Solana Dashboard Helper")
    st.write("Welcome to Sodh! Your Solana dashboard is up and running.")

if __name__ == "__main__":
    main()
EOL
fi

# Create a simple requirements.txt if it doesn't exist
if [ ! -f requirements.txt ]; then
    echo "📄 Creating requirements.txt..."
    cat > requirements.txt << 'EOL'
streamlit>=1.45.1
solana>=0.36.6
solders>=0.26.0
base58>=2.1.1
python-dotenv>=1.1.0
requests>=2.32.3
EOL
fi

# Create a simple .streamlit/config.toml if it doesn't exist
if [ ! -f .streamlit/config.toml ]; then
    echo "📄 Creating .streamlit/config.toml..."
    mkdir -p .streamlit
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
textColor = "#FFFFFF"
font = "sans serif"
EOL
fi

echo "✅ Setup complete!"
echo "You can now run the app with: streamlit run app.py"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ "$PYTHON_VERSION" < "3.8" ]]; then
    echo "❌ Python 3.8 or higher is required. Found Python $PYTHON_VERSION"
    exit 1
fi

echo "✅ Found Python $PYTHON_VERSION"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

echo "✅ Found pip $(pip3 --version | cut -d ' ' -f 2)"

# Create a virtual environment
echo -e "\n🔧 Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Using existing virtual environment"
fi

# Activate virtual environment
if [ "$OS" = "Windows_NT" ]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo -e "\n🔄 Upgrading pip..."
pip install --upgrade pip

# Install Poetry
if ! command -v poetry &> /dev/null; then
    echo -e "\n📦 Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
    echo "✅ Poetry installed"
else
    echo -e "\n✅ Using existing Poetry $(poetry --version | cut -d ' ' -f 3)"
fi

# Install project dependencies
echo -e "\n📦 Installing project dependencies..."
poetry install --no-interaction --no-ansi

echo -e "\n🔧 Setting up pre-commit hooks..."
poetry run pre-commit install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "\n📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ .env file created. Please update it with your configuration."
else
    echo -e "\n✅ .env file already exists"
fi

echo -e "\n✨ Setup complete! ✨"
echo -e "\nTo activate the virtual environment, run:"
if [ "$OS" = "Windows_NT" ]; then
    echo "  .\\venv\\Scripts\\activate"
else
    echo "  source venv/bin/activate"
fi
echo -e "\nTo run the application, use:"
echo "  poetry run streamlit run sodh/app.py"
echo -e "\nOr with Docker:"
echo "  docker-compose up --build"
