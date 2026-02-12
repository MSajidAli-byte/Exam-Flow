import chromadb
from chromadb.utils import embedding_functions
import os
from typing import List, Dict, Any

class RagManager:
    """Manages the Ideal Answer Library using ChromaDB."""
    def __init__(self, persist_directory: str = "chroma_db"):
        self.persist_directory = persist_directory
        self.api_key = os.getenv("GOOGLE_API_KEY")
        
        # Use Google Embeddings to avoid local model download timeouts
        self.embedding_fn = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
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
