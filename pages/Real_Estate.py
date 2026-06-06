import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import os
from dotenv import load_dotenv

# Load environment variables for local testing
load_dotenv()

# Page Configuration
st.set_page_config(page_title="Mumbai Real Estate Analytics", layout="wide")

st.title("🏠 Mumbai Real Estate Sentiment & Price Engine")
st.markdown("This dashboard reflects live property data automatically aggregated via our automated backend pipeline.")

# Database connection function
@st.cache_data(ttl=60) # Caches data for 60 seconds to avoid spamming the DB on widget clicks
def fetch_live_data():
    db_url = os.getenv("SUPABASE_DB_URL")
    if not db_url:
        st.error("Database connection string missing. Check environment variables.")
        return pd.DataFrame()
    
    try:
        conn = psycopg2.connect(db_url)
        query = "SELECT * FROM listings ORDER BY scraped_at DESC;"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching data from cloud database: {e}")
        return pd.DataFrame()

# Load Data
df = fetch_live_data()

if df.empty:
    st.warning("No data found in the cloud database. Run your ingestion script first.")
else:
    # ─── SIDEBAR FILTERS ───
    st.sidebar.header("Filter Options")
    selected_suburbs = st.sidebar.multiselect(
        "Select Suburbs", 
        options=df["suburb"].unique(), 
        default=df["suburb"].unique()
    )
    
    # Filter DataFrame
    filtered_df = df[df["suburb"].isin(selected_suburbs)]

    # ─── KEY METRICS ROW ───
    total_listings = len(filtered_df)
    avg_sqft_price = int(filtered_df["price_per_sqft"].mean()) if total_listings > 0 else 0
    avg_total_price = filtered_df["price_cr"].mean() if total_listings > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Properties Analyzed", value=total_listings)
    col2.metric(label="Avg Price per Sq. Ft.", value=f"₹{avg_sqft_price:,}")
    col3.metric(label="Avg Property Cost", value=f"₹{avg_total_price:.2f} Cr")

    st.markdown("---")

    # ─── CHARTS SECTION ───
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Price Distribution by Suburb")
        fig_box = px.box(
            filtered_df, 
            x="suburb", 
            y="price_cr", 
            color="suburb",
            labels={"suburb": "Suburb", "price_cr": "Price (in Crores)"},
            title="Property Value Spread"
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with chart_col2:
        st.subheader("Avg Price per Sq. Ft. comparison")
        avg_prices = filtered_df.groupby("suburb")["price_per_sqft"].mean().reset_index()
        fig_bar = px.bar(
            avg_prices, 
            x="suburb", 
            y="price_per_sqft", 
            color="suburb",
            labels={"price_per_sqft": "Avg ₹/Sq.Ft"},
            title="Market Rate Analysis"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # ─── RAW DATA EXPANDER ───
    with st.expander("📂 View Live Production Ledger (Raw Database Rows)"):
        st.dataframe(filtered_df, use_container_width=True)