"""
Generate high-resolution, professional portfolio screenshots for LinkedIn and Naukri.
Uses actual calculated results from outputs/reports/ with clear disclaimers.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"

SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

# Set high-DPI modern aesthetic
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica', 'Segoe UI'],
    'axes.edgecolor': '#cbd5e1',
    'axes.linewidth': 1.2,
    'grid.color': '#f1f5f9',
    'grid.linestyle': '--',
    'grid.alpha': 0.7,
})


def generate_screenshot_top_10():
    top_10_csv = REPORTS_DIR / "top_10_books.csv"
    df = pd.read_csv(top_10_csv)
    
    # Sort ascending for horizontal bar chart (so top item is at the top)
    df_sorted = df.sort_values(by="estimated_monthly_units_sold", ascending=True).copy()
    # Format labels with Title and Author
    labels = [f"{row['title']}  —  {row['author']} ({row['genre']})" for _, row in df_sorted.iterrows()]
    values = df_sorted["estimated_monthly_units_sold"]

    fig, ax = plt.subplots(figsize=(16, 9.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#fafbfc')

    # Gradient-like color palette
    colors = sns.color_palette("crest", n_colors=len(df_sorted))

    bars = ax.barh(labels, values, color=colors, height=0.68, edgecolor='#0f172a', linewidth=0.6)

    # Add data labels
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 120,
            bar.get_y() + bar.get_height() / 2,
            f"{width:,.0f} units",
            va='center',
            ha='left',
            fontsize=11.5,
            fontweight='bold',
            color='#1e293b'
        )

    # Title & Subtitle
    plt.text(
        0, 1.08,
        "TOP 10 BEST-SELLING BOOKS (MONTHLY SALES VELOCITY)",
        transform=ax.transAxes,
        fontsize=18,
        fontweight='bold',
        color='#0f172a'
    )
    plt.text(
        0, 1.03,
        "Simulated Amazon Catalog Analysis  |  Ranked by Estimated Monthly Units Sold",
        transform=ax.transAxes,
        fontsize=12,
        color='#64748b'
    )

    # Axis formatting
    ax.set_xlabel("Estimated Monthly Units Sold (Simulated Units)", fontsize=13, fontweight='semibold', color='#334155', labelpad=12)
    ax.set_xlim(0, max(values) * 1.18)
    ax.tick_params(axis='y', labelsize=11, labelcolor='#1e293b')
    ax.tick_params(axis='x', labelsize=11, labelcolor='#475569')

    # Watermark Disclaimer for LinkedIn
    plt.text(
        0.5, -0.09,
        "* Synthetic Demo Dataset for Portfolio Practice  |  Not Actual Proprietary Amazon Sales  |  github.com/lakshitsharma7/amazon-books-analysis",
        transform=ax.transAxes,
        fontsize=10.5,
        color='#94a3b8',
        ha='center',
        style='italic'
    )

    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    output_path = SCREENSHOTS_DIR / "01_top_10_bestselling_books.png"
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f"[SUCCESS] Generated: {output_path}")


def generate_screenshot_genre_sales():
    genre_csv = REPORTS_DIR / "genre_analysis.csv"
    df = pd.read_csv(genre_csv)
    
    # Sort ascending for horizontal bar chart
    df_sorted = df.sort_values(by="total_monthly_sales", ascending=True).copy()
    genres = df_sorted["genre"]
    sales = df_sorted["total_monthly_sales"]
    shares = df_sorted["sales_market_share_pct"]
    book_counts = df_sorted["book_count"]

    fig, ax = plt.subplots(figsize=(16, 9.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#fafbfc')

    colors = sns.color_palette("flare", n_colors=len(df_sorted))

    bars = ax.barh(genres, sales, color=colors, height=0.68, edgecolor='#0f172a', linewidth=0.6)

    # Add text labels on the bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        share = shares.iloc[i]
        count = book_counts.iloc[i]
        ax.text(
            width + 8000,
            bar.get_y() + bar.get_height() / 2,
            f"{width:,.0f} units  ({share:.1f}% Share | {count} Titles)",
            va='center',
            ha='left',
            fontsize=11.5,
            fontweight='bold',
            color='#1e293b'
        )

    # Title & Subtitle
    plt.text(
        0, 1.08,
        "AMAZON BOOKS GENRE SALES & MARKET SHARE ANALYSIS",
        transform=ax.transAxes,
        fontsize=18,
        fontweight='bold',
        color='#0f172a'
    )
    plt.text(
        0, 1.03,
        "Total Estimated Monthly Sales & Volume Share Across 10 Key Book Categories",
        transform=ax.transAxes,
        fontsize=12,
        color='#64748b'
    )

    # Axis formatting
    ax.set_xlabel("Total Estimated Monthly Units Sold (Simulated Units)", fontsize=13, fontweight='semibold', color='#334155', labelpad=12)
    ax.set_xlim(0, max(sales) * 1.25)
    ax.tick_params(axis='y', labelsize=12, labelcolor='#1e293b')
    ax.tick_params(axis='x', labelsize=11, labelcolor='#475569')

    # Watermark Disclaimer for LinkedIn
    plt.text(
        0.5, -0.09,
        "* Synthetic Demo Dataset for Portfolio Practice  |  Not Actual Proprietary Amazon Sales  |  github.com/lakshitsharma7/amazon-books-analysis",
        transform=ax.transAxes,
        fontsize=10.5,
        color='#94a3b8',
        ha='center',
        style='italic'
    )

    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    output_path = SCREENSHOTS_DIR / "02_genre_sales_analysis.png"
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f"[SUCCESS] Generated: {output_path}")


if __name__ == "__main__":
    generate_screenshot_top_10()
    generate_screenshot_genre_sales()
