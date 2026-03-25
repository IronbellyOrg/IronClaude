# Technical Research Report — CLI TDD Integration
## Synthesis Document 02: Target State and Gap Analysis

**Research Question:** What must change in the CLI Python layer to support `superclaude roadmap run <tdd_file>`?
**Source Files:** research/01 through research/06, gaps-and-questions.md
**Date:** 2026-03-25
**Status:** Draft

---

## §3 Target State

### 3.1 Desired Behavior

When a user runs `superclaude roadmap run <tdd_file>` (with `--input-type tdd` or equivalent auto-detection), the pipeline must produce a roadmap that captures structured content from all high-value TDD sections. Specifically the pipeline must surface TDD §7 Data Models, §8 API Specifications, §10 Component Inventory, §14 Observability and Monitoring, §15 Testing Strategy, §19 Migration and Rollout Plan, §24 Release Criteria, and §25 Operational Readiness as distinct extraction artifacts that downstream steps (`generate`, `merge`, `test-strategy`, `spec-fidelity`) can act on.

The spec input path (`superclaude roadmap run <spec_file>`) must continue to work unchanged. All new fields and flags must carry defaults that preserve existing behavior when omitted.

### 3.2 Success Criteria

Derived from research findings across all six investigation files:

| # | Success Criterion | Research Source |
|---|---|---|
| SC-1 | TDD sections captured by extraction rises from 5 CAPTURED to 28 captured (all sections have at least partial extraction instruction) | 06-tdd-template-structure.md §Counts table |
| SC-2 | `build_extract_prompt()` emits at minimum 14 body sections: the existing 8 plus dedicated sections for Data Models and Interfaces, API Specifications, State Management, Component Inventory, Testing Strategy, and Operational Readiness | 02-prompt-language-audit.md §Change 2; 06-tdd-template-structure.md §MISSED entries |
| SC-3 | The 8 MISSED TDD sections (§7, §8, §9, §10, §15, §25, §26, §28) have explicit extraction targets in the TDD prompt variant | 06-tdd-template-structure.md §MISSED rows |
| SC-4 | DEVIATION_ANALYSIS_GATE is redesigned to replace `routing_update_spec` with `routing_update_source` and to support TDD-derived deviation taxonomy; the pre-existing `ambiguous_count` / `ambiguous_deviations` field-name mismatch is resolved as part of this change | 04-gate-compatibility.md §DEVIATION_ANALYSIS_GATE; gaps-and-questions.md §Pre-Existing Codebase Bug |
| SC-5 | `spec_source` in EXTRACT_GATE, GENERATE_A_GATE, GENERATE_B_GATE, MERGE_GATE, and TEST_STRATEGY_GATE is aliased or renamed to `source_document` with backward-compatible fallback | 04-gate-compatibility.md §Summary Table |
| SC-6 | `RoadmapConfig` carries `input_type: Literal["spec", "tdd"] = "spec"` and `tdd_file: Path | None = None`; `TasklistValidateConfig` carries `tdd_file: Path | None = None` | 05-cli-entry-points.md §Fields needed for TDD support |
| SC-7 | `superclaude roadmap run` accepts `--input-type [spec|tdd]` option (default `spec`); `superclaude tasklist validate` accepts optional `--tdd-file <path>` | 05-cli-entry-points.md §Where `--input-type` would be added |
| SC-8 | `build_spec_fidelity_prompt()` is generalized from "specification fidelity analyst" to "source-document fidelity analyst" with expanded comparison dimensions covering API contracts, component inventory, testing strategy, migration/rollout, and operational readiness | 02-prompt-language-audit.md §build_spec_fidelity_prompt() |
| SC-9 | The extract step's identifier language is broadened from FR/NFR examples to preserve interface names, endpoint identifiers, component names, migration phases, and test case IDs | 02-prompt-language-audit.md §Change 3 |
| SC-10 | SPEC_FIDELITY_GATE is renamed to SOURCE_FIDELITY_GATE (or a TDD-specific parallel gate is introduced) | 04-gate-compatibility.md §SPEC_FIDELITY_GATE |
| SC-11 | `fidelity_checker.py` Python-only evidence scan limitation is documented and a non-blocking scope note is added for TypeScript-implemented TDD requirements | 03-pure-python-modules.md §fidelity_checker.py §TDD risks |
| SC-12 | TDD frontmatter `type: "📐 Technical Design Document"` is readable by the pipeline as an auto-detection signal (either via `--input-type` or executor frontmatter inspection) | 06-tdd-template-structure.md §(c) TDD Frontmatter `type` Field |

### 3.3 Constraints

| Constraint | Basis |
|---|---|
| Backward compatibility required — spec inputs must continue to work unchanged | All new RoadmapConfig fields must default to `"spec"` / `None`; all new Click options must default to preserve current behavior. Confirmed pattern: `convergence_enabled: bool = False`, `allow_regeneration: bool = False` (05-cli-entry-points.md §Existing backward-compatible extension pattern) |
| `build_extract_prompt()` change is the single highest-risk edit in the pipeline | Extract is the chokepoint — `generate-*`, `diff`, `debate`, `score`, `merge` all receive only extraction output and have no spec_file access (01-executor-data-flow.md §Summary; 02-prompt-language-audit.md §Severity: CRITICAL) |
| Gate enforcement engine (`gate_passed()`) must not be modified | It is format-agnostic; incompatibilities live entirely in per-gate field lists and semantic checks (04-gate-compatibility.md §Pipeline Gate Engine) |
| `obligation_scanner.py` scans roadmap text only and is unaffected by input format | No change required (03-pure-python-modules.md §obligation_scanner.py §TDD compatibility: N/A) |
| `semantic_layer.py` (~400 lines) and `structural_checkers.py` (~200 lines) involvement in spec processing is unverified and must be treated as Unknown | Implementation work must not assume these modules are inert without further investigation (gaps-and-questions.md §C-1, C-2) |

---

## §4 Gap Analysis

The table below covers all identified gaps. Severity is graded as: **Critical** = blocks TDD support entirely; **High** = produces wrong or incomplete output; **Medium** = reduces fidelity; **Low** = minor or optional improvement.

### 4.1 Prompt Language Gaps

| Gap | Current State | Target State | Severity | Files to Change |
|---|---|---|---|---|
| `build_extract_prompt()` source framing | "Read the provided specification file" / "requirements extraction specialist" — hardcoded spec identity | "Read the provided specification or technical design document" / "requirements and design extraction specialist" | Critical | `src/superclaude/cli/roadmap/prompts.py` |
| `build_extract_prompt()` body section coverage | 8 sections covering FR, NFR, Complexity, Architectural Constraints, Risk, Dependency, Success Criteria, Open Questions — omits all TDD-specific structural areas | Add 6+ dedicated sections: Data Models and Interfaces, API Specifications, State Management, Component Inventory, Testing Strategy, Migration and Rollout Plan, Operational Readiness | Critical | `src/superclaude/cli/roadmap/prompts.py` |
| `build_extract_prompt()` identifier language | "Use the spec's exact requirement identifiers verbatim" with FR/NFR examples only | Broaden to: "Preserve exact identifiers including requirement IDs, interface names, endpoint identifiers, component names, migration phases, and test case IDs" | High | `src/superclaude/cli/roadmap/prompts.py` |
| `build_extract_prompt()` frontmatter schema | 13 requirement-centric fields (`functional_requirements`, `nonfunctional_requirements`, etc.) | Add optional TDD fields: `data_models_identified`, `api_surfaces_identified`, `components_identified`, `test_artifacts_identified`, `migration_items_identified`, `operational_items_identified` | Medium | `src/superclaude/cli/roadmap/prompts.py` |
| `build_spec_fidelity_prompt()` role and input framing | "You are a specification fidelity analyst" / "specification file" / identifiers styled as `(FR-NNN)`, `(NFR-NNN)`, `(SC-NNN)` | "source-document fidelity analyst" / "source specification or TDD file"; expand comparison dimensions to include API contracts, component inventory, testing strategy, migration/rollout, operational procedures | High | `src/superclaude/cli/roadmap/prompts.py` |
| `build_generate_prompt()` TDD artifact planning | Instructions do not explicitly plan roadmap sections around TDD-derived artifacts; only references spec-shaped extraction fields | Add instructions to plan roadmap sections around TDD artifacts: data model implementation, API implementation, component wiring, test implementation, migration/rollback, operational readiness | High | `src/superclaude/cli/roadmap/prompts.py` |
| `build_test_strategy_prompt()` TDD derivation | Does not read original spec/TDD; produces generic roadmap-based validation plan | Strengthen to explicitly derive tests from TDD artifacts when present: API contracts, data models, component interfaces, migration validation, rollback validation, operational readiness validation | Medium | `src/superclaude/cli/roadmap/prompts.py` |
| `build_merge_prompt()` TDD artifact preservation | No explicit instruction to preserve TDD artifact categories in merged roadmap | Add optional instruction to preserve data model tasks, API tasks, component inventory/wiring tasks, testing strategy tasks, migration/rollback tasks, operational readiness tasks | Medium-Low | `src/superclaude/cli/roadmap/prompts.py` |

### 4.2 Gate Schema Gaps

| Gap | Current State | Target State | Severity | Files to Change |
|---|---|---|---|---|
| `spec_source` field in EXTRACT_GATE | Required field named `spec_source`; spec-specific semantics | Alias or rename to `source_document`; maintain backward compatibility for existing `spec_source` outputs | High | `src/superclaude/cli/roadmap/gates.py` |
| `spec_source` field in GENERATE_A_GATE | Required field `spec_source` | Alias or rename to `source_document` | High | `src/superclaude/cli/roadmap/gates.py` |
| `spec_source` field in GENERATE_B_GATE | Required field `spec_source` | Alias or rename to `source_document` | High | `src/superclaude/cli/roadmap/gates.py` |
| `spec_source` field in MERGE_GATE | Required field `spec_source` | Alias or rename to `source_document` | High | `src/superclaude/cli/roadmap/gates.py` |
| `spec_source` field in TEST_STRATEGY_GATE | Required field `spec_source` | Alias or rename to `source_document` | High | `src/superclaude/cli/roadmap/gates.py` |
| DEVIATION_ANALYSIS_GATE `routing_update_spec` field | Field explicitly requires update to the spec document as the remediation target; structurally incompatible with TDD inputs | Replace with `routing_update_source` or support both field names | Critical | `src/superclaude/cli/roadmap/gates.py` |
| DEVIATION_ANALYSIS_GATE `DEV-\d+` routing ID namespace | Deviation IDs hardcoded to `DEV-\d+` pattern; assumes spec-deviation tracking taxonomy | Clarify whether TDD-derived deviations use same namespace; adjust pattern or make configurable | High | `src/superclaude/cli/roadmap/gates.py` |
| DEVIATION_ANALYSIS_GATE `ambiguous_count` / `ambiguous_deviations` field-name mismatch | Required frontmatter field is `ambiguous_count`; semantic check `_no_ambiguous_deviations` reads `ambiguous_deviations` — pre-existing bug; gate may silently pass when `ambiguous_deviations` is absent | Unify to a single canonical field name across the required-fields list and the semantic check | High | `src/superclaude/cli/roadmap/gates.py` |
| DEVIATION_ANALYSIS_GATE slip/intentional/pre-approved taxonomy | Assumes spec document as remediation target throughout deviation routing model | Determine whether taxonomy applies to TDD deviations; generalize language from spec-specific to source-document remediation | High | `src/superclaude/cli/roadmap/gates.py` |
| SPEC_FIDELITY_GATE naming | Gate named `SPEC_FIDELITY_GATE`; semantically incorrect for TDD fidelity checking | Rename to `SOURCE_FIDELITY_GATE` or add parallel `TDD_FIDELITY_GATE`; semantic check logic can remain unchanged | Medium | `src/superclaude/cli/roadmap/gates.py` |
| ANTI_INSTINCT_GATE failure messages | `fingerprint_coverage` failure message reads "spec code-level identifiers insufficiently represented in roadmap" | Generalize to "source-document code-level identifiers" | Low | `src/superclaude/cli/roadmap/gates.py` |
| CERTIFY_GATE `F-\d+` row check | `_has_per_finding_table` hardcodes `F-\d+` row pattern | Relax regex to accept broader finding ID patterns if TDD mode uses different IDs | Low | `src/superclaude/cli/pipeline/gates.py` |

### 4.3 CLI Flag and Invocation Gaps

| Gap | Current State | Target State | Severity | Files to Change |
|---|---|---|---|---|
| No `--input-type` flag on `superclaude roadmap run` | Command positional argument named `spec_file`; docstring reads "SPEC_FILE is the path to a specification markdown file"; no mechanism to signal TDD input | Add `--input-type [spec\|tdd]` option (default `spec`) using `click.Choice` | Critical | `src/superclaude/cli/roadmap/commands.py` |
| No `--tdd-file` flag on `superclaude tasklist validate` | No `--spec` or `--tdd-file` option exists; validate executor is entirely artifact-based and cannot reference original TDD | Add `--tdd-file <path>` optional option | High | `src/superclaude/cli/tasklist/commands.py` |
| `spec_file` positional name semantically incorrect for TDD inputs | CLI argument named `spec_file` when `--input-type tdd` is used creates confusing UX | Consider renaming positional to `input_file`; not required for initial functional support | Low | `src/superclaude/cli/roadmap/commands.py` |

### 4.4 Data Model Gaps

| Gap | Current State | Target State | Severity | Files to Change |
|---|---|---|---|---|
| `RoadmapConfig` has no `input_type` field | No field to propagate input type through executor pipeline | Add `input_type: Literal["spec", "tdd"] = "spec"` following established backward-compatible defaulted-field pattern (same as `convergence_enabled`, `allow_regeneration`) | Critical | `src/superclaude/cli/roadmap/models.py` |
| `RoadmapConfig` has no `tdd_file` field | No field to carry resolved TDD file path | Add `tdd_file: Path \| None = None` | High | `src/superclaude/cli/roadmap/models.py` |
| `TasklistValidateConfig` has no `tdd_file` field | No way for tasklist validate to reference TDD source as an additional validation input | Add `tdd_file: Path \| None = None` | High | `src/superclaude/cli/tasklist/models.py` |
| `executor.py` does not consume `input_type` or `tdd_file` | New dataclass fields are available once added to `RoadmapConfig` but executor has no conditional logic to branch on them | Add branching in `_build_steps()` and prompt-builder calls to select TDD variants when `config.input_type == "tdd"` | Critical | `src/superclaude/cli/roadmap/executor.py` |

### 4.5 Pure Python Module Gaps

| Gap | Current State | Target State | Severity | Files to Change |
|---|---|---|---|---|
| `fidelity_checker.py` Python-only evidence scan | Scans `.py` files only via AST + regex fallback; TypeScript-implemented TDD requirements produce blind spots; TypeScript interface names produce ambiguous fail-open matches | Add explicit scope documentation; optionally extend to scan TypeScript source files for name evidence | High | `src/superclaude/cli/roadmap/fidelity_checker.py` |
| `spec_parser.py` no TypeScript interface semantic extraction | `extract_code_blocks()` captures TypeScript fenced blocks but `extract_function_signatures()` only parses Python `def/class`; `interface Foo {}` definitions not extracted semantically | Add TypeScript interface parser or extend `extract_function_signatures()` to handle TypeScript `interface` blocks | Medium | `src/superclaude/cli/roadmap/spec_parser.py` |
| `spec_parser.py` `DIMENSION_SECTION_MAP` reflects spec headings only | Section mapping encodes spec-oriented headings (e.g., "3. Functional Requirements", "4. File Manifest"); TDD section headings may not map | Update or extend `DIMENSION_SECTION_MAP` to include TDD section heading variants | Medium | `src/superclaude/cli/roadmap/spec_parser.py` |
| `fingerprint.py` does not extract API endpoint paths | Backtick identifier regex requires letter/underscore start; URL paths like `` `/users/{id}` `` are invisible to fingerprint extraction | Add endpoint-path extraction method or relax regex to capture path-style identifiers | Medium | `src/superclaude/cli/roadmap/fingerprint.py` |
| `integration_contracts.py` does not trigger on plain API endpoint tables | `GET /users` endpoint rows do not match any DISPATCH_PATTERNS category; API sections only trigger when wiring/handler/middleware language is present | Add endpoint-table pattern or document scope limitation | Low | `src/superclaude/cli/roadmap/integration_contracts.py` |

### 4.6 TDD Section Coverage Gaps

| Gap | Current State | Target State | Severity | Files to Change |
|---|---|---|---|---|
| §7 Data Models: MISSED | No extraction instruction; TypeScript interfaces captured as raw code blocks only | Add: "Extract entities, fields, types, constraints, relationships, storage/retention/backup strategy, and data-flow steps from code blocks and tables" | Critical | `src/superclaude/cli/roadmap/prompts.py` |
| §8 API Specifications: MISSED | Behavioral text might incidentally produce an FR; endpoint contract (method, path, auth, params, request/response shape, error codes, versioning) not captured | Add: "Extract endpoint inventory, methods, paths, auth, params, request/response schemas, error codes, versioning and deprecation policy from tables and code blocks" | Critical | `src/superclaude/cli/roadmap/prompts.py` |
| §9 State Management: MISSED | No extraction instruction; state interfaces and transition tables not captured | Add: "Extract state stores, state shape, transitions, triggers, and side effects from interface blocks and state tables" | High | `src/superclaude/cli/roadmap/prompts.py` |
| §10 Component Inventory: MISSED | Route tables, shared component tables, ASCII hierarchy trees not captured; none map to FR/NFR/constraints/risk/dependency | Add: "Extract routes, page components, shared components, props interfaces, source locations, and component hierarchy from tables and trees" | High | `src/superclaude/cli/roadmap/prompts.py` |
| §15 Testing Strategy: MISSED | Coverage targets might appear incidentally as NFRs; concrete test case tables, tooling, and environment matrix not captured | Add: "Extract test levels, coverage targets, tools, concrete test cases, and environment matrix from test strategy tables" — highest value for CLI task generation | Critical | `src/superclaude/cli/roadmap/prompts.py` |
| §25 Operational Readiness: MISSED | A few scaling triggers might appear as NFRs; runbook scenarios, on-call expectations, and capacity planning tables entirely outside scope | Add: "Extract runbook scenarios, diagnosis/resolution steps, on-call expectations, response SLAs, and capacity/scaling triggers" | High | `src/superclaude/cli/roadmap/prompts.py` |
| §26 Cost and Resource Estimation: MISSED | No extraction instruction | Add: "Extract resource cost models, scaling economics, cost drivers, and optimization opportunities" | Low | `src/superclaude/cli/roadmap/prompts.py` |
| §28 Glossary: MISSED | No extraction instruction | Add: "Extract glossary terms and definitions to preserve domain vocabulary for downstream roadmap and tasklist use" | Low | `src/superclaude/cli/roadmap/prompts.py` |
| 15 PARTIAL sections (§1–§4, §6, §11–§14, §16–§17, §19, §21, §23, §27) | Useful content exists but structured non-behavioral elements (tables, diagrams, checklists) partially or unreliably captured | Strengthen existing section instructions to explicitly parse TDD table formats and preserve all columns; add conditional-section handling for frontend-only sections (§9, §10, §26) | Medium | `src/superclaude/cli/roadmap/prompts.py` |

### 4.7 Open Questions Carried Forward

The following gaps could not be resolved from the six research slices and must be treated as Unknown in any implementation plan:

| # | Open Question | Impact |
|---|---|---|
| OQ-1 | `semantic_layer.py` (~400 lines) — does it read spec content in the active pipeline? | May add further spec-specific logic not covered above |
| OQ-2 | `structural_checkers.py` (~200 lines) — relationship to `spec_structural_audit.py` unknown | May require parallel TDD-aware structural checking |
| OQ-3 | Does `run_wiring_analysis(wiring_config, source_dir)` reference `spec_file` via `wiring_config`? | If yes, wiring-verification step may also need TDD branching |
| OQ-4 | Which downstream frontmatter consumers rely on current `spec_source` / `functional_requirements` key names? | Full enumeration needed before `spec_source` is renamed or aliased |
| OQ-5 | ANTI_INSTINCT_GATE TDD performance — hypothesis is that richer TDD identifiers improve fingerprint coverage; not empirically verified | Gate may perform better for TDD inputs without changes; verify before modifying |
| OQ-6 | `spec_source` renaming strategy — alias both fields, rename only new outputs, or keep `spec_source` for backward compatibility | Affects 5 gates and 2+ prompt builders; strategy decision required before implementation |
