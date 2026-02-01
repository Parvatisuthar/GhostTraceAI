import os
import re
import json
from datetime import datetime

class MetadataManager:

    def __init__(self, store_path="data_ingestion/metadata_store.json"):
        self.store_path = store_path
        self.metadata = []

    def extract_metadata(self, filepath):
        filename = os.path.basename(filepath)

        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        # version detection
        version_match = re.search(r"VERSION\s+(\d+\.\d+)", text)
        version = version_match.group(1) if version_match else "unknown"

        # deprecated detection
        deprecated = "deprecated" in text.lower() or "deprecation" in text.lower()

        # domain type
        if "payment" in text.lower():
            doc_type = "payment_api"
        elif "auth" in text.lower():
            doc_type = "auth_api"
        elif "sdk" in text.lower():
            doc_type = "sdk"
        elif "webhook" in text.lower():
            doc_type = "webhook"
        elif "migration" in text.lower():
            doc_type = "migration"
        else:
            doc_type = "config"

        meta = {
            "file": filename,
            "path": filepath,
            "version": version,
            "deprecated": deprecated,
            "doc_type": doc_type,
            "ingested_at": datetime.utcnow().isoformat()
        }

        self.metadata.append(meta)
        return meta

    def save(self):
        with open(self.store_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2)

        print(f"✅ Metadata saved to {self.store_path}")

