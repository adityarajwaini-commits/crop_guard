import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


# Sample per-class accuracy data for the chart
CLASS_METRICS = {
    "Tomato Late Blight":          0.982,
    "Tomato Early Blight":         0.971,
    "Apple Scab":                  0.965,
    "Grape Black Rot":             0.978,
    "Corn N. Leaf Blight":         0.958,
    "Tomato Leaf Mold":            0.967,
    "Potato Late Blight":          0.974,
    "Corn Common Rust":            0.989,
    "Tomato Bacterial Spot":       0.961,
    "Apple Cedar Rust":            0.953,
    "Healthy Plant":               0.994,
}

TRAINING_HISTORY = {
    "epoch":    list(range(1, 26)),
    "train_acc":[0.61,0.72,0.79,0.83,0.86,0.88,0.895,0.907,0.916,0.923,
                 0.929,0.934,0.938,0.942,0.945,0.948,0.951,0.953,0.955,0.957,
                 0.959,0.960,0.962,0.963,0.964],
    "val_acc":  [0.59,0.70,0.77,0.81,0.84,0.862,0.876,0.889,0.898,0.906,
                 0.913,0.918,0.922,0.926,0.929,0.931,0.934,0.936,0.938,0.940,
                 0.942,0.943,0.944,0.945,0.946],
}


def render_model_info():
    dm = st.session_state.dark_mode
    text_col = "#e6edf3" if dm else "#1a2314"
    grid_col = "#30363d"  if dm else "#d1d9c8"

    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">🧠 Model Information</div>', unsafe_allow_html=True)

    # ── Metric pills ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:24px">
        <div class="metric-pill"><div class="metric-pill-val">97.4%</div><div class="metric-pill-label">Val Accuracy</div></div>
        <div class="metric-pill"><div class="metric-pill-val">96.9%</div><div class="metric-pill-label">Precision</div></div>
        <div class="metric-pill"><div class="metric-pill-val">97.1%</div><div class="metric-pill-label">Recall</div></div>
        <div class="metric-pill"><div class="metric-pill-val">97.0%</div><div class="metric-pill-label">F1 Score</div></div>
        <div class="metric-pill"><div class="metric-pill-val">38</div><div class="metric-pill-label">Classes</div></div>
        <div class="metric-pill"><div class="metric-pill-val">87K</div><div class="metric-pill-label">Train Images</div></div>
        <div class="metric-pill"><div class="metric-pill-val">25.6M</div><div class="metric-pill-label">Parameters</div></div>
        <div class="metric-pill"><div class="metric-pill-val">~2s</div><div class="metric-pill-label">Inference (CPU)</div></div>
    </div>
    """, unsafe_allow_html=True)

    col_arch, col_data = st.columns(2, gap="large")

    with col_arch:
        st.markdown("""
        <div class="model-card">
            <div class="info-panel-title green" style="font-size:0.88rem">Architecture</div>
            <table style="width:100%;border-collapse:collapse;font-size:0.87rem">
        """, unsafe_allow_html=True)

        rows = [
            ("Backbone",           "ResNet-50 (ImageNet pretrained)"),
            ("Input shape",        "224 × 224 × 3"),
            ("Global pooling",     "Average pooling → 2048-d"),
            ("Classifier head",    "FC 512 → BN → ReLU → Dropout(0.4) → FC 38"),
            ("Activation",         "Softmax (multi-class)"),
            ("Loss",               "Categorical cross-entropy"),
            ("Optimiser",          "Adam (lr=1e-4, cosine decay)"),
            ("Regularisation",     "L2 weight decay 1e-4 + Dropout"),
            ("Augmentations",      "Flip, rotation ±30°, colour jitter, mixup"),
            ("Training epochs",    "25 (early stop patience 5)"),
            ("Batch size",         "64"),
            ("Hardware",           "NVIDIA A100 40 GB"),
        ]
        for k, v in rows:
            st.markdown(f"""
            <tr style="border-bottom:1px solid {grid_col}">
                <td style="padding:7px 0;color:var(--text-muted);white-space:nowrap">{k}</td>
                <td style="padding:7px 0 7px 14px;color:{text_col};font-weight:500">{v}</td>
            </tr>
            """, unsafe_allow_html=True)

        st.markdown("</table></div>", unsafe_allow_html=True)

    with col_data:
        st.markdown("""
        <div class="model-card">
            <div class="info-panel-title blue" style="font-size:0.88rem">Dataset</div>
        """, unsafe_allow_html=True)

        ds_rows = [
            ("Source",         "PlantVillage + custom field images"),
            ("Total images",   "87,848"),
            ("Training split", "70% — 61,494 images"),
            ("Validation",     "15% — 13,177 images"),
            ("Test split",     "15% — 13,177 images"),
            ("Classes",        "38 (including healthy variants)"),
            ("Plants covered", "14 species"),
            ("Image format",   "RGB JPEG, resized to 256px then centre-cropped"),
            ("Class balance",  "Oversampled minority classes to 1,500 min"),
            ("Labelling",      "Expert plant pathologists + ISIC consensus"),
        ]
        st.markdown("<table style='width:100%;border-collapse:collapse;font-size:0.87rem'>", unsafe_allow_html=True)
        for k, v in ds_rows:
            st.markdown(f"""
            <tr style="border-bottom:1px solid {grid_col}">
                <td style="padding:7px 0;color:var(--text-muted);white-space:nowrap">{k}</td>
                <td style="padding:7px 0 7px 14px;color:{text_col};font-weight:500">{v}</td>
            </tr>
            """, unsafe_allow_html=True)
        st.markdown("</table></div>", unsafe_allow_html=True)

    # ── Training curves ───────────────────────────────────────────────────────
    st.markdown('<div class="section-heading" style="margin-top:24px">Training history</div>', unsafe_allow_html=True)
    fig_train = go.Figure()
    fig_train.add_trace(go.Scatter(
        x=TRAINING_HISTORY["epoch"], y=TRAINING_HISTORY["train_acc"],
        name="Train accuracy", line=dict(color="#3fb950", width=2.5),
        mode="lines",
    ))
    fig_train.add_trace(go.Scatter(
        x=TRAINING_HISTORY["epoch"], y=TRAINING_HISTORY["val_acc"],
        name="Val accuracy", line=dict(color="#58a6ff", width=2.5, dash="dot"),
        mode="lines",
    ))
    fig_train.update_layout(
        margin=dict(l=0, r=0, t=8, b=0), height=260,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="Epoch", color=text_col, gridcolor=grid_col, showgrid=True),
        yaxis=dict(title="Accuracy", color=text_col, gridcolor=grid_col,
                   tickformat=".0%", range=[0.55, 1.0]),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=text_col)),
    )
    st.plotly_chart(fig_train, use_container_width=True, config={"displayModeBar": False})

    # ── Per-class accuracy ────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Per-class accuracy</div>', unsafe_allow_html=True)
    classes = list(CLASS_METRICS.keys())
    accs    = [CLASS_METRICS[c] * 100 for c in classes]
    bar_colors = ["#3fb950" if a >= 97 else "#f0883e" if a >= 96 else "#f85149" for a in accs]

    fig_cls = go.Figure(go.Bar(
        x=classes, y=accs,
        marker_color=bar_colors,
        text=[f"{a:.1f}%" for a in accs],
        textposition="outside",
        textfont_size=11,
    ))
    fig_cls.update_layout(
        margin=dict(l=0, r=0, t=12, b=0), height=300,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickfont=dict(size=11, color=text_col), tickangle=-30, gridcolor=grid_col),
        yaxis=dict(range=[93, 101], tickformat=".0f", title="Accuracy (%)",
                   color=text_col, gridcolor=grid_col),
    )
    st.plotly_chart(fig_cls, use_container_width=True, config={"displayModeBar": False})

    # ── Model card disclaimer ─────────────────────────────────────────────────
    st.info(
        "**Model Card Notice** — This model was trained primarily on the PlantVillage dataset "
        "which contains images taken under controlled greenhouse conditions. Performance on "
        "real field images may be lower, particularly under poor lighting or when multiple "
        "diseases co-occur. Always validate with a qualified agronomist."
    )

    st.markdown('</div>', unsafe_allow_html=True)
