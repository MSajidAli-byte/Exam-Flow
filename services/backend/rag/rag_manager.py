import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
import numpy as np
import os
from typing import List, Dict, Any

class GeminiEmbeddingFunction(EmbeddingFunction[Documents]):
    """Custom ChromaDB Embedding Function using Google Generative AI embeddings."""
    def __init__(self, api_key: str, model_name: str = "models/gemini-embedding-001"):
        import google.generativeai as genai
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=self.api_key)
        self._genai = genai

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for text in input:
            res = self._genai.embed_content(
                model=self.model_name,
                content=text,
                task_type="RETRIEVAL_DOCUMENT"
            )
            embeddings.append(np.array(res["embedding"], dtype=np.float32))
        return embeddings

    @staticmethod
    def name() -> str:
        return "custom_gemini_embedding"

class RagManager:
    """Manages the Ideal Answer Library using ChromaDB."""
    def __init__(self, persist_directory: str = "chroma_db"):
        self.persist_directory = persist_directory
        self.api_key = os.getenv("GOOGLE_API_KEY")
        
        # Use Custom Google Embeddings to avoid local model download timeouts & ChromaDB client_options incompatibility
        self.embedding_fn = GeminiEmbeddingFunction(
            api_key=self.api_key,
            model_name="models/gemini-embedding-001"
        )
        
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        try:
            self.collection = self.client.get_or_create_collection(
                name="ideal_solutions",
                embedding_function=self.embedding_fn,
                metadata={"description": "Collection of gold-standard exam solutions"}
            )
            # NEW: Global Cache Collection (Phase 2 Optimization)
            self.cache_collection = self.client.get_or_create_collection(
                name="analysis_cache",
                # No embedding needed here as we use exact hash lookup
                metadata={"description": "Hash-based cache for past reports"}
            )
        except ValueError as e:
            # Handle conflict between 'default' and 'google_generative_ai' embedding functions
            if "conflict" in str(e).lower():
                print("⚠️ Embedding function conflict detected. Resetting 'ideal_solutions' collection...")
                self.client.delete_collection("ideal_solutions")
                self.collection = self.client.create_collection(
                    name="ideal_solutions",
                    embedding_function=self.embedding_fn,
                    metadata={"description": "Collection of gold-standard exam solutions (Reset for Gemini Embeddings)"}
                )
                self.cache_collection = self.client.get_or_create_collection(name="analysis_cache")
            else:
                raise e

    def add_solution(self, solution_id: str, code: str, context: str, metadata: Dict[str, Any] = None):
        """Adds a new ideal solution to the library."""
        self.collection.add(
            documents=[f"Context: {context}\nCode: {code}"],
            metadatas=[metadata or {}],
            ids=[solution_id]
        )
        print(f"Added solution {solution_id} to library.")

    def query_solutions(self, query_text: str, n_results: int = 1) -> Dict[str, Any]:
        """Queries the library for the most similar ideal solutions."""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results

    def get_grading_context(self, student_code: str) -> str:
        """Retrieves and formats the ideal solution context for the grader."""
        results = self.query_solutions(student_code)
        if not results['documents'] or not results['documents'][0]:
            return "No ideal solution found for comparison."
        
        ideal_doc = results['documents'][0][0]
        return f"**IDEAL REFERENCE SOLUTION:**\n{ideal_doc}"

    # --- NEW: CACHING LOGIC ---
    def get_cached_report(self, file_hash: str) -> Dict[str, Any]:
        """Checks if an analysis for this exact file/rubric hash already exists."""
        try:
            result = self.cache_collection.get(ids=[file_hash])
            if result and result['metadatas']:
                import json
                return json.loads(result['metadatas'][0]['report_data'])
        except Exception as e:
            print(f"⚠️ Cache miss or error: {e}")
        return None

    def cache_report(self, file_hash: str, report_data: Dict[str, Any]):
        """Saves a finished report to the cache collection."""
        try:
            import json
            # CRITICAL: Do not cache if the report indicates an API/System error
            report_text = report_data.get("report", "")
            if "ERROR:" in report_text or "Quota exceeded" in report_text or "# ❌" in report_text:
                print(f"⚠️ Skipping cache for report containing errors (Hash: {file_hash})")
                return

            # Pass explicit dummy vector to prevent ChromaDB DefaultEmbeddingFunction ONNX model download/inference timeouts
            dummy_vector = [0.0] * 384
            self.cache_collection.upsert(
                ids=[file_hash],
                embeddings=[dummy_vector],
                documents=[f"Report for hash {file_hash}"],
                metadatas=[{"report_data": json.dumps(report_data)}]
            )
            print(f"✅ Report cached successfully (Hash: {file_hash})")
        except Exception as e:
            print(f"⚠️ Failed to cache report: {e}")

    def clear_cache(self, item_id: str = None):
        """Wipes the entire cache OR a specific item if item_id is provided."""
        try:
            if item_id:
                self.cache_collection.delete(ids=[item_id])
                print(f"🗑️ Specific cache item {item_id} cleared.")
            else:
                self.client.delete_collection("analysis_cache")
                self.cache_collection = self.client.get_or_create_collection(
                    name="analysis_cache",
                    metadata={"description": "Hash-based cache for past reports"}
                )
                print("🗑️ Entire analysis cache cleared.")
        except Exception as e:
            print(f"⚠️ Failed to clear cache: {e}")

    def list_cache(self) -> List[Dict[str, Any]]:
        """Returns a list of all items currently in the analysis cache."""
        try:
            results = self.cache_collection.get()
            cached_items = []
            for i in range(len(results['ids'])):
                import json
                report_data = json.loads(results['metadatas'][i]['report_data'])
                cached_items.append({
                    "id": results['ids'][i],
                    "type": report_data.get("type", "Unknown"),
                    "filename": report_data.get("filename", "N/A"),
                    "source": report_data.get("source", "Unknown"),
                    # Add a snippet of the report to help identify it
                    "preview": report_data.get("report", "")[:100] + "..."
                })
            return cached_items
        except Exception as e:
            print(f"⚠️ Failed to list cache: {e}")
            return []
