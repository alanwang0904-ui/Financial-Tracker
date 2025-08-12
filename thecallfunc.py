# callfunc.py
# Visual upgrades only: consistent style, dollar-format y-axis, value labels, tight layout.

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

# A small helper to format dollars on the y-axis
def _dollar(x, pos):
    # format with thousands and no trailing .0
    return f"${x:,.0f}"

def visualize_quarterly_spending(transactions: pd.DataFrame, show: bool = True):
    """
    Visualizes spending by quarter with improved aesthetics.
    Keeps original name/signature; added 'show' flag (defaults True).
    """
    # Derive quarter if needed (non-destructive)
    df = transactions.copy()
    if "Quarter" not in df.columns:
        df["Quarter"] = df["Date"].dt.to_period("Q")

    quarterly_totals = df.groupby("Quarter", sort=True)["Amount"].sum()

    # Style: clean background, grid on y, readable fonts
    plt.rcParams.update({
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "figure.dpi": 110,
    })

    fig, ax = plt.subplots(figsize=(9, 5.2))
    bars = quarterly_totals.plot(kind="bar", alpha=0.9, ax=ax)

    ax.set_title("Quarterly Spending")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Total Spent (USD)")
    ax.yaxis.set_major_formatter(FuncFormatter(_dollar))
    ax.grid(axis="y", linestyle="--", linewidth=0.8, alpha=0.5)

    # Add value labels on top of bars
    for patch in bars.patches:
        height = patch.get_height()
        ax.annotate(
            f"${height:,.0f}",
            (patch.get_x() + patch.get_width() / 2, height),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    # Keep quarter labels horizontal for compactness
    for label in ax.get_xticklabels():
        label.set_rotation(0)

    fig.tight_layout()

    if show:
        plt.show()

    return fig  # return fig in case you want to save/close in caller