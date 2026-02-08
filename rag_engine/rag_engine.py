# rag_engine/rag_engine.py
from rag_engine.vector_store import VectorStore


class GhostRAG:
    def __init__(self, dataset_id: str = "user_upload"):
        self.dataset_id = dataset_id
        self.store = VectorStore()

    def search(self, query: str, top_k: int = 5):
        return self.store.search(
            query=query,
            top_k=top_k,
            dataset_id=self.dataset_id
        )
