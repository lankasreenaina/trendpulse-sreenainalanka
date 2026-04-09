# task3_analysis.py
# TrendPulse — Task 3: Analyse cleaned data using Pandas and NumPy

import pandas as pd
import numpy as np

# Step 1 — Load and Explore the cleaned CSV
# Load the cleaned CSV produced by Task 2
df = pd.read_csv("data/trends_clean.csv")

print(f"Loaded data: {df.shape}")   # (rows, columns)

# Preview the first 5 rows to confirm data looks right
print("\nFirst 5 rows:")
print(df.head().to_string(index=False))

# Basic averages across all stories using Pandas
avg_score    = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {avg_score:,.0f}")
print(f"Average comments: {avg_comments:,.0f}")
# Step 2 — NumPy Statistics on score column
# Converting to a NumPy array for explicit NumPy usage
scores = df["score"].to_numpy()   # convert Pandas Series → NumPy array

mean_score   = np.mean(scores)
median_score = np.median(scores)
std_score    = np.std(scores)
max_score    = np.max(scores)
min_score    = np.min(scores)

print("\n--- NumPy Stats ---")
print(f"Mean score   : {mean_score:,.0f}")
print(f"Median score : {median_score:,.0f}")
print(f"Std deviation: {std_score:,.0f}")
print(f"Max score    : {max_score:,.0f}")
print(f"Min score    : {min_score:,.0f}")

# Which category has the most stories?
# value_counts() returns categories sorted by frequency
top_category       = df["category"].value_counts().idxmax()
top_category_count = df["category"].value_counts().max()

print(f"\nMost stories in: {top_category} ({top_category_count} stories)")

# Which story has the most comments?
# idxmax() returns the row index of the highest num_comments value
most_commented_idx   = df["num_comments"].idxmax()
most_commented_title = df.loc[most_commented_idx, "title"]
most_commented_count = df.loc[most_commented_idx, "num_comments"]

print(f'\nMost commented story: "{most_commented_title}" — {most_commented_count:,} comments')

# Step 3 — Add new columns
# engagement: measures how much discussion a story sparks per upvote
# +1 avoids division by zero if score is somehow 0
df["engagement"] = (df["num_comments"] / (df["score"] + 1)).round(4)

# is_popular: True if the story's score is above the overall average
# avg_score already computed above using Pandas mean
df["is_popular"] = df["score"] > avg_score

# Quick preview of the new columns
print("\nNew columns preview (engagement & is_popular):")
print(df[["title", "score", "num_comments", "engagement", "is_popular"]].head().to_string(index=False))

# How many stories are flagged as popular?
popular_count = df["is_popular"].sum()
print(f"\n{popular_count} out of {len(df)} stories are marked as popular")

# Step 4 — Save updated DataFrame to CSV

output_path = "data/trends_analysed.csv"
df.to_csv(output_path, index=False)

print(f"\nSaved to {output_path}")
