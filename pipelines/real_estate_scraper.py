import os
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv
import streamlit as st

CSV_PATH = os.path.join(os.path.dirname(__file__), "mumbai_properties.csv")

def get_real_market_data(csv_path, num_listings=2):
    print("📊 Reading Mumbai properties dataset...")
    
    df = pd.read_csv(csv_path)
    
    # Drop rows with missing crucial columns
    df = df.dropna(subset=['locality', 'bedroom_num', 'area', 'price', 'price_per_sqft'])
    
    # Filter out bad data
    df = df[df['area'] > 0]
    df = df[df['price'] > 0]
    df = df[df['bedroom_num'] > 0]
    
    # Sample random listings to simulate daily new entries
    daily_sample = df.sample(n=num_listings)
    
    data = []
    for _, row in daily_sample.iterrows():
        suburb      = str(row['locality']).strip()[:100]
        bhk         = int(row['bedroom_num'])
        sqft        = int(row['area'])
        price_cr    = round(float(row['price']) / 10_000_000, 2)
        price_psqft = int(row['price_per_sqft'])

        data.append({
            "suburb":         suburb,
            "bhk":            bhk,
            "sqft":           sqft,
            "price_cr":       price_cr,
            "price_per_sqft": price_psqft
        })

    print(f"✅ Sampled {len(data)} listings from dataset.")
    return data


def push_to_supabase(data):
    # Works in both GitHub Actions (env vars) and locally (.toml via st.secrets)
    try:
        url = os.environ.get("SUPABASE_URL") or st.secrets["SUPABASE_URL"]
        key = os.environ.get("SUPABASE_KEY") or st.secrets["SUPABASE_KEY"]
    except Exception:
        raise ValueError("❌ SUPABASE_URL or SUPABASE_KEY not found.")
    
    client = create_client(url, key)
    response = client.table("listings").insert(data).execute()
    print(f"🚀 Successfully pushed {len(data)} listings.")

if __name__ == "__main__":
    try:
        new_data = get_real_market_data(CSV_PATH, num_listings=2)
        push_to_supabase(new_data)
    except Exception as e:
        print(f"❌ Pipeline Error: {e}")