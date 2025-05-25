# 🚀 Sodh - Solana Blockchain Explorer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sodh.streamlit.app/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A modern, user-friendly Solana blockchain explorer built with Streamlit, providing real-time analytics, transaction monitoring, and wallet management.

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- [Git](https://git-scm.com/)

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Lucky77-afk/Sodh.git
   cd Sodh
   ```

2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run main/app.py
   ```

5. **Access the app** at http://localhost:8501

## ☁️ Deployment

### Streamlit Cloud (Recommended)

1. Push your code to a GitHub repository
2. Sign in to [Streamlit Cloud](https://share.streamlit.io/)
3. Click "New app" and select your repository
4. Set the main file path to `main/app.py`
5. Click "Deploy!"

## 🏗 Project Structure

```
Sodh/
├── .streamlit/               # Streamlit configuration
│   ├── config.toml           # App configuration
│   └── secrets.toml          # Environment variables (not versioned)
├── main/                     # Main application package
│   ├── __init__.py           # Package initialization
│   └── app.py                # Main Streamlit application
├── requirements.txt          # Python dependencies
└── runtime.txt              # Python version for deployment
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the AGPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## ✨ Features

- 🚀 **Real-time Blockchain Data**: Monitor Solana network activity in real-time
- 🔍 **Transaction Explorer**: Search and analyze transactions on the Solana blockchain
- 💰 **Wallet Management**: View balances, tokens, and transaction history
- 📊 **Analytics Dashboard**: Visualize network statistics and trends
- 🌐 **Web3 Integration**: Connect with popular Solana wallets
- 🔒 **Secure**: Built with security best practices in mind
- ☁️ **Cloud-Ready**: Optimized for deployment on Streamlit Cloud

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- [Git](https://git-scm.com/)
- [Poetry](https://python-poetry.org/) (recommended) or pip

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Lucky77-afk/Sodh.git
   cd Sodh
   ```

2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python run.py
   ```
   
   Or for development with auto-reload:
   ```bash
   streamlit run app.py
   ```

5. **Access the app** at http://localhost:8501

## ☁️ Deployment

### Streamlit Cloud (Recommended)

1. Push your code to a GitHub repository
2. Sign in to [Streamlit Cloud](https://share.streamlit.io/)
3. Click "New app" and select your repository
4. Set the main file path to `app.py`
5. Add any required environment variables in the settings
6. Click "Deploy!"

### Health Check

To verify the app is running, access the health check endpoint:
```bash
curl "https://your-app-url.streamlit.app/?health_check=true"
```

## 🏗 Project Structure

```
Sodh/
├── .streamlit/               # Streamlit configuration
│   ├── config.toml           # App configuration
│   └── secrets.example.toml  # Example secrets (copy to secrets.toml)
├── assets/                   # Static assets (images, etc.)
├── app.py                    # Main Streamlit application
├── run.py                    # Entry point with process management
├── requirements.txt          # Python dependencies
└── Procfile                  # Process configuration for deployment
```

## 🔧 Configuration

Copy the example secrets file and update with your configuration:

```bash
cp .streamlit/secrets.example.toml .streamlit/secrets.toml
# Edit the secrets.toml file with your configuration
```

## 🧪 Testing

Run the test suite:

```bash
python test_app.py
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the AGPL-3.0 License - see the [LICENSE](LICENSE) file for details.
   poetry run streamlit run sodh/app.py
   ```
   
   Or with the run script:
   ```bash
   python run.py
   ```

#### Manual Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Lucky77-afk/Sodh.git
   cd Sodh
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Update the variables in `.env` with your configuration
   - For Streamlit-specific settings, copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`

5. **Run the application**:
   ```bash
   streamlit run sodh/app.py
   ```

## 🐳 Docker Deployment

1. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

2. **Access the application**:
   - Open your browser and go to `http://localhost:8501`

## ☁️ Cloud Deployment

### Streamlit Cloud

1. **Fork this repository**
2. **Go to [Streamlit Cloud](https://share.streamlit.io/)**
3. **Click "New app"** and select your forked repository
4. **Configure the app**:
   - Set the branch to `main`
   - Set the main file path to `sodh/app.py`
   - Add your environment variables in the advanced settings
5. **Click Deploy!**

### Other Platforms

This application can be deployed to any platform that supports Python applications or Docker containers, including:

- [Heroku](https://www.heroku.com/)
- [Railway](https://railway.app/)
- [Render](https://render.com/)
- [Google Cloud Run](https://cloud.google.com/run)
- [AWS App Runner](https://aws.amazon.com/apprunner/)
- [Azure Container Apps](https://azure.microsoft.com/en-us/products/container-apps/)

## 🛠 Development

### Project Structure

```
sodh/
├── components/         # Streamlit UI components
├── utils/              # Utility functions and helpers
├── app.py              # Main application entry point
├── run.py              # Application runner
└── __init__.py         # Package definition
```

### Code Style

This project uses:
- [Black](https://github.com/psf/black) for code formatting
- [isort](https://pycqa.github.io/isort/) for import sorting
- [Flake8](https://flake8.pycqa.org/) for linting
- [Mypy](http://mypy-lang.org/) for static type checking

Run the following commands to ensure code quality:

```bash
# Format code
poetry run black .

# Sort imports
poetry run isort .

# Run linter
poetry run flake8

# Run type checking
poetry run mypy .
```

### Testing

Run tests with:

```bash
poetry run pytest
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to contribute to this project.

## 📄 License

This project is licensed under the AGPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support, please open an issue in the [GitHub repository](https://github.com/Lucky77-afk/Sodh/issues).

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Solana](https://solana.com/) for the blockchain platform
- [Poetry](https://python-poetry.org/) for dependency management
- All the open-source libraries used in this project
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
