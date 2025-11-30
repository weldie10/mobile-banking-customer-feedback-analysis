"""
Task 1: Web Scraping Script
Scrapes reviews from Google Play Store for three Ethiopian banks:
- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

Target: 400+ reviews per bank (1,200 total)
"""

import pandas as pd
from google_play_scraper import app, reviews, Sort
import time
from datetime import datetime
import os

# Bank app package names (these need to be verified/updated with actual package names)
BANK_APPS = {
    'CBE': 'com.cbe.mobilebanking',  # Commercial Bank of Ethiopia
    'BOA': 'com.bankofabyssinia.mobilebanking',  # Bank of Abyssinia
    'Dashen': 'com.dashenbank.mobilebanking'  # Dashen Bank
}

# Alternative: Use app IDs if package names don't work
# You may need to search for the actual app IDs on Google Play Store

def scrape_reviews(app_id, bank_name, count=400, sort=Sort.NEWEST):
    """
    Scrape reviews for a specific bank app.
    
    Args:
        app_id: Google Play Store app ID or package name
        bank_name: Name of the bank
        count: Number of reviews to scrape (default: 400)
        sort: Sort order (NEWEST, RATING, MOST_RELEVANT)
    
    Returns:
        List of review dictionaries
    """
    print(f"Scraping reviews for {bank_name}...")
    
    try:
        # Scrape reviews
        result, continuation_token = reviews(
            app_id,
            lang='en',
            country='et',  # Ethiopia
            sort=sort,
            count=count
        )
        
        # If we need more reviews, continue scraping
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
                time.sleep(2)  # Be respectful with rate limiting
            except Exception as e:
                print(f"Error continuing scrape for {bank_name}: {e}")
                break
        
        print(f"Successfully scraped {len(reviews_list)} reviews for {bank_name}")
        return reviews_list[:count]  # Return up to count reviews
        
    except Exception as e:
        print(f"Error scraping {bank_name}: {e}")
        print(f"Trying alternative method...")
        # Try with app() first to get app info
        try:
            app_info = app(app_id, lang='en', country='et')
            print(f"App found: {app_info['title']}")
            # Retry reviews
            result, _ = reviews(
                app_id,
                lang='en',
                country='et',
                sort=sort,
                count=min(count, 200)  # Start with smaller batch
            )
            return result
        except Exception as e2:
            print(f"Failed to scrape {bank_name}: {e2}")
            return []


def format_reviews(reviews_list, bank_name):
    """
    Format scraped reviews into a standardized format.
    
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
            'date': review.get('at', datetime.now()).strftime('%Y-%m-%d') if review.get('at') else None,
            'bank': bank_name,
            'source': 'Google Play'
        })
    return formatted


def main():
    """Main function to scrape reviews for all banks."""
    print("Starting web scraping for bank reviews...")
    print("=" * 50)
    
    all_reviews = []
    
    # Scrape reviews for each bank
    for bank_name, app_id in BANK_APPS.items():
        reviews_list = scrape_reviews(app_id, bank_name, count=400)
        formatted_reviews = format_reviews(reviews_list, bank_name)
        all_reviews.extend(formatted_reviews)
        print(f"Total reviews collected so far: {len(all_reviews)}")
        time.sleep(3)  # Rate limiting between banks
    
    # Create DataFrame
    df = pd.DataFrame(all_reviews)
    
    # Save to CSV
    output_dir = '../Data'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'all_banks_raw.csv')
    df.to_csv(output_file, index=False)
    
    print("=" * 50)
    print(f"Scraping complete!")
    print(f"Total reviews collected: {len(df)}")
    print(f"Reviews per bank:")
    print(df['bank'].value_counts())
    print(f"\nData saved to: {output_file}")
    
    return df


if __name__ == "__main__":
    df = main()

