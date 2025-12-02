"""
Task 1: Web Scraping Script (OOP Version)
Scrapes reviews from Google Play Store for three Ethiopian banks.
"""

import pandas as pd
from google_play_scraper import app, reviews, Sort
import time
from datetime import datetime
import os
from typing import List, Dict, Any


class PlayStoreScraper:
    """Handles scraping of reviews from Google Play Store."""
    
    # Bank app package names
    BANK_APPS = {
        'CBE': 'com.cbe.mobilebanking',
        'BOA': 'com.bankofabyssinia.mobilebanking',
        'Dashen': 'com.dashenbank.mobilebanking'
    }
    
    def __init__(self, output_dir: str = '../Data'):
        """
        Initialize the scraper.
        
        Args:
            output_dir: Directory to save output files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def scrape_reviews(self, app_id: str, bank_name: str, count: int = 400, 
                      sort: Sort = Sort.NEWEST) -> List[Dict[str, Any]]:
        """
        Scrape reviews for a specific bank app.
        
        Args:
            app_id: Google Play Store app ID or package name
            bank_name: Name of the bank
            count: Number of reviews to scrape
            sort: Sort order
        
        Returns:
            List of review dictionaries
        """
        print(f"Scraping reviews for {bank_name}...")
        
        try:
            # Scrape reviews
            result, continuation_token = reviews(
                app_id,
                lang='en',
                country='et',
                sort=sort,
                count=count
            )
            
            # Continue scraping if needed
            reviews_list = result
            while len(reviews_list) < count and continuation_token:
                try:
                    result, continuation_token = reviews(
                        app_id,
                        continuation_token=continuation_token,
                        lang='en',
                        country='et'
                    )
                    reviews_list.extend(result)
                    time.sleep(2)  # Rate limiting
                except Exception as e:
                    print(f"Error continuing scrape for {bank_name}: {e}")
                    break
            
            print(f"Successfully scraped {len(reviews_list)} reviews for {bank_name}")
            return reviews_list[:count]
            
        except Exception as e:
            print(f"Error scraping {bank_name}: {e}")
            print(f"Trying alternative method...")
            return self._try_alternative_scrape(app_id, bank_name, count, sort)
    
    def _try_alternative_scrape(self, app_id: str, bank_name: str, 
                               count: int, sort: Sort) -> List[Dict[str, Any]]:
        """Try alternative scraping method."""
        try:
            app_info = app(app_id, lang='en', country='et')
            print(f"App found: {app_info['title']}")
            result, _ = reviews(
                app_id,
                lang='en',
                country='et',
                sort=sort,
                count=min(count, 200)
            )
            return result
        except Exception as e2:
            print(f"Failed to scrape {bank_name}: {e2}")
            return []
    
    def format_reviews(self, reviews_list: List[Dict[str, Any]], 
                      bank_name: str) -> List[Dict[str, Any]]:
        """
        Format scraped reviews into standardized format.
        
        Args:
            reviews_list: List of review dictionaries from scraper
            bank_name: Name of the bank
        
        Returns:
            List of formatted review dictionaries
        """
        formatted = []
        for review in reviews_list:
            formatted.append({
                'review': review.get('content', ''),
                'rating': review.get('score', 0),
                'date': review.get('at', datetime.now()).strftime('%Y-%m-%d') 
                       if review.get('at') else None,
                'bank': bank_name,
                'source': 'Google Play'
            })
        return formatted
    
    def scrape_all_banks(self, count_per_bank: int = 400) -> pd.DataFrame:
        """
        Scrape reviews for all banks.
        
        Args:
            count_per_bank: Number of reviews to scrape per bank
        
        Returns:
            DataFrame with all reviews
        """
        print("Starting web scraping for bank reviews...")
        print("=" * 50)
        
        all_reviews = []
        
        for bank_name, app_id in self.BANK_APPS.items():
            reviews_list = self.scrape_reviews(app_id, bank_name, count=count_per_bank)
            formatted_reviews = self.format_reviews(reviews_list, bank_name)
            all_reviews.extend(formatted_reviews)
            print(f"Total reviews collected so far: {len(all_reviews)}")
            time.sleep(3)  # Rate limiting between banks
        
        df = pd.DataFrame(all_reviews)
        return df
    
    def save_results(self, df: pd.DataFrame, filename: str = 'all_banks_raw.csv'):
        """
        Save scraped data to CSV.
        
        Args:
            df: DataFrame to save
            filename: Output filename
        """
        output_file = os.path.join(self.output_dir, filename)
        df.to_csv(output_file, index=False)
        
        print("=" * 50)
        print(f"Scraping complete!")
        print(f"Total reviews collected: {len(df)}")
        print(f"Reviews per bank:")
        print(df['bank'].value_counts())
        print(f"\nData saved to: {output_file}")
    
    def run(self, count_per_bank: int = 400) -> pd.DataFrame:
        """
        Run the complete scraping process.
        
        Args:
            count_per_bank: Number of reviews to scrape per bank
        
        Returns:
            DataFrame with all reviews
        """
        df = self.scrape_all_banks(count_per_bank)
        self.save_results(df)
        return df


def main():
    """Main function for backward compatibility."""
    scraper = PlayStoreScraper()
    return scraper.run()


if __name__ == "__main__":
    df = main()
