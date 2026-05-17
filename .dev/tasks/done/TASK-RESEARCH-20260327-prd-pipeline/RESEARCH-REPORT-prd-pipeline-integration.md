# Technical Research Report: PRD as Supplementary Pipeline Input

**Date:** 2026-03-27
**Depth:** Standard
**Research files:** 5 codebase + 1 web research
**Scope:** src/superclaude/cli/roadmap/, src/superclaude/cli/tasklist/, src/superclaude/skills/, src/superclaude/commands/

---

## Table of Contents

1. [Problem Statement](#section-1-problem-statement)
2. [Current State Analysis](#section-2-current-state-analysis)
3. [Target State](#section-3-target-state)
4. [Gap Analysis](#section-4-gap-analysis)
5. [External Research Findings](#section-5-external-research-findings)
6. [Options Analysis](#section-6-options-analysis)
7. [Recommendation](#section-7-recommendation)
8. [Implementation Plan](#section-8-implementation-plan)
9. [Open Questions](#section-9-open-questions)
10. [Evidence Trail](#section-10-evidence-trail)

---

## Section 1: Problem Statement

### 1.1 Research Question

How should `--prd-file` be added as a supplementary input to the `superclaude roadmap` and `superclaude tasklist` CLI pipelines, such that PRD business context -- currently lost during TDD extraction -- flows into roadmap generation, scoring, fidelity checks, and test strategy?

### 1.2 Why This Matters

The TDD PRD Extraction Agent extracts exactly **5 of 28 PRD sections** (~18% coverage). The 23 sections that are dropped contain business rationale, user context, compliance requirements, risk analysis, customer journeys, edge cases, and API contracts that the pipeline currently cannot access.

Source: `05-prd-content-analysis.md`, Section 2.1 (lines 64-76) and Section 2.3 (lines 110-116).

**What the TDD extraction preserves:**

| # | PRD Section Extracted | Content |
|---|---|---|
| S12 | Scope Definition | In-scope / out-of-scope boundaries |
| S14 | Technical Requirements | FRs, NFRs, constraints |
| S19 | Success Metrics & Measurement | Metric, baseline, target, measurement method |
| S21 | Implementation Plan (Epics) | Epic ID, title, description |
| S21 | Implementation Plan (Stories) | User stories with acceptance criteria |

Source: `05-prd-content-analysis.md`, Section 2.1, lines 66-76.

**What the TDD extraction loses -- critical categories:**

| Category | Lost PRD Sections | Pipeline Impact |
|---|---|---|
| Business rationale | S1, S2, S3, S4, S5, S8, S9 | No "why" context for prioritization or phasing |
| User context | S6 (JTBD), S7 (Personas), S16 (UX), S22 (Journey) | No persona-driven sequencing, no E2E test scenarios |
| Compliance | S17 (Legal & Compliance) | Missing compliance NFRs entirely |
| Risk | S10 (Assumptions/Constraints), S20 (Risk Analysis) | No risk-aware milestone ordering |
| Edge cases & contracts | S23 (Error Handling), S25 (API Contracts) | No edge-case test inputs, no contract test data |

Source: `05-prd-content-analysis.md`, Section 2.2, lines 80-108.

### 1.3 What Triggered This Investigation

The roadmap extraction pipeline has **zero steps** for business rationale, personas, stakeholder needs, or success metrics beyond what the TDD passes through. The pipeline's extraction step (`build_extract_prompt` and `build_extract_prompt_tdd` in `src/superclaude/cli/roadmap/prompts.py`) accepts only `spec_file` and `retrospective_content` -- there is no parameter for PRD content. [CODE-VERIFIED: `01-roadmap-cli-integration-points.md`, Section 4, lines 177-180]

The `RoadmapConfig` dataclass has a `tdd_file` field (line 115 of `src/superclaude/cli/roadmap/models.py`) that is dead code -- never referenced by the executor or exposed as a CLI flag. This confirms that supplementary input wiring was attempted but never completed for the roadmap pipeline. [CODE-VERIFIED: `01-roadmap-cli-integration-points.md`, Section 1, line 25]

### 1.4 Scope of the Gap

The roadmap pipeline has 10 prompt builders. None accept PRD content:

| Prompt Builder | Current Supplementary Params | PRD Gap |
|---|---|---|
| `build_extract_prompt` (line 82) | `retrospective_content` | No PRD |
| `build_extract_prompt_tdd` (line 161) | `retrospective_content` | No PRD |
| `build_generate_prompt` (line 288) | None | No PRD |
| `build_diff_prompt` (line 338) | None | No PRD |
| `build_debate_prompt` (line 363) | None | No PRD |
| `build_score_prompt` (line 390) | None | No PRD |
| `build_merge_prompt` (line 416) | None | No PRD |
| `build_spec_fidelity_prompt` (line 448) | None | No PRD |
| `build_wiring_verification_prompt` (line 528) | None | No PRD |
| `build_test_strategy_prompt` (line 586) | None | No PRD |

Source: `02-prompt-enrichment-mapping.md`, lines 96-101, 147-152, 194-196, 247-249, 288-295, 331-337, 380-386, 426-431, 477-482, 496-501. All signatures marked [CODE-VERIFIED].

The tasklist pipeline has the same gap: `build_tasklist_fidelity_prompt` accepts `tdd_file` but not `prd_file`. Source: `03-tasklist-integration-points.md`, Section 4, lines 183-190.

---


## Section 2: Current State Analysis

### 2.1 Roadmap CLI Structure

**Source:** `01-roadmap-cli-integration-points.md` (all claims [CODE-VERIFIED] unless noted)

The roadmap CLI lives in `src/superclaude/cli/roadmap/` and consists of four layers:

```
src/superclaude/cli/roadmap/
    models.py      -- RoadmapConfig dataclass (line 95)
    commands.py    -- Click CLI commands: run (line 32), validate (line 247)
    executor.py    -- Pipeline orchestrator: _build_steps (line 843), execute_roadmap (line 1728)
    prompts.py     -- 10 prompt builder functions (lines 82-629)
    gates.py       -- Gate definitions for step validation
```

#### Models Layer

`RoadmapConfig` extends `PipelineConfig` and defines these supplementary input fields:

| Field | Type | Line | Status |
|---|---|---|---|
| `spec_file` | `Path` | 102 | Active -- primary input |
| `retrospective_file` | `Path \| None` | 111 | Active -- optional supplementary input |
| `input_type` | `Literal["auto","tdd","spec"]` | 114 | Active -- controls detection routing |
| `tdd_file` | `Path \| None` | 115 | **DEAD CODE** -- no CLI flag, no executor reference |

Source: `01-roadmap-cli-integration-points.md`, Section 1, lines 16-24.

The `tdd_file` field is dead code: it exists on the model but has no `--tdd-file` CLI flag and is never read by the executor. Source: `01-roadmap-cli-integration-points.md`, line 25 and line 54. [CODE-VERIFIED]

#### Commands Layer

The `run` command (line 32) accepts these supplementary CLI flags:

| Flag | Line | Type | Notes |
|---|---|---|---|
| `--retrospective` | 96-104 | `click.Path(exists=False)` | Uses `exists=False` -- missing file is not an error |
| `--input-type` | 106-110 | `click.Choice(["auto","tdd","spec"])` | Controls detection routing |

No `--tdd-file` flag exists. No `--prd-file` flag exists. Source: `01-roadmap-cli-integration-points.md`, Section 2, lines 47-53.

The `validate` command (line 247) has no supplementary input flags at all. Source: `01-roadmap-cli-integration-points.md`, line 77-79.

#### Executor Layer

`_build_steps()` (lines 843-1012) constructs the pipeline as a list of `Step` objects. The current supplementary input handling uses the retrospective pattern: content is loaded as a string and passed into the prompt builder as a parameter -- NOT added to the `inputs` file list. Source: `01-roadmap-cli-integration-points.md`, lines 106-108.

Pipeline steps and their PRD relevance:

| Step | ID | Prompt Builder | PRD Relevance |
|---|---|---|---|
| 1 | `extract` | `build_extract_prompt` / `build_extract_prompt_tdd` | **HIGH** |
| 2a/2b | `generate-{agent}` | `build_generate_prompt` | LOW (uses extraction output) |
| 3 | `diff` | `build_diff_prompt` | NONE |
| 4 | `debate` | `build_debate_prompt` | NONE |
| 5 | `score` | `build_score_prompt` | NONE |
| 6 | `merge` | `build_merge_prompt` | NONE |
| 7 | `anti-instinct` | (non-LLM deterministic) | POSSIBLE |
| 8 | `test-strategy` | `build_test_strategy_prompt` | LOW |
| 8b | `spec-fidelity` | `build_spec_fidelity_prompt` | **MEDIUM** |
| 9 | `wiring-verification` | `build_wiring_verification_prompt` | NONE |

Source: `01-roadmap-cli-integration-points.md`, Section 3, lines 116-127.

**Data flow (current state):**

```
                       spec_file (Path)
                            |
                            v
    +--[ detect_input_type() ]--+     retrospective_file (Path|None)
    |                           |              |
    v                           v              v
build_extract_prompt    build_extract_prompt_tdd
    |                           |       (retrospective_content loaded as str)
    |                           |
    v                           v
  extraction.md -------> build_generate_prompt (agent_a)
                  \----> build_generate_prompt (agent_b)
                              |          |
                              v          v
                        roadmap_a    roadmap_b
                              |          |
                              +----+-----+
                                   |
                              diff -> debate -> score -> merge
                                                          |
                                                          v
                                                    merged_roadmap
                                                     /    |    \
                                                    /     |     \
                                       anti-instinct  test-strat  spec-fidelity
                                                              \      |
                                                               v     v
                                                        wiring-verification
```

No PRD input enters this flow at any point. Source: `01-roadmap-cli-integration-points.md`, lines 163-169; `02-prompt-enrichment-mapping.md`, lines 543-566.

#### Stale Documentation (Roadmap)

| Location | Issue | Status |
|---|---|---|
| `models.py` line 98-99 | `RoadmapConfig` docstring omits `convergence_enabled`, `allow_regeneration`, `input_type`, `tdd_file` | [CODE-CONTRADICTED] |
| `executor.py` line 987 | Comment says "Step 8" for spec-fidelity; docstring says "9-step pipeline" but there are 10+ step entries | [CODE-CONTRADICTED] |

Source: `01-roadmap-cli-integration-points.md`, Section "Stale Documentation Found", lines 254-258.

---

### 2.2 Tasklist CLI Structure

**Source:** `03-tasklist-integration-points.md` (all claims [CODE-VERIFIED] unless noted)

The tasklist CLI lives in `src/superclaude/cli/tasklist/` and follows the same 4-layer pattern:

```
src/superclaude/cli/tasklist/
    models.py      -- TasklistValidateConfig dataclass (26 lines)
    commands.py    -- Click CLI: validate command (130 lines)
    executor.py    -- Pipeline step builder (~270 lines)
    prompts.py     -- build_tasklist_fidelity_prompt (126 lines)
```

#### TDD Integration Pattern (Reference Implementation)

The tasklist pipeline has a complete, working `--tdd-file` integration. This is the reference pattern for PRD integration:

| Layer | File | Line(s) | What It Does |
|---|---|---|---|
| CLI flag | `commands.py` | 61-66 | `--tdd-file` option, `click.Path(exists=True, path_type=Path)` |
| Config field | `models.py` | 25 | `tdd_file: Path \| None = None` on `TasklistValidateConfig` |
| Input assembly | `executor.py` | 193-194 | `if config.tdd_file is not None: all_inputs.append(config.tdd_file)` |
| Prompt builder kwarg | `executor.py` | 202 | `tdd_file=config.tdd_file` passed to prompt builder |
| Prompt parameter | `prompts.py` | 20 | `tdd_file: Path \| None = None` on `build_tasklist_fidelity_prompt` |
| Conditional block | `prompts.py` | 110-123 | Appends `## Supplementary TDD Validation` section with 3 checks |

Source: `01-roadmap-cli-integration-points.md`, Section 5, lines 226-232; `03-tasklist-integration-points.md`, Sections 1-4.

**End-to-end wiring:**

```
CLI flag (commands.py)
  |
  v  click.Path(exists=True) -> Path | None
Config field (models.py)
  |
  v  TasklistValidateConfig.tdd_file
Executor (executor.py)
  |
  +--> all_inputs.append(config.tdd_file)     [file content embedding]
  |
  +--> build_tasklist_fidelity_prompt(         [prompt instruction injection]
  |        tdd_file=config.tdd_file)
  v
Prompt builder (prompts.py)
  |
  v  if tdd_file is not None: base += "## Supplementary TDD Validation ..."
```

Source: `03-tasklist-integration-points.md`, Section 5, lines 275-295.

The TDD supplementary block in `prompts.py` (lines 110-123) checks 3 things: testing strategy coverage (TDD S15), rollback procedures (TDD S19), and component inventory (TDD S10). All deviations flagged as MEDIUM severity. Source: `03-tasklist-integration-points.md`, Section 4, lines 193-209.

---

### 2.3 Prompt Builder Inventory

**Source:** `02-prompt-enrichment-mapping.md` (all signatures [CODE-VERIFIED])

File: `src/superclaude/cli/roadmap/prompts.py`

| # | Function | Line | Current Params | Return Pattern | PRD Value |
|---|---|---|---|---|---|
| 1 | `build_extract_prompt` | 82 | `spec_file`, `retrospective_content` | `base = (...); return base + block` | HIGH (P1) |
| 2 | `build_extract_prompt_tdd` | 161 | `spec_file`, `retrospective_content` | `base = (...); return base + block` | MEDIUM (P2) |
| 3 | `build_generate_prompt` | 288 | `agent`, `extraction_path` | Single `return (...)` expression | HIGH (P1) |
| 4 | `build_diff_prompt` | 338 | `variant_a_path`, `variant_b_path` | Single `return (...)` expression | LOW (P3) |
| 5 | `build_debate_prompt` | 363 | `diff_path`, `variant_a_path`, `variant_b_path`, `depth` | Single `return (...)` expression | LOW (P3) |
| 6 | `build_score_prompt` | 390 | `debate_path`, `variant_a_path`, `variant_b_path` | Single `return (...)` expression | MEDIUM (P2) |
| 7 | `build_merge_prompt` | 416 | `base_selection_path`, `variant_a_path`, `variant_b_path`, `debate_path` | Single `return (...)` expression | LOW (P3) |
| 8 | `build_spec_fidelity_prompt` | 448 | `spec_file`, `roadmap_path` | Single `return (...)` expression | HIGH (P1) |
| 9 | `build_wiring_verification_prompt` | 528 | `merge_file`, `spec_source` | Single `return (...)` expression | NONE (skip) |
| 10 | `build_test_strategy_prompt` | 586 | `roadmap_path`, `extraction_path` | Single `return (...)` expression | HIGH (P1) |

Source: `02-prompt-enrichment-mapping.md`, lines 96-101, 147-152, 194-196, 247-249, 288-295, 331-337, 380-386, 426-431, 477-482, 496-501.

**Refactoring requirement:** 7 of 10 builders use a single `return (...)` expression. Adding conditional PRD blocks requires refactoring these to `base = (...); if prd_file: base += ...; return base + _OUTPUT_FORMAT_BLOCK`. Only `build_extract_prompt` and `build_extract_prompt_tdd` already use the `base` pattern. Source: `02-prompt-enrichment-mapping.md`, lines 574-592.

File: `src/superclaude/cli/tasklist/prompts.py`

| Function | Line | Current Params | PRD Value |
|---|---|---|---|
| `build_tasklist_fidelity_prompt` | 17 | `roadmap_file`, `tasklist_dir`, `tdd_file` | HIGH |

Source: `03-tasklist-integration-points.md`, Section 4, lines 183-190.

---

### 2.4 Skill and Reference Layer

**Source:** `04-skill-reference-layer.md` (verification status per-claim)

Four reference/skill documents contain TDD-conditional content that would need PRD parallels:

| File | Lines | TDD Content | PRD Status |
|---|---|---|---|
| `extraction-pipeline.md` | 143-207 | Steps 9-15: TDD-specific extraction | No PRD equivalent exists |
| `scoring.md` | 7-108 | TDD 7-factor scoring formula | No PRD equivalent exists |
| `tasklist SKILL.md` | 140-196 | Sections 4.1a (TDD context) and 4.4a (TDD task generation) | No PRD equivalent exists |
| `spec-panel.md` | 32-405 | Steps 6a-6b (TDD input detection) and TDD output modes | No PRD equivalent exists |

Source: `04-skill-reference-layer.md`, Sections 1-4.

**Contradiction between skill docs and CLI code:**

| Skill Doc Claim | CLI Code Reality | Status |
|---|---|---|
| extraction-pipeline.md: TDD detection uses 3-rule boolean OR | `executor.py` L57-117: uses weighted scoring system with threshold >= 5 | [CODE-CONTRADICTED] |
| tasklist SKILL.md: uses `--spec` flag | `tasklist/commands.py` L62-65: uses `--tdd-file` flag | [CODE-CONTRADICTED] |
| tasklist SKILL.md S4.4a: 7 task generation patterns from TDD | `tasklist/prompts.py` L110-123: only 3 validation checks implemented | [CODE-CONTRADICTED] |
| scoring.md: TDD 7-factor formula | No `scoring.py` in CLI -- scoring is inference-based only | [UNVERIFIED] |

Source: `04-skill-reference-layer.md`, Section 7, lines 276-283.

**Design note:** `spec-panel.md` is purely inference-based (no programmatic CLI backing). PRD additions to it update only the protocol doc, not Python code. Source: `04-skill-reference-layer.md`, line 269.

---

### 2.5 PRD Content Structure

**Source:** `05-prd-content-analysis.md` (all claims [DOC-SOURCED] from `src/superclaude/skills/prd/SKILL.md` lines 996-1085 unless noted)

The PRD template defines 28 sections plus appendices. Grouped by content type:

| Content Type | PRD Sections |
|---|---|
| Strategic context | S1 (Executive Summary), S4 (Product Vision) |
| Business rationale | S2 (Problem Statement), S3 (Background), S5 (Business Context), S8 (Value Prop Canvas) |
| Business metrics | S5 (Business Context -- TAM/SAM/SOM, KPIs), S19 (Success Metrics) |
| User needs | S6 (JTBD), S7 (Personas), S16 (UX Requirements), S22 (Customer Journey) |
| Market intelligence | S9 (Competitive Analysis) |
| Risk/scope | S10 (Assumptions & Constraints), S12 (Scope Definition) |
| Technical/org | S11 (Dependencies) |
| Technical spec | S14 (Technical Requirements), S15 (Technology Stack), S23 (Error Handling), S25 (API Contracts) |
| Compliance | S17 (Legal & Compliance) |
| Business spec | S18 (Business Requirements) |
| Implementation spec | S21 (Implementation Plan) |
| UX/design | S24 (User Interaction & Design) |
| Process | S13 (Open Questions), S26 (Contributors), S28 (Maintenance) |
| Reference | S27 (Related Resources), Appendices |

Source: `05-prd-content-analysis.md`, Section 1, lines 22-52.

For Feature/Component PRDs (vs. Product PRDs), sections S5, S8, S9, S17, S18 are typically N/A or abbreviated. Source: `05-prd-content-analysis.md`, line 56.

---

### 2.6 TDD Extraction Coverage

**Source:** `05-prd-content-analysis.md`, Section 2 (lines 60-116). TDD extraction agent source: `src/superclaude/skills/tdd/SKILL.md` lines 944-978 [DOC-SOURCED].

**Extracted (5 sections, ~18% coverage):**

| Extraction Output | Source PRD Section | Content |
|---|---|---|
| Epics | S21.1 | Epic ID, title, description |
| User Stories & AC | S21.1 | Stories with acceptance criteria, grouped by epic |
| Success Metrics | S19 | Metric, baseline, target, measurement method |
| Technical Requirements | S14 | Flat list with type labels (functional, NFR, constraint) |
| Scope Boundaries | S12 | In-scope / out-of-scope lists |

**Not extracted (23 sections, ~82% of PRD content):**

| Tier | Count | Sections | Pipeline Value |
|---|---|---|---|
| Tier 1 (High) | 9 | S6, S7, S10, S11, S17, S20, S22, S23, S25 | Direct enrichment to extract, generate, test-strategy, spec-fidelity |
| Tier 2 (Medium) | 6 | S2, S5, S8, S13, S16, S24 | Prioritization context, UX test criteria, risk awareness |
| Tier 3 (Low) | 6 | S1, S3, S4, S9, S15, S18 | General framing, tie-breaking, often redundant |
| No value | 3 | S26, S27, S28 | Process metadata only |

Source: `05-prd-content-analysis.md`, Section 4.1, lines 196-236.

**Recommended minimal expansion:** Add Tier 1 sections (9 additional) to raise extraction coverage from ~18% to ~50% (14 of 28 sections). Source: `05-prd-content-analysis.md`, Section 4.2, lines 238-245.

**PRD sections with highest cross-step impact** (referenced by 3+ pipeline steps):

| PRD Section | Pipeline Steps That Benefit |
|---|---|
| S7 (User Personas) | generate, test-strategy, spec-fidelity |
| S17 (Legal & Compliance) | extract, test-strategy, spec-fidelity |
| S10 (Assumptions & Constraints) | extract, generate, spec-fidelity |
| S6 (JTBD) | extract, generate, spec-fidelity |
| S22 (Customer Journey Map) | test-strategy |
| S20 (Risk Analysis) | generate, debate, score |

Source: `05-prd-content-analysis.md`, Section 3.3, lines 177-188; `02-prompt-enrichment-mapping.md`, Summary section, lines 615-626.

---


## Section 3: Target State

### 3.1 Desired Behavior

The `--prd-file` flag provides **supplementary PRD enrichment** across both the roadmap and tasklist CLI pipelines. It follows the established TDD integration pattern: an optional file path is accepted via CLI flag, resolved to an absolute path, stored on the pipeline config dataclass, passed into the executor's step builder, appended to step input lists for file embedding, and forwarded as a keyword argument to prompt builders that conditionally append PRD-aware instruction blocks.

PRD content enriches the pipeline by injecting business context ("why/who") that specification and TDD files ("what/how") do not carry. The enrichment is advisory -- PRD content informs prioritization, fidelity checks, and test strategy but never overrides technical dependency ordering or specification authority.

**End-to-end data flow (both pipelines):**

```
CLI invocation
  |
  v
--prd-file <path>                    click.Path(exists=True, path_type=Path)
  |
  v
Config dataclass                     prd_file: Path | None = None
  |
  v
Executor _build_steps()
  |
  +---> step.inputs.append(prd_file) file content embedded via _embed_inputs()
  |
  +---> prompt_builder(prd_file=...) conditional supplementary block activated
  |
  v
Claude subprocess receives:
  - Embedded PRD file content (fenced code block in prompt)
  - Supplementary PRD instruction block (numbered checks + severity guidance)
```

**Roadmap pipeline enrichment targets (by step):**

| Step | Prompt Builder | PRD Enrichment | Priority |
|------|---------------|----------------|----------|
| extract | `build_extract_prompt` | Business objectives, personas, scope boundaries, compliance, JTBD | P1 |
| extract (TDD mode) | `build_extract_prompt_tdd` | Personas, compliance, success metrics (subset of above) | P2 |
| generate-A/B | `build_generate_prompt` | Value-based phasing, persona-driven sequencing, compliance gates, scope guardrails | P1 |
| diff | `build_diff_prompt` | Business alignment comparison (indirect) | P3 |
| debate | `build_debate_prompt` | Business value evaluation criterion | P3 |
| score | `build_score_prompt` | Business value delivery, persona coverage, compliance alignment scoring | P2 |
| merge | `build_merge_prompt` | Persona and metric preservation verification | P3 |
| test-strategy | `build_test_strategy_prompt` | Persona acceptance tests, journey E2E tests, KPI validation, compliance test category, edge cases | P1 |
| spec-fidelity | `build_spec_fidelity_prompt` | Persona coverage (dim 12), metric traceability (dim 13), compliance coverage (dim 14), scope boundary enforcement (dim 15) | P1 |
| wiring-verification | `build_wiring_verification_prompt` | None -- structural code verification, no PRD relevance | Skip |

**Tasklist pipeline enrichment targets:**

| Step | Prompt Builder | PRD Enrichment | Priority |
|------|---------------|----------------|----------|
| tasklist-fidelity | `build_tasklist_fidelity_prompt` | Persona flow coverage, KPI instrumentation tasks, compliance tasks, UX flow alignment | P1 |

**PRD sections most referenced across all prompt blocks:**

| PRD Section | # of Prompt Builders Referencing It |
|-------------|-------------------------------------|
| S7: User Personas | 8 of 9 |
| S19: Success Metrics | 7 of 9 |
| S17: Legal & Compliance | 6 of 9 |
| S12: Scope Definition | 4 of 9 |
| S22: Customer Journey Map | 3 of 9 |
| S6: JTBD | 2 of 9 (but highest value in extract) |

### 3.2 Success Criteria

| # | Criterion | Verification Method |
|---|-----------|-------------------|
| SC-1 | **Backward compatible**: All pipeline commands produce identical output when `--prd-file` is not provided | Run existing test suite; all tests pass without modification |
| SC-2 | **No new mode**: `--input-type` choices remain `["auto", "tdd", "spec"]`; `detect_input_type()` is unchanged | Code inspection; no new enum values or detection signals added |
| SC-3 | **PRD sections accessible in prompts**: When `--prd-file` is provided, the embedded PRD file content appears in the Claude subprocess prompt for targeted steps | Integration test: invoke pipeline with `--prd-file`, inspect generated prompt for `## Supplementary PRD` heading |
| SC-4 | **Both-files coexistence**: `--prd-file` and `--tdd-file` (tasklist) or `--retrospective` (roadmap) can be provided simultaneously without conflict | Test: provide both flags; verify both supplementary blocks appear in prompt |
| SC-5 | **File validation**: `--prd-file` with a nonexistent path fails with Click's standard error before pipeline execution | Test: invoke with nonexistent path; verify Click error |
| SC-6 | **Advisory guardrail in all prompt blocks**: Every supplementary PRD block includes the phrase "do NOT treat PRD content as hard requirements" | Grep prompt builder source for guardrail text |
| SC-7 | **TDD pattern fidelity**: The `--prd-file` integration follows the exact 4-layer wiring pattern demonstrated by `--tdd-file` in the tasklist pipeline | Code review against `src/superclaude/cli/tasklist/` reference implementation |

### 3.3 Constraints

| # | Constraint | Rationale | Source |
|---|-----------|-----------|--------|
| C-1 | **Must follow TDD integration pattern** | The `--tdd-file` wiring in `src/superclaude/cli/tasklist/` is the established, tested pattern for supplementary inputs. | Files 01, 03 |
| C-2 | **No `detect_input_type()` changes** | PRD is supplementary context, not a primary input mode. | File 01 (executor.py L59-117) |
| C-3 | **No new `--input-type` choices** | `Literal["auto", "tdd", "spec"]` remains unchanged. | File 01 (models.py L114) |
| C-4 | **PRD file must exist when specified** | Use `click.Path(exists=True)` (not `exists=False` like `--retrospective`). | File 01 (commands.py pattern analysis) |
| C-5 | **No prompt builders for wiring-verification gain `prd_file`** | Zero PRD relevance for structural code verification. | File 02 (builder analysis) |
| C-6 | **Supplementary blocks must not restructure phases** | PRD context annotates but does not dictate technical ordering. Industry consensus: engineering roadmap = How/When; PRD provides Why annotations. | web-01 (Section 3.1, 3.2) [EXTERNAL] |
| C-7 | **`prd_file` must be wired end-to-end** | The existing `tdd_file` on `RoadmapConfig` is dead code. `prd_file` must not replicate this mistake. | File 01 (gap finding) |
| C-8 | **PRD content is advisory** | All supplementary prompt blocks must include guardrail: "do NOT treat PRD content as hard requirements unless also stated in the specification/TDD." | File 02 (design decision #1) |

---


## Section 4: Gap Analysis

### 4.1 Gap Analysis Table

| # | Gap | Current State | Target State | Severity |
|---|-----|--------------|--------------|----------|
| **G-1** | **Model field missing: `RoadmapConfig.prd_file`** | `RoadmapConfig` has `tdd_file: Path \| None = None` at L115 but NO `prd_file` field. `tdd_file` is dead code. | Add `prd_file: Path \| None = None` after `tdd_file` at L115. | HIGH |
| **G-2** | **Model field missing: `TasklistValidateConfig.prd_file`** | `TasklistValidateConfig` has `tdd_file` at L25 but NO `prd_file` field. | Add `prd_file: Path \| None = None` after `tdd_file` at L25. | HIGH |
| **G-3** | **CLI flag missing: roadmap `run` lacks `--prd-file`** | `commands.py` has `--retrospective` and `--input-type` but no `--prd-file`. | Add `@click.option("--prd-file", type=click.Path(exists=True, path_type=Path), ...)`. | HIGH |
| **G-4** | **CLI flag missing: tasklist `validate` lacks `--prd-file`** | `commands.py` has `--tdd-file` but no `--prd-file`. | Add `@click.option("--prd-file", ...)` after `--tdd-file`. | HIGH |
| **G-5** | **Executor wiring missing: roadmap `_build_steps()` does not pass `prd_file`** | `_build_steps()` (L843-1012) passes `retrospective_content` but has no `prd_file` handling. | Pass `prd_file=config.prd_file` to prompt builder calls at 10 call sites. Add to `step.inputs` for P1/P2 steps. | HIGH |
| **G-6** | **Executor wiring missing: tasklist `_build_steps()` does not pass `prd_file`** | `_build_steps()` (L188-211) handles `tdd_file` but not `prd_file`. | Add `prd_file` to `all_inputs` and pass to prompt builder. | HIGH |
| **G-7** | **Prompt enrichment missing: `build_extract_prompt`** | Signature has `retrospective_content` but no `prd_file`. Already uses `base = (...)` pattern. | Add `prd_file` param and 5-check supplementary block. | HIGH |
| **G-8** | **Prompt enrichment missing: `build_extract_prompt_tdd`** | Same gap as G-7 for TDD extraction mode. Already uses `base = (...)` pattern. | Add `prd_file` param and 3-check supplementary block. | MEDIUM |
| **G-9** | **Prompt enrichment missing: `build_generate_prompt`** | Returns single concatenated expression. No supplementary inputs. | Add `prd_file` param + refactor to base pattern + 4-check block. | HIGH |
| **G-10** | **Prompt enrichment missing: `build_spec_fidelity_prompt`** | Returns single expression. Has 11 existing comparison dimensions. | Add `prd_file` param + refactor + dimensions 12-15. | HIGH |
| **G-11** | **Prompt enrichment missing: `build_test_strategy_prompt`** | Returns single expression. No supplementary inputs. | Add `prd_file` param + refactor + 5-check block. | HIGH |
| **G-12** | **Prompt enrichment missing: `build_score_prompt`** | Returns single expression. No supplementary inputs. | Add `prd_file` param + refactor + 3 scoring dimensions. | MEDIUM |
| **G-13** | **Prompt enrichment missing: diff, debate, merge prompts** | Three builders (L338, L363, L416) return single expressions. | Add `prd_file` param + minimal blocks. | LOW |
| **G-14** | **Prompt enrichment missing: `build_tasklist_fidelity_prompt`** | Signature has `tdd_file` but no `prd_file`. Already uses base pattern. | Add `prd_file` param + 4-check supplementary block. | HIGH |
| **G-15** | **Skill layer missing: `extraction-pipeline.md` has no PRD content** | TDD extraction steps (9-15) exist, no PRD equivalent. | Add PRD-supplementary extraction guidance. | MEDIUM |
| **G-16** | **Skill layer missing: `scoring.md` has no PRD scoring guidance** | TDD 7-factor formula exists, no PRD equivalent. | Add PRD type match entry, use standard 5-factor formula. | LOW |
| **G-17** | **Skill layer missing: tasklist `SKILL.md` has no PRD context** | Sections 4.1a and 4.4a (TDD) exist, no PRD equivalents. | Add Sections 4.1b and 4.4b for PRD. | MEDIUM |
| **G-18** | **PRD content mapping: only 5 of 28 sections reach pipeline** | TDD extraction covers ~18%. 23 sections lost. | With `--prd-file`, pipeline gains access to all 28 sections. Prompt blocks prioritize 9 Tier-1 sections, raising effective coverage to ~50%. | HIGH |
| **G-19** | **Prompt builder refactoring: 7 of 9 builders need base pattern** | 7 builders use single `return (...)` expression pattern. | Refactor to `base = (...); if prd_file: ...; return base + block`. | MEDIUM |
| **G-20** | **`spec-panel.md` has no PRD input handling** | Step 6a-6b for TDD exist, no PRD equivalent. | Add Steps 6c-6d and PRD output section. | LOW |

### 4.2 Gap Severity Distribution

| Severity | Count | Gaps |
|----------|-------|------|
| HIGH | 12 | G-1, G-2, G-3, G-4, G-5, G-6, G-7, G-9, G-10, G-11, G-14, G-18 |
| MEDIUM | 5 | G-8, G-12, G-15, G-17, G-19 |
| LOW | 3 | G-13, G-16, G-20 |

### 4.3 Implementation Dependency Map

```
                    G-1 (RoadmapConfig.prd_file)
                   /                              \
                  v                                v
        G-3 (roadmap --prd-file)          G-5 (roadmap executor wiring)
                  |                        /    |    |    |    \
                  v                       v     v    v    v     v
            config_kwargs          G-7  G-8  G-9  G-10  G-11  (+ G-12, G-13)
                                 extract  tdd  gen  fid  test   score/diff/etc

                    G-2 (TasklistConfig.prd_file)
                   /                              \
                  v                                v
        G-4 (tasklist --prd-file)          G-6 (tasklist executor wiring)
                  |                                |
                  v                                v
            config with prd_file             G-14 (tasklist prompt)


        G-19 (refactoring) --blocks--> G-9, G-10, G-11, G-12, G-13
                                       (builders requiring base pattern)

        G-15, G-16, G-17, G-20 (skill/reference docs) -- independent of code gaps
```

### 4.4 Contradictions and Discrepancies Found

| # | Contradiction | Sources | Resolution |
|---|--------------|---------|------------|
| 1 | File 01 says "9-step pipeline" but File 05 counts 11 step entries. | File 01 (executor.py docstring), File 05 (Section 3.1) | Both correct at different scopes. `_build_steps()` returns 9 `Step` objects; the full pipeline includes non-LLM anti-instinct and post-pipeline certify for 11 total. Cosmetic discrepancy. |
| 2 | File 04 originally proposed extending `detect_input_type()` for PRD mode, contradicting File 01. | File 04 (original), File 01 (Section 3) | Resolved in QA fix-cycle 1. PRD is supplementary only. No `detect_input_type()` changes. |
| 3 | File 02 proposes PRD enrichment for ALL 9 non-wiring builders. File 05 recommends only steps that need it. | File 02 (full mapping), File 05 (Section 4.3) | Not a true contradiction. Both agree P3 has diminishing returns. Recommendation: add `prd_file` parameter to all 9 for API consistency, but only embed the PRD file in `step.inputs` for P1/P2 steps. |
| 4 | `extraction-pipeline.md` TDD detection describes 3-rule boolean OR. Code uses weighted scoring. | File 04 (Section 1.1), File 01 (Section 3) | Stale doc. Code's scoring-based approach is authoritative. [CODE-CONTRADICTED] |
| 5 | Tasklist `SKILL.md` references `--spec` flag. CLI uses `--tdd-file`. | File 04 (Section 3.1) | Expected divergence: SKILL.md is inference-based protocol; CLI is programmatic. [CODE-CONTRADICTED, expected] |

### 4.5 Open Questions Deferred to Implementation

| # | Question | Recommendation | Source |
|---|----------|---------------|--------|
| 1 | Should the dead `tdd_file` on `RoadmapConfig` be wired up or removed? | Separate tech debt task. | File 01 |
| 2 | Should `--prd-file` be added to `superclaude roadmap validate`? | Defer. Add after `run` integration is proven. | File 01 |
| 3 | PRD template section numbering -- cross-validate against actual template? | Yes -- verify before finalizing prompt block section references. | gaps-and-questions.md Q#7 |
| 4 | Token budget impact of embedding full PRD in multiple steps? | Cap at P1/P2 steps only. `_EMBED_SIZE_LIMIT` (100KB) guards against oversized prompts. | File 03, File 05 |
| 5 | PRD staleness relative to TDD? | Defer consistency check to future enhancement. | File 05 |
| 6 | Circular dependency: PRD skill output vs. pipeline input expectations? | Define schema contract. Not blocking for initial implementation. | File 04 |

---


## Section 5: External Research Findings

> **EXTERNAL CONTEXT NOTICE**: Every finding below is drawn from publicly available industry sources. No finding should be treated as a codebase requirement without internal validation.

### 5.1 PRD Structure and Engineering-Relevant Sections

**Sources:** [Aha! - PRD Templates](https://www.aha.io/roadmapping/guide/requirements-management/what-is-a-good-product-requirements-document-template), [Perforce - How to Write a PRD](https://www.perforce.com/blog/alm/how-write-product-requirements-document-prd), [Productboard - PRD Guide](https://www.productboard.com/blog/product-requirements-document-guide/), [Chisel - How to Write PRD Using AI](https://chisellabs.com/blog/how-to-write-prd-using-ai/), [Kuse.ai - PRD Document Template 2025](https://www.kuse.ai/blog/tutorials/prd-document-template-in-2025-how-to-write-effective-product-requirements)

Modern PRDs have converged on a leaner, iterative format organized around hierarchical requirement structures: themes (strategic goals, multi-quarter), initiatives/epics (large projects), and features/user stories (specific functionality). The sections with highest engineering roadmap value are: Purpose and Goals, User Needs/Personas, Prioritization Constraints, Success Metrics/KPIs, and Timeline/Release Plan. AI-assisted PRD generation (2025-2026) has made PRDs increasingly machine-parseable.

**Relevance:** HIGH | **Relationship:** SUPPORTS existing design direction -- PRD sections provide the "why" layer that TDD/spec inputs lack.

### 5.2 Value-Based Prioritization Frameworks

**Sources:** [Fygurs - Prioritization Frameworks Compared](https://www.fygurs.com/blog/product-prioritization-frameworks-compared), [Centercode - RICE vs WSJF](https://www.centercode.com/blog/rice-vs-wsjf-prioritization-framework), [Atlassian - Prioritization Frameworks](https://www.atlassian.com/agile/product-management/prioritization-framework), [PPM Express - 13 Prioritization Techniques](https://www.ppm.express/blog/13-prioritization-techniques), [AltexSoft - Popular Prioritization Techniques](https://www.altexsoft.com/blog/most-popular-prioritization-techniques-and-methods-moscow-rice-kano-model-walking-skeleton-and-others/), [ProductLift - 10 Prioritization Frameworks 2026](https://www.productlift.dev/blog/product-prioritization-framework)

| Framework | Formula | Best Fit | PRD Relevance |
|-----------|---------|----------|---------------|
| RICE | (Reach x Impact x Confidence) / Effort | Team-level, 20-50 features, quarterly | Reach and Impact from PRD; Effort from TDD |
| WSJF (SAFe) | (User-Biz Value + Time Criticality + Risk Reduction) / Job Duration | Portfolio-level, 50+ product staff | Numerator components map directly to PRD business context |
| MoSCoW | Must/Should/Could/Won't classification | Release scope negotiation | Phase constraints: Must-have in Phase 1, Could-have deferred to Phase 3+ |

**Layered framework usage:** Mature organizations layer WSJF at portfolio level, RICE at team level, MoSCoW for release scope. This validates using PRD context as a supplementary scoring signal rather than replacing technical scoring.

**Relevance:** HIGH | **Relationship:** EXTENDS -- WSJF is the best-fit scoring framework for combining PRD business signals with TDD technical signals.

### 5.3 Product Roadmap vs. Engineering Roadmap Boundary

**Sources:** [Fibery - Engineering Roadmap vs Product Roadmap](https://fibery.io/blog/product-management/engineering-roadmap-vs-product-roadmap/), [Amoeboids - Technical vs Product Roadmap](https://amoeboids.com/blog/product-vs-technology-roadmaps-whats-the-difference/), [Aha! - Product vs Technology Roadmap](https://www.aha.io/blog/the-product-roadmap-vs-the-technology-roadmap), [CloudBees - Prioritizing Technical vs Product Roadmap](https://www.cloudbees.com/blog/prioritizing-technical-roadmap-product-roadmap)

Industry consensus defines a clear boundary: Product roadmap covers What and Why (business-facing). Engineering roadmap covers How and When (team-facing). Key practices: (1) business rationale annotates but does not dictate technical ordering, (2) technical dependencies still govern sequence, (3) dual scoring keeps business value and technical complexity independent, (4) technical debt has its own track even without PRD backing.

**Relevance:** HIGH | **Relationship:** SUPPORTS -- validates that PRD context injects business rationale without changing the engineering roadmap's nature.

### 5.4 JTBD as the Bridge Between PRD and Engineering Roadmap

**Sources:** [THRV - JTBD vs Personas Ultimate Guide](https://www.thrv.com/blog/jobs-to-be-done-vs-personas-the-ultimate-guide-to-unified-customer-understanding-in-product-development), [Agile Seekers - JTBD in Tech Product Discovery](https://agileseekers.com/blog/applying-jobs-to-be-done-jtbd-framework-to-tech-product-discovery), [Product School - JTBD Framework](https://productschool.com/blog/product-fundamentals/jtbd-framework)

JTBD focuses on what customers are trying to accomplish. For engineering enrichment, JTBD is a decision tool (evidence-backed), while personas are communication tools (role and context). Features enabling multiple personas to complete high-importance jobs get prioritization.

PRD sections ranked by engineering value: (1) JTBD/User Stories -- HIGH, (2) Success Metrics/KPIs -- HIGH, (3) Compliance/Regulatory -- HIGH (hard constraints), (4) Personas -- MEDIUM, (5) Business Model/Revenue -- MEDIUM, (6) Market Positioning -- LOW, (7) Stakeholder Map -- LOW.

**Relevance:** HIGH | **Relationship:** EXTENDS -- provides focused extraction target ranking for PRD processing.

### 5.5 Dual-Track Agile as Organizational Pattern

**Sources:** [Productboard - Dual-Track Agile](https://www.productboard.com/glossary/dual-track-agile/), [SVPG - Dual-Track Agile](https://www.svpg.com/dual-track-agile/), [Lumenalta - Build Less Deliver More](https://lumenalta.com/insights/build-less-deliver-more-the-case-for-dual-track-agile), [Jeff Patton - Dual Track Development](https://jpattonassociates.com/dual-track-development/)

Dual-track agile separates Discovery (validate what to build) from Delivery (build it). The `--prd-file` flag represents the programmatic interface between these tracks. PRD file = validated discovery output; roadmap pipeline = delivery planning.

**Relevance:** MEDIUM | **Relationship:** SUPPORTS -- validates supplementary PRD input as a well-established bridge between product and engineering workflows.

### 5.6 Context Engineering for LLM Pipelines

**Sources:** [Prompt Engineering Guide - Context Engineering](https://www.promptingguide.ai/guides/context-engineering-guide), [Deepset - Context Engineering: Next Frontier](https://www.deepset.ai/blog/context-engineering-the-next-frontier-beyond-prompt-engineering), [Addy Osmani - Context Engineering](https://addyo.substack.com/p/context-engineering-bringing-engineering), [arXiv - Context Engineering for Multi-Agent LLM Code Assistants](https://arxiv.org/html/2508.08322v1)

Context engineering (2025-2026) principles for multi-document LLM pipelines: (1) structured context injection -- bullet points and Q&A pairs outperform long paragraphs, (2) high signal-to-noise ratio, (3) multi-stage processing into structured representations, (4) selective injection based on relevance per step.

**Relevance:** HIGH | **Relationship:** EXTENDS -- PRD extraction should produce a structured dataclass (not raw text) with selective per-step injection.

### 5.7 External Research Summary

| Metric | Value |
|--------|-------|
| Total findings synthesized | 8 topic areas from 27 unique sources |
| Reliability | 25 HIGH, 2 MEDIUM |
| Relevance | 6 HIGH, 2 MEDIUM |
| Relationship | 4 SUPPORTS, 4 EXTENDS, 0 CONTRADICTS |

**Key takeaways for implementation:**

1. **WSJF is the best-fit scoring framework** for combining PRD business signals with TDD technical signals.
2. **PRD extraction should target 4 sections**, ranked: JTBD/User Stories, Success Metrics/KPIs, Compliance/Regulatory, Personas.
3. **Business rationale annotates phases but does not restructure them.** Technical dependency ordering is inviolable.
4. **Pre-process PRD into structured summaries** before injection. A typed `PRDContext` dataclass with selective per-step injection is recommended.
5. **Scoring should be dual-track with configurable weighting** (suggested default: 0.6 technical / 0.4 business).
6. **MoSCoW classifications act as phase constraints**, not scores.

---


## Section 6: Options Analysis

### 6.0 Framing

The design approach is already specified: replicate the tasklist TDD supplementary pattern for PRD. The options below vary in **implementation scope** -- how many pipeline touchpoints receive PRD enrichment in the initial implementation.

All three options share the same CLI plumbing foundation:
- `prd_file: Path | None = None` field on `RoadmapConfig` and `TasklistValidateConfig`
- `--prd-file` Click option on `roadmap run` and `tasklist validate` commands
- Conditional `.resolve()` wiring in command functions
- `config.prd_file` passed through executor to prompt builders

### 6.1 Option A: Full Enrichment

**Scope:** P1 + P2 prompt builders (6) + tasklist prompt + skill/reference layer updates.

| Assessment Dimension | Rating |
|---------------------|--------|
| Effort | High -- ~200-250 lines new code + ~100 lines refactoring + ~200 lines skill docs + ~150 lines tests |
| Risk | Medium -- refactoring 5 prompt builders increases regression surface |
| Reuse of TDD pattern | Full |
| Files changed | 12-14 files |

**Pros:** Complete coverage. Skill docs synchronized. Full pattern established once.
**Cons:** 2-3 sessions effort. Largest diff. P2 enrichment delivers lower marginal value.

### 6.2 Option B: Minimal Enrichment

**Scope:** P1 builders only (4 roadmap) + tasklist fidelity prompt. Defer P2/P3 and all skill/reference docs.

| Assessment Dimension | Rating |
|---------------------|--------|
| Effort | Low-Medium -- ~120-150 lines new code + ~60 lines refactoring + ~80 lines tests |
| Risk | Low -- fewer files changed |
| Reuse of TDD pattern | Partial -- CLI layers replicated, skill layer deferred |
| Files changed | 7-9 files |

**Pros:** Smallest scope. 1 session. Covers highest-value touchpoints.
**Cons:** TDD+PRD combo missing PRD context in TDD extraction. Skill docs stale indefinitely.

### 6.3 Option C: Progressive Enrichment (Two Phases)

**Scope:** Phase 1 = CLI plumbing + P1 builders + tasklist. Phase 2 = P2 builders + skill/reference layer. Each phase independently shippable.

| Assessment Dimension | Rating |
|---------------------|--------|
| Effort | Medium total, split across 2 increments |
| Risk | Low per phase |
| Reuse of TDD pattern | Full (by end of Phase 2) |
| Files changed | Phase 1: 7-9; Phase 2: 6-8 |

**Pros:** Highest value first (~80% in Phase 1). Phase 2 benefits from Phase 1 learnings. Time-bounded skill doc sync.
**Cons:** Two review cycles. Brief stale period between phases.

### 6.4 Options Comparison

| Dimension | Option A: Full | Option B: Minimal | Option C: Progressive |
|-----------|---------------|-------------------|----------------------|
| Prompt builders enriched | 7 | 5 | 5 then 7 |
| Skill/ref docs updated | Yes | No | No then Yes |
| Estimated effort | 2-3 sessions | 1 session | 1 + 1 sessions |
| Files changed (total) | 12-14 | 7-9 | 13-17 |
| Regression risk | Medium | Low | Low per phase |
| PRD value delivered | ~95% | ~80% | ~80% then ~95% |
| TDD+PRD combo support | Full | Partial | Partial then Full |
| Skill doc sync | Immediate | Deferred indefinitely | Deferred then synchronized |
| Follow-up required | No | Yes | Yes (scoped) |

### 6.5 Key Trade-offs

**Coverage vs. velocity:** Option A delivers complete coverage but takes 2-3x longer than Option B. The P2 builders deliver ~15% of total PRD pipeline value.

**Skill doc synchronization:** Options B and C (Phase 1) leave skill/reference docs stale. Inference-based workflows will not know about `--prd-file` until updated.

**Refactoring scope:** All options require refactoring at least 3 prompt builders from single-return to base-pattern. This is mechanical but increases diff size.

**TDD+PRD interaction:** Only Option A enriches `build_extract_prompt_tdd` with PRD context in the initial delivery.

---


## Section 7: Recommendation

### 7.1 Recommended Option: A (Full Enrichment) — Single Delivery

**Updated recommendation (post-research decision):** Option A is selected — all PRD enrichment (P1 + P2 builders + skill/reference layer) in a single implementation pass. This was a user decision to avoid the coordination overhead of two delivery increments.

**Rationale:**

1. **Complete coverage in one pass.** All 7 target prompt builders, tasklist fidelity, and skill/reference docs updated together. No stale period, no deferred follow-up.

2. **Pattern established once.** The `--prd-file` supplementary pattern is fully demonstrated across all touchpoints, providing a complete reference for future supplementary inputs.

3. **Prompt builder refactoring batched.** The 7 builders needing base-pattern conversion are refactored in one pass, reducing the total number of times these files are modified.

4. **Skill doc synchronization is immediate.** Inference-based workflows see PRD-aware behavior as soon as the implementation lands.

**Note:** The dead `tdd_file` field on `RoadmapConfig` (models.py:115) exists but was never wired through the roadmap executor or CLI. Since the PRD integration touches all the same files with the same pattern, both `tdd_file` AND `prd_file` should be wired in the roadmap pipeline together in this implementation. This ensures both supplementary inputs are designed and wired consistently in one pass.

### 7.2 Key Trade-off Acknowledgments

**Larger single diff:** All enrichment in one pass means a 12-14 file change set. Mitigated by the changes being additive with `None` defaults — zero behavioral change when `--prd-file` is absent.

**Refactoring scope:** 7 prompt builders need base-pattern conversion. This is mechanical (no behavior change) but increases diff size. Should be done as prerequisite steps before adding PRD blocks to keep the diff reviewable.

### 7.3 Full Implementation Scope Summary

| Component | File | Change |
|-----------|------|--------|
| Model field | `roadmap/models.py` | Add `prd_file: Path \| None = None` |
| Model field | `tasklist/models.py` | Add `prd_file: Path \| None = None` |
| CLI flag | `roadmap/commands.py` | Add `--prd-file` option + wire into `config_kwargs` |
| CLI flag | `tasklist/commands.py` | Add `--prd-file` option + wire into config |
| Executor wiring | `roadmap/executor.py` | Wire both `config.tdd_file` and `config.prd_file` to target prompt builders + add to extract step `inputs` |
| Executor wiring | `tasklist/executor.py` | Pass `config.prd_file` to prompt builder + add to `all_inputs` |
| Prompt enrichment | `roadmap/prompts.py` | Add `prd_file` param + supplementary blocks to 7 builders (P1: extract, generate, spec-fidelity, test-strategy; P2: extract_tdd, score; P3: diff, debate, merge stubs) |
| Prompt enrichment | `tasklist/prompts.py` | Add `prd_file` param + blocks to fidelity AND generation builders |
| Refactoring | `roadmap/prompts.py` | Convert 7 builders to base-pattern (prerequisite for conditional blocks) |
| Dead tdd_file fix | `roadmap/commands.py`, `executor.py`, `prompts.py` | Add `--tdd-file` CLI flag, wire through executor, redundancy guard |
| State auto-wire | `roadmap/executor.py`, `tasklist/executor.py` | Store/read `tdd_file`+`prd_file` in `.roadmap-state.json` |
| Tasklist generation | `tasklist/prompts.py`, `tasklist/executor.py` | Enrich generation (not just validation) with TDD/PRD |
| Skill/reference | `extraction-pipeline.md`, `scoring.md`, `SKILL.md`, `spec-panel.md` | PRD protocol, auto-wire docs, generation enrichment, expanded 4.4a/4.4b |
| Tests | `tests/roadmap/`, `tests/tasklist/` | 6 scenarios, auto-wire, generation, redundancy guard |

**Estimated: ~876 lines across ~14 files.**

**Out of scope:** WSJF-inspired scoring formula (future enhancement).

---


## Section 8: Implementation Plan

### Overview

This plan adds `--prd-file` as input to both the roadmap and tasklist pipelines, wires the dead `tdd_file` on `RoadmapConfig`, implements auto-wiring via `.roadmap-state.json`, and enriches tasklist generation (not just validation) with full TDD/PRD content.

**Design principle:** The typical usage is `superclaude roadmap run tdd.md --prd-file prd.md`. The TDD is the primary input (auto-detected). The PRD provides integrated business context — not tacked-on "supplementary validation" but woven into extraction and generation from the start. Both documents should be used to their fullest extent without requiring complex argument gymnastics.

Industry research validates this: PRD context should annotate engineering phases with business rationale without restructuring them [web-01, Finding 3]. The `--prd-file` flag acts as a programmatic bridge between product discovery and engineering delivery tracks [web-01, Finding 6].

The plan is structured as **7 phases** covering CLI, prompts, skills, state management, and tasklist generation enrichment. All changes are additive with `None` defaults — zero backward-compatibility risk.

**Estimated: ~876 lines across ~14 files.**

**In scope (4 mandatory requirements identified during E2E testing):**
1. Wire dead `tdd_file` on `RoadmapConfig` end-to-end alongside `prd_file` (Phase 5)
2. Auto-wire supplementary files from `.roadmap-state.json` so downstream tasklist doesn't need re-passing (Phase 6)
3. Auto-wire `prd_file` via the same state file mechanism (Phase 6)
4. Enrich tasklist GENERATION (not just validation) with TDD/PRD content (Phase 7)

**Out of scope:** WSJF-inspired scoring formula (future enhancement).

**Redundancy guard:** When the primary input IS a TDD (`--input-type tdd` or auto-detected), passing `--tdd-file` is redundant. The executor detects this and warns/ignores.

---

### Phase 1: CLI Plumbing — Model Fields, CLI Flags, Executor Wiring

#### 1.1 Model and CLI Plumbing -- Roadmap Pipeline

**Note:** `tdd_file` already exists on `RoadmapConfig` (L115) but is dead code — never wired through CLI or executor. Steps below wire BOTH `tdd_file` and `prd_file` consistently.

| Step | Action | File | Details |
|------|--------|------|---------|
| 1.1.1 | Add `prd_file` field | `roadmap/models.py` | `prd_file: Path \| None = None` after `tdd_file` at L115 |
| 1.1.2 | Add `--tdd-file` Click option | `roadmap/commands.py` | `click.Path(exists=True, path_type=Path)` — mirrors tasklist pattern at `tasklist/commands.py:62-66`. Wire existing dead `tdd_file` model field. |
| 1.1.3 | Add `--prd-file` Click option | `roadmap/commands.py` | `click.Path(exists=True, path_type=Path)` after `--tdd-file` |
| 1.1.4 | Add both to function signature | `roadmap/commands.py` | `tdd_file: Path \| None, prd_file: Path \| None` on `run()` |
| 1.1.5 | Wire both into `config_kwargs` | `roadmap/commands.py` | `"tdd_file": tdd_file.resolve() if tdd_file else None, "prd_file": prd_file.resolve() if prd_file else None` |
| 1.1.6 | Wire both into extract step inputs | `roadmap/executor.py` | Conditionally append both `config.tdd_file` and `config.prd_file` to step inputs when present |
| 1.1.7 | Pass both to prompt builders | `roadmap/executor.py` | `tdd_file=config.tdd_file, prd_file=config.prd_file` kwargs to target builders |

#### 1.2 Model and CLI Plumbing -- Tasklist Pipeline

| Step | Action | File | Details |
|------|--------|------|---------|
| 1.2.1 | Add `prd_file` field | `tasklist/models.py` | `prd_file: Path \| None = None` after `tdd_file` at L25 |
| 1.2.2 | Add `--prd-file` Click option | `tasklist/commands.py` | After `--tdd-file` (L61-66) |
| 1.2.3 | Add to function signature | `tasklist/commands.py` | `prd_file: Path \| None` on `validate()` |
| 1.2.4 | Wire into config construction | `tasklist/commands.py` | `prd_file=prd_file.resolve() if prd_file else None` |
| 1.2.5 | Add to `all_inputs` | `tasklist/executor.py` | `if config.prd_file is not None: all_inputs.append(config.prd_file)` |
| 1.2.6 | Pass to prompt builder | `tasklist/executor.py` | `prd_file=config.prd_file` kwarg |

### Phase 2: Prompt Builder Refactoring + P1 Enrichment

#### 2.1 P1 Prompt Enrichment -- Roadmap Extract

| Step | Action | Details |
|------|--------|---------|
| 1.3.1 | Add `prd_file` param to `build_extract_prompt` | No refactoring needed -- already uses base pattern |
| 1.3.2 | Add PRD supplementary block | 5 checks: Success Metrics (S19), Personas (S7), Scope (S12), Compliance (S17), JTBD (S6). Advisory guardrail. |

#### 2.2 P1 Prompt Enrichment -- Spec Fidelity and Test Strategy (Quality Gates)

| Step | Action | Details |
|------|--------|---------|
| 1.4.1 | Refactor `build_spec_fidelity_prompt` to base pattern | Single return -> `base = (...); return base + block` |
| 1.4.2 | Add `prd_file` param and dimensions 12-15 | Persona Coverage (S7), Metric Traceability (S19), Compliance (S17, HIGH severity), Scope Boundary (S12) |
| 1.4.3 | Wire `prd_file` to spec-fidelity step in executor | Kwarg + add to step `inputs` |
| 1.4.4 | Refactor `build_test_strategy_prompt` to base pattern | Single return -> base pattern |
| 1.4.5 | Add `prd_file` param and 5-check block | Persona acceptance tests (S7), journey E2E (S22), KPI validation (S19), compliance tests (S17), edge cases (S23) |
| 1.4.6 | Wire `prd_file` to test-strategy step in executor | Kwarg + add to step `inputs` |

#### 2.3 P1 Prompt Enrichment -- Generate (Variant Shaping)

| Step | Action | Details |
|------|--------|---------|
| 1.5.1 | Refactor `build_generate_prompt` to base pattern | Single return -> base pattern |
| 1.5.2 | Add `prd_file` param and 4-check block | Value-based phasing (S5, S19), persona sequencing (S7, S22), compliance gates (S17), scope guardrails (S12) |
| 1.5.3 | Wire `prd_file` to both generate steps | Kwarg + add to step `inputs` |

#### 2.4 Tasklist Fidelity Prompt

| Step | Action | Details |
|------|--------|---------|
| 1.6.1 | Add `prd_file` param | After existing `tdd_file` param |
| 1.6.2 | Add PRD supplementary block | 4 checks: Persona Flow Coverage, KPI Instrumentation, Stakeholder/Compliance Tasks, UX Flow Alignment. MEDIUM severity. |

---

### Phase 3: P2 Prompt Enrichment + P3 API Stubs

#### 3.1 P2 Prompt Enrichment -- TDD Extract Mode

| Step | Action | Details |
|------|--------|---------|
| 2.1.1 | Add `prd_file` param to `build_extract_prompt_tdd` | No refactoring needed -- already uses base pattern |
| 2.1.2 | Add PRD supplementary block (TDD mode) | 3 checks: Success Metrics (S19), Personas (S7), Compliance (S17). Advisory guardrail. |

#### 3.2 P2 Prompt Enrichment -- Score (Variant Selection)

| Step | Action | Details |
|------|--------|---------|
| 2.2.1 | Refactor `build_score_prompt` to base pattern | Single return -> base pattern |
| 2.2.2 | Add `prd_file` param and 3 scoring dimensions | Business value delivery (S19), persona coverage (S7), compliance alignment (S17) |
| 2.2.3 | Wire `prd_file` to score step in executor | Kwarg |

#### 3.3 P3 API-Only Stubs

Add `prd_file: Path | None = None` parameter only (no supplementary blocks) to `build_diff_prompt`, `build_debate_prompt`, `build_merge_prompt` for API consistency. No executor wiring changes needed for P3 steps.

### Phase 4: Skill and Reference Layer

**Goal:** Update 4 skill/reference documents for inference-based workflows.

| Step | File | Change |
|------|------|--------|
| 2.4.1 | `extraction-pipeline.md` | Add PRD-supplementary extraction context section + storage keys |
| 2.4.2 | `scoring.md` | Add PRD scoring guidance + `product` type to Type Match Lookup |
| 2.4.3 | `tasklist SKILL.md` | Add Sections 4.1b (PRD context) and 4.4b (PRD task generation) |
| 2.4.4 | `spec-panel.md` | Add Steps 6c-6d (PRD detection + frontmatter) + PRD output section |

**Validation:** `make verify-sync` to confirm src/ and .claude/ in sync.

### Phase 5: Fix Dead `tdd_file` in Roadmap Pipeline

**Goal:** Wire the existing dead `tdd_file` field on `RoadmapConfig` end-to-end. When primary input is a spec, `--tdd-file` provides TDD engineering context as supplementary enrichment (same pattern as `--prd-file`). When primary input IS a TDD, `--tdd-file` is redundant — emit warning and ignore.

| Step | Action | File | Details |
|------|--------|------|---------|
| 5.1 | Add `--tdd-file` Click option to `run` | `roadmap/commands.py` | Same pattern as `--prd-file`. Mirrors `tasklist/commands.py:62-66`. |
| 5.2 | Wire into `config_kwargs` | `roadmap/commands.py` | `"tdd_file": tdd_file.resolve() if tdd_file else None` |
| 5.3 | Wire into extract step inputs | `roadmap/executor.py` | Conditionally append alongside `prd_file`. Order: `[spec_file, tdd_file, prd_file]` |
| 5.4 | Pass to prompt builders | `roadmap/executor.py` | `tdd_file=config.tdd_file` kwarg to target builders |
| 5.5 | Add `tdd_file` param and blocks to prompt builders | `roadmap/prompts.py` | Conditional block when `tdd_file` provided AND primary input is NOT already TDD |
| 5.6 | Add redundancy guard | `roadmap/executor.py` | If `input_type == "tdd" and config.tdd_file`, warn and set `config.tdd_file = None` |

---

### Phase 6: Auto-Wire Supplementary Files from `.roadmap-state.json`

**Goal:** When tasklist reads a roadmap output directory, auto-detect TDD and PRD files from `.roadmap-state.json` without requiring re-passing of flags. Explicit CLI flags override auto-wired values.

| Step | Action | File | Details |
|------|--------|------|---------|
| 6.1 | Store `tdd_file` and `prd_file` in state | `roadmap/executor.py` | Add to `.roadmap-state.json` during roadmap runs |
| 6.2 | Read state in tasklist executor | `tasklist/executor.py` | Look for `.roadmap-state.json` alongside `config.roadmap_file` |
| 6.3 | Auto-wire with existence check | `tasklist/executor.py` | If file in state AND `config.field is None` AND file exists on disk, auto-set |
| 6.4 | Precedence: explicit flags override | `tasklist/executor.py` | Auto-wire only fills `None` fields |
| 6.5 | Emit info messages | `tasklist/executor.py` | `[tasklist] Auto-wired tdd_file from roadmap state: {path}` |
| 6.6 | Auto-wire on `--resume` | `roadmap/executor.py` | Same pattern for roadmap resume from state |
| 6.7 | Document in skill docs | `sc-tasklist-protocol/SKILL.md`, `extraction-pipeline.md` | Auto-wire behavior documentation |

---

### Phase 7: Enrich Tasklist Generation with TDD/PRD Content

**Goal:** Tasklist GENERATION (not just validation) reads TDD and PRD source documents for richer task decomposition. Currently generation only reads `roadmap.md`, losing TDD-specific detail (test cases, API schemas, component props, rollback steps) and PRD context (personas, metrics, journeys, acceptance scenarios).

| Step | Action | File | Details |
|------|--------|------|---------|
| 7.1 | Wire `--tdd-file` and `--prd-file` to tasklist generate | `tasklist/commands.py`, `tasklist/executor.py` | If CLI generate command exists; otherwise skill-layer only |
| 7.2 | Add TDD generation enrichment block | `tasklist/prompts.py` | 5 checks: test cases (§15), API schemas (§8), components (§10), rollback steps (§19), data models (§7) |
| 7.3 | Add PRD generation enrichment block | `tasklist/prompts.py` | 5 checks: persona context (§7), acceptance scenarios (§10/§22), success metrics (§19), stakeholder priorities (§5), scope boundaries (§12). Guardrail: PRD enriches task descriptions, does NOT generate standalone tasks. |
| 7.4 | Handle both TDD+PRD together | `tasklist/prompts.py` | Stack both blocks. TDD for implementation specifics, PRD for descriptions/priorities/acceptance criteria. |
| 7.5 | Update skill protocol | `sc-tasklist-protocol/SKILL.md` | Add "Source Document Enrichment" section. Expand 4.4a (TDD) and 4.4b (PRD) from validation-only to generation enrichment. |

---

### Phase 8: Testing

**Scenario matrix (both pipelines, all enriched builders):**

| Scenario | Primary Input | `--tdd-file` | `--prd-file` | Expected Behavior |
|----------|--------------|-------------|-------------|-------------------|
| A | spec | absent | absent | Baseline, no enrichment blocks |
| B | TDD (auto) | absent | absent | TDD extraction, no supplementary blocks |
| C | spec | absent | provided | Spec extraction + PRD enrichment |
| D | TDD (auto) | absent | provided | TDD extraction + PRD enrichment (most common usage) |
| E | spec | provided | provided | Spec extraction + TDD supplementary + PRD enrichment |
| F | TDD (auto) | provided | absent | Warning: --tdd-file redundant, ignored |

**Test coverage:**

| Area | Tests |
|------|-------|
| CLI flag parsing | Both `--tdd-file` and `--prd-file` on roadmap run; `--prd-file` on tasklist |
| Prompt builder output | Parametrized A-F for all enriched builders |
| Redundancy guard | Scenario F: warning emitted, `tdd_file` set to None |
| Auto-wire from state | Roadmap stores paths, tasklist reads them, explicit flags override |
| Tasklist generation enrichment | With/without TDD, with/without PRD, with both |
| Refactoring regression | Byte-identical output when no supplementary files for all refactored builders |
| Skill doc verification | Verify PRD/TDD sections reference correct CLI flags |

**Validation:** `uv run pytest tests/` full suite. `make verify-sync` for skill docs.

---

### Change Summary

| Category | Files Modified | Lines Added (est.) |
|----------|---------------|-------------------|
| Models | 2 | ~6 |
| Commands (CLI) | 2 | ~40 |
| Executors | 2 | ~80 |
| Prompts | 2 | ~200 |
| Skill/Reference docs | 4 | ~250 |
| Tests | 2-4 | ~300 |
| **Total** | **~14 files** | **~876 lines** |

All changes are additive with `None` defaults. Zero backward-compatibility risk.

### Phases Summary

| Phase | Scope | CLI | Skills |
|-------|-------|-----|--------|
| 1 | Model/CLI plumbing for `--prd-file` | YES | — |
| 2 | Prompt builder refactoring + P1 enrichment | YES | — |
| 3 | P2 prompt enrichment + P3 API stubs | YES | — |
| 4 | Skill/reference layer for PRD protocol | — | YES |
| 5 | Fix dead `tdd_file` in roadmap pipeline | YES | — |
| 6 | Auto-wire from `.roadmap-state.json` | YES | YES |
| 7 | Enrich tasklist generation with TDD/PRD | YES | YES |
| 8 | Testing (all 6 interaction scenarios) | YES | — |

---


## Section 9: Open Questions

### 9.1 Unresolved Questions from Gaps Log

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| Q1 | `tdd_file` on `RoadmapConfig` (models.py:115) is dead code. Should PRD integration clean this up? | MEDIUM | Clean up as separate preparatory commit. Do not replicate the mistake for `prd_file`. |
| Q2 | 7 of 9 roadmap prompt builders need refactoring before PRD blocks can be added. Does this increase scope? | MEDIUM | Yes. Mitigate with parametrized tests verifying identical output pre/post refactoring. |
| Q3 | PRD supplementary task generation is weaker than TDD -- PRDs describe "what/why" not "how". Acceptable? | LOW | Accept as known limitation. PRD enrichment improves task quality, not quantity. |
| Q4 | spec-panel is inference-only. PRD additions update protocol doc only. Sufficient? | LOW | Sufficient. No CLI code changes needed for spec-panel. |
| Q5 | Deferred TDD generate prompt comment at prompts.py:309-316. Address alongside PRD? | LOW | Acknowledge during implementation. Implement or explicitly re-defer. |
| Q6 | `gates.py` received minimal investigation. Verified? | LOW | Confirm during implementation by reading gate constants. No new gates expected. |
| Q7 | PRD template section numbering -- cross-validate against actual template? | IMPORTANT | Cross-validate `src/superclaude/examples/prd_template.md` vs `prd/SKILL.md` before drafting prompt blocks. |
| Q8 | "9-step pipeline" vs 11 step entries discrepancy? | LOW | Cosmetic. `_build_steps()` produces 9 LLM steps; 11 total includes non-LLM and post-pipeline steps. |

### 9.2 Unresolved Questions from Research Files

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| Q9 | Should PRD context flow only into extraction, or also into downstream steps? | MEDIUM | Implement P1 (extract, generate, spec-fidelity, test-strategy) and P2 (extract_tdd, score). Defer P3. |
| Q10 | Content embedding vs file reference for PRD? | MEDIUM | Use `inputs` file path pattern (PRDs can be large). Consistent with TDD handling in tasklist. |
| Q11 | Should `--prd-file` be added to `roadmap validate`? | LOW | Defer. Focus on `roadmap run` and `tasklist validate` first. |
| Q12 | State persistence: should `prd_file` survive `--resume` cycles? | LOW | Do not persist initially. `retrospective_file` sets this precedent. |
| Q13 | Triple input (PRD + TDD + spec) handling? | LOW | Stack both blocks: TDD first (technical "how"), then PRD (business "why"). |
| Q14 | Both TDD and PRD files could exceed `_EMBED_SIZE_LIMIT` (100KB)? | LOW | Acceptable. Executor logs warning but proceeds. Add PRD summarization if needed later. |
| Q15 | PRD extraction timing: once at pipeline start or per-step? | MEDIUM | Single extraction at `extract` step recommended for efficiency. |
| Q16 | PRD-TDD consistency check? | LOW | Defer. Trust both documents as-is initially. |
| Q17 | Circular dependency: PRD skill output vs pipeline input expectations? | MEDIUM | Add lightweight PRD structure validation at pipeline start. Log warnings for missing sections. |
| Q18 | PRD scoring formula: custom 7-factor or standard 5-factor? | LOW | Standard 5-factor initially. Revisit after production usage data. |

### 9.3 Unverified Claims

| # | Claim | Source | Risk if Wrong | Verification |
|---|-------|--------|---------------|-------------|
| U1 | Scoring formulas are inference-based only, no `scoring.py` in CLI | File 04, Section 2.1 | LOW | Grep for scoring factor names in `src/superclaude/cli/` |
| U2 | Tasklist SKILL.md task generation is inference-only, not in CLI | File 04, Section 3.1 | LOW | Confirm `tasklist/executor.py` only does validation |
| U3 | PRD template has 28 sections matching `prd/SKILL.md` inventory | Files 04, 05 | IMPORTANT | Read `src/superclaude/examples/prd_template.md` and cross-validate |
| U4 | PRD detection signals sufficient for future auto-detection | File 04, Section 5 | LOW | Not needed now -- explicit `--prd-file` flag bypasses detection |

---


## Section 10: Evidence Trail

### 10.1 Codebase Research Files

All codebase research conducted on 2026-03-27 against the `feat/tdd-spec-merge` branch.

| File | Full Path | Topic |
|------|-----------|-------|
| research-notes.md | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/research/research-notes.md` | Research planning: file inventory, patterns, solution approach |
| 01-roadmap-cli-integration-points.md | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/research/01-roadmap-cli-integration-points.md` | Roadmap CLI layers: commands, models, executor; dead `tdd_file`; step injection points |
| 02-prompt-enrichment-mapping.md | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/research/02-prompt-enrichment-mapping.md` | PRD supplementary text for 10 prompt builders; refactoring requirements; executor call sites |
| 03-tasklist-integration-points.md | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/research/03-tasklist-integration-points.md` | Tasklist CLI layers; full TDD pattern trace (reference implementation) |
| 04-skill-reference-layer.md | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/research/04-skill-reference-layer.md` | PRD updates for extraction-pipeline.md, scoring.md, tasklist SKILL.md, spec-panel.md |
| 05-prd-content-analysis.md | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/research/05-prd-content-analysis.md` | 28-section PRD inventory; TDD extraction loss analysis; tiered section recommendation |

### 10.2 Web Research Files

| File | Full Path | Topic |
|------|-----------|-------|
| web-01-prd-driven-roadmapping.md | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/research/web-01-prd-driven-roadmapping.md` | RICE/WSJF/MoSCoW frameworks; product vs engineering roadmap boundary; JTBD; context engineering |

### 10.3 Synthesis Files

| File | Full Path | Sections Covered | Source Research |
|------|-----------|-----------------|-----------------|
| synth-01 | `synthesis/synth-01-problem-current-state.md` | S1 Problem Statement, S2 Current State | 01, 02, 03, 04, 05 |
| synth-02 | `synthesis/synth-02-target-gaps.md` | S3 Target State, S4 Gap Analysis | All research files |
| synth-03 | `synthesis/synth-03-external-findings.md` | S5 External Research | web-01 |
| synth-04 | `synthesis/synth-04-options-recommendation.md` | S6 Options, S7 Recommendation | All research files |
| synth-05 | `synthesis/synth-05-implementation-plan.md` | S8 Implementation Plan | 01, 02, 03, 04 |
| synth-06 | `synthesis/synth-06-questions-evidence.md` | S9 Open Questions, S10 Evidence Trail | All files |

### 10.4 Gaps Log

| File | Full Path | Purpose |
|------|-----------|---------|
| gaps-and-questions.md | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/gaps-and-questions.md` | Consolidated gap tracking: 4 resolved issues, 8 open questions |

### 10.5 Stale Documentation Findings

| # | Location | Finding | Severity |
|---|----------|---------|----------|
| D1 | `RoadmapConfig` docstring (models.py:98-99) | Omits `convergence_enabled`, `allow_regeneration`, `input_type`, `tdd_file` | LOW |
| D2 | `_build_steps()` docstring (executor.py) | Says "9-step pipeline" but function produces 10-11 entries | LOW |
| D3 | extraction-pipeline.md TDD detection rule (L145) | Describes boolean OR; actual code uses weighted scoring | MEDIUM |
| D4 | tasklist SKILL.md `--spec` flag (Section 4.1a) | Protocol says `--spec`; CLI uses `--tdd-file` | LOW |
| D5 | tasklist SKILL.md Section 4.4a task generation | Describes 7 patterns; CLI implements 3 checks | MEDIUM |
| D6 | TDD detection rule duplication | Same rule in 4 files with textual variations | LOW |
| D7 | `build_generate_prompt` deferred work (prompts.py:309-316) | References planned TDD-aware enrichment never implemented | LOW |

---

*End of report.*
