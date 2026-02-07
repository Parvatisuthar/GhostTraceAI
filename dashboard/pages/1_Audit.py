import streamlit as st
import httpx
from typing import Dict, Any

# Chat history state
if "history" not in st.session_state:
    st.session_state.history = []  # [{query, result}]
if "last_result" not in st.session_state:
    st.session_state.last_result = None

st.markdown("### ")  # small spacer

left, right = st.columns([0.34, 0.66], gap="large")

API_URL = st.session_state.get("api_url", "http://localhost:8000")


def call_audit_api(query: str) -> Dict[str, Any]:
    with httpx.Client(timeout=30) as client:
        resp = client.post(
            f"{API_URL}/audit",
            json={"query": query}
        )
        resp.raise_for_status()
        return resp.json()


def risk_badge_class(level: str) -> str:
    lvl = level.upper()
    if lvl == "HIGH":
        return "risk-badge risk-badge-high"
    if lvl == "MEDIUM":
        return "risk-badge risk-badge-medium"
    return "risk-badge risk-badge-low"


with left:
    st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Conversation</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:0.3rem;"></div>', unsafe_allow_html=True)

    # Scrollable chat history
    st.markdown('<div class="chat-scroll">', unsafe_allow_html=True)
    if st.session_state.history:
        for item in st.session_state.history[-6:]:
            q = item["query"]
            r = item["result"]
            level = str(r.get("risk_level", "")).upper()
            score = float(r.get("risk_score", 0.0))

            st.markdown(
                f"""
                <div style="margin-bottom:0.35rem;display:flex;justify-content:flex-end;">
                  <div style="max-width:85%;padding:0.45rem 0.7rem;border-radius:999px;
                              border-bottom-right-radius:6px;
                              background:rgba(129,140,248,0.18);
                              border:1px solid rgba(129,140,248,0.6);
                              font-size:0.8rem;">
                    {q}
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div style="margin-bottom:0.7rem;display:flex;justify-content:flex-start;">
                  <div style="max-width:90%;padding:0.45rem 0.7rem;border-radius:16px;
                              border-top-left-radius:6px;
                              background:rgba(15,23,42,0.95);
                              border:1px solid rgba(55,65,81,0.9);
                              font-size:0.78rem;">
                    <div style="font-size:0.7rem;color:#9ca3af;margin-bottom:0.15rem;">
                        Risk: {level} • Score {score:.0f}
                    </div>
                    <div style="color:#e5e7eb;">
                      {r.get("explanation","")[:180]}...
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.caption("Start by asking GhostTrace about your payment/auth APIs or policies.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Ask GhostTrace</div>', unsafe_allow_html=True)

    query = st.text_input(
        "Ask a question about your API / contracts",
        value="how to migrate from v1 to v3?",
        label_visibility="collapsed",
        placeholder="Example: how do I charge a payment?",
    )

    col_btn1, col_btn2 = st.columns([1, 1])
    run_clicked = False
    with col_btn1:
        run_clicked = st.button("🚀 Run Risk Audit", use_container_width=True)
    with col_btn2:
        clear_history = st.button("🧹 Clear Conversation", use_container_width=True)

    if clear_history:
        st.session_state.history = []
        st.session_state.last_result = None
        st.experimental_rerun()

    st.markdown('<div style="height:0.8rem;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Pipeline Status</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card-soft">', unsafe_allow_html=True)
        st.markdown("**Role 1 • Data Ingestion**", unsafe_allow_html=True)
        st.caption("✓ API docs indexed • FAISS/Chroma vectors saved • metadata_store.json ready")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)

        st.markdown('<div class="card-soft">', unsafe_allow_html=True)
        st.markdown("**Role 3 • Risk Engine Tests**", unsafe_allow_html=True)
        st.caption("✓ Deprecated v1.0 • v3.0 docs • Migration guide • Rate limit tests completed")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


with right:
    st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">GhostTrace Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:0.4rem;"></div>', unsafe_allow_html=True)

    result = st.session_state.get("last_result")

    if run_clicked and query.strip():
        try:
            result = call_audit_api(query.strip())
            st.session_state.last_result = result
            st.session_state.history.append({"query": query.strip(), "result": result})
        except Exception as e:
            st.error(f"Backend error: {e}")

    if result:
        risk_level = str(result.get("risk_level", "")).upper()
        score = float(result.get("risk_score", 0.0))

        col_head1, col_head2 = st.columns([0.6, 0.4])
        with col_head1:
            st.markdown(
                f'<div class="{risk_badge_class(risk_level)}">RISK LEVEL • {risk_level}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div style='margin-top:0.6rem;font-size:0.8rem;color:#9ca3af;'>"
                f"Query: <code>{query}</code></div>",
                unsafe_allow_html=True,
            )
        with col_head2:
            st.markdown(
                """
                <div style="display:flex;justify-content:flex-end;">
                  <div class="risk-meter-wrapper fade-in">
                    <div class="risk-meter">
                      <div class="risk-meter-inner">
                """,
                unsafe_allow_html=True,
            )
            st.markdown(f"{score:.0f}%", unsafe_allow_html=True)
            st.markdown(
                """
                      </div>
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div style='text-align:right;margin-top:0.25rem;'>"
                f"<span class='score-chip'>Score: {score:.0f}</span></div>",
                unsafe_allow_html=True,
            )

        st.markdown('<div style="height:0.7rem;"></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">Why this risk?</div>', unsafe_allow_html=True)
        explanation = result.get("explanation") or ""
        if explanation:
            st.markdown(
                f"<div style='font-size:0.85rem;margin-top:0.2rem;color:#e5e7eb;'>{explanation}</div>",
                unsafe_allow_html=True,
            )

        flags = [e.get("flag") for e in result.get("evidence", []) if isinstance(e, dict) and e.get("flag")]
        if flags:
            st.markdown('<div style="height:0.7rem;"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Flags</div>', unsafe_allow_html=True)
            st.markdown(
                "<ul style='font-size:0.82rem;color:#e5e7eb;'>" +
                "".join(f"<li>{f}</li>" for f in flags) +
                "</ul>",
                unsafe_allow_html=True,
            )

        actions = result.get("recommended_actions") or []
        if actions:
            st.markdown('<div style="height:0.7rem;"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Recommended Actions</div>', unsafe_allow_html=True)
            st.markdown(
                "<ul style='font-size:0.82rem;color:#e5e7eb;'>" +
                "".join(f"<li>{a}</li>" for a in actions) +
                "</ul>",
                unsafe_allow_html=True,
            )

        sources = result.get("sources") or []
        if sources:
            st.markdown('<div style="height:0.7rem;"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Top Documents Used</div>', unsafe_allow_html=True)
            st.markdown(
                "<ul style='font-size:0.82rem;color:#9ca3af;'>" +
                "".join(f"<li>{s}</li>" for s in sources) +
                "</ul>",
                unsafe_allow_html=True,
            )
    else:
        st.caption("Run an audit from the left panel to see risk analysis here.")

    st.markdown("</div>", unsafe_allow_html=True)

# Bottom console log
st.markdown('<div style="margin-top:1.3rem;" class="console-box fade-in">', unsafe_allow_html=True)
st.markdown("""
<div class="console-line-info">GHOSTTRACE SYSTEM BOOTING</div>
<div>------------------------------------------------------------------</div>
<div class="console-line-prompt">$ role_1_ingestion ▶ API docs indexed · FAISS/Chroma index (10 vectors) ready</div>
<div class="console-line-prompt">$ role_3_risk_tests ▶ Deprecated v1.0 · v3.0 docs · Migration guide</div>
<div class="console-line-info">All tests complete. Ready for interactive RAG + FastAPI (Roles 4 & 5).</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
