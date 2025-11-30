# Customer Experience Analytics for Fintech Apps

A Real-World Data Engineering Challenge: Scraping, Analyzing, and Visualizing Google Play Store Reviews

## Project Overview

This project analyzes customer satisfaction with mobile banking apps by collecting and processing user reviews from the Google Play Store for three Ethiopian banks:

- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

## Objectives

- Scrape user reviews from the Google Play Store
- Analyze sentiment (positive/negative/neutral) and extract themes
- Identify satisfaction drivers and pain points
- Store cleaned review data in a Postgres database
- Deliver a report with visualizations and actionable recommendations

## Project Structure

```
.
├── Data/                    # Raw and processed data files
├── scripts/                 # Analysis scripts
│   ├── task1_scraping.py   # Web scraping script
│   ├── task1_preprocessing.py  # Data preprocessing
│   ├── task2_sentiment.py   # Sentiment analysis
│   └── task2_thematic.py    # Thematic analysis
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run scraping script (Task 1):
```bash
python scripts/task1_scraping.py
```

3. Run preprocessing script (Task 1):
```bash
python scripts/task1_preprocessing.py
```

4. Run sentiment analysis (Task 2):
```bash
python scripts/task2_sentiment.py
```

5. Run thematic analysis (Task 2):
```bash
python scripts/task2_thematic.py
```

## Methodology

### Task 1: Data Collection and Preprocessing
- Web scraping using `google-play-scraper`
- Target: 400+ reviews per bank (1,200 total)
- Preprocessing: Remove duplicates, handle missing data, normalize dates
- Output: CSV with columns: review, rating, date, bank, source

### Task 2: Sentiment and Thematic Analysis
- Sentiment analysis using distilbert-base-uncased-finetuned-sst-2-english or VADER
- Thematic analysis using TF-IDF and keyword extraction
- Theme clustering: 3-5 themes per bank
- Output: CSV with sentiment scores and identified themes

## Data Quality KPIs

- 1,200+ reviews collected with <5% missing data
- Sentiment scores for 90%+ reviews
- 3+ themes per bank with examples

## Author

Data Analyst at Omega Consultancy

