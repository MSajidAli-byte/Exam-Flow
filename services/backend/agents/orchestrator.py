from typing import Dict, Any
from .visual_proctor import VisualProctorAgent
from .code_reviewer import CodeReviewerAgent
from .integrity_auditor import IntegrityAuditorAgent
from .final_grader import FinalGraderAgent
from rag.rag_manager import RagManager
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
        # Step 1: Retrieval (RAG)
        print("📚 Retrieving ideal solution context...")
        ideal_context = self.rag_manager.get_grading_context(source_code)
        
        # Step 2: Parallel Analysis
        print("🚀 Agent B & C starting analysis...")
        
        visual_report = self.visual_proctor.run(video_data)
        code_report = self.code_reviewer.run({
            "source_code": source_code,
            "rubric": f"{rubric}\n\n{ideal_context}"
        })
        
        # Step 3: Cross-Reference (Integrity Auditor)
        print("🔍 Agent C performing integrity audit...")
        audit_report = self.integrity_auditor.run({
            "visual_report": visual_report,
            "code_report": code_report
        })
        
        # Step 4: Final Synthesis (Final Grader)
        print("🏆 Agent D generating final verdict...")
        final_report = self.final_grader.run({
            "audit_report": audit_report,
            "code_score": "See code report" # Simplification for now
        })
        
        return final_report
