import streamlit as st
import random
from utils.predictor import HEALTHY_TIPS


def render_home():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">🌿 AI-Powered Agronomy</div>
        <div class="hero-title">Protect your crops with<br><span>instant disease detection</span></div>
        <div class="hero-sub">
            Upload a single leaf photo and get a diagnosis in under 3 seconds —
            powered by a deep-learning model trained on 87,000+ annotated plant images
            across 38 disease classes.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CTA button via Streamlit (so it actually navigates)
    if st.button("🔬  Start Detecting →", key="hero_cta", use_container_width=False):
        st.session_state.page = "Detection"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Stats ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="stats-row">
        <div class="stat-card">
            <div class="stat-value">97.4%</div>
            <div class="stat-label">Validation Accuracy</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">38</div>
            <div class="stat-label">Disease Classes</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">87K+</div>
            <div class="stat-label">Training Images</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">&lt;3s</div>
            <div class="stat-label">Inference Time</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Features ──────────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Core features</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">🔬</div>
            <div class="feature-title">Instant Diagnosis</div>
            <div class="feature-desc">ResNet-50 backbone delivers results in under 3 seconds, even on CPU.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Confidence Scoring</div>
            <div class="feature-desc">Calibrated probability scores with top-3 predictions help you understand model certainty.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">💊</div>
            <div class="feature-title">Treatment Guidance</div>
            <div class="feature-desc">Every diagnosis includes actionable treatment and prevention recommendations.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📋</div>
            <div class="feature-title">Downloadable Reports</div>
            <div class="feature-desc">Generate a full diagnostic report you can share with agronomists or input into field records.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🕒</div>
            <div class="feature-title">Prediction History</div>
            <div class="feature-desc">Every scan is logged automatically so you can track field health over time.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🌙</div>
            <div class="feature-title">Dark / Light Mode</div>
            <div class="feature-desc">Toggle themes to suit field conditions — bright sun or dim storage shed.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Supported crops ───────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Supported crops</div>', unsafe_allow_html=True)
    crops = [
        ("🍅", "Tomato", "10 diseases"),
        ("🌽", "Corn",   "4 diseases"),
        ("🍎", "Apple",  "4 diseases"),
        ("🍇", "Grape",  "4 diseases"),
        ("🥔", "Potato", "3 diseases"),
        ("🌾", "Wheat",  "4 diseases"),
        ("🌿", "Soybean","4 diseases"),
        ("🍑", "Peach",  "2 diseases"),
    ]
    cols = st.columns(len(crops))
    for col, (icon, name, count) in zip(cols, crops):
        with col:
            st.markdown(f"""
            <div style="text-align:center; padding:14px 8px;
                background:var(--bg-card); border:1px solid var(--border);
                border-radius:10px; cursor:default;">
                <div style="font-size:1.8rem">{icon}</div>
                <div style="font-size:0.82rem;font-weight:700;margin-top:6px">{name}</div>
                <div style="font-size:0.7rem;color:var(--text-muted)">{count}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Healthy tip ───────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    tip = random.choice(HEALTHY_TIPS)
    st.info(f"**Today's tip →**  {tip}")

    st.markdown('</div>', unsafe_allow_html=True)
