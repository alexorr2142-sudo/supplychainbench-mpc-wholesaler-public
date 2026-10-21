# [Draft — not submitted] Non-LLM wholesaler policy: 76.78 on `standard` (16/16 clean)

Submitter: Solved Supply Lab.

## Summary and caveats (please read first)
This beats the `agent:adaptive` reference on the 16 official seeds (76.78 vs 73.86), but **not significantly**, and results
on fresh seeds are **mixed**:
- Per-seed gain vs adaptive on the official seeds: 14.8 ± 10.3 SE (~1.4 SE). 11 wins / 0 ties / 5 losses, 6 wins by 1.0.
- The gain is concentrated: shifted_mean_doubled_variance +256.5 cost units, burst_and_collapse −27.5 (worse);
  two seeds carry 232.5 of the 236.5 total gain.
- On 100 fresh seeds (25/bucket, disjoint from all benchmark seeds): −4.1% cost vs adaptive (16.1 ± 3.8 SE, 67/100 wins),
  but worse in in_distribution (−1.8%) and burst_and_collapse (−2.3%); the gain comes from shifted_mean (+7.8%).
- The 16 official seeds are public; we tuned only on separate fresh design seeds and ran the official suite once.
- On the serial `eval/held_out_seeds.json` protocol it only matches the tuned base-stock (51.58).
No LLM, no GPU, no API calls.

## Method
Wholesaler-only, role-local observation (no capacity, demand law or seed is read). Exponentially smoothed demand forecast
(α = 0.15) plus a newsvendor order-up-to target: L·f + z·σ̂·√L with L = 3, σ̂ from the last 16 forecast residuals and
z at the cost-ratio quantile b/(b+h) = 2/3. Selected from a pre-registered grid (288 points) on 48 fresh design seeds,
confirmed on another 48 (gain over adaptive > 2 SE on both), then frozen before the single official run.

## Results
| Suite | Score | Mean cost | Clean |
|---|---|---|---|
| standard (official evaluator) | 76.78 | 374.06 | 16/16 |
| agent:adaptive (reference, upstream) | 73.86 | 388.84 | 16/16 |
| serial held_out_seeds (100) | 51.58 | 1624.97 (system) | n/a, 0 format failures |

## Reproduce
```bash
git clone https://github.com/ConstantinVictorBeatErtel/Supply_Chain_Bench /tmp/scb && git -C /tmp/scb checkout 20236bc
python -m venv .venv && . .venv/bin/activate && pip install -e /tmp/scb numpy
cd scb-attempt && python official.py standard   # writes results/standard_frozen.json
python official.py heldout                       # writes results/heldout_frozen.json
```
The provider is injected by replacing `supplychainbench.eval.create_provider`; evaluator, environment and scoring are unmodified.

## License
Our code: MIT (to be added with the submitter's copyright line). The benchmark (Supply_Chain_Bench) is MIT © 2026 Consti Ertel;
no upstream code is copied — we import it unmodified.
