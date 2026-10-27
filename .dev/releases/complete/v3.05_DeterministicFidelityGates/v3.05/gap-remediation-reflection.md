# Gap Remediation Tasklist Reflection: v3.05

**Date**: 2026-03-21
**Reviewed by**: Reflection agent
**Source tasklist**: `gap-remediation-tasklist.md`
**Source report**: `roadmap-gap-analysis-merged.md`
**Files verified**: `executor.py`, `convergence.py`, `sprint/models.py`, `remediate_executor.py`

---

## Fidelity Check

### P0 Recommendations (3 Critical Bugs)

| Rec # | Recommendation | Task | Covered? | Accurate? | Notes |
|-------|---------------|------|----------|-----------|-------|
| P0-1 | Fix `DeviationRegistry.load_or_create()` call (B1) | T01 | YES | YES | Correctly identifies 1-arg vs 3-arg mismatch. |
| P0-2 | Fix `merge_findings()` calls (B2) | T02 | YES | YES | Correctly identifies structural/semantic split fix. |
| P0-3 | Fix dict/object mismatch (B3) | T03 | YES | PARTIAL | Fix is correct for the immediate crash, but misses a critical downstream issue (see Approach Validation). |

### P1 Recommendations (2 Spec Deviations)

| Rec # | Recommendation | Task | Covered? | Accurate? | Notes |
|-------|---------------|------|----------|-----------|-------|
| P1-4 | Use `MAX_CONVERGENCE_BUDGET` (B4) | T04 | YES | YES | Correct. |
| P1-4 | Add missing TurnLedger constructor params (B5) | T05 | YES | YES | Correct parameterization. |

### P2 Recommendations (3 Medium Gaps)

| Rec # | Recommendation | Task | Covered? | Accurate? | Notes |
|-------|---------------|------|----------|-----------|-------|
| P2-5 | Verify `remediate_executor.py` v3.05 deliverables (B8) | T06 | YES | YES | Read-only verification. |
| P2-6 | Fix wiring-verification target directory (B9) | T08 | YES | PARTIAL | Investigation-oriented; actual fix location is vague. |
| P2-7 | Add integration test for `_run_convergence_spec_fidelity()` (B10) | T07 | YES | YES | Good test coverage plan. |

### P3 Recommendations (3 Low Gaps)

| Rec # | Recommendation | Task | Covered? | Accurate? | Notes |
|-------|---------------|------|----------|-----------|-------|
| P3-8 | Add `budget_snapshot` to `RunMetadata` (B6) | T09 | YES | YES | Correct field addition. |
| P3-9 | Add budget state to progress proof logs (B7) | T10 | YES | YES | Correct log format. |
| P3-10 | Create persistent E2E tests for SC-1--SC-6 (B10) | T11 | YES | YES | Good test plan. |

### Additional Tasks (not from recommendations)

| Task | Purpose | Justified? |
|------|---------|-----------|
| T12 | Smoke test convergence path | YES -- validates the combined fixes. |
| T13 | Run full test suite | YES -- regression check. |
| T14 | Regenerate wiring-verification artifact | YES -- follows from T08. |

---

## Approach Validation

### T01: Fix `DeviationRegistry.load_or_create()` call signature

- **Line reference accuracy**: Tasklist says line 566. Actual file line 566 is exactly `registry = DeviationRegistry.load_or_create(config.output_dir / "deviation-registry.json")`. **CORRECT.**
- **Fix correctness**: The proposed fix is correct. `load_or_create()` at convergence.py:100 requires `(path, release_id, spec_hash)`.
- **`hashlib` import**: Tasklist note 6 says to check if `executor.py` already imports `hashlib`. Verified: `import hashlib` is already at line 14 of executor.py. **No additional import needed.** The tasklist says "Add `import hashlib` near the top of `_run_convergence_spec_fidelity()`" which is unnecessary. This won't cause harm (redundant import is harmless) but is sloppy.
- **Fix sufficiency**: YES -- resolves B1 completely.
- **New issues**: None. The `FileNotFoundError` risk is correctly noted and acceptable.

**Verdict: PASS (minor: remove unnecessary hashlib import note)**

### T02: Fix `merge_findings()` call arity

- **Line reference accuracy**: Tasklist says lines 587 and 599. Actual file:
  - Line 587: `reg.merge_findings(structural_findings, run_number)` -- **CORRECT.**
  - Line 599: `reg.merge_findings(semantic_result.findings, run_number)` -- **CORRECT.**
- **Fix correctness**: The proposed fix (`merge_findings(structural_findings, [], run_number)` and `merge_findings([], semantic_result.findings, run_number)`) is correct. The `merge_findings` signature at convergence.py:143 is `(structural: list[Finding], semantic: list[Finding], run_number: int)`.
- **Fix sufficiency**: YES -- resolves B2 completely and preserves BF-3 structural/semantic split.
- **New issues**: The risk note about `run_all_checkers()` return type is valid. `run_all_checkers()` returns `list[Finding]` which matches the expected type.

**Verdict: PASS**

### T03: Fix dict/object attribute access mismatch

- **Line reference accuracy**: Tasklist says lines 611-613. Actual file:
  - Line 611: `for finding in active_highs:` -- **CORRECT.**
  - Line 612: `for f in finding.files_affected:` -- **CORRECT.**
  - Line 613: `findings_by_file.setdefault(f, []).append(finding)` -- **CORRECT.**
- **Fix correctness**: The fix from `.files_affected` to `.get("files_affected", [])` is correct for preventing `AttributeError` on dicts.
- **Fix sufficiency**: **INSUFFICIENT.** This is the most significant issue in the tasklist. The fix resolves the immediate `AttributeError` but creates a silent downstream incompatibility:
  1. After the fix, `findings_by_file` maps `str -> list[dict]` (dicts from registry).
  2. `execute_remediation()` at `remediate_executor.py:732` has signature `(findings_by_file: dict[str, list[Finding]], ...)`.
  3. `execute_remediation()` and its downstream functions (e.g., `remediate_executor.py:172` `finding.files_affected`, lines 467, 514) use attribute access on Finding dataclass instances.
  4. Passing dicts where Finding objects are expected will cause `AttributeError` crashes inside `execute_remediation()`.

  The fix stops the crash at line 612 but pushes it downstream to `execute_remediation()`. The tasklist notes the risk ("Downstream `execute_remediation()` may also assume Finding dataclass instances") but does not include a task to fix it.

  **Required additional fix**: Either (a) convert registry dicts back to Finding dataclass instances before passing to `execute_remediation()`, or (b) modify the `_run_remediation()` function to reconstruct Finding objects from the dict data.

- **New issues**: YES -- downstream crash in `execute_remediation()`.

**Verdict: NEEDS AMENDMENT -- add dict-to-Finding conversion step**

### T04: Use `MAX_CONVERGENCE_BUDGET` instead of `STD_CONVERGENCE_BUDGET`

- **Line reference accuracy**: Tasklist says lines 571-572. Actual file:
  - Line 571: `from .convergence import STD_CONVERGENCE_BUDGET` -- **CORRECT.**
  - Line 572: `ledger = TurnLedger(initial_budget=STD_CONVERGENCE_BUDGET)` -- **CORRECT.**
- **Fix correctness**: Correct import and value change.
- **Fix sufficiency**: YES -- resolves B4.

**Verdict: PASS**

### T05: Add missing TurnLedger constructor parameters

- **Line reference accuracy**: Same region as T04 (line 572). **CORRECT.**
- **Fix correctness**: Verified against `TurnLedger` at `sprint/models.py:530-538`:
  - `minimum_allocation: int = 5` -- default 5, spec requires `CHECKER_COST` (10). **CORRECT.**
  - `minimum_remediation_budget: int = 3` -- default 3, spec requires `REMEDIATION_COST` (8). **CORRECT.**
  - `reimbursement_rate: float = 0.8` -- default already 0.8. Explicit is fine but not strictly needed.
- **Fix sufficiency**: YES -- resolves B5 and the guard hole.
- **The combined T04+T05 import line**: Tasklist proposes `from .convergence import MAX_CONVERGENCE_BUDGET, CHECKER_COST, REMEDIATION_COST`. This is correct; all three constants exist at convergence.py:25-27.

**Verdict: PASS**

### T06: Verify `remediate_executor.py` v3.05 deliverables

- **Approach**: Read-only verification task. Appropriate.
- **Risk**: Low.

**Verdict: PASS**

### T07: Write integration test for `_run_convergence_spec_fidelity()`

- **Approach**: Good test design covering all 5 bug sites. Seven tests mapped to specific bugs.
- **Note**: Test 4 (`test_remediation_dict_access`) would need updating to also test the dict-to-Finding conversion if T03 is amended per the recommendation above.

**Verdict: PASS (pending T03 amendment)**

### T08: Fix wiring-verification target directory

- **Line reference accuracy**: N/A -- investigation task.
- **Fix correctness**: The analysis is correct. Looking at executor.py:429, `source_dir = config.output_dir.parent` -- this is the actual issue. For a roadmap outputting to `.dev/releases/current/`, `output_dir.parent` is `.dev/releases/current` (a directory of release folders, not source code). The fix should be straightforward but the tasklist says "investigate location" which is vague.
- **Fix sufficiency**: PARTIAL -- the root cause is visible at executor.py:429 (`source_dir = config.output_dir.parent`). The tasklist could have been more specific.

**Verdict: PASS (could be more specific but investigation is appropriate)**

### T09: Add `budget_snapshot` field to `RunMetadata`

- **Line reference accuracy**: Tasklist says lines 72-84. `RunMetadata` dataclass is at convergence.py:72-84. **CORRECT.**
- **Fix correctness**: Adding `budget_snapshot: dict | None = None` to the dataclass is correct. However, the proposed population code writes to `registry.runs[-1]` (a dict), NOT to a `RunMetadata` instance. `RunMetadata` is a dataclass defined but never actually used to populate runs -- `begin_run()` at line 135 creates plain dicts. So adding the field to the dataclass is cosmetic. The actual fix (writing to `registry.runs[-1]`) is where the real work happens and that part is correct.
- **Fix sufficiency**: The proposed code is sufficient for adding budget snapshots to the JSON output, even though the `RunMetadata` dataclass change is cosmetic.

**Verdict: PASS (note: RunMetadata dataclass is not actually used for run storage; the dict approach is the real fix)**

### T10: Add budget state to progress proof log messages

- **Line reference accuracy**: Tasklist says lines 487-490. Actual convergence.py line 487-489 is:
  ```python
  progress_msg = (
      f"Run {run_idx + 1} ({run_label}): structural {prev_structural_highs} -> {curr_structural}"
  )
  ```
  **CORRECT.**
- **Fix correctness**: Appending budget state to the progress message is straightforward.
- **Also mentions line 474-477**: The PASS log at lines 474-477 is correct.
- **Fix sufficiency**: YES.

**Verdict: PASS**

### T11: Create persistent E2E verification tests

- **Approach**: Good test plan with 6 tests mapped to success criteria SC-1 through SC-6.
- **Risk**: Reasonable.

**Verdict: PASS**

### T12-T14: Final validation tasks

- All are appropriate validation/verification tasks.

**Verdict: PASS**

---

## Refactoring Recommendations

### Amendment 1: T03 must include dict-to-Finding conversion (CRITICAL)

**Problem**: T03 fixes the immediate `AttributeError` at executor.py:612 but the resulting `findings_by_file: dict[str, list[dict]]` is passed to `execute_remediation()` which expects `dict[str, list[Finding]]`. This creates a deferred crash.

**Corrected approach**: Add a conversion step in `_run_remediation()` that reconstructs `Finding` objects from registry dicts before calling `execute_remediation()`:

```python
def _run_remediation(reg: DeviationRegistry) -> None:
    """Run remediation on active HIGH findings."""
    from .models import Finding
    active_highs = reg.get_active_highs()
    if not active_highs:
        return

    # Convert registry dicts to Finding dataclass instances
    finding_objects = []
    for d in active_highs:
        finding_objects.append(Finding(
            id=d.get("stable_id", ""),
            severity=d.get("severity", "HIGH"),
            dimension=d.get("dimension", ""),
            description=d.get("description", ""),
            location=d.get("location", ""),
            evidence="",
            fix_guidance="",
            files_affected=d.get("files_affected", []),
            status=d.get("status", "ACTIVE"),
        ))

    # Group by file using Finding objects
    findings_by_file: dict[str, list] = {}
    for finding in finding_objects:
        for f in finding.files_affected:
            findings_by_file.setdefault(f, []).append(finding)

    execute_remediation(
        findings_by_file=findings_by_file,
        config=config,
        output_dir=config.output_dir,
        allow_regeneration=getattr(config, "allow_regeneration", False),
    )
```

**Note**: This also reveals that registry dicts may not have a `files_affected` key at all -- the `DeviationRegistry.merge_findings()` method at convergence.py:168 does NOT store `files_affected` in the finding dict. The Finding dataclass has `files_affected` but it is not persisted to the registry. This means even with dict access, `finding.get("files_affected", [])` will always return `[]`, making remediation unable to route findings to files. This is a deeper design gap that should be flagged.

### Amendment 2: T01 should note hashlib is already imported

**Problem**: T01 note 3 says "Add `import hashlib` near the top of `_run_convergence_spec_fidelity()`" and note 6 says to verify. `hashlib` is already imported at line 14 of executor.py.

**Corrected approach**: Remove the note about adding the import. Just use it.

### Amendment 3: T03 risk section should be elevated to a required sub-task

**Problem**: The risk note "Downstream `execute_remediation()` may also assume Finding dataclass instances" is not speculative -- it is a confirmed fact. `remediate_executor.py:733` has `findings_by_file: dict[str, list[Finding]]` in its type signature.

**Corrected approach**: Elevate the risk to a required sub-task or add a new T03b task.

---

## Coverage Summary

| Metric | Count |
|--------|-------|
| Recommendations fully covered | 8/10 |
| Recommendations partially covered | 2/10 (T03/B3 and T08/B9) |
| Recommendations missing | 0/10 |
| Tasks needing refactoring | 2 (T01 minor, T03 critical) |

---

## Discovered Issues Not in Source Report

### D-NEW-1: `files_affected` not persisted in registry

The `DeviationRegistry.merge_findings()` method (convergence.py:168-180) stores findings as dicts but does NOT include `files_affected` from the original Finding objects. The stored dict has: `stable_id, dimension, severity, description, location, source_layer, status, first_seen_run, last_seen_run, debate_verdict, debate_transcript`. No `files_affected`.

This means:
1. `get_active_highs()` returns dicts without `files_affected`.
2. Even with T03's dict-access fix, `finding.get("files_affected", [])` returns `[]`.
3. Remediation cannot route findings to target files.
4. The `_run_remediation()` function would produce an empty `findings_by_file` dict every time.

**Severity**: HIGH -- this makes convergence-mode remediation non-functional even after all P0 fixes.

**Recommended fix**: Either:
- (a) Store `files_affected` in the registry dict during `merge_findings()`, OR
- (b) Re-derive `files_affected` from the `location` field (which is stored) at remediation time.

This should be added as a new task (T03b or T15) at P0 severity, in Wave 1.

---

## Final Verdict

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| **Fidelity** | **HIGH** | All 10 source recommendations have corresponding tasks. No recommendations are missing. |
| **Approach quality** | **MEDIUM** | T01-T02, T04-T14 are correct. T03 has a critical gap: it fixes the surface crash but the underlying dict-to-Finding impedance mismatch and missing `files_affected` persistence mean remediation remains non-functional. |
| **Ready for execution** | **YES WITH AMENDMENTS** | Execute Waves 1-2 as-is (the P0 crash fixes and budget fixes are correct). Before T03 is considered "done", the dict-to-Finding conversion must be added and the `files_affected` persistence gap must be addressed. |

### Required Amendments Before Execution

1. **T03**: Expand scope to include dict-to-Finding conversion in `_run_remediation()` and flag the `files_affected` registry persistence gap.
2. **T01**: Remove the unnecessary `import hashlib` note (already imported at module level).
3. **Add T15**: Store `files_affected` in `DeviationRegistry.merge_findings()` dict entries (P0 severity, Wave 1).
