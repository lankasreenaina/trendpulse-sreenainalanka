# task1_data_collection.py
import requests
import json
import os

API_URL = "https://restcountries.com/v3.1/all?fields=name,population,region,area"
headers = {"User-Agent": "Mozilla/5.0"}

try:
    response = requests.get(API_URL, headers=headers, timeout=15)
    print(f"HTTP Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Total countries retrieved: {len(data)}")

        os.makedirs("data", exist_ok=True)
        with open("data/raw_countries.json", "w") as f:
            json.dump(data, f, indent=2)
        print("Raw data saved to data/raw_countries.json")

    else:
        print(f"Error: {response.status_code} - {response.reason}")

except requests.exceptions.ConnectionError:
    print("Error: Could not connect to the API.")
except requests.exceptions.Timeout:
    print("Error: Request timed out.")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")