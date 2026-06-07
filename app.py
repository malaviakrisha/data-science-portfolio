import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Data Science Portfolio Hub",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM UI/UX CSS INJECTION ───
st.markdown("""
<style>
    .main { background-color: #0f1116; }
    h1, h2, h3 { font-family: 'Inter', sans-serif !important; font-weight: 700 !important; }

    .portfolio-card {
        background: linear-gradient(145deg, #161920, #1b1f2a);
        border: 1px solid #262c3d;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        transition: transform 0.3s ease, border-color 0.3s ease;
        min-height: 460px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .portfolio-card:hover { transform: translateY(-5px); border-color: #4f46e5; }

    .badge {
        background-color: rgba(79, 70, 229, 0.15);
        color: #818cf8;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 12px;
        border: 1px solid rgba(79, 70, 229, 0.3);
    }
    .badge-pipeline {
        background-color: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .card-title {
        color: #ffffff;
        font-size: 22px;
        margin-top: 5px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .section-label {
        color: #9ca3af;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 12px;
        margin-bottom: 4px;
        font-weight: 600;
    }
    .section-desc {
        color: #e5e7eb;
        font-size: 14px;
        line-height: 1.5;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ─── HEADER HERO SECTION ───
st.title("🚀 Data Science & Machine Learning Portfolio Hub")
st.markdown("""
Welcome to my production-grade data science project showcase. This platform hosts interactive applications
demonstrating end-to-end data pipelines, predictive modeling, and scalable MLOps architectures.
""")

st.markdown("---")

# ─── PORTFOLIO INTRODUCTION LAYOUT ───
col_left, col_right = st.columns([2.25, 1])

with col_left:
    st.subheader("👨‍💻 About the Engineer")
    st.markdown("""
Aspiring Data Scientist interested in turning data into useful insights and real-world solutions. I enjoy exploring machine learning, analytics, predictive modeling, and AI-driven systems to understand patterns in technology and human behavior. Constantly learning and experimenting with new tools and techniques, I aim to build data-driven solutions that solve practical problems and help make better decisions.

""")

with col_right:
    st.subheader("🎯 System Status")
    m1, m2 = st.columns(2)
    m1.metric(label="Data Pipelines", value="Active", delta="100%")
    m2.metric(label="DB Gateway", value="Connected", delta="Supabase")

st.markdown("---")

# ─── HELPER: build a card HTML string cleanly ───
def make_card(badge_class, badge_text, icon, title, sections: list[tuple[str, str]]) -> str:
    """
    sections: list of (label, description) tuples
    Builds the full card HTML as one compact string so Streamlit's markdown
    parser never gets a chance to escape inner tags.
    """
    rows = "".join(
        f'<p class="section-label">{lbl}</p><p class="section-desc">{desc}</p>'
        for lbl, desc in sections
    )
    return (
        f'<div class="portfolio-card">'
        f'<div>'
        f'<span class="badge {badge_class}">{badge_text}</span>'
        f'<div class="card-title">{icon} {title}</div>'
        f'{rows}'
        f'</div>'
        f'</div>'
    )


# ─── INTERACTIVE PORTFOLIO GRID ───
st.subheader("📂 Deployed Applications Overview")
card1, card2, card3 = st.columns(3)

# --- PROJECT 1: MUMBAI REAL ESTATE ---
with card1:
    st.markdown(
        make_card(
            badge_class="",
            badge_text="Real Estate Analytics",
            icon="🏠",
            title="Mumbai Price Engine",
            sections=[
                ("The Problem",
                 "Metropolitan property valuation data is highly fragmented, unstable, and prone to severe pricing anomalies and human bias."),
                ("Data Architecture",
                 "Automated scraping pipeline harvesting web data directly into an integrated cloud execution layer."),
                ("Infrastructure Matrix",
                 "GitHub Actions chron-runner executing daily scheduled updates, feeding into a secure Supabase relational network."),
                ("Core Innovation",
                 "Algorithmic Interquartile Range (IQR) filters to strip data noise, displaying real-time spatial distribution metrics."),
            ],
        ),
        unsafe_allow_html=True,
    )

# --- PROJECT 2: NASA TURBOFAN ---
with card2:
    st.markdown(
        make_card(
            badge_class="",
            badge_text="Predictive Maintenance",
            icon="⚙️",
            title="NASA Turbofan Monitor",
            sections=[
                ("The Problem",
                 "Unscheduled mechanical asset downtime compromises industrial throughput and costs manufacturing operations millions annually."),
                ("Data Architecture",
                 "NASA C-MAPSS Jet Engine Degradation datasets detailing multi-dimensional sensor metrics across temporal windows."),
                ("Infrastructure Matrix",
                 "Serialized Random Forest and regression models handling rolling window feature generation and real-time inference."),
                ("Core Innovation",
                 "Interactive, high-fidelity life-cycle playback simulation pairing remaining useful life (RUL) limits with risk dials."),
            ],
        ),
        unsafe_allow_html=True,
    )

# --- PROJECT 3: AI BIAS AUDIT ---
with card3:
    st.markdown(
        make_card(
            badge_class="badge-pipeline",
            badge_text="AI Governance &amp; Trust",
            icon="⚖️",
            title="Algorithmic Bias Auditor",
            sections=[
                ("The Problem",
                 "Production models frequently perpetuate institutional discrimination, creating hidden regulatory compliance liabilities."),
                ("Data Architecture",
                 "Protected attribute demographic profiles evaluated across live banking/credit approval scoring testbeds."),
                ("Infrastructure Matrix",
                 "Continuous validation middleware calculating real-time variance in statistical parity and historical training equity."),
                ("Core Innovation",
                 "Interactive threshold adjustment engine allowing stakeholders to actively balance predictive loss against mathematical fairness."),
            ],
        ),
        unsafe_allow_html=True,
    )