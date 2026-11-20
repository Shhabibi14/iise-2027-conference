"""
Scenario S1 experiment runner (equipment upgrade).

For each of N_INSTANCES instances we sample:
  - which factors change and by how much (delta_f in [0, 1])
  - the method's knowledge graph G (the default in bayesian_trust.make_default_graph)
  - an ORACLE graph G_oracle that shares ~70% of its edges with G but adds
    a handful of "unknown" factors the method cannot see. The simulator's
    ground truth for each item is driven by G_oracle, which gives the
    method an honest handicap and addresses M6 (ground truth is NOT the
    same mechanism the method uses).

For each policy (proposed, B1, B3, B4, B5) and each of N_REPS replications
we run the policy loop with the SAME ground truth per (instance, rep)
to make policy comparisons paired and low-variance.

Outputs:
  code/results/raw_results.csv : one row per (instance, rep, policy)
"""
from __future__ import annotations

import copy
import csv
import os
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

from bayesian_trust import BipartiteTrustNet, make_default_graph
from decision_agent import (ACTIVITY_COST, ACTIVITY_LATENCY_H, DAILY_HOURS,
                            EV_PASS_VALID, EV_PASS_INVALID,
                            apply_evidence, apply_shadow_group, apply_formula,
                            classify, item_risk, TAU_USE, TAU_DISC,
                            total_risk, select_activity,
                            COST_WRONG_USE, COST_WRONG_DISC, COST_ESCALATE)
from baselines import NoShareTrustNet, b1_select, b3_select, b4_select, b5_select


# ------------------- experiment configuration --------------------------
N_INSTANCES = 50
N_REPS = 10
BUDGET = 500.0          # CU per instance
HORIZON_DAYS = 10
SEED = 20261119
RESULTS_DIR = Path(__file__).parent / "results"


# ------------------- ground truth via oracle graph ---------------------
def build_oracle_graph(method_net: BipartiteTrustNet,
                       rng: np.random.Generator) -> Dict:
    """Oracle graph for ground truth generation.

    Keeps ~70% of method edges (with jittered weights), drops ~30% of
    method edges, and adds 2 "hidden" factors the method does not have,
    each wired to a random subset of items. This creates a residual
    truth mechanism the method cannot explain away via its own graph.
    """
    oracle_edges: Dict[Tuple[str, str], float] = {}
    for (k, f), w in method_net.edges.items():
        if rng.random() < 0.70:
            oracle_edges[(k, f)] = float(np.clip(w + rng.normal(0, 0.1), 0.1, 1.0))
    hidden_factors = ["hidden_1", "hidden_2"]
    for hf in hidden_factors:
        for k in method_net.items:
            if rng.random() < 0.35:
                oracle_edges[(k, hf)] = float(rng.uniform(0.3, 0.8))
    oracle_factors = list(set(method_net.factors + hidden_factors))
    return {"edges": oracle_edges, "factors": oracle_factors,
            "items": list(method_net.items)}


def sample_delta(method_net: BipartiteTrustNet, oracle: Dict,
                 rng: np.random.Generator) -> Tuple[Dict[str, float], Dict[str, float]]:
    """Sample factor change intensities for the method's factors and the
    oracle's hidden factors. We draw a scenario severity in [0, 1] and
    then let each factor either change (U[0,1]) or stay (0) under a
    coin flip whose prob tracks severity.
    """
    severity = float(rng.uniform(0.3, 0.9))
    delta_method: Dict[str, float] = {}
    for f in method_net.factors:
        if rng.random() < severity:
            delta_method[f] = float(rng.uniform(0.3, 1.0))
        else:
            delta_method[f] = float(rng.uniform(0.0, 0.2))
    delta_oracle_only: Dict[str, float] = {}
    for f in oracle["factors"]:
        if f in method_net.factors:
            continue
        if rng.random() < severity:
            delta_oracle_only[f] = float(rng.uniform(0.3, 1.0))
        else:
            delta_oracle_only[f] = float(rng.uniform(0.0, 0.2))
    return delta_method, delta_oracle_only


def sample_truth(oracle: Dict, delta_method: Dict[str, float],
                 delta_oracle_only: Dict[str, float],
                 rng: np.random.Generator) -> Dict[str, bool]:
    """For each item k, sample V_k_true from the oracle noisy-OR using both
    method-visible and hidden factor deltas.
    """
    full_delta = {**delta_method, **delta_oracle_only}
    truth: Dict[str, bool] = {}
    for k in oracle["items"]:
        prob_invalid = 1.0
        any_edge = False
        for (ki, f), w in oracle["edges"].items():
            if ki != k:
                continue
            any_edge = True
            d = full_delta.get(f, 0.0)
            # If factor is fully stable (d=0) it cannot invalidate; if fully
            # changed (d=1) it invalidates with probability w.
            prob_invalid *= (1.0 - w * d)
        p_valid = prob_invalid if any_edge else 0.999
        truth[k] = bool(rng.random() < p_valid)
    return truth


# ------------------- evidence sampling using ground truth --------------
def sample_evidence_bool(k: str, activity: str, truth: Dict[str, bool],
                         rng: np.random.Generator) -> bool:
    v = truth[k]
    if v:
        p_pass = EV_PASS_VALID[activity]
    else:
        p_pass = EV_PASS_INVALID[activity]
    return bool(rng.random() < p_pass)


# ------------------- policy loop ---------------------------------------
def run_policy(policy_name: str, method_net_init: BipartiteTrustNet,
               delta_method: Dict[str, float], truth: Dict[str, bool],
               seed: int) -> Dict:
    """Run one policy on one instance-rep. Return a results dict."""
    rng = np.random.default_rng(seed)
    # Initialize the belief network freshly
    net = copy.deepcopy(method_net_init)
    for f in net.factors:
        net.delta[f] = delta_method.get(f, 0.0)
        net.pz[f] = 1.0 - delta_method.get(f, 0.0)
    if policy_name == "B3":
        net = NoShareTrustNet(net)

    pending = list(net.items)
    verification_spent = 0.0
    day = 0
    max_decisions_per_day = 6  # cap number of activities per day

    # Policy dispatcher
    def pick(net_, pending_):
        if policy_name == "proposed":
            return select_activity(net_, pending_, rng)
        if policy_name == "B1":
            return b1_select(net_, pending_, rng)
        if policy_name == "B3":
            return b3_select(net_, pending_, rng)
        if policy_name == "B4":
            return b4_select(net_, pending_, rng)
        if policy_name == "B5":
            return b5_select(net_, pending_, rng)
        raise ValueError(policy_name)

    while pending and day < HORIZON_DAYS and verification_spent < BUDGET:
        day += 1
        day_hours = DAILY_HOURS
        actions_today = 0
        while (pending and day_hours > 0 and actions_today < max_decisions_per_day
               and verification_spent < BUDGET):
            sel = pick(net, pending)
            if sel is None:
                break
            activity, items = sel
            cost = ACTIVITY_COST[activity] * (len(items) if activity == "expert" else 1.0)
            if verification_spent + cost > BUDGET:
                break
            lat = ACTIVITY_LATENCY_H[activity]
            if lat > day_hours:
                # Activity rolls to next day
                break
            day_hours -= lat
            verification_spent += cost
            actions_today += 1
            # Apply evidence using ground truth
            if activity == "shadow_mode":
                outcomes = {k: sample_evidence_bool(k, "shadow_mode", truth, rng)
                            for k in items}
                apply_shadow_group(net, outcomes)
            elif activity == "formula":
                # Formula uses a noisy ground-truth-anchored factor estimate
                fe: Dict[str, float] = {}
                for f in net.item_factors(items[0]):
                    # Noisy estimate of Pr(Z_f = 1) based on whether the oracle
                    # sees the factor as unchanged; sigma=0.20
                    est = 1.0 - min(1.0, max(0.0, delta_method.get(f, 0.0)
                                             + rng.normal(0, 0.20)))
                    fe[f] = float(np.clip(est, 0.02, 0.98))
                apply_formula(net, items[0], fe)
            else:
                for k in items:
                    o = sample_evidence_bool(k, activity, truth, rng)
                    apply_evidence(net, k, activity, o)

            # Classify any items whose beliefs have crossed a threshold with
            # high margin; remove them from pending so the next iteration
            # focuses on the undecided set.
            still_pending: List[str] = []
            for k in list(pending):
                p = net.item_trust(k)
                if p >= TAU_USE + 0.02 or p <= TAU_DISC - 0.02:
                    pass  # consider resolved; still finalize below for scoring
                still_pending.append(k)
            pending = still_pending
            # Removal of resolved items is handled in the finalization loop
            # to keep scoring consistent; the heuristic above intentionally
            # does not prune to avoid thrashing.

    # Final classification pass
    decisions: Dict[str, str] = {}
    for k in net.items:
        decisions[k] = classify(net.item_trust(k))

    # Score decision outcomes against truth
    decision_cost = 0.0
    incorrect_reuse = 0
    escalations = 0
    for k, dec in decisions.items():
        v = truth[k]
        if dec == "use" and not v:
            decision_cost += COST_WRONG_USE
            incorrect_reuse += 1
        elif dec == "discard" and v:
            decision_cost += COST_WRONG_DISC
        elif dec == "escalate":
            decision_cost += COST_ESCALATE
            escalations += 1
    total_cost = verification_spent + decision_cost
    n_items = len(net.items)
    return {
        "policy": policy_name,
        "verification_cost": verification_spent,
        "decision_cost": decision_cost,
        "total_cost": total_cost,
        "incorrect_reuse_count": incorrect_reuse,
        "incorrect_reuse_rate": incorrect_reuse / n_items,
        "escalation_rate": escalations / n_items,
        "decision_days": day,
        "n_items": n_items,
    }


# ------------------- top-level runner ---------------------------------
def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    master_rng = np.random.default_rng(SEED)
    policies = ["proposed", "B1", "B3", "B4", "B5"]
    rows: List[Dict] = []
    t_start = time.time()
    for inst in range(N_INSTANCES):
        method_net = make_default_graph(seed=inst)
        oracle_rng = np.random.default_rng(SEED + inst * 101)
        oracle = build_oracle_graph(method_net, oracle_rng)
        delta_rng = np.random.default_rng(SEED + inst * 211)
        delta_method, delta_oracle_only = sample_delta(method_net, oracle, delta_rng)
        for rep in range(N_REPS):
            truth_rng = np.random.default_rng(SEED + inst * 1000 + rep)
            truth = sample_truth(oracle, delta_method, delta_oracle_only, truth_rng)
            for p in policies:
                res = run_policy(p, method_net, delta_method, truth,
                                 seed=SEED + inst * 10000 + rep * 100 + hash(p) % 97)
                res["instance"] = inst
                res["rep"] = rep
                rows.append(res)
        if (inst + 1) % 10 == 0:
            el = time.time() - t_start
            print(f"instance {inst+1}/{N_INSTANCES} done, elapsed {el:.1f}s")
    out_path = RESULTS_DIR / "raw_results.csv"
    cols = ["instance", "rep", "policy", "verification_cost", "decision_cost",
            "total_cost", "incorrect_reuse_count", "incorrect_reuse_rate",
            "escalation_rate", "decision_days", "n_items"]
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r[c] for c in cols})
    print(f"wrote {len(rows)} rows to {out_path}")
    print(f"total runtime {time.time()-t_start:.1f}s")


if __name__ == "__main__":
    main()
