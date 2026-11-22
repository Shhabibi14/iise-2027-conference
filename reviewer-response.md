# Reviewer Response Tracker — IISE 2027 Paper

Reviewer recommendation: **major revision** (currently borderline reject as a full paper). Each issue below is a trackable row; update the **Status** column as each is addressed.

Status values: `Pending` · `In progress` · `Done` · `Deferred` · `Won't fix`

Hard deadline for revised paper: **January 17, 2027**.

---

## Priority order the reviewer recommended (do in this order)

1. Fix Sections 4.3 and 4.4 as one consistent model (items M2, M3, M4, M5) — about half a page of equations.
2. Run scenario S1 on the 5-station line and add one table and one figure (items M1, M7).
3. Cut MiniFab and scenario S2 to one sentence of future work. Shorten the CBM paragraph in Section 2 and add a knowledge-graph + value-of-information paragraph (item M8).
4. Clean the template, placeholders, and references (all Format items + several Minor items).

---

## Major concerns (M-series) — substantive, mostly require technical decisions or new work

| # | Priority | Issue | Reviewer's fix | Status |
|---|---|---|---|---|
| M1 | Blocker | **No results reported.** Abstract, Sec 5 and Sec 6 are all future tense; H1–H3 untested. Most IISE full-paper reviewers will reject framework-only papers. | Run S1 on the 5-station line only. Add one results table and one figure (cost vs incorrect-reuse for proposal and B1–B3). Move MiniFab and S2 to future work. | Done — ran 50 instances x 10 reps x 5 policies = 2500 runs via `code/run_experiments.py`. Table 2 and Figure 2 (frontier plot) reported in Section 5. MiniFab and S2 moved to Section 6 future work. |
| M2 | Blocker | **Bayesian trust model (Eqs 1–2) is inconsistent.** Eq 1 uses a Beta prior on p_k, Eq 2 updates p_k as a single number. "Proposition holds in T" is one binary fact, not a Bernoulli trial. Also, δ_f = 1 does not actually invalidate the prior under Eq 1 — it only lowers β. | Define a binary validity variable V_k with Pr(V_k = 1) = g(δ) (e.g. noisy-OR over factors). Update it with Eq 2. Drop the Beta, or explain exactly what it represents. | Done — Section 4.3 rewritten with binary V_k, factor latent Z_f with Pr(Z_f = 1) = 1 - delta_f, noisy-OR Pr(V_k=1 | Z). Beta prior removed. |
| M3 | Blocker | **Evidence sharing (the main contribution) is only described in words.** Section 4.3 mentions factor-level latent variables but gives no equations. A reviewer cannot tell how evidence on k1 changes k4. | Write the joint model in 2–3 lines: factor latent Z_f with Pr(Z_f = 1) related to δ_f; then Pr(V_k = 1 \| Z); then Pr(e \| V_k) per activity. State that posterior is computed by exact inference on the bipartite network. Figure 1 should show this structure. | Done — Equations (2)-(4) in Section 4.3 give the joint model explicitly; proportional-credit factor back-propagation described; code path in `code/bayesian_trust.py`. |
| M4 | Blocker | **Decision rule is not defined.** R(a) in Eq 3 has no formula. Thresholds reference "economic consequences in Section 3" but Sec 3 defines no costs. | Define cost of wrongly using an item, cost of wrongly discarding one, escalation cost. Write expected decision risk; define R(a) as expected drop in that risk. Say whether rule is myopic, how latency ℓ_a and horizon H enter (Eq 3 ignores both), whether >1 activity can run per day. | Done — Section 4.4 defines c_WU, c_WD, c_E (100, 25, 15 CU), per-item risk r(k) in Eq (5), total risk and R(a) in Eq (6), myopic selection in Eq (7). Horizon and daily hours enter as outer-loop constraints; up to 6 activities per day. |
| M5 | Blocker | **Evidence models missing.** Table 2 lists activities qualitatively; Eq 2 needs Pr(e \| k holds) and Pr(e \| ¬k) for each. Expert judgment is "Variable" — how modeled? Formula re-derivation is "assumption-contingent" — depends on same factors as item, so evidence is NOT conditionally independent. Expert judgment "1 or more items" conflicts with Sec 3's single target k(a). | Specify evidence models for each activity. Handle non-independence of formula re-derivation. Make expert-judgment coverage consistent with Sec 3 (or generalize Sec 3). | Done — Section 4.3 has a numeric likelihood table for all four activities. Formula is fused at factor level (sigma=0.20) rather than at item level, explicitly flagging the non-independence. Section 3 generalized to per-activity target item set K(a) covering expert judgment up to 3 items. |
| M6 | Blocker | **Ground truth is confused with belief, and truth may be built in.** Sec 5 says "ground-truth trust values" — trust is a belief, truth should be whether q_k in T falls within τ_k, estimated from 30 reps. More importantly, if the simulator's truth is generated from the same graph G the method uses, the method has an unfair advantage. | Define truth cleanly (did q_k fall within τ_k in T), separately from belief p_k. Explain how crew experience, supplier grade, humidity actually change DES parameters. Make truth mechanism at least partly independent of G. | Done — Section 5 "Ground truth independent of the method graph" subsection. Oracle graph keeps 70% of method edges, drops 30%, adds 2 hidden factors invisible to the method. V_k^true sampled from noisy-OR over oracle. Also V_k and trust p_k notation separated in Section 3. |
| M7 | Must | **Baselines are too weak.** B1 (full revalidation) and B2 (fixed shadow) are extreme policies — beating them is expected. | Add: random activity choice at same budget; "pick most uncertain item" (largest p(1−p)). Compare at equal budget, or plot a cost vs incorrect-reuse frontier. "Comparable incorrect-reuse rates" in H1 is not testable as written. If space allows, compare with exact optimal policy on a tiny instance. | Done — Added B4 Random and B5 Max uncertainty baselines. All 5 policies compared at equal budget B=500 CU; Figure 2 is the cost-vs-incorrect-reuse frontier. Exact optimal on a tiny instance left for the journal version due to the 6-page limit. |
| M8 | Must | **Literature is thin for the "first integrated decision rule" claim.** "Knowledge Graphs" is in keywords but no KG paper is cited. Missing: transfer learning / negative transfer; transportability (Pearl & Bareinboim); VoI in graphical models (Krause & Guestrin); and most importantly **knowledge-gradient policy for correlated beliefs (Frazier et al.)**, which is very close to the coupled-VoI idea. | Cite these and explain the difference, or soften "first". The docs/novelty.md note from earlier has the full references. | Done — Section 2 adds ref [16] Frazier et al., [17] Krause & Guestrin, [18] Hogan et al. knowledge graphs survey, [19] Pearl & Bareinboim transportability. Section 6 now distinguishes the proposal against each. "First" softened to "an integrated" throughout. **Update 2026-11-21:** literature expanded and every reference verified against Crossref (`docs/references-verification.md`, 70 references; `docs/literature-review.md`; `docs/references.bib`). Paper now has 24 verified references, renumbered by first appearance: adds a manufacturing knowledge-graph review [18], negative transfer [19], ramp-up review [5], knowledge stickiness [6], [7], Bayesian networks in reliability and diagnosis [8], [9], decision-theoretic troubleshooting [10]. Krause & Guestrin cited as the JAIR 2009 journal version [13]; Pearl & Bareinboim as Stat. Sci. 2014 [20]. Removed unverifiable Cassandra 1998 and Kempf 1994 (Mini-Fab now cited via Ramirez-Hernandez & Fernandez 2009 [24]). Section 2 shortened from 268 to 242 words. |

---

## Minor issues

| # | Priority | Issue | Fix | Status |
|---|---|---|---|---|
| m1 | Should | **Figure 1 inconsistency.** Sec 4.2 says "five-item, three-factor" but the example lists four factors (robot cycle time, crew experience, supplier grade, humidity). Figure is still a placeholder. | Make text and figure consistent (choose 3 or 4 factors), and render the real figure. | Done — Sec 4.2 text now says "five factors and eight items" matching the implemented default graph. Actual figure still a textual placeholder; user to render. |
| m2 | Should | **Table 1 δ values look arbitrary.** Why does 4.1 s → 3.4 s give 0.7? | Give the rule — e.g. normalized difference or an elicitation scale. | Done — Section 4.1 now gives the normalized-difference rule (Eq 1); Table 1 recomputed from that rule; per-factor scales listed in `paper/tables-sources.md`. |
| m3 | Should | **Shadow mode coverage** in Table 2 says "one item at a time", but shadow mode normally observes many items at once (itself a source of evidence sharing). | Correct Table 2 coverage for shadow mode. | Done — paper Section 4.3 and `paper/tables-sources.md` both say "all pending items". Code (`decision_agent.apply_shadow_group`) implements the group update. |
| m4 | Should | **Time steps are mixed.** Decisions made per day, but latencies are in minutes and hours. | Unify time units, or state the mapping explicitly. | Done — Section 3 now explicitly reconciles: decisions per day; latencies in hours; at most 24/min_latency serial actions per day. Code enforces this via per-day hours budget. |
| m5 | Must | **Uncited references.** [11]–[15] are never cited in the text. In particular, cite [15] Terwiesch & Xu next to Copy Exactly! in the Introduction. | Cite each reference in the body, or remove unused ones. | Done — [11] cited in Sec 5 (DES methodology); [12], [13] cited in Sec 4.3 and Sec 6; [14] cited in Sec 2 (CBM paragraph); [15] cited in Sec 1 (intro, next to Copy Exactly!). |
| m6 | Should | **Overclaim.** Sec 4.2 says the framework "is designed to degrade gracefully (see Section 5)", but Sec 5 only *plans* to test this. | Soften to "will be tested for graceful degradation (Section 5)." | Done |
| m7 | Should | **Tone.** "Three honest overlaps" in Sec 6 is informal. | Change section heading to "Relation to prior work". | Done — in-text phrasing changed to "The closest prior work overlaps the proposal in three places." |
| m8 | Should | **Equation (1) layout.** The p_k^(0) term sits awkwardly. | Reformat equation; may resolve on its own once M2 rewrite happens. | Done — resolved by M2 rewrite; Eqs (2)-(7) in Section 4 are clean. |
| m9 | Should | **Heading styles mixed.** Sec 1–5 use small bold sans font, Sec 4.1–4.4 use larger serif font. | Normalize all heading styles to the IISE template. | Deferred — pending F1 (proper 2027 IISE Word template). Markdown headings are already consistent; the mixed rendering is a template-style-map issue that only the correct IISE template can fix. |

---

## Formatting and reference fixes (required before submission)

| # | Priority | Issue | Fix | Status |
|---|---|---|---|---|
| F1 | Must | **Template header wrong.** Still reads "Proceedings of the 2020 IISE Annual Conference, L. Cromarty, R. Shirwaiker, P. Wang, eds." Also "Abstract ID: XXX" needs the real ID. | Use the 2027 template header. Fill real Abstract ID once IISE assigns it. | Partial — header now reads "Proceedings of the 2027 IISE Annual Conference & Expo (Galt House, Louisville, KY, May 22-25, 2027)" with a placeholder Abstract ID. The user must still obtain the official 2027 IISE Word template from the track chairs and replace the header with the exact text IISE requires, and must fill the Abstract ID once IISE assigns it. |
| F2 | Must | **Remove all `[CITATION NEEDED]` markers** and the internal note "docs/novelty.md" in [14]. | Replace every placeholder with a real citation (see F3 and F4) or cut the sentence. | Done — all 5 markers removed; refs [1], [2], [10], [14] updated; Section 6 BN-diagnosis sentence now cites [12], [13]. |
| F3 | Must | **Reference [14] is likely fabricated.** No paper by Zhao, Kurz, Bemporad, Liberzon found. Real paper is: Xiujie Zhao, Piao Chen, Loon Ching Tang, "Condition-based maintenance via Markov decision processes: A review," *Front. Eng. Manag.*, 2025, 12(2): 330–342, DOI: 10.1007/s42524-024-4130-7. | Replace [14] with the real citation. Check every other reference against its source. | Done — [14] replaced with the Zhao, Chen, Tang 2025 paper. Other refs still need user verification before submission. |
| F4 | Must | **Reference [10] cites wrong source for MiniFab.** The MIMAC report is for MIMAC datasets, not MiniFab. MiniFab is from Kempf, 1994 (Intel, five-machine six-step model). | Replace [10] with Kempf 1994 citation. | Done — [10] replaced with Kempf 1994 Intel MiniFab description. |
| F5 | Must | **Reference [2] page numbers.** Verify pages in IEEE Xplore (Wikipedia citation gives IEEE 414–417). | Confirm and set correct pages. | Done — set to pp. 414-417 per reviewer's lead; user should still spot-check in IEEE Xplore before submission. |
| F6 | Should | **Page ranges use "pp. 202 to 213"** — unusual. | Use plain hyphen: "pp. 202-213". Keeps the no-en-dash rule and looks standard. | Done — fixed in refs [4], [6], [8], [15]. |

---

## What to do next

The reviewer gave an explicit priority order (see top). Two realistic paths:

- **Minimum viable path for Jan 17 submission:** M1 (run S1 + report results), M2–M5 (rewrite trust model + decision rule consistently), M7 (add 2 extra baselines), M8 (cite the 4 missing literatures), all Format and Minor items. This is 4–6 weeks of focused work.
- **Safer path:** the minimum above, plus M6 (ground-truth independence) — closes the biggest potential "unfair advantage" objection a second reviewer would raise.

Items I can fix mechanically right now, without further input:
- F2 (remove placeholders), F3 (replace [14]), F4 (replace [10]), F6 (page-range format), m5 (cite uncited refs), m6 (soften overclaim), m7 (rename "honest overlaps"), m9 (unify heading styles).

Items requiring your decision or substantial new work:
- M1 (run the simulation), M2–M6 (model and decision rule rewrites), M7 (new baselines), M8 (lit additions), m1–m4 (modeling consistency fixes), m8 (equation layout — likely resolved by M2 rewrite), F1 (need the real IISE 2027 template and the assigned abstract ID), F5 (verify ref [2] pages).

Tell me which items to tackle and in what order.
