# Exam-Flow Backend Architecture & Flow Charts

## 1. Overall System Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                     EXAM-FLOW BACKEND SYSTEM                     │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│  Video Upload    │
│  (MP4, WebM,     │
│   AVI, MOV,      │
│   MKV, FLV)      │
└────────┬─────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│              FastAPI Backend (main.py)                           │
│  Endpoints:                                                      │
│  • POST /analyze-video (Custom uploads)                         │
│  • GET  /analyze-demo/{type} (Pre-loaded demos)                 │
└────────┬────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    File Processing Layer                         │
│  • Save uploaded file to uploads/ directory                     │
│  • Extract metadata (filename, size, format)                    │
│  • Validate file integrity                                      │
└────────┬────────────────────────────────────────────────────────┘
         │
         ▼
    ┌────┴────┐
    │ Routing │
    └────┬────┘
         │
    ┌────┴──────────────────────────────┐
    │                                   │
    ▼                                   ▼
┌──────────────────┐          ┌──────────────────┐
│  Proctoring      │          │  Skip Proctoring │
│  Enabled?        │          │  (Direct to AI)  │
└────────┬─────────┘          └────────┬─────────┘
         │                              │
         ▼                              │
┌─────────────────────────────────────┐│
│   ProctorEngine (proctor.py)        ││
│   ┌─────────────────────────────┐   ││
│   │ OpenCV Video Analysis       │   ││
│   │ • Face Detection            │   ││
│   │ • Eye/Gaze Tracking         │   ││
│   │ • Behavioral Flag Generation│   ││
│   └─────────────────────────────┘   ││
│   Returns: behavioral_flags[]       ││
└────────┬────────────────────────────┘│
         │                              │
         └──────────────┬───────────────┘
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│              AIGrader (ai_grader.py)                             │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ 1. Upload video to Gemini API                             │  │
│  │ 2. Wait for file processing (ACTIVE state)                │  │
│  │ 3. Determine grading mode:                                │  │
│  │    ┌──────────────────────────────────────────────────┐   │  │
│  │    │ Custom Rubric Provided?                          │   │  │
│  │    │  YES → Custom Rubric Mode                        │   │  │
│  │    │  NO  → Check Proctoring Status                   │   │  │
│  │    │         • Enabled  → Integrity-First Mode        │   │  │
│  │    │         • Disabled → Technical-Only Mode         │   │  │
│  │    └──────────────────────────────────────────────────┘   │  │
│  │ 4. Build dynamic AI prompt based on mode                  │  │
│  │ 5. Send to Gemini 2.0 Flash (with fallback chain)         │  │
│  │ 6. Parse and return structured report                     │  │
│  └───────────────────────────────────────────────────────────┘  │
└────────┬────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Response Assembly                             │
│  {                                                               │
│    "type": "Python/Java/Docker/General",                        │
│    "report": "AI-generated technical assessment",               │
│    "behavioral_flags": [...],                                   │
│    "proctoring_enabled": true/false                             │
│  }                                                               │
└────────┬────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│              Return to Frontend (Streamlit)                      │
│  • Display AI Report                                            │
│  • Show Behavioral Timeline                                     │
│  • Generate PDF Export                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Video Processing Pipeline (Detailed)

```text
START: Video File Received
         │
         ▼
┌─────────────────────────────────────────┐
│  Step 1: File Validation                │
│  • Check file extension                 │
│  • Verify file size (< 2GB recommended) │
│  • Validate MIME type                   │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Step 2: Save to Disk                   │
│  Path: uploads/{filename}               │
│  • Create uploads/ if not exists        │
│  • Write binary content                 │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Step 3: Parallel Processing            │
│  ┌─────────────┐  ┌──────────────────┐  │
│  │ Proctoring  │  │ AI Upload        │  │
│  │ Analysis    │  │ to Gemini        │  │
│  │ (if enabled)│  │                  │  │
│  └──────┬──────┘  └────────┬─────────┘  │
└─────────┼──────────────────┼────────────┘
          │                  │
          ▼                  ▼
    [OpenCV]           [Gemini API]
    Processing         File Upload
          │                  │
          │                  ▼
          │         ┌─────────────────┐
          │         │ Wait for ACTIVE │
          │         │ (polling loop)  │
          │         └────────┬────────┘
          │                  │
          └──────────┬───────┘
                     ▼
         ┌────────────────────────┐
         │ Combine Results        │
         │ • Behavioral Flags     │
         │ • Video File Reference │
         └────────┬───────────────┘
                  │
                  ▼
         ┌────────────────────────┐
         │ Send to AI Grader      │
         └────────────────────────┘
```

---

## 3. AI Grading Decision Tree

```text
                    ┌──────────────────────┐
                    │  Receive Grading     │
                    │  Request             │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Proctoring Enabled?  │
                    └──────────┬───────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
               YES                           NO
                │                             │
                ▼                             ▼
    ┌────────────────────────┐    ┌──────────────────────┐
    │ Behavioral Flags       │    │ Technical-Only Mode  │
    │ Available?             │    │ • No behavioral data │
    └────────┬───────────────┘    │ • Pure code grading  │
             │                    │ • 0-100 score range  │
    ┌────────┴────────┐           └──────────────────────┘
    │                 │
   YES               NO
    │                 │
    ▼                 ▼
┌─────────────┐  ┌─────────────────┐
│ Has Custom  │  │ Default Mode    │
│ Rubric?     │  │ (No Flags)      │
└──────┬──────┘  └─────────────────┘
       │
  ┌────┴────┐
  │         │
 YES       NO
  │         │
  ▼         ▼
┌──────────────────────┐  ┌────────────────────────────┐
│ CUSTOM RUBRIC MODE   │  │ INTEGRITY-FIRST MODE       │
│ ─────────────────────│  │ ───────────────────────────│
│ Prompt Structure:    │  │ Prompt Structure:          │
│ • Custom criteria    │  │ • ELITE PROCTOR persona    │
│   as PRIMARY         │  │ • 20/100 cap for cheating  │
│ • Behavioral data    │  │ • Cross-reference CV flags │
│   as SUPPLEMENTARY   │  │   with code events         │
│ • No automatic caps  │  │ • Strict integrity checks  │
│ • Flexible scoring   │  │ • Forensic timeline        │
└──────────┬───────────┘  └────────────┬───────────────┘
           │                           │
           └────────────┬──────────────┘
                        ▼
            ┌────────────────────────┐
            │ Model Fallback Chain   │
            │ 1. gemini-2.0-flash    │
            │ 2. gemini-1.5-flash    │
            │ 3. gemini-1.5-pro      │
            └────────────┬───────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │ Parse AI Response      │
            │ • Extract score        │
            │ • Format timeline      │
            │ • Structure report     │
            └────────────┬───────────┘
                         │
                         ▼
                    RETURN REPORT
```

---

## 4. Proctoring Analysis Flow (OpenCV Engine)

```text
START: Video File Path
         │
         ▼
┌─────────────────────────────────────────┐
│  Initialize Haar Cascade Classifiers    │
│  • haarcascade_frontalface_default.xml  │
│  • haarcascade_eye.xml                  │
│  • haarcascade_eye_tree_eyeglasses.xml  │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Open Video with cv2.VideoCapture       │
│  • Get FPS (frames per second)          │
│  • Calculate total frames               │
│  • Set sampling interval (every 2 sec)  │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Frame Processing Loop                  │
│  FOR each sampled frame:                │
└────────┬────────────────────────────────┘
         │
         ▼
    ┌────────────────────┐
    │ Convert to Grayscale│
    └────────┬───────────┘
             │
             ▼
    ┌────────────────────┐
    │ Detect Faces       │
    │ (Haar Cascade)     │
    └────────┬───────────┘
             │
        ┌────┴────┐
        │         │
    No Face    Face Found
        │         │
        ▼         ▼
  ┌──────────┐  ┌──────────────────┐
  │ Flag:    │  │ Detect Eyes/Gaze │
  │ Face     │  │ in face region   │
  │ Missing  │  └────────┬─────────┘
  └──────────┘           │
                    ┌────┴────┐
                    │         │
                No Eyes    Eyes Found
                    │         │
                    ▼         ▼
            ┌──────────┐  ┌──────────┐
            │ Flag:    │  │ Normal   │
            │ Gaze     │  │ (No flag)│
            │ Aversion │  └──────────┘
            └──────────┘
                    │
                    ▼
         ┌────────────────────────┐
         │ Accumulate Flags       │
         │ {                      │
         │   timestamp: "MM:SS",  │
         │   issue: "...",        │
         │   severity: "High/Med" │
         │ }                      │
         └────────┬───────────────┘
                  │
                  ▼
         ┌────────────────────────┐
         │ Continue to Next Frame │
         └────────┬───────────────┘
                  │
                  ▼
         ┌────────────────────────┐
         │ END: Return Flag Array │
         └────────────────────────┘
```

---

## 5. Model Fallback & Error Handling

```text
┌──────────────────────────────────────────┐
│  AI Grading Request Initiated            │
└────────┬─────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│  Try Model: gemini-2.0-flash             │
└────────┬─────────────────────────────────┘
         │
    ┌────┴────┐
    │         │
 Success   Error (429/500)
    │         │
    │         ▼
    │    ┌──────────────────────────────┐
    │    │ Log Error & Try Next Model   │
    │    │ → gemini-1.5-flash           │
    │    └────────┬─────────────────────┘
    │             │
    │        ┌────┴────┐
    │        │         │
    │     Success   Error
    │        │         │
    │        │         ▼
    │        │    ┌──────────────────────┐
    │        │    │ Try Final Fallback   │
    │        │    │ → gemini-1.5-pro     │
    │        │    └────────┬─────────────┘
    │        │             │
    │        │        ┌────┴────┐
    │        │        │         │
    │        │     Success   Error
    │        │        │         │
    └────────┴────────┘         ▼
             │            ┌──────────────┐
             │            │ Raise HTTP   │
             │            │ Exception    │
             │            │ 500          │
             │            └──────────────┘
             ▼
    ┌──────────────────┐
    │ Return AI Report │
    └──────────────────┘
```

---

## 6. Key Components Explained

### **main.py** (FastAPI Backend)

- **Purpose**: HTTP endpoint orchestration
- **Key Functions**:
  - `analyze_demo()`: Pre-loaded demo video analysis
  - `analyze_video_v2()`: Custom video upload handler
- **Responsibilities**:
  - File upload handling
  - Rubric selection/validation
  - Coordinating ProctorEngine and AIGrader
  - Response formatting

### **proctor.py** (OpenCV Proctoring Engine)

- **Purpose**: Behavioral analysis using computer vision
- **Key Functions**:
  - `analyze_behavior()`: Main entry point
  - Face detection using Haar Cascades
  - Eye/gaze tracking with eyeglasses support
- **Output**: Array of timestamped behavioral flags

### **ai_grader.py** (Gemini AI Integration)

- **Purpose**: Video content analysis and grading
- **Key Functions**:
  - `grade_video()`: Main grading orchestrator
  - `upload_to_gemini()`: File upload to Gemini API
  - `wait_for_files_active()`: Polling for file processing
- **Features**:
  - Dynamic prompt generation (3 modes)
  - Model fallback chain for reliability
  - Structured report parsing

---

## 7. Data Flow Summary

```text
Video Upload → File Save → Parallel Processing
                              │
                ┌─────────────┴─────────────┐
                │                           │
         OpenCV Analysis            Gemini Upload
                │                           │
         Behavioral Flags            File Reference
                │                           │
                └─────────────┬─────────────┘
                              │
                        AI Grading
                              │
                    ┌─────────┴─────────┐
                    │                   │
            Custom Rubric        Default Rubric
                    │                   │
                    └─────────┬─────────┘
                              │
                      Technical Report
                              │
                        JSON Response
```

---

## 8. Supported Video Formats

| Format | Extension | MIME Type           | Notes                    |
|--------|-----------|---------------------|--------------------------|
| MP4    | .mp4      | video/mp4           | Most common, recommended |
| WebM   | .webm     | video/webm          | Web-optimized            |
| AVI    | .avi      | video/x-msvideo     | Legacy support           |
| MOV    | .mov      | video/quicktime     | Apple format             |
| MKV    | .mkv      | video/x-matroska    | High-quality container   |
| FLV    | .flv      | video/x-flv         | Flash video              |

All formats are processed identically by both OpenCV and Gemini API.
