# Deployment Checklist

Use this checklist to ensure everything is set up correctly.

## Pre-Deployment

- [ ] Google Cloud Platform account ready
- [ ] Project `gen-ai-pritha` exists and is accessible
- [ ] `gcloud` CLI installed (`gcloud --version`)
- [ ] `gcloud` authenticated (`gcloud auth login`)
- [ ] GitHub account ready
- [ ] Gemini API key obtained from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Backend Deployment

- [ ] Navigate to `career-agent` directory
- [ ] Create `backend/.env` file from `.env.example`
- [ ] Add `GEMINI_API_KEY` to `backend/.env`
- [ ] Run `./scripts/deploy-backend.sh`
- [ ] Verify deployment succeeded
- [ ] Copy Cloud Run service URL
- [ ] Test API with curl:
  ```bash
  curl -X POST YOUR_URL -H "Content-Type: application/json" -d '{"question":"test"}'
  ```

## Frontend Configuration

- [ ] Open `sop.js`
- [ ] Replace `YOUR_CLOUD_RUN_URL_HERE` with actual Cloud Run URL
- [ ] Save file

## Add Your Documents

- [ ] Add `autobiography.pdf` to `career-agent/` directory
- [ ] Add `resume.pdf` to `career-agent/` directory
- [ ] Add `cover_letter.pdf` to `career-agent/` directory (optional)
- [ ] Verify PDFs are readable and not corrupted

## GitHub Pages Setup

- [ ] Check if username `prithaguha` is available on GitHub
- [ ] If taken, decide on suffix (e.g., `prithaguha-1`)
- [ ] Run `./scripts/setup-github.sh prithaguha` (or with suffix)
- [ ] Create GitHub repository:
  - [ ] Name: `prithaguha.github.io` (or with suffix)
  - [ ] Make it **public**
  - [ ] Don't initialize with README (we have one)
- [ ] Push to GitHub: `git push -u origin main`
- [ ] Enable GitHub Pages:
  - [ ] Go to repository Settings
  - [ ] Navigate to Pages section
  - [ ] Source: Deploy from branch
  - [ ] Branch: `main` / `/ (root)`
  - [ ] Click Save
- [ ] Wait 1-2 minutes for site to go live
- [ ] Visit `https://prithaguha.github.io` (or your URL)

## Testing

- [ ] Landing page loads correctly
- [ ] All PDF links work (click each one)
- [ ] Q&A interface appears
- [ ] Test question: "What is the candidate's experience with Python?"
- [ ] Verify answer appears
- [ ] Test another question
- [ ] Check browser console for errors (F12)

## QR Code

- [ ] Generate QR code pointing to GitHub Pages URL
- [ ] Test QR code with phone camera
- [ ] Verify it opens correct website
- [ ] Add QR code to resume

## Cost Monitoring

- [ ] Set up GCP billing account (if not already)
- [ ] Create budget alert in GCP Console:
  - [ ] Go to Billing > Budgets & alerts
  - [ ] Create budget for `gen-ai-pritha`
  - [ ] Set threshold (e.g., $10/month)
  - [ ] Add email alerts
- [ ] Monitor Cloud Run usage in first week

## Documentation Review

- [ ] Read `README.md` for overview
- [ ] Read `QUICKSTART.md` for quick setup
- [ ] Read `DEPLOYMENT.md` for detailed steps
- [ ] Read `ARCHITECTURE.md` for technical details
- [ ] Read `PROJECT_SUMMARY.md` for project overview

## Final Verification

- [ ] Website is accessible
- [ ] All PDFs download correctly
- [ ] Q&A interface works
- [ ] AI provides relevant answers
- [ ] No console errors
- [ ] Mobile responsive (test on phone)
- [ ] QR code works
- [ ] Costs are minimal

## Maintenance Reminders

- [ ] Update PDFs when you have new experience
- [ ] Monitor GCP costs monthly
- [ ] Review Cloud Run logs periodically
- [ ] Update SOP prompt if needed (in `backend/main.py`)
- [ ] Keep Gemini API key secure

## Troubleshooting

If something doesn't work:

- [ ] Check Cloud Run logs: `gcloud run services logs read career-agent-api --region us-central1`
- [ ] Check browser console for frontend errors
- [ ] Verify API URL in `sop.js`
- [ ] Verify API key in Cloud Run environment
- [ ] Test API directly with curl
- [ ] Check GitHub Pages build status
- [ ] Review documentation in `DEPLOYMENT.md`

---

**Status**: Ready to deploy  
**Estimated Time**: 30-45 minutes  
**Difficulty**: Intermediate

