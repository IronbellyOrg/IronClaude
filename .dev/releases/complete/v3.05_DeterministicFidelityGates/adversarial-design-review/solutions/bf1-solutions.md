# BF-1 Solutions: ACTIVE Status Crashes __post_init__

## Problem Statement

Architecture design Sec 4.4.2 uses `status="ACTIVE"` for findings in the deviation registry.
The `Finding` dataclass in `models.py` validates status against `VALID_FINDING_STATUSES = {"PENDING", "FIXED", "FAILED", "SKIPPED"}`, raising `ValueError` on any other value.
Creating a `Finding(status="ACTIVE")` crashes at runtime.

---

## Solution A: Add ACTIVE alongside PENDING (Both Valid)

### Description
Add `"ACTIVE"` to `VALID_FINDING_STATUSES` so both `PENDING` and `ACTIVE` are accepted.
The deviation registry uses `ACTIVE`; existing pipeline code continues using `PENDING`.

### Code Changes

**`src/superclaude/cli/roadmap/models.py`** (1 line changed):
```python
# Before:
VALID_FINDING_STATUSES = frozenset({"PENDING", "FIXED", "FAILED", "SKIPPED"})

# After:
VALID_FINDING_STATUSES = frozenset({"PENDING", "ACTIVE", "FIXED", "FAILED", "SKIPPED"})
```

**Docstring update** (models.py line 27):
```python
# Before:
#   PENDING -> FIXED | FAILED | SKIPPED (all terminal).
# After:
#   PENDING/ACTIVE -> FIXED | FAILED | SKIPPED (all terminal).
```

### Lines Changed: 2

### Backward Compatibility: FULL
- All existing code using `status="PENDING"` continues to work unchanged.
- No test modifications required.
- The default `status: str = "PENDING"` remains.

### Risk to Pipeline Steps 1-7: NONE
- Steps 1-7 never use `"ACTIVE"`. They are untouched.
- The deviation registry (new module, not yet implemented) will use `"ACTIVE"`.

### FR-6 Alignment
- FR-6 lists "FIXED, SKIPPED, FAILED" as terminal statuses. It does not prescribe the initial status name.
- `ACTIVE` is a synonym for `PENDING` used by the registry for clarity.
- Both `PENDING` and `ACTIVE` map to the same lifecycle position: "not yet resolved."
- **Partial alignment**: FR-6 does not mention ACTIVE, but doesn't prohibit it either. Having two synonymous initial statuses creates semantic ambiguity.

---

## Solution B: Replace PENDING with ACTIVE Everywhere

### Description
Remove `"PENDING"` from `VALID_FINDING_STATUSES`, add `"ACTIVE"`, change the default, and update all references throughout the codebase.

### Code Changes

**`src/superclaude/cli/roadmap/models.py`** (3 lines changed):
```python
VALID_FINDING_STATUSES = frozenset({"ACTIVE", "FIXED", "FAILED", "SKIPPED"})
# Docstring: ACTIVE -> FIXED | FAILED | SKIPPED
status: str = "ACTIVE"
```

**`src/superclaude/cli/roadmap/remediate.py`** (4 occurrences):
- Line 173: `f.status == "PENDING"` -> `f.status == "ACTIVE"`
- Line 174: `f.status != "PENDING"` -> `f.status != "ACTIVE"`
- Line 369: `status="PENDING"` -> `status="ACTIVE"`

**`src/superclaude/cli/roadmap/remediate_executor.py`** (3 occurrences):
- Line 320: `f.status == "PENDING"` -> `f.status == "ACTIVE"`
- Line 366: `"PENDING"` in status check -> `"ACTIVE"`

**`src/superclaude/cli/roadmap/remediate_parser.py`** (3 occurrences):
- Lines 168, 389: `status="PENDING"` -> `status="ACTIVE"`

**`src/superclaude/cli/roadmap/gates.py`** (3 occurrences in comments/logic):
- Lines 220, 224: Comments referencing PENDING -> ACTIVE

**Tests** (~30+ occurrences across 10 test files):
- Every `status="PENDING"` and `"PENDING"` assertion must change.
- Files: test_certify_prompts.py, test_integration_v5_pipeline.py, test_inline_fallback.py, test_remediate_prompts.py, test_remediate.py, test_phase7_hardening.py, test_pipeline_integration.py, test_remediate_parser.py, test_models.py, test_remediate_executor.py, test_checkpoint.py

### Lines Changed: ~50+ (source) + ~30+ (tests) = ~80+ total

### Backward Compatibility: BREAKING
- Any external code, serialized data, or config files using `status="PENDING"` will break.
- The `remediate.py` fallback `record.get("status", "PENDING")` at line 369 would need updating.
- Any persisted remediation tasklists with "PENDING" entries become invalid.

### Risk to Pipeline Steps 1-7: LOW-MEDIUM
- Steps 1-7 don't directly create Findings, but step 5 (spec-fidelity) and step 6 (remediate) do.
- If any intermediate files on disk contain "PENDING", the pipeline could break on resume.

### FR-6 Alignment
- FR-6 says "FIXED, SKIPPED, FAILED (matching current system)" for terminal statuses.
- Changing the initial status from PENDING to ACTIVE does not violate FR-6 (it only lists terminals).
- However, FR-6 says "matching current system" -- the current system uses PENDING.
- Architecture Sec 4.4.2 explicitly says ACTIVE replaces PENDING "for registry clarity."
- **Stronger alignment with architecture**, but **weaker alignment with FR-6's "matching current system"** phrase.

---

## Adversarial Comparison

| Criterion                    | Weight | Solution A (Add ACTIVE) | Solution B (Replace PENDING) |
|------------------------------|--------|------------------------|------------------------------|
| Backward Compatibility       | 40%    | 10/10 - Zero breakage  | 4/10 - ~80 lines, breaking  |
| Alignment with Requirements  | 30%    | 7/10 - FR-6 neutral, arch satisfied | 8/10 - Arch aligned, FR-6 "matching current" tension |
| Simplicity                   | 30%    | 10/10 - 2-line change  | 3/10 - 80+ lines across 15 files |
| **Weighted Score**           |        | **8.9**                | **4.9**                      |

### Scoring Detail

**Backward Compatibility (40%)**:
- A: 10 * 0.4 = 4.0
- B: 4 * 0.4 = 1.6

**Alignment (30%)**:
- A: 7 * 0.3 = 2.1
- B: 8 * 0.3 = 2.4

**Simplicity (30%)**:
- A: 10 * 0.3 = 3.0
- B: 3 * 0.3 = 0.9

**Totals**: A = 9.1, B = 4.9

## Winner: Solution A

Solution A wins decisively. It satisfies the architecture requirement (deviation registry can use `ACTIVE`) without touching any existing code. The semantic overlap between PENDING and ACTIVE is a minor concern that can be addressed with documentation: PENDING is the legacy/pipeline term, ACTIVE is the registry term, both mean "not yet resolved."
