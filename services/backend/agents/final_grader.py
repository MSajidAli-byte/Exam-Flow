from .base_agent import BaseAgent
from typing import Dict, Any

class FinalGraderAgent(BaseAgent):
    """Agent D: The Final Grader. Synthesizes all data into a final report."""
    
    def run(self, input_data: Dict[str, Any]) -> str:
        audit_report = input_data.get("audit_report", "")
        code_report = input_data.get("code_report", "No technical analysis provided.")
        
        prompt = f"""
You are the CHIEF ASSESSMENT AI (EXAM-FLOW SENIOR ARCHITECT). Your role is to produce the final academic verdict based on a complex multi-agent analysis.

**INPUT DATA FOR SYNTHESIS:**
1. **INTEGRITY AUDIT REPORT:**
{audit_report}

2. **PRELIMINARY TECHNICAL REPORT:**
{code_report}

**YOUR MISSION:**
Synthesize these disparate reports into a SINGLE, high-fidelity, and professional "EXAM-FLOW ASSESSMENT INTELLIGENCE" document. This report is for professors and must look technical and trustworthy.

**REQUIRED OUTPUT STRUCTURE & FORMAT (Follow EXACTLY):**

# Exam-Flow Assessment Intelligence
**Assessment Details:** [Subject From Rubric] | **System Instance:** Agentic Multimodal (Phase 2)
---

## 📊 AI Technical Score
**SCORE:** [X/100]

---

## 🧐 INTEGRITY RECONNAISSANCE
**Verdict:** [PASS / FAIL / FLAGGED]
**Integrity Status:** [AI Default / Certified / Suspicious]
**Integrity Notes:** [Provide a high-level summary of the candidate's development process. Does it appear independent, or are there significant gaps?]

---

## ⏱️ CHRONOLOGICAL LOG & TIMESTAMPS
[Carefully combine the Code Reviewer's event list with the Visual Proctor's behavioral flags into a single, cohesive timeline.]
- 00:00 - ...
- 00:15 - [Event Description e.g., 'Candidate begins typing class structure']
- ...

---

## 📝 RUBRIC ASSESSMENT
[List the technical requirements from the rubric and how the student met them based on the Code Reviewer's analysis.]

---

## 🚨 BEHAVIORAL RED FLAGS
[Explicitly list any discrepancies, gaze aversion, sudden logic, or tab switching with timestamps and estimated severity.]
- [Timestamp] - [Flag Type] - [Severity (Low/Medium/High)] - [Context]

---

## 📄 FINAL VERDICT SCORE & JUSTIFICATION
**FINAL GRADE:** [X/100]
**STATUS:** [Certified / Flagged / Failed]
**EXECUTIVE SUMMARY:** [An exhaustive narrative explaining the final decision. Integrate findings from both technical and behavioral streams. **CRITICAL**: If the Integrity Audit is a FAIL or indicates FRAUD, the final grade MUST be capped at 20/100.]

---

**CRITICAL RULE:** Do NOT use simple summaries. Be as descriptive as the provided examples. The report should feel long and authoritative.
"""
        return self.generate_response(prompt)
