# ISS-017: TRUNCATION_MARKER Missing Heading Name

> **Severity**: MEDIUM (spec omits something that exists and matters)
> **Source**: Compatibility Report, Section 3
> **Affected Spec**: FR-4.2 (Prompt Budget Enforcement), FR-5 (Sectional/Chunked Comparison)
> **Issue Registry**: `issues-classified.md`

## Problem Statement

The spec (FR-4.2) requires truncation markers to include the heading name:

> Sections: tail-truncated on line boundary with `[TRUNCATED: N bytes omitted from '<heading>']` marker

However, the current implementation at `semantic_layer.py:28` defines:

```python
TRUNCATION_MARKER = "[TRUNCATED: {} bytes omitted]"
```

The `_truncate_to_budget()` function (lines 145-168) accepts only `(content, budget_bytes)` -- no heading parameter. The heading name is lost at truncation time, making it impossible for downstream consumers (LLM semantic layer, human auditors) to identify which section was truncated.

## Overlap with Existing Resolutions

ISS-002 (CRITICAL) proposals mention this fix as a side-effect ("same minor change") but do not provide standalone spec text or code changes for ISS-017. No HIGH-severity proposals address this. This proposal provides the focused resolution.

---

## Proposal A: Minimal Code Fix -- Update Constant and Function Signature

**Approach**: Fix the implementation to match the existing spec text. No spec change needed -- the spec already says what it should say. This is purely a code-side fix.

### Code Changes

**Before** (`semantic_layer.py:28`):
```python
TRUNCATION_MARKER = "[TRUNCATED: {} bytes omitted]"
```

**After**:
```python
TRUNCATION_MARKER = "[TRUNCATED: {} bytes omitted from '{}']"
```

**Before** (`semantic_layer.py:145-168`):
```python
def _truncate_to_budget(content: str, budget_bytes: int) -> str:
    """Tail-truncate content to fit within byte budget on line boundaries."""
    encoded = content.encode("utf-8")
    if len(encoded) <= budget_bytes:
        return content

    omitted = len(encoded) - budget_bytes
    marker = TRUNCATION_MARKER.format(omitted)
    ...
    return truncated + "\n" + marker
```

**After**:
```python
def _truncate_to_budget(content: str, budget_bytes: int, heading: str = "") -> str:
    """Tail-truncate content to fit within byte budget on line boundaries."""
    encoded = content.encode("utf-8")
    if len(encoded) <= budget_bytes:
        return content

    omitted = len(encoded) - budget_bytes
    marker = TRUNCATION_MARKER.format(omitted, heading) if heading else f"[TRUNCATED: {omitted} bytes omitted]"
    ...
    return truncated + "\n" + marker
```

**Callers updated** (`build_semantic_prompt()` lines 206, 213, 216):
```python
combined = _truncate_to_budget(combined, spec_roadmap_budget, heading="spec+roadmap")
structural_text = _truncate_to_budget(structural_text, structural_budget, heading="structural findings")
prior_text = _truncate_to_budget(request.prior_findings_summary, prior_budget, heading="prior findings")
```

### Spec Text Change

None. FR-4.2 already specifies the correct marker format. The spec is correct; only the implementation is wrong.

### Acceptance Criteria Impact

FR-4.2 AC-3 (`Oversized sections are tail-truncated on line boundaries with visible markers`) is already satisfied in form but not in full spec compliance. This fix closes the gap.

### Risk: LOW
- Additive parameter with default value; backward-compatible
- No spec text change needed
- ISS-002 proposals already flag this as a minor side-fix

---

## Proposal B: Spec Hardening -- Add Explicit Acceptance Criterion for Heading Name

**Approach**: The current spec mentions the heading format in prose but does not have a dedicated acceptance criterion. Add one to FR-4.2 to make the requirement testable and prevent future regression.

### Spec Text Change

**Before** (FR-4.2 Acceptance Criteria):
```markdown
- [ ] `MAX_PROMPT_BYTES = 30_720` as configurable module constant
- [ ] Budget ratios are module-level constants, overridable via config
- [ ] Oversized sections are tail-truncated on line boundaries with visible markers
- [ ] `assert` before LLM call confirms prompt <= budget
- [ ] Template exceeding 5% allocation raises `ValueError`
- [ ] Empty sections produce a valid prompt without errors
```

**After**:
```markdown
- [ ] `MAX_PROMPT_BYTES = 30_720` as configurable module constant
- [ ] Budget ratios are module-level constants, overridable via config
- [ ] Oversized sections are tail-truncated on line boundaries with visible markers
- [ ] Truncation markers include section heading: `[TRUNCATED: N bytes omitted from '<heading>']`
- [ ] `assert` before LLM call confirms prompt <= budget
- [ ] Template exceeding 5% allocation raises `ValueError`
- [ ] Empty sections produce a valid prompt without errors
```

### Code Changes

Same as Proposal A.

### Risk: LOW
- One new acceptance criterion line in FR-4.2
- Makes the requirement independently testable
- Aligns spec prose with spec acceptance criteria

---

## Proposal C: Propagate Heading Through Section Splitter (FR-5 Alignment)

**Approach**: The truncation marker issue is a symptom of a deeper gap: `_truncate_to_budget()` operates on raw strings with no section awareness. When FR-5 (sectional/chunked comparison) is implemented, each chunk will have a heading. This proposal aligns the truncation fix with FR-5 by designing the heading propagation from section splitter through to truncation.

### Spec Text Changes

**Add to FR-5 Acceptance Criteria** (after existing items):
```markdown
- [ ] Each section chunk carries its heading name through to truncation markers
- [ ] `_truncate_to_budget()` receives the originating heading for inclusion in the `[TRUNCATED]` marker
```

**Add to FR-4.2 Acceptance Criteria** (same as Proposal B):
```markdown
- [ ] Truncation markers include section heading: `[TRUNCATED: N bytes omitted from '<heading>']`
```

### Code Changes

Same as Proposal A, plus: when FR-5's section splitter is built (ISS-018), it must pass the heading name through to `_truncate_to_budget()`. The `heading=""` default in Proposal A's signature ensures backward compatibility until FR-5 is implemented.

### Risk: LOW-MEDIUM
- Touches two spec sections (FR-4.2 and FR-5)
- Creates a soft dependency between ISS-017 and ISS-018 (section splitter)
- More future-proof but slightly wider scope

---

## Recommendation

**Proposal B** is the recommended approach.

- Proposal A fixes the code but leaves the spec with an implicit requirement buried in prose -- easy to regress.
- Proposal B adds one explicit acceptance criterion, making the requirement testable and traceable (G6: Auditability).
- Proposal C is architecturally sound but couples ISS-017 to ISS-018, which is not yet scoped. The FR-5 alignment can be added when ISS-018 is resolved.

The code fix (Proposal A's changes) should be applied regardless of which spec proposal is chosen.
