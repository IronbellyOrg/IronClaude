# Technical Research Report: CLI TDD Integration
## Synthesis Document 01 — Problem Statement and Current State Analysis

**Research Task:** TASK-RESEARCH-20260325-001
**Date:** 2026-03-25
**Status:** Synthesis — Sections §1 and §2 only
**Sources:** Research files 01–06 + gaps-and-questions.md

---

## §1 Problem Statement

### 1.1 The Question

What Python CLI files must change to support `superclaude roadmap run <tdd_file>`?

The CLI currently treats every positional input as a specification file. The `spec_file` positional argument in `roadmap/commands.py` is typed as `click.Path(exists=True, path_type=Path)` with no flag to indicate input type. The command docstring reads: "SPEC_FILE is the path to a specification markdown file." [CODE-VERIFIED: research/05-cli-entry-points.md] No `--input-type`, `--tdd-file`, or equivalent flag exists anywhere in the entry point. [CODE-VERIFIED: research/05-cli-entry-points.md]

This means the CLI, the config model, the executor, and the prompt builders all assume input is a spec file. Running `superclaude roadmap run my_tdd.md` today would not error — but the extraction LLM would receive spec-oriented extraction instructions that omit 8 major TDD content categories, and the downstream steps would never recover that content.

### 1.2 Why It Matters

A Technical Design Document (TDD) is a richer engineering artifact than a spec file. The TDD template contains 28 sections including TypeScript interface definitions, API endpoint contract tables, state machine schemas, component inventory trees, concrete test case matrices, migration phase tables, and operational runbook tables. [CODE-VERIFIED: research/06-tdd-template-structure.md]

The current extraction prompt instructs only 8 output sections (Functional Requirements, Non-Functional Requirements, Complexity Assessment, Architectural Constraints, Risk Inventory, Dependency Inventory, Success Criteria, Open Questions). Of the 28 TDD sections, only 5 are CAPTURED by the current extraction mandate, 15 are PARTIAL, and 8 are entirely MISSED. [CODE-VERIFIED: research/06-tdd-template-structure.md]

The 8 MISSED sections are not peripheral. They include:

- §7 Data Models — TypeScript interfaces, field tables, storage strategy
- §8 API Specifications — endpoint tables, request/response schemas, error tables, versioning policy
- §9 State Management — state shape, transitions, side effects
- §10 Component Inventory — route tables, component tables, ASCII hierarchy
- §15 Testing Strategy — test pyramid, unit/integration/E2E case tables
- §25 Operational Readiness — runbook tables, on-call expectations, capacity planning
- §26 Cost & Resource Estimation
- §28 Glossary

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

## §2 Current State Analysis

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

### 2.2 Prompt Layer: spec-specific language in prompts

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

**Stale documentation note:** The `prompts.py` module docstring states the executor appends `--file <path>` to subprocess calls. This is false. The executor uses `_embed_inputs()` for inline file embedding. [CODE-VERIFIED: research/01-executor-data-flow.md — stale documentation section]

### 2.3 Pure Python Analysis Modules: TDD Compatibility

Five pure-Python analysis modules are used by the anti-instinct step and structural audit hook. [CODE-VERIFIED: research/03-pure-python-modules.md]

| Module | What It Reads | TDD Compatible? | Key Finding |
|---|---|---|---|
| `spec_parser.py` | Any markdown text (frontmatter, tables, code blocks, sections) | Partial | Generic parsing works; `parse_frontmatter()` handles any YAML block; `extract_requirement_ids()` captures `FR-xxx` IDs present in TDD §5; `extract_function_signatures()` parses Python only — TypeScript `interface Foo {}` definitions NOT extracted; `DIMENSION_SECTION_MAP` encodes spec-oriented headings and may not map to TDD headings |
| `fidelity_checker.py` | FR sections in spec/TDD + `.py` source files in codebase | Partial | `FR-xxx` IDs in TDD §5 are processed identically to spec IDs; evidence search scans `.py` files only via AST — TDD requirements implemented in TypeScript or other languages produce blind spots; fail-open for ambiguous matches |
| `integration_contracts.py` | Any text (spec or TDD) | Mostly yes | Format-agnostic; 7 dispatch-pattern categories cover architecture prose; TDD §6 Architecture content (registries, DI, middleware, event listeners, handler maps) fits well; plain API endpoint tables (e.g., `GET /users`) do NOT trigger patterns unless described as wiring mechanisms |
| `fingerprint.py` | Any text (spec or TDD) for identifier extraction; roadmap text for coverage check | Mostly yes | Extracts backtick identifiers, code-block definitions (`def`/`class`), and ALL_CAPS constants; TDD TypeScript type names in backticks (e.g., `` `UserProfile` ``) are extracted; API endpoint paths (e.g., `` `/users/{id}` ``) do NOT match identifier regex; TDD's richer backtick identifier density may improve coverage ratio |
| `obligation_scanner.py` | Roadmap text only — never reads spec or TDD | N/A | Completely unaffected by input type; scans roadmap for obligation language only |

[CODE-VERIFIED: research/03-pure-python-modules.md]

**Key cross-reference:** `fidelity_checker.py`'s Python-only evidence scan is a structural limitation that intersects directly with TDD §7 (TypeScript interfaces) and §8 (API endpoints). TDD requirements implemented in TypeScript would register as unfound even when correctly implemented. [CODE-VERIFIED: research/03-pure-python-modules.md; cross-reference with research/06-tdd-template-structure.md §7 analysis]

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
| ANTI_INSTINCT_GATE | 3 | Conditional | Semantically spec-phrased failure messages ("spec code-level identifiers"); hypothesis that TDD's richer identifier density may improve pass rate (UNVERIFIED — see gaps) |
| TEST_STRATEGY_GATE | 9 | Conditional | `spec_source` only; all semantic checks (complexity class, interleave ratio, milestone counts, philosophy, policy) are workflow-specific and TDD-compatible |
| SPEC_FIDELITY_GATE | 6 | Conditional | Gate name and framing are semantically wrong for TDD; code-level checks (deviation counts, `tasklist_ready` consistency) are generic |
| WIRING_GATE | 16 | Yes | None — analyzes code wiring, independent of source document type |
| DEVIATION_ANALYSIS_GATE | 9 | No | `routing_update_spec` is explicitly spec-specific; `DEV-\d+` routing ID namespace assumes spec-deviation taxonomy; slip/intentional/pre-approved model assumes spec as remediation target |
| REMEDIATE_GATE | 6 | Yes | None |
| CERTIFY_GATE | 5 | Conditional | `_has_per_finding_table` hardcodes `F-\d+` row pattern; if TDD uses different finding ID format, relaxation required |
| TASKLIST_FIDELITY_GATE | 6 | Conditional | Structurally generic; semantically framed as source-fidelity; naming only |

[CODE-VERIFIED: research/04-gate-compatibility.md]

**`spec_source` is the most widespread blocker:** It appears in EXTRACT, GENERATE_A, GENERATE_B, MERGE, and TEST_STRATEGY gates. If TDD pipeline outputs emit `spec_source` using the TDD filename (which is technically valid as a provenance field), many gates can pass without change. The aliasing/renaming strategy is an unresolved implementation question. [CODE-VERIFIED: research/04-gate-compatibility.md — Gaps section]

**DEVIATION_ANALYSIS_GATE pre-existing bug:** The gate requires `ambiguous_count` in frontmatter, but the semantic check `_no_ambiguous_deviations` reads the field `ambiguous_deviations`. This is a field-name mismatch in the existing codebase, independent of TDD. [CODE-VERIFIED: research/04-gate-compatibility.md — stale/bug section; confirmed by QA spot-check in gaps-and-questions.md]

### 2.5 CLI Entry Points

Sources: `src/superclaude/cli/roadmap/commands.py`, `src/superclaude/cli/roadmap/models.py`, `src/superclaude/cli/tasklist/commands.py`, `src/superclaude/cli/tasklist/models.py`. [CODE-VERIFIED: research/05-cli-entry-points.md]

| Command | Current Flags | Missing Flag | Extension Point |
|---|---|---|---|
| `superclaude roadmap run <spec_file>` | `--agents`, `--output`, `--depth`, `--resume`, `--dry-run`, `--model`, `--max-turns`, `--debug`, `--no-validate`, `--allow-regeneration`, `--retrospective` | `--input-type [spec\|tdd]` | Additive `@click.option` in `roadmap/commands.py`; add `input_type` field to `RoadmapConfig` |
| `superclaude tasklist validate <output_dir>` | `--roadmap-file`, `--tasklist-dir`, `--model`, `--max-turns`, `--debug` | `--tdd-file` | Additive `@click.option` in `tasklist/commands.py`; add `tdd_file` field to `TasklistValidateConfig` |
| `superclaude roadmap validate <output_dir>` | `--agents`, `--model`, `--max-turns`, `--debug` | None required | `ValidateConfig` is artifact-only; no spec or TDD reference; no changes needed unless roadmap validation itself must reference TDD |

[CODE-VERIFIED: research/05-cli-entry-points.md]

**Established backward-compatible extension pattern:** `RoadmapConfig` already uses additive defaulted fields for version extensions — `convergence_enabled: bool = False` and `allow_regeneration: bool = False` were both added this way. New fields `input_type: Literal["spec", "tdd"] = "spec"` and `tdd_file: Path | None = None` follow the same pattern exactly. [CODE-VERIFIED: research/05-cli-entry-points.md, models.py]

**New fields are immediately available to executor:** `execute_roadmap(config: RoadmapConfig, ...)` receives the config instance directly. Adding fields to `RoadmapConfig` makes them accessible as `config.input_type` and `config.tdd_file` in executor code — but explicit usage logic must still be written. [CODE-VERIFIED: research/05-cli-entry-points.md]

**No feature flag framework exists:** The codebase has no `TODO`, `NotImplemented`, or feature-flag markers in these four files. Extension is purely additive via Click options and dataclass fields. [CODE-VERIFIED: research/05-cli-entry-points.md]

The call chain from CLI to pipeline is:

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
| CAPTURED | 5 | §5 Technical Requirements (FR/NFR tables), §18 Dependencies, §20 Risks & Mitigations, §22 Open Questions, §24 Release Criteria |
| PARTIAL | 15 | §1 Executive Summary, §2 Problem Statement, §3 Goals & Non-Goals, §4 Success Metrics, §6 Architecture, §11 User Flows, §12 Error Handling, §13 Security, §14 Observability, §16 Accessibility, §17 Performance Budgets, §19 Migration & Rollout Plan, §21 Alternatives Considered, §23 Timeline & Milestones, §27 References |
| MISSED | 8 | §7 Data Models (TypeScript interfaces + field tables), §8 API Specifications (endpoint tables + schemas), §9 State Management (state machine + transitions), §10 Component Inventory (route/component tables + ASCII hierarchy), §15 Testing Strategy (test pyramid + case tables), §25 Operational Readiness (runbook tables), §26 Cost & Resource Estimation, §28 Glossary |

[CODE-VERIFIED: research/06-tdd-template-structure.md]

The 8 MISSED sections contain the highest-value TDD artifacts for downstream task generation. §15 Testing Strategy is specifically noted as the highest-value miss for CLI sprint task generation, as test validation steps should be derived from concrete test case tables. §19 Migration & Rollout Plan is PARTIAL but contains rollout procedure ordering and rollback trigger logic that encodes task dependencies — this is structural content that the current extraction mandate does not capture. [CODE-VERIFIED: research/06-tdd-template-structure.md]

**TDD auto-detection signal:** The TDD template frontmatter contains `type: "📐 Technical Design Document"`. No equivalent `spec_type` field exists. The current CLI does not read frontmatter before constructing the extract prompt, so this signal is currently unused. [CODE-VERIFIED: research/06-tdd-template-structure.md]

**FR identifier compatibility:** TDD §5 uses `FR-001`, `FR-002` format. `spec_parser.extract_requirement_ids()` regex `r'\bFR-\d+(?:\.\d+)?\b'` matches these identically to spec FR IDs. [CODE-VERIFIED: research/06-tdd-template-structure.md, research/03-pure-python-modules.md]

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
        | [GEN-A]   [GEN-B]       (LLM — extraction.md only)
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

**Key observations from this diagram:**

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
| Tasklist entry point | `tasklist/commands.py`, `tasklist/models.py` | Add `--tdd-file` flag and `tdd_file` field | Optional / supplemental |

---

## Unverified Items (from gaps-and-questions.md)

The following items appeared in research gaps and MUST NOT be treated as verified facts in downstream synthesis documents.

| Gap ID | Item | Why It Matters | Handling |
|---|---|---|---|
| C-1 | `semantic_layer.py` (~400 lines) — not investigated; unknown if it reads spec content in the active pipeline | Could represent an additional spec_file touch point not captured in §2.1 | Treat as Unknown; flag as Open Question in implementation plan |
| C-2 | `structural_checkers.py` (~200 lines) — relationship to `spec_structural_audit.py` unknown | May add to the list of pure-Python spec-reading modules | Treat as Unknown; flag as Open Question |
| I-1 | `run_wiring_analysis(wiring_config, source_dir)` — does `wiring_config` reference `spec_file`? | Would add wiring-verify to the spec_file receiver list if confirmed | Exclude from definitive step count; note as open question |
| I-3 | `spec_source` rename strategy — alias both, rename only new outputs, or maintain backward compat? | Affects 5 gates and 2+ prompt builders; aliasing vs. rename is an implementation decision | Mark as open question in implementation plan |
| I-5 | ANTI_INSTINCT_GATE TDD performance — hypothesis that TDD's richer identifier density improves pass rate | Determines whether anti-instinct gate needs adjustment for TDD mode | Present as hypothesis with evidence rationale; do not assert as fact |

[SOURCE: gaps-and-questions.md, QA verdict: PASS — synthesis may proceed]
