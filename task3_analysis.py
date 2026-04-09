# task3_analysis.py
import pandas as pd

df = pd.read_csv("data/cleaned_countries.csv")

print("=" * 50)
print("TRENDPULSE — COUNTRY DATA ANALYSIS")
print("=" * 50)

# 1. Region with highest total population
region_pop = df.groupby("region")["population"].sum().sort_values(ascending=False)
print("\n1. Total Population by Region:")
print(region_pop.to_string())
print(f"\n   → Highest: {region_pop.idxmax()} ({region_pop.max():,} people)")

# 2. Country with the largest area
largest = df.loc[df["area"].idxmax()]
print(f"\n2. Largest Country by Area:")
print(f"   → {largest['common_name']} ({largest['area']:,.2f} km²)")

# 3. Top 5 most populous countries
print("\n3. Top 5 Most Populous Countries:")
top5 = df.nlargest(5, "population")[["common_name", "population", "region"]]
print(top5.to_string(index=False))

# 4. Most densely populated country (min area filter to avoid micro-states skew)
df_filtered = df[df["area"] >= 1000]
densest = df_filtered.loc[df_filtered["pop_density"].idxmax()]
print(f"\n4. Most Densely Populated Country (area ≥ 1000 km²):")
print(f"   → {densest['common_name']} ({densest['pop_density']:,.2f} people/km²)")

# 5. Average population per region
print("\n5. Average Country Population by Region:")
avg_pop = df.groupby("region")["population"].mean().round(0).sort_values(ascending=False)
print(avg_pop.to_string())