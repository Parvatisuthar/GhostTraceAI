# data_ingestion/upload_ingest.py
from pathlib import Path
import json
from typing import List, Dict
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer

DATA_DIR = Path("data_ingestion")
INDEX_PATH = DATA_DIR / "faiss.index"
META_PATH = DATA_DIR / "vector_metadata.json"
TEXT_PATH = DATA_DIR / "vector_texts.json"


def _load_store():
    with open(META_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    with open(TEXT_PATH, "r", encoding="utf-8") as f:
        texts = json.load(f)
    index = faiss.read_index(str(INDEX_PATH))
    return texts, metadata, index


def _save_store(texts, metadata, index):
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    with open(TEXT_PATH, "w", encoding="utf-8") as f:
        json.dump(texts, f, ensure_ascii=False, indent=2)
    faiss.write_index(index, str(INDEX_PATH))


def ingest_uploaded_files(
    contents: List[str],
    filenames: List[str],
    dataset_id: str = "user_upload",
):
    """
    Add uploaded text files into existing FAISS + metadata JSON.
    Each file becomes one or more chunks (simple split).
    """
    texts, metadata, index = _load_store()

    # Rebuild TF-IDF on existing texts + new ones
    vectorizer = TfidfVectorizer(stop_words="english", max_features=2048)
    all_texts = texts.copy()

    new_metadata = []
    snippet_map: Dict[str, str] = {}  # filename -> first chunk

    for file_content, name in zip(contents, filenames):
        chunks = [file_content[i:i + 400] for i in range(0, len(file_content), 400)]
        for chunk_idx, chunk in enumerate(chunks):
            if not chunk.strip():
                continue
            all_texts.append(chunk)
            meta = {
                "file": name,
                "version": "user",
                "deprecated": False,
                "doc_type": "uploaded",
                "path": f"uploaded/{name}",
                "dataset_id": dataset_id,
                "chunk_id": chunk_idx,
            }
            new_metadata.append(meta)
            # store first non-empty chunk as snippet for suggestions
            if name not in snippet_map:
                snippet_map[name] = chunk

    # Fit vectorizer on all texts (old + new)
    vectorizer.fit(all_texts)
    all_vecs = vectorizer.transform(all_texts).toarray().astype("float32")

    # Rebuild FAISS index from scratch (for simplicity)
    dim = all_vecs.shape[1]
    new_index = faiss.IndexFlatL2(dim)
    new_index.add(all_vecs)

    # Update store and save
    texts = all_texts
    metadata.extend(new_metadata)
    _save_store(texts, metadata, new_index)

    print(f"✅ Ingested {len(new_metadata)} new chunks from {len(filenames)} uploaded files into dataset '{dataset_id}'")
    return snippet_map  # NEW: {filename: snippet}
