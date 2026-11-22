# Reference Verification Log

Verification date: 2026-11-21. Every reference used in `docs/literature-review.md` and in `paper/iise-2027-paper.md` is listed here.

## How each reference was checked

- **DOI items.** Queried `https://api.crossref.org/works/<DOI>` and confirmed that the title, first author, year, and venue match the citation. Volume, issue, and pages in the citations are taken from the Crossref record. "Cites" is Crossref `is-referenced-by-count` on the verification date.
- **Items without a DOI.** Checked through a publisher catalog, a library or arXiv record, or a Crossref-indexed review of the book. The source used is named in the table.
- **Quartile.** SCImago (scimagojr.com) blocks automated access (HTTP 403). Quartiles were therefore taken from secondary sources that report SCImago data, and the source type is labelled:
  - `Q1 (SJR mirror)`: SCImago SJR data as republished by scijournal.org.
  - `Q1 (SJR listing)`: a SCImago category-ranking page seen in web search results (Scopus data as of March 2026).
  - `Q1 (aggregators)`: two or more third-party sites that cite SCImago agree on the quartile.
  - `not verified`: no reliable quartile found. Q1 is not claimed.
  - `n/a`: book, conference paper, technical journal without SJR, or a journal that has ceased publication.
  Quartiles change every year. Confirm them on scimagojr.com before any formal reporting.

## Verified references

Numbers in the **LR** column are the citation numbers used in `docs/literature-review.md`. Numbers in the **Paper** column are the citation numbers used in `paper/iise-2027-paper.md` (blank = not cited in the paper).

| LR | Paper | Citation | DOI | Verification | Cites | Quartile | Theme |
|---|---|---|---|---|---|---|---|
| 1 | 2 | C. J. McDonald, "Copy EXACTLY! A paradigm shift in technology transfer method," Proc. IEEE/SEMI ASMC, 1997, pp. 414-417 | 10.1109/ASMC.1997.630771 | Crossref: title, author, venue, pages match | 8 | n/a (conference) | Ramp-up |
| 2 | 1 | C. J. McDonald, "The evolution of Intel's Copy EXACTLY! technology transfer method," Intel Technology Journal, vol. 2, no. 4 (Q4 1998) | none | No DOI. Verified via the Q4 1998 issue PDF on intel.com and the Wikipedia "Copy Exactly!" citation. Page numbers omitted because they were not confirmed from the primary PDF | n/a | n/a | Ramp-up |
| 3 | 4 | C. Terwiesch, R. E. Bohn, "Learning and process improvement during production ramp-up," Int. J. Prod. Econ., 70(1), 1-19, 2001 | 10.1016/S0925-5273(00)00045-1 | Crossref match | 265 | Q1 (SJR mirror) | Ramp-up |
| 4 | 3 | C. Terwiesch, Y. Xu, "The copy-exactly ramp-up strategy: Trading-off learning with process change," IEEE Trans. Eng. Manag., 51(1), 70-84, 2004 | 10.1109/TEM.2003.822465 | Crossref match | 93 | Q1 (aggregators) | Ramp-up |
| 5 | | L. Surbier, G. Alpan, E. Blanco, "A comparative study on production ramp-up: state-of-the-art and new challenges," Prod. Plan. Control, 25(15), 1264-1286, 2014 | 10.1080/09537287.2013.817624 | Crossref match | 89 | Q1 (SJR mirror) | Ramp-up |
| 6 | 5 | C. H. Glock, E. H. Grosse, "Decision support models for production ramp-up: a systematic literature review," Int. J. Prod. Res., 53(21), 6637-6651, 2015 | 10.1080/00207543.2015.1064185 | Crossref match | 82 | Q1 (SJR mirror) | Ramp-up |
| 7 | | S. Doltsinis, P. Ferreira, N. Lohse, "An MDP model-based reinforcement learning approach for production station ramp-up optimization: Q-learning analysis," IEEE Trans. Syst. Man Cybern. Syst., 44(9), 1125-1138, 2014 | 10.1109/TSMC.2013.2294155 | Crossref match | 59 | Q1 (aggregators) | Ramp-up |
| 8 | | L. Argote, S. L. Beckman, D. Epple, "The persistence and transfer of learning in industrial settings," Manage. Sci., 36(2), 140-154, 1990 | 10.1287/mnsc.36.2.140 | Crossref match | 909 | Q1 (SJR mirror) | Transfer |
| 9 | | P. S. Adler, K. B. Clark, "Behind the learning curve: A sketch of the learning process," Manage. Sci., 37(3), 267-281, 1991 | 10.1287/mnsc.37.3.267 | Crossref match | 415 | Q1 (SJR mirror) | Transfer |
| 10 | | G. P. Pisano, "Knowledge, integration, and the locus of learning: An empirical analysis of process development," Strateg. Manag. J., 15(S1), 85-100, 1994 | 10.1002/smj.4250150907 | Crossref match | 572 | Q1 (SJR listing) | Transfer |
| 11 | | E. von Hippel, "'Sticky information' and the locus of problem solving: Implications for innovation," Manage. Sci., 40(4), 429-439, 1994 | 10.1287/mnsc.40.4.429 | Crossref match | 2460 | Q1 (SJR mirror) | Transfer |
| 12 | 6 | G. Szulanski, "Exploring internal stickiness: Impediments to the transfer of best practice within the firm," Strateg. Manag. J., 17(S2), 27-43, 1996 | 10.1002/smj.4250171105 | Crossref match | 5319 | Q1 (SJR listing) | Transfer |
| 13 | 7 | M. J. Tyre, E. von Hippel, "The situated nature of adaptive learning in organizations," Organ. Sci., 8(1), 71-83, 1997 | 10.1287/orsc.8.1.71 | Crossref match | 379 | Q1 (SJR listing) | Transfer |
| 14 | | L. Argote, P. Ingram, "Knowledge transfer: A basis for competitive advantage in firms," Organ. Behav. Hum. Decis. Process., 82(1), 150-169, 2000 | 10.1006/obhd.2000.2893 | Crossref match | 2835 | Q1 (SJR listing) | Transfer |
| 15 | | K. Ferdows, "Transfer of changing production know-how," Prod. Oper. Manag., 15(1), 1-9, 2006 | 10.1111/j.1937-5956.2006.tb00031.x | Crossref match (published as "POM Forum: Transfer of Changing Production Know-How") | 131 | Q1 (SJR mirror) | Transfer |
| 16 | | L. Argote, Organizational Learning: Creating, Retaining and Transferring Knowledge, 2nd ed., Springer, 2013 | 10.1007/978-1-4614-5251-5 | Crossref match (book) | 460 | n/a (book) | Transfer |
| 17 | 17 | A. Hogan et al., "Knowledge graphs," ACM Comput. Surv., 54(4), 1-37, 2022 | 10.1145/3447772 | Crossref match (18 authors) | 2041 | Q1 (SJR mirror) | Knowledge graphs |
| 18 | | S. Ji, S. Pan, E. Cambria, P. Marttinen, P. S. Yu, "A survey on knowledge graphs: Representation, acquisition, and applications," IEEE Trans. Neural Netw. Learn. Syst., 33(2), 494-514, 2022 | 10.1109/TNNLS.2021.3070843 | Crossref match | 2462 | not verified | Knowledge graphs |
| 19 | 18 | G. Buchgeher, D. Gabauer, J. Martinez-Gil, L. Ehrlinger, "Knowledge graphs in manufacturing and production: A systematic literature review," IEEE Access, 9, 55537-55554, 2021 | 10.1109/ACCESS.2021.3070395 | Crossref match | 158 | Q1 (SJR mirror) | Knowledge graphs |
| 20 | | X. Li, M. Lyu, Z. Wang, C.-H. Chen, P. Zheng, "Exploiting knowledge graphs in industrial products and services: A survey of key aspects, challenges, and future perspectives," Comput. Ind., 129, 103449, 2021 | 10.1016/j.compind.2021.103449 | Crossref match | 135 | Q1 (SJR mirror) | Knowledge graphs |
| 21 | | P. Zheng, L. Xia, C. Li, X. Li, B. Liu, "Towards Self-X cognitive manufacturing network: An industrial knowledge graph-based multi-agent reinforcement learning approach," J. Manuf. Syst., 61, 16-26, 2021 | 10.1016/j.jmsy.2021.08.002 | Crossref match | 212 | Q1 (SJR mirror) | Knowledge graphs |
| 22 | | B. Zhou, J. Bao, J. Li, Y. Lu, T. Liu, Q. Zhang, "A novel knowledge graph-based optimization approach for resource allocation in discrete manufacturing workshops," Robot. Comput.-Integr. Manuf., 71, 102160, 2021 | 10.1016/j.rcim.2021.102160 | Crossref match | 149 | Q1 (aggregators) | Knowledge graphs |
| 23 | | L. Xia, Y. Liang, J. Leng, P. Zheng, "Maintenance planning recommendation of complex industrial equipment based on knowledge graph and graph neural network," Reliab. Eng. Syst. Saf., 232, 109068, 2023 | 10.1016/j.ress.2022.109068 | Crossref match | 153 | Q1 (SJR mirror) | Knowledge graphs |
| 24 | 21 | J. Pearl, Probabilistic Reasoning in Intelligent Systems: Networks of Plausible Inference, Morgan Kaufmann, 1988 | 10.1016/C2009-0-27609-4 | Crossref match (book record, 1988) | 113 (book record) | n/a (book) | Bayesian networks |
| 25 | 22 | D. Koller, N. Friedman, Probabilistic Graphical Models: Principles and Techniques, MIT Press, 2009 | none | No DOI. Verified via a Crossref-indexed book review in Knowl. Eng. Rev. (10.1017/S0269888910000275) | n/a | n/a (book) | Bayesian networks |
| 26 | 10 | D. Heckerman, J. S. Breese, K. Rommelse, "Decision-theoretic troubleshooting," Commun. ACM, 38(3), 49-57, 1995 | 10.1145/203330.203341 | Crossref match | 106 | Q1 (SJR mirror) | Bayesian networks, VoI |
| 27 | 8 | H. Langseth, L. Portinale, "Bayesian networks in reliability," Reliab. Eng. Syst. Saf., 92(1), 92-108, 2007 | 10.1016/j.ress.2005.11.037 | Crossref match | 466 | Q1 (SJR mirror) | Bayesian networks |
| 28 | | P. Weber, G. Medina-Oliva, C. Simon, B. Iung, "Overview on Bayesian networks applications for dependability, risk analysis and maintenance areas," Eng. Appl. Artif. Intell., 25(4), 671-682, 2012 | 10.1016/j.engappai.2010.06.002 | Crossref match | 647 | Q1 (aggregators) | Bayesian networks |
| 29 | 9 | B. Cai, L. Huang, M. Xie, "Bayesian networks in fault diagnosis," IEEE Trans. Ind. Inform., 13(5), 2227-2240, 2017 | 10.1109/TII.2017.2695583 | Crossref match | 464 | Q1 (aggregators) | Bayesian networks |
| 30 | | S. Kabir, Y. Papadopoulos, "Applications of Bayesian networks and Petri nets in safety, reliability, and risk assessments: A review," Saf. Sci., 115, 154-175, 2019 | 10.1016/j.ssci.2019.02.009 | Crossref match | 379 | Q1 (SJR listing) | Bayesian networks |
| 31 | | E. Wolbrecht, B. D'Ambrosio, R. Paasch, D. Kirby, "Monitoring and diagnosis of a multistage manufacturing process using Bayesian networks," AI EDAM, 14(1), 53-67, 2000 | 10.1017/S0890060400141058 | Crossref match | 24 | not verified | Bayesian networks |
| 32 | | S. Nannapaneni, S. Mahadevan, S. Rachuri, "Performance evaluation of a manufacturing process under uncertainty using Bayesian networks," J. Clean. Prod., 113, 947-959, 2016 | 10.1016/j.jclepro.2015.12.003 | Crossref match | 69 | Q1 (SJR mirror) | Bayesian networks |
| 33 | 11 | R. A. Howard, "Information value theory," IEEE Trans. Syst. Sci. Cybern., 2(1), 22-26, 1966 | 10.1109/TSSC.1966.300074 | Crossref match | 669 | n/a (journal ceased) | VoI |
| 34 | | H. Raiffa, R. Schlaifer, Applied Statistical Decision Theory, Harvard Business School, 1961 | none | No DOI. Verified via Crossref-indexed 1961 review in Technometrics (10.2307/1266736) | n/a | n/a (book) | VoI |
| 35 | | K. Chaloner, I. Verdinelli, "Bayesian experimental design: A review," Stat. Sci., 10(3), 273-304, 1995 | 10.1214/ss/1177009939 | Crossref match | 1355 | Q1 (SJR mirror) | VoI |
| 36 | | T. Rainforth, A. Foster, D. R. Ivanova, F. Bickford Smith, "Modern Bayesian experimental design," Stat. Sci., 39(1), 100-114, 2024 | 10.1214/23-STS915 | Crossref match | 119 | Q1 (SJR mirror) | VoI |
| 37 | | P. I. Frazier, W. B. Powell, S. Dayanik, "A knowledge-gradient policy for sequential information collection," SIAM J. Control Optim., 47(5), 2410-2439, 2008 | 10.1137/070693424 | Crossref match | 371 | Q1 (SJR mirror) | VoI |
| 38 | 12 | P. I. Frazier, W. B. Powell, S. Dayanik, "The knowledge-gradient policy for correlated normal beliefs," INFORMS J. Comput., 21(4), 599-613, 2009 | 10.1287/ijoc.1080.0314 | Crossref match | 337 | Q1 (SJR mirror) | VoI |
| 39 | | I. O. Ryzhov, W. B. Powell, P. I. Frazier, "The knowledge gradient algorithm for a general class of online learning problems," Oper. Res., 60(1), 180-195, 2012 | 10.1287/opre.1110.0999 | Crossref match | 104 | Q1 (SJR listing) | VoI |
| 40 | | W. B. Powell, I. O. Ryzhov, Optimal Learning, Wiley, 2012 | 10.1002/9781118309858 | Crossref match (book) | 167 | n/a (book) | VoI |
| 41 | 13 | A. Krause, C. Guestrin, "Optimal value of information in graphical models," J. Artif. Intell. Res., 35, 557-591, 2009 | 10.1613/jair.2737 | Crossref match | 43 | Q1 (SJR mirror) | VoI |
| 42 | | J. M. Keisler, Z. A. Collier, E. Chu, N. Sinatra, I. Linkov, "Value of information analysis: The state of application," Environ. Syst. Decis., 34(1), 3-23, 2014 | 10.1007/s10669-013-9439-4 | Crossref match | 125 | not verified | VoI |
| 43 | | D. Straub, "Value of information analysis with structural reliability methods," Struct. Saf., 49, 75-85, 2014 | 10.1016/j.strusafe.2013.08.006 | Crossref match | 169 | Q1 (SJR mirror) | VoI |
| 44 | | M. Memarzadeh, M. Pozzi, "Value of information in sequential decision making: Component inspection, permanent monitoring and system-level scheduling," Reliab. Eng. Syst. Saf., 154, 137-151, 2016 | 10.1016/j.ress.2016.05.014 | Crossref match | 86 | Q1 (SJR mirror) | VoI, CBM |
| 45 | 15 | C. P. Andriotis, K. G. Papakonstantinou, E. N. Chatzi, "Value of structural health information in partially observable stochastic environments," Struct. Saf., 93, 102072, 2021 | 10.1016/j.strusafe.2020.102072 | Crossref match. Note: the DOI contains "2020" although the volume is 2021 | 29 | Q1 (SJR mirror) | VoI, CBM |
| 46 | | A. O'Hagan et al., Uncertain Judgements: Eliciting Experts' Probabilities, Wiley, 2006 | 10.1002/0470033312 | Crossref match (book) | 1026 | n/a (book) | Expert elicitation |
| 47 | | H. Shimodaira, "Improving predictive inference under covariate shift by weighting the log-likelihood function," J. Stat. Plan. Inference, 90(2), 227-244, 2000 | 10.1016/S0378-3758(00)00115-4 | Crossref match | 1181 | not verified | Transfer learning |
| 48 | | S. J. Pan, Q. Yang, "A survey on transfer learning," IEEE Trans. Knowl. Data Eng., 22(10), 1345-1359, 2010 | 10.1109/TKDE.2009.191 | Crossref match | 20332 | Q1 (SJR listing) | Transfer learning |
| 49 | | F. Zhuang et al., "A comprehensive survey on transfer learning," Proc. IEEE, 109(1), 43-76, 2021 | 10.1109/JPROC.2020.3004555 | Crossref match | 6055 | Q1 (one aggregator only; treat as unconfirmed) | Transfer learning |
| 50 | 19 | W. Zhang, L. Deng, L. Zhang, D. Wu, "A survey on negative transfer," IEEE/CAA J. Autom. Sinica, 10(2), 305-329, 2023 | 10.1109/JAS.2022.106004 | Crossref match | 419 | Q1 (SJR listing) | Transfer learning |
| 51 | | J. Gama, I. Žliobaitė, A. Bifet, M. Pechenizkiy, A. Bouchachia, "A survey on concept drift adaptation," ACM Comput. Surv., 46(4), 1-37, 2014 | 10.1145/2523813 | Crossref match | 3423 | Q1 (SJR mirror) | Transfer learning |
| 52 | | J. Lu, A. Liu, F. Dong, F. Gu, J. Gama, G. Zhang, "Learning under concept drift: A review," IEEE Trans. Knowl. Data Eng., 31(12), 2346-2363, 2019 | 10.1109/TKDE.2018.2876857 | Crossref match on DOI, title, authors. The Crossref record is the 2018 early-access version without volume or pages; vol. 31, no. 12, pp. 2346-2363 confirmed via a library catalog record and the arXiv journal reference (arXiv:2004.05785) | 998 | Q1 (SJR listing) | Transfer learning |
| 53 | | J. Pearl, E. Bareinboim, "Transportability of causal and statistical relations: A formal approach," Proc. AAAI Conf. Artif. Intell., 25(1), 247-254, 2011 | 10.1609/aaai.v25i1.7861 | Crossref match | 57 | n/a (conference) | Transportability |
| 54 | 20 | J. Pearl, E. Bareinboim, "External validity: From do-calculus to transportability across populations," Stat. Sci., 29(4), 579-595, 2014 | 10.1214/14-STS486 | Crossref match | 336 | Q1 (SJR mirror) | Transportability |
| 55 | | E. Bareinboim, J. Pearl, "Causal inference and the data-fusion problem," Proc. Natl. Acad. Sci. USA, 113(27), 7345-7352, 2016 | 10.1073/pnas.1510507113 | Crossref match | 481 | Q1 (aggregators) | Transportability |
| 56 | | B. Maschler, M. Weyrich, "Deep transfer learning for industrial automation: A review and discussion of new techniques for data-driven machine learning," IEEE Ind. Electron. Mag., 15(2), 65-75, 2021 | 10.1109/MIE.2020.3034884 | Crossref match | 123 | not verified | Transfer learning |
| 57 | | H. Tercan, T. Meisen, "Machine learning and deep learning based predictive quality in manufacturing: A systematic review," J. Intell. Manuf., 33(7), 1879-1905, 2022 | 10.1007/s10845-022-01963-8 | Crossref match | 389 | Q1 (SJR mirror) | Transfer learning |
| 58 | 14 | K. G. Papakonstantinou, M. Shinozuka, "Planning structural inspection and maintenance policies via dynamic programming and Markov processes. Part I: Theory," Reliab. Eng. Syst. Saf., 130, 202-213, 2014 | 10.1016/j.ress.2014.04.005 | Crossref match | 101 | Q1 (SJR mirror) | CBM |
| 59 | 14 | K. G. Papakonstantinou, M. Shinozuka, "... Part II: POMDP implementation," Reliab. Eng. Syst. Saf., 130, 214-224, 2014 | 10.1016/j.ress.2014.04.006 | Crossref match | 131 | Q1 (SJR mirror) | CBM |
| 60 | | S. Alaswad, Y. Xiang, "A review on condition-based maintenance optimization models for stochastically deteriorating system," Reliab. Eng. Syst. Saf., 157, 54-63, 2017 | 10.1016/j.ress.2016.08.009 | Crossref match | 767 | Q1 (SJR mirror) | CBM |
| 61 | | B. de Jonge, P. A. Scarf, "A review on maintenance optimization," Eur. J. Oper. Res., 285(3), 805-824, 2020 | 10.1016/j.ejor.2019.09.047 | Crossref match | 548 | Q1 (SJR mirror) | CBM |
| 62 | 16 | X. Zhao, P. Chen, L. C. Tang, "Condition-based maintenance via Markov decision processes: A review," Front. Eng. Manag., 12(2), 330-342, 2025 | 10.1007/s42524-024-4130-7 | Crossref match | 48 | Q2 (aggregators) | CBM |
| 63 | | J. J. Nielsen, J. D. Sørensen, "On risk-based operation and maintenance of offshore wind turbine components," Reliab. Eng. Syst. Saf., 96(1), 218-229, 2011 | 10.1016/j.ress.2010.07.007 | Crossref match | 193 | Q1 (SJR mirror) | CBM |
| 64 | | R. G. Sargent, "Verification and validation of simulation models," J. Simul., 7(1), 12-24, 2013 | 10.1057/jos.2012.20 | Crossref match | 912 | Q2 (SJR mirror) | Digital twin, validity |
| 65 | | F. Tao, H. Zhang, A. Liu, A. Y. C. Nee, "Digital twin in industry: State-of-the-art," IEEE Trans. Ind. Inform., 15(4), 2405-2415, 2019 | 10.1109/TII.2018.2873186 | Crossref match | 4566 | Q1 (aggregators) | Digital twin, validity |
| 66 | | D. Jones, C. Snider, A. Nassehi, J. Yon, B. Hicks, "Characterising the digital twin: A systematic literature review," CIRP J. Manuf. Sci. Technol., 29, 36-52, 2020 | 10.1016/j.cirpj.2020.02.002 | Crossref match | 2411 | Q1 (aggregators) | Digital twin, validity |
| 67 | | L. Wright, S. Davidson, "How to tell the difference between a model and a digital twin," Adv. Model. Simul. Eng. Sci., 7, 13, 2020 | 10.1186/s40323-020-00147-4 | Crossref match | 564 | not verified | Digital twin, validity |
| 68 | | M. G. Kapteyn, J. V. R. Pretorius, K. E. Willcox, "A probabilistic graphical model foundation for enabling predictive digital twins at scale," Nat. Comput. Sci., 1(5), 337-347, 2021 | 10.1038/s43588-021-00069-0 | Crossref match | 388 | Q1 (SJR listing) | Digital twin, validity |
| 69 | 23 | J. Banks, J. S. Carson, B. L. Nelson, D. M. Nicol, Discrete-Event System Simulation, 5th ed., Pearson, 2010 | none | No DOI. Verified via the Pearson catalog, ISBN 978-0-13-606212-7 | n/a | n/a (book) | Testbed |
| 70 | 24 | J. A. Ramírez-Hernández, E. Fernandez, "A simulation-based approximate dynamic programming approach for the control of the Intel Mini-Fab benchmark model," Proc. Winter Simulation Conf., 2009, pp. 1634-1645 | 10.1109/WSC.2009.5429179 | Crossref match. Abstract (OpenAlex) confirms it uses the Intel Mini-Fab benchmark model | 10 | n/a (conference) | Testbed |

**Totals.** 70 verified references. 49 journal articles carry a Q1 label from a SCImago-derived source: 10 from a SCImago category listing, 31 from the SCImago data mirror, and 8 from agreeing aggregators. Two are Q2 [62], [64]. Six journals could not be verified and are labelled so. Zhuang et al. [49] has a single-aggregator Q1 report and is not counted as Q1. The remaining 12 entries are books, conference papers, or venues without SJR (n/a).

## Candidates rejected or replaced

| Candidate | Problem | Action |
|---|---|---|
| K. G. Kempf, "Intel five-machine six-step mini-fab description," Intel, 1994 (paper ref [10] in the previous draft, suggested by the reviewer) | Internal Intel document. No Crossref or OpenAlex record, and web search found no primary copy or catalog record | Removed. Replaced by the verified Ramírez-Hernández and Fernandez (2009) paper on the Intel Mini-Fab benchmark. If you obtain Kempf (1994) from a library or a track chair, it can be cited alongside |
| A. R. Cassandra, "A survey of POMDP applications," AAAI Fall Symp., 1998 (previous paper ref [3]) | No Crossref or OpenAlex record found | Removed. The CBM/POMDP stream is covered by verified journal reviews [58]-[62] |
| A. Krause, C. Guestrin, "Near-optimal nonmyopic value of information in graphical models," UAI 2005 (previous paper ref [17]) | The paper exists (arXiv 10.48550/arXiv.1207.1394), but the page numbers 324-331 could not be confirmed | Replaced by the peer-reviewed journal version: Krause and Guestrin, JAIR 35, 2009 [41] |
| D. Golovin, A. Krause, "Adaptive submodularity," JAIR 2011 | The DOI tried (10.1613/jair.3278) returned 404 from Crossref | Not used |
| J. Spier, K. G. Kempf, "Simulation of emergent behavior in manufacturing systems," ASMC 1995 (10.1109/ASMC.1995.484347) | Verified, but its abstract is about operator behavior in simulation. It does not describe the Mini-Fab model | Not used as the Mini-Fab source |
| Three DOIs first guessed from memory: 10.1109/TEM.2003.822462, 10.1287/opre.1110.1010, 10.1016/j.strusafe.2021.102072 | The first two resolved to unrelated papers; the third returned 404 | Correct DOIs found by Crossref bibliographic search: 10.1109/TEM.2003.822465, 10.1287/opre.1110.0999, 10.1016/j.strusafe.2020.102072 |

## Re-verification of references in the previous paper draft

| Old # | Reference | Result | Action |
|---|---|---|---|
| [1] | McDonald 1998, Intel Technol. J. | Exists (intel.com Q4 1998 issue); no DOI | Kept as new [1]; added vol. 2, no. 4 |
| [2] | McDonald 1997, ASMC, pp. 414-417 | Crossref confirms pages | Kept as new [2]; DOI added |
| [3] | Cassandra 1998 | Could not verify | Removed |
| [4] | Papakonstantinou and Shinozuka 2014, Parts I and II | Crossref confirms both parts | Kept as new [14]; DOIs added |
| [5] | Andriotis et al. 2021 | Correct; DOI is 10.1016/j.strusafe.2020.102072 | Kept as new [15]; DOI added |
| [6] | Terwiesch and Bohn 2001 | Correct | Kept as new [4] |
| [7] | Argote 2013 | Correct, but it was **not cited anywhere in the previous paper body** | Removed from the paper (kept in the literature review as [16]) |
| [8] | Howard 1966 | Correct | Kept as new [11] |
| [9] | Raiffa and Schlaifer 1961 | Exists; verified via 1961 review | Removed from the paper to save space (kept in the literature review as [34]) |
| [10] | Kempf 1994 | Could not verify | Replaced (see above) by new [24] |
| [11] | Banks et al. 2010 | Correct (Pearson catalog) | Kept as new [23] |
| [12] | Pearl 1988 | Correct | Kept as new [21] |
| [13] | Koller and Friedman 2009 | Correct | Kept as new [22] |
| [14] | Zhao, Chen, Tang 2025 | Correct | Kept as new [16] |
| [15] | Terwiesch and Xu 2004 | Correct; full subtitle restored | Kept as new [3]; DOI added |
| [16] | Frazier et al. 2009 | Correct | Kept as new [12]; DOI added |
| [17] | Krause and Guestrin 2005 (UAI) | Pages unverified | Replaced by JAIR 2009 version, new [13] |
| [18] | Hogan et al. 2022 | Correct. Crossref lists pages 1-37 rather than "art. 71" | Kept as new [17], with Crossref pagination |
| [19] | Pearl and Bareinboim 2011 (AAAI) | Correct | Replaced in the paper by the journal version, Pearl and Bareinboim 2014, Stat. Sci. (new [20]); the AAAI paper stays in the literature review as [53] |
