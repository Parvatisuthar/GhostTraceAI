# In rag_pipeline.py
from rag_engine import GhostRAG
from rag_engine.explanation import calculate_risk, format_for_ui


def analyze_query(query: str):
    rag = GhostRAG()
    results = rag.search(query)
    risk = calculate_risk(results)
    return {
        "query": query,
        "documents": results,
        "risk_assessment": format_for_ui(risk)
    }

def pretty_print(result: dict):
    print("\n🧠 GHOSTTRACE ANALYSIS")
    print("=" * 50)

    print(f"\n📝 Query:")
    print(f"  {result['query']}")

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



if __name__ == "__main__":
    q = input("Ask a question: ")
    result = analyze_query(q)
    pretty_print(result)


