"""F-RUNS-RL (TESTING section 2, REQ-29, REQ-39 to REQ-43): synthetic run folders for the arms Z0-raw, Z0, K and RL,
two documents (doc-a with 4 items, doc-b with 3, see fixtures/gt/synthetic-gt.json), 5 replicates each: 40 runs, 3
reviewers per run, known found sets, timings, flags (`fallback`, `check_skipped`, `reask`, `killed`, `invalid`,
`retries`), ledgers, merge ledgers and judge folders. Everything is invented.

    build(root, variant="base") -> SimpleNamespace(runs, scoring, gt, cand, run_ids)
        root/runs/stage1-<arm>-<doc>-r<n>/    run.json timing.json resolution.json reviews/ normalised/ merged/ledger.json
                                              and, for an RL run whose check ran, check/<rid>.ledger.json, check/check.json
        root/scoring/                         labels.tsv and one judge folder per label (first and second judge)
        root/cand/<doc>/candidate.md          the reviewed plans (copies of fixtures/plans)
      variant "d6fail" changes the found sets of two RL runs of doc-a so that the RL reach of item A1 drops from 1.0 to
      0.6 while D2 and D3 still pass (the REQ-42 case).
    EXPECTED is the hand-computed answer, written as arithmetic on the tables below, never by calling analysis/analyze.py;
    `expected.json` next to this file is EXPECTED written out (python make_runs.py writes it).

The hand computation, in short. FOUND lists the judged found set of each run; n = 4 items in doc-a, 3 in doc-b.
  found fraction: sizes / n, pooled over the 10 runs of an arm, e.g. Z0: doc-a sizes 1,2,1,1,2 give 7/4 and doc-b sizes
  1,1,2,0,1 give 5/3, so (7/4 + 5/3) / 10. Half share: runs with at least 2 items in either document (1.5 rounds up).
  Jaccard: the 10 pairs per document, a pair of two empty sets left out, e.g. Z0 doc-a: .5 + 1 + 0 + .5 + .5 + .5 + 1/3 +
  0 + .5 + 0 = 23/6 and doc-b 4.5, so (23/6 + 4.5) / 20 = 5/12.
  Consistent: an item found in at least 3 of 5 runs; stable-hit rate = consistent / found at least once.
  Per-class reach: hits over 5 runs x items of the class (C4 holds A1 and B1: 10 trials).
Elapsed: ELAPSED below, medians and means by hand, 90th percentile = x[3] + .6 (x[4] - x[3]) for 5 runs, and
x[8] + .1 (x[9] - x[8]) for 10 runs.
"""

import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
RLROOT = HERE.parents[1]
if str(RLROOT) not in sys.path:
    sys.path.insert(0, str(RLROOT))

from analysis import judge_audit as ja  # noqa: E402
from fixtures.judge import make_judge as mj  # noqa: E402
from rl import rowcheck  # noqa: E402

GT_PATH = HERE.parent / "gt" / "synthetic-gt.json"
PLANS = HERE.parent / "plans"
PLAN_OF = {"doc-a": "p_basic.md", "doc-b": "p_clean.md"}
SEED = 20261115
ARMS = ("Z0-raw", "Z0", "K", "RL")
DOCS = ("doc-a", "doc-b")
REVIEWERS = (
    ("t2b-1", "muse-ember-1.0"),
    ("t3-1", "gpt-6-luna"),
    ("t4-1", "gpt-6-luna"),
)
LENS = {
    "t2b-1": ["C4", "C5", "C6", "C8"],
    "t3-1": ["C2", "C4", "C7"],
    "t4-1": ["C1", "C2", "C3"],
}
BLOCKING_ITEMS = {"A1", "A3", "B1", "B3"}
OTHER_QUOTE = "the stated count is four but the table lists five"

# judged found set per (arm, doc), replicates 1 to 5
FOUND = {
    ("Z0-raw", "doc-a"): ["A1", "A1", "", "A1 A2", "A1"],
    ("Z0", "doc-a"): ["A1", "A1 A2", "A1", "A2", "A1 A3"],
    ("K", "doc-a"): ["A1 A2", "A1", "A1 A2", "A1", "A1 A3"],
    ("RL", "doc-a"): ["A1 A2 A3", "A1 A2", "A1 A3", "A1 A2 A3", "A1 A2"],
    ("Z0-raw", "doc-b"): ["B1", "", "B1", "", "B1"],
    ("Z0", "doc-b"): ["B1", "B1", "B1 B2", "", "B1"],
    ("K", "doc-b"): ["B1", "B1 B2", "B1", "B1", "B1 B3"],
    ("RL", "doc-b"): ["B1 B2", "B1 B3", "B1 B2", "B1", "B1 B2 B3"],
}
VARIANTS = {
    "d6fail": {("RL", "doc-a"): ["A1 A2 A3", "A2 A3", "A1 A3", "A1 A2 A3", "A2 A3"]}
}
# panel_elapsed_s per (arm, doc) and replicate
ELAPSED = {
    ("Z0-raw", "doc-a"): [95, 97, 99, 101, 103],
    ("Z0", "doc-a"): [100, 102, 104, 106, 108],
    ("K", "doc-a"): [101, 103, 105, 107, 109],
    ("RL", "doc-a"): [120, 124, 126, 130, 136],
    ("Z0-raw", "doc-b"): [115, 117, 119, 121, 127],
    ("Z0", "doc-b"): [120, 122, 124, 126, 130],
    ("K", "doc-b"): [121, 123, 125, 127, 131],
    ("RL", "doc-b"): [140, 144, 148, 152, 162],
}
WRONG = {
    ("Z0-raw", "doc-a"): [1, 1, 0, 2, 1],
    ("Z0", "doc-a"): [0, 1, 0, 1, 0],
    ("K", "doc-a"): [1, 0, 0, 1, 0],
    ("RL", "doc-a"): [0, 1, 1, 0, 2],
    ("Z0-raw", "doc-b"): [1, 1, 0, 1, 0],
    ("Z0", "doc-b"): [0, 0, 1, 0, 1],
    ("K", "doc-b"): [0, 0, 0, 1, 0],
    ("RL", "doc-b"): [1, 0, 0, 0, 1],
}
FREE = {
    "Z0-raw": 2,
    "Z0": 2,
    "K": 3,
    "RL": 1,
}  # findings lines a reviewer writes besides the ones for found items
TOKENS = {"Z0-raw": 1000, "Z0": 1000, "K": 1100, "RL": 1500}
KILLED = {("Z0", "doc-a", 3): "t3-1", ("RL", "doc-a", 3): "t4-1"}
INVALID = {("Z0-raw", "doc-a", 4): "t3-1"}
RETRIES = {("K", "doc-a", 2): 1, ("Z0-raw", "doc-b", 3): 2, ("RL", "doc-b", 1): 1}
REASK = {
    ("doc-b", 2): "t2b-1"
}  # RL: the ember's ledger was missing, the re-ask was accepted
FALLBACK = {("doc-a", 5)}  # RL: the lens render failed, the Z0 briefs ran
SKIPPED = {("doc-a", 2)}  # RL: the row check raised, the raw reports were merged
# the reach plan of the 8 RL runs whose check ran: (item, reviewer, level, kind)
#   level  sel       an OK row covers the item
#          act       a supported PROBLEM row covers it, no finding is linked and none promoted
#          link      a supported PROBLEM row with a finding linked by probe, in the merge
#          link_lost the same, but the finding is not in the merge
#          promo     a supported PROBLEM row whose promoted line is in the merge
#   kind   exact (the item's own quote), near (the line above it), wider (the whole line that holds it)
PLAN = {
    ("doc-a", 1): [
        ("A1", "t2b-1", "link", "exact"),
        ("A2", "t3-1", "link", "exact"),
        ("A3", "t2b-1", "link", "exact"),
        ("A4", "t2b-1", "act", "exact"),
    ],
    ("doc-a", 3): [("A1", "t2b-1", "link", "exact"), ("A3", "t2b-1", "link", "exact")],
    ("doc-a", 4): [
        ("A1", "t2b-1", "link", "near"),
        ("A2", "t3-1", "promo", "exact"),
        ("A3", "t2b-1", "link", "exact"),
        ("A4", "t2b-1", "sel", "exact"),
    ],
    ("doc-b", 1): [
        ("B1", "t2b-1", "link", "exact"),
        ("B2", "t4-1", "link", "exact"),
        ("B3", "t3-1", "link_lost", "exact"),
    ],
    ("doc-b", 2): [("B1", "t3-1", "link", "exact"), ("B3", "t3-1", "link", "exact")],
    ("doc-b", 3): [
        ("B1", "t2b-1", "link", "exact"),
        ("B1", "t3-1", "sel", "exact"),
        ("B2", "t4-1", "link", "wider"),
    ],
    ("doc-b", 4): [("B1", "t2b-1", "link", "exact")],
    ("doc-b", 5): [
        ("B1", "t2b-1", "link", "exact"),
        ("B2", "t4-1", "link", "exact"),
        ("B3", "t3-1", "promo", "exact"),
    ],
}
OMIT = {
    ("doc-b", 3, "t4-1"): ["C3"],
    ("doc-a", 4, "t3-1"): ["C7"],
}  # recipes with no row at all (recipe_missing)
MISSING = {("doc-b", 4, "t3-1")}  # a luna whose ledger is missing: no re-ask
ROW_CAP = {("doc-a", 4, "t2b-1"): 6}  # every other lens cap is 14
BAD_QUOTE = {
    ("doc-a", 1, "t3-1")
}  # one PROBLEM row whose quote_plan is not in the plan
FORMAT_ERROR = {("doc-b", 2, "t3-1")}


def run_id(arm, doc, rep):
    return f"stage1-{arm.lower().replace('-', '')}-{doc}-r{rep}"


def gt_items():
    docs = json.loads(GT_PATH.read_text(encoding="utf-8"))["docs"]
    return {d: v["items"] for d, v in docs.items()}


def found_table(variant):
    return {**FOUND, **VARIANTS.get(variant, {})}


def put(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def dump(path, obj):
    put(path, json.dumps(obj, indent=1, sort_keys=True) + "\n")


def finding(fid, claim, anchor, **keys):
    return {
        "id": fid,
        "severity": "MINOR",
        "blocking": False,
        "category": "other",
        "anchor": anchor,
        "refs": [],
        "claim": claim,
        **keys,
    }


def findings_report(lines):
    body = "\n".join(json.dumps(x, sort_keys=True) for x in lines)
    return f"review: 1 of 3\n\n## Findings block\n\n```findings-v1\n{body}\n```\n\nverdict: PASS\n"


def row(
    item,
    verdict="OK",
    qp="",
    qo="",
    ran="compared both scopes",
    plan_ok=True,
    over=None,
    none_found=False,
    line=0,
):
    problem = verdict == "PROBLEM"
    supported = problem and plan_ok and bool(qp) and bool(qo)
    return {
        "item": item,
        "verdict": verdict,
        "quote_plan": qp,
        "quote_other": qo,
        "problem": "the plan states two different things" if problem else "",
        "ran": ran,
        "line": line,
        "limits_violated": [],
        "unknown_item": False,
        "over_budget": over,
        "none_found": none_found,
        "corpus": "candidate" if qo else None,
        "quote_plan_ok": bool(qp) and plan_ok,
        "quote_other_ok": bool(qo),
        "quotes_supported": supported,
        "search_supported": False,
        "supported": supported,
    }


def quote_for(text, quote, kind):
    lines = text.splitlines()
    at = next(i for i, ln in enumerate(lines) if quote in ln)
    if kind == "near":
        return lines[at - 1].strip()
    if kind == "wider":
        return lines[at].strip()
    return quote


def ledger_of(doc, rep, rid, items, text):
    """(ledger dict, findings lines of the raw report, promoted lines, merged members) of one reviewer of a checked RL run."""
    base = {
        "rid": rid,
        "ledger_missing": False,
        "reason": None,
        "format_errors": 0,
        "errors": [],
        "normalised_verdict": 0,
        "dup_line": [],
        "unknown_item": [],
        "block_unusable": None,
        "via_reask": REASK.get((doc, rep)) == rid,
        "row_cap": ROW_CAP.get((doc, rep, rid), 14),
        "rows": [],
        "recipe_missing": [],
        "over_budget": [],
        "none_found_with_rows": [],
        "links": {},
        "demoted": {
            "no_cb3": 0,
            "row_missing": 0,
            "row_unsupported": 0,
            "row_unsure": 0,
        },
        "demoted_ids": {},
        "format_induced_demotions": 0,
        "probe_unknown": 0,
        "ok_but_finding": 0,
        "promoted": [],
        "promotion_failures": [],
    }
    free = [
        finding(f"F{k}", f"free finding {k} of {rid}", f"free anchor {rid} {k}")
        for k in (1,)
    ]
    if (doc, rep, rid) in MISSING:
        base.update(ledger_missing=True, reason="no_ledger_heading")
        return base, free, [], []
    recipes = [c for c in LENS[rid] if c not in OMIT.get((doc, rep, rid), [])]
    base["recipe_missing"] = [c for c in LENS[rid] if c not in recipes]
    by_id = {i["id"]: i for i in items}
    rows, count = [], {}
    for c in recipes:
        count[c] = 1
        none_found = c == "C3"
        rows.append(
            row(
                f"{c}.1",
                ran="NONE FOUND after the search"
                if none_found
                else "compared both scopes",
                none_found=none_found,
            )
        )
    links, promoted, members, raw, extra = {}, [], [], list(free), []
    for item, who, level, kind in PLAN.get((doc, rep), []):
        if who != rid:
            continue
        c = by_id[item]["class"]
        count[c] = count.get(c, 0) + 1
        rid_item = f"{c}.{count[c]}"
        qp = quote_for(text, by_id[item]["plan_quote"], kind)
        if level == "sel":
            rows.append(row(rid_item, qp=qp))
            continue
        rows.append(row(rid_item, "PROBLEM", qp, OTHER_QUOTE))
        if level in ("link", "link_lost"):
            fid = f"F{len(raw) + 1}"
            raw.append(
                finding(
                    fid, f"claim for {item}", by_id[item]["plan_quote"], probe=rid_item
                )
            )
            links[fid] = rid_item
            if level == "link":
                members.append((fid, by_id[item]["plan_quote"]))
        elif level == "promo":
            fid = f"P{rid_item}"
            promoted.append(fid)
            extra.append(
                finding(
                    fid,
                    "the plan states two different things",
                    qp,
                    probe=rid_item,
                    src="ledger",
                    **{"class": c},
                )
            )
            members.append((fid, qp))
    if (doc, rep, rid) in BAD_QUOTE:
        count["C2"] += 1
        rows.append(
            row(
                f"C2.{count['C2']}",
                "PROBLEM",
                "this text is not in the plan",
                plan_ok=False,
            )
        )
    if (doc, rep, rid) in FORMAT_ERROR:
        base.update(
            format_errors=1,
            errors=[{"line": 30, "msg": "not JSON", "item": None, "named": None}],
        )
    rows.sort(key=lambda r: tuple(int(x) for x in r["item"][1:].split(".")))
    within = 0
    for n, r in enumerate(rows):
        r["line"] = 8 + n
        within += 1
        if within > base["row_cap"]:
            r["over_budget"] = "lens"
    base.update(
        rows=rows,
        links=links,
        promoted=promoted,
        over_budget=[
            {"row": r["item"], "reason": r["over_budget"]}
            for r in rows
            if r["over_budget"]
        ],
    )
    return base, raw, extra, members


def build(root, variant="base"):
    root = Path(root)
    items = gt_items()
    found = found_table(variant)
    runs, scoring, cand = root / "runs", root / "scoring", root / "cand"
    texts = {}
    for doc, name in PLAN_OF.items():
        texts[doc] = (PLANS / name).read_text(encoding="utf-8")
        put(cand / doc / "candidate.md", texts[doc])
    ids = []
    for arm in ARMS:
        for doc in DOCS:
            for rep in range(1, 6):
                rid_run = run_id(arm, doc, rep)
                ids.append(rid_run)
                write_run(
                    runs / rid_run,
                    arm,
                    doc,
                    rep,
                    items[doc],
                    texts[doc],
                    found[(arm, doc)][rep - 1].split(),
                    cand / doc / "candidate.md",
                    rid_run,
                )
    write_scoring(root, runs, scoring, ids, found, items)
    return SimpleNamespace(
        root=root, runs=runs, scoring=scoring, gt=GT_PATH, cand=cand, run_ids=ids
    )


def write_run(d, arm, doc, rep, items, text, found, cand_path, rid_run):
    key = (arm, doc, rep)
    killed, invalid = KILLED.get(key), INVALID.get(key)
    rl = arm == "RL"
    fallback = rl and (doc, rep) in FALLBACK
    skipped = rl and (doc, rep) in SKIPPED
    checked = rl and not fallback and not skipped
    reviewers = {}
    for rid, model in REVIEWERS:
        status = "killed" if rid == killed else "invalid" if rid == invalid else "ok"
        luna = model == "gpt-6-luna"
        wall = (
            192
            if rid == killed
            else (96 if rl and not fallback else 80)
            if luna
            else 70
            if rl and not fallback
            else 60
        )
        reviewers[rid] = {
            "model": model,
            "status": status,
            "killed": rid == killed,
            "wall_s": wall,
            "merged": status == "ok",
        }
    present = [rid for rid, v in reviewers.items() if v["status"] == "ok"]
    meta = {
        "arm": arm,
        "panel": "primary",
        "doc": doc,
        "run_id": rid_run,
        "replicate": rep,
        "block": rep,
        "retries": RETRIES.get(key, 0),
        "reask": [REASK[(doc, rep)]] if rl and (doc, rep) in REASK else [],
        "fallback": fallback,
        "check_ran": checked,
        "check_skipped": skipped,
        "reviewers": reviewers,
    }
    dump(d / "run.json", meta)
    dump(
        d / "timing.json",
        {
            "arm": arm,
            "panel_elapsed_s": ELAPSED[(arm, doc)][rep - 1],
            "slowest_reviewer_s": ELAPSED[(arm, doc)][rep - 1] - 1,
            "reask_s": 12 if meta["reask"] else 0,
            "check_s": 0.5 if checked else 0,
        },
    )
    dump(
        d / "resolution.json",
        {"reviewers": [{"reviewer_id": r, "model": m} for r, m in REVIEWERS]},
    )
    ledgers, merged_rows, n_lid = {}, [], 0

    def add_merged(anchor, members):
        nonlocal n_lid
        n_lid += 1
        merged_rows.append(
            {
                "lid": f"L{n_lid}",
                "anchor": anchor,
                "blocking": False,
                "members": [
                    {"round": 1, "reviewer_id": r, "fid": f, "blocking": False}
                    for r, f in members
                ],
            }
        )

    for pos, rid in enumerate(r for r, _ in REVIEWERS):
        tokens = (
            0 if reviewers[rid]["status"] != "ok" else TOKENS["Z0" if fallback else arm]
        )
        dump(
            d / "reviews" / f"{rid}.cost.json",
            {"attempts": 1, "total_output_tokens_all": tokens},
        )
        if rid not in present:
            continue
        if checked:
            led, raw, extra, members = ledger_of(doc, rep, rid, items, text)
            ledgers[rid] = led
            for fid, anchor in members:
                add_merged(anchor, [(rid, fid)])
            for ln in raw:
                if "probe" not in ln:
                    add_merged(ln["anchor"], [(rid, ln["id"])])
            put(d / "reviews" / f"{rid}.md", findings_report(raw))
            put(d / "check" / f"{rid}.checked.md", findings_report(raw + extra))
            put(d / "normalised" / f"{rid}.md", findings_report(raw + extra))
            dump(d / "check" / f"{rid}.ledger.json", led)
            continue
        held = [
            it
            for k, it in enumerate(items)
            if it["id"] in found and present[k % len(present)] == rid
        ]
        probe_found = (
            rl and not fallback
        )  # a skipped RL run: the reviewers' own findings carry `probe`
        lines = [
            finding(
                f"F{k}",
                f"finding for {it['id']}",
                it["plan_quote"],
                **({"probe": it["class"] + ".9"} if probe_found else {}),
            )
            for k, it in enumerate(held, 1)
        ]
        noise = (FREE["Z0"] if fallback else FREE[arm]) - (
            0 if probe_found else len(held)
        )
        lines += [
            finding(f"F{len(lines) + k}", f"free finding {k}", f"free anchor {rid} {k}")
            for k in range(1, noise + 1)
        ]
        for ln in lines:
            add_merged(ln["anchor"], [(rid, ln["id"])])
        for name in (f"reviews/{rid}.md", f"normalised/{rid}.md"):
            put(d / name, findings_report(lines))
    if checked:
        lost = {"t4-1": ["C1", "C3"]} if killed == "t4-1" else {}
        agg = rowcheck.aggregate(ledgers, lost)
        agg["reask"] = {
            "t2b-1": {
                "allowed": False,
                "accepted": False,
                "reason": "ledger_present",
                "seconds": 0.0,
            }
        }
        if meta["reask"]:
            agg["reask"]["t2b-1"] = {
                "allowed": True,
                "asked": True,
                "accepted": True,
                "reason": "accepted",
                "seconds": 12.0,
            }
        dump(d / "check" / "check.json", agg)
    dump(
        d / "merged" / "ledger.json",
        {"schema": "review-ledger/1", "doc": str(cand_path), "rows": merged_rows},
    )


def write_scoring(root, runs, scoring, ids, found, items):
    plan = ja.plan(runs, ids, SEED)
    put(scoring / "labels.tsv", "".join("\t".join(r) + "\n" for r in plan))
    for label, run, doc, _role in plan:
        arm = next(
            a for a in ARMS if run.startswith(f"stage1-{a.lower().replace('-', '')}-")
        )
        rep = int(run.rsplit("-r", 1)[1])
        got = found[(arm, doc)][rep - 1].split()
        score = {
            "label": label,
            "combo": label,
            "package": doc,
            "gt_total": len(items[doc]),
            "gt_covered_any": got,
            "gt_covered_blocking": [g for g in got if g in BLOCKING_ITEMS],
            "ledger_rows_total": mj.ROWS,
            "ledger_rows_blocking": mj.BLOCKING,
            "blocking_rows_gt_matched": 1,
            "wrong_blockers": WRONG[(arm, doc)][rep - 1],
            "notes": "invented",
        }
        d = scoring / label
        merged = d / "merged-anon.md"
        put(merged, mj.ANON.format(sha="cd" * 32))
        put(d / "judge.json", json.dumps(mj._result(mj.OK_MSG)))
        put(d / "judge.err", "")
        dump(d / "score.json", score)
        os.utime(merged, (mj.T0, mj.T0))
        for f in ("judge.json", "judge.err", "score.json"):
            os.utime(d / f, (mj.T0 + 5, mj.T0 + 5))


# ---------------------------------------------------------------- the hand-computed answer
# elapsed (RL doc-a [120,124,126,130,136], doc-b [140,144,148,152,162]; Z0 doc-a [100,102,104,106,108],
# doc-b [120,122,124,126,130])
EXPECTED = {
    "arms": {
        "Z0-raw": {
            "runs": 10,
            "found_fraction_mean": (5 / 4 + 3 / 3)
            / 10,  # doc-a sizes 1,1,0,2,1; doc-b sizes 1,0,1,0,1
            "half_found_share": 1 / 10,  # one run (doc-a r4) has 2 items
            "jaccard_mean": (4.5 + 3)
            / 19,  # doc-a 4.5 over 10 pairs; doc-b 3 over 9 (the pair r2, r4 is empty)
            "jaccard_pairs": 19,
            "consistent_items": 2,  # A1 in 4 runs, B1 in 3; A2 in 1
            "consistent_share": 2 / 7,
            "stable_hit_rate": 2 / 3,  # found at least once: A1, A2, B1
            "wrong_blockers_per_run": (5 + 3) / 10,
            "found_blocking_mean": (4 / 4 + 3 / 3) / 10,
            "nonprobe_findings_per_run": (9 * 6 + 4)
            / 10,  # 2 lines x 3 reviewers; doc-a r4 has one reviewer less (invalid)
            "elapsed_mean": (495 + 599) / 10,
            "elapsed_median": (103 + 115) / 2,
            "elapsed_p90": 121 + 0.1 * (127 - 121),
            "tokens_per_run": (9 * 3000 + 2000) / 10,
            "kills": 0,
            "reviewer_runs": 30,
            "retries": 2,
            "reasks": 0,
            "fallbacks": 0,
            "invalid": 1,
            "check_skipped": 0,
            "class_reach": {
                "C4": [7, 10],
                "C2": [1, 5],
                "C5": [0, 5],
                "C8": [0, 5],
                "C1": [0, 5],
                "C7": [0, 5],
            },
        },
        "Z0": {
            "runs": 10,
            "found_fraction_mean": (7 / 4 + 5 / 3) / 10,
            "half_found_share": 3 / 10,
            "jaccard_mean": (23 / 6 + 4.5) / 20,
            "jaccard_pairs": 20,
            "consistent_items": 2,  # A1 and B1, each in 4 runs
            "consistent_share": 2 / 7,
            "stable_hit_rate": 2 / 5,  # found at least once: A1, A2, A3, B1, B2
            "wrong_blockers_per_run": (2 + 2) / 10,
            "found_blocking_mean": (5 / 4 + 4 / 3) / 10,
            "nonprobe_findings_per_run": (9 * 6 + 4)
            / 10,  # doc-a r3 has one reviewer less (killed)
            "elapsed_mean": (520 + 622) / 10,
            "elapsed_median": (108 + 120) / 2,
            "elapsed_p90": 126 + 0.1 * (130 - 126),
            "tokens_per_run": (9 * 3000 + 2000) / 10,
            "kills": 1,
            "reviewer_runs": 30,
            "retries": 0,
            "reasks": 0,
            "fallbacks": 0,
            "invalid": 0,
            "check_skipped": 0,
            "class_reach": {
                "C4": [8, 10],
                "C2": [2, 5],
                "C5": [1, 5],
                "C8": [0, 5],
                "C1": [1, 5],
                "C7": [0, 5],
            },
        },
        "K": {
            "runs": 10,
            "found_fraction_mean": (8 / 4 + 7 / 3) / 10,
            "half_found_share": 5 / 10,
            "jaccard_mean": (17 / 3 + 19 / 3) / 20,
            "jaccard_pairs": 20,
            "consistent_items": 2,  # A1 and B1, each in all 5 runs
            "consistent_share": 2 / 7,
            "stable_hit_rate": 2 / 6,
            "wrong_blockers_per_run": (2 + 1) / 10,
            "found_blocking_mean": (6 / 4 + 6 / 3) / 10,
            "nonprobe_findings_per_run": 9.0,  # 3 lines x 3 reviewers
            "elapsed_mean": (525 + 627) / 10,
            "elapsed_median": (109 + 121) / 2,
            "elapsed_p90": 127 + 0.1 * (131 - 127),
            "tokens_per_run": 3300.0,
            "kills": 0,
            "reviewer_runs": 30,
            "retries": 1,
            "reasks": 0,
            "fallbacks": 0,
            "invalid": 0,
            "check_skipped": 0,
            "class_reach": {
                "C4": [10, 10],
                "C2": [2, 5],
                "C5": [1, 5],
                "C8": [0, 5],
                "C1": [1, 5],
                "C7": [1, 5],
            },
        },
        "RL": {
            "runs": 10,
            "found_fraction_mean": (12 / 4 + 10 / 3) / 10,
            "half_found_share": 9 / 10,
            "jaccard_mean": (20 / 3 + 5.5) / 20,
            "jaccard_pairs": 20,
            "consistent_items": 5,  # A1, A2, A3, B1, B2 (A3 and B2 in exactly 3 runs, B3 in 2)
            "consistent_share": 5 / 7,
            "stable_hit_rate": 5 / 6,
            "wrong_blockers_per_run": (4 + 2) / 10,
            "found_blocking_mean": (8 / 4 + 7 / 3) / 10,
            # 1 free line per reviewer = 3 per run; doc-a r3 has two reviewers (2), the fallback run doc-a r5 wrote 2 lines each (6)
            "nonprobe_findings_per_run": (3 + 3 + 2 + 3 + 6 + 5 * 3) / 10,
            "elapsed_mean": (636 + 746) / 10,
            "elapsed_median": (136 + 140) / 2,
            "elapsed_p90": 152 + 0.1 * (162 - 152),
            "tokens_per_run": (4500 + 4500 + 3000 + 4500 + 3000 + 5 * 4500)
            / 10,  # doc-a r3 lost a reviewer, r5 ran the Z0 briefs
            "kills": 1,
            "reviewer_runs": 30,
            "retries": 1,
            "reasks": 1,
            "fallbacks": 1,
            "invalid": 0,
            "check_skipped": 1,
            "class_reach": {
                "C4": [10, 10],
                "C2": [4, 5],
                "C5": [3, 5],
                "C8": [0, 5],
                "C1": [3, 5],
                "C7": [2, 5],
            },
        },
    },
    # per document, found-fraction mean = size sum / (n x 5) and the elapsed figures
    "documents": {
        "Z0": {
            "doc-a": {
                "found_fraction_mean": 7 / 4 / 5,
                "elapsed_mean": 104.0,
                "elapsed_median": 104,
                "elapsed_p90": 106 + 0.6 * 2,
            },
            "doc-b": {
                "found_fraction_mean": 5 / 3 / 5,
                "elapsed_mean": 124.4,
                "elapsed_median": 124,
                "elapsed_p90": 126 + 0.6 * 4,
            },
        },
        "RL": {
            "doc-a": {
                "found_fraction_mean": 12 / 4 / 5,
                "elapsed_mean": 127.2,
                "elapsed_median": 126,
                "elapsed_p90": 130 + 0.6 * 6,
            },
            "doc-b": {
                "found_fraction_mean": 10 / 3 / 5,
                "elapsed_mean": 149.2,
                "elapsed_median": 148,
                "elapsed_p90": 152 + 0.6 * 10,
            },
        },
    },
    "d1": {
        "doc-a": {
            "ratio_median": 126 / 104,
            "ratio_mean": 127.2 / 104,
            "ratio_p90": (130 + 0.6 * 6) / (106 + 0.6 * 2),
        },
        "doc-b": {
            "ratio_median": 148 / 124,
            "ratio_mean": 149.2 / 124.4,
            "ratio_p90": (152 + 0.6 * 10) / (126 + 0.6 * 4),
        },
        "kills": 1,
        "kill_rate": 1 / 30,
    },
    # pooled mean found fraction: Z0 (7/4 + 5/3) / 10, K (8/4 + 7/3) / 10, RL (12/4 + 10/3) / 10, Z0-raw (5/4 + 3/3) / 10
    "shares": {
        "H share": (7 / 4 + 5 / 3) / 10 - (5 / 4 + 3 / 3) / 10,
        "prompting share": (8 / 4 + 7 / 3) / 10 - (7 / 4 + 5 / 3) / 10,
        "redesign share": (12 / 4 + 10 / 3) / 10 - (7 / 4 + 5 / 3) / 10,
    },
    "gates": {
        "D2_diff": (12 / 4 + 10 / 3) / 10 - (7 / 4 + 5 / 3) / 10,
        "D3": [5, 2],
        "D7_gain": (12 / 4 + 10 / 3) / 10 - (8 / 4 + 7 / 3) / 10,
    },
    # stage rows of the RL arm: 8 checked runs, 3 reviewers; 3 doc-a runs x 4 items x 3 + 5 doc-b runs x 3 items x 3 = 81
    # (item, reviewer) cells; selection counted run by run: doc-a r1 4, r3 2, r4 3 (A4 is over the lens cap), doc-b 3, 2, 3, 1, 3 = 21;
    # act: 4, 2, 3, then 3, 2, 2 (B1 at t3-1 is an OK row), 1, 3 = 20; merge: 3, 2, 3, then 2 (B3 lost), 2, 2, 1, 3 = 18,
    # plus 2 + 2 by anchor in the skipped run (r2) and the fallback run (r5) of doc-a, whose selection and act are null.
    "stages": {
        "rl_rows": 81 + 24,
        "rl_rows_selection_null": 24,
        "selection": 21,
        "act": 20,
        "merge_survival_checked": 18,
        "merge_survival_by_anchor": 4,
    },
    "stage_cells": [
        # run, item, reviewer, selection, act, merge_survival, credit any, credit blocking
        [
            "stage1-rl-doc-a-r4",
            "A1",
            "t2b-1",
            True,
            True,
            True,
            True,
            True,
        ],  # the quote is the line above (near)
        [
            "stage1-rl-doc-a-r4",
            "A4",
            "t2b-1",
            False,
            False,
            False,
            False,
            False,
        ],  # an OK row over the lens cap of 6
        [
            "stage1-rl-doc-a-r1",
            "A4",
            "t2b-1",
            True,
            True,
            False,
            False,
            False,
        ],  # a PROBLEM row nothing links to
        [
            "stage1-rl-doc-b-r1",
            "B3",
            "t3-1",
            True,
            True,
            False,
            False,
            False,
        ],  # the linked finding is not in the merge
        [
            "stage1-rl-doc-b-r3",
            "B1",
            "t3-1",
            True,
            False,
            False,
            True,
            True,
        ],  # an OK row of the second C4 holder
        ["stage1-rl-doc-b-r3", "B1", "t2b-1", True, True, True, True, True],
        [
            "stage1-rl-doc-b-r3",
            "B2",
            "t4-1",
            True,
            True,
            True,
            True,
            False,
        ],  # the quote is the whole line (wider)
        [
            "stage1-rl-doc-b-r5",
            "B3",
            "t3-1",
            True,
            True,
            True,
            True,
            True,
        ],  # a promoted line
        [
            "stage1-rl-doc-b-r4",
            "B1",
            "t3-1",
            False,
            False,
            False,
            True,
            True,
        ],  # ledger missing
        ["stage1-rl-doc-a-r3", "A1", "t4-1", False, False, False, True, True],  # killed
        [
            "stage1-rl-doc-a-r2",
            "A1",
            "t2b-1",
            None,
            None,
            True,
            True,
            True,
        ],  # check skipped: merge by anchor
        [
            "stage1-z0-doc-a-r3",
            "A1",
            "t2b-1",
            None,
            None,
            True,
            True,
            True,
        ],  # Z0, the killed reviewer holds nothing
        ["stage1-rl-doc-a-r5", "A2", "t3-1", None, None, True, True, False],  # fallback
    ],
    # RL, class C4 (items A1 in 5 doc-a runs and B1 in 5 doc-b runs, all credited: 10 (run, item) pairs, so 10 rows per reviewer):
    # t2b-1 has a ledger in 3 + 5 runs; it selects A1 in r1, r3, r4 and B1 in r1, r3, r4, r5 = 7; every selected row is a
    # supported PROBLEM = 7 acts; merge survival: A1 in r1, r3, r4 and (by anchor) r2, r5, B1 in r1, r3, r4, r5 = 9.
    # t3-1 selects B1 in r2 (link) and r3 (OK row) = 2, acts once (r2), survives the merge once (r2).
    "stage_rates_rl_c4": {
        "items": 10,
        "judge_credit_any": 10,
        "judge_credit_blocking": 10,
        "t2b-1": {
            "rows": 10,
            "ledger_rows": 8,
            "selection": 7,
            "act": 7,
            "merge_survival": 9,
        },
        "t3-1": {
            "rows": 10,
            "ledger_rows": 8,
            "selection": 2,
            "act": 1,
            "merge_survival": 1,
        },
    },
    # lens-cap displacement: the one row over the cap (C8.2 of t2b-1 in doc-a r4) comes back if C4, C5 or C6 rows are absent
    "ablation": {
        "C4": 100 * 1 / (81 - 24),  # 24 cells hold a C4 item (A1 x 9, B1 x 15)
        "C5": 100 * 1 / (81 - 9),
        "C6": 100 * 1 / 81,
        "C1": 0.0,
        "C2": 0.0,
        "C3": 0.0,
        "C7": 0.0,
        "C8": 0.0,
    },
    "time": {
        "b": [
            100,
            103,
        ],  # the smallest Z0 median of the slowest reviewer: doc-a [99,101,103,105,107]
        "breakeven": [2.07, round((0.35 * 103 - 6) / 14, 2)],
        "c": [
            2.0,
            (96 - 80 - 4) / (51 / 14),
        ],  # luna wall 96 against 80, minus 4 s, over 51 rows in 14 luna ledgers
        "cap": [14, 9],  # floor((0.35 x 103 - 6) / 3.294) = floor(9.12)
    },
    # the check of the 8 RL runs that ran it: 3 reviewers each, one killed (no ledger file)
    "compliance": {
        "runs_checked": 8,
        "reviewer_runs": 23,
        "reviewers_without_ledger_file": 1,
        "ledger_missing_count": 2,  # doc-b r4 luna (final) and doc-b r2 ember (repaired by the accepted re-ask)
        "recipe_missing": {"C3": 1, "C7": 1},
        "quote_rows": 23,  # 22 covering rows of PLAN plus the PROBLEM row with a quote that is not in the plan
        "quote_ok": 22,
        "format_errors": 1,
        "none_found": {
            "C3": 6
        },  # a NONE FOUND row for C3 in each of the 7 t4-1 ledgers but doc-b r3
        "over_budget": {"recipe": 0, "lens": 1},
        "reask": {"asked": 1, "accepted": 1},
        "rows_per_reviewer": {"t2b-1": 44 / 8, "t3-1": 28 / 7, "t4-1": 23 / 7},
    },
    # DESIGN 12.5 per arm. Only the 8 checked RL runs (doc-a r1, r3, r4; doc-b r1 to r5) have ledgers: 3 reviewers each, the
    # killed t4-1 of doc-a r3 has none, so 23 ledger files; the luna ledger of doc-b r4 is missing, so 22 ledgers with rows.
    # Z0-raw, Z0 and K write no ledger and no check.json: every count is zero, every share dict is empty.
    "ledger_metrics": {
        "RL": {
            # the one row over the lens cap of 6 (C8.2 of t2b-1, doc-a r4); no row is over a recipe budget
            "over_budget": {"recipe": 0, "lens": 1},
            "recipe_missing": {
                "C3": 1,
                "C7": 1,
            },  # t4-1 doc-b r3 has no C3 row, t3-1 doc-a r4 has no C7 row
            "unknown_item": 0,
            # classes_lost of check.json: only the killed t4-1 (doc-a r3) lists any, its lens C1, C2, C3 less C2 which t3-1
            # also holds: the fixture writes {"t4-1": ["C1", "C3"]}
            "classes_lost": {"C1": 1, "C3": 1},
            "reask_asked": 1,  # the accepted ember re-ask of doc-b r2
            "reask_accepted": 1,
            # ran = ledgers (with rows) that hold a row of the class. t2b-1 (C4 C5 C6 C8): 8 ledgers; t3-1 (C2 C4 C7): 7
            # ledgers, 6 for C7 (doc-a r4 omits it); t4-1 (C1 C2 C3): 7 ledgers, 6 for C3 (doc-b r3 omits it).
            # C1 7; C2 7 + 7 = 14; C3 6; C4 8 + 7 = 15; C5 8; C6 8; C7 6; C8 8.
            # none_found = ledgers with a NONE FOUND row of the class: the C3 row of the 6 t4-1 ledgers that have one.
            "none_found_share": {
                "C1": [0, 7],
                "C2": [0, 14],
                "C3": [6, 6],
                "C4": [0, 15],
                "C5": [0, 8],
                "C6": [0, 8],
                "C7": [0, 6],
                "C8": [0, 8],
            },
            # mean rows of the ledgers that are not missing: t2b-1 44 rows over 8, t3-1 28 over 7, t4-1 23 over 7 (see
            # "compliance"; 4 recipe rows + 12 plan rows, 20 + 8 (7 plan rows and the bad-quote row), 20 + 3)
            "rows_per_lens": {"t2b-1": 44 / 8, "t3-1": 28 / 7, "t4-1": 23 / 7},
            # found fraction of the re-asked run (doc-b r2: B1 B3 of 3 items) and of the other 9 RL runs:
            # all 10 runs sum to 12/4 + 10/3 = 19/3, without r2 that is 19/3 - 2/3 = 17/3 over 9 runs
            "reask_yield": {
                "with": [1, 2 / 3],
                "without": [9, (19 / 3 - 2 / 3) / 9],
            },
        },
        "Z0-raw": {
            "reask_yield": {"with": [0, None], "without": [10, (5 / 4 + 3 / 3) / 10]}
        },
        "Z0": {
            "reask_yield": {"with": [0, None], "without": [10, (7 / 4 + 5 / 3) / 10]}
        },
        "K": {
            "reask_yield": {"with": [0, None], "without": [10, (8 / 4 + 7 / 3) / 10]}
        },
    },
}


def write_expected(path=HERE / "expected.json"):
    dump(path, EXPECTED)


if __name__ == "__main__":
    write_expected()
    print(f"wrote {HERE / 'expected.json'}")
