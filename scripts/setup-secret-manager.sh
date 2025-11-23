#!/bin/bash

# Setup Secret Manager for Gemini API Key
# Usage: ./scripts/setup-secret-manager.sh [api_key]

set -e

PROJECT_ID="gen-ai-pritha"
SECRET_NAME="gemini-api-key"
REGION="us-central1"
SERVICE_NAME="career-agent-api"

echo "🔐 Setting up Secret Manager for Gemini API Key..."
echo "Project: $PROJECT_ID"
echo "Secret: $SECRET_NAME"
echo ""

# Set the project
gcloud config set project $PROJECT_ID

# Enable Secret Manager API
echo "🔌 Enabling Secret Manager API..."
gcloud services enable secretmanager.googleapis.com --project=$PROJECT_ID

# Get API key
if [ -z "$1" ]; then
    # Try to read from .env file
    if [ -f "backend/.env" ]; then
        API_KEY=$(grep GEMINI_API_KEY backend/.env | cut -d '=' -f2 | tr -d ' ')
        if [ -z "$API_KEY" ] || [ "$API_KEY" = "your_api_key_here" ]; then
            echo "❌ Error: No API key found in backend/.env"
            echo "Usage: $0 <api_key>"
            echo "   Or: Add GEMINI_API_KEY to backend/.env first"
            exit 1
        fi
    else
        echo "❌ Error: No API key provided and backend/.env not found"
        echo "Usage: $0 <api_key>"
        exit 1
    fi
else
    API_KEY="$1"
fi

# Check if secret already exists
if gcloud secrets describe $SECRET_NAME --project=$PROJECT_ID &>/dev/null; then
    echo "⚠️  Secret '$SECRET_NAME' already exists."
    read -p "Do you want to update it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📝 Updating secret..."
        echo -n "$API_KEY" | gcloud secrets versions add $SECRET_NAME \
            --data-file=- \
            --project=$PROJECT_ID
        echo "✅ Secret updated!"
    else
        echo "ℹ️  Keeping existing secret."
        exit 0
    fi
else
    # Create the secret
    echo "📝 Creating secret..."
    echo -n "$API_KEY" | gcloud secrets create $SECRET_NAME \
        --data-file=- \
        --replication-policy="automatic" \
        --project=$PROJECT_ID
    echo "✅ Secret created!"
fi

# Get the Cloud Run service account email
echo "🔍 Getting Cloud Run service account..."
SERVICE_ACCOUNT=$(gcloud run services describe $SERVICE_NAME \
    --region $REGION \
    --project $PROJECT_ID \
    --format="value(spec.template.spec.serviceAccountName)" 2>/dev/null || echo "")

if [ -z "$SERVICE_ACCOUNT" ]; then
    # Use default compute service account
    PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
    SERVICE_ACCOUNT="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
    echo "ℹ️  Using default compute service account: $SERVICE_ACCOUNT"
else
    echo "ℹ️  Using service account: $SERVICE_ACCOUNT"
fi

# Grant Secret Manager access to Cloud Run service account
echo "🔑 Granting Secret Manager access..."
gcloud secrets add-iam-policy-binding $SECRET_NAME \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/secretmanager.secretAccessor" \
    --project=$PROJECT_ID

echo ""
echo "✅ Secret Manager setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Deploy/update Cloud Run service to use the secret:"
echo "   ./scripts/deploy-backend.sh"
echo ""
echo "2. Or manually update the service:"
echo "   gcloud run services update $SERVICE_NAME \\"
echo "       --update-secrets=\"GEMINI_API_KEY=$SECRET_NAME:latest\" \\"
echo "       --region $REGION \\"
echo "       --project $PROJECT_ID"

