# Customer Experience Analytics for Fintech Apps
## Project Summary Report

**Project:** Mobile Banking Customer Feedback Analysis  
**Client:** Omega Consultancy (Supporting Ethiopian Banks)  
**Analyst:** Data Analyst Team  
**Date:** November 2024

---

## Page 1: Understanding and Defining the Business Objective

### 1.1 Business Context

Omega Consultancy is supporting three major Ethiopian banks—Commercial Bank of Ethiopia (CBE), Bank of Abyssinia (BOA), and Dashen Bank—to improve their mobile banking applications. The primary goal is to enhance customer retention and satisfaction by identifying pain points and satisfaction drivers through comprehensive analysis of user reviews from the Google Play Store.

### 1.2 Core Business Objectives

**Primary Objective:**
Improve mobile banking app performance to enhance customer retention and satisfaction for three Ethiopian banks through data-driven insights from user feedback.

**Specific Objectives:**
1. **Data Collection:** Scrape and collect a minimum of 1,200 user reviews (400+ per bank) from Google Play Store
2. **Sentiment Analysis:** Quantify customer sentiment (positive/negative/neutral) across all reviews
3. **Thematic Analysis:** Identify key themes and patterns in customer feedback (e.g., bugs, UI issues, feature requests)
4. **Insight Generation:** Identify satisfaction drivers (e.g., speed, ease of use) and pain points (e.g., crashes, slow loading)
5. **Data Storage:** Store cleaned review data in a structured format for future analysis
6. **Actionable Recommendations:** Deliver insights that guide product, marketing, and engineering teams

### 1.3 Business Scenarios Addressed

**Scenario 1: Retaining Users**
- **Challenge:** CBE (4.2★), BOA (3.4★), and Dashen (4.1★) ratings indicate room for improvement. Users complain about slow loading during transfers.
- **Analysis Goal:** Determine if slow loading is a broader issue across all banks and identify specific areas for app investigation.

**Scenario 2: Enhancing Features**
- **Challenge:** Banks need to stay competitive by understanding desired features.
- **Analysis Goal:** Extract desired features (e.g., transfer improvements, fingerprint login, faster loading) through keyword and theme extraction.

**Scenario 3: Managing Complaints**
- **Challenge:** Improve customer support efficiency and guide AI chatbot integration.
- **Analysis Goal:** Cluster and track complaints (e.g., "login error") to inform support strategies.

### 1.4 Success Metrics

- **Data Quality:** 1,200+ reviews with <5% missing data
- **Analysis Coverage:** Sentiment scores for 90%+ of reviews
- **Theme Identification:** 3+ distinct themes per bank with supporting examples
- **Actionability:** Clear recommendations for each bank's improvement priorities

---

## Page 2: Discussion of Completed Work and Initial Analysis

### 2.1 Data Collection and Preprocessing (Task 1)

#### 2.1.1 Data Collection Summary

**Total Data Collected:**
- **Total Reviews:** 9,572 reviews (exceeds 1,200 minimum requirement by 697%)
- **Reviews by Bank:**
  - Commercial Bank of Ethiopia (CBE): 7,974 reviews (83.3%)
  - Bank of Abyssinia (BOA): 1,100 reviews (11.5%)
  - Dashen Bank: 497 reviews (5.2%)
- **Data Source:** Google Play Store
- **Collection Method:** Automated web scraping using `google-play-scraper` library

#### 2.1.2 Data Quality Metrics

**Data Completeness:**
- **Review Text:** Complete (0% missing) - all reviews contain text
- **Ratings:** Complete (0% missing) - all reviews have 1-5 star ratings
- **Dates:** Normalized to YYYY-MM-DD format
- **Bank Identification:** Complete (0% missing)
- **Overall Missing Data:** <1% (well below 5% KPI threshold) ✓

**Rating Distribution:**
- **5 Stars:** 5,971 reviews (62.4%) - Strong positive sentiment
- **4 Stars:** 925 reviews (9.7%)
- **3 Stars:** 595 reviews (6.2%)
- **2 Stars:** 390 reviews (4.1%)
- **1 Star:** 1,690 reviews (17.7%) - Significant negative feedback
- **Average Rating:** 3.8/5.0

**Key Observations:**
- CBE dominates the dataset with 83% of reviews, indicating higher user engagement
- 62.4% of reviews are 5-star, suggesting overall satisfaction
- 17.7% are 1-star reviews, indicating specific pain points requiring attention

#### 2.1.3 Preprocessing Pipeline

**Completed Steps:**
1. **Duplicate Removal:** Removed exact duplicate reviews based on review text and bank
2. **Missing Data Handling:** Removed rows with missing critical fields (review text, invalid ratings)
3. **Date Normalization:** Standardized all dates to YYYY-MM-DD format
4. **Data Validation:** Ensured all ratings are between 1-5, validated bank names
5. **Output Format:** Clean CSV with columns: `review`, `rating`, `date`, `bank`, `source`

**Output Files:**
- `Data/all_banks.csv` - Clean, preprocessed dataset ready for analysis

### 2.2 Sentiment and Thematic Analysis (Task 2)

#### 2.2.1 Sentiment Analysis Implementation

**Methodology:**
- **Primary Model:** distilbert-base-uncased-finetuned-sst-2-english (state-of-the-art transformer model)
- **Fallback:** VADER (Valence Aware Dictionary and sEntiment Reasoner) for reliability
- **Text Preprocessing:** URL removal, email removal, lowercase conversion, whitespace normalization
- **Output:** Sentiment labels (positive/negative/neutral) and confidence scores (0-1)

**Expected Coverage:** 90%+ of reviews will have sentiment scores (KPI target)

#### 2.2.2 Thematic Analysis Implementation

**Methodology:**
- **Keyword Extraction:** TF-IDF (Term Frequency-Inverse Document Frequency) vectorization
- **N-gram Analysis:** Unigrams and bigrams (1-2 word phrases)
- **Stop Word Removal:** English stop words filtered
- **Theme Clustering:** Rule-based clustering into 7 predefined themes:
  1. **Account Access Issues:** Login, password, authentication problems
  2. **Transaction Performance:** Transfer speed, loading times, delays
  3. **User Interface & Experience:** UI design, navigation, ease of use
  4. **Customer Support:** Support quality, response times, issue resolution
  5. **Feature Requests:** Desired features, missing functionality
  6. **App Reliability:** Crashes, bugs, stability issues
  7. **Security Concerns:** Security features, privacy, trust

**Expected Output:** 3-5 themes per bank with keyword examples and review counts

#### 2.2.3 Initial Analysis Insights

**Preliminary Findings (Based on Rating Distribution):**

1. **High Satisfaction Areas:**
   - 62.4% 5-star reviews indicate strong overall satisfaction
   - Positive sentiment likely around: ease of use, convenience, basic functionality

2. **Critical Pain Points (17.7% 1-star reviews):**
   - Likely themes: app crashes, slow performance, login issues, transaction failures
   - Requires immediate attention from engineering teams

3. **Moderate Concerns (10.3% 2-3 star reviews):**
   - Areas needing improvement: UI/UX, feature completeness, support quality

4. **Bank-Specific Observations:**
   - **CBE:** Highest volume (7,974 reviews) suggests active user base, but also more feedback to analyze
   - **BOA:** Moderate volume (1,100 reviews), 3.4★ average indicates need for improvement
   - **Dashen:** Lower volume (497 reviews), 4.1★ suggests better satisfaction but smaller sample

### 2.3 Technical Implementation

**Scripts Developed:**
1. `task1_scraping.py` - Automated web scraping with error handling and rate limiting
2. `task1_preprocessing.py` - Comprehensive data cleaning and validation pipeline
3. `task2_sentiment.py` - Sentiment analysis with dual-model approach
4. `task2_thematic.py` - Thematic analysis with TF-IDF and clustering
5. `utils.py` - Shared utility functions for text processing

**Code Quality:**
- Modular design with separate functions for each task
- Comprehensive error handling and fallback mechanisms
- Detailed docstrings and inline documentation
- Data validation at each processing stage

---

## Page 3: Next Steps and Key Areas of Focus

### 3.1 Immediate Next Steps

#### 3.1.1 Complete Sentiment Analysis Execution
- **Action:** Run `task2_sentiment.py` on the full dataset (9,572 reviews)
- **Deliverable:** `all_banks_with_sentiment.csv` with sentiment labels and scores
- **Timeline:** Immediate
- **Success Criteria:** 90%+ coverage of reviews with sentiment scores

#### 3.1.2 Complete Thematic Analysis Execution
- **Action:** Run `task2_thematic.py` to extract themes for each bank
- **Deliverable:** `all_banks_with_sentiment_themes.csv` with identified themes
- **Timeline:** Immediate
- **Success Criteria:** 3-5 distinct themes per bank with supporting keywords

#### 3.1.3 Database Integration
- **Action:** Design and implement PostgreSQL database schema
- **Tables:** reviews, sentiment_scores, themes, bank_metrics
- **Deliverable:** Populated database with all cleaned and analyzed data
- **Timeline:** Week 3

### 3.2 Key Areas of Focus for Analysis

#### 3.2.1 Scenario 1: Retaining Users - Slow Loading Investigation

**Focus Areas:**
1. **Transaction Performance Theme Analysis:**
   - Extract all reviews mentioning "slow", "loading", "transfer", "timeout"
   - Quantify frequency across banks
   - Correlate with sentiment scores
   - Identify specific transaction types affected

2. **Rating-Sentiment Correlation:**
   - Analyze if 1-star reviews correlate with "slow" keywords
   - Determine if slow loading is a primary driver of negative sentiment
   - Compare slow loading complaints across CBE, BOA, and Dashen

3. **Recommendations:**
   - Prioritize performance optimization for identified slow operations
   - Focus on transfer functionality if it's the primary pain point
   - Benchmark against competitor performance

#### 3.2.2 Scenario 2: Enhancing Features - Competitive Analysis

**Focus Areas:**
1. **Feature Request Extraction:**
   - Identify most requested features per bank
   - Compare feature requests across banks
   - Prioritize features by frequency and sentiment impact

2. **Competitive Positioning:**
   - Analyze which banks have better feature coverage
   - Identify gaps in each bank's feature set
   - Recommend features that would improve competitive position

3. **Key Features to Analyze:**
   - Fingerprint/biometric login
   - Transaction history improvements
   - Real-time notifications
   - Bill payment features
   - Account management tools

#### 3.2.3 Scenario 3: Managing Complaints - Support Optimization

**Focus Areas:**
1. **Complaint Clustering:**
   - Group similar complaints (e.g., "login error", "password reset", "account locked")
   - Identify most frequent complaint categories
   - Map complaints to resolution strategies

2. **AI Chatbot Integration:**
   - Identify top 10-15 complaint types for chatbot training
   - Prioritize complaints that can be automated
   - Design conversation flows for common issues

3. **Support Efficiency Metrics:**
   - Track complaint frequency trends
   - Identify recurring issues that need permanent fixes
   - Measure sentiment improvement potential

### 3.3 Advanced Analysis Opportunities

#### 3.3.1 Temporal Analysis
- **Trend Analysis:** Analyze sentiment and theme trends over time
- **Update Impact:** Correlate app updates with sentiment changes
- **Seasonal Patterns:** Identify if certain issues are time-sensitive

#### 3.3.2 Comparative Analysis
- **Bank-to-Bank Comparison:** Direct comparison of satisfaction drivers and pain points
- **Best Practice Identification:** Identify what each bank does well
- **Cross-Bank Learning:** Share successful features across banks

#### 3.3.3 Predictive Insights
- **Churn Risk:** Identify reviews indicating potential customer churn
- **Feature Impact Prediction:** Predict sentiment improvement from feature additions
- **Priority Scoring:** Score issues by impact and frequency

### 3.4 Deliverables Roadmap

**Week 2 (Current):**
- ✅ Data collection and preprocessing (Task 1)
- ✅ Sentiment and thematic analysis scripts (Task 2)
- ⏳ Execute analysis on full dataset
- ⏳ Generate initial insights report

**Week 3:**
- Database schema design and implementation
- Data visualization dashboard
- Comprehensive analysis report with visualizations
- Actionable recommendations per bank

**Week 4:**
- Final report presentation
- Stakeholder review and feedback
- Implementation roadmap for recommendations

### 3.5 Success Metrics for Next Phase

1. **Analysis Completion:**
   - 100% of reviews analyzed for sentiment
   - 3-5 themes identified per bank with statistical significance
   - All three business scenarios addressed with data-driven insights

2. **Actionability:**
   - Top 5 pain points identified per bank
   - Top 5 satisfaction drivers identified per bank
   - Prioritized recommendations with expected impact

3. **Stakeholder Value:**
   - Clear, visual presentation of findings
   - Bank-specific action plans
   - Measurable improvement targets

---

## Conclusion

This project has successfully established a robust foundation for customer experience analytics through comprehensive data collection (9,572 reviews) and preprocessing. The implementation of advanced sentiment and thematic analysis pipelines positions Omega Consultancy to deliver actionable insights that will directly impact customer retention and satisfaction for CBE, BOA, and Dashen Bank.

The next phase will focus on executing the analysis, generating visualizations, and delivering bank-specific recommendations that address the three critical business scenarios: user retention, feature enhancement, and complaint management.

**Project Repository:** https://github.com/weldie10/mobile-banking-customer-feedback-analysis  
**Main Branch:** Contains complete project with all scripts and documentation

---

*Report prepared by Data Analyst Team, Omega Consultancy*

