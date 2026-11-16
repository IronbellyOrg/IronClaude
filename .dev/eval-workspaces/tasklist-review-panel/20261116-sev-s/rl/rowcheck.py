"""R3, the ledger row check (DESIGN 7.2 to 7.5, DR-5, DR-6). No model, no network, no clock: a pure function of the
report, the lens, the candidate, the source and the run's tool results.

`check_reviewer(report, lens, corpora, ...)` does the work for one reviewer and returns (ledger dict, checked text):
read the ledger (a block that is not directly above the findings block is `ledger_missing`), the row-id grammar
`^C[0-9]+\\.[0-9]+$` with the class in the reviewer's lens (else `unknown_item`: kept for counting, never linked or
promoted), the quote tests, `over_budget` (reason `recipe`: the id number or the rank among the recipe's rows is above
its budget; reason `lens`: beyond the lens `row_cap` in the order written, counting only rows within their recipe's
budget), recipe coverage (`recipe_missing`; a row of any kind covers its recipe, so a lone `NONE FOUND` row does), the
`none_found` flag and `none_found_with_rows`, then link, demote and promote. A reviewer whose ledger is missing is not
repaired, demoted or promoted: its report goes on as written.

`check_run(run, candidate, source=None, via_reask=())` does every reviewer of a run folder and writes
`check/<rid>.ledger.json`, `check/<rid>.checked.md` and `check/check.json` (DESIGN 7.4 and `classes_lost`). The raw
`reviews/<rid>.md` is never edited. It raises on any error and writes nothing then, so the launcher can set
`check_skipped`. `RL_FORCE_EXC=check` makes it raise (the test hook of bin/rl-env.sh).

Inputs from the run folder: `lens/<rid>.json` (the lens render: recipes, budgets, row_cap), `reviews/<rid>.md` (the
final message), `reviews/<rid>.attempt1.json` (the run transcript, tool results only are read), `reviews/<rid>.meta.json`
(a reviewer that is killed, invalid, in error or on the wrong model is dropped from the check and its classes that no
other reviewer holds are listed in `classes_lost`). `via_reask` lists the reviewers whose report was repaired by the
re-ask: their rows are never promoted. The `reask` key of check.json is left empty for the launcher to fill.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

from rl import ledger_api as api
from scaffold import cards as cards_mod
from scaffold import telemetry

ROW_ID = re.compile(r"C[0-9]+\.[0-9]+")  # fullmatch: the grammar ^C[0-9]+\.[0-9]+$
CAUSES = ("row_unsupported", "row_unsure", "no_cb3", "row_missing")
VERDICTS = ("OK", "PROBLEM", "UNSURE")


class _Assigned:
    """The row ids a reviewer may write: the grammar, and a class of its lens. Any number is accepted here; budgets
    are the next check, so a fifth row of a 4-row recipe is `over_budget`, not `unknown_item` (DR-5, DR-6)."""

    def __init__(self, recipes):
        self.recipes = set(recipes)

    def __contains__(self, item):
        return bool(ROW_ID.fullmatch(item)) and item.split(".")[0] in self.recipes


def _none_found(row: dict) -> bool:
    return (
        row["verdict"] == "OK"
        and not row["quote_plan"]
        and "none found" in row["ran"].lower()
    )


def mark_rows(rows: list[dict], lens: dict) -> list[dict]:
    """Copies of the rows with `over_budget` (None, "recipe" or "lens") and `none_found` set."""
    rank: dict[str, int] = {}
    within = 0
    out = []
    for r in rows:
        r = dict(r, over_budget=None, none_found=_none_found(r))
        if not r["unknown_item"]:
            cls, number = r["item"].split(".")
            rank[cls] = rank.get(cls, 0) + 1
            if int(number) > lens["budgets"][cls] or rank[cls] > lens["budgets"][cls]:
                r["over_budget"] = "recipe"
            else:
                within += 1
                if within > lens["row_cap"]:
                    r["over_budget"] = "lens"
        out.append(r)
    return out


def check_reviewer(
    report: str,
    lens: dict,
    corpora: dict,
    via_reask: bool = False,
    scope=None,
    categories=None,
) -> tuple[dict, str]:
    rd = api.read(report, _Assigned(lens["recipes"]))
    led = {
        "rid": lens["rid"],
        "ledger_missing": rd["ledger_missing"],
        "reason": rd["reason"],
        "format_errors": rd["format_errors"],
        "errors": rd["errors"],
        "normalised_verdict": rd["normalised_verdict"],
        "dup_line": rd["dup_line"],
        "unknown_item": rd["unknown_item"],
        "block_unusable": rd["block_unusable"],
        "loose_layout": rd.get("loose_layout", False),
        "forgiven": rd.get("forgiven", []),
        "via_reask": via_reask,
        "row_cap": lens["row_cap"],
        "rows": [],
        "recipe_missing": [],
        "over_budget": [],
        "none_found_with_rows": [],
        "links": {},
        "demoted": dict.fromkeys(CAUSES, 0),
        "demoted_ids": {},
        "format_induced_demotions": 0,
        "probe_unknown": 0,
        "ok_but_finding": 0,
        "promoted": [],
        "promotion_failures": [],
    }
    if rd["ledger_missing"]:
        return led, report
    rows = mark_rows(api.check(rd["rows"], corpora), lens)
    known = [r for r in rows if not r["unknown_item"]]
    by_class: dict[str, list[dict]] = {}
    for r in known:
        by_class.setdefault(telemetry.class_of(r["item"]), []).append(r)
    ld = api.link_demote(report, rows, rd["errors"], scope)
    pr = api.promote(ld["report"], rows, ld["linked"], categories, via_reask)
    led.update(
        rows=rows,
        recipe_missing=[c for c in lens["recipes"] if c not in by_class],
        over_budget=[
            {"row": r["item"], "reason": r["over_budget"]}
            for r in rows
            if r["over_budget"]
        ],
        none_found_with_rows=[
            c
            for c, rs in by_class.items()
            if any(r["none_found"] for r in rs) and len(rs) > 1
        ],
        links=ld["links"],
        demoted=ld["demoted"],
        demoted_ids=ld["demoted_ids"],
        format_induced_demotions=ld["format_induced_demotions"],
        probe_unknown=ld["probe_unknown"],
        ok_but_finding=ld["ok_but_finding"],
        promoted=pr["promoted"],
        promotion_failures=pr["promotion_failures"],
    )
    return led, pr["report"]


def aggregate(ledgers: dict[str, dict], classes_lost: dict) -> dict:
    """check/check.json (DESIGN 7.4) from the per-reviewer ledger dicts."""
    out = {
        "ledger_missing": [i for i, d in ledgers.items() if d["ledger_missing"]],
        "recipe_missing": {
            i: d["recipe_missing"] for i, d in ledgers.items() if d["recipe_missing"]
        },
        "unknown_item": 0,
        "over_budget": {i: len(d["over_budget"]) for i, d in ledgers.items()},
        "format_errors": 0,
        "normalised_verdict": 0,
        "dup_line": 0,
        "probe_unknown": 0,
        "none_found": {},
        "none_found_with_rows": 0,
        "rows": dict.fromkeys(VERDICTS, 0),
        "rows_per_reviewer": {i: len(d["rows"]) for i, d in ledgers.items()},
        "rows_per_recipe": {},
        "demoted": dict.fromkeys(CAUSES, 0),
        "format_induced_demotions": 0,
        "promoted": 0,
        "promotion_failures": [],
        "ok_but_finding": 0,
        "block_unusable": [i for i, d in ledgers.items() if d["block_unusable"]],
        "classes_lost": classes_lost,
        "reask": {},
    }
    for rid, d in ledgers.items():
        out["unknown_item"] += len(d["unknown_item"])
        out["dup_line"] += len(d["dup_line"])
        out["none_found_with_rows"] += len(d["none_found_with_rows"])
        for k in (
            "format_errors",
            "normalised_verdict",
            "probe_unknown",
            "format_induced_demotions",
            "ok_but_finding",
        ):
            out[k] += d[k]
        out["promoted"] += len(d["promoted"])
        out["promotion_failures"] += [dict(f, rid=rid) for f in d["promotion_failures"]]
        for cause, n in d["demoted"].items():
            out["demoted"][cause] += n
        for r in d["rows"]:
            out["rows"][r["verdict"]] += 1
            cls = telemetry.class_of(r["item"])
            if cls:
                out["rows_per_recipe"][cls] = out["rows_per_recipe"].get(cls, 0) + 1
            if r["none_found"] and cls:
                out["none_found"][cls] = out["none_found"].get(cls, 0) + 1
    return out


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def _dropped(reviews: Path, rid: str) -> bool:
    """No report, or a reviewer that the harness marked killed, invalid, in error or on the wrong model (DESIGN 8 row 6)."""
    md = reviews / f"{rid}.md"
    if not md.is_file() or not md.read_text(encoding="utf-8").strip():
        return True
    meta = _read_json(reviews / f"{rid}.meta.json") or {}
    return (
        bool(meta.get("killed") or meta.get("invalid") or meta.get("error"))
        or meta.get("model_ok") is False
    )


def _transcript(path: Path) -> str | None:
    try:
        return api.transcript_text(path.read_text(encoding="utf-8"))
    except (
        OSError,
        ValueError,
    ):  # no run file, or a cut-off one: the transcript corpus is then empty
        return None


def _dumps(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, indent=1) + "\n"


def check_run(run, candidate, source=None, via_reask=(), scope=None) -> dict:
    if os.environ.get("RL_FORCE_EXC") == "check":
        raise RuntimeError("RL_FORCE_EXC=check")
    run = Path(run)
    lenses = {}
    for f in sorted((run / "lens").glob("*.json")):
        if f.name != "error.json":
            lens = json.loads(f.read_text(encoding="utf-8"))
            lenses[lens["rid"]] = lens
    if not lenses:
        raise ValueError(f"no lens files in {run / 'lens'}")
    reviews = run / "reviews"
    base = {
        "candidate": Path(candidate).read_text(encoding="utf-8"),
        "source": Path(source).read_text(encoding="utf-8") if source else None,
    }
    categories = {c: card["promote_category"] for c, card in cards_mod.load().items()}
    ledgers, texts = {}, {}
    for rid, lens in lenses.items():
        if not _dropped(reviews, rid):
            corpora = dict(
                base, transcript=_transcript(reviews / f"{rid}.attempt1.json")
            )
            report = (reviews / f"{rid}.md").read_text(encoding="utf-8")
            ledgers[rid], texts[rid] = check_reviewer(
                report, lens, corpora, rid in via_reask, scope, categories
            )
    held = {c for rid in ledgers for c in lenses[rid]["recipes"]}
    lost = {
        rid: [c for c in lens["recipes"] if c not in held]
        for rid, lens in lenses.items()
        if rid not in ledgers
    }
    result = aggregate(ledgers, {rid: cs for rid, cs in lost.items() if cs})
    out = run / "check"
    out.mkdir(parents=True, exist_ok=True)
    for rid, led in ledgers.items():
        (out / f"{rid}.ledger.json").write_text(_dumps(led), encoding="utf-8")
        (out / f"{rid}.checked.md").write_text(texts[rid], encoding="utf-8")
    (out / "check.json").write_text(_dumps(result), encoding="utf-8")
    return result
