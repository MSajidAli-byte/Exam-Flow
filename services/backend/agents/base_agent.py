import google.generativeai as genai
from typing import List, Any, Dict
import os
import time

class BaseAgent:
    """Base class for all Phase 2 agents with intelligent multi-model fallback."""
    
    # Priority order based on ACTUAL available models and quota limits
    # Strategy: Use stable 2.5/2.0 models, avoid experimental variants
    MODEL_FALLBACK_ORDER = [
        'models/gemini-2.5-flash',        # Primary: Latest stable, 161K TPM, 2/5 RPM (from screenshot)
        'models/gemini-2.0-flash',        # Fallback 1: Unlimited TPM, 0/15 RPD (fresh quota)
        'models/gemini-flash-latest',     # Fallback 2: Alias to stable flash (48K TPM)
        'models/gemini-2.5-pro',          # Fallback 3: Unlimited TPM, high reasoning
        'models/gemini-pro-latest',       # Fallback 4: Stable pro alias
        'models/gemini-2.0-flash-lite',   # Fallback 5: Lightweight, unlimited TPM
    ]
    
    def __init__(self, model_name: str = None):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)
        self.current_model_index = 0
        self.model_name = model_name or self.MODEL_FALLBACK_ORDER[0]
        self.model = genai.GenerativeModel(self.model_name)

    def generate_response(self, prompt: str) -> str:
        """Generate response with automatic model fallback on quota errors."""
        for attempt, model_name in enumerate(self.MODEL_FALLBACK_ORDER):
            try:
                # Switch to next model in fallback chain
                if attempt > 0:
                    print(f"🔄 Switching to fallback model: {model_name}")
                    self.model = genai.GenerativeModel(model_name)
                    self.model_name = model_name
                
                response = self.model.generate_content(prompt)
                
                # Success! Log which model worked
                if attempt > 0:
                    print(f"✅ Success with {model_name}")
                
                return response.text
                
            except Exception as e:
                error_message = str(e)
                
                # Check if this is a quota error
                if "429" in error_message or "quota" in error_message.lower():
                    print(f"🛑 Quota exceeded for {model_name}")
                    
                    # If this was the last model, return error
                    if attempt == len(self.MODEL_FALLBACK_ORDER) - 1:
                        return f"ERROR: All models exhausted. Please wait 60 seconds and try again."
                    
                    # Otherwise, continue to next model
                    time.sleep(2)  # Brief pause before trying next model
                    continue
                
                # For non-quota errors, try next model but log the error
                print(f"⚠️ Error with {model_name}: {error_message[:100]}")
                
                if attempt == len(self.MODEL_FALLBACK_ORDER) - 1:
                    return f"ERROR: All models failed. Last error: {error_message[:200]}"
                
                time.sleep(1)
                continue
        
        return "ERROR: Unexpected fallback loop termination."

    def run(self, input_data: Dict[str, Any]) -> str:
        raise NotImplementedError("Subclasses must implement run()")

    def get_confidence_score(self) -> float:
        return 0.9
