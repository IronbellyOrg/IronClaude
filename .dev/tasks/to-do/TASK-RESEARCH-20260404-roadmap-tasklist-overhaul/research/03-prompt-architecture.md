# Research: Prompt Architecture

**Investigation type:** Code Tracer
**Scope:** src/superclaude/cli/roadmap/prompts.py (all functions and constants)
**Status:** Complete
**Date:** 2026-04-04

---

## Table of Contents

1. [Shared Constants](#1-shared-constants)
2. [build_extract_prompt](#2-build_extract_prompt)
3. [build_extract_prompt_tdd](#3-build_extract_prompt_tdd)
4. [build_generate_prompt](#4-build_generate_prompt)
5. [build_diff_prompt](#5-build_diff_prompt)
6. [build_debate_prompt](#6-build_debate_prompt)
7. [build_score_prompt](#7-build_score_prompt)
8. [build_merge_prompt](#8-build_merge_prompt)
9. [build_spec_fidelity_prompt](#9-build_spec_fidelity_prompt)
10. [build_wiring_verification_prompt](#10-build_wiring_verification_prompt)
11. [build_test_strategy_prompt](#11-build_test_strategy_prompt)
12. [Per-Prompt Summary Table](#12-per-prompt-summary-table)
13. [Gaps and Questions](#13-gaps-and-questions)
14. [Stale Documentation Found](#14-stale-documentation-found)
15. [Summary](#15-summary)

---

## 1. Shared Constants

File: `src/superclaude/cli/roadmap/prompts.py`, lines 17-79.

### `_DEPTH_INSTRUCTIONS` (dict, lines 17-36)

Maps depth levels to debate round instructions:

| Key | Rounds | Description |
|-----|--------|-------------|
| `"quick"` | 1 | Single focused round: positions on key divergence points, then convergence assessment |
| `"standard"` | 2 | Round 1: initial positions. Round 2: rebuttals. Then convergence assessment |
| `"deep"` | 3 | Round 1: positions. Round 2: rebuttals. Round 3: concessions and remaining disagreements. Then convergence assessment |

**Granularity impact:** None directly -- these control debate thoroughness, not data fidelity. However, "quick" may miss divergence points that "deep" would surface, indirectly affecting merge quality.

### `_INTEGRATION_ENUMERATION_BLOCK` (string, lines 38-49)

Appended to `build_generate_prompt`. Requires explicit enumeration of integration points:
- Named Artifact (dispatch table, registry, mechanism name)
- Wired Components (implementations wired into it)
- Owning Phase (which phase creates/populates)
- Cross-Reference (which phase(s) consume)

**Key instruction:** "Do NOT assume that standard skeleton-to-implement phasing covers custom dispatch/wiring mechanisms. Each mechanism requires an explicit wiring task."

**Granularity impact:** PRESERVES. Forces explicit enumeration of wiring mechanisms that would otherwise be lost in generic "implement phase" tasks.

### `_INTEGRATION_WIRING_DIMENSION` (string, lines 51-60)

Appended to `build_spec_fidelity_prompt` as dimension #6. Requires verification that the roadmap contains explicit tasks for each dispatch table, registry, DI injection point, callback binding, middleware chain, or strategy pattern to:
- Create/populate the mechanism
- Wire concrete implementations
- Test the wiring end-to-end

**Severity classification:** HIGH if mechanism exists in spec but has no corresponding wiring task.

**Granularity impact:** PRESERVES. This is a validation dimension, not a transformation. It catches granularity loss in the generate step.

### `_OUTPUT_FORMAT_BLOCK` (string, lines 62-79)

Appended to ALL prompt functions. Wraps output in `<output_format>` tags. Contains:
- "CRITICAL: Your response MUST begin with YAML frontmatter (--- delimited block)."
- "Do NOT include any text, preamble, or commentary before the opening ---."
- Correct/incorrect examples showing no conversational preamble.

**Granularity impact:** None. This is a formatting constraint, not a content constraint.

---

## 2. build_extract_prompt

**Function signature:** `build_extract_prompt(spec_file, retrospective_content=None, tdd_file=None, prd_file=None) -> str`
**Step ID:** `extract`
**Lines:** 82-205
**Role instruction:** "You are a requirements extraction specialist."

### Format Requested

YAML frontmatter with 13 fields:
- `spec_source`, `generated`, `generator` (provenance)
- `functional_requirements`, `nonfunctional_requirements`, `total_requirements` (counts)
- `complexity_score` (float 0.0-1.0), `complexity_class` (LOW/MEDIUM/HIGH)
- `domains_detected` (list of strings)
- `risks_identified`, `dependencies_identified`, `success_criteria_count` (counts)
- `extraction_mode` (standard/chunked)

Body: 8 structured sections:
1. Functional Requirements
2. Non-Functional Requirements
3. Complexity Assessment
4. Architectural Constraints
5. Risk Inventory
6. Dependency Inventory
7. Success Criteria
8. Open Questions

### Minimum Counts

No explicit minimum counts specified. The prompt says "Be thorough and precise. Extract every requirement, even implicit ones."

### Key Instructions (verbatim)

- "Use the spec's exact requirement identifiers verbatim as primary IDs. Do NOT create a new numbering scheme (e.g., do NOT renumber as FR-001, FR-002)."
- "If a spec uses FR-EVAL-001.1, use FR-EVAL-001.1."
- "If a requirement needs sub-decomposition, use suffixes on the original ID (e.g., FR-EVAL-001.1a, FR-EVAL-001.1b)."
- "If the spec has no requirement IDs, then use FR-NNN as a fallback."
- "The functional_requirements frontmatter count must equal the number of top-level requirements in the spec, not sub-decompositions."

### Optional Blocks

- **Retrospective** (when `retrospective_content` provided): Framed as "advisory context only... NOT additional requirements and MUST NOT be treated as such." Feeds into risk assessment and open questions. RSK-004 mitigation.
- **TDD context** (when `tdd_file` provided): 6 enrichment instructions pulling from TDD sections 7, 8, 10, 15, 19, 25. Key: "preserve the spec's requirement IDs and language as primary."
- **PRD context** (when `prd_file` provided): 5 enrichment instructions pulling from PRD sections S6, S7, S12, S17, S19. Key: "When PRD business requirements conflict with the specification's technical approach, the specification wins on implementation details but the PRD wins on business intent and constraints."

### Template References

None. This is a pure prompt with no external template files.

### Granularity Impact: REDUCES

**Critical assessment:** This is the first major granularity reduction point. A specification document with tables, code blocks, field definitions, and detailed API contracts gets summarized into 8 prose sections. While the prompt says "extract every requirement, even implicit ones," the output format is free-form markdown under section headings -- there is no instruction to preserve tables, code blocks, or structured data formats from the source document. The extraction is a lossy summarization.

**Specific losses:**
- Table structures from the spec become prose bullet lists
- Code interface definitions become text descriptions
- Field-level type/constraint details may be collapsed into entity-level summaries
- The frontmatter counts (e.g., `functional_requirements: 42`) track quantity but not the actual content fidelity

---

## 3. build_extract_prompt_tdd

**Function signature:** `build_extract_prompt_tdd(spec_file, retrospective_content=None, tdd_file=None, prd_file=None) -> str`
**Step ID:** `extract` (when input is a TDD)
**Lines:** 208-395
**Role instruction:** "You are a requirements and design extraction specialist."

### Format Requested

YAML frontmatter with 19 fields (13 standard + 6 TDD-specific):
- All 13 fields from `build_extract_prompt`
- `data_models_identified` (integer, or 0 if absent)
- `api_surfaces_identified` (integer, or 0 if absent)
- `components_identified` (integer, or 0 if absent)
- `test_artifacts_identified` (integer, or 0 if absent)
- `migration_items_identified` (integer, or 0 if absent)
- `operational_items_identified` (integer, or 0 if absent)

Body: 14 structured sections (8 standard + 6 TDD-specific):
1-8. Same as `build_extract_prompt`
9. Data Models and Interfaces
10. API Specifications
11. Component Inventory
12. Testing Strategy
13. Migration and Rollout Plan
14. Operational Readiness

### Minimum Counts

No explicit minimums. But each TDD-specific section requires unique IDs (DM-NNN, API-NNN, COMP-NNN, TEST-NNN, MIG-NNN, OPS-NNN) and each item "must appear as a separate ### heading with its ID."

### Key Instructions (verbatim, unique to TDD variant)

- "Preserve exact identifiers from the source document including requirement IDs (FR-xxx, NFR-xxx), interface names, endpoint identifiers, component names, migration phase names, and test case IDs."
- "After the frontmatter, provide the following 14 structured sections"
- For Data Models: "Extract all data entities, TypeScript/code interfaces, field definitions with types/constraints/required status, entity relationships, data-flow steps, and storage/retention/backup strategy from fenced code blocks and markdown tables."
- For API Specifications: "Extract endpoint inventory: HTTP method, URL path, auth requirements, rate limits, query parameters, request body schema, response schema, error codes and responses, versioning strategy, deprecation policy. Extract from endpoint tables and code examples even when no behavioral shall/must language is present."
- For Component Inventory: "Extract route/page tables, shared component tables with props/usage/locations, ASCII component hierarchy trees, state stores with shape/transitions/triggers/side effects."
- For Testing Strategy: "Extract test pyramid breakdown with coverage levels/tooling/targets/ownership, concrete test case tables with test-name/input/expected-output/mocks."
- For Migration: "Preserve sequential ordering as it implies task dependencies."

### Optional Blocks

- **Retrospective:** Same as standard extract.
- **TDD context** (supplementary): Cross-referencing instructions for consistency validation between primary and supplementary TDD.
- **PRD context:** Same as standard extract but references "TDD" instead of "specification."

### Template References

None.

### Granularity Impact: REDUCES (less than standard extract)

**Critical assessment:** This is significantly better than `build_extract_prompt` for TDD inputs. It explicitly asks for field-level extraction ("field definitions with types/constraints/required status"), per-endpoint details ("HTTP method, URL path, auth requirements, rate limits, query parameters, request body schema, response schema, error codes"), and per-component details ("props/usage/locations"). The ID assignment scheme (DM-NNN, API-NNN, etc.) with separate ### headings forces itemized output rather than prose summarization.

**However, still reduces because:**
- Code blocks and tables from the TDD become prose descriptions under ### headings
- The extraction is still a rewrite, not a passthrough -- the LLM must understand and re-express the content
- Relationships between entities (e.g., "UserProfile has a field of type Address[]") may be described narratively rather than preserved as structured schemas
- No instruction to preserve original table formats or code block syntax

---

## 4. build_generate_prompt

**Function signature:** `build_generate_prompt(agent, extraction_path, tdd_file=None, prd_file=None) -> str`
**Step ID:** `generate-{agent.id}` (e.g., `generate-opus-architect`, `generate-haiku-architect`)
**Lines:** 398-506
**Role instruction:** `"You are a {agent.persona} specialist creating a project roadmap."`

### Format Requested

YAML frontmatter with 3 fields:
- `spec_source` (string)
- `complexity_score` (float 0.0-1.0)
- `primary_persona` (string, from agent)

Body: 6 sections:
1. Executive summary
2. Phased implementation plan with milestones
3. Risk assessment and mitigation strategies
4. Resource requirements and dependencies
5. Success criteria and validation approach
6. Timeline estimates per phase

### Minimum Counts

No explicit task count minimums. But with TDD context: "A TDD with 876 lines should produce MORE roadmap task rows than a 312-line spec, not fewer."

### Key Instructions (verbatim)

- "IMPORTANT: Preserve ALL IDs from the extraction document -- requirement IDs (FR-xxx, NFR-xxx) AND entity IDs (DM-xxx, API-xxx, COMP-xxx, TEST-xxx, MIG-xxx, OPS-xxx). Do NOT renumber, relabel, or create new IDs."
- "Each ID must appear as a separate task row in the phased implementation plan."
- "Apply your {agent.persona} perspective throughout: prioritize concerns, risks, and recommendations that a {agent.persona} would emphasize."
- "Use numbered and bulleted lists for actionable items. Be specific and concrete."
- Appends `_INTEGRATION_ENUMERATION_BLOCK` (explicit wiring task enumeration)
- Appends `_OUTPUT_FORMAT_BLOCK`

### Optional Blocks

- **TDD context** (when `tdd_file` provided): This is a critical block.
  - "The TDD is the PRIMARY source of work items for the roadmap"
  - "CRITICAL: Read the TDD directly and create a SEPARATE task table row for EACH independently implementable item"
  - Lists specific item types: each data model/interface AND each field, each API endpoint AND sub-concerns, each UI/service component AND sub-concerns, each test case, each migration phase/feature flag/rollback step, each operational readiness item
  - "Use technical-layer phasing (Foundation -> Core Logic -> Integration -> Hardening -> Production Readiness) regardless of any rollout/milestone structure in the TDD."
  
- **PRD context** (when `prd_file` provided): 4 enrichment instructions for value-based phasing, persona-driven sequencing, compliance gates, scope guardrails. Key: "PRD personas, compliance requirements, and success metrics should appear as ADDITIONAL task rows or acceptance criteria, not as reasons to consolidate existing tasks."

### Template References

None. But references `AgentSpec.persona` from `models.py`.

### Granularity Impact: DESTROYS (without TDD) / REDUCES (with TDD)

**Critical assessment:**

**Without TDD input:** The prompt asks for a "comprehensive project roadmap" with "phased implementation plan" but gives no structural format for the task table. The output is free-form markdown. The LLM is told to preserve IDs and create "separate task rows" but there is no table schema defined, no required columns, no minimum granularity per row. The persona instruction ("prioritize concerns... that a {agent.persona} would emphasize") actively encourages the LLM to filter/consolidate based on its role perspective, which destroys granularity that the other persona might retain.

**With TDD input:** Significantly better. The TDD block explicitly asks for per-field, per-endpoint, per-component task rows and says "A TDD with 876 lines should produce MORE roadmap task rows than a 312-line spec, not fewer." However, the output format is still undefined -- there is no task table schema (columns like Task ID | Phase | Description | Dependencies | Acceptance Criteria) specified in the prompt.

**Key gap:** The prompt never defines a task table format. It says "task rows" and "task table row" but never specifies what columns a row should have. This leaves the LLM to invent its own table structure, which varies between runs and between agent personas.

---

## 5. build_diff_prompt

**Function signature:** `build_diff_prompt(variant_a_path, variant_b_path) -> str`
**Step ID:** `diff`
**Lines:** 509-531
**Role instruction:** "You are a comparative analysis specialist."

### Format Requested

YAML frontmatter with 2 fields:
- `total_diff_points` (integer)
- `shared_assumptions_count` (integer)

Body: 4 sections:
1. Shared assumptions and agreements between variants
2. Numbered list of divergence points (description, which variant takes which position, potential impact)
3. Areas where one variant is clearly stronger
4. Areas requiring debate to resolve

### Minimum Counts

None.

### Key Instructions (verbatim)

- "Be objective. Present both positions fairly without bias."

### Optional Blocks

None. This prompt takes no `tdd_file` or `prd_file` parameters.

### Template References

None.

### Granularity Impact: REDUCES

**Critical assessment:** The diff prompt transforms two full roadmaps into a summary of divergence points. By design, it discards all areas of agreement (only counting them as `shared_assumptions_count`) and focuses on differences. Shared content is not preserved in the output -- it gets a count and a summary, not verbatim preservation. This means any granularity that both variants preserved correctly is reduced to a mention in section 1, while only the divergences get detailed treatment.

---

## 6. build_debate_prompt

**Function signature:** `build_debate_prompt(diff_path, variant_a_path, variant_b_path, depth) -> str`
**Step ID:** `debate`
**Lines:** 534-558
**Role instruction:** "You are a structured debate facilitator."

### Format Requested

YAML frontmatter with 2 fields:
- `convergence_score` (float 0.0-1.0)
- `rounds_completed` (integer)

Body: Full debate transcript with:
- Each round clearly labeled
- Positions attributed to Variant A and Variant B
- Convergence assessment

### Minimum Counts

None. But round count is controlled by `depth` parameter (1/2/3 rounds for quick/standard/deep).

### Key Instructions (verbatim)

- "Ensure each perspective argues its strongest case. Do not artificially force agreement."
- Depth instruction is interpolated from `_DEPTH_INSTRUCTIONS[depth]`.

### Optional Blocks

None. This prompt takes no `tdd_file` or `prd_file` parameters.

### Template References

References `_DEPTH_INSTRUCTIONS` constant.

### Granularity Impact: NEUTRAL (transforms, does not destroy)

**Critical assessment:** The debate prompt doesn't reduce granularity in the same sense as extraction or generation. It takes divergence points and produces argumentative text about them. The original roadmap variants are still available as inputs to downstream steps (merge, score). The debate transcript is an additive artifact -- it creates new analysis rather than summarizing existing content.

---

## 7. build_score_prompt

**Function signature:** `build_score_prompt(debate_path, variant_a_path, variant_b_path, tdd_file=None, prd_file=None) -> str`
**Step ID:** `score`
**Lines:** 561-616
**Role instruction:** "You are an objective evaluation specialist."

### Format Requested

YAML frontmatter with 2 fields:
- `base_variant` (string, identifier of selected base)
- `variant_scores` (string summary, e.g., "A:78 B:72")

Body: 5 sections:
1. Scoring criteria (derived from debate)
2. Per-criterion scores for each variant
3. Overall scores with justification
4. Base variant selection rationale
5. Specific improvements from non-base variant to incorporate in merge

### Minimum Counts

None.

### Key Instructions (verbatim)

- "Be evidence-based. Reference specific debate points and variant content."

### Optional Blocks

- **TDD context:** 3 additional scoring dimensions: technical completeness (data models/APIs/components), testing strategy alignment, migration feasibility.
- **PRD context:** 3 additional scoring dimensions: business value delivery speed, persona coverage, compliance alignment.

### Template References

None.

### Granularity Impact: REDUCES

**Critical assessment:** The score step reduces two full roadmaps and a debate transcript into a selection decision with scores. Section 5 ("specific improvements from the non-base variant to incorporate") is the critical granularity bottleneck -- the merge step relies on this summary to know what to incorporate, but it's free-form prose with no structured format. If the scorer misses an improvement or describes it vaguely, the merge step loses that information.

---

## 8. build_merge_prompt

**Function signature:** `build_merge_prompt(base_selection_path, variant_a_path, variant_b_path, debate_path, tdd_file=None, prd_file=None) -> str`
**Step ID:** `merge`
**Lines:** 619-681
**Role instruction:** "You are a synthesis specialist producing the final merged roadmap."

### Format Requested

YAML frontmatter with 3 fields:
- `spec_source` (string)
- `complexity_score` (float)
- `adversarial: true`

Body: 6 sections (same structure as generate):
1. Executive summary (synthesized from both variants)
2. Phased implementation plan incorporating debate-resolved improvements
3. Risk assessment merging insights from both perspectives
4. Resource requirements
5. Success criteria and validation approach
6. Timeline estimates

### Minimum Counts

None.

### Key Instructions (verbatim)

- "Use the selected base variant as foundation and incorporates the best elements from the other variant as identified in the debate."
- "Use proper heading hierarchy (H2, H3, H4) with no gaps."
- "Ensure all internal cross-references resolve."
- "Do not duplicate heading text at H2 or H3 level."

### Optional Blocks

- **TDD context:** 3 instructions: preserve exact technical identifiers, prefer TDD-matching variant on disagreements, retain all TDD-derived implementation tasks.
- **PRD context:** 4 instructions: maintain persona alignment, preserve success metric targets (no averaging/dropping), prefer stronger compliance gates, use PRD to break ties.

### Template References

None.

### Granularity Impact: PRESERVES-OR-DESTROYS (depends on variant quality)

**Critical assessment:** The merge prompt inherits whatever granularity the base variant has. It does not add its own structural constraints -- no task table schema, no minimum row counts, no ID preservation instructions. This is a significant gap compared to `build_generate_prompt` which at least says "Each ID must appear as a separate task row."

**Missing from merge that exists in generate:**
- No "Preserve ALL IDs" instruction
- No "Each ID must appear as a separate task row" instruction
- No `_INTEGRATION_ENUMERATION_BLOCK` (not appended)
- No explicit granularity floor

The merge prompt trusts that the base variant already has the right granularity and asks the LLM to combine variants. If the LLM simplifies during merge (common behavior), granularity is destroyed with no safeguard.

---

## 9. build_spec_fidelity_prompt

**Function signature:** `build_spec_fidelity_prompt(spec_file, roadmap_path, tdd_file=None, prd_file=None) -> str`
**Step ID:** `spec-fidelity`
**Lines:** 684-792
**Role instruction:** "You are a source-document fidelity analyst."

### Format Requested

YAML frontmatter with 6 fields:
- `high_severity_count` (integer)
- `medium_severity_count` (integer)
- `low_severity_count` (integer)
- `total_deviations` (integer)
- `validation_complete` (boolean)
- `tasklist_ready` (boolean, true only if `high_severity_count == 0` AND `validation_complete == true`)

Body: 2 sections:
1. Deviation Report -- numbered entries with ID (DEV-NNN), severity, deviation description, source quote, roadmap quote (or [MISSING]), impact, recommended correction
2. Summary

### Minimum Counts

None.

### Key Instructions (verbatim)

- Severity definitions with precise criteria (HIGH/MEDIUM/LOW) -- RSK-007 mitigation
- 6 comparison dimensions (base): Signatures, Data Models, Gates, CLI Options, NFRs, Integration Wiring Completeness
- With TDD: 5 additional dimensions (7-11): API Endpoints, Component Inventory, Testing Strategy, Migration & Rollout, Operational Readiness
- With PRD: 4 additional dimensions (12-15): Persona Coverage, Business Metric Traceability, Compliance & Legal Coverage, Scope Boundary Enforcement
- "Quote both documents for every deviation."
- "Do not invent deviations -- only report genuine differences."

### Template References

Uses `_INTEGRATION_WIRING_DIMENSION` constant as dimension #6.

### Granularity Impact: MEASURES (does not transform)

**Critical assessment:** This is a validation/audit step, not a transformation. It compares the spec against the roadmap and reports deviations. It does not transform data -- it produces a quality report. The `tasklist_ready` flag is the gate that determines whether downstream steps proceed.

**However**, the quality of its measurement depends on whether the comparison dimensions match what the spec actually contains. If a spec has 200 field-level definitions but the fidelity check only looks at "Data Models" at the entity level, field-level losses go undetected.

---

## 10. build_wiring_verification_prompt

**Function signature:** `build_wiring_verification_prompt(merge_file, spec_source) -> str`
**Step ID:** `wiring-verification`
**Lines:** 795-850
**Role instruction:** "You are a static wiring verification analyst."

### Format Requested

YAML frontmatter with 15 fields:
- `gate: wiring-verification`
- `target_dir`, `files_analyzed`, `files_skipped`
- `rollout_mode: shadow`
- `analysis_complete: true`
- `audit_artifacts_used: 0`
- `unwired_callable_count`, `orphan_module_count`, `unwired_registry_count`
- `critical_count`, `major_count`, `info_count`
- `total_findings`, `blocking_findings`
- `whitelist_entries_applied`

Body: 7 sections:
1. Summary of analysis scope and findings
2. Unwired Optional Callable Injections
3. Orphan Modules / Symbols
4. Unregistered Dispatch Entries
5. Suppressions and Dynamic Retention notes
6. Recommended Remediation actions
7. Evidence and Limitations

### Minimum Counts

None.

### Key Instructions (verbatim)

- Checks for 3 defect classes: G-001 (unwired Optional[Callable]), G-002 (orphan modules), G-003 (unregistered dispatch entries)
- "In shadow mode, report all findings but do not block the pipeline."

### Optional Blocks

None. No `tdd_file` or `prd_file` parameters.

### Template References

None.

### Granularity Impact: NEUTRAL (validation step)

**Critical assessment:** This is a code-quality audit step that operates on the merged roadmap's described architecture. It does not transform data. It operates in "shadow" mode -- it reports but does not block. This prompt is notable for being the most structurally detailed in terms of frontmatter fields (15 fields), but it has the least impact on the data pipeline since it runs in shadow mode.

**Anomaly:** This prompt appears to ask for static analysis of actual code ("codebase described in the roadmap") but the roadmap is a planning document, not code. The prompt's 3 defect classes (Optional[Callable] wiring, orphan modules, unregistered dispatch entries) are code-level concerns being analyzed from a roadmap document. This may produce unreliable results since the LLM is inferring code structure from planning text.

---

## 11. build_test_strategy_prompt

**Function signature:** `build_test_strategy_prompt(roadmap_path, extraction_path, tdd_file=None, prd_file=None) -> str`
**Step ID:** `test-strategy`
**Lines:** 853-942
**Role instruction:** "You are a test strategy specialist."

### Format Requested

YAML frontmatter with 6 fields:
- `complexity_class` (LOW/MEDIUM/HIGH)
- `validation_philosophy` (must be exactly `"continuous-parallel"`)
- `validation_milestones` (integer, count of M# or Phase headings)
- `work_milestones` (integer, count of M# or Phase headings)
- `interleave_ratio` (string, derived from complexity: LOW=1:3, MEDIUM=1:2, HIGH=1:1)
- `major_issue_policy` (must be exactly `"stop-and-fix"`)

Body: 6 sections:
1. Validation milestones mapped to roadmap phases
2. Test categories (unit, integration, E2E, acceptance)
3. Test-implementation interleaving strategy with ratio justification
4. Risk-based test prioritization
5. Acceptance criteria per milestone
6. Quality gates between phases

Also includes an Issue Classification table (CRITICAL/MAJOR/MINOR/COSMETIC with actions and gate impacts).

### Minimum Counts

None explicit. But the `interleave_ratio` formula implies a minimum relationship between validation and work milestones.

### Key Instructions (verbatim)

- "Be specific about what to test at each milestone."
- Issue classification table is embedded in the prompt.
- `validation_philosophy` and `major_issue_policy` are hardcoded strings.

### Optional Blocks

- **TDD context:** 6 enrichment instructions: test pyramid alignment, named test cases, API contract tests, data model validation, migration rollback tests, operational readiness tests. Key: "Preserve exact test case IDs and names from the TDD."
- **PRD context:** 5 enrichment instructions: persona-based acceptance tests, customer journey E2E tests, KPI validation tests, compliance test category, edge case coverage.

### Template References

None.

### Granularity Impact: PRESERVES (when TDD provided) / NEUTRAL (without)

**Critical assessment:** This prompt does not transform data from the pipeline -- it generates a new derivative artifact (test strategy) from the roadmap and extraction. The test strategy is additive content. With TDD context, it's instructed to preserve exact test case IDs and names, which is good for traceability.

---

## 12. Per-Prompt Summary Table

| # | Function Name | Step ID | Format Requested | Granularity Impact | Template Used | Minimum Counts | Key Output Fields |
|---|--------------|---------|------------------|-------------------|---------------|----------------|-------------------|
| 1 | `build_extract_prompt` | extract | YAML FM (13 fields) + 8 sections | **REDUCES** -- lossy summarization of spec into prose | None | None | FR/NFR counts, complexity, domains, risks |
| 2 | `build_extract_prompt_tdd` | extract (TDD) | YAML FM (19 fields) + 14 sections | **REDUCES** (less loss) -- per-item ID assignment preserves structure | None | None, but requires ### per item | DM/API/COMP/TEST/MIG/OPS counts + all standard |
| 3 | `build_generate_prompt` | generate-{id} | YAML FM (3 fields) + 6 sections | **DESTROYS** (no TDD) / **REDUCES** (with TDD) -- no task table schema | None (uses AgentSpec) | "MORE rows than spec lines" (TDD only) | spec_source, complexity_score, primary_persona |
| 4 | `build_diff_prompt` | diff | YAML FM (2 fields) + 4 sections | **REDUCES** -- discards agreed content, summarizes divergences | None | None | total_diff_points, shared_assumptions_count |
| 5 | `build_debate_prompt` | debate | YAML FM (2 fields) + transcript | **NEUTRAL** -- additive analysis, not summarization | _DEPTH_INSTRUCTIONS | Round count by depth | convergence_score, rounds_completed |
| 6 | `build_score_prompt` | score | YAML FM (2 fields) + 5 sections | **REDUCES** -- collapses variants into selection + improvement list | None | None | base_variant, variant_scores |
| 7 | `build_merge_prompt` | merge | YAML FM (3 fields) + 6 sections | **PRESERVES-OR-DESTROYS** -- no ID preservation instruction | None | None | spec_source, complexity_score, adversarial |
| 8 | `build_spec_fidelity_prompt` | spec-fidelity | YAML FM (6 fields) + deviation report | **MEASURES** -- validation, not transformation | _INTEGRATION_WIRING_DIMENSION | None | severity counts, tasklist_ready |
| 9 | `build_wiring_verification_prompt` | wiring-verification | YAML FM (15 fields) + 7 sections | **NEUTRAL** -- shadow-mode audit | None | None | finding counts, blocking_findings |
| 10 | `build_test_strategy_prompt` | test-strategy | YAML FM (6 fields) + 6 sections + table | **PRESERVES** (TDD) / **NEUTRAL** (no TDD) -- derivative artifact | None | Interleave ratio by complexity | complexity_class, interleave_ratio, major_issue_policy |

---

## 13. Gaps and Questions

### Critical Gaps

1. **No task table schema anywhere.** `build_generate_prompt` says "task rows" and "task table row" but never defines columns. `build_merge_prompt` doesn't even mention task rows. This means task granularity and structure is entirely LLM-invented and varies per run.

2. **Merge prompt lacks ID preservation.** `build_generate_prompt` explicitly says "Preserve ALL IDs... Do NOT renumber." `build_merge_prompt` has no such instruction. The merge step can silently consolidate or drop IDs.

3. **Merge prompt lacks `_INTEGRATION_ENUMERATION_BLOCK`.** The generate prompt appends it, but the merge prompt does not. Wiring tasks enumerated during generation can be lost during merge.

4. **No granularity floor in any prompt.** No prompt says "the output must contain at least N task rows" or "the output must have at least as many items as the extraction." The only approximation is the TDD block in `build_generate_prompt` which says "MORE roadmap task rows than a 312-line spec, not fewer" -- but this is a relative guidance, not a count-based floor.

5. **Extraction is lossy for structured data.** Neither extract prompt instructs the LLM to preserve tables, code blocks, or schema definitions in their original format. Field-level detail (types, constraints, defaults) may be collapsed into entity-level summaries.

6. **Diff discards agreements.** The diff step only counts shared assumptions, it does not preserve them in detail. If both variants correctly preserved a requirement with identical granularity, that correct preservation is not reinforced -- it just gets a count.

### Questions

1. Should `build_merge_prompt` append `_INTEGRATION_ENUMERATION_BLOCK` like `build_generate_prompt` does?
2. Should `build_merge_prompt` include an explicit "Preserve ALL IDs" instruction matching `build_generate_prompt`?
3. Should there be a defined task table schema (columns, required fields) that both generate and merge prompts enforce?
4. Should extract prompts instruct the LLM to preserve original table/code-block formats rather than rewriting into prose?
5. Is `build_wiring_verification_prompt` producing useful output? It asks for code-level static analysis from a planning document.
6. Should `build_diff_prompt` and `build_debate_prompt` accept `tdd_file`/`prd_file` parameters for enriched comparison, or is their current scope intentional?

---

## 14. Stale Documentation Found

1. **Wiring verification prompt hardcodes `rollout_mode: shadow` and `audit_artifacts_used: 0`** -- these appear to be development-time defaults that should be parameterized or removed if the feature is production-ready.

2. **TDD section references use hardcoded section numbers** (e.g., "the TDD's Data Models section (S7)", "the TDD's Testing Strategy section (S15)"). These assume a specific TDD template structure. If the TDD template changes section numbering, these references become stale.

3. **PRD section references use hardcoded section numbers** (e.g., "S7", "S12", "S17", "S19", "S22", "S23"). Same staleness risk as TDD references.

---

## 15. Summary

The prompts.py file contains 10 prompt-building functions and 4 shared constants. The file is 942 lines of pure Python string construction with no external template files.

**Architecture pattern:** Each function returns a string that becomes the `-p` argument to `claude`. File inputs are embedded inline into the prompt by `_embed_inputs()` in executor.py (the `--file` flag is explicitly avoided per code comments at executor.py:719-721). All functions append `_OUTPUT_FORMAT_BLOCK` to enforce YAML frontmatter.

**Granularity flow through the pipeline:**

```
Spec/TDD (maximum granularity)
  |
  v
Extract (REDUCES: summarizes into sections, assigns IDs)
  |
  v
Generate x2 (REDUCES/DESTROYS: creates roadmap with undefined task table format)
  |
  v
Diff (REDUCES: discards agreements, focuses on divergences)
  |
  v
Debate (NEUTRAL: additive analysis)
  |
  v
Score (REDUCES: collapses to selection decision)
  |
  v
Merge (PRESERVES-OR-DESTROYS: no structural guardrails)
  |
  v
Spec Fidelity (MEASURES: catches some losses, but only at dimension level)
  |
  v
Wiring Verification (NEUTRAL: shadow audit)
  |
  v
Test Strategy (PRESERVES/NEUTRAL: derivative artifact)
```

**The three most impactful granularity bottlenecks are:**

1. **Extract step** -- first lossy transformation. Tables and code blocks become prose.
2. **Generate step** -- no task table schema. Output structure is LLM-invented.
3. **Merge step** -- missing ID preservation, missing integration enumeration block, no granularity floor. This is the most dangerous bottleneck because it operates on already-reduced data and has fewer safeguards than the generate step.
