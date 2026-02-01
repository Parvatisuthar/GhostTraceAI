"""
Role 3 Testing Suite
Run: python drift_analysis/test_scenarios.py
"""

from ghost_scoring import demo_risk_analysis

TEST_QUERIES = [
("how do I charge a payment?", "HIGH", "Deprecated v1.0"),
("what are the latest webhook events?", "LOW", "v3.0 docs"),
("how to migrate from v1 to v3?", "MEDIUM", "Migration guide"),
("what is the auth API login endpoint?", "HIGH", "v1.0 auth"),
("rate limits policy?", "LOW", "v3.0 rate_limits"),
]

print("🧪 GhostTrace Risk Engine – Test Suite")
print("=" * 60)

for query, expected_level, description in TEST_QUERIES:
print(f"
📝 {description}")
demo_risk_analysis(query)
print("-" * 60)

print("✅ All tests complete. Ready for Role 4 integration!")
