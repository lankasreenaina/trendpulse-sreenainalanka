# task4_visualization.py
# TrendPulse — Task 4: Create charts and a dashboard from analysed data

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
# Step 1 — Setup: load data and create outputs folder
# Load the analysed CSV produced by Task 3
df = pd.read_csv("data/trends_analysed.csv")
print(f"Loaded {len(df)} stories from data/trends_analysed.csv")

# Create outputs/ folder if it doesn't exist
os.makedirs("outputs", exist_ok=True)

# Helper: shorten titles longer than 50 characters for readable axis labels
def shorten_title(title, max_len=50):
    return title if len(title) <= max_len else title[:max_len] + "..."

# Chart 1 — Top 10 Stories by Score (horizontal bar)
# Shows which individual stories got the most upvotes
# Sort by score descending and take the top 10
top10 = df.nlargest(10, "score").copy()
top10["short_title"] = top10["title"].apply(shorten_title)

fig1, ax1 = plt.subplots(figsize=(10, 6))

# Horizontal bar chart — titles on y-axis, scores on x-axis
ax1.barh(top10["short_title"], top10["score"], color="steelblue")

# Invert y-axis so the highest score appears at the top
ax1.invert_yaxis()

ax1.set_title("Top 10 Stories by Score", fontsize=14, fontweight="bold")
ax1.set_xlabel("Score (Upvotes)")
ax1.set_ylabel("Story Title")

plt.tight_layout()

# Save before show() — required so the file is written before display clears it
plt.savefig("outputs/chart1_top_stories.png", dpi=150)
print("Saved outputs/chart1_top_stories.png")
plt.show()
plt.close()

# Chart 2 — Stories per Category (bar chart)
# Shows which categories contributed the most stories
# Count stories per category and sort for a cleaner look
category_counts = df["category"].value_counts().sort_values(ascending=False)

# Assign a distinct colour to each bar
colours = ["steelblue", "darkorange", "mediumseagreen", "tomato", "mediumpurple"]

fig2, ax2 = plt.subplots(figsize=(8, 5))

ax2.bar(category_counts.index, category_counts.values, color=colours)

ax2.set_title("Stories per Category", fontsize=14, fontweight="bold")
ax2.set_xlabel("Category")
ax2.set_ylabel("Number of Stories")

# Add count labels on top of each bar for quick reading
for i, count in enumerate(category_counts.values):
    ax2.text(i, count + 0.3, str(count), ha="center", fontsize=10)

plt.tight_layout()
plt.savefig("outputs/chart2_categories.png", dpi=150)
print("Saved outputs/chart2_categories.png")
plt.show()
plt.close()

# Chart 3 — Score vs Comments (scatter plot)
# Reveals whether high-scoring stories also get more comments
# Popular stories (above average score) shown in a different colour
# Split into popular and non-popular groups using the is_popular column
popular     = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

fig3, ax3 = plt.subplots(figsize=(9, 6))

# Plot non-popular stories first (background layer)
ax3.scatter(not_popular["score"], not_popular["num_comments"],
            color="steelblue", alpha=0.6, label="Not Popular", s=60)

# Plot popular stories on top so they stand out
ax3.scatter(popular["score"], popular["num_comments"],
            color="tomato", alpha=0.8, label="Popular", s=80, marker="*")

ax3.set_title("Score vs Number of Comments", fontsize=14, fontweight="bold")
ax3.set_xlabel("Score (Upvotes)")
ax3.set_ylabel("Number of Comments")
ax3.legend(title="Popularity")

plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png", dpi=150)
print("Saved outputs/chart3_scatter.png")
plt.show()
plt.close()

# Bonus — Dashboard: all 3 charts in one figure
# Uses subplots(1, 3) for a side-by-side layout
fig, axes = plt.subplots(1, 3, figsize=(20, 6))
fig.suptitle("TrendPulse Dashboard", fontsize=18, fontweight="bold", y=1.02)

# --- Dashboard Panel 1: Top 10 by Score ---
axes[0].barh(top10["short_title"], top10["score"], color="steelblue")
axes[0].invert_yaxis()
axes[0].set_title("Top 10 Stories by Score")
axes[0].set_xlabel("Score")
axes[0].tick_params(axis="y", labelsize=7)

# --- Dashboard Panel 2: Stories per Category ---
axes[1].bar(category_counts.index, category_counts.values, color=colours)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Count")
for i, count in enumerate(category_counts.values):
    axes[1].text(i, count + 0.2, str(count), ha="center", fontsize=9)

# --- Dashboard Panel 3: Score vs Comments Scatter ---
axes[2].scatter(not_popular["score"], not_popular["num_comments"],
                color="steelblue", alpha=0.6, label="Not Popular", s=50)
axes[2].scatter(popular["score"], popular["num_comments"],
                color="tomato", alpha=0.8, label="Popular", s=70, marker="*")
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Comments")

# Manual legend patches for the scatter panel
pop_patch     = mpatches.Patch(color="tomato",    label="Popular")
not_pop_patch = mpatches.Patch(color="steelblue", label="Not Popular")
axes[2].legend(handles=[pop_patch, not_pop_patch], fontsize=8)

plt.tight_layout()
plt.savefig("outputs/dashboard.png", dpi=150, bbox_inches="tight")
print("Saved outputs/dashboard.png")
plt.show()
plt.close()

print("\nAll charts saved to outputs/")
