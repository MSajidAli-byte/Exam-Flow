from .base_agent import BaseAgent
from typing import Dict, Any

class VisualProctorAgent(BaseAgent):
    """Agent A: The Visual Proctor. Analyzes behavioral logs and video context."""
    
    def run(self, input_data: Dict[str, Any]) -> str:
        cv_context = input_data.get("cv_context", "No behavioral data provided.")
        gemini_video_file = input_data.get("gemini_video_file", None)
        
        system_instructions = """
You are the VISUAL BEHAVIOR EXPERT. Your role is to detect cheating by watching the candidate's physical actions and eye contact.

**INPUT SOURCES:**
1. **CV FORENSIC LOGS (from OpenCV):** 
{cv_context}
2. **RAW VIDEO (If provided):** You can see the candidate's actual face through the webcam feed (usually a small PIP or overlay).

**YOUR TASKS:**
1. **Validation**: Confirm if the OpenCV 'Gaze Aversion' or 'Face Missing' flags are true.
2. **Discovery**: Look for quick gaze shifts to the side (left/right of the screen) that OpenCV might have missed. 
3. **Speed Awareness**: The video might be recorded at high speed (2x). Pay attention to any consistent pattern of looking away, even if brief.
4. **Context**: Looking at the keyboard is usually normal. Looking 45 degrees away from the monitor consistently is a RED FLAG (external notes/phone).

**OUTPUT FORMAT:**
- VERDICT: [CLEAR/SUSPICIOUS/CRITICAL]
- ANOMALY LOG: [MM:SS - Type - Intensity]
- REASONING: [Explain exactly what you saw. "Candidate repeatedly looked to the left at X:XX"]
"""
        if gemini_video_file:
            return self.generate_response([gemini_video_file, system_instructions.format(cv_context=cv_context)])
        
        return self.generate_response(system_instructions.format(cv_context=cv_context))
