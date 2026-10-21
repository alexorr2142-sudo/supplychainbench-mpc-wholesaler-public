"""Episode runners for both protocols using upstream simulators unmodified."""
import sys; sys.path.insert(0, "/tmp/scb")
from . import schema
def run_standard(policy, bucket, seed_hex):
    from supplychainbench.suites import SuiteEpisode, build_episode
    from beer_distribution_rl.research.live_y_domain_randomized_grpo_v1.environment import research_spec
    job = SuiteEpisode("standard", seed_hex, 0, bucket, research_spec(seed_hex, bucket=bucket), {}, None, None)
    e = build_episode(job); o = e.start()
    while not e.done:
        r = e.place_order(int(policy.act(schema.from_standard(o))))
        if not r["done"]: o = r["next_observation"]
    g = e.outcome["grade"]; return float(g["primary"]["local_total_cost"]), bool(g.get("protocol_clean"))
class SerialBatch:
    """run_eval.BatchPolicy adapter: one policy instance per episode, built by `factory`."""
    def __init__(self, factory, name="scb_attempt"): self.factory, self.name, self.failures, self.calls, self.pols = factory, name, 0, 0, None
    def orders(self, observations):
        if self.pols is None or observations[0]["t"] == 0: self.pols = [self.factory() for _ in observations]
        self.calls += len(observations); return [int(p.act(schema.from_serial(o))) for p, o in zip(self.pols, observations)]
def run_serial(factory, seeds):
    from eval.run_eval import evaluate
    return evaluate(SerialBatch(factory), seeds)
