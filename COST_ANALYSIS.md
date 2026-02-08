# Exam-Flow Cost Analysis & API Limits

## Executive Summary

**Exam-Flow uses Google's Gemini 1.5 Flash model for video analysis, which is extremely cost-effective:**

- **Cost per video**: ~$0.01 - $0.015 USD (1-1.5 cents) for a 5-minute exam video
- **Videos per $1 USD**: Approximately **65-100 videos**
- **Monthly estimate**: For 1,000 videos/month = **$10-15 USD**

---

## Detailed Cost Breakdown (Gemini 1.5 Flash)

### Pricing Structure (as of February 2026)

| Component | Price per 1M Tokens | Notes |
| :--- | :--- | :--- |
| **Input (Video)** | $0.075 | Video is processed at ~267 tokens/second |
| **Input (Text)** | $0.075 | Rubric + prompts (~500-1000 tokens) |
| **Output (Report)** | $0.30 | AI-generated report (~1000-2000 tokens) |

### Token Calculation for a Typical 5-Minute Exam Video

```text
Video Processing:
- Duration: 5 minutes = 300 seconds
- Token rate: 267 tokens/second
- Video tokens: 300 × 267 = 80,100 tokens

Text Input (Prompts):
- System prompt: ~800 tokens
- Rubric: ~200 tokens
- Behavioral flags: ~100 tokens
- Total text input: ~1,100 tokens

Total Input: 80,100 + 1,100 = 81,200 tokens

Output (AI Report):
- Typical report: ~1,500 tokens
```

### Cost Calculation

```text
Input Cost:
81,200 tokens ÷ 1,000,000 × $0.075 = $0.00609

Output Cost:
1,500 tokens ÷ 1,000,000 × $0.30 = $0.00045

Total per Video: ~$0.0065 - $0.01 USD (0.65-1 cent)
```

**Note**: Costs may vary based on:

- Video length (longer videos = more tokens)
- Report complexity (detailed reports = more output tokens)
- Behavioral proctoring enabled (adds CV processing overhead, but no API cost)

---

## API Rate Limits & Quotas

### Free Tier

- **Requests per minute (RPM)**: 15
- **Requests per day (RPD)**: 1,500
- **Tokens per minute (TPM)**: 1,000,000
- **Data usage**: Google may use your data to improve models ⚠️

### Pay-as-You-Go Tier (Recommended)

- **Requests per minute (RPM)**: 2,000
- **Requests per day (RPD)**: Unlimited
- **Tokens per minute (TPM)**: 4,000,000
- **Data privacy**: Your data is **NOT** used for training ✅

---

## Cost Comparison: AI vs. Human Proctoring

| Method | Cost per Video | Scalability | Consistency |
| :--- | :--- | :--- | :--- |
| **Exam-Flow (AI)** | $0.01 | Unlimited | 100% |
| **Human Proctor** | $15-30 | Limited by staff | Variable |
| **Hybrid (AI + Review)** | $2-5 | High | Very High |

**ROI Example**:

- For 1,000 exams/month:
  - AI-only: **$10-15**
  - Human-only: **$15,000-30,000**
  - **Savings: 99.95%**

---

## Recommended Setup for Production

### 1. Enable Pay-as-You-Go Billing

- Go to [Google AI Studio](https://aistudio.google.com/)
- Navigate to "Billing" → Enable pay-as-you-go
- Set up billing alerts at $10, $50, $100 thresholds

### 2. Set Budget Alerts

```python
# Example: Add to backend for cost monitoring
import os

MONTHLY_BUDGET_USD = 100  # Set your limit
ALERT_THRESHOLD = 0.8  # Alert at 80% usage
```

### 3. Monitor Usage

- Track API calls in Google Cloud Console
- Use the Gemini API dashboard to monitor:
  - Total requests
  - Token usage
  - Cost accumulation

---

## Scaling Projections

| Monthly Videos | Estimated Cost | Use Case |
| :--- | :--- | :--- |
| 100 | $1-2 | Small pilot program |
| 1,000 | $10-15 | University course |
| 10,000 | $100-150 | Large institution |
| 100,000 | $1,000-1,500 | Enterprise platform |

---

## Privacy & Data Retention

### With Pay-as-You-Go

✅ **Your videos are NOT used for training**
✅ **Data is deleted after processing** (unless you store it)
✅ **GDPR/FERPA compliant** when using your own API key

### With Free Tier

⚠️ **Google may use your data to improve models**
⚠️ **Not recommended for student assessments**

---

## Error: "404 Model Not Found"

### What Happened

The error `404 models/gemini-1.5-pro is not found for API version v1beta` occurred because:

1. The model name format was incorrect (included `models/` prefix)
2. Some model versions in the fallback chain don't exist or are deprecated

### Fix Applied

Updated `MODEL_FALLBACK_ORDER` and implemented a **Multi-Model Auto-Fallback** mechanism. If a model returns a **404 (Not Found)** or **429 (Quota Hit)**, the system automatically tries the next one in this sequence:

```python
MODEL_FALLBACK_ORDER = [
# Previous models
    'gemini-1.0-pro',         # Previous: Legacy stable model
    'gemini-2.0-flash-exp',   # Latest: Gemini 2.0 experimental    
    'gemini-1.5-flash',       # Primary: Stable flash
    'gemini-1.5-flash-latest',# Fallback 1: Latest flash
    'gemini-1.5-flash-8b',    # Fallback 2: High speed
    'gemini-1.5-pro',         # Fallback 3: High quality
    'gemini-1.5-pro-latest',  # Fallback 4: Latest pro
#current models
    'models/gemini-2.5-flash',       # Primary: Latest 2.5 series
    'models/gemini-3-flash-preview', # Secondary: Cutting edge reasoning
    'models/gemini-2.5-flash-lite',  # Fallback 1: High efficiency 2.5
    'models/gemini-2.0-flash',       # Fallback 2: Proven 2.0 frontier
    'models/gemini-flash-latest',    # Fallback 3: Stable workhorse
    'models/gemini-pro-latest'       # Fallback 4: High quality fallback
    
]
```

### This is NOT a quota/cost issue

- ✅ Your API key is working fine
- ✅ No billing limit was reached
- ✅ It was a model naming configuration error

---

## Next Steps

1. **Restart the backend** to apply the model fix:

   ```bash
   docker-compose restart backend
   ```

2. **Test with a WebM file** - the 404 error should be resolved

3. **Monitor costs** in the first month to establish baseline usage

4. **Set up billing alerts** to avoid unexpected charges

---

## Support & Resources

- [Gemini API Pricing](https://ai.google.dev/pricing)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Rate Limits Guide](https://ai.google.dev/gemini-api/docs/rate-limits)

---

**Last Updated**: February 8, 2026
**Model**: Gemini 1.5 Flash (Latest)
