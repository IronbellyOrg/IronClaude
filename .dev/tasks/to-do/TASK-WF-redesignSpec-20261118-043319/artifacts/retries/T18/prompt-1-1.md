b0c108f0b013dfe9fb8c39a63c81db0363faee02
Review one task for spec compliance.

Task brief: ## Task 18: Frame-aware tests, Q7 re-pin, height and pty checks, golden, close the Phase 4 gate

Depends on: Task 17

Spec steps 3.5 to 3.10. Add `unframe(line)` and `title_of(lines)` to `tests/observe/conftest.py`. Convert the whole-line checks to frame-aware ones as step 3.6 lists (`DESK_TITLE in title_of(lines)` at `tests/observe/test_render.py` lines 900, 924, 997; `unframe` at 897, 964 and the desk slice 951-966, 938, 948, 479, 646, 547; `tests/observe/test_question_cap.py` lines 77 and 121; `tests/observe/test_commands.py` lines 672-675 and 690, per decision D-9 default yes), re-pin `test_decision_2` (line 660) from the measured value and record in the commit notes that "the questions win on a short terminal" still holds, and keep `test_r3_the_desk_gives_way...` (line 990) passing. Re-pin the Q7 tests through `unframe` with the single-column inner widths (154, 110, 74). Extend `tests/observe/test_height_budget.py` to framed screens at heights 8 (diagnostic), 12, 24, 40, 44 and, in `tests/observe/test_live_screen_pty.py`, assert at heights 24 and 40 that the last stream row holds the `shown x/y` footer. Regenerate `tests/observe/golden_questions_linkoff.json`. Run the gate into `./artifacts/gates/p3/` with RB-02 (questions, desk), RB-07 and earlier rows in scope.

Acceptance criteria:
- `uv run pytest tests/observe/ -v` is green; `golden_release1_surface.json` and `golden_release1_records.json` are untouched.
- Gate record `.dev/issues/409/visual-parity/scores/p3/scores.json` shows all in-scope High and Medium rows PASS with the NO_COLOR and ASCII passes present (ASCII pass: `+ - |` borders, no `?`), or `stop.md` exists.
Global constraints: - Numbering: plan Phase N is spec Phase N-1 (plan Phase 1 is the spec's Phase 0, plan Phase 8 is the spec's Phase 7). Task text names the plan phase unless it says "spec Phase".
- Shorthand used in every task: OBS is `src/superclaude/cli/observe/`; T is `tests/observe/`; VP is `.dev/issues/409/visual-parity/`; RR is `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md`; "the spec" is `./source.md` (its section numbers, Part B step numbers such as 1.4 and Part C step numbers such as 2.12 are cited in each task).
- Do not edit `OBS/export.py`. `record_text` and `snapshot_json` stay byte-identical. Question text appears on screen only; both hash canaries (record and snapshot) pass from Phase 1 onward.
- NO_COLOR output has zero ESC bytes and the same text as the coloured output after SGR removal. ASCII output is pure ASCII with `+ - |` borders and `#` for the block glyph. The 16-colour theme keeps eight distinct role colours.
- Draw only facts the screen has: no owner, requester, mapped-tree, SIGNALS bars or affected-session list (accepted divergences AD-1 to AD-8 of the spec).
- Existing source guards stay true: `QUESTION_GATE_PASSED` and `QUESTION_LINK_PASSED` (`OBS/commands.py` lines 67 and 70) untouched, the words `release-gates.md` and `Task 18` stay in `OBS/commands.py`, no `Console(`, `from_markup`, `sorted(`, `.sort(` or adapter, collector, parse import in `OBS/render.py`, and `len(group.renderables) == len(screen_lines(...))` holds.
- Owner rulings already applied (spec section 10 and Part C): Decision Desk in two columns at 160 and 116 and stacked at 80; questions screen stacked at every width; the 64-hex hash is never shown on screen; the other defaults of spec section 10 apply (D-2 to D-5, D-7 to D-12). OPEN-1 to OPEN-3 are treated as Medium and gating.
- Phase gate rule (spec section 8): each phase ends with the render gate, at most 3 iterations, a fresh reviewer per width each iteration. A phase closes only when every in-scope High and Medium rubric row passes in the last iteration. If a row still fails after iteration 3, or two consecutive iterations do not improve the passing count, write `./.dev/issues/409/visual-parity/scores/<phase>/stop.md` (path relative to the repository root), stop, and ask the owner. Never start the next phase before the previous gate closes.
- Gate outputs (renders, captures, scores) are written under `./artifacts/gates/<phase>/iter-<n>/` in this package; the closing record `scores.json` of the last iteration is also copied to `.dev/issues/409/visual-parity/scores/<phase>/` because the spec's definition of done reads it there.
- The spec's Phase 0 inputs (`render_current.py` and the baseline captures) exist only untracked in a local checkout that must never be edited. They are not on this branch, so Phase 1 rebuilds `render_current.py` from the observer's own view builders and fixtures. Never edit the local checkout.
- Goldens are regenerated only from the current tree, in the same change set as the change that moves them; styled bytes are never written into a golden.
- Nothing under `.claude/` is staged. This plan does not commit, push or open a PR before a human asks; the final task states the PR route for that moment (`/sc:pr-submit --monitor 3`, target `IronbellyOrg/IronClaude`, never `SuperClaude-Org`).
- Judgment call recorded here: spec step 2.13 names `_field_lines`, a function that step 5.2 only creates in the desk phase (spec Phase 5, plan Phase 6). The space-diet work (spec Phase 2, plan Phase 3) therefore applies the label, alignment and badge changes to the existing desk field loop in `OBS/render.py` (lines 347-353 today), and plan Phase 6 replaces that loop with `_field_lines` while keeping those changes.
Start sha: b0c108f0b013dfe9fb8c39a63c81db0363faee02
Diff against the start snapshot: diff --git a/.dev/issues/409/visual-parity/scores/baseline.json b/.dev/issues/409/visual-parity/scores/baseline.json
deleted file mode 100644
index 4643d7ee8..000000000
--- a/.dev/issues/409/visual-parity/scores/baseline.json
+++ /dev/null
@@ -1,39 +0,0 @@
-{
-  "phase": "P0 baseline",
-  "iteration": 1,
-  "method": "text and ANSI tier (no PNG: no browser installed, see png-route.md); one fresh reviewer per width, all rows RB-01 to RB-29 scored",
-  "harness_run": "package folder artifacts/gates/p0/iter-1/ (checks.json + per-width files)",
-  "full_evidence": "the three reviewer returns with one evidence line per row are kept in the package folder artifacts/gates/p0/iter-1/reviewer-outputs/ (width-160.scores.md, width-116.scores.md, width-80.scores.md)",
-  "rows": {
-    "RB-01": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
-    "RB-02": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
-    "RB-03": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
-    "RB-04": {"160": "FAIL", "116": "FAIL", "80": "PASS"},
-    "RB-05": {"160": "PASS", "116": "PASS", "80": "PASS"},
-    "RB-06": {"160": "PASS", "116": "PASS", "80": "PASS"},
-    "RB-07": {"160": "PASS", "116": "PASS", "80": "PASS"},
-    "RB-08": {"160": "PASS", "116": "PASS", "80": "FAIL"},
-    "RB-09": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
-    "RB-10": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
-    "RB-11": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
-    "RB-12": {"160": "PASS", "116": "FAIL", "80": "FAIL"},
-    "RB-13": {"160": "PASS", "116": "FAIL", "80": "FAIL"},
-    "RB-14": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
-    "RB-15": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
-    "RB-16": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
-    "RB-17": {"160": "PASS", "116": "PASS", "80": "PASS"},
-    "RB-18": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
-    "RB-19": {"160": "PASS", "116": "PASS", "80": "PASS"},
-    "RB-20": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
-    "RB-21": {"160": "PASS", "116": "PASS", "80": "FAIL"},
-    "RB-22": {"160": "PASS", "116": "FAIL", "80": "FAIL"},
-    "RB-23": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
-    "RB-24": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
-    "RB-25": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
-    "RB-26": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
-    "RB-27": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
-    "RB-28": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
-    "RB-29": {"160": "FAIL", "116": "FAIL", "80": "FAIL"}
-  },
-  "discrimination_note": "High rows that pass on the baseline are RB-05, RB-06, RB-07 (and RB-08 at 160 and 116, RB-04 at 80 by design: no strip exists at 80). The spec expects exactly these plain-text rows to pass today, so the rubric is discriminating and was not revised. RB-17 and RB-19 pass only vacuously or by the old rule (RB-27 replaces RB-19 and fails)."
-}
diff --git a/.dev/issues/409/visual-parity/scores/baseline.md b/.dev/issues/409/visual-parity/scores/baseline.md
deleted file mode 100644
index 6b612ee47..000000000
--- a/.dev/issues/409/visual-parity/scores/baseline.md
+++ /dev/null
@@ -1,11 +0,0 @@
-# Baseline measurements (plan Phase 1, spec step 0.8)
-
-Measured at the start commit of this work (observer unchanged, `git diff --stat -- src/` empty), from the harness output in the package folder `artifacts/gates/p0/iter-1/`.
-
-RB-22 threshold N: 18
-
-The number is the longest run of consecutive spaces between two non-space characters inside a ledger row line of the `ledger` screen (`base` fixture) at 160 columns (37 row lines). The same measure at 116 columns is 48 and at 80 columns is 34, so RB-22 fails on the baseline for both (a wide blank band after the id column, finding M-17).
-
-Height test (`tests/observe/test_height_budget.py`): all 18 cases pass on today's code, heights 24, 40 and 44 at widths 160, 116 and 80 with 3 and 20 questions. No failing height set exists, so none is excluded.
-
-PNG route: FAIL (no browser installed); the scores below come from the text and ANSI tier (`png-route.md`).
diff --git a/.dev/issues/409/visual-parity/scores/p1/ruling.md b/.dev/issues/409/visual-parity/scores/p1/ruling.md
deleted file mode 100644
index 8da300b79..000000000
--- a/.dev/issues/409/visual-parity/scores/p1/ruling.md
+++ /dev/null
@@ -1,7 +0,0 @@
-# Owner ruling on the Phase 2 gate stop (2026-11-18, given in chat)
-
-The owner answered "A" to the question in `stop.md`.
-
-Ruling: for the colour and theme phase (plan Phase 2) only, the footer-key clause of RB-08 at width 80 (finding M-11, the cut key list on the ledger screen) is deferred to the text-defects phase, where Task 11 fixes it and RB-13 scores it. With that clause deferred, every in-scope High and Medium row passes in iteration 3 at all three widths (`artifacts/gates/p1/iter-3/reviewer-outputs/`), so the phase gate is closed as passed. The rubric file is not edited: the deferral is recorded here, and the text-defects phase gate must score RB-08 at width 80 in full.
-
-Cost if wrong: none for this phase; if Task 11 does not fix the key list, RB-08 at 80 stays failing and that later gate stops.
diff --git a/.dev/issues/409/visual-parity/scores/p1/stop.md b/.dev/issues/409/visual-parity/scores/p1/stop.md
deleted file mode 100644
index aa0e5b566..000000000
--- a/.dev/issues/409/visual-parity/scores/p1/stop.md
+++ /dev/null
@@ -1,30 +0,0 @@
-# Gate stop: colour and theme phase (plan Phase 2, spec P1)
-
-Status: STOPPED after iteration 3. The next phase is not started. Owner decision needed.
-
-## Failing rows after iteration 3
-
-- RB-08 at width 80 (High). Evidence: the ledger screen's key list is cut at 80 columns (`... m mark  e exp>`, the `e export all  q quit` part is lost) and the last line of the screen is `shown 31/54 | collected 80 / reported 80`, so "the footer keys are the last lines" does not hold. The script check (`checks.json`, RB-08, case `ledger@80`) fails the same way in all three iterations. All other in-scope rows (RB-01, RB-05, RB-06, RB-07, RB-09, RB-10, RB-11, RB-23) pass at all three widths in iteration 3.
-
-## Iteration scores (failing High and Medium rows, per width)
-
-| Iteration | 160 | 116 | 80 | What changed before it |
-|---|---|---|---|---|
-| 1 | RB-11 | RB-11 | RB-08, RB-11 | first render |
-| 2 | RB-11 | none | RB-08, RB-11 | absent values at the end of a counts token muted; the selected question keeps its reason muted |
-| 3 | none | none | RB-08 | the counts line `... unavailable (no source)` muted |
-
-Reviewer answers (one per width per iteration): `artifacts/gates/p1/iter-<n>/reviewer-outputs/width-<W>.scores.md` in the plan package.
-
-## Why this cannot be fixed inside this phase
-
-The cut key list at 80 columns is finding M-11. The spec closes it in the text-defects phase (spec P2, step 2.3, `wrap_groups`, rubric RB-13) and that phase regenerates both presentation goldens. The colour phase must leave every `screen_lines` string and both goldens byte-identical (spec P1, "Byte-identical in this phase"). Fixing it here would break that rule. The same defect already failed on the baseline (`scores/baseline.json`, RB-08 at 80 is FAIL), although the spec's baseline expectation listed RB-08 as passing.
-
-## Decision needed from the owner
-
-Choose one:
-
-- Option A (recommended): for this phase's gate only, treat the footer-key clause of RB-08 at width 80 as deferred to the text-defects phase, where RB-13 and the footer fix land, and close this phase as passed. Nothing else changes.
-- Option B: pull the key-list fix (M-11) forward into this phase and re-baseline the release-1 presentation golden here; the colour phase then loses its "no text change" guarantee.
-
-Until the owner answers, no later task of the plan is started.
diff --git a/.dev/issues/409/visual-parity/scores/p2/notes.md b/.dev/issues/409/visual-parity/scores/p2/notes.md
deleted file mode 100644
index 70f804c54..000000000
--- a/.dev/issues/409/visual-parity/scores/p2/notes.md
+++ /dev/null
@@ -1,22 +0,0 @@
-# Text-defects phase notes (plan Phase 3)
-
-## RB-22 (wide blank band after the id column), spec step 2.6: not applied, deferred (Low row)
-
-Measured at the start of the phase on the `ledger` screen, `base` fixture (`scores/baseline.md`): the longest blank run inside a row is 18 cells at 160 columns (threshold N), 48 at 116 and 34 at 80, so RB-22 fails at 116 and 80.
-
-Why step 2.6 was not applied: the step gives `line` and `short` the full-width id rule (`22 + min(extra, 26)`, rest to the flags column). Worked from the formulas in `_columns`:
-
-- at 116 columns the id column would go from 52 to 48 cells (blank run about 43, still above 18);
-- at 80 columns it would go from 38 to 42 cells (a wider band, not a narrower one).
-
-Reaching N = 18 needs an id column of about 22 cells, which would cut the long identifiers of the `long-identifiers` fixture with `>` in the list. The spec marks the step optional and the row Low, and a Low row may be logged as deferred. RB-22 is deferred with this reason; the rule that column widths stay static between refreshes (finding M-17) is untouched.
-
-## Phase 3 gate (tasks 10 to 16), all runs in `artifacts/gates/p2/`
-
-Both sub-gates (2a and 2b) were run as one gate after Task 16; iteration 1 failed RB-24 (116, 80), RB-28 (80) and RB-29 (116, 80); iteration 2 passed every in-scope High and Medium row at 160, 116 and 80.
-
-- RB-22 after the space diet: the harness measures a longest blank run of 44 cells at 116 and 25 at 80 (N = 18). The row is Low and stays deferred: the long runs sit between a short fixture id and the next column, and the status column now grows to the widest status shown (a merged status is never cut), so a narrower id column would cut real ids. Reviewers recorded it as out of scope; the script row says fail.
-- Rubric conflict, RB-12 versus RB-28: RB-12 (heading and rule at 116 and 80) was scored when it was written; Task 15 and RB-28 then removed the rule row under the heading. The footer rule stays (RB-20). Reviewers scored RB-12 as the heading with no rule row.
-- Harness changes to follow the spec (rubric wording untouched): the `(no source)` tail is dropped from the screen count (2.9 (c)); the desk starts with `age <age>` and has no message id (2.9 (d)); desk labels are plain and aligned (2.13); RB-19 is replaced by RB-27 (2.12); script checks were added for RB-24, RB-25, RB-26 and RB-28.
-- Plan wording that cannot hold as written (recorded, not blocking): the trailing-hash fixture keeps its four-line cut with `...` only at 80 columns (stripped it is 327 characters and fits four lines at 116 and 160); the selected list row is a strict prefix of the question text ending in `>`, so the string census passes on the whole text but a reviewer may read the prefix as a second mention.
-- The worktree note moved to the worker inspector (shown only when the questions are on).
diff --git a/.dev/issues/409/visual-parity/scores/p2/scores.json b/.dev/issues/409/visual-parity/scores/p2/scores.json
deleted file mode 100644
index ea6320ee2..000000000
--- a/.dev/issues/409/visual-parity/scores/p2/scores.json
+++ /dev/null
@@ -1,18 +0,0 @@
-{
-  "phase": "plan Phase 3 (spec Phase 2), sub-gates 2a and 2b run together after Task 16",
-  "iteration": 2,
-  "gate_dir": ".dev/tasks/to-do/TASK-WF-redesignSpec-20261118-043319/artifacts/gates/p2/iter-2",
-  "route": "text and ANSI tier (the PNG route is unavailable, see png-route.md)",
-  "widths": {
-    "160": {"failing_high_medium": [], "other": {"RB-22": "FAIL (Low, deferred, see notes.md)"}},
-    "116": {"failing_high_medium": [], "other": {"RB-22": "FAIL (Low, deferred, see notes.md); reviewer marked it out of scope"}},
-    "80": {"failing_high_medium": [], "other": {"RB-22": "FAIL (Low, deferred, see notes.md); reviewer marked it out of scope"}}
-  },
-  "in_scope_rows": ["RB-01", "RB-05", "RB-06", "RB-07", "RB-08", "RB-09", "RB-10", "RB-11", "RB-12", "RB-13", "RB-15", "RB-20", "RB-21", "RB-22", "RB-23", "RB-24", "RB-25", "RB-26", "RB-27", "RB-28", "RB-29"],
-  "script_rows": "artifacts/gates/p2/iter-2/checks.json: every row passes except RB-22",
-  "iteration_1": {
-    "failed": {"116": ["RB-24", "RB-29"], "80": ["RB-24", "RB-28", "RB-29"], "160": []},
-    "fixes": "80 column liveness dot and legend, id and status columns sized to the widest value, script rows for RB-24/25/26/28, reviewer scope note for RB-29"
-  },
-  "result": "PASS for every in-scope High and Medium row; RB-22 (Low) failing and deferred"
-}
diff --git a/.dev/issues/409/visual-parity/tools/render_compare.py b/.dev/issues/409/visual-parity/tools/render_compare.py
deleted file mode 100644
index 5e6e6eb7b..000000000
--- a/.dev/issues/409/visual-parity/tools/render_compare.py
+++ /dev/null
@@ -1,521 +0,0 @@
-"""Render-compare harness for the observer visual-parity gate (issue #606, spec section 8 and step 0.3).
-
-Command::
-
-    uv run python .dev/issues/409/visual-parity/tools/render_compare.py --out <dir> \
-        [--depth 16,256,truecolor] [--heights 44,40,24,12,8] [--check]
-
-For the screens ``ledger``, ``questions``, ``desk`` and ``desk-planask`` (views from
-``inputs/tools/render_current.py``) at widths 160, 116 and 80 (heights 48, 42, 42) it writes, per
-width into ``<out>/<width>/``:
-
-    <screen>.txt                 plain ``screen_lines``
-    <screen>.<depth>.ansi/.html  the coloured stream and ``export_html`` for each selected depth
-    <screen>.nocolor.txt         env NO_COLOR=1
-    <screen>.ascii.txt           ``--ascii`` plain, and <screen>.ascii.ansi (16-colour stream)
-    <screen>.h<height>.txt       with --heights: a text-only height matrix
-    manifest.json                line counts, widest cell, and which depths were really produced
-
-``--check`` also writes ``<out>/checks.json``: one entry per script-checked rubric row, each
-``{"status": "pass"|"fail"|"na", "evidence": [...]}``. A run without ``--check`` or without all
-five passes is not a valid gate run.
-
-The capture is ``console.file.getvalue()`` of a recording console; ``export_text(styles=True)``
-is never used (it ignores NO_COLOR and the colour downgrade).
-"""
-
-from __future__ import annotations
-
-import argparse
-import dataclasses
-import importlib.util
-import io
-import json
-import re
-import sys
-from dataclasses import dataclass
-from pathlib import Path
-
-HERE = Path(__file__).resolve().parent
-VP = HERE.parent
-ROOT = VP.parents[3]
-if str(ROOT) not in sys.path:
-    sys.path.insert(0, str(ROOT))
-
-
-def _load_current():
-    spec = importlib.util.spec_from_file_location(
-        "render_current", VP / "inputs" / "tools" / "render_current.py"
-    )
-    module = importlib.util.module_from_spec(spec)
-    spec.loader.exec_module(module)
-    return module
-
-
-current = _load_current()
-
-from rich.cells import cell_len  # noqa: E402
-
-from superclaude.cli.observe import view as observe_view  # noqa: E402
-from superclaude.cli.observe.render import render, screen_lines  # noqa: E402
-from superclaude.cli.observe.terminal import make_console, resolve_policy  # noqa: E402
-
-SCREENS = current.SCREENS
-WIDTHS = current.WIDTHS
-HEIGHTS = current.MOCKUP_HEIGHTS
-RICH_DEPTH = {"16": "standard", "256": "256", "truecolor": "truecolor"}
-SGR = re.compile(r"\x1b\[[0-9;]*m")
-ANSI_ANY = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
-# The eight mockup palette triples (spec RB-01, 04 section 2).
-PALETTE = {
-    (225, 233, 238): "base",
-    (165, 182, 194): "muted",
-    (82, 108, 128): "slate",
-    (250, 178, 25): "amber",
-    (112, 205, 226): "cyan",
-    (139, 215, 175): "green",
-    (240, 141, 150): "red",
-    (194, 173, 242): "violet",
-}
-HEX_RUN = re.compile(r"[0-9a-fA-F]{32,}")
-
-
-def strip_sgr(text: str) -> str:
-    return SGR.sub("", text)
-
-
-@dataclass
-class CaseOutput:
-    plain: list[str]
-    stream: str
-    html: str
-    produced_depth: str  # the depth really rendered ("n/a" when the policy cannot carry it yet)
-
-
-def _policy(width: int, height: int, *, env: dict, ascii: bool):
-    return resolve_policy(env, "utf-8", {"ascii": ascii}, width, height)
-
-
-def render_case(view, width: int, height: int, *, env: dict, ascii: bool, depth: str = "16") -> CaseOutput:
-    """One render: the plain lines, the written stream (SGR included) and the recorded HTML."""
-    policy = _policy(width, height, env=env, ascii=ascii)
-    produced = depth
-    if hasattr(policy, "color_system"):
-        if policy.color_system is not None:
-            policy = dataclasses.replace(policy, color_system=RICH_DEPTH[depth])
-    elif depth != "16":
-        produced = "not-available-before-P1"  # make_console pins "standard" until step 1.1
-    console = make_console(policy, file=io.StringIO(), record=True)
-    console.print(render(view, policy))
-    return CaseOutput(
-        plain=screen_lines(view, policy),
-        stream=console.file.getvalue(),
-        html=console.export_html(inline_styles=True),
-        produced_depth=produced,
-    )
-
-
-def _write(path: Path, text: str) -> None:
-    path.parent.mkdir(parents=True, exist_ok=True)
-    path.write_text(text, encoding="utf-8")
-
-
-# -- checks ---------------------------------------------------------------------------------
-
-
-def _row(status: str, *evidence: str) -> dict:
-    return {"status": status, "evidence": [e for e in evidence if e]}
-
-
-def _flat(lines) -> str:
-    return " ".join(" ".join(lines).split())
-
-
-def _unframe(line: str) -> str:
-    """Strip a one-cell margin and a rounded, heavy or ASCII border pair when present."""
-    text = re.sub(r"^\s?[│┃|]\s", "", line)
-    return re.sub(r"\s[│┃|]\s?$", "", text) if text != line else line
-
-
-def _required_literals(name: str, view) -> list[str]:
-    out: list[str] = []
-    panel = view.questions
-    if panel is None:
-        out.append(view.gap_notice)
-    else:
-        # the screen count drops "(no source)" (spec 2.9 (c)); the record keeps the full counts_line
-        out += [
-            panel.disclosure,
-            panel.caveat_line,
-            panel.retention_line,
-            getattr(panel, "screen_counts_line", "") or panel.counts_line,
-        ]
-        if name in ("desk", "desk-planask"):
-            out.append(observe_view.DESK_TITLE)
-    return [x for x in out if x]
-
-
-def check_screen(name: str, view, width: int, height: int, outs: dict, nocolor: CaseOutput, ascii_out: CaseOutput):
-    """Per-screen rows; returns {row: {status, evidence}} for one width."""
-    rows: dict[str, dict] = {}
-    plain = outs["plain"]
-    flat = _flat(plain)
-
-    # RB-05 required literals, whole and uncut (whitespace-collapsed, so wrapping is allowed).
-    missing = [lit for lit in _required_literals(name, view) if _flat([lit]) not in flat]
-    rows["RB-05"] = _row("fail", *[f"missing or cut: {m[:70]}" for m in missing]) if missing else _row("pass")
-
-    # RB-06 NO_COLOR: no ESC, same text as the coloured pass after SGR removal.
-    esc = "\x1b" in nocolor.stream
-    coloured = [ln.rstrip() for ln in strip_sgr(outs["stream"]).split("\n")]
-    plain_lines = [ln.rstrip() for ln in plain]
-    same = [ln for ln in coloured if ln] == [ln for ln in plain_lines if ln]
-    rows["RB-06"] = (
-        _row("fail", "ESC byte in NO_COLOR stream" if esc else "", "" if same else "SGR-stripped text differs from plain")
-        if esc or not same
-        else _row("pass")
-    )
-
-    # RB-07 ASCII: pure ASCII; a framed pane uses + - |, never ?
-    bad: list[str] = []
-    if not all(ln.isascii() for ln in ascii_out.plain) or not ascii_out.stream.isascii():
-        bad.append("non-ASCII in ASCII pass")
-    borders = [ln for ln in ascii_out.plain if ln.lstrip().startswith("+")]
-    bad += [f"? inside a border: {ln[:60]}" for ln in borders if "?" in ln]
-    rows["RB-07"] = _row("fail", *bad) if bad else (_row("pass") if borders else _row("pass", "no frame yet; text part only"))
-
-    # RB-08 fit: width, height, footer last, no blink, no mouse sequences.
-    problems: list[str] = []
-    for ln in plain:
-        if cell_len(ln) > width:
-            problems.append(f"line wider than {width}: {ln[:50]}")
-    if len(plain) > height:
-        problems.append(f"{len(plain)} rows > height {height}")
-    if not any("q quit" in ln for ln in plain[-4:]):
-        problems.append("footer keys are not among the last lines")
-    for label, text in (("stream", outs["stream"]), ("nocolor", nocolor.stream)):
-        if re.search(r"\x1b\[(?:[0-9;]*;)?[56](?:;[0-9;]*)?m", text):
-            problems.append(f"SGR 5 or 6 (blink) in {label}")
-        if re.search(r"\x1b\[\?100[0236]h", text):
-            problems.append(f"mouse sequence in {label}")
-    rows["RB-08"] = _row("fail", *problems) if problems else _row("pass")
-
-    # RB-13 the key list is whole: every two-space group sits whole on one line; none cut by ' >'.
-    help_line = getattr(view, "help_line", "")
-    groups = [g for g in re.split(r"\s{2,}", help_line.strip()) if g]
-    cut = [g for g in groups if not any(g in ln for ln in plain)]
-    rows["RB-13"] = _row("fail", *[f"key group not whole: {g}" for g in cut]) if cut else _row("pass")
-
-    # RB-20 a rule line precedes the footer keys; the key pair n/p question is intact when linked.
-    first_help = next((i for i, ln in enumerate(plain) if groups and groups[0] in ln), None)
-    rule_ok = first_help is not None and first_help > 0 and bool(re.fullmatch(r"[─-]{10,}", plain[first_help - 1].strip()))
-    pair_ok = "n/p question" not in help_line or any("n/p question" in ln for ln in plain)
-    rows["RB-20"] = _row("pass") if rule_ok and pair_ok else _row("fail", "" if rule_ok else "no rule line above the footer", "" if pair_ok else "n/p question split")
-
-    # RB-21 counts lines are not cut inside a token: a trailing ' >' must follow a space.
-    cut_counts = [ln for ln in plain[:6] if ln.endswith(">") and len(ln) > 1 and ln[-2] != " "]
-    rows["RB-21"] = _row("fail", *[f"cut inside a token: {ln[-30:]}" for ln in cut_counts]) if cut_counts else _row("pass")
-
-    # RB-19 Q7 is replaced by RB-27 (spec step 2.12): the hash is no longer shown at all.
-    if name == "desk-planask":
-        rows["RB-19"] = _row("na", "replaced by RB-27 (spec step 2.12): the hash is not shown")
-    # RB-27 no run of 32 hex characters on the questions screen or the desk.
-    if name != "ledger":
-        runs = [ln for ln in plain if HEX_RUN.search(ln)]
-        rows["RB-27"] = _row("fail", *[f"hex run shown: {ln.strip()[:70]}" for ln in runs[:2]]) if runs else _row("pass")
-
-    # RB-24 string census (Part C): the question text, the Run id, the count words and the
-    # freshness state of the question source each occur once on the screen (the panel's own state
-    # line `question read: ...` is the one allowed second mention of the state, RR 45).
-    panel = view.questions
-    if panel is not None and name != "ledger":
-        census: dict[str, int] = {}
-        if getattr(view, "desk", None) is not None and view.desk.ask:
-            census[f"question text {view.desk.ask[:30]!r}"] = flat.count(_flat([view.desk.ask]))
-        else:
-            for q in panel.lines:
-                census[f"question text {q.shown[:30]!r}"] = flat.count(_flat([q.shown]))
-        census["Run id"] = flat.count(panel.run_id)
-        census["seen, not resolved"] = flat.count("seen, not resolved")
-        census["closed by evidence"] = flat.count("closed by evidence")
-        census["freshness cell"] = flat.count(getattr(panel, "screen_cell", "") or "questions OK")
-        twice = [f"{k}: {n} times" for k, n in census.items() if n != 1]
-        rows["RB-24"] = _row("fail", *twice) if twice else _row("pass")
-
-        # RB-25 reasons said once, in the title.
-        has_reason = any(getattr(q, "reason", "") for q in panel.lines)
-        suffix = [ln for ln in plain if "reason unknown" in ln]
-        note = "reasons: none in source" in flat
-        bad = [f"row suffix: {ln.strip()[:60]}" for ln in suffix[:2]] + ([] if note or has_reason else ["title note missing"])
-        rows["RB-25"] = _row("fail", *bad) if bad else _row("pass")
-
-    # RB-26 status: one ACTIVE badge only for active/active/none, else three raw values.
-    if name == "ledger":
-        wrong = []
-        for rv in view.visible_rows:
-            line = next((ln for ln in plain if rv.dispatch_id in ln), "")
-            active = (rv.dispatch_status, rv.terminal_state, rv.outcome) == ("active", "active", "none")
-            triple = f"{rv.dispatch_status}/{rv.terminal_state}/{rv.outcome}"
-            if line and active != (" ACTIVE" in line) and "FROZEN" not in line:
-                wrong.append(f"{rv.dispatch_id}: ACTIVE shown={not active}")
-            if line and not active and triple not in line and width >= 116:
-                wrong.append(f"{rv.dispatch_id}: raw values {triple} not shown whole")
-        rows["RB-26"] = _row("fail", *wrong[:3]) if wrong else _row("pass")
-    elif name in ("desk", "desk-planask") and getattr(view, "desk", None) is not None:
-        fields = dict(view.desk.session_fields)
-        triple = (fields.get("dispatchStatus"), fields.get("terminalState"), fields.get("outcome"))
-        block = plain[next(i for i, ln in enumerate(plain) if observe_view.DESK_TITLE in ln) :]
-        shown_badge = any(re.match(r"^status\s+ACTIVE\b", _unframe(ln)) for ln in block)
-        raw_rows = [lbl for lbl in ("dispatchStatus", "terminalState", "outcome") if any(re.match(rf"^{lbl}\s+\S", _unframe(ln)) for ln in block)]
-        ok = shown_badge if triple == ("active", "active", "none") else (not shown_badge and len(raw_rows) == 3)
-        rows["RB-26"] = _row("pass") if ok else _row("fail", f"badge={shown_badge} raw rows={raw_rows} for {triple}")
-
-    # RB-28 ledger diet (the script part): no flags column, one rule line (above the footer), no
-    # '+N more' row, a legend, and any non-alive value spelled out in the NO_COLOR pass.
-    if name == "ledger":
-        problems = []
-        if any(re.search(r"\bflags\b", ln) for ln in plain[:12]):
-            problems.append("a flags column heading is shown")
-        rules = [ln for ln in plain if re.fullmatch(r"[─-]{10,}", ln.strip())]
-        if len(rules) != 1:
-            problems.append(f"{len(rules)} rule lines (only the footer rule may stay)")
-        if any(re.search(r"\+\d+ more", ln) for ln in plain):
-            problems.append("a '+N more' row is shown")
-        if True:  # the liveness dot is at every width (the 80 column short form too)
-            for rv in view.visible_rows:
-                verdict = str(rv.raw.liveness_verdict)
-                line = next((ln for ln in nocolor.plain if rv.dispatch_id in ln), "")
-                if line and verdict not in ("alive", "live") and verdict not in line and "unknown" not in line:
-                    problems.append(f"{rv.dispatch_id}: non-alive value {verdict!r} not spelled out")
-        rows["RB-28"] = _row("fail", *problems[:3]) if problems else _row("pass")
-
-    # RB-14 desk (a), (c), (d) on the plain pass.
-    if name in ("desk", "desk-planask"):
-        body = [_unframe(ln) for ln in plain]
-        try:
-            start = next(i for i, ln in enumerate(body) if observe_view.DESK_TITLE in ln)
-            first = body[start + 1]
-            # spec 2.9 (d) and 2.13: the first body line is `age <age>` (no message id) and the
-            # field lines are `label<padding>value` with plain labels in one aligned column
-            label = r"(?:session|state|alive|next|status|worktree|dispatchStatus|terminalState|outcome)"
-            fields = [(i, ln) for i, ln in enumerate(body[start + 1 :], start + 1) if re.match(rf"^{label}\s+\S", ln)]
-            a_ok = bool(re.match(r"^(?:\S+\s+)?age\s", first)) and (not fields or all(i > start + 1 for i, _ in fields))
-            offsets = {re.match(rf"^({label}\s+)", ln).end() for _, ln in fields}
-            c_ok = len(offsets) <= 1
-            d_ok = all(cell_len(ln) <= width for ln in plain)
-            parts = [] if a_ok else ["question text does not lead (qid age, then text, then fields)"]
-            parts += [] if c_ok else [f"field values start at {len(offsets)} different offsets"]
-            parts += [] if d_ok else ["a line exceeds the width"]
-            rows["RB-14"] = _row("fail", *parts) if parts else _row("pass")
-        except (StopIteration, IndexError):
-            rows["RB-14"] = _row("fail", "desk not found on screen")
-
-    # RB-17 census (b)/(c): run, caveat and retention lines occur exactly once each.
-    if view.questions is not None:
-        census = {lit: flat.count(_flat([lit])) for lit in (view.questions.run_line, view.questions.caveat_line, view.questions.retention_line) if lit}
-        wrong = [f"{k[:40]}: {n} times" for k, n in census.items() if n != 1]
-        rows["RB-17"] = _row("fail", *wrong) if wrong else _row("pass", "census only; pane frame checked after phase 4")
-
-    # RB-04 (c), (d): the counts line is whole on one line with the figure.
-    if view.questions is not None:
-        counts = getattr(view.questions, "screen_counts_line", "") or view.questions.counts_line
-        whole = any(_flat([counts]) in _flat([ln]) for ln in plain)
-        rows["RB-04"] = _row("pass") if whole else _row("fail", "counts line not whole on one line")
-
-    # RB-01 (a): every foreground colour of the truecolor stream is one of the eight triples.
-    return rows
-
-
-def role_census_truecolor(stream: str) -> dict:
-    colours = set()
-    for m in re.finditer(r"\x1b\[([0-9;]*)m", stream):
-        parts = [int(p) for p in m.group(1).split(";") if p.isdigit()]
-        i = 0
-        while i < len(parts):
-            if parts[i] == 38 and parts[i + 1 : i + 2] == [2] and len(parts) >= i + 5:
-                colours.add(tuple(parts[i + 2 : i + 5]))
-                i += 5
-            elif parts[i] == 38 and parts[i + 1 : i + 2] == [5]:
-                colours.add(("idx", parts[i + 2]) if i + 2 < len(parts) else ("idx", -1))
-                i += 3
-            else:
-                if 30 <= parts[i] <= 37 or 90 <= parts[i] <= 97:
-                    colours.add(("ansi", parts[i]))
-                i += 1
-    return {c for c in colours}
-
-
-def theme_rows() -> dict:
-    """RB-09 and RB-10(d) read the theme module when it exists (phase 2 onward)."""
-    try:
-        from superclaude.cli.observe import theme  # type: ignore
-    except ImportError:
-        return {
-            "RB-09": _row("na", "theme.py not built yet (plan Phase 2)"),
-            "RB-10": _row("na", "theme.py not built yet (plan Phase 2)"),
-        }
-    palette_roles = ("attention", "identity", "secondary", "muted", "state_running", "state_settled", "state_failed", "state_frozen")
-    codes = {}
-    for role in palette_roles:
-        style = theme.style_for(role, "standard")
-        codes[role] = None if style is None else style.color.number if style.color is not None else None
-    distinct = len({v for v in codes.values() if v is not None}) == len([v for v in codes.values() if v is not None]) and len(set(codes.values())) == len(codes)
-    rb09 = _row("pass") if distinct else _row("fail", f"16-colour role codes collide: {codes}")
-    keys = [("workerState", "running"), ("workerState", "succeeded"), ("workerState", "failed"), ("dispatchStatus", "completed"), ("liveness", "alive")]
-    state = getattr(theme, "STATE_ROLE", {})
-    missing = [k for k in keys if k not in state]
-    frozen_ok = getattr(theme, "FROZEN_ROLE", None) == "state_frozen"
-    rb10 = _row("pass", "(d) table keys only; (a)(b) census is added with the phase 2 gate") if not missing and frozen_ok else _row("fail", f"STATE_ROLE missing {missing}", "" if frozen_ok else "FROZEN_ROLE != state_frozen")
-    return {"RB-09": rb09, "RB-10": rb10}
-
-
-def fg_by_char(stream_line: str) -> list[tuple[str, int | None]]:
-    """(character, foreground SGR code) for each visible character of one 16-colour stream line."""
-    out: list[tuple[str, int | None]] = []
-    fg: int | None = None
-    pos = 0
-    for m in SGR.finditer(stream_line):
-        out += [(ch, fg) for ch in stream_line[pos : m.start()]]
-        for p in [int(x) if x else 0 for x in m.group(0)[2:-1].split(";")]:
-            if p == 0 or p == 39:
-                fg = None
-            elif 30 <= p <= 37 or 90 <= p <= 97:
-                fg = p
-        pos = m.end()
-    out += [(ch, fg) for ch in stream_line[pos:]]
-    return out
-
-
-def state_census(stream: str) -> dict:
-    """RB-10 (a) and (b) on the 16-colour ledger stream: a state word in the table carries exactly
-    its role's colour, and every other state word carries the body colour (never a state role)."""
-    try:
-        from superclaude.cli.observe import theme  # type: ignore
-    except ImportError:
-        return _row("na", "theme.py not built yet (plan Phase 2)")
-
-    def code(role: str) -> int | None:
-        style = theme.style_for(role, "standard")
-        number = style.color.number if style and style.color is not None else None
-        return None if number is None else (30 + number if number < 8 else 82 + number)
-
-    in_table = {value: theme.STATE_ROLE[key] for key, value in ((k, k[1]) for k in theme.STATE_ROLE)}
-    other = ("idle", "blocked", "exited", "ready", "stopped", "abandoned", "active", "dispatched", "ended", "unverifiable")
-    bad: list[str] = []
-    checked = 0
-    for line in stream.split("\n"):
-        plain = strip_sgr(line)
-        if not re.search(r"\bw-\d{3}\b", plain):
-            continue
-        chars = fg_by_char(line)
-        for m in re.finditer(r"\b[A-Za-z]+\b", plain):
-            word = m.group(0)
-            if word in in_table:
-                want = code(in_table[word])
-            elif word in other:
-                want = code("body")
-            else:
-                continue
-            checked += 1
-            got = {fg for _, fg in chars[m.start() : m.end()]}
-            if got != {want}:
-                bad.append(f"{word!r} has colours {sorted(map(str, got))}, want {want}: {plain.strip()[:60]}")
-    if not checked:
-        return _row("fail", "no state word found on the ledger rows")
-    return _row("fail", *bad[:4]) if bad else _row("pass", f"{checked} state words checked against the table")
-
-
-# -- main -----------------------------------------------------------------------------------
-
-
-def main(argv=None) -> int:
-    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
-    ap.add_argument("--out", required=True)
-    ap.add_argument("--depth", default="16,256,truecolor")
-    ap.add_argument("--heights", default="")
-    ap.add_argument("--check", action="store_true")
-    args = ap.parse_args(argv)
-    out = Path(args.out)
-    depths = [d.strip() for d in args.depth.split(",") if d.strip()]
-    for d in depths:
-        if d not in RICH_DEPTH:
-            ap.error(f"unknown depth {d!r}; use 16, 256 or truecolor")
-    heights = [int(h) for h in args.heights.split(",") if h.strip()]
-    views = current.build_views()
-    checks: dict[str, dict] = {}
-    all_rows: dict[str, list] = {}
-
-    def merge(row_id: str, key: str, row: dict) -> None:
-        all_rows.setdefault(row_id, []).append((key, row))
-
-    for width in WIDTHS:
-        wdir = out / str(width)
-        height = HEIGHTS[width]
-        manifest: dict = {"width": width, "height": height, "screens": {}}
-        for name in SCREENS:
-            view = views[name]
-            base = render_case(view, width, height, env={}, ascii=False, depth="16")
-            nocolor = render_case(view, width, height, env={"NO_COLOR": "1"}, ascii=False)
-            ascii_out = render_case(view, width, height, env={}, ascii=True)
-            _write(wdir / f"{name}.txt", "\n".join(base.plain) + "\n")
-            _write(wdir / f"{name}.nocolor.txt", nocolor.stream)
-            _write(wdir / f"{name}.ascii.txt", "\n".join(ascii_out.plain) + "\n")
-            _write(wdir / f"{name}.ascii.ansi", ascii_out.stream)
-            entry = {"lines": len(base.plain), "widest_cell": max((cell_len(x) for x in base.plain), default=0), "depths": {}}
-            truecolor_stream = ""
-            for depth in depths:
-                case = render_case(view, width, height, env={}, ascii=False, depth=depth)
-                _write(wdir / f"{name}.{depth}.ansi", case.stream)
-                _write(wdir / f"{name}.{depth}.html", case.html)
-                entry["depths"][depth] = case.produced_depth
-                if depth == "truecolor":
-                    truecolor_stream = case.stream
-            for h in heights:
-                _write(wdir / f"{name}.h{h}.txt", "\n".join(render_case(view, width, h, env={}, ascii=False).plain) + "\n")
-            manifest["screens"][name] = entry
-            if args.check:
-                rows = check_screen(name, view, width, height, {"plain": base.plain, "stream": base.stream}, nocolor, ascii_out)
-                for rid, row in rows.items():
-                    merge(rid, f"{name}@{width}", row)
-                if name == "ledger" and width == 160:
-                    merge("RB-10", "census@160", state_census(base.stream))
-                if truecolor_stream and entry["depths"].get("truecolor") == "truecolor":
-                    colours = role_census_truecolor(truecolor_stream)
-                    stray = [c for c in colours if c not in PALETTE]
-                    merge("RB-01", f"{name}@{width}", _row("fail", f"foreground colours outside the eight triples: {sorted(map(str, stray))[:4]}") if stray else _row("pass", "census (a) only; (b)-(f) are reviewer rows"))
-                else:
-                    merge("RB-01", f"{name}@{width}", _row("na", "no truecolor stream before plan Phase 2"))
-        _write(wdir / "manifest.json", json.dumps(manifest, indent=1, sort_keys=True))
-
-    if args.check:
-        for rid, row in theme_rows().items():
-            merge(rid, "theme", row)
-        for rid in ("RB-16",):
-            all_rows[rid] = [("roles", _row("na", "needs role spans (plan Phase 2 and Phase 5); checked then"))]
-        baseline_md = VP / "scores" / "baseline.md"
-        n_known = baseline_md.exists() and re.search(r"RB-22 threshold N:\s*(\d+)", baseline_md.read_text(encoding="utf-8"))
-        ledger_rows = []
-        for width in (116, 80):
-            lines = (out / str(width) / "ledger.txt").read_text(encoding="utf-8").splitlines()
-            runs = [max((len(m.group(0)) for m in re.finditer(r"(?<=\S) {2,}(?=\S)", ln)), default=0) for ln in lines if re.search(r"w-\d{3}", ln)]
-            ledger_rows.append((width, max(runs, default=0)))
-        if n_known:
-            limit = int(n_known.group(1))
-            bad = [f"{w} cols: blank run {r} > N={limit}" for w, r in ledger_rows if r > limit]
-            all_rows["RB-22"] = [("ledger", _row("fail", *bad) if bad else _row("pass", f"N={limit}"))]
-        else:
-            all_rows["RB-22"] = [("ledger", _row("na", f"threshold N not recorded yet; measured {ledger_rows}"))]
-        for rid, entries in sorted(all_rows.items()):
-            statuses = {row["status"] for _, row in entries}
-            status = "fail" if "fail" in statuses else ("pass" if "pass" in statuses else "na")
-            checks[rid] = {
-                "status": status,
-                "cases": {key: row for key, row in entries if row["status"] != "pass"} or {"all": "pass"},
-            }
-        _write(out / "checks.json", json.dumps(checks, indent=1, sort_keys=True))
-    print(f"render_compare: wrote {out}" + (f" ({len(checks)} rubric rows checked)" if args.check else ""))
-    return 0
-
-
-if __name__ == "__main__":
-    raise SystemExit(main())
diff --git a/src/superclaude/cli/observe/render.py b/src/superclaude/cli/observe/render.py
index 736937e2b..29444567e 100644
--- a/src/superclaude/cli/observe/render.py
+++ b/src/superclaude/cli/observe/render.py
@@ -850,16 +850,9 @@ def _panel_lines(
     ``desk_open``; otherwise it is the hidden-desk notice and goes inside the list frame. The list
     is heavy when no desk is shown and round when one is."""
     pane, inner = _pane_widths(policy)
-    note = "" if any(q.reason for q in panel.lines) else f"  {QUESTIONS_REASONS_NOTE}"
-    lines = _wrapped(f"{panel.run_line}{note}", inner, policy, "muted")
-    for state_line in panel.state_lines:  # the state of the read comes first
-        lines += _wrapped(state_line, inner, policy, "muted")
-    lines += [
-        _absent_tail(text, "identity")
-        for text in wrap(panel.screen_counts_line or panel.counts_line, inner, policy)
-    ]
     shown, cut = panel.window(capacity)
-    lines += [_question_line(q, policy, stub=desk_open, inner=inner) for q in shown]
+    # The question rows lead the pane; the Run id is in the border title.
+    lines = [_question_line(q, policy, stub=desk_open, inner=inner) for q in shown]
     if cut:
         lines += _wrapped(cut, inner, policy, "muted")
     if any(q.selected for q in panel.lines) and not any(q.selected for q in shown):
@@ -871,12 +864,20 @@ def _panel_lines(
     for text in (panel.empty_text, panel.window_full_text, *panel.notes):
         if text:
             lines += _wrapped(text, inner, policy, "muted")
+    for state_line in panel.state_lines:  # the state of the read, then the count
+        lines += _wrapped(state_line, inner, policy, "muted")
+    lines += [
+        _absent_tail(text, "identity")
+        for text in wrap(panel.screen_counts_line or panel.counts_line, inner, policy)
+    ]
+    if not any(q.reason for q in panel.lines):  # said once, not on every row
+        lines += _wrapped(QUESTIONS_REASONS_NOTE, inner, policy, "muted")
     lines += _wrapped(panel.disclosure, inner, policy, "muted")
     lines += _wrapped(panel.caveat_line, inner, policy, "muted")
     lines += _wrapped(panel.retention_line, inner, policy, "muted")
     framed = _indent(
         _frame(
-            panel.title,
+            f"{panel.title}  {panel.run_line}",
             lines,
             pane,
             policy,
diff --git a/src/superclaude/cli/observe/theme.py b/src/superclaude/cli/observe/theme.py
deleted file mode 100644
index a8346b182..000000000
--- a/src/superclaude/cli/observe/theme.py
+++ /dev/null
@@ -1,126 +0,0 @@
-"""Colour roles for the observer screens, one explicit table per colour depth.
-
-The screen builders tag text with a semantic role (``attention``, ``muted``, ``state_running``
-and so on); this module maps a role and a depth to a Rich ``Style``. The depth is the
-``color_system`` of the terminal policy: ``"truecolor"`` uses the design-mockup palette exactly,
-``"256"`` the nearest indexed colours, and ``"standard"`` (16 colours) named ANSI colours only,
-because Rich's automatic downgrade of the mockup RGB values collapses several roles onto one
-index. No role sets blink, dim or reverse. No module here builds a console or reads the
-environment: the terminal policy module owns both.
-"""
-
-from __future__ import annotations
-
-from rich.style import Style
-
-ROLES: tuple[str, ...] = (
-    "title",
-    "attention",
-    "attention_title",
-    "identity",
-    "secondary",
-    "body",
-    "body_bold",
-    "muted",
-    "selected",
-    "border_attention",
-    "border_secondary",
-    "border_count",
-    "state_running",
-    "state_settled",
-    "state_failed",
-    "state_frozen",
-)
-
-# Each role names one of the eight palette colours and says whether it is bold.
-_PALETTE_OF: dict[str, str] = {
-    "title": "cyan",
-    "attention": "amber",
-    "attention_title": "amber",
-    "identity": "base",
-    "secondary": "slate",
-    "body": "base",
-    "body_bold": "base",
-    "muted": "muted",
-    "selected": "amber",
-    "border_attention": "amber",
-    "border_secondary": "slate",
-    "border_count": "cyan",
-    "state_running": "green",
-    "state_settled": "cyan",
-    "state_failed": "red",
-    "state_frozen": "violet",
-}
-_BOLD: frozenset[str] = frozenset(
-    {"title", "attention", "attention_title", "secondary", "body_bold", "selected"}
-)
-
-# The eight palette colours per depth (mockup RGB; 256-colour indexes; named 16-colour ANSI colours).
-_COLOURS: dict[str, dict[str, str]] = {
-    "truecolor": {
-        "base": "rgb(225,233,238)",
-        "muted": "rgb(165,182,194)",
-        "slate": "rgb(82,108,128)",
-        "amber": "rgb(250,178,25)",
-        "cyan": "rgb(112,205,226)",
-        "green": "rgb(139,215,175)",
-        "red": "rgb(240,141,150)",
-        "violet": "rgb(194,173,242)",
-    },
-    "256": {
-        "base": "color(189)",
-        "muted": "color(145)",
-        "slate": "color(60)",
-        "amber": "color(214)",
-        "cyan": "color(80)",
-        "green": "color(115)",
-        "red": "color(210)",
-        "violet": "color(147)",
-    },
-    "standard": {
-        "base": "bright_white",
-        "muted": "white",
-        "slate": "bright_black",
-        "amber": "bright_yellow",
-        "cyan": "bright_cyan",
-        "green": "green",
-        "red": "red",
-        "violet": "magenta",
-    },
-}
-
-# Display mapping from a real state word to a state role, keyed by (field, exact raw value).
-# This is a display choice, not a count mapping and not a health verdict: the word is always
-# printed, and every value not listed here keeps the body role.
-STATE_ROLE: dict[tuple[str, str], str] = {
-    ("workerState", "running"): "state_running",
-    ("liveness", "alive"): "state_running",
-    ("liveness", "live"): "state_running",
-    ("workerState", "succeeded"): "state_settled",
-    ("dispatchStatus", "completed"): "state_settled",
-    ("workerState", "failed"): "state_failed",
-    ("dispatchStatus", "failed"): "state_failed",
-}
-FROZEN_ROLE = (
-    "state_frozen"  # a flags cell holding the frozen marker (fixture mode only)
-)
-
-_CACHE: dict[tuple[str, str], Style] = {}
-
-
-def style_for(role: str, depth: str | None) -> Style | None:
-    """The Rich style of ``role`` at ``depth``; ``None`` when there is no colour depth.
-
-    Styles are cached per ``(role, depth)`` so a style made for one depth in a process is never
-    reused for another (Rich caches the ANSI codes it renders on a ``Style``).
-    """
-    if role not in _PALETTE_OF:
-        raise KeyError(f"unknown role: {role!r}")
-    if depth is None:
-        return None
-    key = (role, depth)
-    style = _CACHE.get(key)
-    if style is None:
-        style = Style(color=_COLOURS[depth][_PALETTE_OF[role]], bold=role in _BOLD)
-        _CACHE[key] = style
-    return style
diff --git a/tests/observe/conftest.py b/tests/observe/conftest.py
index 8d9c62908..a75cae8f6 100644
--- a/tests/observe/conftest.py
+++ b/tests/observe/conftest.py
@@ -367,6 +367,45 @@ def question_rows(lines) -> list[str]:
     return [ln for ln in lines if QUESTION_ROW.match(ln)]
 
 
+# -- frame-aware helpers (the questions-on screens are framed from the frame phase on) ---------------------
+
+_TOP_ROW = re.compile(
+    r"^ ?[╭┏+][─━-] (.*?) [─━-]*[╮┓+]$"
+)  # corner, rule, title, rule, corner
+_BOTTOM_ROW = re.compile(r"^ ?[╰┗+][─━-]+[╯┛+]$")
+_BODY_ROW = re.compile(r"^ ?[│┃|] (.*) [│┃|]$")
+
+
+def unframe(line: str) -> str:
+    """``line`` without its margin, its left and right border glyph (rounded, heavy or ASCII)
+    and one padding cell on each side; trailing spaces are removed. A top or bottom border row
+    has no body and becomes the empty string (read its title with ``title_of``). A line that is
+    not framed is returned as it is."""
+    if _TOP_ROW.match(line) or _BOTTOM_ROW.match(line):
+        return ""
+    match = _BODY_ROW.match(line)
+    return match.group(1).rstrip() if match else line
+
+
+def title_of(lines) -> list[str]:
+    """The text inset in every top border of ``lines``, in order."""
+    return [m.group(1) for ln in lines if (m := _TOP_ROW.match(ln))]
+
+
+def unframed(lines) -> list[str]:
+    """``lines`` as the plain screen read before the frames: each top border becomes its title
+    row, each body row loses its borders, each bottom border is dropped, other lines stay."""
+    out: list[str] = []
+    for ln in lines:
+        if m := _TOP_ROW.match(ln):
+            out.append(m.group(1))
+        elif _BOTTOM_ROW.match(ln):
+            continue
+        else:
+            out.append(unframe(ln))
+    return out
+
+
 # -- styled-output helpers (the screen carries SGR from the colour phase on) ------------------------------
 
 _SGR = re.compile(r"\x1b\[([0-9;]*)m")
diff --git a/tests/observe/live_child.py b/tests/observe/live_child.py
deleted file mode 100644
index 7f040265e..000000000
--- a/tests/observe/live_child.py
+++ /dev/null
@@ -1,41 +0,0 @@
-"""Live-screen child: draws one questions screen through the real ``LiveScreen`` on a pty.
-
-Run only by ``test_live_screen_pty.py``. It reads the terminal size and the environment the way
-the command does (``detect_size``, ``resolve_policy``), draws once, prints ``LIVE_READY`` and
-waits for one line on stdin, then closes the screen so the alternate screen is left cleanly.
-"""
-
-from __future__ import annotations
-
-import os
-import sys
-from pathlib import Path
-
-sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
-
-from superclaude.cli.observe.commands import LiveScreen  # noqa: E402
-from superclaude.cli.observe.terminal import (  # noqa: E402
-    detect_size,
-    output_encoding,
-    resolve_policy,
-)
-from tests.observe.conftest import FakeClock  # noqa: E402
-from tests.observe.test_render import r3_rows, r3_screen  # noqa: E402
-
-
-def main() -> int:
-    width, height = detect_size()
-    policy = resolve_policy(os.environ, output_encoding(), {}, width, height)
-    rows = r3_rows([("w-001", "first?"), ("w-002", "second?"), ("w-003", "third?")])
-    _, view = r3_screen(FakeClock(), rows, 1, width, height)
-    screen = LiveScreen()
-    screen.draw(view, policy, None)
-    sys.stdout.write("LIVE_READY\n")
-    sys.stdout.flush()
-    sys.stdin.readline()
-    screen.close()
-    return 0
-
-
-if __name__ == "__main__":
-    raise SystemExit(main())
diff --git a/tests/observe/test_commands.py b/tests/observe/test_commands.py
index 8dcb6f7f9..f079b7840 100644
--- a/tests/observe/test_commands.py
+++ b/tests/observe/test_commands.py
@@ -608,6 +608,7 @@ from tests.observe.conftest import (  # noqa: E402
     make_question_rows,
     question_payload,
     routed_runner_responses,
+    title_of,
 )
 
 
@@ -691,7 +692,8 @@ def test_with_the_guard_open_and_a_width_the_screen_shows_the_panel(
     code, out = once(Options(once=True, run_id=QRUN, questions=True, width=116), deps)
     lines = out.splitlines()
     assert code == 0 and all(cell_len(l) <= 116 for l in lines)
-    assert any(l.startswith("COORDINATOR QUESTIONS") for l in lines)
+    # the list is a titled frame: the title is inset in its top border
+    assert any(t.startswith("COORDINATOR QUESTIONS") for t in title_of(lines))
     assert GAP_NOTICE not in lines
 
 
diff --git a/tests/observe/test_golden_contract.py b/tests/observe/test_golden_contract.py
index cccc13b55..e29a16f99 100644
--- a/tests/observe/test_golden_contract.py
+++ b/tests/observe/test_golden_contract.py
@@ -372,6 +372,8 @@ from tests.observe.conftest import (  # noqa: E402
     make_rows,
     question_rows,
     routed_runner_responses,
+    title_of,
+    unframed,
 )
 
 QUESTION_GOLDEN = (
@@ -429,8 +431,8 @@ def test_t55_the_success_sample_parses_to_its_two_questions_at_every_width(fake_
     for width in (160, 116, 80):
         lines = screen_lines(view, policy(width))
         assert all(cell_len(line) <= width for line in lines)
-        assert any(line.startswith("COORDINATOR QUESTIONS") for line in lines)
-        assert len(question_rows(lines)) == 2
+        assert any(t.startswith("COORDINATOR QUESTIONS") for t in title_of(lines))
+        assert len(question_rows(unframed(lines))) == 2
 
 
 def test_t55_the_missing_sample_fails_by_shape_then_by_no_active_terminal_and_keeps_questions(
diff --git a/tests/observe/test_height_budget.py b/tests/observe/test_height_budget.py
deleted file mode 100644
index 444a40047..000000000
--- a/tests/observe/test_height_budget.py
+++ /dev/null
@@ -1,26 +0,0 @@
-"""The questions-on screen never has more rows than the terminal (pins today's height budget).
-
-On ``Live(screen=True)`` rows past ``policy.height`` are dropped from the bottom, which are the
-footer keys and the ``shown x/y`` line, with no warning. Every phase that adds rows (frames, a
-count strip, a RETAIN CONTEXT pane) keeps this test green.
-"""
-
-from __future__ import annotations
-
-import pytest
-
-from tests.observe.test_render import WIDTHS, policy_for, r3_rows, r3_screen
-
-HEIGHTS = (24, 40, 44)
-
-
-@pytest.mark.parametrize("width", WIDTHS)
-@pytest.mark.parametrize("height", HEIGHTS)
-@pytest.mark.parametrize("count", (3, 20))
-def test_questions_on_screen_fits_the_height(fake_clock, width, height, count):
-    rows = r3_rows([("w-001", f"question {i}?") for i in range(count)])
-    lines, _ = r3_screen(fake_clock, rows, 0, width, height=height)
-    policy = policy_for(width, height=height)
-    assert len(lines) <= policy.height or policy.too_small, (
-        f"{len(lines)} rows at height {height}, width {width}"
-    )
diff --git a/tests/observe/test_live_screen_pty.py b/tests/observe/test_live_screen_pty.py
deleted file mode 100644
index 009a9137f..000000000
--- a/tests/observe/test_live_screen_pty.py
+++ /dev/null
@@ -1,93 +0,0 @@
-"""The real ``LiveScreen`` on a pty: alternate screen, colour depth, no blink, no mouse (Q5 live gate).
-
-``Console(file=StringIO)`` writes nothing under ``Live(screen=True)``, so the live path is only
-checked on a real pseudo-terminal. The child is ``live_child.py``.
-"""
-
-from __future__ import annotations
-
-import os
-import re
-import sys
-from pathlib import Path
-
-import pytest
-
-pexpect = pytest.importorskip("pexpect")
-pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="POSIX pty test")
-
-CHILD = Path(__file__).with_name("live_child.py")
-ROOT = Path(__file__).resolve().parents[2]
-SGR = re.compile(rb"\x1b\[([0-9;]*)m")
-MOUSE = (b"\x1b[?1000h", b"\x1b[?1002h", b"\x1b[?1003h", b"\x1b[?1006h")
-
-
-def run_child(env_extra: dict, rows: int = 40, cols: int = 160) -> bytes:
-    """Everything the live screen wrote to the terminal, from start to a clean exit."""
-    env = {
-        k: v
-        for k, v in os.environ.items()
-        if k not in ("COLUMNS", "LINES", "NO_COLOR", "COLORTERM", "TERM")
-    }
-    env["TERM"] = "xterm"
-    env.update(env_extra)
-    child = pexpect.spawn(
-        sys.executable,
-        [str(CHILD)],
-        env=env,
-        dimensions=(rows, cols),
-        encoding=None,
-        cwd=str(ROOT),
-        timeout=60,
-    )
-    child.expect(b"LIVE_READY")
-    before = child.before + b"LIVE_READY"
-    child.sendline(b"")
-    child.expect(pexpect.EOF)
-    return before + child.before
-
-
-def sgr_codes(data: bytes) -> list[int]:
-    """Every SGR code in ``data``; the arguments of extended colours (38 and 48) are skipped."""
-    codes: list[int] = []
-    for match in SGR.finditer(data):
-        params = [int(p) if p else 0 for p in match.group(1).split(b";")]
-        i = 0
-        while i < len(params):
-            if params[i] in (38, 48) and i + 1 < len(params):
-                i += 3 if params[i + 1] == 5 else 5
-                continue
-            codes.append(params[i])
-            i += 1
-    return codes
-
-
-def test_the_live_screen_uses_the_alternate_screen_and_no_mouse_or_blink():
-    out = run_child({})
-    assert b"\x1b[?1049h" in out and b"\x1b[?1049l" in out  # entered and left cleanly
-    assert not any(seq in out for seq in MOUSE)
-    assert not {5, 6} & set(sgr_codes(out))  # no blink
-
-
-def test_a_truecolor_terminal_gets_the_mockup_palette():
-    out = run_child({"COLORTERM": "truecolor"})
-    assert b"38;2;" in out
-
-
-def test_a_256_colour_terminal_gets_indexed_colours_only():
-    out = run_child({"TERM": "xterm-256color"})
-    assert b"38;5;" in out and b"38;2;" not in out
-
-
-def test_a_16_colour_terminal_gets_only_16_colour_codes():
-    out = run_child({})
-    codes = sgr_codes(out)
-    assert codes and b"38;2;" not in out and b"38;5;" not in out
-    assert all(c in (0, 1, 22) or 30 <= c <= 37 or 90 <= c <= 97 for c in codes)
-
-
-def test_no_color_writes_no_colour_or_weight_codes():
-    out = run_child({"NO_COLOR": "1", "COLORTERM": "truecolor"})
-    assert b"\x1b[?1049h" in out
-    # Measured: with NO_COLOR the console sets no style at all, so no SGR sequence is written.
-    assert sgr_codes(out) == []
diff --git a/tests/observe/test_question_cap.py b/tests/observe/test_question_cap.py
index cc504aa59..e858e113a 100644
--- a/tests/observe/test_question_cap.py
+++ b/tests/observe/test_question_cap.py
@@ -31,6 +31,8 @@ from tests.observe.conftest import (
     make_question_rows,
     make_rows,
     routed_runner_responses,
+    unframe,
+    unframed,
 )
 
 
@@ -74,8 +76,10 @@ def test_a_100_row_reply_sets_window_full_and_the_panel_says_so(fake_clock, argv
     assert result.question_state == "OK" and result.questions.window_full is True
     view, lines = screen(result, fake_clock)
     assert view.questions.window_full_text == QUESTIONS_WINDOW_FULL
-    assert "window full: older questions may be missing" in lines
-    flat = " ".join(" ".join(lines).split())
+    assert "window full: older questions may be missing" in [
+        unframe(ln) for ln in lines
+    ]
+    flat = " ".join(" ".join(unframed(lines)).split())
     assert QUESTIONS_DISCLOSURE in flat
     assert "bounded best effort; coverage unknown" in flat
     assert "seen, not resolved: 100+ (window full) |" in flat
@@ -118,7 +122,9 @@ def test_a_moved_window_keeps_the_dropped_questions_and_the_open_total_does_not_
         "seen, not resolved: 110+ (window full) |"
     )
     assert sum("no longer in source window" in line for line in lines) == 10
-    assert "window full: older questions may be missing" in lines
+    assert "window full: older questions may be missing" in [
+        unframe(ln) for ln in lines
+    ]
 
 
 def test_the_panel_never_prints_a_total_taken_from_result_count(fake_clock, argv_log):
diff --git a/tests/observe/test_render.py b/tests/observe/test_render.py
index 69b20ba72..34f762698 100644
--- a/tests/observe/test_render.py
+++ b/tests/observe/test_render.py
@@ -14,14 +14,29 @@ from rich.cells import cell_len
 import superclaude.cli.observe.render as render_module
 from superclaude.cli.observe.adapter import LiveSource
 from superclaude.cli.observe.collector import Collector, FixtureSource
-from superclaude.cli.observe.render import render, screen_lines
+from superclaude.cli.observe.render import render
+from superclaude.cli.observe.render import screen_lines as framed_screen_lines
 from superclaude.cli.observe.terminal import MIN_ROWS, make_console, resolve_policy
 from superclaude.cli.observe.view import GAP_NOTICE, Session, build_view
-from tests.observe.conftest import FakeDiscover, FakeRunner, make_envelope, make_rows
+from tests.observe.conftest import (
+    FakeDiscover,
+    FakeRunner,
+    make_envelope,
+    make_rows,
+    unframe,
+    unframed,
+)
 
 WIDTHS = (160, 116, 80)
 
 
+def screen_lines(view, policy, message=None):
+    """The screen with each frame read as before it existed (top border to its title row, body
+    rows without their borders, bottom borders dropped), for the checks of text and order.
+    The checks of frame shape and of height use ``framed_screen_lines``."""
+    return unframed(framed_screen_lines(view, policy, message))
+
+
 def policy_for(width, height=40, ascii=False, no_color=False):
     env = {"NO_COLOR": "1"} if no_color else {}
     return resolve_policy(env, "utf-8", {"ascii": ascii}, width, height)
@@ -473,7 +488,7 @@ def test_every_screen_line_fits_at_160_116_and_80_with_the_panel(
     )
     _, result = question_result(ok_message(rows), fake_clock)
     policy = policy_for(width, height=height)
-    lines = screen_lines(build_view(result, Session(), fake_clock), policy)
+    lines = framed_screen_lines(build_view(result, Session(), fake_clock), policy)
     assert all(cell_len(l) <= width for l in lines)
     assert len(lines) <= height or policy.too_small
     if height >= 24:
@@ -708,14 +723,16 @@ def test_decision_2_the_questions_win_on_a_short_terminal_the_ledger_is_squeezed
         ok_message(make_question_rows(8)), fake_clock, n_workers=30
     )
     view = build_view(result, Session(), fake_clock)
-    lines = screen_lines(view, policy_for(120, height=26))
+    framed = framed_screen_lines(view, policy_for(120, height=26))
+    lines = unframed(framed)
     assert len(question_rows(lines)) == 8  # every question is shown ...
     ledger_rows = [ln for ln in lines if " w-0" in ln]
-    # ... and the ledger keeps what is left: 4 rows, measured after the space diet (the title
-    # row carries the Run, the rule and "+N more" rows are gone); the questions still win
-    assert len(ledger_rows) == 4
-    assert any(re.search(r"shown 4/30$", ln) for ln in lines)
-    assert len(lines) <= 26
+    # ... and the ledger keeps what is left: 2 rows (4 before the frames; the list frame takes
+    # two rows out of the same budget). The owner's rule "the questions win on a short terminal"
+    # still holds: all 8 questions show and the ledger is squeezed, never the list.
+    assert len(ledger_rows) == 2
+    assert any(re.search(r"shown 2/30$", ln) for ln in lines)
+    assert len(framed) <= 26
 
 
 def test_decision_3_and_4_the_count_is_seen_not_resolved_and_a_full_window_reads_100_plus(
@@ -911,8 +928,10 @@ def r3_screen(
     ascii=False,
     no_color=False,
     workers=3,
+    raw=False,
 ):
-    """(lines, view) of a link-on questions screen with question ``selected`` chosen."""
+    """(lines, view) of a link-on questions screen with question ``selected`` chosen. The lines
+    are read without their frames unless ``raw`` is true (the checks of frame shape and height)."""
     worker = (0, json.dumps(make_envelope(make_rows(workers, 1), total=workers)))
     runner = FakeRunner([], [routed_runner_responses(worker, ok_message(rows))])
     result = Collector(
@@ -927,7 +946,8 @@ def r3_screen(
     )
     view = build_view(result, session, clock)
     policy = policy_for(width, height=height, ascii=ascii, no_color=no_color)
-    return screen_lines(view, policy), view
+    shown = framed_screen_lines if raw else screen_lines
+    return shown(view, policy), view
 
 
 @pytest.mark.parametrize("width", WIDTHS)
@@ -1152,14 +1172,27 @@ def test_reasons_are_said_once_in_the_title_and_not_on_every_row(fake_clock, wid
     plain = [strip_sgr(ln) for ln in lines]
     assert not any("reason unknown" in ln for ln in plain)
     assert sum("reasons: none in source" in ln for ln in plain) == 1
-    title = next(
-        i for i, ln in enumerate(plain) if ln.startswith("COORDINATOR QUESTIONS")
-    )
-    assert "reasons: none in source" in "".join(plain[title : title + 2])
+    rows_at = [i for i, ln in enumerate(plain) if question_rows([ln])]
+    note = next(i for i, ln in enumerate(plain) if "reasons: none in source" in ln)
+    assert note > max(rows_at)  # the note stands under the rows: the rows lead the pane
     assert len(question_rows(plain)) == 2
     assert "reason unknown" in record_text(view)  # the record keeps its wording
 
 
+@pytest.mark.parametrize("width", WIDTHS)
+def test_the_question_rows_lead_the_list_pane_and_the_run_id_is_in_its_title(
+    fake_clock, width
+):
+    rows = r3_rows([("w-001", "first?"), ("w-002", "second?")])
+    lines, view = r3_screen(fake_clock, rows, None, width, height=70, raw=True)
+    top = next(i for i, ln in enumerate(lines) if "COORDINATOR QUESTIONS" in ln)
+    assert (
+        view.questions.run_id in lines[top]
+    )  # one Run only: <id>, in the border title
+    first_body = unframe(lines[top + 1])
+    assert question_rows([first_body])  # the first row of the pane is a question row
+
+
 def test_a_row_with_a_reason_shows_it_and_the_title_note_goes(fake_clock):
     rows = r3_rows([("w-001", "first?"), ("w-002", "second?")])
     lines, view = r3_screen(fake_clock, rows, 0, 160, height=70)
@@ -1309,16 +1342,20 @@ def test_a_selected_question_is_one_bold_amber_line_and_the_others_have_parts(
     rows = r3_rows([("w-001", "first?"), ("w-002", "second?")])
     _, view = r3_screen(fake_clock, rows, 1, 160, height=60)
     lines = _compose(view, policy_for(160, height=60))
-    selected = next(ln for ln in lines if ln.plain.startswith("▸ "))
+    selected = next(ln for ln in lines if "▸ " in ln.plain)
     assert roles_at(selected, "second>") == {"selected"}
     assert roles_at(selected, "▸") == {"selected"}
     assert "reason unknown" not in selected.plain  # said once in the title note
     other = first_line(lines, "first?")
     assert roles_at(other, "first?") == {"body_bold"}
-    assert roles_at(other, other.plain.strip().split()[0]) == {"attention"}  # the age
-    title = first_line(lines, "COORDINATOR QUESTIONS")
-    assert roles_at(title, "COORDINATOR") == {"attention_title"}
-    assert roles_at(title, "reasons: none in source") == {"muted"}
+    assert roles_at(other, "1h") == {"attention"}  # the age
+    title = first_line(
+        lines, "COORDINATOR QUESTIONS"
+    )  # inset in the border of a round frame
+    assert roles_at(title, "COORDINATOR") == {"secondary"}
+    assert roles_at(title, "╭") == {"border_secondary"}
+    note = first_line(lines, "reasons: none in source")
+    assert roles_at(note, "reasons: none in source") == {"muted"}
 
 
 def test_absent_values_are_muted_and_state_words_follow_the_table(fake_clock):
@@ -1690,7 +1727,7 @@ def desk_after(fake_clock, mutate, width=116):
             (
                 i
                 for i, ln in enumerate(desk)
-                if ln.startswith("retention") or "bounded" in ln
+                if ln.startswith("worker-reported")  # the ledger title follows the desk
             ),
             len(desk),
         )
@@ -1791,7 +1828,9 @@ def test_questions_on_panes_are_framed_to_the_pane_width_and_ascii_has_no_questi
     fake_clock, width, ascii_mode
 ):
     rows = r3_rows([("w-001", "first?"), ("w-002", CENSUS_ASK)])
-    lines, _ = r3_screen(fake_clock, rows, 1, width, height=70, ascii=ascii_mode)
+    lines, _ = r3_screen(
+        fake_clock, rows, 1, width, height=70, ascii=ascii_mode, raw=True
+    )
     framed = frame_lines(lines)
     assert framed and all(cell_len(ln) == width - MARGIN for ln in framed)
     if ascii_mode:
@@ -1808,10 +1847,23 @@ def test_questions_on_panes_are_framed_to_the_pane_width_and_ascii_has_no_questi
         assert "COORDINATOR QUESTIONS" in tops[0] and "DECISION DESK" in tops[1]
 
 
+@pytest.mark.parametrize("width", WIDTHS)
+def test_the_text_inside_a_pane_is_at_most_width_minus_six_cells(fake_clock, width):
+    """Single column: inner width is width - 6 (154 at 160, 110 at 116, 74 at 80)."""
+    rows = r3_rows([("w-001", "x" * 300), ("w-002", PLAN_ASK)])
+    lines, _ = r3_screen(fake_clock, rows, 1, width, height=70, raw=True)
+    bodies = [unframe(ln) for ln in frame_lines(lines)]
+    assert bodies and all(cell_len(b) <= width - 6 for b in bodies)
+    assert (
+        max(cell_len(b) for b in bodies) >= width - 6 - 40
+    )  # long text uses the width
+    assert width - 6 == {160: 154, 116: 110, 80: 74}[width]
+
+
 @pytest.mark.parametrize("width", WIDTHS)
 def test_the_list_pane_is_heavy_when_no_desk_is_shown(fake_clock, width):
     rows = r3_rows([("w-001", "first?")])
-    lines, _ = r3_screen(fake_clock, rows, None, width, height=70)
+    lines, _ = r3_screen(fake_clock, rows, None, width, height=70, raw=True)
     tops = [ln for ln in lines if ln.startswith((" ╭", " ┏"))]
     assert len(tops) == 1 and tops[0].startswith(" ┏")
 
@@ -1825,7 +1877,7 @@ def test_framed_screens_never_exceed_the_height(
 ):
     rows = r3_rows([("w-001", "first?"), ("w-002", CENSUS_ASK), ("w-003", "third?")])
     lines, _ = r3_screen(
-        fake_clock, rows, selected, width, height=height, ascii=ascii_mode
+        fake_clock, rows, selected, width, height=height, ascii=ascii_mode, raw=True
     )
     assert len(lines) <= height
     assert all(cell_len(ln) <= width for ln in lines)
@@ -1838,9 +1890,11 @@ def test_the_hidden_desk_notice_sits_inside_the_list_frame(fake_clock):
     rows = r3_rows([("w-001", "first?"), ("w-002", "second?")])
     seen_inside = False
     for height in range(16, 40):
-        lines, _ = r3_screen(fake_clock, rows, 1, 116, height=height)
+        lines, _ = r3_screen(fake_clock, rows, 1, 116, height=height, raw=True)
         for ln in lines:
             if DESK_HIDDEN in ln and ln.startswith(" ┃ "):
                 assert ln.endswith(" ┃")  # a heavy list frame row
                 seen_inside = True
-    assert seen_inside  # the notice is reached at some height and sits in the frame body
+    assert (
+        seen_inside
+    )  # the notice is reached at some height and sits in the frame body
diff --git a/tests/observe/test_styled_capture.py b/tests/observe/test_styled_capture.py
deleted file mode 100644
index 51ca96474..000000000
--- a/tests/observe/test_styled_capture.py
+++ /dev/null
@@ -1,83 +0,0 @@
-"""The one-shot path can carry the screen's colour and weight; the capture is never export_text(styles=True)."""
-
-from __future__ import annotations
-
-import io
-
-import pytest
-
-from superclaude.cli.observe.commands import (
-    Options,
-    _screen_text,
-    _stdout_is_tty,
-    execute,
-)
-from superclaude.cli.observe.terminal import resolve_policy
-from tests.observe.conftest import strip_sgr
-from tests.observe.test_commands import deps_for
-from tests.observe.test_render import WIDTHS, fixture_view
-
-
-class _Tty(io.StringIO):
-    def isatty(self) -> bool:
-        return True
-
-
-def _policy(width, env=None, ascii=False):
-    return resolve_policy(env or {}, "utf-8", {"ascii": ascii}, width, 40)
-
-
-@pytest.mark.parametrize("width", WIDTHS)
-def test_a_styled_screen_has_escapes_and_the_same_text_as_the_plain_one(
-    fake_clock, width
-):
-    view = fixture_view("base", fake_clock)
-    policy = _policy(width)
-    styled = _screen_text(view, policy, styled=True)
-    plain = _screen_text(view, policy, styled=False)
-    assert "\x1b[" in styled
-    assert strip_sgr(styled) == plain and "\x1b" not in plain
-
-
-@pytest.mark.parametrize("width", WIDTHS)
-def test_no_color_gives_zero_escape_bytes_even_when_styled_is_asked_for(
-    fake_clock, width
-):
-    view = fixture_view("base", fake_clock)
-    out = _screen_text(view, _policy(width, {"NO_COLOR": "1"}), styled=True)
-    assert "\x1b" not in out
-
-
-@pytest.mark.parametrize("width", WIDTHS)
-def test_ascii_stays_ascii_with_colour_on(fake_clock, width):
-    view = fixture_view("long-identifiers", fake_clock)
-    out = _screen_text(view, _policy(width, ascii=True), styled=True)
-    assert "\x1b[" in out and out.isascii()
-
-
-def test_the_styled_capture_follows_the_colour_depth(fake_clock):
-    view = fixture_view("base", fake_clock)
-    truecolor = _screen_text(
-        view, _policy(160, {"COLORTERM": "truecolor"}), styled=True
-    )
-    standard = _screen_text(view, _policy(160), styled=True)
-    assert "38;2;" in truecolor and "38;2;" not in standard
-
-
-def test_a_piped_one_shot_stays_plain_and_a_terminal_one_is_styled(fake_clock):
-    options = Options(once=True, fixture="base", width=160)
-    piped = deps_for(fake_clock)  # a StringIO: not a terminal
-    assert execute(options, piped) == 0 and "\x1b" not in piped.stdout.getvalue()
-    tty = deps_for(fake_clock, stdout=_Tty())
-    assert execute(options, tty) == 0 and "\x1b[" in tty.stdout.getvalue()
-    quiet = deps_for(fake_clock, stdout=_Tty(), env={"NO_COLOR": "1"})
-    assert execute(options, quiet) == 0 and "\x1b" not in quiet.stdout.getvalue()
-    assert strip_sgr(tty.stdout.getvalue()) == piped.stdout.getvalue()
-
-
-def test_a_stream_without_isatty_counts_as_not_a_terminal(fake_clock):
-    class _Bare:
-        def write(self, text):
-            return len(text)
-
-    assert _stdout_is_tty(deps_for(fake_clock, stdout=_Bare())) is False
diff --git a/tests/observe/test_theme.py b/tests/observe/test_theme.py
deleted file mode 100644
index 8add9681d..000000000
--- a/tests/observe/test_theme.py
+++ /dev/null
@@ -1,95 +0,0 @@
-"""Colour roles: every role exists at every depth, the 16-colour floor keeps its roles apart."""
-
-from __future__ import annotations
-
-import pytest
-
-from superclaude.cli.observe import theme
-from superclaude.cli.observe.theme import (
-    FROZEN_ROLE,
-    ROLES,
-    STATE_ROLE,
-    style_for,
-)
-
-DEPTHS = ("standard", "256", "truecolor")
-# One role per palette colour, so eight distinct colours means eight distinct roles (RB-09).
-PALETTE_ROLES = (
-    "attention",  # amber
-    "identity",  # base
-    "secondary",  # slate
-    "muted",
-    "state_running",  # green
-    "state_settled",  # cyan
-    "state_failed",  # red
-    "state_frozen",  # violet
-)
-
-
-@pytest.mark.parametrize("depth", DEPTHS)
-def test_every_role_has_a_style_at_every_depth(depth):
-    for role in ROLES:
-        assert style_for(role, depth) is not None
-
-
-def test_no_depth_means_no_style():
-    assert all(style_for(role, None) is None for role in ROLES)
-
-
-def test_an_unknown_role_is_an_error_not_a_silent_default():
-    with pytest.raises(KeyError):
-        style_for("nonsense", "standard")
-
-
-def test_the_eight_palette_roles_keep_eight_distinct_colours_at_16_colours():
-    numbers = [style_for(role, "standard").color.number for role in PALETTE_ROLES]
-    assert len(set(numbers)) == 8
-
-
-def test_the_four_state_roles_have_four_different_codes_at_16_colours():
-    roles = ("state_running", "state_settled", "state_failed", "state_frozen")
-    codes = {style_for(role, "standard").color.number for role in roles}
-    assert len(codes) == 4
-
-
-def test_the_state_table_is_not_empty_and_names_the_minimum_keys():
-    required = [
-        ("workerState", "running"),
-        ("workerState", "succeeded"),
-        ("workerState", "failed"),
-        ("dispatchStatus", "completed"),
-        ("liveness", "alive"),
-    ]
-    assert all(key in STATE_ROLE for key in required)
-    assert FROZEN_ROLE == "state_frozen"
-    assert all(role in ROLES for role in (*STATE_ROLE.values(), FROZEN_ROLE))
-    # A word the table does not name keeps the body role: it is never classified.
-    assert ("workerState", "blocked") not in STATE_ROLE
-    assert ("terminalState", "released") not in STATE_ROLE
-
-
-def test_no_style_blinks_dims_or_reverses():
-    for depth in DEPTHS:
-        for role in ROLES:
-            style = style_for(role, depth)
-            assert not (style.blink or style.blink2 or style.dim or style.reverse)
-
-
-def test_styles_are_distinct_objects_per_depth_and_cached_per_depth():
-    standard = style_for("attention", "standard")
-    truecolor = style_for("attention", "truecolor")
-    assert standard is not truecolor and standard != truecolor
-    assert style_for("attention", "standard") is standard
-    assert truecolor.color.get_truecolor().hex == "#fab219"
-
-
-def test_the_theme_module_holds_no_terminal_facts():
-    text = open(theme.__file__, encoding="utf-8").read()
-    for literal in (
-        "Console(",
-        "NO_COLOR",
-        "COLUMNS",
-        "stdout.encoding",
-        "getpreferredencoding",
-    ):
-        assert literal not in text


Codegraph context: index_state=fresh checked_at=2026-11-18T04:42:32Z worktree_root=issue-606 worktree projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-606
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor: export.py (untouched) reads QuestionsPanel title, run_line, summary, state_lines, disclosure, counts_line, caveat_line, retention_line and QuestionLine qid, text, dispatch_id, link; View.header1 and header2.
New untracked files are not in the diff: read them in the worktree: .dev/issues/409/visual-parity/scores/p2/scores.json and the gate folders .dev/tasks/to-do/TASK-WF-redesignSpec-20261118-043319/artifacts/gates/p2/iter-1 and iter-2 (checks.json and the per-width scorecards are summarised in scores.json and notes.md). The two golden files are excluded from the diff for size: Read tests/observe/golden_questions_linkoff.json and tests/observe/golden_release1_surface.json when you need them.
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
