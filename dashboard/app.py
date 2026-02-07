import streamlit as st

st.set_page_config(
    page_title="GhostTrace AI",
    page_icon="🕵️",
    layout="wide"
)

st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #141726 0, #050711 55%, #020309 100%);
    color: #ecf0f1;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
}

/* Main padding */
.main-block {
    padding: 1.5rem 2rem 2rem 2rem;
}

/* Navbar */
.navbar {
    position: sticky;
    top: 0;
    z-index: 50;
    padding: 0.8rem 1.4rem;
    border-radius: 999px;
    backdrop-filter: blur(22px);
    background: linear-gradient(120deg, rgba(34,40,72,0.92), rgba(18,20,38,0.97));
    border: 1px solid rgba(129,140,248,0.5);
    box-shadow: 0 18px 60px rgba(0,0,0,0.75);
}
.nav-title {
    font-weight: 600;
    letter-spacing: 0.05em;
    font-size: 0.9rem;
    text-transform: uppercase;
}
.nav-pill {
    padding: 0.15rem 0.7rem;
    border-radius: 999px;
    font-size: 0.7rem;
    text-transform: uppercase;
    background: rgba(34,197,94,0.14);
    border: 1px solid rgba(34,197,94,0.6);
    color: #bbf7d0;
}

/* Cards */
.card {
    border-radius: 22px;
    padding: 1.1rem 1.3rem;
    background: radial-gradient(circle at top left, rgba(148,163,255,0.18), rgba(15,23,42,0.98));
    border: 1px solid rgba(148,163,255,0.45);
    box-shadow: 0 18px 55px rgba(15,23,42,0.9);
}
.card-soft {
    border-radius: 18px;
    padding: 0.9rem 1.1rem;
    background: rgba(15,23,42,0.9);
    border: 1px solid rgba(51,65,85,0.95);
}

/* Sections */
.section-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: #9ca3af;
}
.section-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: #e5e7eb;
}

/* Risk badge + score chip */
.risk-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.18rem 0.7rem;
    border-radius: 999px;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}
.risk-badge-high {
    background: rgba(248,113,113,0.12);
    border: 1px solid rgba(248,113,113,0.7);
    color: #fecaca;
}
.risk-badge-medium {
    background: rgba(251,191,36,0.12);
    border: 1px solid rgba(251,191,36,0.7);
    color: #fef9c3;
}
.risk-badge-low {
    background: rgba(34,197,94,0.12);
    border: 1px solid rgba(34,197,94,0.7);
    color: #bbf7d0;
}

.score-chip {
    padding: 0.18rem 0.7rem;
    border-radius: 999px;
    background: rgba(56,189,248,0.12);
    border: 1px solid rgba(56,189,248,0.7);
    color: #e0f2fe;
    font-size: 0.72rem;
}

/* Circular risk meter */
.risk-meter-wrapper {
    position: relative;
    width: 82px;
    height: 82px;
}
.risk-meter {
    width: 82px;
    height: 82px;
    border-radius: 999px;
    padding: 4px;
    background:
      conic-gradient(from 220deg,
        #22c55e 0deg,
        #22c55e 80deg,
        #facc15 160deg,
        #f97316 220deg,
        #ef4444 320deg,
        #1f2937 320deg,
        #1f2937 360deg);
    display: flex;
    align-items: center;
    justify-content: center;
}
.risk-meter-inner {
    width: 100%;
    height: 100%;
    border-radius: 999px;
    background: radial-gradient(circle at 30% 20%, #020617, #020617);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #e5e7eb;
    font-size: 0.75rem;
    font-weight: 500;
}

/* Console */
.console-box {
    font-family: "JetBrains Mono", Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    font-size: 0.75rem;
    background: radial-gradient(circle at top left, #111827, #020617);
    border-radius: 16px;
    padding: 0.75rem 1rem;
    border: 1px solid rgba(55,65,81,0.9);
    color: #e5e7eb;
}
.console-line-prompt { color: #4ade80; }
.console-line-info { color: #93c5fd; }
.console-line-warn { color: #f97316; }

/* Simple fade-in anim on updates */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}
.fade-in {
    animation: fadeInUp 0.25s ease-out;
}

/* Scrollable chat history */
.chat-scroll {
    max-height: 260px;
    overflow-y: auto;
    padding-right: 0.1rem;
}
.chat-scroll::-webkit-scrollbar {
    width: 3px;
}
.chat-scroll::-webkit-scrollbar-thumb {
    background: rgba(75,85,99,0.9);
    border-radius: 999px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-block">', unsafe_allow_html=True)

col_nav, col_env = st.columns([5, 1])
with col_nav:
    st.markdown("""
    <div class="navbar fade-in">
      <div style="display:flex;align-items:center;justify-content:space-between;gap:0.75rem;">
        <div style="display:flex;align-items:center;gap:0.6rem;">
          <div style="width:20px;height:20px;border-radius:8px;
                      background:conic-gradient(from 180deg, #22d3ee, #818cf8, #f97316, #22d3ee);
                      box-shadow:0 0 18px rgba(129,140,248,0.9);"></div>
          <div>
            <div class="nav-title">GhostTrace AI</div>
            <div style="font-size:0.72rem;color:#9ca3af;">RAG-powered Contract & API Risk Auditor</div>
          </div>
        </div>
        <div style="display:flex;align-items:center;gap:0.4rem;">
          <span class="nav-pill">LIVE • DEMO</span>
          <div style="width:22px;height:22px;border-radius:999px;
                      background:radial-gradient(circle at 30% 20%, #facc15, #4f46e5);
                      box-shadow:0 0 10px rgba(129,140,248,0.8);"></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_env:
    st.empty()

st.markdown("</div>", unsafe_allow_html=True)
