"""
Baseline validation policies for comparison with the proposed agent.

B1 Full revalidation   : run a trial_run on every item, in random order,
                         until each item's posterior crosses a decision
                         threshold. Approximates the Copy Exactly! extreme.
B3 No evidence sharing : identical action rule to the proposed agent, but
                         evidence on item k does NOT update beliefs about
                         items that share factors with k. Isolates the
                         contribution of graph coupling.
B4 Random              : pick a uniformly random (activity, items) pair at
                         each step among admissible options.
B5 Max uncertainty     : pick the single item with the largest p*(1-p) and
                         run the cheapest activity that targets it (formula
                         if its factors are known, else expert).

We deliberately drop B2 (fixed-duration monitoring) since the reviewer
noted it is an extreme policy and tends to dominate B1 on cost only.
B3 is the one that isolates our graph-coupling contribution.
"""
from __future__ import annotations

import copy
from typing import Dict, List, Optional, Tuple

import numpy as np

from bayesian_trust import BipartiteTrustNet
from decision_agent import (ACTIVITY_COST, EV_PASS_VALID, EV_PASS_INVALID,
                            apply_evidence, apply_shadow_group, apply_formula,
                            classify, item_risk, TAU_USE, TAU_DISC,
                            total_risk)


# ---- B1 ------------------------------------------------------------
def b1_select(net: BipartiteTrustNet, pending: List[str],
              rng: np.random.Generator) -> Optional[Tuple[str, List[str]]]:
    """Pick any pending item (random) and run trial_run on it."""
    if not pending:
        return None
    k = pending[int(rng.integers(0, len(pending)))]
    return ("trial_run", [k])


# ---- B3 (no sharing) -----------------------------------------------
class NoShareTrustNet(BipartiteTrustNet):
    """Evidence on item k updates ONLY k's posterior, not shared factors.

    We implement this by overriding the update methods to apply a direct
    Bayes update on a per-item stored probability, bypassing the factor
    posterior entirely.
    """

    def __init__(self, base: BipartiteTrustNet):
        # Shallow init from the base graph
        super().__init__(items=list(base.items),
                         factors=list(base.factors),
                         edges=dict(base.edges),
                         delta=dict(base.delta))
        # Per-item independent posteriors seeded from the bipartite prior
        self.p_item: Dict[str, float] = {k: base.item_trust(k) for k in self.items}

    def item_trust(self, k: str) -> float:  # type: ignore[override]
        return float(self.p_item.get(k, 0.9))

    def update_from_item_evidence(self, k, e_pass, p_e_given_valid, p_e_given_invalid):  # type: ignore[override]
        p = self.p_item[k]
        if e_pass:
            num = p_e_given_valid * p
            den = num + p_e_given_invalid * (1.0 - p)
        else:
            num = (1.0 - p_e_given_valid) * p
            den = num + (1.0 - p_e_given_invalid) * (1.0 - p)
        if den > 0:
            self.p_item[k] = float(num / den)

    def update_from_shadow_mode(self, items_pass, p_e_given_valid, p_e_given_invalid):  # type: ignore[override]
        for k, e in items_pass.items():
            self.update_from_item_evidence(k, e, p_e_given_valid, p_e_given_invalid)

    def update_from_formula(self, k, factor_estimate, sigma=0.20):  # type: ignore[override]
        # Treat the formula estimate as a soft posterior-mean hint on V_k.
        est = float(np.mean(list(factor_estimate.values()))) if factor_estimate else self.p_item[k]
        w = 1.0 / max(sigma * sigma, 1e-4)
        self.p_item[k] = float(np.clip(
            (self.p_item[k] + 0.1 * w * est) / (1.0 + 0.1 * w), 0.02, 0.98))


def b3_select(net: NoShareTrustNet, pending: List[str],
              rng: np.random.Generator) -> Optional[Tuple[str, List[str]]]:
    """Same rule as the proposed agent, applied over the no-sharing net."""
    # Import here to avoid circular import at module load time
    from decision_agent import select_activity
    return select_activity(net, pending, rng)


# ---- B4 ------------------------------------------------------------
def b4_select(net: BipartiteTrustNet, pending: List[str],
              rng: np.random.Generator) -> Optional[Tuple[str, List[str]]]:
    if not pending:
        return None
    menu = ["trial_run", "formula", "expert", "shadow_mode"]
    act = menu[int(rng.integers(0, len(menu)))]
    if act == "shadow_mode":
        return ("shadow_mode", list(pending))
    if act == "expert" and len(pending) >= 3 and rng.random() < 0.5:
        idx = rng.choice(len(pending), size=3, replace=False)
        return ("expert", [pending[i] for i in idx])
    k = pending[int(rng.integers(0, len(pending)))]
    return (act, [k])


# ---- B5 ------------------------------------------------------------
def b5_select(net: BipartiteTrustNet, pending: List[str],
              rng: np.random.Generator) -> Optional[Tuple[str, List[str]]]:
    if not pending:
        return None
    k = max(pending, key=lambda kk: (lambda p: p * (1 - p))(net.item_trust(kk)))
    # Prefer cheap formula if the item has factors; otherwise expert
    factors_k = net.item_factors(k) if hasattr(net, "item_factors") else []
    if factors_k:
        return ("formula", [k])
    return ("expert", [k])
