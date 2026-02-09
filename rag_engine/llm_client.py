# rag_engine/llm_client.py
import subprocess
from typing import List

OLLAMA_MODEL = "llama3"   # change if you use another model


def _call_ollama(prompt: str) -> str:
    """
    Calls Ollama via CLI and returns raw text.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt,
            text=True,
            capture_output=True,
            check=True,
        )
        return result.stdout.strip()
    except Exception as e:
        print("❌ Ollama error:", e)
        return ""


# ─────────────────────────────────────────────────────
# 🔹 USED BY RAG PIPELINE (audit explanation)
# ─────────────────────────────────────────────────────
def llm_explain(
    query: str,
    documents: List[dict],
    risk_level: str,
    persona: str = "developer",
) -> str:
    """
    Generate persona-based explanation for audit result.
    """

    if not documents:
        return ""

    doc_list = ""
    for d in documents[:3]:
        doc_list += f"- {d['file']} (v{d.get('version','?')})\n"

    prompt = f"""
You are an AI Risk & Compliance Auditor.

Persona: {persona.upper()}
Risk Level: {risk_level}

User Question:
{query}

Documents Used:
{doc_list}

Explain:
- Why this risk level was assigned
- What the user should be careful about
- Keep it concise and practical
"""

    return _call_ollama(prompt)


# ─────────────────────────────────────────────────────
# 🔹 FEATURE-4: LLM-DRIVEN QUERY SUGGESTIONS
# ─────────────────────────────────────────────────────
def suggest_queries_for_dataset(
    file_names: List[str],
    snippets: List[str],
    max_queries: int = 5,
) -> List[str]:
    """
    Generate audit-style questions based on uploaded docs.
    """

    if not file_names or not snippets:
        return []

    context = ""
    for name, snip in zip(file_names, snippets):
        context += f"\nFILE: {name}\nSNIPPET:\n{snip[:300]}\n"

    prompt = f"""
You are an AI Risk & Compliance Auditor.

Based on the following documentation snippets,
generate {max_queries} HIGH-VALUE audit questions.

Rules:
- Focus on migration, versioning, security, compliance, or risks
- One question per line
- No numbering, no bullets, no explanations

Documentation:
{context}

Output ONLY the questions.
"""

    raw = _call_ollama(prompt)
    if not raw:
        return []

    questions = []
    for line in raw.splitlines():
        line = line.strip("-• ").strip()
        if len(line) > 10:
            questions.append(line)

    return questions[:max_queries]