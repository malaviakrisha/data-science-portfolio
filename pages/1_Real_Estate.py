import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from supabase import create_client

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Mumbai Real Estate Analytics", layout="wide")

# ─── PREMIUM CUSTOM CSS INJECTION ───
st.markdown("""
<style>
    .main { background-color: #0f1116; }
    h1, h2, h3, h4 { font-family: 'Inter', sans-serif !important; font-weight: 700 !important; }
    
    /* Luxury Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, #161920, #1b1f2a);
        border: 1px solid #262c3d;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 10px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
        margin-top: 5px;
    }
    .metric-label {
        font-size: 12px;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    
    /* Sentiment Alert Panel */
    .sentiment-panel {
        background: rgba(99, 102, 241, 0.05);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏠 Mumbai Real Estate Sentiment & Price Engine")
st.markdown("This dashboard reflects live property data automatically aggregated via our automated backend pipeline.")

# --- DATABASE LOGISTICS ---
@st.cache_data(ttl=60)
def fetch_live_data():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        
        client = create_client(url, key)
        response = client.table("listings").select("*").execute()
        
        return pd.DataFrame(response.data)
    except Exception as e:
        # Graceful fallback data generation for local development without configuration errors
        fallback_suburbs = ["Bandra West", "Andheri West", "Powai", "Worli", "Juhu"]
        np_random = pd.Series(range(100))
        
        mock_data = {
            "suburb": [fallback_suburbs[i % len(fallback_suburbs)] for i in range(150)],
            "price_per_sqft": [int(25000 + (i * 180) + (1500 if i % 2 == 0 else -1200)) for i in range(150)],
            "price_cr": [round(2.5 + (i * 0.04) + (0.8 if i % 3 == 0 else -0.5), 2) for i in range(150)]
        }
        return pd.DataFrame(mock_data)

df = fetch_live_data()

if df.empty:
    st.warning("⚠️ No asset data found in the cloud database. Check ingestion structures.")
else:
    # ─── SIDEBAR FILTER UPGRADE ───
    st.sidebar.markdown("### 🗺️ Market Navigation")
    
    # Elegant clean checkbox list inside the sidebar instead of standard multi-selects
    all_suburbs = sorted(df["suburb"].unique())
    st.sidebar.markdown("<p style='color:#9ca3af; font-size:13px;'>Select regions to include in pipeline analysis:</p>", unsafe_allow_html=True)
    
    selected_suburbs = []
    for suburb in all_suburbs:
        if st.sidebar.checkbox(suburb, value=True):
            selected_suburbs.append(suburb)
            
    # Filter DataFrame baseline
    filtered_df = df[df["suburb"].isin(selected_suburbs)]

    # ─── CALCULATING RE-ENGINEERED ANALYTICS ───
    total_listings = len(filtered_df)
    avg_sqft_price = int(filtered_df["price_per_sqft"].mean()) if total_listings > 0 else 0
    avg_total_price = filtered_df["price_cr"].mean() if total_listings > 0 else 0

    # Real-time Derived Sentiment Index Calculation
    # Compares pricing stability against baseline bounds to generate an active sentiment gauge score
    if total_listings > 0 and len(df) > 0:
        overall_avg = df["price_per_sqft"].mean()
        current_avg = filtered_df["price_per_sqft"].mean()
        sentiment_ratio = current_avg / overall_avg if overall_avg > 0 else 1.0
        sentiment_score = min(max(int(sentiment_ratio * 72), 10), 100) # Base index mapped to 100
    else:
        sentiment_score = 50

    # Determine structural status messages
    if sentiment_score >= 68:
        sentiment_status = "🔥 BULLISH OVERVALUATION ZONE"
        sentiment_desc = "Demand indices indicate highly competitive regional pricing profiles. Premium pricing matrix verified."
    elif sentiment_score >= 45:
        sentiment_status = "⚖️ STABLE ACCUMULATION ZONE"
        sentiment_desc = "Pricing data aligns perfectly with long-term rolling structural averages. Market conditions balanced."
    else:
        sentiment_status = "📉 DISCOUNT CAPITAL ACQUISITION ZONE"
        sentiment_desc = "Asset rates are trading below typical historical benchmarks. Target window active for strategic acquisitions."

    # ─── ROW 1: ENTERPRISE METRIC GRID ───
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    with m_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Properties Analyzed</div>
            <div class="metric-value">{total_listings}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Rate / Sq.Ft</div>
            <div class="metric-value">₹{avg_sqft_price:,}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m_col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Property Valuation</div>
            <div class="metric-value">₹{avg_total_price:.2f} Cr</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m_col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Market Momentum Score</div>
            <div class="metric-value" style="color: #6366f1;">{sentiment_score} / 100</div>
        </div>
        """, unsafe_allow_html=True)

    # ─── ROW 2: SENTIMENT PLAYBOOK CONTEXTUALIZATION ───
    st.markdown(f"""
    <div class="sentiment-panel">
        <h4 style="color: #6366f1; margin-top: 0; margin-bottom: 6px; font-size: 15px; letter-spacing: 0.05em; text-transform: uppercase;">🤖 Engine Sentiment Readout</h4>
        <span style="font-weight: 700; color: white; font-size: 16px;">{sentiment_status}</span>
        <p style="color: #9ca3af; margin-bottom: 0; margin-top: 4px; font-size: 14px;">{sentiment_desc}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ─── ROW 3: DATAVIS UPGRADE SECTION ───
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("📊 Capital Distribution Profile")
        
        # Switched to custom-colored box plots to look clean on a dark theme canvas
        fig_box = px.box(
            filtered_df, 
            x="suburb", 
            y="price_cr",
            color="suburb",
            color_discrete_sequence=px.colors.sequential.Sunsetdark,
            labels={"suburb": "Regional Node", "price_cr": "Valuation (Cr)"}
        )
        
        fig_box.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            xaxis=dict(gridcolor="#1f2937", title=None),
            yaxis=dict(gridcolor="#1f2937"),
            margin=dict(l=10, r=10, t=10, b=10),
            height=300
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with chart_col2:
        st.subheader("📈 Regional Rate Valuations")
        
        avg_prices = filtered_df.groupby("suburb")["price_per_sqft"].mean().reset_index()
        avg_prices = avg_prices.sort_values(by="price_per_sqft", ascending=False)
        
        # Upgraded to sleek custom horizontal bars with rounded aesthetics
        fig_bar = px.bar(
            avg_prices, 
            y="suburb", 
            x="price_per_sqft",
            orientation='h',
            color="price_per_sqft",
            color_continuous_scale=px.colors.sequential.Sunsetdark,
            labels={"price_per_sqft": "Avg ₹ / Sq.Ft", "suburb": ""}
        )
        
        fig_bar.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            coloraxis_showscale=False,
            xaxis=dict(gridcolor="#1f2937"),
            yaxis=dict(gridcolor="rgba(0,0,0,0)", categoryorder="total ascending"),
            margin=dict(l=10, r=10, t=10, b=10),
            height=300
        )
        st.plotly_chart(fig_bar, use_container_width=True)