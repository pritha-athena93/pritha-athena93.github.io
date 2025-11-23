# Deployment Guide

Complete step-by-step guide to deploy the Career Agent application.

## Prerequisites

- Google Cloud Platform account with project `gen-ai-pritha`
- `gcloud` CLI installed and authenticated
- GitHub account
- Python 3.9+ (for local testing)

## Part 1: GCP Backend Deployment

### Step 1: Enable Required APIs

```bash
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    aiplatform.googleapis.com \
    --project=gen-ai-pritha
```

### Step 2: Create Service Account

```bash
# Create service account
gcloud iam service-accounts create career-agent-api \
    --display-name="Career Agent API Service Account" \
    --project=gen-ai-pritha

# Grant necessary permissions
gcloud projects add-iam-policy-binding gen-ai-pritha \
    --member="serviceAccount:career-agent-api@gen-ai-pritha.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"
```

### Step 3: Set Up Secret Manager (Recommended)

1. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Setup Secret Manager:

```bash
cd career-agent
./scripts/setup-secret-manager.sh YOUR_GEMINI_API_KEY_HERE
```

This will:
- Create a secret in Secret Manager
- Grant Cloud Run access to the secret
- Store your API key securely

**See [SECRET_MANAGER_SETUP.md](./SECRET_MANAGER_SETUP.md) for detailed instructions.**

### Step 4: Build and Deploy to Cloud Run

```bash
# From the career-agent directory
./scripts/deploy-backend.sh
```

This will automatically:
- Use the secret from Secret Manager
- Build and deploy using Cloud Build
- Configure Cloud Run with proper settings

**Or manually:**

```bash
cd backend
gcloud run deploy career-agent-api \
    --source . \
    --region us-central1 \
    --platform managed \
    --allow-unauthenticated \
    --memory 512Mi \
    --cpu 1 \
    --timeout 300 \
    --max-instances 10 \
    --update-secrets="GEMINI_API_KEY=gemini-api-key:latest" \
    --project gen-ai-pritha
```

### Step 5: Get the Service URL

After deployment, you'll get a URL like:
```
https://career-agent-api-xxxxx-uc.a.run.app
```

Copy this URL - you'll need it for the frontend.

## Part 2: GitHub Pages Setup

### Step 1: Create GitHub Repository

1. Go to GitHub and create a new repository
2. Repository name: `prithaguha.github.io` (or try `prithaguha-1`, `prithaguha-2`, etc. if taken)
3. Make it public
4. Initialize with README (optional)

### Step 2: Update Frontend Configuration

1. Edit `sop.js` and replace `YOUR_CLOUD_RUN_URL_HERE` with your Cloud Run URL:

```javascript
const API_ENDPOINT = 'https://career-agent-api-xxxxx-uc.a.run.app';
```

### Step 3: Add Your PDFs

Place your PDF files in the repository root:
- `autobiography.pdf`
- `resume.pdf`
- `cover_letter.pdf`

### Step 4: Push to GitHub

```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit: Career Agent website"
git branch -M main
git remote add origin https://github.com/prithaguha/prithaguha.github.io.git
git push -u origin main
```

### Step 5: Enable GitHub Pages

1. Go to repository Settings
2. Navigate to Pages section
3. Source: Deploy from a branch
4. Branch: `main` / `/ (root)`
5. Click Save

Your site will be live at `https://prithaguha.github.io` in a few minutes.

## Part 3: Testing

### Test the Backend API

```bash
curl -X POST https://career-agent-api-xxxxx-uc.a.run.app \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the candidate'\''s experience with Python?"}'
```

### Test the Frontend

1. Visit `https://prithaguha.github.io`
2. Try asking a question
3. Verify the answer appears correctly

## Part 4: QR Code Generation

Generate a QR code pointing to your GitHub Pages URL:

1. Use any QR code generator (e.g., [QR Code Generator](https://www.qr-code-generator.com/))
2. URL: `https://prithaguha.github.io`
3. Download and add to your resume

## Troubleshooting

### Backend Issues

- **403 Forbidden**: Check service account permissions
- **500 Error**: Check Cloud Run logs: `gcloud run services logs read career-agent-api --region us-central1`
- **API Key Error**: Verify Gemini API key in environment variables

### Frontend Issues

- **CORS Error**: Cloud Run service should allow unauthenticated access
- **404 on PDFs**: Ensure PDFs are in repository root and committed
- **API Not Working**: Verify the URL in `sop.js` matches your Cloud Run URL

### Cost Monitoring

Monitor costs in GCP Console:
- Cloud Run: Cloud Run > Services
- API Usage: APIs & Services > Dashboard

Set up billing alerts to avoid surprises.

## Updating the Application

### Update Backend

```bash
cd backend
# Make your changes
gcloud run deploy career-agent-api --source . --region us-central1 --project gen-ai-pritha
```

### Update Frontend

```bash
# Make your changes
git add .
git commit -m "Update frontend"
git push
```

GitHub Pages will automatically rebuild.

## Security Notes

- The Cloud Run service is set to allow unauthenticated access for simplicity
- For production, consider adding authentication
- API keys are stored in Cloud Run environment variables (secure)
- GitHub Pages is public by design

## Support

For issues or questions:
1. Check Cloud Run logs
2. Check browser console for frontend errors
3. Verify all URLs and API keys are correct

