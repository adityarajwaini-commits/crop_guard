import io
import base64
from datetime import datetime

import streamlit as st
import plotly.graph_objects as go

from utils.predictor import mock_predict, get_confidence_color, get_severity_badge, HEALTHY_TIPS
from utils.report import generate_report


# ── helpers ───────────────────────────────────────────────────────────────────
def _img_b64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode()


def _confidence_bar(label: str, value: float, color: str):
    pct  = f"{value*100:.1f}%"
    fill = f"{value*100:.2f}%"
    st.markdown(f"""
    <div class="confidence-bar-wrap">
        <div class="confidence-label"><span>{label}</span><span>{pct}</span></div>
        <div class="confidence-track">
            <div class="confidence-fill" style="width:{fill};background:{color}"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _top3_chart(top3: list):
    diseases = [d.replace(" ", "<br>") for d, _ in top3]
    confs    = [c * 100 for _, c in top3]
    colors   = [get_confidence_color(c / 100) for c in confs]

    fig = go.Figure(go.Bar(
        x=confs, y=diseases,
        orientation="h",
        marker_color=colors,
        text=[f"{c:.1f}%" for c in confs],
        textposition="outside",
        textfont_size=13,
    ))
    fig.update_layout(
        margin=dict(l=0, r=60, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            range=[0, 110],
            showgrid=False, zeroline=False,
            showticklabels=False,
            color="#8b949e",
        ),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(size=12),
            color="#e6edf3" if st.session_state.dark_mode else "#1a2314",
        ),
        height=180,
        bargap=0.35,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _history_panel():
    history = st.session_state.prediction_history
    if not history:
        st.info("No scans yet. Upload a leaf image to get started.")
        return

    if st.button("🗑  Clear history", key="clear_hist"):
        st.session_state.prediction_history = []
        st.rerun()

    for item in reversed(history[-20:]):       # latest first, cap at 20
        conf  = item["confidence"]
        color = get_confidence_color(conf)
        st.markdown(f"""
        <div class="hist-row">
            <img class="hist-thumb"
                 src="data:image/jpeg;base64,{item['thumb']}"
                 alt="leaf thumbnail"/>
            <div>
                <div class="hist-disease">{item['disease']}</div>
                <div class="hist-meta">🌱 {item['plant']} &nbsp;·&nbsp; 🕒 {item['timestamp']}</div>
            </div>
            <div class="hist-conf" style="color:{color}">{conf*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)


# ── main page ─────────────────────────────────────────────────────────────────
def render_detection():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">🔬 Disease Detection</div>', unsafe_allow_html=True)

    tab_scan, tab_hist = st.tabs(["📷  New Scan", "🕒  Prediction History"])

    # ── NEW SCAN ──────────────────────────────────────────────────────────────
    with tab_scan:
        col_up, col_res = st.columns([1, 1.1], gap="large")

        with col_up:
            st.markdown("""
            <div class="info-panel" style="margin-bottom:16px">
                <div class="info-panel-title blue">How to get the best results</div>
                <ul>
                    <li>Photograph a single leaf against a plain background</li>
                    <li>Ensure the lesion / affected area is in the frame</li>
                    <li>Use natural daylight; avoid harsh shadows</li>
                    <li>Accepted formats: JPG, PNG, WEBP (max 10 MB)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

            uploaded = st.file_uploader(
                "Upload leaf image",
                type=["jpg", "jpeg", "png", "webp"],
                label_visibility="collapsed",
                key="leaf_upload",
            )

            if uploaded:
                image_bytes = uploaded.read()
                st.image(image_bytes, caption="Uploaded leaf", use_container_width=True)

                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔬  Analyse Leaf", type="primary", use_container_width=True):
                    with st.spinner("Running inference…"):
                        result = mock_predict(image_bytes)
                    result["image_bytes"] = image_bytes
                    result["image_name"]  = uploaded.name
                    st.session_state.last_prediction = result

                    # save to history (thumbnail only)
                    st.session_state.prediction_history.append({
                        "disease":    result["disease"],
                        "confidence": result["confidence"],
                        "plant":      result["info"]["plant"],
                        "timestamp":  result["timestamp"],
                        "thumb":      _img_b64(image_bytes),
                    })
                    st.rerun()
            else:
                st.markdown("""
                <div class="upload-zone">
                    <div class="upload-icon">🍃</div>
                    <div class="upload-title">Drag & drop your leaf image here</div>
                    <div class="upload-hint">or click the area above to browse files</div>
                </div>
                """, unsafe_allow_html=True)

        # ── RESULTS PANEL ──────────────────────────────────────────────────
        with col_res:
            pred = st.session_state.get("last_prediction")
            if not pred:
                st.markdown("""
                <div style="height:420px;display:flex;flex-direction:column;
                     align-items:center;justify-content:center;
                     background:var(--bg-card);border:1px solid var(--border);
                     border-radius:14px;color:var(--text-muted);gap:12px;">
                    <div style="font-size:2.5rem">🌿</div>
                    <div style="font-size:0.95rem;font-weight:600">Results will appear here</div>
                    <div style="font-size:0.8rem">Upload an image and click Analyse</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                info     = pred["info"]
                conf     = pred["confidence"]
                bar_col  = get_confidence_color(conf)
                badge_html = get_severity_badge(info["severity"])

                # ── Primary card ──────────────────────────────────────────
                st.markdown(f"""
                <div class="pred-card">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start">
                        <div>
                            <div class="pred-disease">{pred['disease']}</div>
                            <div class="pred-plant">Host: {info['plant']} &nbsp;·&nbsp; {info['pathogen']}</div>
                        </div>
                        {badge_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # ── Confidence bar ────────────────────────────────────────
                st.markdown('<div class="pred-card" style="padding:18px 24px">', unsafe_allow_html=True)
                st.markdown('<div style="font-size:0.8rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px">Model confidence</div>', unsafe_allow_html=True)
                _confidence_bar(pred["disease"], conf, bar_col)
                st.markdown("</div>", unsafe_allow_html=True)

                # ── Top-3 chart ──────────────────────────────────────────
                st.markdown('<div class="section-heading" style="margin-top:8px">Top 3 predictions</div>', unsafe_allow_html=True)
                _top3_chart(pred["top3"])

                # ── Description / Symptoms ────────────────────────────────
                with st.expander("📄 Disease description & symptoms", expanded=True):
                    st.markdown(f"<div style='font-size:0.88rem;color:var(--text-secondary);line-height:1.65'>{info['description']}</div>", unsafe_allow_html=True)
                    st.markdown("<br>**Observed symptoms:**", unsafe_allow_html=True)
                    for s in info["symptoms"]:
                        st.markdown(f"- {s}")

                # ── Treatment ─────────────────────────────────────────────
                with st.expander("💊 Recommended treatment", expanded=False):
                    st.markdown("""
                    <div class="info-panel">
                        <div class="info-panel-title orange">Treatment steps</div>
                        <ul>
                    """ + "".join(f"<li>{t}</li>" for t in info["treatment"]) + """
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

                # ── Prevention ────────────────────────────────────────────
                with st.expander("🛡 Prevention measures", expanded=False):
                    st.markdown("""
                    <div class="info-panel">
                        <div class="info-panel-title green">Prevention strategies</div>
                        <ul>
                    """ + "".join(f"<li>{p}</li>" for p in info["prevention"]) + """
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

                # ── Download report ───────────────────────────────────────
                report_text = generate_report(pred, pred.get("image_name", "leaf.jpg"))
                st.download_button(
                    label="📥  Download Diagnostic Report",
                    data=report_text.encode("utf-8"),
                    file_name=f"cropguard_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    use_container_width=True,
                    key="dl_report",
                )

    # ── HISTORY ───────────────────────────────────────────────────────────────
    with tab_hist:
        st.markdown('<div class="section-heading">🕒 Prediction history</div>', unsafe_allow_html=True)
        _history_panel()

    # ── Healthy tips ──────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-heading">🌱 Healthy plant tips</div>', unsafe_allow_html=True)

    tip_cols = st.columns(2)
    for i, tip in enumerate(HEALTHY_TIPS):
        with tip_cols[i % 2]:
            st.markdown(f"""
            <div class="info-panel" style="margin-bottom:10px">
                <div style="font-size:0.87rem;color:var(--text-secondary);line-height:1.55">{tip}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
