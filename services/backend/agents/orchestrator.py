from typing import Dict, Any
from .visual_proctor import VisualProctorAgent
from .code_reviewer import CodeReviewerAgent
from .integrity_auditor import IntegrityAuditorAgent
from .final_grader import FinalGraderAgent
from rag.rag_manager import RagManager
import google.generativeai as genai
import os

class AgentOrchestrator:
    """Orchestrates the multi-agent workflow for Phase 2."""
    def __init__(self):
        # We use Gemini 1.5 Flash for speed/cost in agents
        self.visual_proctor = VisualProctorAgent()
        self.code_reviewer = CodeReviewerAgent()
        self.integrity_auditor = IntegrityAuditorAgent()
        self.final_grader = FinalGraderAgent()
        self.rag_manager = RagManager()

    async def run_analysis(self, video_data: Dict[str, Any], source_code: str, rubric: str) -> str:
        import time

        # Step 1: RAG Retrieval — fetch ideal solution context from ChromaDB
        print("📚 Retrieving ideal solution context from RAG...")
        ideal_context = self.rag_manager.get_grading_context(source_code)

        # Step 1.5: Upload video to Gemini Files API (shared across agents)
        # This restores Phase 1's screen-reading capability inside the agentic workflow.
        # All agents that need video get the same uploaded file object — no re-upload.
        gemini_video_file = None
        video_path = video_data.get("video_path")
        if video_path and os.path.exists(video_path):
            try:
                print(f"⬆️ Uploading video to Gemini Files API for screen-reading: {video_path}")
                gemini_video_file = genai.upload_file(video_path)
                # Wait for Gemini to process the video
                while gemini_video_file.state.name == "PROCESSING":
                    print(".", end="", flush=True)
                    time.sleep(2)
                    gemini_video_file = genai.get_file(gemini_video_file.name)
                if gemini_video_file.state.name != "ACTIVE":
                    print("⚠️ Video upload failed — falling back to text-only analysis.")
                    gemini_video_file = None
                else:
                    print("\n✅ Video active and ready for multimodal analysis.")
            except Exception as e:
                print(f"⚠️ Could not upload video to Gemini: {e}")
                gemini_video_file = None

        # Step 2: Visual Proctor — interprets OpenCV behavioral flags via LLM
        print("🚀 Agent A (Visual Proctor) starting analysis...")
        visual_report = self.visual_proctor.run(video_data)

        print("⏳ Rate limiting delay (10s)...")
        time.sleep(10)

        # Step 3: Code Reviewer — reads submitted code AND watches screen recording
        # Phase 2 superiority: Gemini cross-references what was SUBMITTED vs what was TYPED on screen
        print("🚀 Agent B (Code Reviewer) starting analysis...")
        code_report = self.code_reviewer.run({
            "source_code": source_code,
            "video_path": video_path,
            "gemini_video_file": gemini_video_file,  # Pass uploaded file directly
            "rubric": f"{rubric}\n\nIDEAL SOLUTION CONTEXT (from RAG library):\n{ideal_context}"
        })

        print("⏳ Rate limiting delay (10s)...")
        time.sleep(10)

        # Step 4: Integrity Auditor — cross-references video screen events with code report
        # This is the key Phase 2 feature: structured triangulation between all data sources
        print("🔍 Agent C (Integrity Auditor) performing audit...")
        audit_report = self.integrity_auditor.run({
            "visual_report": visual_report,
            "code_report": code_report,
            "gemini_video_file": gemini_video_file,  # Auditor also watches the screen
        })

        print("⏳ Rate limiting delay (10s)...")
        time.sleep(10)

        # Step 5: Final Grader — synthesizes all agent reports into one verdict
        print("🏆 Agent D (Final Grader) generating verdict...")
        final_report = self.final_grader.run({
            "visual_report": visual_report,
            "code_report": code_report,
            "audit_report": audit_report,
            "rubric": rubric
        })

        return final_report
