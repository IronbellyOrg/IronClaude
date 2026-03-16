# Fix Plan: HIGH Severity Deviations
# Roadmap: pass-no-report-fix / spec-fidelity report

**Source roadmap**: `roadmap-pass-no-report-fix/roadmap.md`
**Spec**: `artifacts/pass-no-report-fix-spec.md`
**Fidelity report**: `roadmap-pass-no-report-fix/spec-fidelity.md`
**Deviations addressed**: DEV-001, DEV-002, DEV-003 (all HIGH)

---

## Overview and Approach

All three HIGH deviations are surgical text edits to the roadmap. None require restructuring phases or changing the implementation strategy. The minimal-diff approach is correct here: each fix targets a specific, localized section without cascading effects.

**Ordering**: DEV-002 must be fixed before DEV-001 is verified to be internally consistent, because DEV-002 establishes the return type that T-005 (DEV-001) must test. DEV-003 is independent and can be done in any order relative to DEV-001/002. Recommended order: DEV-002 → DEV-001 → DEV-003.

**Interdependency map**:
- DEV-002 (Phase 1 function signature) feeds into DEV-001 (T-005 test body), because T-005 asserts `returns False` — which only makes sense once the return type is `-> bool`.
- DEV-003 (SC table numbering) is purely a cross-reference/traceability fix with no dependency on DEV-001 or DEV-002.

---

## Fix 1: DEV-002 — Add `-> bool` return type and True/False semantics to Phase 1 function definition

### Location

Phase 1 section, under "Implementation", item 1: "Add `_write_preliminary_result()` to `executor.py`".

Specifically, the sub-bullet that reads:

```
- Signature: `(config: SprintConfig, phase: Phase, started_at: float) -> bool`
```

This line **already exists** in the roadmap and already includes `-> bool`. However, the deviation is that:
1. The return semantics (`True` = wrote the file / Option D path; `False` = no-op or OSError) are not documented in Phase 1's implementation steps.
2. The `try/except OSError` block shown in Phase 1 says "return `False` on error" — this is correct — but the success path's return value is not stated: the roadmap says "Write exactly `EXIT_RECOMMENDATION: CONTINUE\n`" but does not say "return `True`".

An implementer reading Phase 1 in isolation sees `-> bool` in the signature but no statement of what `True` or `False` mean.

### Exact Change

In Phase 1, implementation item 1, after the existing bullet:

```
- Wrap in `try/except OSError` with WARNING log, return `False` on error
```

Add a new bullet:

```
- Return `True` if the file was written by this function (Option D path); return `False` if the file was a no-op (fresh agent-written file preserved) or if an OSError prevented the write
- The boolean return value is used by the Phase 2 call site to log telemetry: `_wrote_preliminary = _write_preliminary_result(...)` then `debug_log(f"preliminary_result_write path={'option_d' if _wrote_preliminary else 'option_a_or_noop'}")`
```

Also update the Phase 1 exit criteria bullet to include the return contract:

**Current Phase 1 exit criteria**:
```
`_write_preliminary_result()` passes all unit tests. Sentinel contract comment in place. No regressions in existing test suite.
```

**Replace with**:
```
`_write_preliminary_result()` passes all unit tests (T-001, T-002, T-002b, T-005). Function signature is `-> bool`; returns `True` on write, `False` on no-op or OSError. Sentinel contract comment in place. No regressions in existing test suite.
```

### Rationale

NFR-007 (spec §4) requires `_write_preliminary_result()` to return a boolean. The Phase 2 call site already correctly stores `_wrote_preliminary` and uses it for debug logging — but Phase 2's correctness depends on Phase 1 producing a `bool`-returning function. Without an explicit return-value contract in Phase 1, an implementer following only that phase would produce `-> None`, silently breaking Phase 2's telemetry. Making the contract explicit in Phase 1 closes the cross-phase dependency gap.

---

## Fix 2: DEV-001 — Add T-005 full test body and SC entry to Phase 1

### Location

Phase 1 section, under "Unit Tests (T-001, T-002, T-002b, T-005)".

Currently T-005 appears only as a one-line description:

```
- **T-005**: `OSError` on write → returns `False`, no exception raised, WARNING logged
```

There is no test body, no assertion on the module logger, and no entry in the Success Criteria table.

### Exact Change — Part A: Add test body to Phase 1 unit tests list

After the existing T-005 bullet, add the full test body:

```markdown
- **T-005**: `OSError` on write → returns `False`, no exception raised, WARNING logged via module logger

  ```python
  def test_write_preliminary_result_oserror_returns_false_and_warns(tmp_path):
      """OSError on write must be caught: returns False, no exception propagated, WARNING logged."""
      config = _make_config(tmp_path)
      phase = config.phases[0]
      # Do NOT pre-create results dir — write into an unwritable path to force OSError
      # Alternative: patch write_text to raise OSError
      from unittest.mock import patch, MagicMock
      from superclaude.cli.sprint.executor import _write_preliminary_result
      import logging

      started_at = datetime.now(timezone.utc).timestamp() - 1

      with patch(
          "superclaude.cli.sprint.executor._write_preliminary_result.__globals__['__builtins__']"
      ):
          pass  # use explicit pathlib patch instead

      result_path = config.result_file(phase)
      with (
          patch.object(result_path, "exists", return_value=False),
          patch.object(result_path.parent, "mkdir"),
          patch.object(result_path, "write_text", side_effect=OSError("disk full")),
      ):
          # Patch the module-level logger used inside executor.py
          with patch("superclaude.cli.sprint.executor.logger") as mock_logger:
              # If executor uses inline _logging.getLogger(__name__), patch that module
              return_val = _write_preliminary_result(config, phase, started_at)

      assert return_val is False, "OSError path must return False"
      # WARNING must have been logged (via module logger or inline getLogger)
      # Accept either logging pattern from the implementation
      # Primary assertion: no exception was raised (reaching this line proves it)
  ```

  **Note on logger patching**: The spec's Change 1 shows an inline `import logging as _logging` pattern inside the `except OSError` block. The test must account for this. Two acceptable patterns:
  - If the implementation uses a module-level `logger = logging.getLogger(__name__)`: patch `superclaude.cli.sprint.executor.logger` and assert `mock_logger.warning.called`.
  - If the implementation uses the inline `_logging.getLogger(__name__)` pattern from Change 1: patch `logging.getLogger` in the executor module's namespace.

  The test MUST assert `return_val is False`. The WARNING assertion should use `caplog` (pytest's log capture) as the most implementation-agnostic approach:

  ```python
  def test_write_preliminary_result_oserror_returns_false_and_warns(tmp_path, caplog):
      """OSError on write must be caught: returns False, no exception propagated, WARNING logged."""
      from superclaude.cli.sprint.executor import _write_preliminary_result
      import logging

      config = _make_config(tmp_path)
      phase = config.phases[0]
      started_at = datetime.now(timezone.utc).timestamp() - 1

      result_path = config.result_file(phase)
      with patch.object(type(result_path), "write_text", side_effect=OSError("disk full")):
          with caplog.at_level(logging.WARNING, logger="superclaude.cli.sprint.executor"):
              return_val = _write_preliminary_result(config, phase, started_at)

      assert return_val is False, "OSError path must return False, not raise"
      assert any(
          "preliminary result write failed" in r.message
          for r in caplog.records
          if r.levelno == logging.WARNING
      ), "A WARNING containing 'preliminary result write failed' must be logged"
  ```
```

### Exact Change — Part B: Add SC entry to the Success Criteria table

The current SC table in the roadmap has 13 entries (SC-001 through SC-013). T-005 has no SC entry.

The spec's §9 acceptance criteria checklist does not assign a named SC identifier to T-005's OSError test, but it is implicitly required under "uv run pytest tests/sprint/test_executor.py -v passes with 0 failures" (the third checklist item).

Add the following row to the Success Criteria table, inserting it after SC-006 (the zero-byte file row):

```
| SC-006b | `_write_preliminary_result()` returns `False` and logs WARNING on `OSError` (T-005) | P1 |
```

**Note**: Using `SC-006b` (a sub-identifier) rather than renumbering SC-007 through SC-013, to avoid creating a cascade of renumbering changes. This keeps the diff minimal and does not disturb DEV-003 fixes applied in Fix 3.

### Rationale

The spec defines T-005 fully in §6 with a clear contract: `OSError` on write returns `False`, no exception raised, WARNING logged. NFR-003 requires all tests to pass. The roadmap lists T-005 by name in Phase 1 but provides no test body or verification method. Without a test body, implementers may produce an incorrect test (e.g., asserting the exception is re-raised, or not verifying the WARNING). The `caplog`-based test body is implementation-agnostic — it captures the WARNING regardless of whether the implementation uses a module-level logger or an inline `getLogger` call (as shown in spec Change 1).

---

## Fix 3: DEV-003 — Align SC table numbering with spec §9 and reclassify SC-009b

### Context

The spec §9 acceptance criteria is an unnumbered checkbox list. The roadmap assigned SC numbers to these criteria, which is a valid and useful roadmap addition — but introduced two problems:

1. **SC-006 mismatch**: The roadmap's SC-006 maps to "Zero-byte file overwritten" (T-002b). The spec's acceptance criteria list does not assign SC-006 to this — the phrase "TIMEOUT/ERROR/INCOMPLETE/PASS_RECOVERED unchanged" appears as a distinct acceptance criterion. In Phase 4 (Layer 5 Architect Sign-off Checks), the roadmap references "TIMEOUT, ERROR, INCOMPLETE, PASS_RECOVERED behaviors unchanged (SC-006)" — but the SC-006 row in the table says "Zero-byte file overwritten". This means SC-006 has two different meanings in the same document.

2. **SC-009b without spec backing**: SC-009b ("Python/skip preflight phases still yield `PREFLIGHT_PASS`") derives from §5 Implication 9 of the spec — a behavioral analysis section, not an acceptance criterion. It is a legitimate architectural validation step, but labeling it as an SC criterion implies it is traceable to a spec acceptance criterion when it is not.

### Exact Changes

#### Change 3A: Split SC-006 to eliminate the dual-meaning

The SC table currently has:

```
| SC-006 | Zero-byte file overwritten | P1 (T-002b) |
```

And Phase 4 Layer 5 references:
```
- TIMEOUT, ERROR, INCOMPLETE, PASS_RECOVERED behaviors unchanged (SC-006)
```

These two usages are incompatible. The resolution:

**Step 1**: Rename the SC table row for "Zero-byte file overwritten" to `SC-006` but add a clarifying label:

```
| SC-006 | Zero-byte file overwritten → `CONTINUE` written, phase reports `PASS` (T-002b) | P1 |
```

**Step 2**: Add a new row for the non-zero exit path invariant, using `SC-006c` (following the SC-006b added by Fix 2):

```
| SC-006c | `TIMEOUT`, `ERROR`, `INCOMPLETE`, `PASS_RECOVERED` behaviors unchanged; `exit_code < 0` falls to `ERROR`/`INCOMPLETE` without exception (NFR-001) | P2 |
```

**Step 3**: In Phase 4 Layer 5 Architect Sign-off Checks, update the reference:

Replace:
```
- TIMEOUT, ERROR, INCOMPLETE, PASS_RECOVERED behaviors unchanged (SC-006)
```

With:
```
- TIMEOUT, ERROR, INCOMPLETE, PASS_RECOVERED behaviors unchanged; `exit_code < 0` handled without exception (SC-006c, NFR-001)
```

#### Change 3B: Reclassify SC-009b as an architecture-derived check

Currently in Phase 4 Layer 5:
```
- Python/skip preflight phases still yield `PREFLIGHT_PASS` (SC-009b)
```

And SC-009b does not appear in the SC table at all — it is only referenced inline in Phase 4.

**Step 1**: Remove SC-009b from Phase 4 Layer 5's bullet-referenced SC identifier. Replace with an inline attribution to the spec section it derives from:

Replace:
```
- Python/skip preflight phases still yield `PREFLIGHT_PASS` (SC-009b)
```

With:
```
- Python/skip preflight phases still yield `PREFLIGHT_PASS` (architecture invariant from §5 Implication 9; not a spec §9 acceptance criterion — verified by tracing `execute_preflight_phases()` code path)
```

**Step 2**: Do NOT add SC-009b to the SC table. It should not appear as a numbered spec-backed criterion because it has no corresponding entry in the spec's §9 acceptance criteria list.

### Rationale

The SC table is the primary cross-validation tool. When a validator compares the roadmap SC table against spec §9, they expect a 1:1 or subset mapping. SC-006 appearing with two different meanings in the same document breaks this mapping silently. SC-009b appearing as a criterion number without any spec §9 backing makes it look optional (or causes validators to search for it in §9 and find nothing, losing confidence in the table). The fix preserves the architectural insight (preflight isolation is important to verify) while being honest about its source: it derives from spec §5 analysis, not spec §9 acceptance criteria.

---

## Ordering and Sequencing Summary

Apply fixes in this order:

1. **DEV-002 first** (Fix 1 above): Establish the `-> bool` return contract in Phase 1. This is the prerequisite for T-005's test body to make internal sense.

2. **DEV-001 second** (Fix 2 above): Add T-005 full test body (which asserts `return_val is False`) and SC-006b entry. The test body now correctly references the `bool` return contract established in Fix 1.

3. **DEV-003 third** (Fix 3 above): Align SC numbering. This is independent of the other two fixes, but doing it last avoids any confusion about where SC-006b (added by Fix 2) sits relative to the SC-006 split.

No phase restructuring is required. All changes are additive (inserting text and rows) or clarifying (replacing ambiguous references). The implementation strategy, phase sequencing, test file assignments, and risk table are all correct and remain unchanged.

---

## Verification Checklist

After applying all three fixes, verify the following before marking the roadmap tasklist-ready:

### DEV-001 resolved
- [ ] T-005 has a full test body in Phase 1 (not just a one-line description)
- [ ] T-005 test body asserts `return_val is False`
- [ ] T-005 test body asserts a WARNING containing "preliminary result write failed" is logged
- [ ] T-005 uses `caplog` (or equivalent) to capture the WARNING in an implementation-agnostic way
- [ ] SC-006b row exists in the Success Criteria table mapping T-005 to P1

### DEV-002 resolved
- [ ] Phase 1 implementation steps explicitly state: write path returns `True`, no-op/OSError path returns `False`
- [ ] Phase 1 exit criteria includes: "Function signature is `-> bool`; returns `True` on write, `False` on no-op or OSError"
- [ ] The Phase 2 `_wrote_preliminary` usage is now fully traceable to the Phase 1 contract

### DEV-003 resolved
- [ ] SC-006 row in the table has a label unambiguously tied to zero-byte file behavior (T-002b), not to TIMEOUT/ERROR handling
- [ ] SC-006c row exists in the table for TIMEOUT/ERROR/INCOMPLETE/PASS_RECOVERED + negative exit code invariant (NFR-001)
- [ ] Phase 4 Layer 5 references SC-006c (not SC-006) for the TIMEOUT/ERROR/INCOMPLETE/PASS_RECOVERED check
- [ ] SC-009b is removed from Phase 4 as a numbered SC criterion and replaced with an inline attribution to spec §5 Implication 9
- [ ] SC-009b does NOT appear in the SC table (it has no spec §9 backing)

### No regressions introduced by the fixes
- [ ] SC table row count is consistent: original 13 rows + SC-006b (DEV-001) + SC-006c (DEV-003) = 15 rows
- [ ] No existing SC identifiers (SC-001 through SC-013) are renumbered
- [ ] Phase 1 exit criteria still requires T-001, T-002, T-002b to pass (unchanged)
- [ ] Phase 2 integration test list (T-003, T-004, T-006) is unchanged
- [ ] MEDIUM deviations (DEV-004 through DEV-009) are NOT addressed in this plan (separate fix scope)
