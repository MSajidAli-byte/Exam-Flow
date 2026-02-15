import zipfile
import os
import shutil
from typing import Dict, Any

class PackageProcessor:
    """Processes uploaded ZIP packages containing video, code, and context."""
    
    @staticmethod
    def process_zip(zip_path: str, extract_dir: str) -> Dict[str, Any]:
        """Extracts ZIP and returns paths to key files (recursively searching)."""
        os.makedirs(extract_dir, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            
        result = {
            "video": None,
            "code": [],  # Changed to list to support multiple files
            "context": None
        }
        
        # Recursively walk to find files even if nested in folders
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                file_path = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()
                
                # Check for Video
                if ext in ['.mp4', '.webm', '.mov', '.avi', '.mkv', '.flv']:
                    if not result["video"]:
                        result["video"] = file_path
                
                # Check for Code or Context
                elif ext in ['.java', '.py', '.js', '.yaml', '.yml', '.txt', '.md', '.c', '.cpp', '.cs', '.h', '.ts', '.go']:
                    is_context = 'context' in file.lower() or 'instruction' in file.lower() or 'readme' in file.lower()
                    
                    if is_context:
                         # Keep only one primary context file to avoid confusion, or could list them too.
                         # For now, prioritize README/Instructions.
                         if not result["context"]:
                             result["context"] = file_path
                    elif ext not in ['.txt', '.md']:
                         # It's a code file! Add to list.
                         result["code"].append(file_path)

        # Final pass: If no context found, check .txt files again
        if not result["context"]:
             for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    ext = os.path.splitext(file)[1].lower()
                    if ext == '.txt' and file_path not in result["code"]:
                        result["context"] = file_path
                        break

        return result

    @staticmethod
    def read_file(file_path_or_list: Any) -> str:
        """Reads content from a single file path or a list of paths."""
        if not file_path_or_list:
            return ""
            
        # Handle list of files (concatenation)
        if isinstance(file_path_or_list, list):
            combined_content = ""
            for path in file_path_or_list:
                if os.path.exists(path):
                    filename = os.path.basename(path)
                    content = ""
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    combined_content += f"\n\n--- FILE: {filename} ---\n{content}"
            return combined_content.strip()

        # Handle single file path
        if not os.path.exists(file_path_or_list):
            return ""
        with open(file_path_or_list, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()

    @staticmethod
    def cleanup(extract_dir: str):
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
