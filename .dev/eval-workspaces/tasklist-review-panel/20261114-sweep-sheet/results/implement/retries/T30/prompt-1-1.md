7bafcbf33de7c8149d90339da1813c48ade1408b
Review one task for spec compliance.

Task brief: ## Task 30: Add the gates, shares, stage rows, preregistration and report to the analysis script

Depends on: Task 29, Task 28, Task 26

Extend `analysis/analyze.py` with the subcommands `all`, `audit-judges`, `compliance`, `prereg` and `sample-second-judge` and the outputs of DESIGN 14.3: gates D1 to D7 with a bootstrap that resamples documents first and then runs, the three shares (`Z0 - Z0raw`, `K - Z0`, `SS - Z0`) as three labelled lines never summed, `stages.jsonl` rows with the five stage fields (extraction, selection, act, merge survival read from `merged/ledger.json` through `(reviewer_id, finding id)`, judge credit), `ok_rate_planted.json`, `judge_audit.json`, the break-even values (planned and measured side by side), the DD-7 count of `## Ledger` headings in Z0 and K reports, the REQ-45 claim sentence, the D6 blocking rule and `prereg --write` with `prereg.json` carrying a band `[lo, hi]` with `0 <= lo < hi <= 1` for each of C1 to C8. Create `tests/test_report.py`, `tests/test_stages.py`, `tests/test_prereg.py` and `tests/test_verifier_off_path.py`.

Acceptance criteria:
- T30.AC1: `$T $SW/tests/test_report.py $SW/tests/test_stages.py $SW/tests/test_prereg.py $SW/tests/test_verifier_off_path.py $SW/tests/test_analyze.py -q` exits 0.
- T30.AC2: Required tests present: `test_three_shares_separate`, `test_no_summed_headline`, `test_breakeven_values`, `test_report_shows_planned_and_measured`, `test_claim_template_text`, `test_stage_rows_schema`, `test_stage_values_on_fixture`, `test_act_bands_for_all_classes`, `test_d6_failure_blocks_adoption`, `test_no_verifier_step_in_clock`, `test_verifier_default_off` and `test_verifier_time_excluded`.
- T30.AC3: `breakeven(b=122)` prints about 21.7 s and 3.71 s; the claim sentence equals the REQ-45 sentence and no other sentence uses "consistent" for another class; a fixture where D2 and D3 pass and D6 fails gives "do not adopt".
- T30.AC4: `analysis/analyze.py` never reads a `ground-truth*.json`; `stages.jsonl` takes the ground-truth path as an argument and tests pass only the synthetic one. Dependents: `bin/make-schedule.py` and `bin/check-order.sh` read the `prereg.json` it writes (Tasks 32 and 33).
Global constraints: - Names used by every task. `SW` is the folder `.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet` (repo-relative). Its three specification files are `SW/DESIGN.md`, `SW/IMPLEMENTATION.md` (section 2 holds the steps) and `SW/TESTING.md` (section 2 fixtures, section 3 requirement map, section 4 constraint tests). Section and row names in a task refer to those files. Test names written `file::function` live under `SW/tests/`. `MR` is `.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md`, `RR` is `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh`, `JJ` is `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/tmp-scripts/judge-one.sh`, `FND` is `src/superclaude/cli/review/findings.py`, `MRG` is `src/superclaude/cli/review/merge_cmd.py`, `LED` is `src/superclaude/cli/review/ledger.py`.
- Shell variables for every command, run from the repository root: `REPO="$(git rev-parse --show-toplevel)"`, `SW="$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet"`, `T="uv run --frozen --project $REPO pytest -p no:cacheprovider"`, `PYRUN="uv run --frozen --project $REPO python"`, and `export PYTHONDONTWRITEBYTECODE=1`. Python only through `uv run`; never `python -m`, `pip install` or bare `python script.py`.
- Git-write check. `gitcheck() { grep -rnE '\bgit\b[^|;&]*\b(add|commit|tag|push)\b' "$1" | grep -vE 'git -C "\$\{?SB[A-Za-z_]*\}?' | grep -vE ':[0-9]+:[[:space:]]*(#|echo|printf)'; }` prints nothing for a directory when no script in it runs `git add`, `commit`, `tag` or `push` except as `git -C "$SB..."` (a sandbox directory variable), in printed text or in a comment. A script that must read a tag uses `git rev-parse`, `git log` or `git for-each-ref`, never `git tag`. Tasks 8, 27 and 33 run it; Task 27 also shows it prints the probe line for a temporary file that holds `git add -A`, so the check is not vacuous.
- Write scope (DESIGN K1). Every file the build creates lives under `SW`. Scratch goes only to pytest `tmp_path` or `/tmp`; the sandbox root is `/tmp/evalsb-sweep`. `src/`, `tests/`, `.claude/` and every existing folder under `.dev/tasks/` are not touched. Evidence a task produces is written under `SW/results/`, not into this plan's package.
- Git scope. The build stages, commits and pushes nothing, and creates no tag (DESIGN K5). Staging of this plan's package stays with the session that runs `/sc:implement`. The sandbox builder's own `git init`, `git add` and snapshot commit run inside a throwaway sandbox under `/tmp` and are not repository writes; they are spelled `git -C "$SB..."`, which is how the git-write check (`gitcheck`, above) tells them from a write to the real repository.
- No model. No reviewer, judge or spike session is started. Every test that needs `claude` uses the fake `SW/tests/fakes/claude` (TESTING F-FAKE). Scripts that start models in real use (`bin/run-spike.sh`, `bin/run-schedule.sh`, `bin/judge-batch.sh`) are built and tested only against the fake.
- Never open any `ground-truth*.json` or score file. Tests marked `freeze` (the real-ground-truth lint, the recall tests) are written but not run by the build; the build runs `-m "not slow and not freeze"` plus `-m slow` where a task says so.
- Read-only imports. `FND`, `MRG` and `LED` are imported or called, never edited. `FND._check_finding` and `FND._blocks_after` are private; they are reached only through `SW/scaffold/fnd.py` (DESIGN section 2.3).
- Folder names. No folder is named `lib/` (`.gitignore` line 13 ignores it; DESIGN K7). Code folders are `scaffold/`, `sweep/` and `analysis/`.
- Decisions DD-1 to DD-15 of DESIGN section 1.3 hold as written; a conflict between this plan and DESIGN.md is settled by DESIGN.md. Step 0 is done (`SW/results/step0.md`); its sub-steps 0.4, 0.5 and 0.6 were not run, so the task that needs each one runs or reads it first (0.4 in Task 24, 0.5 in Task 26, 0.6 in Tasks 6 and 28). Step 0.3 measured a scope taken from IMPLEMENTATION.md, not the DD-5 scope; Task 23 measures the DD-5 scope.
- Out of scope: steps 14 to 16, Redesign 2, the optional verifier of `MR` 3.0.9, any change under `src/`, and any file under `fixtures/recall/` or `holdout-gt/`.
- Line counts in the design are planning values (unmeasured).
Start sha: 7bafcbf33de7c8149d90339da1813c48ade1408b
Diff against the start snapshot: diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/analysis/analyze.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/analysis/analyze.py
index b7a592330..f9e147304 100644
--- a/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/analysis/analyze.py
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/analysis/analyze.py
@@ -32,6 +32,8 @@ from __future__ import annotations
 import argparse
 import json
 import math
+import os
+import random
 import sys
 from dataclasses import dataclass, field
 from pathlib import Path
@@ -39,7 +41,7 @@ from pathlib import Path
 SW = Path(__file__).resolve().parents[1]
 sys.path.insert(0, str(SW))
 
-from scaffold import fnd  # noqa: E402
+from scaffold import clock, fnd, judge  # noqa: E402
 
 SCHEMA = "sweep-metrics/1"
 CONSISTENT_NUM, CONSISTENT_DEN = 6, 10  # reached in at least 60% of the runs
@@ -62,6 +64,8 @@ METRICS = (
     "retries",
     "fallbacks",
     "class_reach",
+    "ledger_headings",
+    "ok_rate_planted",
 )
 
 
@@ -79,6 +83,8 @@ class Run:
     reason: object
     elapsed: float
     reviewers: dict  # rid -> {"status", "attempts", "tokens", "nonprobe"}
+    panel: str | None = None
+    slowest: float | None = None  # timing.json slowest_reviewer_s: the run's own b
     found_any: frozenset | None = None
     found_blocking: frozenset | None = None
     gt_total: int = 0
@@ -156,6 +162,8 @@ def load_run(folder, scores=True) -> Run:
         reason=meta.get("reason"),
         elapsed=float(t["panel_elapsed_s"]),
         reviewers={rid: _reviewer(folder, rid, st) for rid, st in status.items()},
+        panel=meta.get("panel"),
+        slowest=t.get("slowest_reviewer_s"),
         path=folder,
     )
     if scores:
@@ -448,6 +456,744 @@ def d1_inputs(runs, arm, base="Z0") -> dict:
     )
 
 
+# --- gates D1 to D7 (MR 5.7), shares and the outcome ------------------------------------------------------------------
+
+BOOTSTRAP_SEED = 20261115
+BOOTSTRAP_N = 2000
+BOOTSTRAP_Q = 0.05  # the lower end of the two-sided 90% interval
+EPS = 1e-9
+GENERAL_CLASSES = ("C2", "C4", "C5", "C6", "C8")
+CLASSES = tuple(f"C{n}" for n in range(1, 9))
+# Documents that are not decision documents: the derivation set, the planted set, clean twins, documentation, the sanity set.
+NON_DECISION = frozenset(
+    {
+        "planted",
+        "twin",
+        "docs",
+        "spec",
+        "derivation",
+        "sanity",
+        "defect-rich",
+        "control",
+    }
+)
+BLOCKING = ("D6",)
+LIMITS = {
+    "d1_median_ratio": 1.35,
+    "d1_p90_ratio": 1.50,
+    "d1_kill_share": 0.10,
+    "d2_effect": 0.12,
+    "d2_lower_bound": 0.04,
+    "d3_consistent_items": 3,
+    "d4_wrong_blockers": 1.0,
+    "d4_twin_blocking": 0.7,
+    "d5_detection": 0.40,
+    "d5_classes": 3,
+    "d6_within": 0.10,
+    "d6_reach_floor": 0.5,
+    "d7_gain": 0.04,
+}
+# REQ-45: the one sentence that may be written about consistency.
+CLAIM = (
+    "raises the per-run found fraction; consistency is expected only for I4 and I7 (classes C4 and C8), "
+    "and only for Redesign 1 at the high end of its range"
+)
+ARMS = ("Z0-raw", "Z0", "K", "SS")
+SHARES = (
+    ("H share", "Z0", "Z0-raw", "Z0 - Z0raw"),
+    ("Prompting share", "K", "Z0", "K - Z0"),
+    ("Redesign share", "SS", "Z0", "SS - Z0"),
+)
+# DESIGN 15.1 decision 2 and 1: recommended values, used until the owner gives others.
+ACT_BANDS = {
+    "C1": [0.10, 0.40],
+    "C2": [0.20, 0.45],
+    "C3": [0.03, 0.15],
+    "C4": [0.50, 0.75],
+    "C5": [0.35, 0.60],
+    "C6": [0.05, 0.30],
+    "C7": [0.15, 0.35],
+    "C8": [0.40, 0.65],
+}
+RECOMMENDED_FLOOR = 0.45
+STAGE1_RUNS = {"panel_runs": 75, "arms_z0_k_ss": 60, "z0_raw": 15}
+
+
+def load_sets(path=None) -> dict:
+    """{document id: set} from config/packages.json (`packages.<doc>.set`). A document that is not listed is a decision document."""
+    p = Path(path) if path else SW / "config" / "packages.json"
+    return {d: v.get("set") for d, v in _json(p).get("packages", {}).items()}
+
+
+def doc_set(sets, doc):
+    return (sets or {}).get(doc) or "holdout"
+
+
+def decision_runs(runs, sets=None):
+    return [r for r in runs if doc_set(sets, r.doc) not in NON_DECISION]
+
+
+def _arm(runs, arm):
+    return [r for r in runs if r.arm == arm]
+
+
+def _common(a, b):
+    """The runs of the two arms on the documents that both have."""
+    docs = {r.doc for r in a} & {r.doc for r in b}
+    return [r for r in a if r.doc in docs], [r for r in b if r.doc in docs]
+
+
+def mean_found(runs):
+    return _mean([found_fraction(r) for r in runs])
+
+
+def bootstrap_lower(
+    arm_runs, base_runs, seed=BOOTSTRAP_SEED, n=BOOTSTRAP_N, q=BOOTSTRAP_Q
+):
+    """Lower bound of the arm-minus-base difference of mean found fraction: documents are resampled first, then the runs."""
+    a_by = {d: [found_fraction(r) for r in g] for d, g in _by_doc(arm_runs).items()}
+    b_by = {d: [found_fraction(r) for r in g] for d, g in _by_doc(base_runs).items()}
+    docs = sorted(set(a_by) & set(b_by))
+    if not docs:
+        raise AnalysisError("no document with runs of both arms")
+    rng = random.Random(seed)
+    diffs = []
+    for _ in range(n):
+        a_vals, b_vals = [], []
+        for _d in docs:
+            d = docs[rng.randrange(len(docs))]
+            a_vals += [rng.choice(a_by[d]) for _ in a_by[d]]
+            b_vals += [rng.choice(b_by[d]) for _ in b_by[d]]
+        diffs.append(sum(a_vals) / len(a_vals) - sum(b_vals) / len(b_vals))
+    return percentile(diffs, q)
+
+
+def _status(checks):
+    if any(c is False for c in checks):
+        return "fail"
+    if any(c is None for c in checks):
+        return "pending"
+    return "pass"
+
+
+def gate_d1(runs, arm, base):
+    inputs, checks = {}, []
+    for panel in sorted({r.panel or "" for r in _arm(runs, arm)}):
+        d = d1_inputs([r for r in runs if (r.panel or "") == panel], arm, base)
+        inputs[panel or "unknown"] = d
+        docs = d["docs"].values()
+        checks += [
+            all(v["ratio"] <= LIMITS["d1_median_ratio"] + EPS for v in docs),
+            all(v["p90_ratio"] <= LIMITS["d1_p90_ratio"] + EPS for v in docs),
+            d["kill_share"] is not None
+            and d["kill_share"] <= LIMITS["d1_kill_share"] + EPS,
+        ]
+    return {"status": _status(checks), "inputs": inputs}
+
+
+def _effect(arm_runs, base_runs):
+    a, b = _common(arm_runs, base_runs)
+    if not a:
+        return None
+    return {
+        "difference": mean_found(a) - mean_found(b),
+        "lower_bound": bootstrap_lower(a, b),
+        "arm_mean": mean_found(a),
+        "base_mean": mean_found(b),
+    }
+
+
+def gate_d2(arm_runs, base_runs):
+    e = _effect(arm_runs, base_runs)
+    if e is None:
+        return {"status": "pending"}
+    ok = (
+        e["difference"] + EPS >= LIMITS["d2_effect"]
+        and e["lower_bound"] > LIMITS["d2_lower_bound"]
+    )
+    return {"status": _status([ok]), **_r(e)}
+
+
+def gate_d3(arm_runs, base_runs):
+    a, b = _common(arm_runs, base_runs)
+    if not a:
+        return {"status": "pending"}
+    ca, cb = consistent_items(a), consistent_items(b)
+    ok = ca >= cb + LIMITS["d3_consistent_items"]
+    return {
+        "status": _status([ok]),
+        "arm_consistent_items": ca,
+        "base_consistent_items": cb,
+    }
+
+
+def merged_blocking_rows(run) -> int:
+    p = run.path / "merged" / "ledger.json"
+    if not p.is_file():
+        return 0
+    return sum(bool(row.get("blocking")) for row in _json(p).get("rows", []))
+
+
+def gate_d4(runs, arm, base, sets):
+    a, b = _common(
+        _arm(decision_runs(runs, sets), arm), _arm(decision_runs(runs, sets), base)
+    )
+    if not a:
+        return {"status": "pending"}
+    wa, wb = (
+        _mean([wrong_blockers(r) for r in a]),
+        _mean([wrong_blockers(r) for r in b]),
+    )
+    out = {
+        "wrong_blockers_arm": wa,
+        "wrong_blockers_base": wb,
+        "wrong_blockers_difference": wa - wb,
+    }
+    checks = [wa - wb <= LIMITS["d4_wrong_blockers"] + EPS]
+    ta = [r for r in _arm(runs, arm) if doc_set(sets, r.doc) == "twin"]
+    tb = [r for r in _arm(runs, base) if doc_set(sets, r.doc) == "twin"]
+    if ta and tb:
+        da, db = (
+            _mean([merged_blocking_rows(r) for r in ta]),
+            _mean([merged_blocking_rows(r) for r in tb]),
+        )
+        out.update(
+            twin_blocking_arm=da,
+            twin_blocking_base=db,
+            twin_blocking_difference=da - db,
+        )
+        checks.append(da - db <= LIMITS["d4_twin_blocking"] + EPS)
+    else:
+        checks.append(None)  # no clean-twin runs yet
+    return {"status": _status(checks), **_r(out)}
+
+
+def gate_d5(runs, arm, base, sets, classes):
+    mine = [r for r in _arm(runs, arm) if doc_set(sets, r.doc) == "planted"]
+    out, checks = {}, []
+    if mine and classes:
+        reach = class_reach(mine, classes)
+        det = {c: reach[c]["reach"] for c in GENERAL_CLASSES if c in reach}
+        passing = sorted(c for c, v in det.items() if v + EPS >= LIMITS["d5_detection"])
+        out.update(planted_detection=det, planted_classes_passing=passing)
+        checks.append(len(passing) >= LIMITS["d5_classes"])
+    else:
+        checks.append(None)
+    for label in ("docs", "spec"):
+        a = [r for r in _arm(runs, arm) if doc_set(sets, r.doc) == label]
+        b = [r for r in _arm(runs, base) if doc_set(sets, r.doc) == label]
+        e = _effect(a, b) if a and b else None
+        if e is None:
+            checks.append(None)
+            continue
+        out[f"{label}_difference"], out[f"{label}_lower_bound"] = (
+            e["difference"],
+            e["lower_bound"],
+        )
+        checks.append(
+            e["difference"] + EPS >= LIMITS["d2_effect"] and e["lower_bound"] > 0
+        )
+    return {"status": _status(checks), **_r(out)}
+
+
+def _item_reach(runs):
+    return {(d, g): hit / n for d, g, hit, n in _reach(runs)}
+
+
+def gate_d6(arm_runs, base_runs):
+    a, b = _common(arm_runs, base_runs)
+    if not a:
+        return {"status": "pending"}
+    ra, rb = _item_reach(a), _item_reach(b)
+    checked = sorted(k for k, v in rb.items() if v + EPS >= LIMITS["d6_reach_floor"])
+    failing = [
+        {
+            "doc": d,
+            "item": g,
+            "base_reach": rb[(d, g)],
+            "arm_reach": ra.get((d, g), 0.0),
+        }
+        for d, g in checked
+        if ra.get((d, g), 0.0) < rb[(d, g)] - LIMITS["d6_within"] - EPS
+    ]
+    status = "fail" if failing else ("pass" if checked else "pending")
+    return {
+        "status": status,
+        "items_checked": len(checked),
+        "failing_items": _r(failing),
+    }
+
+
+def gate_d7(arm_runs, checklist_runs):
+    e = _effect(arm_runs, checklist_runs)
+    if e is None:
+        return {"status": "pending"}
+    ok = e["difference"] + EPS >= LIMITS["d7_gain"]
+    return {
+        "status": _status([ok]),
+        "gain": round(e["difference"], DIGITS),
+        "winner": "arm" if ok else "checklist",
+    }
+
+
+def outcome(g) -> dict:
+    """The adoption result of the gates: any failed gate means do not adopt; D6 is blocking (REQ-42)."""
+    failed = sorted(k for k, v in g.items() if v["status"] == "fail")
+    pending = sorted(k for k, v in g.items() if v["status"] == "pending")
+    if failed:
+        names = ", ".join(k + (" (blocking)" if k in BLOCKING else "") for k in failed)
+        result, text = "do not adopt", f"do not adopt: {names} failed"
+    elif pending:
+        result, text = (
+            "pending",
+            "pending: " + ", ".join(pending) + " not yet evaluated",
+        )
+    else:
+        result, text = "adopt", "adopt: every gate passed"
+    return {
+        "result": result,
+        "text": text,
+        "failed": failed,
+        "pending": pending,
+        "blocking": [k for k in failed if k in BLOCKING],
+    }
+
+
+def gates(runs, arm="SS", base="Z0", checklist="K", sets=None, classes=None) -> dict:
+    """Gates D1 to D7 of the arm against the base arm and the checklist arm, pooled over the decision documents."""
+    dec = decision_runs(runs, sets)
+    a, b, k = _arm(dec, arm), _arm(dec, base), _arm(dec, checklist)
+    if not a or not b:
+        raise AnalysisError(
+            f"gates need runs of {arm} and {base} on decision documents"
+        )
+    g = {
+        "D1": gate_d1(dec, arm, base),
+        "D2": gate_d2(a, b),
+        "D3": gate_d3(a, b),
+        "D4": gate_d4(runs, arm, base, sets),
+        "D5": gate_d5(runs, arm, base, sets, classes),
+        "D6": gate_d6(a, b),
+        "D7": gate_d7(a, k),
+    }
+    return {
+        "arm": arm,
+        "base": base,
+        "checklist": checklist,
+        "limits": LIMITS,
+        "bootstrap": {
+            "seed": BOOTSTRAP_SEED,
+            "resamples": BOOTSTRAP_N,
+            "lower_quantile": BOOTSTRAP_Q,
+        },
+        "gates": g,
+        "outcome": outcome(g),
+    }
+
+
+def shares(runs) -> list:
+    """The three gains as three separate numbers, each over the documents that both of its arms ran. Never added."""
+    out = []
+    for label, a, b, formula in SHARES:
+        ra, rb = _common(_arm(runs, a), _arm(runs, b))
+        out.append(
+            {
+                "label": label,
+                "formula": formula,
+                "value": mean_found(ra) - mean_found(rb) if ra else None,
+                "documents": sorted({r.doc for r in ra}),
+            }
+        )
+    return _r(out)
+
+
+# --- stages (REQ-41), the rubber-stamp measure, compliance and DD-7 ----------------------------------------------------
+
+
+def _opt(path):
+    return _json(path) if path.is_file() else None
+
+
+def _span(loc):
+    """A 0-based half-open line range from a 1-based inclusive location."""
+    if not loc or "line_start" not in loc:
+        return None
+    return (loc["line_start"] - 1, loc["line_end"])
+
+
+def covers(text, span, quote, quote_spans) -> bool:
+    """DESIGN 14.1: the flattened quote contains the text or is contained in it (text of 12 or more characters), or the
+    line spans come within 3 lines of each other (the rule of FND.same_defect)."""
+    a, q = fnd.flat(text or ""), fnd.flat(quote)
+    if a and q and (q in a or (len(a) >= 12 and a in q)):
+        return True
+    return span is not None and any(
+        span[0] <= s[1] + 3 and s[0] <= span[1] + 3 for s in quote_spans
+    )
+
+
+def _finding_lines(path):
+    if not path.is_file():
+        return []
+    rows = []
+    for raw in fnd.lenient_lines(path.read_text(encoding="utf-8")):
+        try:
+            row = json.loads(raw)
+        except ValueError:
+            continue
+        if isinstance(row, dict) and row.get("anchor"):
+            rows.append(row)
+    return rows
+
+
+def _members(run):
+    m = _opt(run.path / "merged" / "ledger.json")
+    if m is None:
+        return None
+    return {(x["reviewer_id"], x["fid"]) for row in m["rows"] for x in row["members"]}
+
+
+def stage_rows(run, gt_items, cand_text) -> list:
+    """One row per ground-truth item of the run's document: extraction, selection, act, merge survival, judge credit.
+
+    Sheet arm (SS with a pre-pass): extraction = some candidate covers the item; selection = some selected item covers it;
+    act = a PROBLEM row with its quotes or search result (`supported`) on a covering item; survival = a finding of that row
+    (a linked finding or the promoted line) is a member of a merged row. Other arms have no extractor or sheet: extraction
+    and selection are null, act = a reviewer finding whose anchor covers the item, survival the same through its member.
+    A stage whose input file is missing is null. Judge credit = the judge's `gt_covered_any`.
+    """
+    p = run.path
+    items = _opt(p / "prepass" / "items.json")
+    cands = _opt(p / "prepass" / "candidates.json")
+    members = _members(run)
+    ok_reviewers = [rid for rid, v in run.reviewers.items() if v["status"] == "ok"]
+    sheet = run.arm == "SS" and items is not None and not run.fallback
+    checks = {rid: _opt(p / "check" / f"{rid}.ledger.json") for rid in ok_reviewers}
+    findings = {} if sheet else _reports_findings(run, ok_reviewers)
+    rows = []
+    for g in gt_items:
+        spans = fnd.locate(cand_text, g["plan_quote"])
+        row = {
+            "run": run.name,
+            "arm": run.arm,
+            "doc": run.doc,
+            "item": g["id"],
+            "class": g["class"],
+            "blocking_in_implement": g.get("blocking_in_implement"),
+            "extraction": None,
+            "selection": None,
+            "act": None,
+            "merge_survival": None,
+            "judge_credit": g["id"] in run.found_any,
+        }
+        if sheet:
+            if cands is not None:
+                row["extraction"] = any(
+                    _covers_entry(c, g, spans) for c in cands["candidates"]
+                )
+            ids = {i["item_id"] for i in items["items"] if _covers_entry(i, g, spans)}
+            row["selection"] = bool(ids)
+            row["act"], acting = _sheet_acts(checks, ids)
+        else:
+            acting = [
+                (rid, f["id"])
+                for rid, lines in findings.items()
+                for f in lines
+                if covers(
+                    f["anchor"],
+                    _finding_span(cand_text, f["anchor"]),
+                    g["plan_quote"],
+                    spans,
+                )
+            ]
+            row["act"] = bool(acting)
+        row["merge_survival"] = (
+            None if members is None else any(a in members for a in acting)
+        )
+        rows.append(row)
+    return rows
+
+
+def _covers_entry(entry, g, spans) -> bool:
+    return covers(
+        entry.get("anchor_text"), _span(entry.get("location")), g["plan_quote"], spans
+    )
+
+
+def _reports_findings(run, rids) -> dict:
+    out = {}
+    for rid in rids:
+        for sub in ("normalised", "reviews"):
+            f = run.path / sub / f"{rid}.md"
+            if f.is_file():
+                out[rid] = _finding_lines(f)
+                break
+    return out
+
+
+def _sheet_acts(checks, ids):
+    """(did a reviewer write a supported PROBLEM row on one of the items, the (reviewer id, finding id) pairs of those rows)."""
+    acted, pairs = False, []
+    for rid, led in checks.items():
+        if led is None:
+            continue
+        hit = {
+            r["item"]
+            for r in led["ledger"]["rows"]
+            if r["item"] in ids and r["verdict"] == "PROBLEM" and r.get("supported")
+        }
+        if hit:
+            acted = True
+            pairs += [
+                (rid, f["id"])
+                for f in led["findings"]
+                if f.get("row_item") in hit and f.get("link")
+            ]
+            pairs += [
+                (rid, x["id"]) for x in led.get("promoted", []) if x["item"] in hit
+            ]
+    return acted, pairs
+
+
+def _finding_span(cand_text, anchor):
+    spans = fnd.locate(cand_text, anchor)
+    return (min(s[0] for s in spans), max(s[1] for s in spans)) if spans else None
+
+
+def ok_rate_planted(runs, gt_by_doc, sets) -> dict:
+    """Share of OK rows among the rows on selected items that cover a ground-truth item of a planted document.
+
+    gt_by_doc maps a document to {"text": the candidate text, "items": the ground-truth items}. A row counts once in the
+    total; in a class's own count once for each class of the items it covers.
+    """
+    rows = {}  # (run, reviewer, item id) -> [verdict, classes]
+    for r in runs:
+        if r.arm != "SS" or doc_set(sets, r.doc) != "planted":
+            continue
+        items = _opt(r.path / "prepass" / "items.json")
+        if items is None:
+            continue
+        for g in gt_by_doc[r.doc]["items"]:
+            spans = fnd.locate(gt_by_doc[r.doc]["text"], g["plan_quote"])
+            ids = {i["item_id"] for i in items["items"] if _covers_entry(i, g, spans)}
+            for rid, v in r.reviewers.items():
+                led = (
+                    _opt(r.path / "check" / f"{rid}.ledger.json")
+                    if v["status"] == "ok"
+                    else None
+                )
+                for row in (led or {}).get("ledger", {}).get("rows", []):
+                    if row["item"] in ids:
+                        entry = rows.setdefault(
+                            (r.name, rid, row["item"]), [row["verdict"], set()]
+                        )
+                        entry[1].add(g["class"])
+    total, ok = len(rows), sum(v == "OK" for v, _ in rows.values())
+    per_class = {}
+    for verdict, classes in rows.values():
+        for c in classes:
+            t = per_class.setdefault(c, {"rows": 0, "ok": 0})
+            t["rows"] += 1
+            t["ok"] += verdict == "OK"
+    for t in per_class.values():
+        t["ok_rate"] = t["ok"] / t["rows"]
+    return _r(
+        {
+            "rows": total,
+            "ok": ok,
+            "ok_rate": ok / total if total else None,
+            "per_class": dict(sorted(per_class.items())),
+        }
+    )
+
+
+def ledger_headings(runs) -> dict:
+    """DD-7: for Z0 and K, the accepted reports that hold a `## Ledger` heading (a reviewer reads CB-2 and may write one)."""
+    out = {}
+    for arm in ("Z0", "K"):
+        reports = n = 0
+        for r in _arm(runs, arm):
+            for rid, v in r.reviewers.items():
+                if v["status"] != "ok":
+                    continue
+                for sub in ("reviews", "normalised"):
+                    f = r.path / sub / f"{rid}.md"
+                    if f.is_file():
+                        reports += 1
+                        n += any(
+                            ln.strip() == "## Ledger"
+                            for ln in f.read_text(encoding="utf-8").splitlines()
+                        )
+                        break
+        out[arm] = {"reports": reports, "with_ledger_heading": n}
+    return out
+
+
+COMPLIANCE_LIMIT = 0.10
+
+
+def compliance(runs_dir) -> dict:
+    """REQ-17: `ledger_missing` rate, quote validity, format errors and format-induced demotions of the compliance-spike runs."""
+    root = Path(runs_dir)
+    checked = missing = quote_rows = quote_ok = errors = induced = runs = 0
+    for run in sorted(
+        p for p in root.iterdir() if (p / "check" / "check.json").is_file()
+    ):
+        ck = _json(run / "check" / "check.json")
+        runs += 1
+        missing += len(ck.get("ledger_missing") or [])
+        errors += int(ck.get("format_errors") or 0)
+        induced += int(ck.get("format_induced_demotions") or 0)
+        for f in sorted((run / "check").glob("*.ledger.json")):
+            checked += 1
+            for row in _json(f).get("ledger", {}).get("rows", []):
+                if row.get("quote_plan"):
+                    quote_rows += 1
+                    quote_ok += bool(row.get("quote_plan_ok"))
+    if not runs:
+        raise AnalysisError(f"no run with check/check.json under {root}")
+    rate = missing / checked if checked else None
+    return _r(
+        {
+            "runs": runs,
+            "reviewers_checked": checked,
+            "ledger_missing": missing,
+            "ledger_missing_rate": rate,
+            "limit": COMPLIANCE_LIMIT,
+            "go": rate is not None and rate <= COMPLIANCE_LIMIT + EPS,
+            "quote_rows": quote_rows,
+            "quote_plan_ok_share": quote_ok / quote_rows if quote_rows else None,
+            "format_errors": errors,
+            "format_induced_demotions": induced,
+        }
+    )
+
+
+def prereg(owner=None) -> dict:
+    """The pre-registration record (REQ-41, REQ-44): arms, run counts, the consistency definition, the gates, the floor and
+    the act bands. Without owner values the recommended defaults stand and the record says so."""
+    owner = owner or {}
+    bands = {c: list(v) for c, v in ACT_BANDS.items()}
+    bands.update({c: list(v) for c, v in (owner.get("act_bands") or {}).items()})
+    if sorted(bands) != list(CLASSES):
+        raise AnalysisError(f"act bands must name exactly {', '.join(CLASSES)}")
+    for c, band in bands.items():
+        if len(band) != 2 or not 0 <= band[0] < band[1] <= 1:
+            raise AnalysisError(
+                f"act band of {c} is not [lo, hi] with 0 <= lo < hi <= 1: {band}"
+            )
+    return {
+        "schema": "sweep-prereg/1",
+        "arms": list(ARMS),
+        "stage1_runs": STAGE1_RUNS,
+        "consistency": {
+            "reach_at_least": CONSISTENT_NUM / CONSISTENT_DEN,
+            "of_runs": "3 of 5",
+        },
+        "gates": {"limits": LIMITS, "blocking": list(BLOCKING)},
+        "selection_recall_floor": owner.get(
+            "selection_recall_floor", RECOMMENDED_FLOOR
+        ),
+        "act_bands": bands,
+        "ground_truth_sha256": owner.get("ground_truth_sha256", {}),
+        "owner_confirmed": bool(owner),
+        "source": "owner values"
+        if owner
+        else "recommended defaults of DESIGN 15.1, not confirmed by the owner",
+    }
+
+
+# --- break-even and the report ----------------------------------------------------------------------------------------
+
+
+def breakeven_values(b, values=None) -> dict:
+    be = clock.breakeven(b, values=values)
+    return {"prepass_s": be.prepass_s, "per_item_s": be.per_item_s}
+
+
+def breakeven_lines(runs=None, values=None) -> list:
+    """The break-even values next to the planned and the measured ones (REQ-31)."""
+    v = clock.load_values() if values is None else values
+    at = {b: breakeven_values(b, v) for b in (100, 122)}
+    spike = v.get("spike") or {}
+    c = spike.get("c_luna")
+    lines = [
+        f"Pre-pass seconds: planned {v.get('prepass_s_planning')} s, measured {v.get('prepass_s')} s; "
+        f"break-even {at[100]['prepass_s']:.1f} s at b = 100 and {at[122]['prepass_s']:.1f} s at b = 122.",
+        "Seconds per item (luna): planned "
+        f"{v.get('breakeven', {}).get('c_ref')} s, measured "
+        + (f"{c:.2f} s" if c is not None else "not measured yet (no spike record)")
+        + f"; break-even {at[100]['per_item_s']:.2f} s at b = 100 and {at[122]['per_item_s']:.2f} s at b = 122.",
+    ]
+    if runs:
+        for doc, group in sorted(_by_doc(_arm(runs, "Z0")).items()):
+            slow = [r.slowest for r in group if r.slowest is not None]
+            if slow:
+                planned = v.get("b", {}).get(group[0].panel or "primary", {}).get(doc)
+                shown = "not set" if planned is None else f"{planned} s"
+                lines.append(
+                    f"b of {doc} (Z0 slowest reviewer, median): planned {shown}, measured {median(slow):.1f} s."
+                )
+    return lines
+
+
+def _fmt(x, nd=4):
+    return "n/a" if x is None else f"{x:.{nd}f}"
+
+
+def render_report(runs, g, sh, ledger, values=None, label=None, audit=None) -> str:
+    """results/report.md: three shares as three lines, the one claim sentence, the arms, the gates, break-even, DD-7."""
+    out = [f"# Sweep Sheet analysis{' (' + label + ')' if label else ''}", ""]
+    out += [
+        f"Runs read: {len(runs)}; arms: {', '.join(sorted({r.arm for r in runs}))}.",
+        "",
+    ]
+    out += ["## Gains (three separate numbers, never added)", ""]
+    out += [f"- {s['label']} ({s['formula']}): {_fmt(s['value'])}" for s in sh]
+    out += ["", "## Claim", "", f"The Sweep Sheet {CLAIM}.", "", "## Arms", ""]
+    out += [
+        "| arm | runs | found fraction | found blocking | consistent items | elapsed mean s | elapsed median s | kills | fallbacks |"
+    ]
+    out += ["|---|---|---|---|---|---|---|---|---|"]
+    for arm in sorted({r.arm for r in runs}):
+        m = group_metrics(_arm(runs, arm))
+        out.append(
+            f"| {arm} | {m['runs']} | {_fmt(m['found_fraction']['mean'])} | {_fmt(m['found_blocking_fraction']['mean'])} | "
+            f"{m['consistent_items']} | {_fmt(m['elapsed_s']['mean'], 1)} | {_fmt(m['elapsed_s']['median'], 1)} | {m['kills']} | {m['fallbacks']} |"
+        )
+    out += ["", f"## Gates ({g['arm']} against {g['base']} and {g['checklist']})", ""]
+    for k, v in g["gates"].items():
+        extra = ", ".join(
+            f"{a} {_fmt(b, 3) if isinstance(b, float) else b}"
+            for a, b in v.items()
+            if a
+            in (
+                "difference",
+                "lower_bound",
+                "gain",
+                "items_checked",
+                "arm_consistent_items",
+                "base_consistent_items",
+            )
+        )
+        out.append(f"- {k}: {v['status']}" + (f" ({extra})" if extra else ""))
+    out += ["", f"Outcome: {g['outcome']['text']}.", "", "## Time and break-even", ""]
+    out += [f"- {ln}" for ln in breakeven_lines(runs, values)]
+    out += ["", "## Ledger headings in Z0 and K reports (DD-7)", ""]
+    out += [
+        f"- {arm}: {v['with_ledger_heading']} of {v['reports']} reports"
+        for arm, v in ledger.items()
+    ]
+    if audit is not None:
+        out += [
+            "",
+            "## Judge audit",
+            "",
+            f"- {audit['checked']} judge folders checked, {audit['bad']} bad.",
+        ]
+    return "\n".join(out) + "\n"
+
+
 # --- command line -----------------------------------------------------------------------------------------------------
 
 
@@ -481,6 +1227,111 @@ def cmd_d1(a):
     _write(d1_inputs(load_runs(a.runs, scores=False), a.arm, a.base), a.out)
 
 
+def _runs_dir(a) -> Path:
+    if a.runs:
+        return Path(a.runs)
+    if a.stage:
+        # `all --stage 1` reads SW/runs/stage1; the other commands take the folder name (`audit-judges stage1`)
+        return SW / "runs" / (f"stage{a.stage}" if a.cmd == "all" else a.stage)
+    raise AnalysisError("give a stage name or --runs")
+
+
+def judge_folders(runs_dir) -> list:
+    """The judge folders that the label keys of the run folders name: the first judge and, when there is one, the second."""
+    out = []
+    for f in sorted(Path(runs_dir).iterdir()):
+        key = f / "scoring" / "label-key.json"
+        if key.is_file():
+            k = _json(key)
+            out.append(k["dir"])
+            if k.get("second"):
+                out.append(k["second"]["dir"])
+    return out
+
+
+def _gt_file(gt, doc) -> Path:
+    p = Path(gt)
+    return p / f"{doc}.json" if p.is_dir() else p
+
+
+def cmd_all(a):
+    runs = load_runs(_runs_dir(a))
+    sets, out = load_sets(a.packages), Path(a.out)
+    classes = gt_by_doc = None
+    if a.gt:
+        docs = sorted({r.doc for r in runs})
+        classes = {d: load_classes(a.gt, d) for d in docs}
+        gt_by_doc = {
+            d: {
+                "items": _json(_gt_file(a.gt, d))["items"],
+                "text": (Path(a.cand_root) / d / "candidate.md").read_text(
+                    encoding="utf-8"
+                ),
+            }
+            for d in docs
+        }
+    result = gates(runs, a.arm, a.base, a.checklist, sets, classes)
+    _write(metrics(runs, classes), out / "metrics.json")
+    _write(result, out / "gates.json")
+    _write(result["gates"]["D1"]["inputs"], out / "d1.json")
+    if gt_by_doc:
+        rows = [
+            row
+            for r in runs
+            for row in stage_rows(
+                r, gt_by_doc[r.doc]["items"], gt_by_doc[r.doc]["text"]
+            )
+        ]
+        stages = _writable(out / "stages.jsonl")
+        stages.write_text(
+            "".join(json.dumps(x, sort_keys=True) + "\n" for x in rows),
+            encoding="utf-8",
+        )
+        _write(ok_rate_planted(runs, gt_by_doc, sets), out / "ok_rate_planted.json")
+    audit = judge.audit(judge_folders(_runs_dir(a)))
+    _write(audit, out / "judge_audit.json")
+    report = render_report(
+        runs, result, shares(runs), ledger_headings(runs), label=a.label, audit=audit
+    )
+    _writable(out / "report.md").write_text(report, encoding="utf-8")
+    print(result["outcome"]["text"])
+
+
+def cmd_audit_judges(a):
+    audit = judge.audit(judge_folders(_runs_dir(a)))
+    _write(audit, a.out)
+    print(f"judge audit: {audit['checked']} checked, {audit['bad']} bad")
+    return 1 if audit["bad"] else 0
+
+
+def cmd_sample_second_judge(a):
+    ids = [
+        f.name
+        for f in sorted(_runs_dir(a).iterdir())
+        if (f / "run.json").is_file() and (f / "merged" / "merged-1.md").is_file()
+    ]
+    for i in judge.sample(ids, a.seed):
+        print(i)
+
+
+def cmd_compliance(a):
+    result = compliance(a.runs)
+    _write(result, a.out)
+    print(
+        f"ledger_missing {result['ledger_missing']} of {result['reviewers_checked']}: {'go' if result['go'] else 'no go'}"
+    )
+    return 0 if result["go"] else 1
+
+
+def cmd_prereg(a):
+    owner = _json(Path(a.owner_values)) if a.owner_values else None
+    record = prereg(owner)
+    if a.write:
+        print(_write(record, a.out))
+    else:
+        print(json.dumps(record, indent=1, sort_keys=True))
+
+
 def main(argv=None) -> int:
     ap = argparse.ArgumentParser(prog="analyze.py", description=__doc__.split("\n")[0])
     sub = ap.add_subparsers(dest="cmd", required=True)
@@ -495,13 +1346,63 @@ def main(argv=None) -> int:
     d.add_argument("--base", default="Z0")
     d.add_argument("--out", default=str(SW / "results" / "d1.json"))
     d.set_defaults(fn=cmd_d1)
+    al = sub.add_parser(
+        "all", help="metrics, gates D1-D7, stages.jsonl, shares and report.md"
+    )
+    al.add_argument(
+        "--stage", help="a stage name or number: runs are read from SW/runs/stage<N>"
+    )
+    al.add_argument("--runs", help="the run folders (instead of SW/runs/stage<N>)")
+    al.add_argument("--out", required=True)
+    al.add_argument(
+        "--gt", help="a ground-truth file or folder (stages, per-class reach)"
+    )
+    al.add_argument(
+        "--cand-root",
+        default=str(Path(os.environ.get("SW_SB_ROOT", "/tmp/evalsb-sweep")) / "cand"),
+    )
+    al.add_argument("--packages", help="a packages file (default config/packages.json)")
+    al.add_argument("--arm", default="SS")
+    al.add_argument("--base", default="Z0")
+    al.add_argument("--checklist", default="K")
+    al.add_argument("--label")
+    al.set_defaults(fn=cmd_all)
+    aj = sub.add_parser("audit-judges", help="audit every judge folder of a stage")
+    aj.add_argument("stage", nargs="?")
+    aj.add_argument("--runs")
+    aj.add_argument("--out", default=str(SW / "results" / "judge_audit.json"))
+    aj.set_defaults(fn=cmd_audit_judges)
+    sj = sub.add_parser(
+        "sample-second-judge", help="the seeded 15% sample of runs for a second judge"
+    )
+    sj.add_argument("stage", nargs="?")
+    sj.add_argument("--runs")
+    sj.add_argument("--seed", type=int, default=20261115)
+    sj.set_defaults(fn=cmd_sample_second_judge)
+    co = sub.add_parser(
+        "compliance",
+        help="ledger_missing rate and quote validity of the compliance-spike runs",
+    )
+    co.add_argument("--runs", required=True)
+    co.add_argument("--out", default=str(SW / "results" / "compliance.json"))
+    co.set_defaults(fn=cmd_compliance)
+    pr = sub.add_parser(
+        "prereg",
+        help="the pre-registration record (arms, run counts, gates, floor, act bands)",
+    )
+    pr.add_argument("--write", action="store_true")
+    pr.add_argument(
+        "--owner-values",
+        help="a JSON file: selection_recall_floor, act_bands, ground_truth_sha256",
+    )
+    pr.add_argument("--out", default=str(SW / "config" / "prereg.json"))
+    pr.set_defaults(fn=cmd_prereg)
     args = ap.parse_args(argv)
     try:
-        args.fn(args)
+        return args.fn(args) or 0
     except AnalysisError as e:
         print(f"analyze: {e}", file=sys.stderr)
         return 1
-    return 0
 
 
 if __name__ == "__main__":
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/fixtures/runs/make_runs.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/fixtures/runs/make_runs.py
index 748e402be..b11eb6df8 100644
--- a/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/fixtures/runs/make_runs.py
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/fixtures/runs/make_runs.py
@@ -201,7 +201,9 @@ def write_run(runs_dir, scoring_dir, s, label):
             }
         )
     )
-    (run / "timing.json").write_text(json.dumps({"panel_elapsed_s": s["secs"]}))
+    (run / "timing.json").write_text(
+        json.dumps({"panel_elapsed_s": s["secs"], "slowest_reviewer_s": s["secs"] - 10})
+    )
     probes = 0 if s["fallback"] else s["probes"]
     ledger = 0 if s["fallback"] else s["ledger"]
     folder = "reviews" if s["arm"] == "Z0-raw" else "normalised"
@@ -358,3 +360,187 @@ def build(root, arms=DEFAULT_ARMS, docs=DOCS):
     return SimpleNamespace(
         root=root, runs=runs, scoring=scoring, specs=spec_list, expected=exp
     )
+
+
+# --- stage runs: one sheet run and one plain run on fixtures/plans/p_basic.md, for the stage tests ---------------------
+
+FIXTURES = Path(__file__).resolve().parents[1]
+STAGE_DOC = "synth-a"
+GT_FILE = FIXTURES / "gt" / "synthetic-gt.json"
+PLAN = FIXTURES / "plans" / "p_basic.md"
+UNRELATED = "Run the full test suite and sync `docs/guide.md` with the code."
+
+
+def _line_of(text, quote):
+    """The 1-based line of the first line that holds the quote (a plain search, not the code under test)."""
+    for n, ln in enumerate(text.splitlines(), 1):
+        if quote in ln:
+            return n
+    raise ValueError(quote)
+
+
+def _entry(text, anchor, item_id, cls=None):
+    n = _line_of(text, anchor)
+    return {
+        "item_id": item_id,
+        "class": cls,
+        "anchor_text": anchor,
+        "location": {"line_start": n, "line_end": n},
+    }
+
+
+def _row(item, verdict, supported):
+    return {"item": item, "verdict": verdict, "supported": supported}
+
+
+def _led(rows, findings, promoted=()):
+    return {
+        "ledger": {"rows": rows},
+        "findings": [{"id": i, "row_item": it, "link": "probe"} for i, it in findings],
+        "promoted": list(promoted),
+    }
+
+
+def build_stage_runs(root):
+    """Write root/cand/synth-a/candidate.md, root/runs/stage-s/{ss-stage-r1, z0-stage-r1} and their judge folders.
+
+    The sheet run (SS): selected items S1 (the quote of GT1), S3 (GT5), S4 (GT6), S5 (GT7); a dropped candidate for GT3; one
+    unrelated candidate; nothing for GT4 and GT8. The judge credits GT1, GT4 and GT6. The plain run (Z0): finding F1 of t2b-1
+    anchors the text of GT6, F2 the text of GT1; the merge holds F1 only; the judge credits GT6.
+    """
+    root = Path(root)
+    plan = PLAN.read_text(encoding="utf-8")
+    cand = root / "cand" / STAGE_DOC
+    cand.mkdir(parents=True)
+    (cand / "candidate.md").write_text(plan, encoding="utf-8")
+    quotes = {
+        g["id"]: g["plan_quote"] for g in json.loads(GT_FILE.read_text())["items"]
+    }
+    runs, scoring = root / "runs" / "stage-s", root / "scoring" / "stage-s"
+    for sub in ("ss-stage-r1", "z0-stage-r1"):
+        for d in ("reviews", "normalised", "scoring", "prepass", "check", "merged"):
+            (runs / sub / d).mkdir(parents=True)
+    ss, z0 = runs / "ss-stage-r1", runs / "z0-stage-r1"
+    # the sheet run
+    items = [
+        _entry(plan, quotes["GT1"], "S1", "C1"),
+        _entry(plan, quotes["GT5"], "S3", "C5"),
+        _entry(plan, quotes["GT6"], "S4", "C6"),
+        _entry(plan, quotes["GT7"], "S5", "C7"),
+    ]
+    cands = [
+        *items,
+        {**_entry(plan, quotes["GT3"], None, "C3"), "drop_reason": "pre_rank"},
+        _entry(plan, UNRELATED, None, "C1"),
+    ]
+    (ss / "prepass" / "items.json").write_text(json.dumps({"items": items}))
+    (ss / "prepass" / "candidates.json").write_text(json.dumps({"candidates": cands}))
+    rows_a = [
+        _row("S1", "PROBLEM", True),
+        _row("S3", "PROBLEM", True),
+        _row("S4", "PROBLEM", True),
+        _row("S5", "PROBLEM", False),
+    ]
+    rows_b = [
+        _row("S1", "OK", False),
+        _row("S3", "OK", False),
+        _row("S4", "PROBLEM", True),
+        _row("S5", "OK", False),
+    ]
+    led_a = _led(
+        rows_a,
+        [("F1", "S1"), ("F4", "S4"), ("F5", "S5")],
+        [{"id": "PS3", "item": "S3", "class": "C5", "line": 30}],
+    )
+    led_b = _led(rows_b, [("F1", "S4")])
+    (ss / "check" / "t2b-1.ledger.json").write_text(json.dumps(led_a))
+    (ss / "check" / "t3-1.ledger.json").write_text(json.dumps(led_b))
+    members = [
+        {"reviewer_id": "t2b-1", "fid": "F1"},
+        {"reviewer_id": "t3-1", "fid": "F1"},
+    ]
+    (ss / "merged" / "ledger.json").write_text(
+        json.dumps({"rows": [{"members": members}]})
+    )
+    # the plain run
+    (z0 / "merged" / "ledger.json").write_text(
+        json.dumps({"rows": [{"members": [{"reviewer_id": "t2b-1", "fid": "F1"}]}]})
+    )
+    anchors = {
+        "t2b-1": [
+            ("F1", "only the retention job removes a report file"),
+            ("F2", "returns an empty result for an empty report"),
+        ],
+        "t3-1": [("F1", UNRELATED)],
+    }
+    for rid, found in anchors.items():
+        lines = [
+            json.dumps(
+                {
+                    "id": i,
+                    "severity": "MINOR",
+                    "blocking": False,
+                    "category": "other",
+                    "anchor": a,
+                    "refs": [],
+                    "claim": "A wording point.",
+                }
+            )
+            for i, a in found
+        ]
+        text = (
+            "review: 1 of 3\n\n## Findings block\n\n```findings-v1\n"
+            + "\n".join(lines)
+            + "\n```\n\nverdict: PASS\n"
+        )
+        (z0 / "normalised" / f"{rid}.md").write_text(text)
+    for run, arm, found, label in (
+        (ss, "SS", ("GT1", "GT4", "GT6"), "js0001"),
+        (z0, "Z0", ("GT6",), "js0002"),
+    ):
+        status = {rid: {"model": MODELS[rid], "status": "ok"} for rid in RIDS}
+        (run / "run.json").write_text(
+            json.dumps(
+                {
+                    "arm": arm,
+                    "panel": "primary",
+                    "doc": STAGE_DOC,
+                    "replicate": 1,
+                    "block": 1,
+                    "fallback": False,
+                    "reason": None,
+                    "reviewers": 3,
+                    "reviewer_status": status,
+                }
+            )
+        )
+        (run / "timing.json").write_text(
+            json.dumps({"panel_elapsed_s": 100.0, "slowest_reviewer_s": 90.0})
+        )
+        jd = scoring / label
+        jd.mkdir(parents=True)
+        (jd / "score.json").write_text(
+            json.dumps(
+                {
+                    "label": label,
+                    "gt_total": ITEMS,
+                    "gt_covered_any": list(found),
+                    "gt_covered_blocking": [],
+                    "wrong_blockers": 0,
+                }
+            )
+        )
+        (run / "scoring" / "label-key.json").write_text(
+            json.dumps(
+                {
+                    "label": label,
+                    "dir": str(jd),
+                    "run": run.name,
+                    "doc": STAGE_DOC,
+                    "second": None,
+                }
+            )
+        )
+    return SimpleNamespace(
+        root=root, runs=runs, cand_root=root / "cand", gt=GT_FILE, scoring=scoring
+    )
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_prereg.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_prereg.py
new file mode 100644
index 000000000..182dbeacc
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_prereg.py
@@ -0,0 +1,87 @@
+"""REQ-41, REQ-44: the pre-registration record (arms, run counts, consistency definition, gates, floor, per-class act bands)."""
+
+import json
+
+import pytest
+
+from analysis import analyze
+
+CLASSES = [f"C{n}" for n in range(1, 9)]
+
+
+def test_act_bands_for_all_classes():
+    rec = analyze.prereg()
+    assert sorted(rec["act_bands"]) == CLASSES
+    for c, (lo, hi) in rec["act_bands"].items():
+        assert 0 <= lo < hi <= 1, c
+    # DESIGN 15.1 decision 2, written out here so the code cannot grade itself
+    assert rec["act_bands"]["C3"] == [0.03, 0.15] and rec["act_bands"]["C4"] == [
+        0.50,
+        0.75,
+    ]
+    assert rec["owner_confirmed"] is False and "not confirmed" in rec["source"]
+    assert rec["selection_recall_floor"] == 0.45
+
+
+def test_owner_values_replace_defaults_and_are_validated(tmp_path):
+    rec = analyze.prereg(
+        {
+            "selection_recall_floor": 0.5,
+            "act_bands": {"C3": [0.02, 0.2]},
+            "ground_truth_sha256": {"HO-1": "ab" * 32},
+        }
+    )
+    assert rec["act_bands"]["C3"] == [0.02, 0.2] and rec["act_bands"]["C1"] == [
+        0.10,
+        0.40,
+    ]
+    assert rec["selection_recall_floor"] == 0.5 and rec["ground_truth_sha256"] == {
+        "HO-1": "ab" * 32
+    }
+    assert rec["owner_confirmed"] is True and rec["source"] == "owner values"
+    for bad in ([0.3, 0.3], [0.4, 0.2], [0.1, 1.2], [-0.1, 0.5], [0.1]):
+        with pytest.raises(analyze.AnalysisError, match="C3"):
+            analyze.prereg({"act_bands": {"C3": bad}})
+    with pytest.raises(analyze.AnalysisError, match="exactly"):
+        analyze.prereg({"act_bands": {"C9": [0.1, 0.2]}})
+
+
+def test_record_names_arms_run_counts_consistency_and_gates():
+    rec = analyze.prereg()
+    assert rec["arms"] == ["Z0-raw", "Z0", "K", "SS"]
+    assert rec["stage1_runs"] == {"panel_runs": 75, "arms_z0_k_ss": 60, "z0_raw": 15}
+    assert rec["consistency"] == {"reach_at_least": 0.6, "of_runs": "3 of 5"}
+    lim = rec["gates"]["limits"]
+    assert (lim["d1_median_ratio"], lim["d2_effect"], lim["d3_consistent_items"]) == (
+        1.35,
+        0.12,
+        3,
+    )
+    assert (
+        lim["d4_wrong_blockers"],
+        lim["d4_twin_blocking"],
+        lim["d6_within"],
+        lim["d7_gain"],
+    ) == (1.0, 0.7, 0.1, 0.04)
+    assert rec["gates"]["blocking"] == ["D6"]
+
+
+def test_command_writes_only_under_sw_or_tmp(tmp_path, capsys):
+    owner = tmp_path / "owner.json"
+    owner.write_text(json.dumps({"selection_recall_floor": 0.4}))
+    out = tmp_path / "config" / "prereg.json"
+    rc = analyze.main(
+        ["prereg", "--write", "--owner-values", str(owner), "--out", str(out)]
+    )
+    assert rc == 0 and json.loads(out.read_text())["selection_recall_floor"] == 0.4
+    assert out.read_text().endswith("\n")
+    # without --write the record is printed and nothing is written
+    capsys.readouterr()
+    assert analyze.main(["prereg", "--out", str(tmp_path / "never.json")]) == 0
+    printed = json.loads(capsys.readouterr().out)
+    assert printed["schema"] == "sweep-prereg/1" and printed["owner_confirmed"] is False
+    assert not (tmp_path / "never.json").exists()
+    assert (
+        analyze.main(["prereg", "--write", "--out", "/var/tmp/sw-prereg-refused.json"])
+        == 1
+    )
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_report.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_report.py
new file mode 100644
index 000000000..7856c4535
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_report.py
@@ -0,0 +1,423 @@
+"""REQ-31, REQ-40, REQ-42, REQ-45, REQ-17, DD-7: the gates, the three shares, the claim, the break-even values, the report.
+Run folders are synthetic (fixtures/runs/make_runs.py); the numbers marked as hand-worked come from its tables:
+mean found fraction Z0-raw 16/80, Z0 25/80, K 32/80, SS 43/80 (8 items, 10 runs per arm)."""
+
+import json
+import re
+
+import pytest
+
+from analysis import analyze
+from fixtures.runs import make_runs
+from scaffold import clock, judge
+
+
+@pytest.fixture
+def world(tmp_path):
+    return make_runs.build(tmp_path, arms=make_runs.ALL_ARMS)
+
+
+def build_custom(root, tweak):
+    """Runs of Z0, K and SS written from the tables after `tweak(spec)` changed each spec (see make_runs.specs)."""
+    runs, scoring = root / "runs" / "stage1", root / "scoring" / "stage1"
+    runs.mkdir(parents=True)
+    specs = make_runs.specs()
+    z0_secs = {(s["doc"], s["rep"]): s["secs"] for s in specs if s["arm"] == "Z0"}
+    for n, s in enumerate(specs, 1):
+        tweak(s, z0_secs)
+        make_runs.write_run(runs, scoring, s, f"j{n:06x}")
+    return runs
+
+
+def fast_ss(s, z0_secs):
+    """SS as fast as Z0 on the same document and replicate, so that gate D1 is not what fails."""
+    if s["arm"] == "SS":
+        s["secs"] = z0_secs[(s["doc"], s["rep"])]
+
+
+def fast_ss_keeping_gt3(s, z0_secs):
+    fast_ss(s, z0_secs)
+    if (s["arm"], s["doc"], s["rep"]) == ("SS", "synth-a", 4):
+        s["found"] = s["found"] | {"GT3"}  # SS now reaches GT3 in 4 of 5 runs, like Z0
+
+
+def gates_of(root, tweak):
+    runs = analyze.load_runs(build_custom(root, tweak))
+    return runs, analyze.gates(runs)
+
+
+def test_three_shares_separate(world):
+    runs = analyze.load_runs(world.runs)
+    sh = analyze.shares(runs)
+    assert [(s["label"], s["formula"]) for s in sh] == [
+        ("H share", "Z0 - Z0raw"),
+        ("Prompting share", "K - Z0"),
+        ("Redesign share", "SS - Z0"),
+    ]
+    # 25/80 - 16/80, 32/80 - 25/80, 43/80 - 25/80
+    assert [s["value"] for s in sh] == [0.1125, 0.0875, 0.225]
+    text = analyze.render_report(
+        runs, analyze.gates(runs), sh, analyze.ledger_headings(runs)
+    )
+    lines = [ln for ln in text.splitlines() if ln.startswith("- ") and "share (" in ln]
+    assert lines == [
+        "- H share (Z0 - Z0raw): 0.1125",
+        "- Prompting share (K - Z0): 0.0875",
+        "- Redesign share (SS - Z0): 0.2250",
+    ]
+
+
+def test_no_summed_headline(world):
+    runs = analyze.load_runs(world.runs)
+    text = analyze.render_report(
+        runs, analyze.gates(runs), analyze.shares(runs), analyze.ledger_headings(runs)
+    )
+    names = ("H share", "Prompting share", "Redesign share")
+    for line in text.splitlines():
+        assert sum(n.lower() in line.lower() for n in names) <= 1, line
+        if "share (" in line:
+            assert "+" not in line and "total" not in line.lower(), line
+    # the shares are never added in the numbers either
+    assert not re.search(r"0\.4250|0\.3250|0\.5250", text)
+    # a share is computed over the documents that both of its arms ran
+    only_a = [r for r in runs if not (r.arm == "Z0-raw" and r.doc == "synth-b")]
+    h = analyze.shares(only_a)[0]
+    assert h["documents"] == ["synth-a"] and h["value"] == pytest.approx(0.35 - 9 / 40)
+
+
+def test_breakeven_values():
+    assert analyze.breakeven_values(100) == {"prepass_s": 14.0, "per_item_s": 2.75}
+    at = analyze.breakeven_values(122)
+    assert at["prepass_s"] == pytest.approx(21.7, abs=0.05)
+    assert at["per_item_s"] == pytest.approx(3.71, abs=0.01)
+
+
+def test_report_shows_planned_and_measured(world):
+    runs = analyze.load_runs(world.runs)
+    values = {**clock.load_values(), "spike": {"runs": 5, "c_luna": 2.1}}
+    lines = analyze.breakeven_lines(runs, values)
+    assert (
+        "Pre-pass seconds: planned 8 s, measured 0.59 s; break-even 14.0 s at b = 100 and 21.7 s at b = 122."
+        in lines
+    )
+    assert (
+        "Seconds per item (luna): planned 2 s, measured 2.10 s; break-even 2.75 s at b = 100 and 3.71 s at b = 122."
+        in lines
+    )
+    # b of a document: the median of the Z0 runs' slowest reviewer (secs - 10 in the fixture: 90 100 85 110 95)
+    assert (
+        "b of synth-a (Z0 slowest reviewer, median): planned not set, measured 95.0 s."
+        in lines
+    )
+    text = analyze.render_report(
+        runs,
+        analyze.gates(runs),
+        analyze.shares(runs),
+        analyze.ledger_headings(runs),
+        values=values,
+    )
+    section = text.split("## Time and break-even")[1].split("##")[0]
+    for ln in section.splitlines():
+        if ln.startswith("- "):
+            assert "planned" in ln and "measured" in ln, ln
+    # without a spike record the measured cost per item is said to be missing, not invented
+    none = analyze.breakeven_lines(
+        None, {k: v for k, v in values.items() if k != "spike"}
+    )
+    assert any("measured not measured yet (no spike record)" in ln for ln in none)
+
+
+def test_claim_template_text(world):
+    runs = analyze.load_runs(world.runs)
+    text = analyze.render_report(
+        runs, analyze.gates(runs), analyze.shares(runs), analyze.ledger_headings(runs)
+    )
+    req45 = (
+        "raises the per-run found fraction; consistency is expected only for I4 and I7 (classes C4 and C8), "
+        "and only for Redesign 1 at the high end of its range"
+    )
+    assert analyze.CLAIM == req45
+    assert text.count(f"The Sweep Sheet {req45}.") == 1
+    # no other sentence says "consistent" for a class
+    for line in text.splitlines():
+        if "consistent" in line.lower():
+            assert not re.search(r"\b[CI][1-8]\b", line), line
+    assert len(re.findall(r"\bI4\b", text)) == 1
+
+
+def test_d6_failure_blocks_adoption(tmp_path):
+    runs, g = gates_of(tmp_path, fast_ss)
+    st = {k: v["status"] for k, v in g["gates"].items()}
+    # D2 (0.225 over Z0) and D3 (9 consistent items against 5) pass; D6 fails because SS reaches GT3 of synth-a in 3 of 5 runs
+    # where Z0 reaches it in 4 of 5, a drop of 0.2 against the 0.10 allowed
+    assert (st["D1"], st["D2"], st["D3"], st["D6"], st["D7"]) == (
+        "pass",
+        "pass",
+        "pass",
+        "fail",
+        "pass",
+    )
+    assert (st["D4"], st["D5"]) == (
+        "pending",
+        "pending",
+    )  # no clean twins, no planted set
+    assert g["gates"]["D2"]["difference"] == pytest.approx(0.225)
+    assert g["gates"]["D2"]["lower_bound"] > 0.04
+    assert (
+        g["gates"]["D3"]["arm_consistent_items"],
+        g["gates"]["D3"]["base_consistent_items"],
+    ) == (
+        9,
+        5,
+    )  # SS: 5 in synth-a (GT1 2 3 5 6) and 4 in synth-b (GT4 5 6 8); Z0: 3 and 2
+    assert g["gates"]["D6"]["failing_items"] == [
+        {"doc": "synth-a", "item": "GT3", "base_reach": 0.8, "arm_reach": 0.6}
+    ]
+    assert g["gates"]["D6"]["items_checked"] == 5
+    out = g["outcome"]
+    assert (
+        out["result"] == "do not adopt"
+        and out["blocking"] == ["D6"]
+        and out["failed"] == ["D6"]
+    )
+    assert out["text"] == "do not adopt: D6 (blocking) failed"
+    text = analyze.render_report(
+        runs, g, analyze.shares(runs), analyze.ledger_headings(runs)
+    )
+    assert "Outcome: do not adopt: D6 (blocking) failed." in text
+
+
+def test_gates_with_d6_met_are_pending_not_adopted(tmp_path):
+    # the control: SS also reaches GT3 in 4 of 5 runs, so D6 passes; D4 and D5 still lack data, so the result is not "adopt"
+    _, g = gates_of(tmp_path, fast_ss_keeping_gt3)
+    assert (
+        g["gates"]["D6"]["status"] == "pass" and g["gates"]["D6"]["failing_items"] == []
+    )
+    assert g["outcome"]["result"] == "pending" and g["outcome"]["blocking"] == []
+    assert g["outcome"]["pending"] == ["D4", "D5"]
+
+
+def test_d1_fails_when_the_arm_is_slow(world):
+    runs = analyze.load_runs(world.runs)
+    g = analyze.gates(runs)
+    d1 = g["gates"]["D1"]
+    # SS median 142 against Z0 median 85 on synth-b: 1.67 > 1.35
+    assert d1["status"] == "fail"
+    assert d1["inputs"]["primary"]["docs"]["synth-b"]["ratio"] == pytest.approx(
+        142 / 85, abs=1e-5
+    )
+    assert "D1" in g["outcome"]["failed"]
+
+
+def test_bootstrap_is_seeded_and_resamples_documents(world):
+    runs = analyze.load_runs(world.runs)
+    ss, z0 = analyze._arm(runs, "SS"), analyze._arm(runs, "Z0")
+    a = analyze.bootstrap_lower(ss, z0, seed=1, n=300)
+    assert a == analyze.bootstrap_lower(ss, z0, seed=1, n=300)
+    assert a != analyze.bootstrap_lower(ss, z0, seed=2, n=300)
+    assert a < analyze.mean_found(ss) - analyze.mean_found(z0)
+    with pytest.raises(analyze.AnalysisError, match="no document"):
+        analyze.bootstrap_lower(ss, [r for r in z0 if r.doc == "nope"])
+
+
+def test_gates_need_both_arms(world):
+    runs = [r for r in analyze.load_runs(world.runs) if r.arm != "Z0"]
+    with pytest.raises(analyze.AnalysisError, match="SS and Z0"):
+        analyze.gates(runs)
+
+
+def test_twin_and_planted_gates_use_their_own_sets(tmp_path):
+    runs = analyze.load_runs(build_custom(tmp_path, fast_ss))
+    sets = {"synth-a": "holdout", "synth-b": "twin"}
+    twin_runs = [r for r in runs if r.doc == "synth-b"]
+    assert {r.doc for r in analyze.decision_runs(runs, sets)} == {"synth-a"}
+    for r in (
+        twin_runs
+    ):  # a clean twin: every blocking row of a merged ledger is a wrong blocker
+        rows = [{"blocking": r.arm == "SS", "members": []}] * 2
+        (r.path / "merged").mkdir()
+        (r.path / "merged" / "ledger.json").write_text(json.dumps({"rows": rows}))
+    d4 = analyze.gates(runs, sets=sets)["gates"]["D4"]
+    # 2 blocking rows per SS run against none for Z0: 2.0 > 0.7
+    assert d4["twin_blocking_difference"] == 2.0 and d4["status"] == "fail"
+    classes = {
+        d: {f"GT{n}": f"C{n}" for n in range(1, 9)} for d in ("synth-a", "synth-b")
+    }
+    d5 = analyze.gates(
+        runs, sets={"synth-a": "holdout", "synth-b": "planted"}, classes=classes
+    )["gates"]["D5"]
+    # planted detection of SS on synth-b, class C4 = GT4: found in 5 of 5; C5: 5 of 5; C6: 4 of 5; C8 (GT8): 5 of 5; C2: 0 of 5
+    assert d5["planted_detection"] == {
+        "C2": 0.0,
+        "C4": 1.0,
+        "C5": 1.0,
+        "C6": 0.8,
+        "C8": 1.0,
+    }
+    assert d5["planted_classes_passing"] == ["C4", "C5", "C6", "C8"]
+    assert (
+        d5["status"] == "pending"
+    )  # the documentation arm and the spec set have no runs yet
+
+
+def make_compliance(root, missing_per_run):
+    for k, missing in enumerate(missing_per_run, 1):
+        run = root / f"c{k}"
+        (run / "check").mkdir(parents=True)
+        (run / "check" / "check.json").write_text(
+            json.dumps(
+                {
+                    "ledger_missing": missing,
+                    "format_errors": 1 if k == 1 else 0,
+                    "format_induced_demotions": 0,
+                }
+            )
+        )
+        for i, rid in enumerate(("t2b-1", "t3-1", "t4-1")):
+            ok = not (
+                k == 1 and i == 0
+            )  # one reviewer wrote a quote that is not in the candidate
+            rows = [
+                {
+                    "item": "S1",
+                    "verdict": "PROBLEM",
+                    "quote_plan": "a quote",
+                    "quote_plan_ok": ok,
+                },
+                {
+                    "item": "S2",
+                    "verdict": "OK",
+                    "quote_plan": "",
+                    "quote_plan_ok": False,
+                },
+            ]
+            (run / "check" / f"{rid}.ledger.json").write_text(
+                json.dumps({"ledger": {"rows": rows}})
+            )
+    return root
+
+
+def test_compliance_go_no_go(tmp_path):
+    ok = make_compliance(tmp_path / "ok", [["t4-1"], [], [], [], []])
+    r = analyze.compliance(ok)
+    # 5 runs of 3 reviewers; 1 ledger missing in 15 is 0.0667, within the 10% limit; 14 of 15 quotes are in the candidate
+    assert (r["runs"], r["reviewers_checked"], r["ledger_missing"]) == (5, 15, 1)
+    assert (
+        r["ledger_missing_rate"] == pytest.approx(1 / 15, abs=1e-6) and r["go"] is True
+    )
+    assert (r["quote_rows"], r["quote_plan_ok_share"], r["format_errors"]) == (
+        15,
+        pytest.approx(14 / 15, abs=1e-6),
+        1,
+    )
+    bad = make_compliance(tmp_path / "bad", [["t4-1"], ["t3-1"], [], [], []])
+    r = analyze.compliance(bad)  # 2 of 15 is 0.1333
+    assert (
+        r["ledger_missing_rate"] == pytest.approx(2 / 15, abs=1e-6) and r["go"] is False
+    )
+    out = tmp_path / "out" / "compliance.json"
+    assert analyze.main(["compliance", "--runs", str(ok), "--out", str(out)]) == 0
+    assert analyze.main(["compliance", "--runs", str(bad), "--out", str(out)]) == 1
+    assert json.loads(out.read_text())["go"] is False
+    with pytest.raises(analyze.AnalysisError, match="no run with check"):
+        analyze.compliance(tmp_path / "out")
+
+
+def test_ledger_headings_counted_in_z0_and_k(world):
+    runs = analyze.load_runs(world.runs)
+    assert analyze.ledger_headings(runs) == {
+        "Z0": {"reports": 30, "with_ledger_heading": 0},
+        "K": {
+            "reports": 29,
+            "with_ledger_heading": 0,
+        },  # one K reviewer was invalid: no report
+    }
+    f = world.runs / "z0-synth-a-r1" / "normalised" / "t2b-1.md"
+    f.write_text(f.read_text() + "\n## Ledger\n\n| lid |\n")
+    k = world.runs / "k-synth-a-r2" / "normalised" / "t3-1.md"
+    k.write_text("## Ledger\n" + k.read_text())
+    got = analyze.ledger_headings(analyze.load_runs(world.runs))
+    assert (got["Z0"]["with_ledger_heading"], got["K"]["with_ledger_heading"]) == (1, 1)
+
+
+def test_all_writes_every_output(tmp_path):
+    w = make_runs.build_stage_runs(tmp_path)
+    packages = tmp_path / "packages.json"
+    packages.write_text(json.dumps({"packages": {}}))
+    out = tmp_path / "out" / "stage-s"
+    argv = ["all", "--runs", str(w.runs), "--out", str(out), "--gt", str(w.gt)]
+    argv += [
+        "--cand-root",
+        str(w.cand_root),
+        "--packages",
+        str(packages),
+        "--label",
+        "fixture",
+    ]
+    assert analyze.main(argv) == 0
+    names = {p.name for p in out.iterdir()}
+    assert names >= {
+        "metrics.json",
+        "gates.json",
+        "d1.json",
+        "stages.jsonl",
+        "ok_rate_planted.json",
+        "judge_audit.json",
+        "report.md",
+    }
+    rows = [json.loads(x) for x in (out / "stages.jsonl").read_text().splitlines()]
+    assert len(rows) == 16 and {r["run"] for r in rows} == {
+        "ss-stage-r1",
+        "z0-stage-r1",
+    }
+    report = (out / "report.md").read_text()
+    assert (
+        report.startswith("# Sweep Sheet analysis (fixture)")
+        and "## Judge audit" in report
+    )
+    # D7 has no checklist runs: pending, never passed by default
+    assert (
+        json.loads((out / "gates.json").read_text())["gates"]["D7"]["status"]
+        == "pending"
+    )
+
+
+def test_audit_judges_and_sample_second_judge_commands(world, tmp_path, capsys):
+    runs = sorted(p.name for p in world.runs.iterdir())
+    for name in runs:  # the sample is drawn over the runs that have a merged report
+        (world.runs / name / "merged").mkdir()
+        (world.runs / name / "merged" / "merged-1.md").write_text("x")
+    capsys.readouterr()
+    assert (
+        analyze.main(["sample-second-judge", "--runs", str(world.runs), "--seed", "7"])
+        == 0
+    )
+    assert capsys.readouterr().out.split() == judge.sample(runs, 7)
+    out = tmp_path / "judge_audit.json"
+    # the synthetic judge folders hold only a score file: every one is flagged (no judge output, no merged report)
+    assert (
+        analyze.main(["audit-judges", "--runs", str(world.runs), "--out", str(out)])
+        == 1
+    )
+    got = json.loads(out.read_text())
+    assert (got["checked"], got["bad"]) == (len(runs), len(runs))
+    assert "judge_missing" in got["items"][0]["problems"]
+
+
+def test_stage_names_resolve_as_documented():
+    """TESTING section 5: `all --stage 1` reads SW/runs/stage1; `audit-judges stage1` names the folder."""
+    ns = analyze.argparse.Namespace
+    assert (
+        analyze._runs_dir(ns(cmd="all", runs=None, stage="1"))
+        == analyze.SW / "runs" / "stage1"
+    )
+    assert (
+        analyze._runs_dir(ns(cmd="audit-judges", runs=None, stage="stage1"))
+        == analyze.SW / "runs" / "stage1"
+    )
+    assert (
+        analyze._runs_dir(ns(cmd="all", runs="/tmp/x", stage="1")).as_posix()
+        == "/tmp/x"
+    )
+    with pytest.raises(analyze.AnalysisError, match="stage name"):
+        analyze._runs_dir(ns(cmd="all", runs=None, stage=None))
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_stages.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_stages.py
new file mode 100644
index 000000000..9d167d312
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_stages.py
@@ -0,0 +1,137 @@
+"""REQ-41: reach logged per stage (extraction, selection, act, merge survival, judge credit), the rubber-stamp measure.
+The scenario is built by fixtures/runs/make_runs.py (build_stage_runs) on fixtures/plans/p_basic.md and the synthetic ground
+truth; the expected values below were worked out by hand from the line numbers of the plan (a quote on line L covers another
+quote when the text matches or the two lines are within 4 lines: 28 GT8, 30 GT2, 34 GT1, 40 GT5, 45 GT4, 54 GT3, 59 GT6, 66 GT7)."""
+
+import json
+
+import pytest
+
+from analysis import analyze
+from fixtures.runs import make_runs
+
+STAGES = ("extraction", "selection", "act", "merge_survival", "judge_credit")
+GT = json.loads(make_runs.GT_FILE.read_text())["items"]
+FLAG = {"T": True, "F": False, "N": None}
+
+
+def flags(word):
+    """'TTFFN' -> (True, True, False, False, None): the five stages in the order of STAGES."""
+    return tuple(FLAG[c] for c in word)
+
+
+@pytest.fixture
+def world(tmp_path):
+    w = make_runs.build_stage_runs(tmp_path)
+    w.loaded = {r.name: r for r in analyze.load_runs(w.runs)}
+    w.cand = (w.cand_root / "synth-a" / "candidate.md").read_text()
+    return w
+
+
+def rows_of(loaded, cand, name):
+    return {
+        r["item"]: tuple(r[s] for s in STAGES)
+        for r in analyze.stage_rows(loaded[name], GT, cand)
+    }
+
+
+def test_stage_rows_schema(world):
+    rows = analyze.stage_rows(world.loaded["ss-stage-r1"], GT, world.cand)
+    assert [r["item"] for r in rows] == [f"GT{n}" for n in range(1, 9)]
+    for r, g in zip(rows, GT):
+        assert set(r) == {
+            "run",
+            "arm",
+            "doc",
+            "item",
+            "class",
+            "blocking_in_implement",
+            *STAGES,
+        }
+        assert r["run"] == "ss-stage-r1" and r["arm"] == "SS" and r["doc"] == "synth-a"
+        assert (r["class"], r["blocking_in_implement"]) == (
+            g["class"],
+            g["blocking_in_implement"],
+        )
+        assert all(
+            isinstance(r[s], bool) for s in STAGES
+        )  # a sheet run has every stage
+    plain = analyze.stage_rows(world.loaded["z0-stage-r1"], GT, world.cand)
+    # no extractor and no sheet in an arm without a pre-pass: those two stages are null, not false
+    assert all(r["extraction"] is None and r["selection"] is None for r in plain)
+    assert all(isinstance(r[s], bool) for r in plain for s in STAGES[2:])
+
+
+def test_stage_values_on_fixture(world):
+    # stages in order: extraction, selection, act, merge survival, judge credit
+    sheet = {
+        "GT1": "TTTTT",  # the item of its quote, a supported PROBLEM row, its finding is merged, credited
+        "GT2": "TTTTF",  # reached only through the 3-line rule (GT1's item is 4 lines away)
+        "GT3": "TFFFF",  # a candidate that the top-K cut dropped
+        "GT4": "FFFFT",  # no candidate at all; the judge still credits a free-review finding
+        "GT5": "TTTFF",  # the act is a promoted line that the merge did not keep
+        "GT6": "TTTTT",  # the second reviewer's finding is a member of the merged row
+        "GT7": "TTFFF",  # selected, but the PROBLEM row has no support: not an act
+        "GT8": "FFFFF",  # 6 lines from the nearest item
+    }
+    got = rows_of(world.loaded, world.cand, "ss-stage-r1")
+    assert got == {k: flags(v) for k, v in sheet.items()}
+    plain = {
+        "GT1": "NNTFF",  # F2 anchors its text, F2 is not in the merge
+        "GT2": "NNTFF",  # F2 again, through the 3-line rule
+        "GT3": "NNFFF",
+        "GT4": "NNFFF",
+        "GT5": "NNFFF",
+        "GT6": "NNTTT",  # F1 anchors its text and is in the merge
+        "GT7": "NNFFF",
+        "GT8": "NNFFF",
+    }
+    got = rows_of(world.loaded, world.cand, "z0-stage-r1")
+    assert got == {k: flags(v) for k, v in plain.items()}
+
+
+def test_missing_inputs_give_null_not_false(world):
+    (world.runs / "ss-stage-r1" / "merged" / "ledger.json").unlink()
+    loaded = {r.name: r for r in analyze.load_runs(world.runs)}
+    got = rows_of(loaded, world.cand, "ss-stage-r1")
+    # no merged ledger: survival is unknown, and the stages before it are unaffected
+    assert all(v[3] is None for v in got.values())
+    assert got["GT1"][:3] == (True, True, True)
+
+
+def test_covers_rule_literals():
+    q = "Every module under `src/exporter/` returns an empty result for an empty report."
+    spans = [(33, 34)]
+    assert analyze.covers(q, None, q, spans)
+    assert analyze.covers("returns an empty result for an empty report", None, q, spans)
+    # text of under 12 characters is not a match by containment
+    assert not analyze.covers("empty", None, q, spans)
+    # the quote is on line 34 (span 33 to 34, half-open). Line 30 (span 29 to 30) is 4 lines away: the rule of
+    # FND.same_defect (a start at most 3 beyond the other's end) counts it. Line 29 is 5 lines away and does not count.
+    assert analyze.covers("unrelated words here", (29, 30), q, spans)
+    assert not analyze.covers("unrelated words here", (28, 29), q, spans)
+    assert analyze.covers(
+        "unrelated words here", (37, 38), q, spans
+    )  # line 38, 4 lines after
+    assert not analyze.covers("unrelated words here", (38, 39), q, spans)
+    assert not analyze.covers("unrelated words here", None, q, spans)
+
+
+def test_ok_rate_planted(world):
+    runs = list(world.loaded.values())
+    gt = {"synth-a": {"text": world.cand, "items": GT}}
+    got = analyze.ok_rate_planted(runs, gt, {"synth-a": "planted"})
+    # rows on selected items: t2b-1 PROBLEM on S1 S3 S4 S5 and t3-1 OK on S1 S3 S5, PROBLEM on S4 -> 8 rows, 3 OK
+    assert (got["rows"], got["ok"], got["ok_rate"]) == (8, 3, 0.375)
+    # a row counts for each class of the items it covers: S1 covers GT1 (C1) and GT2 (C2)
+    per = {c: (v["rows"], v["ok"], v["ok_rate"]) for c, v in got["per_class"].items()}
+    assert per == {
+        "C1": (2, 1, 0.5),
+        "C2": (2, 1, 0.5),
+        "C5": (2, 1, 0.5),
+        "C6": (2, 0, 0.0),
+        "C7": (2, 1, 0.5),
+    }
+    # a document that is not in the planted set is not measured
+    none = analyze.ok_rate_planted(runs, gt, {})
+    assert (none["rows"], none["ok_rate"]) == (0, None)
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_verifier_off_path.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_verifier_off_path.py
new file mode 100644
index 000000000..d215f75dc
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_verifier_off_path.py
@@ -0,0 +1,81 @@
+"""REQ-46: the optional verifier never sits on the critical path, cannot add claims, and its time is excluded.
+The verifier itself is not built; these tests guard the seam."""
+
+import json
+import re
+import subprocess
+
+import pytest
+from helpers import SW
+
+from analysis import analyze
+from fixtures.runs import make_runs
+from scaffold import clock
+
+RUN_PANEL = SW / "bin" / "run-panel.sh"
+
+
+def test_no_verifier_step_in_clock():
+    # the clock times three stages; a verifier stage is refused, and timing.json has no verifier field
+    assert "verifier" not in " ".join(clock.PanelClock.STAGES).lower()
+    pc = clock.PanelClock("SS", now=iter([0.0, 1.0, 2.0, 3.0, 4.0]).__next__)
+    pc.start()
+    with pytest.raises(clock.ClockError, match="unknown stage verifier"):
+        pc.stage_start("verifier")
+    assert "verifier" not in clock.PanelClock.__doc__.lower()
+    # the launcher: every mention is a comment, the default, or the refusal; there is no step that runs one
+    for n, line in enumerate(RUN_PANEL.read_text().splitlines(), 1):
+        if re.search(r"verifier", line, re.I):
+            assert re.match(
+                r"\s*#|VERIFIER=\$\{VERIFIER:-0\}$|\[ \"\$VERIFIER\" = 0 \]", line
+            ), (n, line)
+
+
+def test_verifier_default_off(tmp_roots):
+    assert "VERIFIER=${VERIFIER:-0}" in RUN_PANEL.read_text().splitlines()
+    # any other value is refused before anything runs
+    r = subprocess.run(
+        [
+            "bash",
+            str(RUN_PANEL),
+            "--arm",
+            "Z0",
+            "--panel",
+            "primary",
+            "--doc",
+            "d",
+            "--run",
+            str(tmp_roots.root / "r"),
+        ],
+        capture_output=True,
+        text=True,
+        env=tmp_roots.with_env(VERIFIER="1"),
+    )
+    assert r.returncode == 2 and "E_VERIFIER" in r.stderr
+    assert not (tmp_roots.root / "r").exists()
+
+
+def test_verifier_time_excluded(tmp_path):
+    # the clock: time that passes after the last reviewer (a verifier, H2, the merge, the judge) is not panel time
+    ticks = iter(
+        [100.0, 100.0, 130.0, 130.0, 150.0]
+    )  # t0, start A, end A, start B, end B
+    pc = clock.PanelClock("Z0", now=ticks.__next__)
+    pc.start()
+    pc.reviewer_start("a")
+    pc.reviewer_end("a")
+    pc.reviewer_start("b")
+    pc.reviewer_end("b")
+    t = pc.timing()
+    assert t["panel_elapsed_s"] == 50.0 and "verifier_s" not in t
+    assert clock.panel_elapsed_s("Z0", 100.0, {"a": 130.0, "b": 150.0}) == 50.0
+    # the analysis: a `verifier_s` in timing.json is not in the elapsed time, and it adds no finding
+    w = make_runs.build_stage_runs(tmp_path)
+    before = {r.name: r for r in analyze.load_runs(w.runs)}["z0-stage-r1"]
+    timing = w.runs / "z0-stage-r1" / "timing.json"
+    data = json.loads(timing.read_text())
+    timing.write_text(json.dumps({**data, "verifier_s": 30.0}))
+    after = {r.name: r for r in analyze.load_runs(w.runs)}["z0-stage-r1"]
+    assert before.elapsed == after.elapsed == 100.0
+    assert analyze.nonprobe_findings(before) == analyze.nonprobe_findings(after)
+    assert analyze.elapsed_s(after) == 100.0

Codegraph context: index_state: fresh; checked_at: 2026-11-14T20:52:06Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel; projectPath: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel. Call codegraph only when index_state: fresh, never to widen scope. Q2b: the files this task changed are new files that the graph does not index (shell, new Python, Markdown) plus small additions to existing test files; the dependents of the changed symbols were searched with Grep and no dependent outside the diff was found.
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
