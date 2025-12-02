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
│   ├── task2_thematic.py    # Thematic analysis
│   └── task3_database.py    # Database integration
├── schema.sql               # PostgreSQL database schema
├── .env                     # Database credentials (not in git)
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

6. Setup PostgreSQL database (Task 3):
   - Install PostgreSQL on your system
   - Create a database named `bank_reviews`
   - Create a `.env` file in the project root with database credentials:
     ```
     DB_HOST=localhost
     DB_PORT=5432
     DB_NAME=bank_reviews
     DB_USER=postgres
     DB_PASSWORD=your_password
     ```
   - Run the database setup script:
     ```bash
     python scripts/task3_database.py
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

### Task 3: Database Integration
- PostgreSQL database setup with normalized schema
- Stores cleaned review data and sentiment analysis results
- Data integrity verification queries
- Output: Populated PostgreSQL database with >1,000 reviews

## Data Quality KPIs

- 1,200+ reviews collected with <5% missing data
- Sentiment scores for 90%+ reviews
- 3+ themes per bank with examples
- PostgreSQL database with >1,000 review entries

## Database Schema

### Banks Table
Stores information about the banks.

| Column | Type | Description |
|--------|------|-------------|
| `bank_id` | SERIAL PRIMARY KEY | Unique identifier for each bank |
| `bank_name` | VARCHAR(255) NOT NULL | Bank name (CBE, BOA, Dashen) |
| `app_name` | VARCHAR(255) | Full application name |
| `description` | TEXT | Bank description |
| `created_at` | TIMESTAMP | Record creation timestamp |

### Reviews Table
Stores the scraped and processed review data.

| Column | Type | Description |
|--------|------|-------------|
| `review_id` | SERIAL PRIMARY KEY | Unique identifier for each review |
| `bank_id` | INTEGER NOT NULL | Foreign key to banks table |
| `review_text` | TEXT NOT NULL | The review content |
| `rating` | NUMERIC(2,1) | Rating (1.0 to 5.0) |
| `review_date` | DATE | Date when review was posted |
| `sentiment_label` | VARCHAR(50) | Sentiment classification (positive/negative/neutral) |
| `sentiment_score` | NUMERIC(3,2) | Sentiment score (0.00 to 1.00) |
| `source` | VARCHAR(255) | Source of review (e.g., "Google Play") |
| `created_at` | TIMESTAMP | Record creation timestamp |

### Relationships
- `reviews.bank_id` → `banks.bank_id` (Foreign Key with CASCADE DELETE)

### Indexes
- `idx_reviews_bank_id` on `reviews(bank_id)`
- `idx_reviews_rating` on `reviews(rating)`
- `idx_reviews_sentiment_label` on `reviews(sentiment_label)`
- `idx_reviews_review_date` on `reviews(review_date)`
- `idx_banks_bank_name` on `banks(bank_name)`

### Database Setup

1. **Create Database:**
   ```sql
   CREATE DATABASE bank_reviews;
   ```

2. **Run Schema:**
   ```bash
   psql -U postgres -d bank_reviews -f schema.sql
   ```

3. **Insert Data:**
   ```bash
   python scripts/task3_database.py
   ```

### Verification Queries

Count reviews per bank:
```sql
SELECT b.bank_name, COUNT(r.review_id) as review_count
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_id, b.bank_name
ORDER BY review_count DESC;
```

Average rating per bank:
```sql
SELECT b.bank_name, 
       ROUND(AVG(r.rating)::numeric, 2) as avg_rating,
       COUNT(r.review_id) as review_count
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
WHERE r.rating IS NOT NULL
GROUP BY b.bank_id, b.bank_name
ORDER BY avg_rating DESC;
```

Sentiment distribution:
```sql
SELECT sentiment_label, COUNT(*) as count
FROM reviews
WHERE sentiment_label IS NOT NULL
GROUP BY sentiment_label
ORDER BY count DESC;
```

## Author

Data Analyst at Omega Consultancy

