"""
Utility functions for data analysis scripts.
Common helper functions used across Task 2 scripts.
"""

import pandas as pd
import re


def clean_text(text):
    """
    Clean and normalize text for analysis.
    
    Args:
        text: Raw text string
    
    Returns:
        Cleaned text string
    """
    if pd.isna(text) or not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text


def validate_rating(rating):
    """
    Validate that rating is between 1 and 5.
    
    Args:
        rating: Rating value
    
    Returns:
        Valid rating or None
    """
    try:
        rating = float(rating)
        if 1 <= rating <= 5:
            return int(rating)
    except (ValueError, TypeError):
        pass
    return None


def get_bank_stats(df, bank_name):
    """
    Get statistics for a specific bank.
    
    Args:
        df: DataFrame with reviews
        bank_name: Name of the bank
    
    Returns:
        Dictionary with statistics
    """
    bank_df = df[df['bank'] == bank_name]
    
    stats = {
        'total_reviews': len(bank_df),
        'avg_rating': bank_df['rating'].mean() if 'rating' in bank_df.columns else None,
        'rating_distribution': bank_df['rating'].value_counts().to_dict() if 'rating' in bank_df.columns else None,
    }
    
    if 'sentiment_label' in bank_df.columns:
        stats['sentiment_distribution'] = bank_df['sentiment_label'].value_counts().to_dict()
        stats['avg_sentiment_score'] = bank_df['sentiment_score'].mean()
    
    return stats

