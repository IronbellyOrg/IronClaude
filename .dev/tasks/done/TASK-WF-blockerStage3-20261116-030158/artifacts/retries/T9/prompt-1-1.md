828ddc7fb1b92304db6e57bad9bd490d7fa1bb8e
Review one task for spec compliance.

Task brief: Task 9 of the plan .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md (AC ids T9.AC1 to T9.AC3 in source order).
## Task 9: Add the reverse scan for the old sentence

Depends on: Task 3, Task 4, Task 5, Task 6

Create `tests/skills/test_review_old_rule_scan.py`. The scan walks every `*.md` file under `src/superclaude` and `plugins/superclaude` from the directory tree (not from `git ls-files`, so an unstaged file is scanned too; nothing there is edited) and fails when a file holds the old sentence that followed the opening of S1: "Blocking is a real defect: wrong behaviour, a false claim, a missing required deliverable, or a security or data-loss risk" (whitespace-collapsed). The opening sentence "Grade every review finding as blocking or minor" stays in the new S1 (`test_review_severity_rule.py` requires it), so the scan must not match it. There is no allow-list, no scale map and no `exempt-by-retirement` row: at the time of this task the old sentence is in no file outside the ten tuple files and `pragmatic.md` (checked by `grep -rlF` over `src` and `plugins`), and Tasks 2 and 3 removed it from those eleven. Code files under `src/superclaude/cli/` are not scanned. The scan does not match the merge-rule phrases (`highest severity`, `more severe rating`, `higher severity`); merge-rule coverage rests on the greps of Tasks 4, 5 and 6.

Acceptance criteria:
- `uv run pytest tests/skills/test_review_old_rule_scan.py -v` passes on the current tree after Tasks 3 to 6.
- A temporary-tree test where a Markdown file holds the old sentence fails the scan, and one where a Python file under `cli/` holds it passes.
- A temporary-tree test where a file holds only the opening sentence "Grade every review finding as blocking or minor" passes the scan.

Global constraints:
## Constraints

- Spec and cuts: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), revert triggers (RT1 to RT8) and owner decisions (OD1 to OD17) refer to the spec. The cuts that shaped this plan are in `cuts-debate/final-cuts.md` in PF (rows C1 to C14, the S3 table of its section (b), the cross-package facts of its section (c)); where that file and the spec disagree about scope, the cuts file wins. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger `stage-requests/README.md` in PF), found by that folder name in the to-do or done subfolder of the repository task folder. The stage 0 package is `TASK-WF-blockerStage0-20261116-021044` and the stage 1 package `TASK-WF-blockerStage1-20261116-030154`. The stage 2 package is withdrawn: its one survivor, the `/sc:implement` print, is task 2 of the stage 1 package.
- One package, one stage. This is stage 3 of the packages that remain (stage 0, stage 1, this one, stage 4). It changes the live review rule. Entry check, read from files and not from memory: the stage 0 package's `./artifacts/stage0c-regrade.md` exists; the stage 1 package is done (it is in the done subfolder of the repository task folder, or it is in the to-do subfolder with a `complete` line for every task in its `progress.md` and a latest `FINAL:` line that reads `FINAL: pass`); the stage 0 errata task has reworded the spec's RT1 row to read "any real blocker found in a Medium list" (`grep -c -F "any real blocker found in a Medium list"` over the spec prints 1 or more; Task 10 quotes it); the stage 3 row of `stage-requests/README.md` in PF holds the owner's go with a date (the go is a chat message recorded there by the session that received it; no hash and no line ruling are part of it). Task 1 runs this check before it creates any file under `src/` or `tests/`, and Task 2 runs it again before the first rule-file edit. A failed check stops the task before any edit and halts the run for the owner. While the check fails, no fix pass, repair, retry or adviser step edits a file under `src/`, `tests/` or `plugins/`, and the acceptance lines of that task that describe the edit do not apply. No task edits the ledger row. Stage 4 starts only after the owner has read the first five runs' Medium lists after the switch and RT1 did not trip (the stage 3 note says how), and the owner's go in chat.
- Limit of what this package shows. The stage 0 regrade is a lower bound: it regrades findings that were already supplied and cannot measure whether a reviewer would have found a defect. The stage 0 result, as its control test supports it, is only that the new text does not change grades on a table already filed as blocking (310 of 318 stay blocking under both texts, 82 of 82 panel blockers kept); both arms carried the old rule through the same hook, so no task here and no sentence of the Task 10 note cites that regrade as evidence that the new text works. No seeded-defect experiment is run here (the earlier one was confounded: both arms carried the old output style through the SubagentStart hook). What covers discovery is RT1 (spec section 13.2) read by the owner on the first five runs' Medium lists and one small planted-defect check run as part of the live RT1 audit after the switch; both go into the Task 10 note and neither is a build task.
- Owner decisions use the spec's recommendations unless the owner changes them, and none of them is converted into an owner answer here: OD1 no new skill folder, the S1 to S5 bullets of `pragmatic.md` are the one source; OD2 the Medium offer once per run plus at any escalation halt; OD9 reviewer-named consumer; OD11 replace label-max merging, staged (this stage the three agents; the rest is stage 4); OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD16 option (b) for Rule 6 of `rf-qa-qualitative.md`. OD3 (finding text leaving the machine) is open and no task depends on its answer; OD4 stands (no classifier in version 1).
- Retired carriers are not edited. The owner is retiring `/sc:task` and the task-builder: no task here edits `src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/` or `src/superclaude/agents/rf-task-builder.md`. Tests that exist only to pin those files are not re-pinned here; where one test pins both a retired and an active carrier, only the active carrier's part is re-pinned.
- Follow-up list. The list of minors is the reviewers' own `follow-up candidates` section plus each task's `notes.md`; no list file, codec, sweep or registry is built. The stage 1 package prints that list at the end of `/sc:implement` (one paragraph titled "Follow-up print (record and print only).", command `superclaude review safety-scan`). This package edits no `sc-implement-protocol` file, no plugin file and no `refs/qa.md`. The once-per-run offer question stays with the top-level session through the output style (the Medium rule of `pragmatic.md`, changed from per loop to per run in Task 2), so no command gains a question.
- Plugin surface. IronClaude is installed from the Coder template or from a clone plus `superclaude install`, not as a plugin, so this package edits nothing under `plugins/` and creates no plugin mirror, parity test or plugin registry row. `src/superclaude/commands/spec-panel.md` and its plugin twin keep their "once per loop" wording, pinned by `tests/skills/test_review_severity_mapping.py`, `tests/skills/test_review_loop_extension.py` and `tests/skills/test_spec_panel_review_loop.py`; that wording moves in stage 4.
- Not built here: no classifier (`superclaude review classify` does not exist), no follow-up list file or `follow-ups` command group, no `sc-review-severity` skill folder, scale map, carrier registry, doctor check or registry drift test, no seeded-recall run, hash-bound owner ruling, shadow stage or baseline file, no Jev or other external judge call, no change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), to `src/superclaude/cli/review/ledger.py` or `review-ledger/1`, to the own-scale primitives of spec section 9.3, to code-assigned severity in `src/superclaude/cli/**/*.py`, to the cap of 2 fix cycles, or to the 35 percent target. Stage 4 edits the doubt wording and the merge text of the templates and rule prompts; this package only copies the S1 to S3 and S5 bullets into the ten tuple files (Task 3).
- Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N").
- `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev` (it copies skills, agents, commands, hooks and templates; it does not copy `output-styles/`, `core/` or `rules/`). The installed `~/.claude/output-styles/pragmatic.md` therefore changes only at a refresh (Task 10 says how). Staging anything under the project `.claude/` folder is forbidden (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
- Kept mechanical gates (fixed FAIL triggers that stay as named gates) are recorded in the editing task's own `./artifacts/kept-mechanical-gates.md`, one bullet per gate: path relative to `src/superclaude/`, the gate's quoted words, the condition it maps to (the Missing condition of the digest), the reason. No `refs/scale-map.md` exists and none is created.
- Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
- Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says it is left out of staging. Staging is not committing.

Start sha: 828ddc7fb1b92304db6e57bad9bd490d7fa1bb8e

Diff against the start snapshot:
```diff
diff --git a/tests/skills/test_review_old_rule_scan.py b/tests/skills/test_review_old_rule_scan.py
new file mode 100644
index 000000000..74d9f5edf
--- /dev/null
+++ b/tests/skills/test_review_old_rule_scan.py
@@ -0,0 +1,75 @@
+"""Reverse scan: the old definition of "blocking" must appear in no Markdown file.
+
+The old sentence followed the opening of the review severity rule's first bullet
+("Grade every review finding as blocking or minor."). The opening stays in the new
+bullet, so the scan matches only the old sentence that came after it. The scan walks
+the directory tree, not `git ls-files`, so an unstaged file is scanned too. It reads
+only `*.md` files, so Python code under `src/superclaude/cli/` is never matched.
+"""
+
+from __future__ import annotations
+
+from pathlib import Path
+
+_REPO = Path(__file__).resolve().parents[2]
+_ROOTS = ("src/superclaude", "plugins/superclaude")
+
+OLD_SENTENCE = (
+    "Blocking is a real defect: wrong behaviour, a false claim, a missing "
+    "required deliverable, or a security or data-loss risk"
+)
+
+
+def _flat(text: str) -> str:
+    return " ".join(text.split())
+
+
+def files_with_old_sentence(base: Path, roots=_ROOTS) -> list[str]:
+    """Repo-relative paths of Markdown files under the roots that hold the old sentence."""
+    hits: list[str] = []
+    for root in roots:
+        folder = base / root
+        if not folder.is_dir():
+            continue
+        for path in sorted(folder.rglob("*.md")):
+            try:
+                text = path.read_text(encoding="utf-8")
+            except (OSError, UnicodeDecodeError):
+                continue
+            if OLD_SENTENCE in _flat(text):
+                hits.append(str(path.relative_to(base)))
+    return hits
+
+
+def test_the_old_sentence_is_in_no_markdown_file():
+    assert files_with_old_sentence(_REPO) == []
+
+
+def test_a_markdown_file_holding_the_old_sentence_fails_the_scan(tmp_path):
+    folder = tmp_path / "src/superclaude/agents"
+    folder.mkdir(parents=True)
+    (folder / "x.md").write_text(
+        "- Grade every review finding as blocking or minor.\n"
+        "  Blocking is a real defect: wrong behaviour, a false claim,\n"
+        "  a missing required deliverable, or a security or data-loss risk.\n",
+        encoding="utf-8",
+    )
+    assert files_with_old_sentence(tmp_path) == ["src/superclaude/agents/x.md"]
+
+
+def test_a_python_file_under_cli_holding_the_old_sentence_passes(tmp_path):
+    folder = tmp_path / "src/superclaude/cli"
+    folder.mkdir(parents=True)
+    (folder / "x.py").write_text(f'TEXT = "{OLD_SENTENCE}"\n', encoding="utf-8")
+    assert files_with_old_sentence(tmp_path) == []
+
+
+def test_a_file_with_only_the_opening_sentence_passes(tmp_path):
+    folder = tmp_path / "plugins/superclaude/skills"
+    folder.mkdir(parents=True)
+    (folder / "y.md").write_text(
+        "- Grade every review finding as blocking or minor. Grade each finding "
+        "by what changes if the flawed text is corrected.\n",
+        encoding="utf-8",
+    )
+    assert files_with_old_sentence(tmp_path) == []
diff --git a/.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/t9-pytest.log b/.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/t9-pytest.log
new file mode 100644
index 000000000..8aafbec94
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/t9-pytest.log
@@ -0,0 +1,14 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.venv/bin/python
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collecting ... collected 4 items
+
+tests/skills/test_review_old_rule_scan.py::test_the_old_sentence_is_in_no_markdown_file PASSED [ 25%]
+tests/skills/test_review_old_rule_scan.py::test_a_markdown_file_holding_the_old_sentence_fails_the_scan PASSED [ 50%]
+tests/skills/test_review_old_rule_scan.py::test_a_python_file_under_cli_holding_the_old_sentence_passes PASSED [ 75%]
+tests/skills/test_review_old_rule_scan.py::test_a_file_with_only_the_opening_sentence_passes PASSED [100%]
+
+============================== 4 passed in 0.12s ===============================
```

Codegraph context
index_state: fresh
checked_at: 2026-11-17T00:49:50Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
projectPath: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: none; a new test file only; it scans Markdown under src/superclaude and plugins/superclaude.

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
