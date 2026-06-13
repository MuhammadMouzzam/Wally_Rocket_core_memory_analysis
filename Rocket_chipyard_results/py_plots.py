#!/usr/bin/env python3

import os
import pandas as pd
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Folder structure
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_DIR = os.path.join(BASE_DIR, "csv")
PLOTS_DIR = os.path.join(BASE_DIR, "plots")

BLOCK_CSV = os.path.join(CSV_DIR, "rocket_block_size_results.csv")
ASSOC_CSV = os.path.join(CSV_DIR, "rocket_set_associativity_results.csv")

os.makedirs(PLOTS_DIR, exist_ok=True)


# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def clean_columns(df):
    """
    Normalize column names so the script works even if spaces,
    hyphens, or capitalization differ slightly.
    """
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.replace("$", "", regex=False)
    )
    return df


def find_col(df, possible_names):
    """
    Find the first matching column from a list of possible names.
    """
    for name in possible_names:
        if name in df.columns:
            return name
    raise KeyError(f"Could not find any of these columns: {possible_names}\nAvailable columns: {list(df.columns)}")


def save_line_plot(x, y, xlabel, ylabel, title, filename, xtick_labels=None):
    """
    Save one clean line plot.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, marker="o")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, linestyle="--", linewidth=0.5)

    if xtick_labels is not None:
        plt.xticks(x, xtick_labels)
    else:
        plt.xticks(x)

    plt.tight_layout()
    out_path = os.path.join(PLOTS_DIR, filename)
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Saved: {out_path}")


# ------------------------------------------------------------
# Load CSV files
# ------------------------------------------------------------

if not os.path.exists(BLOCK_CSV):
    raise FileNotFoundError(f"Missing block-size CSV file: {BLOCK_CSV}")

if not os.path.exists(ASSOC_CSV):
    raise FileNotFoundError(f"Missing associativity CSV file: {ASSOC_CSV}")

block_df = clean_columns(pd.read_csv(BLOCK_CSV))
assoc_df = clean_columns(pd.read_csv(ASSOC_CSV))


# ------------------------------------------------------------
# Detect required block-size columns
# ------------------------------------------------------------

block_size_col = find_col(block_df, ["block_size", "block"])
block_cycles_col = find_col(block_df, ["cycles"])
block_inst_col = find_col(block_df, ["instructions", "instret", "instruction_count"])
block_cpi_col = find_col(block_df, ["cpi"])
block_speedup_col = find_col(block_df, ["speedup_vs_naive", "speedup"])

# Convert block size to numeric.
# Naive should normally be stored as 0.
block_df[block_size_col] = pd.to_numeric(block_df[block_size_col], errors="coerce")

# Keep only valid rows and sort by block size
block_df = block_df.dropna(subset=[block_size_col]).copy()
block_df[block_size_col] = block_df[block_size_col].astype(int)
block_df = block_df.sort_values(by=block_size_col)

# X-axis labels: show block size 0 as Naive
block_x = block_df[block_size_col].tolist()
block_x_labels = ["Naive" if x == 0 else str(x) for x in block_x]


# ------------------------------------------------------------
# Detect required associativity columns
# ------------------------------------------------------------

assoc_ways_col = find_col(assoc_df, ["ways", "associativity", "assoc"])
assoc_cycles_col = find_col(assoc_df, ["cycles"])
assoc_cpi_col = find_col(assoc_df, ["cpi"])
assoc_miss_col = find_col(assoc_df, ["d_cache_miss", "dcache_miss", "d_cache_misses", "dcache_misses", "misses"])
assoc_miss_rate_col = find_col(assoc_df, ["miss_rate", "d_cache_miss_rate", "dcache_miss_rate"])

assoc_df[assoc_ways_col] = pd.to_numeric(assoc_df[assoc_ways_col], errors="coerce")
assoc_df = assoc_df.dropna(subset=[assoc_ways_col]).copy()
assoc_df[assoc_ways_col] = assoc_df[assoc_ways_col].astype(int)
assoc_df = assoc_df.sort_values(by=assoc_ways_col)

assoc_x = assoc_df[assoc_ways_col].tolist()


# ------------------------------------------------------------
# Block-size plots
# ------------------------------------------------------------

save_line_plot(
    x=block_x,
    y=block_df[block_cycles_col],
    xlabel="Block Size",
    ylabel="Cycles",
    title="Block Size vs Cycles",
    filename="block_size_vs_cycles.png",
    xtick_labels=block_x_labels
)

save_line_plot(
    x=block_x,
    y=block_df[block_inst_col],
    xlabel="Block Size",
    ylabel="Instructions",
    title="Block Size vs Instructions",
    filename="block_size_vs_instructions.png",
    xtick_labels=block_x_labels
)

save_line_plot(
    x=block_x,
    y=block_df[block_cpi_col],
    xlabel="Block Size",
    ylabel="CPI",
    title="Block Size vs CPI",
    filename="block_size_vs_cpi.png",
    xtick_labels=block_x_labels
)

save_line_plot(
    x=block_x,
    y=block_df[block_speedup_col],
    xlabel="Block Size",
    ylabel="Speedup vs Naive",
    title="Speedup vs Block Size",
    filename="speedup_vs_block_size.png",
    xtick_labels=block_x_labels
)


# ------------------------------------------------------------
# Associativity plots
# ------------------------------------------------------------

save_line_plot(
    x=assoc_x,
    y=assoc_df[assoc_cycles_col],
    xlabel="Associativity / Ways",
    ylabel="Cycles",
    title="Associativity vs Cycles",
    filename="assoc_vs_cycles.png"
)

save_line_plot(
    x=assoc_x,
    y=assoc_df[assoc_cpi_col],
    xlabel="Associativity / Ways",
    ylabel="CPI",
    title="Associativity vs CPI",
    filename="assoc_vs_cpi.png"
)

save_line_plot(
    x=assoc_x,
    y=assoc_df[assoc_miss_col],
    xlabel="Associativity / Ways",
    ylabel="D-cache Misses",
    title="Associativity vs D-cache Misses",
    filename="assoc_vs_misses.png"
)

save_line_plot(
    x=assoc_x,
    y=assoc_df[assoc_miss_rate_col],
    xlabel="Associativity / Ways",
    ylabel="D-cache Miss Rate",
    title="Associativity vs D-cache Miss Rate",
    filename="assoc_vs_miss_rate.png"
)


print("\nAll plots generated successfully.")
print(f"Plots folder: {PLOTS_DIR}")