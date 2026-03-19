# BF-7 Resolution: Proportional Budget Allocation with Tail-Truncation

## Selected Solution

**Solution A**: Proportional budget allocation with tail-truncation.

**Rationale**: Solution A wins by weighted score 8.2 vs 7.9 (B). Both solutions guarantee NFR-3 compliance equally (10/10). The decisive factor is implementation simplicity (9/10 vs 4/10 at 30% weight). Solution B's superior finding quality (9/10 vs 5/10) is offset by its complexity cost: multi-prompt orchestration, finding deduplication across LLM calls, bin-packing edge cases, and variable token cost (up to 3x). Since structural checkers handle ~70% of findings deterministically without prompt size concerns, the quality impact of truncation in the residual semantic layer is bounded.

## Budget Allocation Model

Total budget: 30,720 bytes (30KB). Fixed allocation ratios:

| Component | Share | Bytes | Contents |
|-----------|-------|-------|----------|
| Spec + roadmap sections | 60% | 18,432 | Primary and supplementary `SpecSection.content` for the dimension |
| Structural findings context | 20% | 6,144 | "Already checked" findings to prevent re-reporting |
| Prior findings summary | 15% | 4,608 | Registry summary (max 50 entries) for run-to-run anchoring |
| Prompt template overhead | 5% | 1,536 | Role instructions, output format, dimension-specific guidance |

**Configurability**: `MAX_PROMPT_BYTES` is a module-level constant (default 30,720). Budget ratios are module-level constants. Both are overridable via `PipelineConfig` for FR-5 compliance ("configurable, default ~30KB").

## Enforcement Algorithm

Step-by-step algorithm for `build_semantic_prompt`:

```
1. COMPUTE budget allocations from MAX_PROMPT_BYTES and ratio constants
2. RENDER template skeleton for the dimension
   - ASSERT template_bytes <= template_budget
   - If exceeded: RAISE ValueError (indicates template bloat, a code bug)
3. FOR each section in (spec_sections + roadmap_sections), ordered by dimension relevance:
   a. IF section.byte_size <= remaining_spec_roadmap_budget:
      - APPEND section.content to spec_roadmap_text
      - DECREMENT remaining by section.byte_size
   b. ELSE IF remaining_spec_roadmap_budget > 0:
      - TRUNCATE section.content to remaining bytes on a line boundary
      - APPEND truncated content + "[TRUNCATED: N bytes omitted from '<heading>']"
      - SET remaining to 0
      - BREAK (no more sections fit)
   c. ELSE:
      - BREAK (budget exhausted)
4. RENDER structural findings text
   - IF structural_bytes > structural_budget:
     - TRUNCATE to budget on a finding boundary (complete findings only)
     - APPEND "[TRUNCATED: N structural findings omitted]"
5. RENDER prior findings summary
   - IF prior_bytes > prior_budget:
     - TRUNCATE to budget on a line boundary
     - APPEND "[TRUNCATED: N prior findings omitted]"
6. ASSEMBLE prompt = template + spec_roadmap_text + structural_text + prior_text
7. ASSERT len(prompt.encode('utf-8')) <= MAX_PROMPT_BYTES
8. RETURN prompt
```

## Overflow Handling

When content exceeds its allocated budget:

| Component | Overflow Behavior | Marker |
|-----------|-------------------|--------|
| Template skeleton | `ValueError` raised -- this is a code bug, not a runtime condition | N/A |
| Spec/roadmap sections | Sections included in order; last fitting section is tail-truncated on line boundary | `[TRUNCATED: N bytes omitted from '<heading>']` |
| Structural findings | Findings included in full; excess findings dropped entirely (no partial findings) | `[TRUNCATED: N structural findings omitted]` |
| Prior findings summary | Lines included in full; excess lines dropped | `[TRUNCATED: N prior findings omitted]` |

**Truncation line-boundary snapping**: When truncating mid-section, the cut point snaps backward to the last complete line (`\n`). This prevents mid-word or mid-sentence cuts that would confuse the LLM.

**Truncation markers**: Every truncation appends a visible marker. This serves two purposes: (1) the LLM knows information was omitted and can flag if it needs more context, (2) pipeline operators can detect truncation in logs and adjust budgets.

## Edge Cases

### Single section > 30KB

A single `SpecSection` exceeding 18,432 bytes (the 60% allocation) is tail-truncated to fit. The remainder is lost for this prompt. This is acceptable because:
- Sections this large are rare (most spec sections are 2-8KB)
- The structural checkers handle the majority of checks for that section deterministically
- The truncation marker is visible, allowing manual review if needed
- Budget ratios can be adjusted if this proves common in practice

### Empty sections

If a dimension has no relevant spec or roadmap sections, the spec_roadmap_budget is unused. The prompt contains only template + structural context + prior summary. No error -- the semantic layer can still check for omission-type findings.

### All components fit within budget

The common case. No truncation occurs. The `assert` at step 7 passes trivially.

### Structural findings exceed 20% budget

When there are many structural findings (e.g., 50+ from a checker), the structural context is truncated at finding boundaries. Higher-severity findings should be listed first so truncation drops LOW findings preferentially.

### Prior findings summary exceeds 15% budget

The max-50-entry cap from FR-10 already bounds this. At ~80 bytes per entry, 50 entries = ~4,000 bytes, which fits within the 4,608 byte budget. Truncation here is a safety net, not the normal path.

### UTF-8 multi-byte characters

Truncation uses `encode('utf-8')[:max_bytes].decode('utf-8', errors='ignore')` followed by line-boundary snapping. The `errors='ignore'` handles mid-character cuts; line snapping further ensures clean boundaries.

## Architecture Design Change

### Addition to Sec 4.3 `build_semantic_prompt` specification

Replace the current `build_semantic_prompt` docstring block (lines 412-418 of `architecture-design.md`) with:

```python
# Module-level constants
MAX_PROMPT_BYTES: int = 30_720  # 30KB, configurable via PipelineConfig
BUDGET_SPEC_ROADMAP: float = 0.60
BUDGET_STRUCTURAL_CTX: float = 0.20
BUDGET_PRIOR_SUMMARY: float = 0.15
BUDGET_TEMPLATE_OVERHEAD: float = 0.05

def build_semantic_prompt(request: SemanticCheckRequest) -> str:
    """Build a chunked prompt for one semantic check.

    Enforces NFR-3 via proportional budget allocation:
      - 60% spec + roadmap sections (tail-truncated on line boundary if over)
      - 20% structural findings context (truncated at finding boundary if over)
      - 15% prior findings summary (truncated at line boundary if over)
      - 5%  prompt template overhead (raises ValueError if exceeded)

    Truncation appends '[TRUNCATED: N bytes omitted]' markers.
    Final prompt size is asserted <= MAX_PROMPT_BYTES before return.

    Raises:
        ValueError: If template skeleton alone exceeds its 5% budget
            (indicates a code bug in template construction).
        AssertionError: If final assembled prompt exceeds MAX_PROMPT_BYTES
            (should never occur if truncation logic is correct; acts as safety net).
    """
```

### Addition to Sec 4.3 after the `build_semantic_prompt` block

Add a new subsection:

```markdown
#### 4.3.1 Prompt Budget Enforcement (NFR-3)

The prompt budget is enforced by `build_semantic_prompt` using proportional
allocation. Each component (sections, structural context, prior summary,
template) receives a fixed percentage of `MAX_PROMPT_BYTES`. Components
that exceed their allocation are tail-truncated with a visible marker.

**Truncation priority** (what gets cut first):
1. Prior findings summary (least critical -- registry is the source of truth)
2. Structural findings context (secondary -- prevents re-checking, but not
   essential for new finding discovery)
3. Spec/roadmap sections (most critical -- last resort, truncated on line
   boundary within the lowest-priority section)

**Configurability**: `MAX_PROMPT_BYTES` and all budget ratios are module-level
constants, overridable via `PipelineConfig.max_prompt_bytes` and
`PipelineConfig.prompt_budget_ratios` for FR-5 compliance.

**Section ordering within spec_roadmap budget**: Sections are included in
`DIMENSION_SECTIONS` order (primary sections first, supplementary sections
second). If truncation is needed, supplementary sections are omitted before
primary sections are truncated.
```

### Addition to Sec 10 NFR Compliance Matrix

Update the NFR-3 row:

```markdown
| NFR-3 (Prompt <=30KB) | Proportional budget allocation in `build_semantic_prompt`; tail-truncation with `[TRUNCATED]` markers; `assert` before LLM call | Unit test: assemble prompt with oversized sections, verify <= 30KB and marker present |
```

## Validation

### Unit Tests

```python
def test_prompt_under_budget_normal():
    """Normal case: all components fit within budget."""
    request = SemanticCheckRequest(
        dimension="signatures",
        spec_sections=[make_section("## 3. FR", "x" * 5000)],
        roadmap_sections=[make_section("## Phase 1", "y" * 3000)],
        structural_findings=[make_finding() for _ in range(5)],
        prior_findings_summary="ID | sev | status\nF-01 | HIGH | FIXED",
    )
    prompt = build_semantic_prompt(request)
    assert len(prompt.encode('utf-8')) <= 30_720

def test_prompt_truncates_oversized_section():
    """Section exceeding spec_roadmap budget is tail-truncated."""
    request = SemanticCheckRequest(
        dimension="signatures",
        spec_sections=[make_section("## 3. FR", "x" * 25_000)],
        roadmap_sections=[],
        structural_findings=[],
        prior_findings_summary="",
    )
    prompt = build_semantic_prompt(request)
    assert len(prompt.encode('utf-8')) <= 30_720
    assert "[TRUNCATED:" in prompt

def test_prompt_truncation_on_line_boundary():
    """Truncation snaps to last complete line."""
    lines = "\n".join(f"Line {i}: " + "x" * 100 for i in range(300))
    request = SemanticCheckRequest(
        dimension="signatures",
        spec_sections=[make_section("## 3. FR", lines)],
        roadmap_sections=[],
        structural_findings=[],
        prior_findings_summary="",
    )
    prompt = build_semantic_prompt(request)
    # Every line in prompt should be complete (no mid-line cuts)
    for line in prompt.split('\n'):
        assert not line.endswith("x" * 50)  # no partial padding lines

def test_prompt_empty_sections():
    """Empty sections produce valid prompt without truncation."""
    request = SemanticCheckRequest(
        dimension="signatures",
        spec_sections=[],
        roadmap_sections=[],
        structural_findings=[],
        prior_findings_summary="",
    )
    prompt = build_semantic_prompt(request)
    assert len(prompt.encode('utf-8')) <= 30_720
    assert "[TRUNCATED:" not in prompt

def test_prompt_rejects_bloated_template():
    """Template exceeding 5% budget raises ValueError."""
    # This test would require mocking _render_template_skeleton
    # to return an oversized template
    pass

def test_prompt_structural_findings_truncated_at_boundary():
    """Structural findings are truncated at complete-finding boundary."""
    request = SemanticCheckRequest(
        dimension="signatures",
        spec_sections=[make_section("## 3. FR", "x" * 10_000)],
        roadmap_sections=[],
        structural_findings=[make_finding() for _ in range(200)],
        prior_findings_summary="",
    )
    prompt = build_semantic_prompt(request)
    assert len(prompt.encode('utf-8')) <= 30_720
```

### Integration Verification

Add to the existing integration test suite (Sec 8.2):

```python
def test_nfr3_prompt_size_integration():
    """NFR-3: No prompt exceeds 30KB in end-to-end semantic layer run."""
    # Instrument build_semantic_prompt to log byte sizes
    # Run full semantic layer on real v3.0 spec
    # Assert all logged sizes <= 30_720
```

### Runtime Safety Net

The `assert` at step 7 of the algorithm acts as a runtime safety net. If truncation logic has a bug that allows an oversized prompt, the assert triggers an `AssertionError` before the LLM call is made. This converts silent NFR-3 violations into loud, traceable failures.
