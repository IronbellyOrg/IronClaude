# Codegraph grounding

## Run state

- index_state: fresh
- checked_at: 2026-11-23T19:57:44Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help
- access: mcp
- Readiness: 0 added, 0 modified, 0 removed. MCP access; CLI not used.

## Resolved symbols

- `src/superclaude/cli/swarm/commands.py`: graph outline resolves `validate_lenses_cmd` at 432 and `scaffold_cmd` at 3802; direct Reads confirm help producers at 435-439 and 3779-3786. Both stale descriptions remain in this checkout. Static confirmation only, not newly executed help/parser evidence.
- Direct Read of `src/superclaude/cli/swarm/preflight.py` 1569-1624 confirms `_apply_custom_prompt_dir` consumes the JobSpec field for the custom lens. No edit planned.
- Direct Read of `src/superclaude/cli/swarm/schema.py` 685-736 confirms `_custom_prompt_dir_lens_failures` permits inline custom prompts and rejects nonempty directory binding to a different lens. No edit planned.
- Direct Read of `docs/swarm/command-reference.md` 56-61 confirms JobSpec `custom_prompt_dir`, custom lens, not a run option. No documentation rewrite needed.
- `tests/swarm/test_cli_registration.py`: direct Read confirms root `main` plus CliRunner conventions and public-group help tests. Add public-help/parser regressions here without rewriting registration tests.
- Existing specialized tests: `tests/swarm/test_scaffold_cmd.py`, `tests/swarm/test_validate_lenses_cmd.py`, `tests/swarm/test_custom_prompt_dir.py`, `tests/swarm/test_custom_prompt_dir_injection_guard.py`. First two read at relevant registration/help sections; custom-directory tests located by Grep, not run.

### Phase structure (standard depth)

- Phase 1: validate-lenses regression. Inputs: source snapshot, historical report/captures, current producer and registration tests. Output: root-command help regression and red-run evidence. Checkpoint: expected help-content failure, not setup/import failure. Dependencies: none.
- Phase 2: scaffold/parser regressions. Inputs: same contracts plus current scaffold option help. Outputs: scaffold help regression, unknown-option parser guard and red/control logs. Checkpoint: both help cases red before product edits; parser control exit 2. Dependencies: Phase 1.
- Phase 3: validate-lenses help correction. Inputs: first regression and custom-directory contracts. Output: docstring correction plus focused green witness. Checkpoint: validate-lenses regression green; scaffold remains red. Dependencies: Phase 2.
- Phase 4: scaffold help correction. Inputs: second regression, option-help literal and prior evidence. Outputs: option-help correction and repaired public-surface evidence. Checkpoint: combined regressions and related suites pass; fresh help/parser captures retained; executor-owned independent review required. Dependencies: Phase 3.

## Dependents

- Graph callers for `validate_lenses_cmd`: 15/15 rows shown; graph impact for `scaffold_cmd`: 16 symbols reported at depth 1. These include imports and callback registrations, not direct Python call-site proof. No exhaustive whole-file blast-radius claim.
- `src/superclaude/cli/swarm/__init__.py` 136-154: direct Read confirms imports and `swarm_group.add_command(scaffold_cmd, name="scaffold")` / `add_command(validate_lenses_cmd, name="validate-lenses")`. Resolution: callback registration confirmed, not a direct invocation of the decorated command.
- `tests/swarm/test_cli_registration.py` 74-110: direct Read confirms root registration and `runner.invoke(main, ["swarm", "--help"])`. Public dependent/root-test pattern confirmed.
- `tests/swarm/test_validate_lenses_cmd.py` 145-150, 160-177 and 438-449: direct Read confirms `runner.invoke(validate_lenses_cmd, ...)` help, normal/warning and custom-only cases. Resolution: callback registration confirmed. Included in Task 3 and Task 4 acceptance.
- `tests/swarm/test_scaffold_cmd.py` 63-69, 88-119 and 250-274: direct Read confirms `runner.invoke(scaffold_cmd, ...)` help, valid output and custom/unknown rejection. Resolution: callback registration confirmed. Included in Task 4 acceptance.
- `tests/swarm/test_custom_prompt_dir.py`: searched reader/metadata/preflight tests. `tests/swarm/test_custom_prompt_dir_injection_guard.py` 1-74: direct Read confirms the guard-parity scope and imported enforcement/reader helpers. Both retained as existing related suites, not changed or claimed passed.
- No production behavior edit reaches loaders, schema or transport factories. Other graph rows are unverified dependency leads and not named as direct callers in the plan.
- Planning recovery note: the first Edit of this newly written grounding artifact was refused by the freshness hook until a tracked Read; performed that Read and retried the same edit. No alternate edit path used.

## Pre-check

- Wave 3 full structural gate observed PASS with UV standard-library read-only checker: workflow-plan/1.2, exact slug/source, four nonempty phases, four contiguous tasks, lower dependencies, acceptance bullets, relative operational paths and no placeholders/checklists/status.
- Source coverage: Task 1 covers validate help reproduction; Task 2 covers scaffold reproduction, unchanged parser and historical-row disposition; Task 3 corrects validate wording and preserves its dependents; Task 4 corrects scaffold wording, captures repaired public surfaces, runs related tests and requires executor-owned independent final review. Constraints preserve plan-only authority, isolation, all historical artifacts and counters, inline custom prompts, injection guards and metadata validation.
- Four tasks checked; all existing product/test/document/evidence inputs named by the tasks resolve from direct Reads or Glob. New regression names and package evidence files are clearly future outputs, not claims of already existing files.
- Three production symbols named for behavior grounding resolve: `validate_lenses_cmd`, `scaffold_cmd`, `_apply_custom_prompt_dir`; schema `_custom_prompt_dir_lens_failures` also read. Both public callback registrations confirmed. No task calls a graph dependency a direct caller.
- Additional unenumerated graph dependents: broader commands.py import consumers, remaining scaffold tests and validate-lenses CI tests. They are not edited; the plan names the specialized command suites and current registrations, and narrows the product diff to two human-facing help blocks. No whole-repository completeness claim.
- Pre-check count: 4 tasks checked, 0 unresolved existing paths/symbols, 0 unaccounted affected production registrations. Planning ran no pytest, public help, parser, model or product fix.
- Advisory reflect was invoked with `--mode pre --spec` this package's `source.md` and `--tasklist` its plan. A delegated general-purpose context attempted the loaded protocol and reported the Write refusal: `Subagents should return findings as text, not write report files. Include this content in your final response instead.` It did not bypass that boundary.
- Parent Glob after the refusal found only `source.md`, the plan and this grounding artifact; no reflection report, input snapshot or return contract was available on disk. Thus `reflect_status: failed`, `reflect_report_path: null`. No PASS/FAIL coverage verdict, finding counts or completed calibration/evidence gate can be accepted.
- Wave 4R cannot consume missing reflection finding counts. Remediation routing was not run and no plan was revised; missing results were not replaced with zero findings. Workflow's explicit failed-reflect rule proceeds to Wave 5 with an unresolved line, without authorizing execution.
- The delegated context also reported an unintended UV environment bootstrap/local-package installation during metadata hashing. This is a reported environment side effect, not product-test evidence; no cleanup was attempted. Parent git diff and cached diff lists remained empty, and status showed only the new task package and the previously transferred diagnostic package.
- Plan-only readiness: structural generation succeeded, independent advisory review remains uncompleted. Do not describe this as an independently approved plan or as repair proof. User authorized creation only; implementation remains unrequested.
