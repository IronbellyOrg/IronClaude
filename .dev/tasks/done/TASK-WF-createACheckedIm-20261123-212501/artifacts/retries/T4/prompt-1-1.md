start=50b87a71cedf08bf630b12be9234faa9a33273e7
Review one task for spec compliance.

Task brief: ## Task 4: Replace the scaffold lens option description

Depends on: Task 3

In `src/superclaude/cli/swarm/commands.py`, replace only the custom-prompt explanation inside `scaffold_cmd`'s `--lens` option help. Refer to directory-backed custom prompts through the JobSpec `custom_prompt_dir` field with `lens: custom`, not a command-line option. Preserve the reason scaffold rejects custom lenses: there are no bundled registry defaults to expand. Read that current option-help block, Task 2's tests and red evidence, `tests/swarm/test_scaffold_cmd.py`'s custom/unknown-lens checks, and the custom-directory note in `docs/swarm/command-reference.md`. Read the historical report's Next Steps and Pipeline Hardening Closure sections to keep its missing-proof requirements separate from this new implementation's evidence.

Acceptance criteria:
- T4.AC1: The final product diff contains only the two intended help blocks in `src/superclaude/cli/swarm/commands.py` plus the new regressions in `tests/swarm/test_cli_registration.py`; internal comments, adjacent error messages, registrations, parser options, preflight, schema and docs are unchanged. Help describes directory-backed prompts as optional for custom specs.
- T4.AC2: Both public-root help regressions and the parser rejection guard pass after their preserved pre-edit observations in `./artifacts/validate-help-red.txt`, `./artifacts/scaffold-help-red.txt` and `./artifacts/parser-before.txt` (F1). Existing registration/help and scaffold tests remain intact, including custom/unknown-lens rejection, schema-valid scaffold output and injection-guard content.
- T4.AC3: Run `uv run pytest tests/swarm/test_cli_registration.py tests/swarm/test_validate_lenses_cmd.py tests/swarm/test_scaffold_cmd.py tests/swarm/test_custom_prompt_dir.py tests/swarm/test_custom_prompt_dir_injection_guard.py --cov=superclaude.cli.swarm --cov-report=term-missing`; preserve command, full output and observed status in `./artifacts/related-tests-green.txt`. No arbitrary coverage percentage is required; report unavailable coverage tooling or any failure honestly and do not silently drop checks.
- T4.AC4: Capture full repaired public outputs by running `uv run superclaude swarm validate-lenses --help`, `uv run superclaude swarm scaffold --help` and `uv run superclaude swarm run --custom-prompt-dir <existing temporary directory>`, in `./artifacts/public-after.txt` (F1), including module origin, commit/checkout provenance, timestamps and observed statuses 0, 0 and 2. Both help outputs omit the rejected option and explain the supported field/custom-lens binding; the actual run parser still rejects that option. Source text inspection or mocked output alone is insufficient. Compare each with the same command's status and output in `./artifacts/public-before.txt` (F1).
- T4.AC5: Retain red/green tests, before/after public captures and the pending/applicability record for the historical diagnostic rows. The executor's independent final applied-fix review must check this exact diff, the effective public surfaces, inline custom support and unchanged guard/metadata behavior, and persist its report under `./artifacts/`. Planning pre-review does not satisfy it.
- T4.AC6: Do not declare repaired-state closure while public positive evidence or independent applied-fix review is absent or failing. Record new evidence and any remaining blockers without editing or retroactively passing the transferred report. No real model run, full custom-job success claim, commit, push, GitHub interaction or worktree creation is part of this plan.
Global constraints: - This package is a plan only. Product edits and test execution require a later explicit implementation instruction. That future instruction may authorize this plan's tests and CLI help/parser probes, not model jobs, commits, pushes, GitHub writes or new worktrees.
- Work only in the assigned isolated checkout. Change product text only in the two help-producing blocks of `src/superclaude/cli/swarm/commands.py`; author regressions only in `tests/swarm/test_cli_registration.py`. Do not clean up internal comments or adjacent diagnostics.
- Do not add `--custom-prompt-dir`, change command registrations or options, prompt-loading semantics, inline custom specs, injection guards or metadata validation. Directory-backed prompts are one supported route, not a requirement for every custom spec. Preserve custom-lens exclusion from registry validation and scaffold rejection of custom/unknown lenses.
- Historical diagnosis: `.dev/troubleshoot/bug-swarm-custom-prompt-help-20261123191427/REPORT.md` remains blocked/partial. The absent repaired public witness and independent applied-fix review are still unproven. Planning and static source inspection do not pass those checks.
- Historical evidence came from commit db57e231863078dbbb8e4e5fb37a61371c89806c; the transferred checkout started at 720cbaf96653c1c983497ba480f76ca6e60e5369. Original absolute paths and line numbers are provenance, not lookup destinations. Use current repo-relative sources and new local captures; never touch the shared original checkout.
- Preserve every transferred artifact unchanged, including the five pending diagnostic comparison rows and copied counter snapshot. Do not run `counter-update.py`, edit a shared diagnostic counter or lock, retroactively mark earlier probes passed, or claim an environmental explanation. Any later disposition must be a new evidence-backed record under this package's `./artifacts/`.
- All new evidence belongs under `./artifacts/`; retain outputs, commands, timestamps, checkout/module provenance and observed exit statuses. Use UV for Python operations and environment references for secrets. No credentials may be written or logged.
- `.dev/tasks/` is staged, including this package and its artifacts; staging does not authorize committing. Do not stage unrelated diagnostic packages or generated `.claude/` mirrors.
- Final whole-plan verification, independent applied-fix review and progress-ledger management belong to the executor. Do not treat this plan's advisory pre-review as an applied-fix review. Report only checks actually observed, and preserve any remaining blocker.
Start sha: 50b87a71cedf08bf630b12be9234faa9a33273e7
Diff against the start snapshot: diff --git a/src/superclaude/cli/swarm/commands.py b/src/superclaude/cli/swarm/commands.py
index 0ce5048b3..5510b96b3 100644
--- a/src/superclaude/cli/swarm/commands.py
+++ b/src/superclaude/cli/swarm/commands.py
@@ -3782,9 +3782,11 @@ def _write_scaffold_atomic(output_path: Path, payload: str) -> None:
         "Expands lens defaults (system/user prompts, recipe, workers, "
         "line_cap, next-command template) into a full DM-001 JobSpec "
         "the operator can edit. ``custom`` and unknown lens names are "
-        "rejected -- ``custom`` is the FR-021 escape hatch whose prompts "
-        "flow in from --custom-prompt-dir at preflight, so it has no "
-        "registry defaults to expand from."
+        "rejected -- ``custom`` is the FR-021 escape hatch with no "
+        "registry defaults to expand from. Directory-backed custom prompts "
+        "use the JobSpec ``custom_prompt_dir`` field with ``lens: custom`` "
+        "and are loaded at preflight; custom specs may instead supply "
+        "inline prompts without a directory."
     ),
 )
 @click.option(

Full task-created file, source line numbers: .dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:1: diff --git a/src/superclaude/cli/swarm/commands.py b/src/superclaude/cli/swarm/commands.py
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:2: index 8577805b1..5510b96b3 100644
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:3: --- a/src/superclaude/cli/swarm/commands.py
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:4: +++ b/src/superclaude/cli/swarm/commands.py
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:5: @@ -434,9 +434,10 @@ def validate_lenses_cmd(warning_mode: bool) -> None:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:6:  
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:7:      Runs the COMP-023 five-assertion lens validator over every entry in
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:8:      :data:`superclaude.cli.swarm.lenses.LENSES`. The ``custom`` escape
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:9: -    hatch (COMP-026) is intentionally skipped — its prompt body flows in
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:10: -    from ``--custom-prompt-dir`` at preflight and is validated on that
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:11: -    path (T02.05 / T02.07).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:12: +    hatch (COMP-026) is intentionally skipped. Directory-backed custom
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:13: +    prompts use the JobSpec ``custom_prompt_dir`` field with ``lens: custom``
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:14: +    and are loaded and validated at preflight (T02.05 / T02.07). Custom
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:15: +    specs may also supply inline prompts without a directory.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:16:  
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:17:      Exit codes (OQ-010 resolution -- see module docstring):
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:18:  
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:19: @@ -3781,9 +3782,11 @@ def _write_scaffold_atomic(output_path: Path, payload: str) -> None:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:20:          "Expands lens defaults (system/user prompts, recipe, workers, "
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:21:          "line_cap, next-command template) into a full DM-001 JobSpec "
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:22:          "the operator can edit. ``custom`` and unknown lens names are "
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:23: -        "rejected -- ``custom`` is the FR-021 escape hatch whose prompts "
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:24: -        "flow in from --custom-prompt-dir at preflight, so it has no "
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:25: -        "registry defaults to expand from."
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:26: +        "rejected -- ``custom`` is the FR-021 escape hatch with no "
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:27: +        "registry defaults to expand from. Directory-backed custom prompts "
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:28: +        "use the JobSpec ``custom_prompt_dir`` field with ``lens: custom`` "
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:29: +        "and are loaded at preflight; custom specs may instead supply "
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:30: +        "inline prompts without a directory."
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:31:      ),
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:32:  )
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:33:  @click.option(
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:34: diff --git a/tests/swarm/test_cli_registration.py b/tests/swarm/test_cli_registration.py
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:35: index 1ff782964..7b9a13e30 100644
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:36: --- a/tests/swarm/test_cli_registration.py
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:37: +++ b/tests/swarm/test_cli_registration.py
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:38: @@ -14,6 +14,8 @@ Enforces AC-002 and COMP-001 from the MultiModelSwarm roadmap:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:39:  
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:40:  from __future__ import annotations
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:41:  
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:42: +from pathlib import Path
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:43: +
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:44:  import pytest
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:45:  from click.testing import CliRunner
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:46:  
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:47: @@ -101,6 +103,40 @@ def test_swarm_help_exits_zero() -> None:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:48:      assert "swarm" in result.output.lower()
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:49:  
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:50:  
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:51: +def test_validate_lenses_help_uses_jobspec_custom_prompt_dir() -> None:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:52: +    """Custom prompt directories are JobSpec fields, not command-line options."""
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:53: +    result = CliRunner().invoke(main, ["swarm", "validate-lenses", "--help"])
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:54: +    assert result.exit_code == 0, result.output
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:55: +    help_text = "".join(result.output.split())
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:56: +    assert "--custom-prompt-dir" not in help_text, result.output
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:57: +    assert "JobSpec" in help_text, result.output
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:58: +    assert "custom_prompt_dir" in help_text, result.output
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:59: +    assert "lens:custom" in help_text.replace("`", ""), result.output
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:60: +
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:61: +
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:62: +def test_scaffold_help_uses_jobspec_custom_prompt_dir() -> None:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:63: +    """Scaffold help names optional directory-backed custom prompt configuration."""
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:64: +    result = CliRunner().invoke(main, ["swarm", "scaffold", "--help"])
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:65: +    assert result.exit_code == 0, result.output
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:66: +    help_text = "".join(result.output.split())
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:67: +    assert "--custom-prompt-dir" not in help_text, result.output
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:68: +    assert "JobSpec" in help_text, result.output
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:69: +    assert "custom_prompt_dir" in help_text, result.output
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:70: +    assert "lens:custom" in help_text.replace("`", ""), result.output
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:71: +    assert "inline" in help_text.lower(), result.output
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:72: +
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:73: +
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:74: +def test_run_rejects_custom_prompt_dir_option(tmp_path: Path) -> None:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:75: +    """The directory belongs in a JobSpec, never in the run option parser."""
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:76: +    result = CliRunner().invoke(
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:77: +        main, ["swarm", "run", "--custom-prompt-dir", str(tmp_path)]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:78: +    )
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:79: +    assert result.exit_code == 2, result.output
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:80: +    assert "No such option" in result.output, result.output
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:81: +    assert "--custom-prompt-dir" in result.output, result.output
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:82: +    assert list(tmp_path.iterdir()) == []
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:83: +
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:84: +
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:85:  def test_swarm_help_lists_all_eight_placeholders() -> None:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:86:      """T01.08 -- ``swarm --help`` advertises every placeholder name."""
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-product.diff:87:      runner = CliRunner()

Full task-created file, source line numbers: .dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-fix-review.md
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-fix-review.md:1: # Independent Applied-Fix Review
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-fix-review.md:2: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-fix-review.md:3: ## AC marks
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-fix-review.md:4: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-fix-review.md:5: Reviewer: swarm-applied-fix-qa, independent read-only review, 2026-11-24. Paths below are repo-relative or package-relative under ./artifacts/.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-fix-review.md:6: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-fix-review.md:7: 1. Diff scope: applied-product.diff:1-33 changes only two blocks in commands.py: the validate-lenses docstring and scaffold lens-option help. applied-product.diff:34-87 changes only the Path import and three regressions in test_cli_registration.py. Live source matches at commands.py:435-440,3780-3790 and test_cli_registration.py:17,106-137. Reviewer cannot run git; parent independently ran git diff --name-only HEAD -- src tests docs and observed only these two files. Internal comments/adjacent diagnostics are unchanged as required.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-fix-review.md:8: 2. Validate-lenses help: commands.py:436-440 and public-after.txt:11-17 omit the false option and name JobSpec custom_prompt_dir with lens: custom, preflight validation and inline custom prompts. Live preflight.py:1569-1596 applies the directory only for custom plus a nonempty field. schema.py:685-723 enforces the binding without requiring a directory for every custom spec; inline support is explicit at schema.py:700-704.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-fix-review.md:9: 3. Scaffold help: commands.py:3784-3789 and public-after.txt:63-70 omit the false option, preserve no-registry-defaults rejection, and describe optional directory-backed or inline prompts.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-fix-review.md:10: 4. Parser: public-after.txt:78-84 retains the same command/directory, unknown-option diagnostic and exit 2 as public-before.txt:73-79. Directory remains empty. test_cli_registration.py:129-137 pins this. No option or registration was added.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-fix-review.md:11: 5. Tests: test_cli_registration.py:106-137 invokes root main, strips whitespace and checks absence plus positive field/lens binding; scaffold requires inline guidance. Reviewer did not read the red logs, only confirmed their presence; reproducing-history verification remains the per-task and FINAL reviewers' responsibility.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-fix-review.md:12: 6. Preserved contracts: commands.py:3826-3844 custom/unknown rejection code is untouched, with corresponding tests passed at related-tests-green.txt:72-73. Validation warning/custom-only tests pass at :34-45. Directory/preflight/guard tests pass at :75-103. Guard/metadata paths are absent from the product diff.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-fix-review.md:13: 7. Test evidence: related-tests-green.txt:5-11 records coverage plugin unavailable and command exit 4. Same five files run without coverage at :14, with 80 passed, 1 skipped, exit 0 at :105-107. Existing NOTSET placeholder skip at :31. Coverage was not measured.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-fix-review.md:14: 8. Historical rows: diagnostic-disposition.md:9-21 records new local evidence only, preserving historical pending rows and making no environment explanation. Its still-required applied-review sentence describes the earlier checkpoint, not this completed review.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-fix-review.md:15: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-fix-review.md:16: ## Findings and result
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-fix-review.md:17: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-fix-review.md:18: No defect found. All four checklist answers are no: ac-outcome-missing, false-claim, harmful-effect, quoted-constraint-breach. No anchors required and no confirmed blocker. Parent-derived result: compliant for the bounded applied fix, not a successful model-backed custom job or a coverage measurement.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-fix-review.md:19: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/applied-fix-review.md:20: All-no form Note: diagnostic-disposition.md:21 still says independent applied-fix review is required. This was true when Task 2 wrote the checkpoint. This separate persisted review and the later Task 4 ledger record provide the new evidence; the earlier checkpoint is retained unchanged. The reviewer requested no code change. This note does not block completion.

Full task-created file, source line numbers: .dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:1: Fresh related-test observation: 2026-11-24T15:29:44Z
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:2: Checkout: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:3: Commit: 720cbaf96653c1c983497ba480f76ca6e60e5369
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:4: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:5: Command: PYTHONDONTWRITEBYTECODE=1 uv run --no-sync pytest tests/swarm/test_cli_registration.py tests/swarm/test_validate_lenses_cmd.py tests/swarm/test_scaffold_cmd.py tests/swarm/test_custom_prompt_dir.py tests/swarm/test_custom_prompt_dir_injection_guard.py --cov=superclaude.cli.swarm --cov-report=term-missing -p no:cacheprovider
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:6: ERROR: usage: pytest [options] [file_or_dir] [file_or_dir] [...]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:7: pytest: error: unrecognized arguments: --cov=superclaude.cli.swarm --cov-report=term-missing
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:8:   inifile: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help/pyproject.toml
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:9:   rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:10: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:11: Coverage-command exit: 4
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:12: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:13: Coverage tooling is unavailable; do not install it. Running the identical five files without coverage arguments, not dropping any test file.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:14: Command: PYTHONDONTWRITEBYTECODE=1 uv run --no-sync pytest tests/swarm/test_cli_registration.py tests/swarm/test_validate_lenses_cmd.py tests/swarm/test_scaffold_cmd.py tests/swarm/test_custom_prompt_dir.py tests/swarm/test_custom_prompt_dir_injection_guard.py -p no:cacheprovider
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:15: ========================================== test session starts ===========================================
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:16: platform linux -- Python 3.13.5, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help/.venv/bin/python
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:17: SuperClaude: 6.1.0
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:18: rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:19: configfile: pyproject.toml
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:20: plugins: anyio-4.16.0, superclaude-6.1.0
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:21: collecting ... collected 81 items
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:22: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:23: tests/swarm/test_cli_registration.py::test_swarm_group_is_top_level_command PASSED                 [  1%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:24: tests/swarm/test_cli_registration.py::test_swarm_not_nested_under_other_groups PASSED              [  2%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:25: tests/swarm/test_cli_registration.py::test_swarm_help_exits_zero PASSED                            [  3%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:26: tests/swarm/test_cli_registration.py::test_validate_lenses_help_uses_jobspec_custom_prompt_dir PASSED [  4%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:27: tests/swarm/test_cli_registration.py::test_scaffold_help_uses_jobspec_custom_prompt_dir PASSED     [  6%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:28: tests/swarm/test_cli_registration.py::test_run_rejects_custom_prompt_dir_option PASSED             [  7%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:29: tests/swarm/test_cli_registration.py::test_swarm_help_lists_all_eight_placeholders PASSED          [  8%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:30: tests/swarm/test_cli_registration.py::test_swarm_group_registers_all_eight_placeholders PASSED     [  9%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:31: tests/swarm/test_cli_registration.py::test_placeholder_exits_non_zero_with_message[NOTSET] SKIPPED [ 11%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:32: tests/swarm/test_cli_registration.py::test_swarm_module_imports_without_error PASSED               [ 12%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:33: tests/swarm/test_validate_lenses_cmd.py::test_validate_lenses_cmd_registered_on_swarm_group PASSED [ 13%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:34: tests/swarm/test_validate_lenses_cmd.py::test_validate_lenses_cmd_advertises_warning_mode_flag PASSED [ 14%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:35: tests/swarm/test_validate_lenses_cmd.py::test_clean_registry_exits_zero PASSED                     [ 16%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:36: tests/swarm/test_validate_lenses_cmd.py::test_clean_registry_warning_mode_also_exits_zero PASSED   [ 17%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:37: tests/swarm/test_validate_lenses_cmd.py::test_bundled_registry_via_main_group_exits_zero PASSED    [ 18%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:38: tests/swarm/test_validate_lenses_cmd.py::test_failing_registry_exits_nonzero_by_default PASSED     [ 19%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:39: tests/swarm/test_validate_lenses_cmd.py::test_failure_diagnostics_name_the_lens_entry PASSED       [ 20%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:40: tests/swarm/test_validate_lenses_cmd.py::test_multiple_failures_each_surface PASSED                [ 22%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:41: tests/swarm/test_validate_lenses_cmd.py::test_failure_diagnostic_format_is_grep_friendly PASSED    [ 23%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:42: tests/swarm/test_validate_lenses_cmd.py::test_failing_registry_warning_mode_exits_zero PASSED      [ 24%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:43: tests/swarm/test_validate_lenses_cmd.py::test_warning_mode_diagnostic_lines_match_blocking_mode PASSED [ 25%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:44: tests/swarm/test_validate_lenses_cmd.py::test_custom_only_registry_exits_zero PASSED               [ 27%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:45: tests/swarm/test_validate_lenses_cmd.py::test_ok_summary_reports_inspected_count PASSED            [ 28%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:46: tests/swarm/test_scaffold_cmd.py::test_scaffold_cmd_registered_on_swarm_group PASSED               [ 29%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:47: tests/swarm/test_scaffold_cmd.py::test_scaffold_help_lists_lens_and_output_flags PASSED            [ 30%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:48: tests/swarm/test_scaffold_cmd.py::test_scaffold_requires_lens_flag PASSED                          [ 32%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:49: tests/swarm/test_scaffold_cmd.py::test_scaffold_stdout_emits_valid_json_per_lens[bare-review] PASSED [ 33%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:50: tests/swarm/test_scaffold_cmd.py::test_scaffold_stdout_emits_valid_json_per_lens[refactor-find] PASSED [ 34%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:51: tests/swarm/test_scaffold_cmd.py::test_scaffold_stdout_emits_valid_json_per_lens[edge-case-hunt] PASSED [ 35%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:52: tests/swarm/test_scaffold_cmd.py::test_scaffold_stdout_emits_valid_json_per_lens[spec-completeness] PASSED [ 37%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:53: tests/swarm/test_scaffold_cmd.py::test_scaffold_stdout_emits_valid_json_per_lens[feasibility-probe] PASSED [ 38%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:54: tests/swarm/test_scaffold_cmd.py::test_scaffold_stdout_emits_valid_json_per_lens[troubleshoot-hypothesis] PASSED [ 39%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:55: tests/swarm/test_scaffold_cmd.py::test_scaffold_stdout_emits_valid_json_per_lens[doc-completeness] PASSED [ 40%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:56: tests/swarm/test_scaffold_cmd.py::test_scaffold_stdout_emits_valid_json_per_lens[reflect-review] PASSED [ 41%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:57: tests/swarm/test_scaffold_cmd.py::test_scaffold_output_validates_via_schema[bare-review] PASSED    [ 43%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:58: tests/swarm/test_scaffold_cmd.py::test_scaffold_output_validates_via_schema[refactor-find] PASSED  [ 44%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:59: tests/swarm/test_scaffold_cmd.py::test_scaffold_output_validates_via_schema[edge-case-hunt] PASSED [ 45%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:60: tests/swarm/test_scaffold_cmd.py::test_scaffold_output_validates_via_schema[spec-completeness] PASSED [ 46%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:61: tests/swarm/test_scaffold_cmd.py::test_scaffold_output_validates_via_schema[feasibility-probe] PASSED [ 48%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:62: tests/swarm/test_scaffold_cmd.py::test_scaffold_output_validates_via_schema[troubleshoot-hypothesis] PASSED [ 49%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:63: tests/swarm/test_scaffold_cmd.py::test_scaffold_output_validates_via_schema[doc-completeness] PASSED [ 50%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:64: tests/swarm/test_scaffold_cmd.py::test_scaffold_output_validates_via_schema[reflect-review] PASSED [ 51%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:65: tests/swarm/test_scaffold_cmd.py::test_scaffold_output_validates_via_swarm_validate PASSED         [ 53%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:66: tests/swarm/test_scaffold_cmd.py::test_scaffold_stdout_carries_injection_guard_substring PASSED    [ 54%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:67: tests/swarm/test_scaffold_cmd.py::test_scaffold_stdout_is_pure_json PASSED                         [ 55%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:68: tests/swarm/test_scaffold_cmd.py::test_scaffold_output_writes_file_atomically PASSED               [ 56%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:69: tests/swarm/test_scaffold_cmd.py::test_scaffold_output_short_flag_alias PASSED                     [ 58%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:70: tests/swarm/test_scaffold_cmd.py::test_scaffold_output_creates_parent_directory PASSED             [ 59%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:71: tests/swarm/test_scaffold_cmd.py::test_scaffold_output_overwrites_existing_file PASSED             [ 60%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:72: tests/swarm/test_scaffold_cmd.py::test_scaffold_rejects_custom_lens PASSED                         [ 61%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:73: tests/swarm/test_scaffold_cmd.py::test_scaffold_rejects_unknown_lens PASSED                        [ 62%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:74: tests/swarm/test_scaffold_cmd.py::test_scaffold_via_main_swarm_group PASSED                        [ 64%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:75: tests/swarm/test_custom_prompt_dir.py::test_read_custom_prompt_dir_happy_path_returns_trio PASSED  [ 65%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:76: tests/swarm/test_custom_prompt_dir.py::test_read_custom_prompt_dir_accepts_pathlike PASSED         [ 66%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:77: tests/swarm/test_custom_prompt_dir.py::test_read_custom_prompt_dir_empty_meta_yields_empty_dict PASSED [ 67%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:78: tests/swarm/test_custom_prompt_dir.py::test_read_custom_prompt_dir_preserves_verbatim_content PASSED [ 69%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:79: tests/swarm/test_custom_prompt_dir.py::test_read_custom_prompt_dir_missing_directory_raises PASSED [ 70%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:80: tests/swarm/test_custom_prompt_dir.py::test_read_custom_prompt_dir_path_is_file_raises PASSED      [ 71%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:81: tests/swarm/test_custom_prompt_dir.py::test_read_custom_prompt_dir_missing_file_raises[system.txt] PASSED [ 72%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:82: tests/swarm/test_custom_prompt_dir.py::test_read_custom_prompt_dir_missing_file_raises[user.txt] PASSED [ 74%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:83: tests/swarm/test_custom_prompt_dir.py::test_read_custom_prompt_dir_missing_file_raises[meta.yaml] PASSED [ 75%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:84: tests/swarm/test_custom_prompt_dir.py::test_read_custom_prompt_dir_batches_missing_files PASSED    [ 76%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:85: tests/swarm/test_custom_prompt_dir.py::test_read_custom_prompt_dir_missing_substring_raises PASSED [ 77%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:86: tests/swarm/test_custom_prompt_dir.py::test_read_custom_prompt_dir_substring_default_disabled PASSED [ 79%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:87: tests/swarm/test_custom_prompt_dir.py::test_read_custom_prompt_dir_guard_uses_central_helper_path_label PASSED [ 80%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:88: tests/swarm/test_custom_prompt_dir.py::test_read_custom_prompt_dir_invalid_yaml_raises PASSED      [ 81%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:89: tests/swarm/test_custom_prompt_dir.py::test_read_custom_prompt_dir_non_mapping_meta_raises PASSED  [ 82%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:90: tests/swarm/test_custom_prompt_dir.py::test_read_custom_prompt_dir_scalar_meta_raises PASSED       [ 83%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:91: tests/swarm/test_custom_prompt_dir.py::test_custom_prompt_dir_contents_round_trip_into_manifest PASSED [ 85%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:92: tests/swarm/test_custom_prompt_dir.py::test_read_custom_prompt_dir_meta_variables_survive_json_round_trip PASSED [ 86%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:93: tests/swarm/test_custom_prompt_dir.py::test_run_preflight_reads_custom_prompt_dir_and_passes_guard PASSED [ 87%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:94: tests/swarm/test_custom_prompt_dir.py::test_run_preflight_custom_dir_missing_system_substring_raises PASSED [ 88%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:95: tests/swarm/test_custom_prompt_dir.py::test_run_preflight_custom_dir_missing_raises PASSED         [ 90%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:96: tests/swarm/test_custom_prompt_dir.py::test_run_preflight_custom_dir_auto_inject_guard PASSED      [ 91%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:97: tests/swarm/test_custom_prompt_dir.py::test_run_preflight_custom_dir_populates_prompt_variables PASSED [ 92%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:98: tests/swarm/test_custom_prompt_dir_injection_guard.py::test_custom_prompt_dir_rejects_missing_substring PASSED [ 93%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:99: tests/swarm/test_custom_prompt_dir_injection_guard.py::test_custom_prompt_dir_accepts_substring_present PASSED [ 95%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:100: tests/swarm/test_custom_prompt_dir_injection_guard.py::test_custom_prompt_dir_failure_message_identifies_rule PASSED [ 96%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:101: tests/swarm/test_custom_prompt_dir_injection_guard.py::test_same_fixture_yields_identical_rejection_on_both_paths PASSED [ 97%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:102: tests/swarm/test_custom_prompt_dir_injection_guard.py::test_mutation_bypassing_predicate_flips_custom_prompt_dir_verdict PASSED [ 98%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:103: tests/swarm/test_custom_prompt_dir_injection_guard.py::test_mutation_skipping_guard_call_would_fail_parity PASSED [100%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:104: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:105: ===================================== 80 passed, 1 skipped in 0.95s ======================================
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:106: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/related-tests-green.txt:107: Observed five-file test exit: 0

Full task-created file, source line numbers: .dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:1: Fresh repaired public observation: 2026-11-24T15:29:46Z
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:2: Checkout: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:3: Commit: 720cbaf96653c1c983497ba480f76ca6e60e5369
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:4: Module origin command: PYTHONDONTWRITEBYTECODE=1 uv run --no-sync python -c 'import superclaude.cli.swarm.commands as commands; print(commands.__file__)'
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:5: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help/src/superclaude/cli/swarm/commands.py
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:6: Existing temporary directory (same as before): /tmp/swarm-help-parser.wYfp70Qi
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:7: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:8: Command: uv run --no-sync superclaude swarm validate-lenses --help
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:9: Usage: superclaude swarm validate-lenses [OPTIONS]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:10: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:11:   Validate the bundled LENSES registry (FR-008 / T02.20).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:12: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:13:   Runs the COMP-023 five-assertion lens validator over every entry in
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:14:   :data:`superclaude.cli.swarm.lenses.LENSES`. The ``custom`` escape hatch (COMP-026) is
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:15:   intentionally skipped. Directory-backed custom prompts use the JobSpec ``custom_prompt_dir``
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:16:   field with ``lens: custom`` and are loaded and validated at preflight (T02.05 / T02.07). Custom
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:17:   specs may also supply inline prompts without a directory.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:18: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:19:   Exit codes (OQ-010 resolution -- see module docstring):
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:20: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:21:       * 0 -- every non-custom entry passes its five COMP-023       assertions, OR ``--warning-
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:22:       mode`` is set and failures are       emitted as warnings rather than errors.     * 1 -- one
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:23:       or more entries failed validation and       ``--warning-mode`` is not set (default blocking
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:24:       branch).     * 2 -- reserved for future usage errors (no path argument       accepted today,
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:25:       but kept consistent with :func:`validate_cmd`       for a future ``--registry-path`` opt-
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:26:       in).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:27: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:28:   Output:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:29: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:30:       * Success: one-line OK summary on stdout naming the registry       size and the count of
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:31:       inspected (non-custom) entries.     * Failure: structured per-entry diagnostic block on
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:32:       stderr,       one line per failing entry, format       ``- <rule> @ <path>: <message>
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:33:       (lens=<lens_name>)``.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:34: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:35: Options:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:36:   --warning-mode  OQ-010 warning branch: emit per-entry diagnostics on stderr but exit 0 even when
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:37:                   entries fail. Use for pre-commit hooks and non-blocking CI advisories. Default
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:38:                   is blocking (exit 1 on any failure).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:39:   -h, --help      Show this message and exit.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:40: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:41: Observed exit status: 0
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:42: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:43: Command: uv run --no-sync superclaude swarm scaffold --help
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:44: Usage: superclaude swarm scaffold [OPTIONS]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:45: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:46:   Emit a starter JobSpec for the named lens (FR-006 / T07.09).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:47: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:48:   Generates a fully-populated DM-001 JobSpec for ``--lens NAME`` so operators have a valid
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:49:   baseline they can edit instead of authoring the spec from scratch. The emitted spec passes
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:50:   ``swarm validate`` out of the box -- the only fields the operator MUST override before invoking
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:51:   ``swarm run`` are ``target.path`` (placeholder ``""``) and ``output.dir`` (placeholder ``""``).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:52:   Model IDs are filled with ``lens-default-model-<i>`` placeholders that schema-validate but never
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:53:   reach the wire (the transport defaults to ``stub`` for the same safe-quick-dispatch reasoning as
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:54:   ``swarm run --lens``).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:55: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:56:   Exit codes:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:57: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:58:       * 0 -- starter spec rendered successfully (to stdout, or to       ``--output`` when
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:59:       supplied).     * 2 -- usage error: lens unknown, lens is the ``custom`` escape       hatch
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:60:       (no registry defaults to expand from), or ``--output``       path is unwritable.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:61: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:62: Options:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:63:   --lens TEXT        Lens to scaffold a starter JobSpec for (e.g. bare-review). Expands lens
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:64:                      defaults (system/user prompts, recipe, workers, line_cap, next-command
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:65:                      template) into a full DM-001 JobSpec the operator can edit. ``custom`` and
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:66:                      unknown lens names are rejected -- ``custom`` is the FR-021 escape hatch with
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:67:                      no registry defaults to expand from. Directory-backed custom prompts use the
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:68:                      JobSpec ``custom_prompt_dir`` field with ``lens: custom`` and are loaded at
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:69:                      preflight; custom specs may instead supply inline prompts without a
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:70:                      directory.  [required]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:71:   -o, --output FILE  Write the starter JobSpec to PATH atomically (tmp + os.replace). When
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:72:                      omitted, the JSON document is emitted to stdout so it can be piped straight
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:73:                      into ``swarm validate`` or redirected with the shell of choice.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:74:   -h, --help         Show this message and exit.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:75: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:76: Observed exit status: 0
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:77: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:78: Command: uv run --no-sync superclaude swarm run --custom-prompt-dir /tmp/swarm-help-parser.wYfp70Qi
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:79: Usage: superclaude swarm run [OPTIONS] [SPEC_PATH]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:80: Try 'superclaude swarm run --help' for help.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:81: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:82: Error: No such option '--custom-prompt-dir'.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:83: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:84: Observed exit status: 2
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:85: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:86: Directory entries after parser probe:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:87: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:88: Comparison with public-before.txt (new analysis, not CLI output):
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:89: The validate-lenses command is identical before:8 and after:8. Both exit 0 (before:39, after:41). The stale option in before:15-16 is replaced by JobSpec custom_prompt_dir, lens: custom, preflight validation and optional inline prompts in after:15-17.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:90: The scaffold command is identical before:41 and after:43. Both exit 0 (before:71, after:76). The stale option in before:64-66 is replaced by the supported field/lens binding and optional inline route in after:66-70; no-registry-defaults rejection remains explicit.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:91: The run-parser command and existing temporary directory are identical before:73 and after:78. Both exit 2 (before:78, after:84), with the same No such option diagnostic (before:77, after:82); the directory remains empty. No model job ran.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/public-after.txt:92: These captures use uv run --no-sync to avoid dependency synchronization. This is fresh repaired public evidence, not a change to historical diagnostic rows or a successful custom-job claim.

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
