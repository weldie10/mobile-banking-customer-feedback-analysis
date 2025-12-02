"""
Task 4: Visualization Script (OOP Version)
Creates visualizations and generates insights from review data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import os
import warnings
from typing import Optional, List
from datetime import datetime

warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


class DataLoader:
    """Handles loading of review data."""
    
    def __init__(self):
        """Initialize data loader."""
        self.files_to_try = [
            '../Data/all_banks_with_sentiment_themes.csv',
            '../Data/all_banks_with_sentiment.csv',
            '../Data/all_banks.csv'
        ]
    
    def load(self) -> pd.DataFrame:
        """
        Load review data, with sentiment and themes if available.
        
        Returns:
            DataFrame with review data
        """
        for file_path in self.files_to_try:
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                print(f"✓ Loaded {len(df)} reviews from {file_path}")
                return df
        
        raise FileNotFoundError("No data file found. Please run preprocessing first.")


class PlotGenerator:
    """Base class for plot generation."""
    
    def __init__(self, output_dir: str = '../Data/visualizations'):
        """
        Initialize plot generator.
        
        Args:
            output_dir: Directory to save plots
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def save_plot(self, filename: str, fig):
        """
        Save plot to file.
        
        Args:
            filename: Output filename
            fig: Matplotlib figure
        """
        filepath = os.path.join(self.output_dir, filename)
        fig.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {filepath}")
        plt.close(fig)


class SentimentPlotter(PlotGenerator):
    """Generates sentiment distribution plots."""
    
    def plot(self, df: pd.DataFrame):
        """
        Plot sentiment distribution by bank.
        
        Args:
            df: DataFrame with sentiment data
        """
        if 'sentiment_label' not in df.columns:
            print("⚠ No sentiment data available. Skipping sentiment distribution plot.")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Overall sentiment distribution
        sentiment_counts = df['sentiment_label'].value_counts()
        axes[0].bar(sentiment_counts.index, sentiment_counts.values, 
                    color=['#2ecc71', '#e74c3c', '#95a5a6'])
        axes[0].set_title('Overall Sentiment Distribution', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Sentiment')
        axes[0].set_ylabel('Number of Reviews')
        axes[0].grid(axis='y', alpha=0.3)
        
        # Sentiment by bank
        if 'bank' in df.columns:
            sentiment_by_bank = pd.crosstab(df['bank'], df['sentiment_label'])
            sentiment_by_bank.plot(kind='bar', ax=axes[1], 
                                  color=['#2ecc71', '#e74c3c', '#95a5a6'])
            axes[1].set_title('Sentiment Distribution by Bank', fontsize=14, fontweight='bold')
            axes[1].set_xlabel('Bank')
            axes[1].set_ylabel('Number of Reviews')
            axes[1].legend(title='Sentiment')
            axes[1].tick_params(axis='x', rotation=45)
            axes[1].grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        self.save_plot('sentiment_distribution.png', fig)


class RatingPlotter(PlotGenerator):
    """Generates rating distribution plots."""
    
    def plot(self, df: pd.DataFrame):
        """
        Plot rating distribution by bank.
        
        Args:
            df: DataFrame with rating data
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Overall rating distribution
        rating_counts = df['rating'].value_counts().sort_index()
        colors = ['#e74c3c', '#e67e22', '#f39c12', '#3498db', '#2ecc71']
        axes[0].bar(rating_counts.index.astype(str), rating_counts.values, color=colors)
        axes[0].set_title('Overall Rating Distribution', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Rating (Stars)')
        axes[0].set_ylabel('Number of Reviews')
        axes[0].grid(axis='y', alpha=0.3)
        
        # Rating by bank
        if 'bank' in df.columns:
            rating_by_bank = pd.crosstab(df['bank'], df['rating'])
            rating_by_bank.plot(kind='bar', ax=axes[1], color=colors)
            axes[1].set_title('Rating Distribution by Bank', fontsize=14, fontweight='bold')
            axes[1].set_xlabel('Bank')
            axes[1].set_ylabel('Number of Reviews')
            axes[1].legend(title='Rating', labels=['1★', '2★', '3★', '4★', '5★'])
            axes[1].tick_params(axis='x', rotation=45)
            axes[1].grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        self.save_plot('rating_distribution.png', fig)


class BankComparisonPlotter(PlotGenerator):
    """Generates bank comparison plots."""
    
    def plot(self, df: pd.DataFrame):
        """
        Create comprehensive bank comparison chart.
        
        Args:
            df: DataFrame with review data
        """
        if 'bank' not in df.columns:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Average rating by bank
        avg_ratings = df.groupby('bank')['rating'].mean().sort_values(ascending=False)
        axes[0, 0].bar(avg_ratings.index, avg_ratings.values, 
                       color=['#3498db', '#2ecc71', '#e74c3c'])
        axes[0, 0].set_title('Average Rating by Bank', fontsize=12, fontweight='bold')
        axes[0, 0].set_ylabel('Average Rating')
        axes[0, 0].set_ylim(0, 5)
        axes[0, 0].grid(axis='y', alpha=0.3)
        
        # Review count by bank
        review_counts = df['bank'].value_counts()
        axes[0, 1].bar(review_counts.index, review_counts.values,
                       color=['#3498db', '#2ecc71', '#e74c3c'])
        axes[0, 1].set_title('Total Reviews by Bank', fontsize=12, fontweight='bold')
        axes[0, 1].set_ylabel('Number of Reviews')
        axes[0, 1].grid(axis='y', alpha=0.3)
        
        # Sentiment by bank (if available)
        if 'sentiment_label' in df.columns:
            sentiment_by_bank = pd.crosstab(df['bank'], df['sentiment_label'], normalize='index') * 100
            sentiment_by_bank.plot(kind='bar', ax=axes[1, 0], stacked=True,
                                  color=['#2ecc71', '#e74c3c', '#95a5a6'])
            axes[1, 0].set_title('Sentiment Percentage by Bank', fontsize=12, fontweight='bold')
            axes[1, 0].set_ylabel('Percentage (%)')
            axes[1, 0].legend(title='Sentiment')
            axes[1, 0].tick_params(axis='x', rotation=45)
            axes[1, 0].grid(axis='y', alpha=0.3)
        
        # Rating distribution comparison
        rating_pct = df.groupby('bank')['rating'].apply(lambda x: (x >= 4).sum() / len(x) * 100)
        axes[1, 1].bar(rating_pct.index, rating_pct.values,
                       color=['#3498db', '#2ecc71', '#e74c3c'])
        axes[1, 1].set_title('Percentage of 4+ Star Reviews by Bank', fontsize=12, fontweight='bold')
        axes[1, 1].set_ylabel('Percentage (%)')
        axes[1, 1].grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        self.save_plot('bank_comparison.png', fig)


class ThemeFrequencyPlotter(PlotGenerator):
    """Generates theme frequency plots."""
    
    def plot(self, df: pd.DataFrame):
        """
        Plot theme frequency by bank.
        
        Args:
            df: DataFrame with theme data
        """
        if 'themes' not in df.columns and 'themes_str' not in df.columns:
            print("⚠ No theme data available. Skipping theme frequency plot.")
            return
        
        theme_col = 'themes' if 'themes' in df.columns else 'themes_str'
        df[theme_col] = df[theme_col].fillna('None')
        
        theme_data = []
        for bank in df['bank'].unique():
            bank_df = df[df['bank'] == bank]
            all_themes = []
            
            for themes in bank_df[theme_col]:
                if pd.notna(themes) and themes != 'None':
                    if isinstance(themes, str):
                        if ';' in themes:
                            all_themes.extend([t.strip() for t in themes.split(';')])
                        else:
                            all_themes.append(themes)
                    elif isinstance(themes, list):
                        all_themes.extend(themes)
            
            theme_counts = Counter(all_themes)
            for theme, count in theme_counts.most_common(10):
                theme_data.append({'Bank': bank, 'Theme': theme, 'Count': count})
        
        if not theme_data:
            print("⚠ No theme data to plot.")
            return
        
        theme_df = pd.DataFrame(theme_data)
        pivot = theme_df.pivot_table(index='Theme', columns='Bank', values='Count', fill_value=0)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        pivot.plot(kind='barh', ax=ax, color=['#3498db', '#2ecc71', '#e74c3c'])
        ax.set_title('Theme Frequency by Bank', fontsize=14, fontweight='bold')
        ax.set_xlabel('Number of Reviews')
        ax.set_ylabel('Theme')
        ax.legend(title='Bank')
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        self.save_plot('theme_frequency.png', fig)


class TimeTrendPlotter(PlotGenerator):
    """Generates time trend plots."""
    
    def plot(self, df: pd.DataFrame):
        """
        Plot rating trends over time.
        
        Args:
            df: DataFrame with date data
        """
        if 'date' not in df.columns:
            print("⚠ No date data available. Skipping time trends plot.")
            return
        
        df['date_parsed'] = pd.to_datetime(df['date'], errors='coerce')
        df = df[df['date_parsed'].notna()]
        
        if len(df) == 0:
            print("⚠ No valid dates found. Skipping time trends plot.")
            return
        
        df['year_month'] = df['date_parsed'].dt.to_period('M')
        
        fig, axes = plt.subplots(2, 1, figsize=(14, 10))
        
        # Average rating over time
        monthly_ratings = df.groupby(['year_month', 'bank'])['rating'].mean().unstack()
        monthly_ratings.plot(ax=axes[0], marker='o', linewidth=2)
        axes[0].set_title('Average Rating Trend Over Time by Bank', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Month')
        axes[0].set_ylabel('Average Rating')
        axes[0].legend(title='Bank')
        axes[0].grid(alpha=0.3)
        axes[0].tick_params(axis='x', rotation=45)
        
        # Review count over time
        monthly_counts = df.groupby(['year_month', 'bank']).size().unstack(fill_value=0)
        monthly_counts.plot(ax=axes[1], kind='bar', width=0.8)
        axes[1].set_title('Review Count Trend Over Time by Bank', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Month')
        axes[1].set_ylabel('Number of Reviews')
        axes[1].legend(title='Bank')
        axes[1].tick_params(axis='x', rotation=45)
        axes[1].grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        self.save_plot('time_trends.png', fig)


class VisualizationPipeline:
    """Main pipeline for generating all visualizations."""
    
    def __init__(self, output_dir: str = '../Data/visualizations'):
        """
        Initialize visualization pipeline.
        
        Args:
            output_dir: Directory to save visualizations
        """
        self.data_loader = DataLoader()
        self.plotters = [
            RatingPlotter(output_dir),
            SentimentPlotter(output_dir),
            BankComparisonPlotter(output_dir),
            ThemeFrequencyPlotter(output_dir),
            TimeTrendPlotter(output_dir)
        ]
    
    def run(self) -> pd.DataFrame:
        """
        Run the complete visualization pipeline.
        
        Returns:
            DataFrame with loaded data
        """
        print("Starting visualization generation...")
        print("=" * 50)
        
        # Load data
        df = self.data_loader.load()
        
        # Generate visualizations
        print("\nGenerating visualizations...")
        for plotter in self.plotters:
            try:
                plotter.plot(df)
            except Exception as e:
                print(f"⚠ Error generating {plotter.__class__.__name__}: {e}")
        
        print("\n" + "=" * 50)
        print("✓ All visualizations generated successfully!")
        print(f"Visualizations saved in: {self.plotters[0].output_dir}")
        print("=" * 50)
        
        return df


def main():
    """Main function for backward compatibility."""
    pipeline = VisualizationPipeline()
    return pipeline.run()


if __name__ == "__main__":
    df = main()
