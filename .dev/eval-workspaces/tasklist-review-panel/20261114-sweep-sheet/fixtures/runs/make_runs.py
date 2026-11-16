"""F-RUNS (TESTING section 2): synthetic run folders, judge outputs and `expected.json` for the analysis tests.

Everything is invented. `build(root)` writes, for 3 arms (Z0, K, SS; `arms=` adds Z0-raw), 2 documents and 5 replicates:
  root/runs/stage1/<arm>-<doc>-r<k>/   run.json, timing.json, reviews/<rid>.{meta,cost}.json, normalised/<rid>.md
                                       (reviews/<rid>.md for Z0-raw), scoring/label-key.json
  root/scoring/stage1/<label>/score.json   the judge output that the label key names
  root/expected.json                   the metrics, worked out below from the tables with plain loops and sets. It is NOT
                                       made by calling analysis/analyze.py, so a shared mistake cannot hide.
A document has 8 ground-truth items GT1 to GT8; item GTn has class Cn (the synthetic ground truth of fixtures/gt).
Replicate k of every arm is in randomised block k. No ground-truth or score file of a study is read or copied.

The tables list, per replicate: the items found at any severity, the items found by a blocking row, the wrong blockers,
the panel seconds, the non-probe findings of the three reviewers, the probe lines and the promoted ledger lines.
"""

import json
from pathlib import Path
from types import SimpleNamespace

DOCS = ("synth-a", "synth-b")
DEFAULT_ARMS = ("Z0", "K", "SS")
ALL_ARMS = ("Z0-raw", *DEFAULT_ARMS)
REPS = 5
ITEMS = 8
RIDS = ("t2b-1", "t3-1", "t4-1")
MODELS = {"t2b-1": "muse-ember-1.0", "t3-1": "gpt-6-luna", "t4-1": "gpt-6-luna"}

# (found any, found blocking, wrong blockers, panel seconds, non-probe findings of t2b-1/t3-1/t4-1, probe lines, ledger lines)
TABLE = {
    ("Z0-raw", "synth-a"): [
        ("12", "1", 3, 105, (1, 1, 1), 0, 0),
        ("1", "1", 4, 115, (1, 0, 1), 0, 0),
        ("123", "1", 2, 100, (2, 1, 1), 0, 0),
        ("12", "1", 3, 125, (1, 1, 1), 0, 0),
        ("1", "", 3, 110, (1, 1, 0), 0, 0),
    ],
    ("Z0-raw", "synth-b"): [
        ("4", "4", 2, 85, (1, 1, 1), 0, 0),
        ("45", "4", 2, 95, (1, 1, 1), 0, 0),
        ("4", "", 1, 90, (1, 2, 1), 0, 0),
        ("4", "4", 2, 75, (1, 1, 1), 0, 0),
        ("45", "4", 1, 105, (1, 1, 1), 0, 0),
    ],
    ("Z0", "synth-a"): [
        ("123", "12", 2, 100, (2, 1, 1), 0, 0),
        ("12", "1", 3, 110, (1, 1, 1), 0, 0),
        ("1234", "12", 1, 95, (2, 2, 1), 0, 0),
        ("13", "1", 2, 120, (1, 1, 2), 0, 0),
        ("123", "12", 2, 105, (2, 1, 0), 0, 0),
    ],
    ("Z0", "synth-b"): [
        ("45", "4", 1, 80, (1, 1, 1), 0, 0),
        ("456", "4", 2, 90, (1, 2, 1), 0, 0),
        ("4", "4", 1, 85, (2, 1, 1), 0, 0),
        ("45", "4", 1, 70, (1, 1, 1), 0, 0),
        ("456", "46", 0, 110, (1, 1, 1), 0, 0),
    ],
    ("K", "synth-a"): [
        ("1235", "12", 2, 115, (2, 1, 1), 0, 0),
        ("125", "12", 2, 120, (1, 1, 1), 0, 0),
        ("1235", "125", 3, 110, (2, 1, 2), 0, 0),
        ("1234", "12", 2, 130, (1, 2, 1), 0, 0),
        ("125", "12", 1, 125, (1, 1, 1), 0, 0),
    ],
    ("K", "synth-b"): [
        ("457", "4", 1, 95, (1, 1, 1), 0, 0),
        ("45", "4", 2, 105, (1, 1, 1), 0, 0),
        ("4567", "46", 1, 100, (2, 1, 1), 0, 0),
        ("457", "4", 1, 90, (1, 1, 1), 0, 0),
        ("45", "4", 0, 110, (1, 1, 2), 0, 0),
    ],
    ("SS", "synth-a"): [
        ("12356", "1235", 2, 135, (1, 1, 1), 3, 1),
        ("1256", "125", 3, 140, (1, 1, 0), 4, 0),
        ("1234", "12", 2, 190, (1, 1, 2), 0, 0),
        ("1256", "1256", 2, 145, (2, 1, 1), 2, 1),
        ("12356", "125", 1, 138, (1, 0, 1), 3, 2),
    ],
    ("SS", "synth-b"): [
        ("45678", "468", 2, 130, (1, 1, 1), 2, 1),
        ("4568", "46", 1, 150, (1, 1, 1), 3, 0),
        ("45678", "4678", 1, 128, (2, 1, 1), 2, 1),
        ("458", "48", 2, 160, (1, 1, 1), 2, 1),
        ("4568", "468", 0, 142, (1, 2, 1), 3, 0),
    ],
}
# special cases: (arm, doc, replicate) -> what happened
FALLBACK = {
    ("SS", "synth-a", 3): "kill"
}  # the pre-pass was killed: no probe lines, the Z0 brief
KILLED = {
    ("SS", "synth-b", 4): "t4-1"
}  # the hang guard killed this reviewer; a stray report file is left behind
INVALID = {
    ("K", "synth-b", 2): "t3-1"
}  # a clean run whose findings block did not parse: no report
RETRIED = {
    ("K", "synth-a", 1): "t2b-1"
}  # two attempts (a pre-DD-8 style run), one retry
BLOCKS = {k: k for k in range(1, REPS + 1)}


def _slug(arm):
    return arm.lower().replace("-", "")


def _line(n, extra=None):
    row = {
        "id": f"F{n}",
        "severity": "MINOR",
        "blocking": False,
        "category": "other",
        "anchor": "returns an empty result for an empty report",
        "refs": [],
        "claim": "The wording leaves one reading open.",
    }
    row.update(extra or {})
    return json.dumps(row)


def _report(nonprobe, probes, ledger):
    lines, n = [], 1
    for _ in range(nonprobe):
        lines.append(_line(n))
        n += 1
    for i in range(probes):
        lines.append(_line(n, {"probe": f"S{i + 1}", "class": "C4", "src": None}))
        n += 1
    for i in range(ledger):
        lines.append(_line(n, {"probe": None, "class": "C1", "src": "ledger"}))
        n += 1
    return (
        "review: 1 of 3\n\n## Findings block\n\n```findings-v1\n"
        + "\n".join(lines)
        + "\n```\n\nverdict: PASS\n"
    )


def specs(arms=DEFAULT_ARMS, docs=DOCS):
    """One dict per run, in a fixed order, with everything the writer and the expected values need."""
    out = []
    for arm in arms:
        for doc in docs:
            for k, row in enumerate(TABLE[(arm, doc)], 1):
                found, blocking, wrong, secs, np3, probes, ledger = row
                key = (arm, doc, k)
                status = {rid: "ok" for rid in RIDS}
                if key in KILLED:
                    status[KILLED[key]] = "killed"
                if key in INVALID:
                    status[INVALID[key]] = "invalid"
                out.append(
                    {
                        "arm": arm,
                        "doc": doc,
                        "rep": k,
                        "block": BLOCKS[k],
                        "found": {f"GT{c}" for c in found},
                        "blocking": {f"GT{c}" for c in blocking},
                        "wrong": wrong,
                        "secs": float(secs),
                        "np": dict(zip(RIDS, np3)),
                        "probes": probes,
                        "ledger": ledger,
                        "status": status,
                        "fallback": key in FALLBACK,
                        "reason": FALLBACK.get(key),
                        "attempts": {
                            rid: 2 if RETRIED.get(key) == rid else 1 for rid in RIDS
                        },
                        "tokens": {
                            rid: 0 if status[rid] == "killed" else 1000 + 10 * k
                            for rid in RIDS
                        },
                    }
                )
    return out


def write_run(runs_dir, scoring_dir, s, label):
    """Write one run folder and its judge folder from a spec dict (see specs); returns the run folder."""
    run = Path(runs_dir) / f"{_slug(s['arm'])}-{s['doc']}-r{s['rep']}"
    for sub in ("reviews", "normalised", "scoring"):
        (run / sub).mkdir(parents=True)
    (run / "run.json").write_text(
        json.dumps(
            {
                "arm": s["arm"],
                "panel": "primary",
                "doc": s["doc"],
                "replicate": s["rep"],
                "seed": 1,
                "block": s["block"],
                "fallback": s["fallback"],
                "reason": s["reason"],
                "reviewers": len(RIDS),
                "reviewer_status": {
                    rid: {"model": MODELS[rid], "status": s["status"][rid]}
                    for rid in RIDS
                },
            }
        )
    )
    (run / "timing.json").write_text(
        json.dumps({"panel_elapsed_s": s["secs"], "slowest_reviewer_s": s["secs"] - 10})
    )
    probes = 0 if s["fallback"] else s["probes"]
    ledger = 0 if s["fallback"] else s["ledger"]
    folder = "reviews" if s["arm"] == "Z0-raw" else "normalised"
    for i, rid in enumerate(RIDS):
        st = s["status"][rid]
        (run / "reviews" / f"{rid}.meta.json").write_text(json.dumps({"status": st}))
        (run / "reviews" / f"{rid}.cost.json").write_text(
            json.dumps(
                {
                    "attempts": s["attempts"][rid],
                    "total_output_tokens_all": s["tokens"][rid],
                    "killed": st == "killed",
                }
            )
        )
        # probe and ledger lines sit in the second and third reviewer's reports; a missing report is a reviewer not ok
        text = _report(s["np"][rid], probes if i == 1 else 0, ledger if i == 2 else 0)
        if st == "ok":
            (run / folder / f"{rid}.md").write_text(text)
        elif st == "killed":  # a leftover that the analysis must not count
            (run / "normalised" / f"{rid}.md").write_text(_report(3, 0, 0))
    jd = Path(scoring_dir) / label
    jd.mkdir(parents=True)
    (jd / "score.json").write_text(
        json.dumps(
            {
                "label": label,
                "combo": "blind",
                "package": s["doc"],
                "gt_total": ITEMS,
                "gt_covered_any": sorted(s["found"]),
                "gt_covered_blocking": sorted(s["blocking"]),
                "ledger_rows_total": 4,
                "ledger_rows_blocking": 1,
                "blocking_rows_gt_matched": 0,
                "wrong_blockers": s["wrong"],
                "notes": "invented",
            }
        )
    )
    (run / "scoring" / "label-key.json").write_text(
        json.dumps(
            {
                "label": label,
                "dir": str(jd),
                "run": run.name,
                "doc": s["doc"],
                "second": None,
            }
        )
    )
    return run


# --- the expected values: plain loops and sets, written out from the tables above ------------------------------------


def _expected_group(by_doc):
    """by_doc: {doc: [spec, ...]}. Returns the group values that analysis.analyze.group_metrics must produce."""
    runs = [s for g in by_doc.values() for s in g]
    n = len(runs)
    found = [len(s["found"]) / ITEMS for s in runs]
    blk = [len(s["blocking"]) / ITEMS for s in runs]
    secs = sorted(s["secs"] for s in runs)
    median = secs[n // 2] if n % 2 else (secs[n // 2 - 1] + secs[n // 2]) / 2
    pos = (n - 1) * 0.9
    lo = int(pos)
    p90 = secs[lo] + (secs[min(lo + 1, n - 1)] - secs[lo]) * (pos - lo)
    consistent, seen = 0, 0
    for g in by_doc.values():
        for item in range(1, ITEMS + 1):
            hits = sum(f"GT{item}" in s["found"] for s in g)
            if hits:
                seen += 1
            if hits * 10 >= 6 * len(g):
                consistent += 1
    # run_jaccard pools the pairs of all documents (pairs never cross documents)
    all_pairs = []
    for g in by_doc.values():
        sets = [s["found"] for s in g]
        for i in range(len(sets)):
            for j in range(i + 1, len(sets)):
                if sets[i] | sets[j]:
                    all_pairs.append(len(sets[i] & sets[j]) / len(sets[i] | sets[j]))
    nonprobe = [
        sum(c for rid, c in s["np"].items() if s["status"][rid] == "ok") for s in runs
    ]
    toks = [sum(s["tokens"].values()) for s in runs]
    reach = {}
    for s in runs:
        for item in range(1, ITEMS + 1):
            cls = f"C{item}"
            k, t = reach.get(cls, (0, 0))
            reach[cls] = (k + (f"GT{item}" in s["found"]), t + 1)
    return {
        "runs": n,
        "found_fraction": {"per_run": found, "mean": sum(found) / n},
        "found_blocking_fraction": {"per_run": blk, "mean": sum(blk) / n},
        "share_runs_found_half": sum(len(s["found"]) >= ITEMS / 2 for s in runs) / n,
        "run_jaccard": sum(all_pairs) / len(all_pairs) if all_pairs else None,
        "consistent_items": consistent,
        "consistent_share": consistent / (ITEMS * len(by_doc)),
        "stable_hit_rate": consistent / seen if seen else None,
        "wrong_blockers": {
            "per_run": [s["wrong"] for s in runs],
            "mean": sum(s["wrong"] for s in runs) / n,
        },
        "nonprobe_findings": {"per_run": nonprobe, "mean": sum(nonprobe) / n},
        "elapsed_s": {
            "per_run": [s["secs"] for s in runs],
            "mean": sum(secs) / n,
            "median": median,
            "p90": p90,
        },
        "tokens": {"per_run": toks, "mean": sum(toks) / n},
        "kills": sum(v == "killed" for s in runs for v in s["status"].values()),
        "retries": sum(a - 1 for s in runs for a in s["attempts"].values()),
        "fallbacks": sum(s["fallback"] for s in runs),
        "invalid": sum(
            v not in ("ok", "killed") for s in runs for v in s["status"].values()
        ),
        "class_reach": {
            c: {"found": k, "trials": t, "reach": k / t}
            for c, (k, t) in sorted(reach.items())
        },
    }


def expected(spec_list):
    arms = {}
    for arm in sorted({s["arm"] for s in spec_list}):
        mine = [s for s in spec_list if s["arm"] == arm]
        by_doc = {}
        for s in mine:
            by_doc.setdefault(s["doc"], []).append(s)
        arms[arm] = {
            "runs": len(mine),
            "docs": {d: _expected_group({d: g}) for d, g in sorted(by_doc.items())},
            "pooled": _expected_group(dict(sorted(by_doc.items()))),
        }
    return {"schema": "sweep-metrics/1", "arms": arms}


def build(root, arms=DEFAULT_ARMS, docs=DOCS):
    """Write the runs, the judge folders and expected.json under root; returns a namespace of the paths and values."""
    root = Path(root)
    runs, scoring = root / "runs" / "stage1", root / "scoring" / "stage1"
    runs.mkdir(parents=True)
    spec_list = specs(arms, docs)
    for n, s in enumerate(spec_list, 1):
        write_run(runs, scoring, s, f"j{n:06x}")
    exp = expected(spec_list)
    (root / "expected.json").write_text(json.dumps(exp, indent=1, sort_keys=True))
    return SimpleNamespace(
        root=root, runs=runs, scoring=scoring, specs=spec_list, expected=exp
    )


# --- stage runs: one sheet run and one plain run on fixtures/plans/p_basic.md, for the stage tests ---------------------

FIXTURES = Path(__file__).resolve().parents[1]
STAGE_DOC = "synth-a"
GT_FILE = FIXTURES / "gt" / "synthetic-gt.json"
PLAN = FIXTURES / "plans" / "p_basic.md"
UNRELATED = "Run the full test suite and sync `docs/guide.md` with the code."


def _line_of(text, quote):
    """The 1-based line of the first line that holds the quote (a plain search, not the code under test)."""
    for n, ln in enumerate(text.splitlines(), 1):
        if quote in ln:
            return n
    raise ValueError(quote)


def _entry(text, anchor, item_id, cls=None):
    n = _line_of(text, anchor)
    return {
        "item_id": item_id,
        "class": cls,
        "anchor_text": anchor,
        "location": {"line_start": n, "line_end": n},
    }


def _row(item, verdict, supported):
    return {"item": item, "verdict": verdict, "supported": supported}


def _led(rows, findings, promoted=()):
    return {
        "ledger": {"rows": rows},
        "findings": [{"id": i, "row_item": it, "link": "probe"} for i, it in findings],
        "promoted": list(promoted),
    }


def build_stage_runs(root):
    """Write root/cand/synth-a/candidate.md, root/runs/stage-s/{ss-stage-r1, z0-stage-r1} and their judge folders.

    The sheet run (SS): selected items S1 (the quote of GT1), S3 (GT5), S4 (GT6), S5 (GT7); a dropped candidate for GT3; one
    unrelated candidate; nothing for GT4 and GT8. The judge credits GT1, GT4 and GT6. The plain run (Z0): finding F1 of t2b-1
    anchors the text of GT6, F2 the text of GT1; the merge holds F1 only; the judge credits GT6.
    """
    root = Path(root)
    plan = PLAN.read_text(encoding="utf-8")
    cand = root / "cand" / STAGE_DOC
    cand.mkdir(parents=True)
    (cand / "candidate.md").write_text(plan, encoding="utf-8")
    quotes = {
        g["id"]: g["plan_quote"] for g in json.loads(GT_FILE.read_text())["items"]
    }
    runs, scoring = root / "runs" / "stage-s", root / "scoring" / "stage-s"
    for sub in ("ss-stage-r1", "z0-stage-r1"):
        for d in ("reviews", "normalised", "scoring", "prepass", "check", "merged"):
            (runs / sub / d).mkdir(parents=True)
    ss, z0 = runs / "ss-stage-r1", runs / "z0-stage-r1"
    # the sheet run
    items = [
        _entry(plan, quotes["GT1"], "S1", "C1"),
        _entry(plan, quotes["GT5"], "S3", "C5"),
        _entry(plan, quotes["GT6"], "S4", "C6"),
        _entry(plan, quotes["GT7"], "S5", "C7"),
    ]
    cands = [
        *items,
        {**_entry(plan, quotes["GT3"], None, "C3"), "drop_reason": "pre_rank"},
        _entry(plan, UNRELATED, None, "C1"),
    ]
    (ss / "prepass" / "items.json").write_text(json.dumps({"items": items}))
    (ss / "prepass" / "candidates.json").write_text(json.dumps({"candidates": cands}))
    rows_a = [
        _row("S1", "PROBLEM", True),
        _row("S3", "PROBLEM", True),
        _row("S4", "PROBLEM", True),
        _row("S5", "PROBLEM", False),
    ]
    rows_b = [
        _row("S1", "OK", False),
        _row("S3", "OK", False),
        _row("S4", "PROBLEM", True),
        _row("S5", "OK", False),
    ]
    led_a = _led(
        rows_a,
        [("F1", "S1"), ("F4", "S4"), ("F5", "S5")],
        [{"id": "PS3", "item": "S3", "class": "C5", "line": 30}],
    )
    led_b = _led(rows_b, [("F1", "S4")])
    (ss / "check" / "t2b-1.ledger.json").write_text(json.dumps(led_a))
    (ss / "check" / "t3-1.ledger.json").write_text(json.dumps(led_b))
    members = [
        {"reviewer_id": "t2b-1", "fid": "F1"},
        {"reviewer_id": "t3-1", "fid": "F1"},
    ]
    (ss / "merged" / "ledger.json").write_text(
        json.dumps({"rows": [{"members": members}]})
    )
    # the plain run
    (z0 / "merged" / "ledger.json").write_text(
        json.dumps({"rows": [{"members": [{"reviewer_id": "t2b-1", "fid": "F1"}]}]})
    )
    anchors = {
        "t2b-1": [
            ("F1", "only the retention job removes a report file"),
            ("F2", "returns an empty result for an empty report"),
        ],
        "t3-1": [("F1", UNRELATED)],
    }
    for rid, found in anchors.items():
        lines = [
            json.dumps(
                {
                    "id": i,
                    "severity": "MINOR",
                    "blocking": False,
                    "category": "other",
                    "anchor": a,
                    "refs": [],
                    "claim": "A wording point.",
                }
            )
            for i, a in found
        ]
        text = (
            "review: 1 of 3\n\n## Findings block\n\n```findings-v1\n"
            + "\n".join(lines)
            + "\n```\n\nverdict: PASS\n"
        )
        (z0 / "normalised" / f"{rid}.md").write_text(text)
    for run, arm, found, label in (
        (ss, "SS", ("GT1", "GT4", "GT6"), "js0001"),
        (z0, "Z0", ("GT6",), "js0002"),
    ):
        status = {rid: {"model": MODELS[rid], "status": "ok"} for rid in RIDS}
        (run / "run.json").write_text(
            json.dumps(
                {
                    "arm": arm,
                    "panel": "primary",
                    "doc": STAGE_DOC,
                    "replicate": 1,
                    "block": 1,
                    "fallback": False,
                    "reason": None,
                    "reviewers": 3,
                    "reviewer_status": status,
                }
            )
        )
        (run / "timing.json").write_text(
            json.dumps({"panel_elapsed_s": 100.0, "slowest_reviewer_s": 90.0})
        )
        jd = scoring / label
        jd.mkdir(parents=True)
        (jd / "score.json").write_text(
            json.dumps(
                {
                    "label": label,
                    "gt_total": ITEMS,
                    "gt_covered_any": list(found),
                    "gt_covered_blocking": [],
                    "wrong_blockers": 0,
                }
            )
        )
        (run / "scoring" / "label-key.json").write_text(
            json.dumps(
                {
                    "label": label,
                    "dir": str(jd),
                    "run": run.name,
                    "doc": STAGE_DOC,
                    "second": None,
                }
            )
        )
    return SimpleNamespace(
        root=root, runs=runs, cand_root=root / "cand", gt=GT_FILE, scoring=scoring
    )
