start=47cecfa862029804bdc984cbc403745b74a4fe68
Review one task for spec compliance.

Task brief: ## Task 3: Replace the validate-lenses help description

Depends on: Task 2

In `src/superclaude/cli/swarm/commands.py`, replace only the custom-prompt description in the `validate_lenses_cmd` docstring. Describe directory-backed custom prompts as supplied by the JobSpec `custom_prompt_dir` field with `lens: custom` and loaded/validated at preflight, while leaving inline custom prompts valid and custom excluded from bundled registry validation. Read the current docstring, Task 1's test and `./artifacts/validate-help-red.txt`, the custom-directory note in `docs/swarm/command-reference.md`, `_apply_custom_prompt_dir` in `src/superclaude/cli/swarm/preflight.py`, and `_custom_prompt_dir_lens_failures` in `src/superclaude/cli/swarm/schema.py` before editing. Only tests authored by prior tasks may already differ.

Acceptance criteria:
- T3.AC1: Only this docstring block changes in the product source. `validate_lenses_cmd` retains its `_run_validate_lenses` call, `--warning-mode`, exit behavior, registration and custom-registry exclusion; no option, loader or schema changes are introduced.
- T3.AC2: Task 1's public-root help test now passes, while Task 2's scaffold help test still fails for the known stale scaffold description and its parser rejection guard still passes. Retain concrete commands, outputs and observed statuses in `./artifacts/validate-help-green.txt`.
- T3.AC3: Run the existing `tests/swarm/test_validate_lenses_cmd.py` suite with UV and retain its result in `./artifacts/validate-lenses-tests.txt`. This checks existing dependent behavior, including warning mode and custom-only registry handling, rather than replacing it with help-only assertions.
- T3.AC4: The description is explicit about the JobSpec field and custom lens without implying custom prompts must always come from a directory. Preserve the existing registration in `src/superclaude/cli/swarm/__init__.py` and every prompt-loading, guard and metadata contract.
Global constraints: - This package is a plan only. Product edits and test execution require a later explicit implementation instruction. That future instruction may authorize this plan's tests and CLI help/parser probes, not model jobs, commits, pushes, GitHub writes or new worktrees.
- Work only in the assigned isolated checkout. Change product text only in the two help-producing blocks of `src/superclaude/cli/swarm/commands.py`; author regressions only in `tests/swarm/test_cli_registration.py`. Do not clean up internal comments or adjacent diagnostics.
- Do not add `--custom-prompt-dir`, change command registrations or options, prompt-loading semantics, inline custom specs, injection guards or metadata validation. Directory-backed prompts are one supported route, not a requirement for every custom spec. Preserve custom-lens exclusion from registry validation and scaffold rejection of custom/unknown lenses.
- Historical diagnosis: `.dev/troubleshoot/bug-swarm-custom-prompt-help-20261123191427/REPORT.md` remains blocked/partial. The absent repaired public witness and independent applied-fix review are still unproven. Planning and static source inspection do not pass those checks.
- Historical evidence came from commit db57e231863078dbbb8e4e5fb37a61371c89806c; the transferred checkout started at 720cbaf96653c1c983497ba480f76ca6e60e5369. Original absolute paths and line numbers are provenance, not lookup destinations. Use current repo-relative sources and new local captures; never touch the shared original checkout.
- Preserve every transferred artifact unchanged, including the five pending diagnostic comparison rows and copied counter snapshot. Do not run `counter-update.py`, edit a shared diagnostic counter or lock, retroactively mark earlier probes passed, or claim an environmental explanation. Any later disposition must be a new evidence-backed record under this package's `./artifacts/`.
- All new evidence belongs under `./artifacts/`; retain outputs, commands, timestamps, checkout/module provenance and observed exit statuses. Use UV for Python operations and environment references for secrets. No credentials may be written or logged.
- `.dev/tasks/` is staged, including this package and its artifacts; staging does not authorize committing. Do not stage unrelated diagnostic packages or generated `.claude/` mirrors.
- Final whole-plan verification, independent applied-fix review and progress-ledger management belong to the executor. Do not treat this plan's advisory pre-review as an applied-fix review. Report only checks actually observed, and preserve any remaining blocker.
Start sha: 47cecfa862029804bdc984cbc403745b74a4fe68
Diff against the start snapshot: diff --git a/src/superclaude/cli/swarm/commands.py b/src/superclaude/cli/swarm/commands.py
index 8577805b1..0ce5048b3 100644
--- a/src/superclaude/cli/swarm/commands.py
+++ b/src/superclaude/cli/swarm/commands.py
@@ -434,9 +434,10 @@ def validate_lenses_cmd(warning_mode: bool) -> None:
 
     Runs the COMP-023 five-assertion lens validator over every entry in
     :data:`superclaude.cli.swarm.lenses.LENSES`. The ``custom`` escape
-    hatch (COMP-026) is intentionally skipped — its prompt body flows in
-    from ``--custom-prompt-dir`` at preflight and is validated on that
-    path (T02.05 / T02.07).
+    hatch (COMP-026) is intentionally skipped. Directory-backed custom
+    prompts use the JobSpec ``custom_prompt_dir`` field with ``lens: custom``
+    and are loaded and validated at preflight (T02.05 / T02.07). Custom
+    specs may also supply inline prompts without a directory.
 
     Exit codes (OQ-010 resolution -- see module docstring):
 

Full task-created file, source line numbers: .dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:1: Task 3 intermediate regression states after validate-lenses docstring edit
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:2: Timestamp: 2026-11-24T15:22:34Z
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:3: Command: PYTHONDONTWRITEBYTECODE=1 uv run --no-sync pytest tests/swarm/test_cli_registration.py::test_validate_lenses_help_uses_jobspec_custom_prompt_dir tests/swarm/test_cli_registration.py::test_scaffold_help_uses_jobspec_custom_prompt_dir tests/swarm/test_cli_registration.py::test_run_rejects_custom_prompt_dir_option -p no:cacheprovider
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:4: ========================================== test session starts ===========================================
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:5: platform linux -- Python 3.13.5, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help/.venv/bin/python
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:6: SuperClaude: 6.1.0
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:7: rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:8: configfile: pyproject.toml
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:9: plugins: anyio-4.16.0, superclaude-6.1.0
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:10: collecting ... collected 3 items
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:11: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:12: tests/swarm/test_cli_registration.py::test_validate_lenses_help_uses_jobspec_custom_prompt_dir PASSED [ 33%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:13: tests/swarm/test_cli_registration.py::test_scaffold_help_uses_jobspec_custom_prompt_dir FAILED     [ 66%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:14: tests/swarm/test_cli_registration.py::test_run_rejects_custom_prompt_dir_option PASSED             [100%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:15: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:16: ================================================ FAILURES ================================================
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:17: ___________________________ test_scaffold_help_uses_jobspec_custom_prompt_dir ____________________________
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:18: tests/swarm/test_cli_registration.py:122: in test_scaffold_help_uses_jobspec_custom_prompt_dir
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:19:     assert "--custom-prompt-dir" not in help_text, result.output
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:20: E   AssertionError: Usage: main swarm scaffold [OPTIONS]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:21: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:22: E       Emit a starter JobSpec for the named lens (FR-006 / T07.09).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:23: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:24: E       Generates a fully-populated DM-001 JobSpec for ``--lens NAME`` so operators
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:25: E       have a valid baseline they can edit instead of authoring the spec from
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:26: E       scratch. The emitted spec passes ``swarm validate`` out of the box -- the only
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:27: E       fields the operator MUST override before invoking ``swarm run`` are
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:28: E       ``target.path`` (placeholder ``""``) and ``output.dir`` (placeholder ``""``).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:29: E       Model IDs are filled with ``lens-default-model-<i>`` placeholders that schema-
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:30: E       validate but never reach the wire (the transport defaults to ``stub`` for the
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:31: E       same safe-quick-dispatch reasoning as ``swarm run --lens``).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:32: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:33: E       Exit codes:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:34: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:35: E           * 0 -- starter spec rendered successfully (to stdout, or to
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:36: E           ``--output`` when supplied).     * 2 -- usage error: lens unknown, lens is
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:37: E           the ``custom`` escape       hatch (no registry defaults to expand from),
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:38: E           or ``--output``       path is unwritable.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:39: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:40: E     Options:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:41: E       --lens TEXT        Lens to scaffold a starter JobSpec for (e.g. bare-review).
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:42: E                          Expands lens defaults (system/user prompts, recipe,
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:43: E                          workers, line_cap, next-command template) into a full
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:44: E                          DM-001 JobSpec the operator can edit. ``custom`` and
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:45: E                          unknown lens names are rejected -- ``custom`` is the FR-021
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:46: E                          escape hatch whose prompts flow in from --custom-prompt-dir
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:47: E                          at preflight, so it has no registry defaults to expand
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:48: E                          from.  [required]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:49: E       -o, --output FILE  Write the starter JobSpec to PATH atomically (tmp +
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:50: E                          os.replace). When omitted, the JSON document is emitted to
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:51: E                          stdout so it can be piped straight into ``swarm validate``
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:52: E                          or redirected with the shell of choice.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:53: E       -h, --help         Show this message and exit.
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:54: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:55: E   assert '--custom-prompt-dir' not in 'Usage:mains...sageandexit.'
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:56: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:57: E     '--custom-prompt-dir' is contained here:
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:58: E       Usage:mainswarmscaffold[OPTIONS]EmitastarterJobSpecforthenamedlens(FR-006/T07.09).Generatesafully-populatedDM-001JobSpecfor``--lensNAME``sooperatorshaveavalidbaselinetheycaneditinsteadofauthoringthespecfromscratch.Theemittedspecpasses``swarmvalidate``outofthebox--theonlyfieldstheoperatorMUSToverridebeforeinvoking``swarmrun``are``target.path``(placeholder``""``)and``output.dir``(placeholder``""``).ModelIDsarefilledwith``lens-default-model-<i>``placeholdersthatschema-validatebutneverreachthewire(thetransportdefaultsto``stub``forthesamesa...
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:59: E     
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:60: E     ...Full output truncated, use '-vv' to show
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:61: ======================================== short test summary info =========================================
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:62: FAILED tests/swarm/test_cli_registration.py::test_scaffold_help_uses_jobspec_custom_prompt_dir - Assert...
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:63: ====================================== 1 failed, 2 passed in 0.77s =======================================
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:64: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-help-green.txt:65: Observed pytest exit status: 1 (expected 1: scaffold remains stale)

Full task-created file, source line numbers: .dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:1: Command: PYTHONDONTWRITEBYTECODE=1 uv run --no-sync pytest tests/swarm/test_validate_lenses_cmd.py -p no:cacheprovider
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:2: ========================================== test session starts ===========================================
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:3: platform linux -- Python 3.13.5, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help/.venv/bin/python
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:4: SuperClaude: 6.1.0
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:5: rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:6: configfile: pyproject.toml
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:7: plugins: anyio-4.16.0, superclaude-6.1.0
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:8: collecting ... collected 13 items
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:9: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:10: tests/swarm/test_validate_lenses_cmd.py::test_validate_lenses_cmd_registered_on_swarm_group PASSED [  7%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:11: tests/swarm/test_validate_lenses_cmd.py::test_validate_lenses_cmd_advertises_warning_mode_flag PASSED [ 15%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:12: tests/swarm/test_validate_lenses_cmd.py::test_clean_registry_exits_zero PASSED                     [ 23%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:13: tests/swarm/test_validate_lenses_cmd.py::test_clean_registry_warning_mode_also_exits_zero PASSED   [ 30%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:14: tests/swarm/test_validate_lenses_cmd.py::test_bundled_registry_via_main_group_exits_zero PASSED    [ 38%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:15: tests/swarm/test_validate_lenses_cmd.py::test_failing_registry_exits_nonzero_by_default PASSED     [ 46%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:16: tests/swarm/test_validate_lenses_cmd.py::test_failure_diagnostics_name_the_lens_entry PASSED       [ 53%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:17: tests/swarm/test_validate_lenses_cmd.py::test_multiple_failures_each_surface PASSED                [ 61%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:18: tests/swarm/test_validate_lenses_cmd.py::test_failure_diagnostic_format_is_grep_friendly PASSED    [ 69%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:19: tests/swarm/test_validate_lenses_cmd.py::test_failing_registry_warning_mode_exits_zero PASSED      [ 76%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:20: tests/swarm/test_validate_lenses_cmd.py::test_warning_mode_diagnostic_lines_match_blocking_mode PASSED [ 84%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:21: tests/swarm/test_validate_lenses_cmd.py::test_custom_only_registry_exits_zero PASSED               [ 92%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:22: tests/swarm/test_validate_lenses_cmd.py::test_ok_summary_reports_inspected_count PASSED            [100%]
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:23: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:24: =========================================== 13 passed in 0.76s ===========================================
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:25: 
.dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-212501/artifacts/validate-lenses-tests.txt:26: Observed pytest exit status: 0

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
