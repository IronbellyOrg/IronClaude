"""Item-to-reviewer assignment (DESIGN 7, REQ-20).

Inputs are the selected items (select.py rows: `item_id`, `class`, `priority`, `route`, `evidence`), a panel name from
config/panels.json, the set of available reviewer ids and the seed. Roles: `S` the search reviewer, `L1` and `L2` the
two lunas; each has a `rid` and a `cap`. Nothing here reads a clock or the network; the same input gives the same output.

    replica target   1 for an item with empty evidence, else 2; every item 1 when fewer than three reviewers are
                     available (the caps are not raised)
    pass 1           descending priority; a search item goes to S when S is allowed and under cap, else the lighter
                     luna; a read item goes to the lighter luna (ties: L1)
    pass 2           descending priority, items with target 2: the lighter luna that is not the first reviewer, else S
                     (allowed, under cap); never the first reviewer; none free -> `replica_dropped`
    cap_slots        an item that cannot get even one reviewer is `dropped:cap_slots`
    S allowed        the panel's `classes` is "any", or the item has evidence and its class is in the list
                     (haiku: C4, C5, C8)
    order            each reviewer's items are shuffled with random.Random(f"{seed}:{rid}")

Gaps in DESIGN 7.2 resolved here (all consistent with DD-4, REQ-20 and 7.3):
  G1  A pass-1 read item whose two lunas are both at cap (7.2 names only the lighter luna) goes to S if S is allowed
      and under cap, so it keeps a reviewer instead of being dropped; a pass-1 search item that cannot go to S
      uses the lighter luna, and then the other luna, for the same reason.
  G2  "Lighter luna" ignores a luna that is at cap or is the first reviewer; the choice is by current load, ties L1.
      For pass 2, the search rule ("the lighter luna") and the read rule ("the other luna, then S") reduce to one
      order: lunas other than the first by load, then S. When the first reviewer is S, both lunas compete by load.
  G3  A reviewer that is not in `available` takes nothing and has no entry; with S missing no item has S allowed.
      With fewer than three available reviewers (including one or none) the same two passes run with every target 1.
  G4  The pre-launch unavailable case (7.3, "the harness re-runs assign") is `assign(..., available=...)`.
      The after-launch failure (7.3, REQ-20) is `fail`: survivors keep exactly their lists and loads, the failed
      reviewer's items are listed in `lost_replica`; nothing is re-assigned and nothing can exceed a cap.
  G5  Pass 1 and pass 2 both visit items by descending priority; equal priorities keep the input order (items.json
      order, already tie-broken by select.py).
  G6  The pass-2 order alone can strand a slot: with 7 search and 5 read items the lunas can fill with other second
      replicas before the last search item's second is placed, while S still has room (S ends at 7, sum 23), which
      contradicts the 8, 8, 8 of the worked check and of REQ-20. A second replica that no reviewer can take is
      therefore retried once after pass 2: another item's second replica that sits on a reviewer who may take it is
      moved to a free reviewer (never the first one, never a cap exceeded), and the stranded item takes the freed
      slot. Only second replicas move; first replicas never do. It is listed in `replica_dropped` only if no such
      move exists.
"""

from __future__ import annotations

import copy
import json
import os
import random
from dataclasses import dataclass, field
from pathlib import Path

PANELS_PATH = Path(__file__).resolve().parents[1] / "config" / "panels.json"
ROLES = ("S", "L1", "L2")
STATUS_CAP_SLOTS = "dropped:cap_slots"


def load_panels(path=None) -> dict:
    """The `panels` mapping of config/panels.json: {panel: {label, S, L1, L2}}.

    SW_PANELS names another panel file for one schedule run (bin/run-schedule.sh writes the spike fallback caps into a copy;
    bin/common.sh accepts it only under /tmp/ or SW/runs/). Without it the file is config/panels.json.
    """
    p = Path(path) if path else Path(os.environ.get("SW_PANELS") or PANELS_PATH)
    return json.loads(p.read_text(encoding="utf-8"))["panels"]


@dataclass
class Assignment:
    panel: str
    seed: int | str
    caps: dict  # rid -> cap, available reviewers only
    reviewers: dict  # rid -> item ids in the shuffled print order
    item_reviewers: dict  # item id -> reviewer ids (first, then second)
    replicas: dict  # item id -> replica target (1 or 2)
    replica_dropped: list = field(default_factory=list)
    dropped: dict = field(default_factory=dict)  # item id -> "dropped:cap_slots"
    lost_replica: list = field(default_factory=list)
    failed: list = field(default_factory=list)

    @property
    def loads(self) -> dict:
        return {rid: len(ids) for rid, ids in self.reviewers.items()}

    def to_json(self) -> dict:
        return {
            "panel": self.panel,
            "seed": self.seed,
            "caps": dict(self.caps),
            "loads": self.loads,
            "reviewers": {r: list(v) for r, v in self.reviewers.items()},
            "item_reviewers": {i: list(v) for i, v in self.item_reviewers.items()},
            "replicas": dict(self.replicas),
            "replica_dropped": list(self.replica_dropped),
            "dropped": dict(self.dropped),
            "lost_replica": list(self.lost_replica),
            "failed": list(self.failed),
        }


def s_allowed(item: dict, s_cfg: dict) -> bool:
    """May the search reviewer take this item (DESIGN 7.1: the haiku panel only takes evidence-bearing C4, C5, C8)."""
    classes = s_cfg.get("classes", "any")
    if classes == "any":
        return True
    return bool(item.get("evidence")) and item["class"] in classes


def assign(items, panel="primary", available=None, seed=0, panels=None) -> Assignment:
    """Assign `items` to the reviewers of `panel` (DESIGN 7.2) and shuffle each reviewer's list (7.3)."""
    cfg = (panels if panels is not None else load_panels())[panel]
    role_of = {cfg[r]["rid"]: r for r in ROLES}
    rids = [
        cfg[r]["rid"] for r in ROLES if available is None or cfg[r]["rid"] in available
    ]
    caps = {rid: cfg[role_of[rid]]["cap"] for rid in rids}
    s_rid = cfg["S"]["rid"] if cfg["S"]["rid"] in rids else None
    lunas = [
        cfg[r]["rid"] for r in ("L1", "L2") if cfg[r]["rid"] in rids
    ]  # L1 first: the tie-break
    load = dict.fromkeys(rids, 0)
    given: dict[str, list] = {rid: [] for rid in rids}
    of_item: dict[str, list] = {}
    order = sorted(range(len(items)), key=lambda n: (-items[n]["priority"], n))
    ordered = [items[n] for n in order]
    full = len(rids) >= 3
    target = {
        it["item_id"]: (2 if full and it.get("evidence") else 1) for it in ordered
    }

    def lighter(exclude=()):
        free = [r for r in lunas if r not in exclude and load[r] < caps[r]]
        return sorted(free, key=lambda r: (load[r], lunas.index(r)))

    def s_free(it, exclude=()):
        ok = (
            s_rid
            and s_rid not in exclude
            and load[s_rid] < caps[s_rid]
            and s_allowed(it, cfg["S"])
        )
        return [s_rid] if ok else []

    def put(it, rid):
        load[rid] += 1
        given[rid].append(it["item_id"])
        of_item.setdefault(it["item_id"], []).append(rid)

    dropped, replica_dropped = {}, []
    for it in ordered:  # pass 1
        pick = (
            s_free(it) + lighter()
            if it["route"] == "search"
            else lighter() + s_free(it)
        )  # G1: both lists fall back to the other kind of reviewer
        if pick:
            put(it, pick[0])
        else:
            dropped[it["item_id"]] = STATUS_CAP_SLOTS
    for it in ordered:  # pass 2
        iid = it["item_id"]
        if target[iid] < 2 or iid in dropped:
            continue
        first = of_item[iid]
        pick = lighter(first) + s_free(it, first)  # G2
        if pick:
            put(it, pick[0])
        else:
            replica_dropped.append(iid)

    def make_room(it) -> bool:
        """G6: free a slot for `it`'s second replica by moving another item's second replica elsewhere."""
        first = of_item[it["item_id"]]
        for y in rids:
            if y in first or (y == s_rid and not s_allowed(it, cfg["S"])):
                continue
            for x in ordered:
                who = of_item.get(x["item_id"], [])
                if x is it or len(who) != 2 or who[1] != y:
                    continue
                to = (lighter(who) + s_free(x, who))[:1]
                if to:
                    load[y] -= 1
                    given[y].remove(x["item_id"])
                    who[1] = to[0]
                    load[to[0]] += 1
                    given[to[0]].append(x["item_id"])
                    put(it, y)
                    return True
        return False

    by_id = {it["item_id"]: it for it in ordered}
    replica_dropped = [i for i in replica_dropped if not make_room(by_id[i])]

    for rid in rids:  # shuffle once, after both passes (7.3)
        random.Random(f"{seed}:{rid}").shuffle(given[rid])
    return Assignment(
        panel=panel,
        seed=seed,
        caps=caps,
        reviewers=given,
        item_reviewers=of_item,
        replicas=target,
        replica_dropped=replica_dropped,
        dropped=dropped,
    )


def fail(a: Assignment, rid: str) -> Assignment:
    """A reviewer failed after launch (DESIGN 7.3): the survivors keep exactly their lists, so no load grows.

    The failed reviewer's items are listed in `lost_replica`; nothing is re-assigned (REQ-20)."""
    if rid not in a.reviewers:
        raise ValueError(f"{rid} is not a reviewer of this assignment")
    b = copy.deepcopy(a)
    b.lost_replica += [i for i in b.reviewers.pop(rid) if i not in b.lost_replica]
    b.caps.pop(rid, None)
    b.failed.append(rid)
    for iid, who in b.item_reviewers.items():
        if rid in who:
            b.item_reviewers[iid] = [r for r in who if r != rid]
    return b
