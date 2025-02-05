import psycopg2
import os
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()

# Database connection details from .env file
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Connect to PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Database connected successfully!")
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

# Insert place details
def insert_place(name, address, latitude, longitude, phone, rating, opening_hours):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO places (name, address, latitude, longitude, phone, rating, opening_hours)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            ''', (name, address, latitude, longitude, phone, rating, opening_hours))
            place_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            print(f"Place inserted successfully with ID: {place_id}")
        except Exception as e:
            print(f"Error inserting place: {e}")

# Fetch all places and tabulate the output
def fetch_places():
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM places;")
            rows = cur.fetchall()

            # Tabulate the results
            headers = [desc[0] for desc in cur.description]  # Get column names
            print(tabulate(rows, headers=headers, tablefmt="grid"))

            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error fetching places: {e}")

# Setup database
def setup_database():
    os.system('clear')
    data = int(input("1: Add data \n2: View data \n Enter function - [1/2] : "))
    if data == 1:
        insert_place(
            place_info["name"],
            place_info["address"],
            place_info["latitude"],
            place_info["longitude"],
            place_info["phone"],
            place_info["rating"],
            place_info["opening_hours"]
        )
    elif data == 2:
        fetch_places()

if __name__ == "__main__":
    # from source_details import place_info  
    # setup_database(place_info)
    setup_database()
