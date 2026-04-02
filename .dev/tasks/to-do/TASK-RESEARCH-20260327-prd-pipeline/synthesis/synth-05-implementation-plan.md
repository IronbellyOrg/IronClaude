# Section 8: Implementation Plan

**Synthesized from:** Research files 01-04 + web-01
**Date:** 2026-03-27
**Scope:** Detailed, actionable implementation plan for adding `--prd-file` to both roadmap and tasklist pipelines

---

## Overview

This plan adds a `--prd-file` supplementary input flag to both the roadmap (`superclaude roadmap run`) and tasklist (`superclaude tasklist validate`) pipelines. The implementation follows the proven `--tdd-file` integration pattern already working in the tasklist pipeline [Research 01, Section 5; Research 03, Section 5]. All changes are additive with `None` defaults, ensuring zero backward-compatibility risk [Research 02, Summary].

The plan is structured in four phases: model/CLI plumbing, prompt enrichment, skill/reference layer updates, and testing. Each phase is self-contained and can be validated independently before proceeding to the next.

Industry research validates this approach: PRD context should annotate engineering phases with business rationale without restructuring them, and technical dependency ordering must never be overridden by business priority [Web Research, Finding 3]. The `--prd-file` flag acts as a programmatic bridge between product discovery and engineering delivery tracks, consistent with dual-track agile patterns [Web Research, Finding 6].

---

## Phase 1: Model and CLI Plumbing

**Goal:** Add the `prd_file` field to config dataclasses and `--prd-file` CLI flags to both pipelines, wiring the value through executors so downstream code can access it. No prompt changes yet -- this phase establishes the data path.

**Dependencies:** None (first phase).

### 1.1 Roadmap Pipeline

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 1.1.1 | Add `prd_file` field to `RoadmapConfig` | `src/superclaude/cli/roadmap/models.py` | Add `prd_file: Path \| None = None` after `tdd_file` at line 115 of `RoadmapConfig` dataclass. Follow identical pattern to existing `tdd_file: Path \| None` field. [Research 01, Section 1] |
| 1.1.2 | Add `--prd-file` Click option to `run` command | `src/superclaude/cli/roadmap/commands.py` | Add `@click.option("--prd-file", type=click.Path(exists=True, path_type=Path), default=None, help="Path to a PRD file for supplementary context enrichment.")` after the `--input-type` option (around line 110). Use `exists=True` (not `exists=False` like `--retrospective`). [Research 01, Section 2] |
| 1.1.3 | Add `prd_file` to `run` function signature | `src/superclaude/cli/roadmap/commands.py` | Add `prd_file: Path \| None` parameter to the `run()` function signature (lines 112-127). [Research 01, Section 2] |
| 1.1.4 | Wire `prd_file` into `config_kwargs` | `src/superclaude/cli/roadmap/commands.py` | Add `"prd_file": prd_file.resolve() if prd_file is not None else None` to the `config_kwargs` dict (lines 170-181). Follows `retrospective_file` resolution pattern. [Research 01, Section 2] |
| 1.1.5 | Wire `prd_file` into extract step inputs | `src/superclaude/cli/roadmap/executor.py` | In `_build_steps()` (lines 843-1012), modify the extract step's `inputs` list: `inputs=[config.spec_file] + ([config.prd_file] if config.prd_file else [])`. This makes the PRD file content available to the subprocess via `_embed_inputs()`. [Research 01, Section 3] |
| 1.1.6 | Pass `prd_file` to extract prompt builders | `src/superclaude/cli/roadmap/executor.py` | In `_build_steps()`, add `prd_file=config.prd_file` kwarg to both `build_extract_prompt()` (line 893) and `build_extract_prompt_tdd()` (line 888) calls. Parameter will be accepted but unused until Phase 2. [Research 01, Section 3; Research 02, Executor Wiring table] |

### 1.2 Tasklist Pipeline

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 1.2.1 | Add `prd_file` field to `TasklistValidateConfig` | `src/superclaude/cli/tasklist/models.py` | Add `prd_file: Path \| None = None` after `tdd_file` at line 25. Comment: `# PRD integration: optional PRD file for enriched validation`. [Research 03, Section 2] |
| 1.2.2 | Add `--prd-file` Click option to `validate` command | `src/superclaude/cli/tasklist/commands.py` | Add `@click.option("--prd-file", type=click.Path(exists=True, path_type=Path), default=None, help="Path to the PRD file used as an additional validation input.")` after the existing `--tdd-file` option (lines 61-66). [Research 03, Section 1] |
| 1.2.3 | Add `prd_file` to `validate` function signature | `src/superclaude/cli/tasklist/commands.py` | Add `prd_file: Path \| None` parameter to the `validate()` function signature (line 74). [Research 03, Section 1] |
| 1.2.4 | Wire `prd_file` into `TasklistValidateConfig` construction | `src/superclaude/cli/tasklist/commands.py` | Add `prd_file=prd_file.resolve() if prd_file is not None else None` to the `TasklistValidateConfig(...)` call (line 114). [Research 03, Section 1] |
| 1.2.5 | Add `prd_file` to `all_inputs` in executor | `src/superclaude/cli/tasklist/executor.py` | In `_build_steps()` (lines 188-211), add after the TDD input block: `if config.prd_file is not None: all_inputs.append(config.prd_file)`. Order: roadmap, tasklists, tdd, prd. [Research 03, Section 3] |
| 1.2.6 | Pass `prd_file` to prompt builder | `src/superclaude/cli/tasklist/executor.py` | Add `prd_file=config.prd_file` kwarg to the `build_tasklist_fidelity_prompt()` call (line 202). [Research 03, Section 3] |

**Phase 1 validation:** Run `uv run pytest tests/` to confirm no regressions. Verify `--prd-file` appears in `superclaude roadmap run --help` and `superclaude tasklist validate --help`. Pass `--prd-file /dev/null` to confirm Click path validation works (should fail with "does not exist" if file missing, succeed if file exists).

---

## Phase 2: Prompt Enrichment

**Goal:** Add `prd_file` parameter and conditional supplementary blocks to each target prompt builder. When `--prd-file` is provided, prompts gain PRD-specific extraction/validation instructions. When absent, prompts are identical to current behavior.

**Dependencies:** Phase 1 complete (CLI flags wired, executor passes `prd_file` to prompt builders).

### 2.1 Roadmap Extract Prompts (P1 -- Primary Injection Point)

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 2.1.1 | Add `prd_file` param to `build_extract_prompt` | `src/superclaude/cli/roadmap/prompts.py` | Change signature (line 82) to: `def build_extract_prompt(spec_file: Path, retrospective_content: str \| None = None, prd_file: Path \| None = None) -> str:`. No refactoring needed -- already uses `base = (...)` pattern. [Research 02, Section: Prompt Builder 1] |
| 2.1.2 | Add PRD supplementary block to `build_extract_prompt` | `src/superclaude/cli/roadmap/prompts.py` | After retrospective block, before `_OUTPUT_FORMAT_BLOCK`, insert conditional: `if prd_file is not None: base += (...)`. Block contains 5 check items referencing PRD sections: Success Metrics (SS19), User Personas (SS7), Scope Definition (SS12), Legal/Compliance (SS17), JTBD (SS6). Includes guardrail: "PRD is advisory context -- do NOT treat PRD content as hard requirements unless also stated in the specification." [Research 02, Section: Prompt Builder 1, drafted block text] |
| 2.1.3 | Add `prd_file` param to `build_extract_prompt_tdd` | `src/superclaude/cli/roadmap/prompts.py` | Change signature (line 161) to: `def build_extract_prompt_tdd(spec_file: Path, retrospective_content: str \| None = None, prd_file: Path \| None = None) -> str:`. No refactoring needed. [Research 02, Section: Prompt Builder 2] |
| 2.1.4 | Add PRD supplementary block to `build_extract_prompt_tdd` | `src/superclaude/cli/roadmap/prompts.py` | Conditional block with 3 check items referencing: Success Metrics (SS19), User Personas (SS7), Legal/Compliance (SS17). Shorter than spec-mode block because TDD already captures structured technical content. Guardrail: "do NOT treat PRD content as hard requirements unless also stated in the TDD." [Research 02, Section: Prompt Builder 2, drafted block text] |

### 2.2 Roadmap Spec Fidelity and Test Strategy Prompts (P1 -- Quality Gates)

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 2.2.1 | Refactor `build_spec_fidelity_prompt` to base pattern | `src/superclaude/cli/roadmap/prompts.py` | Refactor single return expression (lines 461-525) into `base = (...); return base + _OUTPUT_FORMAT_BLOCK` pattern. Behavioral output must be identical when `prd_file=None`. [Research 02, Refactoring table] |
| 2.2.2 | Add `prd_file` param and block to `build_spec_fidelity_prompt` | `src/superclaude/cli/roadmap/prompts.py` | Add `prd_file: Path \| None = None` to signature (line 448). Conditional block adds dimensions 12-15: Persona Coverage (SS7, MEDIUM), Business Metric Traceability (SS19, MEDIUM), Compliance/Legal Coverage (SS17, HIGH), Scope Boundary Enforcement (SS12, MEDIUM). Numbering continues from existing 11 dimensions. [Research 02, Section: Prompt Builder 8] |
| 2.2.3 | Wire `prd_file` to spec-fidelity step in executor | `src/superclaude/cli/roadmap/executor.py` | Add `prd_file=config.prd_file` to `build_spec_fidelity_prompt()` call (line 990). Also add `config.prd_file` to the spec-fidelity step's `inputs` list so the subprocess can read the PRD file. [Research 02, Executor Wiring table] |
| 2.2.4 | Refactor `build_test_strategy_prompt` to base pattern | `src/superclaude/cli/roadmap/prompts.py` | Refactor single return expression (lines 596-629) into base pattern. [Research 02, Refactoring table] |
| 2.2.5 | Add `prd_file` param and block to `build_test_strategy_prompt` | `src/superclaude/cli/roadmap/prompts.py` | Add `prd_file: Path \| None = None` to signature (line 586). Block with 5 items: persona-based acceptance tests (SS7), customer journey E2E tests (SS22), KPI validation tests (SS19), compliance test category (SS17), edge case coverage (SS23). [Research 02, Section: Prompt Builder 10] |
| 2.2.6 | Wire `prd_file` to test-strategy step in executor | `src/superclaude/cli/roadmap/executor.py` | Add `prd_file=config.prd_file` to `build_test_strategy_prompt()` call (line 980). Add `config.prd_file` to test-strategy step `inputs`. [Research 02, Executor Wiring table] |

### 2.3 Roadmap Generate Prompt (P1 -- Variant Shaping)

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 2.3.1 | Refactor `build_generate_prompt` to base pattern | `src/superclaude/cli/roadmap/prompts.py` | Refactor single return expression (lines 295-335) into `base = (...); return base + _INTEGRATION_ENUMERATION_BLOCK + _OUTPUT_FORMAT_BLOCK`. [Research 02, Section: Prompt Builder 3] |
| 2.3.2 | Add `prd_file` param and block to `build_generate_prompt` | `src/superclaude/cli/roadmap/prompts.py` | Add `prd_file: Path \| None = None` to signature (line 288). Block with 4 items: value-based phasing (SS5, SS19), persona-driven sequencing (SS7, SS22), compliance gates (SS17), scope guardrails (SS12). Guardrail: "do NOT let PRD override technical sequencing constraints from the extraction." [Research 02, Section: Prompt Builder 3, drafted block text] |
| 2.3.3 | Wire `prd_file` to both generate steps in executor | `src/superclaude/cli/roadmap/executor.py` | Add `prd_file=config.prd_file` to both `build_generate_prompt()` calls (lines 908, 918). Add `config.prd_file` to both generate step `inputs` lists. [Research 02, Executor Wiring table] |

### 2.4 Roadmap Score Prompt (P2 -- Variant Selection)

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 2.4.1 | Refactor `build_score_prompt` to base pattern | `src/superclaude/cli/roadmap/prompts.py` | Refactor single return expression (lines 399-413). [Research 02, Refactoring table] |
| 2.4.2 | Add `prd_file` param and block to `build_score_prompt` | `src/superclaude/cli/roadmap/prompts.py` | Add `prd_file: Path \| None = None` to signature (line 390). Block with 3 scoring dimensions: business value delivery (SS19), persona coverage (SS7), compliance alignment (SS17). [Research 02, Section: Prompt Builder 6] |
| 2.4.3 | Wire `prd_file` to score step in executor | `src/superclaude/cli/roadmap/executor.py` | Add `prd_file=config.prd_file` to `build_score_prompt()` call (line 950). [Research 02, Executor Wiring table] |

### 2.5 Tasklist Fidelity Prompt

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 2.5.1 | Add `prd_file` param to `build_tasklist_fidelity_prompt` | `src/superclaude/cli/tasklist/prompts.py` | Change signature (line 17) to: `def build_tasklist_fidelity_prompt(roadmap_file: Path, tasklist_dir: Path, tdd_file: Path \| None = None, prd_file: Path \| None = None) -> str:`. [Research 03, Section 4] |
| 2.5.2 | Add PRD supplementary block to `build_tasklist_fidelity_prompt` | `src/superclaude/cli/tasklist/prompts.py` | After TDD block (line 123), before `return base + _OUTPUT_FORMAT_BLOCK` (line 125), insert conditional: `if prd_file is not None: base += (...)`. Block with 4 checks: Persona Flow Coverage, KPI Instrumentation, Stakeholder/Compliance Tasks, UX Flow Alignment. All flagged as MEDIUM severity. [Research 03, Section 4, drafted block text] |

### 2.6 Deferred P3 Prompts (diff, debate, merge)

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 2.6.1 | Add `prd_file` parameter only (no blocks) to P3 builders | `src/superclaude/cli/roadmap/prompts.py` | Add `prd_file: Path \| None = None` to `build_diff_prompt` (line 338), `build_debate_prompt` (line 363), `build_merge_prompt` (line 416). Do NOT add supplementary blocks yet -- PRD context at these steps has diminishing returns [Research 02, Priority Matrix]. Refactoring and block text are drafted in research for future activation. |

**Phase 2 validation:** For each modified prompt builder, verify: (a) output with `prd_file=None` is byte-identical to pre-change output, (b) output with `prd_file=Path("test.md")` includes the supplementary block heading. Run `uv run pytest tests/roadmap/test_spec_fidelity.py` to confirm no regressions.

---

## Phase 3: Skill and Reference Layer

**Goal:** Update the four skill/reference documents with PRD-conditional content so that inference-based execution (via `/sc:roadmap`, `/sc:tasklist`, `/sc:spec-panel`) also benefits from PRD context. These are protocol documents consumed by Claude during inference, not by the CLI code.

**Dependencies:** Phase 2 design decisions finalized (so protocol docs align with CLI behavior).

### 3.1 Extraction Pipeline Reference

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 3.1.1 | Add PRD detection gate text | `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` | After TDD-Specific Extraction Steps (line 207), add new section: "PRD-Supplementary Extraction Context." State that PRD is NOT a new input mode -- it is injected via `--prd-file` as conditional prompt enrichment blocks. Reference the design decision from Research 04, Section 1.3. [Research 04, Section 1.2-1.3] |
| 3.1.2 | Add PRD extraction storage keys | `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` | Document proposed storage keys from Research 04: `user_personas`, `user_stories`, `success_metrics`, `market_constraints`, `release_strategy`, `stakeholder_priorities`, `acceptance_scenarios`. Note these are consumed by the inference protocol and enrich the extraction output, not as separate extraction steps. [Research 04, Section 1.2] |

### 3.2 Scoring Reference

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 3.2.1 | Add PRD scoring guidance | `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` | After TDD 7-factor formula section, add: "PRD Supplementary Scoring." State that PRD inputs use the standard 5-factor formula (Option B from Research 04, Section 2.2). Add `product` type to Type Match Lookup table with: Exact Match = product/feature, Related = improvement, Unrelated = docs/security/migration. [Research 04, Section 2.2-2.3] |

### 3.3 Tasklist SKILL.md

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 3.3.1 | Add Section 4.1b "Supplementary PRD Context" | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | New section parallel to 4.1a. PRD detection via `--prd-file` flag (no auto-detection). Six extraction keys: `user_personas`, `user_stories`, `success_metrics`, `release_strategy`, `stakeholder_priorities`, `acceptance_scenarios`. Fallback: if file doesn't exist, abort. [Research 04, Section 3.2] |
| 3.3.2 | Add Section 4.4b "Supplementary PRD Task Generation" | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | New section parallel to 4.4a. Task patterns: user stories -> `Implement user story: [actor] [goal]` tasks; success metrics -> `Validate metric: [name] meets [target]` tasks; acceptance scenarios -> `Verify acceptance: [scenario]` tasks. Note: PRD generates fewer mandatory tasks than TDD -- primary value is enrichment. [Research 04, Section 3.2] |

### 3.4 Spec Panel Command

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 3.4.1 | Add Step 6c "PRD Input Detection" | `src/superclaude/commands/spec-panel.md` | New step parallel to 6a. PRD detection gate. Panel validates completeness of personas, stories, acceptance criteria. Assesses business alignment. Unlike TDD, PRD does NOT require `target_release` scoping. [Research 04, Section 4.2] |
| 3.4.2 | Add Step 6d "Downstream Roadmap Frontmatter for PRD" | `src/superclaude/commands/spec-panel.md` | New step parallel to 6b. Conditional on `--downstream roadmap`. Ensures output contains: `spec_type: "product-requirements"`, `complexity_score`, `target_audience`, `success_metrics_count`. [Research 04, Section 4.2] |
| 3.4.3 | Add "Output -- When Input Is a PRD" section | `src/superclaude/commands/spec-panel.md` | Parallel to existing TDD output section (lines 399-405). (a) Review mode: covers Product Overview, Personas, Stories, FRs, NFRs, Metrics, Risks. (b) Scoped release spec mode: extracts FRs, NFRs, risks, acceptance criteria, priority ordering from PRD. Expert panel adjustments: Wiegers focuses on requirement-to-persona traceability, Cockburn validates user story structure, Adzic checks metric measurability, Fowler/Newman assess architectural sufficiency. [Research 04, Section 4.2] |

**Phase 3 validation:** Run `make verify-sync` to confirm `src/superclaude/` and `.claude/` are in sync after edits. Review each modified doc for internal consistency (section numbering, cross-references).

---

## Phase 4: Testing

**Goal:** Comprehensive test coverage for all 4 interaction scenarios: neither supplementary file, TDD only, PRD only, and both TDD + PRD. Tests must cover CLI flag parsing, config wiring, prompt builder output, and executor step construction.

**Dependencies:** Phases 1-2 complete (Phase 3 is doc-only and doesn't require test coverage).

### 4.1 Scenario Matrix

The four interaction scenarios that must be tested across both pipelines:

| Scenario | `--tdd-file` | `--prd-file` | Expected Behavior |
|----------|-------------|-------------|-------------------|
| A: Neither | absent | absent | Baseline behavior, no supplementary blocks in prompts, no extra files in `inputs` |
| B: TDD only | provided | absent | Existing TDD blocks active, no PRD blocks, TDD file in `inputs` |
| C: PRD only | absent | provided | PRD blocks active, no TDD blocks, PRD file in `inputs` |
| D: Both | provided | provided | Both TDD and PRD blocks active (stacked independently), both files in `inputs` |

### 4.2 Roadmap Pipeline Tests

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 4.2.1 | Test `--prd-file` CLI flag parsing | `tests/roadmap/test_commands.py` (new or extend) | Verify: flag accepted by Click, `prd_file` resolved to absolute path in `RoadmapConfig`, `None` when absent. Test invalid path produces Click error. |
| 4.2.2 | Test `build_extract_prompt` PRD block | `tests/roadmap/test_prompts.py` (new or extend) | Parametrized test for all 4 scenarios (A-D). When `prd_file` provided, output contains `"## Supplementary PRD Context"`. When absent, output does NOT contain that heading. Output with `prd_file=None` must match pre-change baseline. |
| 4.2.3 | Test `build_extract_prompt_tdd` PRD block | `tests/roadmap/test_prompts.py` | Same parametrized pattern as 4.2.2 for the TDD extractor variant. |
| 4.2.4 | Test `build_spec_fidelity_prompt` PRD dimensions | `tests/roadmap/test_spec_fidelity.py` (extend existing) | Verify dimensions 12-15 appear when `prd_file` provided. Verify dimensions 1-11 unchanged regardless of `prd_file`. |
| 4.2.5 | Test `build_test_strategy_prompt` PRD block | `tests/roadmap/test_prompts.py` | Verify PRD supplementary block appears when `prd_file` provided, absent when `None`. |
| 4.2.6 | Test `build_generate_prompt` PRD block | `tests/roadmap/test_prompts.py` | Verify refactored return structure produces identical output for `prd_file=None`. Verify PRD block present when `prd_file` provided. |
| 4.2.7 | Test `build_score_prompt` PRD block | `tests/roadmap/test_prompts.py` | Same pattern. |
| 4.2.8 | Test extract step `inputs` list | `tests/roadmap/test_executor.py` (new or extend) | Verify `_build_steps()` includes `config.prd_file` in extract step `inputs` when provided, omits when `None`. |

### 4.3 Tasklist Pipeline Tests

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 4.3.1 | Test `--prd-file` CLI flag parsing | `tests/tasklist/test_commands.py` (new or extend) | Verify flag accepted, resolved to absolute path, `None` when absent. |
| 4.3.2 | Test `build_tasklist_fidelity_prompt` PRD block | `tests/tasklist/test_prompts.py` (new or extend) | Parametrized for all 4 scenarios (A-D). When `prd_file` provided: `"## Supplementary PRD Validation"` present. When both TDD and PRD provided: both `"## Supplementary TDD Validation"` and `"## Supplementary PRD Validation"` present (stacked). [Research 03, Section 3: Both-Files Behavior] |
| 4.3.3 | Test `all_inputs` assembly | `tests/tasklist/test_executor.py` (new or extend) | Verify ordering: `[roadmap_file, *tasklist_files, tdd_file, prd_file]` when both provided. Verify PRD absent from list when `prd_file=None`. |

### 4.4 Refactoring Regression Tests

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 4.4.1 | Snapshot pre-refactor prompt output | `tests/roadmap/test_prompts.py` | Before Phase 2 refactoring, capture output of `build_generate_prompt`, `build_spec_fidelity_prompt`, `build_test_strategy_prompt`, `build_score_prompt` with current code. Store as test fixtures. After refactoring, compare output with `prd_file=None` to snapshots -- must be byte-identical. [Research 02, Gaps Q3] |

**Phase 4 validation:** `uv run pytest tests/ -v` -- all tests pass. Coverage report shows new prompt builder paths exercised for all 4 scenarios.

---

## Integration Checklist

Final verification steps before the implementation can be considered complete. Each item must pass.

### CLI Layer
- [ ] `superclaude roadmap run --help` shows `--prd-file` option with correct help text
- [ ] `superclaude tasklist validate --help` shows `--prd-file` option with correct help text
- [ ] `superclaude roadmap run spec.md --prd-file nonexistent.md` produces Click error ("Path 'nonexistent.md' does not exist")
- [ ] `superclaude roadmap run spec.md --prd-file valid-prd.md` accepted without error (dry-run or early exit is fine)
- [ ] `superclaude tasklist validate --prd-file valid-prd.md` accepted without error

### Model Layer
- [ ] `RoadmapConfig(spec_file=Path("."))` succeeds with `prd_file` defaulting to `None` [Research 01, Section 1]
- [ ] `RoadmapConfig(spec_file=Path("."), prd_file=Path("test.md"))` stores resolved path
- [ ] `TasklistValidateConfig()` succeeds with `prd_file` defaulting to `None` [Research 03, Section 2]

### Executor Layer
- [ ] Roadmap `_build_steps()` extract step `inputs` includes PRD file when `config.prd_file` is set [Research 01, Section 3]
- [ ] Roadmap `_build_steps()` extract step `inputs` does NOT include PRD file when `config.prd_file` is `None`
- [ ] Tasklist `_build_steps()` `all_inputs` includes PRD file when `config.prd_file` is set [Research 03, Section 3]
- [ ] `detect_input_type()` is NOT modified -- PRD is supplementary, not a mode [Research 01, Section 3]

### Prompt Layer
- [ ] `build_extract_prompt(Path("."))` output identical to pre-change (no `prd_file` arg)
- [ ] `build_extract_prompt(Path("."), prd_file=Path("prd.md"))` output contains `"## Supplementary PRD Context"`
- [ ] `build_extract_prompt_tdd(Path("."), prd_file=Path("prd.md"))` output contains `"## Supplementary PRD Context"`
- [ ] `build_spec_fidelity_prompt(Path("."), Path("."), prd_file=Path("prd.md"))` output contains dimensions 12-15
- [ ] `build_test_strategy_prompt(Path("."), Path("."), prd_file=Path("prd.md"))` output contains persona/KPI test items
- [ ] `build_generate_prompt(agent, Path("."), prd_file=Path("prd.md"))` output contains business-context block
- [ ] `build_tasklist_fidelity_prompt(Path("."), Path("."), prd_file=Path("prd.md"))` output contains `"## Supplementary PRD Validation"`
- [ ] All PRD blocks include the advisory guardrail: "do NOT treat PRD content as hard requirements"
- [ ] Scenario D (both TDD + PRD): both supplementary blocks present, non-overlapping

### Skill/Reference Layer
- [ ] `extraction-pipeline.md` contains PRD-supplementary section with storage keys [Research 04, Section 1.2]
- [ ] `scoring.md` contains `product` type in Type Match Lookup table [Research 04, Section 2.3]
- [ ] Tasklist `SKILL.md` contains Section 4.1b and 4.4b [Research 04, Section 3.2]
- [ ] `spec-panel.md` contains Steps 6c, 6d, and PRD output section [Research 04, Section 4.2]
- [ ] `make verify-sync` passes (src/ and .claude/ in sync)

### Testing
- [ ] `uv run pytest tests/` -- all tests pass
- [ ] All 4 interaction scenarios (A: neither, B: TDD only, C: PRD only, D: both) covered
- [ ] Refactoring regression tests confirm byte-identical output when `prd_file=None`
- [ ] No existing tests broken by the changes

---

## Phase 5: Fix Dead `tdd_file` in Roadmap Pipeline

**Goal:** Wire the existing dead `tdd_file` field on `RoadmapConfig` (models.py:115) end-to-end in the roadmap pipeline. This field was added during TDD integration but never connected to a CLI flag or used in the executor. Fix it alongside `prd_file` so both supplementary inputs are consistently wired.

**Dependencies:** Phase 1 complete (both fields exist on models).

**Context:** The `tdd_file` field on `RoadmapConfig` exists but has no `--tdd-file` CLI flag in `roadmap/commands.py` and zero references in `roadmap/executor.py`. It IS fully wired in the tasklist pipeline (commands, executor, prompts, models). This was an oversight in the original TDD integration task (TASK-RF-20260325-cli-tdd) — item 2.2 added the model field but no corresponding CLI flag or executor wiring was created for the roadmap side.

**What `tdd_file` does in the roadmap pipeline:** When the primary input is a spec (not a TDD), a user may still want to provide a TDD for supplementary enrichment — the same way `--prd-file` provides PRD enrichment. The TDD has structured data models, API specs, component inventories, test strategies, and migration plans that a spec lacks. Feeding it as supplementary context enriches the roadmap without changing the primary extraction mode.

**When `tdd_file` is NOT needed:** When the primary input IS a TDD (auto-detected or `--input-type tdd`), the TDD is already the `spec_file`. Passing `--tdd-file` in addition would be redundant. The executor should detect this case and warn/ignore.

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 5.1 | Add `--tdd-file` Click option to `run` command | `src/superclaude/cli/roadmap/commands.py` | Add `@click.option("--tdd-file", type=click.Path(exists=True, path_type=Path), default=None, help="Path to a TDD file for supplementary context enrichment.")` after the `--input-type` option. Pattern: identical to how `--prd-file` is added in Phase 1 step 1.1.2. |
| 5.2 | Add `tdd_file` to `run` function signature | `src/superclaude/cli/roadmap/commands.py` | Add `tdd_file: Path \| None` parameter. Wire into `config_kwargs` as `"tdd_file": tdd_file.resolve() if tdd_file is not None else None`. |
| 5.3 | Wire `tdd_file` into extract step inputs | `src/superclaude/cli/roadmap/executor.py` | In `_build_steps()`, modify extract step `inputs`: include `config.tdd_file` when not None, same pattern as `config.prd_file` from Phase 1 step 1.1.5. Order: `[spec_file, tdd_file (if set), prd_file (if set)]`. |
| 5.4 | Pass `tdd_file` to prompt builders | `src/superclaude/cli/roadmap/executor.py` | Add `tdd_file=config.tdd_file` kwarg to `build_extract_prompt()` and `build_extract_prompt_tdd()` calls. Also to `build_spec_fidelity_prompt()`, `build_test_strategy_prompt()`, `build_generate_prompt()`, `build_score_prompt()`. |
| 5.5 | Add `tdd_file` param and supplementary blocks to prompt builders | `src/superclaude/cli/roadmap/prompts.py` | For each prompt builder that receives `prd_file` (Phase 2), also add `tdd_file: Path \| None = None` param. Add conditional blocks: when `tdd_file` is provided AND primary input is NOT already a TDD (`input_type != "tdd"`), append supplementary TDD context block with structured data (data models, API specs, component inventory, test strategy, migration plan). When primary IS TDD, skip (redundant). |
| 5.6 | Add redundancy guard in executor | `src/superclaude/cli/roadmap/executor.py` | After `detect_input_type()`, if `config.input_type == "tdd" and config.tdd_file is not None`, emit warning: "Ignoring --tdd-file: primary input is already a TDD document." Set `config.tdd_file = None` to avoid double-injection. |
| 5.7 | Wire `tdd_file` to spec-fidelity, test-strategy, generate, score steps | `src/superclaude/cli/roadmap/executor.py` | Add `config.tdd_file` to the `inputs` list of each step that receives supplementary context (same steps that get `prd_file`). |

**Phase 5 validation:** `superclaude roadmap run --help` shows `--tdd-file`. Run `uv run pytest tests/` — all pass. Verify: when `--input-type tdd` and `--tdd-file` both provided, warning is emitted and `tdd_file` is ignored.

---

## Phase 6: Auto-Wire Supplementary Files from `.roadmap-state.json`

**Goal:** When the tasklist pipeline reads a roadmap output directory, it should auto-detect the source TDD and/or PRD files from `.roadmap-state.json` without requiring the user to pass `--tdd-file` and `--prd-file` manually. Users should never have to remember to re-pass flags that the roadmap pipeline already recorded.

**Dependencies:** Phase 1 complete (both fields exist on models). Phase 5 complete (`tdd_file` wired in roadmap).

**Context:** `.roadmap-state.json` already records `spec_file` (the primary input). We need to also record `tdd_file` and `prd_file` when they were provided during the roadmap run, and have the tasklist pipeline read them back.

### 6.1 Store Supplementary Files in Roadmap State

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 6.1.1 | Add `tdd_file` and `prd_file` to state file schema | `src/superclaude/cli/roadmap/executor.py` | In `_write_state()` or wherever `.roadmap-state.json` is composed, add `"tdd_file": str(config.tdd_file) if config.tdd_file else null` and `"prd_file": str(config.prd_file) if config.prd_file else null`. These are absolute paths, same as `spec_file`. |
| 6.1.2 | Bump `schema_version` if needed | `src/superclaude/cli/roadmap/executor.py` | If the state file has versioned schema handling, bump from 1 to 2 to indicate new fields. Old readers should tolerate unknown keys. |

### 6.2 Read Supplementary Files in Tasklist Pipeline

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 6.2.1 | Add auto-wire logic to tasklist executor | `src/superclaude/cli/tasklist/executor.py` | At the start of `_build_steps()` or in the config resolution phase, look for `.roadmap-state.json` in the same directory as `config.roadmap_file`. If found, read it. If `tdd_file` is present in the state AND `config.tdd_file is None` (user didn't pass `--tdd-file`), auto-set `config.tdd_file = Path(state["tdd_file"])` if the file still exists on disk. Same for `prd_file`. |
| 6.2.2 | Add file existence check | `src/superclaude/cli/tasklist/executor.py` | When auto-wiring from state, verify the referenced file still exists: `if Path(state["tdd_file"]).exists()`. If not (file moved/deleted since roadmap run), emit warning and leave as None. |
| 6.2.3 | Add precedence rule | `src/superclaude/cli/tasklist/executor.py` | Explicit `--tdd-file` / `--prd-file` flags always override auto-wired values. The auto-wire only fills in when the config field is None. Document this in help text. |
| 6.2.4 | Emit info message on auto-wire | `src/superclaude/cli/tasklist/executor.py` | When a supplementary file is auto-wired from state, emit: `click.echo(f"[tasklist] Auto-wired {field} from roadmap state: {path}", err=True)` so the user knows what happened. |

### 6.3 Same Auto-Wire for Roadmap Resume

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 6.3.1 | Auto-wire on `--resume` | `src/superclaude/cli/roadmap/executor.py` | When `--resume` is used, the executor already reads `.roadmap-state.json`. If `tdd_file` and `prd_file` are in the state, auto-wire them into the config (same precedence rules as 6.2.3). |

### 6.4 Skill Layer: Document Auto-Wire Behavior

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 6.4.1 | Document auto-wire in sc-tasklist SKILL.md | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | Add section documenting: when `.roadmap-state.json` exists alongside the roadmap file, the tasklist generator auto-loads `tdd_file` and `prd_file` from it. Explicit CLI flags override. This enables seamless pipeline chaining: `roadmap run spec.md --tdd-file tdd.md --prd-file prd.md` → `tasklist validate roadmap-dir/` (auto-wires both). |
| 6.4.2 | Document auto-wire in extraction-pipeline.md | `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` | Add note that `.roadmap-state.json` now stores supplementary file paths for downstream pipeline consumption. |

**Phase 6 validation:** Run `superclaude roadmap run spec.md --tdd-file tdd.md --prd-file prd.md --output dir/`. Verify `.roadmap-state.json` contains `tdd_file` and `prd_file`. Then run `superclaude tasklist validate dir/` (no `--tdd-file` or `--prd-file`). Verify both files are auto-wired and info messages emitted.

---

## Phase 7: Enrich Tasklist Generation with TDD/PRD Content

**Goal:** The tasklist *generator* (not just the validator) should read TDD and PRD source documents to produce richer, more complete task decomposition. Currently, tasklist generation only reads `roadmap.md`, which is a distilled summary that loses TDD-specific detail (exact test cases, API schemas, component props, rollback procedures) and PRD-specific context (personas, business metrics, user journeys, acceptance scenarios). The full source documents should inform task breakdown.

**Dependencies:** Phase 6 complete (auto-wiring available). Phase 1 complete (model fields exist).

**Context:** The roadmap pipeline's extraction step captures TDD/PRD content, but the generate/merge steps distill it further. By the time `roadmap.md` is written, specific test case names, API request/response schemas, component prop types, migration rollback steps, persona names, KPI targets, and acceptance scenario details are often summarized away. The tasklist generator working from `roadmap.md` alone cannot decompose tasks to the level of specificity that the original TDD/PRD provides.

### 7.1 CLI Layer: Tasklist Generate Command

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 7.1.1 | Identify tasklist generation entry point | `src/superclaude/cli/tasklist/commands.py`, `src/superclaude/cli/tasklist/executor.py` | Determine how `superclaude tasklist generate` (or equivalent) invokes the generation prompt. Identify the prompt builder function and executor step where the roadmap is read and tasks are produced. **NOTE:** The tasklist `validate` command already has `--tdd-file` and `--prd-file` (after Phase 1). The `generate` command (if separate) needs the same flags. If generation is part of the `/sc:tasklist` skill only (inference-based, no CLI), then this phase focuses on the skill layer. |
| 7.1.2 | Add `--tdd-file` and `--prd-file` to tasklist generate command | `src/superclaude/cli/tasklist/commands.py` | If a `generate` CLI command exists, add both flags following the `validate` pattern. If generation is inference-only, skip to 7.2. |
| 7.1.3 | Wire supplementary files into generation step inputs | `src/superclaude/cli/tasklist/executor.py` | Add `config.tdd_file` and `config.prd_file` to the generation step's `inputs` list so the subprocess can read them. |
| 7.1.4 | Pass supplementary files to generation prompt builder | `src/superclaude/cli/tasklist/executor.py` | Add `tdd_file=config.tdd_file, prd_file=config.prd_file` kwargs to the generation prompt builder call. |

### 7.2 Prompt Layer: Tasklist Generation Enrichment

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 7.2.1 | Add `tdd_file` param and block to tasklist generation prompt | `src/superclaude/cli/tasklist/prompts.py` | Conditional block when `tdd_file` is provided: "A Technical Design Document (TDD) is included alongside the roadmap. Use it to enrich task decomposition with: (1) Specific test cases from §15 Testing Strategy — each test case should map to a validation task with exact test name and expected behavior. (2) API endpoint schemas from §8 — each endpoint should have implementation tasks with request/response field details. (3) Component specifications from §10 — each component should have tasks with prop types, dependencies, and integration points. (4) Migration rollback steps from §19 — each rollback procedure should be a contingency task with trigger conditions. (5) Data model field definitions from §7 — each entity should have schema implementation tasks with exact field types." |
| 7.2.2 | Add `prd_file` param and block to tasklist generation prompt | `src/superclaude/cli/tasklist/prompts.py` | Conditional block when `prd_file` is provided: "A Product Requirements Document (PRD) is included alongside the roadmap. Use it to enrich task decomposition with: (1) User persona context from §7 — tasks touching user-facing flows should reference which persona is served and their specific needs. (2) Acceptance scenarios from §10/§22 — each user story acceptance criterion should map to a verification task. (3) Success metrics from §19 — tasks should include metric instrumentation subtasks (tracking, dashboards, alerts) where applicable. (4) Stakeholder priorities from §5 — task priority should reflect business value ordering, not just technical dependency. (5) Scope boundaries from §12 — tasks must not exceed defined scope; generate explicit 'out of scope' markers where roadmap milestones approach scope edges." Guardrail: "PRD context informs task descriptions and priorities but does NOT generate standalone implementation tasks. Engineering tasks come from the roadmap; PRD enriches them." |
| 7.2.3 | Handle both TDD + PRD together | `src/superclaude/cli/tasklist/prompts.py` | When both are provided, stack both blocks (TDD first, then PRD). Add interaction note: "When both TDD and PRD are available, TDD provides structural engineering detail and PRD provides product context. TDD-derived task enrichment (test cases, schemas, components) takes precedence for implementation specifics. PRD-derived enrichment (personas, metrics, priorities) shapes task descriptions, acceptance criteria, and priority ordering." |

### 7.3 Skill Layer: Tasklist Generation Protocol

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 7.3.1 | Add Section 3.x "Source Document Enrichment" to sc-tasklist SKILL.md | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | New section documenting: when the tasklist generator has access to TDD and/or PRD source documents (via auto-wired paths from `.roadmap-state.json` or explicit `--tdd-file`/`--prd-file` flags), it MUST read them and use their structured content to produce more specific, actionable task decomposition. Without source documents, the generator works from the roadmap alone (current behavior). With source documents, the generator cross-references roadmap milestones against source document sections to produce tasks with: exact function/class names from TDD, specific test case references, persona-tagged acceptance criteria from PRD, metric instrumentation subtasks, and migration contingency tasks. |
| 7.3.2 | Update existing Section 4.4a "Supplementary TDD Task Generation" | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | Expand from validation-only to also cover generation enrichment. Currently 4.4a describes task patterns for validation checks. Add generation-time enrichment: component inventory → implementation tasks with named components, test strategy → validation tasks with named test cases, migration plan → deployment tasks with rollback steps. |
| 7.3.3 | Update Section 4.4b "Supplementary PRD Task Generation" | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | Same expansion: from validation-only to generation enrichment. User stories → implementation tasks tagged with persona, success metrics → instrumentation subtasks, acceptance scenarios → verification tasks with specific criteria. |
| 7.3.4 | Add enrichment to extraction-pipeline.md | `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` | Document that tasklist generation is a downstream consumer of TDD/PRD content. Note that the extraction step's output (extraction.md) feeds the roadmap, but the original TDD/PRD files should also be available to the tasklist generator for finer-grained task decomposition that extraction.md's summary doesn't capture. |

**Phase 7 validation:** Generate a tasklist from a roadmap that was produced from a TDD with `--tdd-file` and `--prd-file`. Compare task specificity against a tasklist generated from the same roadmap without supplementary files. The enriched tasklist should contain: named test cases, named components, named API endpoints, persona references, metric targets — none of which appear in the non-enriched version.

---

## Change Summary

| Category | Files Modified | Lines Added (est.) |
|----------|---------------|-------------------|
| Models | `roadmap/models.py`, `tasklist/models.py` | ~6 |
| Commands (CLI) | `roadmap/commands.py`, `tasklist/commands.py` | ~40 (both `--tdd-file` and `--prd-file` on roadmap; `--prd-file` on tasklist; generate command flags) |
| Executors | `roadmap/executor.py`, `tasklist/executor.py` | ~80 (wiring, auto-wire from state, redundancy guard, state file schema) |
| Prompts | `roadmap/prompts.py`, `tasklist/prompts.py` | ~200 (PRD blocks + TDD supplementary blocks in roadmap prompts + generation enrichment blocks in tasklist prompts + refactoring) |
| Skill/Reference docs | `extraction-pipeline.md`, `scoring.md`, `SKILL.md`, `spec-panel.md` | ~250 (auto-wire docs, generation enrichment protocol, expanded 4.4a/4.4b) |
| Tests | `tests/roadmap/`, `tests/tasklist/` | ~300 |
| **Total** | **~14 files** | **~876 lines** |

All changes are additive with `None` defaults. Zero backward-compatibility risk.

### Phases Summary

| Phase | Scope | CLI | Skills |
|-------|-------|-----|--------|
| 1 | Model/CLI plumbing for `--prd-file` | YES | — |
| 2 | Prompt enrichment for PRD context | YES | — |
| 3 | Skill/reference layer for PRD protocol | — | YES |
| 4 | Testing (all 4 interaction scenarios) | YES | — |
| 5 | Fix dead `tdd_file` in roadmap pipeline | YES | — |
| 6 | Auto-wire from `.roadmap-state.json` | YES | YES |
| 7 | Enrich tasklist generation with TDD/PRD | YES | YES |

### The 4 Requirements This Plan Addresses

1. **Auto-wire `tdd_file` from `.roadmap-state.json`** → Phase 6, steps 6.2.1-6.2.4
2. **Wire dead `tdd_file` in roadmap pipeline end-to-end** → Phase 5, steps 5.1-5.7
3. **Auto-wire `prd_file` from `.roadmap-state.json`** → Phase 6, steps 6.1.1-6.1.2 + 6.2.1-6.2.4
4. **Enrich tasklist generation (not just validation) with full TDD/PRD content** → Phase 7, steps 7.1.1-7.3.4
