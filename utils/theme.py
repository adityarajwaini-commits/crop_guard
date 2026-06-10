import streamlit as st

DARK_CSS = """
:root {
    --bg-primary:     #0d1117;
    --bg-secondary:   #161b22;
    --bg-card:        #1c2333;
    --bg-card-hover:  #21273a;
    --border:         #30363d;
    --accent:         #3fb950;
    --accent-dim:     #238636;
    --accent-glow:    rgba(63,185,80,0.18);
    --warn:           #f0883e;
    --danger:         #f85149;
    --info:           #58a6ff;
    --text-primary:   #e6edf3;
    --text-secondary: #8b949e;
    --text-muted:     #484f58;
    --gradient-hero:  linear-gradient(135deg,#0d1117 0%,#0f2417 60%,#0a2010 100%);
}
"""

LIGHT_CSS = """
:root {
    --bg-primary:     #f4f6f0;
    --bg-secondary:   #eef1ea;
    --bg-card:        #ffffff;
    --bg-card-hover:  #f8faf5;
    --border:         #d1d9c8;
    --accent:         #2d8a3e;
    --accent-dim:     #206030;
    --accent-glow:    rgba(45,138,62,0.12);
    --warn:           #d97706;
    --danger:         #dc2626;
    --info:           #2563eb;
    --text-primary:   #1a2314;
    --text-secondary: #4a5740;
    --text-muted:     #8a9a80;
    --gradient-hero:  linear-gradient(135deg,#f4f6f0 0%,#e6f0e0 60%,#dcecd4 100%);
}
"""

SHARED_CSS = """
/* ── Reset & Base ─────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

/* ── Streamlit chrome overrides ──────────────────────────── */
.stApp { background-color: var(--bg-primary) !important; }
section[data-testid="stSidebar"] {
    background-color: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text-primary) !important; }
.stButton > button {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border: 1px solid transparent !important;
    border-radius: 8px !important;
    text-align: left !important;
    padding: 10px 14px !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    transition: all 0.18s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: var(--accent-glow) !important;
    border-color: var(--border) !important;
    color: var(--accent) !important;
}

/* ── Sidebar ──────────────────────────────────────────────── */
.sidebar-logo {
    display: flex; align-items: center; gap: 12px;
    padding: 20px 4px 16px;
}
.logo-icon { font-size: 2.2rem; }
.logo-title {
    font-size: 1.3rem; font-weight: 700; letter-spacing: -0.3px;
    color: var(--accent) !important;
}
.logo-sub { font-size: 0.72rem; color: var(--text-muted) !important; margin-top: 2px; }
.sidebar-divider {
    height: 1px; background: var(--border); margin: 8px 0 12px;
}
.toggle-label {
    font-size: 0.85rem; color: var(--text-secondary);
    line-height: 2.2rem; font-weight: 500;
}
.sidebar-footer {
    position: absolute; bottom: 20px; left: 0; right: 0;
    text-align: center; font-size: 0.7rem;
    color: var(--text-muted) !important; padding: 0 16px;
}

/* ── Page wrapper ─────────────────────────────────────────── */
.page-wrap { max-width: 1080px; margin: 0 auto; padding: 0 8px; }

/* ── Hero ─────────────────────────────────────────────────── */
.hero {
    background: var(--gradient-hero);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 56px 48px;
    margin-bottom: 32px;
    position: relative; overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; top: -60px; right: -60px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, var(--accent-glow) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    background: var(--accent-glow);
    border: 1px solid var(--accent-dim);
    color: var(--accent) !important;
    font-size: 0.72rem; font-weight: 600; letter-spacing: 0.08em;
    text-transform: uppercase; border-radius: 20px;
    padding: 4px 12px; margin-bottom: 18px;
}
.hero-title {
    font-size: 2.8rem; font-weight: 800;
    letter-spacing: -0.8px; line-height: 1.15;
    margin-bottom: 14px; color: var(--text-primary) !important;
}
.hero-title span { color: var(--accent) !important; }
.hero-sub {
    font-size: 1.05rem; color: var(--text-secondary) !important;
    line-height: 1.65; max-width: 560px; margin-bottom: 28px;
}
.hero-cta {
    display: inline-flex; align-items: center; gap: 8px;
    background: var(--accent) !important;
    color: #fff !important; font-weight: 600; font-size: 0.95rem;
    border: none; border-radius: 10px;
    padding: 12px 24px; cursor: pointer;
    text-decoration: none;
    transition: all 0.2s ease;
    box-shadow: 0 4px 14px var(--accent-glow);
}
.hero-cta:hover { background: var(--accent-dim) !important; transform: translateY(-1px); }

/* ── Stat cards ──────────────────────────────────────────── */
.stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 32px; }
.stat-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 12px; padding: 20px 18px;
    transition: border-color 0.2s;
}
.stat-card:hover { border-color: var(--accent-dim); }
.stat-value {
    font-size: 1.9rem; font-weight: 800; color: var(--accent) !important;
    letter-spacing: -0.5px; line-height: 1;
}
.stat-label { font-size: 0.78rem; color: var(--text-muted) !important; margin-top: 4px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.06em; }

/* ── Feature cards ──────────────────────────────────────── */
.features-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 32px; }
.feature-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 12px; padding: 22px 20px;
    transition: all 0.2s ease;
}
.feature-card:hover {
    background: var(--bg-card-hover);
    border-color: var(--accent-dim);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}
.feature-icon { font-size: 1.8rem; margin-bottom: 10px; }
.feature-title { font-size: 0.95rem; font-weight: 700; margin-bottom: 6px; color: var(--text-primary) !important; }
.feature-desc { font-size: 0.82rem; color: var(--text-secondary) !important; line-height: 1.5; }

/* ── Section heading ─────────────────────────────────────── */
.section-heading {
    font-size: 1.2rem; font-weight: 700; margin-bottom: 16px;
    color: var(--text-primary) !important; letter-spacing: -0.2px;
    display: flex; align-items: center; gap: 8px;
}
.section-heading::after {
    content: ''; flex: 1; height: 1px; background: var(--border);
}

/* ── Upload zone ─────────────────────────────────────────── */
.upload-zone {
    background: var(--bg-card); border: 2px dashed var(--border);
    border-radius: 14px; padding: 48px 32px;
    text-align: center; transition: all 0.2s ease;
    cursor: pointer;
}
.upload-zone:hover {
    border-color: var(--accent); background: var(--accent-glow);
}
.upload-icon { font-size: 3rem; margin-bottom: 12px; }
.upload-title { font-size: 1.05rem; font-weight: 600; margin-bottom: 6px; }
.upload-hint { font-size: 0.82rem; color: var(--text-muted) !important; }

/* ── Prediction card ─────────────────────────────────────── */
.pred-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 14px; padding: 24px;
    margin-bottom: 16px;
}
.pred-disease {
    font-size: 1.5rem; font-weight: 800;
    color: var(--text-primary) !important; margin-bottom: 4px;
}
.pred-plant { font-size: 0.85rem; color: var(--text-secondary) !important; font-weight: 500; }

.confidence-bar-wrap { margin: 18px 0 4px; }
.confidence-label {
    display: flex; justify-content: space-between;
    font-size: 0.8rem; color: var(--text-secondary) !important; margin-bottom: 6px;
}
.confidence-track {
    height: 8px; background: var(--border);
    border-radius: 99px; overflow: hidden;
}
.confidence-fill {
    height: 100%; border-radius: 99px;
    transition: width 0.6s ease;
}

/* ── Severity badge ──────────────────────────────────────── */
.badge {
    display: inline-block; border-radius: 20px;
    padding: 3px 10px; font-size: 0.72rem; font-weight: 600;
    letter-spacing: 0.05em; text-transform: uppercase;
}
.badge-high   { background: rgba(248,81,73,0.15);  color: var(--danger)  !important; border: 1px solid var(--danger); }
.badge-medium { background: rgba(240,136,62,0.15); color: var(--warn)   !important; border: 1px solid var(--warn);   }
.badge-low    { background: rgba(63,185,80,0.15);  color: var(--accent)  !important; border: 1px solid var(--accent); }
.badge-healthy{ background: rgba(88,166,255,0.15); color: var(--info)    !important; border: 1px solid var(--info);   }

/* ── Info panels ─────────────────────────────────────────── */
.info-panel {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 12px; padding: 20px 22px; margin-bottom: 14px;
}
.info-panel-title {
    font-size: 0.88rem; font-weight: 700; margin-bottom: 10px;
    text-transform: uppercase; letter-spacing: 0.06em;
}
.info-panel-title.green { color: var(--accent) !important; }
.info-panel-title.orange { color: var(--warn) !important; }
.info-panel-title.blue   { color: var(--info) !important; }
.info-panel ul { padding-left: 18px; margin: 0; }
.info-panel li {
    font-size: 0.87rem; color: var(--text-secondary) !important;
    margin-bottom: 6px; line-height: 1.5;
}

/* ── History table ───────────────────────────────────────── */
.hist-row {
    display: flex; align-items: center; gap: 12px;
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 10px; padding: 12px 16px; margin-bottom: 8px;
    transition: border-color 0.18s;
}
.hist-row:hover { border-color: var(--accent-dim); }
.hist-thumb {
    width: 40px; height: 40px; border-radius: 8px;
    object-fit: cover; border: 1px solid var(--border);
}
.hist-disease { font-size: 0.9rem; font-weight: 600; }
.hist-meta    { font-size: 0.75rem; color: var(--text-muted) !important; }
.hist-conf    { margin-left: auto; font-size: 0.82rem; font-weight: 700; color: var(--accent) !important; }

/* ── Model info cards ─────────────────────────────────────── */
.model-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 12px; padding: 22px;
}
.metric-pill {
    display: inline-flex; flex-direction: column;
    background: var(--bg-secondary); border: 1px solid var(--border);
    border-radius: 10px; padding: 14px 18px; margin: 6px;
    min-width: 100px; text-align: center;
}
.metric-pill-val {
    font-size: 1.6rem; font-weight: 800; color: var(--accent) !important; line-height: 1;
}
.metric-pill-label { font-size: 0.72rem; color: var(--text-muted) !important; margin-top: 4px; }

/* ── About page ──────────────────────────────────────────── */
.team-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 12px; padding: 24px; text-align: center;
}
.team-avatar { font-size: 2.6rem; margin-bottom: 10px; }
.team-name { font-size: 1rem; font-weight: 700; }
.team-role { font-size: 0.78rem; color: var(--text-muted) !important; margin-top: 4px; }

/* ── Streamlit widget overrides ──────────────────────────── */
.stFileUploader {
    border: 2px dashed var(--border) !important;
    border-radius: 14px !important;
    background: var(--bg-card) !important;
    padding: 8px !important;
    transition: border-color 0.2s !important;
}
.stFileUploader:hover { border-color: var(--accent) !important; }
.stFileUploader label { color: var(--text-secondary) !important; }

div[data-testid="stMetricValue"] { color: var(--accent) !important; }

.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent-dim), var(--accent)) !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border-radius: 8px 8px 0 0 !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
}
.stTabs [data-baseweb="tab-list"] {
    border-bottom: 1px solid var(--border) !important;
    background: transparent !important;
}

.stAlert, .stInfo, .stSuccess, .stWarning, .stError {
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
}

/* scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* ── Responsive ──────────────────────────────────────────── */
@media (max-width: 900px) {
    .stats-row { grid-template-columns: repeat(2, 1fr); }
    .features-grid { grid-template-columns: repeat(2, 1fr); }
    .hero-title { font-size: 2rem; }
}
@media (max-width: 600px) {
    .stats-row, .features-grid { grid-template-columns: 1fr; }
}
"""


def apply_theme():
    dark = st.session_state.get("dark_mode", True)
    color_css = DARK_CSS if dark else LIGHT_CSS
    st.markdown(f"<style>{color_css}{SHARED_CSS}</style>", unsafe_allow_html=True)
