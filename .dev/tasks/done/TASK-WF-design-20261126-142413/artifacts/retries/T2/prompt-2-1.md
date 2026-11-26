67868a89d6068cd2e9395f5895d60d1b5e9d21ae
Review one task for spec compliance.

Task brief: T2, "Task 2: Add the Phase A depth pins and the review-only pin to the route-table test module". The package folder is `.dev/tasks/to-do/TASK-WF-design-20261126-142413`; the plan's `./artifacts/` means that folder's `artifacts/`. Task text: "Edit only `tests/cli/reflect/test_remediation_route_table.py`. The module already defines `_ROOT`, `_REF` (the file `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md`), `_SKILL` (`src/superclaude/skills/sc-reflect-protocol/SKILL.md`) and `_CMD` (`src/superclaude/commands/reflect.md`) at lines 13 to 16, imports `re`, and has `_row` at line 21. Keep its five existing tests and its docstring unchanged. Add after `_row`: A constant `_ROW_PREFIX` equal to the text that starts the delegation-table row in `SKILL.md`: a pipe, a space, then the backticked name `sc:workflow-protocol`, then the text ` (skill, not agent)`. A helper `_region(text, start, end)` that asserts `text.count(start) == 1` and `text.count(end) == 1` (each message names the anchor), asserts `start` comes before `end`, and returns the text from `start` up to `end`. A helper `_depth_tokens(text)` that returns `re.findall(r"--depth\s+([^\s`]+)", text)`. A helper `_delegation_row()` that returns the single line of `_SKILL` that starts with `_ROW_PREFIX` and asserts that exactly one such line exists. Then add these five test functions, each assertion carrying a message that names its site. The five functions take no arguments (no `parametrize`) and read `_REF`, `_SKILL` and `_CMD` inside their bodies: `test_phase_a_depth_ref_region`: region is `_region(_REF, "### Phase A", "### Phase B")` (lines 28 to 76 today). Assert the token list is not empty, every token equals `standard`, the region contains `--depth standard --handoff none`, and the region does not contain `--strategy`. `test_phase_a_depth_skill_region`: region is `_region(_SKILL, "- **Phase A", "- **Phase B")` (lines 374 to 375 today). Assert the token list is not empty, every token equals `standard`, and `--strategy` is absent. `test_phase_a_depth_delegation_row`: row is `_delegation_row()` (line 624 today). Assert the token list is not empty, every token equals `standard`, and `--strategy` is absent. `test_no_placeholder_depth_on_sc_workflow_lines`: for each of `_REF`, `_SKILL`, `_CMD` and every line containing `sc:workflow`, no token from `_depth_tokens(line)` starts with `<`, `{` or `$`. `test_review_only_decision_stays_written_down`: assert `plan_depth`, `Plan depth` and `--plan-depth` occur in none of `_REF`, `_SKILL`, `_CMD`; assert the sentence `` `--depth deep` only sets the review depth `` (backticks included) occurs in `_SKILL` and in `_CMD`; assert the delegation row's last cell, computed as `row.rstrip().rstrip("|").rsplit("|", 1)[-1].strip()`, equals `None; surface the report path and recommend manual planning`, and that `--depth deep` is not in the row. The unattended continuation lines (`refs/remediation-handoff.md` line 73 and `SKILL.md` line 375) carry no `--depth` and lie inside the two Phase A regions, so these scans block an override there. Prose outside the three regions and outside `sc:workflow` lines is not covered; say so in a one-line comment above the new tests." Acceptance criteria: T2.AC1: "`uv run pytest tests/cli/reflect/test_remediation_route_table.py -v` on the unedited `SKILL.md` shows the five existing tests passing; `test_phase_a_depth_ref_region`, `test_phase_a_depth_skill_region` and `test_no_placeholder_depth_on_sc_workflow_lines` passing; and `test_phase_a_depth_delegation_row` and `test_review_only_decision_stays_written_down` failing, because line 624 yields the tokens standard and deep and its last cell ends with `or --depth deep`. The output is saved to `./artifacts/t2-red.log`." T2.AC2: "`uv run ruff check tests/cli/reflect/test_remediation_route_table.py` and `uv run ruff format --check tests/cli/reflect/test_remediation_route_table.py` exit 0."
Global constraints: Constraints of the plan: "- The owner decision of 26 Nov 2026 is final: `--depth deep` stays review-only. Phase A keeps calling `sc:workflow-protocol` with `--depth standard --handoff none` at every reflect depth. Add no `plan_depth`, no `Plan depth` prompt line, and no change to `src/superclaude/cli/reflect/runner.py`." "- The contract stays at 1.9.0. The key `remediation_task_path` stays in the section 9.1 block of `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (pinned by `tests/cli/reflect/test_shadow_skill_contract.py`) and in the allow-list in `src/superclaude/cli/reflect/panel_lint.py`. The eight YAML fixtures under `tests/cli/reflect/fixtures/` keep the key. Do not touch `refs/remediation-handoff.md`, `src/superclaude/commands/reflect.md` or either `HOW-WE-WORK.md`." "- Edit only `src/superclaude/`, `docs/developer-guide/session-memory.md` and `tests/cli/reflect/`. Never edit or stage `.claude/` or `.dev/issues/`. No plugin copy of the reflect skill exists, so `make sync-dev` then `make verify-sync` is the whole mirror step." "- The guard test `tests/cli/reflect/test_shadow_skill_contract.py::test_skill_changes_are_confined_to_the_allowed_sections` runs `git diff HEAD -U0` on `SKILL.md` and allows hunks only under sections 3.1, 4.3a, 5.4, 9.1, 9.2 and 17.6. The fallback edit is under section 7, so that one test is red between the `SKILL.md` edit and the commit. From the Task 7 `SKILL.md` edit until the commit, every pytest run this plan orders that collects `tests/cli/reflect/test_shadow_skill_contract.py` deselects exactly that node id with `--deselect tests/cli/reflect/test_shadow_skill_contract.py::test_skill_changes_are_confined_to_the_allowed_sections`. The Task 1 baseline and the complete run after the commit include it. Never widen its allow-list and never report a deselected run as the complete suite." "- The commit and the complete test run after it are not tasks. `/sc:implement` never commits. After this plan, the commit step of the story commits on the feature branch with a conventional-commit message (staging `src/`, `docs/`, `tests/` and `.dev/tasks`), and then the complete `uv run pytest` runs on the committed tree, guard included, and its failures are compared by node id with `./artifacts/baseline-pytest.md`. Until the commit and the complete run after it, report the final verification as blocked." "- Line length is 88 (`pyproject.toml`, `line-length = 88`). New or edited Python must pass `uv run ruff check src/ tests/`, and `uv run ruff format --check src/ tests/` must list no file that Task 1 did not list; fix formatting with `uv run ruff format <each file you edited>`; run `make format` only if Task 1's `uv run ruff format --check .` exited 0, and otherwise record the departure from spec step 5 as a necessary deviation in `./artifacts/t7-checks.md`." "- A collected test count is not a pass. Report observed pass and fail counts and node ids." "- Line citations into `SKILL.md` in the developer guide are re-checked with `sed -n` if the branch is rebased onto `origin/integration`."
Start sha: 67868a89d6068cd2e9395f5895d60d1b5e9d21ae
Diff against the start snapshot: One tracked file changed, `tests/cli/reflect/test_remediation_route_table.py` (74 insertions, no deletion); its diff follows. The task also created two untracked evidence files under `.dev/tasks/to-do/TASK-WF-design-20261126-142413/artifacts/`: `t2-red.log` (47 lines, the pytest `-v` output) and `t2-ruff.txt` (the ruff commands and exit codes); read them at those paths. The pytest result lines of `t2-red.log`: the five existing tests, `test_phase_a_depth_ref_region`, `test_phase_a_depth_skill_region` and `test_no_placeholder_depth_on_sc_workflow_lines` PASSED; `test_phase_a_depth_delegation_row` and `test_review_only_decision_stays_written_down` FAILED; summary `2 failed, 8 passed in 0.10s`. `t2-ruff.txt` shows `uv run ruff check` exit code 0 and `uv run ruff format --check` exit code 0 for the file. The file was formatted once with `uv run ruff format` (one file reformatted) before these runs.

diff --git a/tests/cli/reflect/test_remediation_route_table.py b/tests/cli/reflect/test_remediation_route_table.py
--- a/tests/cli/reflect/test_remediation_route_table.py
+++ b/tests/cli/reflect/test_remediation_route_table.py
@@ -22,6 +22,27 @@ def _row(prefix: str) -> str:
     return next(ln for ln in _REF.splitlines() if ln.startswith(prefix))
 
 
+_ROW_PREFIX = "| `sc:workflow-protocol` (skill, not agent)"
+
+
+def _region(text: str, start: str, end: str) -> str:
+    assert text.count(start) == 1, f"anchor {start!r} must occur exactly once"
+    assert text.count(end) == 1, f"anchor {end!r} must occur exactly once"
+    first, last = text.index(start), text.index(end)
+    assert first < last, f"anchor {start!r} must come before {end!r}"
+    return text[first:last]
+
+
+def _depth_tokens(text: str) -> list[str]:
+    return re.findall(r"--depth\s+([^\s`]+)", text)
+
+
+def _delegation_row() -> str:
+    rows = [ln for ln in _SKILL.splitlines() if ln.startswith(_ROW_PREFIX)]
+    assert len(rows) == 1, f"expected one delegation row, found {len(rows)}"
+    return rows[0]
+
+
 def test_route_table_pins_the_single_plan_route():
     assert "Route selection" in _REF
     plan = _row("| `--remediate` (any depth)")
@@ -56,3 +77,56 @@ def test_handoff_implement_only_appears_as_a_prohibition():
 
 def test_legacy_grammar_still_documented():
     assert "--type task --analyze" in _CMD and "--type task --validate" in _CMD
+
+
+# Not covered: prose outside the three Phase A sites and outside `sc:workflow` lines.
+def test_phase_a_depth_ref_region():
+    region = _region(_REF, "### Phase A", "### Phase B")
+    tokens = _depth_tokens(region)
+    assert tokens, "ref Phase A region: no --depth token (a deleted flag cannot pass)"
+    assert all(t == "standard" for t in tokens), f"ref Phase A region: {tokens}"
+    assert "--depth standard --handoff none" in region, "ref Phase A region: call text"
+    assert "--strategy" not in region, "ref Phase A region: --strategy must be absent"
+
+
+def test_phase_a_depth_skill_region():
+    region = _region(_SKILL, "- **Phase A", "- **Phase B")
+    tokens = _depth_tokens(region)
+    assert tokens, (
+        "SKILL.md Phase A bullet: no --depth token (a deleted flag cannot pass)"
+    )
+    assert all(t == "standard" for t in tokens), f"SKILL.md Phase A bullet: {tokens}"
+    assert "--strategy" not in region, "SKILL.md Phase A bullet: --strategy present"
+
+
+def test_phase_a_depth_delegation_row():
+    row = _delegation_row()
+    tokens = _depth_tokens(row)
+    assert tokens, (
+        "SKILL.md delegation row: no --depth token (a deleted flag cannot pass)"
+    )
+    assert all(t == "standard" for t in tokens), f"SKILL.md delegation row: {tokens}"
+    assert "--strategy" not in row, "SKILL.md delegation row: --strategy present"
+
+
+def test_no_placeholder_depth_on_sc_workflow_lines():
+    for name, text in (("ref", _REF), ("skill", _SKILL), ("command", _CMD)):
+        for ln in text.splitlines():
+            if "sc:workflow" not in ln:
+                continue
+            for token in _depth_tokens(ln):
+                assert not token.startswith(("<", "{", "$")), f"{name}: {ln}"
+
+
+def test_review_only_decision_stays_written_down():
+    for name, text in (("ref", _REF), ("skill", _SKILL), ("command", _CMD)):
+        for banned in ("plan_depth", "Plan depth", "--plan-depth"):
+            assert banned not in text, f"{name}: {banned} must not appear"
+    sentence = "`--depth deep` only sets the review depth"
+    assert sentence in _SKILL, "SKILL.md: the review-only sentence is missing"
+    assert sentence in _CMD, "reflect.md: the review-only sentence is missing"
+    row = _delegation_row()
+    last_cell = row.rstrip().rstrip("|").rsplit("|", 1)[-1].strip()
+    expected = "None; surface the report path and recommend manual planning"
+    assert last_cell == expected, f"SKILL.md delegation row last cell: {last_cell!r}"
+    assert "--depth deep" not in row, "SKILL.md delegation row: --depth deep present"
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
