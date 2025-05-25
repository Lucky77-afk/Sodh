# Deployment Guide for Sodh - Solana Blockchain Explorer

This guide provides instructions for deploying the Sodh application on Streamlit Cloud.

## Prerequisites

- A GitHub account
- A Streamlit Cloud account (https://streamlit.io/cloud)
- Your repository pushed to GitHub

## Deployment Steps

1. **Prepare your repository**
   - Ensure your code is pushed to a GitHub repository
   - Verify that all required files are present:
     - `app.py` - Main Streamlit application
     - `run.py` - Entry point script
     - `requirements.txt` - Python dependencies
     - `Procfile` - Process configuration
     - `.streamlit/config.toml` - Streamlit configuration

2. **Set up Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Click "New app"
   - Select your repository and branch
   - Set the following configuration:
     - Main file path: `app.py`
     - Python version: 3.9 (or your preferred version)

3. **Configure Environment Variables**
   - In the Streamlit Cloud settings, go to "Advanced settings"
   - Add any required environment variables from `.streamlit/secrets.example.toml`
   - Set `HEALTH_CHECK=false` for normal operation

4. **Deploy**
   - Click "Deploy"
   - Wait for the build to complete
   - Your app will be available at `https://share.streamlit.io/your-username/your-repo`

## Health Check

To verify the app is running:

```bash
curl "https://your-app-url.streamlit.app/?health_check=true"
```

## Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a local secrets file:
   ```bash
   cp .streamlit/secrets.example.toml .streamlit/secrets.toml
   # Edit the secrets.toml file with your local configuration
   ```

4. Run the app locally:
   ```bash
   streamlit run app.py
   ```

## Troubleshooting

- **App not starting**: Check the logs in Streamlit Cloud for errors
- **Missing dependencies**: Ensure all required packages are in `requirements.txt`
- **Environment variables**: Verify all required environment variables are set
- **Port conflicts**: Ensure port 8501 is available if running locally

## Security Notes

- Never commit sensitive information to version control
- Use environment variables for all secrets
- Keep your dependencies up to date
- Regularly review and rotate API keys and credentials
