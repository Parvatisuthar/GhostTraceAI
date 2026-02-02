from pathlib import Path
import json
from typing import List, Dict


def find_metadata_store():
    """Find metadata_store.json in current or parent dirs."""
    possible_paths = [
        Path("metadata_store.json"),
        Path("data_ingestion/metadata_store.json"),
        Path("data_ingestion/sample_datasets/metadata_store.json"),
        Path("./metadata_store.json")
    ]

    for p in possible_paths:
        if p.exists():
            print(f"✅ Found metadata at: {p.absolute()}")
            return p

    print("❌ metadata_store.json not found. Available JSON files:")
    for p in Path(".").rglob("*.json"):
        print(f"  {p}")
    return None


def load_documents() -> List[Dict]:
    """Load documents from metadata_store.json."""

    # Find metadata file
    meta_path = find_metadata_store()
    if not meta_path:
        print("ERROR: No metadata_store.json found!")
        return []

    # Load metadata
    with open(meta_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    print(f"✅ Loaded {len(metadata)} metadata entries")

    docs = []
    for i, meta in enumerate(metadata):
        file_path = Path(meta["path"])
        print(f"Checking file: {file_path}")

        if file_path.exists():
            text = file_path.read_text(encoding="utf-8")
            doc = {
                "doc_id": i + 1,
                "name": meta["file"],
                "text": text,
                "year": 2024 if not meta["deprecated"] else 2021,
                "version": meta["version"],
                "source": meta["doc_type"],
                "is_expired": meta["deprecated"],
                "path": str(file_path)
            }
            docs.append(doc)
            print(f"  ✅ Loaded: {meta['file']}")
        else:
            print(f"  ❌ Missing: {meta['path']}")

    print(f"\n🎉 FINAL: {len(docs)} documents ready for GhostTrace!")
    return docs


if __name__ == "__main__":
    docs = load_documents()

