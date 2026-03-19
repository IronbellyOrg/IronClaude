# BF-1 Resolution: Add ACTIVE to Valid Finding Statuses

## Selected Solution

**Solution A**: Add `"ACTIVE"` to `VALID_FINDING_STATUSES` alongside `"PENDING"`.

**Rationale**: Solution A wins by weighted score 9.1 vs 4.9 (B). The decisive factors:

1. **Zero backward compatibility risk** (40% weight, scored 10/10). No existing code changes. No test updates. No risk of breaking persisted data or pipeline steps 1-7.
2. **Maximal simplicity** (30% weight, scored 10/10). A 2-line change vs 80+ lines across 15 files.
3. **Adequate requirements alignment** (30% weight, scored 7/10). FR-6 specifies terminal statuses (FIXED, SKIPPED, FAILED) but does not prescribe the initial status name. The architecture's use of ACTIVE for registry clarity is fully enabled without removing PENDING from the existing pipeline vocabulary.

Solution B (replace PENDING with ACTIVE everywhere) provides marginally better architecture alignment but at catastrophic cost: 80+ changed lines, breaking changes to serialized data, and risk to pipeline resume behavior.

## Architecture Design Change

In `architecture-design.md` Section 4.4, add a clarifying note after the status values line (line ~582):

```markdown
- **Status values**: `ACTIVE`, `FIXED`, `FAILED`, `SKIPPED` — matching existing `Finding.status` but with `ACTIVE` replacing `PENDING` for registry clarity.
- **Note**: Both `ACTIVE` and `PENDING` are valid initial statuses in the `Finding` dataclass. The deviation registry uses `ACTIVE`; existing pipeline steps use `PENDING`. Both represent the same lifecycle state: "not yet resolved." The distinction is cosmetic — `ACTIVE` reads better in registry context (a finding is actively tracked), while `PENDING` is the legacy default in pipeline code.
```

## Code Change Specification

### File: `src/superclaude/cli/roadmap/models.py`

**Change 1** — Line 16, add ACTIVE to valid statuses:
```python
# Before:
VALID_FINDING_STATUSES = frozenset({"PENDING", "FIXED", "FAILED", "SKIPPED"})

# After:
VALID_FINDING_STATUSES = frozenset({"PENDING", "ACTIVE", "FIXED", "FAILED", "SKIPPED"})
```

**Change 2** — Line 27, update docstring lifecycle:
```python
# Before:
#     PENDING -> FIXED | FAILED | SKIPPED (all terminal).

# After:
#     PENDING/ACTIVE -> FIXED | FAILED | SKIPPED (all terminal).
```

**No other files require changes.**

### Files NOT Changed (and why)
- `remediate.py` — continues using `"PENDING"`, which remains valid
- `remediate_executor.py` — continues using `"PENDING"`, which remains valid
- `remediate_parser.py` — continues using `"PENDING"`, which remains valid
- `gates.py` — checks for terminal statuses (FIXED/FAILED), unaffected
- All test files — all use `"PENDING"` which remains valid

## Backward Compatibility

**Impact: None.**

- `PENDING` remains a valid status and the default for `Finding.status`.
- All existing Finding instances, serialized data, and pipeline behavior are unchanged.
- The new `deviation_registry.py` module (not yet implemented) can freely use `status="ACTIVE"` without triggering the `__post_init__` ValueError.
- Pipeline resume from persisted state with `"PENDING"` entries continues to work.
- No test changes required.

## Validation

### Manual Verification
```python
from superclaude.cli.roadmap.models import Finding

# Existing behavior preserved:
f1 = Finding(id="F-01", severity="HIGH", dimension="completeness",
             description="test", location="FR-1", evidence="ev",
             fix_guidance="fix")
assert f1.status == "PENDING"  # default unchanged

# New behavior enabled:
f2 = Finding(id="F-02", severity="HIGH", dimension="completeness",
             description="test", location="FR-1", evidence="ev",
             fix_guidance="fix", status="ACTIVE")
assert f2.status == "ACTIVE"  # no longer crashes

# Invalid statuses still rejected:
try:
    Finding(id="F-03", severity="HIGH", dimension="completeness",
            description="test", location="FR-1", evidence="ev",
            fix_guidance="fix", status="INVALID")
    assert False, "Should have raised ValueError"
except ValueError:
    pass  # correct behavior
```

### Automated Test
Add to `tests/roadmap/test_models.py`:
```python
def test_finding_active_status_valid():
    """BF-1: ACTIVE status must be accepted for deviation registry use."""
    f = Finding(
        id="F-01", severity="HIGH", dimension="completeness",
        description="test", location="FR-1", evidence="ev",
        fix_guidance="fix", status="ACTIVE",
    )
    assert f.status == "ACTIVE"
```

### Existing Test Suite
Run `uv run pytest tests/roadmap/test_models.py -v` to confirm no regressions.
All existing tests pass without modification since PENDING remains valid.
