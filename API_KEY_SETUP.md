# Gemini API Key Setup in GCP

## Where to Store the API Key

**Recommended**: Use **Google Cloud Secret Manager** for the most secure storage.  
**Alternative**: Store as an **environment variable** in your **Cloud Run service** (simpler but less secure).

👉 **See [SECRET_MANAGER_SETUP.md](./SECRET_MANAGER_SETUP.md) for Secret Manager setup (recommended)**

## Option 1: Set During Deployment (Recommended)

The deployment script automatically sets the API key from your `.env` file:

### Step 1: Create `.env` file

```bash
cd career-agent/backend
cp .env.example .env
```

### Step 2: Add your API key to `.env`

Edit `backend/.env` and add your key:

```bash
GEMINI_API_KEY=your_actual_api_key_here
PORT=8080
```

### Step 3: Deploy (script reads from .env)

```bash
cd ..
./scripts/deploy-backend.sh
```

The script automatically reads the key from `.env` and sets it in Cloud Run.

## Option 2: Set via gcloud Command

If you prefer to set it manually or update it later:

```bash
gcloud run services update career-agent-api \
    --set-env-vars="GEMINI_API_KEY=your_actual_api_key_here" \
    --region us-central1 \
    --project gen-ai-pritha
```

## Option 3: Set via GCP Console (Web UI)

1. Go to [Cloud Run Console](https://console.cloud.google.com/run)
2. Select project: `gen-ai-pritha`
3. Click on service: `career-agent-api`
4. Click **EDIT & DEPLOY NEW REVISION**
5. Scroll to **Variables & Secrets** section
6. Click **ADD VARIABLE**
7. Name: `GEMINI_API_KEY`
8. Value: Paste your API key
9. Click **DEPLOY**

## Option 4: Use Secret Manager (Most Secure - Advanced)

For production, use Google Secret Manager:

### Step 1: Create Secret

```bash
echo -n "your_actual_api_key_here" | gcloud secrets create gemini-api-key \
    --data-file=- \
    --project=gen-ai-pritha
```

### Step 2: Grant Cloud Run Access

```bash
gcloud secrets add-iam-policy-binding gemini-api-key \
    --member="serviceAccount:825707201403-compute@developer.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor" \
    --project=gen-ai-pritha
```

### Step 3: Update Cloud Run to Use Secret

```bash
gcloud run services update career-agent-api \
    --update-secrets="GEMINI_API_KEY=gemini-api-key:latest" \
    --region us-central1 \
    --project gen-ai-pritha
```

### Step 4: Update Code (if using Secret Manager)

Modify `backend/main.py` to handle secret format:

```python
# If using Secret Manager, the secret is automatically available as env var
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
```

## Verify API Key is Set

### Check via gcloud

```bash
gcloud run services describe career-agent-api \
    --region us-central1 \
    --project gen-ai-pritha \
    --format="value(spec.template.spec.containers[0].env)"
```

### Check via Console

1. Go to Cloud Run > `career-agent-api`
2. Click on the service
3. Check **Variables & Secrets** tab
4. You should see `GEMINI_API_KEY` listed

### Test the API

```bash
# Get your service URL
SERVICE_URL=$(gcloud run services describe career-agent-api \
    --region us-central1 \
    --project gen-ai-pritha \
    --format="value(status.url)")

# Test with a question
curl -X POST $SERVICE_URL \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Python?"}'
```

## Security Best Practices

### ✅ DO:
- Store API key in Cloud Run environment variables (encrypted at rest)
- Use Secret Manager for production (most secure)
- Never commit `.env` file to git (already in `.gitignore`)
- Rotate API keys periodically
- Use least privilege access

### ❌ DON'T:
- Hardcode API key in source code
- Commit API key to git repository
- Share API key in logs or error messages
- Use the same key for multiple projects without isolation

## Updating the API Key

If you need to update the API key:

### Method 1: Via gcloud

```bash
gcloud run services update career-agent-api \
    --update-env-vars="GEMINI_API_KEY=new_api_key_here" \
    --region us-central1 \
    --project gen-ai-pritha
```

### Method 2: Via Console

1. Cloud Run > `career-agent-api` > Edit
2. Update `GEMINI_API_KEY` value
3. Deploy new revision

## Troubleshooting

### API Key Not Working

1. **Verify key is set:**
   ```bash
   gcloud run services describe career-agent-api \
       --region us-central1 \
       --format="yaml(spec.template.spec.containers[0].env)"
   ```

2. **Check logs for errors:**
   ```bash
   gcloud run services logs read career-agent-api \
       --region us-central1 \
       --limit 50
   ```

3. **Test API key directly:**
   ```python
   import google.generativeai as genai
   genai.configure(api_key="your_key")
   model = genai.GenerativeModel('gemini-pro')
   response = model.generate_content("Hello")
   print(response.text)
   ```

### Common Issues

- **"API key not set"**: Key not in environment variables
- **"Invalid API key"**: Key is incorrect or expired
- **"Quota exceeded"**: Free tier limit reached
- **"Permission denied"**: Service account lacks permissions

## Quick Reference

**Location**: Cloud Run Service Environment Variables  
**Service**: `career-agent-api`  
**Region**: `us-central1`  
**Variable Name**: `GEMINI_API_KEY`  
**Project**: `gen-ai-pritha`

## Summary

The **easiest method** is Option 1 (deployment script):
1. Create `backend/.env` with your API key
2. Run `./scripts/deploy-backend.sh`
3. Done! ✅

For **production**, consider Option 4 (Secret Manager) for enhanced security.

---

**Note**: The API key is stored securely in GCP and is never exposed in the frontend code or GitHub repository.

