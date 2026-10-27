# D-0001: OQ-A/OQ-B/OQ-C Resolution — GateCriteria.aux_inputs Decision

**Task:** T01.01
**Date:** 2026-03-16
**Status:** RESOLVED

---

## Inspected Definition

**File:** `src/superclaude/cli/pipeline/models.py` (lines 66–73)

```python
@dataclass
class GateCriteria:
    """Defines what constitutes a passing output for a pipeline step."""

    required_frontmatter_fields: list[str]
    min_lines: int
    enforcement_tier: Literal["STRICT", "STANDARD", "LIGHT", "EXEMPT"] = "STANDARD"
    semantic_checks: list[SemanticCheck] | None = None
```

**Complete field list:**
- `required_frontmatter_fields: list[str]`
- `min_lines: int`
- `enforcement_tier: Literal["STRICT", "STANDARD", "LIGHT", "EXEMPT"]` (default: "STANDARD")
- `semantic_checks: list[SemanticCheck] | None` (default: None)

**`aux_inputs` field:** DOES NOT EXIST on `GateCriteria`.

---

## OQ-A Resolution

**Decision: Option B — Frontmatter Embedding**

`GateCriteria` does not have an `aux_inputs` field and there is no mechanism for passing auxiliary inputs through the gate criteria dataclass. FR-079 implementation must use **Option B: frontmatter embedding**, where any supplementary routing or context information is embedded directly in the step prompt or output frontmatter rather than passed as a separate gate criteria field.

**Rationale:** Adding `aux_inputs` to `GateCriteria` would require modifying `src/superclaude/cli/pipeline/models.py`, which is a generic pipeline layer component. Architecture constraint AC-1 prohibits modifications to generic pipeline layer files (`pipeline/executor.py` and `pipeline/models.py`). Therefore Option A is architecturally blocked and Option B is the only valid path.

---

## OQ-B Resolution (cascading from OQ-A)

FR-088 extended validation depends on OQ-A. Since Option B (frontmatter embedding) was chosen:
- Extended validation data must be read from step output frontmatter fields
- No new `GateCriteria` fields are required for extended validation
- Validation logic reads from existing `required_frontmatter_fields` mechanism or from file content post-gate

**Impact:** FR-088 extended validation deferral remains valid. The gate enforcement layer does not need modification.

---

## OQ-C Resolution — PRE_APPROVED ID Extraction

**Search result:** `PRE_APPROVED` does not appear anywhere in `src/superclaude/cli/`. There is no existing extraction mechanism.

**Decision:** PRE_APPROVED ID extraction for v2.26 will use **frontmatter field parsing** — the step output YAML frontmatter will contain a `pre_approved_ids` field (or equivalent) that is parsed by the sprint executor layer, not the pipeline layer. The extraction implementation belongs in the sprint-specific layer.

**Method:** String-parse the YAML frontmatter of the relevant step output file. No new generic pipeline primitives required.

---

## Summary Table

| OQ | Decision | Option Chosen | Constraint |
|----|----------|---------------|------------|
| OQ-A | No `aux_inputs` field on GateCriteria | Option B (frontmatter embedding) | AC-1: no pipeline/models.py modification |
| OQ-B | FR-088 reads from frontmatter, not gate criteria | Frontmatter-based | Follows from OQ-A |
| OQ-C | PRE_APPROVED extraction via frontmatter YAML parsing | Frontmatter field parsing | Sprint-layer only, no pipeline modification |
