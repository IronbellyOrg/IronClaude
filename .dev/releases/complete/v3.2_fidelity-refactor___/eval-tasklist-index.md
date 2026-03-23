# TASKLIST — Unified Real-Eval Execution for v3.05, v3.1, and v3.2

## Metadata

| Field | Value |
|---|---|
| Tasklist Root | `.dev/releases/complete/v3.2_fidelity-refactor___/` |
| Source Proposal | `.dev/releases/complete/v3.2_fidelity-refactor___/unified-eval-design-proposal-v3.05-v3.1-v3.2.md` |
| Objective | Build and run no-mock, real-pipeline evals that produce third-party-verifiable artifacts for v3.1, v3.2, and v3.05 |
| Execution Mode | Sequential |
| Evidence Standard | Real CLI pipeline only; no mocks; no unit-test-only proof |
| Recommended Entry Command | `superclaude sprint run .dev/releases/complete/v3.2_fidelity-refactor___/eval-tasklist-index.md` |

## Phase Files

| Phase 1 Tasklist | `TASKLIST_ROOT/eval-phase-1-tasklist.md` |
| Phase 2 Tasklist | `TASKLIST_ROOT/eval-phase-2-tasklist.md` |
| Phase 3 Tasklist | `TASKLIST_ROOT/eval-phase-3-tasklist.md` |
| Phase 4 Tasklist | `TASKLIST_ROOT/eval-phase-4-tasklist.md` |
| Phase 5 Tasklist | `TASKLIST_ROOT/eval-phase-5-tasklist.md` |
| Phase 6 Tasklist | `TASKLIST_ROOT/eval-phase-6-tasklist.md` |
| Phase 7 Tasklist | `TASKLIST_ROOT/eval-phase-7-tasklist.md` |
| Phase 8 Tasklist | `TASKLIST_ROOT/eval-phase-8-tasklist.md` |

## Scope Guardrails

1. Every eval must invoke the real affected pipeline surface (`superclaude roadmap run` and/or `superclaude sprint run`).
2. Every eval must write inspectable disk artifacts.
3. Any approach that replaces pipeline execution with unit tests, synthetic gate-only tests, or mocks is out of scope.
4. Warning-only scenarios do not count as core proof unless they persist stable artifacts.
5. If an eval cannot produce third-party-verifiable artifacts, stop and tighten the fixture before continuing.
