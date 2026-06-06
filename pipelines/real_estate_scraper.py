import os
import random
from supabase import create_client
from dotenv import load_dotenv

SUBURBS = ["Bandra West", "Andheri West", "Dadar West", "Powai", "Borivali West"]

def generate_data(num_listings=5):
    data = []
    for _ in range(num_listings):
        suburb = random.choice(SUBURBS)
        bhk = random.choice([1, 2, 3, 4])
        price_per_sqft = random.randint(15000, 60000)
        sqft = bhk * random.randint(450, 600)
        price_cr = round((sqft * price_per_sqft) / 10000000, 2)
        data.append({
            "suburb": suburb,
            "bhk": bhk,
            "sqft": sqft,
            "price_cr": price_cr,
            "price_per_sqft": price_per_sqft
        })
    return data

def push_to_supabase(data):
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    client = create_client(url, key)
    response = client.table("listings").insert(data).execute()
    print(f"✅ Successfully pushed {len(data)} rows to Supabase.")

if __name__ == "__main__":
    new_data = generate_data(5)
    push_to_supabase(new_data)