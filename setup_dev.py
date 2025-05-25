#!/usr/bin/env python3
"""
Development setup script for Sodh.
This script helps set up the development environment.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f" {text}".upper())
    print("=" * 80)

def run_command(command, cwd=None):
    """Run a shell command."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            check=True,
            text=True,
            capture_output=True
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}", file=sys.stderr)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        return False

def create_virtualenv():
    """Create a Python virtual environment if it doesn't exist."""
    venv_dir = "venv"
    if not os.path.exists(venv_dir):
        print_header("Creating Python virtual environment")
        if not run_command(f"python -m venv {venv_dir}"):
            sys.exit(1)
    return venv_dir

def install_dependencies(venv_dir):
    """Install Python dependencies."""
    print_header("Installing Python dependencies")
    pip = os.path.join(venv_dir, "Scripts", "pip") if os.name == 'nt' else os.path.join(venv_dir, "bin", "pip")
    
    # Upgrade pip and install requirements
    if not run_command(f"{pip} install --upgrade pip"):
        sys.exit(1)
    if not run_command(f"{pip} install -r requirements.txt"):
        sys.exit(1)

def setup_environment():
    """Set up environment variables and configuration files."""
    print_header("Setting up environment")
    
    # Create .streamlit directory if it doesn't exist
    os.makedirs(".streamlit", exist_ok=True)
    
    # Copy secrets.toml.example to secrets.toml if it doesn't exist
    secrets_example = ".streamlit/secrets.toml.example"
    secrets_file = ".streamlit/secrets.toml"
    
    if os.path.exists(secrets_example) and not os.path.exists(secrets_file):
        print(f"Creating {secrets_file} from example")
        shutil.copy2(secrets_example, secrets_file)
    
    # Copy .env.example to .env if it doesn't exist
    if os.path.exists(".env.example") and not os.path.exists(".env"):
        print("Creating .env from .env.example")
        shutil.copy2(".env.example", ".env")

def check_requirements():
    """Check if all required tools are installed."""
    print_header("Checking system requirements")
    required_tools = [
        ("Python", "python --version"),
        ("Pip", "pip --version"),
        ("Git", "git --version")
    ]
    
    all_ok = True
    for name, cmd in required_tools:
        try:
            version = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True).strip()
            print(f"✓ {name}: {version}")
        except subprocess.CalledProcessError:
            print(f"✗ {name} is not installed")
            all_ok = False
    
    if not all_ok:
        print("\nSome required tools are missing. Please install them and try again.")
        sys.exit(1)

def main():
    """Main setup function."""
    print_header("Setting up Sodh development environment")
    
    # Check system requirements
    check_requirements()
    
    # Create virtual environment
    venv_dir = create_virtualenv()
    
    # Install dependencies
    install_dependencies(venv_dir)
    
    # Set up environment
    setup_environment()
    
    print_header("Setup complete!")
    print("\nTo activate the virtual environment, run:")
    if os.name == 'nt':  # Windows
        print("  .\\venv\\Scripts\\activate")
    else:  # Unix/Linux/Mac
        print("  source venv/bin/activate")
    
    print("\nTo run the application:")
    print("  streamlit run run.py")

if __name__ == "__main__":
    main()
