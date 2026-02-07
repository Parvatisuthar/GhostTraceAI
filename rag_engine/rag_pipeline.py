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




def run_rag():
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
            print(f"Query: {result['query']}")
            print(
                f"Risk Level: {result['risk_assessment']['risk']['level']} "
                f"(Score: {result['risk_assessment']['risk']['score']})"
            )

            print("\nWhy this risk?")
            for reason in result['risk_assessment']['risk']['reasons']:
                print(f" - {reason}")

            print("\nRecommended Actions:")
            for rec in result['risk_assessment']['risk']['recommendations']:
                print(f" - {rec}")

            print("\nTop Documents Used:")
            for doc in result['documents']:
                print(f" - {doc['file']} (v{doc['version']})")


if __name__ == "__main__":
    run_rag()

