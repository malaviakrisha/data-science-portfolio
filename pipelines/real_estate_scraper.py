import os
import random
import psycopg2
from dotenv import load_dotenv

SUBURBS = ["Bandra West", "Andheri West", "Dadar West", "Powai", "Borivali West"]

def generate_data(num_listings=2): # Changed to 5 as requested
    data = []
    for _ in range(num_listings):
        suburb = random.choice(SUBURBS)
        bhk = random.choice([1, 2, 3, 4])
        price_per_sqft = random.randint(15000, 60000)
        sqft = bhk * random.randint(450, 600)
        price_cr = round((sqft * price_per_sqft) / 10000000, 2)
        
        # Append as a tuple
        data.append((suburb, bhk, sqft, price_cr, price_per_sqft))
    return data

def push_to_supabase(data):
    load_dotenv()
    db_url = os.getenv("SUPABASE_DB_URL")
    
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    # Use executemany for high-performance bulk insertion
    insert_query = """
    INSERT INTO listings (suburb, bhk, sqft, price_cr, price_per_sqft) 
    VALUES (%s, %s, %s, %s, %s)
    """
    
    cur.executemany(insert_query, data)
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Successfully pushed {len(data)} rows to Supabase.")

if __name__ == "__main__":
    new_data = generate_data(5) # Fetch 2 rows
    push_to_supabase(new_data)