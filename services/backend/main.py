from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from ai_grader import AIGrader
from proctor import ProctorEngine
from rag.rag_manager import RagManager
from package_processor import PackageProcessor
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="Exam-Flow AI Backend")

# Initialize AI Services
api_key = os.getenv("GOOGLE_API_KEY")
grader = AIGrader(api_key) if api_key else None
proctor = ProctorEngine()
rag_manager = RagManager()

class SolutionPackage(BaseModel):
    solution_id: str
    code: str
    context: str
    category: str = "General"

@app.post("/library/upload")
async def upload_to_library(package: SolutionPackage):
    """Adds a gold-standard solution to the RAG library."""
    try:
        rag_manager.add_solution(
            solution_id=package.solution_id,
            code=package.code,
            context=package.context,
            metadata={"category": package.category}
        )
        return {"status": "success", "message": f"Solution {package.solution_id} added to library."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cache/clear")
async def clear_analysis_cache(item_id: str = None):
    """Wipes the analysis cache (full or specific item)."""
    try:
        rag_manager.clear_cache(item_id)
        msg = f"Cache item {item_id} cleared." if item_id else "All cache cleared."
        return {"status": "success", "message": msg}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cache/list")
async def list_cache():
    """Lists all cached analyses."""
    return rag_manager.list_cache()

@app.get("/cache/get")
async def get_cache_item(item_id: str):
    """Retrieves a specific cached report by its hash ID."""
    cached = rag_manager.get_cached_report(item_id)
    if not cached:
        raise HTTPException(status_code=404, detail="Cache item not found")
    return cached

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Exam-Flow Backend is running", "status": "online"}

@app.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):
    # Save the file locally first
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
        
    return {"filename": file.filename, "status": "received", "path": file_path}

@app.get("/analyze-demo/{demo_type}")
async def analyze_demo(demo_type: str):
    """
    Analyzes one of the local demo videos.
    """
    if not grader:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY not configured")

    if os.path.exists("/project_root"):
        project_root = "/project_root"
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
    
    rubrics = {
        "java": "1. Correct Java Syntax. 2. Implementation of a recursive factorial. 3. Successful execution in console.",
        "docker": "1. Use of basic Docker commands (ps, start, stop). 2. Correct Container ID usage. 3. Successful container lifecycle management.",
        "python": "1. Correct Python 3 syntax. 2. Use of PEP 8 naming conventions. 3. Proper use of functions or classes.",
        "general": "1. Logical problem solving. 2. Code readability and comments. 3. Final output accuracy."
    }

    if demo_type == "java":
        video_path = os.path.join(project_root, "Java_Demo_Exam-Flow.mp4")
    elif demo_type == "docker":
        video_path = os.path.join(project_root, "docker_demo-Exam-Flow.mp4")
    else:
        raise HTTPException(status_code=400, detail="Invalid demo type")

    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail=f"Video not found at {video_path}")

    behavioral_flags = proctor.analyze_behavior(video_path)
    report = await grader.grade_video(video_path, rubrics.get(demo_type, rubrics["general"]), behavioral_flags=behavioral_flags)

    return {
        "demo": demo_type,
        "report": report,
        "behavioral_flags": behavioral_flags
    }

@app.post("/analyze-video")
async def analyze_video_v2(
    assessment_type: str, 
    custom_rubric: str = None, 
    enable_proctoring: bool = True,
    file: UploadFile = File(...)
):
    """
    Analyzes an uploaded video based on the selected assessment type and optional custom rubric.
    """
    if not grader:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY not configured")

    # Save the file locally
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # Use custom rubric if provided, otherwise fallback to defaults
    rubric = custom_rubric
    if not rubric or rubric.strip() == "" or "Enter your custom" in rubric:
        rubrics = {
            "Java": "1. Correct Java Syntax. 2. Logical implementation. 3. Execution output.",
            "Docker": "1. Proper CLI usage. 2. Container management. 3. Dockerfile best practices.",
            "Python": "1. Python 3.x compatibility. 2. Idiomatic code (List comprehensions, proper imports). 3. Error handling.",
            "General": "1. Overall code structure. 2. Clarity and comments. 3. Problem solving approach."
        }
        rubric = rubrics.get(assessment_type, rubrics["General"])

    # Run Analysis
    try:
        behavioral_flags = []
        if enable_proctoring:
            behavioral_flags = proctor.analyze_behavior(file_path)
        
        # Grade with CV flags if enabled, otherwise just grade the video
        report = await grader.grade_video(file_path, rubric, behavioral_flags=behavioral_flags if enable_proctoring else None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "type": assessment_type,
        "report": report,
        "behavioral_flags": behavioral_flags,
        "proctoring_enabled": enable_proctoring
    }

@app.post("/analyze-package")
async def analyze_package(
    assessment_type: str,
    custom_rubric: str = None,
    enable_proctoring: bool = True,
    file: UploadFile = File(...)
):
    """
    Analyzes a ZIP package containing video, code, and context.
    """
    if not grader:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY not configured")

    # Save ZIP locally
    upload_dir = "uploads"
    package_dir = os.path.join(upload_dir, "extracted_" + file.filename.replace(".", "_"))
    os.makedirs(upload_dir, exist_ok=True)
    zip_path = os.path.join(upload_dir, file.filename)
    
    with open(zip_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    try:
        # Process Package
        package_info = PackageProcessor.process_zip(zip_path, package_dir)
        print(f"📦 Extracted Package Info: {package_info}")
        
        source_code = PackageProcessor.read_file(package_info["code"])
        context = PackageProcessor.read_file(package_info["context"])
        
        # Combine contextual info into rubric if needed
        # Combine contextual info: UI Text Area + File Context
        rubric_parts = []
        if custom_rubric and custom_rubric.strip():
            rubric_parts.append(f"INSTRUCTOR GUIDELINES:\n{custom_rubric}")
        
        if context and context.strip():
            rubric_parts.append(f"PROJECT README/CONTEXT:\n{context}")
            
        rubric = "\n\n".join(rubric_parts) if rubric_parts else "Standard Technical Assessment"
        
        # --- NEW: Phase 2 Analysis Caching ---
        import hashlib
        # Combine file content, rubric, and proctoring setting into a unique hash
        hash_obj = hashlib.md5()
        hash_obj.update(content)
        hash_obj.update(str(rubric).encode())
        hash_obj.update(str(enable_proctoring).encode())
        file_hash = hash_obj.hexdigest()
        
        cached_result = rag_manager.get_cached_report(file_hash)
        if cached_result:
            print(f"💎 CACHE HIT: Returning pre-analyzed report for {file_hash}")
            cached_result["source"] = "Cached Research Result"
            return cached_result

        # Run Analysis (If not cached)
        behavioral_flags = []
        video_path = package_info["video"]
        print(f"🎥 Video Path for Proctoring: {video_path}")
        
        if video_path and enable_proctoring:
            behavioral_flags = proctor.analyze_behavior(video_path)
        
        # Grade with all multi-modal context
        report = await grader.grade_video(
            video_path=video_path, 
            rubric=rubric, 
            behavioral_flags=behavioral_flags,
            source_code=source_code
        )
        
        # --- NEW: Integrity Guard (Don't cache if all models failed) ---
        if "ERROR: All models failed" in report or "# ❌ API Request Failed" in report:
            print("⚠️ System Failure detected. Returning raw error and skipping cache.")
            return {
                "type": assessment_type,
                "report": report,
                "behavioral_flags": [],
                "source": "System Error (No Cache)"
            }
        
        final_response = {
            "type": assessment_type,
            "report": report,
            "behavioral_flags": behavioral_flags,
            "has_code": bool(source_code),
            "has_video": bool(video_path),
            "source": "Agentic Analysis (Fresh)",
            "filename": file.filename
        }

        # Save to Cache for next time
        rag_manager.cache_report(file_hash, final_response)
        
        # Cleanup
        PackageProcessor.cleanup(package_dir)
        
        return final_response

    except Exception as e:
        PackageProcessor.cleanup(package_dir)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
