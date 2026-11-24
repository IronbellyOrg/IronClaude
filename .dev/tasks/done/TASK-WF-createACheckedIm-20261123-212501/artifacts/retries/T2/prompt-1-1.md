start=f647b2362128593cd33049b703bba5d61c1ced67
Review one task for spec compliance.

Task brief: ## Task 2: Add scaffold help and unsupported-option regressions

Depends on: Task 1

Add a scaffold help regression and an unsupported-option parser regression in `tests/swarm/test_cli_registration.py` using the existing root `main` plus `CliRunner` pattern. Read the `scaffold_cmd` lens-option help in `src/superclaude/cli/swarm/commands.py`, its registration in `src/superclaude/cli/swarm/__init__.py`, existing help/rejection tests in `tests/swarm/test_scaffold_cmd.py`, and the transferred `scaffold-help.txt`, `run-rejection.txt` and `diagnosability-tasklist.md`. The reference contract remains the custom-directory note in `docs/swarm/command-reference.md` and the schema/preflight symbols named in Task 1.

Acceptance criteria:
- T2.AC1: The scaffold regression invokes `main` with `swarm scaffold --help`, expects exit 0, rejects `--custom-prompt-dir`, and positively requires JobSpec, `custom_prompt_dir` and custom-lens guidance. Assert semantic tokens after whitespace normalization, not full-line formatting. The text must not imply every custom spec needs a directory.
- T2.AC2: The parser regression invokes `main` with `swarm run --custom-prompt-dir` and a temporary directory argument, expects exit 2 and an unknown-option diagnostic naming the exact rejected option. It never launches a swarm job or calls a model; the temporary directory remains unchanged.
- T2.AC3: Before product edits, run both new help cases and the parser guard with concrete pytest node ids. Both help cases must fail for their expected content mismatch while the parser guard passes. Preserve commands, timestamps, outputs and individual exit statuses in `./artifacts/scaffold-help-red.txt` and `./artifacts/parser-before.txt`; preserve Task 1's red evidence unchanged.
- T2.AC4: Capture fresh public CLI baselines using `uv run superclaude swarm validate-lenses --help`, `uv run superclaude swarm scaffold --help`, and `uv run superclaude swarm run --custom-prompt-dir` followed by an existing temporary directory. Record full output plus observed exit statuses 0, 0 and 2 in `./artifacts/public-before.txt`, along with commit, checkout root and imported commands-module origin. If results differ, stop and explain instead of forcing the old diagnosis.
- T2.AC5: Keep all five historical diagnostic rows pending in their original package. Record in `./artifacts/diagnostic-disposition.md` how new local captures address the two exact-help observations; explain that identical reference forms provide no independent control and the no-op row has no causal discrimination for this wording defect. An applicability decision needs cited source and observed outputs, not invented passing results; mark unresolved rows explicitly if evidence is insufficient.
Global constraints: - This package is a plan only. Product edits and test execution require a later explicit implementation instruction. That future instruction may authorize this plan's tests and CLI help/parser probes, not model jobs, commits, pushes, GitHub writes or new worktrees.
- Work only in the assigned isolated checkout. Change product text only in the two help-producing blocks of `src/superclaude/cli/swarm/commands.py`; author regressions only in `tests/swarm/test_cli_registration.py`. Do not clean up internal comments or adjacent diagnostics.
- Do not add `--custom-prompt-dir`, change command registrations or options, prompt-loading semantics, inline custom specs, injection guards or metadata validation. Directory-backed prompts are one supported route, not a requirement for every custom spec. Preserve custom-lens exclusion from registry validation and scaffold rejection of custom/unknown lenses.
- Historical diagnosis: `.dev/troubleshoot/bug-swarm-custom-prompt-help-20261123191427/REPORT.md` remains blocked/partial. The absent repaired public witness and independent applied-fix review are still unproven. Planning and static source inspection do not pass those checks.
- Historical evidence came from commit db57e231863078dbbb8e4e5fb37a61371c89806c; the transferred checkout started at 720cbaf96653c1c983497ba480f76ca6e60e5369. Original absolute paths and line numbers are provenance, not lookup destinations. Use current repo-relative sources and new local captures; never touch the shared original checkout.
- Preserve every transferred artifact unchanged, including the five pending diagnostic comparison rows and copied counter snapshot. Do not run `counter-update.py`, edit a shared diagnostic counter or lock, retroactively mark earlier probes passed, or claim an environmental explanation. Any later disposition must be a new evidence-backed record under this package's `./artifacts/`.
- All new evidence belongs under `./artifacts/`; retain outputs, commands, timestamps, checkout/module provenance and observed exit statuses. Use UV for Python operations and environment references for secrets. No credentials may be written or logged.
- `.dev/tasks/` is staged, including this package and its artifacts; staging does not authorize committing. Do not stage unrelated diagnostic packages or generated `.claude/` mirrors.
- Final whole-plan verification, independent applied-fix review and progress-ledger management belong to the executor. Do not treat this plan's advisory pre-review as an applied-fix review. Report only checks actually observed, and preserve any remaining blocker.
Start sha: f647b2362128593cd33049b703bba5d61c1ced67
Diff against the start snapshot: diff --git a/tests/swarm/test_cli_registration.py b/tests/swarm/test_cli_registration.py
index 6988f50f7..7b9a13e30 100644
--- a/tests/swarm/test_cli_registration.py
+++ b/tests/swarm/test_cli_registration.py
@@ -14,6 +14,8 @@ Enforces AC-002 and COMP-001 from the MultiModelSwarm roadmap:
 
 from __future__ import annotations
 
+from pathlib import Path
+
 import pytest
 from click.testing import CliRunner
 
@@ -112,6 +114,29 @@ def test_validate_lenses_help_uses_jobspec_custom_prompt_dir() -> None:
     assert "lens:custom" in help_text.replace("`", ""), result.output
 
 
+def test_scaffold_help_uses_jobspec_custom_prompt_dir() -> None:
+    """Scaffold help names optional directory-backed custom prompt configuration."""
+    result = CliRunner().invoke(main, ["swarm", "scaffold", "--help"])
+    assert result.exit_code == 0, result.output
+    help_text = "".join(result.output.split())
+    assert "--custom-prompt-dir" not in help_text, result.output
+    assert "JobSpec" in help_text, result.output
+    assert "custom_prompt_dir" in help_text, result.output
+    assert "lens:custom" in help_text.replace("`", ""), result.output
+    assert "inline" in help_text.lower(), result.output
+
+
+def test_run_rejects_custom_prompt_dir_option(tmp_path: Path) -> None:
+    """The directory belongs in a JobSpec, never in the run option parser."""
+    result = CliRunner().invoke(
+        main, ["swarm", "run", "--custom-prompt-dir", str(tmp_path)]
+    )
+    assert result.exit_code == 2, result.output
+    assert "No such option" in result.output, result.output
+    assert "--custom-prompt-dir" in result.output, result.output
+    assert list(tmp_path.iterdir()) == []
+
+
 def test_swarm_help_lists_all_eight_placeholders() -> None:
     """T01.08 -- ``swarm --help`` advertises every placeholder name."""
     runner = CliRunner()

Full task-created file, source line numbers: .dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:1: Task 2: both help regressions before either product edit
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:2: Timestamp: 2026-11-24T15:18:41Z
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:3: Checkout: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:4: Commit: 720cbaf96653c1c983497ba480f76ca6e60e5369
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:5: Module origin: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help/src/superclaude/cli/swarm/commands.py
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:6: Command: PYTHONDONTWRITEBYTECODE=1 uv run --no-sync pytest tests/swarm/test_cli_registration.py::test_validate_lenses_help_uses_jobspec_custom_prompt_dir tests/swarm/test_cli_registration.py::test_scaffold_help_uses_jobspec_custom_prompt_dir -p no:cacheprovider
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:7: ========================================== test session starts ===========================================
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:8: platform linux -- Python 3.13.5, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help/.venv/bin/python
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:9: SuperClaude: 6.1.0
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:10: rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:11: configfile: pyproject.toml
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:12: plugins: anyio-4.16.0, superclaude-6.1.0
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:13: collecting ... collected 2 items
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:14: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:15: tests/swarm/test_cli_registration.py::test_validate_lenses_help_uses_jobspec_custom_prompt_dir FAILED [ 50%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:16: tests/swarm/test_cli_registration.py::test_scaffold_help_uses_jobspec_custom_prompt_dir FAILED     [100%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:17: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:18: ================================================ FAILURES ================================================
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:19: ________________________ test_validate_lenses_help_uses_jobspec_custom_prompt_dir ________________________
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:20: tests/swarm/test_cli_registration.py:111: in test_validate_lenses_help_uses_jobspec_custom_prompt_dir
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:21:     assert "--custom-prompt-dir" not in help_text, result.output
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:22: E   AssertionError: Usage: main swarm validate-lenses [OPTIONS]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:23: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:24: E       Validate the bundled LENSES registry (FR-008 / T02.20).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:25: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:26: E       Runs the COMP-023 five-assertion lens validator over every entry in
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:27: E       :data:`superclaude.cli.swarm.lenses.LENSES`. The ``custom`` escape hatch
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:28: E       (COMP-026) is intentionally skipped — its prompt body flows in from
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:29: E       ``--custom-prompt-dir`` at preflight and is validated on that path (T02.05 /
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:30: E       T02.07).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:31: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:32: E       Exit codes (OQ-010 resolution -- see module docstring):
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:33: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:34: E           * 0 -- every non-custom entry passes its five COMP-023       assertions,
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:35: E           OR ``--warning-mode`` is set and failures are       emitted as warnings
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:36: E           rather than errors.     * 1 -- one or more entries failed validation and
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:37: E           ``--warning-mode`` is not set (default blocking branch).     * 2 --
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:38: E           reserved for future usage errors (no path argument       accepted today,
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:39: E           but kept consistent with :func:`validate_cmd`       for a future
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:40: E           ``--registry-path`` opt-in).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:41: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:42: E       Output:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:43: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:44: E           * Success: one-line OK summary on stdout naming the registry       size
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:45: E           and the count of inspected (non-custom) entries.     * Failure: structured
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:46: E           per-entry diagnostic block on stderr,       one line per failing entry,
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:47: E           format       ``- <rule> @ <path>: <message> (lens=<lens_name>)``.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:48: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:49: E     Options:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:50: E       --warning-mode  OQ-010 warning branch: emit per-entry diagnostics on stderr
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:51: E                       but exit 0 even when entries fail. Use for pre-commit hooks
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:52: E                       and non-blocking CI advisories. Default is blocking (exit 1 on
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:53: E                       any failure).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:54: E       -h, --help      Show this message and exit.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:55: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:56: E   assert '--custom-prompt-dir' not in 'Usage:mains...sageandexit.'
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:57: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:58: E     '--custom-prompt-dir' is contained here:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:59: E     ?                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              ...
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:60: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:61: E     ...Full output truncated, use '-vv' to show
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:62: ___________________________ test_scaffold_help_uses_jobspec_custom_prompt_dir ____________________________
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:63: tests/swarm/test_cli_registration.py:122: in test_scaffold_help_uses_jobspec_custom_prompt_dir
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:64:     assert "--custom-prompt-dir" not in help_text, result.output
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:65: E   AssertionError: Usage: main swarm scaffold [OPTIONS]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:66: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:67: E       Emit a starter JobSpec for the named lens (FR-006 / T07.09).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:68: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:69: E       Generates a fully-populated DM-001 JobSpec for ``--lens NAME`` so operators
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:70: E       have a valid baseline they can edit instead of authoring the spec from
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:71: E       scratch. The emitted spec passes ``swarm validate`` out of the box -- the only
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:72: E       fields the operator MUST override before invoking ``swarm run`` are
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:73: E       ``target.path`` (placeholder ``""``) and ``output.dir`` (placeholder ``""``).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:74: E       Model IDs are filled with ``lens-default-model-<i>`` placeholders that schema-
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:75: E       validate but never reach the wire (the transport defaults to ``stub`` for the
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:76: E       same safe-quick-dispatch reasoning as ``swarm run --lens``).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:77: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:78: E       Exit codes:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:79: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:80: E           * 0 -- starter spec rendered successfully (to stdout, or to
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:81: E           ``--output`` when supplied).     * 2 -- usage error: lens unknown, lens is
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:82: E           the ``custom`` escape       hatch (no registry defaults to expand from),
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:83: E           or ``--output``       path is unwritable.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:84: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:85: E     Options:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:86: E       --lens TEXT        Lens to scaffold a starter JobSpec for (e.g. bare-review).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:87: E                          Expands lens defaults (system/user prompts, recipe,
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:88: E                          workers, line_cap, next-command template) into a full
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:89: E                          DM-001 JobSpec the operator can edit. ``custom`` and
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:90: E                          unknown lens names are rejected -- ``custom`` is the FR-021
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:91: E                          escape hatch whose prompts flow in from --custom-prompt-dir
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:92: E                          at preflight, so it has no registry defaults to expand
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:93: E                          from.  [required]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:94: E       -o, --output FILE  Write the starter JobSpec to PATH atomically (tmp +
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:95: E                          os.replace). When omitted, the JSON document is emitted to
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:96: E                          stdout so it can be piped straight into ``swarm validate``
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:97: E                          or redirected with the shell of choice.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:98: E       -h, --help         Show this message and exit.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:99: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:100: E   assert '--custom-prompt-dir' not in 'Usage:mains...sageandexit.'
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:101: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:102: E     '--custom-prompt-dir' is contained here:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:103: E       Usage:mainswarmscaffold[OPTIONS]EmitastarterJobSpecforthenamedlens(FR-006/T07.09).Generatesafully-populatedDM-001JobSpecfor``--lensNAME``sooperatorshaveavalidbaselinetheycaneditinsteadofauthoringthespecfromscratch.Theemittedspecpasses``swarmvalidate``outofthebox--theonlyfieldstheoperatorMUSToverridebeforeinvoking``swarmrun``are``target.path``(placeholder``""``)and``output.dir``(placeholder``""``).ModelIDsarefilledwith``lens-default-model-<i>``placeholdersthatschema-validatebutneverreachthewire(thetransportdefaultsto``stub``forthesamesa...
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:104: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:105: E     ...Full output truncated, use '-vv' to show
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:106: ======================================== short test summary info =========================================
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:107: FAILED tests/swarm/test_cli_registration.py::test_validate_lenses_help_uses_jobspec_custom_prompt_dir
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:108: FAILED tests/swarm/test_cli_registration.py::test_scaffold_help_uses_jobspec_custom_prompt_dir - Assert...
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:109: =========================================== 2 failed in 0.96s ============================================
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:110: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/scaffold-help-red.txt:111: Observed pytest exit status: 1

Full task-created file, source line numbers: .dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/parser-before.txt
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/parser-before.txt:1: Task 2: unsupported-option guard before product edits
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/parser-before.txt:2: Timestamp: 2026-11-24T15:18:43Z
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/parser-before.txt:3: Checkout: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/parser-before.txt:4: Command: PYTHONDONTWRITEBYTECODE=1 uv run --no-sync pytest tests/swarm/test_cli_registration.py::test_run_rejects_custom_prompt_dir_option -p no:cacheprovider
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/parser-before.txt:5: ========================================== test session starts ===========================================
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/parser-before.txt:6: platform linux -- Python 3.13.5, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help/.venv/bin/python
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/parser-before.txt:7: SuperClaude: 6.1.0
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/parser-before.txt:8: rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/parser-before.txt:9: configfile: pyproject.toml
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/parser-before.txt:10: plugins: anyio-4.16.0, superclaude-6.1.0
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/parser-before.txt:11: collecting ... collected 1 item
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/parser-before.txt:12: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/parser-before.txt:13: tests/swarm/test_cli_registration.py::test_run_rejects_custom_prompt_dir_option PASSED             [100%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/parser-before.txt:14: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/parser-before.txt:15: =========================================== 1 passed in 0.96s ============================================
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/parser-before.txt:16: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/parser-before.txt:17: Observed pytest exit status: 0

Full task-created file, source line numbers: .dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:1: Public pre-fix baseline
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:2: Timestamp: 2026-11-24T15:18:58Z
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:3: Checkout: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:4: Commit: 720cbaf96653c1c983497ba480f76ca6e60e5369
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:5: Module origin: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help/src/superclaude/cli/swarm/commands.py
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:6: Parser temporary directory: /tmp/swarm-help-parser.wYfp70Qi
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:7: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:8: Command: uv run --no-sync superclaude swarm validate-lenses --help
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:9: Usage: superclaude swarm validate-lenses [OPTIONS]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:10: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:11:   Validate the bundled LENSES registry (FR-008 / T02.20).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:12: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:13:   Runs the COMP-023 five-assertion lens validator over every entry in
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:14:   :data:`superclaude.cli.swarm.lenses.LENSES`. The ``custom`` escape hatch (COMP-026) is
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:15:   intentionally skipped — its prompt body flows in from ``--custom-prompt-dir`` at preflight and
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:16:   is validated on that path (T02.05 / T02.07).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:17: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:18:   Exit codes (OQ-010 resolution -- see module docstring):
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:19: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:20:       * 0 -- every non-custom entry passes its five COMP-023       assertions, OR ``--warning-
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:21:       mode`` is set and failures are       emitted as warnings rather than errors.     * 1 -- one
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:22:       or more entries failed validation and       ``--warning-mode`` is not set (default blocking
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:23:       branch).     * 2 -- reserved for future usage errors (no path argument       accepted today,
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:24:       but kept consistent with :func:`validate_cmd`       for a future ``--registry-path`` opt-
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:25:       in).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:26: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:27:   Output:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:28: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:29:       * Success: one-line OK summary on stdout naming the registry       size and the count of
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:30:       inspected (non-custom) entries.     * Failure: structured per-entry diagnostic block on
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:31:       stderr,       one line per failing entry, format       ``- <rule> @ <path>: <message>
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:32:       (lens=<lens_name>)``.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:33: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:34: Options:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:35:   --warning-mode  OQ-010 warning branch: emit per-entry diagnostics on stderr but exit 0 even when
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:36:                   entries fail. Use for pre-commit hooks and non-blocking CI advisories. Default
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:37:                   is blocking (exit 1 on any failure).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:38:   -h, --help      Show this message and exit.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:39: Observed exit status: 0
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:40: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:41: Command: uv run --no-sync superclaude swarm scaffold --help
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:42: Usage: superclaude swarm scaffold [OPTIONS]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:43: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:44:   Emit a starter JobSpec for the named lens (FR-006 / T07.09).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:45: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:46:   Generates a fully-populated DM-001 JobSpec for ``--lens NAME`` so operators have a valid
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:47:   baseline they can edit instead of authoring the spec from scratch. The emitted spec passes
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:48:   ``swarm validate`` out of the box -- the only fields the operator MUST override before invoking
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:49:   ``swarm run`` are ``target.path`` (placeholder ``""``) and ``output.dir`` (placeholder ``""``).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:50:   Model IDs are filled with ``lens-default-model-<i>`` placeholders that schema-validate but never
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:51:   reach the wire (the transport defaults to ``stub`` for the same safe-quick-dispatch reasoning as
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:52:   ``swarm run --lens``).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:53: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:54:   Exit codes:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:55: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:56:       * 0 -- starter spec rendered successfully (to stdout, or to       ``--output`` when
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:57:       supplied).     * 2 -- usage error: lens unknown, lens is the ``custom`` escape       hatch
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:58:       (no registry defaults to expand from), or ``--output``       path is unwritable.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:59: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:60: Options:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:61:   --lens TEXT        Lens to scaffold a starter JobSpec for (e.g. bare-review). Expands lens
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:62:                      defaults (system/user prompts, recipe, workers, line_cap, next-command
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:63:                      template) into a full DM-001 JobSpec the operator can edit. ``custom`` and
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:64:                      unknown lens names are rejected -- ``custom`` is the FR-021 escape hatch
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:65:                      whose prompts flow in from --custom-prompt-dir at preflight, so it has no
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:66:                      registry defaults to expand from.  [required]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:67:   -o, --output FILE  Write the starter JobSpec to PATH atomically (tmp + os.replace). When
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:68:                      omitted, the JSON document is emitted to stdout so it can be piped straight
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:69:                      into ``swarm validate`` or redirected with the shell of choice.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:70:   -h, --help         Show this message and exit.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:71: Observed exit status: 0
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:72: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:73: Command: uv run --no-sync superclaude swarm run --custom-prompt-dir /tmp/swarm-help-parser.wYfp70Qi
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:74: Usage: superclaude swarm run [OPTIONS] [SPEC_PATH]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:75: Try 'superclaude swarm run --help' for help.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:76: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:77: Error: No such option '--custom-prompt-dir'.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:78: Observed exit status: 2
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:79: Temporary directory contents after rejection: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-before.txt:80: Expected observed status sequence: 0,0,2

Full task-created file, source line numbers: .dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/diagnostic-disposition.md
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/diagnostic-disposition.md:1: # Historical Diagnostic Disposition
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/diagnostic-disposition.md:2: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/diagnostic-disposition.md:3: ## Fresh observations
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/diagnostic-disposition.md:4: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/diagnostic-disposition.md:5: Fresh pre-edit captures are ./public-before.txt (2026-11-24T15:18:58Z), bound to the current checkout, imported commands.py and commit 720cbaf96653c1c983497ba480f76ca6e60e5369. Public validate-lenses/scaffold help each exits 0 and advertises the unsupported option; run with that option exits 2 before any job. Expected observed status sequence is 0/0/2. ./scaffold-help-red.txt separately shows two collected root-command help regressions fail on their stale-option assertions; ./parser-before.txt shows the parser regression passes and its temporary directory stays empty.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/diagnostic-disposition.md:6: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/diagnostic-disposition.md:7: These are new implementation observations, not retroactive validation of the copied diagnosis. Historical report and tasklist remain unchanged under .dev/troubleshoot/bug-swarm-custom-prompt-help-20261123191427/.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/diagnostic-disposition.md:8: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/diagnostic-disposition.md:9: ## Historical row applicability
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/diagnostic-disposition.md:10: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/diagnostic-disposition.md:11: | Historical row | New evidence / applicability | Historical state |
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/diagnostic-disposition.md:12: |---|---|---|
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/diagnostic-disposition.md:13: | P1-exact | New validate-lenses public capture exposes stale spelling, exit 0. Source producer commands.py:432-439 matches this wording. | Pending record preserved; new local evidence only |
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/diagnostic-disposition.md:14: | P2-exact | New scaffold public capture exposes stale spelling, exit 0. Source lens-option help commands.py:3773-3786 matches. | Pending record preserved; new local evidence only |
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/diagnostic-disposition.md:15: | P1-ref | Historical tasklist:19-20 prescribes identical validate-lenses --help form and predictions for exact/reference. No different control input or discriminatory outcome exists for this pair. The fresh capture covers that same form, not an independent control. | Applicability disposition here; not retroactively passed |
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/diagnostic-disposition.md:16: | P2-ref | Historical tasklist:21-22 likewise uses identical scaffold --help form and predictions. Fresh scaffold capture covers that form but cannot establish an independent control. | Applicability disposition here; not retroactively passed |
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/diagnostic-disposition.md:17: | control | Historical tasklist:23 gives a no-op with unknown true/false outcomes and says either is inconclusive. A no-op has no causal discrimination for the emitted wording. It is not needed to distinguish two visible source/help descriptions from the rejecting parser; no environment-property claim is made. | Inapplicable to this bounded wording comparison; pending original untouched |
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/diagnostic-disposition.md:18: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/diagnostic-disposition.md:19: ## Limits
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/diagnostic-disposition.md:20: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/diagnostic-disposition.md:21: This record addresses the two exact-help observations and supplies an evidence-backed applicability decision for the identical reference/no-op rows. It does not prove a fixed state, full custom-job success, environment comparison, or independent applied-fix review. Repaired public outputs and applied-fix review are still required later. No counter-update.py invocation, shared-store edit, historical status rewrite, model-backed job or GitHub action occurred. User-requested path relocation happened before this implementation and is separately documented in the original report; no further historical evidence was changed.

Codegraph context
index_state: fresh
access: mcp
checked_at: 2026-11-24T15:14:41Z
worktree_root:/home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help
call codegraph only when index_state: fresh, never to widen scope
Graph rows are leads. Native Reads confirm public registration, schema/preflight field binding and unchanged runtime contracts. No direct function call is inferred from a callback-registration row.

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
