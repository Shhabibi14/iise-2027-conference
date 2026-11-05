# Conference Paper Review Tasks

## Round 1 (all 15 items DONE)

Items from first Claude AI review. All addressed.

| # | Priority | Item | Status |
|---|----------|------|--------|
| 1 | Must fix | TL false acceptance inflation — replaced with variance-reduction model | DONE |
| 2 | Must fix | Spread never tested under variance inflation — added §3.4 + fig6 | DONE |
| 3 | Must fix | Double-blind anonymization | DONE |
| 4 | Fix in text | IUT vs. Bonferroni — Berger [9] added | DONE |
| 5 | Fix in text | Condition (iii) inconsistency — acknowledged in limitations | DONE |
| 6 | Fix in text | Justify 1σ margin — tied to B-basis | DONE |
| 7 | Fix in text | Reframe "below 2%" result | DONE |
| 8 | Fix in text | Equivalence vs. non-inferiority terminology | DONE |
| 9 | Fix in text | Augment alpha-spending — acknowledged in limitations | DONE |
| 10 | Minor | TL threshold precision — grid expanded | DONE |
| 11 | Minor | Monte Carlo SE reported | DONE |
| 12 | Minor | Fig 3 regime boundaries corrected | DONE |
| 13 | Minor | Missing references added | DONE |
| 14 | Minor | Plateau explanation corrected | DONE |
| 15 | Admin | Co-author awareness confirmed | DONE |

## Round 2

Items from second Claude AI review. Numbers reproduced, round 1 fixes confirmed.

| # | Priority | Item | Status |
|---|----------|------|--------|
| 16 | Must fix | **TL model is miscalibrated interval** — Implemented calibrated TL (samples from reduced variance, standard CI) and overclaimed TL (full variance, artificially narrow CI). Updated simulation, fig3, fig5, §2.2, §3.2, abstract, §4, §5. Calibrated 2x: accept=0.92 at n=10, false_accept=1.5%. Overclaimed 2x: accept=0.80 at n=10, false_accept=5.5%. | DONE |
| 17 | Should do | **Drop-Bonferroni comparison** — Run at full α=0.05 (IUT). Reviewer says accept=0.85 at n=12 with 4.8% false acceptance. Add one line on Fig 1 or one sentence. Move IUT paragraph to Methods or Discussion. | TODO |
| 18 | Fix in text | **Ref [4] status** — Says "accepted" but revision may still be under review. Confirm actual status and update. | TODO |
| 19 | Fix in text | **FAA AC 33.15-3 scope** — Covers premium titanium rotating parts, not AM. Correct or qualify the citation in §1. | TODO |
| 20 | Fix in text | **Condition (iii) is chi-square, not F-test** — With σ_ref treated as known, it's a chi-square test. Also define the line between "decisive" and "marginal" exceedance. | TODO |
| 21 | Fix in text | **B-basis vs 10th percentile** — μ−1.282σ is the population 10th percentile, not the B-basis value (which is a 95% lower confidence bound on P10). Use "10th percentile" or qualify. | TODO |
| 22 | Fix in text | **Reference order** — [10] appears before [2] and [3] in text. Renumber in order of first citation. Add MMPDS next to CMH-17. | TODO |
| 23 | Minor | **Em dashes** — Five remain in §2.1, §3.1 (×2), §3.4, and Limitation 6. Replace with standard dashes or rephrase. | TODO |
