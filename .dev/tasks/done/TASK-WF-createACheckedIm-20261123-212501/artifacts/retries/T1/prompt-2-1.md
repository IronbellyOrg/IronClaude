start=fdff62848f3268733cedac6bf940bf08f30663b8
Review one task for spec compliance.

Task brief: ## Task 1: Add the public validate-lenses help regression

Add a new validate-lenses help regression to `tests/swarm/test_cli_registration.py`, using its existing `CliRunner` and root `main` imports to invoke `main` with `swarm validate-lenses --help`. Name the new test clearly for the custom-prompt help contract. Read the historical report's Evidence, Proposed Fix and Next Steps sections, `doc-context.md`, `runtime-entrypoint.md` and `validate-lenses-help.txt` in the transferred diagnostic package. Confirm the current `validate_lenses_cmd` help-producing docstring in `src/superclaude/cli/swarm/commands.py` and registration in `src/superclaude/cli/swarm/__init__.py` before authoring assertions. Ground expected wording in `docs/swarm/command-reference.md` (the note explaining the directory is not a run flag), `_apply_custom_prompt_dir` in `src/superclaude/cli/swarm/preflight.py`, and `_custom_prompt_dir_lens_failures` in `src/superclaude/cli/swarm/schema.py`.

Acceptance criteria:
- T1.AC1: The new test invokes the root public command, requires exit 0, rejects the exact token `--custom-prompt-dir`, and positively requires JobSpec, `custom_prompt_dir` and custom-lens guidance. Normalize whitespace rather than pinning Click's wrapping or an entire help transcript.
- T1.AC2: Before either product edit, run the new test through `uv run pytest` with its concrete node id. Preserve command, checkout/module origin, timestamp, output and observed nonzero status in `./artifacts/validate-help-red.txt`. A missing import, collection error or unrelated failure does not count as reproducing the bug.
- T1.AC3: The observed failure is caused by the stale help contract in `validate_lenses_cmd`, not a mocked helper. If the current public help already satisfies the regression or the expected mismatch cannot be reproduced, stop implementation and report the conflict rather than applying a speculative wording change.
- T1.AC4: Only the regression test is added; `validate_lenses_cmd`, `scaffold_cmd`, registry behavior and existing registration tests remain unchanged at this checkpoint.
Global constraints: - This package is a plan only. Product edits and test execution require a later explicit implementation instruction. That future instruction may authorize this plan's tests and CLI help/parser probes, not model jobs, commits, pushes, GitHub writes or new worktrees.
- Work only in the assigned isolated checkout. Change product text only in the two help-producing blocks of `src/superclaude/cli/swarm/commands.py`; author regressions only in `tests/swarm/test_cli_registration.py`. Do not clean up internal comments or adjacent diagnostics.
- Do not add `--custom-prompt-dir`, change command registrations or options, prompt-loading semantics, inline custom specs, injection guards or metadata validation. Directory-backed prompts are one supported route, not a requirement for every custom spec. Preserve custom-lens exclusion from registry validation and scaffold rejection of custom/unknown lenses.
- Historical diagnosis: `.dev/troubleshoot/bug-swarm-custom-prompt-help-20261123191427/REPORT.md` remains blocked/partial. The absent repaired public witness and independent applied-fix review are still unproven. Planning and static source inspection do not pass those checks.
- Historical evidence came from commit db57e231863078dbbb8e4e5fb37a61371c89806c; the transferred checkout started at 720cbaf96653c1c983497ba480f76ca6e60e5369. Original absolute paths and line numbers are provenance, not lookup destinations. Use current repo-relative sources and new local captures; never touch the shared original checkout.
- Preserve every transferred artifact unchanged, including the five pending diagnostic comparison rows and copied counter snapshot. Do not run `counter-update.py`, edit a shared diagnostic counter or lock, retroactively mark earlier probes passed, or claim an environmental explanation. Any later disposition must be a new evidence-backed record under this package's `./artifacts/`.
- All new evidence belongs under `./artifacts/`; retain outputs, commands, timestamps, checkout/module provenance and observed exit statuses. Use UV for Python operations and environment references for secrets. No credentials may be written or logged.
- `.dev/tasks/` is staged, including this package and its artifacts; staging does not authorize committing. Do not stage unrelated diagnostic packages or generated `.claude/` mirrors.
- Final whole-plan verification, independent applied-fix review and progress-ledger management belong to the executor. Do not treat this plan's advisory pre-review as an applied-fix review. Report only checks actually observed, and preserve any remaining blocker.
Start sha: fdff62848f3268733cedac6bf940bf08f30663b8
Diff against the start snapshot: diff --git a/tests/swarm/test_cli_registration.py b/tests/swarm/test_cli_registration.py
index 1ff782964..6988f50f7 100644
--- a/tests/swarm/test_cli_registration.py
+++ b/tests/swarm/test_cli_registration.py
@@ -101,6 +101,17 @@ def test_swarm_help_exits_zero() -> None:
     assert "swarm" in result.output.lower()
 
 
+def test_validate_lenses_help_uses_jobspec_custom_prompt_dir() -> None:
+    """Custom prompt directories are JobSpec fields, not command-line options."""
+    result = CliRunner().invoke(main, ["swarm", "validate-lenses", "--help"])
+    assert result.exit_code == 0, result.output
+    help_text = "".join(result.output.split())
+    assert "--custom-prompt-dir" not in help_text, result.output
+    assert "JobSpec" in help_text, result.output
+    assert "custom_prompt_dir" in help_text, result.output
+    assert "lens:custom" in help_text.replace("`", ""), result.output
+
+
 def test_swarm_help_lists_all_eight_placeholders() -> None:
     """T01.08 -- ``swarm --help`` advertises every placeholder name."""
     runner = CliRunner()

Full task-created file: .dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-red.txt
Task 1 fresh red observation
Timestamp: 2026-11-24T15:05:52Z
Checkout: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help
Commit: 720cbaf96653c1c983497ba480f76ca6e60e5369
Module origin command: uv run --no-sync python -I -c import/module-location
/home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help/src/superclaude/cli/swarm/commands.py

Command: PYTHONDONTWRITEBYTECODE=1 uv run --no-sync pytest tests/swarm/test_cli_registration.py::test_validate_lenses_help_uses_jobspec_custom_prompt_dir -p no:cacheprovider
========================================== test session starts ===========================================
platform linux -- Python 3.13.5, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help/.venv/bin/python
SuperClaude: 6.1.0
rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help
configfile: pyproject.toml
plugins: anyio-4.16.0, superclaude-6.1.0
collecting ... collected 1 item

tests/swarm/test_cli_registration.py::test_validate_lenses_help_uses_jobspec_custom_prompt_dir FAILED [100%]

================================================ FAILURES ================================================
________________________ test_validate_lenses_help_uses_jobspec_custom_prompt_dir ________________________
tests/swarm/test_cli_registration.py:109: in test_validate_lenses_help_uses_jobspec_custom_prompt_dir
    assert "--custom-prompt-dir" not in help_text, result.output
E   AssertionError: Usage: main swarm validate-lenses [OPTIONS]
E     
E       Validate the bundled LENSES registry (FR-008 / T02.20).
E     
E       Runs the COMP-023 five-assertion lens validator over every entry in
E       :data:`superclaude.cli.swarm.lenses.LENSES`. The ``custom`` escape hatch
E       (COMP-026) is intentionally skipped — its prompt body flows in from
E       ``--custom-prompt-dir`` at preflight and is validated on that path (T02.05 /
E       T02.07).
E     
E       Exit codes (OQ-010 resolution -- see module docstring):
E     
E           * 0 -- every non-custom entry passes its five COMP-023       assertions,
E           OR ``--warning-mode`` is set and failures are       emitted as warnings
E           rather than errors.     * 1 -- one or more entries failed validation and
E           ``--warning-mode`` is not set (default blocking branch).     * 2 --
E           reserved for future usage errors (no path argument       accepted today,
E           but kept consistent with :func:`validate_cmd`       for a future
E           ``--registry-path`` opt-in).
E     
E       Output:
E     
E           * Success: one-line OK summary on stdout naming the registry       size
E           and the count of inspected (non-custom) entries.     * Failure: structured
E           per-entry diagnostic block on stderr,       one line per failing entry,
E           format       ``- <rule> @ <path>: <message> (lens=<lens_name>)``.
E     
E     Options:
E       --warning-mode  OQ-010 warning branch: emit per-entry diagnostics on stderr
E                       but exit 0 even when entries fail. Use for pre-commit hooks
E                       and non-blocking CI advisories. Default is blocking (exit 1 on
E                       any failure).
E       -h, --help      Show this message and exit.
E     
E   assert '--custom-prompt-dir' not in 'Usage:mains...sageandexit.'
E     
E     '--custom-prompt-dir' is contained here:
E     ?                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              ...
E     
E     ...Full output truncated, use '-vv' to show
======================================== short test summary info =========================================
FAILED tests/swarm/test_cli_registration.py::test_validate_lenses_help_uses_jobspec_custom_prompt_dir
=========================================== 1 failed in 0.76s ============================================

Observed pytest exit status: 1

Full task-created file: .dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-red-strengthened.txt
Task 1 strengthened test, before either help edit
Timestamp: 2026-11-24T15:10:26Z
Command: PYTHONDONTWRITEBYTECODE=1 uv run --no-sync pytest tests/swarm/test_cli_registration.py::test_validate_lenses_help_uses_jobspec_custom_prompt_dir -p no:cacheprovider
========================================== test session starts ===========================================
platform linux -- Python 3.13.5, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help/.venv/bin/python
SuperClaude: 6.1.0
rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help
configfile: pyproject.toml
plugins: anyio-4.16.0, superclaude-6.1.0
collecting ... collected 1 item

tests/swarm/test_cli_registration.py::test_validate_lenses_help_uses_jobspec_custom_prompt_dir FAILED [100%]

================================================ FAILURES ================================================
________________________ test_validate_lenses_help_uses_jobspec_custom_prompt_dir ________________________
tests/swarm/test_cli_registration.py:109: in test_validate_lenses_help_uses_jobspec_custom_prompt_dir
    assert "--custom-prompt-dir" not in help_text, result.output
E   AssertionError: Usage: main swarm validate-lenses [OPTIONS]
E     
E       Validate the bundled LENSES registry (FR-008 / T02.20).
E     
E       Runs the COMP-023 five-assertion lens validator over every entry in
E       :data:`superclaude.cli.swarm.lenses.LENSES`. The ``custom`` escape hatch
E       (COMP-026) is intentionally skipped — its prompt body flows in from
E       ``--custom-prompt-dir`` at preflight and is validated on that path (T02.05 /
E       T02.07).
E     
E       Exit codes (OQ-010 resolution -- see module docstring):
E     
E           * 0 -- every non-custom entry passes its five COMP-023       assertions,
E           OR ``--warning-mode`` is set and failures are       emitted as warnings
E           rather than errors.     * 1 -- one or more entries failed validation and
E           ``--warning-mode`` is not set (default blocking branch).     * 2 --
E           reserved for future usage errors (no path argument       accepted today,
E           but kept consistent with :func:`validate_cmd`       for a future
E           ``--registry-path`` opt-in).
E     
E       Output:
E     
E           * Success: one-line OK summary on stdout naming the registry       size
E           and the count of inspected (non-custom) entries.     * Failure: structured
E           per-entry diagnostic block on stderr,       one line per failing entry,
E           format       ``- <rule> @ <path>: <message> (lens=<lens_name>)``.
E     
E     Options:
E       --warning-mode  OQ-010 warning branch: emit per-entry diagnostics on stderr
E                       but exit 0 even when entries fail. Use for pre-commit hooks
E                       and non-blocking CI advisories. Default is blocking (exit 1 on
E                       any failure).
E       -h, --help      Show this message and exit.
E     
E   assert '--custom-prompt-dir' not in 'Usage:mains...sageandexit.'
E     
E     '--custom-prompt-dir' is contained here:
E     ?                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              ...
E     
E     ...Full output truncated, use '-vv' to show
======================================== short test summary info =========================================
FAILED tests/swarm/test_cli_registration.py::test_validate_lenses_help_uses_jobspec_custom_prompt_dir
=========================================== 1 failed in 1.26s ============================================

Observed pytest exit status: 1

Codegraph context
index_state: fresh
access: mcp
checked_at: 2026-11-24T15:04:13Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help
call codegraph only when index_state: fresh, never to widen scope
Graph rows are leads. Native Reads confirm public registration, schema/preflight field binding and unchanged runtime contracts. No direct function call is inferred from a callback-registration row.

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-red.txt b/.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-red.txt
deleted file mode 100644
index 9eb3f81e4..000000000
--- a/.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-red.txt
+++ /dev/null
@@ -1,67 +0,0 @@
-Task 1 fresh red observation
-Timestamp: 2026-11-24T15:05:52Z
-Checkout: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help
-Commit: 720cbaf96653c1c983497ba480f76ca6e60e5369
-Module origin command: uv run --no-sync python -I -c import/module-location
-/home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help/src/superclaude/cli/swarm/commands.py
-
-Command: PYTHONDONTWRITEBYTECODE=1 uv run --no-sync pytest tests/swarm/test_cli_registration.py::test_validate_lenses_help_uses_jobspec_custom_prompt_dir -p no:cacheprovider
-========================================== test session starts ===========================================
-platform linux -- Python 3.13.5, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help/.venv/bin/python
-SuperClaude: 6.1.0
-rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help
-configfile: pyproject.toml
-plugins: anyio-4.16.0, superclaude-6.1.0
-collecting ... collected 1 item
-
-tests/swarm/test_cli_registration.py::test_validate_lenses_help_uses_jobspec_custom_prompt_dir FAILED [100%]
-
-================================================ FAILURES ================================================
-________________________ test_validate_lenses_help_uses_jobspec_custom_prompt_dir ________________________
-tests/swarm/test_cli_registration.py:109: in test_validate_lenses_help_uses_jobspec_custom_prompt_dir
-    assert "--custom-prompt-dir" not in help_text, result.output
-E   AssertionError: Usage: main swarm validate-lenses [OPTIONS]
-E     
-E       Validate the bundled LENSES registry (FR-008 / T02.20).
-E     
-E       Runs the COMP-023 five-assertion lens validator over every entry in
-E       :data:`superclaude.cli.swarm.lenses.LENSES`. The ``custom`` escape hatch
-E       (COMP-026) is intentionally skipped — its prompt body flows in from
-E       ``--custom-prompt-dir`` at preflight and is validated on that path (T02.05 /
-E       T02.07).
-E     
-E       Exit codes (OQ-010 resolution -- see module docstring):
-E     
-E           * 0 -- every non-custom entry passes its five COMP-023       assertions,
-E           OR ``--warning-mode`` is set and failures are       emitted as warnings
-E           rather than errors.     * 1 -- one or more entries failed validation and
-E           ``--warning-mode`` is not set (default blocking branch).     * 2 --
-E           reserved for future usage errors (no path argument       accepted today,
-E           but kept consistent with :func:`validate_cmd`       for a future
-E           ``--registry-path`` opt-in).
-E     
-E       Output:
-E     
-E           * Success: one-line OK summary on stdout naming the registry       size
-E           and the count of inspected (non-custom) entries.     * Failure: structured
-E           per-entry diagnostic block on stderr,       one line per failing entry,
-E           format       ``- <rule> @ <path>: <message> (lens=<lens_name>)``.
-E     
-E     Options:
-E       --warning-mode  OQ-010 warning branch: emit per-entry diagnostics on stderr
-E                       but exit 0 even when entries fail. Use for pre-commit hooks
-E                       and non-blocking CI advisories. Default is blocking (exit 1 on
-E                       any failure).
-E       -h, --help      Show this message and exit.
-E     
-E   assert '--custom-prompt-dir' not in 'Usage:mains...sageandexit.'
-E     
-E     '--custom-prompt-dir' is contained here:
-E     ?                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              ...
-E     
-E     ...Full output truncated, use '-vv' to show
-======================================== short test summary info =========================================
-FAILED tests/swarm/test_cli_registration.py::test_validate_lenses_help_uses_jobspec_custom_prompt_dir
-=========================================== 1 failed in 0.76s ============================================
-
-Observed pytest exit status: 1
diff --git a/tests/swarm/test_cli_registration.py b/tests/swarm/test_cli_registration.py
index e7eaa1906..6988f50f7 100644
--- a/tests/swarm/test_cli_registration.py
+++ b/tests/swarm/test_cli_registration.py
@@ -109,7 +109,7 @@ def test_validate_lenses_help_uses_jobspec_custom_prompt_dir() -> None:
     assert "--custom-prompt-dir" not in help_text, result.output
     assert "JobSpec" in help_text, result.output
     assert "custom_prompt_dir" in help_text, result.output
-    assert "lens" in help_text and "custom" in help_text, result.output
+    assert "lens:custom" in help_text.replace("`", ""), result.output
 
 
 def test_swarm_help_lists_all_eight_placeholders() -> None:

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B1 ac=T1.AC1 at=tests/swarm/test_cli_registration.py:112 anchor="positively requires JobSpec, `custom_prompt_dir` and custom-lens guidance" chk=y,n,n,n family=weak-custom-lens-assertion fix=replace the bare substring check with actual custom-lens binding guidance covers="custom-lens guidance" first=A1 origin=new: Current stale help already contains both lens and custom, so the final assertion cannot discriminate the required binding. Parent Read-back confirms the quoted AC and added assertion; no inherited cap. Verdict: missing, one Q5 fix pass authorized. No product help edit at this task.
Saved-probe re-check hit locations (may be empty): tests/swarm/test_cli_registration.py:112

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
