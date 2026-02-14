from .base_agent import BaseAgent
from typing import Dict, Any

class VisualProctorAgent(BaseAgent):
    """Agent C: The Visual Proctor. Analyzes behavioral logs and video context."""
    
    def run(self, input_data: Dict[str, Any]) -> str:
        cv_context = input_data.get("cv_context", "No behavioral data provided.")
        
        prompt = f"""
You are the VISUAL PROCTOR AGENT. Your role is to examine behavioral data detected by Computer Vision.

**BEHAVIORAL DATA:**
{cv_context}

**TASKS:**
1. Identify specific timestamps where anomalous behavior occurred (gaze aversion, face missing, etc).
2. Rate the intensity of these anomalies (Low, Medium, High).
3. Provide a 'Visual Integrity Verdict'.

**OUTPUT FORMAT:**
- VERDICT: [CLEAR/SUSPICIOUS/CRITICAL]
- ANOMALY LOG: [MM:SS - Type - Intensity]
- REASONING: [Brief explanation]
"""
        return self.generate_response(prompt)
