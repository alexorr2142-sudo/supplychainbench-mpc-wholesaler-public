"""Wholesaler policies on schema.Obs. P0 = repo reference re-expressed; P1 adaptive+; P2 newsvendor MPC."""
import math, numpy as np
from dataclasses import dataclass, field
class P0:
    def __init__(self, f0=15.0, alpha=0.25, L=3): self.f, self.a, self.L = f0, alpha, L
    def act(self, o):
        self.f = (1 - self.a) * self.f + self.a * o.demand
        return min(o.order_cap, max(0, math.ceil(self.L * self.f) - o.inv_position))
class P1:
    def __init__(self, f0=15.0, alpha=.25, cover=3.0, z=.5, beta=1.0, taper=1, L=3, fill_est=True):
        self.f, self.d, self.a, self.cover, self.z, self.beta, self.taper, self.L, self.fe = f0, 0.0, alpha, cover, z, beta, taper, L, fill_est
        self.orders, self.recv = [], []
    def act(self, o):
        err = o.demand - self.f; self.d = (1 - self.a) * self.d + self.a * abs(err); self.f += self.a * err
        f = self.f; self.recv.append(o.received)
        if self.fe and len(self.orders) > self.L + 8:      # capacity / supply-fill estimate from own pipeline only
            sent = sum(self.orders[-self.L - 8:-self.L]); got = sum(self.recv[-8:])
            if sent > 0: f *= 1.0 / min(1.0, max(2 / 3, got / sent))
        target = self.cover * f + self.z * self.d * math.sqrt(self.cover)
        if self.taper:
            left = o.weeks_remaining + o.settlement - self.L      # weeks of demand an order placed now can still serve
            target = min(target, max(0.0, left + self.L) * f + self.z * self.d)
        q = f + self.beta * (target - o.inv_position) if self.beta < 1 else target - o.inv_position
        q = int(min(o.order_cap, max(0, round(q)))); self.orders.append(q); return q
class P2:
    def __init__(self, f0=15.0, alpha=.25, W=8, L=3, taper=1):
        self.f, self.a, self.W, self.L, self.taper, self.res = f0, alpha, W, L, taper, []
    def act(self, o):
        self.res.append(o.demand - self.f); self.f += self.a * (o.demand - self.f)
        r = np.array(self.res[-self.W:]); cr = o.back / (o.back + o.hold)
        # L-week demand = L*f + sum of L bootstrap residuals (deterministic: all L-combinations approximated by quantile)
        sd = (r.std() if len(r) > 1 else 0.5 * self.f) * math.sqrt(self.L); mu = self.L * self.f
        from statistics import NormalDist
        target = mu + sd * NormalDist().inv_cdf(cr)
        if self.taper: target = min(target, max(0, o.weeks_remaining + o.settlement) * self.f)
        return int(min(o.order_cap, max(0, round(target - o.inv_position))))
