---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-createACheckedIm-20261123-212501
version: "1"
priority: Medium
created_date: "2026-11-23"
---

# Correct swarm custom-prompt help without changing its interface

Source: ./source.md
Goal: Both public swarm help descriptions explain directory-based custom prompts through the JobSpec `custom_prompt_dir` field with `lens: custom`, never through an unsupported option, with observed failing-then-passing regressions and unchanged parser/prompt-loading behavior.

## Constraints

- This package is a plan only. Product edits and test execution require a later explicit implementation instruction. That future instruction may authorize this plan's tests and CLI help/parser probes, not model jobs, commits, pushes, GitHub writes or new worktrees.
- Work only in the assigned isolated checkout. Change product text only in the two help-producing blocks of `src/superclaude/cli/swarm/commands.py`; author regressions only in `tests/swarm/test_cli_registration.py`. Do not clean up internal comments or adjacent diagnostics.
- Do not add `--custom-prompt-dir`, change command registrations or options, prompt-loading semantics, inline custom specs, injection guards or metadata validation. Directory-backed prompts are one supported route, not a requirement for every custom spec. Preserve custom-lens exclusion from registry validation and scaffold rejection of custom/unknown lenses.
- Historical diagnosis: `.dev/troubleshoot/bug-swarm-custom-prompt-help-20261123191427/REPORT.md` remains blocked/partial. The absent repaired public witness and independent applied-fix review are still unproven. Planning and static source inspection do not pass those checks.
- Historical evidence came from commit db57e231863078dbbb8e4e5fb37a61371c89806c; the transferred checkout started at 720cbaf96653c1c983497ba480f76ca6e60e5369. Original absolute paths and line numbers are provenance, not lookup destinations. Use current repo-relative sources and new local captures; never touch the shared original checkout.
- Preserve every transferred artifact unchanged, including the five pending diagnostic comparison rows and copied counter snapshot. Do not run `counter-update.py`, edit a shared diagnostic counter or lock, retroactively mark earlier probes passed, or claim an environmental explanation. Any later disposition must be a new evidence-backed record under this package's `./artifacts/`.
- All new evidence belongs under `./artifacts/`; retain outputs, commands, timestamps, checkout/module provenance and observed exit statuses. Use UV for Python operations and environment references for secrets. No credentials may be written or logged.
- `.dev/tasks/` is staged, including this package and its artifacts; staging does not authorize committing. Do not stage unrelated diagnostic packages or generated `.claude/` mirrors.
- Final whole-plan verification, independent applied-fix review and progress-ledger management belong to the executor. Do not treat this plan's advisory pre-review as an applied-fix review. Report only checks actually observed, and preserve any remaining blocker.

## Phase 1: Reproduce validate-lenses help drift

## Task 1: Add the public validate-lenses help regression

Add a new validate-lenses help regression to `tests/swarm/test_cli_registration.py`, using its existing `CliRunner` and root `main` imports to invoke `main` with `swarm validate-lenses --help`. Name the new test clearly for the custom-prompt help contract. Read the historical report's Evidence, Proposed Fix and Next Steps sections, `doc-context.md`, `runtime-entrypoint.md` and `validate-lenses-help.txt` in the transferred diagnostic package. Confirm the current `validate_lenses_cmd` help-producing docstring in `src/superclaude/cli/swarm/commands.py` and registration in `src/superclaude/cli/swarm/__init__.py` before authoring assertions. Ground expected wording in `docs/swarm/command-reference.md` (the note explaining the directory is not a run flag), `_apply_custom_prompt_dir` in `src/superclaude/cli/swarm/preflight.py`, and `_custom_prompt_dir_lens_failures` in `src/superclaude/cli/swarm/schema.py`.

Acceptance criteria:
- The new test invokes the root public command, requires exit 0, rejects the exact token `--custom-prompt-dir`, and positively requires JobSpec, `custom_prompt_dir` and custom-lens guidance. Normalize whitespace rather than pinning Click's wrapping or an entire help transcript.
- Before either product edit, run the new test through `uv run pytest` with its concrete node id. Preserve command, checkout/module origin, timestamp, output and observed nonzero status in `./artifacts/validate-help-red.txt`. A missing import, collection error or unrelated failure does not count as reproducing the bug.
- The observed failure is caused by the stale help contract in `validate_lenses_cmd`, not a mocked helper. If the current public help already satisfies the regression or the expected mismatch cannot be reproduced, stop implementation and report the conflict rather than applying a speculative wording change.
- Only the regression test is added; `validate_lenses_cmd`, `scaffold_cmd`, registry behavior and existing registration tests remain unchanged at this checkpoint.

## Phase 2: Reproduce scaffold help drift and pin parser rejection

## Task 2: Add scaffold help and unsupported-option regressions

Depends on: Task 1

Add a scaffold help regression and an unsupported-option parser regression in `tests/swarm/test_cli_registration.py` using the existing root `main` plus `CliRunner` pattern. Read the `scaffold_cmd` lens-option help in `src/superclaude/cli/swarm/commands.py`, its registration in `src/superclaude/cli/swarm/__init__.py`, existing help/rejection tests in `tests/swarm/test_scaffold_cmd.py`, and the transferred `scaffold-help.txt`, `run-rejection.txt` and `diagnosability-tasklist.md`. The reference contract remains the custom-directory note in `docs/swarm/command-reference.md` and the schema/preflight symbols named in Task 1.

Acceptance criteria:
- The scaffold regression invokes `main` with `swarm scaffold --help`, expects exit 0, rejects `--custom-prompt-dir`, and positively requires JobSpec, `custom_prompt_dir` and custom-lens guidance. Assert semantic tokens after whitespace normalization, not full-line formatting. The text must not imply every custom spec needs a directory.
- The parser regression invokes `main` with `swarm run --custom-prompt-dir` and a temporary directory argument, expects exit 2 and an unknown-option diagnostic naming the exact rejected option. It never launches a swarm job or calls a model; the temporary directory remains unchanged.
- Before product edits, run both new help cases and the parser guard with concrete pytest node ids. Both help cases must fail for their expected content mismatch while the parser guard passes. Preserve commands, timestamps, outputs and individual exit statuses in `./artifacts/scaffold-help-red.txt` and `./artifacts/parser-before.txt`; preserve Task 1's red evidence unchanged.
- Capture fresh public CLI baselines using `uv run superclaude swarm validate-lenses --help`, `uv run superclaude swarm scaffold --help`, and `uv run superclaude swarm run --custom-prompt-dir` followed by an existing temporary directory. Record full output plus observed exit statuses 0, 0 and 2 in `./artifacts/public-before.txt`, along with commit, checkout root and imported commands-module origin. If results differ, stop and explain instead of forcing the old diagnosis.
- Keep all five historical diagnostic rows pending in their original package. Record in `./artifacts/diagnostic-disposition.md` how new local captures address the two exact-help observations; explain that identical reference forms provide no independent control and the no-op row has no causal discrimination for this wording defect. An applicability decision needs cited source and observed outputs, not invented passing results; mark unresolved rows explicitly if evidence is insufficient.

## Phase 3: Correct validate-lenses custom-prompt guidance

## Task 3: Replace the validate-lenses help description

Depends on: Task 2

In `src/superclaude/cli/swarm/commands.py`, replace only the custom-prompt description in the `validate_lenses_cmd` docstring. Describe directory-backed custom prompts as supplied by the JobSpec `custom_prompt_dir` field with `lens: custom` and loaded/validated at preflight, while leaving inline custom prompts valid and custom excluded from bundled registry validation. Read the current docstring, Task 1's test and `./artifacts/validate-help-red.txt`, the custom-directory note in `docs/swarm/command-reference.md`, `_apply_custom_prompt_dir` in `src/superclaude/cli/swarm/preflight.py`, and `_custom_prompt_dir_lens_failures` in `src/superclaude/cli/swarm/schema.py` before editing. Only tests authored by prior tasks may already differ.

Acceptance criteria:
- Only this docstring block changes in the product source. `validate_lenses_cmd` retains its `_run_validate_lenses` call, `--warning-mode`, exit behavior, registration and custom-registry exclusion; no option, loader or schema changes are introduced.
- Task 1's public-root help test now passes, while Task 2's scaffold help test still fails for the known stale scaffold description and its parser rejection guard still passes. Retain concrete commands, outputs and observed statuses in `./artifacts/validate-help-green.txt`.
- Run the existing `tests/swarm/test_validate_lenses_cmd.py` suite with UV and retain its result in `./artifacts/validate-lenses-tests.txt`. This checks existing dependent behavior, including warning mode and custom-only registry handling, rather than replacing it with help-only assertions.
- The description is explicit about the JobSpec field and custom lens without implying custom prompts must always come from a directory. Preserve the existing registration in `src/superclaude/cli/swarm/__init__.py` and every prompt-loading, guard and metadata contract.

## Phase 4: Correct scaffold guidance and retain repaired public evidence

## Task 4: Replace the scaffold lens option description

Depends on: Task 3

In `src/superclaude/cli/swarm/commands.py`, replace only the custom-prompt explanation inside `scaffold_cmd`'s `--lens` option help. Refer to directory-backed custom prompts through the JobSpec `custom_prompt_dir` field with `lens: custom`, not a command-line option. Preserve the reason scaffold rejects custom lenses: there are no bundled registry defaults to expand. Read that current option-help block, Task 2's tests and red evidence, `tests/swarm/test_scaffold_cmd.py`'s custom/unknown-lens checks, and the custom-directory note in `docs/swarm/command-reference.md`. Read the historical report's Next Steps and Pipeline Hardening Closure sections to keep its missing-proof requirements separate from this new implementation's evidence.

Acceptance criteria:
- The final product diff contains only the two intended help blocks in `src/superclaude/cli/swarm/commands.py` plus the new regressions in `tests/swarm/test_cli_registration.py`; internal comments, adjacent error messages, registrations, parser options, preflight, schema and docs are unchanged. Help describes directory-backed prompts as optional for custom specs.
- Both public-root help regressions and the parser rejection guard pass after their preserved pre-edit observations in `./artifacts/validate-help-red.txt`, `./artifacts/scaffold-help-red.txt` and `./artifacts/parser-before.txt` (F1). Existing registration/help and scaffold tests remain intact, including custom/unknown-lens rejection, schema-valid scaffold output and injection-guard content.
- Run `uv run pytest tests/swarm/test_cli_registration.py tests/swarm/test_validate_lenses_cmd.py tests/swarm/test_scaffold_cmd.py tests/swarm/test_custom_prompt_dir.py tests/swarm/test_custom_prompt_dir_injection_guard.py --cov=superclaude.cli.swarm --cov-report=term-missing`; preserve command, full output and observed status in `./artifacts/related-tests-green.txt`. No arbitrary coverage percentage is required; report unavailable coverage tooling or any failure honestly and do not silently drop checks.
- Capture full repaired public outputs by running `uv run superclaude swarm validate-lenses --help`, `uv run superclaude swarm scaffold --help` and `uv run superclaude swarm run --custom-prompt-dir <existing temporary directory>`, in `./artifacts/public-after.txt` (F1), including module origin, commit/checkout provenance, timestamps and observed statuses 0, 0 and 2. Both help outputs omit the rejected option and explain the supported field/custom-lens binding; the actual run parser still rejects that option. Source text inspection or mocked output alone is insufficient. Compare each with the same command's status and output in `./artifacts/public-before.txt` (F1).
- Retain red/green tests, before/after public captures and the pending/applicability record for the historical diagnostic rows. The executor's independent final applied-fix review must check this exact diff, the effective public surfaces, inline custom support and unchanged guard/metadata behavior, and persist its report under `./artifacts/`. Planning pre-review does not satisfy it.
- Do not declare repaired-state closure while public positive evidence or independent applied-fix review is absent or failing. Record new evidence and any remaining blockers without editing or retroactively passing the transferred report. No real model run, full custom-job success claim, commit, push, GitHub interaction or worktree creation is part of this plan.
