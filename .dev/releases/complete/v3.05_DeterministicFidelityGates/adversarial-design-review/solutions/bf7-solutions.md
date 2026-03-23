# BF-7 Solutions: NFR-3 Prompt Size Has No Enforcement Mechanism

## Problem Statement

`build_semantic_prompt()` (Architecture Sec 4.3) claims to enforce NFR-3 ("No single prompt exceeds 30KB") but specifies no truncation, splitting, or error-handling mechanism. The architecture tracks `byte_size` per `SpecSection` (Sec 4.1) and assigns sections per dimension via `DIMENSION_SECTIONS` (Sec 4.1), but never describes what happens when the assembled prompt exceeds 30,720 bytes.

**Key context**:
- NFR-3: "No single prompt exceeds 30KB" with measurement "Measured before LLM call"
- FR-5: "Prompt size per checker call is bounded (configurable, default ~30KB)"
- Each `SpecSection` tracks `byte_size: int` via `len(content.encode('utf-8'))`
- A semantic prompt contains: spec sections + roadmap sections + structural findings context + prior findings summary (max 50 entries) + prompt template overhead
- Sections vary wildly in size -- some spec sections could be 10KB+ alone

---

## Solution A: Proportional Budget Allocation with Tail-Truncation

### Design

Total budget: 30,720 bytes (30KB). Allocate proportionally across prompt components:

| Component | Budget Share | Bytes |
|-----------|-------------|-------|
| Spec + roadmap sections | 60% | 18,432 |
| Structural findings context | 20% | 6,144 |
| Prior findings summary | 15% | 4,608 |
| Prompt template overhead | 5% | 1,536 |

**Algorithm**:

```python
MAX_PROMPT_BYTES = 30_720  # 30KB

BUDGET_SPEC_ROADMAP = 0.60
BUDGET_STRUCTURAL_CTX = 0.20
BUDGET_PRIOR_SUMMARY = 0.15
BUDGET_TEMPLATE_OVERHEAD = 0.05

def build_semantic_prompt(request: SemanticCheckRequest) -> str:
    budget = MAX_PROMPT_BYTES
    template_budget = int(budget * BUDGET_TEMPLATE_OVERHEAD)
    spec_roadmap_budget = int(budget * BUDGET_SPEC_ROADMAP)
    structural_budget = int(budget * BUDGET_STRUCTURAL_CTX)
    prior_budget = int(budget * BUDGET_PRIOR_SUMMARY)

    # 1. Render template skeleton (role instructions, output format)
    template = _render_template_skeleton(request.dimension)
    assert len(template.encode('utf-8')) <= template_budget

    # 2. Fit spec + roadmap sections within their budget
    spec_roadmap_text = _fit_sections(
        request.spec_sections + request.roadmap_sections,
        spec_roadmap_budget,
    )

    # 3. Fit structural findings within their budget
    structural_text = _fit_structural_findings(
        request.structural_findings,
        structural_budget,
    )

    # 4. Fit prior findings summary within its budget
    prior_text = _fit_prior_summary(
        request.prior_findings_summary,
        prior_budget,
    )

    # 5. Assemble and assert total
    prompt = template + spec_roadmap_text + structural_text + prior_text
    prompt_bytes = len(prompt.encode('utf-8'))
    assert prompt_bytes <= MAX_PROMPT_BYTES, (
        f"Prompt {prompt_bytes}B exceeds {MAX_PROMPT_BYTES}B budget"
    )
    return prompt

def _fit_sections(sections: list[SpecSection], budget: int) -> str:
    """Include sections in order, tail-truncating if budget exceeded."""
    result_parts = []
    remaining = budget
    for section in sections:
        section_bytes = section.byte_size
        if section_bytes <= remaining:
            result_parts.append(section.content)
            remaining -= section_bytes
        else:
            # Tail-truncate this section
            truncated = _truncate_to_bytes(section.content, remaining)
            omitted = section_bytes - remaining
            result_parts.append(truncated)
            result_parts.append(f"\n[TRUNCATED: {omitted} bytes omitted from '{section.heading}']\n")
            remaining = 0
            break
    return "\n".join(result_parts)

def _truncate_to_bytes(text: str, max_bytes: int) -> str:
    """Truncate text to fit within max_bytes (UTF-8), on a line boundary."""
    encoded = text.encode('utf-8')
    if len(encoded) <= max_bytes:
        return text
    truncated = encoded[:max_bytes].decode('utf-8', errors='ignore')
    # Snap to last complete line
    last_newline = truncated.rfind('\n')
    if last_newline > 0:
        truncated = truncated[:last_newline]
    return truncated
```

### Analysis

**NFR-3 compliance guarantee**: YES. The `assert` at the end is a hard guarantee. Every component is individually capped, and the total is verified before return.

**Finding quality impact**: NEGATIVE. Tail-truncation loses information from the end of sections. If critical requirements appear late in a section, they will be silently dropped. The `[TRUNCATED]` marker signals omission but doesn't recover the lost content.

**Implementation complexity**: LOW. ~60 lines of straightforward byte-counting logic. No additional LLM calls. No state management.

**Token cost**: NONE. Single prompt per dimension, same as current design. No extra LLM calls.

**Edge case -- single section > 30KB**: The section is tail-truncated to fit its 60% allocation (18,432 bytes). Approximately 40% of that section is lost. The `[TRUNCATED]` marker indicates the loss. No other sections will fit. This is a significant quality degradation for very large sections.

---

## Solution B: Section Splitting with Priority Ranking

### Design

If total content exceeds 30KB, distribute across multiple sub-prompts. Each sub-prompt gets the highest-priority sections first. Findings from all sub-prompts are merged. No content is ever truncated.

**Algorithm**:

```python
MAX_PROMPT_BYTES = 30_720

def build_semantic_prompts(request: SemanticCheckRequest) -> list[str]:
    """Build one or more prompts, each <= 30KB. Never truncates."""

    # 1. Score and rank all sections by dimension relevance
    scored_sections = _rank_sections(
        request.spec_sections + request.roadmap_sections,
        request.dimension,
    )

    # 2. Calculate fixed-cost components
    template = _render_template_skeleton(request.dimension)
    template_bytes = len(template.encode('utf-8'))

    structural_text = _render_structural_findings(request.structural_findings)
    structural_bytes = len(structural_text.encode('utf-8'))

    prior_text = request.prior_findings_summary
    prior_bytes = len(prior_text.encode('utf-8'))

    fixed_cost = template_bytes + structural_bytes + prior_bytes

    # 3. Pack sections into prompts using first-fit-decreasing bin packing
    prompts = []
    current_sections = []
    current_size = fixed_cost

    for score, section in scored_sections:
        section_bytes = section.byte_size
        if current_size + section_bytes <= MAX_PROMPT_BYTES:
            current_sections.append(section)
            current_size += section_bytes
        else:
            # Emit current prompt if it has content
            if current_sections:
                prompts.append(_assemble_prompt(
                    template, current_sections, structural_text,
                    prior_text, len(prompts) + 1,
                ))
            # Start new prompt with this section
            if fixed_cost + section_bytes <= MAX_PROMPT_BYTES:
                current_sections = [section]
                current_size = fixed_cost + section_bytes
            else:
                # Single section > available space: must sub-split
                sub_chunks = _split_section(section, MAX_PROMPT_BYTES - fixed_cost)
                for chunk in sub_chunks:
                    prompts.append(_assemble_prompt(
                        template, [chunk], structural_text,
                        prior_text, len(prompts) + 1,
                    ))
                current_sections = []
                current_size = fixed_cost

    if current_sections:
        prompts.append(_assemble_prompt(
            template, current_sections, structural_text,
            prior_text, len(prompts) + 1,
        ))

    return prompts

def _rank_sections(
    sections: list[SpecSection],
    dimension: str,
) -> list[tuple[float, SpecSection]]:
    """Rank sections by relevance to the dimension.

    Primary sections (from DIMENSION_SECTIONS) get score 1.0.
    Supplementary sections (from cross_references) get score 0.7.
    Other sections get score 0.3.
    Returns sorted descending by score.
    """

def _split_section(
    section: SpecSection,
    max_bytes: int,
) -> list[SpecSection]:
    """Split an oversized section into sub-sections on heading/paragraph boundaries."""

def run_semantic_layer(...) -> list[Finding]:
    """Modified: iterate over all sub-prompts, merge findings by stable_id."""
    for request in dimension_requests:
        prompts = build_semantic_prompts(request)
        for prompt in prompts:
            assert len(prompt.encode('utf-8')) <= MAX_PROMPT_BYTES
            findings.extend(_call_llm(prompt))
    return _deduplicate_findings(findings)
```

### Analysis

**NFR-3 compliance guarantee**: YES. Each sub-prompt is individually capped at 30KB. The `assert` before each LLM call verifies compliance. The bin-packing algorithm guarantees no prompt exceeds the limit.

**Finding quality impact**: POSITIVE. No information is lost. Every section is included in at least one prompt. Priority ranking ensures the most relevant sections appear in the first prompt (which the LLM sees with freshest attention). Findings across sub-prompts are merged.

**Implementation complexity**: HIGH. ~150 lines. Requires: bin-packing algorithm, section ranking logic, sub-section splitting for oversized sections, finding deduplication across multiple prompts, modification of `run_semantic_layer` to iterate over multiple prompts per dimension.

**Token cost**: VARIABLE, potentially HIGH. If content is 90KB, that's 3 LLM calls per dimension instead of 1. With 5 dimensions, worst case could be 15 calls instead of 5. At ~$0.01-0.05 per call, this could 3x the semantic layer cost.

**Edge case -- single section > 30KB**: The section is split into sub-sections on heading or paragraph boundaries using `_split_section()`. Each chunk gets its own prompt with the fixed-cost components (template, structural findings, prior summary). No content is lost, but the LLM sees the section in pieces, which may impair cross-paragraph reasoning within that section.

---

## Comparative Scoring

| Criterion | Weight | Solution A | Solution B |
|-----------|--------|-----------|-----------|
| NFR-3 compliance guarantee | 40% | 10/10 -- hard assert, single prompt | 10/10 -- hard assert per sub-prompt |
| Finding quality preservation | 30% | 5/10 -- truncation loses tail content | 9/10 -- no loss, but fragmented context |
| Implementation simplicity | 30% | 9/10 -- ~60 LOC, no new API surface | 4/10 -- ~150 LOC, new multi-prompt flow |

**Weighted scores**:
- Solution A: (10 * 0.4) + (5 * 0.3) + (9 * 0.3) = 4.0 + 1.5 + 2.7 = **8.2**
- Solution B: (10 * 0.4) + (9 * 0.3) + (4 * 0.3) = 4.0 + 2.7 + 1.2 = **7.9**

---

## Winner: Solution A (Proportional Budget with Tail-Truncation)

Solution A wins by a narrow margin (8.2 vs 7.9). The decisive factor is implementation simplicity: Solution A requires no changes to the `run_semantic_layer` API, no finding deduplication logic, and no multi-prompt orchestration. Both solutions guarantee NFR-3 compliance equally.

**Mitigation for Solution A's quality weakness**: The `[TRUNCATED]` marker makes information loss visible in the output. If truncation is observed in practice, the budget ratios can be tuned (e.g., increase spec_roadmap share to 70%) or the 30KB limit can be made configurable per FR-5.

**Why not Solution B despite better quality?** The token cost multiplier and implementation complexity introduce new failure modes (finding deduplication bugs, bin-packing edge cases) that offset the quality advantage. The architecture already limits semantic checking to ~30% of findings; the structural checkers handle the majority deterministically and are unaffected by prompt size limits.
