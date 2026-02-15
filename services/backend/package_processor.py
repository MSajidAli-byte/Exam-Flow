import zipfile
import os
import shutil
from typing import Dict, Any

class PackageProcessor:
    """Processes uploaded ZIP packages containing video, code, and context."""
    
    @staticmethod
    def process_zip(zip_path: str, extract_dir: str) -> Dict[str, str]:
        """Extracts ZIP and returns paths to key files (recursively searching)."""
        os.makedirs(extract_dir, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            
        result = {
            "video": None,
            "code": None,
            "context": None
        }
        
        # Recursively walk to find files even if nested in folders
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                file_path = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()
                
                # Check for Video
                if ext in ['.mp4', '.webm', '.mov', '.avi', '.mkv', '.flv']:
                    # Prioritize video if multiple found, or just take first
                    if not result["video"]:
                        result["video"] = file_path
                
                # Check for Code or Context
                elif ext in ['.java', '.py', '.js', '.yaml', '.yml', '.txt', '.md', '.c', '.cpp', '.cs']:
                    # Explicit context identification
                    if 'context' in file.lower() or 'instruction' in file.lower() or 'readme' in file.lower():
                        result["context"] = file_path
                    # Code identification (avoid overwriting if we already found a 'better' code file)
                    elif ext not in ['.txt', '.md']:
                        result["code"] = file_path
                    # Fallback for text files if no code found yet
                    elif not result["code"] and not result["context"]:
                        # Could be code in .txt? Rare but possible
                        pass
        
        # Final pass: If we found code but no context, and have a .txt left over, use it as context
        if result["code"] and not result["context"]:
             for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    ext = os.path.splitext(file)[1].lower()
                    if ext == '.txt' and file_path != result["code"]:
                        result["context"] = file_path
                        break

        return result

    @staticmethod
    def read_file(file_path: str) -> str:
        if not file_path or not os.path.exists(file_path):
            return ""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()

    @staticmethod
    def cleanup(extract_dir: str):
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
