# rag_engine/explanation.py
"""
Role 4: Risk Analysis → Human-readable explanations for developers.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
from collections import Counter


class RiskLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass
class RiskAssessment:
    score: int  # 0-100
    level: RiskLevel  # LOW/MEDIUM/HIGH
    reasons: List[str]  # Bullet points for UI
    recommendations: List[str]  # Actionable steps
    explanation: str  # Single paragraph for devs


def calculate_risk(results: List[Dict]) -> RiskAssessment:
    """
    Convert RAG results → structured risk assessment.

    Args:
        results: List from GhostRAG.search() with file, version, deprecated, doc_type

    Example input:
    [
        {"rank":1, "file":"payment_api_v1.0_2021.txt", "deprecated":True, "doc_type":"payment_api"},
        {"rank":2, "file":"payment_api_v3.0_2024.txt", "deprecated":False, "version":"3.0"},
        ...
    ]
    """
    score = 0
    reasons = []
    recommendations = []

    # 1. Group by doc_type for domain-specific analysis
    by_domain = {}
    for r in results:
        domain = r["doc_type"]
        by_domain.setdefault(domain, []).append(r)

    # 2. Analyze each domain
    for domain, docs in by_domain.items():
        # Critical domains = higher weight
        weight = 1.4 if domain in {"payment_api", "auth_api", "sdk"} else 1.0

        # DEPRECATED docs = highest penalty
        deprecated_docs = [d for d in docs if d["deprecated"]]
        if deprecated_docs:
            count = len(deprecated_docs)
            score += 35 * weight * count
            bad_files = ", ".join([d["file"] for d in deprecated_docs[:2]])
            reasons.append(f"🚨 DEPRECATED {domain.upper()} used ({count}/{len(docs)} docs): {bad_files}")
            recommendations.append("Archive deprecated docs from RAG index")

        # OLD VERSION (non-deprecated but not latest)
        active_versions = [d["version"] for d in docs if not d["deprecated"]]
        if active_versions:
            latest_in_results = max(active_versions)
            if latest_in_results != "3.0":
                score += 18 * weight
                reasons.append(f"⚠️ Oldest version {min(active_versions)} in {domain} (latest expected: 3.0)")
                recommendations.append(f"Prioritize v{latest_in_results} docs in retrieval")

        # DOMAIN IMPACT multiplier
        if domain in {"payment_api", "auth_api", "security_protocols"}:
            reasons.append(f"🔥 HIGH IMPACT DOMAIN: {domain}")
            score *= 1.2  # Final multiplier

    # 3. Cap score and map to levels
    score = min(int(score), 100)

    if score <= 20:
        level = RiskLevel.LOW
    elif score <= 55:
        level = RiskLevel.MEDIUM
    else:
        level = RiskLevel.HIGH

    # 4. Generate explanation paragraph
    explanation = _generate_explanation(level, reasons, recommendations, results)

    return RiskAssessment(
        score=score,
        level=level,
        reasons=reasons,
        recommendations=recommendations,
        explanation=explanation
    )


def _generate_explanation(
        level: RiskLevel,
        reasons: List[str],
        recommendations: List[str],
        results: List[Dict]
) -> str:
    """Template-based explanation generator."""

    # Extract key facts
    deprecated_files = [r["file"] for r in results if r["deprecated"]]
    domains = list({r["doc_type"] for r in results})

    if level == RiskLevel.HIGH:
        if deprecated_files:
            prefix = f"The answer relies on deprecated files like {deprecated_files[0]}"
            action = "This poses production risks - migrate immediately."
        else:
            prefix = f"Critical {domains[0]} domain with outdated docs detected"
            action = "High-impact surface - validate before production use."

    elif level == RiskLevel.MEDIUM:
        prefix = "Retrieved docs include older versions"
        action = "Answer may work but lacks latest features/security. Review before use."

    else:  # LOW
        prefix = "All retrieved documents appear current"
        action = "Answer should be safe for production use."

    return (
        f"{prefix} ({', '.join(domains)} domain). "
        f"{action} "
        f"GhostTrace recommends: {recommendations[0] if recommendations else 'monitor updates'}."
    )


def format_for_ui(assessment: RiskAssessment) -> Dict:
    """Convert RiskAssessment → UI-ready JSON."""
    return {
        "risk": {
            "score": assessment.score,
            "level": assessment.level.value,
            "reasons": assessment.reasons,
            "recommendations": assessment.recommendations[:3]  # Max 3 for UI
        },
        "explanation": assessment.explanation
    }

def generate_explanation(risk_result: dict) -> str:
    """
    Convert risk output into human-readable explanation
    """
    level = risk_result.get("level", "UNKNOWN")
    reasons = risk_result.get("reasons", [])

    explanation = f"Risk Level: {level}\n"
    for r in reasons:
        explanation += f"- {r}\n"

    return explanation



# === CLI DEBUG TOOL ===
if __name__ == "__main__":
    # Sample test
    sample_results = [
        {"file": "payment_api_v1.0_2021.txt", "deprecated": True, "doc_type": "payment_api"},
        {"file": "payment_api_v3.0_2024.txt", "deprecated": False, "version": "3.0", "doc_type": "payment_api"},
        {"file": "webhook_events_v3.0.txt", "deprecated": False, "version": "3.0", "doc_type": "webhook"}
    ]

    risk = calculate_risk(sample_results)
    print("🧪 Sample Risk Assessment:")
    print(f"Score: {risk.score} | Level: {risk.level.value}")
    print("Reasons:", "".join(risk.reasons))
    print("Explanation: ", risk.explanation)
