# Can We Still Trust Our Knowledge? Cost-Aware Validation of Manufacturing Knowledge After Production System Change

## Abstract

Over years of production, manufacturers learn which station is the bottleneck, how long changeovers take, and what scrap rates to expect. When a line gets new assets or moves to a new plant, some of this knowledge still holds and some does not, and firms cannot tell which. Trusting all of it risks costly wrong decisions, while revalidating all of it, as in Intel's Copy Exactly strategy, consumes time and money. This study frames knowledge validation as an economic decision problem. Each knowledge item is a testable statement with a tolerance, linked in a knowledge graph to the context factors it depends on, such as machine reliability, crew skill, and supplier quality. When factors change, a Bayesian network estimates the probability that each linked item still holds, and evidence on one item updates every item sharing the same factor. During ramp-up, a cost-aware decision agent chooses daily among four evidence sources (trial runs, shadow mode, formula-based re-derivation, and expert judgment) by expected risk reduction per unit cost, then uses each item or escalates it to engineers. We evaluate the framework on a discrete-event simulation of a five-station line under 200 randomized changes, with ground truth from 30 replications each, and on the public MiniFab model. Baselines include full revalidation, fixed one-week shadow mode, a single similarity score, the agent without evidence sharing, and an LLM agent. Reported measures include total cost, wrong reuse, lost value, and time to full use, with robustness tests on incomplete knowledge graphs.

## Keywords

Manufacturing Knowledge Transfer; Knowledge Graphs; Bayesian Networks; Value of Information; Discrete-Event Simulation; Production Ramp-Up

## Suggested Track

- **Primary:** Manufacturing & Design (M&D) — fits "AI/ML in Manufacturing", "Semiconductor Manufacturing" (Intel Copy Exactly), "Cyber-Physical Manufacturing Systems", "Big Data Analytics in Manufacturing", and "Industry Applications of New Technologies".
- **Second choice:** Operational Excellence (OpEx) — fits ramp-up, knowledge transfer, and cost-aware decision making.
