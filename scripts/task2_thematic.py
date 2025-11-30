"""
Task 2: Thematic Analysis Script
Extracts keywords and clusters them into themes for each bank.

Uses TF-IDF for keyword extraction and manual/rule-based clustering.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import os
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Try to import spacy for advanced NLP
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    USE_SPACY = True
except:
    print("spaCy not available, using basic text processing")
    USE_SPACY = False


def preprocess_text(text):
    """
    Preprocess text for keyword extraction.
    
    Args:
        text: Raw review text
    
    Returns:
        Preprocessed text
    """
    if pd.isna(text):
        return ""
    
    text = str(text).lower()
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text


def extract_keywords_tfidf(reviews, max_features=50, ngram_range=(1, 2)):
    """
    Extract keywords using TF-IDF.
    
    Args:
        reviews: List of review texts
        max_features: Maximum number of features to extract
        ngram_range: Range of n-grams to consider
    
    Returns:
        List of keywords and their importance scores
    """
    # Preprocess reviews
    processed_reviews = [preprocess_text(review) for review in reviews]
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        stop_words='english',
        min_df=2,  # Word must appear in at least 2 documents
        max_df=0.95  # Word must appear in less than 95% of documents
    )
    
    try:
        tfidf_matrix = vectorizer.fit_transform(processed_reviews)
        feature_names = vectorizer.get_feature_names_out()
        
        # Get mean TF-IDF scores for each feature
        mean_scores = np.array(tfidf_matrix.mean(axis=0)).flatten()
        
        # Create keyword-score pairs
        keywords = list(zip(feature_names, mean_scores))
        keywords.sort(key=lambda x: x[1], reverse=True)
        
        return keywords
    except Exception as e:
        print(f"Error in TF-IDF extraction: {e}")
        return []


def cluster_keywords_into_themes(keywords, bank_name):
    """
    Cluster keywords into themes using rule-based approach.
    
    Args:
        keywords: List of (keyword, score) tuples
        bank_name: Name of the bank (for context)
    
    Returns:
        Dictionary mapping themes to keywords
    """
    # Define theme patterns/keywords
    theme_patterns = {
        'Account Access Issues': [
            'login', 'password', 'account', 'access', 'unable', 'cannot', 'error',
            'failed', 'blocked', 'locked', 'verify', 'authentication'
        ],
        'Transaction Performance': [
            'transfer', 'transaction', 'slow', 'fast', 'speed', 'timeout',
            'pending', 'delay', 'instant', 'quick', 'wait', 'loading'
        ],
        'User Interface & Experience': [
            'ui', 'interface', 'design', 'layout', 'easy', 'simple', 'user friendly',
            'beautiful', 'modern', 'confusing', 'complicated', 'navigation', 'menu'
        ],
        'Customer Support': [
            'support', 'help', 'service', 'contact', 'response', 'assistance',
            'complaint', 'issue', 'problem', 'resolve', 'fix'
        ],
        'Feature Requests': [
            'feature', 'add', 'need', 'want', 'missing', 'request', 'suggest',
            'improve', 'enhance', 'option', 'functionality', 'fingerprint', 'biometric'
        ],
        'App Reliability': [
            'crash', 'bug', 'error', 'freeze', 'hang', 'close', 'stop', 'work',
            'stable', 'reliable', 'problem', 'issue', 'fix', 'update'
        ],
        'Security Concerns': [
            'security', 'safe', 'secure', 'privacy', 'data', 'protection',
            'hack', 'breach', 'trust', 'worried'
        ]
    }
    
    # Map keywords to themes
    theme_keywords = {theme: [] for theme in theme_patterns.keys()}
    unassigned = []
    
    for keyword, score in keywords:
        keyword_lower = keyword.lower()
        assigned = False
        
        for theme, patterns in theme_patterns.items():
            for pattern in patterns:
                if pattern in keyword_lower or keyword_lower in pattern:
                    theme_keywords[theme].append((keyword, score))
                    assigned = True
                    break
            if assigned:
                break
        
        if not assigned:
            unassigned.append((keyword, score))
    
    # Filter out themes with no keywords
    theme_keywords = {k: v for k, v in theme_keywords.items() if v}
    
    # If we have unassigned keywords, create a "General" theme
    if unassigned:
        theme_keywords['General'] = unassigned[:10]  # Top 10 unassigned
    
    return theme_keywords


def identify_review_themes(review_text, theme_keywords):
    """
    Identify which themes are present in a review.
    
    Args:
        review_text: Review text
        theme_keywords: Dictionary of themes and their keywords
    
    Returns:
        List of theme names present in the review
    """
    review_lower = preprocess_text(review_text)
    identified_themes = []
    
    for theme, keywords in theme_keywords.items():
        for keyword, _ in keywords:
            if keyword in review_lower:
                identified_themes.append(theme)
                break  # Only need one keyword match per theme
    
    return identified_themes


def main():
    """Main thematic analysis function."""
    print("Starting thematic analysis...")
    print("=" * 50)
    
    # Read data with sentiment analysis
    input_file = '../Data/all_banks_with_sentiment.csv'
    
    # Fallback to basic data if sentiment file doesn't exist
    if not os.path.exists(input_file):
        input_file = '../Data/all_banks.csv'
        print(f"Sentiment file not found, using: {input_file}")
    
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        print("Please run task1_preprocessing.py first")
        return
    
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} reviews from {input_file}")
    
    # Analyze themes for each bank
    all_results = []
    
    for bank in df['bank'].unique():
        print(f"\nAnalyzing themes for {bank}...")
        bank_df = df[df['bank'] == bank].copy()
        bank_reviews = bank_df['review'].tolist()
        
        # Extract keywords
        print(f"  Extracting keywords from {len(bank_reviews)} reviews...")
        keywords = extract_keywords_tfidf(bank_reviews, max_features=50)
        
        print(f"  Found {len(keywords)} keywords")
        print(f"  Top 10 keywords: {[k[0] for k in keywords[:10]]}")
        
        # Cluster into themes
        print(f"  Clustering keywords into themes...")
        theme_keywords = cluster_keywords_into_themes(keywords, bank)
        
        print(f"  Identified {len(theme_keywords)} themes:")
        for theme, kw_list in theme_keywords.items():
            print(f"    - {theme}: {len(kw_list)} keywords")
            print(f"      Top keywords: {[k[0] for k in kw_list[:5]]}")
        
        # Identify themes for each review
        print(f"  Identifying themes in reviews...")
        bank_df['themes'] = bank_df['review'].apply(
            lambda x: identify_review_themes(x, theme_keywords)
        )
        
        # Convert themes list to string for CSV storage
        bank_df['themes_str'] = bank_df['themes'].apply(lambda x: '; '.join(x) if x else 'None')
        
        all_results.append(bank_df)
    
    # Combine all banks
    result_df = pd.concat(all_results, ignore_index=True)
    
    # Check KPI: 3+ themes per bank
    print("\n" + "=" * 50)
    print("Thematic Analysis Summary")
    print("=" * 50)
    
    for bank in result_df['bank'].unique():
        bank_df = result_df[result_df['bank'] == bank]
        # Count unique themes
        all_themes = []
        for themes_list in bank_df['themes']:
            all_themes.extend(themes_list)
        unique_themes = set(all_themes)
        
        print(f"\n{bank}:")
        print(f"  Unique themes identified: {len(unique_themes)}")
        print(f"  Themes: {', '.join(sorted(unique_themes))}")
        
        # Theme frequency
        theme_counts = Counter(all_themes)
        print(f"  Top themes:")
        for theme, count in theme_counts.most_common(5):
            print(f"    - {theme}: {count} reviews")
        
        if len(unique_themes) >= 3:
            print(f"  ✓ KPI met: >=3 themes identified")
        else:
            print(f"  ✗ KPI not met: <3 themes identified")
    
    print("=" * 50 + "\n")
    
    # Save results
    output_file = '../Data/all_banks_with_sentiment_themes.csv'
    result_df.to_csv(output_file, index=False)
    print(f"Results saved to: {output_file}")
    
    return result_df


if __name__ == "__main__":
    df = main()

