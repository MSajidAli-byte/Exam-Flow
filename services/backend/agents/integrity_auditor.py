from .base_agent import BaseAgent
from typing import Dict, Any

class IntegrityAuditorAgent(BaseAgent):
    """Agent C: The Integrity Auditor. Cross-references Visual and Code analysis."""
    
    def run(self, input_data: Dict[str, Any]) -> str:
        visual_report = input_data.get("visual_report", "")
        code_report = input_data.get("code_report", "")
        
        prompt = f"""
You are the ELITE INTEGRITY AUDITOR. Your role is to find correlations between physical behavior and digital work.

**VISUAL PROCTOR FINDINGS:**
{visual_report}

**CODE REVIEWER FINDINGS:**
{code_report}

**CRITICAL CORRELATION TASK:**
Confirm if technical milestones in the code align with the candidate's presence and engagement in the video.
- Flag if 'Sudden Logic' occurred while the user was 'Gaze Averted' or 'Face Missing'.

**OUTPUT FORMAT:**
- AUDIT STATUS: [PASS/FAIL/INVESTIGATION]
- CONFIDENCE SCORE: [0.0 - 1.0]
- DISCREPANCIES: [List any mismatched events with timestamps]
"""
        response = self.model.generate_content(prompt)
        return response.text
