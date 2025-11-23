# GitHub Pages Setup - Quick Guide

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `prithaguha.github.io`
   - If that's taken, try: `prithaguha-1.github.io`, `prithaguha-2.github.io`, etc.
3. Make it **Public** (required for free GitHub Pages)
4. **Don't** initialize with README (we have files already)
5. Click "Create repository"

## Step 2: Push Your Code

```bash
cd /Users/pritha/playground/career-agent

# Add all files
git add .

# Commit
git commit -m "Initial commit: Career Agent website"

# Add remote (replace with your actual username if different)
git remote add origin https://github.com/prithaguha/prithaguha.github.io.git

# Push to GitHub
git push -u origin main
```

## Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** (top right)
3. Scroll down to **Pages** (left sidebar)
4. Under **Source**, select:
   - **Deploy from a branch**
   - **Branch**: `main`
   - **Folder**: `/ (root)`
5. Click **Save**

## Step 4: Wait for Deployment

- GitHub will build your site (takes 1-2 minutes)
- You'll see a green checkmark when it's ready
- Your site will be live at: `https://prithaguha.github.io`

## Troubleshooting

### If username is taken:
- Try with a suffix: `prithaguha-1`, `prithaguha-2`, etc.
- Update the repository name and remote URL accordingly

### If site shows 404:
- Wait 2-3 minutes for GitHub to build
- Check repository Settings > Pages for build status
- Verify branch is `main` and folder is `/ (root)`

### If API doesn't work:
- Check browser console (F12) for CORS errors
- Verify API URL in `sop.js` is correct
- Test API directly: `curl -X POST https://career-agent-api-tvpksobx5a-uc.a.run.app -H "Content-Type: application/json" -d '{"question":"test"}'`

