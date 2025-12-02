# AI Mastery: Mobile Banking Customer Feedback Analysis - Week 0 Challenge

Kickstart your AI Mastery with comprehensive customer experience analytics for Ethiopian mobile banking apps. This project focuses on understanding, exploring, and analyzing customer reviews from Google Play Store to identify satisfaction drivers, pain points, and actionable insights for Commercial Bank of Ethiopia (CBE), Bank of Abyssinia (BOA), and Dashen Bank.

## Table of Contents

- [Project Overview](#project-overview)
- [Business Objective](#business-objective)
- [Dataset Overview](#dataset-overview)
- [Folder Structure](#folder-structure)
- [Setup & Installation](#setup--installation)
- [Tasks Completed](#tasks-completed)
- [Technologies Used](#technologies-used)
- [Key Observations](#key-observations)

## Project Overview

Week 2 challenge for AI Mastery focuses on end-to-end customer feedback analysis:

- Data collection, cleaning, and preprocessing
- Sentiment and thematic analysis using NLP
- PostgreSQL database integration
- Cross-bank comparison and visualization
- Insights generation with actionable recommendations

The project uses real customer review data from Google Play Store for three major Ethiopian banks.

## Business Objective

Omega Consultancy seeks to enhance customer retention and satisfaction for Ethiopian banks via data-driven insights from mobile app reviews. Your task is to analyze customer feedback and provide actionable recommendations for identifying satisfaction drivers, addressing pain points, and improving app performance.

## Dataset Overview

The dataset contains customer review data from Google Play Store:

| Column | Description |
|--------|-------------|
| `review` | Customer review text content |
| `rating` | Star rating (1-5) |
| `date` | Review posting date (YYYY-MM-DD) |
| `bank` | Bank name (CBE, BOA, Dashen) |
| `source` | Data source (Google Play) |
| `sentiment_label` | Sentiment classification (positive/negative/neutral) |
| `sentiment_score` | Sentiment score (0.00 to 1.00) |
| `themes` | Identified themes (semicolon-separated) |

**Dataset Statistics:**
- Total reviews: 9,571 (697% of 1,200 target)
- Missing data: <1% (exceeds <5% KPI threshold)
- Date range: 2014-02-17 to 2025-10-16
- Banks: CBE (7,974), BOA (1,100), Dashen (497)

Cleaned datasets are saved in `/Data/` (processed files ignored in git).

## Folder Structure

```
mobile-banking-customer-feedback-analysis/
├── Data/                           # Data files and visualizations
│   ├── all_banks.csv               # Cleaned review data
│   ├── all_banks_with_sentiment.csv
│   ├── all_banks_with_sentiment_themes.csv
│   └── visualizations/             # Generated plots
├── scripts/                        # Analysis scripts (OOP)
│   ├── utils.py                    # Utility classes (TextProcessor, DataValidator)
│   ├── task1_scraping.py           # PlayStoreScraper class
│   ├── task1_preprocessing.py     # DataPreprocessor class
│   ├── task2_sentiment.py          # SentimentAnalyzer, SentimentAnalysisPipeline
│   ├── task2_thematic.py           # ThematicAnalyzer, KeywordExtractor, ThemeClusterer
│   ├── task3_database.py          # DatabaseManager, SchemaManager, ReviewInserter
│   ├── task4_visualization.py      # VisualizationPipeline, PlotGenerator classes
│   └── task4_insights.py           # InsightsAnalyzer, DriverAnalyzer, PainPointAnalyzer
├── schema.sql                      # PostgreSQL database schema
├── .env                            # Database credentials (not in git)
├── requirements.txt                # Python dependencies
├── README.md                       # Project overview and instructions
└── .gitignore                      # Git ignore rules
```

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/<username>/mobile-banking-customer-feedback-analysis.git
cd mobile-banking-customer-feedback-analysis

# Create a Python virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

1. **Install PostgreSQL** and create database:
   ```sql
   CREATE DATABASE bank_reviews;
   ```

2. **Create `.env` file** in project root:
   ```
   DB_HOST=localhost
   DB_PORT=port
   DB_NAME=bank_reviews
   DB_USER=username
   DB_PASSWORD=your_password
   ```

3. **Initialize schema**:
   ```bash
   psql -U postgres -d bank_reviews -f schema.sql
   ```

### 3. Run Analysis Pipeline

```bash
# Task 1: Data Collection and Preprocessing
python scripts/task1_scraping.py
python scripts/task1_preprocessing.py

# Task 2: Sentiment and Thematic Analysis
python scripts/task2_sentiment.py
python scripts/task2_thematic.py

# Task 3: Database Integration
python scripts/task3_database.py

# Task 4: Visualization and Insights
python scripts/task4_visualization.py
python scripts/task4_insights.py
```

## Tasks Completed

### Task 1: Data Collection and Preprocessing

- **Web Scraping**: Automated scraping using `google-play-scraper` for all three banks
- **Data Cleaning**: 
  - Duplicate removal
  - Missing data handling
  - Date normalization
  - Data quality validation
- **Classes**: `PlayStoreScraper`, `DataPreprocessor`
- **Output**: Clean CSV with 9,571 reviews (<1% missing data)

### Task 2: Sentiment and Thematic Analysis

- **Sentiment Analysis**: 
  - Dual-model approach (distilbert-base-uncased-finetuned-sst-2-english + VADER fallback)
  - Sentiment labels and scores for all reviews
- **Thematic Analysis**:
  - TF-IDF keyword extraction
  - Rule-based theme clustering
  - 7 themes identified: Account Access, Transaction Performance, UI/UX, Customer Support, Feature Requests, App Reliability, Security
- **Classes**: `SentimentAnalyzer`, `ThematicAnalyzer`, `KeywordExtractor`, `ThemeClusterer`
- **Output**: CSV with sentiment and theme data

### Task 3: Database Integration

- **PostgreSQL Setup**: Normalized schema with banks and reviews tables
- **Data Migration**: Batch insertion with duplicate checking
- **Data Integrity**: Verification queries for reviews per bank, average ratings, sentiment distribution
- **Classes**: `DatabaseManager`, `SchemaManager`, `ReviewInserter`, `DataIntegrityVerifier`
- **Output**: Populated PostgreSQL database with 9,571 reviews

### Task 4: Visualization and Insights

- **Visualizations Generated** (5 plots):
  - Rating Distribution (overall and by bank)
  - Sentiment Distribution (overall and by bank)
  - Bank Comparison (ratings, counts, sentiment percentages)
  - Theme Frequency by Bank
  - Time Trends (rating and review count over time)
- **Insights Analysis**:
  - Satisfaction driver identification from positive reviews
  - Pain point detection from negative reviews
  - Cross-bank comparison
  - Actionable recommendations per bank
- **Classes**: `VisualizationPipeline`, `InsightsAnalyzer`, `DriverAnalyzer`, `PainPointAnalyzer`, `RecommendationGenerator`
- **Output**: PNG visualizations and insights report

## Technologies Used

- **Python 3.8+**
- **Data Processing**: Pandas, NumPy
- **NLP**: transformers, vaderSentiment, textblob, scikit-learn, nltk
- **Database**: PostgreSQL, psycopg2-binary
- **Visualization**: Matplotlib, Seaborn
- **Web Scraping**: google-play-scraper
- **Utilities**: python-dotenv
- **Version Control**: Git & GitHub
- **Architecture**: Object-Oriented Programming (OOP)

## Key Observations

- **CBE** has the highest number of reviews (7,974) with average rating of 4.06, indicating strong user engagement but room for improvement in satisfaction.
- **BOA** shows the lowest average rating (3.09) with 1,100 reviews, requiring immediate attention to address critical pain points.
- **Dashen** has the highest average rating (4.09) but fewer reviews (497), suggesting good satisfaction but smaller user base.
- **Sentiment Distribution**: Positive sentiment dominates across all banks, but negative reviews highlight critical issues requiring prioritization.
- **Common Themes**: Transaction performance and app reliability are key concerns, while ease of use and convenience drive satisfaction.
- **Temporal Trends**: Review volume and sentiment show patterns that correlate with app updates and feature releases.

---

## Database Schema

### Banks Table
| Column | Type | Description |
|--------|------|-------------|
| `bank_id` | SERIAL PRIMARY KEY | Unique identifier |
| `bank_name` | VARCHAR(255) NOT NULL | Bank name (CBE, BOA, Dashen) |
| `app_name` | VARCHAR(255) | Full application name |
| `description` | TEXT | Bank description |
| `created_at` | TIMESTAMP | Record creation timestamp |

### Reviews Table
| Column | Type | Description |
|--------|------|-------------|
| `review_id` | SERIAL PRIMARY KEY | Unique identifier |
| `bank_id` | INTEGER NOT NULL | Foreign key to banks |
| `review_text` | TEXT NOT NULL | Review content |
| `rating` | NUMERIC(2,1) | Rating (1.0 to 5.0) |
| `review_date` | DATE | Review posting date |
| `sentiment_label` | VARCHAR(50) | Sentiment (positive/negative/neutral) |
| `sentiment_score` | NUMERIC(3,2) | Sentiment score (0.00 to 1.00) |
| `source` | VARCHAR(255) | Source (e.g., "Google Play") |
| `created_at` | TIMESTAMP | Record creation timestamp |

**Relationships:** `reviews.bank_id` → `banks.bank_id` (Foreign Key with CASCADE DELETE)
