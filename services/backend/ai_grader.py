import google.generativeai as genai
import os
import time
from typing import Dict, Any

from agents.orchestrator import AgentOrchestrator
from rag.rag_manager import RagManager

class AIGrader:
    # Optimized for video analysis - Prioritizing Gemini 3 and 2.5 series
    MODEL_FALLBACK_ORDER = [
        'models/gemini-3-flash-preview', # Primary: Cutting edge reasoning
        'models/gemini-2.5-flash',       # Fallback 1: Latest 2.5 series
        'models/gemini-2.5-flash-lite',  # Fallback 2: High efficiency 2.5
        'models/gemini-2.0-flash',       # Fallback 3: Proven 2.0 frontier
        'models/gemini-flash-latest',    # Fallback 4: Stable workhorse
        'models/gemini-pro-latest'       # Fallback 5: High quality fallback
    ]
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.api_key = api_key
        self.model = None
        self.current_model_name = None
        
        # Phase 2 Components
        self.orchestrator = AgentOrchestrator()
        self.rag_manager = RagManager()
        self.agentic_mode = os.getenv("AGENTIC_MODE", "off").lower() == "on"
        
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

    async def grade_video(self, video_path: str, rubric: str, behavioral_flags: list = None, source_code: str = None) -> str:
        """Analyzes a video against a rubric using dynamic model fallback or Agentic Orchestration."""
        
        # Phase 2: Agentic Workflow
        if self.agentic_mode:
            print("🧠 Phase 2: Triggering Agentic Multi-Modal Analysis...")
            cv_summary = ""
            if behavioral_flags:
                for flag in behavioral_flags:
                    cv_summary += f"- [{flag['timestamp']}] {flag['issue']} ({flag['severity']})\n"
            
            # Run the multi-agent synthesis
            return await self.orchestrator.run_analysis(
                video_data={"cv_context": cv_summary, "video_path": video_path},
                source_code=source_code or "No code provided",
                rubric=rubric
            )

        # Phase 1: Legacy Linear Workflow (Fallback)
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

            # Build dynamic prompt based on proctoring mode and rubric type
            if proctoring_enabled:
                # Check if this is a custom rubric or a default one
                is_custom_rubric = rubric and not any(default in rubric for default in [
                    "Python 3.x compatibility", 
                    "Correct Java Syntax", 
                    "Proper CLI usage",
                    "Overall code structure"
                ])
                
                if is_custom_rubric:
                    # CUSTOM RUBRIC MODE: User's instructions take priority, behavioral data is supplementary
                    prompt = f"""
You are a Technical Assessment AI evaluating a candidate's coding performance.

**PRIMARY DIRECTIVE - CUSTOM GRADING RUBRIC:**
{rubric}

**SUPPLEMENTARY BEHAVIORAL DATA:**
The following behavioral events were detected during the session:
{cv_context if cv_context else "No significant behavioral anomalies detected."}

**ANALYSIS TASKS:**
1. Evaluate the candidate strictly according to the CUSTOM RUBRIC provided above.
2. Use the behavioral data as supplementary context, but the rubric is your PRIMARY instruction.
3. Provide specific timestamps for key events.
4. Give a score from 0-100 based on the custom rubric criteria.

**OUTPUT FORMAT:**

### 📝 Assessment Report
**Status:** [Complete / Incomplete]

### 📋 Executive Summary
[Brief overview of the candidate's performance against the custom rubric]

### 🕒 Detailed Timeline
[Chronological log with MM:SS timestamps of key events]

### 📊 Custom Rubric Evaluation
[Item-by-item assessment based on the provided custom rubric]

### 🚨 Behavioral Context (Supplementary)
[Summary of behavioral flags if any, for context only]

### 🏆 Final Score
**X/100**

### 🖋️ Justification
[Detailed explanation of the score based on the custom rubric]
                    """
                else:
                    # STRICT MODE: Default rubric with integrity-first scoring
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
                    # Handle both quota issues AND "Model Not Found" issues
                    if any(x in error_msg.lower() for x in ["429", "quota", "404", "not found", "supported"]):
                        print(f"⚠️ Model {model_name} failed or unavailable. Attempting fallback...")
                        continue # Try next model
                    else:
                        raise e # Re-raise if it's a critical logic/auth error

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
