"""
Task 1: Data Preprocessing Script
Cleans and preprocesses scraped review data:
- Remove duplicates
- Handle missing data
- Normalize dates
- Validate data quality

Output: Clean CSV with columns: review, rating, date, bank, source
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def remove_duplicates(df):
    """
    Remove duplicate reviews based on review text and bank.
    
    Args:
        df: DataFrame with reviews
    
    Returns:
        DataFrame with duplicates removed
    """
    initial_count = len(df)
    # Remove exact duplicates
    df = df.drop_duplicates(subset=['review', 'bank'], keep='first')
    removed = initial_count - len(df)
    print(f"Removed {removed} duplicate reviews")
    return df


def handle_missing_data(df):
    """
    Handle missing values in the dataset.
    
    Args:
        df: DataFrame with reviews
    
    Returns:
        DataFrame with missing data handled
    """
    initial_count = len(df)
    
    # Remove rows with missing review text (critical field)
    df = df.dropna(subset=['review'])
    
    # Remove rows with empty review text
    df = df[df['review'].str.strip() != '']
    
    # Fill missing ratings with 0 (will be filtered out if needed)
    df['rating'] = df['rating'].fillna(0)
    
    # Remove rows with invalid ratings (should be 1-5)
    df = df[(df['rating'] >= 1) & (df['rating'] <= 5)]
    
    # Handle missing dates - set to None (will be handled in normalization)
    # Don't remove rows with missing dates as they might still be useful
    
    removed = initial_count - len(df)
    print(f"Removed {removed} rows with missing/invalid data")
    return df


def normalize_dates(df):
    """
    Normalize date formats to YYYY-MM-DD.
    
    Args:
        df: DataFrame with reviews
    
    Returns:
        DataFrame with normalized dates
    """
    def parse_date(date_value):
        """Parse various date formats to YYYY-MM-DD."""
        if pd.isna(date_value):
            return None
        
        # If already a string in YYYY-MM-DD format
        if isinstance(date_value, str):
            try:
                # Try parsing common formats
                for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y']:
                    try:
                        dt = datetime.strptime(date_value, fmt)
                        return dt.strftime('%Y-%m-%d')
                    except ValueError:
                        continue
                # If all formats fail, try pandas parsing
                dt = pd.to_datetime(date_value, errors='coerce')
                if pd.notna(dt):
                    return dt.strftime('%Y-%m-%d')
            except:
                pass
            return None
        
        # If it's already a datetime object
        if isinstance(date_value, datetime) or pd.api.types.is_datetime64_any_dtype(type(date_value)):
            try:
                return pd.to_datetime(date_value).strftime('%Y-%m-%d')
            except:
                return None
        
        return None
    
    df['date'] = df['date'].apply(parse_date)
    
    # Count how many dates were successfully normalized
    normalized_count = df['date'].notna().sum()
    print(f"Normalized {normalized_count} out of {len(df)} dates")
    
    return df


def validate_data_quality(df):
    """
    Validate data quality and report statistics.
    
    Args:
        df: DataFrame with reviews
    
    Returns:
        DataFrame (validated)
    """
    print("\n" + "=" * 50)
    print("Data Quality Report")
    print("=" * 50)
    
    total_rows = len(df)
    print(f"Total reviews: {total_rows}")
    
    # Missing data check
    missing_review = df['review'].isna().sum()
    missing_rating = df['rating'].isna().sum()
    missing_date = df['date'].isna().sum()
    missing_bank = df['bank'].isna().sum()
    
    print(f"\nMissing data:")
    print(f"  Review text: {missing_review} ({missing_review/total_rows*100:.2f}%)")
    print(f"  Rating: {missing_rating} ({missing_rating/total_rows*100:.2f}%)")
    print(f"  Date: {missing_date} ({missing_date/total_rows*100:.2f}%)")
    print(f"  Bank: {missing_bank} ({missing_bank/total_rows*100:.2f}%)")
    
    # Rating distribution
    print(f"\nRating distribution:")
    print(df['rating'].value_counts().sort_index())
    
    # Reviews per bank
    print(f"\nReviews per bank:")
    print(df['bank'].value_counts())
    
    # Check KPI: <5% missing data
    total_missing_pct = (missing_review + missing_rating + missing_date + missing_bank) / (total_rows * 4) * 100
    print(f"\nOverall missing data: {total_missing_pct:.2f}%")
    if total_missing_pct < 5:
        print("✓ KPI met: <5% missing data")
    else:
        print("✗ KPI not met: >=5% missing data")
    
    # Check KPI: 1200+ reviews
    if total_rows >= 1200:
        print(f"✓ KPI met: {total_rows} >= 1200 reviews")
    else:
        print(f"✗ KPI not met: {total_rows} < 1200 reviews")
    
    print("=" * 50 + "\n")
    
    return df


def main():
    """Main preprocessing function."""
    print("Starting data preprocessing...")
    print("=" * 50)
    
    # Read raw data
    input_file = '../Data/all_banks_raw.csv'
    
    # If raw file doesn't exist, try reading the existing all_banks.csv
    if not os.path.exists(input_file):
        input_file = '../Data/all_banks.csv'
        print(f"Raw file not found, using existing file: {input_file}")
    
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        print("Please run task1_scraping.py first")
        return
    
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} reviews from {input_file}")
    
    # Preprocessing steps
    print("\n1. Removing duplicates...")
    df = remove_duplicates(df)
    
    print("\n2. Handling missing data...")
    df = handle_missing_data(df)
    
    print("\n3. Normalizing dates...")
    df = normalize_dates(df)
    
    # Ensure correct column order: review, rating, date, bank, source
    df = df[['review', 'rating', 'date', 'bank', 'source']]
    
    # Validate data quality
    df = validate_data_quality(df)
    
    # Save cleaned data
    output_file = '../Data/all_banks.csv'
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to: {output_file}")
    
    return df


if __name__ == "__main__":
    df = main()

