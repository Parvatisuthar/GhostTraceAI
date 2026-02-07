# rag_engine/__init__.py
from .rag_engine import GhostRAG
from .rag_pipeline import analyze_query
from .explanation import RiskLevel, generate_explanation  # optional helper

__version__ = "1.0.0"
__all__ = ["GhostRAG", "analyze_query", "RiskLevel", "generate_explanation"]
