from .base_agent import BaseAgent
from typing import Dict, Any

class CodeReviewerAgent(BaseAgent):
    """Agent B: The Code Reviewer. Analyzes source code for technical logic."""
    
    def run(self, input_data: Dict[str, Any]) -> str:
        source_code = input_data.get("source_code", "No source code provided.")
        rubric = input_data.get("rubric", "Standard Assessment")
        
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
