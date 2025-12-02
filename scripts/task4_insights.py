"""
Task 4: Insights and Recommendations Script (OOP Version)
Identifies drivers, pain points, compares banks, and generates recommendations.
"""

import pandas as pd
import numpy as np
from collections import Counter
import os
import re
from typing import Dict, List, Tuple, Any
from utils import TextProcessor


class DriverAnalyzer:
    """Identifies satisfaction drivers from positive reviews."""
    
    POSITIVE_KEYWORDS = {
        'fast': ['fast', 'quick', 'speed', 'instant', 'rapid', 'swift'],
        'easy': ['easy', 'simple', 'user friendly', 'convenient', 'straightforward'],
        'reliable': ['reliable', 'stable', 'works', 'good', 'excellent'],
        'secure': ['secure', 'safe', 'security', 'protected'],
        'features': ['feature', 'functionality', 'useful', 'helpful']
    }
    
    def __init__(self):
        """Initialize driver analyzer."""
        self.text_processor = TextProcessor()
    
    def identify_drivers(self, df: pd.DataFrame, bank_name: str, 
                        min_reviews: int = 10) -> List[Dict[str, Any]]:
        """
        Identify satisfaction drivers for a bank.
        
        Args:
            df: DataFrame with reviews
            bank_name: Name of the bank
            min_reviews: Minimum reviews mentioning a driver
        
        Returns:
            List of driver dictionaries
        """
        bank_df = df[df['bank'] == bank_name]
        # Focus on positive reviews (4-5 stars)
        positive_reviews = bank_df[bank_df['rating'] >= 4]
        
        drivers = []
        for driver_name, keywords in self.POSITIVE_KEYWORDS.items():
            count = 0
            examples = []
            
            for _, row in positive_reviews.iterrows():
                review_text = self.text_processor.clean_text(str(row['review']))
                if any(keyword in review_text for keyword in keywords):
                    count += 1
                    if len(examples) < 3:
                        examples.append(row['review'][:100] + '...')
            
            if count >= min_reviews:
                drivers.append({
                    'driver': driver_name.title(),
                    'count': count,
                    'percentage': (count / len(positive_reviews)) * 100,
                    'examples': examples
                })
        
        # Sort by count
        drivers.sort(key=lambda x: x['count'], reverse=True)
        return drivers


class PainPointAnalyzer:
    """Identifies pain points from negative reviews."""
    
    NEGATIVE_KEYWORDS = {
        'slow': ['slow', 'delay', 'timeout', 'wait', 'lag', 'loading'],
        'crash': ['crash', 'freeze', 'hang', 'stop', 'close', 'error'],
        'login': ['login', 'password', 'access', 'unable', 'cannot', 'failed'],
        'support': ['support', 'help', 'service', 'response', 'complaint'],
        'missing': ['missing', 'need', 'want', 'add', 'feature', 'lack']
    }
    
    def __init__(self):
        """Initialize pain point analyzer."""
        self.text_processor = TextProcessor()
    
    def identify_pain_points(self, df: pd.DataFrame, bank_name: str,
                            min_reviews: int = 10) -> List[Dict[str, Any]]:
        """
        Identify pain points for a bank.
        
        Args:
            df: DataFrame with reviews
            bank_name: Name of the bank
            min_reviews: Minimum reviews mentioning a pain point
        
        Returns:
            List of pain point dictionaries
        """
        bank_df = df[df['bank'] == bank_name]
        # Focus on negative reviews (1-2 stars)
        negative_reviews = bank_df[bank_df['rating'] <= 2]
        
        pain_points = []
        for pain_name, keywords in self.NEGATIVE_KEYWORDS.items():
            count = 0
            examples = []
            
            for _, row in negative_reviews.iterrows():
                review_text = self.text_processor.clean_text(str(row['review']))
                if any(keyword in review_text for keyword in keywords):
                    count += 1
                    if len(examples) < 3:
                        examples.append(row['review'][:100] + '...')
            
            if count >= min_reviews:
                pain_points.append({
                    'pain_point': pain_name.title(),
                    'count': count,
                    'percentage': (count / len(negative_reviews)) * 100 if len(negative_reviews) > 0 else 0,
                    'examples': examples
                })
        
        # Sort by count
        pain_points.sort(key=lambda x: x['count'], reverse=True)
        return pain_points


class BankComparator:
    """Compares banks across various metrics."""
    
    def __init__(self):
        """Initialize bank comparator."""
        pass
    
    def compare_ratings(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compare average ratings across banks.
        
        Args:
            df: DataFrame with reviews
        
        Returns:
            DataFrame with comparison metrics
        """
        comparison = df.groupby('bank').agg({
            'rating': ['mean', 'std', 'count'],
        }).round(2)
        
        comparison.columns = ['avg_rating', 'std_rating', 'review_count']
        comparison = comparison.sort_values('avg_rating', ascending=False)
        return comparison
    
    def compare_sentiment(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compare sentiment distribution across banks.
        
        Args:
            df: DataFrame with sentiment data
        
        Returns:
            DataFrame with sentiment comparison
        """
        if 'sentiment_label' not in df.columns:
            return pd.DataFrame()
        
        comparison = pd.crosstab(df['bank'], df['sentiment_label'], normalize='index') * 100
        return comparison.round(2)
    
    def compare_themes(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Compare theme frequency across banks.
        
        Args:
            df: DataFrame with theme data
        
        Returns:
            Dictionary of theme comparisons
        """
        if 'themes' not in df.columns and 'themes_str' not in df.columns:
            return {}
        
        theme_col = 'themes' if 'themes' in df.columns else 'themes_str'
        theme_comparisons = {}
        
        # Extract all unique themes
        all_themes = set()
        for themes in df[theme_col]:
            if pd.notna(themes) and themes != 'None':
                if isinstance(themes, str):
                    if ';' in themes:
                        all_themes.update([t.strip() for t in themes.split(';')])
                    else:
                        all_themes.add(themes)
                elif isinstance(themes, list):
                    all_themes.update(themes)
        
        # Count themes per bank
        for theme in all_themes:
            theme_counts = []
            for bank in df['bank'].unique():
                bank_df = df[df['bank'] == bank]
                count = 0
                for themes in bank_df[theme_col]:
                    if pd.notna(themes) and themes != 'None':
                        if isinstance(themes, str):
                            theme_list = [t.strip() for t in themes.split(';')] if ';' in themes else [themes]
                        else:
                            theme_list = themes
                        if theme in theme_list:
                            count += 1
                theme_counts.append({'Bank': bank, 'Count': count})
            
            theme_comparisons[theme] = pd.DataFrame(theme_counts)
        
        return theme_comparisons


class RecommendationGenerator:
    """Generates recommendations based on analysis."""
    
    def __init__(self):
        """Initialize recommendation generator."""
        pass
    
    def generate_recommendations(self, drivers: List[Dict], pain_points: List[Dict],
                                 bank_name: str) -> List[Dict[str, Any]]:
        """
        Generate recommendations for a bank.
        
        Args:
            drivers: List of identified drivers
            pain_points: List of identified pain points
            bank_name: Name of the bank
        
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        # Recommendations based on pain points
        for pain_point in pain_points[:3]:  # Top 3 pain points
            rec = self._generate_pain_point_recommendation(pain_point, bank_name)
            if rec:
                recommendations.append(rec)
        
        # Recommendations based on missing drivers
        if len(drivers) < 3:
            recommendations.append({
                'type': 'Enhancement',
                'priority': 'Medium',
                'title': 'Expand Positive Features',
                'description': f'Consider enhancing features that drive satisfaction. Currently identified {len(drivers)} key drivers.',
                'bank': bank_name
            })
        
        return recommendations
    
    def _generate_pain_point_recommendation(self, pain_point: Dict,
                                          bank_name: str) -> Dict[str, Any]:
        """Generate recommendation for a specific pain point."""
        pain_name = pain_point['pain_point'].lower()
        priority = 'High' if pain_point['count'] > 50 else 'Medium'
        
        recommendations_map = {
            'slow': {
                'title': 'Optimize App Performance',
                'description': 'Investigate and optimize slow loading times, transaction delays, and timeout issues. Consider server upgrades, caching strategies, and code optimization.'
            },
            'crash': {
                'title': 'Improve App Stability',
                'description': 'Address app crashes, freezes, and errors. Implement comprehensive error handling, testing, and monitoring systems.'
            },
            'login': {
                'title': 'Enhance Authentication System',
                'description': 'Improve login process, password recovery, and account access. Consider biometric authentication options.'
            },
            'support': {
                'title': 'Strengthen Customer Support',
                'description': 'Enhance customer support responsiveness and effectiveness. Consider AI chatbot integration and improved support channels.'
            },
            'missing': {
                'title': 'Address Feature Gaps',
                'description': 'Identify and implement frequently requested features based on user feedback.'
            }
        }
        
        if pain_name in recommendations_map:
            rec = recommendations_map[pain_name].copy()
            rec['type'] = 'Improvement'
            rec['priority'] = priority
            rec['bank'] = bank_name
            rec['affected_reviews'] = pain_point['count']
            return rec
        
        return None


class InsightsAnalyzer:
    """Main class for insights analysis."""
    
    def __init__(self):
        """Initialize insights analyzer."""
        self.driver_analyzer = DriverAnalyzer()
        self.pain_point_analyzer = PainPointAnalyzer()
        self.comparator = BankComparator()
        self.recommendation_generator = RecommendationGenerator()
    
    def analyze_bank(self, df: pd.DataFrame, bank_name: str) -> Dict[str, Any]:
        """
        Analyze a specific bank.
        
        Args:
            df: DataFrame with reviews
            bank_name: Name of the bank
        
        Returns:
            Dictionary with analysis results
        """
        drivers = self.driver_analyzer.identify_drivers(df, bank_name)
        pain_points = self.pain_point_analyzer.identify_pain_points(df, bank_name)
        recommendations = self.recommendation_generator.generate_recommendations(
            drivers, pain_points, bank_name
        )
        
        return {
            'bank': bank_name,
            'drivers': drivers,
            'pain_points': pain_points,
            'recommendations': recommendations
        }
    
    def analyze_all_banks(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        Analyze all banks.
        
        Args:
            df: DataFrame with reviews
        
        Returns:
            Dictionary of analysis results per bank
        """
        results = {}
        for bank in df['bank'].unique():
            results[bank] = self.analyze_bank(df, bank)
        return results
    
    def compare_banks(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Compare all banks.
        
        Args:
            df: DataFrame with reviews
        
        Returns:
            Dictionary with comparison results
        """
        return {
            'ratings': self.comparator.compare_ratings(df),
            'sentiment': self.comparator.compare_sentiment(df),
            'themes': self.comparator.compare_themes(df)
        }


class InsightsReportGenerator:
    """Generates insights report."""
    
    def __init__(self, output_dir: str = '../Data'):
        """
        Initialize report generator.
        
        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_text_report(self, analysis_results: Dict[str, Dict[str, Any]],
                            comparison_results: Dict[str, Any]) -> str:
        """
        Generate text report of insights.
        
        Args:
            analysis_results: Results from analyze_all_banks
            comparison_results: Results from compare_banks
        
        Returns:
            Report text
        """
        report = []
        report.append("=" * 70)
        report.append("INSIGHTS AND RECOMMENDATIONS REPORT")
        report.append("=" * 70)
        report.append("")
        
        # Bank-specific insights
        for bank, results in analysis_results.items():
            report.append(f"\n{'='*70}")
            report.append(f"BANK: {bank}")
            report.append(f"{'='*70}")
            
            # Drivers
            report.append("\nSATISFACTION DRIVERS:")
            if results['drivers']:
                for i, driver in enumerate(results['drivers'][:3], 1):
                    report.append(f"  {i}. {driver['driver']}")
                    report.append(f"     - Mentioned in {driver['count']} positive reviews ({driver['percentage']:.1f}%)")
            else:
                report.append("  No significant drivers identified.")
            
            # Pain points
            report.append("\nPAIN POINTS:")
            if results['pain_points']:
                for i, pain in enumerate(results['pain_points'][:3], 1):
                    report.append(f"  {i}. {pain['pain_point']}")
                    report.append(f"     - Mentioned in {pain['count']} negative reviews ({pain['percentage']:.1f}%)")
            else:
                report.append("  No significant pain points identified.")
            
            # Recommendations
            report.append("\nRECOMMENDATIONS:")
            for i, rec in enumerate(results['recommendations'][:3], 1):
                report.append(f"  {i}. [{rec['priority']} Priority] {rec['title']}")
                report.append(f"     {rec['description']}")
        
        # Bank comparison
        report.append(f"\n{'='*70}")
        report.append("BANK COMPARISON")
        report.append(f"{'='*70}")
        
        if 'ratings' in comparison_results:
            report.append("\nAverage Ratings:")
            for bank, row in comparison_results['ratings'].iterrows():
                report.append(f"  {bank}: {row['avg_rating']:.2f} (from {int(row['review_count'])} reviews)")
        
        report.append("\n" + "=" * 70)
        
        return "\n".join(report)
    
    def save_report(self, report_text: str, filename: str = 'insights_report.txt'):
        """
        Save report to file.
        
        Args:
            report_text: Report text
            filename: Output filename
        """
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"✓ Insights report saved to: {filepath}")


class InsightsPipeline:
    """Complete pipeline for insights analysis."""
    
    def __init__(self, input_file: str = '../Data/all_banks.csv',
                 output_dir: str = '../Data'):
        """
        Initialize insights pipeline.
        
        Args:
            input_file: Path to input CSV
            output_dir: Directory for output files
        """
        self.input_file = input_file
        self.output_dir = output_dir
        self.analyzer = InsightsAnalyzer()
        self.report_generator = InsightsReportGenerator(output_dir)
    
    def run(self) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Any]]:
        """
        Run the complete insights analysis pipeline.
        
        Returns:
            Tuple of (analysis_results, comparison_results)
        """
        print("Starting insights analysis...")
        print("=" * 50)
        
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(f"Input file not found: {self.input_file}")
        
        df = pd.read_csv(self.input_file)
        print(f"✓ Loaded {len(df)} reviews from {self.input_file}")
        
        # Analyze all banks
        print("\nAnalyzing banks...")
        analysis_results = self.analyzer.analyze_all_banks(df)
        
        # Compare banks
        print("Comparing banks...")
        comparison_results = self.analyzer.compare_banks(df)
        
        # Generate report
        print("Generating report...")
        report_text = self.report_generator.generate_text_report(analysis_results, comparison_results)
        self.report_generator.save_report(report_text)
        
        # Print summary
        print("\n" + "=" * 50)
        print("INSIGHTS SUMMARY")
        print("=" * 50)
        for bank, results in analysis_results.items():
            print(f"\n{bank}:")
            print(f"  Drivers identified: {len(results['drivers'])}")
            print(f"  Pain points identified: {len(results['pain_points'])}")
            print(f"  Recommendations: {len(results['recommendations'])}")
        
        print("\n✓ Insights analysis complete!")
        print("=" * 50)
        
        return analysis_results, comparison_results


def main():
    """Main function for backward compatibility."""
    pipeline = InsightsPipeline()
    return pipeline.run()


if __name__ == "__main__":
    pipeline = InsightsPipeline()
    pipeline.run()

