import csv
from pathlib import Path
import matplotlib.pyplot as plt

results_dir = Path.home() / "cvw" / "cep_results"
csv_path = results_dir / "wally_transpose_results.csv"

rows = []
with open(csv_path, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        row["block_size"] = int(row["block_size"])
        row["cycles"] = int(row["cycles"])
        row["instructions"] = int(row["instructions"])
        row["cpi"] = float(row["cpi"])
        row["speedup_vs_naive"] = float(row["speedup_vs_naive"])
        rows.append(row)

rows = sorted(rows, key=lambda r: r["block_size"])

x = list(range(len(rows)))
labels = ["Naive" if r["block_size"] == 0 else f"B={r['block_size']}" for r in rows]

def make_plot(y_key, ylabel, title, filename):
    y = [r[y_key] for r in rows]
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, marker="o")
    plt.xticks(x, labels)
    plt.xlabel("Transpose version / block size")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(results_dir / filename, dpi=200)
    plt.close()

make_plot("cycles", "Cycles", "Wally Transpose: Cycles vs Block Size", "wally_cycles_vs_block.png")
make_plot("instructions", "Instructions retired", "Wally Transpose: Instructions vs Block Size", "wally_instructions_vs_block.png")
make_plot("cpi", "CPI", "Wally Transpose: CPI vs Block Size", "wally_cpi_vs_block.png")
make_plot("speedup_vs_naive", "Speedup vs naive", "Wally Transpose: Speedup vs Block Size", "wally_speedup_vs_block.png")

print("Generated plots:")
for name in [
    "wally_cycles_vs_block.png",
    "wally_instructions_vs_block.png",
    "wally_cpi_vs_block.png",
    "wally_speedup_vs_block.png",
]:
    print(results_dir / name)
