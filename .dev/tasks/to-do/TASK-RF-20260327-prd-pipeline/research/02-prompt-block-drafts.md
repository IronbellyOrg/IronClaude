# Prompt Block Compilation: PRD Supplementary Blocks by Builder

**Research type:** Prompt Block Compilation
**Source:** `02-prompt-enrichment-mapping.md` + `synth-05-implementation-plan.md` Phase 7
**Verified against:** `src/superclaude/cli/roadmap/prompts.py`, `src/superclaude/cli/tasklist/prompts.py`
**Status:** Complete
**Date:** 2026-03-27

---

## How to Use This Reference

Each builder entry below provides everything needed for implementation:
- Copy the **Proposed Parameter Change** into the function signature
- Copy the **Supplementary Block** into the function body (location noted per builder)
- If **Refactoring Required** is YES, convert the single `return (...)` expression to `base = (...); if prd_file: base += ...; return base + _OUTPUT_FORMAT_BLOCK`
- Wire `prd_file=config.prd_file` at the executor call site listed

---

## Builder 1: `build_extract_prompt` [P1 -- HIGH]

**File:** `src/superclaude/cli/roadmap/prompts.py`
**Current signature (line 82-85):**
```python
def build_extract_prompt(
    spec_file: Path,
    retrospective_content: str | None = None,
) -> str:
```

**Refactoring required:** NO (already uses `base = (...)` pattern)
**Insertion point:** After retrospective block (line ~156), before `return base + _OUTPUT_FORMAT_BLOCK`
**Executor call site:** Line ~893

**Proposed parameter change:**
```python
def build_extract_prompt(
    spec_file: Path,
    retrospective_content: str | None = None,
    prd_file: Path | None = None,
) -> str:
```

**Supplementary block:**
```python
if prd_file is not None:
    base += (
        "\n\n## Supplementary PRD Context (when PRD file is provided)\n\n"
        "A Product Requirements Document (PRD) is included in the inputs alongside "
        "the specification. Use it as supplementary business context for extraction. "
        "Additionally extract:\n"
        "1. Business objectives and success metrics from the PRD's Success Metrics "
        "section (S19) -- surface as additional Success Criteria.\n"
        "2. User personas from the PRD's User Personas section (S7) -- note in the "
        "Architectural Constraints section as persona-driven design requirements.\n"
        "3. Scope boundaries from the PRD's Scope Definition section (S12) -- use to "
        "validate that extracted requirements fall within stated scope.\n"
        "4. Legal and compliance requirements from the PRD's Legal & Compliance "
        "section (S17) -- surface as Non-Functional Requirements if not already "
        "present in the spec.\n"
        "5. Jobs To Be Done from the PRD's JTBD section (S6) -- note in Open "
        "Questions if any JTBD lack corresponding functional requirements.\n"
        "The PRD is advisory context for enrichment -- do NOT treat PRD content "
        "as hard requirements unless they are also stated in the specification."
    )
```

**PRD sections referenced:** S6 JTBD, S7 User Personas, S12 Scope Definition, S17 Legal/Compliance, S19 Success Metrics

---

## Builder 2: `build_extract_prompt_tdd` [P2 -- MEDIUM]

**File:** `src/superclaude/cli/roadmap/prompts.py`
**Current signature (line 161-164):**
```python
def build_extract_prompt_tdd(
    spec_file: Path,
    retrospective_content: str | None = None,
) -> str:
```

**Refactoring required:** NO (already uses `base = (...)` pattern)
**Insertion point:** After retrospective block (line ~283), before `return base + _OUTPUT_FORMAT_BLOCK`
**Executor call site:** Line ~888

**Proposed parameter change:**
```python
def build_extract_prompt_tdd(
    spec_file: Path,
    retrospective_content: str | None = None,
    prd_file: Path | None = None,
) -> str:
```

**Supplementary block:**
```python
if prd_file is not None:
    base += (
        "\n\n## Supplementary PRD Context (when PRD file is provided)\n\n"
        "A Product Requirements Document (PRD) is included in the inputs alongside "
        "the TDD. The TDD captures technical design; the PRD provides business "
        "context. Additionally extract:\n"
        "1. Business success metrics from the PRD's Success Metrics section (S19) "
        "-- surface as additional Success Criteria alongside TDD-derived criteria.\n"
        "2. User personas from the PRD's User Personas section (S7) -- note as "
        "persona-driven design requirements in Architectural Constraints.\n"
        "3. Legal and compliance requirements from the PRD's Legal & Compliance "
        "section (S17) -- surface as Non-Functional Requirements if not already "
        "present in the TDD.\n"
        "The PRD is advisory context for enrichment -- do NOT treat PRD content "
        "as hard requirements unless also stated in the TDD."
    )
```

**PRD sections referenced:** S7 User Personas, S17 Legal/Compliance, S19 Success Metrics

---

## Builder 3: `build_generate_prompt` [P1 -- HIGH]

**File:** `src/superclaude/cli/roadmap/prompts.py`
**Current signature (line 288):**
```python
def build_generate_prompt(agent: AgentSpec, extraction_path: Path) -> str:
```

**Refactoring required:** YES -- currently returns a single concatenated expression (lines 295-335). Must refactor to `base = (...); if prd_file: base += ...; return base + _INTEGRATION_ENUMERATION_BLOCK + _OUTPUT_FORMAT_BLOCK`
**Executor call sites:** Lines ~908, ~918 (called twice, once per agent variant)

**Proposed parameter change:**
```python
def build_generate_prompt(
    agent: AgentSpec,
    extraction_path: Path,
    prd_file: Path | None = None,
) -> str:
```

**Supplementary block (insert before `_INTEGRATION_ENUMERATION_BLOCK` concatenation):**
```python
if prd_file is not None:
    base += (
        "\n\n## Supplementary PRD Context (when PRD file is provided)\n\n"
        "A Product Requirements Document (PRD) is included in the inputs alongside "
        "the extraction. Use PRD content to inform roadmap prioritization and phasing:\n"
        "1. **Value-based phasing**: Use the PRD's Business Context (S5) and Success "
        "Metrics (S19) to prioritize phases that deliver measurable business value earliest.\n"
        "2. **Persona-driven sequencing**: Use the PRD's User Personas (S7) and Customer "
        "Journey Map (S22) to ensure the roadmap addresses highest-impact user needs first.\n"
        "3. **Compliance gates**: If the PRD's Legal & Compliance section (S17) defines "
        "regulatory requirements, ensure the roadmap includes compliance validation "
        "milestones at appropriate phases.\n"
        "4. **Scope guardrails**: Use the PRD's Scope Definition (S12) to flag any "
        "roadmap items that fall outside stated product scope.\n"
        "The PRD provides business 'why' context -- do NOT let it override technical "
        "sequencing constraints from the extraction."
    )
```

**PRD sections referenced:** S5 Business Context, S7 User Personas, S12 Scope Definition, S17 Legal/Compliance, S19 Success Metrics, S22 Customer Journey Map

**Stale comment note:** Lines 309-316 contain a deferred work comment referencing TDD-aware generate prompt update. PRD integration should either address this alongside or explicitly note it remains deferred.

---

## Builder 4: `build_diff_prompt` [P3 -- LOW]

**File:** `src/superclaude/cli/roadmap/prompts.py`
**Current signature (line 338):**
```python
def build_diff_prompt(variant_a_path: Path, variant_b_path: Path) -> str:
```

**Refactoring required:** YES -- single expression return (lines 345-360)
**Executor call site:** Line ~930

**Proposed parameter change:**
```python
def build_diff_prompt(
    variant_a_path: Path,
    variant_b_path: Path,
    prd_file: Path | None = None,
) -> str:
```

**Supplementary block:**
```python
if prd_file is not None:
    base += (
        "\n\n## Supplementary PRD Context (when PRD file is provided)\n\n"
        "A Product Requirements Document (PRD) is included in the inputs. When "
        "comparing variants, additionally assess:\n"
        "1. Which variant better aligns with the PRD's stated business objectives "
        "(S5 Business Context) and success metrics (S19).\n"
        "2. Whether either variant omits persona-critical user journeys from the "
        "PRD's Customer Journey Map (S22).\n"
        "Note these as additional divergence points where relevant."
    )
```

**PRD sections referenced:** S5 Business Context, S19 Success Metrics, S22 Customer Journey Map

---

## Builder 5: `build_debate_prompt` [P3 -- LOW]

**File:** `src/superclaude/cli/roadmap/prompts.py`
**Current signature (line 363-368):**
```python
def build_debate_prompt(
    diff_path: Path,
    variant_a_path: Path,
    variant_b_path: Path,
    depth: Literal["quick", "standard", "deep"],
) -> str:
```

**Refactoring required:** YES -- single expression return (lines 374-387)
**Executor call site:** Line ~940

**Proposed parameter change:**
```python
def build_debate_prompt(
    diff_path: Path,
    variant_a_path: Path,
    variant_b_path: Path,
    depth: Literal["quick", "standard", "deep"],
    prd_file: Path | None = None,
) -> str:
```

**Supplementary block:**
```python
if prd_file is not None:
    base += (
        "\n\n## Supplementary PRD Context (when PRD file is provided)\n\n"
        "A Product Requirements Document (PRD) is included in the inputs. When "
        "debating divergence points, each perspective should consider business "
        "value alignment with the PRD's Success Metrics (S19) and User Personas "
        "(S7) as an additional evaluation criterion."
    )
```

**PRD sections referenced:** S7 User Personas, S19 Success Metrics

---

## Builder 6: `build_score_prompt` [P2 -- MEDIUM]

**File:** `src/superclaude/cli/roadmap/prompts.py`
**Current signature (line 390-394):**
```python
def build_score_prompt(
    debate_path: Path,
    variant_a_path: Path,
    variant_b_path: Path,
) -> str:
```

**Refactoring required:** YES -- single expression return (lines 399-413)
**Executor call site:** Line ~950

**Proposed parameter change:**
```python
def build_score_prompt(
    debate_path: Path,
    variant_a_path: Path,
    variant_b_path: Path,
    prd_file: Path | None = None,
) -> str:
```

**Supplementary block:**
```python
if prd_file is not None:
    base += (
        "\n\n## Supplementary PRD Context (when PRD file is provided)\n\n"
        "A Product Requirements Document (PRD) is included in the inputs. When "
        "scoring variants, include these additional scoring dimensions:\n"
        "1. **Business value delivery**: Score how quickly each variant delivers "
        "against the PRD's Success Metrics (S19).\n"
        "2. **Persona coverage**: Score whether each variant addresses all user "
        "personas defined in the PRD (S7).\n"
        "3. **Compliance alignment**: Score whether each variant accounts for "
        "legal and compliance requirements from the PRD (S17).\n"
        "Weight these alongside technical scoring criteria."
    )
```

**PRD sections referenced:** S7 User Personas, S17 Legal/Compliance, S19 Success Metrics

---

## Builder 7: `build_merge_prompt` [P3 -- LOW]

**File:** `src/superclaude/cli/roadmap/prompts.py`
**Current signature (line 416-420):**
```python
def build_merge_prompt(
    base_selection_path: Path,
    variant_a_path: Path,
    variant_b_path: Path,
    debate_path: Path,
) -> str:
```

**Refactoring required:** YES -- single expression return (lines 426-445)
**Executor call site:** Line ~960

**Proposed parameter change:**
```python
def build_merge_prompt(
    base_selection_path: Path,
    variant_a_path: Path,
    variant_b_path: Path,
    debate_path: Path,
    prd_file: Path | None = None,
) -> str:
```

**Supplementary block:**
```python
if prd_file is not None:
    base += (
        "\n\n## Supplementary PRD Context (when PRD file is provided)\n\n"
        "A Product Requirements Document (PRD) is included in the inputs. When "
        "producing the merged roadmap, verify the final output preserves:\n"
        "1. Coverage of all user personas from the PRD (S7).\n"
        "2. Alignment with business success metrics from the PRD (S19).\n"
        "Do NOT introduce new requirements from the PRD that were not part of "
        "the debate -- the merge synthesizes debate-resolved content only."
    )
```

**PRD sections referenced:** S7 User Personas, S19 Success Metrics

---

## Builder 8: `build_spec_fidelity_prompt` [P1 -- HIGH]

**File:** `src/superclaude/cli/roadmap/prompts.py`
**Current signature (line 448-451):**
```python
def build_spec_fidelity_prompt(
    spec_file: Path,
    roadmap_path: Path,
) -> str:
```

**Refactoring required:** YES -- single expression return (lines 461-525)
**Executor call site:** Line ~990

**Proposed parameter change:**
```python
def build_spec_fidelity_prompt(
    spec_file: Path,
    roadmap_path: Path,
    prd_file: Path | None = None,
) -> str:
```

**Supplementary block (insert before `_OUTPUT_FORMAT_BLOCK`):**
```python
if prd_file is not None:
    base += (
        "\n\n## Supplementary PRD Validation (when PRD file is provided)\n\n"
        "A Product Requirements Document (PRD) is included in the inputs alongside "
        "the specification and roadmap. Additionally check these PRD-derived dimensions:\n"
        "12. **Persona Coverage**: Every user persona defined in the PRD (S7) should "
        "have at least one roadmap phase or task addressing their primary needs. Flag "
        "missing persona coverage as MEDIUM severity.\n"
        "13. **Business Metric Traceability**: Success metrics from the PRD (S19) "
        "should have corresponding validation milestones or acceptance criteria in "
        "the roadmap. Flag untraced metrics as MEDIUM severity.\n"
        "14. **Compliance & Legal Coverage**: Legal and compliance requirements from "
        "the PRD (S17) should have corresponding roadmap tasks or gates. Flag missing "
        "compliance coverage as HIGH severity.\n"
        "15. **Scope Boundary Enforcement**: The roadmap should not contain items that "
        "fall outside the PRD's Scope Definition (S12 In-Scope vs Out-of-Scope). Flag "
        "out-of-scope roadmap items as MEDIUM severity."
    )
```

**Note:** Dimensions numbered 12-15 continue from the existing 11 dimensions (dimension 6 is from `_INTEGRATION_WIRING_DIMENSION`).

**PRD sections referenced:** S7 User Personas, S12 Scope Definition, S17 Legal/Compliance, S19 Success Metrics

---

## Builder 9: `build_wiring_verification_prompt` [SKIP -- NONE]

**File:** `src/superclaude/cli/roadmap/prompts.py`
**Current signature (line 528-531):**
```python
def build_wiring_verification_prompt(
    merge_file: Path,
    spec_source: str,
) -> str:
```

**Refactoring required:** N/A
**Rationale:** Pure structural code verification. PRD content (personas, business context, success metrics) has zero relevance to structural wiring analysis. No enrichment needed.

**No parameter change. No supplementary block.**

---

## Builder 10: `build_test_strategy_prompt` [P1 -- HIGH]

**File:** `src/superclaude/cli/roadmap/prompts.py`
**Current signature (line 586-589):**
```python
def build_test_strategy_prompt(
    roadmap_path: Path,
    extraction_path: Path,
) -> str:
```

**Refactoring required:** YES -- single expression return (lines 596-629)
**Executor call site:** Line ~980

**Proposed parameter change:**
```python
def build_test_strategy_prompt(
    roadmap_path: Path,
    extraction_path: Path,
    prd_file: Path | None = None,
) -> str:
```

**Supplementary block (insert before `_OUTPUT_FORMAT_BLOCK`):**
```python
if prd_file is not None:
    base += (
        "\n\n## Supplementary PRD Context (when PRD file is provided)\n\n"
        "A Product Requirements Document (PRD) is included in the inputs alongside "
        "the roadmap and extraction. Use PRD content to enrich the test strategy:\n"
        "1. **Persona-based acceptance tests**: For each user persona in the PRD "
        "(S7), define at least one acceptance test scenario that validates their "
        "primary workflow.\n"
        "2. **Customer journey E2E tests**: Map the PRD's Customer Journey Map "
        "(S22) to end-to-end test flows covering the critical path for each journey.\n"
        "3. **KPI validation tests**: For each success metric in the PRD (S19), "
        "define a validation test that measures or proxies the metric.\n"
        "4. **Compliance test category**: If the PRD's Legal & Compliance section "
        "(S17) defines regulatory requirements, add a dedicated compliance test "
        "category with specific test cases.\n"
        "5. **Edge case coverage**: Reference the PRD's Error Handling & Edge Cases "
        "section (S23) to ensure negative test scenarios are included."
    )
```

**PRD sections referenced:** S7 User Personas, S17 Legal/Compliance, S19 Success Metrics, S22 Customer Journey Map, S23 Error Handling & Edge Cases

---

## Builder 11: `build_tasklist_fidelity_prompt` [Existing TDD Pattern -- PRD Extension Needed]

**File:** `src/superclaude/cli/tasklist/prompts.py`
**Current signature (line 17-21):**
```python
def build_tasklist_fidelity_prompt(
    roadmap_file: Path,
    tasklist_dir: Path,
    tdd_file: Path | None = None,
) -> str:
```

**Refactoring required:** NO (already uses `base = (...)` pattern with TDD conditional block at lines 110-123)
**Existing TDD block:** Lines 110-123 -- the reference pattern for all supplementary blocks

**Proposed parameter change:**
```python
def build_tasklist_fidelity_prompt(
    roadmap_file: Path,
    tasklist_dir: Path,
    tdd_file: Path | None = None,
    prd_file: Path | None = None,
) -> str:
```

**Supplementary PRD block (insert after TDD block, before `return base + _OUTPUT_FORMAT_BLOCK`):**
```python
if prd_file is not None:
    base += (
        "\n\n## Supplementary PRD Validation (when PRD file is provided)\n\n"
        "A Product Requirements Document (PRD) is included in the inputs alongside "
        "the roadmap and tasklist. Additionally check:\n"
        "1. User persona coverage from the PRD's User Personas section (S7) -- "
        "tasks touching user-facing flows should reference which persona is served.\n"
        "2. Success metrics from the PRD's Success Metrics section (S19) should "
        "have corresponding instrumentation or measurement tasks in the tasklist.\n"
        "3. Acceptance scenarios from the PRD's Scope Definition (S12) and Customer "
        "Journey Map (S22) should have corresponding verification tasks.\n"
        "Flag missing coverage as MEDIUM severity deviations."
    )
```

**PRD sections referenced:** S7 User Personas, S12 Scope Definition, S19 Success Metrics, S22 Customer Journey Map

---

## Tasklist Generation Enrichment Blocks (from synth-05 Phase 7, Steps 7.2.1-7.2.3)

These blocks target a tasklist **generation** prompt builder (not the fidelity validator above). They apply when a `build_tasklist_generate_prompt` or equivalent exists in `src/superclaude/cli/tasklist/prompts.py`. Currently no such function exists -- it would need to be created as part of Phase 7 implementation.

### 7.2.1: TDD Generation Enrichment Block

```python
if tdd_file is not None:
    base += (
        "\n\n## Supplementary TDD Enrichment (for task generation)\n\n"
        "A Technical Design Document (TDD) is included alongside the roadmap. "
        "Use it to enrich task decomposition with:\n"
        "1. Specific test cases from S15 Testing Strategy -- each test case should "
        "map to a validation task with exact test name and expected behavior.\n"
        "2. API endpoint schemas from S8 -- each endpoint should have implementation "
        "tasks with request/response field details.\n"
        "3. Component specifications from S10 -- each component should have tasks "
        "with prop types, dependencies, and integration points.\n"
        "4. Migration rollback steps from S19 -- each rollback procedure should be "
        "a contingency task with trigger conditions.\n"
        "5. Data model field definitions from S7 -- each entity should have schema "
        "implementation tasks with exact field types."
    )
```

### 7.2.2: PRD Generation Enrichment Block

```python
if prd_file is not None:
    base += (
        "\n\n## Supplementary PRD Enrichment (for task generation)\n\n"
        "A Product Requirements Document (PRD) is included alongside the roadmap. "
        "Use it to enrich task decomposition with:\n"
        "1. User persona context from S7 -- tasks touching user-facing flows should "
        "reference which persona is served and their specific needs.\n"
        "2. Acceptance scenarios from S7/S22 -- each user story acceptance criterion "
        "should map to a verification task.\n"
        "3. Success metrics from S19 -- tasks should include metric instrumentation "
        "subtasks (tracking, dashboards, alerts) where applicable.\n"
        "4. Stakeholder priorities from S5 -- task priority should reflect business "
        "value ordering, not just technical dependency.\n"
        "5. Scope boundaries from S12 -- tasks must not exceed defined scope; "
        "generate explicit 'out of scope' markers where roadmap milestones approach "
        "scope edges.\n"
        "PRD context informs task descriptions and priorities but does NOT generate "
        "standalone implementation tasks. Engineering tasks come from the roadmap; "
        "PRD enriches them."
    )
```

### 7.2.3: Combined TDD + PRD Interaction Note

When both are provided, stack both blocks (TDD first, then PRD) and append:

```python
if tdd_file is not None and prd_file is not None:
    base += (
        "\n\n## TDD + PRD Interaction\n\n"
        "When both TDD and PRD are available, TDD provides structural engineering "
        "detail and PRD provides product context. TDD-derived task enrichment "
        "(test cases, schemas, components) takes precedence for implementation "
        "specifics. PRD-derived enrichment (personas, metrics, priorities) shapes "
        "task descriptions, acceptance criteria, and priority ordering."
    )
```

---

## Summary Table

| # | Builder | File | Priority | Refactoring | PRD Sections | Check Items |
|---|---------|------|----------|-------------|--------------|-------------|
| 1 | `build_extract_prompt` | roadmap/prompts.py | P1 | No | S6,S7,S12,S17,S19 | 5 |
| 2 | `build_extract_prompt_tdd` | roadmap/prompts.py | P2 | No | S7,S17,S19 | 3 |
| 3 | `build_generate_prompt` | roadmap/prompts.py | P1 | YES | S5,S7,S12,S17,S19,S22 | 4 |
| 4 | `build_diff_prompt` | roadmap/prompts.py | P3 | YES | S5,S19,S22 | 2 |
| 5 | `build_debate_prompt` | roadmap/prompts.py | P3 | YES | S7,S19 | 1 |
| 6 | `build_score_prompt` | roadmap/prompts.py | P2 | YES | S7,S17,S19 | 3 |
| 7 | `build_merge_prompt` | roadmap/prompts.py | P3 | YES | S7,S19 | 2 |
| 8 | `build_spec_fidelity_prompt` | roadmap/prompts.py | P1 | YES | S7,S12,S17,S19 | 4 (dims 12-15) |
| 9 | `build_wiring_verification_prompt` | roadmap/prompts.py | Skip | No | -- | 0 |
| 10 | `build_test_strategy_prompt` | roadmap/prompts.py | P1 | YES | S7,S17,S19,S22,S23 | 5 |
| 11 | `build_tasklist_fidelity_prompt` | tasklist/prompts.py | P1 | No | S7,S12,S19,S22 | 3 |

**Refactoring tally:** 7 builders need single-expression-to-base-pattern refactoring
**Total supplementary blocks drafted:** 11 (9 roadmap + 1 tasklist fidelity + 1 tasklist generation set)
**All signatures verified against current source files on 2026-03-27**

### Executor Wiring (all in `src/superclaude/cli/roadmap/executor.py`)

| Approx Line | Call | Change |
|-------------|------|--------|
| ~888 | `build_extract_prompt_tdd(...)` | Add `prd_file=config.prd_file` |
| ~893 | `build_extract_prompt(...)` | Add `prd_file=config.prd_file` |
| ~908 | `build_generate_prompt(agent_a, ...)` | Add `prd_file=config.prd_file` |
| ~918 | `build_generate_prompt(agent_b, ...)` | Add `prd_file=config.prd_file` |
| ~930 | `build_diff_prompt(...)` | Add `prd_file=config.prd_file` |
| ~940 | `build_debate_prompt(...)` | Add `prd_file=config.prd_file` |
| ~950 | `build_score_prompt(...)` | Add `prd_file=config.prd_file` |
| ~960 | `build_merge_prompt(...)` | Add `prd_file=config.prd_file` |
| ~980 | `build_test_strategy_prompt(...)` | Add `prd_file=config.prd_file` |
| ~990 | `build_spec_fidelity_prompt(...)` | Add `prd_file=config.prd_file` |
| ~1000 | `build_wiring_verification_prompt(...)` | **No change** |

### Model & CLI Changes Required

- `RoadmapConfig` in `models.py`: Add `prd_file: Path | None = None`
- `commands.py`: Add `--prd-file` Click option
- Executor `_build_steps()`: Include `config.prd_file` in `step.inputs` for P1/P2 steps (embed the file so LLM reads it). P3 steps get the parameter but do NOT embed the PRD file.

### Design Guardrails (consistent across all blocks)

1. PRD is advisory, not authoritative: all blocks include "do NOT treat PRD content as hard requirements unless also stated in the specification/TDD"
2. Severity defaults: PRD-derived deviations default to MEDIUM, except compliance gaps which are HIGH
3. Pattern fidelity: every block follows the `build_tasklist_fidelity_prompt` pattern -- conditional check, `\n\n##` heading, numbered check items, severity guidance
4. Most-referenced PRD sections: S7 (Personas), S12 (Scope), S17 (Compliance), S19 (Success Metrics), S22 (Customer Journey)
