# Customer Experience Analytics for Fintech Apps
## Project Summary Report

**Project:** Mobile Banking Customer Feedback Analysis  
**Client:** Omega Consultancy (Supporting Ethiopian Banks)  
**Date:** November 2024  
**Repository:** https://github.com/weldie10/mobile-banking-customer-feedback-analysis

---

## Page 1: Understanding and Defining the Business Objective

### 1.1 Business Context and Objectives

Omega Consultancy is supporting three major Ethiopian banks—Commercial Bank of Ethiopia (CBE), Bank of Abyssinia (BOA), and Dashen Bank—to improve their mobile banking applications. The primary goal is to enhance customer retention and satisfaction through data-driven insights from Google Play Store user reviews.

**Table 1.1: Core Business Objectives**

| Objective | Description | Success Metric |
|-----------|-------------|----------------|
| **Data Collection** | Scrape 1,200+ reviews (400+ per bank) from Google Play Store | 1,200+ reviews, <5% missing data |
| **Sentiment Analysis** | Quantify customer sentiment (positive/negative/neutral) | 90%+ reviews with sentiment scores |
| **Thematic Analysis** | Identify key themes and patterns in feedback | 3+ themes per bank with examples |
| **Insight Generation** | Identify satisfaction drivers and pain points | Top 5 drivers/pain points per bank |
| **Data Storage** | Store cleaned data in structured format | PostgreSQL database with schema |
| **Recommendations** | Deliver actionable insights for teams | Bank-specific action plans |

### 1.2 Business Scenarios Addressed

**Table 1.2: Business Scenarios and Analysis Goals**

| Scenario | Challenge | Analysis Goal | Expected Outcome |
|----------|-----------|---------------|------------------|
| **Scenario 1: Retaining Users** | CBE (4.2★), BOA (3.4★), Dashen (4.1★). Users complain about slow loading during transfers | Determine if slow loading is a broader issue; identify specific areas for investigation | Performance optimization roadmap |
| **Scenario 2: Enhancing Features** | Banks need to stay competitive by understanding desired features | Extract desired features (transfer improvements, fingerprint login, faster loading) through keyword/theme extraction | Prioritized feature request list |
| **Scenario 3: Managing Complaints** | Improve customer support efficiency and guide AI chatbot integration | Cluster and track complaints (e.g., "login error") to inform support strategies | Top 10-15 complaint categories for chatbot training |

### 1.3 Success Metrics

**Table 1.3: Project Success Metrics**

| Metric Category | Target | Status |
|----------------|--------|--------|
| **Data Quality** | 1,200+ reviews, <5% missing data | ✅ **9,572 reviews, <1% missing** |
| **Analysis Coverage** | Sentiment scores for 90%+ reviews | ⏳ Scripts ready, execution pending |
| **Theme Identification** | 3+ distinct themes per bank | ⏳ Scripts ready, execution pending |
| **Actionability** | Clear recommendations per bank | ⏳ Pending analysis execution |

---

## Page 2: Completed Work and Data Analysis

### 2.1 Data Collection Summary

**Table 2.1: Data Collection Statistics**

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| **Total Reviews** | 9,572 | 1,200 | ✅ **697% of target** |
| **CBE Reviews** | 7,974 (83.3%) | 400+ | ✅ **1,894% of target** |
| **BOA Reviews** | 1,100 (11.5%) | 400+ | ✅ **275% of target** |
| **Dashen Reviews** | 497 (5.2%) | 400+ | ✅ **124% of target** |
| **Data Source** | Google Play Store | Google Play Store | ✅ |
| **Collection Method** | Automated scraping (`google-play-scraper`) | Automated scraping | ✅ |

**Table 2.2: Reviews Distribution by Bank**

| Bank | Reviews | Percentage | Average Rating* | Status |
|------|---------|------------|-----------------|--------|
| **CBE** | 7,974 | 83.3% | 4.2★ | Highest engagement |
| **BOA** | 1,100 | 11.5% | 3.4★ | Needs improvement |
| **Dashen** | 497 | 5.2% | 4.1★ | Good satisfaction |
| **Total** | 9,572 | 100% | 3.8★ | Exceeds requirement |

*Average ratings from challenge description

### 2.2 Data Quality Metrics

**Table 2.3: Data Completeness and Quality**

| Field | Missing Count | Missing % | Status | Notes |
|-------|---------------|-----------|--------|-------|
| **Review Text** | 0 | 0% | ✅ Complete | All reviews contain text |
| **Rating** | 0 | 0% | ✅ Complete | All ratings 1-5 stars |
| **Date** | <100 | <1% | ✅ Normalized | YYYY-MM-DD format |
| **Bank** | 0 | 0% | ✅ Complete | All banks identified |
| **Source** | 0 | 0% | ✅ Complete | All from Google Play |
| **Overall Missing Data** | <1% | <1% | ✅ **Exceeds KPI** | Target: <5% |

**Table 2.4: Rating Distribution**

| Rating | Count | Percentage | Interpretation |
|--------|-------|------------|----------------|
| **5 Stars** | 5,971 | 62.4% | Strong positive sentiment |
| **4 Stars** | 925 | 9.7% | Positive feedback |
| **3 Stars** | 595 | 6.2% | Neutral/moderate |
| **2 Stars** | 390 | 4.1% | Negative concerns |
| **1 Star** | 1,690 | 17.7% | Critical pain points |
| **Total** | 9,571 | 100% | Average: 3.8/5.0 |

**Key Observations:**
- 62.4% 5-star reviews indicate strong overall satisfaction
- 17.7% 1-star reviews highlight critical pain points requiring immediate attention
- CBE dominates dataset (83.3%), indicating highest user engagement

### 2.3 Preprocessing Pipeline

**Table 2.5: Preprocessing Steps Completed**

| Step | Description | Result |
|------|-------------|--------|
| **1. Duplicate Removal** | Remove exact duplicates (review text + bank) | Duplicates eliminated |
| **2. Missing Data Handling** | Remove rows with missing critical fields | Clean dataset |
| **3. Date Normalization** | Standardize to YYYY-MM-DD format | Consistent date format |
| **4. Data Validation** | Validate ratings (1-5), bank names | All data validated |
| **5. Output Format** | CSV: review, rating, date, bank, source | `Data/all_banks.csv` |

### 2.4 Sentiment and Thematic Analysis Implementation

**Table 2.6: Analysis Methodology**

| Analysis Type | Method | Model/Library | Output | Status |
|---------------|--------|---------------|--------|--------|
| **Sentiment Analysis** | Transformer + Fallback | distilbert-base-uncased-finetuned-sst-2-english / VADER | Sentiment label + score (0-1) | ✅ Script ready |
| **Thematic Analysis** | TF-IDF + Clustering | scikit-learn TF-IDF, rule-based clustering | 7 themes per bank | ✅ Script ready |
| **Text Preprocessing** | Cleaning pipeline | Custom utils.py | Cleaned text | ✅ Implemented |

**Table 2.7: Identified Themes for Analysis**

| Theme ID | Theme Name | Key Keywords | Use Case |
|----------|------------|--------------|----------|
| **T1** | Account Access Issues | login, password, authentication, error | Scenario 3: Complaint management |
| **T2** | Transaction Performance | slow, transfer, loading, timeout, delay | Scenario 1: Retaining users |
| **T3** | User Interface & Experience | UI, design, navigation, easy, confusing | General improvement |
| **T4** | Customer Support | support, help, service, response, complaint | Scenario 3: Support optimization |
| **T5** | Feature Requests | feature, add, need, fingerprint, biometric | Scenario 2: Feature enhancement |
| **T6** | App Reliability | crash, bug, error, freeze, stable | General improvement |
| **T7** | Security Concerns | security, safe, privacy, trust, breach | General improvement |

### 2.5 Technical Implementation

**Table 2.8: Scripts Developed**

| Script | Purpose | Lines of Code | Features |
|--------|---------|---------------|----------|
| `task1_scraping.py` | Web scraping | 151 | Error handling, rate limiting |
| `task1_preprocessing.py` | Data cleaning | 221 | Validation, normalization |
| `task2_sentiment.py` | Sentiment analysis | 228 | Dual-model approach |
| `task2_thematic.py` | Thematic analysis | 285 | TF-IDF, clustering |
| `utils.py` | Shared utilities | 81 | Text cleaning, validation |
| **Total** | **5 scripts** | **966 lines** | **Modular, documented** |

---

## Page 3: Initial Analysis Insights and Findings

### 3.1 Preliminary Findings Based on Rating Distribution

**Table 3.1: Initial Insights by Rating Category**

| Rating Category | Count | % | Likely Themes | Priority | Action Required |
|----------------|-------|---|--------------|----------|----------------|
| **High Satisfaction (5★)** | 5,971 | 62.4% | Ease of use, convenience, basic functionality | Monitor | Maintain strengths |
| **Positive (4★)** | 925 | 9.7% | Good features, minor improvements needed | Medium | Incremental improvements |
| **Neutral (3★)** | 595 | 6.2% | UI/UX, feature completeness | Medium | Address gaps |
| **Negative (2★)** | 390 | 4.1% | Performance issues, missing features | High | Investigate causes |
| **Critical (1★)** | 1,690 | 17.7% | Crashes, slow performance, login issues, failures | **Critical** | **Immediate action** |

### 3.2 Bank-Specific Observations

**Table 3.2: Bank Comparison and Characteristics**

| Bank | Reviews | % of Total | Avg Rating* | Characteristics | Key Focus Areas |
|------|---------|------------|-------------|----------------|----------------|
| **CBE** | 7,974 | 83.3% | 4.2★ | Highest engagement, largest user base | Performance optimization, scalability |
| **BOA** | 1,100 | 11.5% | 3.4★ | Lowest rating, needs improvement | Critical issues, feature gaps |
| **Dashen** | 497 | 5.2% | 4.1★ | Good satisfaction, smaller sample | Feature expansion, user growth |

*From challenge description

### 3.3 Expected Analysis Outcomes

**Table 3.3: Expected Results from Sentiment Analysis**

| Bank | Expected Positive % | Expected Negative % | Expected Neutral % | Focus Area |
|------|---------------------|----------------------|---------------------|------------|
| **CBE** | ~65-70% | ~20-25% | ~5-10% | Maintain satisfaction, address pain points |
| **BOA** | ~40-50% | ~40-50% | ~5-10% | Critical improvement needed |
| **Dashen** | ~60-65% | ~25-30% | ~5-10% | Enhance features, grow user base |

**Table 3.4: Expected Theme Distribution (Top 3 per Bank)**

| Bank | Expected Top Theme 1 | Expected Top Theme 2 | Expected Top Theme 3 |
|------|---------------------|---------------------|---------------------|
| **CBE** | Transaction Performance | App Reliability | Feature Requests |
| **BOA** | Account Access Issues | Transaction Performance | Customer Support |
| **Dashen** | Feature Requests | User Interface | Transaction Performance |

---

## Page 4: Next Steps and Key Areas of Focus

### 4.1 Immediate Next Steps - Task 3 & Task 4 Implementation

**Table 4.1: Task 3 - Database Integration Roadmap**

| Component | Action | Deliverable | Success Criteria |
|-----------|--------|-------------|------------------|
| **Schema Design** | Design PostgreSQL database schema | ER diagram, schema SQL | Normalized tables, relationships defined |
| **Table Creation** | Create tables: reviews, sentiment_scores, themes, bank_metrics | Database schema file | All tables with proper constraints |
| **Data Migration** | Load cleaned data from CSV to PostgreSQL | Populated database | 100% data migrated, integrity verified |
| **Indexing** | Create indexes on key columns | Optimized queries | Fast query performance |
| **Connection Script** | Develop Python script for database operations | `task3_database.py` | CRUD operations functional |

**Table 4.2: Task 4 - Visualization and Reporting Roadmap**

| Component | Action | Deliverable | Success Criteria |
|-----------|--------|-------------|------------------|
| **Dashboard Design** | Design interactive dashboard layout | Dashboard mockup | All key metrics visualized |
| **Visualization Scripts** | Create visualization scripts using matplotlib/seaborn | `task4_visualization.py` | Charts for all scenarios |
| **Key Visualizations** | Generate: sentiment distribution, theme analysis, bank comparison | PNG/PDF charts | Clear, actionable insights |
| **Report Generation** | Create comprehensive analysis report | Final report document | All scenarios addressed |
| **Presentation** | Prepare stakeholder presentation | Presentation slides | Clear recommendations |

### 4.2 Task 3: Database Integration Details

**Table 4.3: Database Schema Design**

| Table Name | Purpose | Key Columns | Relationships |
|------------|---------|-------------|--------------|
| **reviews** | Store raw review data | review_id, bank, rating, review, date, source | Primary table |
| **sentiment_scores** | Store sentiment analysis results | review_id, sentiment_label, sentiment_score, model_used | Foreign key to reviews |
| **themes** | Store identified themes | theme_id, theme_name, keywords | Many-to-many with reviews |
| **review_themes** | Junction table | review_id, theme_id, confidence_score | Links reviews to themes |
| **bank_metrics** | Store aggregated metrics | bank, metric_name, metric_value, calculation_date | Aggregated from reviews |

**Table 4.4: Database Implementation Tasks**

| Task | Description | Priority |
|------|-------------|----------|
| **Schema Design** | Design normalized schema with proper relationships | Critical |
| **Data Types** | Define appropriate data types (VARCHAR, INTEGER, DATE, FLOAT) | High |
| **Constraints** | Add primary keys, foreign keys, check constraints | High |
| **Indexes** | Create indexes on bank, date, rating, sentiment_label | Medium |
| **Data Loading** | Write ETL script to load CSV data into PostgreSQL | Critical |
| **Data Validation** | Verify data integrity after loading | Critical |
| **Query Optimization** | Optimize queries for dashboard performance | Medium |

### 4.3 Task 4: Visualization and Reporting Details

**Table 4.5: Required Visualizations**

| Visualization Type | Purpose | Data Source | Use Case |
|-------------------|--------|-------------|----------|
| **Sentiment Distribution** | Show sentiment breakdown by bank | sentiment_scores | Overall satisfaction overview |
| **Rating Distribution** | Display rating distribution charts | reviews | Customer satisfaction levels |
| **Theme Frequency** | Bar chart of theme frequency per bank | themes, review_themes | Identify common issues |
| **Bank Comparison** | Side-by-side comparison charts | All tables | Competitive analysis |
| **Trend Analysis** | Time series of sentiment over time | reviews, sentiment_scores | Identify improvement trends |
| **Pain Points Heatmap** | Heatmap of issues by bank and theme | review_themes | Prioritize improvements |
| **Feature Requests** | Word cloud or bar chart of requested features | themes (Feature Requests) | Scenario 2 analysis |
| **Complaint Categories** | Pie chart of complaint types | themes (Account Access, Support) | Scenario 3 analysis |

**Table 4.6: Report Structure for Task 4**

| Section | Content | Visualizations |
|---------|---------|----------------|
| **Executive Summary** | Key findings, recommendations | High-level dashboard |
| **Scenario 1 Analysis** | Slow loading investigation | Performance charts, correlation analysis |
| **Scenario 2 Analysis** | Feature enhancement recommendations | Feature request charts, gap analysis |
| **Scenario 3 Analysis** | Complaint management strategy | Complaint clustering, chatbot training data |
| **Bank-Specific Insights** | Individual bank recommendations | Bank comparison charts |
| **Action Plan** | Prioritized recommendations | Roadmap visualization |

### 4.4 Key Focus Areas by Business Scenario

| Focus Area | Analysis Method | Expected Output | Priority |
|------------|----------------|-----------------|----------|
| **Transaction Performance** | Extract reviews with "slow", "loading", "transfer", "timeout" | Frequency by bank, transaction type | High |
| **Rating-Sentiment Correlation** | Correlate 1-star reviews with performance keywords | Performance impact on satisfaction | Critical |
| **Bank Comparison** | Compare slow loading complaints across banks | Bank-specific performance issues | High |
| **Recommendations** | Prioritize optimization areas | Performance roadmap | Critical |

**Table 4.7: Scenario 1 - Retaining Users (Slow Loading Investigation)**

| Focus Area | Analysis Method | Expected Output | Priority |
|------------|----------------|-----------------|----------|
| **Feature Requests** | Extract feature-related keywords | Top requested features per bank | High |
| **Competitive Positioning** | Compare feature coverage across banks | Feature gap analysis | Medium |
| **Key Features** | Analyze: fingerprint login, transaction history, notifications | Prioritized feature list | High |
| **Recommendations** | Rank features by frequency and impact | Feature development roadmap | High |

**Table 4.8: Scenario 2 - Enhancing Features (Competitive Analysis)**

| Focus Area | Analysis Method | Expected Output | Priority |
|------------|----------------|-----------------|----------|
| **Feature Requests** | Extract feature-related keywords | Top requested features per bank | High |
| **Competitive Positioning** | Compare feature coverage across banks | Feature gap analysis | Medium |
| **Key Features** | Analyze: fingerprint login, transaction history, notifications | Prioritized feature list | High |
| **Recommendations** | Rank features by frequency and impact | Feature development roadmap | High |

**Table 4.9: Scenario 3 - Managing Complaints (Support Optimization)**

| Focus Area | Analysis Method | Expected Output | Priority |
|------------|----------------|-----------------|----------|
| **Complaint Clustering** | Group similar complaints (login error, password reset, etc.) | Top 10-15 complaint categories | Critical |
| **AI Chatbot Training** | Identify automatable complaints | Chatbot conversation flows | High |
| **Support Efficiency** | Track complaint frequency and trends | Support optimization strategy | Medium |
| **Resolution Mapping** | Map complaints to resolution strategies | Support playbook | High |

### 4.5 Deliverables Roadmap - Task 3 & Task 4 Focus

**Table 4.10: Project Timeline and Deliverables**

| Week | Task | Deliverables | Status |
|------|------|-------------|--------|
| **Week 2 (Completed)** | **Task 1 & Task 2** | ✅ Data collection (9,572 reviews)<br>✅ Preprocessing pipeline<br>✅ Sentiment analysis scripts<br>✅ Thematic analysis scripts | ✅ Complete |
| **Week 3 (Current)** | **Task 3: Database** | ⏳ PostgreSQL schema design<br>⏳ Database implementation<br>⏳ Data migration scripts<br>⏳ Data loading and validation | In Progress |
| **Week 4 (Next)** | **Task 4: Visualization** | ⏳ Visualization scripts<br>⏳ Dashboard creation<br>⏳ Comprehensive analysis report<br>⏳ Bank-specific recommendations<br>⏳ Final presentation | Planned |

### 4.6 Success Metrics for Task 3 & Task 4

**Table 4.11: Task 3 Success Criteria**

| Metric Category | Target | Measurement Method |
|----------------|--------|-------------------|
| **Schema Design** | Normalized schema with proper relationships | ER diagram review, schema validation |
| **Data Migration** | 100% of reviews loaded into database | Data count verification, integrity checks |
| **Query Performance** | All queries execute in <2 seconds | Performance testing |
| **Data Integrity** | Zero data loss, all constraints satisfied | Validation scripts |

**Table 4.12: Task 4 Success Criteria**

| Metric Category | Target | Measurement Method |
|----------------|--------|-------------------|
| **Visualization Coverage** | All 8 visualization types created | Visualization checklist |
| **Report Completeness** | All 3 scenarios addressed with data-driven insights | Report review, stakeholder feedback |
| **Actionability** | Top 5 pain points per bank identified<br>Top 5 satisfaction drivers per bank identified<br>Prioritized recommendations with impact | Ranked lists, impact scores |
| **Stakeholder Value** | Clear visual presentation<br>Bank-specific action plans<br>Measurable improvement targets | Presentation quality, feedback |

### 4.7 Task 3 & Task 4 Implementation Checklist

**Table 4.13: Task 3 Implementation Checklist**

| Task | Component | Status | Notes |
|------|-----------|-------|-------|
| **Database Setup** | Install PostgreSQL | ⏳ | Local or cloud instance |
| **Schema Design** | Create ER diagram | ⏳ | Normalize to 3NF |
| **Table Creation** | Write CREATE TABLE statements | ⏳ | Include constraints |
| **Data Migration** | Write ETL script | ⏳ | Load from CSV |
| **Testing** | Verify data integrity | ⏳ | Run validation queries |
| **Documentation** | Document schema and procedures | ⏳ | For future reference |

**Table 4.14: Task 4 Implementation Checklist**

| Task | Component | Status | Notes |
|------|-----------|-------|-------|
| **Visualization Setup** | Install matplotlib, seaborn | ⏳ | Or use Plotly for interactivity |
| **Chart Creation** | Create all 8 visualization types | ⏳ | Follow design guidelines |
| **Report Writing** | Write comprehensive analysis report | ⏳ | Address all 3 scenarios |
| **Dashboard** | Create interactive dashboard | ⏳ | Optional but recommended |
| **Presentation** | Prepare stakeholder presentation | ⏳ | Highlight key insights |
| **Documentation** | Document visualization code | ⏳ | For reproducibility |

---

## Conclusion

This project has successfully established a robust foundation for customer experience analytics through comprehensive data collection (9,572 reviews, 697% of target) and preprocessing (<1% missing data, exceeding 5% KPI threshold). The implementation of advanced sentiment and thematic analysis pipelines positions Omega Consultancy to deliver actionable insights that will directly impact customer retention and satisfaction for CBE, BOA, and Dashen Bank.

**Key Achievements (Task 1 & Task 2):**
- ✅ 9,572 reviews collected (exceeds 1,200 requirement by 697%)
- ✅ <1% missing data (exceeds <5% KPI threshold)
- ✅ Complete preprocessing pipeline implemented
- ✅ Sentiment and thematic analysis scripts ready
- ✅ All three business scenarios addressed with analysis framework

**Next Phase Focus - Task 3 & Task 4:**
**Task 3 (Database Integration):** Design and implement PostgreSQL database schema, migrate all cleaned and analyzed data, ensure data integrity and query performance optimization.

**Task 4 (Visualization & Reporting):** Create comprehensive visualizations for all three business scenarios, generate actionable analysis report with bank-specific recommendations, and prepare stakeholder presentation.

---

*Report prepared by Data Analyst Team, Omega Consultancy*
