# Remediation Plan: v3.3 TurnLedger Validation

**Generated**: 2026-03-23
**Verdict**: GO
**Total Findings**: 3 (0 CRITICAL, 0 HIGH, 2 MEDIUM, 1 LOW)

---

## Executive Summary

Since the verdict is **GO**, no blocking remediation is required. The following items are **optional improvements** that can be applied to improve roadmap completeness without blocking tasklist generation.

---

## Remediation Phases

### Phase R8: Low-Priority and Cleanup (Optional)

These remediations are **recommended but not required** for GO status.

#### GAP-M001: FR-1.19 SHADOW_GRACE_INFINITE Explicit Coverage

- **Current Status**: PARTIAL (implicitly covered via FR-3.1b shadow mode tests)
- **Recommended Action**: Add explicit test mention in Phase 2A table
- **Effort**: TRIVIAL

**Patch**:
```markdown
# In roadmap.md Phase 2A table, add to 2A.5 row:
| 2A.5 | FR-1.9 – FR-1.10, FR-1.19 | 3 tests: Gate result accumulation; SHADOW_GRACE_INFINITE constant validation |
```

#### GAP-M002: FR-1.20 __post_init__ Derivation Explicit Coverage

- **Current Status**: PARTIAL (implicitly covered via config tests)
- **Recommended Action**: Add explicit test mention in Phase 2A table
- **Effort**: TRIVIAL

**Patch**:
```markdown
# In roadmap.md Phase 2A table, add new row:
| 2A.13 | FR-1.20 | 1 test: __post_init__() config derivation validation |
```

#### ADV-001: Document Orphan Tasks 4.5 and 4.6

- **Current Status**: LOW (orphan tasks without spec traceability)
- **Recommended Action**: Document as "Release Engineering Tasks" section
- **Effort**: TRIVIAL

**Patch**:
```markdown
# In roadmap.md Phase 4 table, add note column:
| 4.5 | — | Generate final wiring-verification artifact | Release engineering task |
| 4.6 | — | Update docs/memory/solutions_learned.jsonl | Release engineering task |
```

---

## Patch Checklist

- [ ] **GAP-M001** (MEDIUM, TRIVIAL): Add FR-1.19 to Phase 2A.5 description
  - File: roadmap.md
  - Action: EDIT
  - Change: Extend 2A.5 to mention SHADOW_GRACE_INFINITE
  - Dependencies: None

- [ ] **GAP-M002** (MEDIUM, TRIVIAL): Add FR-1.20 to Phase 2A table
  - File: roadmap.md
  - Action: ADD
  - Change: Add 2A.13 row for __post_init__ derivation
  - Dependencies: None

- [ ] **ADV-001** (LOW, TRIVIAL): Document tasks 4.5 and 4.6 as release engineering
  - File: roadmap.md
  - Action: EDIT
  - Change: Add note column or parenthetical to Phase 4 table
  - Dependencies: None

---

## Remediation Impact Projection

If all remediations applied:

| Metric | Before | After |
|--------|--------|-------|
| Weighted Coverage | 98.1% | 98.1% |
| PARTIAL Findings | 2 | 0 |
| LOW Findings | 1 | 0 |
| Total Findings | 3 | 0 |
| Verdict | GO | GO |

**Note**: Coverage improvement is minimal because PARTIAL items already receive 0.5 weight. The benefit is explicit traceability, not coverage percentage.

---

## Verification Steps

After applying remediations:

1. Re-run `/sc:validate-roadmap` to confirm:
   - No PARTIAL findings remain
   - No LOW findings remain
   - Verdict remains GO
   - All remediations properly applied

2. Verify task IDs remain unique after additions

3. Verify FR references in spec still match roadmap

---

## Next Steps

Since verdict is **GO**:

1. **Option A** (Recommended): Proceed directly to `/sc:tasklist` generation. Apply optional remediations later.

2. **Option B** (Thorough): Apply optional remediations first, then re-validate, then proceed to `/sc:tasklist`.

Both options are valid. The roadmap is ready for tasklist generation as-is.
