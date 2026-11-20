"""
Summarize experiment results and produce the frontier figure.

Inputs
------
code/results/raw_results.csv  (produced by run_experiments.py)

Outputs
-------
code/results/results_table.csv
code/results/results_table.md
code/results/figure_cost_vs_incorrect_reuse.png
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


RESULTS_DIR = Path(__file__).parent / "results"
POLICY_LABEL = {
    "proposed": "Proposed",
    "B1": "B1 Full revalidation",
    "B3": "B3 No sharing",
    "B4": "B4 Random",
    "B5": "B5 Max uncertainty",
}
POLICY_ORDER = ["proposed", "B1", "B3", "B4", "B5"]


def _mean_std(series: pd.Series) -> str:
    return f"{series.mean():.1f} ± {series.std():.1f}"


def main():
    df = pd.read_csv(RESULTS_DIR / "raw_results.csv")
    # Per-policy aggregates
    agg = df.groupby("policy").agg(
        total_cost_mean=("total_cost", "mean"),
        total_cost_std=("total_cost", "std"),
        verification_cost_mean=("verification_cost", "mean"),
        decision_cost_mean=("decision_cost", "mean"),
        incorrect_reuse_rate_mean=("incorrect_reuse_rate", "mean"),
        incorrect_reuse_rate_std=("incorrect_reuse_rate", "std"),
        escalation_rate_mean=("escalation_rate", "mean"),
        decision_days_mean=("decision_days", "mean"),
    ).reindex(POLICY_ORDER)

    agg.to_csv(RESULTS_DIR / "results_table.csv")

    # Pretty markdown table
    md_lines = [
        "# Results: S1 (equipment upgrade), 5-station line",
        "",
        f"N_INSTANCES = {df['instance'].nunique()}, N_REPS = {df['rep'].nunique()}, total runs = {len(df)}.",
        "Numbers are mean ± std across the pooled (instance, rep) grid.",
        "",
        "| Policy | Total cost (CU) | Verification cost | Decision cost | Incorrect reuse rate | Escalation rate | Decision days |",
        "|---|---|---|---|---|---|---|",
    ]
    for p in POLICY_ORDER:
        row = df[df["policy"] == p]
        md_lines.append(
            f"| {POLICY_LABEL[p]} | {_mean_std(row['total_cost'])} "
            f"| {_mean_std(row['verification_cost'])} "
            f"| {_mean_std(row['decision_cost'])} "
            f"| {row['incorrect_reuse_rate'].mean():.3f} ± {row['incorrect_reuse_rate'].std():.3f} "
            f"| {row['escalation_rate'].mean():.3f} ± {row['escalation_rate'].std():.3f} "
            f"| {row['decision_days'].mean():.2f} |")
    (RESULTS_DIR / "results_table.md").write_text("\n".join(md_lines),
                                                  encoding="utf-8")

    # Frontier figure (verification cost vs incorrect reuse rate)
    fig, ax = plt.subplots(figsize=(5.5, 4.0))
    markers = {"proposed": "o", "B1": "s", "B3": "D", "B4": "^", "B5": "v"}
    for p in POLICY_ORDER:
        row = df[df["policy"] == p]
        x = row["verification_cost"].mean()
        y = row["incorrect_reuse_rate"].mean()
        xerr = row["verification_cost"].std() / np.sqrt(len(row))
        yerr = row["incorrect_reuse_rate"].std() / np.sqrt(len(row))
        ax.errorbar(x, y, xerr=xerr, yerr=yerr, marker=markers[p], ms=9,
                    linestyle="None", capsize=3, label=POLICY_LABEL[p])
    ax.set_xlabel("Verification cost (CU, mean)")
    ax.set_ylabel("Incorrect knowledge reuse rate (mean)")
    ax.set_title("Cost vs. incorrect reuse frontier, S1, 5-station line")
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend(loc="best", frameon=True, fontsize=8)
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "figure_cost_vs_incorrect_reuse.png", dpi=150)
    plt.close(fig)

    print("wrote results_table.csv, results_table.md, figure_cost_vs_incorrect_reuse.png")
    print("\nSummary:")
    print(agg.round(2).to_string())


if __name__ == "__main__":
    main()
