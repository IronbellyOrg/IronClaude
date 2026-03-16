# Fix Plan: MEDIUM Severity Deviations (DEV-004 through DEV-009)

**Roadmap**: `roadmap-pass-no-report-fix/roadmap.md`
**Spec**: `artifacts/pass-no-report-fix-spec.md`
**Source report**: `roadmap-pass-no-report-fix/spec-fidelity.md`
**Date**: 2026-03-16

---

## Overview

Six MEDIUM severity deviations require targeted edits to `roadmap.md`. No structural
sections need to be added or removed — all fixes are either text substitutions, additions
to existing bullet lists, or additions to the existing success criteria table. The roadmap
structure remains intact.

### Fix Complexity Classification

| ID | Type | Effort |
|----|------|--------|
| DEV-004 | Text substitution — one token swap | Trivial |
| DEV-005 | Two additions: SC table row + exit criteria bullet | Simple |
| DEV-006 | Text expansion — strengthen one test description | Simple |
| DEV-007 | Two changes: strengthen assertion wording + add cross-ref note | Simple |
| DEV-008 | One addition: exit criteria bullet | Simple |
| DEV-009 | One addition: verification step bullet | Simple |

### Grouping Strategy

Apply fixes in three passes, ordered by section proximity in the roadmap:

- **Pass A (Phase 1 section)**: DEV-005, DEV-006, DEV-008 — all three touch Phase 1 content
- **Pass B (Phase 2 section)**: DEV-004, DEV-009 — both touch Phase 2 content
- **Pass C (Phase 3 section)**: DEV-007 — touches Phase 3 content
- **Pass D (SC table)**: DEV-005 SC row addition — touches the global success criteria table

Passes A–C can be applied left-to-right through the file; Pass D (SC table) is at the
bottom of the roadmap and should be applied last to avoid offset confusion.

---

## Pass A: Phase 1 Fixes (DEV-005, DEV-006, DEV-008)

### DEV-006 — Strengthen T-005 description in Phase 1

**Location**: Phase 1, "Unit Tests" subsection, T-005 bullet (roadmap line 98)

**Current text**:
```
- **T-005**: `OSError` on write → returns `False`, no exception raised, WARNING logged
```

**Replacement text**:
```
- **T-005**: `OSError` on write → returns `False`, no exception raised, WARNING emitted
  via the module logger (`logging.getLogger(__name__)`) with the exact message format:
  `"preliminary result write failed: %s; phase may report PASS_NO_REPORT"` (FR-001)
```

**Rationale**: The spec (FR-001, §3) specifies both the logger identity (`getLogger(__name__)`)
and the exact `%s`-style message string. The roadmap's "WARNING logged" is too weak — a test
asserting only that any warning was logged could pass with a wrong logger or wrong message.
Strengthening the description ensures the test author asserts the correct logger namespace
and message template.

---

### DEV-005 — Add NFR-006 to Phase 1 exit criteria

**Location**: Phase 1, "Exit Criteria" paragraph (roadmap line 103–104)

**Current text**:
```
`_write_preliminary_result()` passes all unit tests. Sentinel contract comment in place.
No regressions in existing test suite.
```

**Replacement text**:
```
`_write_preliminary_result()` passes all unit tests. Sentinel contract comment in place
per NFR-006 (comment added at the `CONTINUE`-check point inside `_determine_phase_status()`
documenting the `EXIT_RECOMMENDATION: CONTINUE` sentinel contract). TOCTOU/concurrency
limitation documented in `_write_preliminary_result()` docstring per NFR-002. No regressions
in existing test suite.
```

**Rationale**: NFR-006 is mentioned in the Phase 1 implementation steps ("do not defer") but
absent from the exit criteria. Without an exit-criteria entry, a reviewer completing Phase 1
has no checklist item to verify the sentinel comment was actually placed. The TOCTOU docstring
note (NFR-002, DEV-008) is co-located here since it is also a Phase 1 docstring requirement —
combining them in the exit criteria avoids two separate exit criteria edits in the same block.

---

### DEV-008 — NFR-002 TOCTOU note

**Disposition**: Resolved jointly with DEV-005 above (both are Phase 1 exit criteria additions
to the same paragraph). The combined replacement text above covers both deviations. No
additional edit required.

---

## Pass B: Phase 2 Fixes (DEV-004, DEV-009)

### DEV-004 — Replace non-existent `FR-008` reference

**Location**: Phase 2, "Implementation" subsection, item 2 (roadmap line 122–126)

**Current text**:
```
2. **Verify ordering invariant** (FR-008)
   - Confirm the three calls appear in this exact order:
     1. `_write_preliminary_result()`
     2. `_determine_phase_status()`
     3. `_write_executor_result_file()`
```

**Replacement text**:
```
2. **Verify ordering invariant** (FR-001 ordering invariant, FR-002)
   - Confirm the three calls appear in this exact order:
     1. `_write_preliminary_result()`
     2. `_determine_phase_status()`
     3. `_write_executor_result_file()`
```

**Rationale**: `FR-008` does not exist in the spec. The ordering invariant is defined in
FR-001 ("Ordering invariant (see FR-002): This function MUST always be called BEFORE...") and
FR-002 (injection site requirements). Referencing a non-existent FR causes traceability
failure — an implementer checking this against the spec finds nothing and may treat the
invariant as advisory. Using `(FR-001 ordering invariant, FR-002)` traces directly to the
normative spec text.

---

### DEV-009 — Add explicit `exit_code < 0` verification to Phase 2

**Location**: Phase 2, "Implementation" subsection, item 3 (roadmap lines 128–130)

**Current text**:
```
3. **Verify non-zero exit paths untouched** (FR-005, NFR-001)
   - Trace TIMEOUT, ERROR, INCOMPLETE, PASS_RECOVERED paths — none should reach
     `_write_preliminary_result()`
```

**Replacement text**:
```
3. **Verify non-zero exit paths untouched** (FR-005, NFR-001)
   - Trace TIMEOUT, ERROR, INCOMPLETE, PASS_RECOVERED paths — none should reach
     `_write_preliminary_result()`
   - Explicitly verify `exit_code < 0` (signal-killed subprocess, e.g. SIGKILL=-9,
     SIGTERM=-15): `_determine_phase_status()` must fall through to ERROR or INCOMPLETE
     without raising — not raise an exception (NFR-001)
```

**Rationale**: NFR-001 specifically calls out negative exit codes as a distinct verification
target: "On Linux, a subprocess killed by a signal returns a negative `returncode`... Verify
that `_determine_phase_status()` handles `exit_code < 0` without exception." The roadmap's
OQ-005 raises this as a Phase 0 question but frames it as discovery, not a mandatory
post-implementation gate. Adding an explicit Phase 2 bullet closes the gap: even if OQ-005
found no issue, Phase 2 must confirm the negative-exit path is clean after the patch lands.

---

## Pass C: Phase 3 Fix (DEV-007)

### DEV-007 — Strengthen `as_posix()` assertion and add OQ-001 explicit forward reference

**Location**: Phase 3, "Implementation" subsection, item 2 (roadmap lines 165–169)

**Current text**:
```
2. **Write prompt assertion test**
   - Verify `prompt.rindex("## Result File") > prompt.rindex("## Important")` (SC-013)
   - Verify path is absolute and uses POSIX separators
   - Verify no existing sections repositioned
```

**Replacement text**:
```
2. **Write prompt assertion test**
   - Verify `prompt.rindex("## Result File") > prompt.rindex("## Important")` (SC-013)
   - Verify path is formatted using `config.result_file(self.phase).as_posix()` — assert
     the path string in the prompt exactly matches `config.result_file(phase).as_posix()`
     (FR-006 constraint: `as_posix()` is required, not just "absolute with POSIX
     separators" — a relative POSIX path would satisfy the weaker check but violate the spec)
   - Confirm OQ-001 was resolved in M0: the attribute name used in `build_prompt()` must
     match the actual attribute set by `ClaudeProcess.__init__` — do not assume `self.phase`
     without verifying against the constructor (FR-006)
   - Verify no existing sections repositioned
```

**Rationale**: The spec (FR-006) has two explicit constraints that the current roadmap
understates. First, "The injected path MUST use `config.result_file(self.phase).as_posix()`"
— `as_posix()` is normative; "absolute and uses POSIX separators" is a weaker description
that a relative POSIX path could satisfy. Second, "Verify attribute name: The attribute
`self.phase` in `build_prompt()` must match the actual attribute name set in
`ClaudeProcess.__init__`. Confirm against the constructor before implementing." The Phase 3
implementation already references OQ-001 ("attribute name confirmed in M0 via OQ-001") but
the verification step does not echo this gate, so a rushed implementer could skip it.

---

## Pass D: Success Criteria Table Fix (DEV-005)

### DEV-005 — Add NFR-006 row to SC table

**Location**: Success Criteria table (roadmap lines 268–283), after the SC-013 row (last row)

**Current table tail** (last two rows):
```
| SC-012 | Pre-implementation baseline green | P0 |
| SC-013 | `## Result File` is last `##` section in built prompt | P3 |
```

**Replacement** (append new row):
```
| SC-012 | Pre-implementation baseline green | P0 |
| SC-013 | `## Result File` is last `##` section in built prompt | P3 |
| SC-014 | Sentinel contract comment present in `_determine_phase_status()` at `CONTINUE`-check point (NFR-006) | P1 |
```

**Rationale**: NFR-006 requires the sentinel comment to be verifiable as an acceptance
criterion. Without an SC entry, the validation matrix has no explicit row to check off during
Phase 4. SC-014 assigns it to P1, matching where the implementation step lives, and makes
it a first-class checkable item in the architect sign-off layer (Phase 4, Layer 5).

---

## Interdependency Notes

- DEV-005 and DEV-008 are co-located in the Phase 1 exit criteria paragraph. Applying them
  together (as shown in Pass A) is more efficient than two separate edits.
- DEV-005 also requires the SC table addition (Pass D). The Phase 1 exit criteria edit and
  the SC table edit are independent of each other's text but both belong to DEV-005.
- All other deviations (DEV-004, DEV-006, DEV-007, DEV-009) are fully independent of each
  other and can be applied in any order.
- No fix changes the section structure, heading hierarchy, or phase ordering of the roadmap.

---

## Final Verification Checklist

After applying all edits, verify each MEDIUM deviation is resolved:

- [ ] **DEV-004**: Phase 2, item 2 header reads `(FR-001 ordering invariant, FR-002)` —
      `FR-008` no longer appears anywhere in the roadmap
- [ ] **DEV-005 (exit criteria)**: Phase 1 exit criteria paragraph includes "Sentinel contract
      comment in place per NFR-006" with explicit reference to `_determine_phase_status()`
- [ ] **DEV-005 (SC table)**: SC-014 row exists in the success criteria table, maps NFR-006
      to P1
- [ ] **DEV-006**: T-005 bullet in Phase 1 specifies `logging.getLogger(__name__)` and the
      exact message format `"preliminary result write failed: %s; phase may report
      PASS_NO_REPORT"`
- [ ] **DEV-007 (as_posix)**: Phase 3 assertion step specifies `config.result_file(self.phase).as_posix()`
      by name, not just "absolute and POSIX separators"
- [ ] **DEV-007 (OQ-001)**: Phase 3 assertion step includes explicit instruction to confirm
      OQ-001 attribute name resolution before implementing
- [ ] **DEV-008**: Phase 1 exit criteria paragraph includes "TOCTOU/concurrency limitation
      documented in docstring per NFR-002"
- [ ] **DEV-009**: Phase 2, item 3 includes a bullet explicitly checking `exit_code < 0`
      falls through to ERROR/INCOMPLETE without raising

**Cross-check**: Run a text search for `FR-008` in the updated roadmap — it must return zero
matches. Run a search for `NFR-006` — it must appear in both the Phase 1 exit criteria and
the SC table.
