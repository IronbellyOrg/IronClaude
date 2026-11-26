"""Telemetry keys of a findings line and the per-class table (Tier B, built locally; MR 3.0.6, SWD 9.2 and DD-12).

A findings-v1 line may carry `class` (C1-C8 or null), `probe` (the ledger row id or null) and `src` (`ledger` for a
promoted line, otherwise null). The real merge ignores unknown keys (step 0.2 of the build), so the keys live in
`check/<rid>.checked.md` and are joined to the merged ledger by (reviewer id, finding id).

    class_of(item)          "C4.1" -> "C4"; None for anything that is not a recipe row id
    tag(finding, class_=None, probe=None, src=None)
                            a copy of the finding with the given keys set; keys given as None are left out
    per_class_table(findings, wrong=(), seconds=None)
                            {class: {"found": n, "wrong_blockers": n, "seconds": s}} for tagged findings; findings
                            without a class are counted under "none". `wrong` is the set of finding ids a judge called
                            wrong, `seconds` maps class to time; both come from the caller (this file judges nothing).
"""

from __future__ import annotations

import re

KEYS = ("class", "probe", "src")
_ROW = re.compile(r"^(C[0-9]+)\.[0-9]+$")


def class_of(item: str) -> str | None:
    m = _ROW.match(item or "")
    return m.group(1) if m else None


def tag(finding: dict, class_=None, probe=None, src=None) -> dict:
    keys = {"class": class_, "probe": probe, "src": src}
    return dict(finding, **{k: v for k, v in keys.items() if v is not None})


def per_class_table(findings, wrong=(), seconds=None) -> dict:
    table: dict[str, dict] = {}
    for f in findings:
        cls = f.get("class") or "none"
        row = table.setdefault(
            cls,
            {"found": 0, "wrong_blockers": 0, "seconds": (seconds or {}).get(cls, 0)},
        )
        row["found"] += 1
        row["wrong_blockers"] += bool(f.get("blocking") and f.get("id") in wrong)
    return table
