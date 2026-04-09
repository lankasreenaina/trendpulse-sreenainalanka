# task4_visualization.py
import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("data/cleaned_countries.csv")
os.makedirs("plots", exist_ok=True)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("TrendPulse — Country Data Dashboard", fontsize=16, fontweight="bold")

# Plot 1 — Total population by region (bar chart)
region_pop = df.groupby("region")["population"].sum().sort_values(ascending=False)
axes[0, 0].bar(region_pop.index, region_pop.values / 1e9, color="steelblue")
axes[0, 0].set_title("Total Population by Region (Billions)")
axes[0, 0].set_xlabel("Region")
axes[0, 0].set_ylabel("Population (Billions)")
axes[0, 0].tick_params(axis="x", rotation=30)

# Plot 2 — Top 10 largest countries by area (horizontal bar)
top10_area = df.nlargest(10, "area")[["common_name", "area"]]
axes[0, 1].barh(top10_area["common_name"], top10_area["area"] / 1e6, color="darkorange")
axes[0, 1].set_title("Top 10 Largest Countries by Area")
axes[0, 1].set_xlabel("Area (Million km²)")
axes[0, 1].invert_yaxis()

# Plot 3 — Number of countries per region (pie chart)
region_count = df["region"].value_counts()
axes[1, 0].pie(region_count.values, labels=region_count.index,
               autopct="%1.1f%%", startangle=140)
axes[1, 0].set_title("Countries per Region")

# Plot 4 — Population density distribution (histogram)
df_filtered = df[df["pop_density"] < 500]  # exclude extreme outliers
axes[1, 1].hist(df_filtered["pop_density"], bins=40, color="mediumseagreen", edgecolor="white")
axes[1, 1].set_title("Population Density Distribution (< 500 /km²)")
axes[1, 1].set_xlabel("People per km²")
axes[1, 1].set_ylabel("Number of Countries")

plt.tight_layout()
plt.savefig("plots/trendpulse_dashboard.png", dpi=150)
print("Dashboard saved to plots/trendpulse_dashboard.png")
plt.show()