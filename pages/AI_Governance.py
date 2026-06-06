import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Governance & Bias Audit", layout="wide")

st.title("⚖️ AI Governance: Algorithmic Bias Audit")
st.markdown("""
**The Challenge:** Machine learning models trained on historical data often inherit systemic biases. 
In this audit of an Income Prediction algorithm, the baseline model exhibited severe bias against the unprivileged demographic, failing the legal **Disparate Impact** threshold of 0.80.

**The Solution:** Instead of discarding the model, we implemented an **Automated Post-Processing Mitigation** layer. 
Use the slider below to act as the "Gatekeeper"—adjusting the decision threshold to force mathematical fairness, and observe the resulting impact on overall business accuracy.
""")

st.markdown("---")

# --- INTERACTIVE CONTROLS ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🎛️ Mitigation Tuning")
    st.markdown("Lowering the threshold for the unprivileged group counteracts historical dataset bias.")
    
    # The Slider: Starts at standard 0.50, goes down to 0.05
    threshold = st.slider(
        "Unprivileged Group Threshold", 
        min_value=0.05, 
        max_value=0.50, 
        value=0.50, 
        step=0.01,
        help="Adjust the probability threshold required for a positive prediction."
    )
    
    # Mathematical simulation of the Colab Auto-Tuner results for instantaneous UI rendering
    # As threshold drops, Fairness (DI) goes up, but Accuracy drops slightly.
    baseline_di = 0.413
    baseline_acc = 86.01
    
    # Calculate dynamic metrics
    tuning_factor = (0.50 - threshold) / 0.45
    current_di = baseline_di + (tuning_factor * 0.55)
    current_acc = baseline_acc - (tuning_factor * 2.8)

    # Compliance Gatekeeper Logic
    is_compliant = current_di >= 0.80

with col2:
    st.subheader("📊 Live Audit Metrics")
    
    metric_col1, metric_col2 = st.columns(2)
    
    with metric_col1:
        st.metric(
            label="Overall Pipeline Accuracy", 
            value=f"{current_acc:.2f}%", 
            delta=f"{(current_acc - baseline_acc):.2f}%" if threshold < 0.50 else "Baseline",
            delta_color="normal"
        )
        
    with metric_col2:
        st.metric(
            label="Disparate Impact Ratio", 
            value=f"{current_di:.3f}", 
            delta="COMPLIANT" if is_compliant else "BIASED",
            delta_color="normal" if is_compliant else "inverse"
        )

# --- VISUALIZATION: THE FAIRNESS GAUGE ---
st.markdown("### 🛡️ Gatekeeper Status")

# Create a Plotly Gauge to make the "Compliance" aspect highly visual
fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = current_di,
    title = {'text': "Disparate Impact (Legal Minimum: 0.80)"},
    domain = {'x': [0, 1], 'y': [0, 1]},
    gauge = {
        'axis': {'range': [0, 1.2]},
        'bar': {'color': "darkblue"},
        'steps': [
            {'range': [0, 0.799], 'color': "lightcoral"},
            {'range': [0.80, 1.2], 'color': "lightgreen"}
        ],
        'threshold': {
            'line': {'color': "black", 'width': 4},
            'thickness': 0.75,
            'value': 0.80
        }
    }
))

fig.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20))
st.plotly_chart(fig, use_container_width=True)

if is_compliant:
    st.success("✅ **DEPLOYMENT APPROVED:** The mitigation threshold has successfully balanced the demographic outcomes. The model passes the fairness audit.")
else:
    st.error("🚨 **DEPLOYMENT BLOCKED:** The model's Disparate Impact Ratio is below 0.80. Adjust the threshold to achieve compliance.")