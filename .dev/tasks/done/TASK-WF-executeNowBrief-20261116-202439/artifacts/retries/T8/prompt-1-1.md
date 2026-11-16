67bc121890a07fa3adaf6fa0a7803f63948c1a54
Review one task for spec compliance.

Task brief: ## Task 8: Move the snapshot schema load and validation out of export.py into the test conftest (S2)

Edit `src/superclaude/cli/observe/export.py`: remove the `from importlib import resources` import (:14), `from jsonschema import Draft7Validator` (:18), `SCHEMA_PACKAGE` and `SCHEMA_FILE` (:24-25), and the `SCHEMA` load plus `Draft7Validator.check_schema` call (:29-34); keep `SCHEMA_VERSION` (:23, used at :195) and re-check that `resources` has no other use in the file. Edit `tests/observe/conftest.py`: define `SCHEMA` there (read `snapshot.schema.json` from the package `superclaude.cli.observe` with `importlib.resources`, parse it, and run `Draft7Validator.check_schema` on it). Remove `SCHEMA` from the `from superclaude.cli.observe.export import ...` lines: in `tests/observe/test_commands.py:34` the whole line goes (it imports only `SCHEMA`), and in `tests/observe/test_snapshot_schema.py:15` keep `snapshot_json`, which the file uses about eleven times. Add `SCHEMA` to the existing `from tests.observe.conftest import ...` line in each file (`tests/observe/test_commands.py:36`, `tests/observe/test_snapshot_schema.py:18`). In `tests/observe/test_snapshot_schema.py` (:52-72) remove only the assertion that now compares the file with a copy of itself (`assert json.loads(text) == SCHEMA`, :60), the read that exists only for it, and the `from importlib import resources` import (:8) if nothing else in the file uses it; keep `Draft7Validator.check_schema(SCHEMA)`, the draft-07 `$schema` check and the closed-object checks.

Acceptance criteria:
- `PKG/export.py` no longer imports `jsonschema` or `importlib.resources` and defines no `SCHEMA`; Grep shows `SCHEMA` is read only from `tests/observe/conftest.py` by the two test modules; ruff reports no unused import in either test module and `snapshot_json` is still imported in `tests/observe/test_snapshot_schema.py`.
- `tests/observe/test_snapshot_schema.py::test_the_schema_ships_in_the_package_is_draft_7_and_closed_on_the_producer_side` and every snapshot validation test still pass, and a snapshot written by `export.py` still validates against the schema.
- No test function is deleted: the passed count is unchanged and the gate passes.
Global constraints: 
- Shorthand. PKG is `src/superclaude/cli/observe/`. TESTS is `tests/observe/`. SPECDIR is `.dev/issues/409/bmad/spec-orca-observer/`. The debate's final list and its row text are copied into `./source.md`; each task below restates what it needs.
- Scope is these eleven rows only. No commit, no push, no pull request. Every other row of the debate (KEEP, owner decisions, low confidence) is out of scope.
- Never touch: the sanitizer (`PKG/sanitize.py` and its use), the argv allow-list and forbidden verbs in `PKG/adapter.py`, process-group kill and output caps, terminal restore on exit and signals, the rule that message bodies, payload and `to_handle` are never kept, snapshot redaction, the disclosure label `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost`, `QUESTION_GATE_TEXT` in `PKG/commands.py` (pinned by `TESTS/test_commands.py`), any DIRECTION-SELECTED line, and any file git does not track (for example `.dev/issues/409/handoff-mvp-brainstorm.md`).
- Line numbers in the tasks were read live on 2026-11-16 at HEAD f104ca51a and are leads only: re-grep every target right before editing, because other sessions share the worktree.
- Gate for every task: `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/observe -q` passes and `uv run ruff check src/superclaude/cli/observe tests/observe` is clean. The baseline is 694 passed; the passed count falls only by the test functions a task deliberately deletes, and the task states the number it expects and the number it got. UV only; never bare python or pip. A failing gate is reported as a finding and never loosened to pass.
- Edits touch only `src/`, `tests/`, `.dev/issues/409/` and this package's `./artifacts/`; nothing under `.claude/`.
- Whole-package checks, applied by the final review and not tasks of their own: Task 1 first saves `git status --short` to `./artifacts/baseline-status.txt`; at the end `git status --short` differs from that baseline only by the files these tasks name, `.dev/issues/409/` and this package; the full gate passes with the passed count equal to 694 minus the test cases the tasks removed (9 in Task 1 and 1 in Task 9, so 684, unless Task 6 had to remove an aggregate-only test); and `grep -rn "run-use" src/superclaude/cli/observe/` shows `run-use` only in the forbidden set in `PKG/adapter.py` and in the help text that says the observer never runs it.
- Names, not line numbers, wherever a check or a document points at code, because earlier tasks shift line numbers (for example `_question_refusal` in `PKG/commands.py`). A Grep check below means uses of the named symbol, not test function names that merely contain the word (`tests/observe/test_questions.py:50` and `tests/observe/test_view.py:174` keep such names).
- Labels. T5, T7, T8 and T9 in task titles are the debate's row names; the spec test ids in Task 12 are written "spec test T7", "T17", "T45" and "T50".
- Facts the debate found false in the earlier proposal, not to be repeated: the R1 test ranges were too wide, R3 must not drop the five parsed row fields, T9 keeps the `test_render.py` copy and deletes the `test_terminal.py` copy, T7 keeps the 32-character rule and the id rule, T8 keeps all 27 cases, D1 touches owner decisions 6 and 8 only.
Start sha: 67bc121890a07fa3adaf6fa0a7803f63948c1a54
Diff against the start snapshot: diff --git a/src/superclaude/cli/observe/export.py b/src/superclaude/cli/observe/export.py
index e35514d73..ab864542b 100644
--- a/src/superclaude/cli/observe/export.py
+++ b/src/superclaude/cli/observe/export.py
@@ -13,3 +13,2 @@ import os
 import tempfile
-from importlib import resources
 from pathlib import Path
@@ -17,4 +16,2 @@ from typing import Any
 
-from jsonschema import Draft7Validator
-
 from superclaude.cli.observe.sanitize import sanitize
@@ -23,4 +20,2 @@ from superclaude.cli.observe.view import ORDER_UNKNOWN_FLAG, UNKNOWN, RowView, V
 SCHEMA_VERSION = 1
-SCHEMA_PACKAGE = "superclaude.cli.observe"
-SCHEMA_FILE = "snapshot.schema.json"
 SNAPSHOT_NAME = "snapshot.json"
@@ -28,9 +23,2 @@ UNKNOWN_TEXT = "UNKNOWN"  # the snapshot spelling of a missing value
 
-SCHEMA: dict = json.loads(
-    resources.files(SCHEMA_PACKAGE).joinpath(SCHEMA_FILE).read_text(encoding="utf-8")
-)
-Draft7Validator.check_schema(
-    SCHEMA
-)  # a broken schema fails at import, not in the field
-
 # snapshot key (dotted for nesting) -> attribute of the typed row
diff --git a/tests/observe/conftest.py b/tests/observe/conftest.py
index ecf39a14b..43eb772d9 100644
--- a/tests/observe/conftest.py
+++ b/tests/observe/conftest.py
@@ -9,6 +9,9 @@ from __future__ import annotations
 import io
+import json
 import subprocess
 from datetime import datetime, timedelta, timezone
+from importlib import resources
 
 import pytest
+from jsonschema import Draft7Validator
 
@@ -21,2 +24,10 @@ QUESTION_BASE = ["orchestration", "check", "--all", "--types", "question"]
 
+# The snapshot schema as shipped in the package; a broken schema fails at collection.
+SCHEMA: dict = json.loads(
+    resources.files("superclaude.cli.observe")
+    .joinpath("snapshot.schema.json")
+    .read_text(encoding="utf-8")
+)
+Draft7Validator.check_schema(SCHEMA)
+
 
diff --git a/tests/observe/test_commands.py b/tests/observe/test_commands.py
index dcc3c7632..55f1daacf 100644
--- a/tests/observe/test_commands.py
+++ b/tests/observe/test_commands.py
@@ -33,5 +33,10 @@ from superclaude.cli.observe.commands import (
 )
-from superclaude.cli.observe.export import SCHEMA
 from superclaude.cli.observe.view import GAP_NOTICE, Key
-from tests.observe.conftest import FakeDiscover, FakeRunner, make_envelope, make_rows
+from tests.observe.conftest import (
+    SCHEMA,
+    FakeDiscover,
+    FakeRunner,
+    make_envelope,
+    make_rows,
+)
 
diff --git a/tests/observe/test_snapshot_schema.py b/tests/observe/test_snapshot_schema.py
index e560879fe..7c4acc6d1 100644
--- a/tests/observe/test_snapshot_schema.py
+++ b/tests/observe/test_snapshot_schema.py
@@ -7,3 +7,2 @@ import json
 import re
-from importlib import resources
 
@@ -14,6 +13,12 @@ from superclaude.cli.observe.adapter import LiveSource
 from superclaude.cli.observe.collector import Collector, FixtureSource
-from superclaude.cli.observe.export import SCHEMA, snapshot_json
+from superclaude.cli.observe.export import snapshot_json
 from superclaude.cli.observe.parse import VARIANTS, load_fixture
 from superclaude.cli.observe.view import Session, build_view
-from tests.observe.conftest import FakeDiscover, FakeRunner, make_envelope, make_rows
+from tests.observe.conftest import (
+    SCHEMA,
+    FakeDiscover,
+    FakeRunner,
+    make_envelope,
+    make_rows,
+)
 
@@ -54,8 +59,2 @@ def walk(value, path=()):
 def test_the_schema_ships_in_the_package_is_draft_7_and_closed_on_the_producer_side():
-    text = (
-        resources.files("superclaude.cli.observe")
-        .joinpath("snapshot.schema.json")
-        .read_text(encoding="utf-8")
-    )
-    assert json.loads(text) == SCHEMA
     Draft7Validator.check_schema(SCHEMA)
Evidence this task produced (machine output of the gate, file /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/artifacts/t8-gate.log):
== grep (each pattern expected to match nothing)
none: SCHEMA_PACKAGE|SCHEMA_FILE
none: export import .*SCHEMA\b
== pytest
.                                                                        [100%]

============================= 685 passed in 22.90s =============================
== ruff
All checks passed!
== export.py: jsonschema / importlib / SCHEMA uses (expect none besides SCHEMA_VERSION)
20:SCHEMA_VERSION = 1
183:        "schemaVersion": SCHEMA_VERSION,
== SCHEMA readers in tests
tests/observe/test_snapshot_schema.py:18:    SCHEMA,
tests/observe/test_snapshot_schema.py:25:VALIDATOR = Draft7Validator(SCHEMA)
tests/observe/test_snapshot_schema.py:60:    Draft7Validator.check_schema(SCHEMA)
tests/observe/test_snapshot_schema.py:63:        SCHEMA,
tests/observe/conftest.py:26:SCHEMA: dict = json.loads(
tests/observe/conftest.py:31:Draft7Validator.check_schema(SCHEMA)
tests/observe/test_commands.py:36:    SCHEMA,
tests/observe/test_commands.py:43:VALIDATOR = Draft7Validator(SCHEMA)
== snapshot_json import kept
14:from superclaude.cli.observe.export import snapshot_json
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
