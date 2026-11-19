# Novelty Positioning: Cost-Aware Validation of Manufacturing Knowledge

This note establishes exactly what is new in this paper relative to three adjacent literatures: Bayesian inspection and partially observable condition-based maintenance, manufacturing knowledge transfer and ramp-up (including Intel's Copy Exactly!), and the value-of-information (VoI) tradition in decision analysis. The purpose is to identify the combination of features our setting requires, show what each literature supplies and what it does not, and state the specific gap this paper fills.

## 1. The problem's requirements

A production line has just undergone a system change (new assets, new plant, new crew mix). The firm holds a stock of learned knowledge items: numerical statements with tolerances about which station bottlenecks, how long changeovers take, which rework loops are tolerable, what scrap rates to expect, and so on. After the change:

1. The decision maker must act on each individual knowledge item (use it, revalidate it, or escalate it), not on a single aggregated machine state. The items are heterogeneous in cost of being wrong, in tolerance width, and in the context factors they depend on.
2. The items are statistically coupled through shared context factors (crew skill, supplier quality, equipment reliability, material grade), so evidence collected on one item must update beliefs about every item that shares a factor. The coupling structure is a graph, not a single latent variable.
3. The available evidence sources (short trial runs, shadow-mode mirroring of the old setpoints, formula-based re-derivation from physics, expert judgment) differ in cost, latency, and signal strength. The selection among them is itself a sequential decision.
4. The horizon is a short ramp-up window with a hard economic cost to running wrong decisions (scrap, late shipments, wasted capacity) and a hard cost to over-testing (lost production, engineering time).
5. The knowledge graph may be incomplete: some items may be mis-linked or have missing factors. The framework must degrade gracefully when the structure is wrong.

Any adjacent literature that solves (1) to (5) jointly is a competitor. No single adjacent literature does.

## 2. Bayesian inspection and partially observable condition-based maintenance

Unit of analysis. A physical asset (component, structure, machine) with a hidden degradation state. The observation model relates sensor readings to that state; the belief over the state is updated by Bayes rule, and the decision is when to inspect, repair, or replace.

What it decides. An inspection and maintenance policy over time that minimizes expected total cost, typically formalized as a POMDP or a special-structure Markov decision process. Surveys and foundational treatments include Cassandra's POMDP applications survey (Cassandra, 1998), Papakonstantinou and Shinozuka's two-part series on structural inspection via POMDPs (Reliability Engineering and System Safety, 2014), Andriotis, Papakonstantinou, and Chatzi on the value of structural health information (Structural Safety, 2021), and recent reviews on condition-based maintenance via MDPs and POMDPs (Zhao et al., 2025).

What it does not handle for this setting.
- The unit of analysis is a single asset's hidden state, not a portfolio of testable textual-plus-numerical statements with per-item tolerances. The knowledge items in our setting are not component states; they are claims whose truth value is itself the thing in doubt.
- Coupling across items is modeled through one-dimensional degradation processes or a small number of latent variables. There is no explicit graph in which an arbitrary number of items share named context factors, and no mechanism by which evidence on one item updates every other item through those named factors.
- The action space is typically inspect, repair, replace, or do nothing. It does not include selecting among qualitatively different evidence sources (trial, shadow, derive, ask the expert) where the cost structure and signal differ by kind, not just by inspection quality.
- The reward model is cost of maintenance versus cost of failure. It does not include the asymmetric cost of using a wrong knowledge item in production decisions downstream.

## 3. Manufacturing knowledge transfer, ramp-up, and Copy Exactly!

Unit of analysis. Either a whole process or plant (in the Copy Exactly! tradition), or a learning curve on yield or output over calendar time (in the ramp-up tradition).

What it decides. In the ramp-up literature (Terwiesch and Bohn, 2001, International Journal of Production Economics; Terwiesch and Xu, 2004), the decision is how much to sacrifice short-run capacity in favor of deliberate experiments that improve long-run yield. In the Copy Exactly! tradition (McDonald, 1997, IEEE/SEMI ASMC; McDonald, 1998, Intel Technology Journal), the decision is implicit: copy everything that can be copied unless physically impossible, which avoids the question of selective revalidation by refusing to be selective. Argote's organizational-learning program supplies the empirical backbone on what transfers and what does not.

What it does not handle for this setting.
- The ramp-up literature optimizes an aggregate output or yield curve. It does not represent individual knowledge items with tolerances, nor does it update beliefs item by item. Learning is modeled as a monolithic rate, not as a graph of coupled propositions.
- Copy Exactly! is deliberately uneconomic about selective revalidation. It solves the problem of ramp risk by eliminating the choice. Our setting is exactly the case where a firm cannot afford to copy everything, either because it does not have the budget, the time, or the physical possibility (new plant, new crew, new supplier).
- Transfer-learning in machine learning offers mechanisms to port a trained model from a source to a target domain. It does not provide a cost-aware, per-item decision over heterogeneous evidence sources with sequential updating, and it does not link items through named context factors that an engineer can audit.
- None of these traditions supplies a decision rule that chooses, on day t, which of several qualitatively different evidence sources to buy next, for which knowledge item, under a budget constraint.

## 4. Value of Information

Unit of analysis. A single decision-maker with a prior over one or more uncertain variables and a menu of possible information-gathering actions.

What it decides. Whether and how much to pay for information before acting, and in what sequence. The foundations are Howard's Information Value Theory (Howard, 1966) and the Bayesian decision-theoretic framework of Raiffa and Schlaifer (1961, 1976). Extensions include the value of sequential information (Management Science, 1975), modern VoI in medical decision making, oil and gas exploration, and structural health monitoring (Andriotis et al., 2021, is a direct example of VoI applied to POMDP maintenance).

What it does not handle for this setting.
- VoI classically is computed for one decision at a time against one or a small set of uncertain quantities. Our setting has hundreds of coupled knowledge items whose joint posterior matters, and the agent must repeatedly choose which item to investigate with which evidence source.
- VoI frameworks typically assume the information source is a known-quality noisy observation of the uncertainty of interest. Our evidence sources include formula-based re-derivation (not a noisy measurement; a model-based assertion with its own context assumptions) and expert judgment (not independent of the prior). The decision agent must trade these off against straightforward trial runs and shadow-mode readings.
- The literature rarely combines VoI with an explicit knowledge-graph structure that routes evidence from one tested item to many untested but linked items. Where it does (e.g., in Bayesian experimental design on networks), the network is of parameters or latent factors, not of engineering knowledge items with tolerances and per-item usage decisions.

## 5. The specific gap this paper fills

No existing stream combines a graph-structured posterior over per-item knowledge claims, a menu of qualitatively different evidence sources with their own cost and noise, and a cost-aware sequential agent that picks (item, source) pairs by expected risk reduction per unit cost over a short ramp-up horizon. The Bayesian inspection stream has the sequential updating and the cost model, but not the item-level portfolio or the graph. The ramp-up and Copy Exactly! stream has the context (production system change, scarce time) but not the formal decision rule. The VoI stream has the information-pricing logic but neither the item portfolio nor the heterogeneous evidence menu. Putting the three together with a knowledge graph as the coupling substrate is the paper's contribution.

## 6. Our contribution in one sentence

We propose a cost-aware validation framework that treats each manufacturing knowledge item as a testable proposition linked through a shared-factor graph to a Bayesian posterior, and chooses, day by day during ramp-up, which item to probe with which of four heterogeneous evidence sources by expected risk reduction per unit cost, unifying item-level VoI, graph-coupled Bayesian updating, and sequential inspection under one decision rule tailored to production system change.

## 7. Honest overlaps and how we remain different

Overlap 1: POMDPs with shared latent variables. There is a body of work in condition-based maintenance that models several components as sharing a latent environmental factor (a common load, a shared operating regime). Evidence on one component then updates beliefs about the others through the shared factor. This is structurally similar to our shared-context-factor coupling. Distinguishing feature: in that work the shared latent is a continuous environment variable and the per-component state is a degradation level, so the update rule is a Kalman-like or gamma-process filter. We use a discrete knowledge graph in which items are propositions with tolerances, factors are named engineering causes, and the posterior is a factor-graph Bayesian network that an engineer can inspect, audit, and edit. Our evaluation includes robustness tests where edges in the graph are wrong, which is not a scenario those models typically consider.

Overlap 2: Bayesian network diagnosis for root cause in manufacturing. Several papers use Bayesian networks to diagnose process faults from sensor evidence. These models answer the question of what caused the current defect. Distinguishing feature: diagnosis infers a hidden root cause from fixed observations; our framework decides, prospectively, which observation to buy next, for which knowledge item, given a budget and a cost of being wrong. The evidence source itself is a decision variable, and the four sources differ qualitatively, not just in noise level.

Overlap 3: VoI with linked tests and Bayesian experimental design on networks. This line of work selects experiments or measurements on a network of parameters to maximize information gain subject to budget. Distinguishing feature: those methods target parameter estimation or hypothesis testing on continuous or latent variables, with symmetric objectives. Our objective is the asymmetric economic cost of using a wrong knowledge item in production, our tests include a formula-based re-derivation that is not a measurement at all, and the horizon is a short ramp-up window with a hard terminal boundary (speaker registration, handover), not an open-ended estimation task. We also test an LLM agent as a baseline for the test-selection policy, which the VoI literature has not yet made standard.
