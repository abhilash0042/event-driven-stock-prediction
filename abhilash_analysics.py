import requests
import pandas as pd
from datetime import datetime
import sys
print(sys.executable)

# Parameters
query = "Apple"
limit = 50
subreddit = "stocks"
MIN_SCORE = 200

# Reddit's public JSON API endpoint (no authentication required)
url = f"https://www.reddit.com/r/{subreddit}/search.json?q={query}&restrict_sr=1&sort=new&limit={limit}"
headers = {"User-Agent": "Mozilla/5.0 (compatible; AppleNewsBot/1.0)"}

# Fetch data
response = requests.get(url, headers=headers)
if response.status_code != 200:
    print(f"⚠ Failed to fetch data: HTTP {response.status_code}")
    sys.exit()

data = response.json()["data"]["children"]

# Extract relevant post info
posts = []
for item in data:
    post = item["data"]
    posts.append({
        "title": post["title"],
        "score": post["score"],
        "url": f"https://reddit.com{post['permalink']}",
        "created": datetime.fromtimestamp(post["created_utc"]),
        "content": post.get("selftext", "")
    })

# Convert to DataFrame
df = pd.DataFrame(posts)

# Keyword filter
keywords = ["Apple", "AAPL", "iPhone", "MacBook", "Tim Cook"]
pattern = "|".join(keywords)
df = df[
    df["title"].str.contains(pattern, case=False, na=False) |
    df["content"].str.contains(pattern, case=False, na=False)
]

# Filter trending (high-score) posts
df_filtered = df[df["score"] > MIN_SCORE]

# Save to file
file_path = f"apple_trending_{datetime.now():%Y%m%d_%H%M}.txt"
with open(file_path, "w", encoding="utf-8") as f:
    if df_filtered.empty:
        f.write("No trending Apple-related posts found.\n")
        print("⚠ No matching posts found.")
    else:
        for i, row in df_filtered.iterrows():
            f.write(f"Post #{i + 1}\n")
            f.write(f"📌 Title   : {row['title']}\n")
            f.write(f"🔥 Score   : {row['score']}\n")
            f.write(f"🔗 URL     : {row['url']}\n")
            f.write(f"🕓 Created : {row['created']}\n")
            f.write("📝 Content:\n")
            for line in row['content'].splitlines():
                for segment in [line[i:i+80] for i in range(0, len(line), 80)]:
                    f.write(f"    {segment}\n")
            f.write("-" * 100 + "\n\n")
        print(f"✅ File saved: {file_path}")


