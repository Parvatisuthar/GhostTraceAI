import streamlit as st
import math
import random

# ─────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="GhostTrace AI",
    page_icon="👻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "files" not in st.session_state:
    st.session_state.files = []
if "audit_data" not in st.session_state:
    st.session_state.audit_data = None

# ─────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────
st.markdown("""
<style>
.stApp { background: #0d1117; color: #e5e7eb; }
[data-testid="stSidebar"] { background: #161b22; }
h1,h2,h3 { color: #f8fafc; }
.gt-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 20px;
}
.gt-title { font-size: 20px; font-weight: 800; }
.gt-sub { color: #9ca3af; font-size: 14px; }
.gt-pill {
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 13px;
    font-weight: 600;
    border: 1px solid;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────────────
st.sidebar.markdown("## 👻 GhostTrace AI")
st.sidebar.markdown("AI Risk & Compliance Auditor")

st.session_state.page = st.sidebar.radio(
    "Navigation",
    ["Home", "Upload Dataset", "Audit Result"]
)

# ─────────────────────────────────────────────────────
# RISK RING SVG
# ─────────────────────────────────────────────────────
def risk_ring(score, color):
    r = 70
    c = 2 * math.pi * r
    d = (score / 100) * c
    return f"""
    <svg width="180" height="180">
        <circle cx="90" cy="90" r="{r}" stroke="#2d333b" stroke-width="12" fill="none"/>
        <circle cx="90" cy="90" r="{r}" stroke="{color}" stroke-width="12" fill="none"
            stroke-dasharray="{d} {c-d}"
            stroke-linecap="round"
            transform="rotate(-90 90 90)" />
        <text x="50%" y="50%" text-anchor="middle" dy="8px"
            font-size="40" fill="{color}" font-weight="800">{score}%</text>
    </svg>
    """

# ─────────────────────────────────────────────────────
# DYNAMIC AUDIT ENGINE (TEMP LOGIC)
# ─────────────────────────────────────────────────────
def run_audit(query, files):

    # Query complexity score
    query_score = min(40, len(query.split()) * 3)

    # File count score
    file_score = min(40, len(files) * 10)

    # Base score
    score = query_score + file_score

    # Clamp score
    score = max(10, min(95, score))

    if score >= 70:
        label, color = "HIGH RISK", "#ef4444"
    elif score >= 40:
        label, color = "MEDIUM RISK", "#eab308"
    else:
        label, color = "LOW RISK", "#22c55e"

    return {
        "score": score,
        "label": label,
        "color": color,
        "explanation": """
        Risk score calculated using query complexity and number of documentation sources.
        Higher number of sources or complex migration queries increase hallucination risk.
        """,
        "actions": [
            "Verify version compatibility",
            "Review deprecated endpoints",
            "Cross-check documentation sources"
        ]
    }


# ─────────────────────────────────────────────────────
# PAGE 1 — HOME
# ─────────────────────────────────────────────────────
if st.session_state.page == "Home":
    st.markdown("""
    <div class="gt-card">
        <h1>👻 GhostTrace AI</h1>
        <p class="gt-sub">
        AI-powered risk auditing for LLM outputs, APIs & documentation.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div class="gt-card">
            <h3>What GhostTrace Does</h3>
            <ul>
                <li>Detects outdated or conflicting sources</li>
                <li>Scores hallucination & compliance risk</li>
                <li>Audits API & policy responses</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# PAGE 2 — UPLOAD DATASET
# ─────────────────────────────────────────────────────
elif st.session_state.page == "Upload Dataset":
    st.markdown("""
    <div class="gt-card">
        <h2>📤 Upload Documentation</h2>
        <p class="gt-sub">PDF, TXT, CSV supported</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload files",
        accept_multiple_files=True,
        type=["pdf", "txt", "csv"]
    )

    if uploaded:
        st.session_state.files = uploaded
        st.success(f"Uploaded {len(uploaded)} file(s)")

    if st.session_state.files:
        st.markdown("### Uploaded Files")
        for f in st.session_state.files:
            st.markdown(f"- 📄 `{f.name}`")

# ─────────────────────────────────────────────────────
# PAGE 3 — AUDIT RESULT
# ─────────────────────────────────────────────────────
elif st.session_state.page == "Audit Result":
    st.markdown("""
    <div class="gt-card">
        <h2>🧠 Run Audit</h2>
    </div>
    """, unsafe_allow_html=True)

    query = st.text_input("Ask a question", placeholder="How do I migrate from v1 to v3?")

    if st.button("Run Audit", type="primary") and query:
        st.session_state.audit_data = run_audit(query, st.session_state.files)

    if st.session_state.audit_data:
        d = st.session_state.audit_data
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"""
            <div class="gt-card">
                <h3>Explanation</h3>
                <p>{d['explanation']}</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="gt-card">
                <h3>Recommended Actions</h3>
            """, unsafe_allow_html=True)

            for a in d["actions"]:
                st.markdown(f"<span class='gt-pill' style='border-color:{d['color']};color:{d['color']}'>{a}</span>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="gt-card" style="text-align:center">
                <h3>Risk Score</h3>
            """, unsafe_allow_html=True)
            st.markdown(risk_ring(d["score"], d["color"]), unsafe_allow_html=True)
            st.markdown(f"<b style='color:{d['color']}'>{d['label']}</b>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
