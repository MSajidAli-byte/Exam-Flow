import google.generativeai as genai
import os
import time
from typing import Dict, Any

class AIGrader:
    # Verified exact model names for quota resilience and performance
    MODEL_FALLBACK_ORDER = [
        'models/gemini-2.0-flash',
        'models/gemini-2.5-flash',
        'models/gemini-3-flash-preview',
        'models/gemini-flash-latest',
        'models/gemini-2.0-flash-lite',
        'models/gemini-1.5-pro',
    ]
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.api_key = api_key
        self.model = None
        self.current_model_name = None
        
        # Initial model selection
        self.switch_model(self.MODEL_FALLBACK_ORDER[0])

    def switch_model(self, model_name: str):
        """Switches the active model instance."""
        try:
            self.model = genai.GenerativeModel(model_name)
            self.current_model_name = model_name
            print(f"🔄 Switched to model: {model_name}")
            return True
        except Exception as e:
            print(f"⚠️ Failed to switch to {model_name}: {e}")
            return False

    def upload_to_gemini(self, path: str, mime_type: str = None):
        """Uploads the given file to Gemini."""
        file = genai.upload_file(path, mime_type=mime_type)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file

    def wait_for_files_active(self, files):
        """Waits for the given files to be active."""
        print("Waiting for file processing...")
        for name in (f.name for f in files):
            file = genai.get_file(name)
            while file.state.name == "PROCESSING":
                print(".", end="", flush=True)
                time.sleep(2)
                file = genai.get_file(name)
            if file.state.name != "ACTIVE":
                raise Exception(f"File {file.name} failed to process")
        print("...all files active")

    def grade_video(self, video_path: str, rubric: str, behavioral_flags: list = None) -> str:
        """Analyzes a video against a rubric using dynamic model fallback for quota resilience."""
        video_file = None
        try:
            video_file = self.upload_to_gemini(video_path, mime_type="video/mp4")
            self.wait_for_files_active([video_file])

            # Determine if proctoring is enabled
            proctoring_enabled = behavioral_flags is not None and len(behavioral_flags) > 0
            
            # Format CV flags for the prompt (only if proctoring is enabled)
            cv_context = ""
            if proctoring_enabled:
                cv_context = "\n**COMPUTER VISION FORENSIC FLAGS:**\n"
                for flag in behavioral_flags:
                    if flag['severity'] != 'Info':
                        cv_context += f"- [{flag['timestamp']}] {flag['issue']} (Severity: {flag['severity']})\n"

            # Build dynamic prompt based on proctoring mode
            if proctoring_enabled:
                # STRICT MODE: Integrity-first scoring with behavioral analysis
                prompt = f"""
You are an ELITE ACADEMIC PROCTOR and SENIOR TECHNICAL INVESTIGATOR. Your primary goal is to verify the INDEPENDENT production of work.

{cv_context}

**CRITICAL DIRECTIVE: INTEGRITY-FIRST SCORING**
- If you detect COPY-PASTING of significant code blocks, EXTERNAL ASSISTANCE, or deliberate PLAGIARISM, the **MAXIMUM score you can give is 20/100**.
- A functional solution that was cheated on is a FAILURE. Do not reward technical correctness if the process was fraudulent.
- Cross-reference Behavioral Flags (detected by CV or observed in video) with technical events (sudden appearance of logic). 

**GRADING RUBRIC:**
{rubric}

**ANALYSIS TASKS:**

## 1. INTEGRITY & PROCTORING (HIGHEST PRIORITY)
- Monitor for **Sudden Code Appearance**: If complex logic appears in <3 seconds, flag as possible paste.
- Monitor for **Gaze Aversion**: Looking away from the screen for >5s during critical coding moments is a major red flag (Investigation required).
- Monitor for **Window Switching**: Any evidence of unauthorized tool usage or browser searching.

## 2. TECHNICAL & CODE EVALUATION
- ONLY if integrity is verified, assess technical skill.
- Analyze logic, syntax, best practices, and error handling.
- Note specific timestamps for all major technical milestones.

**OUTPUT FORMAT:**
You must provide a professional proctoring investigation report.

### 🕵️ INTEGRITY RECONNAISSANCE
**Verdict:** [PASS / SUSPICIOUS / FAIL]
**Integrity Notes:** [Explain why you trust or distrust the candidate. Specifically link physical behavior to on-screen code changes.]

### 📝 CHRONOLOGICAL LOG & TIMESTAMPS
[Detailed breakdown: 
HH:MM - [ACTION] - [OBSERVATION]
Example: 00:45 - High-level logic suddenly appeared - SUSPICION: Plagiarism/Paste.]

### 📊 RUBRIC ASSESSMENT
[Evaluate each item from the rubric provided.]

### 🔴 BEHAVIORAL RED FLAGS
[List infractions with timestamps. If none, state: "No forensic anomalies detected."]

### 🏆 FINAL VERDICT SCORE
**X/100**

**VERDICT JUSTIFICATION:**
[A strong, clear explanation of why this score was given. If plagiarism was found, explicitly state that the score was capped due to integrity failure.]
                """
            else:
                # TECHNICAL-ONLY MODE: Pure code grading without behavioral analysis
                prompt = f"""
You are a Senior Technical Interviewer evaluating a candidate's coding performance based solely on the technical quality of their work.

**IMPORTANT**: Behavioral proctoring has been DISABLED for this assessment. Do NOT analyze gaze, face detection, or copy-paste behavior. Focus ONLY on the technical rubric below.

**GRADING RUBRIC:**
{rubric}

**ANALYSIS TASKS:**
1. Watch the video and evaluate the candidate's technical approach.
2. Assess the final code quality, logic, and adherence to the rubric.
3. Provide specific timestamps for key technical milestones.
4. Give a score from 0-100 based purely on technical merit.

**OUTPUT FORMAT:**

### 📝 Technical Assessment Report
**Status:** [Complete / Incomplete]

### 📋 Executive Summary
[Brief overview of the candidate's technical performance]

### 🕒 Detailed Timeline
[Chronological log with MM:SS timestamps of key technical events]

### 📊 Rubric Evaluation
[Item-by-item assessment based on the provided rubric]

### 🏆 Final Technical Score
**X/100**

### 🖋️ Justification
[Detailed explanation of the score based on technical merit only]
                """

            # Dynamic Fallback Loop
            tried_models = []
            for model_name in self.MODEL_FALLBACK_ORDER:
                tried_models.append(model_name)
                success = self.switch_model(model_name)
                if not success: continue
                
                try:
                    response = self.model.generate_content([video_file, prompt])
                    return response.text
                except Exception as e:
                    error_msg = str(e)
                    if "429" in error_msg or "quota" in error_msg.lower():
                        print(f"🛑 Quota hit for {model_name}. Attempting fallback...")
                        continue # Try next model
                    else:
                        raise e # Re-raise if it's not a quota issue

            # If all models fail
            return f"""
# ❌ Quota Exhausted Across All Models

The system attempted multiple models ({', '.join(tried_models)}) to bypass the Gemini API free-tier limits, but all are currently at their capacity.

**Recommendations:**
1. Wait 60 seconds (RPM limit) or 24 hours (Daily limit)
2. Upgrade to a paid plan for unlimited production access
3. Provide a fresh API key in the configuration
            """

        except Exception as e:
            return f"# ❌ Analysis Error\n\n**Details:** {str(e)}"
