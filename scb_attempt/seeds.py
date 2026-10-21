"""Fresh design seeds, asserted disjoint from every seed the benchmark defines."""
import hashlib, json, random, sys
from pathlib import Path
SCB = Path("/tmp/scb"); BUCKETS = ("in_distribution", "canonical_held_out_step", "shifted_mean_doubled_variance", "burst_and_collapse")
def _forbidden_hex():
    sys.path.insert(0, str(SCB))
    from supplychainbench.suites.core import expected_seeds, derive_seed, SUITE_IDS
    from beer_distribution_rl.research.live_y_domain_randomized_grpo_v1.environment import derive_research_seed
    s = set(expected_seeds("standard"))
    for b in BUCKETS: s |= {derive_research_seed(b, i) for i in range(1000)}
    for su in SUITE_IDS: s |= {derive_seed(su, i) for i in range(1000)} | {derive_seed(su, i, phase=p) for p in ("adaptation", "test", "world") for i in range(1000)}
    return s
def _forbidden_int():
    sys.path.insert(0, str(SCB)); from eval.run_eval import read_held_out_seeds, training_seeds
    return set(read_held_out_seeds()) | set(training_seeds())
def standard_design(tag, n=12):
    out = [(b, hashlib.sha256(f"scb-attempt|design|{tag}|{b}|{i}".encode()).hexdigest()[:16]) for b in BUCKETS for i in range(n)]
    assert not ({s for _, s in out} & _forbidden_hex()); return out
def serial_design(rng_seed, n=100):
    r = random.Random(rng_seed); out = [r.randrange(1, 2**63) for _ in range(n)]
    assert not (set(out) & _forbidden_int()); return out
