"""Telemetry keys of a findings line and the per-class tables (DESIGN 9.3 "Telemetry on reviewer lines", DD-12).

Reviewers set only `probe`. The check fills `class` from the item a line links to (`fill_class`: added when missing,
corrected when it differs) and writes `class`, `probe` and `src: "ledger"` on every line it promotes
(`promoted_keys`). `FND._check_finding` has no key whitelist and the merge copies only fixed fields (REQ-11), so the
keys stay in `check/<rid>.checked.md` and never reach `merged-1.md`. Analysis counts a line with `probe` set or with
`src: ledger` apart from the reviewers' free findings (REQ-42).

`per_class` turns the per-reviewer results of `ledgerv1.check_report` into one table per class (rows by verdict,
linked findings, demotions, `ok_but_finding`, promotions and refused promotions), for the extras of check.json.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping

CLASS_KEY = "class"
PROBE_KEY = "probe"
SRC_KEY = "src"
SRC_LEDGER = "ledger"
VERDICT_KEYS = ("OK", "PROBLEM", "UNSURE")


def promoted_keys(item: str, item_class: str) -> dict:
    """The three telemetry keys of a promoted line."""
    return {CLASS_KEY: item_class, PROBE_KEY: item, SRC_KEY: SRC_LEDGER}


def fill_class(obj: dict, item_class: str | None) -> str | None:
    """Set obj["class"] to the class of the item. Returns "added", "corrected" or None (already right, or no class)."""
    if not item_class:
        return None
    if CLASS_KEY not in obj:
        state = "added"
    elif obj[CLASS_KEY] != item_class:
        state = "corrected"
    else:
        return None
    obj[CLASS_KEY] = item_class
    return state


def _blank() -> dict:
    return {
        "rows": dict.fromkeys(VERDICT_KEYS, 0),
        "linked": 0,
        "demoted": 0,
        "ok_but_finding": 0,
        "promoted": 0,
        "promotion_failures": 0,
    }


def per_class(results: Iterable[dict], classes: Mapping[str, str]) -> dict:
    """{class: counts} over the per-reviewer check results; `classes` is {item id: class}. Items of no class are left out."""
    table: dict[str, dict] = {}

    def of(item: str | None) -> dict | None:
        cls = classes.get(item) if item else None
        return table.setdefault(cls, _blank()) if cls else None

    for res in results:
        for r in res["ledger"]["rows"]:
            if (t := of(r["item"])) is not None:
                t["rows"][r["verdict"]] += 1
        for f in res["findings"]:
            if f["link"] and (t := of(f["row_item"])) is not None:
                t["linked"] += 1
                t["demoted"] += f["demoted"]
                t["ok_but_finding"] += f["ok_but_finding"]
        for p in res["promoted"]:
            if (t := of(p["item"])) is not None:
                t["promoted"] += 1
        for p in res["promotion_failures"]:
            if (t := of(p["item"])) is not None:
                t["promotion_failures"] += 1
    return dict(sorted(table.items()))
