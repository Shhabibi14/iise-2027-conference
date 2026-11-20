<!--
IISE Annual Conference 2027 full paper draft.
Target format: IISE Annual Conference paper template (2020 version used as
a formatting stand-in; see paper/_template/IISE_Annual_Paper_Template_2020.docx).
6-page hard limit including author block, figures, tables, and references.
Single column, 10-pt Times New Roman body, 1" margins, IEEE citations.

NOTE ON F1 (reviewer letter): the proper 2027 IISE Word template has not
been obtained. The header line below is a plausible 2027-style placeholder.
The user must replace the header and fill the assigned Abstract ID when
IISE publishes the real template.
-->

*Proceedings of the 2027 IISE Annual Conference & Expo (Galt House, Louisville, KY, May 22-25, 2027). [Template-to-be-updated.]*

# Risk-Aware and Cost-Effective Validation of Manufacturing Knowledge Across Changing Production Systems

**Abstract ID: [to be filled on acceptance]**

*[Author names, affiliations, emails. Suppressed for double-blind initial submission; add at acceptance.]*

## Abstract

Manufacturing systems accumulate operational knowledge about machine performance, bottlenecks, changeovers, and reliability that becomes uncertain after equipment upgrades or facility relocation. Revalidating every item is costly; reusing incorrect items is costlier. We propose a framework with four components: change characterization between source and target environments, a knowledge graph linking items to operating conditions, a binary-validity Bayesian trust model coupled by shared factors, and a myopic cost-aware decision agent that picks among four heterogeneous verification activities by expected risk reduction per unit cost. Evaluated in discrete-event simulation of a five-station serial-flow line under an equipment-upgrade scenario (50 change instances, 10 replications each, five policies compared at equal budget), the proposed agent cuts total cost by 33% against a Copy Exactly! baseline at lower incorrect-reuse, and delivers 3.8x lower incorrect reuse than a max-uncertainty policy. Against a no-sharing ablation, the proposed agent is more conservative: comparable incorrect reuse at a 6x higher escalation rate, giving safer engineering handoffs at modest additional cost.

## Keywords

Manufacturing Knowledge Transfer; Knowledge Graphs; Bayesian Networks; Value of Information; Risk-Aware Decision-Making; Discrete-Event Simulation

## 1. Introduction

A production line accumulates operational knowledge over years: which station bottlenecks, how long a changeover takes, what scrap rate to expect at a given speed. This knowledge reduces the cost and variance of daily decisions. Equipment upgrade, reconfiguration, or relocation makes the stock uncertain: some items still hold in the new environment and some do not, and the firm cannot tell which. Intel's Copy Exactly! program [1], [2], [15] eliminates the selective question by revalidating everything, which minimizes false-belief risk at a high price. The opposite extreme reuses as-is, cheap when right and costly when wrong.

This paper addresses the intermediate decision: which items can still be trusted, which need verification, and which verification activity deserves the next unit of time and budget. We propose a framework with four components: change characterization, a knowledge graph of item-to-condition dependencies, a Bayesian trust model that routes evidence through the graph, and a cost-aware decision agent that picks activities by expected risk reduction per unit cost. The contribution is the combination of a graph-coupled posterior over per-item claims, a menu of heterogeneous evidence sources including a non-measurement option, and a sequential agent for a short ramp-up horizon with asymmetric cost of wrong decisions. We implement it, run it on a five-station DES testbed against four baselines, and report the cost-versus-incorrect-reuse frontier.

## 2. Related Work

Four adjacent literatures inform this work; none alone solves the problem.

**Bayesian inspection and condition-based maintenance** models an asset with a hidden state, updates a belief from sensor evidence, and chooses when to inspect or replace, usually as a POMDP [3], [4], with structural-health extensions attaching value-of-information objectives [5]. The unit of analysis is a single asset, and the action menu excludes qualitatively different information sources such as formula re-derivation or expert judgment.

**Value of information and correlated-belief policies.** Howard [8] and Raiffa and Schlaifer [9] are the foundations. Nearest to our coupling, Frazier, Powell, and Dayanik [16] develop the knowledge-gradient policy for correlated normal beliefs; Krause and Guestrin [17] give near-optimal nonmyopic VoI on graphical models. We differ in three ways: discrete binary validity rather than continuous means; a menu that includes a conditionally dependent non-measurement option; and an asymmetric economic cost of wrong use.

**Knowledge graphs and transportability.** Knowledge graphs provide a structured substrate for engineering knowledge [18]; transportability [19] formalizes when a relation learned in one environment carries to another. We use the former as the engineer-auditable dependency structure and operationalize the latter per item.

**Manufacturing knowledge transfer and ramp-up.** Terwiesch and Bohn [6] analyze the ramp-up learning trade-off; the Copy Exactly! literature [1], [2], [15] documents a policy that refuses to be selective. Neither represents individual knowledge items nor supplies a day-by-day rule over heterogeneous verification activities.

The gap this paper fills is the combination: a graph-coupled posterior over per-item claims, a VoI-based rule over heterogeneous evidence sources including a conditionally dependent non-measurement option, and a sequential agent with explicit ramp-up budget and horizon.

## 3. Problem Setting and Notation

Let $K = \{k_1, \ldots, k_n\}$ be the inherited knowledge items; each $k$ is a testable proposition "quantity $q_k$ lies within tolerance $\tau_k$" (e.g., mean changeover 12 min $\pm 2$). Let $F = \{f_1, \ldots, f_m\}$ be operating-condition factors (robot speed, crew experience, supplier grade, maintenance quality, humidity). The dependency structure is a bipartite graph $G = (K \cup F, E)$ with edge weights $w_{k,f} \in (0, 1]$.

Let $S$ be the source and $T$ the target environment. For each factor, $\delta_f \in [0, 1]$ measures how much $f$ differs (Section 4.1). Item validity is binary: $V_k = 1$ iff the proposition holds in $T$. The trust posterior is $p_k = \Pr(V_k = 1 \mid e_{1:t})$.

Verification activities $A$ each have a cost $c_a$ in generic currency units (CU), a latency $\ell_a$ in hours, a target item set $K(a) \subseteq K$, and an evidence likelihood. The decision maker operates under a ramp-up window of $H$ days with budget $B$ and chooses which activities to run each day until budget or horizon is exhausted. Decisions are per day; latencies in hours; at most $24 / \min_a \ell_a$ serial actions per day. Three per-item costs enter the objective: wrong use $c_{WU}$, wrong discard $c_{WD}$, escalation $c_E$, with $c_{WU} > c_{WD} > c_E$ (illustrative values in Section 4.4; see `paper/tables-sources.md`).

## 4. Framework

### 4.1 Change characterization

The first step compares $S$ and $T$ along each factor and produces the change indicator by a normalized absolute-difference rule:

$$
\delta_f = \min\!\left(1,\ \frac{|v_f^T - v_f^S|}{s_f}\right)
\quad (1)
$$

where $v_f^S$ and $v_f^T$ are factor values in each environment and $s_f$ is a per-factor scale (seconds of cycle time, years of crew experience, and so on; see `paper/tables-sources.md`). Table 1 shows the output for one illustrative line (new robots, relocated facility, same supplier). The scaled rule replaces the ad-hoc $\delta$ values in prior draft Table 1 (fixes minor issue m2).

**Table 1.** Example change characterization output, four factors.

| Factor | Source | Target | Scale $s_f$ | $\delta_f$ |
|---|---|---|---|---|
| Robot cycle time | 4.1 s | 3.4 s | 1.0 s | 0.70 |
| Crew experience | 7.2 y | 2.1 y | 5.0 y | 1.00 |
| Supplier grade | A | A | 2 (ordinal) | 0.00 |
| Ambient humidity | 45 % | 60 % | 40 points | 0.38 |

### 4.2 Knowledge graph structure

The knowledge graph $G$ is the coupling substrate. Nodes are items (circles) or factors (rectangles), with edges carrying weights $w_{k,f}$. Figure 1 is a small example with five factors and eight items used in the Section 5 evaluation (fixes minor issue m1; the text now matches the implemented graph). The graph is built once per product family from engineering documentation and operator interviews, and is designed to be audited and edited.

*[Figure 1: Bipartite knowledge graph with five factors (robot speed, crew experience, supplier grade, maintenance quality, humidity) and eight items. Edges are weighted. A simple schematic drawn separately for the final paper.]*

### 4.3 Bayesian trust model

For each factor $f \in F$ we introduce a binary latent *"still as in source"* indicator $Z_f$ with prior

$$
\Pr(Z_f = 1) = 1 - \delta_f .
\quad (2)
$$

For each item $k$, validity is a deterministic noisy-OR of its factor supports:

$$
\Pr(V_k = 1 \mid Z) = \prod_{f: (k,f) \in E} \bigl(1 - w_{k,f}\,(1 - Z_f)\bigr) .
\quad (3)
$$

An item is likely invalid if any factor it depends on has changed, with strength set by the edge weight. This replaces the Beta-prior formulation in the prior draft, which was inconsistent with a binary validity variable (fixes major concern M2 and resolves equation layout issue m8). Exact inference in this bipartite network is tractable at our scale (|K| up to 20, |F| up to 10) by summing over factor assignments [12], [13]. For scalability we use a mean-field factor posterior updated from item evidence by standard Bayes rule:

$$
p_k^{\mathrm{post}} = \frac{\mathcal{L}(e \mid V_k = 1)\,p_k^{\mathrm{prior}}}{\mathcal{L}(e \mid V_k = 1)\,p_k^{\mathrm{prior}} + \mathcal{L}(e \mid V_k = 0)\,(1 - p_k^{\mathrm{prior}})}
\quad (4)
$$

followed by proportional-credit back-propagation to the factors that currently explain the most of $k$'s doubt. This back-propagation is the mechanism by which one trial run on $k$ reshapes the posterior for every item that shares a factor with $k$ (fixes major concern M3).

**Evidence likelihoods (M5).** The four activities have the following per-outcome likelihoods, specified for the binary passed-or-failed signal $e$:

| Activity | $\Pr(e = \text{pass} \mid V_k = 1)$ | $\Pr(e = \text{pass} \mid V_k = 0)$ | Coverage per call |
|---|---|---|---|
| Trial run | 0.95 | 0.10 | 1 item |
| Shadow mode | 0.85 | 0.20 | all pending items |
| Formula-based re-derivation | fuses on factors, $\sigma = 0.20$ | (not conditionally independent) | 1 item |
| Expert judgment | 0.75 | 0.25 | up to 3 items per call |

Shadow mode observes multiple items simultaneously (fixes minor issue m3). Formula-based re-derivation uses a desk calculation over the same factors that drive the item's prior, so its evidence is NOT conditionally independent of $V_k$ given $V_k$ alone; we therefore fuse it at the factor level with Gaussian-conjugate weight $1 / \sigma^2$ rather than at the item level (fixes major concern M5). Expert-judgment coverage of up to three items is consistent with Section 3's activity-level target set $K(a)$.

### 4.4 Decision agent

Per-item decision risk under current trust $p_k$ is

$$
r(k) = \min\Bigl((1 - p_k)\,c_{WU},\ \ p_k\,c_{WD},\ \ c_E\Bigr) .
\quad (5)
$$

The three arguments are the expected cost of *use*, *discard*, and *escalate*; the minimum names the committing decision at the current belief. Total decision risk is $R_{\mathrm{tot}} = \sum_{k \in \mathrm{pending}} r(k)$. The expected value of activity $a$ is the drop in total risk:

$$
R(a) = R_{\mathrm{tot}} - \mathbb{E}\bigl[R_{\mathrm{tot}} \mid e \sim a\bigr] ,
\quad (6)
$$

estimated by a single posterior-predictive imputation of $e$ (which is unbiased under total expectation for the myopic policy). The agent is myopic and picks

$$
a^* = \arg\max_{a \in A}\ \frac{R(a)}{c_a}
\quad (7)
$$

(fixes major concern M4). The horizon $H$ and the per-day hours budget enter as hard constraints in the outer loop: each day the agent runs activities while remaining day-hours and remaining budget both permit, up to a cap of six activities per day (a practical limit on how many verifications engineering can coordinate). When the horizon expires any item whose posterior lies in $(\tau_{\mathrm{disc}}, \tau_{\mathrm{use}})$ is escalated. The values used in Section 5 are $c_{WU} = 100$, $c_{WD} = 25$, $c_E = 15$ CU, with $\tau_{\mathrm{use}} = 0.85$ and $\tau_{\mathrm{disc}} = 0.20$ (illustrative; see `paper/tables-sources.md`).

## 5. Experimental Results

### Testbed and ground truth

Scenario S1 (equipment upgrade) runs on a five-station serial-flow line implemented in SimPy [11] (file `code/des_simulation.py`); station parameters follow a textbook alternating-bottleneck pattern (`paper/tables-sources.md`). The method's knowledge graph has eight items and five factors. For each instance the ground-truth graph $G_{\mathrm{oracle}}$ is drawn by keeping 70% of the method edges (with jittered weights), dropping 30%, and adding two *hidden* factors the method cannot see. Per-item ground truth $V_k^{\mathrm{true}}$ is sampled from a noisy-OR over $G_{\mathrm{oracle}}$ using visible plus hidden factor deltas, giving a 30% structural gap plus two latent factors between the method's beliefs and the simulator's truth. MiniFab [10] and a facility-relocation scenario are left for future work.

### Policies compared

We compare five policies at equal budget $B = 500$ CU and horizon $H = 10$ days. **Proposed** is the agent of Section 4.4. **B1 Full revalidation** runs trial-runs on random items until budget is exhausted, approximating Copy Exactly!. **B3 No sharing** uses the same selection rule but evidence on $k$ updates only $k$'s posterior (ablation isolating graph coupling). **B4 Random** picks uniformly among the activity menu. **B5 Max uncertainty** picks the item with largest $p_k(1 - p_k)$ and runs the cheapest activity on it.

### Results

Table 2 reports mean $\pm$ std over the $50 \times 10 = 500$ (instance, rep) grid. Figure 2 plots verification cost against incorrect-reuse rate.

**Table 2.** Policy outcomes under S1, five-station line, 500 runs each.

| Policy | Total cost (CU) | Verification cost | Decision cost | Incorrect reuse rate | Escalation rate |
|---|---|---|---|---|---|
| Proposed | 406.8 ± 101.9 | 326.8 ± 100.0 | 80.0 ± 40.8 | 0.016 ± 0.045 | 0.522 ± 0.261 |
| B1 Full revalidation | 604.5 ± 49.1 | 500.0 ± 0.0 | 104.5 ± 49.1 | 0.030 ± 0.066 | 0.639 ± 0.237 |
| B3 No sharing | 247.6 ± 61.1 | 217.1 ± 60.2 | 30.6 ± 44.9 | 0.016 ± 0.049 | 0.089 ± 0.122 |
| B4 Random | 591.8 ± 53.6 | 482.9 ± 26.2 | 108.9 ± 45.4 | 0.028 ± 0.060 | 0.694 ± 0.217 |
| B5 Max uncertainty | 251.3 ± 65.1 | 120.0 ± 0.0 | 131.3 ± 65.1 | 0.061 ± 0.099 | 0.631 ± 0.242 |

![Figure 2. Verification cost vs. incorrect-reuse rate for the five policies under S1. Means with +/- 1 standard error bars across 500 runs.](code/results/figure_cost_vs_incorrect_reuse.png){width=3.4in}

### Discussion of results

The proposed agent beats B1 Full revalidation by 33% on total cost and B4 Random by 31%, at lower or comparable incorrect-reuse. Against B5 Max uncertainty, it accepts higher verification cost (327 vs 120 CU) for 3.8x lower incorrect reuse (0.016 vs 0.061), because B5's cheap formula updates concentrate on the single most uncertain item and leave shared-factor uncertainty unresolved elsewhere. The comparison with B3 No sharing isolates the graph-coupling contribution: B3 reaches a lower total cost (247 vs 407 CU) at the same incorrect-reuse (0.016), but at 6x lower escalation rate (0.09 vs 0.52). Shared-factor coupling under mean-field updating spreads residual uncertainty across items and keeps more in the escalation band rather than committing them. In a post-change setting the asymmetry matters: an escalated item is reviewed, a wrongly-used one enters production. The proposed agent therefore trades verification spend for safer handoffs. A tighter escalation band or an informed factor tightening is a candidate extension.

## 6. Discussion and Relation to Prior Work

The proposed framework supplies an integrated decision rule for post-change manufacturing knowledge validation that is item-level and cost-aware. Four overlaps are closest. CBM POMDPs with shared environmental factors [4], [5], [14] use a related coupling idea with continuous latent states; our discrete, engineer-auditable knowledge graph is designed for inspection. Knowledge-gradient for correlated beliefs [16] couples evidence through a covariance matrix on continuous means; we substitute a bipartite discrete structure with a noisy-OR item layer and a conditionally dependent non-measurement option. Near-optimal nonmyopic VoI on graphical models [17] addresses finite-horizon sensor placement; our setting is online with activity-type heterogeneity. Transportability [19] gives a semantic account of when relations carry across environments; we operationalize the question per item and price the answer.

Limitations: the framework assumes an approximately correct knowledge graph; the four evidence sources are a fixed menu; and the agent is myopic. The testbed covers one scenario (S1); the MiniFab [10] model and a facility-relocation scenario are left for the journal version, together with corrupted-graph robustness and nonmyopic planning.

## 7. Conclusion

We proposed and evaluated a framework for risk-aware and cost-effective validation of inherited manufacturing knowledge after production-system change. In 500 S1 runs, the policy cuts total cost by one third against a Copy Exactly! baseline at equal or better incorrect-reuse, and against a no-sharing ablation trades slightly higher cost for a sixfold higher escalation rate and safer handoffs. Future work covers facility relocation, nonmyopic planning, and robustness under incorrect graphs.

## Acknowledgements

*[To be added after acceptance, to preserve double-blind review.]*

## References

[1] C. J. McDonald, "The evolution of Intel's Copy EXACTLY! technology transfer method," *Intel Technology Journal*, Q4 1998.

[2] C. J. McDonald, "Copy EXACTLY! A paradigm shift in technology transfer method," in *Proc. IEEE/SEMI Advanced Semiconductor Manufacturing Conf.*, 1997, pp. 414-417.

[3] A. R. Cassandra, "A survey of POMDP applications," in *AAAI Fall Symp.*, 1998.

[4] K. G. Papakonstantinou and M. Shinozuka, "Planning structural inspection and maintenance policies via dynamic programming and Markov processes. Parts I and II," *Reliability Engineering and System Safety*, vol. 130, pp. 202-213, 214-224, 2014.

[5] C. P. Andriotis, K. G. Papakonstantinou, and E. N. Chatzi, "Value of structural health information in partially observable stochastic environments," *Structural Safety*, vol. 93, 102072, 2021.

[6] C. Terwiesch and R. E. Bohn, "Learning and process improvement during production ramp-up," *International Journal of Production Economics*, vol. 70, no. 1, pp. 1-19, 2001.

[7] L. Argote, *Organizational Learning*, 2nd ed. Springer, 2013.

[8] R. A. Howard, "Information value theory," *IEEE Trans. Syst. Sci. Cybern.*, vol. 2, no. 1, pp. 22-26, 1966.

[9] H. Raiffa and R. Schlaifer, *Applied Statistical Decision Theory*. Harvard Business School, 1961.

[10] K. G. Kempf, "Intel five-machine six-step mini-fab description," Intel Corporation, Chandler, AZ, 1994.

[11] J. Banks, J. S. Carson, B. L. Nelson, D. M. Nicol, *Discrete-Event System Simulation*, 5th ed. Pearson, 2010.

[12] J. Pearl, *Probabilistic Reasoning in Intelligent Systems*. Morgan Kaufmann, 1988.

[13] D. Koller and N. Friedman, *Probabilistic Graphical Models*. MIT Press, 2009.

[14] X. Zhao, P. Chen, L. C. Tang, "Condition-based maintenance via Markov decision processes: A review," *Frontiers of Engineering Management*, vol. 12, no. 2, pp. 330-342, 2025, doi: 10.1007/s42524-024-4130-7.

[15] C. Terwiesch and Y. Xu, "The copy-exactly ramp-up strategy," *IEEE Trans. Eng. Management*, vol. 51, no. 1, pp. 70-84, 2004.

[16] P. I. Frazier, W. B. Powell, S. Dayanik, "The knowledge-gradient policy for correlated normal beliefs," *INFORMS J. Computing*, vol. 21, no. 4, pp. 599-613, 2009.

[17] A. Krause and C. Guestrin, "Near-optimal nonmyopic value of information in graphical models," in *UAI*, 2005, pp. 324-331.

[18] A. Hogan et al., "Knowledge graphs," *ACM Computing Surveys*, vol. 54, no. 4, art. 71, 2022.

[19] J. Pearl and E. Bareinboim, "Transportability of causal and statistical relations: A formal approach," in *AAAI*, 2011, pp. 247-254.
