"""
Task 2: Sentiment Analysis Script (OOP Version)
Analyzes sentiment of reviews using distilbert or VADER.
"""

import pandas as pd
import numpy as np
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import warnings
from utils import TextProcessor
from typing import Tuple, Optional

warnings.filterwarnings('ignore')


class SentimentAnalyzer:
    """Handles sentiment analysis of reviews."""
    
    def __init__(self, use_distilbert: bool = True):
        """
        Initialize the sentiment analyzer.
        
        Args:
            use_distilbert: Whether to use distilbert model (falls back to VADER if fails)
        """
        self.text_processor = TextProcessor()
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.use_distilbert = False
        self.sentiment_pipeline = None
        
        if use_distilbert:
            self._load_distilbert()
    
    def _load_distilbert(self):
        """Try to load distilbert model."""
        try:
            print("Loading distilbert sentiment model...")
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=-1
            )
            self.use_distilbert = True
            print("✓ Distilbert model loaded successfully")
        except Exception as e:
            print(f"Could not load distilbert model: {e}")
            print("Falling back to VADER sentiment analyzer")
            self.use_distilbert = False
    
    def analyze_with_distilbert(self, text: str) -> Tuple[str, float]:
        """
        Analyze sentiment using distilbert model.
        
        Args:
            text: Review text
        
        Returns:
            Tuple of (label, score)
        """
        try:
            max_length = 512
            if len(text) > max_length:
                text = text[:max_length]
            
            result = self.sentiment_pipeline(text)[0]
            label = result['label'].upper()
            score = result['score']
            
            if label == 'POSITIVE':
                return 'positive', score
            elif label == 'NEGATIVE':
                return 'negative', score
            else:
                return 'neutral', score
        except Exception as e:
            print(f"Error in distilbert analysis: {e}")
            return self.analyze_with_vader(text)
    
    def analyze_with_vader(self, text: str) -> Tuple[str, float]:
        """
        Analyze sentiment using VADER.
        
        Args:
            text: Review text
        
        Returns:
            Tuple of (label, score)
        """
        try:
            scores = self.vader_analyzer.polarity_scores(text)
            compound = scores['compound']
            
            if compound >= 0.05:
                return 'positive', compound
            elif compound <= -0.05:
                return 'negative', abs(compound)
            else:
                return 'neutral', abs(compound)
        except Exception as e:
            print(f"Error in VADER analysis: {e}")
            return 'neutral', 0.0
    
    def analyze(self, text: str) -> Tuple[str, float]:
        """
        Main sentiment analysis function.
        
        Args:
            text: Review text
        
        Returns:
            Tuple of (label, score)
        """
        if not text or pd.isna(text) or str(text).strip() == '':
            return 'neutral', 0.0
        
        cleaned_text = self.text_processor.clean_text(str(text))
        if not cleaned_text:
            return 'neutral', 0.0
        
        if self.use_distilbert:
            return self.analyze_with_distilbert(cleaned_text)
        else:
            return self.analyze_with_vader(cleaned_text)
    
    def analyze_dataframe(self, df: pd.DataFrame, review_column: str = 'review') -> pd.DataFrame:
        """
        Analyze sentiment for all reviews in a DataFrame.
        
        Args:
            df: DataFrame with reviews
            review_column: Name of the review column
        
        Returns:
            DataFrame with sentiment labels and scores added
        """
        print("\nAnalyzing sentiment for all reviews...")
        print("This may take a while...")
        
        results = []
        total = len(df)
        
        for idx, row in df.iterrows():
            if (idx + 1) % 100 == 0:
                print(f"Processed {idx + 1}/{total} reviews...")
            
            label, score = self.analyze(row[review_column])
            results.append({
                'review_id': idx,
                'sentiment_label': label,
                'sentiment_score': score
            })
        
        sentiment_df = pd.DataFrame(results)
        df = df.reset_index().rename(columns={'index': 'review_id'})
        df = pd.merge(df, sentiment_df, on='review_id', how='left')
        df = df.drop('review_id', axis=1)
        
        return df
    
    def aggregate_statistics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate sentiment statistics by bank and rating.
        
        Args:
            df: DataFrame with sentiment analysis results
        
        Returns:
            DataFrame (same, for chaining)
        """
        print("\n" + "=" * 50)
        print("Sentiment Analysis Summary")
        print("=" * 50)
        
        if 'sentiment_label' not in df.columns:
            print("No sentiment data available")
            return df
        
        # Overall sentiment by bank
        print("\nSentiment distribution by bank:")
        for bank in df['bank'].unique():
            bank_df = df[df['bank'] == bank]
            print(f"\n{bank}:")
            print(bank_df['sentiment_label'].value_counts())
            if 'sentiment_score' in bank_df.columns:
                print(f"Mean sentiment score: {bank_df['sentiment_score'].mean():.3f}")
        
        # Sentiment by rating
        print("\n\nSentiment distribution by rating:")
        for rating in sorted(df['rating'].unique()):
            rating_df = df[df['rating'] == rating]
            print(f"\nRating {rating}:")
            print(rating_df['sentiment_label'].value_counts())
            if 'sentiment_score' in rating_df.columns:
                print(f"Mean sentiment score: {rating_df['sentiment_score'].mean():.3f}")
        
        # Cross-tabulation
        print("\n\nCross-tabulation: Bank vs Sentiment")
        print(pd.crosstab(df['bank'], df['sentiment_label']))
        
        print("=" * 50 + "\n")
        return df
    
    def check_kpi(self, df: pd.DataFrame) -> bool:
        """
        Check if sentiment analysis KPI is met (90%+ coverage).
        
        Args:
            df: DataFrame with sentiment data
        
        Returns:
            True if KPI met, False otherwise
        """
        if 'sentiment_label' not in df.columns:
            return False
        
        sentiment_coverage = df['sentiment_label'].notna().sum() / len(df) * 100
        print(f"\nSentiment coverage: {sentiment_coverage:.2f}%")
        
        if sentiment_coverage >= 90:
            print("✓ KPI met: >=90% reviews have sentiment scores")
            return True
        else:
            print("✗ KPI not met: <90% reviews have sentiment scores")
            return False


class SentimentAnalysisPipeline:
    """Complete pipeline for sentiment analysis."""
    
    def __init__(self, input_file: str = '../Data/all_banks.csv',
                 output_file: str = '../Data/all_banks_with_sentiment.csv'):
        """
        Initialize the pipeline.
        
        Args:
            input_file: Path to input CSV
            output_file: Path to output CSV
        """
        self.input_file = input_file
        self.output_file = output_file
        self.analyzer = SentimentAnalyzer()
    
    def run(self) -> pd.DataFrame:
        """
        Run the complete sentiment analysis pipeline.
        
        Returns:
            DataFrame with sentiment analysis results
        """
        print("Starting sentiment analysis...")
        print("=" * 50)
        
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(f"Input file not found: {self.input_file}. Please run task1_preprocessing.py first")
        
        df = pd.read_csv(self.input_file)
        print(f"Loaded {len(df)} reviews from {self.input_file}")
        
        # Analyze sentiment
        df = self.analyzer.analyze_dataframe(df)
        
        # Aggregate statistics
        df = self.analyzer.aggregate_statistics(df)
        
        # Check KPI
        self.analyzer.check_kpi(df)
        
        # Save results
        df.to_csv(self.output_file, index=False)
        print(f"\nResults saved to: {self.output_file}")
        
        return df


def main():
    """Main function for backward compatibility."""
    pipeline = SentimentAnalysisPipeline()
    return pipeline.run()


if __name__ == "__main__":
    df = main()
