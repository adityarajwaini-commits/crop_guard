import streamlit as st


def render_about():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📖 About CropGuard</div>', unsafe_allow_html=True)

    # ── Mission ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero" style="padding:36px 40px;margin-bottom:24px">
        <div class="hero-badge">Our Mission</div>
        <div class="hero-title" style="font-size:2rem">
            Giving every farmer a plant pathologist<br>
            <span>in their pocket</span>
        </div>
        <div class="hero-sub">
            700 million smallholder farmers worldwide lose up to 40% of crop yields to diseases every year.
            CropGuard uses state-of-the-art computer vision to put expert-level diagnosis on any smartphone —
            no internet required for inference, no expensive laboratory needed.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Problem / Solution ────────────────────────────────────────────────────
    col_p, col_s = st.columns(2, gap="large")
    with col_p:
        st.markdown("""
        <div class="info-panel">
            <div class="info-panel-title" style="color:var(--danger)">😔 The problem</div>
            <ul>
                <li>Late disease identification leads to crop loss of 20–40%</li>
                <li>Expert agronomists are scarce in rural areas</li>
                <li>Chemical overuse increases costs and environmental damage</li>
                <li>Smallholders lack access to diagnostics tools</li>
                <li>Disease outbreaks can cascade across entire regions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_s:
        st.markdown("""
        <div class="info-panel">
            <div class="info-panel-title green">✅ Our solution</div>
            <ul>
                <li>Sub-3-second AI diagnosis from a single leaf photo</li>
                <li>97.4% accuracy across 38 disease classes</li>
                <li>Actionable treatment guidance — no agronomy degree required</li>
                <li>Works offline after model download (planned feature)</li>
                <li>Free, open-source, and built for global deployment</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # ── Tech stack ────────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading" style="margin-top:8px">Technology stack</div>', unsafe_allow_html=True)

    stack = [
        ("🤖", "PyTorch",     "Deep learning framework for model training and inference"),
        ("🏗️", "ResNet-50",   "Pre-trained backbone fine-tuned on PlantVillage dataset"),
        ("🖥️", "Streamlit",   "Rapid web application framework for ML prototypes & products"),
        ("📊", "Plotly",      "Interactive charts for confidence scores and training curves"),
        ("🖼️", "Pillow",      "Image preprocessing and augmentation pipeline"),
        ("📦", "NumPy",       "Numerical computing for inference post-processing"),
    ]

    cols = st.columns(3)
    for i, (icon, name, desc) in enumerate(stack):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{name}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Roadmap ───────────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading" style="margin-top:24px">Product roadmap</div>', unsafe_allow_html=True)

    phases = [
        ("v1.0 · Now",        "accent", ["Leaf image classification (38 classes)", "Diagnosis reports", "Prediction history", "Treatment recommendations"]),
        ("v1.5 · Q3 2025",    "warn",   ["Mobile app (React Native)", "Offline inference (TFLite)", "Multi-language support (Hindi, Swahili, Spanish)", "Weather-integrated risk forecasting"]),
        ("v2.0 · Q1 2026",    "info",   ["Whole-plant / field-level detection", "Drone image integration", "Agronomist marketplace", "API for third-party integration"]),
    ]

    road_cols = st.columns(3)
    for col, (phase, color_key, items) in zip(road_cols, phases):
        with col:
            color_map = {"accent": "var(--accent)", "warn": "var(--warn)", "info": "var(--info)"}
            color = color_map[color_key]
            items_html = "".join(f"<li>{it}</li>" for it in items)
            st.markdown(f"""
            <div class="info-panel" style="height:100%">
                <div class="info-panel-title" style="color:{color}">{phase}</div>
                <ul>{items_html}</ul>
            </div>
            """, unsafe_allow_html=True)

    # ── Team ──────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading" style="margin-top:24px">Team</div>', unsafe_allow_html=True)

    team = [
        ("👩‍💻", "Priya Sharma",    "ML Engineer",       "Trained the ResNet model; leads model evaluation pipeline"),
        ("👨‍🌾", "Arjun Patel",     "Domain Expert",      "Plant pathologist; curated dataset and validated predictions"),
        ("👩‍🎨", "Mei Lin",         "Product Designer",  "UX research, wireframing, and interface design"),
        ("👨‍💻", "Carlos Reyes",    "Full-Stack Dev",     "Streamlit app, backend API, and deployment infrastructure"),
    ]
    team_cols = st.columns(4)
    for col, (avatar, name, role, desc) in zip(team_cols, team):
        with col:
            st.markdown(f"""
            <div class="team-card">
                <div class="team-avatar">{avatar}</div>
                <div class="team-name">{name}</div>
                <div class="team-role">{role}</div>
                <div style="font-size:0.75rem;color:var(--text-muted);margin-top:8px;line-height:1.5">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Citations / acknowledgements ──────────────────────────────────────────
    st.markdown('<div class="section-heading" style="margin-top:24px">Acknowledgements</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-panel">
        <div class="info-panel-title blue">Dataset & Research</div>
        <ul>
            <li><strong>PlantVillage Dataset</strong> — Hughes, D. P., & Salathé, M. (2015). An open access repository of images of healthy and diseased crop plants. <em>arXiv:1511.08060</em></li>
            <li><strong>ResNet</strong> — He, K. et al. (2016). Deep residual learning for image recognition. <em>CVPR 2016</em></li>
            <li>USDA National Plant Diagnostic Network for disease reference material</li>
            <li>FAO global crop loss statistics (2023 report)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ── License / links ───────────────────────────────────────────────────────
    st.markdown("""
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:4px">
        <a href="https://github.com/your-org/cropguard"
           style="display:inline-block;background:var(--bg-card);border:1px solid var(--border);
                  border-radius:8px;padding:8px 16px;font-size:0.82rem;font-weight:600;
                  color:var(--text-secondary);text-decoration:none">
            🐙 GitHub
        </a>
        <a href="#"
           style="display:inline-block;background:var(--bg-card);border:1px solid var(--border);
                  border-radius:8px;padding:8px 16px;font-size:0.82rem;font-weight:600;
                  color:var(--text-secondary);text-decoration:none">
            📄 MIT Licence
        </a>
        <a href="#"
           style="display:inline-block;background:var(--bg-card);border:1px solid var(--border);
                  border-radius:8px;padding:8px 16px;font-size:0.82rem;font-weight:600;
                  color:var(--text-secondary);text-decoration:none">
            📧 Contact us
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
