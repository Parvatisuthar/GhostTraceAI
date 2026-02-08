# rag_engine/vector_store.py
import json
import faiss
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer

DATA_DIR = Path("data_ingestion")
INDEX_PATH = DATA_DIR / "faiss.index"
META_PATH = DATA_DIR / "vector_metadata.json"
TEXT_PATH = DATA_DIR / "vector_texts.json"


class VectorStore:
    def __init__(self):
        if not INDEX_PATH.exists():
            raise RuntimeError("FAISS index not found. Run ingestion first.")

        self.texts = json.load(open(TEXT_PATH, encoding="utf-8"))
        self.metadata = json.load(open(META_PATH, encoding="utf-8"))
        self.index = faiss.read_index(str(INDEX_PATH))

        self.vectorizer = TfidfVectorizer(stop_words="english", max_features=2048)
        self.vectorizer.fit(self.texts)

    def search(self, query: str, top_k: int = 5, dataset_id: str | None = None):
        q_vec = self.vectorizer.transform([query]).toarray().astype("float32")
        _, indices = self.index.search(q_vec, top_k * 3)

        results = []
        rank = 1

        for idx in indices[0]:
            meta = self.metadata[idx]

            if dataset_id and meta.get("dataset_id") != dataset_id:
                continue

            results.append({
                "rank": rank,
                "file": meta.get("file"),
                "version": meta.get("version", "unknown"),
                "deprecated": meta.get("deprecated", False),
                "doc_type": meta.get("doc_type", "general"),
            })

            rank += 1
            if len(results) >= top_k:
                break

        return results
