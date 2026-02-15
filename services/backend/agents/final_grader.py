from .base_agent import BaseAgent
from typing import Dict, Any

class FinalGraderAgent(BaseAgent):
    """Agent D: The Final Grader. Synthesizes all data into a final report."""
    
    def run(self, input_data: Dict[str, Any]) -> str:
        audit_report = input_data.get("audit_report", "")
        code_report = input_data.get("code_report", "No technical analysis provided.")
        
        prompt = f"""
You are the CHIEF ASSESSMENT AI. Your role is to produce the final academic verdict.

**INTEGRITY AUDIT REPORT:**
{audit_report}

**PRELIMINARY TECHNICAL REPORT:**
{code_report}

**TASKS:**
1. Extract the Technical Score from the Preliminary Report.
2. Determine the Final Grade based on Integrity Audit + Technical Score.
3. **IMPORTANT**: If the Audit Report shows a FAIL, the maximum score allowed is 20/100.
4. Write a professional executive summary for the professor/instructor.

**OUTPUT FORMAT:**
- FINAL GRADE: [X/100]
- STATUS: [Certified/Flagged/Failed]
- EXECUTIVE SUMMARY: [Professional narrative]
"""
        return self.generate_response(prompt)
