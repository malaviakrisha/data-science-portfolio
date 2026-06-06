import streamlit as st

st.set_page_config(
    page_title="Data Science Portfolio",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data Science Hub")
st.subheader("Welcome to my professional portfolio.")

st.markdown("""
This platform hosts my industry-grade data science and engineering projects. 
Please use the sidebar to navigate through the interactive applications:

* **🏠 Mumbai Real Estate Engine:** An automated data pipeline and analytics dashboard.
* **⚙️ Infrastructure Monitor:** Predictive maintenance modeling using time-series sensor data.
* **⚖️ Bias Audit:** An algorithmic fairness analyzer for machine learning models.
""")

st.info("👈 Select a project from the sidebar to begin.")