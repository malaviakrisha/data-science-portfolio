import streamlit as st

# Page configuration
st.set_page_config(page_title="Data Science Portfolio Hub", layout="wide")

# Main Header
st.title("🚀 Data Science & Machine Learning Portfolio Hub")
st.markdown("""
Welcome to my production-grade data science project showcase. This platform hosts interactive applications demonstrating end-to-end data pipelines, predictive modeling, and scalable MLOps architectures.
""")

st.markdown("---")

# Portfolio Introduction Layout
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("👨‍💻 About the Engineer")
    st.markdown("""
    I specialize in building software-centric AI solutions, transforming raw, messy real-world data into actionable business intelligence. 
    My engineering approach emphasizes **robust system orchestration**, clean feature engineering pipelines, and interactive analytical interfaces that bridge complex backend models with intuitive user operations.
    
    **Core Technical Competencies:**
    * **Languages & Frameworks:** Python, Streamlit, FastAPI, Pandas, NumPy
    * **Machine Learning & MLOps:** Scikit-Learn, XGBoost, Automated ETL Pipelines, Git LFS
    * **Data Architecture:** SQL, Supabase, Programmatic Web Scraping (Scrapy)
    """)

with col_right:
    st.subheader("🎯 Project Navigation Guide")
    st.markdown("""
    Use the sidebar menu on the left to seamlessly hop between the deployed applications:
    
    1. **🏠 Real Estate Market Engine:** Explore automated daily property data tracking, algorithmic outlier detection, and geospatial market visualizations.
    2. **⚙️ Infrastructure Predictive Monitor:** Review real-time aerospace-grade failure probability estimation using actual historical fleet data arrays from NASA.
    """)

st.markdown("---")

# Quick Project Summaries
st.subheader("📂 Deployed Applications Overview")

card1, card2 = st.columns(2)

with card1:
    st.info("### 🏠 Mumbai Real Estate Engine")
    st.markdown("""
    **The Problem:** Real estate data is fragmented, filled with pricing noise, and highly volatile.
    * **Data Source:** Programmatically harvested web data pipelines.
    * **Infrastructure:** GitHub Actions cloud-runner executing daily scheduled synchronization directly into a secure Supabase SQL storage matrix.
    * **Key Feature:** Algorithmic IQR filter cleaning and spatial distribution maps.
    """)

with card2:
    st.warning("### ⚙️ NASA Turbofan Core Monitor")
    st.markdown("""
    **The Problem:** Unscheduled mechanical downtime costs industries billions in lost operational uptime.
    * **Data Source:** NASA C-MAPSS Jet Engine Degradation Simulation Dataset.
    * **Infrastructure:** Serialized Random Forest predictive architecture handling multi-dimensional feature windowing.
    * **Key Feature:** Interactive historical lifecycle time-machine playback with a real-time risk gauge.
    """)