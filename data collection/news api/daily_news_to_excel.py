import feedparser
import pandas as pd
from urllib.parse import quote_plus
from datetime import datetime
import re

IMPORTANT_KEYWORDS = [
    "earnings", "results", "revenue", "profit", "loss",
    "guidance", "forecast", "layoffs", "acquisition", "merger",
    "stock", "shares", "price", "surge", "drop",
    "rise", "fall", "fed", "interest", "inflation"
]

def clean_text(text):
    text = re.sub("<.*?>", "", text)
    return text.replace("\n", " ").strip()

def is_important(text):
    return any(k in text.lower() for k in IMPORTANT_KEYWORDS)

def format_date(published):
    try:
        return datetime(*published[:6]).strftime("%Y-%m-%d")
    except:
        return ""

def to_three_lines(title, summary):
    text = f"{title}. {summary}"
    text = clean_text(text)
    return text[:450]   # ~3 readable lines

def collect_daily_news(asset, query, excel_file):
    encoded_query = quote_plus(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(url)

    rows = []

    for entry in feed.entries:
        title = clean_text(entry.title)
        summary = clean_text(entry.summary) if "summary" in entry else ""

        if not is_important(title):
            continue

        rows.append({
            "asset": asset,
            "date": format_date(entry.published_parsed),
            "news": to_three_lines(title, summary),
            "link": entry.link
        })

    df = pd.DataFrame(rows)

    # Keep only 3–4 important news per day
    final_rows = []
    for date, group in df.groupby("date"):
        final_rows.append(group.head(4))

    final_df = pd.concat(final_rows)

    # Write to Excel (clean & readable)
    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        final_df.to_excel(writer, index=False, sheet_name="Daily News")

        sheet = writer.sheets["Daily News"]
        sheet.column_dimensions["A"].width = 15
        sheet.column_dimensions["B"].width = 14
        sheet.column_dimensions["C"].width = 90
        sheet.column_dimensions["D"].width = 50

    print(excel_file, ": ready for analysis")


# -------- STOCKS --------
collect_daily_news("Amazon", "Amazon stock earnings", "amazon_daily.xlsx")
collect_daily_news("Apple", "Apple stock earnings", "apple_daily.xlsx")
collect_daily_news("Microsoft", "Microsoft stock earnings", "microsoft_daily.xlsx")
collect_daily_news("Tesla", "Tesla stock earnings", "tesla_daily.xlsx")
collect_daily_news("NVIDIA", "NVIDIA stock earnings", "nvidia_daily.xlsx")

# -------- COMMODITIES --------
collect_daily_news("Gold", "Gold price inflation", "gold_daily.xlsx")
collect_daily_news("Silver", "Silver price inflation", "silver_daily.xlsx")
