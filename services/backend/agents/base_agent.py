import google.generativeai as genai
from typing import List, Any, Dict
import os
import time

class BaseAgent:
    """Base class for all Phase 2 agents with intelligent multi-model fallback."""
    
    # Priority order based on ACTUAL available models and quota limits
    # Strategy: Use stable 2.5/2.0 models, avoid experimental variants
    MODEL_FALLBACK_ORDER = [
        'models/gemini-1.5-flash',
        'models/gemini-1.5-flash-latest',
        'models/gemini-2.0-flash-exp',
        'models/gemini-2.0-flash-001',
        'models/gemini-2.0-flash-lite-001',
        'models/gemini-2.5-flash',
        'models/gemini-2.5-flash-lite',
        'models/gemini-3-flash-preview'
    ]
    
    def __init__(self, model_name: str = None):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)
        self.current_model_index = 0
        self.model_name = model_name or self.MODEL_FALLBACK_ORDER[0]
        self.model = genai.GenerativeModel(self.model_name)

    def generate_response(self, prompt: Any) -> str:
        """Generate response with automatic model fallback on quota errors. Supports text or multimodal input."""
        attempted_errors = {}
        for attempt, model_name in enumerate(self.MODEL_FALLBACK_ORDER):
            try:
                if attempt > 0:
                    print(f"🔄 Switching to fallback model: {model_name}")
                    self.model = genai.GenerativeModel(model_name)
                    self.model_name = model_name
                
                response = self.model.generate_content(prompt)
                
                if attempt > 0:
                    print(f"✅ Success with {model_name}")
                
                return response.text
                
            except Exception as e:
                error_message = str(e)
                attempted_errors[model_name] = error_message
                
                if "429" in error_message or "quota" in error_message.lower() or "not found" in error_message.lower() or "supported" in error_message.lower():
                    print(f"🛑 Error/Quota exceeded for {model_name}: {error_message[:100]}")
                    if attempt == len(self.MODEL_FALLBACK_ORDER) - 1:
                        error_details = "\\n".join([f"- **{m}**: {t}" for m, t in attempted_errors.items()])
                        return f"ERROR: All models failed.\\n\\n**Details:**\\n{error_details}"
                    time.sleep(2)
                    continue
                
                print(f"⚠️ Error with {model_name}: {error_message[:100]}")
                if attempt == len(self.MODEL_FALLBACK_ORDER) - 1:
                    error_details = "\\n".join([f"- **{m}**: {t}" for m, t in attempted_errors.items()])
                    return f"ERROR: All models failed.\\n\\n**Details:**\\n{error_details}"
                time.sleep(1)
                continue

        
        return "ERROR: Unexpected fallback loop termination."

    def run(self, input_data: Dict[str, Any]) -> str:
        raise NotImplementedError("Subclasses must implement run()")

    def get_confidence_score(self) -> float:
        return 0.9
