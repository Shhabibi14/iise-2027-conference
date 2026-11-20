"""
Five-station serial-flow line DES testbed.

A lightweight SimPy model of a five-station serial line with stochastic
processing times, random breakdowns, and setup-dependent changeovers.
It produces the physical observables used by two of the paper's knowledge
items (bottleneck station and mean changeover duration). The remaining
knowledge items derive from engineering tolerances on these observables
and are evaluated against the simulator's ground truth in run_experiments.

References
----------
[11] J. Banks, J. S. Carson, B. L. Nelson, and D. M. Nicol,
     Discrete-Event System Simulation, 5th ed. Pearson, 2010.
[10] K. G. Kempf, "Intel five-machine six-step mini-fab description,"
     Intel Corporation, Chandler, AZ, 1994 (five-machine topology
     reference; Kempf's MiniFab is the inspiration for the five-station
     layout used here, not literal MiniFab parameters).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np
import simpy


@dataclass
class StationParams:
    name: str
    mean_proc_time: float  # minutes per part
    cv_proc_time: float    # coefficient of variation
    mtbf_min: float        # mean time between failures, minutes
    mttr_min: float        # mean time to repair, minutes
    changeover_min: float  # fixed setup when product changes


@dataclass
class LineConfig:
    stations: List[StationParams]
    product_mix: List[str] = field(default_factory=lambda: ["A", "B"])
    changeover_prob: float = 0.08  # per part, probability next part is a different product

    @staticmethod
    def default() -> "LineConfig":
        """Illustrative five-station serial line. Parameters set to realistic ranges.
        Ratios between stations follow the 2-3-2-3-2 pattern used in textbook
        serial lines in [11]. Absolute values are not calibrated to a real plant.
        """
        return LineConfig(stations=[
            StationParams("S1", 1.8, 0.25, 480, 15, 2.0),
            StationParams("S2", 2.4, 0.30, 360, 18, 3.0),
            StationParams("S3", 1.9, 0.25, 420, 12, 2.0),
            StationParams("S4", 2.5, 0.35, 300, 20, 3.5),
            StationParams("S5", 1.7, 0.20, 540, 10, 1.5),
        ])


def _lognormal_sample(rng: np.random.Generator, mean: float, cv: float) -> float:
    if cv <= 0:
        return mean
    sigma2 = np.log(1.0 + cv ** 2)
    mu = np.log(max(mean, 1e-9)) - 0.5 * sigma2
    return float(rng.lognormal(mu, np.sqrt(sigma2)))


def _station_process(env: simpy.Environment, station: StationParams,
                     in_q: simpy.Store, out_q: simpy.Store,
                     rng: np.random.Generator, stats: Dict, last_product: Dict):
    """One SimPy process per station."""
    next_failure = env.now + rng.exponential(station.mtbf_min)
    while True:
        part = yield in_q.get()
        # Setup if product changed
        current = last_product.get(station.name, part["product"])
        if current != part["product"]:
            yield env.timeout(station.changeover_min)
            stats[station.name]["changeovers"] += 1
            stats[station.name]["changeover_time"] += station.changeover_min
        last_product[station.name] = part["product"]
        # Breakdown check (coarse model: if next_failure due before next proc end, repair first)
        proc_time = _lognormal_sample(rng, station.mean_proc_time, station.cv_proc_time)
        if env.now + proc_time > next_failure:
            repair_time = rng.exponential(station.mttr_min)
            yield env.timeout(max(0.0, next_failure - env.now))
            yield env.timeout(repair_time)
            stats[station.name]["breakdown_time"] += repair_time
            stats[station.name]["breakdowns"] += 1
            next_failure = env.now + rng.exponential(station.mtbf_min)
        yield env.timeout(proc_time)
        stats[station.name]["busy_time"] += proc_time
        stats[station.name]["parts_out"] += 1
        yield out_q.put(part)


def _source(env: simpy.Environment, first_q: simpy.Store, cfg: LineConfig,
            rng: np.random.Generator, n_parts: int):
    last = cfg.product_mix[0]
    for i in range(n_parts):
        if rng.random() < cfg.changeover_prob:
            last = cfg.product_mix[(cfg.product_mix.index(last) + 1) % len(cfg.product_mix)]
        yield first_q.put({"id": i, "product": last})
    # Sentinel so downstream stations stop naturally in the run
    yield env.timeout(0)


def run_line(cfg: LineConfig, n_parts: int = 400, seed: int = 0) -> Dict[str, float]:
    """Run the line once. Return a dict of KPIs used as physical ground truth.

    KPIs:
      throughput_per_min : total parts completed divided by sim time
      bottleneck         : station name with the highest utilization
      mean_changeover    : average changeover duration seen across stations
      mean_breakdown_min : total breakdown time per station, mean
    """
    rng = np.random.default_rng(seed)
    env = simpy.Environment()
    queues = [simpy.Store(env) for _ in range(len(cfg.stations) + 1)]
    stats = {s.name: {"parts_out": 0, "busy_time": 0.0,
                      "breakdowns": 0, "breakdown_time": 0.0,
                      "changeovers": 0, "changeover_time": 0.0}
             for s in cfg.stations}
    last_product: Dict[str, str] = {}
    env.process(_source(env, queues[0], cfg, rng, n_parts))
    for i, s in enumerate(cfg.stations):
        env.process(_station_process(env, s, queues[i], queues[i + 1], rng, stats, last_product))
    # Run until last station has processed all n_parts or a time cap hits
    time_cap = n_parts * max(s.mean_proc_time for s in cfg.stations) * 2.5
    while stats[cfg.stations[-1].name]["parts_out"] < n_parts and env.now < time_cap:
        env.run(until=env.now + 50)
    total_time = max(env.now, 1.0)
    util = {name: s["busy_time"] / total_time for name, s in stats.items()}
    bottleneck = max(util, key=util.get)
    total_co_events = sum(s["changeovers"] for s in stats.values())
    total_co_time = sum(s["changeover_time"] for s in stats.values())
    mean_changeover = total_co_time / max(total_co_events, 1)
    mean_breakdown_min = np.mean([s["breakdown_time"] for s in stats.values()])
    throughput = stats[cfg.stations[-1].name]["parts_out"] / total_time
    return {
        "throughput_per_min": throughput,
        "bottleneck": bottleneck,
        "mean_changeover": mean_changeover,
        "mean_breakdown_min": float(mean_breakdown_min),
        "sim_time": total_time,
    }


def perturb_config(cfg: LineConfig, factor_deltas: Dict[str, float],
                   rng: np.random.Generator) -> LineConfig:
    """Apply factor-level change intensities to produce a target-environment config.

    factor_deltas keys recognized here:
      robot_speed      : lower cycle time at S2 and S4 by up to 25% at delta=1
      crew_experience  : raise CV of processing time at all stations by up to 60%
      supplier_grade   : raise mean breakdowns (lower MTBF) by up to 40%
      maintenance_qual : raise mean repair time (MTTR) by up to 50%
      humidity         : small randomized perturbation to scrap-adjacent timing
    """
    stations = []
    for s in cfg.stations:
        mt = s.mean_proc_time
        cv = s.cv_proc_time
        mtbf = s.mtbf_min
        mttr = s.mttr_min
        if s.name in ("S2", "S4"):
            mt *= (1.0 - 0.25 * factor_deltas.get("robot_speed", 0.0))
        cv *= (1.0 + 0.60 * factor_deltas.get("crew_experience", 0.0))
        mtbf *= (1.0 - 0.40 * factor_deltas.get("supplier_grade", 0.0))
        mttr *= (1.0 + 0.50 * factor_deltas.get("maintenance_qual", 0.0))
        # small humidity noise
        mt *= (1.0 + 0.05 * factor_deltas.get("humidity", 0.0) * rng.normal(0, 1))
        stations.append(StationParams(s.name, max(mt, 0.1), max(cv, 0.01),
                                      max(mtbf, 10), max(mttr, 1), s.changeover_min))
    return LineConfig(stations=stations, product_mix=cfg.product_mix,
                      changeover_prob=cfg.changeover_prob)


if __name__ == "__main__":
    base = LineConfig.default()
    kpis = run_line(base, n_parts=300, seed=1)
    print("baseline run KPIs:", kpis)
