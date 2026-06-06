import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="NASA Fleet Telemetry Overlook", layout="wide")

st.title("🛡️ NASA Turbofan Fleet Telemetry Overlook")
st.markdown("This control center monitors live data matrices across an active fleet. Select an engine unit below to replay its true historical lifecycle logs and observe real-time model predictions.")

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
    
    # Dropdown to select a 100% REAL historical engine
    engine_list = sorted(fleet_df['unit_nr'].unique())
    selected_unit = st.sidebar.selectbox("Select Aircraft Engine Unit", engine_list, index=3) # Default to Unit 4
    
    # Isolate data for this specific engine
    engine_df = fleet_df[fleet_df['unit_nr'] == selected_unit].copy()
    max_cycles = int(engine_df['time_cycles'].max())
    
    st.sidebar.markdown(f"**Engine Specs Profile:**")
    st.sidebar.info(f"• Total Logged Lifespan: {max_cycles} Cycles\n• Operational Status: Log Concluded")
    
    # Pre-calculate probabilities for the entire engine history to populate our tracking chart
    features = ['s_2_smoothed', 's_3_smoothed', 's_4_smoothed', 's_11_smoothed']
    all_prob = model.predict_proba(engine_df[features])[:, 1] * 100
    engine_df['calculated_risk'] = all_prob

    # Time-machine timeline slider (Resets instantly to Cycle 1 when switching engines!)
    current_cycle = st.slider("🕰️ Scrub Engine Operational Timeline (Flight Cycles)", min_value=1, max_value=max_cycles, value=1)
    
    # Extract telemetry row matching this specific cycle time step
    current_row = engine_df[engine_df['time_cycles'] == current_cycle].iloc[0]
    failure_probability = current_row['calculated_risk']

    st.markdown("---")

    # ─── REAL-TIME TELEMETRY TELEMETRY METRIC DISPLAY ───
    st.subheader(f"📊 Telemetry Readouts — Cycle {current_cycle} of {max_cycles}")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("LPC Outlet Temp (s_2)", f"{current_row['s_2']:,.2f} °R")
    m2.metric("HPC Outlet Temp (s_3)", f"{current_row['s_3']:,.2f} °R")
    m3.metric("LPT Outlet Temp (s_4)", f"{current_row['s_4']:,.2f} °R")
    m4.metric("HPC Static Pressure (s_11)", f"{current_row['s_11']:,.2f} psia")

    st.markdown("---")

    # ─── RISK ASSESSMENT & ANALYTICAL VISUALIZATION ───
    left_col, right_col = st.columns([1, 2])
    
    with left_col:
        st.metric(label="Calculated Maintenance Failure Risk", value=f"{failure_probability:.1f}%")
        
        # Actionable Business Alerts
        if failure_probability >= 70.0:
            st.error(f"🚨 **CRITICAL RISK FLASH:** Engine Unit {selected_unit} has breached safe structural thresholds at cycle {current_cycle}. Failure predicted within 30 cycles. Grounding aircraft immediately.")
        elif failure_probability >= 40.0:
            st.warning("⚠️ **MAINTENANCE WARNING:** Structural anomalies detected in core compression matrices. Route to nearest terminal hub for sensor check.")
        else:
            st.success("✅ **PROPULSION STABLE:** Internal core performance metrics tracking cleanly within safe limits.")

        # Gauge Chart Visualizer
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=failure_probability,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Current Structural Risk %", 'font': {'size': 14}},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "navy"},
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(40, 167, 69, 0.15)'},
                    {'range': [40, 70], 'color': 'rgba(255, 193, 7, 0.15)'},
                    {'range': [70, 100], 'color': 'rgba(220, 53, 69, 0.15)'}
                ],
                'threshold': {'line': {'color': "red", 'width': 4}, 'value': 70}
            }
        ))
        fig_gauge.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with right_col:
        # Beautiful timeline tracking chart showing historical degradation up to current point
        history_slice = engine_df[engine_df['time_cycles'] <= current_cycle]
        
        fig_trend = go.Figure()
        
        # Risk projection path
        fig_trend.add_trace(go.Scatter(
            x=engine_df['time_cycles'], 
            y=engine_df['calculated_risk'],
            mode='lines',
            name='Complete Lifespan Lifecycle Risk Trajectory',
            line=dict(color='rgba(150, 150, 150, 0.3)', dash='dot')
        ))
        
        # Current progress path
        fig_trend.add_trace(go.Scatter(
            x=history_slice['time_cycles'], 
            y=history_slice['calculated_risk'],
            mode='lines',
            name='Current Flight Path Progression',
            line=dict(color='firebrick', width=3)
        ))
        
        # Target Alert line
        fig_trend.add_shape(
            type="line", x0=1, y0=70, x1=max_cycles, y1=70,
            line=dict(color="Red", width=2, dash="dashdot")
        )
        
        fig_trend.update_layout(
            title=f"Historical Wear & Failure Probability Arc for Engine #{selected_unit}",
            xaxis_title="Flight Operating Cycles (Time)",
            yaxis_title="Computed Model Risk Probability (%)",
            yaxis=dict(range=[0, 105]),
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=40, b=20),
            height=380
        )
        st.plotly_chart(fig_trend, use_container_width=True)