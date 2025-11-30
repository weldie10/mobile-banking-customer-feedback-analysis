"""
Task 2: Sentiment Analysis Script
Analyzes sentiment of reviews using distilbert-base-uncased-finetuned-sst-2-english
or VADER as a fallback.

Output: CSV with sentiment_label, sentiment_score for each review
"""

import pandas as pd
import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import warnings
warnings.filterwarnings('ignore')

# Initialize VADER as fallback
vader_analyzer = SentimentIntensityAnalyzer()

# Try to load distilbert model, fallback to VADER if it fails
try:
    print("Loading distilbert sentiment model...")
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=-1  # Use CPU
    )
    USE_DISTILBERT = True
    print("✓ Distilbert model loaded successfully")
except Exception as e:
    print(f"Could not load distilbert model: {e}")
    print("Falling back to VADER sentiment analyzer")
    USE_DISTILBERT = False


def analyze_sentiment_distilbert(text):
    """
    Analyze sentiment using distilbert model.
    
    Args:
        text: Review text
    
    Returns:
        Tuple of (label, score)
    """
    try:
        # Truncate text if too long (distilbert has token limit)
        max_length = 512
        if len(text) > max_length:
            text = text[:max_length]
        
        result = sentiment_pipeline(text)[0]
        label = result['label'].upper()
        score = result['score']
        
        # Map to our labels: POSITIVE, NEGATIVE, NEUTRAL
        if label == 'POSITIVE':
            return 'positive', score
        elif label == 'NEGATIVE':
            return 'negative', score
        else:
            return 'neutral', score
            
    except Exception as e:
        print(f"Error in distilbert analysis: {e}")
        return analyze_sentiment_vader(text)


def analyze_sentiment_vader(text):
    """
    Analyze sentiment using VADER.
    
    Args:
        text: Review text
    
    Returns:
        Tuple of (label, score)
    """
    try:
        scores = vader_analyzer.polarity_scores(text)
        compound = scores['compound']
        
        # Classify based on compound score
        if compound >= 0.05:
            label = 'positive'
            score = compound
        elif compound <= -0.05:
            label = 'negative'
            score = abs(compound)
        else:
            label = 'neutral'
            score = abs(compound)
        
        return label, score
        
    except Exception as e:
        print(f"Error in VADER analysis: {e}")
        return 'neutral', 0.0


def analyze_sentiment(text):
    """
    Main sentiment analysis function that uses the appropriate method.
    
    Args:
        text: Review text
    
    Returns:
        Tuple of (label, score)
    """
    if not text or pd.isna(text) or str(text).strip() == '':
        return 'neutral', 0.0
    
    if USE_DISTILBERT:
        return analyze_sentiment_distilbert(str(text))
    else:
        return analyze_sentiment_vader(str(text))


def aggregate_sentiment_by_bank(df):
    """
    Aggregate sentiment statistics by bank and rating.
    
    Args:
        df: DataFrame with sentiment analysis results
    
    Returns:
        Dictionary with aggregated statistics
    """
    print("\n" + "=" * 50)
    print("Sentiment Analysis Summary")
    print("=" * 50)
    
    # Overall sentiment by bank
    print("\nSentiment distribution by bank:")
    for bank in df['bank'].unique():
        bank_df = df[df['bank'] == bank]
        print(f"\n{bank}:")
        print(bank_df['sentiment_label'].value_counts())
        print(f"Mean sentiment score: {bank_df['sentiment_score'].mean():.3f}")
    
    # Sentiment by rating
    print("\n\nSentiment distribution by rating:")
    for rating in sorted(df['rating'].unique()):
        rating_df = df[df['rating'] == rating]
        print(f"\nRating {rating}:")
        print(rating_df['sentiment_label'].value_counts())
        print(f"Mean sentiment score: {rating_df['sentiment_score'].mean():.3f}")
    
    # Cross-tabulation: Bank vs Sentiment
    print("\n\nCross-tabulation: Bank vs Sentiment")
    print(pd.crosstab(df['bank'], df['sentiment_label']))
    
    print("=" * 50 + "\n")
    
    return df


def main():
    """Main sentiment analysis function."""
    print("Starting sentiment analysis...")
    print("=" * 50)
    
    # Read preprocessed data
    input_file = '../Data/all_banks.csv'
    
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        print("Please run task1_preprocessing.py first")
        return
    
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} reviews from {input_file}")
    
    # Analyze sentiment for each review
    print("\nAnalyzing sentiment for all reviews...")
    print("This may take a while...")
    
    results = []
    total = len(df)
    
    for idx, row in df.iterrows():
        if (idx + 1) % 100 == 0:
            print(f"Processed {idx + 1}/{total} reviews...")
        
        label, score = analyze_sentiment(row['review'])
        results.append({
            'review_id': idx,
            'sentiment_label': label,
            'sentiment_score': score
        })
    
    # Merge results with original data
    sentiment_df = pd.DataFrame(results)
    df = df.reset_index().rename(columns={'index': 'review_id'})
    df = pd.merge(df, sentiment_df, on='review_id', how='left')
    
    # Drop review_id if not needed
    df = df.drop('review_id', axis=1)
    
    # Aggregate and display statistics
    df = aggregate_sentiment_by_bank(df)
    
    # Check KPI: 90%+ reviews have sentiment scores
    sentiment_coverage = df['sentiment_label'].notna().sum() / len(df) * 100
    print(f"\nSentiment coverage: {sentiment_coverage:.2f}%")
    if sentiment_coverage >= 90:
        print("✓ KPI met: >=90% reviews have sentiment scores")
    else:
        print("✗ KPI not met: <90% reviews have sentiment scores")
    
    # Save results
    output_file = '../Data/all_banks_with_sentiment.csv'
    df.to_csv(output_file, index=False)
    print(f"\nResults saved to: {output_file}")
    
    return df


if __name__ == "__main__":
    df = main()

