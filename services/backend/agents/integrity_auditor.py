from .base_agent import BaseAgent
from typing import Dict, Any

class IntegrityAuditorAgent(BaseAgent):
    """Agent C: The Integrity Auditor. Cross-references Visual Proctor flags, Code Review, and screen recording."""
    
    def run(self, input_data: Dict[str, Any]) -> str:
        visual_report = input_data.get("visual_report", "")
        code_report = input_data.get("code_report", "")
        gemini_video_file = input_data.get("gemini_video_file", None)

        # PHASE 2 SUPERIORITY: The Integrity Auditor watches the screen recording directly.
        # It has THREE sources simultaneously: OpenCV face flags, Code Review report, AND raw video.
        # Phase 1 had ONE source (Gemini watching the video alone).
        # Phase 2 has the structured agent reports as additional evidence alongside the video.
        if gemini_video_file:
            prompt = [
                gemini_video_file,
                f"""
You are the ELITE INTEGRITY AUDITOR with access to structured agent reports AND the raw screen recording.

**OPENCV BEHAVIORAL FLAGS (from Visual Proctor Agent):**
{visual_report}

**CODE REVIEW FINDINGS (from Code Reviewer Agent — includes Screen vs Submission analysis):**
{code_report}

**YOUR TASKS — Final Triangulation:**
1. Watch the screen recording for any behavioral events not captured by OpenCV (e.g., tab switching, external help).
2. Cross-reference the Code Reviewer's 'Sudden Logic Events' with the student's face/gaze data in the video.
3. Cross-reference the Code Reviewer's 'Screen vs Submission Match' — if discrepancies exist, flag them.
4. Determine a final integrity confidence score.

**CRITICAL CORRELATION RULES:**
- If complex code appeared suddenly (Code Reviewer flag) AND the face was absent (Visual Proctor flag) at that timestamp → HIGH RISK FRAUD. (Pasting test data, arrays, or boilerplate is NOT fraud).
- If submitted code differs fundamentally from what was typed on screen (e.g. different algorithms or completely altered logic) → SUBMISSION TAMPERING. (Minor missing edge-cases, removed print statements, or changed array data are NOT tampering).
- If code appeared while gaze was averted → EXTERNAL REFERENCE suspected.

**OUTPUT FORMAT:**
- AUDIT STATUS: [PASS / FAIL / INVESTIGATION]
- CONFIDENCE SCORE: [0.0 - 1.0]
- DISCREPANCIES: [List any mismatched events with timestamps. 'None' if clean.]
- REASONING: [Concise explanation of the verdict]
"""
            ]
            return self.generate_response(prompt)

        # FALLBACK: No video — text-only cross-reference (still better than Phase 1 for structured output)
        prompt = f"""
You are the ELITE INTEGRITY AUDITOR. Cross-reference behavioral and code analysis reports.

**VISUAL PROCTOR FINDINGS:**
{visual_report}

**CODE REVIEWER FINDINGS:**
{code_report}

**CRITICAL CORRELATION TASK:**
Confirm if technical milestones in the code align with the candidate's presence and engagement.
- Flag if 'Sudden Logic' occurred while the user was 'Gaze Averted' or 'Face Missing'.

**OUTPUT FORMAT:**
- AUDIT STATUS: [PASS/FAIL/INVESTIGATION]
- CONFIDENCE SCORE: [0.0 - 1.0]
- DISCREPANCIES: [List any mismatched events with timestamps]
- REASONING: [Brief explanation]
"""
        return self.generate_response(prompt)
