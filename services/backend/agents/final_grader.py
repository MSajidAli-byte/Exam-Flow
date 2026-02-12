from .base_agent import BaseAgent
from typing import Dict, Any

class FinalGraderAgent(BaseAgent):
    """Agent D: The Final Grader. Synthesizes all data into a final report."""
    
    def run(self, input_data: Dict[str, Any]) -> str:
        audit_report = input_data.get("audit_report", "")
        code_score = input_data.get("code_score", "0")
        
        prompt = f"""
You are the CHIEF ASSESSMENT AI. Your role is to produce the final academic verdict.

**INTEGRITY AUDIT REPORT:**
{audit_report}

**PRELIMINARY TECHNICAL SCORE:**
{code_score}

**TASKS:**
1. Determine the final score. 
2. **IMPORTANT**: If the Audit Report shows a FAIL, the maximum score allowed is 20/100, regardless of technical quality.
3. Write a professional executive summary for the professor/instructor.

**OUTPUT FORMAT:**
- FINAL GRADE: [X/100]
- STATUS: [Certified/Flagged/Failed]
- EXECUTIVE SUMMARY: [Professional narrative]
"""
        response = self.model.generate_content(prompt)
        return response.text
