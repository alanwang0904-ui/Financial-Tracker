# Financial Tracker.py
# Visual upgrades only: clearer console messages, dollar formatting, nicer charts.
# Keeps your interactive input() flow and overall structure.

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from thecallfunc import visualize_quarterly_spending

def _dollar(x, pos):
    return f"${x:,.0f}"

def import_and_process_data():
    """
    Imports and processes transaction data from a CSV file.
    Returns a DataFrame with an additional 'Month' column.
    (Unchanged behavior; improved error messages.)
    """
    while True:
        try:
            file_name = input("Enter the name of your CSV file (e.g., transactions.csv): ").strip()
            transactions = pd.read_csv(file_name)
            if not all(col in transactions.columns for col in ['Date', 'Amount']):
                raise ValueError("CSV must include 'Date' and 'Amount' columns.")
            # Convert 'Date' to datetime and add 'Month'
            transactions['Date'] = pd.to_datetime(transactions['Date'], errors="coerce")
            transactions = transactions.dropna(subset=['Date', 'Amount']).copy()
            transactions['Month'] = transactions['Date'].dt.to_period('M')
            print("✅ Loaded data successfully.\n")
            return transactions
        except Exception as e:
            print(f"⚠️  Error: {e}\nPlease check your file name and format, then try again.\n")

def calculate_and_alert(transactions, limit):
    """
    Calculates monthly spending totals and alerts for overspending.
    Returns a Series of monthly totals.
    (Same logic; nicer printing.)
    """
    monthly_totals = transactions.groupby('Month')['Amount'].sum()

    print("\n--- Monthly Spending (by Month) ---")
    for m, total in monthly_totals.items():
        print(f"  {m}: ${total:,.2f}")

    # Overspending alert
    print("\n--- Overspending Alerts ---")
    any_alert = False
    for month, total in monthly_totals.items():
        if total > limit:
            print(f"  ⚠️  {month}: ${total:,.2f} (over your limit of ${limit:,.2f})")
            any_alert = True
    if not any_alert:
        print("  None. 🎉")

    # Suggested budget (unchanged)
    average_spending = monthly_totals.mean() if len(monthly_totals) else 0.0
    suggested_budget = average_spending * 0.9
    print(f"\nSuggested monthly budget based on your history: ${suggested_budget:,.2f}")

    return monthly_totals

def additional_reports(monthly_totals):
    """
    Generates additional spending insights like highest spending month and cumulative spending.
    (Same logic; prettier printing.)
    """
    if monthly_totals.empty:
        print("\nNo data available for additional reports.")
        return None, pd.Series(dtype=float)

    highest_month = monthly_totals.idxmax()
    highest_amount = monthly_totals.max()
    print(f"\nHighest Spending Month: {highest_month}  (${highest_amount:,.2f})")

    cumulative_spending = monthly_totals.cumsum()
    print("\n--- Cumulative Spending ---")
    for m, total in cumulative_spending.items():
        print(f"  Through {m}: ${total:,.2f}")

    return highest_month, cumulative_spending

def _style_matplotlib():
    # Apply a consistent, clean look to your charts
    plt.rcParams.update({
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "figure.dpi": 110,
        "axes.grid": True,
        "grid.linestyle": "--",
        "grid.linewidth": 0.8,
        "grid.alpha": 0.5,
    })

def visualize_spending(monthly_totals, cumulative_spending):
    """
    Visualizes monthly spending and cumulative spending using bar and line charts.
    (Same plots; improved formatting and labels.)
    """
    _style_matplotlib()

    # Bar chart for monthly totals
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    monthly_totals.plot(kind='bar', alpha=0.9, ax=ax1)
    ax1.set_title("Monthly Spending")
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Total Spent (USD)")
    ax1.yaxis.set_major_formatter(FuncFormatter(_dollar))
    for label in ax1.get_xticklabels():
        label.set_rotation(45)
        label.set_ha("right")
    # Value labels
    for p in ax1.patches:
        height = p.get_height()
        ax1.annotate(f"${height:,.0f}",
                     (p.get_x() + p.get_width()/2, height),
                     xytext=(0, 6), textcoords="offset points",
                     ha='center', va='bottom', fontsize=9)
    fig1.tight_layout()
    plt.show()

    # Line chart for cumulative spending
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    cumulative_spending.plot(kind='line', marker='o', ax=ax2)
    ax2.set_title("Cumulative Spending Over Time")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Cumulative Spent (USD)")
    ax2.yaxis.set_major_formatter(FuncFormatter(_dollar))
    for label in ax2.get_xticklabels():
        label.set_rotation(45)
        label.set_ha("right")
    fig2.tight_layout()
    plt.show()

def monthly_comparison(monthly_totals):
    """
    Compares monthly spending against the average monthly spending.
    (Same logic; clearer message.)
    """
    average_spending = monthly_totals.mean() if len(monthly_totals) else 0.0
    print("\n--- Monthly Spending vs. Average ---")
    for month, total in monthly_totals.items():
        diff = total - average_spending
        direction = "above" if diff > 0 else "below"
        print(f"  {month}: ${total:,.2f} ({abs(diff):,.2f} {direction} average ${average_spending:,.2f})")

def transaction_summary(transactions):
    """
    Provides a summary of all transactions, including counts by size.
    (Same logic; cleaner output.)
    """
    total_transactions = len(transactions)
    print(f"\nTotal transactions recorded: {total_transactions:,}")

    small = transactions[transactions['Amount'] < 100]
    medium = transactions[(transactions['Amount'] >= 100) & (transactions['Amount'] < 500)]
    large = transactions[transactions['Amount'] >= 500]

    print(f"  Small (< $100): {len(small):,}")
    print(f"  Medium ($100–$500): {len(medium):,}")
    print(f"  Large (>= $500): {len(large):,}")

def main():
    """
    Main function to coordinate the finance tracker workflow.
    (Behavior unchanged; output is prettier.)
    """
    print("Welcome to the Enhanced Personal Finance Tracker!")
    print("This tool helps track spending, set a budget, and gain insights into your financial habits.\n")

    # Step 1: Import and process data
    transactions = import_and_process_data()

    # Step 2: Set spending limit
    while True:
        try:
            limit_str = input("Enter your monthly spending limit (e.g., 1500): ").strip()
            limit = float(limit_str)
            if limit <= 0:
                raise ValueError("Limit must be greater than zero.")
            break
        except ValueError as e:
            print(f"⚠️  Error: {e}\nPlease enter a positive number.\n")

    # Step 3: Calculate spending and alerts
    monthly_totals = calculate_and_alert(transactions, limit)

    # Step 4: Generate additional reports
    _highest_month, cumulative_spending = additional_reports(monthly_totals)

    # Step 5: Visualize quarterly spending (improved visuals)
    visualize_quarterly_spending(transactions, show=True)

    # Step 6: Visualize spending in detail (improved visuals)
    visualize_spending(monthly_totals, cumulative_spending)

    # Step 7: Monthly comparison (cleaner output)
    monthly_comparison(monthly_totals)

    # Step 8: Transaction summary (cleaner output)
    transaction_summary(transactions)

    print("\nThanks for using Alan's Finance Tracker!")

if __name__ == "__main__":
    main()