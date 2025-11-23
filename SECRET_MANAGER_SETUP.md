# Secret Manager Setup Guide

This guide shows you how to use **Google Cloud Secret Manager** to securely store your Gemini API key.

## Why Secret Manager?

✅ **More Secure**: Secrets are encrypted and managed by GCP  
✅ **Audit Trail**: Track who accessed secrets and when  
✅ **Version Control**: Manage multiple versions of secrets  
✅ **Rotation**: Easy to rotate secrets without code changes  
✅ **Best Practice**: Industry standard for production applications  

## Quick Setup

### Option 1: Automated Setup (Recommended)

```bash
cd career-agent

# Run setup script with your API key
./scripts/setup-secret-manager.sh YOUR_API_KEY_HERE

# Or if you have it in backend/.env
./scripts/setup-secret-manager.sh
```

Then deploy:
```bash
./scripts/deploy-backend.sh
```

### Option 2: Manual Setup

#### Step 1: Enable Secret Manager API

```bash
gcloud services enable secretmanager.googleapis.com \
    --project=gen-ai-pritha
```

#### Step 2: Create the Secret

```bash
echo -n "YOUR_GEMINI_API_KEY_HERE" | gcloud secrets create gemini-api-key \
    --data-file=- \
    --replication-policy="automatic" \
    --project=gen-ai-pritha
```

#### Step 3: Grant Cloud Run Access

Get your Cloud Run service account:

```bash
# Get project number
PROJECT_NUMBER=$(gcloud projects describe gen-ai-pritha --format="value(projectNumber)")

# Default service account
SERVICE_ACCOUNT="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

# Grant access
gcloud secrets add-iam-policy-binding gemini-api-key \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/secretmanager.secretAccessor" \
    --project=gen-ai-pritha
```

#### Step 4: Deploy Cloud Run with Secret

```bash
cd career-agent/backend

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

## Verify Setup

### Check Secret Exists

```bash
gcloud secrets describe gemini-api-key \
    --project=gen-ai-pritha
```

### Check Cloud Run is Using Secret

```bash
gcloud run services describe career-agent-api \
    --region us-central1 \
    --project gen-ai-pritha \
    --format="yaml(spec.template.spec.containers[0].env)"
```

You should see:
```yaml
env:
- name: GEMINI_API_KEY
  valueFrom:
    secretKeyRef:
      key: latest
      name: gemini-api-key
```

### Test the Service

```bash
# Get service URL
SERVICE_URL=$(gcloud run services describe career-agent-api \
    --region us-central1 \
    --project gen-ai-pritha \
    --format="value(status.url)")

# Test
curl -X POST $SERVICE_URL \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Python?"}'
```

## Updating the Secret

### Update Secret Value

```bash
echo -n "NEW_API_KEY_HERE" | gcloud secrets versions add gemini-api-key \
    --data-file=- \
    --project=gen-ai-pritha
```

This creates a new version. Cloud Run will automatically use the latest version.

### Force Cloud Run to Use New Version

If you want to explicitly update to a specific version:

```bash
gcloud run services update career-agent-api \
    --update-secrets="GEMINI_API_KEY=gemini-api-key:2" \
    --region us-central1 \
    --project gen-ai-pritha
```

## Viewing Secret Versions

```bash
gcloud secrets versions list gemini-api-key \
    --project=gen-ai-pritha
```

## Accessing Secret Value (for verification)

```bash
gcloud secrets versions access latest \
    --secret=gemini-api-key \
    --project=gen-ai-pritha
```

## Security Best Practices

### ✅ DO:
- Use Secret Manager for all sensitive data
- Grant minimal permissions (only to service accounts that need it)
- Enable audit logging
- Rotate secrets periodically
- Use versioning to track changes

### ❌ DON'T:
- Store secrets in code or environment variables directly
- Grant broad access to secrets
- Commit secrets to version control
- Share secret values in logs or error messages

## Cost

Secret Manager pricing (as of 2024):
- **Storage**: $0.06 per secret per month
- **Access**: $0.03 per 10,000 operations
- **Free Tier**: 6 secrets, 6 versions per secret

For this project: **~$0.06/month** (very affordable!)

## Troubleshooting

### "Permission denied" Error

Make sure the service account has access:

```bash
# Check IAM policy
gcloud secrets get-iam-policy gemini-api-key \
    --project=gen-ai-pritha

# Re-grant access if needed
PROJECT_NUMBER=$(gcloud projects describe gen-ai-pritha --format="value(projectNumber)")
gcloud secrets add-iam-policy-binding gemini-api-key \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor" \
    --project=gen-ai-pritha
```

### Secret Not Found

Verify the secret exists:

```bash
gcloud secrets list --project=gen-ai-pritha
```

### Cloud Run Can't Access Secret

Check Cloud Run logs:

```bash
gcloud run services logs read career-agent-api \
    --region us-central1 \
    --limit 50
```

Look for errors like "Permission denied" or "Secret not found".

## Migration from Environment Variables

If you previously used environment variables and want to migrate:

1. **Create secret** (see Step 2 above)
2. **Update Cloud Run** to use secret instead of env var:

```bash
gcloud run services update career-agent-api \
    --remove-env-vars="GEMINI_API_KEY" \
    --update-secrets="GEMINI_API_KEY=gemini-api-key:latest" \
    --region us-central1 \
    --project gen-ai-pritha
```

## Using Secret Manager in Code

The code doesn't need to change! Secret Manager automatically injects the secret as an environment variable. Your code in `backend/main.py` will work as-is:

```python
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
```

Cloud Run automatically reads from Secret Manager and makes it available as an environment variable.

## Summary

1. **Create secret**: `./scripts/setup-secret-manager.sh YOUR_API_KEY`
2. **Deploy**: `./scripts/deploy-backend.sh`
3. **Done!** ✅

The secret is now securely stored and automatically available to your Cloud Run service.

---

**Last Updated**: 2024-2025  
**Cost**: ~$0.06/month  
**Security**: Enterprise-grade encryption and access control

