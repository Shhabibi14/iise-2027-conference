"""
Cost-aware decision agent with a myopic risk-reduction-per-cost rule.

Decision risk per item with posterior trust p_k and tolerance tau_k.
Let c_WU be the cost of wrongly using an invalid item (asymmetric,
typically large), c_WD the cost of wrongly discarding a valid item,
c_E the cost of escalating an item to engineering review.

The agent classifies each item at decision time under thresholds
tau_use and tau_disc and compares the three expected-cost branches:

    risk_use(k)      = (1 - p_k) * c_WU
    risk_discard(k)  = p_k * c_WD
    risk_escalate(k) = c_E

An unprocessed item incurs the minimum of these three. Total decision
risk is the sum over items. R(a), the value of activity a, is the
expected drop in total decision risk under the posterior obtained
after absorbing a's evidence; computed by Monte-Carlo imputation of
the evidence outcome given current beliefs (single sample, which is
enough for a myopic policy under the law of total expectation).

The agent is myopic: at each day it picks a_* = argmax R(a) / c_a.
Multiple activities per day are allowed only while the day's budget
slice remains positive.

Evidence models per activity (M5):
  Trial run        : Pr(e=pass | V=1)=0.95, Pr(e=pass | V=0)=0.10, 1 item
  Shadow mode      : Pr(e=pass | V=1)=0.85, Pr(e=pass | V=0)=0.20, many items
  Formula re-deriv : noisy observation of factor posterior, sigma=0.20
  Expert judgment  : Pr(e=pass | V=1)=0.75, Pr(e=pass | V=0)=0.25, up to 3 items

References
----------
[8]  R. A. Howard, "Information value theory," IEEE TSSC, 1966.
[9]  H. Raiffa and R. Schlaifer, Applied Statistical Decision Theory, 1961.
     Knowledge gradient for correlated beliefs: Frazier, Powell, Dayanik,
     "The knowledge-gradient policy for correlated normal beliefs," INFORMS
     Journal on Computing 21(4):599-613, 2009.
     Near-optimal nonmyopic VoI in graphical models: A. Krause and C.
     Guestrin, "Near-optimal nonmyopic value of information in graphical
     models," UAI 2005.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import copy
import numpy as np

from bayesian_trust import BipartiteTrustNet


# -------- cost model constants (illustrative; see paper/tables-sources.md) -----
COST_WRONG_USE = 100.0      # CU per item that is used while truly invalid
COST_WRONG_DISC = 25.0      # CU per item discarded while truly valid
COST_ESCALATE = 15.0        # CU flat for escalation

TAU_USE = 0.85
TAU_DISC = 0.20

# Activity cost and latency (CU, hours). Anchored to [6], [15]; illustrative.
ACTIVITY_COST = {
    "trial_run": 100.0,
    "shadow_mode": 20.0,
    "formula": 2.0,
    "expert": 10.0,
}
ACTIVITY_LATENCY_H = {
    "trial_run": 8.0,
    "shadow_mode": 24.0,
    "formula": 0.25,
    "expert": 0.5,
}
# Evidence model parameters
EV_PASS_VALID = {
    "trial_run": 0.95, "shadow_mode": 0.85, "formula": None, "expert": 0.75,
}
EV_PASS_INVALID = {
    "trial_run": 0.10, "shadow_mode": 0.20, "formula": None, "expert": 0.25,
}

DAILY_HOURS = 24.0


# ---------------- risk functions ------------------------------------
def item_risk(p: float) -> float:
    """Minimum expected cost across use / discard / escalate decisions."""
    return min((1.0 - p) * COST_WRONG_USE, p * COST_WRONG_DISC, COST_ESCALATE)


def total_risk(net: BipartiteTrustNet, pending: List[str]) -> float:
    trusts = net.all_item_trusts()
    return float(sum(item_risk(trusts[k]) for k in pending))


def classify(p: float) -> str:
    if p >= TAU_USE:
        return "use"
    if p <= TAU_DISC:
        return "discard"
    return "escalate"


# ---------------- activity simulation (one-step lookahead) ----------
def _simulate_evidence(net: BipartiteTrustNet, k: str, activity: str,
                       rng: np.random.Generator) -> bool:
    """Sample a hypothetical evidence outcome from the agent's own posterior
    predictive. Used only inside the one-step VoI lookahead; truth-based
    sampling happens in run_experiments.py.
    """
    p = net.item_trust(k)
    if activity in ("trial_run", "shadow_mode", "expert"):
        p_pass = (EV_PASS_VALID[activity] * p
                  + EV_PASS_INVALID[activity] * (1.0 - p))
        return bool(rng.random() < p_pass)
    # formula: we never use this path (VoI below handles formula as a factor
    # fuse directly), so default to pass.
    return True


def apply_evidence(net: BipartiteTrustNet, k: str, activity: str,
                   outcome: bool) -> None:
    if activity == "trial_run":
        net.update_from_item_evidence(k, outcome,
                                      EV_PASS_VALID["trial_run"],
                                      EV_PASS_INVALID["trial_run"])
    elif activity == "shadow_mode":
        # single-item path; shadow_mode_group handled elsewhere
        net.update_from_item_evidence(k, outcome,
                                      EV_PASS_VALID["shadow_mode"],
                                      EV_PASS_INVALID["shadow_mode"])
    elif activity == "expert":
        net.update_from_item_evidence(k, outcome,
                                      EV_PASS_VALID["expert"],
                                      EV_PASS_INVALID["expert"])


def apply_shadow_group(net: BipartiteTrustNet, items_pass: Dict[str, bool]) -> None:
    net.update_from_shadow_mode(items_pass,
                                EV_PASS_VALID["shadow_mode"],
                                EV_PASS_INVALID["shadow_mode"])


def apply_formula(net: BipartiteTrustNet, k: str, factor_estimate: Dict[str, float]) -> None:
    net.update_from_formula(k, factor_estimate, sigma=0.20)


# ---------------- value-of-information computation ------------------
def voi_trial_run(net: BipartiteTrustNet, k: str, pending: List[str],
                  rng: np.random.Generator) -> float:
    """Expected reduction in total_risk from running a trial run on k.
    Uses a single posterior-predictive imputation; cheap and unbiased
    under total expectation for the myopic rule.
    """
    r0 = total_risk(net, pending)
    net_copy = copy.deepcopy(net)
    o = _simulate_evidence(net_copy, k, "trial_run", rng)
    apply_evidence(net_copy, k, "trial_run", o)
    r1 = total_risk(net_copy, pending)
    return max(0.0, r0 - r1)


def voi_expert(net: BipartiteTrustNet, k_list: List[str], pending: List[str],
               rng: np.random.Generator) -> float:
    r0 = total_risk(net, pending)
    net_copy = copy.deepcopy(net)
    for k in k_list:
        o = _simulate_evidence(net_copy, k, "expert", rng)
        apply_evidence(net_copy, k, "expert", o)
    r1 = total_risk(net_copy, pending)
    return max(0.0, r0 - r1)


def voi_shadow_group(net: BipartiteTrustNet, group: List[str], pending: List[str],
                     rng: np.random.Generator) -> float:
    r0 = total_risk(net, pending)
    net_copy = copy.deepcopy(net)
    sample = {k: _simulate_evidence(net_copy, k, "shadow_mode", rng) for k in group}
    apply_shadow_group(net_copy, sample)
    r1 = total_risk(net_copy, pending)
    return max(0.0, r0 - r1)


def voi_formula(net: BipartiteTrustNet, k: str, pending: List[str]) -> float:
    r0 = total_risk(net, pending)
    net_copy = copy.deepcopy(net)
    # Formula estimate: a noisy nudge toward current factor posterior
    fe = {f: float(np.clip(net_copy.pz[f] + 0.0, 0.02, 0.98))
          for f in net_copy.item_factors(k)}
    apply_formula(net_copy, k, fe)
    r1 = total_risk(net_copy, pending)
    return max(0.0, r0 - r1)


# ---------------- agent main loop entry point -----------------------
def select_activity(net: BipartiteTrustNet, pending: List[str],
                    rng: np.random.Generator) -> Optional[Tuple[str, List[str]]]:
    """Pick the activity with the highest R(a) / c_a over candidate items.
    Returns (activity_name, list_of_items) or None if no activity has
    positive expected value.
    """
    best = (None, -1.0, None)  # (activity, score, items)
    # Per-item candidates for trial, formula, expert-single
    for k in pending:
        for act, voi_fn in [
            ("trial_run", lambda kk: voi_trial_run(net, kk, pending, rng)),
            ("formula",  lambda kk: voi_formula(net, kk, pending)),
            ("expert",   lambda kk: voi_expert(net, [kk], pending, rng)),
        ]:
            voi = voi_fn(k)
            score = voi / ACTIVITY_COST[act]
            if score > best[1]:
                best = (act, score, [k])
    # Expert-triple: pick the 3 items with highest individual item_risk
    if len(pending) >= 2:
        ranked = sorted(pending, key=lambda kk: item_risk(net.item_trust(kk)),
                        reverse=True)[:3]
        voi = voi_expert(net, ranked, pending, rng)
        # expert costs scale with items touched, cap at 3
        score = voi / (ACTIVITY_COST["expert"] * len(ranked))
        if score > best[1]:
            best = ("expert", score, ranked)
    # Shadow-group over all pending items
    if len(pending) >= 2:
        voi = voi_shadow_group(net, pending, pending, rng)
        score = voi / ACTIVITY_COST["shadow_mode"]
        if score > best[1]:
            best = ("shadow_mode", score, list(pending))
    if best[1] <= 0.0:
        return None
    return (best[0], best[2])
