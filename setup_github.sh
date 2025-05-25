#!/bin/bash

# Exit on error
set -e

echo "===== Setting up GitHub Repository for Sodh Solana Explorer ====="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Git is not installed. Please install git first."
    exit 1
fi

# Initialize git repository
echo "Initializing git repository..."
if [ ! -d ".git" ]; then
    git init
else
    echo "Git repository already initialized."
fi

# Create .gitignore file
echo "Creating .gitignore file..."
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# Streamlit
.streamlit/secrets.toml

# Mobile App
mobile-app/node_modules/
mobile-app/.expo/
mobile-app/dist/
mobile-app/npm-debug.*
mobile-app/*.jks
mobile-app/*.p8
mobile-app/*.p12
mobile-app/*.key
mobile-app/*.mobileprovision
mobile-app/*.orig.*
mobile-app/web-build/

# Local configuration
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.idea/
.vscode/
*.swp
*.swo

# Database
*.db
*.sqlite
*.sqlite3

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
EOF

# Create README.md file
echo "Creating README.md file..."
cat > README.md << EOF
# Sodh - Solana Blockchain Explorer

A comprehensive Solana blockchain explorer platform built with Streamlit, focusing on user-friendly transaction exploration and custom blockchain interaction tools.

![Sodh Explorer](assets/logo.jpeg)

## Features

- Real-time Solana blockchain data exploration
- Transaction history and details
- Wallet connection and account management
- Smart contract interaction
- Project collaboration through DAPPR smart contract
- SOL and USDT token support
- Dark-themed UI with Solana design aesthetics

## Repository Structure

The project contains:

- **Streamlit Web App**: The main application, featuring a complete blockchain explorer
- **Mobile App**: A React Native application for mobile access to the platform
- **Web Migration**: React-based web version (in progress)
- **Documentation**: Including whitepaper and development guides

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 16+ (for mobile app)
- PostgreSQL database

### Installation

1. Clone the repository:
   \`\`\`
   git clone https://github.com/yourusername/sodh-explorer.git
   cd sodh-explorer
   \`\`\`

2. Install Python dependencies:
   \`\`\`
   pip install -r requirements.txt
   \`\`\`

3. Run the Streamlit app:
   \`\`\`
   streamlit run app.py
   \`\`\`

### Mobile App

For mobile development:

1. Navigate to the mobile app directory:
   \`\`\`
   cd mobile-app
   \`\`\`

2. Install dependencies:
   \`\`\`
   npm install
   \`\`\`

3. Start the development server:
   \`\`\`
   npm start
   \`\`\`

4. Build for Android:
   \`\`\`
   chmod +x build-android.sh
   ./build-android.sh
   \`\`\`

## Deployment

### Web App

The Streamlit app can be deployed on any platform that supports Python applications:

- Streamlit Cloud
- Heroku
- Replit
- AWS, Google Cloud, Azure

### Mobile App

The mobile app can be deployed to:

- Google Play Store (Android)
- App Store (iOS)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Solana Foundation for blockchain infrastructure
- Streamlit for the web framework
- React Native for mobile development
EOF

# Create initial commit
echo "Creating initial commit..."
git add .
git commit -m "Initial commit for Sodh Solana Explorer"

echo "===== GitHub Repository Setup Complete ====="
echo ""
echo "Next steps:"
echo "1. Create a GitHub repository at https://github.com/new"
echo "2. Run the following commands to push your code:"
echo "   git remote add origin https://github.com/yourusername/sodh-explorer.git"
echo "   git push -u origin main"
echo ""
echo "Replace 'yourusername' with your actual GitHub username and 'sodh-explorer' with your repository name."