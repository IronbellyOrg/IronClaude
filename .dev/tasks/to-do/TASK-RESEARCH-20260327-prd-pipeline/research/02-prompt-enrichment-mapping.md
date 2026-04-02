# Research: Prompt Enrichment Mapping

**Investigation type:** Code Tracer + Doc Analyst
**Scope:** src/superclaude/cli/roadmap/prompts.py
**Status:** Complete
**Date:** 2026-03-27

---

## Reference Pattern: TDD Supplementary Block

The established pattern for supplementary input enrichment comes from `build_tasklist_fidelity_prompt()` in `src/superclaude/cli/tasklist/prompts.py:17-125`. [CODE-VERIFIED]

**Signature pattern:**
```python
def build_tasklist_fidelity_prompt(
    roadmap_file: Path,
    tasklist_dir: Path,
    tdd_file: Path | None = None,  # <-- optional supplementary input
) -> str:
```

**Conditional block pattern (lines 110-123):**
```python
# TDD integration: append supplementary validation when TDD file is provided
if tdd_file is not None:
    base += (
        "\n\n## Supplementary TDD Validation (when TDD file is provided)\n\n"
        "A Technical Design Document (TDD) is included in the inputs alongside "
        "the roadmap and tasklist. Additionally check:\n"
        "1. Test cases from the TDD's Testing Strategy section (§15) should have "
        "corresponding validation or test tasks in the tasklist.\n"
        "2. Rollback procedures from the TDD's Migration & Rollout Plan section (§19) "
        "should have corresponding contingency or rollback tasks.\n"
        "3. Components listed in the TDD's Component Inventory (§10) should have "
        "corresponding implementation tasks.\n"
        "Flag missing coverage as MEDIUM severity deviations."
    )
```

**Key design characteristics:** [CODE-VERIFIED]
- Block appended AFTER the main `base` string but BEFORE `_OUTPUT_FORMAT_BLOCK`
- Uses `\n\n##` heading for the supplementary section
- References specific PRD/TDD section numbers (§N)
- Provides numbered check items (typically 3-5)
- Ends with severity classification guidance
- Block is concise (~6-10 lines of prompt text) — NOT a full prompt rewrite

---

## PRD Template Section Inventory

From `src/superclaude/examples/prd_template.md`, the PRD has 28 sections: [CODE-VERIFIED]

| # | Section | Pipeline-Relevant? | Primary Pipeline Consumer |
|---|---------|-------------------|--------------------------|
| 1 | Executive Summary | YES | extract, generate |
| 2 | Problem Statement | YES | extract, generate |
| 3 | Background & Strategic Fit | LOW | generate |
| 4 | Product Vision | YES | extract, generate |
| 5 | Business Context | YES | extract, generate, score |
| 6 | Jobs To Be Done (JTBD) | YES | extract, generate, test-strategy |
| 7 | User Personas | **HIGH** | extract, generate, test-strategy, spec-fidelity |
| 8 | Value Proposition Canvas | LOW | generate |
| 9 | Competitive Analysis | LOW | — |
| 10 | Assumptions & Constraints | YES | extract |
| 11 | Dependencies | YES | extract |
| 12 | Scope Definition | **HIGH** | extract, spec-fidelity |
| 13 | Open Questions | YES | extract |
| 14 | Technical Requirements | YES | extract (already captured as FRs) |
| 15 | Technology Stack | YES | extract (already captured as constraints) |
| 16 | User Experience Requirements | **HIGH** | generate, test-strategy, spec-fidelity |
| 17 | Legal & Compliance Requirements | **HIGH** | extract, spec-fidelity, test-strategy |
| 18 | Business Requirements | YES | extract, generate |
| 19 | Success Metrics & Measurement | **HIGH** | extract, spec-fidelity, test-strategy |
| 20 | Risk Analysis | YES | extract (already captured in risk inventory) |
| 21 | Implementation Plan (Epics/Stories) | YES | generate, spec-fidelity |
| 22 | Customer Journey Map | **HIGH** | generate, test-strategy |
| 23 | Error Handling & Edge Cases | YES | test-strategy |
| 24 | User Interaction & Design | YES | generate |
| 25 | API Contract Examples | YES | extract (overlaps with TDD) |
| 26 | Contributors & Collaboration | LOW | — |
| 27 | Related Resources | LOW | — |
| 28 | Maintenance & Ownership | LOW | — |

**Most pipeline-relevant PRD sections (the "why/who" content TDD drops):**
- §2 Problem Statement, §4 Product Vision, §5 Business Context
- §6 JTBD, §7 User Personas, §12 Scope Definition
- §16 UX Requirements, §17 Legal/Compliance, §18 Business Requirements
- §19 Success Metrics, §22 Customer Journey Map

---

## Prompt Builder 1: `build_extract_prompt`

**Current signature (line 82-85):** [CODE-VERIFIED]
```python
def build_extract_prompt(
    spec_file: Path,
    retrospective_content: str | None = None,
) -> str:
```

**PRD enrichment value:** HIGH (P1)

**Rationale:** The extraction step is the single chokepoint — content not surfaced here is lost to all downstream steps. [CODE-VERIFIED from research report §2.1] When a spec file is the primary input and a PRD is supplementary, the extractor should additionally surface business context, persona definitions, JTBD, and success metrics that the spec file alone may not contain.

**Proposed parameter change:**
```python
def build_extract_prompt(
    spec_file: Path,
    retrospective_content: str | None = None,
    prd_file: Path | None = None,  # NEW: optional PRD supplementary context
) -> str:
```

**Proposed supplementary block (insert after retrospective block, before `_OUTPUT_FORMAT_BLOCK`):**
```python
if prd_file is not None:
    base += (
        "\n\n## Supplementary PRD Context (when PRD file is provided)\n\n"
        "A Product Requirements Document (PRD) is included in the inputs alongside "
        "the specification. Use it as supplementary business context for extraction. "
        "Additionally extract:\n"
        "1. Business objectives and success metrics from the PRD's Success Metrics "
        "section (§19) — surface as additional Success Criteria.\n"
        "2. User personas from the PRD's User Personas section (§7) — note in the "
        "Architectural Constraints section as persona-driven design requirements.\n"
        "3. Scope boundaries from the PRD's Scope Definition section (§12) — use to "
        "validate that extracted requirements fall within stated scope.\n"
        "4. Legal and compliance requirements from the PRD's Legal & Compliance "
        "section (§17) — surface as Non-Functional Requirements if not already "
        "present in the spec.\n"
        "5. Jobs To Be Done from the PRD's JTBD section (§6) — note in Open "
        "Questions if any JTBD lack corresponding functional requirements.\n"
        "The PRD is advisory context for enrichment — do NOT treat PRD content "
        "as hard requirements unless they are also stated in the specification."
    )
```

**PRD sections referenced:** §6 JTBD, §7 User Personas, §12 Scope Definition, §17 Legal/Compliance, §19 Success Metrics

---

## Prompt Builder 2: `build_extract_prompt_tdd`

**Current signature (line 161-164):** [CODE-VERIFIED]
```python
def build_extract_prompt_tdd(
    spec_file: Path,
    retrospective_content: str | None = None,
) -> str:
```

**PRD enrichment value:** MEDIUM (P2)

**Rationale:** When both TDD and PRD are provided, the TDD extractor already captures deep technical content (data models, APIs, components, etc.). The PRD adds "why/who" context that the TDD inherently lacks. Value is lower than for `build_extract_prompt` because the TDD already contains more structured content, but PRD still provides business context, personas, and compliance requirements that TDD rarely captures.

**Proposed parameter change:**
```python
def build_extract_prompt_tdd(
    spec_file: Path,
    retrospective_content: str | None = None,
    prd_file: Path | None = None,  # NEW: optional PRD supplementary context
) -> str:
```

**Proposed supplementary block (insert after retrospective block, before `_OUTPUT_FORMAT_BLOCK`):**
```python
if prd_file is not None:
    base += (
        "\n\n## Supplementary PRD Context (when PRD file is provided)\n\n"
        "A Product Requirements Document (PRD) is included in the inputs alongside "
        "the TDD. The TDD captures technical design; the PRD provides business "
        "context. Additionally extract:\n"
        "1. Business success metrics from the PRD's Success Metrics section (§19) "
        "— surface as additional Success Criteria alongside TDD-derived criteria.\n"
        "2. User personas from the PRD's User Personas section (§7) — note as "
        "persona-driven design requirements in Architectural Constraints.\n"
        "3. Legal and compliance requirements from the PRD's Legal & Compliance "
        "section (§17) — surface as Non-Functional Requirements if not already "
        "present in the TDD.\n"
        "The PRD is advisory context for enrichment — do NOT treat PRD content "
        "as hard requirements unless also stated in the TDD."
    )
```

**PRD sections referenced:** §7 User Personas, §17 Legal/Compliance, §19 Success Metrics

---

## Prompt Builder 3: `build_generate_prompt`

**Current signature (line 288):** [CODE-VERIFIED]
```python
def build_generate_prompt(agent: AgentSpec, extraction_path: Path) -> str:
```

**PRD enrichment value:** HIGH (P1)

**Rationale:** The generate step produces the roadmap — this is where business context directly shapes prioritization, phasing, and risk assessment. PRD personas inform what gets built first (user-facing features vs. infrastructure), business context shapes ROI-based phasing, and JTBD drives milestone definitions. The generate step currently receives only extraction.md, so PRD enrichment adds value that isn't in the extraction output today.

**Proposed parameter change:**
```python
def build_generate_prompt(
    agent: AgentSpec,
    extraction_path: Path,
    prd_file: Path | None = None,  # NEW: optional PRD supplementary context
) -> str:
```

**Proposed supplementary block (insert before `_INTEGRATION_ENUMERATION_BLOCK` concatenation):**
```python
base = (
    # ... existing prompt text ...
)

if prd_file is not None:
    base += (
        "\n\n## Supplementary PRD Context (when PRD file is provided)\n\n"
        "A Product Requirements Document (PRD) is included in the inputs alongside "
        "the extraction. Use PRD content to inform roadmap prioritization and phasing:\n"
        "1. **Value-based phasing**: Use the PRD's Business Context (§5) and Success "
        "Metrics (§19) to prioritize phases that deliver measurable business value earliest.\n"
        "2. **Persona-driven sequencing**: Use the PRD's User Personas (§7) and Customer "
        "Journey Map (§22) to ensure the roadmap addresses highest-impact user needs first.\n"
        "3. **Compliance gates**: If the PRD's Legal & Compliance section (§17) defines "
        "regulatory requirements, ensure the roadmap includes compliance validation "
        "milestones at appropriate phases.\n"
        "4. **Scope guardrails**: Use the PRD's Scope Definition (§12) to flag any "
        "roadmap items that fall outside stated product scope.\n"
        "The PRD provides business 'why' context — do NOT let it override technical "
        "sequencing constraints from the extraction."
    )

return base + _INTEGRATION_ENUMERATION_BLOCK + _OUTPUT_FORMAT_BLOCK
```

**Note:** This requires refactoring the current return statement (line 295-335) from a single expression into `base = (...)` + conditional + return, matching the pattern used in `build_extract_prompt`. [CODE-VERIFIED: current implementation returns a single concatenated expression]

**PRD sections referenced:** §5 Business Context, §7 User Personas, §12 Scope Definition, §17 Legal/Compliance, §19 Success Metrics, §22 Customer Journey Map

---

## Prompt Builder 4: `build_diff_prompt`

**Current signature (line 338):** [CODE-VERIFIED]
```python
def build_diff_prompt(variant_a_path: Path, variant_b_path: Path) -> str:
```

**PRD enrichment value:** LOW (P3)

**Rationale:** The diff step compares two roadmap variants. PRD context could marginally improve the comparison by adding a "business alignment" dimension, but the variants are already shaped by any PRD context injected at the generate step. Diminishing returns.

**Proposed parameter change:**
```python
def build_diff_prompt(
    variant_a_path: Path,
    variant_b_path: Path,
    prd_file: Path | None = None,  # NEW: optional PRD supplementary context
) -> str:
```

**Proposed supplementary block:**
```python
if prd_file is not None:
    base += (
        "\n\n## Supplementary PRD Context (when PRD file is provided)\n\n"
        "A Product Requirements Document (PRD) is included in the inputs. When "
        "comparing variants, additionally assess:\n"
        "1. Which variant better aligns with the PRD's stated business objectives "
        "(§5 Business Context) and success metrics (§19).\n"
        "2. Whether either variant omits persona-critical user journeys from the "
        "PRD's Customer Journey Map (§22).\n"
        "Note these as additional divergence points where relevant."
    )
```

**Note:** Requires refactoring the return from a single expression to `base = (...); if prd_file: ...; return base + _OUTPUT_FORMAT_BLOCK`.

**PRD sections referenced:** §5 Business Context, §19 Success Metrics, §22 Customer Journey Map

---

## Prompt Builder 5: `build_debate_prompt`

**Current signature (line 363-368):** [CODE-VERIFIED]
```python
def build_debate_prompt(
    diff_path: Path,
    variant_a_path: Path,
    variant_b_path: Path,
    depth: Literal["quick", "standard", "deep"],
) -> str:
```

**PRD enrichment value:** LOW (P3)

**Rationale:** The debate step facilitates adversarial discussion between variants. PRD context could frame debate arguments around business value, but by this point PRD context has already shaped the variants (via generate) and the diff analysis. Adding PRD here risks prompt bloat with diminishing returns.

**Proposed parameter change:**
```python
def build_debate_prompt(
    diff_path: Path,
    variant_a_path: Path,
    variant_b_path: Path,
    depth: Literal["quick", "standard", "deep"],
    prd_file: Path | None = None,  # NEW: optional PRD supplementary context
) -> str:
```

**Proposed supplementary block:**
```python
if prd_file is not None:
    base += (
        "\n\n## Supplementary PRD Context (when PRD file is provided)\n\n"
        "A Product Requirements Document (PRD) is included in the inputs. When "
        "debating divergence points, each perspective should consider business "
        "value alignment with the PRD's Success Metrics (§19) and User Personas "
        "(§7) as an additional evaluation criterion."
    )
```

**PRD sections referenced:** §7 User Personas, §19 Success Metrics

---

## Prompt Builder 6: `build_score_prompt`

**Current signature (line 390-394):** [CODE-VERIFIED]
```python
def build_score_prompt(
    debate_path: Path,
    variant_a_path: Path,
    variant_b_path: Path,
) -> str:
```

**PRD enrichment value:** MEDIUM (P2)

**Rationale:** The score step selects the base variant for the merge. PRD context can provide concrete scoring criteria: does the variant deliver business value faster (§19 metrics), does it cover all personas (§7), does it respect compliance constraints (§17)? This is more valuable than in diff/debate because it directly influences the merge outcome.

**Proposed parameter change:**
```python
def build_score_prompt(
    debate_path: Path,
    variant_a_path: Path,
    variant_b_path: Path,
    prd_file: Path | None = None,  # NEW: optional PRD supplementary context
) -> str:
```

**Proposed supplementary block:**
```python
if prd_file is not None:
    base += (
        "\n\n## Supplementary PRD Context (when PRD file is provided)\n\n"
        "A Product Requirements Document (PRD) is included in the inputs. When "
        "scoring variants, include these additional scoring dimensions:\n"
        "1. **Business value delivery**: Score how quickly each variant delivers "
        "against the PRD's Success Metrics (§19).\n"
        "2. **Persona coverage**: Score whether each variant addresses all user "
        "personas defined in the PRD (§7).\n"
        "3. **Compliance alignment**: Score whether each variant accounts for "
        "legal and compliance requirements from the PRD (§17).\n"
        "Weight these alongside technical scoring criteria."
    )
```

**Note:** Requires refactoring from single expression return to `base = (...); if prd_file: ...; return base + _OUTPUT_FORMAT_BLOCK`.

**PRD sections referenced:** §7 User Personas, §17 Legal/Compliance, §19 Success Metrics

---

## Prompt Builder 7: `build_merge_prompt`

**Current signature (line 416-420):** [CODE-VERIFIED]
```python
def build_merge_prompt(
    base_selection_path: Path,
    variant_a_path: Path,
    variant_b_path: Path,
    debate_path: Path,
) -> str:
```

**PRD enrichment value:** LOW (P3)

**Rationale:** The merge step synthesizes the final roadmap from the scored variants. By this point, PRD context has already influenced extraction, generation, scoring, and debate. The merge should primarily follow the score selection. Adding PRD here risks introducing new requirements at the synthesis stage, violating the pipeline's progressive refinement principle.

**Proposed parameter change:**
```python
def build_merge_prompt(
    base_selection_path: Path,
    variant_a_path: Path,
    variant_b_path: Path,
    debate_path: Path,
    prd_file: Path | None = None,  # NEW: optional PRD supplementary context
) -> str:
```

**Proposed supplementary block:**
```python
if prd_file is not None:
    base += (
        "\n\n## Supplementary PRD Context (when PRD file is provided)\n\n"
        "A Product Requirements Document (PRD) is included in the inputs. When "
        "producing the merged roadmap, verify the final output preserves:\n"
        "1. Coverage of all user personas from the PRD (§7).\n"
        "2. Alignment with business success metrics from the PRD (§19).\n"
        "Do NOT introduce new requirements from the PRD that were not part of "
        "the debate — the merge synthesizes debate-resolved content only."
    )
```

**Note:** Requires refactoring from single expression return.

**PRD sections referenced:** §7 User Personas, §19 Success Metrics

---

## Prompt Builder 8: `build_spec_fidelity_prompt`

**Current signature (line 448-451):** [CODE-VERIFIED]
```python
def build_spec_fidelity_prompt(
    spec_file: Path,
    roadmap_path: Path,
) -> str:
```

**PRD enrichment value:** HIGH (P1)

**Rationale:** Spec fidelity is the critical quality gate. PRD adds comparison dimensions the spec file alone doesn't cover: persona coverage, business metric traceability, compliance validation, and scope boundary enforcement. The current prompt already has 11 comparison dimensions (lines 489-500); PRD enrichment adds 3-4 more. [CODE-VERIFIED]

**Proposed parameter change:**
```python
def build_spec_fidelity_prompt(
    spec_file: Path,
    roadmap_path: Path,
    prd_file: Path | None = None,  # NEW: optional PRD supplementary context
) -> str:
```

**Proposed supplementary block (insert before `_OUTPUT_FORMAT_BLOCK`):**
```python
if prd_file is not None:
    base += (
        "\n\n## Supplementary PRD Validation (when PRD file is provided)\n\n"
        "A Product Requirements Document (PRD) is included in the inputs alongside "
        "the specification and roadmap. Additionally check these PRD-derived dimensions:\n"
        "12. **Persona Coverage**: Every user persona defined in the PRD (§7) should "
        "have at least one roadmap phase or task addressing their primary needs. Flag "
        "missing persona coverage as MEDIUM severity.\n"
        "13. **Business Metric Traceability**: Success metrics from the PRD (§19) "
        "should have corresponding validation milestones or acceptance criteria in "
        "the roadmap. Flag untraced metrics as MEDIUM severity.\n"
        "14. **Compliance & Legal Coverage**: Legal and compliance requirements from "
        "the PRD (§17) should have corresponding roadmap tasks or gates. Flag missing "
        "compliance coverage as HIGH severity.\n"
        "15. **Scope Boundary Enforcement**: The roadmap should not contain items that "
        "fall outside the PRD's Scope Definition (§12 In-Scope vs Out-of-Scope). Flag "
        "out-of-scope roadmap items as MEDIUM severity."
    )
```

**Note:** The dimension numbers (12-15) continue from the existing 11 dimensions in the prompt. [CODE-VERIFIED: existing dimensions numbered 1-11 at lines 489-500, though dimension 6 is from `_INTEGRATION_WIRING_DIMENSION`]

**PRD sections referenced:** §7 User Personas, §12 Scope Definition, §17 Legal/Compliance, §19 Success Metrics

---

## Prompt Builder 9: `build_wiring_verification_prompt`

**Current signature (line 528-531):** [CODE-VERIFIED]
```python
def build_wiring_verification_prompt(
    merge_file: Path,
    spec_source: str,
) -> str:
```

**PRD enrichment value:** NONE (Skip)

**Rationale:** This prompt performs pure structural code verification — checking unwired callables, orphan modules, and unregistered dispatch entries. PRD content (personas, business context, success metrics) has zero relevance to structural wiring analysis. No enrichment needed.

**Proposed parameter change:** None.
**Proposed supplementary block:** None.

---

## Prompt Builder 10: `build_test_strategy_prompt`

**Current signature (line 586-589):** [CODE-VERIFIED]
```python
def build_test_strategy_prompt(
    roadmap_path: Path,
    extraction_path: Path,
) -> str:
```

**PRD enrichment value:** HIGH (P1)

**Rationale:** Test strategy is where PRD content delivers significant unique value. Personas drive acceptance test scenarios. Customer journeys define E2E test flows. Business metrics define KPI validation tests. Compliance requirements mandate regulatory test categories. None of this content is typically in a spec or TDD.

**Proposed parameter change:**
```python
def build_test_strategy_prompt(
    roadmap_path: Path,
    extraction_path: Path,
    prd_file: Path | None = None,  # NEW: optional PRD supplementary context
) -> str:
```

**Proposed supplementary block (insert before `_OUTPUT_FORMAT_BLOCK`):**
```python
if prd_file is not None:
    base += (
        "\n\n## Supplementary PRD Context (when PRD file is provided)\n\n"
        "A Product Requirements Document (PRD) is included in the inputs alongside "
        "the roadmap and extraction. Use PRD content to enrich the test strategy:\n"
        "1. **Persona-based acceptance tests**: For each user persona in the PRD "
        "(§7), define at least one acceptance test scenario that validates their "
        "primary workflow.\n"
        "2. **Customer journey E2E tests**: Map the PRD's Customer Journey Map "
        "(§22) to end-to-end test flows covering the critical path for each journey.\n"
        "3. **KPI validation tests**: For each success metric in the PRD (§19), "
        "define a validation test that measures or proxies the metric.\n"
        "4. **Compliance test category**: If the PRD's Legal & Compliance section "
        "(§17) defines regulatory requirements, add a dedicated compliance test "
        "category with specific test cases.\n"
        "5. **Edge case coverage**: Reference the PRD's Error Handling & Edge Cases "
        "section (§23) to ensure negative test scenarios are included."
    )
```

**PRD sections referenced:** §7 User Personas, §17 Legal/Compliance, §19 Success Metrics, §22 Customer Journey Map, §23 Error Handling & Edge Cases

---

## Executor Wiring Changes Required

The executor at `src/superclaude/cli/roadmap/executor.py` calls each prompt builder at specific locations. [CODE-VERIFIED] For PRD enrichment to work, the executor must pass `prd_file=config.prd_file` to each modified prompt builder.

**Current call sites (from executor grep):**

| Line | Call | Change Needed |
|------|------|---------------|
| 888 | `build_extract_prompt_tdd(config.spec_file, retrospective_content=...)` | Add `prd_file=config.prd_file` |
| 893 | `build_extract_prompt(config.spec_file, retrospective_content=...)` | Add `prd_file=config.prd_file` |
| 908 | `build_generate_prompt(agent_a, extraction)` | Add `prd_file=config.prd_file` |
| 918 | `build_generate_prompt(agent_b, extraction)` | Add `prd_file=config.prd_file` |
| 930 | `build_diff_prompt(roadmap_a, roadmap_b)` | Add `prd_file=config.prd_file` |
| 940 | `build_debate_prompt(diff_file, roadmap_a, roadmap_b, config.depth)` | Add `prd_file=config.prd_file` |
| 950 | `build_score_prompt(debate_file, roadmap_a, roadmap_b)` | Add `prd_file=config.prd_file` |
| 960 | `build_merge_prompt(score_file, roadmap_a, roadmap_b, debate_file)` | Add `prd_file=config.prd_file` |
| 980 | `build_test_strategy_prompt(merge_file, extraction)` | Add `prd_file=config.prd_file` |
| 990 | `build_spec_fidelity_prompt(config.spec_file, merge_file)` | Add `prd_file=config.prd_file` |
| 1000 | `build_wiring_verification_prompt(merge_file, config.spec_file.name)` | **No change** |

**Additionally required:**
- `RoadmapConfig` in `models.py` needs: `prd_file: Path | None = None` (mirrors `tdd_file` at line 115)
- `commands.py` needs: `--prd-file` Click option (mirrors `--tdd-file` pattern if it exists, or follows `--retrospective-file` pattern)
- Executor `_build_steps()` must include `config.prd_file` in `step.inputs` for steps that receive the PRD file (so the LLM can read it via `_embed_inputs`)

---

## Refactoring Required

Several prompt builders currently return a single concatenated expression. To add conditional PRD blocks, they need refactoring to the `base = (...); if prd_file: base += ...; return base + _OUTPUT_FORMAT_BLOCK` pattern.

**Builders needing refactoring:** [CODE-VERIFIED]

| Builder | Current Pattern | Lines |
|---------|----------------|-------|
| `build_generate_prompt` | Single `return (...)` expression | 295-335 |
| `build_diff_prompt` | Single `return (...)` expression | 345-360 |
| `build_debate_prompt` | Single `return (...)` expression | 374-387 |
| `build_score_prompt` | Single `return (...)` expression | 399-413 |
| `build_merge_prompt` | Single `return (...)` expression | 426-445 |
| `build_spec_fidelity_prompt` | Single `return (...)` expression | 461-525 |
| `build_test_strategy_prompt` | Single `return (...)` expression | 596-629 |

**Builders already using `base = (...)` pattern (no refactoring needed):**

| Builder | Lines |
|---------|-------|
| `build_extract_prompt` | 101-158 |
| `build_extract_prompt_tdd` | 180-285 |

---

## Gaps and Questions

### Open Questions

1. **PRD file embedding in step inputs**: Should the PRD file be embedded via `_embed_inputs()` in every step that has PRD enrichment, or only in steps where the supplementary block references specific PRD sections? Embedding adds token cost. **Recommendation:** Embed only in P1 steps (extract, generate, spec-fidelity, test-strategy) and P2 steps (extract_tdd, score). P3 steps (diff, debate, merge) should get the parameter for future use but NOT embed the PRD file — the prompt block should reference PRD content indirectly through the extraction output.

2. **PRD + TDD + spec triple input**: When all three are provided, how should the extraction prompt handle three supplementary contexts? **Recommendation:** Stack both blocks — TDD block first (technical "how"), then PRD block (business "why"). Each block is self-contained and non-overlapping.

3. **Backward compatibility of `build_generate_prompt` refactoring**: The refactoring from single return expression to `base = (...)` pattern changes code structure but not behavior. Tests should verify identical output when `prd_file=None`. **Recommendation:** Add parametrized test cases.

### Stale Documentation Found

1. **Comment in `build_generate_prompt` (lines 309-316)**: Contains a deferred work comment referencing `TASK-RF-20260325-cli-tdd Deferred Work Items` for "Full TDD-aware generate prompt update." This comment suggests TDD-specific generate prompt enrichment was planned but not implemented. [CODE-VERIFIED] The PRD integration should either implement this alongside PRD enrichment or explicitly note it remains deferred.

---

## Summary

### Priority Matrix

| Priority | Builder | PRD Value | Parameter Change | Supplementary Block | Refactoring |
|----------|---------|-----------|-----------------|---------------------|-------------|
| **P1** | `build_extract_prompt` | HIGH | Add `prd_file` | 5 check items | None needed |
| **P1** | `build_generate_prompt` | HIGH | Add `prd_file` | 4 check items | Yes — single expr to base pattern |
| **P1** | `build_spec_fidelity_prompt` | HIGH | Add `prd_file` | 4 dimensions (12-15) | Yes — single expr to base pattern |
| **P1** | `build_test_strategy_prompt` | HIGH | Add `prd_file` | 5 check items | Yes — single expr to base pattern |
| **P2** | `build_extract_prompt_tdd` | MEDIUM | Add `prd_file` | 3 check items | None needed |
| **P2** | `build_score_prompt` | MEDIUM | Add `prd_file` | 3 scoring dimensions | Yes — single expr to base pattern |
| **P3** | `build_diff_prompt` | LOW | Add `prd_file` | 2 check items | Yes — single expr to base pattern |
| **P3** | `build_debate_prompt` | LOW | Add `prd_file` | 1 paragraph | Yes — single expr to base pattern |
| **P3** | `build_merge_prompt` | LOW | Add `prd_file` | 2 check items | Yes — single expr to base pattern |
| **Skip** | `build_wiring_verification_prompt` | NONE | None | None | None |

### Implementation Scope

- **9 prompt builders** gain `prd_file: Path | None = None` parameter
- **9 supplementary blocks** to draft (all provided above)
- **7 builders** need refactoring from single return expression to base pattern
- **1 model field** to add: `RoadmapConfig.prd_file`
- **1 CLI flag** to add: `--prd-file`
- **~10 executor call sites** to update with `prd_file=config.prd_file`
- **0 existing tests broken** (all changes are additive with `None` defaults)

### Key Design Decisions

1. **PRD is advisory, not authoritative**: All supplementary blocks include the guardrail "do NOT treat PRD content as hard requirements unless also stated in the specification/TDD."
2. **Severity classifications**: PRD-derived deviations default to MEDIUM, except compliance gaps which are HIGH (consistent with how the pipeline treats compliance throughout).
3. **Pattern fidelity**: Every supplementary block follows the exact pattern from `build_tasklist_fidelity_prompt` lines 110-123: conditional check, `\n\n##` heading, numbered check items, severity guidance.
4. **PRD sections consistently referenced**: §7 (Personas), §12 (Scope), §17 (Compliance), §19 (Success Metrics), §22 (Customer Journey) appear across multiple builders — these are the highest-value PRD sections for pipeline enrichment.

