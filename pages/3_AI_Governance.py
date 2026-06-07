import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Governance & Bias Audit", layout="wide")

# ─── CUSTOM UI/UX CSS INJECTION ───
st.markdown("""
<style>
    .main { background-color: #0f1116; }
    h1, h2, h3 { font-family: 'Inter', sans-serif !important; font-weight: 700 !important; }
    
    /* Control Panel Card */
    .control-card {
        background: linear-gradient(145deg, #161920, #1b1f2a);
        border: 1px solid #262c3d;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    
    /* Meta text styling */
    .custom-label {
        color: #9ca3af;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER HERO SECTION ---
st.title("⚖️ AI Governance: Algorithmic Bias Audit")
st.markdown("""
**The Challenge:** Machine learning models trained on historical data frequently inherit systemic human prejudices. 
In this audit of an automated recruitment/income evaluation engine, the baseline model exhibited severe systemic bias against the unprivileged demographic group, failing the regulatory **Disparate Impact** compliance threshold of 0.80.

**The Solution:** Instead of discarding the model entirely, we inject an **Automated Post-Processing Mitigation** layer. 
Interact with the fully extended threshold controller below to act as the compliance gatekeeper—adjusting decision boundaries to balance mathematical fairness against overall organizational predictive accuracy.
""")

st.markdown("---")

# --- CORE BACKEND SIMULATION LOGIC ---
# Moving the logic up allows us to use the outputs inside our layout structure seamlessly
# The slider now spans the full, natural visual track (0.0 to 1.0)
threshold = st.slider(
    "Unprivileged Group Classification Threshold", 
    min_value=0.00, 
    max_value=1.00, 
    value=0.50, 
    step=0.01,
    help="Adjust the probability threshold required for a positive system prediction."
)

# Robust mathematical simulation handling both mitigation (<0.50) and aggravated bias (>0.50)
baseline_di = 0.413
baseline_acc = 86.01

if threshold <= 0.50:
    # Mitigation zone: lowering threshold improves fairness, minor hit to accuracy
    tuning_factor = (0.50 - threshold) / 0.50
    current_di = baseline_di + (tuning_factor * 0.587)  # Scales up to 1.0
    current_acc = baseline_acc - (tuning_factor * 3.2)
else:
    # Aggravation zone: raising threshold destroys fairness entirely
    tuning_factor = (threshold - 0.50) / 0.50
    current_di = baseline_di - (tuning_factor * baseline_di)  # Scales down to 0.0
    current_acc = baseline_acc - (tuning_factor * 15.0)       # Drops drastically as approvals bottleneck

is_compliant = current_di >= 0.80

# --- INTERACTIVE PANEL LAYOUT ---
col_controls, col_metrics = st.columns([1.2, 2])

with col_controls:
    # 1. Process custom HTML alerting structures based on the threshold dynamic state
    if threshold == 0.50:
        status_html = """
        <div style="background-color: rgba(28, 140, 240, 0.1); border-left: 4px solid #1c8cf0; padding: 14px; border-radius: 8px; color: #a3d2f9; font-size: 14px; line-height: 1.5;">
            ℹ️ <strong>Standard Baseline:</strong> The model is running on standard unadjusted parameters. Bias is active.
        </div>
        """
    elif threshold < 0.50:
        status_html = """
        <div style="background-color: rgba(16, 185, 129, 0.1); border-left: 4px solid #10b981; padding: 14px; border-radius: 8px; color: #a7f3d0; font-size: 14px; line-height: 1.5;">
            ✨ <strong>Mitigation Layer Active:</strong> Lowering the threshold to grant equitable access.
        </div>
        """
    else:
        status_html = """
        <div style="background-color: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; padding: 14px; border-radius: 8px; color: #fca5a5; font-size: 14px; line-height: 1.5;">
            ⚠️ <strong>Bias Amplified:</strong> Raising the threshold further restricts the unprivileged demographic.
        </div>
        """

    # 2. Render the ENTIRE structural layout inside a unified markdown block
    st.markdown(f"""
    <div class="control-card">
        <h3 style="color: white; margin-top: 0; font-size: 20px; margin-bottom: 12px; font-family: 'Inter', sans-serif;">🎛️ Governance Parameter</h3>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(status_html, unsafe_allow_html=True)

with col_metrics:
    st.subheader("📊 Live Audit Metrics")
    metric_col1, metric_col2 = st.columns(2)
    
    with metric_col1:
        st.metric(
            label="Overall Pipeline Accuracy", 
            value=f"{current_acc:.2f}%", 
            delta=f"{(current_acc - baseline_acc):.2f}%" if threshold != 0.50 else "Baseline Matrix",
            delta_color="normal" if current_acc >= baseline_acc else "inverse"
        )
        
    with metric_col2:
        st.metric(
            label="Disparate Impact Ratio", 
            value=f"{current_di:.3f}", 
            delta="COMPLIANT (Passes 80% Rule)" if is_compliant else "NON-COMPLIANT (Biased)",
            delta_color="normal" if is_compliant else "inverse"
        )

st.markdown("---")

# --- VISUALIZATION: ULTRACLEAN DARK GAUGE ---
st.subheader("🛡️ Gatekeeper Audit Monitoring Window")

# High-fidelity indicator mapping out the compliance cliff
fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = current_di,
    domain = {'x': [0, 1], 'y': [0, 1]},
    gauge = {
        'axis': {'range': [0, 1.0], 'tickwidth': 1, 'tickcolor': "#9ca3af"},
        'bar': {'color': "#6366f1"}, # Elegant indigo tracking bar
        'bgcolor': "#1f2937",
        'borderwidth': 1,
        'bordercolor': "#374151",
        'steps': [
            {'range': [0, 0.80], 'color': "rgba(239, 68, 68, 0.15)"},  # Translucent muted red
            {'range': [0.80, 1.0], 'color': "rgba(16, 185, 129, 0.15)"} # Translucent muted green
        ],
        'threshold': {
            'line': {'color': "#f59e0b", 'width': 3}, # Amber warning line
            'thickness': 0.8,
            'value': 0.80
        }
    }
))

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    height=280, 
    margin=dict(l=40, r=40, t=40, b=20)
)

st.plotly_chart(fig, use_container_width=True)

# Dynamic alert notifications acting as deployment gates
if is_compliant:
    st.success(f"🚨 **DEPLOYMENT AUTHORIZED:** The customized mitigation threshold of **{threshold:.2f}** satisfies regulatory compliance guidelines. Disparate Impact verification logged successfully.")
else:
    st.error(f"🚨 **DEPLOYMENT BLOCKED:** System metric validation failed. Current evaluation ratio ({current_di:.3f}) falls below the critical legal minimum threshold of 0.800.")