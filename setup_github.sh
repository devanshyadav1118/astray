#!/bin/bash

# 🌟 Astrology AI - GitHub Setup Script
# This script helps you push your astrology AI project to GitHub

echo "🌟 Setting up Astrology AI project on GitHub..."
echo "================================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if git is initialized
if [ ! -d ".git" ]; then
    print_error "Git repository not initialized. Run 'git init' first."
    exit 1
fi

print_status "Current git status:"
git status --short

echo ""
print_status "Repository is ready for GitHub upload!"
echo ""

# Prompt for GitHub repository URL
echo "📋 To complete GitHub setup:"
echo ""
echo "1. Go to https://github.com/new"
echo "2. Create a new repository named 'astrology-ai'"
echo "3. Make it public (recommended for open source)"
echo "4. Don't initialize with README (we already have one)"
echo "5. Copy the repository URL"
echo ""

read -p "Enter your GitHub repository URL (e.g., https://github.com/yourusername/astrology-ai.git): " repo_url

if [ -z "$repo_url" ]; then
    print_error "Repository URL is required."
    exit 1
fi

# Add remote origin
print_status "Adding GitHub remote..."
git remote add origin "$repo_url"

if [ $? -eq 0 ]; then
    print_success "Remote origin added successfully"
else
    print_warning "Remote might already exist, continuing..."
fi

# Push to GitHub
print_status "Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    print_success "Successfully pushed to GitHub!"
    echo ""
    echo "🎉 Your Astrology AI project is now on GitHub!"
    echo ""
    echo "📊 Project Statistics:"
    echo "   - 1,287 classical astrological rules"
    echo "   - 6 authoritative source texts"
    echo "   - Complete CLI interface"
    echo "   - AI enhancement roadmap"
    echo "   - Comprehensive documentation"
    echo ""
    echo "🔗 Repository URL: $repo_url"
    echo ""
    echo "📋 Next Steps:"
    echo "   1. Visit your repository on GitHub"
    echo "   2. Set up GitHub Actions (already configured)"
    echo "   3. Add repository description and topics"
    echo "   4. Create issues for Phase 2 development"
    echo "   5. Start inviting collaborators"
    echo ""
    echo "🚀 Recommended GitHub repository settings:"
    echo "   - Description: 'AI-powered Vedic astrology interpretation using classical texts'"
    echo "   - Topics: astrology, ai, vedic, python, nlp, classical-texts"
    echo "   - License: MIT (already included)"
    echo "   - Enable Issues and Discussions"
    echo ""
else
    print_error "Failed to push to GitHub. Please check:"
    echo "   - Repository URL is correct"
    echo "   - You have push access to the repository"
    echo "   - Your GitHub authentication is set up"
    echo ""
    echo "Manual push command:"
    echo "   git push -u origin main"
fi

echo ""
echo "✨ Happy coding! May your interpretations be accurate and your code bug-free!" 