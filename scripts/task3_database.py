"""
Task 3: Database Integration Script (OOP Version)
Stores cleaned and processed review data in PostgreSQL database.
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv
import sys
from typing import Dict, Optional, Tuple

load_dotenv()


class DatabaseConnection:
    """Handles database connection management."""
    
    def __init__(self, config: Optional[Dict[str, str]] = None):
        """
        Initialize database connection.
        
        Args:
            config: Database configuration dict (uses .env if None)
        """
        if config is None:
            self.config = {
                'host': os.getenv('DB_HOST', 'localhost'),
                'port': os.getenv('DB_PORT', '5432'),
                'database': os.getenv('DB_NAME', 'bank_reviews'),
                'user': os.getenv('DB_USER', 'postgres'),
                'password': os.getenv('DB_PASSWORD', 'kacha@gbe')
            }
        else:
            self.config = config
        self.conn = None
    
    def connect(self) -> psycopg2.extensions.connection:
        """Create and return database connection."""
        try:
            self.conn = psycopg2.connect(**self.config)
            print(f"✓ Successfully connected to database: {self.config['database']}")
            return self.conn
        except psycopg2.Error as e:
            print(f"✗ Error connecting to database: {e}")
            sys.exit(1)
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print("✓ Database connection closed")


class SchemaManager:
    """Handles database schema creation and management."""
    
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
    
    def __init__(self, conn: psycopg2.extensions.connection):
        """
        Initialize schema manager.
        
        Args:
            conn: Database connection
        """
        self.conn = conn
    
    def create_tables(self):
        """Create database tables if they don't exist."""
        cursor = self.conn.cursor()
        
        try:
            schema_file = os.path.join(os.path.dirname(__file__), '..', 'schema.sql')
            if os.path.exists(schema_file):
                with open(schema_file, 'r') as f:
                    schema_sql = f.read()
                cursor.execute(schema_sql)
                self.conn.commit()
                print("✓ Database tables created/verified")
            else:
                print(f"⚠ Schema file not found: {schema_file}")
                self._create_tables_manually(cursor)
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"✗ Error creating tables: {e}")
            raise
        finally:
            cursor.close()
    
    def _create_tables_manually(self, cursor):
        """Create tables manually if schema file not found."""
        print("Creating tables manually...")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS banks (
                bank_id SERIAL PRIMARY KEY,
                bank_name VARCHAR(255) NOT NULL,
                app_name VARCHAR(255),
                description TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
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
        for index_sql in [
            "CREATE INDEX IF NOT EXISTS idx_reviews_bank_id ON reviews(bank_id)",
            "CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating)",
            "CREATE INDEX IF NOT EXISTS idx_reviews_sentiment_label ON reviews(sentiment_label)",
            "CREATE INDEX IF NOT EXISTS idx_reviews_review_date ON reviews(review_date)",
            "CREATE INDEX IF NOT EXISTS idx_banks_bank_name ON banks(bank_name)"
        ]:
            cursor.execute(index_sql)
        
        self.conn.commit()
        print("✓ Database tables created")
    
    def insert_banks(self) -> Dict[str, int]:
        """
        Insert bank information into banks table.
        
        Returns:
            Dictionary mapping bank names to bank_ids
        """
        cursor = self.conn.cursor()
        bank_id_map = {}
        
        try:
            for bank_code, bank_data in self.BANK_INFO.items():
                cursor.execute(
                    "SELECT bank_id FROM banks WHERE bank_name = %s",
                    (bank_data['bank_name'],)
                )
                result = cursor.fetchone()
                
                if result:
                    bank_id_map[bank_code] = result[0]
                    print(f"✓ Bank '{bank_data['bank_name']}' already exists (ID: {result[0]})")
                else:
                    cursor.execute("""
                        INSERT INTO banks (bank_name, app_name, description)
                        VALUES (%s, %s, %s)
                        RETURNING bank_id
                    """, (bank_data['bank_name'], bank_data['app_name'], bank_data['description']))
                    
                    bank_id = cursor.fetchone()[0]
                    bank_id_map[bank_code] = bank_id
                    print(f"✓ Inserted bank '{bank_data['bank_name']}' (ID: {bank_id})")
            
            self.conn.commit()
            return bank_id_map
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"✗ Error inserting banks: {e}")
            raise
        finally:
            cursor.close()


class ReviewInserter:
    """Handles insertion of reviews into database."""
    
    def __init__(self, conn: psycopg2.extensions.connection):
        """
        Initialize review inserter.
        
        Args:
            conn: Database connection
        """
        self.conn = conn
    
    def insert_reviews(self, df: pd.DataFrame, bank_id_map: Dict[str, int]) -> int:
        """
        Insert reviews into reviews table, skipping duplicates.
        
        Args:
            df: DataFrame with review data
            bank_id_map: Dictionary mapping bank codes to bank_ids
        
        Returns:
            Number of reviews inserted
        """
        cursor = self.conn.cursor()
        
        try:
            # Check existing reviews
            print("Checking for existing reviews to avoid duplicates...")
            cursor.execute("""
                SELECT bank_id, review_text, review_date, COUNT(*) as count
                FROM reviews
                GROUP BY bank_id, review_text, review_date
            """)
            existing_reviews = set()
            for row in cursor.fetchall():
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
                
                # Get sentiment data
                sentiment_label = row.get('sentiment_label') if 'sentiment_label' in row else None
                sentiment_score = row.get('sentiment_score') if 'sentiment_score' in row else None
                
                if pd.notna(sentiment_score):
                    try:
                        sentiment_score = float(sentiment_score)
                    except:
                        sentiment_score = None
                
                source = row.get('source', 'Google Play')
                
                reviews_to_insert.append((
                    bank_id, review_text, rating, review_date,
                    sentiment_label, sentiment_score, source
                ))
            
            # Batch insert
            if reviews_to_insert:
                insert_query = """
                    INSERT INTO reviews (bank_id, review_text, rating, review_date, 
                                       sentiment_label, sentiment_score, source)
                    VALUES %s
                """
                execute_values(cursor, insert_query, reviews_to_insert)
                self.conn.commit()
                
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
            self.conn.rollback()
            print(f"✗ Error inserting reviews: {e}")
            raise
        finally:
            cursor.close()


class DataIntegrityVerifier:
    """Handles data integrity verification."""
    
    def __init__(self, conn: psycopg2.extensions.connection):
        """
        Initialize verifier.
        
        Args:
            conn: Database connection
        """
        self.conn = conn
    
    def verify(self):
        """Run SQL queries to verify data integrity."""
        cursor = self.conn.cursor()
        
        try:
            print("\n" + "=" * 50)
            print("Data Integrity Verification")
            print("=" * 50)
            
            # Total reviews
            cursor.execute("SELECT COUNT(*) FROM reviews")
            total_reviews = cursor.fetchone()[0]
            print(f"\nTotal reviews in database: {total_reviews}")
            
            # Reviews per bank
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
            
            # Missing sentiment
            cursor.execute("SELECT COUNT(*) FROM reviews WHERE sentiment_label IS NULL")
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


class DatabaseManager:
    """Main class for database operations."""
    
    def __init__(self, csv_file: str = '../Data/all_banks.csv'):
        """
        Initialize database manager.
        
        Args:
            csv_file: Path to CSV file with reviews
        """
        self.csv_file = csv_file
        self.db_conn = DatabaseConnection()
        self.conn = None
        self.schema_manager = None
        self.review_inserter = None
        self.verifier = None
    
    def load_data(self) -> pd.DataFrame:
        """Load review data from CSV."""
        if not os.path.exists(self.csv_file):
            raise FileNotFoundError(f"CSV file not found: {self.csv_file}. Please run task1_preprocessing.py first")
        
        df = pd.read_csv(self.csv_file)
        print(f"✓ Loaded {len(df)} reviews from {self.csv_file}")
        return df
    
    def check_sentiment_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Check if sentiment data exists and merge if available."""
        if 'sentiment_label' in df.columns and 'sentiment_score' in df.columns:
            print("✓ Sentiment data found in CSV")
            return df
        
        sentiment_file = os.path.join(os.path.dirname(__file__), '..', 'Data', 'all_banks_with_sentiment.csv')
        if os.path.exists(sentiment_file):
            print(f"✓ Loading sentiment data from {sentiment_file}")
            sentiment_df = pd.read_csv(sentiment_file)
            
            if 'sentiment_label' in sentiment_df.columns:
                df = pd.merge(
                    df,
                    sentiment_df[['review', 'bank', 'sentiment_label', 'sentiment_score']],
                    on=['review', 'bank'],
                    how='left',
                    suffixes=('', '_sentiment')
                )
                
                if 'sentiment_label_sentiment' in df.columns:
                    df['sentiment_label'] = df['sentiment_label_sentiment']
                    df['sentiment_score'] = df['sentiment_score_sentiment']
                    df = df.drop(['sentiment_label_sentiment', 'sentiment_score_sentiment'], axis=1)
            
            print("✓ Sentiment data merged")
        else:
            print("⚠ No sentiment data found. Reviews will be inserted without sentiment information.")
        
        return df
    
    def run(self) -> Tuple[int, bool]:
        """
        Run the complete database integration process.
        
        Returns:
            Tuple of (inserted_count, kpi_met)
        """
        print("Starting database integration...")
        print("=" * 50)
        
        # Connect to database
        self.conn = self.db_conn.connect()
        
        try:
            # Initialize managers
            self.schema_manager = SchemaManager(self.conn)
            self.review_inserter = ReviewInserter(self.conn)
            self.verifier = DataIntegrityVerifier(self.conn)
            
            # Create tables
            self.schema_manager.create_tables()
            
            # Insert banks
            bank_id_map = self.schema_manager.insert_banks()
            
            # Load and prepare data
            df = self.load_data()
            df = self.check_sentiment_data(df)
            
            # Insert reviews
            inserted_count = self.review_inserter.insert_reviews(df, bank_id_map)
            
            # Verify data integrity
            self.verifier.verify()
            
            # Check KPI
            kpi_met = inserted_count >= 400
            if kpi_met:
                print(f"✓ KPI met: {inserted_count} reviews inserted (target: >=400)")
            else:
                print(f"⚠ KPI not fully met: {inserted_count} reviews inserted (target: >=400)")
            
            print("\n✓ Database integration complete!")
            return inserted_count, kpi_met
            
        except Exception as e:
            print(f"✗ Error: {e}")
            raise
        finally:
            self.db_conn.close()


def main():
    """Main function for backward compatibility."""
    manager = DatabaseManager()
    return manager.run()


if __name__ == "__main__":
    manager = DatabaseManager()
    manager.run()
