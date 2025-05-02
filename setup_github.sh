#!/bin/bash

# Initialize git repository if not already initialized
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
fi

# Add all files to git
echo "Adding files to git..."
git add .

# Commit the changes
echo "Committing changes..."
git commit -m "Initial commit of Sodh - Solana Blockchain Explorer with USDT support"

# Setup GitHub origin - replace with your GitHub URL
echo "Please enter your GitHub repository URL (e.g. https://github.com/username/repo.git):"
read github_url

if [ -n "$github_url" ]; then
    echo "Setting up remote origin..."
    git remote add origin $github_url
    
    echo "Pushing to GitHub..."
    git push -u origin master || git push -u origin main
    
    echo "Done! Your code has been pushed to GitHub."
else
    echo "No GitHub URL provided. You can manually set it later with:"
    echo "git remote add origin YOUR_GITHUB_URL"
    echo "git push -u origin master"
fi