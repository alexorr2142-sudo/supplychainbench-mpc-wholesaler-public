"""One-shot official runs of the FROZEN policy. Upstream evaluators unmodified; our provider is injected.
usage: python official.py standard | heldout"""
import json, sys
sys.path.insert(0, "/tmp/scb")
from pathlib import Path
from scb_attempt import frozen, schema, envs
OUT = Path("results"); OUT.mkdir(exist_ok=True)
if sys.argv[1] == "standard":
    import supplychainbench.eval as ev
    from supplychainbench.providers.base import ActionProvider, ActionResponse
    class Prov(ActionProvider):
        provider_kind = "agent"
        def reset_episode(self, job, episode, observation): self.p = frozen.standard_policy()
        def act(self, system, user, observation):
            q = int(self.p.act(schema.from_standard(observation))); return ActionResponse(q, raw=json.dumps({"quantity": q}))
    ev.create_provider = lambda model, **kw: Prov()
    res = ev.evaluate("agent:scb-attempt-frozen", "standard", output=OUT / "standard_frozen.json", resume=False)
    print(json.dumps(res["aggregate"], indent=1))
else:
    from eval.run_eval import evaluate, NaivePolicy, BaseStockPolicy, read_held_out_seeds, training_seeds, tune_base_stock, score_against_naive
    seeds = read_held_out_seeds(); assert not set(seeds) & set(training_seeds())
    lvl = tune_base_stock(); assert lvl == frozen.SERIAL_LEVEL, lvl
    r = {"naive": evaluate(NaivePolicy(), seeds), "repo_base_stock": evaluate(BaseStockPolicy(lvl), seeds),
         "scb_attempt_frozen": evaluate(envs.SerialBatch(frozen.SerialBaseStock), seeds)}
    n = r["naive"]["mean_total_supply_chain_cost"]
    for v in r.values(): v["benchmark_score_0_to_100"] = score_against_naive(v["mean_total_supply_chain_cost"], n)
    json.dump(r, open(OUT / "heldout_frozen.json", "w"), indent=1); print(json.dumps(r, indent=1))
