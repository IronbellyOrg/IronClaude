# Technical Research Report: PRD Pipeline Integration

**Synthesis of:** Research files 01-05
**Date:** 2026-03-27
**Sections covered:** 1 (Problem Statement), 2 (Current State Analysis)

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
| `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` | 143-207 | Steps 9-15: TDD-specific extraction (component inventory, migration, release criteria, observability, testing, API surface, data model) | No PRD equivalent exists |
| `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` | 7-108 | TDD 7-factor scoring formula (adds `api_surface` + `data_model_complexity` to standard 5 factors) | No PRD equivalent exists |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | 140-196 | Sections 4.1a (supplementary TDD context) and 4.4a (supplementary task generation with 7 patterns) | No PRD equivalent exists |
| `src/superclaude/commands/spec-panel.md` | 32-405 | Steps 6a-6b (TDD input detection + downstream frontmatter) and TDD output modes | No PRD equivalent exists |

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

Sections by pipeline enrichment value tier:

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
