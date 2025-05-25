# Sodh - Solana Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sodh.streamlit.app/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Streamlit-based dashboard for interacting with the Solana blockchain, providing real-time analytics, transaction monitoring, and smart contract interaction.

## ✨ Features

- 📊 Real-time Solana account information and analytics
- 🔍 Transaction monitoring and exploration
- 🤖 Smart contract interaction and deployment
- 📚 Whitepapers and tutorials
- 🚀 Built with modern Python and Streamlit
- 🐳 Docker support for easy deployment
- 🔄 CI/CD ready with GitHub Actions

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) (recommended) or pip
- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/) (optional, for containerized deployment)

### Local Development

#### Using setup script (recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Lucky77-afk/Sodh.git
   cd Sodh
   ```

2. **Run the setup script**:
   - **Windows**:
     ```bash
     .\setup.bat
     ```
   - **macOS/Linux**:
     ```bash
     chmod +x setup.sh
     ./setup.sh
     ```

3. **Start the application**:
   ```bash
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
