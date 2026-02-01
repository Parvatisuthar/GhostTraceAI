"""
GhostTrace Risk Engine – Role 3
Analyzes VectorStore.search() results for deprecated/outdated API docs
"""

import json
import re
from pathlib import Path
from typing import List, Dict


class GhostTraceRiskEngine:
    """
    Main risk scoring engine.

    Input: VectorStore.search() results [file:84]
    Output: {"score": 75, "level": "HIGH", "reasons": [...], "flags": [...]}
    """


def __init__(self, metadata_path: str = "../data_ingestion/metadata_store.json"):
    """
    Initialize with path to Role 1's metadata [file:91]
    """
    self.metadata_path = Path(metadata_path)
    self.global_metadata = self._load_global_metadata()
    self.latest_versions = self._compute_latest_versions()
    self.deprecation_notice_exists = self._has_deprecation_notice()

    print(f"✅ Risk Engine initialized:")
    print(f"   - Loaded {len(self.global_metadata)} total docs")
    print(f"   - Latest versions: {self.latest_versions}")
    print(f"   - Deprecation notice: {'Yes' if self.deprecation_notice_exists else 'No'}")


def _load_global_metadata(self) -> List[Dict]:
    """Load all docs metadata from Role 1 [file:91][file:92]"""
    if not self.metadata_path.exists():
        raise FileNotFoundError(
            f"❌ metadata_store.json not found at {self.metadata_path}. "
            "Run: python data_ingestion/run_metadata.py first."
        )

    with open(self.metadata_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _compute_latest_versions(self) -> Dict[str, str]:
    """For each doc_type, find highest numeric version [file:91]"""
    versions = {}
    for meta in self.global_metadata:
        doc_type = meta.get("doc_type", "unknown")
        version = meta.get("version", "unknown")

        # Only numeric versions (skip "unknown")
        if re.match(r"^d+.d+$", version):
            if doc_type not in versions or float(version) > float(versions[doc_type]):
                versions[doc_type] = version

    return versions


def _has_deprecation_notice(self) -> bool:
    """Check if deprecation notice exists [file:101]"""
    return any(
        "deprecation" in meta["file"].lower()
        for meta in self.global_metadata
    )


def compute_risk(self, results: List[Dict]) -> Dict:
    """
    Main function – takes VectorStore.search() results, returns risk assessment

    Args:
        results: List from vector_store.py [file:84]

    Example:
        results[0]["metadata"] = {"file": "payment_api_v1.0_2021.txt", "version": "1.0", "deprecated": true}
    """
    if not results:
        return {
            "score": 0,
            "level": "LOW",
            "reasons": ["No documents retrieved for analysis."],
            "flags": [],
            "actions": []
        }

    score = 0
    reasons = []
    flags = []

    # === RULE 1: DEPRECATED DOCS (50 points) ===
    deprecated_docs = [r for r in results if r["metadata"].get("deprecated", False)]
    if deprecated_docs:
        score += 50
        for doc in deprecated_docs:
            m = doc["metadata"]
            reasons.append(f"🚨 DEPRECATED DOCUMENT: {m['file']} (v{m['version']})")
            flags.append("DEPRECATED_DOC")

            # === RULE 2: OUTDATED VERSIONS (25 points) ===
    for result in results:
        meta = result["metadata"]
        doc_type = meta.get("doc_type", "unknown")
        version = meta.get("version", "unknown")

        if (version != "unknown" and
                doc_type in self.latest_versions and
                not meta.get("deprecated", False)):

            try:
                current_v = float(version)
                latest_v = float(self.latest_versions[doc_type])

                if current_v < latest_v:
                    score += 25
                    reasons.append(
                        f"⚠️ OUTDATED VERSION: {meta['file']} v{version} "
                        f"(latest v{self.latest_versions[doc_type]} for {doc_type})"
                    )
                    flags.append("OUTDATED_VERSION")
            except ValueError:
                pass  # skip malformed versions

    # === RULE 3: IGNORING DEPRECATION NOTICE (15 points) ===
    if self.deprecation_notice_exists:
        old_versions = [
            r for r in results
            if r["metadata"].get("version", "").startswith(("1.", "2."))
        ]
        if old_versions:
            score += 15
            reasons.append(
                "⚠️ IGNORING DEPRECATION: v1/v2 docs used despite "
                "official deprecation notice in knowledge base."
            )
            flags.append("IGNORING_DEPRECATION")

            # === RULE 4: CRITICAL DOMAIN MULTIPLIER ===
    critical_types = {"payment_api", "auth_api", "webhook", "sdk"}
    has_critical = any(
        r["metadata"].get("doc_type") in critical_types
        for r in results
    )
    if has_critical:
        score = int(score * 1.3)
        reasons.append(
            "🔥 CRITICAL DOMAIN: Payment/Auth/Webhook/SDK docs involved "
            "(risk multiplier applied)"
        )
        flags.append("CRITICAL_DOMAIN")

        # === RULE 5: VERSION IMBALANCE (10 points) ===
    versions_used = [
        r["metadata"].get("version", "unknown")
        for r in results
    ]
    unique_versions = set(v for v in versions_used if v != "unknown")

    if len(unique_versions) == 1 and "3.0" not in unique_versions:
        score += 10
        reasons.append(
            f"📊 VERSION IMBALANCE: All {len(results)} results from "
            f"same old version(s): {list(unique_versions)}"
        )
        flags.append("VERSION_IMBALANCE")

        # === FINAL SCORING ===
    score = max(0, min(100, score))

    if score >= 70:
        level = "HIGH"
    elif score >= 35:
        level = "MEDIUM"
    else:
        level = "LOW"

        # === DEFAULT SAFE MESSAGE ===
    if not reasons:
        reasons.append("✅ No major ghost data risks detected. All documents appear current.")

        # === RECOMMENDED ACTIONS ===
    actions = []
    if any(f in flags for f in ["DEPRECATED_DOC", "OUTDATED_VERSION"]):
        actions.extend(["PRIORITIZE_V3", "ARCHIVE_OLD_VERSIONS"])
    if "IGNORING_DEPRECATION" in flags:
        actions.append("ENFORCE_DEPRECATION_RULES")
    if "CRITICAL_DOMAIN" in flags:
        actions.append("URGENT_REVIEW")
    if level == "LOW":
        actions.append("CONTINUE_MONITORING")

    return {
        "score": score,
        "level": level,
        "reasons": reasons,
        "flags": list(set(flags)),  # dedupe
        "actions": actions
    }

== = QUICK
USAGE == =


def demo_risk_analysis(query: str):
    """
    Quick demo function for testing
    """


from vector_store import VectorStore  # [file:84]

vs = VectorStore()
vs.load()

results = vs.search(query, top_k=3)
engine = GhostTraceRiskEngine()

risk = engine.compute_risk(results)

print(f"

🧪 Query: '{query}'")
print(f"Risk Level: {risk['level']} (Score: {risk['score']})")
print("Reasons:")
for reason in risk['reasons']:
    print(f"  {reason}")
print(f"Flags: {', '.join(risk['flags'])}")
print(f"Actions: {', '.join(risk['actions'])}")

return risk

if name == "main":
# Test queries
demo_risk_analysis("how to charge a payment")  # expect HIGH
demo_risk_analysis("what are webhook events")  # expect LOW/MEDIUM
demo_risk_analysis("how to migrate from v1 to v3")  # expect MEDIUM
