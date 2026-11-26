f76bd67f8f5e0113575b2bf856dad506a59ee6d2
Review one task for spec compliance.

Task brief: ## Task 15: Write the analysis script, the synthetic ground truth and the run-folder fixtures

Depends on: Task 14

Follow `RL/IMPLEMENTATION.md` step 6 (analysis part) and `RL/DESIGN.md` sections 9.3, 12.2 to 12.5 and REQ-17, REQ-29, REQ-31, REQ-39 to REQ-45. Create `RL/fixtures/gt/synthetic-gt.json` (F-GT, invented items for the fixture plan) and `RL/fixtures/runs/make_runs.py` (F-RUNS-RL: synthetic run folders for arms Z0-raw, Z0, K, RL, 2 documents, 5 replicates, known found sets, timings, flags, ledgers and scores, and `expected.json` written by hand-written arithmetic, not by calling `analyze.py`). Create `RL/analysis/analyze.py` with subcommands `all`, `audit-judges`, `compliance`, `prereg`, `sample-second-judge`, `ablate-report`: every metric of `RL/DESIGN.md` 12.5 defined only in this file (`found_fraction` and the other metric names), Wilson intervals, a bootstrap that resamples documents then runs, gates D1 to D7 (D1 on per-document medians, same block only, mean and median both reported; D6 blocking), the three labelled shares `Z0 - Z0raw`, `K - Z0`, `RL - Z0` never summed, per-stage rows `stages.jsonl` (extraction null, selection, act, merge survival, judge credit, class, reviewer id), kills and retries per arm with re-asks apart, non-probe findings per run excluding `probe` lines and `src: ledger` lines, the REQ-45 claim sentence, and `analysis/g0.py` is written in Task 16. The analysis reads real ground truth only when a person runs it on real runs after the freeze; no test or build step does.

Write `RL/tests/test_analyze.py`, `RL/tests/test_report.py` (the REQ-31 `test_report_shows_planned_and_measured`, REQ-40 `test_three_shares_separate` and `test_no_summed_headline`, REQ-45 `test_claim_template_text`), `RL/tests/test_stages.py` (REQ-41), `RL/tests/test_prereg.py::test_act_bands_for_all_classes`, and the analysis-side tests of REQ-29, REQ-30, REQ-39, REQ-42 and REQ-43 listed in `RL/TESTING.md` sections 3.4 and 3.7.

Acceptance criteria (ids added by the orchestrator, in source order):
T15.AC1: `$T $RL/tests/test_analyze.py $RL/tests/test_report.py $RL/tests/test_stages.py $RL/tests/test_prereg.py -q` exits 0.
T15.AC2: Every metric on the F-RUNS-RL fixture equals `expected.json`, and an AST search of `RL` finds `found_fraction` defined only in `analysis/analyze.py`.
T15.AC3: A fixture where D2 and D3 pass and D6 fails yields "do not adopt"; the report has no line that adds two share names.
T15.AC4: `analyze.py compliance` on the fixture reports `ledger_missing`, `recipe_missing`, quote validity, format errors and `none_found` per class equal to the hand-computed values (REQ-17 check itself).

Global constraints: ## Constraints

Path names used by every task (all repo-relative to the checkout root `REPO`, which is `git rev-parse --show-toplevel`):

- `RL` is `.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger`. It holds `DESIGN.md`, `TESTING.md`, `IMPLEMENTATION.md` and `SHARED-MANIFEST-DESIGN-TIME.tsv`, which are the specification and are never edited by the build.
- `SW` is `.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet`, the sibling build (Redesign 1). It is read only: no task writes, edits, moves or deletes anything under it, and no task runs a script or a test from inside it.
- `MR` is `.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md` (sections 3.0, 3.2, 5 and 6 are the requirements source; the design documents already map them). `EVAL` is `.dev/eval-workspaces/tasklist-review-panel/20261111-a1` (read only).
- Design ids: `K1` to `K9` (constraints), `DR-1` to `DR-16` (decisions) and `REQ-nn` (requirements) are those of `RL/DESIGN.md` sections 1.2 and 1.3 and of `RL/TESTING.md` section 3.

Scope rules that hold for every task:

- Create or edit files only under `RL`, plus scratch under `/tmp` (sandboxes under `/tmp/evalsb-recipe`, scratch under `/tmp/rl-*`). Nothing under `src/`, `tests/`, `.claude/`, any existing folder under `.dev/tasks/`, `SW`, `EVAL`, `.dev/eval-workspaces/tasklist-review-panel/20261113-collab` or any other folder is changed.
- No task runs `git commit` or `git push`, and no task runs `git add` for a path under `RL`. The freeze tag (K5) is only printed, never created.
- No task opens, reads, greps the content of or copies any `ground-truth*.json`, score file or judge output of a study package, and no recipe, card, brief, fixture, regex or example uses a study answer. Fixtures are invented. Tests that need ground truth use the synthetic `RL/fixtures/gt/` files only. The tests marked `freeze` (they read the real ground truth or need a second author's records) are never run by this build.
- Python runs only through uv. No `python -m`, no bare `pip`. No code folder is named `lib/` (K7).
- No reviewer or judge session is started and no network call is made. Tests use the fake `claude` at `RL/tests/fakes/claude`. If a task ever needed a model it would use `claude-sonnet-5-5` or `claude-haiku-5-5`; Opus is only the blind judge script's model; never Qwen or glm.
- Files under `RL/scaffold/`, `RL/cards/`, `RL/briefs/`, `RL/bin/common.sh`, `RL/bin/build-sandbox.sh` and the copied tests are copies of sibling files and are never edited after the copy (DESIGN 3.1). A copied test that fails is reported, not edited.
- Shell variables used in task commands:

```
REPO=$(git rev-parse --show-toplevel)
RL=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger
SW=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet
MR=$REPO/.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md
T="uv run --frozen --project $REPO pytest -p no:cacheprovider"
PYRUN="uv run --frozen --project $REPO python"
export PYTHONDONTWRITEBYTECODE=1 NOFALLBACK=1 SUPERCLAUDE_CODEGRAPH_AUTOINIT=0
```


Start sha: f76bd67f8f5e0113575b2bf856dad506a59ee6d2
Diff against the start snapshot: (the diff is 4414 lines; it is saved as a file: read /tmp/rl-impl/T15/diff.patch with the Read tool, in parts. The files it touches exist on disk under the repo; read them as needed.)

Codegraph context: index_state: fresh; checked_at: 2026-11-14T23:20:38Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel; projectPath: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
call codegraph only when index_state: fresh, never to widen scope
Q2b: this task changes no existing symbol; the files it creates are new, so there are no dependents outside the diff.

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/analysis/analyze.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/analysis/analyze.py
index be3e44f3d..1a396e23e 100644
--- a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/analysis/analyze.py
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/analysis/analyze.py
@@ -123,6 +123,8 @@ METRIC_FUNCTIONS = (
     "wilson",
     "percentile",
     "bootstrap_diff",
+    "ledger_counts",
+    "reask_yield",
 )
 
 
@@ -214,6 +216,68 @@ def class_reach(trials):
     return out
 
 
+def ledger_counts(ledgers):
+    """The ledger metrics of DESIGN 12.5 over the ledger dicts of one arm (`check/<rid>.ledger.json`; an arm with no
+    check has none and gets zeros). Keys:
+      over_budget      {recipe, lens}: rows flagged over budget, by reason.
+      recipe_missing   {class: n}: reviewer-runs whose lens recipe for the class has no row.
+      unknown_item     n: rows whose id is outside the grammar or the reviewer's lens.
+      none_found_share {class: {none_found, ran, share}}: `ran` is the reviewer-runs that wrote at least one accepted
+                       (not unknown_item) row of the class; `none_found` is those that wrote a NONE FOUND row for it, so
+                       the share is at most 1. A missing ledger has no rows and is in neither count.
+      rows_per_lens    {rid: mean rows}: a lens is named by its reviewer id; ledgers that are missing are left out."""
+    over = {"recipe": 0, "lens": 0}
+    missing, ran, none_found, rows_by = {}, {}, {}, {}
+    unknown = 0
+    for x in ledgers:
+        unknown += len(x["unknown_item"])
+        if not x["ledger_missing"]:
+            rows_by.setdefault(x["rid"], []).append(len(x["rows"]))
+        for c in x["recipe_missing"]:
+            missing[c] = missing.get(c, 0) + 1
+        seen, found = set(), set()
+        for r in x["rows"]:
+            if r["over_budget"]:
+                over[r["over_budget"]] += 1
+            c = telemetry.class_of(r["item"])
+            if c and not r["unknown_item"]:
+                seen.add(c)
+                if r["none_found"]:
+                    found.add(c)
+        for c in seen:
+            ran[c] = ran.get(c, 0) + 1
+        for c in found:
+            none_found[c] = none_found.get(c, 0) + 1
+    return {
+        "over_budget": over,
+        "recipe_missing": dict(sorted(missing.items())),
+        "unknown_item": unknown,
+        "none_found_share": {
+            c: {
+                "none_found": none_found.get(c, 0),
+                "ran": n,
+                "share": none_found.get(c, 0) / n,
+            }
+            for c, n in sorted(ran.items())
+        },
+        "rows_per_lens": {k: statistics.fmean(v) for k, v in sorted(rows_by.items())},
+    }
+
+
+def reask_yield(fractions, reasked):
+    """Found-fraction yield of the runs with a re-asked reviewer and of the runs without one (DESIGN 8 row 23).
+    `fractions` and `reasked` are parallel lists, one entry per run. The judge credits a run, not a reviewer, so this
+    compares two groups of runs; a group with no run has mean None."""
+    out = {}
+    for name, flag in (("with", True), ("without", False)):
+        xs = [f for f, a in zip(fractions, reasked, strict=True) if a == flag]
+        out[name] = {
+            "runs": len(xs),
+            "found_fraction_mean": statistics.fmean(xs) if xs else None,
+        }
+    return out
+
+
 def bootstrap_diff(cand, ctrl, seed, n=BOOT_N):
     """Sorted differences of pooled means; `cand` and `ctrl` map a document to its per-run values.
 
@@ -303,6 +367,15 @@ def reviewers(run):
     }
 
 
+def run_ledgers(run):
+    """The ledger dicts of a run's reviewers (RL runs whose check ran; none for any other run)."""
+    leds = (
+        read_json(run["dir"] / "check" / f"{rid}.ledger.json")
+        for rid in run["meta"].get("reviewers", {})
+    )
+    return [x for x in leds if x is not None]
+
+
 def report_text(run, rid):
     """The report as it reaches the merge: normalised, else the checked report, else the raw final message."""
     d = run["dir"]
@@ -372,6 +445,7 @@ def arm_metrics(runs, gt, scores):
         ),
         0,
     )
+    ledgers, reasked, lost, asked, accepted = [], [], {}, 0, 0
     for doc, rs in sorted(by_doc.items()):
         items = gt[doc]
         ids = {i["id"] for i in items}
@@ -381,6 +455,16 @@ def arm_metrics(runs, gt, scores):
             found = set(s["gt_covered_any"]) & ids
             sets.append(found)
             fr.append(found_fraction(found, len(items)))
+            ledgers += run_ledgers(r)
+            reasked.append(bool(r["meta"].get("reask")))
+            chk = read_json(r["dir"] / "check" / "check.json") or {}
+            for rec in (chk.get("reask") or {}).values():
+                was = rec.get("asked", rec.get("allowed", False))
+                asked += bool(was)
+                accepted += bool(was and rec.get("accepted"))
+            for classes in (chk.get("classes_lost") or {}).values():
+                for c in classes:
+                    lost[c] = lost.get(c, 0) + 1
             fb.append(found_fraction(set(s["gt_covered_blocking"]) & ids, len(items)))
             wb.append(s)
             npf.append(run_nonprobe(r))
@@ -433,6 +517,11 @@ def arm_metrics(runs, gt, scores):
         "elapsed_p90": elapsed_stats(el)["p90"],
         "tokens_per_run": statistics.fmean(tk),
         **cnt,
+        **ledger_counts(ledgers),
+        "classes_lost": dict(sorted(lost.items())),
+        "reask_asked": asked,
+        "reask_accepted": accepted,
+        "reask_yield": reask_yield(fr, reasked),
         "item_reach": reach,
         "class_reach": class_reach(trials),
     }
@@ -1078,6 +1167,7 @@ def build_report(m):
             out.append(
                 f"| {arm} | {c} | {r['hits']} | {r['trials']} | {fmt(r['rate'])} | {fmt(r['lo'])} | {fmt(r['hi'])} |"
             )
+    out += report_ledger_sections(m)
     out += ["", "## Gates", ""]
     for cand, g in m["gates"].items():
         for name in ("D1", "D2", "D3", "D4", "D5", "D6", "D7"):
@@ -1123,6 +1213,58 @@ def build_report(m):
     return "\n".join(out) + "\n"
 
 
+def report_ledger_sections(m):
+    """The per-arm ledger tables of DESIGN 12.5: checks and re-asks, none_found share, rows per lens, reach per class
+    per reviewer id."""
+    out = [
+        "",
+        "## Ledger checks and re-asks per arm (DESIGN 12.5)",
+        "",
+        "| arm | over_budget recipe | over_budget lens | recipe_missing | unknown_item | classes_lost | re-asks asked | re-asks accepted | yield with re-ask (runs) | yield without re-ask (runs) |",
+        "|---|---|---|---|---|---|---|---|---|---|",
+    ]
+    for arm, a in m["arms"].items():
+        p = a["pooled"]
+        y = p["reask_yield"]
+        out.append(
+            f"| {arm} | {p['over_budget']['recipe']} | {p['over_budget']['lens']} | {p['recipe_missing']} | "
+            f"{p['unknown_item']} | {p['classes_lost']} | {p['reask_asked']} | {p['reask_accepted']} | "
+            f"{fmt(y['with']['found_fraction_mean'])} ({y['with']['runs']}) | "
+            f"{fmt(y['without']['found_fraction_mean'])} ({y['without']['runs']}) |"
+        )
+    out += [
+        "",
+        "none_found share: reviewer-runs with a NONE FOUND row of the class over reviewer-runs with a row of the class.",
+        "",
+        "| arm | class | none_found | ran | share |",
+        "|---|---|---|---|---|",
+    ]
+    for arm, a in m["arms"].items():
+        for c, v in a["pooled"]["none_found_share"].items():
+            out.append(
+                f"| {arm} | {c} | {v['none_found']} | {v['ran']} | {fmt(v['share'])} |"
+            )
+    out += ["", "## Rows per lens (mean rows of a ledger, by reviewer id)", ""]
+    out += ["| arm | reviewer id | mean rows |", "|---|---|---|"]
+    for arm, a in m["arms"].items():
+        for rid, v in a["pooled"]["rows_per_lens"].items():
+            out.append(f"| {arm} | {rid} | {fmt(v)} |")
+    out += [
+        "",
+        "## Reach per class per reviewer id",
+        "",
+        "| arm | class | reviewer id | rows | ledger rows | selection | act | merge survival |",
+        "|---|---|---|---|---|---|---|---|",
+    ]
+    for arm, classes in m["stages"].items():
+        for c, v in sorted(classes.items()):
+            for rid, b in sorted(v["by_reviewer"].items()):
+                out.append(
+                    f"| {arm} | {c} | {rid} | {b['rows']} | {b['ledger_rows']} | {b['selection']} | {b['act']} | {b['merge_survival']} |"
+                )
+    return out
+
+
 def gate_detail(name, x):
     if name == "D1":
         parts = [
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/fixtures/runs/expected.json b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/fixtures/runs/expected.json
index 0d9cd22fb..5e84816e0 100644
--- a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/fixtures/runs/expected.json
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/fixtures/runs/expected.json
@@ -292,6 +292,110 @@
   ],
   "D7_gain": 0.2
  },
+ "ledger_metrics": {
+  "K": {
+   "reask_yield": {
+    "with": [
+     0,
+     null
+    ],
+    "without": [
+     10,
+     0.4333333333333334
+    ]
+   }
+  },
+  "RL": {
+   "classes_lost": {
+    "C1": 1,
+    "C3": 1
+   },
+   "none_found_share": {
+    "C1": [
+     0,
+     7
+    ],
+    "C2": [
+     0,
+     14
+    ],
+    "C3": [
+     6,
+     6
+    ],
+    "C4": [
+     0,
+     15
+    ],
+    "C5": [
+     0,
+     8
+    ],
+    "C6": [
+     0,
+     8
+    ],
+    "C7": [
+     0,
+     6
+    ],
+    "C8": [
+     0,
+     8
+    ]
+   },
+   "over_budget": {
+    "lens": 1,
+    "recipe": 0
+   },
+   "reask_accepted": 1,
+   "reask_asked": 1,
+   "reask_yield": {
+    "with": [
+     1,
+     0.6666666666666666
+    ],
+    "without": [
+     9,
+     0.6296296296296295
+    ]
+   },
+   "recipe_missing": {
+    "C3": 1,
+    "C7": 1
+   },
+   "rows_per_lens": {
+    "t2b-1": 5.5,
+    "t3-1": 4.0,
+    "t4-1": 3.2857142857142856
+   },
+   "unknown_item": 0
+  },
+  "Z0": {
+   "reask_yield": {
+    "with": [
+     0,
+     null
+    ],
+    "without": [
+     10,
+     0.3416666666666667
+    ]
+   }
+  },
+  "Z0-raw": {
+   "reask_yield": {
+    "with": [
+     0,
+     null
+    ],
+    "without": [
+     10,
+     0.225
+    ]
+   }
+  }
+ },
  "shares": {
   "H share": 0.11666666666666667,
   "prompting share": 0.09166666666666673,
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/fixtures/runs/make_runs.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/fixtures/runs/make_runs.py
index 7e7cf51fd..6cfd42dfb 100644
--- a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/fixtures/runs/make_runs.py
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/fixtures/runs/make_runs.py
@@ -962,6 +962,57 @@ EXPECTED = {
         "reask": {"asked": 1, "accepted": 1},
         "rows_per_reviewer": {"t2b-1": 44 / 8, "t3-1": 28 / 7, "t4-1": 23 / 7},
     },
+    # DESIGN 12.5 per arm. Only the 8 checked RL runs (doc-a r1, r3, r4; doc-b r1 to r5) have ledgers: 3 reviewers each, the
+    # killed t4-1 of doc-a r3 has none, so 23 ledger files; the luna ledger of doc-b r4 is missing, so 22 ledgers with rows.
+    # Z0-raw, Z0 and K write no ledger and no check.json: every count is zero, every share dict is empty.
+    "ledger_metrics": {
+        "RL": {
+            # the one row over the lens cap of 6 (C8.2 of t2b-1, doc-a r4); no row is over a recipe budget
+            "over_budget": {"recipe": 0, "lens": 1},
+            "recipe_missing": {
+                "C3": 1,
+                "C7": 1,
+            },  # t4-1 doc-b r3 has no C3 row, t3-1 doc-a r4 has no C7 row
+            "unknown_item": 0,
+            # classes_lost of check.json: only the killed t4-1 (doc-a r3) lists any, its lens C1, C2, C3 less C2 which t3-1
+            # also holds: the fixture writes {"t4-1": ["C1", "C3"]}
+            "classes_lost": {"C1": 1, "C3": 1},
+            "reask_asked": 1,  # the accepted ember re-ask of doc-b r2
+            "reask_accepted": 1,
+            # ran = ledgers (with rows) that hold a row of the class. t2b-1 (C4 C5 C6 C8): 8 ledgers; t3-1 (C2 C4 C7): 7
+            # ledgers, 6 for C7 (doc-a r4 omits it); t4-1 (C1 C2 C3): 7 ledgers, 6 for C3 (doc-b r3 omits it).
+            # C1 7; C2 7 + 7 = 14; C3 6; C4 8 + 7 = 15; C5 8; C6 8; C7 6; C8 8.
+            # none_found = ledgers with a NONE FOUND row of the class: the C3 row of the 6 t4-1 ledgers that have one.
+            "none_found_share": {
+                "C1": [0, 7],
+                "C2": [0, 14],
+                "C3": [6, 6],
+                "C4": [0, 15],
+                "C5": [0, 8],
+                "C6": [0, 8],
+                "C7": [0, 6],
+                "C8": [0, 8],
+            },
+            # mean rows of the ledgers that are not missing: t2b-1 44 rows over 8, t3-1 28 over 7, t4-1 23 over 7 (see
+            # "compliance"; 4 recipe rows + 12 plan rows, 20 + 8 (7 plan rows and the bad-quote row), 20 + 3)
+            "rows_per_lens": {"t2b-1": 44 / 8, "t3-1": 28 / 7, "t4-1": 23 / 7},
+            # found fraction of the re-asked run (doc-b r2: B1 B3 of 3 items) and of the other 9 RL runs:
+            # all 10 runs sum to 12/4 + 10/3 = 19/3, without r2 that is 19/3 - 2/3 = 17/3 over 9 runs
+            "reask_yield": {
+                "with": [1, 2 / 3],
+                "without": [9, (19 / 3 - 2 / 3) / 9],
+            },
+        },
+        "Z0-raw": {
+            "reask_yield": {"with": [0, None], "without": [10, (5 / 4 + 3 / 3) / 10]}
+        },
+        "Z0": {
+            "reask_yield": {"with": [0, None], "without": [10, (7 / 4 + 5 / 3) / 10]}
+        },
+        "K": {
+            "reask_yield": {"with": [0, None], "without": [10, (8 / 4 + 7 / 3) / 10]}
+        },
+    },
 }
 
 
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_analyze.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_analyze.py
index 2ace99f44..8eaede49e 100644
--- a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_analyze.py
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_analyze.py
@@ -462,6 +462,144 @@ def test_compliance_fails_above_ten_percent(fx, tmp_path):
     )
 
 
+# ---------------------------------------------------------------- DESIGN 12.5: the ledger metrics per arm
+
+
+def test_ledger_metrics_per_arm_match_expected(fx):
+    for arm, want in mr.EXPECTED["ledger_metrics"].items():
+        got = fx.metrics["arms"][arm]["pooled"]
+        y = got["reask_yield"]
+        for name, (runs, mean) in want["reask_yield"].items():
+            assert y[name]["runs"] == runs, (arm, name)
+            if mean is None:
+                assert y[name]["found_fraction_mean"] is None
+            else:
+                near(y[name]["found_fraction_mean"], mean)
+        # an arm that writes no ledger and no check.json counts zero everywhere
+        zero = {
+            "over_budget": {"recipe": 0, "lens": 0},
+            "recipe_missing": {},
+            "unknown_item": 0,
+            "classes_lost": {},
+            "reask_asked": 0,
+            "reask_accepted": 0,
+            "none_found_share": {},
+            "rows_per_lens": {},
+        }
+        for key, value in {
+            **zero,
+            **{k: v for k, v in want.items() if k != "reask_yield"},
+        }.items():
+            if key == "none_found_share":
+                assert {
+                    c: [v["none_found"], v["ran"]] for c, v in got[key].items()
+                } == value, arm
+                for c, v in got[key].items():
+                    near(v["share"], value[c][0] / value[c][1])
+            elif key == "rows_per_lens":
+                assert set(got[key]) == set(value), arm
+                for rid, mean in value.items():
+                    near(got[key][rid], mean)
+            else:
+                assert got[key] == value, (arm, key)
+
+
+def test_ledger_metrics_per_document_and_in_the_report(fx):
+    doc_b = fx.metrics["arms"]["RL"]["documents"]["doc-b"]  # r2 is the re-asked run
+    assert doc_b["reask_yield"]["with"] == {
+        "runs": 1,
+        "found_fraction_mean": pytest.approx(2 / 3),
+    }
+    near(doc_b["reask_yield"]["without"]["found_fraction_mean"], (10 / 3 - 2 / 3) / 4)
+    assert fx.metrics["arms"]["RL"]["documents"]["doc-a"]["classes_lost"] == {
+        "C1": 1,
+        "C3": 1,
+    }
+    assert doc_b["recipe_missing"] == {"C3": 1} and doc_b["over_budget"] == {
+        "recipe": 0,
+        "lens": 0,
+    }
+    text = az.build_report(fx.metrics)
+    for word in (
+        "## Ledger checks and re-asks per arm",
+        "| RL | 0 | 1 | {'C3': 1, 'C7': 1} | 0 | {'C1': 1, 'C3': 1} | 1 | 1 | 0.667 (1) | 0.630 (9) |",
+        "| RL | C3 | 6 | 6 | 1.000 |",
+        "| RL | C2 | 0 | 14 | 0.000 |",
+        "| RL | t3-1 | 4.000 |",
+        "| RL | t2b-1 | 5.500 |",
+        "## Reach per class per reviewer id",
+        "| RL | C4 | t2b-1 | 10 | 8 | 7 | 7 | 9 |",
+    ):
+        assert word in text, word
+
+
+def led(rid, rows, **kw):
+    return {
+        "rid": rid,
+        "ledger_missing": False,
+        "recipe_missing": [],
+        "unknown_item": [],
+        "rows": rows,
+        **kw,
+    }
+
+
+def lrow(item, over=None, none_found=False, unknown=False):
+    return {
+        "item": item,
+        "over_budget": over,
+        "none_found": none_found,
+        "unknown_item": unknown,
+    }
+
+
+def test_ledger_counts_on_synthetic_ledgers():
+    """The fixture has no unknown_item and no recipe-budget overrun; these ledgers do. Counted by hand:
+    unknown_item 2 (the two entries of the second ledger); over_budget recipe 1 (C4.3), lens 1 (C5.2); recipe_missing
+    C6 once; C5 ran in 2 ledgers (the unknown C5.9 row of the third does not count), NONE FOUND in 1; C4 ran in 2
+    ledgers, NONE FOUND in 1 although it has two such rows there (a reviewer-run is counted once); the missing
+    ledger counts for nothing; rows per lens: t2b-1 (4 + 3 rows) / 2 = 3.5, t3-1 1 row."""
+    a = led(
+        "t2b-1",
+        [
+            lrow("C4.1", none_found=True),
+            lrow("C4.2", none_found=True),
+            lrow("C4.3", over="recipe"),
+            lrow("C5.1", none_found=True),
+        ],
+        recipe_missing=["C6"],
+    )
+    b = led(
+        "t2b-1",
+        [lrow("C4.1"), lrow("C5.1"), lrow("C5.2", over="lens")],
+        unknown_item=["X1", "C9.1"],
+    )
+    c = led("t3-1", [lrow("C5.9", unknown=True)])
+    gone = led("t3-1", [], ledger_missing=True)
+    got = az.ledger_counts([a, b, c, gone])
+    assert got["unknown_item"] == 2
+    assert got["over_budget"] == {"recipe": 1, "lens": 1}
+    assert got["recipe_missing"] == {"C6": 1}
+    assert got["none_found_share"] == {
+        "C4": {"none_found": 1, "ran": 2, "share": 0.5},
+        "C5": {"none_found": 1, "ran": 2, "share": 0.5},
+    }
+    assert got["rows_per_lens"] == {"t2b-1": 3.5, "t3-1": 1.0}
+    assert az.ledger_counts([])["none_found_share"] == {}
+
+
+def test_reask_yield_groups_runs_and_leaves_an_empty_group_none():
+    y = az.reask_yield([0.5, 1.0, 0.0], [True, False, False])
+    assert y == {
+        "with": {"runs": 1, "found_fraction_mean": 0.5},
+        "without": {"runs": 2, "found_fraction_mean": 0.5},
+    }
+    assert az.reask_yield([0.5], [False])["with"] == {
+        "runs": 0,
+        "found_fraction_mean": None,
+    }
+
+
 # ---------------------------------------------------------------- REQ-43, analysis side
 
 

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B4 ac=scope at=.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/analysis/analyze.py:356 anchor="every metric of `RL/DESIGN.md` 12.5 defined only in this file" chk=n,n,n,y family=metrics-12.5-partial fix=add to arm_metrics (and so to metrics.json and report.md) the per-arm over_budget, recipe_missing, unknown_item and classes_lost counts, the none_found share per class, and re-ask yield with and without re-asked reviewers, each with a hand value in make_runs.py EXPECTED covers="every metric of `RL/DESIGN.md` 12.5" first=A1 origin=new: DESIGN 12.5 lists these metrics; unknown_item, classes_lost and re-ask yield are never computed (the only unknown_item hits are analyze.py:641 and :763), and over_budget, recipe_missing and none_found exist only as totals in compliance (:861-927), not per arm or as a share; none of T15.AC1-AC4 requires them, so the ACs stay met.

Saved-probe re-check hit locations (may be empty): 11:        REQ-17 over RL run folders: ledger_missing rate, recipe_missing, quote validity, format errors, none_found per class.
127:    "reask_yield",
222:      over_budget      {recipe, lens}: rows flagged over budget, by reason.
223:      recipe_missing   {class: n}: reviewer-runs whose lens recipe for the class has no row.
224:      unknown_item     n: rows whose id is outside the grammar or the reviewer's lens.
225:      none_found_share {class: {none_found, ran, share}}: `ran` is the reviewer-runs that wrote at least one accepted
226:                       (not unknown_item) row of the class; `none_found` is those that wrote a NONE FOUND row for it, so
230:    missing, ran, none_found, rows_by = {}, {}, {}, {}
233:        unknown += len(x["unknown_item"])
236:        for c in x["recipe_missing"]:
240:            if r["over_budget"]:
241:                over[r["over_budget"]] += 1
243:            if c and not r["unknown_item"]:
245:                if r["none_found"]:
250:            none_found[c] = none_found.get(c, 0) + 1
252:        "over_budget": over,
253:        "recipe_missing": dict(sorted(missing.items())),
254:        "unknown_item": unknown,
255:        "none_found_share": {
257:                "none_found": none_found.get(c, 0),
259:                "share": none_found.get(c, 0) / n,
267:def reask_yield(fractions, reasked):
268:    """Found-fraction yield of the runs with a re-asked reviewer and of the runs without one (DESIGN 8 row 23).
465:            for classes in (chk.get("classes_lost") or {}).values():
521:        "classes_lost": dict(sorted(lost.items())),
524:        "reask_yield": reask_yield(fr, reasked),
730:        if not r["unknown_item"]
731:        and not r["over_budget"]
845:    """The rows of a ledger without the class `drop`, over_budget recomputed for the lens cap in the order written
852:        if r["over_budget"] != "recipe" and not r["unknown_item"]:
854:            r["over_budget"] = "lens" if within > cap else None
951:    """The REQ-17 numbers over RL run folders that have a check: ledger_missing before any re-ask, recipe_missing,
952:    quote validity, format errors and none_found per class."""
978:    recipe_missing, none_found = {}, {}
983:        for c in x["recipe_missing"]:
984:            recipe_missing[c] = recipe_missing.get(c, 0) + 1
986:            if r["none_found"]:
988:                none_found[c] = none_found.get(c, 0) + 1
989:            if r["over_budget"]:
990:                over[r["over_budget"]] += 1
1001:        "recipe_missing": dict(sorted(recipe_missing.items())),
1010:        "none_found": dict(sorted(none_found.items())),
1011:        "over_budget": over,
1217:    """The per-arm ledger tables of DESIGN 12.5: checks and re-asks, none_found share, rows per lens, reach per class
1223:        "| arm | over_budget recipe | over_budget lens | recipe_missing | unknown_item | classes_lost | re-asks asked | re-asks accepte
1228:        y = p["reask_yield"]
1230:            f"| {arm} | {p['over_budget']['recipe']} | {p['over_budget']['lens']} | {p['recipe_missing']} | "
1231:            f"{p['unknown_item']} | {p['classes_lost']} | {p['reask_asked']} | {p['reask_accepted']} | "
1237:        "none_found share: reviewer-runs with a NONE FOUND row of the class over reviewer-runs with a row of the class.",
1239:        "| arm | class | none_found | ran | share |",
1243:        for c, v in a["pooled"]["none_found_share"].items():
1245:                f"| {arm} | {c} | {v['none_found']} | {v['ran']} | {fmt(v['share'])} |"
1427:    print(f"recipe_missing per class: {res['recipe_missing']}")
1433:    print(f"none_found per class: {res['none_found']}")
1435:        f"over_budget: {res['over_budget']}; re-ask: {res['reask']}; rows per reviewer: {res['rows_per_reviewer']}"


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
