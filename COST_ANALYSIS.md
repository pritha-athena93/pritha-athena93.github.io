# Cost Analysis - Career Agent Project

## Gemini AI API Pricing (as of 2024-2025)

### Current Pricing Models

The project uses **Gemini Pro** (or **Gemini 2.5 Pro** if available). Here are the current pricing tiers:

#### Gemini 2.5 Pro (Recommended for Production)

**Input Tokens:**
- Up to 200,000 tokens/month: **$1.25 per million tokens**
- Over 200,000 tokens/month: **$2.50 per million tokens**

**Output Tokens:**
- Up to 200,000 tokens/month: **$10.00 per million tokens**
- Over 200,000 tokens/month: **$15.00 per million tokens**

#### Gemini 2.5 Flash-Lite (Budget Option)

**Input Tokens:**
- Text/Image/Video: **$0.10 per million tokens**
- Audio: **$0.30 per million tokens**

**Output Tokens:**
- **$0.40 per million tokens**

### Free Tier

Google typically offers a **free tier** for new users, but the exact limits vary. Check the [official pricing page](https://ai.google.dev/pricing) for current free tier details.

Common free tier limits (may vary):
- 15 requests per minute (RPM)
- 1,500 requests per day (RPD)
- Limited tokens per month

### Cost Estimation for Career Agent

#### Typical Usage Scenario

**Assumptions:**
- Average question: ~100 tokens input, ~500 tokens output
- 10 questions per day
- 300 questions per month

**Monthly Token Usage:**
- Input: 10 questions/day × 100 tokens × 30 days = **30,000 tokens/month**
- Output: 10 questions/day × 500 tokens × 30 days = **150,000 tokens/month**

#### Cost Calculation (Gemini 2.5 Pro)

**Input Cost:**
- 30,000 tokens = 0.03 million tokens
- Cost: 0.03 × $1.25 = **$0.0375/month**

**Output Cost:**
- 150,000 tokens = 0.15 million tokens
- Cost: 0.15 × $10.00 = **$1.50/month**

**Total Gemini API Cost: ~$1.54/month**

#### Cost Calculation (Gemini 2.5 Flash-Lite - Budget Option)

**Input Cost:**
- 30,000 tokens = 0.03 million tokens
- Cost: 0.03 × $0.10 = **$0.003/month**

**Output Cost:**
- 150,000 tokens = 0.15 million tokens
- Cost: 0.15 × $0.40 = **$0.06/month**

**Total Gemini API Cost: ~$0.06/month**

### Complete Project Cost Breakdown

| Service | Monthly Cost | Notes |
|---------|-------------|-------|
| **GitHub Pages** | $0 | Free tier sufficient |
| **Cloud Run** | $0-1 | Free tier: 2M requests/month |
| **Gemini API (Pro)** | $1.50-2 | 300 questions/month |
| **Gemini API (Flash-Lite)** | $0.06-0.10 | Budget option |
| **Total (Pro)** | **$1.50-3/month** | Very affordable |
| **Total (Flash-Lite)** | **$0.06-1/month** | Extremely cheap |

### Cost Optimization Tips

1. **Use Flash-Lite Model**: Switch to `gemini-2.5-flash-lite` for 95% cost savings
   - Update `backend/main.py`: Change `'gemini-pro'` to `'gemini-2.5-flash-lite'`
   - Quality is slightly lower but usually sufficient for Q&A

2. **Implement Caching**: Cache common questions to reduce API calls
   - Store Q&A pairs in Cloud Run memory or Cloud Storage
   - Check cache before calling API

3. **Rate Limiting**: Limit requests per IP to prevent abuse
   - Add rate limiting in Flask app
   - Use Cloud Run's built-in rate limiting

4. **Monitor Usage**: Set up billing alerts
   - GCP Console > Billing > Budgets & alerts
   - Set threshold (e.g., $5/month)

### High Usage Scenario

**If you get 100 questions/day (3,000/month):**

**Gemini Pro:**
- Input: 300,000 tokens = $0.375
- Output: 1,500,000 tokens = $15.00
- **Total: ~$15.38/month**

**Gemini Flash-Lite:**
- Input: 300,000 tokens = $0.03
- Output: 1,500,000 tokens = $0.60
- **Total: ~$0.63/month**

### Free Tier Strategy

1. **Start with Free Tier**: Use free tier limits first
2. **Monitor Usage**: Track when you approach limits
3. **Upgrade When Needed**: Only pay when you exceed free tier

### Billing Alerts Setup

```bash
# Set up billing alert in GCP Console
# 1. Go to Billing > Budgets & alerts
# 2. Create budget for gen-ai-pritha project
# 3. Set threshold: $5/month
# 4. Add email alerts
```

### Cost Comparison with Alternatives

| Service | Cost per 1M Output Tokens | Notes |
|---------|--------------------------|-------|
| **Gemini 2.5 Flash-Lite** | $0.40 | Budget option |
| **Gemini 2.5 Pro** | $10.00 | Higher quality |
| **OpenAI GPT-4** | ~$30.00 | More expensive |
| **OpenAI GPT-3.5** | ~$1.50 | Comparable to Gemini Pro |

### Recommendations

1. **Start with Flash-Lite**: Use `gemini-2.5-flash-lite` for lowest costs
2. **Monitor First Month**: Track actual usage and costs
3. **Upgrade if Needed**: Switch to Pro if quality is insufficient
4. **Set Alerts**: Always set billing alerts to avoid surprises

### Real-World Example

**Scenario**: 50 recruiters visit, 20 ask questions, average 2 questions each = 40 questions/month

**Cost with Flash-Lite:**
- Input: 4,000 tokens = $0.0004
- Output: 20,000 tokens = $0.008
- **Total: Less than $0.01/month**

**Cost with Pro:**
- Input: 4,000 tokens = $0.005
- Output: 20,000 tokens = $0.20
- **Total: ~$0.21/month**

### Conclusion

For a recruiting assistant with moderate usage:
- **Minimum Cost**: ~$0.06/month (Flash-Lite)
- **Recommended**: ~$1.50-2/month (Pro)
- **High Usage**: ~$15/month (Pro, 100 questions/day)

**The project is extremely cost-effective**, especially with the Flash-Lite model option.

---

**Last Updated**: 2024-2025  
**Source**: [Google AI Pricing](https://ai.google.dev/pricing)  
**Note**: Prices may change - always check official pricing page

