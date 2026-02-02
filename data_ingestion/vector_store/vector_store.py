import os
import json
import numpy as np
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer


class VectorStore:
    def __init__(
        self,
        index_path="data_ingestion/faiss.index",
        meta_path="data_ingestion/vector_metadata.json",
        text_path="data_ingestion/vector_texts.json",
    ):
        self.index_path = index_path
        self.meta_path = meta_path
        self.text_path = text_path

        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.texts = []
        self.metadata = []
        self.index = None

    # ---------------- ADD DOC ----------------
    def add_document(self, text, meta):
        self.texts.append(text)
        self.metadata.append(meta)

    # ---------------- BUILD ----------------
    def build(self):
        if not self.texts:
            raise ValueError("No documents to vectorize")

        vectors = self.vectorizer.fit_transform(self.texts).toarray()
        dim = vectors.shape[1]

        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(vectors).astype("float32"))

        print(f"✅ FAISS index built with {self.index.ntotal} vectors")

    # ---------------- SAVE ----------------
    def save(self):
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)

        faiss.write_index(self.index, self.index_path)

        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2)

        with open(self.text_path, "w", encoding="utf-8") as f:
            json.dump(self.texts, f)

        print("✅ FAISS index & metadata saved")

    # ---------------- LOAD ----------------
    def load(self):
        if not os.path.exists(self.index_path):
            raise FileNotFoundError("❌ FAISS index not found. Run ingestion first.")

        self.index = faiss.read_index(self.index_path)

        with open(self.meta_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        with open(self.text_path, "r", encoding="utf-8") as f:
            self.texts = json.load(f)

        # rebuild vectorizer vocab
        self.vectorizer.fit(self.texts)

        print(f"✅ Loaded FAISS index ({self.index.ntotal} vectors)")

    # ---------------- SEARCH ----------------
    def search(self, query, top_k=3):
        q_vec = self.vectorizer.transform([query]).toarray().astype("float32")
        distances, indices = self.index.search(q_vec, top_k)

        results = []
        for i, idx in enumerate(indices[0]):
            results.append({
                "score": float(distances[0][i]),
                "text": self.texts[idx][:300],
                "metadata": self.metadata[idx]
            })

        return results

    # ---------------- DATASET VIEW ----------------
    def list_datasets(self):
        datasets = {}

        for meta in self.metadata:
            name = meta["file"]
            datasets.setdefault(name, {
                "version": meta["version"],
                "deprecated": meta["deprecated"],
                "doc_type": meta["doc_type"],
                "count": 0
            })
            datasets[name]["count"] += 1

        return datasets
