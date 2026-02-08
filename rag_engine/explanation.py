# rag_engine/explanation.py

from typing import List, Dict
from dataclasses import dataclass
from enum import Enum


class RiskLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass
class RiskAssessment:
    score: int
    level: RiskLevel
    reasons: List[str]
    recommendations: List[str]
    explanation: str


def calculate_risk(results: List[Dict]) -> RiskAssessment:
    score = 0
    reasons = []
    recommendations = []

    by_domain = {}
    for r in results:
        domain = r.get("doc_type", "general")
        by_domain.setdefault(domain, []).append(r)

    for domain, docs in by_domain.items():
        weight = 1.4 if domain in {"payment_api", "auth_api", "sdk"} else 1.0

        deprecated_docs = [d for d in docs if d.get("deprecated")]
        if deprecated_docs:
            score += int(35 * weight * len(deprecated_docs))
            reasons.append(
                f"🚨 Deprecated documents detected in {domain}: "
                f"{deprecated_docs[0]['file']}"
            )
            recommendations.append("Remove deprecated documentation from index")

        versions = [d.get("version") for d in docs if not d.get("deprecated")]
        if versions and max(versions) != "3.0":
            score += int(18 * weight)
            reasons.append(f"⚠️ Older versions detected in {domain}")
            recommendations.append("Prioritize latest documentation")

        if domain in {"payment_api", "auth_api", "security_protocols"}:
            score = int(score * 1.2)
            reasons.append(f"🔥 High impact domain: {domain}")

    score = min(score, 100)

    if score <= 20:
        level = RiskLevel.LOW
    elif score <= 55:
        level = RiskLevel.MEDIUM
    else:
        level = RiskLevel.HIGH

    explanation = (
        f"GhostTrace analyzed {len(results)} documents. "
        f"Detected risk level: {level.value}. "
        f"Primary causes include deprecated or outdated documentation."
    )

    return RiskAssessment(
        score=score,
        level=level,
        reasons=reasons,
        recommendations=recommendations,
        explanation=explanation,
    )


def format_for_ui(assessment: RiskAssessment) -> Dict:
    return {
        "risk": {
            "score": assessment.score,
            "level": assessment.level.value,
            "reasons": assessment.reasons,
            "recommendations": assessment.recommendations[:3],
        },
        "explanation": assessment.explanation,
    }
