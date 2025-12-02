"""
Task 1: Data Preprocessing Script (OOP Version)
Cleans and preprocesses scraped review data.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
from typing import Optional


class DataPreprocessor:
    """Handles data preprocessing operations."""
    
    def __init__(self, input_file: Optional[str] = None, output_file: str = '../Data/all_banks.csv'):
        """
        Initialize the preprocessor.
        
        Args:
            input_file: Path to input CSV file
            output_file: Path to output CSV file
        """
        self.input_file = input_file
        self.output_file = output_file
    
    def load_data(self) -> pd.DataFrame:
        """Load data from input file."""
        # Try to find input file
        if not self.input_file:
            input_file = '../Data/all_banks_raw.csv'
            if not os.path.exists(input_file):
                input_file = '../Data/all_banks.csv'
                print(f"Raw file not found, using existing file: {input_file}")
        else:
            input_file = self.input_file
        
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}. Please run task1_scraping.py first")
        
        df = pd.read_csv(input_file)
        print(f"Loaded {len(df)} reviews from {input_file}")
        return df
    
    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove duplicate reviews based on review text and bank.
        
        Args:
            df: DataFrame with reviews
        
        Returns:
            DataFrame with duplicates removed
        """
        initial_count = len(df)
        df = df.drop_duplicates(subset=['review', 'bank'], keep='first')
        removed = initial_count - len(df)
        print(f"Removed {removed} duplicate reviews")
        return df
    
    def handle_missing_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values in the dataset.
        
        Args:
            df: DataFrame with reviews
        
        Returns:
            DataFrame with missing data handled
        """
        initial_count = len(df)
        
        # Remove rows with missing review text
        df = df.dropna(subset=['review'])
        df = df[df['review'].str.strip() != '']
        
        # Fill missing ratings and validate
        df['rating'] = df['rating'].fillna(0)
        df = df[(df['rating'] >= 1) & (df['rating'] <= 5)]
        
        removed = initial_count - len(df)
        print(f"Removed {removed} rows with missing/invalid data")
        return df
    
    def normalize_dates(self, df: pd.DataFrame) -> pd.DataFrame:
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
            
            if isinstance(date_value, str):
                try:
                    for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y']:
                        try:
                            dt = datetime.strptime(date_value, fmt)
                            return dt.strftime('%Y-%m-%d')
                        except ValueError:
                            continue
                    dt = pd.to_datetime(date_value, errors='coerce')
                    if pd.notna(dt):
                        return dt.strftime('%Y-%m-%d')
                except:
                    pass
                return None
            
            if isinstance(date_value, datetime) or pd.api.types.is_datetime64_any_dtype(type(date_value)):
                try:
                    return pd.to_datetime(date_value).strftime('%Y-%m-%d')
                except:
                    return None
            
            return None
        
        df['date'] = df['date'].apply(parse_date)
        normalized_count = df['date'].notna().sum()
        print(f"Normalized {normalized_count} out of {len(df)} dates")
        return df
    
    def validate_data_quality(self, df: pd.DataFrame) -> pd.DataFrame:
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
        
        # Check KPIs
        total_missing_pct = (missing_review + missing_rating + missing_date + missing_bank) / (total_rows * 4) * 100
        print(f"\nOverall missing data: {total_missing_pct:.2f}%")
        if total_missing_pct < 5:
            print("✓ KPI met: <5% missing data")
        else:
            print("✗ KPI not met: >=5% missing data")
        
        if total_rows >= 1200:
            print(f"✓ KPI met: {total_rows} >= 1200 reviews")
        else:
            print(f"✗ KPI not met: {total_rows} < 1200 reviews")
        
        print("=" * 50 + "\n")
        return df
    
    def process(self) -> pd.DataFrame:
        """
        Run the complete preprocessing pipeline.
        
        Returns:
            Processed DataFrame
        """
        print("Starting data preprocessing...")
        print("=" * 50)
        
        df = self.load_data()
        
        print("\n1. Removing duplicates...")
        df = self.remove_duplicates(df)
        
        print("\n2. Handling missing data...")
        df = self.handle_missing_data(df)
        
        print("\n3. Normalizing dates...")
        df = self.normalize_dates(df)
        
        # Ensure correct column order
        df = df[['review', 'rating', 'date', 'bank', 'source']]
        
        # Validate data quality
        df = self.validate_data_quality(df)
        
        # Save cleaned data
        df.to_csv(self.output_file, index=False)
        print(f"Cleaned data saved to: {self.output_file}")
        
        return df


def main():
    """Main function for backward compatibility."""
    preprocessor = DataPreprocessor()
    return preprocessor.process()


if __name__ == "__main__":
    df = main()
