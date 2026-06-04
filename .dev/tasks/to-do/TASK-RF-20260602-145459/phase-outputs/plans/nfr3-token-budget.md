# NFR-3 Token-Budget Delta — Conditional Deferral Record

**Date:** 2026-06-03
**Step:** Phase 6, Step 6.11
**Resolves:** reflect finding G1 (§8.2 layer not explicitly accounted for)

## Requirement (NFR-RV3-MED.3)
The FR-1/FR-3/FR-4 orchestration additions must add ≤ **+1,000** Claude-orchestration tokens over the T1
path, measured vs a named baseline = current `master` HEAD on the FR-4 eval fixture (`serena-execute-verify`).
- `execute_shell_command` Claude-side cost is ~0 (the test-suite wall-clock runs in the subprocess, not Claude tokens).
- `onboarding` is EXCLUDED from the cap (one-shot, documented context-heavy exception) and measured separately.

## Runner gate (CODE-VERIFIED 2026-06-03)
- `make reflect-eval` and `make reflect-eval-quick` exist, but they run `grader.py` — an **assertion grader**
  (scores `evals.json` assertions against an iteration dir's outputs). They are **NOT a token-ledger runner**.
- A token-ledger runner that measures **baseline-vs-branch Claude orchestration output-token delta** is **NOT
  present** in this workspace.

## Disposition — EXPLICIT DEFERRAL (not silent omission)
- **IF** a token-ledger runner (baseline-vs-branch Claude-output-token diff) is present at execution time:
  run the measurement and assert `delta ≤ 1000` for FR-1/FR-3/FR-4; record `onboarding` separately.
- **IF absent** (the current state): the measurement is **EXPLICITLY DEFERRED**, with this record as the
  deferral. The `serena-token-budget` case ships `status: skeleton-pending-runner` and `disposition:
  RUNNER-DEFERRED`. This is NOT a silent drop — the §8.2 token-budget row is accounted for.

## Eval registration
`serena-token-budget` (id 34) is registered in `evals.json` with a skeleton assertion on
`status: skeleton-pending-runner` (so the grader records the deferral) — to be replaced with a `yaml_field`
on the measured delta when a token-ledger runner lands.
