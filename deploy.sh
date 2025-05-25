#!/bin/bash

# Exit on error
set -e

echo "🚀 Deploying Sodh to Streamlit Cloud"
echo "===================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

echo "✅ Git is installed"

# Check if the current directory is a git repository
if [ ! -d ".git" ]; then
    echo "❌ This is not a Git repository. Please initialize Git first."
    exit 1
fi

echo "✅ Git repository found"

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  There are uncommitted changes. Please commit or stash them first."
    exit 1
fi

echo "✅ No uncommitted changes"

# Get the current branch name
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Push to GitHub
echo -e "\n🔄 Pushing to GitHub..."
git push origin $CURRENT_BRANCH

echo -e "\n✅ Deployment started!"
echo "Your app should be available shortly at: https://share.streamlit.io/your-username/sodh"
echo "\nYou can monitor the deployment progress in your Streamlit Cloud dashboard."
