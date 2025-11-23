#!/bin/bash

# Setup GitHub Pages Repository
# Usage: ./scripts/setup-github.sh [username]

set -e

USERNAME=${1:-"prithaguha"}
REPO_NAME="${USERNAME}.github.io"

echo "📦 Setting up GitHub Pages repository..."
echo "Username: $USERNAME"
echo "Repository: $REPO_NAME"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "🔧 Initializing git repository..."
    git init
    git branch -M main
fi

# Check if remote exists
if git remote get-url origin &>/dev/null; then
    echo "⚠️  Remote 'origin' already exists:"
    git remote get-url origin
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPO_REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "🔗 Adding GitHub remote..."
    git remote add origin "https://github.com/${USERNAME}/${REPO_NAME}.git"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << EOF
# Environment files
backend/.env
*.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF
fi

# Add and commit files
echo "📝 Staging files..."
git add index.html sop.js style.css README.md DEPLOYMENT.md .gitignore

# Check if PDFs exist
if [ -f "autobiography.pdf" ]; then
    git add autobiography.pdf
    echo "✅ Found autobiography.pdf"
else
    echo "⚠️  autobiography.pdf not found - add it later"
fi

if [ -f "resume.pdf" ]; then
    git add resume.pdf
    echo "✅ Found resume.pdf"
else
    echo "⚠️  resume.pdf not found - add it later"
fi

if [ -f "cover_letter.pdf" ]; then
    git add cover_letter.pdf
    echo "✅ Found cover_letter.pdf"
else
    echo "⚠️  cover_letter.pdf not found - add it later"
fi

# Commit
if git diff --staged --quiet; then
    echo "ℹ️  No changes to commit"
else
    echo "💾 Committing files..."
    git commit -m "Initial commit: Career Agent website"
fi

# Instructions
echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Create the repository on GitHub: https://github.com/new"
echo "   Repository name: $REPO_NAME"
echo "   Make it public"
echo ""
echo "2. Push to GitHub:"
echo "   git push -u origin main"
echo ""
echo "3. Enable GitHub Pages:"
echo "   - Go to repository Settings > Pages"
echo "   - Source: Deploy from branch 'main'"
echo "   - Your site will be at: https://${USERNAME}.github.io"
echo ""
echo "4. Don't forget to:"
echo "   - Add your PDF files (autobiography.pdf, resume.pdf, cover_letter.pdf)"
echo "   - Update sop.js with your Cloud Run API URL"
echo "   - Commit and push the changes"

