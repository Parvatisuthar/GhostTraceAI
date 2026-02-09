import streamlit as st
import math
from data_ingestion.upload_ingest import ingest_uploaded_files
from rag_engine.llm_client import suggest_queries_for_dataset
from rag_engine.rag_pipeline import analyze_query

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
if "suggested_queries" not in st.session_state:
    st.session_state.suggested_queries = []
if "persona" not in st.session_state:
    st.session_state.persona = "developer"
if "prefill_query" not in st.session_state:
    st.session_state.prefill_query = ""

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
.gt-sub { color: #9ca3af; font-size: 14px; }
.gt-pill {
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 13px;
    font-weight: 600;
    border: 1px solid #4b5563;
    margin: 4px 6px 4px 0;
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

# ─────────────────────────────────────────────────────
# PAGE 2 — UPLOAD DATASET
# ─────────────────────────────────────────────────────
elif st.session_state.page == "Upload Dataset":
    st.markdown("""
    <div class="gt-card">
        <h2>📤 Upload Documentation</h2>
        <p class="gt-sub">TXT preferred for now.</p>
    </div>
    """, unsafe_allow_html=True)

    dataset_id = st.text_input("Dataset name / ID", value="user_upload")

    uploaded = st.file_uploader(
        "Upload files",
        accept_multiple_files=True,
        type=["txt"],
    )

    if uploaded and st.button("Index into GhostTrace"):
        contents, names = [], []
        for f in uploaded:
            contents.append(f.read().decode("utf-8", errors="ignore"))
            names.append(f.name)

        snippet_map = ingest_uploaded_files(contents, names, dataset_id=dataset_id)
        st.session_state.files = uploaded

        # 🔥 Feature-4: LLM-driven query suggestions
        suggested = suggest_queries_for_dataset(
            list(snippet_map.keys()),
            list(snippet_map.values())
        )
        st.session_state.suggested_queries = suggested

        st.success(f"Indexed {len(uploaded)} file(s) into dataset '{dataset_id}'.")

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

    persona_label = st.radio(
        "Explanation for:",
        options=["Developer", "Compliance"],
        horizontal=True,
    )
    st.session_state.persona = "developer" if persona_label == "Developer" else "compliance"

    # 🔥 Suggested Questions Pills (Feature-4)
    if st.session_state.suggested_queries:
        st.markdown("### 💡 Suggested Questions")
        for q in st.session_state.suggested_queries:
            if st.button(q, key=f"suggest_{q}"):
                st.session_state.prefill_query = q
                st.experimental_rerun()

    query = st.text_input(
        "Ask a question",
        value=st.session_state.prefill_query,
        placeholder="How do I migrate from v1 to v3?"
    )

    if st.button("Run Audit", type="primary") and query:
        result = analyze_query(query, persona=st.session_state.persona)

        risk = result["risk_assessment"]["risk"]
        explanation = result["risk_assessment"]["explanation"]
        documents = result["documents"]

        level = risk["level"]
        score = risk["score"]

        color = "#22c55e"
        label = "LOW RISK"
        if level == "MEDIUM":
            color, label = "#eab308", "MEDIUM RISK"
        elif level == "HIGH":
            color, label = "#ef4444", "HIGH RISK"

        st.session_state.audit_data = {
            "score": score,
            "label": label,
            "color": color,
            "explanation": explanation,
            "reasons": risk["reasons"],
            "actions": risk["recommendations"],
            "sources": [d["file"] for d in documents],
        }

    if st.session_state.audit_data:
        d = st.session_state.audit_data
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"""
            <div class="gt-card">
                <h3>Explanation</h3>
                <p>{d['explanation'].replace('\n', '<br>')}</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div class='gt-card'><h3>Why this risk?</h3>", unsafe_allow_html=True)
            for r in d["reasons"]:
                st.markdown(f"- {r}")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='gt-card'><h3>Recommended Actions</h3>", unsafe_allow_html=True)
            for a in d["actions"]:
                st.markdown(f"<span class='gt-pill'>{a}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='gt-card'><h3>Top Documents Used</h3>", unsafe_allow_html=True)
            for s in d["sources"]:
                st.markdown(f"- `{s}`")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='gt-card' style='text-align:center'><h3>Risk Score</h3>", unsafe_allow_html=True)
            st.markdown(risk_ring(d["score"], d["color"]), unsafe_allow_html=True)
            st.markdown(f"<b style='color:{d['color']}'>{d['label']}</b>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)