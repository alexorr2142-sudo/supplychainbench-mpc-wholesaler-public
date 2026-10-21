"""Shared schema: one role-local observation format for both protocols (no hidden info ever read)."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Obs:
    week: int              # 1-based decision week
    weeks_remaining: int   # decision weeks left incl. this one
    settlement: int        # post-horizon weeks still costed (S: 3, H: 0)
    on_hand: int; backlog: int; inv_position: int; on_order: int
    demand: int            # incoming demand/order this week
    received: int; last_order: int
    hold: float; back: float; order_cap: int
def from_standard(o):
    s, c = o["state"], o["costs"]
    return Obs(o["week"], o["weeks_remaining"], 3, s["inventory_on_hand"], s["backlog"], s["inventory_position"], s["on_order"],
               s["incoming_demand_or_order"], s["shipment_received"], s["last_order_placed"], c["holding_per_unit"],
               c["backlog_per_unit"], o["constraints"]["maximum_order"])
def from_serial(o, horizon=20):
    return Obs(o["t"] + 1, horizon - o["t"], 0, o["inventory"], o["backlog"], o["inventory_position"], o["on_order"],
               o["last_demand_or_order"], o["last_shipment_received"], o["last_order_placed"], o["holding_cost"], o["backlog_cost"], o["order_cap"])
