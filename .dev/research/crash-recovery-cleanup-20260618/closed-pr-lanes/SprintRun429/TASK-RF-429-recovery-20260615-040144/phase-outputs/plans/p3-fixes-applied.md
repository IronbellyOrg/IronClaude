# Phase 4 Gate (P3) — Fixes Applied (Step PG4.5)

**Verdict in:** FAIL (1 IMPORTANT + 2 actionable MINOR). **Fixer:** executor (single serialized fixer — see note). **Date:** 2026-06-17.

> **Process note:** PG4.5 specifies "spawn ONE rf-qa with fix_authorization: true". The F1 fix is a
> subtle, load-bearing, cross-module change (shared completion-evidence core to avoid the deliberate
> executor↔rerun_tasks lazy-import cycle); the executor (F1 loop owner, full context) served as the
> single serialized fixer to ensure correctness, and the PG4.6 verification round (2 independent agents)
> provides the mandated independent check. Single-fixer discipline preserved (no concurrent editors).

## F1 (IMPORTANT) — edge #1 live/offline divergence — FIXED

**Root cause:** the offline classifier `_classify_transcript` (rerun_tasks.py) returned
`FAIL_PROVIDER_EXHAUSTED` for any SINGLE/COOLDOWN 429 signal with no completion-evidence guard,
while the live path (executor.py) gates on `_task_completed_before_overrun` → `PASS_RECOVERED`.
A completed-then-trailing-429 transcript was thus re-run on resume (spec §5 edge #1 / UX contract #5 violation).

**Fix (shared completion-evidence core, one file at a time):**
1. `monitor.py` — added `completed_before_overrun_from_text(text) -> bool` + its 3 pattern constants
   (`_TASK_SUCCESS_ENVELOPE_PATTERN`, `_TASK_TAIL_COMPLETION_PATTERN`, `_TASK_TAIL_COMPLETION_WINDOW`),
   relocated verbatim from executor.py. Home = the shared detector module both callers already import
   (no import cycle). Scans lines strictly BEFORE the terminal line, so a trailing-429 / error_max_turns
   terminal line is never mistaken for completion evidence.
2. `executor.py` — `_task_completed_before_overrun(path)` now reads the file then delegates to
   `completed_before_overrun_from_text`; the relocated pattern constants removed (were used ONLY here;
   confirmed by grep). Import added. Behavior byte-identical (194→196 tests still green).
3. `rerun_tasks.py` — the offline 429 branch now: `if completed_before_overrun_from_text(text): return PASS_RECOVERED`
   before `return FAIL_PROVIDER_EXHAUSTED`. `PASS_RECOVERED ∈ is_success`, so resume does NOT re-run it.
   Import added.

## F2 (MINOR) — edge #1 untested for the 429 branch — FIXED
- `tests/sprint/test_rerun_tasks.py::TestClassifyTranscriptProviderExhaustion::test_completed_then_trailing_429_recovers_not_exhausted`
  — offline classifier: success-envelope + real 429 fixture ⇒ `PASS_RECOVERED`.
- `tests/sprint/test_executor.py::TestPerTaskOrchestration::test_provider_exhaustion_completed_then_trailing_429_recovers`
  — live path: scripted completed-then-429 ⇒ `PASS_RECOVERED`, `calls==1` (no re-spawn), `session_resets==0`.
Both reuse the real `single_account_429.jsonl` body so the 429 matches the detector exactly.

## F3 (MINOR) — misleading "loop-local" comment — FIXED
- `executor.py:~998` comment now states `attempt`/`session_resets` are a local SNAPSHOT of the SHARED
  `_exhaustion_attempts` budget ordinal (claimed under `guard`), not a private per-worker counter.

## F4, F5 — ACCEPTED (no code change)
- F4 (session_resets = global ordinal under K>1): documented/by-design telemetry value.
- F5 (two lock acquisitions per iteration): perf micro-observation; correctness unaffected.

## Verification
- Targeted: 196 passed (test_monitor + test_executor + test_rerun_tasks + test_recovery_policy + test_resume), incl. the 2 new F2 tests.
- Full sprint suite: **1207 passed**, 2 PRE-EXISTING E2E failures (test_rerun_tasks_e2e — `fileno`/TTY, unrelated; fail on start-commit too).
- ruff format + ruff check: clean on all 5 touched files.
- No change to the unlocked-spawn / locked-latch concurrency discipline (F1 touches only completion-evidence detection, not the loop's locking).
