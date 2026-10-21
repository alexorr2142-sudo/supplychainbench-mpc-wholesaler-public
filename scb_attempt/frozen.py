"""FROZEN policy (selected by tune.py on design sets only; see sweeps/)."""
from . import policies as P
STANDARD = dict(kind="P2", params=dict(f0=15.0, alpha=0.15, W=16, L=3, taper=0))   # adopted: beats P0 by >2SE on S-A and S-B
SERIAL_LEVEL = 64   # H: no candidate adopted -> repo-tuned base-stock (level from run_eval.tune_base_stock on training seeds)
def standard_policy(): return P.P2(**STANDARD["params"])
class SerialBaseStock:
    def act(self, o): return max(0, min(o.order_cap, SERIAL_LEVEL - o.inv_position))
