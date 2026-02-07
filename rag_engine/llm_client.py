# rag_engine/llm_client.py
import subprocess
from typing import List, Dict


def _run_ollama(prompt: str, model: str = "llama3") -> str:
    """
    Call Ollama from CLI: `ollama run <model> -p "<prompt>"`.
    If anything fails, return empty string so rest of pipeline still works.
    """
    try:
        proc = subprocess.run(
            ["ollama", "run", model, "-p", prompt],
            capture_output=True,
            text=True,
            check=True,
        )
        return proc.stdout.strip()
    except Exception as e:
        # You can log this later if needed
        print(f"[LLM WARNING] Ollama call failed: {e}")
        return ""


def build_context_for_llm(query: str, documents: List[Dict]) -> str:
    """
    Create a compact context string for LLM from top documents.
    """
    parts = []
    for d in documents[:5]:  # max 5 docs
        file_name = d.get("file", "unknown")
        snippet = d.get("snippet", "")[:600]
        parts.append(f"[{file_name}]\n{snippet}")
    context_block = "\n\n".join(parts)

    return f"""User question:
{query}

Relevant documentation:
{context_block}
"""


def llm_explain(query: str, documents: List[Dict], risk_level: str) -> str:
    """
    Ask LLM to generate bullet-point explanation.
    Returns empty string if LLM not available.
    """
    context = build_context_for_llm(query, documents)

    prompt = f"""
You are GhostTrace, an API and contract risk analysis assistant.

The current risk level (based on rule-based analysis) is: {risk_level}.

{context}

Write a short explanation in 3–5 bullet points covering:
- Why this query looks risky or safe based on the documents
- Mention deprecated or outdated versions visible in file names
- Mention if any critical domains (payment, auth, webhook) are involved

Be concise and professional. Start each line with "- ".
Don't invent new APIs or files, only refer to what you see.
"""

    return _run_ollama(prompt)
