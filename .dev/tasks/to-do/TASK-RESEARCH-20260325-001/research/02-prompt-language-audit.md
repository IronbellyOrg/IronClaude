# Research: Prompt Language Audit

**Investigation type:** Code Tracer
**Scope:** src/superclaude/cli/roadmap/prompts.py
**Status:** Complete
**Date:** 2026-03-25

---

## File Overview

Prompt builders in `src/superclaude/cli/roadmap/prompts.py`:
- `build_extract_prompt(spec_file, retrospective_content=None)`
- `build_generate_prompt(agent, extraction_path)`
- `build_diff_prompt(variant_a_path, variant_b_path)`
- `build_debate_prompt(diff_path, variant_a_path, variant_b_path, depth)`
- `build_score_prompt(debate_path, variant_a_path, variant_b_path)`
- `build_merge_prompt(base_selection_path, variant_a_path, variant_b_path, debate_path)`
- `build_spec_fidelity_prompt(spec_file, roadmap_path)`
- `build_wiring_verification_prompt(merge_file, spec_source)`
- `build_test_strategy_prompt(roadmap_path, extraction_path)`

**No `build_anti_instinct_prompt()` exists.** Anti-instinct is fully programmatic.

---

## `build_extract_prompt()`

**Parameters:** `spec_file: Path`, `retrospective_content: str | None = None`

### Exact 8 body sections
1. `## Functional Requirements`
2. `## Non-Functional Requirements`
3. `## Complexity Assessment`
4. `## Architectural Constraints`
5. `## Risk Inventory`
6. `## Dependency Inventory`
7. `## Success Criteria`
8. `## Open Questions`

### Spec-specific language and assumptions
1. "Read the provided specification file" — explicit spec framing
2. "requirements extraction specialist" / "requirements extraction document" — spec-centric role
3. FR/NFR-centric identifier instructions: "Use the spec's exact requirement identifiers verbatim... FR-EVAL-001.1, FR-EVAL-001.1a/b"
4. Frontmatter fields oriented around requirement counting: `functional_requirements`, `nonfunctional_requirements`, `total_requirements`, `success_criteria_count`
5. "Extract every requirement, even implicit ones" — spec-adequate but insufficient for TDD structural content

### TDD sections absent from extraction body
These TDD sections are NOT represented as dedicated extraction targets:
- §7 Data Models (TypeScript interfaces, field tables, flowcharts, storage tables)
- §8 API Specifications (endpoint tables, request/response schemas, error tables, versioning policy)
- §9 State Management (state tool tables, TypeScript state interfaces, transition tables)
- §10 Component Inventory (route tables, component tables, ASCII hierarchy trees)
- §15 Testing Strategy (test pyramid tables, unit/integration/E2E case tables)
- §19 Migration & Rollout Plan (phase tables, feature flag tables, rollback procedures)
- §25 Operational Readiness (runbook scenario tables, on-call tables, capacity tables)
- §26 Cost & Resource Estimation
- §28 Glossary

### Exact text that must change for TDD input

**Change 1: Source framing (Critical)**
- Old: "Read the provided specification file" / "requirements extraction specialist"
- New: "Read the provided specification or technical design document" / "requirements and design extraction specialist"

**Change 2: Broaden extraction mandate (Critical)**
- Old: 8 sections targeting FR/NFR/constraints/risks/dependencies/success criteria/open questions
- New: Add dedicated sections: `## Data Models and Interfaces`, `## API Specifications`, `## Component Inventory`, `## Testing Strategy`, `## Migration and Rollout Plan`, `## Operational Readiness`

**Change 3: Identifier language (High)**
- Old: "Use the spec's exact requirement identifiers verbatim" with FR/NFR examples
- New: "Preserve exact identifiers from the source document including requirement IDs, interface names, endpoint identifiers, component names, migration phases, and test case IDs"

**Change 4: Frontmatter schema (Medium)**
- Old: 13 requirement-centric fields
- New: Add optional fields: `data_models_identified`, `api_surfaces_identified`, `components_identified`, `test_artifacts_identified`, `migration_items_identified`, `operational_items_identified`

### Severity: **CRITICAL** — single chokepoint; downstream steps only see extraction output

---

## `build_spec_fidelity_prompt()`

**Parameters:** `spec_file: Path`, `roadmap_path: Path`

### Spec-specific language
1. "You are a specification fidelity analyst" — explicit spec framing
2. "Read the provided specification file" / "diverges from or omits requirements in the specification"
3. Example identifiers: `(FR-NNN)`, `(NFR-NNN)`, `(SC-NNN)`
4. "spec's priority ordering"

### What must change for TDD
1. Role: "specification fidelity analyst" → "source-document fidelity analyst"
2. Input label: "specification file" → "source specification or TDD file"
3. Broaden omission language beyond "requirements in the specification" to also cover design decisions, data contracts, interface definitions, endpoints, component responsibilities, migration/rollback procedures, operational procedures, test strategy commitments
4. Expand comparison dimensions to include: API endpoints/request-response contracts, component/module inventory, testing strategy/validation matrix, migration/rollout/rollback, operational readiness/runbooks/alerts

**Note:** This prompt is partially compatible already — it receives spec_file directly and includes some TDD-relevant dimensions like Signatures and Data Models. Still biased toward classic spec/FR/NFR/SC language.

### Severity: **HIGH**

---

## `build_wiring_verification_prompt()`

**Parameters:** `merge_file: Path`, `spec_source: str`

### Spec-specific content
None. The prompt body analyzes code-structural wiring (unwired callables, orphan modules, unregistered dispatch entries) — not source document comparison. `spec_source` is provenance naming only.

### TDD change required: **NONE**
### Severity: **LOW**

---

## `build_generate_prompt()`

**Parameters:** `agent: AgentSpec`, `extraction_path: Path`

Receives **only the extraction document** — the spec_file chokepoint.

### Extraction frontmatter fields referenced by name
- `spec_source`, `generated`, `generator` (provenance)
- `functional_requirements`, `nonfunctional_requirements`, `total_requirements` (scope counts)
- `complexity_score`, `complexity_class` (complexity)
- `domains_detected` (domain list)
- `risks_identified`, `dependencies_identified`, `success_criteria_count`

Required output frontmatter: `spec_source`, `complexity_score`, `primary_persona`

### TDD change required
1. If extraction schema adds TDD-specific count fields (`data_models_identified`, etc.), update referenced fields to include them
2. Add instructions to explicitly plan roadmap sections around TDD-derived artifacts: data model implementation, API implementation, component wiring, test implementation, migration/rollback, operational readiness

### Severity: **HIGH** (inherits extraction chokepoint)

---

## `build_test_strategy_prompt()`

**Parameters:** `roadmap_path: Path`, `extraction_path: Path`

Does not read original spec/TDD directly. Focuses on validation milestones, interleave ratios, and quality gates.

### TDD change required
Strengthen to explicitly derive tests from TDD artifacts if present: API contracts, data models, component interfaces, migration validation, rollback validation, operational readiness validation. Otherwise it produces a generic roadmap-based testing plan.

### Severity: **MEDIUM**

---

## `build_diff_prompt()`, `build_debate_prompt()`, `build_score_prompt()`

**No spec-specific content.** All compare roadmap variants only.

### TDD change required: **NONE**
### Severity: **LOW**

---

## `build_merge_prompt()`

**Parameters:** `base_selection_path`, `variant_a_path`, `variant_b_path`, `debate_path`

Mild provenance coupling via required output frontmatter: `spec_source`, `complexity_score`, `adversarial: true`.

### TDD change required
Optional strengthening to explicitly preserve TDD artifact categories (data model tasks, API tasks, component inventory/wiring tasks, testing strategy tasks, migration/rollback tasks, operational readiness tasks) in merged roadmap.

### Severity: **MEDIUM-LOW**

---

## Summary Table

| Prompt Builder | Parameters | Spec-Specific Language Found | TDD Change Required | Severity |
|---|---|---|---|---|
| `build_extract_prompt` | `spec_file`, `retrospective_content` | Strong: "specification file", FR/NFR-centric IDs, 8 sections miss TDD-specific design areas | Major: neutralize framing; add sections for data models, APIs, components, testing, migration, ops; broaden frontmatter | Critical |
| `build_generate_prompt` | `agent`, `extraction_path` | Indirect: references spec-shaped extraction fields | Update to consume expanded TDD-aware extraction schema; explicitly roadmap TDD-derived artifacts | High |
| `build_spec_fidelity_prompt` | `spec_file`, `roadmap_path` | Strong: "specification fidelity analyst", FR/NFR/SC examples, spec-priority language | Generalize to source-doc/TDD comparison; add dimensions for APIs, components, migration, ops, testing | High |
| `build_test_strategy_prompt` | `roadmap_path`, `extraction_path` | Indirect through extraction | Strengthen to derive tests from TDD artifacts | Medium |
| `build_merge_prompt` | multiple | Mild: `spec_source` provenance | Optional: preserve TDD artifact categories | Medium-Low |
| `build_diff_prompt` | `variant_a_path`, `variant_b_path` | None | None | Low |
| `build_debate_prompt` | `diff_path`, variants, `depth` | None | None | Low |
| `build_score_prompt` | `debate_path`, variants | None | None | Low |
| `build_wiring_verification_prompt` | `merge_file`, `spec_source` | None | None | Low |
| `build_anti_instinct_prompt` | N/A (does not exist) | N/A | N/A | N/A |

---

## Gaps and Questions

- If extraction frontmatter schema changes, all downstream prompt builders and validators that assume current key names will also need updating
- `spec_source` naming: acceptable as provenance even for TDD, but semantically inaccurate; decide whether to preserve for backward compatibility
- Test-strategy prompt is not source-document aware — even after extract changes, may still underrepresent TDD-specific validation unless explicitly instructed

## Summary

`build_extract_prompt()` is the single highest-risk prompt for TDD support. It hardcodes spec-centric language throughout and instructs only 8 body sections that omit 8+ major TDD content areas. Since `build_generate_prompt()` receives ONLY extraction output, any TDD content not surfaced by extract is unrecoverable downstream. `build_spec_fidelity_prompt()` is the next most spec-bound and needs generalization for TDD coverage dimensions. All other builders are mostly spec-neutral and require minimal or no changes.
