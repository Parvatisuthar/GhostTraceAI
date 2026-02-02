from vector_store import VectorStore


def ask_query(query):
    vs = VectorStore()
    vs.load()  # Loads texts + metadata + rebuilds vectors

    results = vs.search(query, top_k=3)

    print(f"\n🔍 Query: '{query}'\n")

    for i, (score, text, meta) in enumerate(results, 1):
        print(f"--- Result {i} (score={score:.3f}) ---")
        print(f"File: {meta['file']} | Version: {meta['version']} | Deprecated: {meta['deprecated']}")
        print(text[:300] + "...\n")

    # Risk check
    risks = []
    for score, text, meta in results:
        if meta["deprecated"]:
            risks.append(f"🚨 DEPRECATED: {meta['file']} (v{meta['version']})")
        elif meta["version"] != "3.0":
            risks.append(f"⚠️ OLD VERSION: {meta['version']} (latest is 3.0)")

    if risks:
        print("👻 GHOSTTRACE RISKS:")
        for risk in risks:
            print(f"  {risk}")
    else:
        print("✅ All documents current!")


if __name__ == "__main__":
    query = input("Ask a question about GhostTrace docs: ")
    ask_query(query)
