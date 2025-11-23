#!/bin/bash

# Deploy Career Agent Backend to Cloud Run
# Usage: ./scripts/deploy-backend.sh
# Note: Assumes Secret Manager is set up (run setup-secret-manager.sh first)

set -e

PROJECT_ID="gen-ai-pritha"
SERVICE_NAME="career-agent-api"
REGION="us-central1"
SECRET_NAME="gemini-api-key"

echo "🚀 Deploying Career Agent API to Cloud Run..."
echo "Project: $PROJECT_ID"
echo "Service: $SERVICE_NAME"
echo "Region: $REGION"
echo ""

# Check if we're in the right directory
if [ ! -f "backend/main.py" ]; then
    echo "❌ Error: backend/main.py not found. Run this script from the career-agent directory."
    exit 1
fi

# Check if secret exists
if ! gcloud secrets describe $SECRET_NAME --project=$PROJECT_ID &>/dev/null; then
    echo "⚠️  Secret '$SECRET_NAME' not found in Secret Manager."
    echo "📝 Setting up Secret Manager first..."
    echo ""
    read -p "Enter your Gemini API key: " -s API_KEY
    echo ""
    if [ -z "$API_KEY" ]; then
        echo "❌ Error: API key is required"
        exit 1
    fi
    ./scripts/setup-secret-manager.sh "$API_KEY"
    echo ""
fi

# Set the project
echo "📋 Setting GCP project..."
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔌 Enabling required APIs..."
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    aiplatform.googleapis.com \
    secretmanager.googleapis.com \
    --project=$PROJECT_ID

# Deploy to Cloud Run with Secret Manager
echo "🏗️  Building and deploying to Cloud Run..."
cd backend

gcloud run deploy $SERVICE_NAME \
    --source . \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --memory 512Mi \
    --cpu 1 \
    --timeout 300 \
    --max-instances 10 \
    --update-secrets="GEMINI_API_KEY=$SECRET_NAME:latest" \
    --project $PROJECT_ID

cd ..

# Get the service URL
echo ""
echo "✅ Deployment complete!"
echo ""
echo "📝 Service URL:"
gcloud run services describe $SERVICE_NAME \
    --region $REGION \
    --project $PROJECT_ID \
    --format="value(status.url)"

echo ""
echo "🔗 Update sop.js with this URL!"

