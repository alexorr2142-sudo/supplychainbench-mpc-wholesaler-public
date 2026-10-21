"""Grid search on design set A, confirmation on B (pre-registered grids). Writes sweeps/*.json."""
import itertools, json, statistics, sys
from pathlib import Path
from scb_attempt import seeds, harness, policies as P
proto = sys.argv[1]
Path("sweeps").mkdir(exist_ok=True)
G1 = [dict(alpha=a, cover=c, z=z, beta=b, taper=t) for a, c, z, b, t in itertools.product([.15,.25,.4,.6],[2,2.5,3,3.5,4],[0,.5,1],[.5,1],[0,1])]
G2 = [dict(alpha=a, W=w, L=l, taper=t) for a, w, l, t in itertools.product([.15,.25,.4,.6],[8,16],[2,3,4],[0,1])]
if proto == "S":
    A, B = seeds.standard_design("A"), seeds.standard_design("B")
    cost = lambda fac, S: [c for c, _ in harness.standard_costs(fac, S)]
    ref = lambda: P.P0(); f0 = 15.0
    cands = [("P1", g) for g in G1] + [("P2", g) for g in G2]
else:
    A, B = seeds.serial_design(6006), seeds.serial_design(7007)
    cost = harness.serial_costs; f0 = 4.0
    import sys as _s; _s.path.insert(0, "/tmp/scb"); from eval.run_eval import tune_base_stock, BaseStockPolicy
    L = tune_base_stock()   # repo procedure on repo training seeds
    class BS:
        def act(self, o): return max(0, min(128, L - o.inv_position))
    ref = BS; cands = [("P1", dict(g, L=2)) for g in G1]
mk = lambda k, g: (lambda: getattr(P, k)(f0=f0, **g))
rA = cost(ref, A); rows = []
for k, g in cands:
    c = cost(mk(k, g), A); rows.append((statistics.fmean(c), k, g))
rows.sort(key=lambda r: r[0]); best = rows[0]
cA = cost(mk(best[1], best[2]), A); cB = cost(mk(best[1], best[2]), B); rB = cost(ref, B)
out = {"protocol": proto, "ref_mean_A": statistics.fmean(rA), "top10_A": rows[:10], "best": best[1:],
       "A": harness.paired(cA, rA), "B": harness.paired(cB, rB)}
out["adopt"] = out["A"]["passes_2se"] and out["B"]["passes_2se"]
if proto == "H": out["ref_level"] = L
json.dump(out, open(f"sweeps/tune_{proto}.json", "w"), indent=1, default=str); print(json.dumps({k: out[k] for k in ("best","A","B","adopt")}, default=str))
