# rag_engine/rag_engine.py
from pathlib import Path
import json
import numpy as np
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Dict, Optional


class GhostRAG:
    """Role 4 core: RAG retrieval + metadata access."""

    def __init__(self, data_dir: str = "data_ingestion"):
        self.data_dir = Path(data_dir)
        self.index_path = self.data_dir / "faiss.index"
        self.meta_path = self.data_dir / "vector_metadata.json"
        self.text_path = self.data_dir / "vector_texts.json"

        self.vectorizer = TfidfVectorizer(stop_words="english", max_features=2048)
        self.texts: List[str] = []
        self.metadata: List[Dict] = []
        self.index: Optional[faiss.Index] = None
        self._loaded = False

    def load(self) -> None:
        """Load index + metadata from disk."""
        if self._loaded:
            return

        if not self.index_path.exists():
            raise FileNotFoundError(
                "❌ Run `python data_ingestion/run_metadata.py` first to build the index."
            )

        self.index = faiss.read_index(str(self.index_path))

        with open(self.meta_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        with open(self.text_path, "r", encoding="utf-8") as f:
            self.texts = json.load(f)

        # Rebuild vectorizer vocab
        self.vectorizer.fit(self.texts)
        self._loaded = True
        print(f"✅ Loaded {self.index.ntotal} vectors")

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Semantic search + metadata."""
        if not self._loaded:
            self.load()

        q_vec = self.vectorizer.transform([query]).toarray().astype("float32")
        distances, indices = self.index.search(q_vec, top_k)

        results = []
        for i, idx in enumerate(indices[0]):
            meta = self.metadata[idx]
            results.append(
                {
                    "rank": i + 1,
                    "score": float(distances[0][i]),
                    "file": meta["file"],
                    "version": meta["version"],
                    "deprecated": meta["deprecated"],
                    "doc_type": meta["doc_type"],
                    "snippet": self.texts[idx][:250] + "...",
                    "path": meta["path"],
                }
            )
        return results
