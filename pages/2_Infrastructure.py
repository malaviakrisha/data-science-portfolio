import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.graph_objects as go

# ─── CONFIGURATION & CUSTOM STYLE LAYER ───
st.set_page_config(page_title="NASA Fleet Telemetry Overlook", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0f1116; }
    h1, h2, h3 { font-family: 'Inter', sans-serif !important; font-weight: 700 !important; }
    
    /* Fleet Control Card Specs */
    .telemetry-card {
        background: linear-gradient(145deg, #161920, #1b1f2a);
        border: 1px solid #262c3d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Playbook Command Output Styles */
    .agent-log {
        background-color: #111827;
        border-left: 4px solid #6366f1;
        padding: 12px;
        border-radius: 6px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 13px;
        color: #e5e7eb;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ NASA Turbofan Fleet Telemetry Overlook")
st.markdown("This control center monitors live data matrices across an active fleet. Select an engine unit below to replay its true historical lifecycle logs, observe real-time model predictions, and trigger prescriptive maintenance actions.")

# ─── LOGISTICS: DATA & MODEL LOADING ───
@st.cache_resource
def load_nasa_assets():
    # 1. Load Model
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "pipelines", "infrastructure_model.joblib")
    model = joblib.load(model_path) if os.path.exists(model_path) else None
    
    # 2. Fetch Real NASA Data to feed the interface directly
    url = "https://raw.githubusercontent.com/mapr-demos/predictive-maintenance/master/notebooks/jupyter/Dataset/CMAPSSData/train_FD001.txt"
    index_names = ['unit_nr', 'time_cycles']
    setting_names = ['setting_1', 'setting_2', 'setting_3']
    sensor_names = [f's_{i}' for i in range(1, 22)]
    col_names = index_names + setting_names + sensor_names
    
    df = pd.read_csv(url, sep=r"\s+", header=None, names=col_names)
    
    # Run identical feature engineering smoothing steps
    target_sensors = ['s_2', 's_3', 's_4', 's_11']
    for feature in target_sensors:
        df[f'{feature}_smoothed'] = df.groupby('unit_nr')[feature].transform(
            lambda x: x.rolling(window=5, min_periods=1).mean()
        )
    return model, df

try:
    model, fleet_df = load_nasa_assets()
except Exception as e:
    model, fleet_df = None, None

if model is None or fleet_df is None:
    st.error("❌ Fleet assets or trained model binary missing! Ensure you ran your training pipeline successfully.")
else:
    # ─── CONTROL PANEL LAYER ───
    st.sidebar.header("🛸 Fleet Navigation Control")
    
    engine_list = sorted(fleet_df['unit_nr'].unique())
    selected_unit = st.sidebar.selectbox("Select Aircraft Engine Unit", engine_list, index=3) # Default to Unit 4
    
    # Isolate data for this specific engine
    engine_df = fleet_df[fleet_df['unit_nr'] == selected_unit].copy()
    max_cycles = int(engine_df['time_cycles'].max())
    
    st.sidebar.markdown("**Engine Specs Profile:**")
    st.sidebar.info(f"• Total Logged Lifespan: {max_cycles} Cycles\n• Operational Status: Log Concluded")
    
    # Pre-calculate probabilities for the entire engine history to populate our tracking chart
    features = ['s_2_smoothed', 's_3_smoothed', 's_4_smoothed', 's_11_smoothed']
    all_prob = model.predict_proba(engine_df[features])[:, 1] * 100
    engine_df['calculated_risk'] = all_prob

    # Time-machine timeline slider
    current_cycle = st.slider("🕰️ Scrub Engine Operational Timeline (Flight Cycles)", min_value=1, max_value=max_cycles, value=1)
    
    # Extract telemetry row matching this specific cycle time step
    current_row = engine_df[engine_df['time_cycles'] == current_cycle].iloc[0]
    failure_probability = current_row['calculated_risk']
    
    # Unique Calculation: Real-time Remaining Useful Life (RUL) estimation
    projected_rul = max_cycles - current_cycle
    
    # Unique Calculation: Performance Degradation Index using mathematical formula
    # Expressing health state as a function of calculated predictive risk
    health_index = 100.0 - failure_probability

    st.markdown("---")

    # ─── ROW 1: CORE TWIN METRICS & METRIC TILES ───
    st.subheader(f"📊 Live Telemetry Twin Matrix — Cycle {current_cycle} of {max_cycles}")
    
    # Let's organize the main status points at the very top using advanced metric typography
    top_col1, top_col2, top_col3 = st.columns(3)
    with top_col1:
        st.metric(label="Estimated Remaining Useful Life (RUL)", value=f"{projected_rul} Cycles", delta=f"-{current_cycle} Accumulation", delta_color="inverse")
    with top_col2:
        st.metric(label="Calculated Health Index", value=f"{health_index:.1f}%", delta=f"-{failure_probability:.1f}% Structural Attrition", delta_color="inverse")
    with top_col3:
        st.metric(label="Asset Mission Risk", value=f"{failure_probability:.1f}%", delta="CRITICAL BREACH" if failure_probability >= 70.0 else "OPERATIONAL")

    # Dropdowns for row sensor variables
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("LPC Outlet Temp (s_2)", f"{current_row['s_2']:,.2f} °R")
    m2.metric("HPC Outlet Temp (s_3)", f"{current_row['s_3']:,.2f} °R")
    m3.metric("LPT Outlet Temp (s_4)", f"{current_row['s_4']:,.2f} °R")
    m4.metric("HPC Static Pressure (s_11)", f"{current_row['s_11']:,.2f} psia")

    st.markdown("---")

    # ─── ROW 2: DATA VISUALIZATIONS (DARK-THEME REHABILITATION) ───
    left_col, right_col = st.columns([1, 1.8])
    
    with left_col:
        # Gauge Chart Visualizer re-engineered to look like aerospace cockpit gear
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=failure_probability,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#9ca3af"},
                'bar': {'color': "#6366f1"},
                'bgcolor': "#1f2937",
                'borderwidth': 1,
                'bordercolor': "#374151",
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(16, 185, 129, 0.1)'},
                    {'range': [40, 70], 'color': 'rgba(245, 158, 11, 0.1)'},
                    {'range': [70, 100], 'color': 'rgba(239, 68, 68, 0.1)'}
                ],
                'threshold': {'line': {'color': "#ef4444", 'width': 3}, 'value': 70}
            }
        ))
        fig_gauge.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=220, 
            margin=dict(l=30, r=30, t=40, b=10)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    with right_col:
        history_slice = engine_df[engine_df['time_cycles'] <= current_cycle]
        fig_trend = go.Figure()
        
        fig_trend.add_trace(go.Scatter(
            x=engine_df['time_cycles'], 
            y=engine_df['calculated_risk'],
            mode='lines',
            name='Complete Wear Arc',
            line=dict(color='rgba(156, 163, 175, 0.25)', dash='dot')
        ))
        
        fig_trend.add_trace(go.Scatter(
            x=history_slice['time_cycles'], 
            y=history_slice['calculated_risk'],
            mode='lines',
            name='Current Progress Tracker',
            line=dict(color='#6366f1', width=3)
        ))
        
        fig_trend.add_shape(
            type="line", x0=1, y0=70, x1=max_cycles, y1=70,
            line=dict(color="#ef4444", width=1.5, dash="dash")
        )
        
        fig_trend.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Flight Operating Cycles",
            yaxis_title="Computed Model Risk %",
            yaxis=dict(range=[-5, 105], gridcolor="#262c3d"),
            xaxis=dict(gridcolor="#262c3d"),
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=10, r=10, t=10, b=10),
            height=220
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")

    # ─── UNIQUE HIGHLIGHT: AI FLEET ORCHESTRATION AGENT PLAYBOOK ───
    st.subheader("🤖 Prescriptive AI Fleet Orchestration Log")
    
    # This design leverages custom HTML encapsulation inside a clean single call to render
    # an agentic prescriptive text field dynamically responding to the timelines.
    if failure_probability < 40.0:
        playbook_html = f"""
        <div class="telemetry-card">
            <h4 style="color: #10b981; margin-top: 0; margin-bottom: 10px;">🟢 Agent Status: Routine Fleet Operations</h4>
            <div class="agent-log">[SYSTEM_AGENT]: Analysing continuous telemetry distribution streams... Sensor vectors normal.</div>
            <div class="agent-log">[LOGISTICS_AGENT]: No immediate maintenance dependencies flag. Sourcing window optimization active.</div>
            <p style="color: #e5e7eb; font-size: 14px; margin-bottom: 0; margin-top: 10px;">
                ⚙️ <strong>Prescriptive Action:</strong> Maintain current international flight assignments. Standard cycle analytics logged to cloud server database. Next automated systemic checkup recommended in 20 operating cycles.
            </p>
        </div>
        """
    elif failure_probability < 70.0:
        playbook_html = f"""
        <div class="telemetry-card">
            <h4 style="color: #f59e0b; margin-top: 0; margin-bottom: 10px;">🟡 Agent Status: Predictive Degradation Warning Triggered</h4>
            <div class="agent-log">[SYSTEM_AGENT]: Thermal metrics across compression nodes s_2 and s_3 displaying structural drift. Dev-Score: +2.4σ.</div>
            <div class="agent-log">[PROCUREMENT_AGENT]: Pre-routing hardware components (Core Seal Kit B) to major hub inventory reserves.</div>
            <p style="color: #e5e7eb; font-size: 14px; margin-bottom: 0; margin-top: 10px;">
                ⚙️ <strong>Prescriptive Action:</strong> Flag asset for routing terminal assignment through upcoming transit vectors. Automated procurement dispatch has proactively staged replacement sensor equipment at hub depot.
            </p>
        </div>
        """
    else:
        playbook_html = f"""
        <div class="telemetry-card">
            <h4 style="color: #ef4444; margin-top: 0; margin-bottom: 10px;">🔴 Agent Status: Core Emergency Intercept Mode</h4>
            <div class="agent-log">[CRITICAL_AGENT]: Unit {selected_unit} safety index degraded below threshold. Failure profile timeline converging.</div>
            <div class="agent-log">[SCHEDULING_AGENT]: Dispatching emergency task work-order #NASA-MNT-9081. Intercepting airport scheduling networks.</div>
            <p style="color: #e5e7eb; font-size: 14px; margin-bottom: 0; margin-top: 10px;">
                ⚙️ <strong>Prescriptive Action:</strong> <strong>GROUND AIRCRAFT IMMEDIATELY</strong> at terminal hub. Predictive models calculate an expected lifecycle terminal breach within {projected_rul} flight operating cycles. Emergency technicians and component replacement hardware deployed to hangar block.
            </p>
        </div>
        """
        
    st.markdown(playbook_html, unsafe_allow_html=True)