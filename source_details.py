import requests
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
PLACE_ID = os.getenv("PLACE_ID")
BASE_URL = "https://maps.googleapis.com/maps/api/place/details/json"

# req params
params = {
    "place_id": PLACE_ID,
    "fields": "name,formatted_address,geometry,international_phone_number,rating,opening_hours",
    "key": API_KEY,
}

# api request
response = requests.get(BASE_URL, params=params)
data = response.json()

if "result" in data:
    place_info = {
        "name": data["result"].get("name", ""),
        "address": data["result"].get("formatted_address", ""),
        "latitude": data["result"]["geometry"]["location"]["lat"],
        "longitude": data["result"]["geometry"]["location"]["lng"],
        "phone": data["result"].get("international_phone_number", ""),
        "rating": data["result"].get("rating", ""),
        "opening_hours": str(data["result"].get("opening_hours", {}).get("weekday_text", ""))
    }
else:
    print("Error fetching place details")
    exit()
