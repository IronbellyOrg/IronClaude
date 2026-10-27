# Merged Proposal: Section-Scoped Duplicate Heading Gate Fix

**Date**: 2026-04-03
**Status**: Implementation-Ready
**Bug**: `_no_duplicate_headings` in `gates.py` performs flat global H3 duplicate detection, causing false positives on structurally valid multi-phase roadmaps.
**Derived from**: proposal-brainstorm.md, proposal-design.md, proposal-improve.md

---

## Adversarial Analysis Summary

### Where all three proposals agree

1. **Root cause**: The flat global `set` for H3 headings is structurally wrong. Repeated subsection names (`### Tasks`, `### Exit Criteria`, `### Risk Burn-Down`) under different `## Phase N` parents are legitimate.
2. **Core fix**: Section-scoped H3 duplicate detection -- track the current H2 parent and reset/scope H3 tracking per parent. H2 remains globally unique.
3. **Edge case: orphan H3s**: H3 headings appearing before any H2 should be scoped together (preamble/top-level scope). Duplicates within that scope are still caught.
4. **Existing tests survive**: The existing `test_no_duplicate_headings_h3_dup` (orphan H3 duplicates) and `test_duplicate_h3_headings_detected` (same-parent H3 dups) remain valid failures under scoped detection. No existing test needs its expected outcome reversed.
5. **Risk**: LOW -- mechanical, single-pass, backward-compatible.

### Where they disagree: error reporting

| Aspect | Brainstorm | Design | Improve |
|--------|-----------|--------|---------|
| **Return type** | `bool \| str` (return diagnostic string on failure) | `CheckResult` dataclass with `__bool__` | Keep `bool`, use module-global side-channel or `last_detail` field on `SemanticCheck` |
| **Model change** | Update `SemanticCheck.check_fn` type hint to `Callable[[str], bool \| str]` | Add `CheckResult` to `models.py`, update consumer with `hasattr` guard | Add `last_detail: str \| None = None` to `SemanticCheck`, or defer entirely |
| **Consumer change** | `result is not True` + `isinstance(result, str)` dispatch | `hasattr(result, "details")` duck-typing | Reset `last_detail` before call, read after |
| **Breaking risk** | None -- `bool` returns still work via `is not True` check | Medium -- `is True`/`is False` assertions break with `CheckResult` | None if deferred; low if `last_detail` added |

### Strengths and weaknesses per proposal

**Brainstorm** (strongest: breadth of alternatives, backward-compat analysis)
- Explored 7 approaches and correctly eliminated exemption lists, regex patterns, configurable scoping, content hashing, and split checks as over-engineered or philosophically wrong
- `bool | str` return is the simplest enrichment with zero breaking changes
- Weakness: did not provide complete test code, only a checklist

**Design** (strongest: edge case catalog, test matrix)
- Most thorough edge-case table (empty headings, leading whitespace, code blocks, no headings)
- Identified the `is True`/`is False` assertion breakage with `CheckResult` -- a real trap
- Most comprehensive test plan (10 new tests + regression fixture)
- Weakness: `CheckResult` dataclass is heavier than needed for a single check; the `__bool__` trick creates a subtle API where `bool(result)` and `result.passed` can diverge in testing assertions

**Improve** (strongest: pragmatism, minimal footprint)
- Correctly identified that diagnostic enrichment can be deferred
- Pragmatic recommendation: fix the scoping bug now, enrichment later
- Weakness: module-global `_duplicate_heading_detail` is the ugliest pattern (thread-unsafe, implicit coupling) -- and the proposal itself calls it out as non-ideal

### Resolution

The merged approach takes:
- **Core fix**: Section-scoped detection (all three agree)
- **Error reporting**: `bool | str` return convention from Brainstorm -- simplest, zero breaking changes, no new types, backward compatible
- **Test strategy**: Design's comprehensive test matrix with Improve's concrete test code
- **Footprint**: Three files changed, zero files created (excluding tests). No `CheckResult` dataclass. No module globals. No `last_detail` field.

---

## 1. Implementation

### 1a. Rewrite `_no_duplicate_headings` in `src/superclaude/cli/roadmap/gates.py`

**Replace lines 92-107** with:

```python
def _no_duplicate_headings(content: str) -> bool | str:
    """No duplicate H2 globally; no duplicate H3 within the same H2 section.

    Returns True on pass. Returns a descriptive string on failure (which is
    truthy but not ``True``; the consumer tests ``result is not True``).
    """
    seen_h2: set[str] = set()
    current_h2: str | None = None
    h3_by_section: dict[str | None, set[str]] = {None: set()}

    for lineno, line in enumerate(content.splitlines(), start=1):
        stripped = line.lstrip()

        if stripped.startswith("## ") and not stripped.startswith("### "):
            text = stripped[3:].strip().lower()
            if text in seen_h2:
                return (
                    f"Duplicate H2 heading '## {stripped[3:].strip()}' "
                    f"at line {lineno}"
                )
            seen_h2.add(text)
            current_h2 = text
            h3_by_section.setdefault(current_h2, set())

        elif stripped.startswith("### "):
            text = stripped[4:].strip().lower()
            section_set = h3_by_section.setdefault(current_h2, set())
            if text in section_set:
                parent_label = current_h2 or "(top-level)"
                return (
                    f"Duplicate H3 heading '### {stripped[4:].strip()}' "
                    f"at line {lineno} within section '## {parent_label}'"
                )
            section_set.add(text)

    return True
```

**Key design decisions**:
- H3s before any H2 are scoped to `None` key. Duplicates in preamble are still caught.
- `setdefault` eliminates the redundant `get` + reassign pattern.
- Returns `True` (bool) on pass, a descriptive `str` on failure.
- The `str` return is truthy, so the consumer MUST test `result is not True` (not `if not result`). This is an intentional design choice that provides richer information without adding types.

### 1b. Update consumer in `src/superclaude/cli/pipeline/gates.py`

**Replace lines 66-72** (the semantic check loop body):

```python
    # STRICT: semantic checks
    if criteria.semantic_checks:
        for check in criteria.semantic_checks:
            result = check.check_fn(content)
            if result is not True:
                detail = result if isinstance(result, str) else check.failure_message
                return (
                    False,
                    f"Semantic check '{check.name}' failed: {detail}",
                )
```

**Backward compatibility**: Existing `bool`-returning checks return `False` on failure. `False is not True` evaluates to `True` (enters the branch). `isinstance(False, str)` is `False`, so the fallback `check.failure_message` is used. Existing behavior is preserved exactly.

### 1c. Update type annotation in `src/superclaude/cli/pipeline/models.py`

**Line 63**: Change the `check_fn` type hint for documentation clarity:

```python
check_fn: Callable[[str], bool | str]
```

This is a type-annotation-only change. No runtime impact. Existing `bool`-returning functions are assignable to `bool | str`.

### 1d. Update `MERGE_GATE` failure message (optional)

In `src/superclaude/cli/roadmap/gates.py`, update the `SemanticCheck` registration for `no_duplicate_headings` to reflect the new scoping:

```python
SemanticCheck(
    name="no_duplicate_headings",
    check_fn=_no_duplicate_headings,
    failure_message="Duplicate H2 (global) or H3 (within same H2 section) heading detected",
),
```

This message is now a fallback only (the `str` return provides richer detail), but should still accurately describe the check's behavior.

---

## 2. Files Modified

| File | Change | Lines |
|------|--------|-------|
| `src/superclaude/cli/roadmap/gates.py` | Rewrite `_no_duplicate_headings` with section-scoped logic and `bool \| str` return; update `failure_message` | ~30 lines changed |
| `src/superclaude/cli/pipeline/gates.py` | Update semantic check evaluator to handle `str` returns via `result is not True` pattern | ~6 lines changed |
| `src/superclaude/cli/pipeline/models.py` | Update `check_fn` type hint from `Callable[[str], bool]` to `Callable[[str], bool \| str]` | 1 line changed |
| `tests/roadmap/test_gates_data.py` | Add `TestNoDuplicateHeadingsScoped` class with 10 new tests | ~80 lines added |

**No new files. No new types. No model additions.**

---

## 3. Test Plan

### 3a. Existing tests -- no changes needed

| Test | Why it still passes |
|------|-------------------|
| `test_no_duplicate_headings_clean` | `"## Alpha\n### Beta\n## Gamma\n### Delta\n"` -- all unique within scope. Returns `True`. `is True` assertion passes. |
| `test_no_duplicate_headings_h2_dup` | `"## Alpha\n### Beta\n## Alpha\n"` -- H2 duplicate, globally caught. Returns a `str`. `is False` assertion -- **WAIT**: `str is False` evaluates to `False` (not identical). The assertion `_no_duplicate_headings(content) is False` would fail because the return is now a `str`, not `False`. |

**Correction**: The existing `is False` assertions DO break with the `bool | str` return. Tests asserting `is False` must change to `assert not ... or ... is not True` or `assert _no_duplicate_headings(content) != True`.

**Resolution**: Update the three existing assertions to use truthiness checks:

```python
# Before:
assert _no_duplicate_headings(content) is False

# After:
assert _no_duplicate_headings(content) is not True
```

This works for both `bool` (`False is not True == True`) and `str` (`"..." is not True == True`). The `is True` assertions for passing cases remain correct since the function returns the literal `True`.

### 3b. Existing tests to update

| File | Test | Change |
|------|------|--------|
| `test_gates_data.py` | `test_no_duplicate_headings_h2_dup` | `is False` -> `is not True` |
| `test_gates_data.py` | `test_no_duplicate_headings_h3_dup` | `is False` -> `is not True` |
| `test_validate_defects.py` | `test_duplicate_h2_headings_detected` | `is False` -> `is not True` |
| `test_validate_defects.py` | `test_duplicate_h3_headings_detected` | `is False` -> `is not True` |

### 3c. New tests to add in `tests/roadmap/test_gates_data.py`

```python
class TestNoDuplicateHeadingsScoped:
    """H3 duplicate detection is scoped to parent H2 section."""

    def test_h3_same_name_different_h2_parents_passes(self):
        """The core false-positive fix: ### Tasks under different ## Phase sections."""
        content = (
            "## Phase 1\n### Tasks\n### Exit Criteria\n"
            "## Phase 2\n### Tasks\n### Exit Criteria\n"
            "## Phase 3\n### Tasks\n### Exit Criteria\n"
        )
        assert _no_duplicate_headings(content) is True

    def test_h3_same_name_same_h2_parent_fails(self):
        """Duplicate H3 within the same H2 section is still caught."""
        content = "## Phase 1\n### Tasks\nsome text\n### Tasks\n"
        result = _no_duplicate_headings(content)
        assert result is not True
        assert "Tasks" in result  # diagnostic contains the heading text

    def test_h2_global_duplicate_still_fails(self):
        """H2 duplicates are always caught regardless of position."""
        content = "## Phase 1\n### Tasks\n## Phase 2\n### Tasks\n## Phase 1\n"
        result = _no_duplicate_headings(content)
        assert result is not True
        assert "Phase 1" in result

    def test_h3_before_any_h2_duplicate_fails(self):
        """H3s before any H2 share a preamble scope -- duplicates are caught."""
        content = "### Intro\ntext\n### Intro\n"
        assert _no_duplicate_headings(content) is not True

    def test_h3_preamble_then_same_under_h2_passes(self):
        """H3 in top-level scope vs under an H2 are different scopes."""
        content = "### Tasks\n## Phase 1\n### Tasks\n"
        assert _no_duplicate_headings(content) is True

    def test_case_insensitive_h3_within_section_fails(self):
        """Duplicate detection is case-insensitive within a section."""
        content = "## Phase 1\n### Tasks\n### tasks\n"
        assert _no_duplicate_headings(content) is not True

    def test_empty_content_passes(self):
        assert _no_duplicate_headings("") is True

    def test_no_headings_passes(self):
        assert _no_duplicate_headings("Just text\nwith no headings\n") is True

    def test_failure_contains_line_number(self):
        """Diagnostic string includes the line number of the offending duplicate."""
        content = "## Phase 1\n### Tasks\n### Tasks\n"
        result = _no_duplicate_headings(content)
        assert result is not True
        assert "line 3" in result.lower()

    def test_real_roadmap_structure_passes(self):
        """Mirrors the actual failing roadmap structure that triggered this bug."""
        content = (
            "## Phase 1: Preparation\n### Tasks\n### Exit Criteria\n"
            "## Phase 2: Extraction\n### Tasks\n### Integration Points\n"
            "### Risk Burn-Down\n### Exit Criteria\n"
            "## Phase 3: Restructuring\n### Tasks\n### Integration Points\n"
            "### Risk Burn-Down\n### Exit Criteria\n"
            "## Phase 4: Verification\n### Tasks\n### Evidence Artifacts\n"
            "### Risk Burn-Down\n### Exit Criteria\n"
            "## Risk Assessment\n## Resource Requirements\n"
            "### Prerequisites\n### Staffing\n### External Dependencies\n"
        )
        assert _no_duplicate_headings(content) is True
```

### 3d. Regression test against real artifact (optional)

```python
def test_prd_refactor_roadmap_passes_duplicate_gate():
    """Regression: the actual roadmap that exposed this bug should pass."""
    roadmap = Path(".dev/releases/backlog/prd-skill-refactor/roadmap.md")
    if not roadmap.exists():
        pytest.skip("roadmap file not present")
    content = roadmap.read_text()
    assert _no_duplicate_headings(content) is True
```

---

## 4. Rejected Alternatives

| Approach | Source | Why rejected |
|----------|--------|-------------|
| Exemption list (`_STRUCTURAL_HEADINGS` set) | Brainstorm #2 | Maintenance burden; masks real same-section duplicates; philosophically wrong |
| Regex pattern exemption | Brainstorm #4 | Same problems as exemption list with added regex complexity |
| Configurable `heading_scope` on `SemanticCheck` | Brainstorm #5 | Over-engineered; only one check would use it |
| Split into two checks (`_no_duplicate_h2` + `_no_duplicate_h3_within_section`) | Brainstorm #6 | Clean design but changes gate definition (3 checks to 4), ripples into count assertions; single function achieves same correctness |
| Content-hash deduplication | Brainstorm #7 | Functionally identical to section-scoped with extra complexity |
| `CheckResult` dataclass | Design #3 | Heavier than needed; `is True`/`is False` assertions break; adds a new type for one check's benefit |
| `CheckResult` with `__bool__` | Design #3 | Subtle API trap -- `bool(result)` works but `result is False` does not; invites assertion bugs |
| Module-global `_duplicate_heading_detail` | Improve #3d | Thread-unsafe; implicit coupling; ugly pattern (proposal itself discourages it) |
| `last_detail` field on `SemanticCheck` | Improve #3b | Requires evaluator to reset before each call and read after; couples the model to a single check's needs |
| Defer diagnostics entirely | Improve #6 | The `bool \| str` approach is so low-cost that deferring gains nothing |

---

## 5. Edge Cases

| Case | Behavior |
|------|----------|
| H3 before any H2 | Scoped to `None` key (preamble). Duplicates within preamble caught. |
| Mixed case (`### Tasks` vs `### tasks`) | Caught -- `.lower()` normalization preserved. |
| Empty heading text (`### `) | Normalized to `""`. Two empty H3 under same parent caught. |
| H4+ headings | Ignored -- out of scope for this check. |
| No headings at all | Returns `True`. |
| Single H2 with unique H3s | Returns `True`. |

---

## 6. Implementation Checklist

1. Edit `src/superclaude/cli/roadmap/gates.py:92-107` -- replace `_no_duplicate_headings` with section-scoped version returning `bool | str`
2. Edit `MERGE_GATE` registration's `failure_message` to reflect scoping
3. Edit `src/superclaude/cli/pipeline/gates.py:66-72` -- update evaluator to use `result is not True` pattern
4. Edit `src/superclaude/cli/pipeline/models.py:63` -- update `check_fn` type hint to `Callable[[str], bool | str]`
5. Update 4 existing test assertions from `is False` to `is not True`
6. Add `TestNoDuplicateHeadingsScoped` class with 10 new tests
7. Run `uv run pytest tests/roadmap/test_gates_data.py tests/roadmap/test_validate_defects.py -v`
8. Run `uv run pytest` (full suite) -- verify no regressions
9. Manually verify: load `.dev/releases/backlog/prd-skill-refactor/roadmap.md` and confirm `_no_duplicate_headings` returns `True`

---

## 7. Estimated Diff

- `gates.py` (roadmap): ~25 lines changed
- `gates.py` (pipeline): ~6 lines changed
- `models.py`: 1 line changed
- `test_gates_data.py`: ~80 lines added, 2 lines updated
- `test_validate_defects.py`: 2 lines updated

**Total**: ~115 lines touched across 5 files. No new files. No new types.
