# SupplyChainBench non-LLM attempt: pre-registration (2026-10-21 ~09:50 CDT, before any policy code or tuning)
Upstream: ConstantinVictorBeatErtel/Supply_Chain_Bench @ 20236bc (MIT), local clone /tmp/scb, unmodified. $0: no LLM, no GPU.

## Protocols
S = official `standard` suite (Y network, wholesaler, 36 weeks, capacity 400 hidden, 16 seeds in 4 buckets).
    Score = 100 * sum(hindsight ref cost) / sum(policy cost) over clean episodes; official only if 16/16 clean.
    Reference to beat: repo's `agent:adaptive` = 73.86 (results/standard/agent-adaptive.json, mean cost 388.84).
    Board top excluding the reference: committed capacity-400 board 62.09 (Claude Opus 5, 15/16 clean).
H = eval/run_eval.py serial 20-week protocol on eval/held_out_seeds.json (100 seeds), system cost,
    score = 100*naive/(naive+policy). References: naive (50) and repo-tuned base-stock (level tuned on training_seeds()).

## Candidate policies (wholesaler only; role-local observation only, capacity/demand law never read)
P0 reference: repo AdaptiveBaseStockPolicy (alpha .25, target ceil(3*f)).
P1 adaptive base-stock+: EWMA level f (alpha), EWMA abs deviation d; target = cover*f + z*d*sqrt(cover);
   order = max(0, f + beta*(target - IP)) (supply-line anchoring); end taper: last `cover` weeks target scaled to
   remaining weeks (terminal IP charge); supply-fill estimate: if received/ordered (lagged) < 0.9, inflate f by 1/fill (capacity est.).
P2 newsvendor MPC: for each q in 0..128 evaluate expected cost at t+L of IP+q-D_L with D_L from empirical
   residual bootstrap around f (window W), critical ratio b/(b+h)=2/3, same taper. 
## Tuning grid (S, design set A only)
P1: alpha {.15,.25,.4,.6} x cover {2,2.5,3,3.5,4} x z {0,.5,1} x beta {.5,1} x taper {0,1}  (240 points)
P2: alpha {.15,.25,.4,.6} x W {8,16} x L {2,3,4} x taper {0,1}  (48 points)
H: same P1 grid re-tuned on serial design set A (protocol-specific parameters, selected by mean system cost).
## Design seeds (fresh; asserted disjoint from the 16 standard seeds, derive_research_seed(bucket,0..999), suite derive_seed
   evaluation seeds 0..999, eval/held_out_seeds.json, and run_eval.training_seeds())
S-A: sha256("scb-attempt|design|A|<bucket>|<i>")[:16], i<12, 4 buckets (48). S-B: same with "B" (48, confirmation only).
H-A: random.Random(6006) 100 ints; H-B: random.Random(7007) 100 ints.
## Adoption rule
Pick the single best grid point (P1 or P2) by mean cost on A. Adopt iff its mean cost improvement over P0 (S) / over
tuned base-stock (H) exceeds 2x the SE of per-seed paired differences on BOTH A and B. Otherwise freeze P0-equivalent
and report that no candidate qualified (still run nothing on test? -> we still run the frozen policy once, as planned).
## Evaluation plan
Freeze (commit) the policy. Then exactly ONE run of the official `supplychainbench.eval` loop on `standard` (provider
injected, evaluator unmodified) and ONE run of run_eval.evaluate on held_out_seeds.json. Report all, incl. cleanliness 16/16.
No re-runs, no changes after seeing either result.
