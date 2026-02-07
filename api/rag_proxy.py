# api/rag_proxy.py
from .models import AuditRequest
import asyncio
import random


async def call_rag_engine(request: AuditRequest) -> dict:
    """Mock RAG Engine - Replace with real rag_engine later"""
    await asyncio.sleep(0.3)  # Simulate processing

    # Mock response (your real RAG will return this format)
    return {
        "risk_score": random.uniform(45, 95),
        "risk_level": random.choice(["LOW", "MEDIUM", "HIGH"]),
        "explanation": f"🔍 Analyzed '{request.query}' across 12 documents. Found {random.randint(2, 5)} potential risks.",
        "evidence": [
            {"chunk": "Suspicious payment clause detected", "score": 0.87},
            {"chunk": "Unusual chargeback pattern", "score": 0.76}
        ],
        "sources": [f"doc_{i}.pdf" for i in range(1, 4)],
        "timestamp": "2026-02-04T22:52:00Z"
    }
