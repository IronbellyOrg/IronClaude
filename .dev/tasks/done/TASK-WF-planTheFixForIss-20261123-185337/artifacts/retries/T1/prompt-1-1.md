f57516e683238103f800bea7787078f9b4358145
Review one task for spec compliance.

Task brief:  Add missing-command and complete-handoff regression checks

Use tests/swarm/test_bundled_lenses.py for a focused refactor-find availability check and tests/swarm/test_commands_run.py for a real CLI stub-transport handoff regression. Reuse the existing LENSES import, _runnable_spec and _write_spec helpers where applicable, and the pattern in test_run_cmd_stub_transport_dispatches_workers_not_noop. Read src/superclaude/cli/swarm/lenses/refactor_find.py, the run_cmd recommendation block in src/superclaude/cli/swarm/commands.py, and src/superclaude/commands/adversarial.md before authoring assertions. Do not change production code in this task.

Assert that the command token emitted for default refactor-find resolves to an actual packaged src/superclaude/commands/<name>.md file; a separately installed or differently namespaced plugin is not a substitute. Assert the full expected /sc:adversarial --compare form, parse its one comma-separated file-list argument, and compare that list to the successful workers' actual final_path values from the generated return-contract.yaml. Check readable file existence and input count, not merely that the template contains text or that the command name looks plausible. Run the generated CLI through the public swarm_group entry point with --transport stub, rather than mocking its reducer or constructing the expected contract directly. Standard-library parsing and existing YAML/test dependencies suffice.

Acceptance criteria:
T1.AC1: The new availability regression fails on the current source because /sc:code-review has no packaged command. The complete-handoff regression also fails for the current emitted instruction or its invalid argument list. Capture assertion failures, invoked test selectors and exit statuses in ./artifacts/regression-before.txt; an import error, bad fixture or proxy/environment failure does not count as reproducing the bug.
T1.AC2: The CLI check uses a target clearing the existing 50-non-whitespace-byte floor, writes reports under pytest's temporary output directory, and checks actual generated output_files and recommended_next_command. It invokes no network/model endpoint and no suggested downstream command.
T1.AC3: This task is complete when the new tests are correctly installed and the expected product-defect failures are observed, not when production is already green. Record those intentional failures explicitly; do not weaken assertions to make them pass. Existing unrelated baseline tests remain unchanged.
Global constraints: 
- This package is a plan only. Generating it does not authorize implementation. Execute only after the person approves execution. Do not commit, push, open a pull request, post an issue comment or launch paid/model-backed reviews.
- Limit production edits to src/superclaude/cli/swarm/lenses/refactor_find.py and the fresh-run recommendation-building block of run_cmd in src/superclaude/cli/swarm/commands.py. Use existing test files and update only the matching current documentation and wizard guidance named in Task 4 (MR-B1).
- The extra existing-review placeholder is not a separate issue to fix everywhere. Adjust refactor-find's bundled handoff only as required by the chosen consumer. Leave every other lens's recommendation, shared reducer, resume behavior, normalization, reviewer output content and success-status policy unchanged.
- Preserve refactor-find's experimental status, suspect=False, worker defaults, and absence of automatic downstream execution. Preserve explicit caller-provided templates and substitutions; do not replace custom instructions or silently validate/rewrite caller-owned inputs under this change.
- The replacement compares and combines reports, not application source. Never add a new command solely to preserve the stale recommendation. The supported command is /sc:adversarial --compare with a comma-separated list of 2-10 existing readable files, per src/superclaude/commands/adversarial.md and the active sc-adversarial-protocol skill.
- No credentials in files or logs; use environment references only. All Python/test operations use UV. Network-free stub reviewer transport is sufficient; never run the downstream adversarial skill or a model-backed swarm to satisfy these tasks.
- Diagnosis is evidence, not repaired-state acceptance. The previous diagnosis reproduced the stale instruction, but has no fix-applied positive witness. Do not relabel that historical report or clear its blocker by assertion. Task 3 must supply new observed red-to-green regression results and actual repaired CLI output.
- Keep task-owned evidence under ./artifacts/ using package-relative links. Keep intermediate evidence. Stage .dev/tasks, including this package and its artifacts, as project policy requires; staging is not a commit. Do not stage generated .claude mirrors. Final independent whole-plan review and archiving belong to the executor, not a separate task here.


Start sha: f57516e683238103f800bea7787078f9b4358145
Diff against the start snapshot: diff --git a/tests/swarm/test_bundled_lenses.py b/tests/swarm/test_bundled_lenses.py
index 065fb7a44..9d7b5c4d5 100644
--- a/tests/swarm/test_bundled_lenses.py
+++ b/tests/swarm/test_bundled_lenses.py
@@ -30,6 +30,8 @@ authoring.
 from __future__ import annotations
 
 import importlib
+import shlex
+from pathlib import Path
 
 import pytest
 
@@ -138,6 +140,17 @@ def test_bare_review_field_guards() -> None:
     assert "{suspect_files}" in lens.recommended_next_command_template
 
 
+def test_refactor_find_followup_is_packaged() -> None:
+    """The default follow-up must resolve to a shipped command, not a plugin."""
+    tokens = shlex.split(LENSES["refactor-find"].recommended_next_command_template)
+    command_name = tokens[0].removeprefix("/sc:")
+    commands_dir = Path(__file__).resolve().parents[2] / "src/superclaude/commands"
+    command_file = commands_dir / f"{command_name}.md"
+    assert command_file.is_file(), f"Unpackaged follow-up: {tokens[0]}"
+    assert tokens == ["/sc:adversarial", "--compare", "{compare_files}"]
+    assert "--compare" in command_file.read_text(encoding="utf-8")
+
+
 def test_edge_case_hunt_workers_is_four() -> None:
     assert LENSES["edge-case-hunt"].default_workers == 4
 
diff --git a/tests/swarm/test_commands_run.py b/tests/swarm/test_commands_run.py
index 70bf51ef2..07d1bad8d 100644
--- a/tests/swarm/test_commands_run.py
+++ b/tests/swarm/test_commands_run.py
@@ -31,10 +31,12 @@ depend on schema-test internals.
 from __future__ import annotations
 
 import json
+import shlex
 from pathlib import Path
 from typing import Any
 
 import pytest
+import yaml
 from click.testing import CliRunner
 
 from superclaude.cli.swarm import swarm_group
@@ -499,6 +501,40 @@ def test_dispatch_wave1_with_transport_calls_send_per_worker() -> None:
     assert [r.index for r in results] == [0, 1, 2]
 
 
+def test_refactor_find_default_handoff(tmp_path: Path) -> None:
+    """Exercise real dispatch through emission, then check the complete suggestion."""
+    spec = _runnable_spec(tmp_path)
+    output = Path(spec["output"]["dir"])
+    result = CliRunner().invoke(
+        swarm_group,
+        [
+            "run",
+            "--lens",
+            "refactor-find",
+            "--transport",
+            "stub",
+            "--target",
+            spec["target"]["path"],
+            "--output",
+            str(output),
+        ],
+    )
+    assert result.exit_code == EXIT_OK, result.output
+    contract = yaml.safe_load((output / "return-contract.yaml").read_text())
+    reports = [
+        worker["final_path"]
+        for worker in contract["output_files"]
+        if worker["status"] == "success"
+    ]
+    assert len(reports) == 3
+    assert all(Path(path).is_file() and Path(path).read_text() for path in reports)
+    tokens = shlex.split(contract["recommended_next_command"])
+    assert tokens[:2] == ["/sc:adversarial", "--compare"]
+    assert len(tokens) == 3
+    assert tokens[2].split(",") == reports
+    assert 2 <= len(reports) <= 10
+
+
 # ---------------------------------------------------------------------------
 # F-P3-1 regression -- real stub dispatch is NOT a no-op
 # ---------------------------------------------------------------------------

Required negative witness: /home/coder/workspaces/worktrees/IronClaude/issue-501-refactor-handoff/.dev/tasks/to-do/TASK-WF-planTheFixForIss-20261123-185337/artifacts/regression-before.txt

Codegraph context
index_state: fresh
checked_at: 2026-11-23T20:00:21Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-501-refactor-handoff
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-501-refactor-handoff
call codegraph only when index_state: fresh, never to widen scope
Q2b: Grep/Read confirms the two new test functions have no production callers. Public swarm_group dispatch registers run_cmd; existing tests remain unchanged.

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
