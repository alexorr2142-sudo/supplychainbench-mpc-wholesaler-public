# Results of frozen policy bd868c8 (one-shot runs, 2026-10-21 CDT)

## Caveats first
- **Not significant on the official seeds.** Per-seed gain vs agent:adaptive on the 16 standard seeds: 14.8 ± 10.3 SE
  (~1.4 SE; our own adoption bar was 2 SE). Wins/ties/losses 11/0/5; 6 of the 11 wins are by exactly 1.0 cost unit.
- **Concentrated gain.** Cost change by bucket (adaptive − frozen): shifted_mean_doubled_variance +256.5,
  in_distribution +3.5, canonical_held_out_step +4.0, burst_and_collapse −27.5 (worse). Total gain 236.5, of which two
  seeds carry 232.5 (141.0 and 91.5). Effective number of contributing seeds (Σ|g|)²/Σg² ≈ 3.2 of 16.
- Note: "verifier-fresh" is just the label of the fresh-seed key; it is kept verbatim so the 100 seeds can be regenerated exactly.
- **Mixed on fresh seeds.** 100 fresh non-public seeds (25/bucket, sha256 of fresh-seed key "verifier-fresh|bucket|i", disjoint
  from all benchmark and design seeds; re-checked here): total cost −4.1% vs adaptive base-stock, paired gain 16.1 ± 3.8 SE,
  67/100 wins. By bucket: shifted_mean +7.8% better (24/25 wins), canonical +0.6% (25/25), in_distribution −1.8% worse
  (10/25), burst_and_collapse −2.3% worse (8/25).
- **The 16 official seeds are public.** Selection used only disjoint design seeds and the suite was run once, but nothing
  upstream enforces that.
- **Held-out serial only matches base-stock.** No candidate beat the repo-tuned base-stock on serial design seeds, so the frozen
  serial policy *is* that base-stock: 51.58 (= repo base_stock; naive 50). No improvement there.
- Tuning notes: chosen α = 0.15 is the lower edge of the grid; the taper option is inert (taper 0/1 give identical costs).
- Correction: an earlier report said "many seeds tie". That was wrong — there are 0 ties between frozen and reference;
  what I saw were 6 episodes at 180 vs the reference's 181 (wins by 1.0).
- Pre-registration timestamp: PREREGISTRATION.md says "~09:50 CDT" but was committed at 09:35:38 CDT (b70b6a5). The commit
  time is authoritative; commit order (b70b6a5 → bd868c8 → 25ed551) shows it predates the policy commits, but git cannot prove
  no code existed beforehand. The file is left unchanged on purpose.

## Scores
Standard (official supplychainbench.eval loop, provider injected, evaluator unmodified): **76.78**, mean cost 374.06, 16/16 clean.
Comparison on the same official hindsight-normalized metric (upstream results/leaderboard.md @ 20236bc):
- #1 ranked: agent:adaptive 73.86 (line 9) → +2.92, not significant (see above).
- Top ranked LLM: GPT-5.6 Sol 43.61 (16/16). Claude Opus 5: 51.28 (15/16 clean, unranked).
- (An earlier write-up compared against 62.09; that is Opus 5's adaptive-normalized mean, a different metric — withdrawn.)
Held-out serial (eval/held_out_seeds.json, 100 seeds): 51.58, identical to repo base-stock.
No reruns of the official suite, no post-hoc changes.
