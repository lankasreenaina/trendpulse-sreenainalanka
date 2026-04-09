# task2_data_processing.py
import json
import pandas as pd

with open("data/raw_countries.json", "r") as f:
    data = json.load(f)

records = []
for country in data:
    records.append({
        "common_name": country.get("name", {}).get("common", "N/A"),
        "population":  country.get("population", 0),
        "region":      country.get("region", "N/A"),
        "area":        country.get("area", None),
    })

df = pd.DataFrame(records)

# Drop rows with missing area
df_clean = df.dropna(subset=["area"])

# Remove countries with 0 population
df_clean = df_clean[df_clean["population"] > 0].reset_index(drop=True)

# Add population density column
df_clean["pop_density"] = (df_clean["population"] / df_clean["area"]).round(2)

print(f"Cleaned dataset: {len(df_clean)} countries")
print("\nFirst 10 rows:")
print(df_clean.head(10).to_string(index=False))

df_clean.to_csv("data/cleaned_countries.csv", index=False)
print("\nCleaned data saved to data/cleaned_countries.csv")