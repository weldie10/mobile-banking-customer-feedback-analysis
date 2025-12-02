"""
Task 3: Database Integration Script
Stores cleaned and processed review data in PostgreSQL database.

This script:
- Connects to PostgreSQL database
- Inserts bank information into banks table
- Inserts review data into reviews table
- Performs data integrity verification queries
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from psycopg2 import sql
import os
from dotenv import load_dotenv
from datetime import datetime
import sys

# Load environment variables
load_dotenv()

# Database configuration from environment variables
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'bank_reviews'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'kacha@gbe')
}

# Bank information mapping
BANK_INFO = {
    'CBE': {
        'bank_name': 'CBE',
        'app_name': 'Commercial Bank of Ethiopia',
        'description': 'Commercial Bank of Ethiopia mobile banking application'
    },
    'BOA': {
        'bank_name': 'BOA',
        'app_name': 'Bank of Abyssinia',
        'description': 'Bank of Abyssinia mobile banking application'
    },
    'Dashen': {
        'bank_name': 'Dashen',
        'app_name': 'Dashen Bank',
        'description': 'Dashen Bank mobile banking application'
    }
}


def get_db_connection():
    """
    Create and return a database connection.
    
    Returns:
        psycopg2 connection object
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print(f"✓ Successfully connected to database: {DB_CONFIG['database']}")
        return conn
    except psycopg2.Error as e:
        print(f"✗ Error connecting to database: {e}")
        sys.exit(1)


def create_tables(conn):
    """
    Create database tables if they don't exist.
    
    Args:
        conn: Database connection
    """
    cursor = conn.cursor()
    
    try:
        # Read and execute schema file
        schema_file = os.path.join(os.path.dirname(__file__), '..', 'schema.sql')
        if os.path.exists(schema_file):
            with open(schema_file, 'r') as f:
                schema_sql = f.read()
            cursor.execute(schema_sql)
            conn.commit()
            print("✓ Database tables created/verified")
        else:
            print(f"⚠ Schema file not found: {schema_file}")
            print("Creating tables manually...")
            
            # Create banks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS banks (
                    bank_id SERIAL PRIMARY KEY,
                    bank_name VARCHAR(255) NOT NULL,
                    app_name VARCHAR(255),
                    description TEXT,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            
            # Create reviews table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    review_id SERIAL PRIMARY KEY,
                    bank_id INTEGER NOT NULL,
                    review_text TEXT NOT NULL,
                    rating NUMERIC(2,1),
                    review_date DATE,
                    sentiment_label VARCHAR(50),
                    sentiment_score NUMERIC(3,2),
                    source VARCHAR(255),
                    created_at TIMESTAMP DEFAULT NOW(),
                    CONSTRAINT reviews_bank_id_fkey FOREIGN KEY (bank_id) 
                        REFERENCES banks(bank_id) ON DELETE CASCADE
                )
            """)
            
            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_reviews_bank_id ON reviews(bank_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_reviews_sentiment_label ON reviews(sentiment_label)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_reviews_review_date ON reviews(review_date)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_banks_bank_name ON banks(bank_name)")
            
            conn.commit()
            print("✓ Database tables created")
            
    except psycopg2.Error as e:
        conn.rollback()
        print(f"✗ Error creating tables: {e}")
        raise
    finally:
        cursor.close()


def insert_banks(conn):
    """
    Insert bank information into banks table.
    
    Args:
        conn: Database connection
    
    Returns:
        Dictionary mapping bank names to bank_ids
    """
    cursor = conn.cursor()
    bank_id_map = {}
    
    try:
        for bank_code, bank_data in BANK_INFO.items():
            # Check if bank already exists
            cursor.execute(
                "SELECT bank_id FROM banks WHERE bank_name = %s",
                (bank_data['bank_name'],)
            )
            result = cursor.fetchone()
            
            if result:
                bank_id_map[bank_code] = result[0]
                print(f"✓ Bank '{bank_data['bank_name']}' already exists (ID: {result[0]})")
            else:
                # Insert new bank
                cursor.execute("""
                    INSERT INTO banks (bank_name, app_name, description)
                    VALUES (%s, %s, %s)
                    RETURNING bank_id
                """, (bank_data['bank_name'], bank_data['app_name'], bank_data['description']))
                
                bank_id = cursor.fetchone()[0]
                bank_id_map[bank_code] = bank_id
                print(f"✓ Inserted bank '{bank_data['bank_name']}' (ID: {bank_id})")
        
        conn.commit()
        return bank_id_map
        
    except psycopg2.Error as e:
        conn.rollback()
        print(f"✗ Error inserting banks: {e}")
        raise
    finally:
        cursor.close()


def load_review_data(csv_file):
    """
    Load review data from CSV file.
    
    Args:
        csv_file: Path to CSV file
    
    Returns:
        DataFrame with review data
    """
    try:
        df = pd.read_csv(csv_file)
        print(f"✓ Loaded {len(df)} reviews from {csv_file}")
        return df
    except Exception as e:
        print(f"✗ Error loading CSV file: {e}")
        sys.exit(1)


def check_sentiment_data(df):
    """
    Check if sentiment data exists in the DataFrame.
    If not, try to load from sentiment file.
    
    Args:
        df: DataFrame with review data
    
    Returns:
        DataFrame with sentiment data if available
    """
    if 'sentiment_label' in df.columns and 'sentiment_score' in df.columns:
        print("✓ Sentiment data found in CSV")
        return df
    
    # Try to load from sentiment file
    sentiment_file = os.path.join(
        os.path.dirname(__file__), '..', 'Data', 'all_banks_with_sentiment.csv'
    )
    
    if os.path.exists(sentiment_file):
        print(f"✓ Loading sentiment data from {sentiment_file}")
        sentiment_df = pd.read_csv(sentiment_file)
        
        # Merge sentiment data
        if 'sentiment_label' in sentiment_df.columns:
            df = pd.merge(
                df,
                sentiment_df[['review', 'bank', 'sentiment_label', 'sentiment_score']],
                on=['review', 'bank'],
                how='left',
                suffixes=('', '_sentiment')
            )
            
            # Use sentiment columns from merged data
            if 'sentiment_label_sentiment' in df.columns:
                df['sentiment_label'] = df['sentiment_label_sentiment']
                df['sentiment_score'] = df['sentiment_score_sentiment']
                df = df.drop(['sentiment_label_sentiment', 'sentiment_score_sentiment'], axis=1)
        
        print("✓ Sentiment data merged")
    else:
        print("⚠ No sentiment data found. Reviews will be inserted without sentiment information.")
    
    return df


def insert_reviews(conn, df, bank_id_map):
    """
    Insert reviews into reviews table, skipping duplicates.
    
    Args:
        conn: Database connection
        df: DataFrame with review data
        bank_id_map: Dictionary mapping bank codes to bank_ids
    
    Returns:
        Number of reviews inserted
    """
    cursor = conn.cursor()
    
    try:
        # Check existing reviews to avoid duplicates
        print("Checking for existing reviews to avoid duplicates...")
        cursor.execute("""
            SELECT bank_id, review_text, review_date, COUNT(*) as count
            FROM reviews
            GROUP BY bank_id, review_text, review_date
        """)
        existing_reviews = set()
        for row in cursor.fetchall():
            # Create a unique key from bank_id, review_text (first 100 chars), and date
            key = (row[0], str(row[1])[:100], row[2])
            existing_reviews.add(key)
        
        print(f"Found {len(existing_reviews)} existing review combinations in database")
        
        # Prepare data for insertion
        reviews_to_insert = []
        skipped_count = 0
        
        for _, row in df.iterrows():
            bank_code = row['bank']
            if bank_code not in bank_id_map:
                print(f"⚠ Skipping review: Unknown bank '{bank_code}'")
                continue
            
            bank_id = bank_id_map[bank_code]
            
            # Parse date
            review_date = None
            if pd.notna(row.get('date')):
                try:
                    review_date = pd.to_datetime(row['date']).date()
                except:
                    pass
            
            # Check for duplicate
            review_text = str(row['review'])
            duplicate_key = (bank_id, review_text[:100], review_date)
            if duplicate_key in existing_reviews:
                skipped_count += 1
                continue
            
            # Parse rating
            rating = None
            if pd.notna(row.get('rating')):
                try:
                    rating = float(row['rating'])
                    if not (1 <= rating <= 5):
                        rating = None
                except:
                    pass
            
            # Get sentiment data if available
            sentiment_label = row.get('sentiment_label') if 'sentiment_label' in row else None
            sentiment_score = row.get('sentiment_score') if 'sentiment_score' in row else None
            
            # Parse sentiment_score
            if pd.notna(sentiment_score):
                try:
                    sentiment_score = float(sentiment_score)
                except:
                    sentiment_score = None
            
            # Get source
            source = row.get('source', 'Google Play')
            
            reviews_to_insert.append((
                bank_id,
                review_text,
                rating,
                review_date,
                sentiment_label,
                sentiment_score,
                source
            ))
        
        # Batch insert reviews
        if reviews_to_insert:
            insert_query = """
                INSERT INTO reviews (bank_id, review_text, rating, review_date, 
                                   sentiment_label, sentiment_score, source)
                VALUES %s
            """
            
            execute_values(cursor, insert_query, reviews_to_insert)
            conn.commit()
            
            inserted_count = len(reviews_to_insert)
            print(f"✓ Inserted {inserted_count} new reviews")
            if skipped_count > 0:
                print(f"⚠ Skipped {skipped_count} duplicate reviews")
            return inserted_count
        else:
            if skipped_count > 0:
                print(f"⚠ All {skipped_count} reviews were duplicates - nothing to insert")
            else:
                print("⚠ No reviews to insert")
            return 0
            
    except psycopg2.Error as e:
        conn.rollback()
        print(f"✗ Error inserting reviews: {e}")
        raise
    finally:
        cursor.close()


def verify_data_integrity(conn):
    """
    Run SQL queries to verify data integrity.
    
    Args:
        conn: Database connection
    """
    cursor = conn.cursor()
    
    try:
        print("\n" + "=" * 50)
        print("Data Integrity Verification")
        print("=" * 50)
        
        # Count total reviews
        cursor.execute("SELECT COUNT(*) FROM reviews")
        total_reviews = cursor.fetchone()[0]
        print(f"\nTotal reviews in database: {total_reviews}")
        
        # Count reviews per bank
        print("\nReviews per bank:")
        cursor.execute("""
            SELECT b.bank_name, COUNT(r.review_id) as review_count
            FROM banks b
            LEFT JOIN reviews r ON b.bank_id = r.bank_id
            GROUP BY b.bank_id, b.bank_name
            ORDER BY review_count DESC
        """)
        
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]} reviews")
        
        # Average rating per bank
        print("\nAverage rating per bank:")
        cursor.execute("""
            SELECT b.bank_name, 
                   ROUND(AVG(r.rating)::numeric, 2) as avg_rating,
                   COUNT(r.review_id) as review_count
            FROM banks b
            LEFT JOIN reviews r ON b.bank_id = r.bank_id
            WHERE r.rating IS NOT NULL
            GROUP BY b.bank_id, b.bank_name
            ORDER BY avg_rating DESC
        """)
        
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]} (from {row[2]} reviews)")
        
        # Sentiment distribution
        print("\nSentiment distribution:")
        cursor.execute("""
            SELECT sentiment_label, COUNT(*) as count
            FROM reviews
            WHERE sentiment_label IS NOT NULL
            GROUP BY sentiment_label
            ORDER BY count DESC
        """)
        
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]} reviews")
        
        # Reviews with missing sentiment
        cursor.execute("""
            SELECT COUNT(*) FROM reviews WHERE sentiment_label IS NULL
        """)
        missing_sentiment = cursor.fetchone()[0]
        if missing_sentiment > 0:
            print(f"\n⚠ Reviews without sentiment data: {missing_sentiment}")
        
        # Date range
        print("\nReview date range:")
        cursor.execute("""
            SELECT MIN(review_date), MAX(review_date)
            FROM reviews
            WHERE review_date IS NOT NULL
        """)
        date_range = cursor.fetchone()
        if date_range[0]:
            print(f"  From: {date_range[0]} to {date_range[1]}")
        
        print("=" * 50 + "\n")
        
    except psycopg2.Error as e:
        print(f"✗ Error verifying data integrity: {e}")
    finally:
        cursor.close()


def main():
    """Main function to insert data into PostgreSQL."""
    print("Starting database integration...")
    print("=" * 50)
    
    # Connect to database
    conn = get_db_connection()
    
    try:
        # Create tables
        create_tables(conn)
        
        # Insert banks
        bank_id_map = insert_banks(conn)
        
        # Load review data
        csv_file = os.path.join(os.path.dirname(__file__), '..', 'Data', 'all_banks.csv')
        if not os.path.exists(csv_file):
            print(f"✗ Error: CSV file not found: {csv_file}")
            print("Please run task1_preprocessing.py first")
            return
        
        df = load_review_data(csv_file)
        
        # Check for sentiment data
        df = check_sentiment_data(df)
        
        # Insert reviews
        inserted_count = insert_reviews(conn, df, bank_id_map)
        
        # Verify data integrity
        verify_data_integrity(conn)
        
        # Check KPI: >1,000 reviews or at least 400
        if inserted_count >= 400:
            print(f"✓ KPI met: {inserted_count} reviews inserted (target: >=400)")
        else:
            print(f"⚠ KPI not fully met: {inserted_count} reviews inserted (target: >=400)")
        
        print("\n✓ Database integration complete!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        raise
    finally:
        conn.close()
        print("✓ Database connection closed")


if __name__ == "__main__":
    main()

