# R2 Test Surfaces — Results (Step 5.6)

**Captured:** 2026-06-02 07:35
**Raw output:** `r2-tests.txt`
**Overall:** ✅ ALL GREEN.

## Per-surface results

| Surface | Result |
|---|---|
| `tests/roadmap/test_spec_roadmap_id_containment.py` | **12 passed** (was 11; +1 new R2 regression) |
| `tests/roadmap/test_gates_data.py` | **227 passed** |
| `tests/roadmap/test_executor.py` | **71 passed** |

## New R2 regression — CONFIRMED PASS
`test_r2_run_start_reset_closes_stale_sidecar_leak` — **PASSED**. Single test body (defeats the autouse `_isolate_gates_state` mask). Exercises the real `executor._reset_id_registry_sidecar_hint` helper:
- Run 1 sets sidecar to spec-A registry; `FR-1` passes under A.
- Run 2 (fresh, extract skipped, new output dir): R2 reset (`resume=False`) clears the hint → gate **fail-shuts** on `FR-1` (string, "Contract #9"), instead of wrongly passing against stale registry A.
- Resume-aware: a `--resume` run with its OWN persisted sidecar re-points and validates `NFR-9` as True (does not fail-shut).
- Fail-before/pass-after: `_reset_id_registry_sidecar_hint` is the R2 fix; pre-fix the import would fail and a fresh second run would inherit run-1's stale sidecar.

## MERGE_GATE composition guard — CONFIRMED INTACT
The composition guard is `test_merge_gate_has_seven_semantic_checks` — it asserts the MERGE gate has **SEVEN** semantic checks (NOT eight; the task text's "8" was an inaccurate upstream assumption). It **PASSES**. The R2/R5 edits modified only the `SpecIdRegistry(...)` reconstruction *inside* `_roadmap_ids_within_spec` (adding `md_ids` with a `.get(...,())` default) — they did NOT add or remove any MERGE semantic check, so the count is unchanged and the guard stays green. `roadmap_ids_within_spec` remains one of the seven registered semantic checks.

## Fail-shut + signature preservation — CONFIRMED
`test_fail_shut_when_sidecar_missing` and `test_fail_shut_when_sidecar_unreadable` both PASS — the `gates.py:1069-1074` fail-shut branches (failure STRING on None/missing/unreadable/malformed) are preserved exactly, and the `Callable[[str], bool|str]` SemanticCheck signature is unchanged.
