import streamlit as st
from utils.state import init_session_state
from utils.theme import apply_theme
from pages.home import render_home
from pages.detection import render_detection
from pages.model_info import render_model_info
from pages.about import render_about

st.set_page_config(
    page_title="CropGuard — Plant Disease Detection",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()
apply_theme()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span class="logo-icon">🌿</span>
        <div>
            <div class="logo-title">CropGuard</div>
            <div class="logo-sub">AI Plant Pathologist</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

    nav_items = {
        "🏠  Home":              "Home",
        "🔬  Disease Detection": "Detection",
        "🧠  Model Information": "Model Info",
        "📖  About Project":     "About",
    }

    for label, key in nav_items.items():
        active = "nav-active" if st.session_state.page == key else ""
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()

    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

    # Dark mode toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<span class='toggle-label'>Dark Mode</span>", unsafe_allow_html=True)
    with col2:
        dark = st.toggle("", value=st.session_state.dark_mode, key="dark_toggle", label_visibility="collapsed")
    if dark != st.session_state.dark_mode:
        st.session_state.dark_mode = dark
        st.rerun()

    st.markdown("<div class='sidebar-footer'>v1.0.0 · Built with ❤️ for farmers</div>", unsafe_allow_html=True)

# ── Page routing ──────────────────────────────────────────────────────────────
page = st.session_state.page
if page == "Home":
    render_home()
elif page == "Detection":
    render_detection()
elif page == "Model Info":
    render_model_info()
elif page == "About":
    render_about()
