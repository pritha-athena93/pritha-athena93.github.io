# Career Agent - GitHub Pages Recruiting Assistant

A professional recruiting assistant website hosted on GitHub Pages with an AI-powered backend on Google Cloud Platform.

## Overview

This project provides:
- A clean, professional landing page for recruiters
- Access to career documents (autobiography, resume, cover letter)
- An AI-powered Q&A interface that answers questions about the candidate's background
- All hosted for free (GitHub Pages + minimal GCP costs)

## Architecture

```
┌─────────────────┐
│  GitHub Pages   │  (Frontend - Free)
│   index.html    │
│   sop.js        │
│   style.css     │
└────────┬────────┘
         │
         │ HTTP POST
         │
┌────────▼────────┐
│  Cloud Run API  │  (Backend - ~$0/month minimal usage)
│  Python Flask   │
│  + Gemini API   │
└─────────────────┘
```

## Repository Structure

```
career-agent/
├── index.html              # Landing page
├── sop.js                  # Frontend JavaScript for API calls
├── style.css               # Styling
├── autobiography.pdf       # Long-form career history (add your file)
├── resume.pdf              # Resume (add your file)
├── cover_letter.pdf        # Cover letter (add your file)
├── README.md               # This file
├── DEPLOYMENT.md           # Deployment instructions
├── backend/                # GCP Cloud Run backend
│   ├── main.py            # Flask API server
│   ├── requirements.txt   # Python dependencies
│   ├── Dockerfile         # Container configuration
│   └── .env.example       # Environment variables template
└── scripts/                # Deployment scripts
    ├── deploy-backend.sh  # Deploy Cloud Run service
    └── setup-github.sh    # Setup GitHub Pages
```

## Setup Instructions

### 1. GitHub Pages Setup

1. Create a new GitHub repository named `prithaguha.github.io` (or with suffix if taken)
2. Push all frontend files to the repository
3. Enable GitHub Pages in repository settings (Settings > Pages)
4. Select main branch as source
5. Your site will be live at `https://prithaguha.github.io`

### 2. GCP Backend Setup

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions.

Quick steps:
1. Enable required APIs in GCP
2. Create a service account with necessary permissions
3. Deploy the Cloud Run service
4. Update `sop.js` with the Cloud Run URL

### 3. Add Your Documents

Replace the placeholder PDFs:
- `autobiography.pdf` - Your comprehensive career history
- `resume.pdf` - Your resume
- `cover_letter.pdf` - Your cover letter

## Features

- **Clean UI**: Professional, responsive design
- **Document Access**: Easy access to all career documents
- **AI Q&A**: Ask questions about background, skills, projects
- **Cost-Effective**: Free frontend, minimal backend costs
- **Secure**: GitHub domain for trust, GCP for secure API

## Cost Estimate

- **GitHub Pages**: Free
- **Cloud Run**: 
  - Free tier: 2 million requests/month
  - After free tier: ~$0.40 per million requests
  - Memory/CPU: Minimal usage, typically < $1/month
- **Gemini API**: Free tier available, then pay-per-use
- **Total**: ~$0-5/month depending on usage

## Maintenance

- Update PDFs when you have new experience
- Monitor Cloud Run usage in GCP Console
- Review and improve AI prompts in `backend/main.py`
- Track common questions to improve responses

## License

Personal project - all rights reserved.

