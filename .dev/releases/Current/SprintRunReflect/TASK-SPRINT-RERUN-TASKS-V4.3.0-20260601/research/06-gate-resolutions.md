# Research: Gate Resolutions (Gap-Fill Cycle 1)
**Topic type:** Gate Resolution
**Scope:** Resolve contradictions and ambiguities flagged by rf-analyst + rf-qa research-gate
**Status:** Complete
**Date:** 2026-06-01
**Authority:** Direct re-Read of TDD `merged-requirements.md` lines 115-130 + spot-check verifications

---

## Resolution 1 — CRITICAL: TaskStatus.FAIL rename (RESOLVED)

**Contradiction:**
- Researcher 1 (file-inventory) §B.18: rename `FAIL` → `FAIL_TERMINAL` keeping serialized `"fail"`
- Researcher 3 (integration-points) IP-3: "no rename — additive sibling only"
- Researcher 5 (template-examples) §4.3: propagates Researcher 3's wrong reading

**Ground truth** (verbatim from TDD `/config/workspace/IronClaude/.dev/releases/backlog/SprintGranularResume/merged-requirements.md` line 119):
> **Back-compat handling**: rename `FAIL` → `FAIL_TERMINAL` BUT keep its serialized string as `"fail"` (Python enum value separate from name). Existing logs deserialize correctly.

**Resolution: ADOPT Researcher 1's reading.** The TDD does specify the rename. Implementation contract:

```python
class TaskStatus(Enum):
    PASS = "pass"
    FAIL_TERMINAL = "fail"        # renamed from FAIL; SAME serialized value for backcompat
    FAIL_RECOVERABLE = "fail_recoverable"
    INCOMPLETE = "incomplete"
    SKIPPED = "skipped"
```

**Implications for the task file:**
- Phase 1 (data-model foundation) MUST include a TaskStatus.FAIL → TaskStatus.FAIL_TERMINAL rename across the whole codebase (grep for `TaskStatus.FAIL` and `TaskStatus\.FAIL[^_]`)
- The rename is API-breaking at the Python-symbol level but BACK-COMPAT at the wire/serialization level (logs deserialize correctly because the enum value `"fail"` is unchanged)
- All call sites that reference `TaskStatus.FAIL` must be updated to `TaskStatus.FAIL_TERMINAL` — this is across executor.py, classifiers.py, and possibly tests

**Override:** All conflicting guidance in 03-integration-points.md IP-3 and 05-template-examples.md §4.3 sample item is **SUPERSEDED** by this resolution.

---

## Resolution 2 — IMPORTANT: `is_failure` predicate semantic (RESOLVED)

**Ambiguity:** rf-qa flagged "is_failure widening semantic is undecided" — should `TaskStatus.FAIL_RECOVERABLE` be a member of the `is_failure` set (for halt logic) or only `FAIL_TERMINAL`?

**Resolution:** **Include `FAIL_RECOVERABLE` in `is_failure`.** Rationale:
1. The phase-aggregate `all_passed = all(r.status == TaskStatus.PASS for r in task_results)` already counts both as non-PASS (current behavior preserved)
2. Halt logic should fire on EITHER terminal or recoverable failure (the operator decides whether to invoke `sprint rerun-tasks` for recovery; the executor should still halt the phase)
3. `rerun-tasks` selector uses **explicit enum membership** (`r.status == TaskStatus.FAIL_RECOVERABLE`), NOT `is_failure`, so the predicate widening doesn't double-count recoverables for retry

**Contract:**
```python
@property
def is_failure(self) -> bool:
    return self in (TaskStatus.FAIL_TERMINAL, TaskStatus.FAIL_RECOVERABLE)
```

---

## Resolution 3 — MINOR: Test count budget (RESOLVED)

**Ambiguity:** Researcher 4 enumerated 73 tests; TDD §Implementation cost estimates ~25 unit + 2 integration = 27.

**Resolution:** **Recommended cut to ~40 tests.** Apply the following trims:

| Original count | Trimmed | Cut |
|---|---|---|
| TestExtractPhaseSubset (6 tests) | 4 | Drop `test_extract_handles_unicode_titles` and `test_extract_preserves_lf_vs_crlf` — covered by integration round-trip |
| TestFailClassificationHeuristic (4 tests) | 3 | Merge 2 sub-cases into parametrize |
| TestFailRecoverableStatus (2 tests) | 1 | Combine into single round-trip enum-value test |
| TestRecoveryBundle (12 tests) | 8 | Drop 4 redundant edge-case state-transition tests |
| TestRerunTasksRoundTrip (3 tests) | 2 | Merge AC2+AC3 into one round-trip equivalence test |
| `test_models.py` edits (+6) | +4 | Drop 2 redundant enum-value round-trip tests |
| `test_executor.py` edits (+6) | +4 | Drop 2 redundant classification-heuristic tests (move to test_rerun_tasks.py) |

**Final budget:** ~42 tests (within ±20% of TDD's ~27 budget given the v4.3.0 additions; acceptable for STRICT-tier feature work).

**Implementation guidance for builder:** Phase 5 (Test suite) item count should be 12-15 individual test-creation items + 5-6 test-edit items, NOT 73 individual items.

---

## Resolution 4 — MINOR: Line-number UNVERIFIED tags (RESOLVED via Phase 1 Discovery item)

**Ambiguity:**
- IP-12 cites `logging_.py:188` for `write_phase_rerun_complete` insertion + `_jsonl` at line 210 + `write_checkpoint_verification` at line 159 — uncited
- IP-9 cites `executor.py:1014-1020` for classification site, but Researcher 1 §B.19 places it near `_run_task_subprocess()` at line 1076 — apparent conflict

**Resolution:** Add a Phase 1 Discovery sub-item to the task file: `T01.NN — Verify integration-point line numbers`. This item:
- Greps `logging_.py` for `write_checkpoint_verification`, `_jsonl`, `write_summary` to confirm IP-12 line numbers
- Greps `executor.py` for the `TaskStatus.FAIL` / classification site to confirm IP-9 line numbers
- Updates the Task Log with confirmed numbers before Phase 2 begins

This converts the UNVERIFIED tags into a verifiable preflight step, consistent with the MultiModelSwarm task pattern (which had a similar Phase 1.2 line-number verification step).

---

## Resolution 5 — MINOR: RecoveryStatus enum location (RESOLVED)

**Ambiguity:** Researcher 1 §B.18 was unclear about whether `RecoveryStatus` enum belongs in `models.py` or `recovery.py`.

**Resolution:** **Place `RecoveryStatus` in `recovery.py`.** Rationale:
- TDD §T6 specifies `recovery.py` is the new module owning the recovery abstraction
- `models.py` is the shared dataclass home for sprint-wide types; a `RecoveryStatus` enum is recovery-specific
- Mirrors the pattern where `CheckpointEntry` lives in `checkpoints.py` (line 312 of checkpoints.py — verified by Researcher 1 §B.5), not in models.py — wait, the existing `CheckpointEntry` IS in models.py at line 312
- BUT: `RecoveryBundle` is the parallel structure to `PhaseResult` (state-bearing dataclass), and the TDD specifies it lives in `recovery.py`. Keep `RecoveryStatus` co-located with `RecoveryBundle` for cohesion.

---

## Summary

All 5 gate findings resolved. Task-builder should treat this file as authoritative when conflicting guidance appears in 03-integration-points.md or 05-template-examples.md.

**Pass-through to builder:**
- Phase 1 MUST include the `FAIL → FAIL_TERMINAL` rename + the `is_failure` predicate widening
- Phase 1 MUST include a discovery sub-item for IP-12 / IP-9 line-number verification
- Phase 5 test count target: ~42 individual tests, NOT 73
- `RecoveryStatus` enum location: `recovery.py`, co-located with `RecoveryBundle`
