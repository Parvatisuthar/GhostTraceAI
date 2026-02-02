import os
from metadata_manager import MetadataManager
from vector_store.vector_store import VectorStore

from create_sample_datasets import create_sample_datasets

sample_dir = "data_ingestion/sample_datasets"

# Step 1: create datasets
create_sample_datasets()

# Step 2: metadata + vectors
mm = MetadataManager()
vs = VectorStore()

print("\n🚀 GhostTrace API Docs Ingestion Started\n")

for file in os.listdir(sample_dir):
    if not file.endswith(".txt"):
        continue

    path = os.path.join(sample_dir, file)

    meta = mm.extract_metadata(path)

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    vs.add_document(text, meta)

mm.save()
vs.build()
vs.save()

print("\n✅ Ingestion Completed Successfully")
