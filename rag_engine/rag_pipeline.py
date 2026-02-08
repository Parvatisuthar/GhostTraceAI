# rag_engine/rag_pipeline.py

from typing import Dict
from rag_engine.rag_engine import GhostRAG
from rag_engine.explanation import calculate_risk, format_for_ui
from rag_engine.llm_client import llm_explain


def analyze_query(
    query: str,
    persona: str = "developer",
    dataset_id: str = "user_upload"
) -> Dict:
    """
    Full GhostTrace audit pipeline.
    """

    # 1️⃣ Retrieve docs
    rag = GhostRAG(dataset_id=dataset_id)
    documents = rag.search(query, top_k=5)

    # 2️⃣ No-doc safety guard
    if not documents:
        return {
            "query": query,
            "documents": [],
            "sources": [],
            "risk_assessment": {
                "risk": {
                    "score": 90,
                    "level": "HIGH",
                    "reasons": ["No relevant documentation matched the query"],
                    "recommendations": ["Upload correct or updated documentation"]
                },
                "explanation": (
                    "No documents were retrieved for this query. "
                    "This creates a high hallucination and compliance risk."
                )
            }
        }

    # 3️⃣ Rule-based risk
    risk_assessment = calculate_risk(documents)
    ui_risk = format_for_ui(risk_assessment)

    # 4️⃣ Persona-based LLM explanation
    llm_text = llm_explain(
        query=query,
        documents=documents,
        risk_level=ui_risk["risk"]["level"],
        persona=persona,
    )

    explanation = risk_assessment.explanation
    if llm_text:
        explanation += f"\n\nLLM ({persona.title()} View):\n{llm_text}"

    return {
        "query": query,
        "documents": documents,
        "sources": [d["file"] for d in documents],
        "risk_assessment": {
            "risk": ui_risk["risk"],
            "explanation": explanation,
        },
    }
