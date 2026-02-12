import google.generativeai as genai
from typing import List, Any, Dict
import os

class BaseAgent:
    """Base class for all Phase 2 agents."""
    def __init__(self, model_name: str = 'gemini-1.5-flash-latest'):
        self.model_name = model_name
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    def run(self, input_data: Dict[str, Any]) -> str:
        raise NotImplementedError("Subclasses must implement run()")

    def get_confidence_score(self) -> float:
        # Placeholder for research-first design: Confidence scoring
        return 0.9
