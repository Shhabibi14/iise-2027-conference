# Results: S1 (equipment upgrade), 5-station line

N_INSTANCES = 50, N_REPS = 10, total runs = 2500.
Numbers are mean ± std across the pooled (instance, rep) grid.

| Policy | Total cost (CU) | Verification cost | Decision cost | Incorrect reuse rate | Escalation rate | Decision days |
|---|---|---|---|---|---|---|
| Proposed | 406.8 ± 101.9 | 326.8 ± 100.0 | 80.0 ± 40.8 | 0.016 ± 0.045 | 0.522 ± 0.261 | 9.89 |
| B1 Full revalidation | 604.5 ± 49.1 | 500.0 ± 0.0 | 104.5 ± 49.1 | 0.030 ± 0.066 | 0.639 ± 0.237 | 2.00 |
| B3 No sharing | 247.6 ± 61.1 | 217.1 ± 60.2 | 30.6 ± 44.9 | 0.016 ± 0.049 | 0.089 ± 0.122 | 10.00 |
| B4 Random | 591.8 ± 53.6 | 482.9 ± 26.2 | 108.9 ± 45.4 | 0.028 ± 0.060 | 0.694 ± 0.217 | 9.62 |
| B5 Max uncertainty | 251.3 ± 65.1 | 120.0 ± 0.0 | 131.3 ± 65.1 | 0.061 ± 0.099 | 0.631 ± 0.242 | 10.00 |