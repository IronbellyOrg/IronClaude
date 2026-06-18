# Phase 4 (P3) — Test Summary (Step 4.8)

**Command:** `uv run pytest tests/sprint/test_recovery_policy.py tests/sprint/test_executor.py -v`
**Result:** **107 passed, 0 failed** (exit 0). Raw output: `p3-pytest.txt`.

Breakdown:
- `test_recovery_policy.py` — 7 passed (parametrized `SessionResetPolicy.decide` truth table; boundary `attempt < cap` → HALT at `==cap`; cooldown fast-path on first attempt).
- `test_executor.py` — 100 passed, including all 6 P3 re-spawn-loop scenarios (`TestPerTaskOrchestration`):
  1. single-429 → clean ⇒ PASS, `session_resets == 1`, 2 spawns.
  2. cooldown attempt-1 ⇒ fast-path FAIL_PROVIDER_EXHAUSTED, 1 spawn, `exhausted_model == "claude-opus-4-8"`.
  3. single-429 × cap=8 ⇒ FAIL_PROVIDER_EXHAUSTED, exactly 8 spawns, persisted `halt_reason == "provider_exhaustion"`.
  4. single-429 → real-failure ⇒ FAIL_TERMINAL (2nd attempt classified by normal ladder), 2 spawns.
  5. K>1 (K=4) all-429 ⇒ single latch halt; storm bounded `cap ≤ total ≤ cap+(K-1)` AND `< K×cap`.
  6. always-429 single (K=1, cap=3) ⇒ exactly 3 spawns (infinite-loop guard).

**Determinism:** the K>1 storm-bound scenario passed on **5 consecutive runs** after the
shared-budget fix (see Phase 4 Findings [FIX]). Previously it was flaky/over-bound because
the loop used a per-worker counter.

**Fix applied during this validation step:** the re-spawn loop initially failed scenarios 3/5/6
(spawned `cap+1` / ≈`K×cap`). Root cause + fix documented in the task's ### Phase 4 Findings:
the loop now consumes the shared `SessionResetPolicy._exhaustion_attempts` budget under the lock
instead of a per-worker `attempt`, satisfying spec §4 Layer 3's storm bound deterministically.

**Pass criterion (Step 4.8):** all targeted tests pass with no regressions — **MET**.
