# QA Report — Structural Diagnostic-Bundle Safety

## Binary Verdict

FAIL

## Lens

diagnostic-bundle-safety (rf-qa, fix_authorization: false)

## Evidence Reviewed

- Manifest: `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/reports/p4-aggregate.md`
- Research: `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/research/04-data-flow-tracer.md` FINDING F-1
- `src/superclaude/cli/sprint/models.py`
- `src/superclaude/cli/sprint/executor.py`
- `tests/sprint/test_models.py`
- `tests/sprint/test_executor.py`

## Passing Checks

- `PROVIDER_EXHAUSTED` is in `is_terminal` but not `is_failure`: `src/superclaude/cli/sprint/models.py:419`, `src/superclaude/cli/sprint/models.py:424-439`, `src/superclaude/cli/sprint/models.py:452-459`.
- Explicit provider-exhausted halt branch sets `SprintOutcome.HALTED`, `halt_phase`, and breaks before diagnostics: `src/superclaude/cli/sprint/executor.py:2250-2253`.
- Diagnostic collection starts only after that branch, under `if status.is_failure`: `src/superclaude/cli/sprint/executor.py:2255-2266`.
- Targeted tests passed during lens verification: provider status, terminal-not-failure, and no-diagnostic-bundle checks.

## Findings

### IMPORTANT — No-diagnostic-bundle test is not sensitive to wrong `is_failure` membership by itself

- Evidence: `tests/sprint/test_executor.py:501-508` asserts provider-exhausted status and absence of `phase-1-diagnostic.md`.
- Evidence: the executor exits at `src/superclaude/cli/sprint/executor.py:2250-2253` before checking `status.is_failure`, so the no-diagnostic-bundle integration test would still bypass diagnostics even if `PROVIDER_EXHAUSTED.is_failure` were incorrectly changed to `True`.
- Evidence: the direct membership guard that would catch the wrong tuple placement is `tests/sprint/test_models.py:117-122`.
- Required fix: either correct the manifest/test claim to identify `test_provider_exhausted_terminal_not_failure` as the mutation guard, or strengthen the no-diagnostic-bundle test with an explicit assertion that `PhaseStatus.PROVIDER_EXHAUSTED.is_failure is False`.

## Confidence

100% — local source/test claims were independently checked by the rf-qa lens agent.
