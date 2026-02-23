from .base_agent import BaseAgent
from typing import Dict, Any

import google.generativeai as genai
import time

class CodeReviewerAgent(BaseAgent):
    """Agent B: The Code Reviewer. Reads submitted code AND watches screen recording simultaneously."""
    
    def run(self, input_data: Dict[str, Any]) -> str:
        source_code = input_data.get("source_code", "No source code provided.")
        video_path = input_data.get("video_path", None)
        rubric = input_data.get("rubric", "Standard Assessment")
        gemini_video_file = input_data.get("gemini_video_file", None)

        # PHASE 2 ENHANCED MODE: Code file submitted + Gemini video uploaded by orchestrator.
        # Gemini watches the screen recording AND reads the submitted code simultaneously.
        # Key advantage over Phase 1: Gemini can now compare "what was typed" vs "what was submitted".
        if gemini_video_file and source_code and len(source_code) > 10:
            print("🎥 Code Reviewer: Multimodal analysis (submitted code + screen recording)...")
            prompt = [
                gemini_video_file,
                f"""
You are the SENIOR CODE REVIEWER AGENT. You have access to BOTH the student's submitted code AND their screen recording.

**SUBMITTED CODE (what the student handed in):**
```
{source_code}
```

**YOUR TASKS — Cross-Reference Screen vs Submission:**
1. Watch the screen recording carefully. Note EXACTLY when each code block appeared on screen.
2. Flag any 'Sudden Logic': code that appears in under 3 seconds rather than being typed incrementally.
3. Compare what was typed on screen with the submitted code. Are they consistent? Any last-minute swaps?
4. Evaluate the technical quality of the submitted code against the rubric.

**GRADING RUBRIC + IDEAL SOLUTION CONTEXT:**
{rubric}

**OUTPUT FORMAT:**
- SCORE: [X/100]
- SCREEN vs SUBMISSION MATCH: [Consistent / Discrepancy found — explain]
- SUDDEN LOGIC EVENTS: [Timestamps where code appeared instantly, if any. 'None' if clean.]
- TECHNICAL ANALYSIS: [Bullet points on code quality]
- INTEGRITY CHECK: [Authentic / Suspicious / Fraudulent — with reasoning]
"""
            ]
            return self.generate_response(prompt)

        # VIDEO-ONLY FALLBACK: No code file submitted — watch screen to extract code (same as Phase 1)
        if (not source_code or "No code provided" in source_code or len(source_code) < 10):
            print("🎥 Code Reviewer: No code file found. Switching to screen-recording analysis...")
            video_file_to_use = gemini_video_file  # Use pre-uploaded if available
            if not video_file_to_use and video_path:
                try:
                    print(f"⬆️ Uploading video to Gemini for OCR analysis: {video_path}")
                    video_file_to_use = genai.upload_file(video_path)
                    while video_file_to_use.state.name == "PROCESSING":
                        print(".", end="", flush=True)
                        time.sleep(2)
                        video_file_to_use = genai.get_file(video_file_to_use.name)
                    if video_file_to_use.state.name != "ACTIVE":
                        return "ERROR: Video processing failed. Cannot extract code."
                except Exception as e:
                    print(f"❌ Video-only review failed: {e}")
                    return "ERROR: Could not perform video-based code review."

            if video_file_to_use:
                prompt = [
                    video_file_to_use,
                    f"""
You are the SENIOR CODE REVIEWER AGENT using VISUAL ANALYSIS.
The candidate did not submit a code file. Analyze the code visible in this screen recording.

**TASKS:**
1. Extract the code being written or shown on screen.
2. Evaluate its syntax, logic, and efficiency.
3. Identify 'Sudden Logic' (large blocks appearing instantly vs being typed).

**GRADING RUBRIC:**
{rubric}

**OUTPUT FORMAT:**
- EXTRACTED CODE SUMMARY: [What code was seen]
- SCORE: [X/100]
- TECHNICAL ANALYSIS: [Bullet points]
- INTEGRITY CHECK: [Natural typing or pasted?]
"""
                ]
                return self.generate_response(prompt)

        # TEXT-ONLY ANALYSIS: No video available at all
        prompt = f"""
You are the SENIOR CODE REVIEWER AGENT. Evaluate the technical quality of the submitted code.

**CODE TO REVIEW:**
```
{source_code}
```

**GRADING RUBRIC:**
{rubric}

**OUTPUT FORMAT:**
- SCORE: [X/100]
- TECHNICAL ANALYSIS: [Bullet points]
- INTEGRITY CHECK: [Is the development process logical?]
"""
        return self.generate_response(prompt)
