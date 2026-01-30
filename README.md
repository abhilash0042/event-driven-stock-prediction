# event-driven-stock-prediction
A machine learning project that predicts stock price movements by analyzing fast-spreading news and social media sentiment from sources like Moneycontrol and Reddit.


## Daily News Collection Module

This module collects daily market-moving financial news using Google News RSS.

### Key Features
- Filters only important financial events (earnings, price movement, macro)
- Limits to 3–4 impactful news per day
- Converts news into readable 2–3 line summaries
- Exports results as Excel files for analysis

### Usage
Run the script inside `data collection/news api`:

```bash
python daily_news_to_excel.py
