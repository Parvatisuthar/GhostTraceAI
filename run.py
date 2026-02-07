"""
GhostTrace – One Command Runner
Usage: python run.py
"""

import sys
import subprocess

# Script-style roles (auto run on import)
import data_ingestion.run_metadata          # Role 1
import drift_analysis.test_queries          # Role 3

# Function-style role
from rag_engine.rag_pipeline import run_rag


VECTOR_VIEWER_CMD = [sys.executable, "-m", "vector_store.vector_viewer"]


def main():
    print("🧠 GHOSTTRACE SYSTEM BOOTING")
    print("=" * 60)

    # ───────────── ROLE 1 ─────────────
    print("\n🚀 Role 1: Data Ingestion")
    print("✔ Ingestion completed")

    # ───────────── ROLE 2 ─────────────
    print("\n🔗 Role 2: Vector Viewer Starting")
    print("🌐 Vector UI will be available at http://127.0.0.1:5000")

    # 🔥 Vector viewer auto-start (NON-BLOCKING)
    subprocess.Popen(VECTOR_VIEWER_CMD)

    # ───────────── ROLE 3 ─────────────
    print("\n🧪 Role 3: Risk Engine Tests")
    print("✔ Risk tests completed")

    # ───────────── ROLE 4 ─────────────
    print("\n🧠 Role 4: Interactive RAG Engine")
    print("Type 'exit' to quit")
    print("-" * 50)

    run_rag()   # 👈 ONLY USER INPUT RUNS HERE


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 GhostTrace shutdown gracefully")
        sys.exit(0)
