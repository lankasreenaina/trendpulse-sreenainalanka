# task2_data_processing.py
# TrendPulse — Task 2: Load raw JSON, clean the data, save as CSV

import pandas as pd
import glob
import os

# Step 1 — Load the JSON file from the data/ folder
# We use glob to find the trends_YYYYMMDD.json file
# without hardcoding the date in the filename

# Find the raw JSON file produced by Task 1
json_files = glob.glob("data/trends_*.json")

if not json_files:
    print("No JSON file found in data/. Run task1_data_collection.py first.")
    exit()

# If multiple files exist, pick the most recent one
json_path = sorted(json_files)[-1]

# Load into a Pandas DataFrame
df = pd.read_json(json_path)

print(f"Loaded {len(df)} stories from {json_path}")


# Step 2 — Clean the data
# Each cleaning step is applied in sequence and logged

# --- 2a: Remove duplicate stories by post_id ---
# Same story can appear under multiple categories if keywords overlap
df = df.drop_duplicates(subset=["post_id"])
print(f"\nAfter removing duplicates: {len(df)}")

# --- 2b: Drop rows where critical fields are missing ---
# A story without post_id, title, or score is unusable
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# --- 2c: Fix data types ---
# score and num_comments must be integers, not floats
# (Pandas reads them as float64 when NaNs were present)
df["score"]        = df["score"].astype(int)
df["num_comments"] = df["num_comments"].fillna(0).astype(int)

# --- 2d: Remove low-quality stories ---
# Stories with score < 5 have very little community engagement
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# --- 2e: Strip extra whitespace from titles ---
# Catches leading/trailing spaces that could affect analysis later
df["title"] = df["title"].str.strip()

# Step 3 — Save cleaned data as CSV


output_path = "data/trends_clean.csv"

# Save without the DataFrame index column
df.to_csv(output_path, index=False)

print(f"\nSaved {len(df)} rows to {output_path}")

# Print a summary of how many stories ended up in each category
print("\nStories per category:")
category_counts = df["category"].value_counts()
for category, count in category_counts.items():
    print(f"  {category:<15} {count}")
