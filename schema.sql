-- PostgreSQL Database Schema for Bank Reviews Analysis
-- Database: bank_reviews

-- Create Banks Table
CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(255) NOT NULL,
    app_name VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create Reviews Table
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
);

-- Create Indexes for Performance
CREATE INDEX IF NOT EXISTS idx_reviews_bank_id ON reviews(bank_id);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);
CREATE INDEX IF NOT EXISTS idx_reviews_sentiment_label ON reviews(sentiment_label);
CREATE INDEX IF NOT EXISTS idx_reviews_review_date ON reviews(review_date);
CREATE INDEX IF NOT EXISTS idx_banks_bank_name ON banks(bank_name);

-- Insert Bank Data (if not exists)
INSERT INTO banks (bank_name, app_name, description) 
SELECT 'CBE', 'Commercial Bank of Ethiopia', 'Commercial Bank of Ethiopia mobile banking application'
WHERE NOT EXISTS (SELECT 1 FROM banks WHERE bank_name = 'CBE');

INSERT INTO banks (bank_name, app_name, description) 
SELECT 'BOA', 'Bank of Abyssinia', 'Bank of Abyssinia mobile banking application'
WHERE NOT EXISTS (SELECT 1 FROM banks WHERE bank_name = 'BOA');

INSERT INTO banks (bank_name, app_name, description) 
SELECT 'Dashen', 'Dashen Bank', 'Dashen Bank mobile banking application'
WHERE NOT EXISTS (SELECT 1 FROM banks WHERE bank_name = 'Dashen');

