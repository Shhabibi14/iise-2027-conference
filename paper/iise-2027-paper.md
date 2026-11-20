<!--
IISE Annual Conference 2027 full paper draft.
Target format: IISE Annual Conference paper template (2020 version used as
reference; see paper/_template/IISE_Annual_Paper_Template_2020.docx). 6-page
hard limit including author block, figures, tables, and references.
Single column, 10-pt Times New Roman body, 1" margins, IEEE citations.
-->

# Risk-Aware and Cost-Effective Validation of Manufacturing Knowledge Across Changing Production Systems

**Abstract ID: XXX**

*[Author names, affiliations, emails. Suppress for double-blind initial submission; add at acceptance.]*

## Abstract

Manufacturing systems accumulate valuable operational knowledge about machine performance, production bottlenecks, changeover times, and process reliability. Equipment upgrades, production reconfigurations, and facility relocation can make this knowledge unreliable. Revalidating every item is costly, while reusing incorrect knowledge produces poor operational decisions. We propose a framework that validates manufacturing knowledge after a production system change through four components: change characterization between source and target environments; a knowledge graph linking items to the operating conditions they depend on; a Bayesian trust model that updates per-item validity probabilities as evidence arrives; and a decision agent that selects verification activities by expected value of information, decision risk, and time and budget constraints. We will evaluate the framework in discrete-event simulation under equipment upgrade and facility relocation scenarios, comparing against full revalidation, fixed-duration monitoring, and validation without evidence sharing. Target measures include total decision and verification cost, incorrect knowledge reuse, and decision time.

## Keywords

Manufacturing Knowledge Transfer; Knowledge Graphs; Bayesian Networks; Value of Information; Risk-Aware Decision-Making; Discrete-Event Simulation

## 1. Introduction

A manufacturing line accumulates a stock of operational knowledge over years of production: which station bottlenecks, how long a changeover takes, what scrap rate to expect at a given line speed. This knowledge is codified in standard operating procedures or held tacitly by operators and engineers. It is a major asset because it reduces the cost and variance of daily decisions.

When the line is changed by equipment upgrade, reconfiguration, or relocation, the value of this stock becomes uncertain. Some items still hold in the new environment and some do not, and the firm cannot tell which. Industry practice falls into two extremes. Intel's Copy Exactly! program [1], [2], [15] copies every parameter and revalidates the full process, which minimizes false-belief risk but is expensive and often infeasible when the target is not identical. The opposite extreme reuses prior knowledge as-is, which is cheap when right and costly when wrong.

This paper addresses the intermediate decision: which items can still be trusted, which need verification, and which verification activity to spend the next unit of time and budget on. We propose a framework with four components: change characterization, a knowledge graph of item-to-condition dependencies, a Bayesian trust model that routes evidence through the graph, and a cost-aware decision agent that picks activities by expected risk reduction per unit cost. The contribution is the integration: a graph-structured posterior over per-item claims, a menu of heterogeneous evidence sources, and a sequential selection rule tailored to a short ramp-up horizon with asymmetric cost of wrong decisions.

## 2. Related Work

Three adjacent literatures inform this work; none individually solves the problem.

**Bayesian inspection and condition-based maintenance.** A long tradition models an asset with a hidden degradation state, updates a belief from sensor evidence, and chooses when to inspect, repair, or replace, often formalized as a partially observable Markov decision process (POMDP) [3], [4], [14]. Recent work extends this to structural health monitoring with value-of-information objectives [5]. The unit of analysis is a single asset or a small set of coupled assets, not a portfolio of testable knowledge items with heterogeneous tolerances, and the action space does not include qualitatively different information sources such as formula-based re-derivation or expert judgment.

**Manufacturing knowledge transfer and ramp-up.** Terwiesch and Bohn [6] analyze the ramp-up trade-off between short-run output and deliberate learning experiments. Argote [7] supplies the organizational-learning backbone on cross-plant transfer. The Copy Exactly! literature [1], [2] documents a policy that eliminates the selective-revalidation question by refusing to be selective. These works do not represent individual knowledge items or supply a day-by-day decision rule over heterogeneous verification activities.

**Value of information and Bayesian experimental design.** Howard [8] introduces the information-value framework; Raiffa and Schlaifer [9] and later work in medical, oil and gas, and structural health settings [5] apply it to inspection and testing. VoI is typically computed for one decision against a small set of quantities, assuming known-quality noisy observations. Our setting has many coupled items, a menu of qualitatively different evidence sources (including a non-measurement option), and a short horizon with asymmetric economic consequences of using a wrong item.

The gap this paper fills is the combination: a graph-coupled Bayesian posterior over per-item claims, a VoI-based selection rule over heterogeneous evidence sources, and a sequential agent tailored to production-system-change with explicit ramp-up budget and time constraints.

## 3. Problem Setting and Notation

Let $K = \{k_1, \ldots, k_n\}$ be the set of inherited knowledge items. Each item $k$ is a testable proposition of the form "quantity $q_k$ lies within tolerance $\tau_k$", for example "mean changeover time between products A and B is 12 minutes, within $\pm 2$ minutes." Let $F = \{f_1, \ldots, f_m\}$ be the set of named operating-condition factors on which items depend: machine reliability, crew experience, supplier material grade, ambient temperature, scheduling policy, and so on. The dependency structure is a bipartite graph $G = (K \cup F, E)$ with an edge $(k, f) \in E$ when the validity of $k$ depends on factor $f$.

Let $S$ denote the source production environment (where the items were learned) and $T$ the target environment (where they must be used). For each factor $f$, a *change indicator* $\delta_f \in [0, 1]$ measures how much $f$ differs between $S$ and $T$ (zero means unchanged, one means fully changed). For each item $k$, the *trust probability* $p_k = \Pr(k \text{ holds in } T \mid \text{evidence so far})$ is updated as evidence accumulates. Initially $p_k$ is driven by the change indicators on the factors $k$ depends on.

Let $A = \{a_1, \ldots, a_r\}$ be the set of verification activities. Each $a \in A$ has a cost $c_a$ (time plus money), a latency $\ell_a$, a target item $k(a)$, and an evidence-generating distribution. The decision maker operates under a ramp-up window $[0, H]$ with a total budget $B$ and chooses, at each day $t$, which activity (if any) to run, until either $t = H$ or all items are classified as *use*, *discard*, or *escalate*.

## 4. Framework

### 4.1 Change characterization

The first step compares $S$ and $T$ along each factor $f \in F$ and produces the change indicator $\delta_f$. The comparison uses a short structured elicitation plus available data: equipment metadata, crew skill records, supplier qualification status, process recipes, and ambient measurements. Table 1 illustrates the output of this step for a four-factor example where a line has been upgraded with new robots and moved to a new facility.

Table 1: Example change characterization output for a line relocated to a new facility with partial equipment upgrade.

| Factor $f$ | Source value | Target value | $\delta_f$ |
|---|---|---|---|
| Robot cycle time | 4.1 s | 3.4 s (new model) | 0.7 |
| Crew experience (median years) | 7.2 | 2.1 | 0.9 |
| Supplier material grade | A | A (same contract) | 0.1 |
| Ambient humidity | 45 percent | 60 percent | 0.4 |

Any factor with $\delta_f = 0$ propagates no change signal. Any factor with $\delta_f = 1$ invalidates the prior for every item that depends on it until evidence restores trust.

### 4.2 Knowledge graph structure

The knowledge graph $G$ is the coupling substrate. Nodes are items (circles) or factors (rectangles); each edge $(k, f)$ asserts that $k$'s validity is a function of $f$. Figure 1 shows a five-item, three-factor example where item $k_1$ (bottleneck station) depends on robot cycle time; $k_2$ (changeover time) depends on crew experience; $k_3$ (scrap rate) depends on crew experience, supplier grade, and humidity; $k_4$ (buffer target) depends on robot cycle time and crew experience; and $k_5$ (first-pass yield) depends on supplier grade and humidity.

*[Figure 1: Small knowledge graph example. Items (circles) connected by edges to factors (rectangles). Placeholder; to be rendered in final paper.]*

The graph is built from engineering documentation and operator interviews once per product family, and is intended to be audited and edited by engineers. The framework will be tested for graceful degradation when the graph is wrong (see Section 5).

### 4.3 Bayesian trust model

The trust probability $p_k$ is modeled as a Bernoulli random variable with a Beta prior. The prior parameters are set from the change indicators of the factors $k$ depends on, so that items depending on highly-changed factors start with low prior trust:

$$
p_k^{(0)} \sim \text{Beta}\!\left(\alpha_0,\ \beta_0 + \gamma \sum_{f : (k,f) \in E} \delta_f\right)
\quad (1)
$$

where $\alpha_0, \beta_0$ are weak prior pseudocounts and $\gamma > 0$ scales the influence of change evidence. When a verification activity $a$ produces evidence $e$ for item $k$, the posterior update follows standard Bayesian inference [12], [13]:

$$
p_k^{(t+1)} = \frac{\Pr(e \mid k \text{ holds}) \cdot p_k^{(t)}}{\Pr(e \mid k \text{ holds}) \cdot p_k^{(t)} + \Pr(e \mid \neg k) \cdot (1 - p_k^{(t)})}
\quad (2)
$$

The key coupling mechanism is that evidence on $k$ also updates beliefs about every item $k'$ that shares a factor with $k$. We implement this through factor-level latent variables: each factor $f$ carries a latent "still as in source" indicator with its own posterior, and item-level evidence revises the factor posterior, which in turn revises all dependent items. This is the mechanism by which one trial run or one shadow-mode reading informs many items at once.

### 4.4 Decision agent

At each day $t$ the agent selects the verification activity $a^*$ that maximizes expected risk reduction per unit cost:

$$
a^* = \arg\max_{a \in A}\ \frac{R(a)}{c_a}
\quad (3)
$$

where $R(a)$ is the expected reduction in total decision risk from running activity $a$, computed over the induced posterior updates of $k(a)$ and every item linked to $k(a)$ through a shared factor. Decision risk is the expected cost of using a knowledge item incorrectly, aggregated across items weighted by their downstream economic impact.

Four evidence sources are supported; their characteristics are summarized in Table 2.

Table 2: Four verification activities supported by the decision agent.

| Activity | Cost | Latency | Signal strength | Coverage |
|---|---|---|---|---|
| Trial run | High | Hours | High | Single item, direct |
| Shadow mode | Medium | 1 day | Medium | One item at a time, in-process |
| Formula-based re-derivation | Low | Minutes | Medium (model-based) | Single item, assumption-contingent |
| Expert judgment | Medium | Minutes | Variable | 1 or more items |

If the posterior $p_k$ for an item never resolves above a use threshold or below a discard threshold after the budget allocated to $k$ is exhausted, $k$ is *escalated* to engineering for structured review rather than used blindly or discarded. The use, discard, and escalation thresholds are set from the economic consequences in Section 3.

## 5. Planned Evaluation

The framework will be evaluated in discrete-event simulation using standard DES methodology [11]. The testbed consists of (i) a five-station serial flow line with stochastic processing times, random breakdowns, and setup-dependent changeovers, and (ii) the public MiniFab semiconductor model [10]. Both have been widely used as reference systems for production-control experiments.

**Scenarios.** Two scenarios will be simulated: (S1) *equipment replacement or upgrades*, in which one or two stations are replaced with faster but less-mature equipment, affecting cycle time, breakdown distribution, and operator familiarity factors; and (S2) *facility relocation*, in which the entire line is moved to a new facility with different crew skill distribution, different supplier material mix, and different ambient conditions. Each scenario is parameterized to produce a range of change severities, giving 200 randomized change instances with ground truth trust values obtained by 30 replications each.

**Baselines.** Three baselines will be compared. (B1) *Full revalidation* runs trial runs on every item until each posterior crosses a decision threshold, representing the Copy Exactly! extreme. (B2) *Fixed-duration monitoring* runs a one-week shadow-mode window on all items, then commits to use decisions for items that did not trigger an alarm. (B3) *No evidence sharing* applies the same decision agent and evidence sources but without routing updates through shared factors, isolating the contribution of graph coupling.

**Measures.** The primary measures are (M1) total decision and verification cost in simulated currency; (M2) *incorrect knowledge reuse*, defined as the fraction of items classified as *use* whose ground-truth trust in $T$ is below a target threshold; and (M3) *decision time*, the number of simulated days until every item is classified. Secondary measures include escalation rate and sensitivity to the tuning constant $\gamma$ in Equation (1).

**Hypotheses.** H1: the proposed framework will achieve lower total cost than B1 at comparable incorrect-reuse rates. H2: the framework will achieve lower incorrect-reuse than B2 at comparable total cost. H3: removing graph coupling (B3) will degrade cost or incorrect-reuse or both, isolating the value of evidence sharing. **Robustness.** H1 to H3 will also be tested under adversarially corrupted knowledge graphs (edges removed, edges added, factors renamed) to characterize how the framework degrades when the graph is wrong.

## 6. Discussion and Expected Contributions

If the planned evaluation supports H1 to H3, the framework supplies an integrated decision rule for post-change manufacturing knowledge validation that is both item-level and cost-aware. The closest prior work overlaps the proposal in three places. First, condition-based maintenance POMDPs with shared environmental factors [3], [5] use a similar coupling idea with continuous latent states and Kalman-type filtering; our discrete, engineer-auditable knowledge graph is designed for inspection and editing. Second, Bayesian network diagnosis in manufacturing, surveyed in [12], [13], infers causes from fixed observations; we instead prospectively choose which observation to buy next. Third, VoI with linked tests [8], [9] selects experiments on networks of parameters; our objective is the asymmetric economic cost of using a wrong knowledge item and our menu includes a non-measurement option.

Limitations: the framework assumes the knowledge graph is roughly correct (the robustness protocol characterizes degradation); item tolerances may themselves be noisy; and the four evidence sources are a fixed menu.

## 7. Conclusion

We proposed a framework for risk-aware and cost-effective validation of manufacturing knowledge after a production system change, integrating change characterization, a knowledge graph of item-to-factor dependencies, a Bayesian trust model that routes evidence through shared factors, and a cost-aware decision agent. The planned discrete-event evaluation will quantify cost, incorrect reuse, and decision time against standard baselines, and will stress-test the framework under incorrect graphs.

## Acknowledgements

*[To be added after acceptance, to preserve double-blind review.]*

## References

[1] C. J. McDonald, "The evolution of Intel's Copy EXACTLY! technology transfer method," *Intel Technology Journal*, Q4 1998.

[2] C. J. McDonald, "Copy EXACTLY! A paradigm shift in technology transfer method," in *Proc. IEEE/SEMI Advanced Semiconductor Manufacturing Conf.*, 1997, pp. 414-417.

[3] A. R. Cassandra, "A survey of POMDP applications," in *Working Notes AAAI Fall Symp. on Planning with POMDPs*, 1998.

[4] K. G. Papakonstantinou and M. Shinozuka, "Planning structural inspection and maintenance policies via dynamic programming and Markov processes. Part I: Theory; Part II: POMDP implementation," *Reliability Engineering and System Safety*, vol. 130, pp. 202-213 and 214-224, 2014.

[5] C. P. Andriotis, K. G. Papakonstantinou, and E. N. Chatzi, "Value of structural health information in partially observable stochastic environments," *Structural Safety*, vol. 93, 102072, 2021.

[6] C. Terwiesch and R. E. Bohn, "Learning and process improvement during production ramp-up," *International Journal of Production Economics*, vol. 70, no. 1, pp. 1-19, 2001.

[7] L. Argote, *Organizational Learning: Creating, Retaining and Transferring Knowledge*, 2nd ed. New York: Springer, 2013.

[8] R. A. Howard, "Information value theory," *IEEE Trans. Systems Science and Cybernetics*, vol. 2, no. 1, pp. 22-26, 1966.

[9] H. Raiffa and R. Schlaifer, *Applied Statistical Decision Theory*. Cambridge, MA: Harvard Business School, 1961.

[10] K. G. Kempf, "Intel five-machine six-step mini-fab description," Intel Corporation, Chandler, AZ, 1994.

[11] J. Banks, J. S. Carson, B. L. Nelson, and D. M. Nicol, *Discrete-Event System Simulation*, 5th ed. Upper Saddle River, NJ: Pearson, 2010.

[12] J. Pearl, *Probabilistic Reasoning in Intelligent Systems: Networks of Plausible Inference*. San Mateo, CA: Morgan Kaufmann, 1988.

[13] D. Koller and N. Friedman, *Probabilistic Graphical Models: Principles and Techniques*. Cambridge, MA: MIT Press, 2009.

[14] X. Zhao, P. Chen, and L. C. Tang, "Condition-based maintenance via Markov decision processes: A review," *Frontiers of Engineering Management*, vol. 12, no. 2, pp. 330-342, 2025. doi: 10.1007/s42524-024-4130-7.

[15] C. Terwiesch and Y. Xu, "The copy-exactly ramp-up strategy: Trading-off learning with process change," *IEEE Trans. Engineering Management*, vol. 51, no. 1, pp. 70-84, 2004.
