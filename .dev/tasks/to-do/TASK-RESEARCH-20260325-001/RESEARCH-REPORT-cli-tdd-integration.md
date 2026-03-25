# Technical Research Report: CLI TDD Integration

**Date:** 2026-03-25
**Depth:** Deep
**Research files:** 6 codebase + 0 web research
**Scope:** src/superclaude/cli/roadmap/, src/superclaude/cli/tasklist/, src/superclaude/cli/pipeline/, src/superclaude/examples/tdd_template.md

---

## Table of Contents

1. [Problem Statement](#1-problem-statement) — The question, why it matters, scope boundaries
2. [Current State Analysis](#2-current-state-analysis) — Data flow, prompt layer, Python modules, gates, CLI entry points, TDD coverage
3. [Target State](#3-target-state) — Desired behavior, success criteria, constraints
4. [Gap Analysis](#4-gap-analysis) — Prompt, gate, CLI, data model, Python module, and TDD section coverage gaps
5. [External Research Findings](#5-external-research-findings) — N/A (codebase-scoped investigation)
6. [Options Analysis](#6-options-analysis) — Three approaches compared: explicit flag, auto-detect, pre-processor
7. [Recommendation](#7-recommendation) — Option A (explicit `--input-type` flag) with rationale
8. [Implementation Plan](#8-implementation-plan) — 6-phase plan with step-level detail for Option A
9. [Open Questions](#9-open-questions) — 2 Critical, 6 Important, 2 Minor questions + 1 pre-existing bug
10. [Evidence Trail](#10-evidence-trail) — All research, synthesis, gaps, and QA artifacts

---

## 1. Problem Statement

### 1.1 The Question

What Python CLI files must change to support `superclaude roadmap run <tdd_file>`?

The CLI currently treats every positional input as a specification file. The `spec_file` positional argument in `roadmap/commands.py` is typed as `click.Path(exists=True, path_type=Path)` with no flag to indicate input type. The command docstring reads: "SPEC_FILE is the path to a specification markdown file." [CODE-VERIFIED: research/05-cli-entry-points.md] No `--input-type`, `--tdd-file`, or equivalent flag exists anywhere in the entry point. [CODE-VERIFIED: research/05-cli-entry-points.md]

This means the CLI, the config model, the executor, and the prompt builders all assume input is a spec file. Running `superclaude roadmap run my_tdd.md` today would not error — but the extraction LLM would receive spec-oriented extraction instructions that omit 8 major TDD content categories, and the downstream steps would never recover that content.

### 1.2 Why It Matters

A Technical Design Document (TDD) is a richer engineering artifact than a spec file. The TDD template contains 28 sections including TypeScript interface definitions, API endpoint contract tables, state machine schemas, component inventory trees, concrete test case matrices, migration phase tables, and operational runbook tables. [CODE-VERIFIED: research/06-tdd-template-structure.md]

The current extraction prompt instructs only 8 output sections (Functional Requirements, Non-Functional Requirements, Complexity Assessment, Architectural Constraints, Risk Inventory, Dependency Inventory, Success Criteria, Open Questions). Of the 28 TDD sections, only 5 are CAPTURED by the current extraction mandate, 15 are PARTIAL, and 8 are entirely MISSED. [CODE-VERIFIED: research/06-tdd-template-structure.md]

The 8 MISSED sections are not peripheral:

- SS7 Data Models — TypeScript interfaces, field tables, storage strategy
- SS8 API Specifications — endpoint tables, request/response schemas, error tables, versioning policy
- SS9 State Management — state shape, transitions, side effects
- SS10 Component Inventory — route tables, component tables, ASCII hierarchy
- SS15 Testing Strategy — test pyramid, unit/integration/E2E case tables
- SS25 Operational Readiness — runbook tables, on-call expectations, capacity planning
- SS26 Cost and Resource Estimation
- SS28 Glossary

Because every downstream pipeline step except three receives only the extraction output — never the original TDD file — content not surfaced at the extraction step is permanently lost. The extraction step is the single chokepoint. [CODE-VERIFIED: research/01-executor-data-flow.md, research/02-prompt-language-audit.md]

A TDD is a superior engineering input for a roadmap because it specifies not just what to build (requirements) but how it must be built (data contracts, interface shapes, component structure, test obligations, migration procedures, and operational posture). A roadmap generated from a TDD without native TDD extraction produces a requirements-level plan that omits implementation contracts the engineering team has already committed to.

### 1.3 What Prior Research Established vs. What This Research Covers

**Prior research (skills layer):** Prior work established TDD as a first-class document type at the skills and framework level. TDD skill templates, agent definitions, and SKILL.md files were developed that describe how agents should interpret and use TDD content. The skills layer governs what Claude does when invoked.

**This research (CLI layer):** This research covers the Python CLI pipeline — the layer below skills — which governs whether TDD content reaches the agents at all, in what form, and whether the pipeline's quality gates will accept the output. The CLI layer includes:

- `roadmap/commands.py` — entry point flags
- `roadmap/models.py` — config dataclass fields
- `roadmap/executor.py` — pipeline step construction and dispatch
- `roadmap/prompts.py` — LLM prompt builders
- Pure-Python analysis modules: `spec_parser.py`, `fidelity_checker.py`, `integration_contracts.py`, `fingerprint.py`, `obligation_scanner.py`
- Gate definitions: `roadmap/gates.py`, `pipeline/gates.py`, `tasklist/gates.py`

Skills-layer TDD capability is irrelevant if the CLI extracts only 5 of 28 TDD sections before invoking any agent. This research locates every CLI-layer change required to make TDD input a first-class pipeline citizen.

---

## 2. Current State Analysis

### 2.1 Data Flow: Which Steps Receive spec_file

The roadmap pipeline is built in `_build_steps()` at `src/superclaude/cli/roadmap/executor.py:775-930`. [CODE-VERIFIED: research/01-executor-data-flow.md]

| Step Name | Input Files | spec_file received? | Pure Python or LLM subprocess? |
|---|---|---|---|
| `extract` | `config.spec_file` | Yes, direct — as `step.inputs` content | LLM subprocess |
| `generate-{agent_a.id}` | `extraction.md` | No | LLM subprocess |
| `generate-{agent_b.id}` | `extraction.md` | No | LLM subprocess |
| `diff` | `roadmap-a`, `roadmap-b` | No | LLM subprocess |
| `debate` | `diff-analysis`, `roadmap-a`, `roadmap-b` | No | LLM subprocess |
| `score` | `debate`, `roadmap-a`, `roadmap-b` | No | LLM subprocess |
| `merge` | `base-selection`, `roadmap-a`, `roadmap-b`, `debate` | No | LLM subprocess |
| `anti-instinct` | `config.spec_file`, `roadmap.md` | Yes, direct — read by `_run_anti_instinct_audit()` | Pure Python |
| `test-strategy` | `roadmap.md`, `extraction.md` | No | LLM subprocess |
| `spec-fidelity` | `config.spec_file`, `roadmap.md` | Yes, direct — as `step.inputs` content | LLM subprocess (or convergence engine) |
| `wiring-verification` | `roadmap.md`, `spec-fidelity.md` | No — `config.spec_file.name` string in prompt only | Pure Python static analysis |

[CODE-VERIFIED: research/01-executor-data-flow.md, executor.py:809-925]

**Critical finding:** `extract` is the single chokepoint. All generate steps receive only `extraction.md` as input — they never see the original file. Content absent from the extraction output is permanently unrecoverable by any downstream LLM step. [CODE-VERIFIED: research/01-executor-data-flow.md, research/02-prompt-language-audit.md]

**Input embedding mechanism:** `_embed_inputs(step.inputs)` at `executor.py:69-82` reads each input file as text and embeds it as a fenced code block with a `# <path>` header. There is no `--file` flag injection; embedding is inline in the composed prompt. [CODE-VERIFIED: research/01-executor-data-flow.md]

**Anti-instinct note:** The anti-instinct step is entirely pure Python. It calls `_run_anti_instinct_audit(spec_file, roadmap_file, output_file)` directly — no LLM subprocess, no prompt builder. [CODE-VERIFIED: research/01-executor-data-flow.md, executor.py:401-408]

**Structural audit hook:** A warning-only Python hook `_run_structural_audit(spec_file, extraction_file)` runs after the extract step completes (`executor.py:515-520`). It calls `check_extraction_adequacy(spec_text, total_req, threshold=0.5)` and logs a warning but never blocks the pipeline. [CODE-VERIFIED: research/01-executor-data-flow.md]

**Validate pipeline:** `validate_executor.py` reads only artifact files (`roadmap.md`, `test-strategy.md`, `extraction.md`) from `output_dir`. It does not revisit the original spec or TDD file. [CODE-VERIFIED: research/05-cli-entry-points.md]

### 2.2 Prompt Layer: Spec-Specific Language in Prompts

All prompt builders live in `src/superclaude/cli/roadmap/prompts.py`. [CODE-VERIFIED: research/02-prompt-language-audit.md]

| Prompt Builder | Spec-Specific Language | TDD Change Required | Severity |
|---|---|---|---|
| `build_extract_prompt(spec_file, retrospective_content)` | "Read the provided specification file"; "requirements extraction specialist"; 8 body sections omit Data Models, APIs, State, Components, Testing, Migration, Ops; frontmatter has 13 requirement-count fields | Major: neutralize framing; add 6+ TDD-specific body sections; broaden frontmatter schema | Critical |
| `build_generate_prompt(agent, extraction_path)` | Indirect: references `spec_source`, `functional_requirements`, `nonfunctional_requirements`, `total_requirements`, and other spec-shaped extraction frontmatter fields by name | Update to consume expanded TDD-aware extraction schema; explicitly direct roadmap to plan TDD artifact categories | High |
| `build_spec_fidelity_prompt(spec_file, roadmap_path)` | "You are a specification fidelity analyst"; "Read the provided specification file"; example identifiers `(FR-NNN)`, `(NFR-NNN)`, `(SC-NNN)`; "spec's priority ordering" | Generalize to source-doc/TDD comparison; add comparison dimensions for APIs, components, migration, ops, test strategy | High |
| `build_test_strategy_prompt(roadmap_path, extraction_path)` | Indirect through extraction schema only | Strengthen to explicitly derive tests from TDD artifacts (API contracts, data models, migration, ops) when present | Medium |
| `build_merge_prompt(base_selection, variant_a, variant_b, debate)` | Mild: `spec_source` provenance field in required output frontmatter | Optional: preserve TDD artifact categories explicitly in merged output | Medium-Low |
| `build_diff_prompt(variant_a, variant_b)` | None | None | Low |
| `build_debate_prompt(diff, variant_a, variant_b, depth)` | None | None | Low |
| `build_score_prompt(debate, variant_a, variant_b)` | None | None | Low |
| `build_wiring_verification_prompt(merge_file, spec_source)` | None — `spec_source` is provenance naming only; body analyzes code-structural wiring | None | Low |
| `build_anti_instinct_prompt` | Does not exist — anti-instinct is pure Python with no prompt builder | N/A | N/A |

[CODE-VERIFIED: research/02-prompt-language-audit.md]

**Why TDD sections are missed -- extraction mandate gap:** The 8 body sections in `build_extract_prompt()` target requirements-level content: Functional Requirements, Non-Functional Requirements, Complexity Assessment, Architectural Constraints, Risk Inventory, Dependency Inventory, Success Criteria, Open Questions. These sections instruct the LLM to extract *what to build* and *what constraints apply*. TDD sections SS7 (Data Models), SS8 (API Specifications), SS9 (State Management), SS10 (Component Inventory), SS15 (Testing Strategy), and SS25 (Operational Readiness) contain implementation-contract-level content -- *how it must be built* -- that has no extraction target in the current prompt. Because the LLM receives no instruction to look for TypeScript interfaces, endpoint tables, component hierarchies, test case matrices, or runbook tables, this content is silently discarded at extraction time. SS14 (Observability) and SS19 (Migration/Rollout) have partial overlap through NFR and Risk extraction respectively, but their structured table content (alert thresholds, metric labels, migration phase dependencies, rollback procedures) degrades to prose fragments without dedicated extraction instructions.

**Stale documentation note:** The `prompts.py` module docstring states the executor appends `--file <path>` to subprocess calls. This is false. The executor uses `_embed_inputs()` for inline file embedding. [CODE-VERIFIED: research/01-executor-data-flow.md -- stale documentation section]

### 2.3 Pure Python Analysis Modules: TDD Compatibility

Five pure-Python analysis modules are used by the anti-instinct step and structural audit hook. [CODE-VERIFIED: research/03-pure-python-modules.md]

| Module | What It Reads | TDD Compatible? | Key Finding |
|---|---|---|---|
| `spec_parser.py` | Any markdown text (frontmatter, tables, code blocks, sections) | Partial | Generic parsing works; `parse_frontmatter()` handles any YAML block; `extract_requirement_ids()` captures `FR-xxx` IDs present in TDD SS5; `extract_function_signatures()` parses Python only — TypeScript `interface Foo {}` definitions NOT extracted; `DIMENSION_SECTION_MAP` encodes spec-oriented headings and may not map to TDD headings |
| `fidelity_checker.py` | FR sections in spec/TDD + `.py` source files in codebase | Partial | `FR-xxx` IDs in TDD SS5 are processed identically to spec IDs; evidence search scans `.py` files only via AST — TDD requirements implemented in TypeScript or other languages produce blind spots; fail-open for ambiguous matches |
| `integration_contracts.py` | Any text (spec or TDD) | Mostly yes | Format-agnostic; 7 dispatch-pattern categories cover architecture prose; TDD SS6 Architecture content (registries, DI, middleware, event listeners, handler maps) fits well; plain API endpoint tables (e.g., `GET /users`) do NOT trigger patterns unless described as wiring mechanisms |
| `fingerprint.py` | Any text (spec or TDD) for identifier extraction; roadmap text for coverage check | Mostly yes | Extracts backtick identifiers, code-block definitions (`def`/`class`), and ALL_CAPS constants; TDD TypeScript type names in backticks (e.g., `UserProfile`) are extracted; API endpoint paths (e.g., `/users/{id}`) do NOT match identifier regex; TDD's richer backtick identifier density may improve coverage ratio |
| `obligation_scanner.py` | Roadmap text only — never reads spec or TDD | N/A | Completely unaffected by input type; scans roadmap for obligation language only |

[CODE-VERIFIED: research/03-pure-python-modules.md]

**Key cross-reference:** `fidelity_checker.py`'s Python-only evidence scan is a structural limitation that intersects directly with TDD SS7 (TypeScript interfaces) and SS8 (API endpoints). TDD requirements implemented in TypeScript would register as unfound even when correctly implemented. [CODE-VERIFIED: research/03-pure-python-modules.md; cross-reference with research/06-tdd-template-structure.md SS7 analysis]

### 2.4 Gate Compatibility

The gate engine in `src/superclaude/cli/pipeline/gates.py` is format-agnostic — all spec-specificity resides in the field names and semantic check functions attached to individual gate definitions. [CODE-VERIFIED: research/04-gate-compatibility.md]

| Gate | Required Fields (count) | TDD Compatible? | Key Blocker |
|---|---|---|---|
| EXTRACT_GATE | 13 | Conditional | `spec_source` field name; requirement-count fields (`functional_requirements`, `nonfunctional_requirements`, `total_requirements`) are spec-centric; LLM could emit them for TDD if explicitly instructed |
| GENERATE_A_GATE | 3 | Conditional | `spec_source` only |
| GENERATE_B_GATE | 3 | Conditional | `spec_source` only |
| DIFF_GATE | 2 | Yes | None |
| DEBATE_GATE | 2 | Yes | None |
| SCORE_GATE | 2 | Yes | None |
| MERGE_GATE | 3 | Conditional | `spec_source` only |
| ANTI_INSTINCT_GATE | 3 | Conditional | Semantically spec-phrased failure messages ("spec code-level identifiers"); hypothesis that TDD's richer identifier density may improve pass rate (UNVERIFIED) |
| TEST_STRATEGY_GATE | 9 | Conditional | `spec_source` only; all semantic checks (complexity class, interleave ratio, milestone counts, philosophy, policy) are workflow-specific and TDD-compatible |
| SPEC_FIDELITY_GATE | 6 | Conditional | Gate name and framing are semantically wrong for TDD; code-level checks (deviation counts, `tasklist_ready` consistency) are generic |
| WIRING_GATE | 16 | Yes | None — analyzes code wiring, independent of source document type |
| DEVIATION_ANALYSIS_GATE | 9 | No | `routing_update_spec` is explicitly spec-specific; `DEV-\d+` routing ID namespace assumes spec-deviation taxonomy; slip/intentional/pre-approved model assumes spec as remediation target |
| REMEDIATE_GATE | 6 | Yes | None |
| CERTIFY_GATE | 5 | Conditional | `_has_per_finding_table` hardcodes `F-\d+` row pattern; if TDD uses different finding ID format, relaxation required |
| TASKLIST_FIDELITY_GATE | 6 | Conditional | Structurally generic; semantically framed as source-fidelity; naming only |

[CODE-VERIFIED: research/04-gate-compatibility.md]

**`spec_source` is the most widespread blocker:** It appears in EXTRACT, GENERATE_A, GENERATE_B, MERGE, and TEST_STRATEGY gates. If TDD pipeline outputs emit `spec_source` using the TDD filename (which is technically valid as a provenance field), many gates can pass without change. The aliasing/renaming strategy is an unresolved implementation question. [CODE-VERIFIED: research/04-gate-compatibility.md]

**DEVIATION_ANALYSIS_GATE pre-existing bug:** The gate requires `ambiguous_count` in frontmatter, but the semantic check `_no_ambiguous_deviations` reads the field `ambiguous_deviations`. This is a field-name mismatch in the existing codebase, independent of TDD. [CODE-VERIFIED: research/04-gate-compatibility.md; confirmed by QA spot-check in gaps-and-questions.md]

### 2.5 CLI Entry Points

Sources: `src/superclaude/cli/roadmap/commands.py`, `src/superclaude/cli/roadmap/models.py`, `src/superclaude/cli/tasklist/commands.py`, `src/superclaude/cli/tasklist/models.py`. [CODE-VERIFIED: research/05-cli-entry-points.md]

| Command | Current Flags | Missing Flag | Extension Point |
|---|---|---|---|
| `superclaude roadmap run <spec_file>` | `--agents`, `--output`, `--depth`, `--resume`, `--dry-run`, `--model`, `--max-turns`, `--debug`, `--no-validate`, `--allow-regeneration`, `--retrospective` | `--input-type [spec\|tdd]` | Additive `@click.option` in `roadmap/commands.py`; add `input_type` field to `RoadmapConfig` |
| `superclaude tasklist validate <output_dir>` | `--roadmap-file`, `--tasklist-dir`, `--model`, `--max-turns`, `--debug` | `--tdd-file` | Additive `@click.option` in `tasklist/commands.py`; add `tdd_file` field to `TasklistValidateConfig` |
| `superclaude roadmap validate <output_dir>` | `--agents`, `--model`, `--max-turns`, `--debug` | None required | `ValidateConfig` is artifact-only; no spec or TDD reference; no changes needed unless roadmap validation itself must reference TDD |

[CODE-VERIFIED: research/05-cli-entry-points.md]

**Established backward-compatible extension pattern:** `RoadmapConfig` already uses additive defaulted fields for version extensions — `convergence_enabled: bool = False` and `allow_regeneration: bool = False` were both added this way. New fields `input_type: Literal["spec", "tdd"] = "spec"` and `tdd_file: Path | None = None` follow the same pattern exactly. [CODE-VERIFIED: research/05-cli-entry-points.md, models.py]

**Call chain from CLI to pipeline:**

```
superclaude roadmap run <spec_file> [flags]
  -> roadmap.commands.run(...)
  -> RoadmapConfig(**config_kwargs)
  -> roadmap.executor.execute_roadmap(config, ...)
  -> _build_steps(config)
  -> pipeline.executor.execute_pipeline(steps, config, run_step=roadmap_run_step, ...)
```

[CODE-VERIFIED: research/05-cli-entry-points.md]

### 2.6 TDD Section Coverage

Source: `src/superclaude/examples/tdd_template.md` analyzed against current `build_extract_prompt()` 8-section mandate. [CODE-VERIFIED: research/06-tdd-template-structure.md]

| Capture Verdict | Count | Key Sections |
|---|---|---|
| CAPTURED | 5 | SS5 Technical Requirements (FR/NFR tables), SS18 Dependencies, SS20 Risks and Mitigations, SS22 Open Questions, SS24 Release Criteria |
| PARTIAL | 15 | SS1 Executive Summary, SS2 Problem Statement, SS3 Goals and Non-Goals, SS4 Success Metrics, SS6 Architecture, SS11 User Flows, SS12 Error Handling, SS13 Security, SS14 Observability, SS16 Accessibility, SS17 Performance Budgets, SS19 Migration and Rollout Plan, SS21 Alternatives Considered, SS23 Timeline and Milestones, SS27 References |
| MISSED | 8 | SS7 Data Models (TypeScript interfaces + field tables), SS8 API Specifications (endpoint tables + schemas), SS9 State Management (state machine + transitions), SS10 Component Inventory (route/component tables + ASCII hierarchy), SS15 Testing Strategy (test pyramid + case tables), SS25 Operational Readiness (runbook tables), SS26 Cost and Resource Estimation, SS28 Glossary |

[CODE-VERIFIED: research/06-tdd-template-structure.md]

**TDD auto-detection signal:** The TDD template frontmatter contains `type: "Technical Design Document"`. No equivalent `spec_type` field exists. The current CLI does not read frontmatter before constructing the extract prompt, so this signal is currently unused. [CODE-VERIFIED: research/06-tdd-template-structure.md]

### 2.7 Current State Summary

The following diagram shows where spec_file enters the pipeline and how content flows to downstream steps.

```
superclaude roadmap run <spec_file>
        |
        v
  RoadmapConfig
  .spec_file = <path>         (no .input_type, no .tdd_file fields)
        |
        v
  _build_steps(config)
        |
        +---> [EXTRACT step] <--- spec_file content embedded (LLM subprocess)
        |         |               build_extract_prompt() [8 sections, spec-centric]
        |         |               WARNING-ONLY: _run_structural_audit() hook
        |         v
        |    extraction.md        <--- ONLY output seen by all downstream LLM steps
        |         |
        |    +----+----+
        |    |         |
        |    v         v
        | [GEN-A]   [GEN-B]       (LLM -- extraction.md only)
        |    |         |
        |    v         v
        |  [DIFF] -> [DEBATE] -> [SCORE] -> [MERGE]
        |                                      |
        |                                   roadmap.md
        |                                      |
        +---> [ANTI-INSTINCT] <--- spec_file + roadmap.md
        |         |               (Pure Python; no LLM)
        |         v
        |    anti-instinct-audit.md
        |
        +---> [TEST-STRATEGY] <--- roadmap.md + extraction.md (LLM)
        |
        +---> [SPEC-FIDELITY] <--- spec_file + roadmap.md (LLM)
        |         |               build_spec_fidelity_prompt() [spec-centric framing]
        |         v
        |    spec-fidelity.md
        |
        +---> [WIRING-VERIFY] <--- roadmap.md + spec-fidelity.md
                                   (Pure Python; spec_file.name string only in prompt)
```

**Key observations:**

- spec_file enters at exactly 3 points: `extract`, `anti-instinct`, `spec-fidelity`
- The extract step is the ONLY point where spec/TDD content can influence the generate steps
- anti-instinct and spec-fidelity receive spec_file AFTER the roadmap is already generated — they perform validation/audit, not generation
- Changing the extract prompt and `build_spec_fidelity_prompt()` covers all LLM-facing spec_file touch points
- `_run_anti_instinct_audit()` in pure Python must be separately assessed for TDD compatibility

**Summary of changes required by layer:**

| Layer | File(s) | Change Required | Priority |
|---|---|---|---|
| CLI entry point | `roadmap/commands.py` | Add `--input-type [spec\|tdd]` flag | Required |
| Config model | `roadmap/models.py` | Add `input_type` and `tdd_file` fields to `RoadmapConfig` | Required |
| Executor dispatch | `roadmap/executor.py` | Branch on `config.input_type` to select prompt builder | Required |
| Extract prompt | `roadmap/prompts.py` | Add `build_extract_prompt_tdd()` with 6+ new sections | Critical |
| Spec-fidelity prompt | `roadmap/prompts.py` | Generalize `build_spec_fidelity_prompt()` for TDD dimensions | High |
| Generate prompt | `roadmap/prompts.py` | Update `build_generate_prompt()` for expanded extraction schema | High |
| Gates | `roadmap/gates.py`, `pipeline/gates.py` | Alias `spec_source`; rename SPEC_FIDELITY_GATE; redesign DEVIATION_ANALYSIS_GATE | Mixed |
| Pure Python modules | `spec_parser.py`, `fidelity_checker.py` | No blocking changes; Python-only scan is a known limitation | Low-Medium |
| Tasklist entry point | `tasklist/commands.py`, `tasklist/models.py` | Add `--tdd-file` flag and `tdd_file` field | Optional |

---

## 3. Target State

### 3.1 Desired Behavior

When a user runs `superclaude roadmap run <tdd_file>` (with `--input-type tdd` or equivalent auto-detection), the pipeline must produce a roadmap that captures structured content from all high-value TDD sections.

**MISSED sections (8) -- must be surfaced as distinct extraction artifacts:** SS7 Data Models, SS8 API Specifications, SS9 State Management, SS10 Component Inventory, SS15 Testing Strategy, SS25 Operational Readiness, SS26 Cost and Resource Estimation, and SS28 Glossary. These have zero coverage in the current 8-section extraction mandate and require dedicated extraction instructions.

**PARTIAL sections requiring strengthened extraction (priority subset):** SS14 Observability and Monitoring and SS19 Migration and Rollout Plan have partial coverage through NFR/Risk extraction but lose structured table content (alert thresholds, metric labels, migration phases, rollback procedures). The TDD extract prompt must add dedicated extraction instructions for these.

**CAPTURED sections (5) -- no extraction changes required:** SS5, SS18, SS20, SS22, SS24 are already captured by the current extraction mandate.

All surfaced extraction artifacts must be available to downstream steps (`generate`, `merge`, `test-strategy`, `spec-fidelity`).

The spec input path (`superclaude roadmap run <spec_file>`) must continue to work unchanged. All new fields and flags must carry defaults that preserve existing behavior when omitted.

### 3.2 Success Criteria

| # | Success Criterion | Research Source |
|---|---|---|
| SC-1 | TDD sections captured by extraction rises from 5 CAPTURED to 28 captured (all sections have at least partial extraction instruction) | 06-tdd-template-structure.md |
| SC-2 | `build_extract_prompt()` emits at minimum 14 body sections: the existing 8 plus dedicated sections for Data Models and Interfaces, API Specifications, State Management, Component Inventory, Testing Strategy, and Operational Readiness | 02-prompt-language-audit.md; 06-tdd-template-structure.md |
| SC-3 | The 8 MISSED TDD sections (SS7, SS8, SS9, SS10, SS15, SS25, SS26, SS28) have explicit extraction targets in the TDD prompt variant | 06-tdd-template-structure.md |
| SC-4 | DEVIATION_ANALYSIS_GATE is redesigned to replace `routing_update_spec` with `routing_update_source` and to support TDD-derived deviation taxonomy; the pre-existing `ambiguous_count` / `ambiguous_deviations` field-name mismatch is resolved as part of this change | 04-gate-compatibility.md |
| SC-5 | `spec_source` in EXTRACT_GATE, GENERATE_A_GATE, GENERATE_B_GATE, MERGE_GATE, and TEST_STRATEGY_GATE is aliased or renamed to `source_document` with backward-compatible fallback | 04-gate-compatibility.md |
| SC-6 | `RoadmapConfig` carries `input_type: Literal["spec", "tdd"] = "spec"` and `tdd_file: Path | None = None`; `TasklistValidateConfig` carries `tdd_file: Path | None = None` | 05-cli-entry-points.md |
| SC-7 | `superclaude roadmap run` accepts `--input-type [spec|tdd]` option (default `spec`); `superclaude tasklist validate` accepts optional `--tdd-file <path>` | 05-cli-entry-points.md |
| SC-8 | `build_spec_fidelity_prompt()` is generalized from "specification fidelity analyst" to "source-document fidelity analyst" with expanded comparison dimensions covering API contracts, component inventory, testing strategy, migration/rollout, and operational readiness | 02-prompt-language-audit.md |
| SC-9 | The extract step's identifier language is broadened from FR/NFR examples to preserve interface names, endpoint identifiers, component names, migration phases, and test case IDs | 02-prompt-language-audit.md |
| SC-10 | SPEC_FIDELITY_GATE is renamed to SOURCE_FIDELITY_GATE (or a TDD-specific parallel gate is introduced) | 04-gate-compatibility.md |
| SC-11 | `fidelity_checker.py` Python-only evidence scan limitation is documented and a non-blocking scope note is added for TypeScript-implemented TDD requirements | 03-pure-python-modules.md |
| SC-12 | TDD frontmatter `type: "Technical Design Document"` is readable by the pipeline as an auto-detection signal (either via `--input-type` or executor frontmatter inspection) | 06-tdd-template-structure.md |

### 3.3 Constraints

| Constraint | Basis |
|---|---|
| Backward compatibility required — spec inputs must continue to work unchanged | All new RoadmapConfig fields must default to `"spec"` / `None`; all new Click options must default to preserve current behavior. Confirmed pattern: `convergence_enabled: bool = False`, `allow_regeneration: bool = False` (05-cli-entry-points.md) |
| `build_extract_prompt()` change is the single highest-risk edit in the pipeline | Extract is the chokepoint — `generate-*`, `diff`, `debate`, `score`, `merge` all receive only extraction output and have no spec_file access (01-executor-data-flow.md; 02-prompt-language-audit.md) |
| Gate enforcement engine (`gate_passed()`) must not be modified | It is format-agnostic; incompatibilities live entirely in per-gate field lists and semantic checks (04-gate-compatibility.md) |
| `obligation_scanner.py` scans roadmap text only and is unaffected by input format | No change required (03-pure-python-modules.md) |
| `semantic_layer.py` (~400 lines) and `structural_checkers.py` (~200 lines) involvement in spec processing is unverified and must be treated as Unknown | Implementation work must not assume these modules are inert without further investigation (gaps-and-questions.md C-1, C-2) |
| `run_wiring_analysis(wiring_config, source_dir)` involvement in spec processing is unverified | If `wiring_config` carries a `spec_file` reference, the wiring-verification step becomes a 5th implementation point for TDD support; implementation work must not assume wiring is inert without investigation (gaps-and-questions.md I-1) |

---

## 4. Gap Analysis

Severity grading: **Critical** = blocks TDD support entirely; **High** = produces wrong or incomplete output; **Medium** = reduces fidelity; **Low** = minor or optional improvement.

### 4.1 Prompt Language Gaps

| Gap | Current State | Target State | Severity | Files to Change |
|---|---|---|---|---|
| `build_extract_prompt()` source framing | "Read the provided specification file" / "requirements extraction specialist" | "Read the provided specification or technical design document" / "requirements and design extraction specialist" | Critical | `roadmap/prompts.py` |
| `build_extract_prompt()` body section coverage | 8 sections covering FR, NFR, Complexity, Architectural Constraints, Risk, Dependency, Success Criteria, Open Questions | Add 6+ dedicated sections: Data Models and Interfaces, API Specifications, State Management, Component Inventory, Testing Strategy, Migration and Rollout Plan, Operational Readiness | Critical | `roadmap/prompts.py` |
| `build_extract_prompt()` identifier language | "Use the spec's exact requirement identifiers verbatim" with FR/NFR examples only | Broaden to: "Preserve exact identifiers including requirement IDs, interface names, endpoint identifiers, component names, migration phases, and test case IDs" | High | `roadmap/prompts.py` |
| `build_extract_prompt()` frontmatter schema | 13 requirement-centric fields | Add optional TDD fields: `data_models_identified`, `api_surfaces_identified`, `components_identified`, `test_artifacts_identified`, `migration_items_identified`, `operational_items_identified` | Medium | `roadmap/prompts.py` |
| `build_spec_fidelity_prompt()` role and input framing | "You are a specification fidelity analyst" / "specification file" / identifiers styled as `(FR-NNN)`, `(NFR-NNN)`, `(SC-NNN)` | "source-document fidelity analyst" / "source specification or TDD file"; expand comparison dimensions for APIs, components, migration/rollout, operational procedures | High | `roadmap/prompts.py` |
| `build_generate_prompt()` TDD artifact planning | Instructions do not explicitly plan roadmap sections around TDD-derived artifacts | Add instructions to plan roadmap sections around TDD artifacts: data model implementation, API implementation, component wiring, test implementation, migration/rollback, operational readiness | High | `roadmap/prompts.py` |
| `build_test_strategy_prompt()` TDD derivation | Does not read original spec/TDD; produces generic roadmap-based validation plan | Strengthen to explicitly derive tests from TDD artifacts when present | Medium | `roadmap/prompts.py` |
| `build_merge_prompt()` TDD artifact preservation | No explicit instruction to preserve TDD artifact categories in merged roadmap | Add optional instruction to preserve data model, API, component, testing, migration, and operational readiness tasks | Medium-Low | `roadmap/prompts.py` |

### 4.2 Gate Schema Gaps

| Gap | Current State | Target State | Severity | Files to Change |
|---|---|---|---|---|
| `spec_source` in EXTRACT_GATE | Required field named `spec_source` | Alias or rename to `source_document`; maintain backward compatibility | High | `roadmap/gates.py` |
| `spec_source` in GENERATE_A/B_GATE | Required field `spec_source` | Alias or rename to `source_document` | High | `roadmap/gates.py` |
| `spec_source` in MERGE_GATE | Required field `spec_source` | Alias or rename to `source_document` | High | `roadmap/gates.py` |
| `spec_source` in TEST_STRATEGY_GATE | Required field `spec_source` | Alias or rename to `source_document` | High | `roadmap/gates.py` |
| DEVIATION_ANALYSIS_GATE `routing_update_spec` | Field explicitly requires update to the spec document as remediation target | Replace with `routing_update_source` or support both field names | Critical | `roadmap/gates.py` |
| DEVIATION_ANALYSIS_GATE `DEV-\d+` namespace | Deviation IDs hardcoded to `DEV-\d+` pattern | Clarify TDD deviation namespace; adjust pattern or make configurable | High | `roadmap/gates.py` |
| DEVIATION_ANALYSIS_GATE `ambiguous_count`/`ambiguous_deviations` mismatch | Required field is `ambiguous_count`; semantic check reads `ambiguous_deviations` — pre-existing bug | Unify to a single canonical field name | High | `roadmap/gates.py` |
| DEVIATION_ANALYSIS_GATE taxonomy | Assumes spec document as remediation target throughout | Generalize from spec-specific to source-document remediation | High | `roadmap/gates.py` |
| SPEC_FIDELITY_GATE naming | Gate named `SPEC_FIDELITY_GATE`; semantically incorrect for TDD | Rename to `SOURCE_FIDELITY_GATE` or add parallel `TDD_FIDELITY_GATE` | Medium | `roadmap/gates.py` |
| ANTI_INSTINCT_GATE failure messages | "spec code-level identifiers insufficiently represented" | Generalize to "source-document code-level identifiers" | Low | `roadmap/gates.py` |
| CERTIFY_GATE `F-\d+` row check | Hardcodes `F-\d+` row pattern | Relax regex for broader finding ID patterns | Low | `pipeline/gates.py` |

### 4.3 CLI Flag and Invocation Gaps

| Gap | Current State | Target State | Severity | Files to Change |
|---|---|---|---|---|
| No `--input-type` flag on `superclaude roadmap run` | Positional argument named `spec_file`; no mechanism to signal TDD input | Add `--input-type [spec\|tdd]` option (default `spec`) | Critical | `roadmap/commands.py` |
| No `--tdd-file` flag on `superclaude tasklist validate` | No `--spec` or `--tdd-file` option; validate executor is entirely artifact-based | Add `--tdd-file <path>` optional option | High | `tasklist/commands.py` |
| `spec_file` positional name semantically incorrect for TDD | CLI argument named `spec_file` when `--input-type tdd` is used | Consider renaming positional to `input_file`; not required for initial support | Low | `roadmap/commands.py` |

### 4.4 Data Model Gaps

| Gap | Current State | Target State | Severity | Files to Change |
|---|---|---|---|---|
| `RoadmapConfig` has no `input_type` field | No field to propagate input type through executor | Add `input_type: Literal["spec", "tdd"] = "spec"` | Critical | `roadmap/models.py` |
| `RoadmapConfig` has no `tdd_file` field | No field to carry resolved TDD file path | Add `tdd_file: Path \| None = None` | High | `roadmap/models.py` |
| `TasklistValidateConfig` has no `tdd_file` field | No way to reference TDD source as validation input | Add `tdd_file: Path \| None = None` | High | `tasklist/models.py` |
| `executor.py` does not consume `input_type` or `tdd_file` | No conditional logic to branch on input type | Add branching in `_build_steps()` and prompt-builder calls | Critical | `roadmap/executor.py` |

### 4.5 Pure Python Module Gaps

| Gap | Current State | Target State | Severity | Files to Change |
|---|---|---|---|---|
| `fidelity_checker.py` Python-only evidence scan | Scans `.py` files only; TypeScript-implemented TDD requirements produce blind spots | Add explicit scope documentation; optionally extend to TypeScript | High | `roadmap/fidelity_checker.py` |
| `spec_parser.py` no TypeScript interface semantic extraction | `extract_function_signatures()` only parses Python `def/class` | Add TypeScript interface parser or extend existing function | Medium | `roadmap/spec_parser.py` |
| `spec_parser.py` `DIMENSION_SECTION_MAP` spec headings | Section mapping encodes spec-oriented headings | Update or extend to include TDD section heading variants | Medium | `roadmap/spec_parser.py` |
| `fingerprint.py` no API endpoint path extraction | Backtick identifier regex requires letter/underscore start; URL paths invisible | Add endpoint-path extraction or relax regex | Medium | `roadmap/fingerprint.py` |
| `integration_contracts.py` no plain API endpoint table trigger | `GET /users` rows do not match dispatch patterns | Add endpoint-table pattern or document limitation | Low | `roadmap/integration_contracts.py` |

### 4.6 TDD Section Coverage Gaps

| Gap | Current State | Target State | Severity |
|---|---|---|---|
| SS7 Data Models: MISSED | No extraction instruction; TypeScript interfaces captured as raw code blocks only | Extract entities, fields, types, constraints, relationships, storage strategy | Critical |
| SS8 API Specifications: MISSED | Endpoint contract not captured | Extract endpoint inventory, methods, paths, auth, schemas, error codes, versioning | Critical |
| SS9 State Management: MISSED | State interfaces and transition tables not captured | Extract state stores, state shape, transitions, triggers, side effects | High |
| SS10 Component Inventory: MISSED | Route tables, component tables, ASCII hierarchy not captured | Extract routes, components, props interfaces, source locations, hierarchy | High |
| SS15 Testing Strategy: MISSED | Concrete test case tables not captured | Extract test levels, coverage targets, tools, test cases, environment matrix | Critical |
| SS25 Operational Readiness: MISSED | Runbook scenarios and capacity planning outside scope | Extract runbook scenarios, on-call expectations, capacity/scaling triggers | High |
| SS26 Cost and Resource Estimation: MISSED | No extraction instruction | Extract resource cost models, scaling economics, optimization opportunities | Low |
| SS28 Glossary: MISSED | No extraction instruction | Extract glossary terms and definitions for domain vocabulary preservation | Low |
| SS14 Observability: PARTIAL | Partially captured through NFR extraction; structured tables (alert thresholds, metric labels, trace sampling, dashboard definitions) lost | Add dedicated extraction: log format, metrics with labels, alert thresholds, trace sampling strategy, dashboard inventory, business instrumentation mappings | High |
| SS19 Migration and Rollout: PARTIAL | Partially captured through Risk extraction; structured tables (migration phases, feature flags, rollback procedures) lost as prose fragments | Add dedicated extraction: migration phases with dependencies, feature flags with cleanup dates, rollout stages with rollback triggers, numbered rollback procedure | High |
| 13 remaining PARTIAL sections | Structured non-behavioral elements partially captured | Strengthen instructions for TDD table formats; add conditional-section handling | Medium |

### 4.7 Open Questions Carried Forward

| # | Open Question | Impact |
|---|---|---|
| OQ-1 | `semantic_layer.py` (~400 lines) — does it read spec content in the active pipeline? | May add further spec-specific logic not covered above |
| OQ-2 | `structural_checkers.py` (~200 lines) — relationship to `spec_structural_audit.py` unknown | May require parallel TDD-aware structural checking |
| OQ-3 | Does `run_wiring_analysis(wiring_config, source_dir)` reference `spec_file` via `wiring_config`? | If yes, wiring-verification step may also need TDD branching |
| OQ-4 | Which downstream frontmatter consumers rely on current `spec_source` / `functional_requirements` key names? | Full enumeration needed before rename or alias |
| OQ-5 | ANTI_INSTINCT_GATE TDD performance — hypothesis that richer TDD identifiers improve fingerprint coverage; not empirically verified | Gate may perform better for TDD without changes; verify before modifying |
| OQ-6 | `spec_source` renaming strategy — alias both, rename only new outputs, or keep for backward compat? | Affects 5 gates and 2+ prompt builders; strategy decision required |

---

## 5. External Research Findings

This investigation was scoped entirely to the IronClaude codebase. No external web research was performed or required.

All findings reported in this research effort are derived from direct source reading of the IronClaude Python CLI, located under `src/superclaude/cli/`. This includes the sprint runner, roadmap executor, wiring gate, fidelity checker, and associated test suites under `tests/`.

External research was not necessary because:

- The research questions concerned internal architecture, existing wiring patterns, and CLI behavior — all answerable from the source tree.
- No third-party library evaluation, API design comparison, or best-practices benchmarking was in scope.

**Guidance for future work:** If subsequent tasks require external research, candidate topics include evaluating alternative Python prompt-engineering architectures for CLI-integrated agents, reviewing best practices for CLI input-type flags and argument validation patterns, and comparing test isolation strategies for CLIs with side-effecting pipeline steps.

---

## 6. Options Analysis

### Framing

Three structurally distinct approaches were identified. All three must address the same two Critical findings:

1. **Extract chokepoint** — `build_extract_prompt()` is the single point of failure. All downstream steps receive only extraction output, never the original TDD file. Any TDD content not surfaced at extract time is unrecoverable. [Sources: research/01-executor-data-flow.md, research/02-prompt-language-audit.md]

2. **DEVIATION_ANALYSIS_GATE structural incompatibility** — The only gate with hard structural incompatibility: `routing_update_spec` is explicitly spec-specific; `DEV-\d+` ID namespace assumes spec-deviation taxonomy. [Source: research/04-gate-compatibility.md]

A third HIGH-severity finding affects all three options equally:

3. **`spec_source` field name** — Appears in 5 gates and at least 2 prompt builders. If TDD-mode LLM outputs still emit `spec_source` (using the TDD filename), these gates can pass without field renaming. Aliasing is optional but semantically desirable. [Source: research/04-gate-compatibility.md]

### Option A: Dual Extract Prompt (Explicit `--input-type` Flag)

Add `--input-type [spec|tdd]` as a Click option. Add `input_type: Literal["spec","tdd"] = "spec"` to `RoadmapConfig`. In `executor.py`, branch on `config.input_type`: call `build_extract_prompt()` for spec mode or a new `build_extract_prompt_tdd()` for TDD mode. The TDD prompt adds dedicated extraction sections for 8 missed TDD content areas. Update `build_spec_fidelity_prompt()` for TDD comparison dimensions. Redesign `DEVIATION_ANALYSIS_GATE`.

| Aspect | Assessment |
|--------|-----------|
| Effort | M |
| Risk | Low |
| Backward compatible? | Yes — `--input-type` defaults to `"spec"`; all existing invocations unchanged |
| Files affected | `roadmap/commands.py`, `roadmap/models.py`, `roadmap/executor.py`, `roadmap/prompts.py` (2 functions), `roadmap/gates.py` (DEVIATION_ANALYSIS_GATE + 5 gates for `spec_source` alias) |
| Pros | User intent is explicit and unambiguous; follows established extension pattern (`convergence_enabled`, `allow_regeneration`); TDD prompt fully decoupled from spec prompt — no regression risk; `spec_source` aliasing can be phased; clean branch point in `_build_steps()` |
| Cons | Requires user to pass `--input-type tdd`; `spec_file` positional name remains awkward for TDD; two prompt functions to maintain in parallel with drift risk |

### Option B: Auto-Detect TDD from Frontmatter

No new CLI flag. The executor reads the YAML `type` field from the input file before building the extract prompt. If `type == "Technical Design Document"`, executor switches to TDD mode. All prompt and gate changes are identical to Option A.

| Aspect | Assessment |
|--------|-----------|
| Effort | M |
| Risk | Medium — fragile detection dependency |
| Backward compatible? | Conditional — existing spec files without a `type` field default to spec mode |
| Files affected | Same as Option A, plus: `executor.py` needs a pre-step frontmatter read routine |
| Pros | Zero user-facing change; no flag to document; TDD template has the `type` field confirmed |
| Cons | Detection depends on exact frontmatter value including emoji; TDD files missing frontmatter silently fall back to spec mode; adds file-read side-effect before step execution; emoji in YAML string comparison edge cases |

### Option C: TDD Pre-Processor Step Using `spec_parser.py`

Add a new `pre-extract` pipeline step before the LLM extract step. This step uses `spec_parser.py` to programmatically parse TDD sections and generates a structured intermediate representation (IR) document fed into the extract prompt.

| Aspect | Assessment |
|--------|-----------|
| Effort | XL |
| Risk | High |
| Backward compatible? | Conditional — new pipeline step; gate configuration must account for new step output |
| Files affected | `executor.py`, `prompts.py`, new `tdd_preprocessor.py`, `roadmap/commands.py`, `roadmap/models.py`, `roadmap/gates.py`, potentially `pipeline/gates.py` |
| Pros | Highest potential accuracy for structured TDD content; programmatic extraction is reproducible and testable; leverages existing `spec_parser.py` modules |
| Cons | `extract_function_signatures()` only parses Python — TypeScript not supported; endpoint paths don't match identifier regex; IR generation logic speculative; `DIMENSION_SECTION_MAP` encodes spec headings; two uninvestigated modules (`semantic_layer.py`, `structural_checkers.py`) carry integration risk |

### Cross-Option Comparison

| Dimension | Option A (Explicit Flag) | Option B (Auto-Detect) | Option C (Pre-Processor) |
|-----------|--------------------------|------------------------|--------------------------|
| Effort | M | M | XL |
| Risk | Low | Medium | High |
| Backward compatible? | Yes (default="spec") | Conditional (fragile detection) | Conditional (new step) |
| User experience | Explicit flag required | Transparent, no flag | Explicit flag required |
| Addresses extract chokepoint? | Yes — via `build_extract_prompt_tdd()` | Yes — same prompt changes | Partially — TS interface gap remains |
| Addresses DEVIATION_ANALYSIS_GATE? | Yes | Yes | Yes |
| New files required | None | None | `tdd_preprocessor.py` |
| Files modified | 4 | 4 + executor startup read | 6+ |
| Silent failure mode? | No | Yes — missing frontmatter falls back silently | No |
| Matches established extension pattern? | Yes | Partial | No |
| TypeScript interface extraction? | LLM-driven (prompt instruction) | LLM-driven (prompt instruction) | Partial programmatic; TS parser absent |
| Incrementally testable? | Yes | Harder — detection is implicit | Harder — IR needs TDD test fixtures |

---

## 7. Recommendation

### Recommended Option: Option A — Dual Extract Prompt with Explicit `--input-type` Flag

Option A has the most favorable risk/effort/compatibility tradeoff. It addresses both Critical findings directly, follows the project's established extension pattern, and does not introduce fragile detection logic or unverified module dependencies.

### Rationale

**Risk/Effort/Compatibility:** Option A is Low risk, M effort, with confirmed backward compatibility following the identical pattern used by `convergence_enabled: bool = False` and `allow_regeneration: bool = False`. [Confirmed: research/05-cli-entry-points.md]

Option B shares effort level but introduces Medium risk via fragile frontmatter detection. The `type` field value includes a Unicode emoji — documents that omit or vary it silently fall back to spec-mode extraction with no user-visible error. Silent failure at the extract chokepoint is particularly severe because all downstream steps propagate the incomplete content.

Option C is XL effort and High risk. Confirmed capability gaps: `extract_function_signatures()` does not parse TypeScript interfaces [research/03-pure-python-modules.md], endpoint URL paths don't match `fingerprint.py` regex [research/03-pure-python-modules.md], and two uninvestigated modules carry unquantifiable integration risk [gaps-and-questions.md C-1, C-2].

**Addressing the Extract Chokepoint:** All three options require a new extract prompt with TDD-specific sections. For Options A and B, LLM-driven extraction with explicit section instructions is the mechanism — the same mechanism validated by the current pipeline. A well-instructed LLM prompt is more likely to produce complete semantic extraction from TypeScript interfaces than a Python parser with no TypeScript AST support (Option C).

**DEVIATION_ANALYSIS_GATE:** All three options require identical gate redesign. The pre-existing `ambiguous_count`/`ambiguous_deviations` bug fix is a no-extra-cost bundled correction.

**Incremental Implementability:** Option A can be staged:

| Stage | Change | Regression risk to spec path |
|-------|--------|------------------------------|
| 1 | Add `--input-type` flag + `input_type` field | Zero — no behavioral change |
| 2 | Implement `build_extract_prompt_tdd()` | Zero — new function, existing untouched |
| 3 | Add branch in `executor.py` `_build_steps()` | Minimal — conditional at executor.py:809-820 |
| 4 | Update `build_spec_fidelity_prompt()` for TDD dimensions | Low — prompt text only |
| 5 | Redesign DEVIATION_ANALYSIS_GATE | Contained — single gate |

### Implementation Priority Order

| Priority | Change | Severity | Rationale |
|----------|--------|----------|-----------|
| 1 | `build_extract_prompt_tdd()` with TDD-specific sections | Critical | Single chokepoint; all downstream steps depend on it |
| 2 | DEVIATION_ANALYSIS_GATE redesign | Required | Only structurally incompatible gate |
| 3 | `build_spec_fidelity_prompt()` generalization | High | Receives spec_file directly; current language is spec-bound |
| 4 | `build_generate_prompt()` TDD frontmatter field consumption | High | Downstream of Priority 1 |
| 5 | `spec_source` aliasing in 5 gates | Important | Semantically desirable; functionally deferrable |
| 6 | `build_test_strategy_prompt()` TDD enrichment | Medium | Strengthens test derivation; not blocking |
| 7 | ANTI_INSTINCT_GATE failure message generalization | Low | Wording inaccuracy; functional behavior unaffected |

---

## 8. Implementation Plan

**Option:** A — Explicit `--input-type [spec|tdd]` flag

> **Scope:** Add `--input-type [spec|tdd]` to `superclaude roadmap run`. When `--input-type tdd` is passed, the pipeline routes through a new `build_extract_prompt_tdd()` builder instead of the existing `build_extract_prompt()`. All other pipeline steps are unchanged. Backward compatibility is preserved: the default value is `spec`.

### Phase 1: CLI and Config Layer

**Prerequisite for everything else. No logic changes — pure wiring.**

**1.1 `roadmap/commands.py` — Add `--input-type` flag**

| Step | Action | File | Details |
|------|--------|------|---------|
| 1.1.1 | Add Click option decorator | `roadmap/commands.py` | `@click.option("--input-type", type=click.Choice(["spec", "tdd"], case_sensitive=False), default="spec", help="Type of input file for roadmap generation.")` Place after existing `--retrospective` option. |
| 1.1.2 | Add `input_type: str` to `run()` signature | `roadmap/commands.py` | Keyword argument alongside other Click-bound params. |
| 1.1.3 | Add `"input_type": input_type` to `config_kwargs` dict | `roadmap/commands.py` | Before `RoadmapConfig(**config_kwargs)` call. |

**1.2 `roadmap/models.py` — Extend `RoadmapConfig`**

| Step | Action | File | Details |
|------|--------|------|---------|
| 1.2.1 | Add `input_type` field | `roadmap/models.py` | `input_type: Literal["spec", "tdd"] = "spec"` — after `allow_regeneration`, following established defaulted-field pattern. |
| 1.2.2 | Add `tdd_file` field | `roadmap/models.py` | `tdd_file: Path \| None = None` — reserved for future use; avoids second models.py change. |

**1.3 `tasklist/commands.py` — Add `--tdd-file` flag**

| Step | Action | File | Details |
|------|--------|------|---------|
| 1.3.1 | Add Click option decorator | `tasklist/commands.py` | `@click.option("--tdd-file", type=click.Path(exists=True, path_type=Path), default=None, help="Path to the TDD file as additional validation input.")` |
| 1.3.2 | Add `tdd_file: Path \| None` to `validate()` signature | `tasklist/commands.py` | Keyword argument. |
| 1.3.3 | Add `tdd_file` to config construction | `tasklist/commands.py` | `tdd_file=tdd_file.resolve() if tdd_file is not None else None` |

**1.4 `tasklist/models.py` — Extend `TasklistValidateConfig`**

| Step | Action | File | Details |
|------|--------|------|---------|
| 1.4.1 | Add `tdd_file` field | `tasklist/models.py` | `tdd_file: Path \| None = None` — after existing `tasklist_dir` field. |

**Phase 1 verification:** `uv run python -c "from superclaude.cli.roadmap.models import RoadmapConfig; c = RoadmapConfig(spec_file=Path('.')); print(c.input_type)"` must print `spec`.

### Phase 2: TDD Extract Prompt (Critical Path)

**This is the single highest-risk change. All generate, diff, debate, score, and merge steps receive only extraction output — making extract the sole chokepoint for TDD content coverage.**

**2.1 `roadmap/prompts.py` — Create `build_extract_prompt_tdd()`**

| Step | Action | Details |
|------|--------|---------|
| 2.1.1 | Add new function | Insert immediately after `build_extract_prompt()`. Do NOT modify `build_extract_prompt()`. |
| 2.1.2 | Signature | `def build_extract_prompt_tdd(spec_file: Path, retrospective_content: str \| None = None) -> str:` — identical to `build_extract_prompt()` for drop-in substitution. |
| 2.1.3 | Neutralize source framing | "Read the provided source specification or technical design document" / "requirements and design extraction specialist" |
| 2.1.4 | Broaden identifier language | "Preserve exact identifiers including requirement IDs (FR-xxx, NFR-xxx), interface names, endpoint identifiers, component names, migration phase names, and test case IDs." |
| 2.1.5 | Retain 8 existing body sections | Functional Requirements, Non-Functional Requirements, Complexity Assessment, Architectural Constraints, Risk Inventory, Dependency Inventory, Success Criteria, Open Questions — identical instruction text. |
| 2.1.6 | Add 6 new TDD-specific body sections | See 2.1.7-2.1.12 below. |

New TDD extraction sections:

| Section | Extraction Instruction |
|---------|----------------------|
| **Data Models and Interfaces** | Extract every entity, field, type, constraint, and relationship from TypeScript interfaces and markdown tables in SS7. Include entity name, all fields with types and constraints, required vs. optional, storage/retention/backup strategy, data-flow steps. |
| **API Specifications** | Extract complete API surface from SS8. For each endpoint: HTTP method, URL path, auth requirement, rate limit, description. Per-endpoint: query parameters, request/response schema, error table, versioning/deprecation. |
| **Component Inventory** | Extract from SS10 and SS9. Route table: paths, components, auth. Shared components: names, props, usage, source locations. ASCII hierarchy: parent-child relationships. State management: stores, state shape, transitions, triggers, side effects. |
| **Testing Strategy** | Extract from SS15. Test pyramid: coverage levels, tooling, targets, ownership. Test case tables: name/ID, input, expected output, mocks/fixtures. Environment matrix. These are primary source of truth for test-related roadmap tasks. |
| **Migration and Rollout Plan** | Extract from SS19. Migration phases: name, tasks, duration, dependencies, rollback option. Feature flags: name, purpose, status, cleanup date. Rollout stages: audience, success criteria, monitoring, rollback triggers. Numbered rollback procedure. Preserve ordering and dependency information. |
| **Operational Readiness** | Extract from SS25 and SS14. Runbook scenarios: name, symptoms, diagnosis, resolution, escalation, prevention. On-call: scenario, page volume, MTTD/MTTR targets, knowledge prerequisites. Capacity: metric, baseline, projections, scaling triggers. Observability: log format, metrics, alert thresholds, trace sampling, dashboards. |

Additional steps:

| Step | Action |
|------|--------|
| 2.1.13 | Expand YAML frontmatter — retain 13 existing fields; add 6 TDD-specific: `data_models_identified`, `api_surfaces_identified`, `components_identified`, `test_artifacts_identified`, `migration_items_identified`, `operational_items_identified`. Set to 0 if section absent. |
| 2.1.14 | Keep `spec_source` field — instruct: "Set `spec_source` to the TDD filename." Preserves backward compatibility with all 5 gates. |
| 2.1.15 | Mirror `if retrospective_content:` block from `build_extract_prompt()`. |

### Phase 3: Executor Branching

**Routes `--input-type tdd` to the new prompt builder. Two localized changes.**

| Step | Action | File | Details |
|------|--------|------|---------|
| 3.1.1 | Add import for `build_extract_prompt_tdd` | `roadmap/executor.py` | Add to existing import block at lines 42-52. |
| 3.1.2 | Branch extract prompt in `_build_steps()` | `roadmap/executor.py` | At executor.py:809-820: if `config.input_type == "tdd"` call `build_extract_prompt_tdd()`, else call `build_extract_prompt()`. All other step fields unchanged. |
| 3.1.3 | No changes to anti-instinct wiring | `roadmap/executor.py` | `config.spec_file` IS the TDD file. `integration_contracts.py` and `fingerprint.py` are format-agnostic. |
| 3.1.4 | No changes to spec-fidelity wiring | `roadmap/executor.py` | TDD file passes through as `spec_file`. Phase 5 updates prompt text. |
| 3.2.1 | Document TDD structural indicator mismatch | `roadmap/executor.py` | `_run_structural_audit()` is warning-only; TDD heading structure differs from spec. Add inline comment; no code change for Phase 1. |

**Open investigation:** `structural_checkers.py` (~200 lines) was not investigated (Gap C-2). Do not rely on structural audit behavior for TDD correctness until resolved.

### Phase 4: Gate Schema Updates

**The gate enforcement engine is format-agnostic. All incompatibilities are in field names and semantic checks within individual gate definitions.**

**4.1 Gates requiring `spec_source` — No code changes needed for Option A**

`build_extract_prompt_tdd()` (Phase 2, step 2.1.14) instructs the LLM to emit `spec_source: <tdd_filename>`. All 5 gates (EXTRACT, GENERATE_A, GENERATE_B, MERGE, TEST_STRATEGY) pass without modification.

**4.2 DEVIATION_ANALYSIS_GATE — Deferred**

| Step | Action | Details |
|------|--------|---------|
| 4.2.1 | Phase 1 TDD: no change | Not in primary roadmap pipeline path for initial TDD support. |
| 4.2.2 | Future: rename `routing_update_spec` to `routing_update_source` | When TDD extends to full deviation analysis pipeline. |
| 4.2.3 | Pre-existing bug: note for awareness | `ambiguous_count` vs. `ambiguous_deviations` field mismatch. File as separate defect. |

**4.3 ANTI_INSTINCT_GATE — No code changes needed.** Semantic checks operate on format-agnostic pure-Python outputs. TDD documents may produce more backtick identifiers, potentially improving fingerprint coverage (UNVERIFIED hypothesis — Gap I-5).

**Open investigation:** `semantic_layer.py` (~400 lines) was not investigated (Gap C-1). Do not assert all gate semantics are TDD-safe until resolved.

### Phase 5: `build_spec_fidelity_prompt()` Update

| Step | Action | Details |
|------|--------|---------|
| 5.1.1 | Generalize analyst role | "specification fidelity analyst" to "source-document fidelity analyst" |
| 5.1.2 | Generalize input label | "specification file" to "source specification or TDD file"; "requirements in the specification" to "requirements, design decisions, or commitments in the source document" |
| 5.1.3 | Generalize identifier examples | Add `(interface-name)`, `(endpoint-path)`, `(component-name)`, `(migration-phase)`, `(test-case-id)` |
| 5.1.4 | Generalize priority language | "spec's priority ordering" to "source document's priority ordering or stated importance hierarchy" |
| 5.1.5 | Add TDD comparison dimensions | API endpoints/contracts, component/module inventory, testing strategy/validation matrix, migration/rollout procedures, operational readiness |
| 5.1.6 | No signature change | `build_spec_fidelity_prompt(spec_file: Path, roadmap_path: Path) -> str` unchanged. |

### Phase 6: Tasklist Validate TDD Enrichment (Deferred)

Depends on Phase 1 being complete. Lower value without Phases 2-5.

| Step | Action | File | Details |
|------|--------|------|---------|
| 6.1.1 | Add TDD file to validation inputs conditionally | `tasklist/executor.py` | If `config.tdd_file is not None`, append to step's `inputs` list. |
| 6.2.1 | Add TDD-aware fidelity instructions | `tasklist/prompts.py` | Verify test cases from TDD SS15 appear as validation tasks; verify rollback procedures from SS19 appear as contingency tasks. |
| 6.2.2 | Keep existing behavior when `tdd_file is None` | `tasklist/prompts.py` | No regression. |

### Phase Dependencies

```
Phase 1 (CLI + Config)
    |
    |--> Phase 2 (TDD Extract Prompt)   <-- Critical path
    |       |
    |       |--> Phase 3 (Executor Branching)
    |               |
    |               |--> Phase 4 (Gate Schema Review)
    |               |--> Phase 5 (Fidelity Prompt)     [parallel with Phase 4]
    |
    |--> Phase 6 (Tasklist Validate)    [optional; deferred]
```

**Minimum viable delivery:** Phases 1 + 2 + 3. With these complete, `superclaude roadmap run tdd.md --input-type tdd` routes through the TDD-aware extraction prompt. The rest of the pipeline works on TDD-derived content, though with residual spec-language in gate error messages and the fidelity prompt.

### Integration Checklist

- [ ] `superclaude roadmap run spec.md` continues unchanged — backward compatibility
- [ ] `superclaude roadmap run tdd.md --input-type tdd` produces `extraction.md` with `## Data Models and Interfaces` section
- [ ] TDD extraction frontmatter contains `spec_source: tdd.md`
- [ ] EXTRACT_GATE passes for TDD-derived `extraction.md` (all 13 required fields present)
- [ ] ANTI_INSTINCT_GATE `fingerprint_coverage` >= 0.7 for reference TDD (UNVERIFIED hypothesis)
- [ ] `superclaude tasklist validate <output_dir>` works unchanged without `--tdd-file`
- [ ] `--dry-run` shows correct prompt builder routing for spec vs. TDD
- [ ] `RoadmapConfig(spec_file=Path("x.md"))` defaults `input_type="spec"`

---

## 9. Open Questions

Ordered by severity: Critical gaps that could change implementation plan scope first, then Important, then Minor, then the confirmed pre-existing bug.

### Critical Questions

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| C-1 | Does `semantic_layer.py` (~400 lines) read `spec_file` at any point in the active pipeline? | If yes, it is a 4th implementation point for TDD support missed in this investigation; the implementation plan would be incomplete | Read `src/superclaude/cli/roadmap/semantic_layer.py` in full; trace call path from `executor.py`; search for `spec_file`, `config.spec_file`, `read_text` references |
| C-2 | Does `structural_checkers.py` (~200 lines) have spec-format-specific assumptions that would break on TDD structural patterns? | If yes, it requires changes when TDD input produces different section headings, table structures, or identifier patterns | Read `src/superclaude/cli/roadmap/structural_checkers.py` in full; check for hardcoded section names, FR/NFR ID assumptions, or spec-template field expectations |

### Important Questions

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| I-1 | Does `run_wiring_analysis(wiring_config, source_dir)` in `executor.py:421-433` read `spec_file` via the `wiring_config` object? | If yes, `wiring-verification` becomes a 5th implementation point | Read executor.py:421-433; inspect `wiring_config` construction |
| I-2 | Which downstream extraction frontmatter consumers read `spec_source` or the new TDD-specific count fields? | If additional consumers exist beyond gates and prompt builders, aliasing strategy must account for them | Search entire roadmap/ and pipeline/ directories for string `spec_source` |
| I-3 | What is the correct `spec_source` rename strategy — alias both, rename only new outputs, or keep for backward compat? | Determines gate/prompt builder change scope | Enumerate all consumers; decide if TDD-mode can emit `spec_source: <tdd-filename>` unchanged |
| I-4 | How should `build_test_strategy_prompt()` be enriched for TDD input? | TDD SS15 contains concrete test case tables that should feed directly into test-strategy step | Specify whether test-strategy step should receive `config.spec_file` or `config.tdd_file` as additional input |
| I-5 | Is the hypothesis that ANTI_INSTINCT_GATE performs better on TDD input empirically correct? | If false, TDD inputs may fail the gate more often than expected | Run `check_fingerprint_coverage()` and `extract_integration_contracts()` on sample TDD vs. spec; compare ratios |
| I-6 | Will `fidelity_checker.py` TypeScript blind spot produce near-zero FR coverage evidence for TDD SS7 Data Models and SS10 Component Inventory? | False-negative findings for TypeScript-implemented requirements | Document as known limitation; mark as out-of-scope for initial pass or add to future work |

### Minor Questions

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| M-1 | What is the full `SpecStructuralAudit` dataclass field structure? | Low — warning-only audit; can be inferred from `check_extraction_adequacy()` behavior | Read `spec_structural_audit.py` if TDD-aware structural thresholds are planned |
| M-2 | Does `_get_all_step_ids()` enumerate a step list consistent with `_build_steps()`? Docstring says "9-step pipeline" but runtime builds 11+ entries. | Low — docstring inconsistency only; no runtime impact | Update docstrings; no logic change |

### Pre-Existing Codebase Bug

| # | Issue | Severity | Evidence | Recommended Action |
|---|-------|----------|----------|--------------------|
| B-1 | DEVIATION_ANALYSIS_GATE field name mismatch: required frontmatter field is `ambiguous_count` but semantic check `_no_ambiguous_deviations` reads `ambiguous_deviations` — gate may silently pass when `ambiguous_deviations` is absent | Medium | Confirmed by rf-qa spot-check against `gates.py`; documented in research/04-gate-compatibility.md and gaps-and-questions.md | Fix as standalone bug before or alongside TDD integration work |

---

## 10. Evidence Trail

### Codebase Research

All six files were produced by dedicated research agents performing direct code inspection. No web research was performed.

| File | Topic | Key Finding |
|------|-------|------------|
| `research/01-executor-data-flow.md` | Pipeline step wiring — which steps receive `spec_file` | Only 3 steps receive `spec_file` directly (`extract`, `anti-instinct`, `spec-fidelity`). Extract is the single chokepoint — all downstream generate steps receive only extraction output. |
| `research/02-prompt-language-audit.md` | Spec-specific language in all 9 prompt builders | `build_extract_prompt()` is CRITICAL — 8 spec-centric sections miss 8+ TDD areas. `build_spec_fidelity_prompt()` is HIGH severity. Five other builders are LOW or require no changes. |
| `research/03-pure-python-modules.md` | TDD compatibility of 5 pure-Python analysis modules | `integration_contracts.py`, `fingerprint.py`, `obligation_scanner.py` mostly compatible. `spec_parser.py` partially compatible (no TypeScript semantic extraction). `fidelity_checker.py` highest risk — Python-only AST scan. |
| `research/04-gate-compatibility.md` | TDD compatibility of all 15 pipeline gates | 5 already compatible (DIFF, DEBATE, SCORE, WIRING, REMEDIATE), 9 conditionally compatible pending `spec_source` aliasing, 1 structurally incompatible (DEVIATION_ANALYSIS_GATE). Pre-existing `ambiguous_count`/`ambiguous_deviations` mismatch confirmed. |
| `research/05-cli-entry-points.md` | CLI parameters, config fields, extension patterns | No `--input-type` flag exists. Project uses additive defaulted dataclass fields as backward-compatible extension pattern. Adding `input_type` and `tdd_file` is sufficient. |
| `research/06-tdd-template-structure.md` | Section-by-section capture analysis of 28 TDD sections | 5 CAPTURED / 15 PARTIAL / 8 MISSED. TDD frontmatter `type` field provides auto-detection discriminator. |

### Web Research

N/A — no web research was performed. All findings are from direct codebase inspection of `src/superclaude/cli/roadmap/`, `src/superclaude/cli/pipeline/`, `src/superclaude/cli/tasklist/`, and `src/superclaude/examples/`.

### Synthesis Files

| File | Report Sections |
|------|----------------|
| `synthesis/synth-01-problem-current-state.md` | SS1 Problem Statement, SS2 Current State Analysis |
| `synthesis/synth-02-target-gaps.md` | SS3 Target State, SS4 Gap Analysis |
| `synthesis/synth-03-external-findings.md` | SS5 External Research Findings |
| `synthesis/synth-04-options-recommendation.md` | SS6 Options Analysis, SS7 Recommendation |
| `synthesis/synth-05-implementation-plan.md` | SS8 Implementation Plan |
| `synthesis/synth-06-questions-evidence.md` | SS9 Open Questions, SS10 Evidence Trail |

### Gaps Log

- `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/gaps-and-questions.md` — 2 Critical gaps, 6 Important gaps, 3 Minor gaps, 1 confirmed pre-existing codebase bug.

### QA Reports

| File | Type | Verdict |
|------|------|---------|
| `qa/analyst-completeness-report.md` | Phase 3 — Research Completeness Verification | CONDITIONAL PASS — 2 critical gaps (`semantic_layer.py`, `structural_checkers.py`) require targeted gap-fill; all other sections cleared |
| `qa/qa-research-gate-report.md` | Phase 4 — Research Gate QA (independent spot-check) | PASS — all 10 checklist items pass; 12 code claims independently verified; no contradictions across 6 research files |
