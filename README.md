# Amazon Best-Selling Books Analysis

An end-to-end, beginner-friendly Data Analytics and Exploratory Data Analysis (EDA) portfolio project analyzing synthetic Amazon best-selling book data using Python, Pandas, NumPy, Matplotlib, and Seaborn.

---

## ⚠️ Dataset Disclaimer
> **Important Note:** The dataset used in this project (`data/raw/amazon_bestselling_books_dummy.csv`) is **synthetic dummy data** created strictly for demonstration, portfolio, and educational practice. It does **not** represent actual proprietary Amazon e-commerce sales, internal Kindle Direct Publishing metrics, or verified Amazon Best Sellers Rank (BSR) figures.

---

## 📁 Repository Structure

```text
amazon-books-analysis/
├── data/
│   ├── raw/
│   │   └── amazon_bestselling_books_dummy.csv    # Original 1,000-record synthetic dataset
│   └── processed/
│       └── cleaned_books_data.csv                # Validated & cleaned dataset (995 unique titles)
├── notebooks/
│   └── amazon_books_analysis.ipynb               # Fully executed interactive Jupyter Notebook
├── src/
│   ├── run_analysis.py                           # Core automated pipeline (cleaning, EDA, charts)
│   ├── generate_dataset.py                       # Reproducible synthetic dataset generator
│   └── create_notebook.py                        # Jupyter notebook builder
├── outputs/
│   ├── charts/                                   # High-resolution statistical visualizations (PNG)
│   │   ├── top_10_books.png
│   │   ├── genre_sales.png
│   │   ├── price_distribution.png
│   │   ├── rating_distribution.png
│   │   └── reviews_vs_sales.png
│   └── reports/                                  # Exported analysis CSV summaries
│       ├── top_10_books.csv
│       ├── genre_analysis.csv
│       ├── author_analysis.csv
│       └── format_analysis.csv
├── .gitignore                                    # Git exclusion rules for cache and editor files
├── requirements.txt                              # Lightweight project dependencies
└── README.md                                     # Project documentation and findings
```

---

## 🎯 Project Objectives & Core Analytical Questions

This project answers fundamental e-commerce merchandising and publishing questions:
1. **Catalog Integrity:** How do we detect, clean, and impute duplicate or missing data appropriately without distorting group metrics?
2. **Top Performers:** What are the top 10 titles by simulated monthly units sold?
3. **Genre Dynamics:** Which genres command the highest volume vs. the highest per-title sales velocity?
4. **Format Breakdown:** How does unit demand divide between Kindle eBooks, Paperbacks, and Hardcovers relative to their respective price points?
5. **Rating vs. Social Proof:** Does a higher customer rating drive higher sales volume, or does review count (social proof) carry stronger predictive weight?

---

## 🛠️ Installation & Setup

### 1. Prerequisites
Ensure Python 3.10+ is installed on your system.

### 2. Clone or Open the Repository
```bash
git clone https://github.com/your-username/amazon-books-analysis.git
cd amazon-books-analysis
```

### 3. Install Dependencies
Install only the packages required by the project:
```bash
pip install -r requirements.txt
```

---

## 🚀 Execution Guide

You can run the project either via Python scripts or interactively in Jupyter:

### Option A: Run the Automated CLI Pipeline
Run the complete analysis pipeline from any directory:
```bash
python src/run_analysis.py
```
This will:
- Load the raw data from `data/raw/`
- Deduplicate and impute missing values, exporting to `data/processed/`
- Compute summary statistics and export CSV reports to `outputs/reports/`
- Generate and save all 5 publication-ready charts to `outputs/charts/`

### Option B: Interactive Jupyter Notebook
Open and run all cells in the notebook:
```bash
jupyter notebook notebooks/amazon_books_analysis.ipynb
```
*(Or open `notebooks/amazon_books_analysis.ipynb` directly in VS Code with the Jupyter extension).*

---

## 🧹 Data Cleaning Methodology

| Check / Issue | Action Taken | Rationale |
| :--- | :--- | :--- |
| **Duplicates (`book_id`)** | 5 duplicates removed | Retained first occurrence to ensure unique catalog records (1,000 → 995 rows). |
| **Missing Prices** | 3 values imputed with format median | Kindle, Paperback, and Hardcover have distinctly separated price distributions. |
| **Missing Ratings** | 4 values imputed with genre median | Preserves category-level baseline quality perception. |
| **Numeric Bounds** | Verified `price > 0`, `rating ∈ [1.0, 5.0]` | Confirmed absence of negative sales or corrupted inputs. |

---

## 📊 Summary of Findings & Key Metrics

### Overall Catalog Metrics
- **Catalog Size:** 995 unique titles
- **Average Price:** **$15.27** (Median: **$13.54**)
- **Average Rating:** **4.40 / 5.00**
- **Total Simulated Monthly Sales:** **3,958,547 units**

### Format Comparison
- **Kindle:** 469 titles | 2,107,969 units (**53.25% market share**) | Avg Price: **$9.02** | Avg Rating: 4.39
- **Paperback:** 372 titles | 1,403,302 units (**35.45% market share**) | Avg Price: **$17.47** | Avg Rating: 4.41
- **Hardcover:** 154 titles | 447,276 units (**11.30% market share**) | Avg Price: **$29.03** | Avg Rating: 4.41

### Top Genres by Monthly Sales
1. **Fiction:** 658,347 units (16.63% share, 164 titles)
2. **Non-Fiction:** 629,804 units (15.91% share, 158 titles)
3. **Sci-Fi & Fantasy:** 570,673 units (14.42% share, 134 titles — highest per-book velocity: 4,258.8 units)
4. **Self-Help:** 496,546 units (12.54% share, 127 titles)
5. **Business & Finance:** 481,884 units (12.17% share, 118 titles)

---

## 💡 Five Evidence-Based Business Insights

1. **Volume Concentration in Fiction & Non-Fiction:**  
   Together, Fiction and Non-Fiction comprise **32.54% of catalog unit volume** (1,288,151 monthly units). Publishers should allocate core catalog acquisition budgets to these broad-audience genres.
2. **Sci-Fi & Fantasy Yields Peak Sales Velocity:**  
   While Fiction has the highest gross volume due to catalog size, **Sci-Fi & Fantasy** achieves the highest average sales per title (**4,258.8 units/book**), suggesting high reader retention and series commitment.
3. **Kindle Price Elasticity Drives Over 53% of Units:**  
   At an accessible average price of **$9.02**, Kindle accounts for **53.25%** of all unit sales. Digital editions serve as the primary discovery and conversion engine.
4. **Social Proof (Reviews) Outweighs Rating Margins ($r = 0.811$ vs. $r = 0.098$):**  
   Review volume demonstrates a strong correlation of **0.811** with monthly sales, whereas star ratings show an almost neutral correlation (**0.098**). Marketing investments are better spent driving review volume than obsessing over fractional star differences.
5. **Evergreen Anchor Titles Drive Recurring Cash Flow:**  
   **173 titles** possess both a rating $\ge 4.5$ and $> 5,000$ reviews. These evergreen titles generate consistent, predictable cash flow with low advertising overhead.

---

## ⚠️ Analytical Limitations: Reviews as a Sales Proxy
When interpreting real-world e-commerce sales, caution must be exercised when using reviews as a proxy for sales volume:
- **Lifetime vs. Current Rate:** Reviews accumulate over many years, whereas monthly sales represent instantaneous demand. An older classic title may hold 50,000 reviews while selling only 100 copies a month today.
- **Category Propensity Differences:** Non-fiction and technical readers leave reviews at significantly higher rates than readers of light romance or pulp fiction.
- **Digital vs. Physical Friction:** Kindle e-readers prompt for a review automatically at the end of the text, giving digital formats an inherently higher review conversion rate than physical print books.
- **Promotional Noise:** Limited-time free downloads and steep discount campaigns generate review spikes without corresponding paid unit sales.

---

## 📜 License & Portfolio Usage
Created for educational and portfolio demonstration. Feel free to use the project structure and analysis pipeline as a template for your own data analytics projects.
