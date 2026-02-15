from .base_agent import BaseAgent
from typing import Dict, Any

import google.generativeai as genai
import time

class CodeReviewerAgent(BaseAgent):
    """Agent B: The Code Reviewer. Analyzes source code or extracts it from video."""
    
    def run(self, input_data: Dict[str, Any]) -> str:
        source_code = input_data.get("source_code", "No source code provided.")
        video_path = input_data.get("video_path", None)
        rubric = input_data.get("rubric", "Standard Assessment")
        
        # 🚨 MULTIMODAL FALLBACK: If no text code, but video exists -> Use Gemini Vision
        if (not source_code or "No code provided" in source_code or len(source_code) < 10) and video_path:
            print("🎥 Code Reviewer: No text code found. Switching to VIDEO-BASED CODE REVIEW...")
            try:
                print(f"⬆️ Uploading video to Gemini for OCR analysis: {video_path}")
                video_file = genai.upload_file(video_path)
                
                # Wait for processing
                while video_file.state.name == "PROCESSING":
                    print(".", end="", flush=True)
                    time.sleep(2)
                    video_file = genai.get_file(video_file.name)
                
                if video_file.state.name != "ACTIVE":
                    return "ERROR: Video processing failed. Cannot extract code."

                print("✅ Video active. Analyzing code from screen recording...")
                
                prompt = [
                    video_file,
                    f"""
You are the SENIOR CODE REVIEWER AGENT using VISUAL ANALYSIS.
The candidate did not submit a text file. You must analyze the code visible in this video.

**TASKS:**
1. Watch the video and EXTRACT the code being written/shown.
2. Evaluate the syntax, logic, and efficiency of this visible code.
3. Identify 'Sudden Logic' (large blocks appearing instantly vs typing).

**GRADING RUBRIC:**
{rubric}

**OUTPUT FORMAT:**
- EXTRACTED CODE SUMMARY: [Brief description of what code was seen]
- SCORE: [X/100]
- TECHNICAL ANALYSIS: [Bullet points on quality]
- INTEGRITY CHECK: [Was the typing natural or pasted?]
"""
                ]
                return self.generate_response(prompt)
                
            except Exception as e:
                print(f"❌ Video-based review failed: {e}")
                return "ERROR: Could not perform video-based code review."

        # STANDARD TEXT ANALYSIS
        prompt = f"""
You are the SENIOR CODE REVIEWER AGENT. Your role is to evaluate the technical quality of the candidate's code.

**CODE TO REVIEW:**
```
{source_code}
```

**GRADING RUBRIC:**
{rubric}

**TASKS:**
1. Evaluate syntax, logic, and efficiency.
2. Identify any 'Sudden Logic' patterns (where complex code appears without intermediate steps).
3. Provide a technical grade (0-100).

**OUTPUT FORMAT:**
- SCORE: [X/100]
- TECHNICAL ANALYSIS: [Bullet points]
- INTEGRITY CHECK: [Was the development process logical?]
"""
        return self.generate_response(prompt)
