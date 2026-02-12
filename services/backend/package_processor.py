import zipfile
import os
import shutil
from typing import Dict, Any

class PackageProcessor:
    """Processes uploaded ZIP packages containing video, code, and context."""
    
    @staticmethod
    def process_zip(zip_path: str, extract_dir: str) -> Dict[str, str]:
        """Extracts ZIP and returns paths to key files."""
        os.makedirs(extract_dir, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            
        files = os.listdir(extract_dir)
        result = {
            "video": None,
            "code": None,
            "context": None
        }
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in ['.mp4', '.webm', '.mov', '.avi', '.mkv', '.flv']:
                result["video"] = os.path.join(extract_dir, file)
            elif ext in ['.java', '.py', '.js', '.yaml', '.yml', '.txt']:
                # For now, we assume .txt without 'context' in name is code, 
                # or we just grab the first one.
                if 'context' in file.lower():
                    result["context"] = os.path.join(extract_dir, file)
                else:
                    result["code"] = os.path.join(extract_dir, file)
                    
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
