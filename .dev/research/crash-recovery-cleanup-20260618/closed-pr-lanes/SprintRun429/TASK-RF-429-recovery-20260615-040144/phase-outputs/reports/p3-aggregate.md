# Phase 4 (P3) — QA Gate Aggregate Manifest (Step PG4.1)

**Phase:** P3 — Policy + Executor Re-Spawn Loop (HIGH RISK live concurrency).
**Aggregated:** 2026-06-17. **Validation:** 107/107 P3 tests pass; ruff format+check clean; verify-sync exit 0.

> **IMPORTANT for lens agents — implementation reflects a spec-mandated deviation from the task item wording.**
> Step 4.3 literally says "loop-local `attempt` counter". The implementation instead consumes the **shared
> `SessionResetPolicy._exhaustion_attempts` budget UNDER the lock**, because spec §4 Layer 3 fixes the K>1 storm
> bound at `≤ cap+(K-1)` ("workers don't each burn the full reset budget … no K×max spawn storm"), which a
> per-worker counter cannot satisfy. Review against the SPEC (§4 Layer 3) and this note, not the literal "loop-local"
> phrasing. Full rationale: task ### Phase 4 Findings [FIX]/[DEVIATION]. `decide()` is unchanged (pure, 7/7 unit tests).

## Deliverables

| File | Purpose |
|------|---------|
| `src/superclaude/cli/sprint/recovery_policy.py` (3.3 KB, NEW) | `Action` enum (4 members; `FAIL_TASK` reserved), `SessionResetPolicy` dataclass (`max_session_resets=8`, `_exhaustion_attempts`, `_latch_tripped`), pure `decide(signal, attempt) -> Action`. |
| `src/superclaude/cli/sprint/executor.py` (modified, +143 lines vs start) | `_run_one_task` `reset_policy` kw-param; bounded re-spawn loop (`executor.py:1009-1088`); latch precheck (locked); unlocked spawn; detector→decide dispatch; status-ladder ordering; `TaskResult` exhaustion fields; `reset_policy` threaded at K>1 (`lock=lock`, ~1216) and K=1 (`lock=None`, ~1431) call sites + shared policy constructed once per phase (~1314-1316); per-task halt derivation; `_write_phase_result_json` halt keys. |
| `src/superclaude/cli/sprint/models.py` (modified, +19 lines) | `PhaseResult.halt_reason`/`exhausted_model` fields (`""` defaults); (P2 added `TaskStatus.FAIL_PROVIDER_EXHAUSTED` + 3 `TaskResult` fields). |
| `tests/sprint/test_recovery_policy.py` (NEW) | parametrized `decide` truth-table (7 rows): cooldown→HALT on any attempt; single→RETRY while `attempt<cap` else HALT (boundary at `==cap`); NONE/TIMEOUT→CONTINUE. |
| `tests/sprint/test_executor.py` (modified, +200 lines) | `_make_scripted_factory` + `_make_threadsafe_repeating_factory` helpers + `_fixture_text` loader; 6 re-spawn scenarios (see below). |
| `phase-outputs/discovery/executor-wiring-points.md` | Step 4.1 verified insertion-point inventory. |
| `phase-outputs/test-results/p3-pytest.txt` / `p3-summary.md` | 107 passed. |
| `phase-outputs/test-results/p3-lint.txt` | ruff format-check + check clean (2 prescribed auto-fixes noted). |
| `phase-outputs/test-results/p3-verify-sync.txt` | exit 0, all in sync. |

## Load-bearing invariants (verify these)

1. **Spawn UNLOCKED, latch LOCKED.** The `subprocess_factory`/`_run_task_subprocess` call is OUTSIDE `with guard:`. The latch precheck AND the latch trip are INSIDE `with guard:` (`guard = lock if lock is not None else contextlib.nullcontext()`). The shared-budget increment+snapshot is ALSO under `guard`.
2. **Storm bound `cap ≤ total ≤ cap+(K-1)` AND `< K×cap`** — achieved DETERMINISTICALLY via the shared `_exhaustion_attempts` budget claimed under the lock (only ≤K-1 already-mid-unlocked-spawn workers overshoot). NOT `≤ cap`.
3. **Completion guard precedes provider-failure re-route** — `_task_completed_before_overrun(task_output_path)` → `PASS_RECOVERED` BEFORE consuming budget (edge #1: completed-then-trailing-429 must not re-spawn).
4. **Status-ladder ordering** — provider-failure handling sits ABOVE `_is_transient_failure` and BELOW the `:1003`-equiv completion/PASS_RECOVERED gate; `_is_transient_failure` UNCHANGED; NONE/OPERATION_TIMEOUT fall through to the normal ladder.
5. **`reset_policy` threaded at BOTH call sites** (K>1 `lock=lock`; K=1 `lock=None`), the SAME instance shared per phase so `_latch_tripped` + budget are sprint-wide.
6. **Persistence on the single path** — `TaskResult.failure_class/session_resets/exhausted_model`; per-task derivation sets `PhaseResult.halt_reason="provider_exhaustion"` + `exhausted_model`; `_write_phase_result_json` emits `halt_reason`/`exhausted_model` keys.
7. **`decide` is pure** — no side effects, never returns `FAIL_TASK`, boundary `attempt < max_session_resets`.

## Test scenarios (`TestPerTaskOrchestration`)

1. single-429 → clean ⇒ `PASS`, `session_resets==1`, 2 spawns.
2. cooldown attempt-1 ⇒ `FAIL_PROVIDER_EXHAUSTED`, 1 spawn, `exhausted_model=="claude-opus-4-8"` (fast path).
3. single-429 × cap=8 ⇒ `FAIL_PROVIDER_EXHAUSTED`, exactly 8 spawns, persisted `halt_reason`.
4. single-429 → real-failure ⇒ `FAIL_TERMINAL` (normal ladder on 2nd attempt), 2 spawns.
5. K>1 (K=4, cap=3) all-429 ⇒ latch trips once; `cap ≤ total ≤ cap+(K-1)` AND `< K×cap`.
6. always-429 K=1, cap=3 ⇒ exactly 3 spawns (infinite-loop guard).
