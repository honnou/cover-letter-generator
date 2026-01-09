#!/bin/bash

echo "=============================================="
echo "  Cover Letter Generator - GitHub Setup"
echo "=============================================="
echo ""
echo "This script will help you push to GitHub."
echo ""

# Get GitHub username
read -p "Enter your GitHub username: " github_username

# Set repository name
repo_name="cover-letter-generator"

echo ""
echo "Repository will be created at:"
echo "https://github.com/${github_username}/${repo_name}"
echo ""

# Add remote
echo "Adding GitHub remote..."
git remote add origin "https://github.com/${github_username}/${repo_name}.git"

# Rename branch to main
echo "Renaming branch to main..."
git branch -M main

echo ""
echo "=============================================="
echo "  Next Steps:"
echo "=============================================="
echo ""
echo "1. Go to GitHub and create a new repository:"
echo "   https://github.com/new"
echo ""
echo "2. Repository name: ${repo_name}"
echo "   Description: AI-powered cover letter generator"
echo "   Keep it PUBLIC or PRIVATE (your choice)"
echo "   DON'T initialize with README, .gitignore, or license"
echo ""
echo "3. After creating the repository, run:"
echo "   git push -u origin main"
echo ""
echo "4. Then deploy to Vercel:"
echo "   npx vercel"
echo ""
echo "=============================================="
