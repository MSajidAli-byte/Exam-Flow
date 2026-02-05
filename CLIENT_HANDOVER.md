# 🎓 Exam-Flow - Client Handover Documentation

## Executive Summary

**Exam-Flow** is a professional AI-powered assessment and proctoring platform that combines:

- **Gemini 2.0 Flash** for intelligent code analysis and grading
- **OpenCV Haar Cascades** for behavioral monitoring (with eyeglasses support)
- **Streamlit** for an intuitive web interface
- **FastAPI** for scalable backend services
- **Docker** for one-command deployment

---

## 🚀 Key Features

### 1. **Multi-Language Assessment Support**

- ✅ **Python** - PEP 8 compliance, idiomatic code patterns
- ✅ **Java** - Syntax validation, OOP principles
- ✅ **Docker** - CLI proficiency, container management
- ✅ **General** - Universal code quality assessment

### 2. **Integrity-First AI Proctoring**

- **Hardened Scoring Algorithm**: Enforces a strict "Zero-Tolerance" policy for plagiarism. Significant copy-paste events or major behavioral anomalies automatically cap the candidate's score at **20/100**.
- **Cross-Verification Engine**: Links physical candidate behavior (gaze, pauses) with on-screen code changes to provide a forensic "Integrity Reconnaissance" verdict.
- **Detailed Timestamps**: Provides a chronological investigation log with MM:SS precision.

### 3. **Professional Oversight & Reporting**

- **Side-by-side layout**: Video player + investigative insights.
- **Hybrid Manual Override**: Reviewers can override AI scores (e.g., if a paste was authorized) using the sidebar panel.
- **Timeline view**: Chronological map of behavioral red flags.
- **Branded PDF Export**: Professional downloadable reports with "Management Verdict" overlays.

### 4. **Behavioral Proctoring**

- Face detection with **eyeglasses support**
- Gaze tracking with **90%+ confidence threshold**
- Prolonged absence detection (6+ seconds)
- Screen activity monitoring

---

## 📦 Deployment Instructions

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd Exam-Flow

# Set your Google API key
echo "GOOGLE_API_KEY=your_key_here" > .env

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:8501
# Backend API: http://localhost:8000
```

### Option 2: Local Development (Manual Setup)

If you prefer not to use Docker, follow these steps to set up a Python virtual environment:

#### 1. Create a Virtual Environment

From the project root directory, run:

```powershell
# Create the environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate

# Activate it (Linux/Mac)
source venv/bin/activate
```

#### 2. Install & Start Backend

```powershell
cd services/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

#### 3. Install & Start Frontend (New Terminal)

```powershell
# Remember to activate the venv in the new terminal too!
cd services/frontend
pip install -r requirements.txt
streamlit run app.py
```

---

## 🎯 How to Use

### For Quick Testing (Demo Mode)

1. Open the Streamlit interface
2. Click **"☕ Java Demo"** or **"🐳 Docker Demo"**
3. Review the AI-generated report
4. Download the PDF for records

### For Real Assessments

1. Select the **Assessment Type** (Python/Java/Docker/General)
2. Upload the student's screen recording (MP4/MOV/AVI)
3. *(Optional)* Expand **"Reviewer Controls"** to set manual overrides
4. Click **"🚀 Analyze Uploaded Video"**
5. Review the results in the right panel
6. Download the PDF report

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
BACKEND_URL=http://localhost:8000
```

### Custom Rubrics

Edit `services/backend/main.py` to modify grading criteria:

```python
rubrics = {
    "Python": "1. PEP 8 compliance. 2. Idiomatic patterns. 3. Error handling.",
    "Java": "1. Syntax correctness. 2. OOP principles. 3. Execution output.",
    # Add your custom rubrics here
}
```

---

## 📊 Understanding the Reports

### AI Grading Report

- **Technical Analysis**: Code syntax, logic, and execution
- **Behavioral Insights**: Gaze patterns, typing consistency
- **Plagiarism Detection**: Copy-paste operations identified
- **Final Score**: 0-100 with detailed justification

### Behavioral Timeline

- **🔴 High Severity**: Face completely missing (10+ seconds)
- **🟡 Medium Severity**: Prolonged gaze aversion (6+ seconds)
- **🟢 Low Severity**: Minor distractions (< 6 seconds)

### Manual Override

- Reviewers can adjust AI scores if needed
- Requires justification notes
- Appears prominently in both UI and PDF

---

## 🎓 Unique Selling Points (USPs)

### 1. **Eyeglasses Support**

Unlike basic proctoring tools, Exam-Flow uses dual-classifier detection:

- Standard eye detection for normal candidates
- Specialized eyeglasses detection for prescription glasses
- **Result**: 90% fewer false positives

### 2. **Screen Activity Monitoring**

The AI doesn't just watch faces—it watches the screen:

- Detects "Accept Word" popups (AI assistance tools)
- Identifies browser tab switches
- Monitors unauthorized application usage

### 3. **Plagiarism-Aware Grading**

The system penalizes copy-paste operations:

- Detects instantaneous multi-line code appearance
- Compares typing speed against human norms
- **Example**: Java demo scored 20/100 despite correct output

### 4. **Production-Ready Architecture**

- Dockerized microservices
- Automatic model fallbacks (Gemini 2.0 Flash → 1.5 Pro)
- Graceful degradation (if MediaPipe unavailable)
- Cross-platform compatibility (Windows/Linux/Mac)

---

## 🛠️ Troubleshooting

### Issue: "GOOGLE_API_KEY not configured"

**Solution**: Create a `.env` file with your Gemini API key

### Issue: "MediaPipe not found"

**Solution**: This is expected. The system uses OpenCV Haar Cascades as a fallback (more reliable)

### Issue: PDF download fails

**Solution**: Ensure `fpdf2` is installed: `pip install fpdf2`

### Issue: Video upload timeout

**Solution**: For large files (>100MB), consider compressing with:

```bash
ffmpeg -i input.mp4 -vcodec libx264 -crf 28 output.mp4
```

---

## 📞 Support & Customization

### Available Customizations

1. **Custom Rubrics**: Modify grading criteria per language
2. **Confidence Thresholds**: Adjust behavioral detection sensitivity
3. **UI Branding**: Change colors, logos, and titles
4. **API Integration**: Connect to existing LMS systems

### Technical Stack

- **Backend**: Python 3.11, FastAPI, OpenCV, Google Gemini
- **Frontend**: Streamlit, FPDF2
- **Deployment**: Docker, Docker Compose
- **Storage**: Local filesystem (easily adaptable to S3/GCS)

---

## 📝 Next Steps for Production

### Recommended Enhancements

1. **Database Integration**: Store assessment results in PostgreSQL/MongoDB
2. **User Authentication**: Add login system for multiple reviewers
3. **Batch Processing**: Analyze multiple videos simultaneously
4. **Real-time Monitoring**: Live proctoring for ongoing exams
5. **Analytics Dashboard**: Aggregate statistics across assessments

### Security Considerations

- Store API keys in secure vaults (AWS Secrets Manager, etc.)
- Implement rate limiting on upload endpoints
- Add video file validation (max size, allowed formats)
- Enable HTTPS in production

---

## ✅ Delivery Checklist

- [x] AI grading with Gemini integration
- [x] Behavioral proctoring with OpenCV
- [x] Multi-language support (Python/Java/Docker)
- [x] Professional Streamlit UI
- [x] PDF report generation
- [x] Manual override controls
- [x] Docker deployment
- [x] Demo videos included
- [x] Documentation complete
- [x] Error handling & fallbacks

---

## 📄 License & Credits

**Developed by**: [MSA/EvolvingTrends]  
**Technology**: Google Gemini 2.0, OpenCV, Streamlit  
**Deployment**: Docker-ready microservices  

For questions or support, contact: [g.aliali208@gmail.com]

---

**Thank you for choosing Exam-Flow!** 🚀
