"""
Dataset Generator for Amazon Best-Selling Books Analysis
Generates a realistic 1,000-record synthetic dataset for educational & portfolio analysis.
"""

import sys
import argparse
from pathlib import Path
import numpy as np
import pandas as pd

# Set up reliable project root and data path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_PATH = RAW_DATA_DIR / "amazon_bestselling_books_dummy.csv"


def generate_dataset(force: bool = False):
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    if OUTPUT_PATH.exists() and not force:
        print(f"[INFO] Dataset already exists at {OUTPUT_PATH}.")
        print("To protect existing data, generation was skipped. Use '--force' flag to overwrite.")
        return

    np.random.seed(42)

    # Sample pools for realistic book generation
    genres = [
        "Fiction", "Non-Fiction", "Self-Help", "Sci-Fi & Fantasy",
        "Business & Finance", "Mystery & Thriller", "Biography & Memoir",
        "Romance", "Health & Wellness", "Technology"
    ]
    genre_weights = [0.18, 0.16, 0.14, 0.12, 0.11, 0.10, 0.07, 0.05, 0.04, 0.03]

    formats = ["Kindle", "Paperback", "Hardcover"]
    format_weights = [0.45, 0.40, 0.15]

    authors_by_genre = {
        "Fiction": ["F. Scott Fitzgerald", "Harper Lee", "George Orwell", "Jane Austen", "Gabriel Garcia Marquez", "Toni Morrison", "Colleen Hoover", "Matt Haig"],
        "Non-Fiction": ["Malcolm Gladwell", "Yuval Noah Harari", "Michael Lewis", "Bill Bryson", "Rebecca Skloot", "David Grann"],
        "Self-Help": ["James Clear", "Dale Carnegie", "Stephen Covey", "Mark Manson", "Brené Brown", "Atomic Thinker", "Robert Kiyosaki"],
        "Sci-Fi & Fantasy": ["Frank Herbert", "J.R.R. Tolkien", "Isaac Asimov", "Brandon Sanderson", "Neil Gaiman", "Andy Weir"],
        "Business & Finance": ["Morgan Housel", "Peter Thiel", "Ray Dalio", "Benjamin Graham", "Alex Hormozi", "Eric Ries"],
        "Mystery & Thriller": ["Agatha Christie", "Gillian Flynn", "Dan Brown", "Stephen King", "Paula Hawkins", "Lucy Foley"],
        "Biography & Memoir": ["Walter Isaacson", "Michelle Obama", "Tara Westover", "Trevor Noah", "Phil Knight"],
        "Romance": ["Emily Henry", "Ali Hazelwood", "Nicholas Sparks", "Sally Rooney", "Taylor Jenkins Reid"],
        "Health & Wellness": ["Peter Attia", "Matthew Walker", "Andrew Huberman", "Michael Pollan", "Tim Ferriss"],
        "Technology": ["Andrew Ng", "Martin Kleppmann", "Stuart Russell", "Chip Huyen", "Gene Kim"]
    }

    title_adjectives = ["Silent", "Atomic", "Infinite", "Subtle", "Deep", "Hidden", "Unreasonable", "Essential", "Brave", "Lost", "Digital", "Curious", "Predictable", "Courageous", "Modern", "Mindful"]
    title_nouns = ["Habits", "World", "Secrets", "Mind", "Code", "Echoes", "Shadows", "Path", "Art", "Empire", "Equation", "Future", "Paradox", "Journey", "Strategy", "Horizon"]

    titles_generated = set()
    records = []

    # Generate 995 unique records, then add 5 duplicates to simulate realistic data-cleaning exercises
    for i in range(1, 996):
        genre = np.random.choice(genres, p=genre_weights)
        author = np.random.choice(authors_by_genre[genre])
        
        adj = np.random.choice(title_adjectives)
        noun = np.random.choice(title_nouns)
        cand_title = f"The {adj} {noun} of {author.split()[-1]}"
        suffix_counter = 1
        while cand_title in titles_generated:
            suffix_counter += 1
            cand_title = f"The {adj} {noun} Vol. {suffix_counter}"
        titles_generated.add(cand_title)
        
        book_format = np.random.choice(formats, p=format_weights)
        
        if book_format == "Kindle":
            price = round(float(np.random.uniform(2.99, 14.99)), 2)
        elif book_format == "Paperback":
            price = round(float(np.random.uniform(9.99, 24.99)), 2)
        else:  # Hardcover
            price = round(float(np.random.uniform(18.99, 39.99)), 2)
            
        rating = round(float(np.clip(np.random.normal(4.4, 0.35), 2.8, 5.0)), 1)
        review_count = int(np.clip(np.random.lognormal(mean=7.5, sigma=1.1), 50, 85000))
        
        base_sales = (review_count ** 0.55) * (rating / 4.0) * 45
        if book_format == "Kindle":
            base_sales *= 1.25
        elif book_format == "Hardcover":
            base_sales *= 0.8
            
        sales = int(np.clip(base_sales * np.random.uniform(0.7, 1.35), 20, 15000))
        pub_year = int(np.random.choice(range(2010, 2025), p=[0.03, 0.03, 0.04, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.10, 0.06, 0.02]))
        
        records.append({
            "book_id": f"B0{1000 + i}",
            "title": cand_title,
            "author": author,
            "genre": genre,
            "format": book_format,
            "price_usd": price,
            "rating": rating,
            "review_count": review_count,
            "estimated_monthly_units_sold": sales,
            "publication_year": pub_year
        })

    # Add 5 intentional duplicates
    duplicate_indices = [12, 45, 120, 250, 480]
    for idx in duplicate_indices:
        records.append(dict(records[idx]))

    df = pd.DataFrame(records)

    # Introduce intentional nulls for data hygiene practice
    null_rating_idx = [34, 88, 215, 604]
    null_price_idx = [102, 340, 712]

    for idx in null_rating_idx:
        df.loc[idx, "rating"] = np.nan
    for idx in null_price_idx:
        df.loc[idx, "price_usd"] = np.nan

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"[SUCCESS] Generated {len(df)} records saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic Amazon books dataset.")
    parser.add_argument("--force", action="store_true", help="Force overwrite existing dataset.")
    args = parser.parse_args()
    generate_dataset(force=args.force)
