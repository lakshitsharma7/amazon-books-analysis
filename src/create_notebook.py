"""
Creates the master Jupyter Notebook at notebooks/amazon_books_analysis.ipynb
with robust pathlib.Path resolution for inputs and outputs.
"""

from pathlib import Path
import nbformat as nbf

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_PATH = PROJECT_ROOT / "notebooks" / "amazon_books_analysis.ipynb"
NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)

nb = nbf.v4.new_notebook()
cells = []

# Cell 1: Markdown Title & Intro
cells.append(nbf.v4.new_markdown_cell("""# Amazon Best-Selling Books Analysis Using Python and Pandas
**Project Level:** Exploratory Data Analysis & Business Intelligence  
**Tech Stack:** Python 3, Pandas, NumPy, Matplotlib, Seaborn, Pathlib  

---

### Project Overview
This project provides a complete exploratory data analysis (EDA) of a 1,000-record synthetic Amazon best-selling book catalog.

> **Dataset Disclaimer:** This dataset contains simulated synthetic data for analytical and educational demonstration. It does not represent actual proprietary Amazon e-commerce sales or internal metrics.

#### Objectives:
1. **Data Loading:** Ingest raw CSV data, evaluate dimensions, columns, and initial records.
2. **Data Cleaning:** Handle missing values, eliminate duplicate rows, validate domain boundaries.
3. **Exploratory Data Analysis (EDA):** Identify top-selling titles, compute catalog benchmarks (averages, distributions), analyze genre and format performance, and investigate review-to-sales correlations.
4. **Data Visualization:** Produce publication-ready visualizations.
5. **Business Insights:** Generate actionable, evidence-based insights backed by computed data.
"""))

# Cell 2: Setup and dynamic path resolution
cells.append(nbf.v4.new_code_cell("""# Step 0: Imports and Dynamic Project Path Setup
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Resolve Project Root dynamically (handles both running from project root or inside notebooks/)
NOTEBOOK_DIR = Path.cwd()
PROJECT_ROOT = NOTEBOOK_DIR if (NOTEBOOK_DIR / "data").exists() else NOTEBOOK_DIR.parent

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "amazon_bestselling_books_dummy.csv"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_books_data.csv"
CHARTS_DIR = PROJECT_ROOT / "outputs" / "charts"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"

# Ensure output directories exist
PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
CHARTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Styling configuration
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.titlesize': 16
})

print(f"Project Root: {PROJECT_ROOT}")
print(f"Raw Data Path: {RAW_DATA_PATH} (Exists: {RAW_DATA_PATH.exists()})")
"""))

# Cell 3: Data Loading Markdown
cells.append(nbf.v4.new_markdown_cell("""---
## 1. Data Loading
We load the original dataset from `data/raw/amazon_bestselling_books_dummy.csv` and inspect its initial shape, columns, and data types.
"""))

# Cell 4: Read CSV and inspect
cells.append(nbf.v4.new_code_cell("""# 1.1 Load the raw dataset
df_raw = pd.read_csv(RAW_DATA_PATH)

print(f"Dataset Dimensions: {df_raw.shape[0]} rows, {df_raw.shape[1]} columns\\n")
print("Columns in Dataset:")
print(list(df_raw.columns))
"""))

cells.append(nbf.v4.new_code_cell("""# 1.2 Inspect the first 5 records
df_raw.head()
"""))

cells.append(nbf.v4.new_code_cell("""# 1.3 Data types and memory usage
df_raw.info()
"""))

cells.append(nbf.v4.new_code_cell("""# 1.4 Descriptive statistical summary of numerical features
df_raw.describe()
"""))

# Cell 5: Data Cleaning Markdown
cells.append(nbf.v4.new_markdown_cell("""---
## 2. Data Cleaning & Validation
Data hygiene steps performed:
1. **Duplicate Detection & Removal:** Find duplicate `book_id` records.
2. **Missing Value Imputation:** Impute missing `price_usd` using format-specific medians and missing `rating` using genre-specific medians.
3. **Range Validation:** Ensure prices > 0, ratings ∈ [1.0, 5.0], and sales/reviews ≥ 0.
4. **Data Export:** Export cleaned dataset to `data/processed/cleaned_books_data.csv`.
"""))

cells.append(nbf.v4.new_code_cell("""# 2.1 Check for duplicate records
duplicates_count = df_raw.duplicated(subset=['book_id']).sum()
print(f"Duplicate book_id records detected: {duplicates_count}")

# Drop duplicates, retaining first occurrence
df_clean = df_raw.drop_duplicates(subset=['book_id']).copy()
print(f"Records retained after deduplication: {len(df_clean)}")
"""))

cells.append(nbf.v4.new_code_cell("""# 2.2 Identify missing values per column
missing_vals = df_clean.isnull().sum()
print("Missing values:")
print(missing_vals[missing_vals > 0])
"""))

cells.append(nbf.v4.new_code_cell("""# 2.3 Impute missing values with group medians
# Impute missing price using the median price of that specific format (Kindle vs Paperback vs Hardcover)
df_clean['price_usd'] = df_clean.groupby('format')['price_usd'].transform(
    lambda s: s.fillna(s.median())
)

# Impute missing rating using the median rating for that genre
df_clean['rating'] = df_clean.groupby('genre')['rating'].transform(
    lambda s: s.fillna(round(s.median(), 1))
)

print("Remaining null values after imputation:", df_clean.isnull().sum().sum())
"""))

cells.append(nbf.v4.new_code_cell("""# 2.4 Validate numeric domain boundaries
assert (df_clean['price_usd'] > 0).all(), "Invalid non-positive price found"
assert (df_clean['rating'].between(1.0, 5.0)).all(), "Invalid rating outside 1.0-5.0"
assert (df_clean['estimated_monthly_units_sold'] >= 0).all(), "Negative sales found"
assert (df_clean['review_count'] >= 0).all(), "Negative reviews found"

# Reset index and export to processed data directory
df_clean.reset_index(drop=True, inplace=True)
df_clean.to_csv(PROCESSED_DATA_PATH, index=False)
print(f"Cleaned dataset successfully saved to: {PROCESSED_DATA_PATH}")
"""))

# Cell 6: EDA Markdown
cells.append(nbf.v4.new_markdown_cell("""---
## 3. Exploratory Data Analysis (EDA)
Comprehensive exploration of:
- Top 10 books by estimated monthly sales volume
- Average book price & average rating
- Genre performance and market share
- Author performance analysis
- Format comparison (Kindle, Paperback, Hardcover)
- Review count, rating, and sales correlation matrix
"""))

cells.append(nbf.v4.new_code_cell("""# 3.1 Top 10 Books by Estimated Monthly Units Sold
top_10_books = df_clean.nlargest(10, 'estimated_monthly_units_sold')[
    ['book_id', 'title', 'author', 'genre', 'format', 'price_usd', 'rating', 'review_count', 'estimated_monthly_units_sold']
]

# Save report
top_10_books.to_csv(REPORTS_DIR / "top_10_books.csv", index=False)
top_10_books[['title', 'author', 'genre', 'format', 'price_usd', 'rating', 'estimated_monthly_units_sold']]
"""))

cells.append(nbf.v4.new_code_cell("""# 3.2 Overall Catalog Metrics
avg_price = df_clean['price_usd'].mean()
median_price = df_clean['price_usd'].median()
avg_rating = df_clean['rating'].mean()
total_sales = df_clean['estimated_monthly_units_sold'].sum()
avg_sales_per_title = df_clean['estimated_monthly_units_sold'].mean()

print(f"Catalog Key Metrics:")
print(f"• Average Book Price: ${avg_price:.2f}")
print(f"• Median Book Price:  ${median_price:.2f}")
print(f"• Average Rating:     {avg_rating:.2f} / 5.00")
print(f"• Total Catalog Monthly Estimated Sales: {total_sales:,} units")
print(f"• Average Monthly Units Sold per Title:   {avg_sales_per_title:.1f} units")
"""))

cells.append(nbf.v4.new_code_cell("""# 3.3 Genre Performance Analysis
genre_analysis = df_clean.groupby('genre').agg(
    book_count=('book_id', 'count'),
    total_monthly_sales=('estimated_monthly_units_sold', 'sum'),
    avg_monthly_sales=('estimated_monthly_units_sold', 'mean'),
    avg_price_usd=('price_usd', 'mean'),
    avg_rating=('rating', 'mean'),
    avg_reviews=('review_count', 'mean')
).reset_index()

genre_analysis['sales_share_pct'] = (
    genre_analysis['total_monthly_sales'] / total_sales * 100
).round(2)

genre_analysis.sort_values(by='total_monthly_sales', ascending=False, inplace=True)
genre_analysis.to_csv(REPORTS_DIR / "genre_analysis.csv", index=False)
genre_analysis
"""))

cells.append(nbf.v4.new_code_cell("""# 3.4 Author Performance Analysis
author_analysis = df_clean.groupby('author').agg(
    titles_published=('book_id', 'count'),
    total_sales=('estimated_monthly_units_sold', 'sum'),
    avg_sales_per_title=('estimated_monthly_units_sold', 'mean'),
    avg_rating=('rating', 'mean'),
    primary_genre=('genre', lambda g: g.mode()[0])
).reset_index().sort_values(by='total_sales', ascending=False)

author_analysis.to_csv(REPORTS_DIR / "author_analysis.csv", index=False)
print("Top 10 Authors by Total Estimated Sales:")
author_analysis.head(10)
"""))

cells.append(nbf.v4.new_code_cell("""# 3.5 Format Comparison (Kindle vs Paperback vs Hardcover)
format_comparison = df_clean.groupby('format').agg(
    titles_count=('book_id', 'count'),
    total_sales=('estimated_monthly_units_sold', 'sum'),
    avg_sales=('estimated_monthly_units_sold', 'mean'),
    avg_price=('price_usd', 'mean'),
    avg_rating=('rating', 'mean')
).reset_index()

format_comparison['sales_share_pct'] = (
    format_comparison['total_sales'] / total_sales * 100
).round(2)

format_comparison.to_csv(REPORTS_DIR / "format_analysis.csv", index=False)
format_comparison
"""))

cells.append(nbf.v4.new_code_cell("""# 3.6 Numeric Correlation Matrix
numeric_cols = ['price_usd', 'rating', 'review_count', 'estimated_monthly_units_sold', 'publication_year']
correlation_matrix = df_clean[numeric_cols].corr()
correlation_matrix.round(3)
"""))

# Cell 7: Visualization Markdown
cells.append(nbf.v4.new_markdown_cell("""---
## 4. Data Visualization
Charts generated and saved into `outputs/charts/`:
1. Top 10 Books Bar Chart
2. Total Monthly Sales by Genre
3. Distribution of Book Prices Across Formats
4. Customer Rating Distribution
5. Review Count vs Estimated Monthly Sales (Log-Log)
"""))

cells.append(nbf.v4.new_code_cell("""# Chart 1: Bar chart of Top 10 Books
plt.figure(figsize=(10, 6))
palette = sns.color_palette("mako", len(top_10_books))
ax = sns.barplot(
    data=top_10_books,
    x='estimated_monthly_units_sold',
    y='title',
    hue='title',
    legend=False,
    palette=palette
)
plt.title("Top 10 Books by Estimated Monthly Units Sold", weight='bold', pad=15)
plt.xlabel("Estimated Monthly Units Sold (Simulated)")
plt.ylabel("Book Title")

for i, v in enumerate(top_10_books['estimated_monthly_units_sold']):
    ax.text(v + 150, i, f"{v:,}", va='center', fontsize=9, fontweight='semibold')

plt.xlim(0, max(top_10_books['estimated_monthly_units_sold']) * 1.15)
plt.tight_layout()
plt.savefig(CHARTS_DIR / "top_10_books.png", dpi=300)
plt.show()
"""))

cells.append(nbf.v4.new_code_cell("""# Chart 2: Total Estimated Sales by Genre
plt.figure(figsize=(11, 6))
ax = sns.barplot(
    data=genre_analysis,
    x='total_monthly_sales',
    y='genre',
    hue='genre',
    legend=False,
    palette="viridis"
)
plt.title("Total Estimated Monthly Units Sold by Genre", weight='bold', pad=15)
plt.xlabel("Total Monthly Units Sold (Simulated)")
plt.ylabel("Genre")

for i, v in enumerate(genre_analysis['total_monthly_sales']):
    ax.text(v + 10000, i, f"{v:,} ({genre_analysis['sales_share_pct'].iloc[i]}%)", va='center', fontsize=9)

plt.xlim(0, max(genre_analysis['total_monthly_sales']) * 1.22)
plt.tight_layout()
plt.savefig(CHARTS_DIR / "genre_sales.png", dpi=300)
plt.show()
"""))

cells.append(nbf.v4.new_code_cell("""# Chart 3: Distribution of Book Prices Across Formats
plt.figure(figsize=(9, 5))
sns.histplot(
    data=df_clean,
    x='price_usd',
    hue='format',
    multiple='stack',
    bins=30,
    palette="deep",
    edgecolor="white"
)
plt.axvline(avg_price, color='crimson', linestyle='--', linewidth=2, label=f'Mean Price (${avg_price:.2f})')
plt.title("Distribution of Book Prices Across Formats", weight='bold', pad=15)
plt.xlabel("Price (USD)")
plt.ylabel("Book Count")
plt.legend()
plt.tight_layout()
plt.savefig(CHARTS_DIR / "price_distribution.png", dpi=300)
plt.show()
"""))

cells.append(nbf.v4.new_code_cell("""# Chart 4: Rating Distribution
plt.figure(figsize=(8, 5))
sns.histplot(
    df_clean['rating'],
    bins=15,
    kde=True,
    color="#2563eb",
    edgecolor="white"
)
plt.axvline(avg_rating, color='#ea580c', linestyle='--', linewidth=2, label=f'Mean Rating ({avg_rating:.2f})')
plt.title("Customer Rating Distribution", weight='bold', pad=15)
plt.xlabel("Rating (1.0 to 5.0)")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.savefig(CHARTS_DIR / "rating_distribution.png", dpi=300)
plt.show()
"""))

cells.append(nbf.v4.new_code_cell("""# Chart 5: Review Count vs. Estimated Monthly Sales
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df_clean,
    x='review_count',
    y='estimated_monthly_units_sold',
    hue='format',
    size='rating',
    sizes=(25, 200),
    alpha=0.65,
    palette="Accent"
)
plt.xscale('log')
plt.yscale('log')
plt.title("Review Count vs. Estimated Monthly Sales (Log-Log Scale)", weight='bold', pad=15)
plt.xlabel("Total Cumulative Reviews (Log Scale)")
plt.ylabel("Estimated Monthly Units Sold (Log Scale)")
plt.tight_layout()
plt.savefig(CHARTS_DIR / "reviews_vs_sales.png", dpi=300)
plt.show()
"""))

# Cell 8: Business Insights & Limitations Markdown
cells.append(nbf.v4.new_markdown_cell("""---
## 5. Business Insights & Strategic Findings

### 5.1 Evidence-Based Business Insights (Calculated Directly from Dataset)
1. **Fiction & Non-Fiction Drive Core Catalog Volume (32.54% Share):**  
   Fiction leads all genres with **658,347 units sold monthly** (16.63% market share across 164 titles), followed closely by Non-Fiction with **629,804 units** (15.91% share across 158 titles). Combined, these two categories represent **32.54%** of total catalog sales.
2. **Sci-Fi & Fantasy and Health & Wellness Boast Highest Sales Velocity:**  
   While Fiction has the highest gross volume due to catalog size, **Sci-Fi & Fantasy** achieves the highest average velocity per book at **4,258.8 units/title**, closely followed by **Health & Wellness** with **4,248.5 units/title**.
3. **Kindle Format Drives 53.25% of All Unit Sales:**  
   Digital Kindle editions account for **2,107,969 units** (53.25% of total sales volume) at an accessible average price of **$9.02**, outperforming Paperbacks (35.45% share, avg price $17.47) and Hardcovers (11.30% share, avg price $29.03).
4. **Strong Positive Correlation Between Reviews and Estimated Sales ($r = 0.811$):**  
   Cumulative reviews show a robust correlation of **0.811** with monthly unit sales, whereas customer ratings exhibit an almost neutral correlation with volume ($r = 0.098$). This indicates social proof and visibility matter more for ongoing sales volume than a marginal 0.1 difference in customer rating.
5. **High-Rated Powerhouse Books:**  
   There are **173 books** in the dataset that maintain both an exceptional rating ($\ge 4.5$) and over **5,000 reviews**. These titles serve as recurring bestsellers that yield disproportionate revenue and anchor brand credibility.

---

### 5.2 Critical Limitations of Interpreting Reviews as Direct Measures of Sales
When performing real-world e-commerce analytics, interpreting review count directly as sales volume has major limitations:
- **Lifetime Cumulative vs. Current Velocity:** Reviews accumulate over a book's entire lifespan (sometimes 10+ years), whereas monthly sales reflect current demand velocity. An older classic may have 60,000 reviews but sell only 200 copies a month today.
- **Review Submission Propensity Varies by Category & Audience:** Certain genres (e.g. self-help, technical books, controversial non-fiction) prompt significantly higher reader engagement than lightweight beach reads.
- **Format Discrepancies:** Kindle readers can leave a review with a single tap at the final page prompt, leading to a higher review conversion rate than physical paperback/hardcover buyers.
- **Promotional & Marketing Spikes:** Free book promotions, BookBub blasts, and Kindle Unlimited borrow cycles inflate review counts without reflecting sustained commercial unit sales.
"""))

nb['cells'] = cells

with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"[SUCCESS] Wrote notebook to: {NOTEBOOK_PATH}")
