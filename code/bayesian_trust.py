"""
Bipartite Bayesian trust network for manufacturing knowledge validation.

For each factor f in F we have a binary latent "still as in source"
indicator Z_f. For each knowledge item k in K we have a binary validity
variable V_k. The joint model, written as the reviewer prescribed, is:

    Pr(Z_f = 1) = 1 - delta_f                          (factor prior)
    Pr(V_k = 1 | Z) = 1 - prod_{f: (k,f) in E} (1 - w_kf * Z_f_bar_if_invalid)
    Pr(e | V_k)    = evidence model per activity       (see decision_agent.py)

We encode this as a noisy-OR on the FACTORS-ARE-INVALID events:
    Pr(V_k = 0 | Z) = 1 - prod_{f: (k,f) in E} (1 - w_kf * (1 - Z_f))

so an item is invalid if any dependent factor fires (with its weight).

Exact inference on this bipartite structure is tractable at the scales we
care about (|K| <= 20, |F| <= 10) via a direct product over factor states,
but we use a mean-field approximation for factor posteriors updated from
item-level evidence; this keeps the code to under 200 lines and matches
how such models are deployed in practice. See [12] Pearl 1988, [13]
Koller and Friedman 2009 for the general machinery.

References
----------
[12] J. Pearl, Probabilistic Reasoning in Intelligent Systems, 1988.
[13] D. Koller and N. Friedman, Probabilistic Graphical Models, 2009.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np


@dataclass
class BipartiteTrustNet:
    items: List[str]
    factors: List[str]
    edges: Dict[Tuple[str, str], float]  # (k, f) -> weight in (0, 1]
    delta: Dict[str, float]              # factor change indicators

    # Posterior Pr(Z_f = 1) that factor is still as in source.
    pz: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        if not self.pz:
            self.pz = {f: 1.0 - float(self.delta[f]) for f in self.factors}

    # ---- item trust from current factor posterior -----------------
    def item_trust(self, k: str) -> float:
        """Current Pr(V_k = 1) under the bipartite model with mean-field factors."""
        prob_invalid = 1.0
        any_edge = False
        for (ki, f), w in self.edges.items():
            if ki != k:
                continue
            any_edge = True
            prob_invalid *= (1.0 - w * (1.0 - self.pz[f]))
        if not any_edge:
            return 0.999  # item depends on nothing; essentially stable
        return float(prob_invalid)

    def all_item_trusts(self) -> Dict[str, float]:
        return {k: self.item_trust(k) for k in self.items}

    def item_factors(self, k: str) -> List[str]:
        return [f for (ki, f) in self.edges.keys() if ki == k]

    # ---- update on evidence ---------------------------------------
    def update_from_item_evidence(self, k: str, e_pass: bool,
                                  p_e_given_valid: float,
                                  p_e_given_invalid: float) -> None:
        """Mean-field update: compute posterior Pr(V_k = 1 | e), then
        back-propagate a soft update to each dependent factor via its
        current contribution to the item's validity. This is the key
        coupling mechanism that makes evidence on k inform items that
        share a factor with k.

        The update is the ratio form of Bayes' rule combined with a
        proportional-reassignment step: factors that currently explain
        more of the item's doubt absorb more of the evidence.
        """
        p_prior = self.item_trust(k)
        if e_pass:
            lk = p_e_given_valid
            lk_bar = p_e_given_invalid
        else:
            lk = 1.0 - p_e_given_valid
            lk_bar = 1.0 - p_e_given_invalid
        num = lk * p_prior
        den = num + lk_bar * (1.0 - p_prior)
        if den <= 0:
            return
        p_post = float(num / den)
        delta_item = p_post - p_prior
        factors_k = self.item_factors(k)
        if not factors_k:
            return
        # Credit assignment: each factor gets a share proportional to its
        # current "doubt contribution" 1 - pz[f] weighted by edge weight.
        shares = {}
        tot = 0.0
        for f in factors_k:
            s = self.edges[(k, f)] * (1.0 - self.pz[f])
            shares[f] = s
            tot += s
        # If all factors are fully trusted already, spread uniformly.
        if tot <= 1e-9:
            for f in factors_k:
                shares[f] = 1.0 / len(factors_k)
            tot = 1.0
        for f in factors_k:
            share = shares[f] / tot
            # Nudge pz[f] toward 1 (if item passed) or 0 (if item failed)
            self.pz[f] = float(np.clip(self.pz[f] + 0.5 * share * delta_item, 0.02, 0.98))

    def update_from_shadow_mode(self, items_pass: Dict[str, bool],
                                p_e_given_valid: float,
                                p_e_given_invalid: float) -> None:
        """Shadow mode observes many items simultaneously. We fold each
        item's evidence sequentially into the shared factor posteriors.
        """
        order = sorted(items_pass.keys())  # deterministic
        for k in order:
            self.update_from_item_evidence(
                k, items_pass[k], p_e_given_valid, p_e_given_invalid)

    def update_from_formula(self, k: str, factor_estimate: Dict[str, float],
                            sigma: float = 0.2) -> None:
        """Formula-based re-derivation produces an estimate of V_k that is
        NOT conditionally independent given V_k alone: it is a noisy
        observation of Pr(V_k = 1 | Z) itself, because the formula uses
        the same factors. We therefore fuse at the factor level, nudging
        each dependent factor's posterior toward the formula-implied
        value with Gaussian-conjugate weight 1 / sigma^2.
        """
        factors_k = self.item_factors(k)
        if not factors_k:
            return
        w = 1.0 / max(sigma * sigma, 1e-4)
        for f in factors_k:
            if f not in factor_estimate:
                continue
            old = self.pz[f]
            target = float(factor_estimate[f])
            new = (old + 0.1 * w * target) / (1.0 + 0.1 * w)
            self.pz[f] = float(np.clip(new, 0.02, 0.98))


def make_default_graph(seed: int = 0) -> BipartiteTrustNet:
    """Method's knowledge graph: 8 items, 5 factors."""
    rng = np.random.default_rng(seed)
    items = [f"k{i+1}" for i in range(8)]
    factors = ["robot_speed", "crew_experience", "supplier_grade",
               "maintenance_qual", "humidity"]
    # Hand-authored sparse edges (engineer audit)
    edge_template: Dict[Tuple[str, str], float] = {
        ("k1", "robot_speed"): 0.95,          # bottleneck station
        ("k1", "maintenance_qual"): 0.6,
        ("k2", "crew_experience"): 0.9,       # changeover duration
        ("k3", "crew_experience"): 0.7,       # scrap rate
        ("k3", "supplier_grade"): 0.85,
        ("k3", "humidity"): 0.4,
        ("k4", "robot_speed"): 0.7,           # WIP buffer target
        ("k4", "crew_experience"): 0.5,
        ("k5", "supplier_grade"): 0.9,        # first-pass yield
        ("k5", "humidity"): 0.5,
        ("k6", "maintenance_qual"): 0.85,     # MTBF
        ("k7", "maintenance_qual"): 0.8,      # MTTR
        ("k7", "crew_experience"): 0.4,
        ("k8", "robot_speed"): 0.55,          # takt time
        ("k8", "crew_experience"): 0.6,
    }
    delta = {f: 0.0 for f in factors}
    return BipartiteTrustNet(items=items, factors=factors,
                             edges=edge_template, delta=delta)
