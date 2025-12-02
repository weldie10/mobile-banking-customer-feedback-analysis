"""
Task 2: Thematic Analysis Script (OOP Version)
Extracts keywords and clusters them into themes for each bank.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import os
from collections import Counter
import warnings
from typing import List, Dict, Tuple, Any

warnings.filterwarnings('ignore')

# Try to import spacy
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    USE_SPACY = True
except:
    USE_SPACY = False


class TextPreprocessor:
    """Handles text preprocessing for thematic analysis."""
    
    @staticmethod
    def preprocess(text: str) -> str:
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
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        text = ' '.join(text.split())
        return text


class KeywordExtractor:
    """Extracts keywords using TF-IDF."""
    
    def __init__(self, max_features: int = 50, ngram_range: Tuple[int, int] = (1, 2)):
        """
        Initialize the keyword extractor.
        
        Args:
            max_features: Maximum number of features to extract
            ngram_range: Range of n-grams to consider
        """
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.preprocessor = TextPreprocessor()
    
    def extract(self, reviews: List[str]) -> List[Tuple[str, float]]:
        """
        Extract keywords using TF-IDF.
        
        Args:
            reviews: List of review texts
        
        Returns:
            List of (keyword, score) tuples
        """
        processed_reviews = [self.preprocessor.preprocess(review) for review in reviews]
        
        vectorizer = TfidfVectorizer(
            max_features=self.max_features,
            ngram_range=self.ngram_range,
            stop_words='english',
            min_df=2,
            max_df=0.95
        )
        
        try:
            tfidf_matrix = vectorizer.fit_transform(processed_reviews)
            feature_names = vectorizer.get_feature_names_out()
            mean_scores = np.array(tfidf_matrix.mean(axis=0)).flatten()
            
            keywords = list(zip(feature_names, mean_scores))
            keywords.sort(key=lambda x: x[1], reverse=True)
            return keywords
        except Exception as e:
            print(f"Error in TF-IDF extraction: {e}")
            return []


class ThemeClusterer:
    """Clusters keywords into themes."""
    
    THEME_PATTERNS = {
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
    
    def cluster(self, keywords: List[Tuple[str, float]], bank_name: str) -> Dict[str, List[Tuple[str, float]]]:
        """
        Cluster keywords into themes.
        
        Args:
            keywords: List of (keyword, score) tuples
            bank_name: Name of the bank
        
        Returns:
            Dictionary mapping themes to keywords
        """
        theme_keywords = {theme: [] for theme in self.THEME_PATTERNS.keys()}
        unassigned = []
        
        for keyword, score in keywords:
            keyword_lower = keyword.lower()
            assigned = False
            
            for theme, patterns in self.THEME_PATTERNS.items():
                for pattern in patterns:
                    if pattern in keyword_lower or keyword_lower in pattern:
                        theme_keywords[theme].append((keyword, score))
                        assigned = True
                        break
                if assigned:
                    break
            
            if not assigned:
                unassigned.append((keyword, score))
        
        theme_keywords = {k: v for k, v in theme_keywords.items() if v}
        
        if unassigned:
            theme_keywords['General'] = unassigned[:10]
        
        return theme_keywords
    
    def identify_themes_in_review(self, review_text: str, 
                                  theme_keywords: Dict[str, List[Tuple[str, float]]]) -> List[str]:
        """
        Identify which themes are present in a review.
        
        Args:
            review_text: Review text
            theme_keywords: Dictionary of themes and their keywords
        
        Returns:
            List of theme names
        """
        review_lower = TextPreprocessor.preprocess(review_text)
        identified_themes = []
        
        for theme, keywords in theme_keywords.items():
            for keyword, _ in keywords:
                if keyword in review_lower:
                    identified_themes.append(theme)
                    break
        
        return identified_themes


class ThematicAnalyzer:
    """Main class for thematic analysis."""
    
    def __init__(self):
        """Initialize the thematic analyzer."""
        self.keyword_extractor = KeywordExtractor()
        self.theme_clusterer = ThemeClusterer()
        self.preprocessor = TextPreprocessor()
    
    def analyze_bank(self, bank_df: pd.DataFrame, bank_name: str) -> pd.DataFrame:
        """
        Analyze themes for a specific bank.
        
        Args:
            bank_df: DataFrame with reviews for one bank
            bank_name: Name of the bank
        
        Returns:
            DataFrame with themes added
        """
        print(f"\nAnalyzing themes for {bank_name}...")
        bank_reviews = bank_df['review'].tolist()
        
        # Extract keywords
        print(f"  Extracting keywords from {len(bank_reviews)} reviews...")
        keywords = self.keyword_extractor.extract(bank_reviews)
        
        print(f"  Found {len(keywords)} keywords")
        print(f"  Top 10 keywords: {[k[0] for k in keywords[:10]]}")
        
        # Cluster into themes
        print(f"  Clustering keywords into themes...")
        theme_keywords = self.theme_clusterer.cluster(keywords, bank_name)
        
        print(f"  Identified {len(theme_keywords)} themes:")
        for theme, kw_list in theme_keywords.items():
            print(f"    - {theme}: {len(kw_list)} keywords")
            print(f"      Top keywords: {[k[0] for k in kw_list[:5]]}")
        
        # Identify themes for each review
        print(f"  Identifying themes in reviews...")
        bank_df = bank_df.copy()
        bank_df['themes'] = bank_df['review'].apply(
            lambda x: self.theme_clusterer.identify_themes_in_review(x, theme_keywords)
        )
        bank_df['themes_str'] = bank_df['themes'].apply(
            lambda x: '; '.join(x) if x else 'None'
        )
        
        return bank_df
    
    def analyze_all_banks(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze themes for all banks.
        
        Args:
            df: DataFrame with reviews
        
        Returns:
            DataFrame with themes added
        """
        all_results = []
        
        for bank in df['bank'].unique():
            bank_df = df[df['bank'] == bank]
            bank_result = self.analyze_bank(bank_df, bank)
            all_results.append(bank_result)
        
        return pd.concat(all_results, ignore_index=True)
    
    def generate_summary(self, df: pd.DataFrame):
        """Generate thematic analysis summary."""
        print("\n" + "=" * 50)
        print("Thematic Analysis Summary")
        print("=" * 50)
        
        for bank in df['bank'].unique():
            bank_df = df[df['bank'] == bank]
            all_themes = []
            
            for themes_list in bank_df['themes']:
                all_themes.extend(themes_list)
            
            unique_themes = set(all_themes)
            theme_counts = Counter(all_themes)
            
            print(f"\n{bank}:")
            print(f"  Unique themes identified: {len(unique_themes)}")
            print(f"  Themes: {', '.join(sorted(unique_themes))}")
            print(f"  Top themes:")
            for theme, count in theme_counts.most_common(5):
                print(f"    - {theme}: {count} reviews")
            
            if len(unique_themes) >= 3:
                print(f"  ✓ KPI met: >=3 themes identified")
            else:
                print(f"  ✗ KPI not met: <3 themes identified")
        
        print("=" * 50 + "\n")


class ThematicAnalysisPipeline:
    """Complete pipeline for thematic analysis."""
    
    def __init__(self, input_file: str = '../Data/all_banks_with_sentiment.csv',
                 output_file: str = '../Data/all_banks_with_sentiment_themes.csv'):
        """
        Initialize the pipeline.
        
        Args:
            input_file: Path to input CSV
            output_file: Path to output CSV
        """
        self.input_file = input_file
        self.output_file = output_file
        self.analyzer = ThematicAnalyzer()
    
    def run(self) -> pd.DataFrame:
        """
        Run the complete thematic analysis pipeline.
        
        Returns:
            DataFrame with thematic analysis results
        """
        print("Starting thematic analysis...")
        print("=" * 50)
        
        # Try to find input file
        if not os.path.exists(self.input_file):
            self.input_file = '../Data/all_banks.csv'
            print(f"Sentiment file not found, using: {self.input_file}")
        
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(f"Input file not found: {self.input_file}. Please run task1_preprocessing.py first")
        
        df = pd.read_csv(self.input_file)
        print(f"Loaded {len(df)} reviews from {self.input_file}")
        
        # Analyze themes
        df = self.analyzer.analyze_all_banks(df)
        
        # Generate summary
        self.analyzer.generate_summary(df)
        
        # Save results
        df.to_csv(self.output_file, index=False)
        print(f"Results saved to: {self.output_file}")
        
        return df


def main():
    """Main function for backward compatibility."""
    pipeline = ThematicAnalysisPipeline()
    return pipeline.run()


if __name__ == "__main__":
    df = main()
