# rag_engine/rag_pipeline.py
from typing import Dict
from rag_engine import GhostRAG
from rag_engine.explanation import calculate_risk, format_for_ui
from rag_engine.llm_client import llm_explain


def analyze_query(query: str) -> Dict:
    """
    Main pipeline:
    - RAG search via GhostRAG
    - Rule-based risk calculation
    - LLM explanation (optional)
    - Combined, UI-ready JSON
    """
    rag = GhostRAG()
    documents = rag.search(query)

    # 1) Rule-based risk assessment
    risk_assessment = calculate_risk(documents)
    ui_risk = format_for_ui(risk_assessment)  # {"risk": {...}, "explanation": str}

    # 2) LLM explanation (optional)
    llm_text = llm_explain(
        query=query,
        documents=documents,
        risk_level=ui_risk["risk"]["level"],
    )

    # 3) Combine explanations:
    # - top: short rule-based paragraph
    # - then (if available) LLM bullets
    combined_explanation = ui_risk["explanation"]
    if llm_text:
        combined_explanation = (
            f"{ui_risk['explanation']}\n\n"
            f"LLM perspective:\n{llm_text}"
        )

    return {
        "query": query,
        "documents": documents,
        "risk_assessment": {
            "risk": ui_risk["risk"],          # score, level, reasons, recommendations
            "explanation": combined_explanation,  # rule-based + LLM
        },
    }


def pretty_print(result: Dict) -> None:
    print("\n🧠 GHOSTTRACE ANALYSIS")
    print("=" * 50)

    print(f"\n📝 Query:\n  {result['query']}")

    risk = result["risk_assessment"]["risk"]
    print(f"\n🚦 Risk Level: {risk['level']} (Score: {risk['score']})")

    print("\n❓ Why this risk?")
    for r in risk["reasons"]:
        print(f"  - {r}")

    print("\n🛠 Recommended Actions:")
    for a in risk["recommendations"]:
        print(f"  - {a}")

    print("\n📄 Top Documents Used:")
    for d in result["documents"]:
        flag = "⚠️ DEPRECATED" if d["deprecated"] else ""
        print(f"  {d['rank']}. {d['file']} (v{d['version']}) {flag}")

    print("\n" + "=" * 50)


def run_rag() -> None:
    print("🧠 GhostTrace Interactive RAG")
    print("Type 'exit' to quit")
    print("=" * 50)

    while True:
        query = input("\nAsk a question: ").strip()

        if query.lower() in {"exit", "quit"}:
            print("\n👋 Exiting GhostTrace. Bye!")
            break

        if not query:
            print("⚠️ Please enter a valid question.")
            continue

        result = analyze_query(query)

        print("\n🧠 GHOSTTRACE ANALYSIS")
        print("=" * 50)
        risk = result["risk_assessment"]["risk"]
        print(f"Query: {result['query']}")
        print(f"Risk Level: {risk['level']} (Score: {risk['score']})")

        print("\nWhy this risk?")
        for reason in risk["reasons"]:
            print(f" - {reason}")

        print("\nRecommended Actions:")
        for rec in risk["recommendations"]:
            print(f" - {rec}")

        print("\nTop Documents Used:")
        for doc in result["documents"]:
            print(f" - {doc['file']} (v{doc['version']})")

        print("\nFull explanation (rule-based + LLM if available):")
        print(result["risk_assessment"]["explanation"])
        print("\n" + "=" * 50)


if __name__ == "__main__":
    run_rag()
