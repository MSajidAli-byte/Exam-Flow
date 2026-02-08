"""
Script to list all available Gemini models and their capabilities.
Run this to see which models support video analysis.
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv
import sys

# Set encoding to UTF-8 for Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

load_dotenv()

# Configure API
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    # No emoji
    print("[ERROR] GOOGLE_API_KEY not found in .env file")
    sys.exit(1)

genai.configure(api_key=api_key)

print("=" * 80)
print("AVAILABLE GEMINI MODELS")
print("=" * 80)

try:
    # list_models is a generator, let's collect it
    print("Fetching models...")
    models = list(genai.list_models())
    
    video_models = []
    
    for model in models:
        # Check if model supports generateContent (required for our use case)
        if 'generateContent' in model.supported_generation_methods:
            print(f"\n[OK] {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Supported Methods: {', '.join(model.supported_generation_methods)}")
            
            # Check if it's likely to support video (flash/pro models typically do)
            if 'flash' in model.name.lower() or 'pro' in model.name.lower():
                video_models.append(model.name)
                print(f"   VIDEO SUPPORT: Likely (Flash/Pro model)")
    
    print("\n" + "=" * 80)
    print("RECOMMENDED MODELS FOR EXAM-FLOW (Video Analysis)")
    print("=" * 80)
    
    if video_models:
        for i, model_name in enumerate(video_models, 1):
            # The model names returned by list_models usually include 'models/' prefix
            # e.g. 'models/gemini-1.5-flash'
            print(f"{i}. {model_name}")
    else:
        print("[WARNING] No video-capable models found. Check your API key permissions.")
    
    print("\n" + "=" * 80)
    print("COPY THIS LIST TO ai_grader.py MODEL_FALLBACK_ORDER")
    print("=" * 80)
    
except Exception as e:
    print(f"[ERROR] Error listing models: {e}")
    print("\nTroubleshooting:")
    print("1. Check your GOOGLE_API_KEY in .env")
    print("2. Ensure you have internet connection")
    print("3. Verify your API key has proper permissions")
