# task1_data_collection.py
# TrendPulse — Task 1: Fetch trending stories from HackerNews API
# Fetches top stories, assigns categories based on keywords, saves to JSON

import requests
import json
import os
import time
from datetime import datetime


# Category keyword mapping (case-insensitive match)
# Each story title is checked against these keywords

CATEGORIES = {
    "technology":    ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews":     ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports":        ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science":       ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"],
}

MAX_PER_CATEGORY = 25      # collect up to 25 stories per category
TOP_STORIES_LIMIT = 500    # fetch first 500 story IDs from HackerNews

HEADERS = {"User-Agent": "TrendPulse/1.0"}

BASE_URL = "https://hacker-news.firebaseio.com/v0"


# Helper: assign a category to a story title
# Returns the first matching category, or None if no match

def assign_category(title):
    if not title:
        return None
    title_lower = title.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                return category
    return None  # story doesn't match any category


# Step 1 — Fetch the top 500 story IDs

print("Fetching top story IDs from HackerNews...")

try:
    response = requests.get(f"{BASE_URL}/topstories.json", headers=HEADERS, timeout=15)
    response.raise_for_status()
    all_ids = response.json()[:TOP_STORIES_LIMIT]  # slice to first 500
    print(f"Retrieved {len(all_ids)} story IDs.")
except requests.exceptions.RequestException as e:
    print(f"Failed to fetch story IDs: {e}")
    all_ids = []

# Step 2 — Fetch each story's details and categorise
# We loop category by category, sleeping 2s between each

# Pre-fetch all story details once to avoid redundant API calls
print("\nFetching individual story details...")

stories_raw = []
for story_id in all_ids:
    try:
        res = requests.get(f"{BASE_URL}/item/{story_id}.json", headers=HEADERS, timeout=10)
        res.raise_for_status()
        story = res.json()

        # Only keep stories that have a title (skip jobs, polls, etc.)
        if story and story.get("title"):
            stories_raw.append(story)

    except requests.exceptions.RequestException as e:
        # If one story fails, log it and continue — don't crash
        print(f"  Skipping story {story_id}: {e}")

print(f"Successfully fetched {len(stories_raw)} story details.")


# Step 3 — Group stories into categories
# Collect up to 25 per category, sleep 2s between categories

print("\nCategorising stories...")

collected_stories = []

for category in CATEGORIES:
    category_count = 0

    for story in stories_raw:
        if category_count >= MAX_PER_CATEGORY:
            break  # stop once we have 25 for this category

        assigned = assign_category(story.get("title", ""))

        if assigned == category:
            # Extract and structure the required 7 fields
            record = {
                "post_id":      story.get("id"),
                "title":        story.get("title"),
                "category":     category,
                "score":        story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author":       story.get("by", "unknown"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            collected_stories.append(record)
            category_count += 1

    print(f"  {category:<15} → {category_count} stories collected")

    # Wait 2 seconds between each category loop as required
    time.sleep(2)

# Step 4 — Save to JSON file in data/ folder
# Filename uses today's date: trends_YYYYMMDD.json

os.makedirs("data", exist_ok=True)  # create data/ folder if it doesn't exist

date_str   = datetime.now().strftime("%Y%m%d")
output_file = f"data/trends_{date_str}.json"

with open(output_file, "w") as f:
    json.dump(collected_stories, f, indent=2)

print(f"\nCollected {len(collected_stories)} stories. Saved to {output_file}")
