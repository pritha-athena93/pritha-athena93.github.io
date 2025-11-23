# Architecture Documentation

## System Overview

The Career Agent application consists of two main components:

1. **Frontend (GitHub Pages)**: Static website served for free
2. **Backend (Cloud Run)**: Python Flask API with Gemini AI integration

## Component Details

### Frontend (GitHub Pages)

**Location**: `index.html`, `sop.js`, `style.css`

**Responsibilities**:
- Display landing page with document links
- Provide Q&A interface
- Send questions to backend API
- Display AI-generated answers

**Technologies**:
- HTML5
- CSS3 (responsive design)
- Vanilla JavaScript (no frameworks)

**Hosting**: GitHub Pages (free, automatic HTTPS)

### Backend (Cloud Run)

**Location**: `backend/main.py`

**Responsibilities**:
- Receive questions from frontend
- Process questions using Gemini AI
- Apply SOP (Standard Operating Procedure) prompts
- Return formatted answers

**Technologies**:
- Python 3.11
- Flask (web framework)
- Google Generative AI (Gemini Pro)
- Gunicorn (WSGI server)

**Hosting**: Google Cloud Run (serverless, pay-per-use)

## Data Flow

```
1. Recruiter visits GitHub Pages URL
   ↓
2. Recruiter types question in frontend
   ↓
3. Frontend sends POST request to Cloud Run API
   ↓
4. Backend processes question with Gemini AI
   ↓
5. Backend applies SOP prompt template
   ↓
6. Gemini generates answer based on SOP
   ↓
7. Backend returns JSON response
   ↓
8. Frontend displays answer to recruiter
```

## SOP (Standard Operating Procedure)

The AI agent follows a structured prompt that:

1. **Understands Context**: Knows it's helping recruiters
2. **Analyzes Questions**: Breaks down recruiter questions
3. **References Documents**: Uses autobiography and career documents
4. **Provides Answers**: Gives detailed, recruiter-friendly responses
5. **Highlights Relevance**: Connects candidate experience to job requirements

The SOP is defined in `backend/main.py` as `SOP_PROMPT`.

## Security Considerations

### Frontend
- Public GitHub repository (by design)
- No sensitive data in frontend code
- API endpoint URL is public (acceptable for this use case)

### Backend
- API key stored in Cloud Run environment variables
- CORS enabled for GitHub Pages domain
- Unauthenticated access (can be restricted if needed)
- Serverless architecture (no persistent storage of questions)

## Cost Breakdown

### GitHub Pages
- **Cost**: Free
- **Limits**: 1GB storage, 100GB bandwidth/month

### Cloud Run
- **Free Tier**: 2 million requests/month
- **After Free Tier**: $0.40 per million requests
- **Compute**: 
  - Memory: 512Mi
  - CPU: 1 vCPU
  - Estimated: < $1/month for low traffic

### Gemini API
- **Free Tier**: Available (check current limits)
- **Pricing**: Pay-per-use after free tier
- **Estimated**: < $5/month for moderate usage

### Total Estimated Cost
- **Low Usage**: $0-2/month
- **Moderate Usage**: $2-10/month
- **High Usage**: $10-50/month

## Scalability

### Frontend
- GitHub Pages handles traffic automatically
- No scaling concerns

### Backend
- Cloud Run auto-scales from 0 to configured max
- Default: 10 max instances
- Can handle traffic spikes automatically
- Cold starts: ~1-2 seconds (acceptable for this use case)

## Monitoring

### Recommended Monitoring
1. **Cloud Run Metrics**: Requests, latency, errors
2. **Cloud Logging**: API logs and errors
3. **Billing Alerts**: Set up in GCP Console
4. **GitHub Pages**: Built-in analytics (if enabled)

### Key Metrics to Watch
- Request count
- Response time
- Error rate
- API costs
- Memory/CPU usage

## Future Enhancements

Potential improvements:
1. **Authentication**: Add API key or OAuth for backend
2. **Caching**: Cache common questions
3. **PDF Processing**: Actually parse PDFs instead of relying on prompts
4. **Analytics**: Track popular questions
5. **Multi-language**: Support multiple languages
6. **Voice Input**: Add speech-to-text
7. **Export**: Allow exporting Q&A sessions

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Solution: Verify CORS is enabled in Flask app
   - Check: Cloud Run allows unauthenticated access

2. **API Key Errors**
   - Solution: Verify GEMINI_API_KEY in Cloud Run environment
   - Check: API key is valid and has quota

3. **Slow Responses**
   - Solution: Check Gemini API latency
   - Consider: Adding timeout handling in frontend

4. **High Costs**
   - Solution: Monitor usage in GCP Console
   - Consider: Adding rate limiting

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│         GitHub Repository               │
│  prithaguha.github.io                   │
│  ├── index.html                         │
│  ├── sop.js                             │
│  ├── style.css                          │
│  └── *.pdf                              │
└──────────────┬──────────────────────────┘
               │
               │ Git Push
               │
┌──────────────▼──────────────────────────┐
│      GitHub Pages (CDN)                 │
│  https://prithaguha.github.io           │
└──────────────┬──────────────────────────┘
               │
               │ HTTP POST
               │
┌──────────────▼──────────────────────────┐
│      Cloud Run Service                  │
│  career-agent-api                       │
│  ├── Flask API                          │
│  └── Gemini AI Integration              │
└──────────────┬──────────────────────────┘
               │
               │ API Call
               │
┌──────────────▼──────────────────────────┐
│      Google Generative AI                │
│      (Gemini Pro)                       │
└─────────────────────────────────────────┘
```

## Environment Variables

### Backend (.env)
- `GEMINI_API_KEY`: Google Generative AI API key
- `PORT`: Server port (set by Cloud Run)

### Frontend (sop.js)
- `API_ENDPOINT`: Cloud Run service URL

## API Specification

### POST /
**Request**:
```json
{
  "question": "Does this candidate have Kubernetes experience?"
}
```

**Response**:
```json
{
  "answer": "Yes, the candidate has extensive experience with Kubernetes...",
  "question": "Does this candidate have Kubernetes experience?"
}
```

**Error Response**:
```json
{
  "error": "Error message here"
}
```

## Dependencies

### Backend
- `flask==3.0.0`: Web framework
- `flask-cors==4.0.0`: CORS support
- `google-generativeai==0.3.1`: Gemini AI SDK
- `gunicorn==21.2.0`: WSGI server

### Frontend
- No external dependencies (vanilla JavaScript)

