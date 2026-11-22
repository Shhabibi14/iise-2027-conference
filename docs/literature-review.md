# Literature Review: Validating Manufacturing Knowledge After Production System Change

Extended review supporting the IISE 2027 paper "Risk-Aware and Cost-Effective Validation of Manufacturing Knowledge Across Changing Production Systems." The paper's Section 2 is a compressed version of this document, held to the 6-page limit. This longer version is intended for the paper's defense in review and for a later journal submission.

Citation numbers [1] to [70] follow the **LR** column of `docs/references-verification.md`. Every reference was checked against Crossref (or a named source for items without a DOI). BibTeX for all of them is in `docs/references.bib`.

## 1. Scope and the question the review answers

The paper addresses one decision. After an equipment upgrade, reconfiguration, or relocation, a firm holds a stock of inherited operational knowledge (bottleneck location, changeover times, scrap rates, yield at a given speed). Some of it still holds in the new environment and some does not. The firm must decide, item by item and under a short ramp-up budget, which knowledge to use, which to discard, which to verify, which verification activity to buy next, and which items to escalate to engineers.

No single literature answers this question. Eight streams each contribute one part:

1. Production ramp-up and Copy Exactly!: the operational setting and the industry default.
2. Organizational learning and knowledge transfer: why inherited knowledge fails to transfer.
3. Knowledge graphs: how engineering knowledge and its dependencies can be represented.
4. Bayesian networks: how to reason about uncertain validity with dependencies.
5. Value of information and sequential information acquisition: how to choose what to learn next.
6. Transfer learning, concept drift, and transportability: when source knowledge carries to a target.
7. Condition-based inspection and maintenance: the closest decision-theoretic template.
8. Simulation validity and digital twins: how model validity is assessed after change, and the testbed.

For each stream the review states what it does, its method and unit of analysis, and what it leaves open for this problem. Sections 10 to 13 then compare methods, list the research gaps, map each gap to the framework, and name the closest overlaps.

## 2. Production ramp-up and Copy Exactly!

**What the stream does.** Ramp-up is the period between the end of development and full-volume production, when output, yield, and capacity are still below target. Terwiesch and Bohn [3] model ramp-up as a trade-off between producing now and running learning experiments that raise future yield and speed, and show that capacity spent on deliberate learning can pay off despite short-run output loss. Surbier, Alpan, and Blanco [5] compare definitions and models across the ramp-up literature and identify open challenges, and Glock and Grosse [6] systematically review decision-support models for ramp-up. Doltsinis, Ferreira, and Lohse [7] treat ramp-up of a single production station as a Markov decision process solved with Q-learning, which shows that sequential decision models have been applied to ramp-up at the station level.

**Copy Exactly!** Intel's Copy Exactly! method [1], [2] transfers a process from a development fab to production fabs by replicating equipment, recipes, and procedures as exactly as possible, so that knowledge from the source is valid by construction. Terwiesch and Xu [4] analyze this strategy formally as a trade-off: freezing the process protects transferred knowledge but forgoes improvements that a process change could bring.

**Method and unit of analysis.** Analytical models of the learning trade-off [3], [4], reviews [5], [6], and an MDP at station level [7]. The unit is the line, plant, or station, and the decision is how much capacity, effort, or process change to allow.

**What it leaves open.** None of these works represents individual knowledge items with tolerances, and none supplies a rule for deciding which items to verify with which activity. Copy Exactly! avoids the question by making the target identical to the source, which is costly and impossible when new equipment or a new site is the point of the change. The question this paper asks lies between the two extremes Terwiesch and Xu [4] describe.

## 3. Organizational learning and knowledge transfer

**What the stream does.** A long empirical tradition shows that production knowledge does not transfer for free. Argote, Beckman, and Epple [8] study shipyards and find that learning depreciates and transfers only partly across plants. Adler and Clark [9] open the learning curve and link it to engineering and training activity. Pisano [10] shows that in process development the value of learning by doing in the target environment, rather than in the lab, depends on how well the underlying science is understood. Von Hippel [11] introduces "sticky information": knowledge that is costly to move from where it was generated. Szulanski [12] finds that the main barriers to transferring best practice inside a firm are knowledge-related (causal ambiguity, absorptive capacity, the relationship between source and recipient) rather than motivational. Tyre and von Hippel [13] show that adaptive learning is situated: engineers often must observe the problem in its physical setting to understand it. Argote and Ingram [14] frame knowledge transfer as a source of competitive advantage, Ferdows [15] studies transfer of production know-how that keeps changing, and Argote [16] synthesizes the field.

**Method and unit of analysis.** Field studies, econometrics on learning curves, and case-based theory. The unit is the firm, plant, practice, or project.

**What it leaves open.** This literature explains why inherited knowledge becomes unreliable after a change: it is tied to a context, and the causes that make it valid are often ambiguous. It does not give an operational method for deciding, item by item, which knowledge still holds. The framework takes the stream's central insight, that validity depends on context, and makes the context explicit as factors in a graph.

## 4. Knowledge graphs

**What the stream does.** Hogan et al. [17] and Ji et al. [18] survey knowledge graphs: their data models, construction, embedding, and reasoning. In manufacturing, Buchgeher et al. [19] review knowledge graph use in manufacturing and production, and Li et al. [20] survey knowledge graphs in industrial products and services. Applications include a knowledge-graph-based multi-agent reinforcement learning approach for cognitive manufacturing networks (Zheng et al. [21]), knowledge-graph-based resource allocation in discrete manufacturing workshops (Zhou et al. [22]), and maintenance planning recommendation that combines a knowledge graph with a graph neural network (Xia et al. [23]).

**Method and unit of analysis.** Graph data models, ontologies, embeddings, and graph neural networks. The unit is a fact, entity, or relation, and the typical task is representation, retrieval, completion, or recommendation.

**What it leaves open.** Knowledge graphs in manufacturing represent what is known. They do not hold a calibrated probability that each fact is still valid after the system changes, and they do not decide which facts to re-verify. Knowledge graph completion predicts missing links. It does not assess whether an existing link has become false because the environment moved. The framework uses the knowledge graph for a different purpose: as an engineer-auditable dependency structure that routes validity evidence between items sharing context factors.

## 5. Bayesian networks for reliability, diagnosis, and manufacturing

**What the stream does.** Pearl [24] and Koller and Friedman [25] give the foundations of Bayesian networks and exact and approximate inference, including noisy-OR models for combining several causes. In reliability and dependability, Langseth and Portinale [27], Weber et al. [28], and Kabir and Papadopoulos [30] review Bayesian network applications to reliability, risk, and maintenance, and Cai, Huang, and Xie [29] review Bayesian networks in fault diagnosis. In manufacturing, Wolbrecht et al. [31] monitor and diagnose a multistage process with a Bayesian network, and Nannapaneni, Mahadevan, and Rachuri [32] evaluate manufacturing process performance under uncertainty. Closest in spirit is decision-theoretic troubleshooting by Heckerman, Breese, and Rommelse [26], which uses a Bayesian network to choose the sequence of observations and repairs that minimizes the expected cost of fixing a faulty device.

**Method and unit of analysis.** Graphical probabilistic models with inference over a fixed structure. The unit is a component, failure mode, or process variable. The task is diagnosis, prediction, or risk assessment.

**What it leaves open.** Diagnostic Bayesian networks ask what is wrong with a system whose structure is fixed. Our question is which inherited beliefs about a changed system are still true. Troubleshooting [26] does select observations by expected cost, but the observations are homogeneous tests on one faulty device. It has no menu of qualitatively different evidence sources, no ramp-up horizon, and no asymmetric cost of using a false belief versus discarding a true one. The framework keeps the Bayesian network machinery (binary validity variables, factor latents, noisy-OR) and changes what the variables mean and what the decisions are.

## 6. Value of information and sequential information acquisition

**What the stream does.** Howard [33] defines the value of information as the expected improvement in a decision from observing an uncertain quantity before acting, and Raiffa and Schlaifer [34] develop the Bayesian decision theory behind it. Chaloner and Verdinelli [35] review Bayesian experimental design, which chooses experiments to maximize expected utility or information, and Rainforth et al. [36] survey its modern computational methods.

The knowledge-gradient family is the closest methodological relative of the decision agent. Frazier, Powell, and Dayanik [37] introduce the knowledge-gradient policy, which picks the measurement with the largest expected one-step improvement in the final decision. They then extend it to correlated normal beliefs [38], where one measurement updates beliefs about many alternatives through a covariance matrix. Ryzhov, Powell, and Frazier [39] generalize it to online learning, and Powell and Ryzhov [40] collect the field in a book. Krause and Guestrin [41] study optimal value of information in graphical models: they give exact algorithms for selecting observations in chain-structured models and prove that extending them to more general structures is computationally hard.

Applied value-of-information work is surveyed by Keisler et al. [42]. In engineering, Straub [43] computes value of information with structural reliability methods, Memarzadeh and Pozzi [44] analyze it for sequential inspection, monitoring, and scheduling, and Andriotis, Papakonstantinou, and Chatzi [45] quantify the value of structural health information in partially observable environments. O'Hagan et al. [46] give methods for eliciting expert probabilities, which matter whenever expert judgment is used as evidence.

**Method and unit of analysis.** Bayesian decision analysis, myopic and nonmyopic policies, and submodular or dynamic-programming selection. The unit is a decision, a set of alternatives, or a set of sensors.

**What it leaves open.** Four features of our setting are not covered together:
- **Belief model.** The knowledge gradient uses continuous, typically Gaussian beliefs over alternative means [37]-[39]. Our variables are binary validity of propositions with tolerances, coupled through shared factors by a noisy-OR.
- **Evidence menu.** The literature mostly assumes one kind of noisy measurement with known quality. We have four qualitatively different sources (trial runs, shadow mode, formula re-derivation, expert judgment) with different cost, latency, coverage, and reliability.
- **Dependent evidence.** One of these sources, formula re-derivation, does not measure the item at all. It recomputes it from the same factors that drive the prior, so its evidence is not conditionally independent of the prior. Standard value-of-information calculations assume conditionally independent observations.
- **Objective.** The cost of using a false item, discarding a true one, or escalating is asymmetric and economic, and there is a hard ramp-up horizon.

## 7. Transfer learning, negative transfer, concept drift, and transportability

**What the stream does.** Machine learning studies when a model trained in one setting works in another. Shimodaira [47] treats covariate shift by reweighting the likelihood. Pan and Yang [48] and Zhuang et al. [49] survey transfer learning. Zhang et al. [50] survey negative transfer, the case where using source knowledge makes performance in the target worse. Gama et al. [51] and Lu et al. [52] review concept drift, where the data-generating process changes over time. In manufacturing, Maschler and Weyrich [56] review deep transfer learning for industrial automation, and Tercan and Meisen [57] review machine learning for predictive quality, where models must cope with changing process conditions.

Causal inference gives the most principled account. Pearl and Bareinboim [53], [54] define transportability: given a causal diagram that marks where the source and target environments differ, they determine whether a causal relation learned in the source can be carried to the target and how. Bareinboim and Pearl [55] generalize this to fusing data from several heterogeneous sources.

**Method and unit of analysis.** Statistical learning, domain adaptation, drift detection, and causal diagrams. The unit is a predictive model or a causal effect.

**What it leaves open.** These methods ask whether a learned model or effect carries over. They mostly assume target data arrives passively, and they do not price the active, costly verification needed to find out. Negative transfer [50] is exactly the failure the framework guards against, and transportability [54] is the formal version of the question "does this item still hold?". Neither prescribes which verification to buy under a budget. The framework works at the level of individual operational propositions, and makes the "which environment differences matter" information explicit as weighted factor-item edges. This plays the role of a transportability diagram, but without requiring a full causal model.

## 8. Condition-based inspection and maintenance

**What the stream does.** Condition-based maintenance decides when to inspect, repair, or replace a deteriorating asset whose state is only partly observed. Papakonstantinou and Shinozuka [58], [59] develop the theory and a POMDP implementation for structural inspection and maintenance. Alaswad and Xiang [60] review condition-based maintenance models for stochastically deteriorating systems. De Jonge and Scarf [61] review maintenance optimization broadly, and Zhao, Chen, and Tang [62] review condition-based maintenance via Markov decision processes. Nielsen and Sørensen [63] apply risk-based inspection and maintenance planning to offshore wind turbine components.

**Method and unit of analysis.** MDPs and POMDPs with Bayesian belief updating from inspections. The unit is an asset or component with a degradation state.

**What it leaves open.** This is the closest decision-theoretic template: hidden state, costly observations, and a belief-based choice between acting and observing. But its unit is a physical asset that degrades over time, not a set of propositions that may have become false all at once when the system changed. The action set offers inspections of one asset rather than heterogeneous evidence sources over many coupled items. The framework borrows the belief-update-then-act structure and applies it to knowledge instead of hardware.

## 9. Simulation validity, digital twins, and the testbed

**What the stream does.** Sargent [64] sets out verification and validation of simulation models, the standard reference for whether a model is credible for its intended use. Digital twin reviews by Tao et al. [65] and Jones et al. [66] describe virtual representations of physical systems that are kept synchronized with data. Wright and Davidson [67] distinguish a digital twin from an ordinary model by its continuous updating from the physical asset. Kapteyn, Pretorius, and Willcox [68] build predictive digital twins on a probabilistic graphical model foundation, which updates the twin's state as data arrives.

**What it leaves open.** Validation in this stream is an engineering activity applied to a model as a whole. Digital twins assume a data stream that keeps the model aligned. Neither treats an organization's informal operational knowledge as a set of separately validated propositions, and neither prices the choice between validation activities. Kapteyn et al. [68] is the nearest neighbor because it also uses a graphical model to track whether a representation still matches the physical system. Its focus, however, is asset-state estimation rather than the economics of choosing which beliefs to re-verify.

**Testbed sources.** The discrete-event simulation follows standard methodology [69]. The Intel Mini-Fab benchmark, used here as future work, is a widely studied five-machine semiconductor model, as in Ramírez-Hernández and Fernandez [70].

## 10. Methodology comparison

Each row is a representative stream or study. Columns are the features this problem needs. "Yes" means the feature is central to the cited work, "Partial" means it appears in a limited form, and "No" means it is absent.

| Stream (representative refs) | Unit of analysis | Uncertainty model | Decision / action space | Heterogeneous evidence sources | Cross-item coupling | Explicit cost of verification | Handles system change |
|---|---|---|---|---|---|---|---|
| Ramp-up models [3], [5]-[7] | Line, plant, station | Learning curves; MDP at station level [7] | Capacity for learning vs output; station settings | No | No | Partial (lost output) | Partial (new process) |
| Copy Exactly! [1], [2], [4] | Whole process | None (validity by replication) | Freeze vs allow change | No | No | Partial (cost of replication) | Avoids it by replication |
| Knowledge transfer [8]-[16] | Firm, plant, practice | Qualitative / econometric | None (descriptive) | No | No | No | Yes (core subject) |
| Manufacturing knowledge graphs [19]-[23] | Fact, entity, relation | Mostly none; embeddings | Retrieval, recommendation, allocation | No | Yes (graph structure) | No | No |
| Bayesian networks in reliability and diagnosis [27]-[32] | Component, failure mode | Discrete probabilistic | Diagnosis, risk assessment | No | Yes | No | No |
| Decision-theoretic troubleshooting [26] | Faulty device | Bayesian network | Observe or repair, sequenced | Partial (tests and repairs) | Yes | Yes | No |
| Knowledge gradient [37]-[40] | Alternatives | Gaussian, correlated [38] | Which alternative to measure | No | Yes (covariance) | Partial (budget) | No |
| VoI in graphical models [41] | Variables in a graphical model | Discrete graphical model | Observation subset or plan | No | Yes | Yes | No |
| Engineering VoI [43]-[45] | Structure, component | Bayesian / POMDP | Inspect, monitor, maintain | Partial (inspection vs monitoring [44]) | Partial | Yes | No |
| Transfer learning, drift [47]-[52], [56], [57] | Predictive model | Statistical | Adapt or retrain model | No | No | No | Yes |
| Transportability [53]-[55] | Causal effect | Causal diagram | Whether and how to transport | No | Yes (diagram) | No | Yes |
| CBM POMDPs [58]-[63] | Deteriorating asset | POMDP belief | Inspect, repair, replace | Partial | Partial | Yes | No (gradual degradation) |
| Digital twins and validation [64]-[68] | Model or asset twin | Bayesian / graphical [68] | Update twin; validate model | No | Partial | No | Partial |
| **This framework** | **Knowledge item (proposition with tolerance)** | **Binary validity, factor latents, noisy-OR** | **Use, discard, verify (which activity), escalate** | **Yes (four, one non-measurement)** | **Yes (shared factors)** | **Yes (cost per unit risk reduced)** | **Yes (core subject)** |

No prior row has all seven features. The nearest rows are decision-theoretic troubleshooting [26], VoI in graphical models [41], and the knowledge gradient with correlated beliefs [38]. All three are methods for choosing observations. None is posed over inherited operational knowledge after a system change, and none combines heterogeneous evidence sources with a conditionally dependent, non-measurement option.

## 11. Research gaps

- **G1. No item-level model of inherited manufacturing knowledge.** Ramp-up and transfer research works at the line, plant, or practice level [3]-[16]. It explains why knowledge fails to transfer, but does not represent individual operational claims with tolerances whose validity can be tested.
- **G2. Manufacturing knowledge graphs do not track validity under change.** Knowledge graphs represent manufacturing knowledge and support retrieval and recommendation [19]-[23]. They do not hold a calibrated belief that each fact still holds after the environment changes.
- **G3. Bayesian network methods diagnose fixed systems.** Reliability and diagnosis networks [26]-[32] infer faults in a system with known structure. None reasons about whether a body of prior knowledge remains true after the system itself has changed.
- **G4. Value-of-information policies assume homogeneous, conditionally independent evidence.** The knowledge gradient [37]-[39], VoI in graphical models [41], and engineering VoI [43]-[45] select among measurements of one kind, or among a small set like inspection versus monitoring [44]. They do not mix trial runs, shadow mode, expert judgment, and formula re-derivation, where the last is a non-measurement whose evidence depends on the same factors as the prior.
- **G5. Transfer and transportability do not price verification.** Negative transfer [50], concept drift [51], [52], and transportability [53]-[55] say when source knowledge may fail in a target. They do not decide which costly checks to run, in what order, under a budget and a ramp-up horizon.
- **G6. The industry default has no selective middle ground.** Copy Exactly! [1], [2] and its analysis [4] frame the choice as replicate everything or accept process change. No published decision rule supports selective verification between "trust all" and "revalidate all."
- **G7. No benchmark for evaluating such a policy.** None of the streams provides a simulation protocol that separates the method's dependency model from the simulator's ground truth. Without that separation, a method is tested against the same structure it assumes (compare simulation validity concerns in [64]).

## 12. How the gaps support the framework's novelty

| Gap | Framework component that addresses it | Contribution claimed |
|---|---|---|
| G1 | Problem setting: knowledge items as testable propositions with tolerances | An item-level, testable representation of inherited operational knowledge |
| G2 | Component 2: knowledge graph of item-to-factor dependencies, with edge weights | The knowledge graph is used as an auditable dependency structure that routes validity evidence, not only as a store of facts |
| G3 | Component 3: Bayesian trust model with factor latents and noisy-OR | Posterior validity of each item after change, with evidence on one item updating every item that shares a factor |
| G4 | Component 4: decision agent over four heterogeneous activities, with factor-level fusion for formula re-derivation | Value-of-information selection across qualitatively different evidence, including a conditionally dependent non-measurement source |
| G5 | Component 4: expected risk reduction per unit cost under budget and horizon | An explicit economic rule for which verification to buy, with use, discard, and escalate outcomes |
| G6 | Components 1 and 4 together | A selective policy between Copy Exactly! and as-is reuse, compared directly against a full-revalidation baseline |
| G7 | Evaluation: oracle ground-truth graph with partial overlap and hidden factors | A benchmark protocol in which the simulator's truth is partly independent of the method's graph |

The paper's contribution sentence follows from this table. The framework is new as a combination: a graph-coupled posterior over per-item validity, a value-of-information rule over heterogeneous evidence including a conditionally dependent non-measurement source, and a sequential agent with an explicit ramp-up budget and horizon. Each ingredient has a precedent. The combination, and its application to inherited manufacturing knowledge after a system change, does not.

## 13. Closest overlaps and how the framework differs

- **Knowledge gradient with correlated beliefs [38].** Both couple evidence across many items, so that one measurement informs others. The knowledge gradient couples continuous means through a covariance matrix and measures one alternative at a time with one kind of noisy observation. The framework couples binary validity through named factors with a noisy-OR, and chooses among four evidence types with different coverage and cost.
- **Decision-theoretic troubleshooting [26].** Both use a Bayesian network to sequence costly observations by expected cost. Troubleshooting repairs a device with fixed structure. The framework re-establishes trust in a body of knowledge about a changed system, with an escalation outcome and a ramp-up horizon.
- **VoI in graphical models [41].** Both pick observations in a graphical model by value of information. Krause and Guestrin give exact solutions for chain structures and show the general case is hard. The framework uses a myopic rule on a bipartite factor-item graph, which is approximate, and adds heterogeneous activity types.
- **Transportability [54].** Both ask whether knowledge from a source environment holds in a target. Transportability answers it formally from a causal diagram without collecting new data. The framework answers it empirically, by buying evidence, and prices each answer.
- **CBM POMDPs [58]-[62].** Both maintain a belief over a hidden state and trade off observing against acting. CBM tracks gradual physical degradation of one asset. The framework tracks the validity of many propositions after a discrete change.

The honest limits of the novelty claim are that the agent is myopic, the evidence menu is fixed, and the dependency graph is assumed roughly correct. These are stated in the paper's Section 6.

## References

[1] C. J. McDonald, "Copy EXACTLY! A paradigm shift in technology transfer method," in *Proc. IEEE/SEMI Advanced Semiconductor Manufacturing Conf.*, 1997, pp. 414-417, doi: 10.1109/ASMC.1997.630771.

[2] C. J. McDonald, "The evolution of Intel's Copy EXACTLY! technology transfer method," *Intel Technology Journal*, vol. 2, no. 4, 1998.

[3] C. Terwiesch and R. E. Bohn, "Learning and process improvement during production ramp-up," *Int. J. Prod. Econ.*, vol. 70, no. 1, pp. 1-19, 2001, doi: 10.1016/S0925-5273(00)00045-1.

[4] C. Terwiesch and Y. Xu, "The copy-exactly ramp-up strategy: Trading-off learning with process change," *IEEE Trans. Eng. Manag.*, vol. 51, no. 1, pp. 70-84, 2004, doi: 10.1109/TEM.2003.822465.

[5] L. Surbier, G. Alpan, and E. Blanco, "A comparative study on production ramp-up: State-of-the-art and new challenges," *Prod. Plan. Control*, vol. 25, no. 15, pp. 1264-1286, 2014, doi: 10.1080/09537287.2013.817624.

[6] C. H. Glock and E. H. Grosse, "Decision support models for production ramp-up: A systematic literature review," *Int. J. Prod. Res.*, vol. 53, no. 21, pp. 6637-6651, 2015, doi: 10.1080/00207543.2015.1064185.

[7] S. Doltsinis, P. Ferreira, and N. Lohse, "An MDP model-based reinforcement learning approach for production station ramp-up optimization: Q-learning analysis," *IEEE Trans. Syst. Man Cybern. Syst.*, vol. 44, no. 9, pp. 1125-1138, 2014, doi: 10.1109/TSMC.2013.2294155.

[8] L. Argote, S. L. Beckman, and D. Epple, "The persistence and transfer of learning in industrial settings," *Manage. Sci.*, vol. 36, no. 2, pp. 140-154, 1990, doi: 10.1287/mnsc.36.2.140.

[9] P. S. Adler and K. B. Clark, "Behind the learning curve: A sketch of the learning process," *Manage. Sci.*, vol. 37, no. 3, pp. 267-281, 1991, doi: 10.1287/mnsc.37.3.267.

[10] G. P. Pisano, "Knowledge, integration, and the locus of learning: An empirical analysis of process development," *Strateg. Manag. J.*, vol. 15, no. S1, pp. 85-100, 1994, doi: 10.1002/smj.4250150907.

[11] E. von Hippel, "'Sticky information' and the locus of problem solving: Implications for innovation," *Manage. Sci.*, vol. 40, no. 4, pp. 429-439, 1994, doi: 10.1287/mnsc.40.4.429.

[12] G. Szulanski, "Exploring internal stickiness: Impediments to the transfer of best practice within the firm," *Strateg. Manag. J.*, vol. 17, no. S2, pp. 27-43, 1996, doi: 10.1002/smj.4250171105.

[13] M. J. Tyre and E. von Hippel, "The situated nature of adaptive learning in organizations," *Organ. Sci.*, vol. 8, no. 1, pp. 71-83, 1997, doi: 10.1287/orsc.8.1.71.

[14] L. Argote and P. Ingram, "Knowledge transfer: A basis for competitive advantage in firms," *Organ. Behav. Hum. Decis. Process.*, vol. 82, no. 1, pp. 150-169, 2000, doi: 10.1006/obhd.2000.2893.

[15] K. Ferdows, "Transfer of changing production know-how," *Prod. Oper. Manag.*, vol. 15, no. 1, pp. 1-9, 2006, doi: 10.1111/j.1937-5956.2006.tb00031.x.

[16] L. Argote, *Organizational Learning: Creating, Retaining and Transferring Knowledge*, 2nd ed. New York: Springer, 2013, doi: 10.1007/978-1-4614-5251-5.

[17] A. Hogan et al., "Knowledge graphs," *ACM Comput. Surv.*, vol. 54, no. 4, pp. 1-37, 2022, doi: 10.1145/3447772.

[18] S. Ji, S. Pan, E. Cambria, P. Marttinen, and P. S. Yu, "A survey on knowledge graphs: Representation, acquisition, and applications," *IEEE Trans. Neural Netw. Learn. Syst.*, vol. 33, no. 2, pp. 494-514, 2022, doi: 10.1109/TNNLS.2021.3070843.

[19] G. Buchgeher, D. Gabauer, J. Martinez-Gil, and L. Ehrlinger, "Knowledge graphs in manufacturing and production: A systematic literature review," *IEEE Access*, vol. 9, pp. 55537-55554, 2021, doi: 10.1109/ACCESS.2021.3070395.

[20] X. Li, M. Lyu, Z. Wang, C.-H. Chen, and P. Zheng, "Exploiting knowledge graphs in industrial products and services: A survey of key aspects, challenges, and future perspectives," *Comput. Ind.*, vol. 129, 103449, 2021, doi: 10.1016/j.compind.2021.103449.

[21] P. Zheng, L. Xia, C. Li, X. Li, and B. Liu, "Towards Self-X cognitive manufacturing network: An industrial knowledge graph-based multi-agent reinforcement learning approach," *J. Manuf. Syst.*, vol. 61, pp. 16-26, 2021, doi: 10.1016/j.jmsy.2021.08.002.

[22] B. Zhou, J. Bao, J. Li, Y. Lu, T. Liu, and Q. Zhang, "A novel knowledge graph-based optimization approach for resource allocation in discrete manufacturing workshops," *Robot. Comput.-Integr. Manuf.*, vol. 71, 102160, 2021, doi: 10.1016/j.rcim.2021.102160.

[23] L. Xia, Y. Liang, J. Leng, and P. Zheng, "Maintenance planning recommendation of complex industrial equipment based on knowledge graph and graph neural network," *Reliab. Eng. Syst. Saf.*, vol. 232, 109068, 2023, doi: 10.1016/j.ress.2022.109068.

[24] J. Pearl, *Probabilistic Reasoning in Intelligent Systems: Networks of Plausible Inference*. San Mateo, CA: Morgan Kaufmann, 1988, doi: 10.1016/C2009-0-27609-4.

[25] D. Koller and N. Friedman, *Probabilistic Graphical Models: Principles and Techniques*. Cambridge, MA: MIT Press, 2009.

[26] D. Heckerman, J. S. Breese, and K. Rommelse, "Decision-theoretic troubleshooting," *Commun. ACM*, vol. 38, no. 3, pp. 49-57, 1995, doi: 10.1145/203330.203341.

[27] H. Langseth and L. Portinale, "Bayesian networks in reliability," *Reliab. Eng. Syst. Saf.*, vol. 92, no. 1, pp. 92-108, 2007, doi: 10.1016/j.ress.2005.11.037.

[28] P. Weber, G. Medina-Oliva, C. Simon, and B. Iung, "Overview on Bayesian networks applications for dependability, risk analysis and maintenance areas," *Eng. Appl. Artif. Intell.*, vol. 25, no. 4, pp. 671-682, 2012, doi: 10.1016/j.engappai.2010.06.002.

[29] B. Cai, L. Huang, and M. Xie, "Bayesian networks in fault diagnosis," *IEEE Trans. Ind. Inform.*, vol. 13, no. 5, pp. 2227-2240, 2017, doi: 10.1109/TII.2017.2695583.

[30] S. Kabir and Y. Papadopoulos, "Applications of Bayesian networks and Petri nets in safety, reliability, and risk assessments: A review," *Saf. Sci.*, vol. 115, pp. 154-175, 2019, doi: 10.1016/j.ssci.2019.02.009.

[31] E. Wolbrecht, B. D'Ambrosio, R. Paasch, and D. Kirby, "Monitoring and diagnosis of a multistage manufacturing process using Bayesian networks," *AI EDAM*, vol. 14, no. 1, pp. 53-67, 2000, doi: 10.1017/S0890060400141058.

[32] S. Nannapaneni, S. Mahadevan, and S. Rachuri, "Performance evaluation of a manufacturing process under uncertainty using Bayesian networks," *J. Clean. Prod.*, vol. 113, pp. 947-959, 2016, doi: 10.1016/j.jclepro.2015.12.003.

[33] R. A. Howard, "Information value theory," *IEEE Trans. Syst. Sci. Cybern.*, vol. 2, no. 1, pp. 22-26, 1966, doi: 10.1109/TSSC.1966.300074.

[34] H. Raiffa and R. Schlaifer, *Applied Statistical Decision Theory*. Boston, MA: Harvard Business School, 1961.

[35] K. Chaloner and I. Verdinelli, "Bayesian experimental design: A review," *Stat. Sci.*, vol. 10, no. 3, pp. 273-304, 1995, doi: 10.1214/ss/1177009939.

[36] T. Rainforth, A. Foster, D. R. Ivanova, and F. Bickford Smith, "Modern Bayesian experimental design," *Stat. Sci.*, vol. 39, no. 1, pp. 100-114, 2024, doi: 10.1214/23-STS915.

[37] P. I. Frazier, W. B. Powell, and S. Dayanik, "A knowledge-gradient policy for sequential information collection," *SIAM J. Control Optim.*, vol. 47, no. 5, pp. 2410-2439, 2008, doi: 10.1137/070693424.

[38] P. I. Frazier, W. B. Powell, and S. Dayanik, "The knowledge-gradient policy for correlated normal beliefs," *INFORMS J. Comput.*, vol. 21, no. 4, pp. 599-613, 2009, doi: 10.1287/ijoc.1080.0314.

[39] I. O. Ryzhov, W. B. Powell, and P. I. Frazier, "The knowledge gradient algorithm for a general class of online learning problems," *Oper. Res.*, vol. 60, no. 1, pp. 180-195, 2012, doi: 10.1287/opre.1110.0999.

[40] W. B. Powell and I. O. Ryzhov, *Optimal Learning*. Hoboken, NJ: Wiley, 2012, doi: 10.1002/9781118309858.

[41] A. Krause and C. Guestrin, "Optimal value of information in graphical models," *J. Artif. Intell. Res.*, vol. 35, pp. 557-591, 2009, doi: 10.1613/jair.2737.

[42] J. M. Keisler, Z. A. Collier, E. Chu, N. Sinatra, and I. Linkov, "Value of information analysis: The state of application," *Environ. Syst. Decis.*, vol. 34, no. 1, pp. 3-23, 2014, doi: 10.1007/s10669-013-9439-4.

[43] D. Straub, "Value of information analysis with structural reliability methods," *Struct. Saf.*, vol. 49, pp. 75-85, 2014, doi: 10.1016/j.strusafe.2013.08.006.

[44] M. Memarzadeh and M. Pozzi, "Value of information in sequential decision making: Component inspection, permanent monitoring and system-level scheduling," *Reliab. Eng. Syst. Saf.*, vol. 154, pp. 137-151, 2016, doi: 10.1016/j.ress.2016.05.014.

[45] C. P. Andriotis, K. G. Papakonstantinou, and E. N. Chatzi, "Value of structural health information in partially observable stochastic environments," *Struct. Saf.*, vol. 93, 102072, 2021, doi: 10.1016/j.strusafe.2020.102072.

[46] A. O'Hagan et al., *Uncertain Judgements: Eliciting Experts' Probabilities*. Chichester: Wiley, 2006, doi: 10.1002/0470033312.

[47] H. Shimodaira, "Improving predictive inference under covariate shift by weighting the log-likelihood function," *J. Stat. Plan. Inference*, vol. 90, no. 2, pp. 227-244, 2000, doi: 10.1016/S0378-3758(00)00115-4.

[48] S. J. Pan and Q. Yang, "A survey on transfer learning," *IEEE Trans. Knowl. Data Eng.*, vol. 22, no. 10, pp. 1345-1359, 2010, doi: 10.1109/TKDE.2009.191.

[49] F. Zhuang et al., "A comprehensive survey on transfer learning," *Proc. IEEE*, vol. 109, no. 1, pp. 43-76, 2021, doi: 10.1109/JPROC.2020.3004555.

[50] W. Zhang, L. Deng, L. Zhang, and D. Wu, "A survey on negative transfer," *IEEE/CAA J. Autom. Sinica*, vol. 10, no. 2, pp. 305-329, 2023, doi: 10.1109/JAS.2022.106004.

[51] J. Gama, I. Žliobaitė, A. Bifet, M. Pechenizkiy, and A. Bouchachia, "A survey on concept drift adaptation," *ACM Comput. Surv.*, vol. 46, no. 4, pp. 1-37, 2014, doi: 10.1145/2523813.

[52] J. Lu, A. Liu, F. Dong, F. Gu, J. Gama, and G. Zhang, "Learning under concept drift: A review," *IEEE Trans. Knowl. Data Eng.*, vol. 31, no. 12, pp. 2346-2363, 2019, doi: 10.1109/TKDE.2018.2876857.

[53] J. Pearl and E. Bareinboim, "Transportability of causal and statistical relations: A formal approach," in *Proc. AAAI Conf. Artif. Intell.*, vol. 25, no. 1, 2011, pp. 247-254, doi: 10.1609/aaai.v25i1.7861.

[54] J. Pearl and E. Bareinboim, "External validity: From do-calculus to transportability across populations," *Stat. Sci.*, vol. 29, no. 4, pp. 579-595, 2014, doi: 10.1214/14-STS486.

[55] E. Bareinboim and J. Pearl, "Causal inference and the data-fusion problem," *Proc. Natl. Acad. Sci. USA*, vol. 113, no. 27, pp. 7345-7352, 2016, doi: 10.1073/pnas.1510507113.

[56] B. Maschler and M. Weyrich, "Deep transfer learning for industrial automation: A review and discussion of new techniques for data-driven machine learning," *IEEE Ind. Electron. Mag.*, vol. 15, no. 2, pp. 65-75, 2021, doi: 10.1109/MIE.2020.3034884.

[57] H. Tercan and T. Meisen, "Machine learning and deep learning based predictive quality in manufacturing: A systematic review," *J. Intell. Manuf.*, vol. 33, no. 7, pp. 1879-1905, 2022, doi: 10.1007/s10845-022-01963-8.

[58] K. G. Papakonstantinou and M. Shinozuka, "Planning structural inspection and maintenance policies via dynamic programming and Markov processes. Part I: Theory," *Reliab. Eng. Syst. Saf.*, vol. 130, pp. 202-213, 2014, doi: 10.1016/j.ress.2014.04.005.

[59] K. G. Papakonstantinou and M. Shinozuka, "Planning structural inspection and maintenance policies via dynamic programming and Markov processes. Part II: POMDP implementation," *Reliab. Eng. Syst. Saf.*, vol. 130, pp. 214-224, 2014, doi: 10.1016/j.ress.2014.04.006.

[60] S. Alaswad and Y. Xiang, "A review on condition-based maintenance optimization models for stochastically deteriorating system," *Reliab. Eng. Syst. Saf.*, vol. 157, pp. 54-63, 2017, doi: 10.1016/j.ress.2016.08.009.

[61] B. de Jonge and P. A. Scarf, "A review on maintenance optimization," *Eur. J. Oper. Res.*, vol. 285, no. 3, pp. 805-824, 2020, doi: 10.1016/j.ejor.2019.09.047.

[62] X. Zhao, P. Chen, and L. C. Tang, "Condition-based maintenance via Markov decision processes: A review," *Front. Eng. Manag.*, vol. 12, no. 2, pp. 330-342, 2025, doi: 10.1007/s42524-024-4130-7.

[63] J. J. Nielsen and J. D. Sørensen, "On risk-based operation and maintenance of offshore wind turbine components," *Reliab. Eng. Syst. Saf.*, vol. 96, no. 1, pp. 218-229, 2011, doi: 10.1016/j.ress.2010.07.007.

[64] R. G. Sargent, "Verification and validation of simulation models," *J. Simul.*, vol. 7, no. 1, pp. 12-24, 2013, doi: 10.1057/jos.2012.20.

[65] F. Tao, H. Zhang, A. Liu, and A. Y. C. Nee, "Digital twin in industry: State-of-the-art," *IEEE Trans. Ind. Inform.*, vol. 15, no. 4, pp. 2405-2415, 2019, doi: 10.1109/TII.2018.2873186.

[66] D. Jones, C. Snider, A. Nassehi, J. Yon, and B. Hicks, "Characterising the digital twin: A systematic literature review," *CIRP J. Manuf. Sci. Technol.*, vol. 29, pp. 36-52, 2020, doi: 10.1016/j.cirpj.2020.02.002.

[67] L. Wright and S. Davidson, "How to tell the difference between a model and a digital twin," *Adv. Model. Simul. Eng. Sci.*, vol. 7, 13, 2020, doi: 10.1186/s40323-020-00147-4.

[68] M. G. Kapteyn, J. V. R. Pretorius, and K. E. Willcox, "A probabilistic graphical model foundation for enabling predictive digital twins at scale," *Nat. Comput. Sci.*, vol. 1, no. 5, pp. 337-347, 2021, doi: 10.1038/s43588-021-00069-0.

[69] J. Banks, J. S. Carson, B. L. Nelson, and D. M. Nicol, *Discrete-Event System Simulation*, 5th ed. Upper Saddle River, NJ: Pearson, 2010.

[70] J. A. Ramírez-Hernández and E. Fernandez, "A simulation-based approximate dynamic programming approach for the control of the Intel Mini-Fab benchmark model," in *Proc. Winter Simulation Conf.*, 2009, pp. 1634-1645, doi: 10.1109/WSC.2009.5429179.
