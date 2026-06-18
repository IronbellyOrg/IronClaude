# P4 / Phase 5 Aggregate Manifest

## Load-bearing invariants

- `PhaseStatus.PROVIDER_EXHAUSTED` exists with value `provider_exhausted` and is included in `is_terminal` only, not `is_success` or `is_failure`.
- The single-session path calls `detect_provider_failure(config.output_file(phase))` after each attempt and short-circuits to `PhaseStatus.PROVIDER_EXHAUSTED` before `_determine_phase_status` on provider exhaustion; preliminary-result fallback writes are allowed only when `exit_code == 0 and status is None`.
- A provider-exhausted halt sets `halt_reason = "provider_exhaustion"` / `exhausted_model` on the `PhaseResult`, halts with `SprintOutcome.HALTED`, and bypasses the diagnostic bundle block so no `phase-N-diagnostic.md` is written for infra exhaustion.
- Resume cross-reference is split by record shape: top-level phase status `"provider_exhausted"` is handled by `_is_pass_family -> PhaseStatus(value).is_success == False`, while per-task provider exhaustion is handled by `_coerce_task_status -> TaskStatus("fail_provider_exhausted")`.
- Resume path split: single-session provider exhaustion persists a phase-level halt (`provider_exhausted`, `halt_reason`, `exhausted_model`) and resumes at phase granularity unless per-task evidence exists; per-task provider exhaustion persists `fail_provider_exhausted` task results and resumes through `_coerce_task_status` at task granularity.

## Deliverables discovered by glob

- `src/superclaude/cli/sprint/models.py` — PhaseStatus.PROVIDER_EXHAUSTED enum/member placement and phase-result persistence fields.
- `src/superclaude/cli/sprint/executor.py` — Single-session provider-exhaustion retry/short-circuit/persistence/halt control flow.
- `tests/sprint/test_models.py` — PhaseStatus terminal-not-failure regression tests.
- `tests/sprint/test_executor.py` — Single-session cooldown halt and no-diagnostic-bundle regression tests.
- `.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/test-results/p4-lint.txt` — P4 validation evidence (pytest/lint/verify-sync output or summary).
- `.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/test-results/p4-pytest.txt` — P4 validation evidence (pytest/lint/verify-sync output or summary).
- `.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/test-results/p4-summary.md` — P4 validation evidence (pytest/lint/verify-sync output or summary).
- `.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/test-results/p4-verify-sync.txt` — P4 validation evidence (pytest/lint/verify-sync output or summary).
