"""
Amazon Best-Selling Books Analysis
Complete end-to-end data processing, exploratory analysis, and visualization pipeline.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Define project directories relative to this file
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "amazon_bestselling_books_dummy.csv"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_books_data.csv"
CHARTS_DIR = PROJECT_ROOT / "outputs" / "charts"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"

# Ensure output directories exist
PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
CHARTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Set clean aesthetic styling for plots
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.titlesize': 16
})

def main():
    print("=" * 65)
    print("1. DATA LOADING")
    print("=" * 65)
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Source dataset not found at {RAW_DATA_PATH}!")

    raw_df = pd.read_csv(RAW_DATA_PATH)
    print(f"Dataset Shape: {raw_df.shape[0]} rows, {raw_df.shape[1]} columns")
    print("\nFirst 5 rows:")
    print(raw_df.head())
    print("\nColumn Data Types:")
    print(raw_df.dtypes)

    print("\n" + "=" * 65)
    print("2. DATA CLEANING")
    print("=" * 65)
    dup_count = raw_df.duplicated(subset=['book_id']).sum()
    print(f"Number of duplicate records (by book_id): {dup_count}")

    missing_vals = raw_df.isnull().sum()
    print("\nMissing values per column:")
    print(missing_vals[missing_vals > 0])

    # Clean duplicates
    df_clean = raw_df.drop_duplicates(subset=['book_id']).copy()

    # Impute missing prices with median price of that format
    df_clean['price_usd'] = df_clean.groupby('format')['price_usd'].transform(
        lambda x: x.fillna(x.median())
    )

    # Impute missing ratings with median rating of that genre
    df_clean['rating'] = df_clean.groupby('genre')['rating'].transform(
        lambda x: x.fillna(round(x.median(), 1))
    )

    # Validate numerical boundaries
    assert (df_clean['price_usd'] > 0).all(), "Found invalid price"
    assert (df_clean['rating'].between(1.0, 5.0)).all(), "Found invalid rating"
    assert (df_clean['estimated_monthly_units_sold'] >= 0).all(), "Found negative sales"
    assert (df_clean['review_count'] >= 0).all(), "Found negative reviews"

    df_clean.reset_index(drop=True, inplace=True)
    df_clean.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"\n[SUCCESS] Cleaned dataset saved to: {PROCESSED_DATA_PATH} ({len(df_clean)} rows)")

    print("\n" + "=" * 65)
    print("3. EXPLORATORY DATA ANALYSIS (EDA)")
    print("=" * 65)

    # 3.1 Top 10 books by estimated sales
    top_10 = df_clean.nlargest(10, 'estimated_monthly_units_sold')[
        ['book_id', 'title', 'author', 'genre', 'format', 'price_usd', 'rating', 'review_count', 'estimated_monthly_units_sold']
    ]
    top_10.to_csv(REPORTS_DIR / "top_10_books.csv", index=False)
    print("Top 10 Books by Estimated Monthly Units Sold:")
    print(top_10[['title', 'author', 'genre', 'estimated_monthly_units_sold']])

    # 3.2 Overall Key Metrics
    avg_price = df_clean['price_usd'].mean()
    median_price = df_clean['price_usd'].median()
    avg_rating = df_clean['rating'].mean()
    total_monthly_sales = df_clean['estimated_monthly_units_sold'].sum()
    avg_monthly_sales = df_clean['estimated_monthly_units_sold'].mean()

    print(f"\nOverall Metrics:")
    print(f"• Average Book Price: ${avg_price:.2f} (Median: ${median_price:.2f})")
    print(f"• Average Customer Rating: {avg_rating:.2f} / 5.0")
    print(f"• Total Catalog Monthly Sales: {total_monthly_sales:,} units")
    print(f"• Average Monthly Sales per Title: {avg_monthly_sales:.1f} units")

    # 3.3 Genre Analysis
    genre_summary = df_clean.groupby('genre').agg(
        book_count=('book_id', 'count'),
        total_monthly_sales=('estimated_monthly_units_sold', 'sum'),
        avg_monthly_sales=('estimated_monthly_units_sold', 'mean'),
        avg_price_usd=('price_usd', 'mean'),
        avg_rating=('rating', 'mean'),
        avg_reviews=('review_count', 'mean')
    ).reset_index()

    genre_summary['sales_market_share_pct'] = (
        genre_summary['total_monthly_sales'] / total_monthly_sales * 100
    ).round(2)
    genre_summary.sort_values(by='total_monthly_sales', ascending=False, inplace=True)
    genre_summary.to_csv(REPORTS_DIR / "genre_analysis.csv", index=False)
    print("\nGenre Performance Summary:")
    print(genre_summary[['genre', 'book_count', 'total_monthly_sales', 'avg_monthly_sales', 'sales_market_share_pct']])

    # 3.4 Author Performance Analysis
    author_summary = df_clean.groupby('author').agg(
        titles_count=('book_id', 'count'),
        total_sales=('estimated_monthly_units_sold', 'sum'),
        avg_sales_per_book=('estimated_monthly_units_sold', 'mean'),
        avg_rating=('rating', 'mean'),
        primary_genre=('genre', lambda x: x.mode()[0])
    ).reset_index().sort_values(by='total_sales', ascending=False)
    author_summary.to_csv(REPORTS_DIR / "author_analysis.csv", index=False)
    print("\nTop 5 Authors by Simulated Monthly Sales:")
    print(author_summary.head(5))

    # 3.5 Format Comparison
    format_summary = df_clean.groupby('format').agg(
        titles_count=('book_id', 'count'),
        total_sales=('estimated_monthly_units_sold', 'sum'),
        avg_sales=('estimated_monthly_units_sold', 'mean'),
        avg_price=('price_usd', 'mean'),
        avg_rating=('rating', 'mean')
    ).reset_index()
    format_summary['sales_share_pct'] = (
        format_summary['total_sales'] / total_monthly_sales * 100
    ).round(2)
    format_summary.to_csv(REPORTS_DIR / "format_analysis.csv", index=False)
    print("\nFormat Comparison:")
    print(format_summary)

    # 3.6 Correlation
    corr = df_clean[['price_usd', 'rating', 'review_count', 'estimated_monthly_units_sold', 'publication_year']].corr()
    print("\nCorrelation Matrix:")
    print(corr[['estimated_monthly_units_sold', 'review_count', 'rating', 'price_usd']])

    print("\n" + "=" * 65)
    print("4. GENERATING VISUALIZATIONS")
    print("=" * 65)

    # Chart 1: Top 10 Books by Monthly Sales
    plt.figure(figsize=(10, 6))
    bar_colors = sns.color_palette("viridis", len(top_10))
    sns.barplot(
        data=top_10,
        x='estimated_monthly_units_sold',
        y='title',
        hue='title',
        legend=False,
        palette=bar_colors
    )
    plt.title("Top 10 Books by Estimated Monthly Units Sold", weight='bold', pad=15)
    plt.xlabel("Estimated Monthly Units Sold")
    plt.ylabel("Book Title")
    for index, value in enumerate(top_10['estimated_monthly_units_sold']):
        plt.text(value + 100, index, f"{value:,}", va='center', fontsize=9, fontweight='semibold')
    plt.tight_layout()
    chart1_path = CHARTS_DIR / "top_10_books.png"
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print(f"Saved: {chart1_path}")

    # Chart 2: Total Estimated Sales by Genre
    plt.figure(figsize=(11, 6))
    sns.barplot(
        data=genre_summary,
        x='total_monthly_sales',
        y='genre',
        hue='genre',
        legend=False,
        palette="flare"
    )
    plt.title("Total Estimated Monthly Units Sold by Genre", weight='bold', pad=15)
    plt.xlabel("Total Monthly Units Sold")
    plt.ylabel("Genre")
    for index, value in enumerate(genre_summary['total_monthly_sales']):
        plt.text(value + 8000, index, f"{value:,}", va='center', fontsize=9)
    plt.tight_layout()
    chart2_path = CHARTS_DIR / "genre_sales.png"
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print(f"Saved: {chart2_path}")

    # Chart 3: Price Distribution by Format
    plt.figure(figsize=(9, 5))
    sns.histplot(
        data=df_clean,
        x='price_usd',
        hue='format',
        multiple='stack',
        bins=30,
        palette="tab10",
        edgecolor="white"
    )
    plt.axvline(avg_price, color='red', linestyle='--', label=f'Mean Price (${avg_price:.2f})')
    plt.title("Distribution of Book Prices by Format", weight='bold', pad=15)
    plt.xlabel("Price (USD)")
    plt.ylabel("Number of Books")
    plt.legend()
    plt.tight_layout()
    chart3_path = CHARTS_DIR / "price_distribution.png"
    plt.savefig(chart3_path, dpi=300)
    plt.close()
    print(f"Saved: {chart3_path}")

    # Chart 4: Rating Distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(
        df_clean['rating'],
        bins=15,
        kde=True,
        color="#3b82f6",
        edgecolor="white"
    )
    plt.axvline(avg_rating, color='darkorange', linestyle='--', label=f'Mean Rating ({avg_rating:.2f})')
    plt.title("Book Rating Distribution", weight='bold', pad=15)
    plt.xlabel("Rating (1.0 to 5.0)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    chart4_path = CHARTS_DIR / "rating_distribution.png"
    plt.savefig(chart4_path, dpi=300)
    plt.close()
    print(f"Saved: {chart4_path}")

    # Chart 5: Review Count vs Estimated Sales
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=df_clean,
        x='review_count',
        y='estimated_monthly_units_sold',
        hue='format',
        size='rating',
        sizes=(30, 200),
        alpha=0.7,
        palette="Set2"
    )
    plt.xscale('log')
    plt.yscale('log')
    plt.title("Review Count vs. Estimated Monthly Sales (Log Scale)", weight='bold', pad=15)
    plt.xlabel("Review Count (Log Scale)")
    plt.ylabel("Estimated Monthly Units Sold (Log Scale)")
    plt.tight_layout()
    chart5_path = CHARTS_DIR / "reviews_vs_sales.png"
    plt.savefig(chart5_path, dpi=300)
    plt.close()
    print(f"Saved: {chart5_path}")

    print("\n[SUCCESS] Pipeline execution complete. Reports & charts saved to 'outputs/'.")

if __name__ == "__main__":
    main()
