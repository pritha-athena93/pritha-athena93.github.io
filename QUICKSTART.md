# Quick Start Guide

Get your Career Agent website up and running in 30 minutes!

## Prerequisites Checklist

- [ ] Google Cloud Platform account with project `gen-ai-pritha`
- [ ] `gcloud` CLI installed and authenticated (`gcloud auth login`)
- [ ] GitHub account
- [ ] Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Step-by-Step Setup

### 1. Get Your Gemini API Key (5 minutes)

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key - you'll need it in step 3

### 2. Setup Secret Manager and Deploy Backend (10 minutes)

```bash
cd career-agent

# Setup Secret Manager with your API key
./scripts/setup-secret-manager.sh YOUR_GEMINI_API_KEY_HERE

# Deploy to Cloud Run (uses Secret Manager automatically)
./scripts/deploy-backend.sh
```

**Note**: The scripts will:
- Create secret in Secret Manager
- Enable required GCP APIs
- Build and deploy to Cloud Run with secret
- Show you the service URL

**Copy the service URL** - you'll need it for the frontend!

**Alternative**: If you prefer, you can store the API key in `backend/.env` and run `./scripts/setup-secret-manager.sh` without arguments.

### 3. Update Frontend with API URL (2 minutes)

Edit `career-agent/sop.js`:

```javascript
const API_ENDPOINT = 'https://career-agent-api-xxxxx-uc.a.run.app'; // Your URL here
```

### 4. Add Your PDFs (5 minutes)

Place your PDF files in `career-agent/`:
- `autobiography.pdf` - Your comprehensive career history
- `resume.pdf` - Your resume
- `cover_letter.pdf` - Your cover letter (optional)

### 5. Setup GitHub Pages (8 minutes)

```bash
cd career-agent

# Try username prithaguha first
./scripts/setup-github.sh prithaguha

# If that's taken, try with suffix
# ./scripts/setup-github.sh prithaguha-1
```

Then:
1. Create repository on GitHub: `https://github.com/new`
   - Name: `prithaguha.github.io` (or with suffix)
   - Make it **public**
2. Push to GitHub:
   ```bash
   git push -u origin main
   ```
3. Enable GitHub Pages:
   - Go to repository **Settings > Pages**
   - Source: **Deploy from branch**
   - Branch: **main** / **/ (root)**
   - Click **Save**

Your site will be live at `https://prithaguha.github.io` in 1-2 minutes!

## Testing

1. Visit your GitHub Pages URL
2. Try asking: "What is the candidate's experience with Python?"
3. Verify you get an answer

## Troubleshooting

### Backend not responding?
- Check Cloud Run logs: `gcloud run services logs read career-agent-api --region us-central1`
- Verify API key in Cloud Run environment variables
- Test API directly: `curl -X POST YOUR_URL -H "Content-Type: application/json" -d '{"question":"test"}'`

### Frontend shows error?
- Check browser console (F12)
- Verify API URL in `sop.js` matches your Cloud Run URL
- Ensure Cloud Run allows unauthenticated access

### PDFs not showing?
- Ensure PDFs are committed to git
- Check file names match exactly (case-sensitive)
- Verify PDFs are in repository root

## Next Steps

- Generate QR code pointing to your GitHub Pages URL
- Add QR code to your resume
- Share the link with recruiters!

## Cost Monitoring

Set up billing alerts in GCP Console:
1. Go to **Billing > Budgets & alerts**
2. Create budget for `gen-ai-pritha` project
3. Set alert threshold (e.g., $10/month)

## Support

- Check [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions
- Check [ARCHITECTURE.md](./ARCHITECTURE.md) for system design
- Review Cloud Run logs for backend issues

