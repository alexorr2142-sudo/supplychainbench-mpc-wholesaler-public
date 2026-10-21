"""Common scoring harness: per-seed costs, paired differences vs a reference, 2xSE adoption test."""
import math, statistics
from . import envs
def standard_costs(factory, seeds): return [envs.run_standard(factory(), b, s) for b, s in seeds]
def serial_costs(factory, seeds):  # per-seed system cost via one-seed batches
    return [envs.run_serial(factory, [s])["mean_total_supply_chain_cost"] for s in seeds]
def paired(cand, ref):
    d = [r - c for c, r in zip(cand, ref)]; m = statistics.fmean(d); se = statistics.stdev(d) / math.sqrt(len(d))
    return {"mean_cand": statistics.fmean(cand), "mean_ref": statistics.fmean(ref), "improvement": m, "se": se, "passes_2se": m > 2 * se}
