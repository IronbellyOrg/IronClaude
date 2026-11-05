"""Deterministic containment matcher for inferred (INF) requirement rows.

Rule (refs/coverage-mapping.md): case-fold, strip stopwords, match a row to the single
task item where >= 0.6 of the quote's content words appear; ties -> highest ratio, then
first task in tasklist order; below threshold -> none.
"""

import json
import re
import sys

STOP = set(
    "a an the and or but nor of in on at to for from by with as is are was were be been being "
    "it its this that these those when while so no not do does did can could will would shall "
    "should may might must than then there their them they we you i he she his her our your "
    "if else into onto over under about after before also any all each every both".split()
)

ROWS = {
    "INF-001": "a new explicit opt-in environment variable CCSESSION_PERMISSIONS=default",
    "INF-002": "When set, ccsession adds no permission-bypass flag (no --dangerously-skip-permissions) on all six launch lines while keeping shim and tier-model routing",
    "INF-003": "when unset, behavior is unchanged for everyone",
    "INF-004": "Do NOT change how an empty CC_CLAUDE_FLAGS is handled (the :- default stays)",
    "INF-005": "Tests must fail on the old code: set -> no bypass flag and shim/model routing kept; unset -> unchanged",
    "INF-006": "Document the variable where ccsession's other variables are documented",
    "INF-007": "Unblocks Coder PR 458",
}


def words(text: str) -> set[str]:
    toks = re.findall(r"[a-z0-9_=\-]+", text.casefold())
    return {t.strip("-_=") for t in toks if t.strip("-_=") and t not in STOP}


def main(plan_path: str) -> None:
    text = open(plan_path, encoding="utf-8").read()
    # items: Constraints bullets + each task section
    parts = re.split(r"(?m)^## (?=Task \d+:|Constraints|Phase \d+:)", text)
    tasks = []
    for p in parts:
        m = re.match(r"Task (\d+):", p)
        if m:
            tasks.append((f"Task {m.group(1)}", p))
    out = []
    for rid, quote in ROWS.items():
        qw = words(quote)
        best = ("none", 0.0)
        for name, body in tasks:
            tw = words(body)
            ratio = len(qw & tw) / len(qw) if qw else 0.0
            if ratio > best[1]:
                best = (name, ratio)
        method = "containment" if best[1] >= 0.6 else "none"
        out.append(
            {
                "id": rid,
                "quote_words": len(qw),
                "best_task": best[0] if method != "none" else None,
                "ratio": round(best[1], 4),
                "match_method": method,
            }
        )
    matched = sum(1 for r in out if r["match_method"] != "none")
    print(json.dumps({"rows": out, "matched": matched, "total": len(out),
                      "coverage_pct_union": round(matched / len(out), 4)}, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
