import google.generativeai as genai
from typing import List, Any, Dict
import os
import time
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

class BaseAgent:
    """Base class for all Phase 2 agents with robust retry logic."""
    def __init__(self, model_name: str = 'models/gemini-flash-latest'):
        self.model_name = model_name
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=30),
        stop=stop_after_attempt(5),
        reraise=True
    )
    def generate_response(self, prompt: str) -> str:
        """Helper method to generate response with retries."""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"⚠️ Agent API Error: {str(e)}")
            raise e

    def run(self, input_data: Dict[str, Any]) -> str:
        raise NotImplementedError("Subclasses must implement run()")

    def get_confidence_score(self) -> float:
        return 0.9
