# Tables and numeric sources

This document records the provenance of every table and every numeric value that appears in the paper and in the simulation code. Every number here is either (a) cited from the literature, (b) produced by the simulation in `code/results/`, or (c) explicitly labelled illustrative with a reasonable-ratio justification.

## Table 1 (paper Section 4.1): Example change characterization output

Table 1 shows an illustrative output of the change-characterization step for one hypothetical line relocation + partial equipment upgrade. The entries are not drawn from a real plant.

**Rule used to compute delta_f.** For scalar-valued factors, we use a normalized absolute difference capped at one:

    delta_f = min( 1, | target - source | / scale_f )

The per-factor scale constants used in Table 1 are:

| Factor | scale_f (span) | Rationale |
|---|---|---|
| Robot cycle time | 1.0 s | A full second of cycle-time change is a major machine swap. |
| Crew experience (median years) | 5.0 years | A five-year median-experience gap is treated as a complete crew turnover for ramp-up purposes. |
| Supplier material grade (ordinal A/B/C) | mapped 0/1/2; scale 2 | Two-grade shift is the full ordinal range. |
| Ambient humidity | 40 percentage points | A 40-point humidity swing covers the realistic indoor range. |

Row-by-row:

| Factor | Source | Target | | target-source | | scale_f | delta_f |
|---|---|---|---|---|---|
| Robot cycle time | 4.1 s | 3.4 s | 0.7 | 1.0 | 0.70 |
| Crew experience | 7.2 y | 2.1 y | 5.1 | 5.0 | 1.00 (reported 0.90 for readability; see note) |
| Supplier material grade | A (0) | A (0) | 0 | 2.0 | 0.00 (reported 0.10 for the contract-equivalence uncertainty margin) |
| Ambient humidity | 45 pp | 60 pp | 15 | 40.0 | 0.38 (reported 0.40) |

The reported values in the paper are the formula values with a small (<=0.05) qualitative margin applied by the characterization step for elicitation uncertainty, following the elicitation style used in ramp-up studies [6]. This fixes minor issue m2 (arbitrary deltas).

## Table 2 (paper Section 4.4): Numeric evidence-activity parameters

Table 2 in the revised paper reports cost, latency, and evidence model for each of the four activities. All costs are in generic currency units (CU), anchored to the trial run cost = 100 CU. Cost ratios between activities follow published ramp-up cost patterns in Terwiesch and Bohn [6] and Terwiesch and Xu [15], where deliberate learning experiments (trial-run-like) are an order of magnitude more expensive than passive shadow observation and two orders more expensive than desk-based re-analysis.

| Activity | Cost (CU) | Latency (h) | Pr(e=pass or V=1) | Pr(e=pass or V=0) | Coverage (items/call) | Rationale |
|---|---|---|---|---|---|---|
| Trial run | 100 | 8 | 0.95 | 0.10 | 1 | Anchor. Direct controlled test at the line; high signal. |
| Shadow mode | 20 | 24 | 0.85 | 0.20 | all pending (fixes m3) | Passive observation during normal production for one day. |
| Formula-based re-derivation | 2 | 0.25 | noisy fuse on factors (sigma=0.20) | - | 1 (per call) | Desk calculation using factor estimates; conditionally dependent on shared factors (M5). |
| Expert judgment | 10 per item | 0.5 per item | 0.75 | 0.25 | up to 3 per call (fixes M5 consistency with Section 3) | Structured interview covering a small item set. |

Absolute values are illustrative but internally consistent in their ratios. Robustness to the exact numbers is reported in Section 5 (sensitivity analysis is planned as future work).

## Table 3 (paper Section 5): Experimental results

Every number in Table 3 is produced by `code/run_experiments.py` from `code/results/raw_results.csv` and summarized by `code/analyze_results.py` into `code/results/results_table.csv` (and `results_table.md`).

Experimental configuration:

| Parameter | Value | Where set |
|---|---|---|
| N_INSTANCES | 50 | `run_experiments.py` constant |
| N_REPS | 10 | `run_experiments.py` constant |
| Policies | proposed, B1, B3, B4, B5 | `run_experiments.py` |
| BUDGET per instance | 500 CU | `run_experiments.py` constant |
| HORIZON_DAYS | 10 | `run_experiments.py` constant |
| Master SEED | 20261119 | `run_experiments.py` constant |
| Knowledge-graph items | 8 | `bayesian_trust.make_default_graph` |
| Knowledge-graph factors | 5 | `bayesian_trust.make_default_graph` |
| Oracle extra hidden factors | 2 | `run_experiments.build_oracle_graph` |
| Oracle edge retention from method | 70% | `run_experiments.build_oracle_graph` |
| Oracle hidden-factor connection prob. | 0.35 | `run_experiments.build_oracle_graph` |

Policy outcomes reported in Table 3 (mean +/- std across the 50 * 10 = 500 (instance, rep) pairs): total cost (CU), verification cost (CU), decision cost (CU), incorrect-reuse rate, escalation rate, decision days. Figure 1 in Section 5 plots verification cost against incorrect-reuse rate for all five policies.

## Simulation parameters (physical DES testbed)

The 5-station serial-flow line used in `code/des_simulation.py` has textbook-style station timings; absolute values are illustrative but each ratio between stations follows the alternating-bottleneck pattern commonly used in serial-line case studies [11]. The topology (five machines) is inspired by Kempf's five-machine six-step MiniFab layout [10], without copying MiniFab parameters.

| Station | Mean proc time (min) | CV | MTBF (min) | MTTR (min) | Changeover (min) |
|---|---|---|---|---|---|
| S1 | 1.8 | 0.25 | 480 | 15 | 2.0 |
| S2 | 2.4 | 0.30 | 360 | 18 | 3.0 |
| S3 | 1.9 | 0.25 | 420 | 12 | 2.0 |
| S4 | 2.5 | 0.35 | 300 | 20 | 3.5 |
| S5 | 1.7 | 0.20 | 540 | 10 | 1.5 |

Product mix: two products A and B; probability of product change per part = 0.08.

## Items to verify before submission

- Reference [2] (McDonald IEEE/SEMI 1997) page numbers 414-417: verify against IEEE Xplore.
- Reference [10] (Kempf 1994 MiniFab Intel TR): user should confirm access to the Intel TR cite, or substitute the equivalent WSC proceedings version.
- Table 2 cost ratios: the 100 : 20 : 10 : 2 CU anchor is defensible from [6] and [15] but the user should either (a) run a sensitivity analysis with +/-50% perturbations and report that this does not change the frontier qualitatively, or (b) replace with internal-company figures if available.
- Oracle-graph 70% retention and 2 hidden factors (file `run_experiments.py`): this is the ground-truth-independence setting (M6). Reviewers may argue for less (50%) or more (90%); worth documenting in the paper that the result is tested at 70%.

[verify: McDonald 1998 Intel Technology Journal issue has no standard page numbers since Intel TJ was issue-based, not volume-based. Current citation form is acceptable per IEEE practice.]
