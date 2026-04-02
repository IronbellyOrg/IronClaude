---
id: TASK-RF-20260325-cli-tdd
title: "CLI TDD Integration — Dual Extract Prompt with --input-type Flag"
status: done-cli-layer
completion_date: 2026-03-26
start_date: 2026-03-26
updated_date: 2026-03-26
priority: high
created: 2026-03-25
type: implementation
template: complex
estimated_items: 29
estimated_phases: 8
---

# CLI TDD Integration — Dual Extract Prompt with --input-type Flag

## Task Overview

This task implements Option A from TASK-RESEARCH-20260325-001: add an `--input-type [spec|tdd]` flag to `superclaude roadmap run`, create a dedicated `build_extract_prompt_tdd()` function with 14 extraction sections (8 existing + 6 new TDD-specific), branch the executor to route TDD inputs through the new prompt builder, generalize the fidelity prompt for TDD comparison dimensions, and optionally add `--tdd-file` to `superclaude tasklist validate`. All changes are backward-compatible — existing spec inputs continue to work unchanged via defaulted fields following the established `convergence_enabled`/`allow_regeneration` extension pattern.

The extract step is the single chokepoint: all generate, diff, debate, score, and merge steps receive ONLY extraction output and never see the original input file. The current `build_extract_prompt()` misses 8 of 28 TDD sections entirely (Data Models, API Specifications, State Management, Component Inventory, Testing Strategy, Operational Readiness, Cost Estimation, Glossary). Content not surfaced at extraction is permanently lost to the pipeline. This task creates the TDD-aware extraction path that captures all high-value TDD sections.

## Key Objectives

- Add `--input-type [spec|tdd]` Click option to `superclaude roadmap run` (default: `spec`)
- Add `input_type` field to `RoadmapConfig` dataclass (backward-compatible default)
- Create `build_extract_prompt_tdd()` with 14 body sections covering all major TDD content areas
- Branch `_build_steps()` in `roadmap/executor.py` to route TDD inputs to the new prompt builder
- Generalize `build_spec_fidelity_prompt()` for TDD comparison dimensions (API contracts, components, testing, migration, operations)
- Add `--tdd-file` to `superclaude tasklist validate` and `tdd_file` to `TasklistValidateConfig` (optional/deferred phase)
- Document open questions (semantic_layer.py, structural_checkers.py, wiring_config) as known risks
- Verify backward compatibility: `superclaude roadmap run spec.md` behavior unchanged

## Prerequisites and Dependencies

**Research Completed:**
- Primary source: `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/RESEARCH-REPORT-cli-tdd-integration.md` (SS8 Implementation Plan)
- Supporting research: 6 topic-specific files in `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/research/`
- QA: Research gate PASS (10/10), Report structural QA PASS (19/19), Report qualitative QA PASS

**Source Files (all under `src/superclaude/cli/`):**
- `roadmap/commands.py` — CLI entry point for `superclaude roadmap run`
- `roadmap/models.py` — `RoadmapConfig` dataclass
- `roadmap/executor.py` — Pipeline step construction (`_build_steps()` at ~line 809-820)
- `roadmap/prompts.py` — All prompt builders (9 functions)
- `tasklist/commands.py` — CLI entry point for `superclaude tasklist validate`
- `tasklist/models.py` — `TasklistValidateConfig` dataclass
- `tasklist/executor.py` — Tasklist validation step construction
- `tasklist/prompts.py` — Tasklist prompt builders

**Open Questions (from research — carry as known risks):**
- C-1: Does `semantic_layer.py` read `spec_file` in active pipeline? If yes, 4th implementation point.
- C-2: Does `structural_checkers.py` have spec-format assumptions? If yes, may need TDD changes.
- I-1: Does `run_wiring_analysis` `wiring_config` reference `spec_file`? If yes, 5th implementation point.
- B-1: DEVIATION_ANALYSIS_GATE `ambiguous_count`/`ambiguous_deviations` field mismatch — pre-existing bug, separate fix.

**Documentation Staleness:** None found. All research findings are CODE-VERIFIED against actual source files with line numbers. One stale docstring (`prompts.py:6-8` says executor uses `--file <path>` but actual behavior is inline embedding) does not affect implementation.

---

## Phase 1: Setup and Handoff Directory Creation (2 items)

- [x] **1.1** Read this task file in full to understand all phases, objectives, and open questions. Update the `status` field in this file's YAML frontmatter from `to-do` to `in-progress`. Once done, mark this item as complete.

- [x] **1.2** Create the handoff directory structure for intra-task outputs: create the directory `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/phase-outputs/` and subdirectories `discovery/`, `test-results/`, `reviews/`, and `reports/`. These directories will hold intermediate outputs passed between phases. If any directory already exists, skip it. Once done, mark this item as complete.

---

## Phase 2: CLI and Config Layer (5 items)

> **Purpose:** Wire the `--input-type` flag through the CLI entry point and config model. No logic changes — pure additive wiring. This phase is the prerequisite for all subsequent phases.

- [x] **2.1** Read the file `commands.py` at `src/superclaude/cli/roadmap/commands.py` to understand the existing Click option decorators and `run()` function signature, then add a new `@click.option("--input-type", type=click.Choice(["spec", "tdd"], case_sensitive=False), default="spec", help="Type of input file for roadmap generation. Default: spec.")` decorator to the `run` command (place after the existing `--retrospective` option), add `input_type: str` as a keyword argument to the `run()` function signature, and add `"input_type": input_type` to the `config_kwargs` dict assembly before the `RoadmapConfig(**config_kwargs)` call, ensuring the decorator follows the exact Click pattern used by existing options like `--depth` which uses `click.Choice`, no existing options are modified, and the function signature change is additive only. If unable to complete due to unexpected file structure, log the specific blocker in the Phase 2 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [x] **2.2** Read the file `models.py` at `src/superclaude/cli/roadmap/models.py` to understand the `RoadmapConfig` dataclass field declarations and the established backward-compatible extension pattern (see `convergence_enabled: bool = False` and `allow_regeneration: bool = False`), then add two new fields to `RoadmapConfig`: `input_type: Literal["spec", "tdd"] = "spec"` and `tdd_file: Path | None = None`, placed after the existing `allow_regeneration` field, ensuring the `Literal` type is imported from `typing` if not already imported, both fields have defaults that preserve existing behavior, and no existing fields are modified. If unable to complete due to missing imports or unexpected dataclass structure, log the specific blocker in the Phase 2 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [x] **2.3** Read the file `commands.py` at `src/superclaude/cli/tasklist/commands.py` to understand the existing Click option decorators and `validate()` function signature, then add a new `@click.option("--tdd-file", type=click.Path(exists=True, path_type=Path), default=None, help="Path to the TDD file used as an additional validation input.")` decorator to the `validate` command, add `tdd_file: Path | None` as a keyword argument to the `validate()` function signature, and add `tdd_file=tdd_file.resolve() if tdd_file is not None else None` to the config construction kwargs, ensuring no existing options are modified and the new option is fully optional. If unable to complete due to unexpected file structure, log the specific blocker in the Phase 2 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [x] **2.4** Read the file `models.py` at `src/superclaude/cli/tasklist/models.py` to understand the `TasklistValidateConfig` dataclass field declarations, then add one new field: `tdd_file: Path | None = None`, placed after the existing `tasklist_dir` field, ensuring the `Path` type is imported if not already and no existing fields are modified. If unable to complete due to unexpected dataclass structure, log the specific blocker in the Phase 2 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [x] **2.5** Verify Phase 2 completion by running the following two commands: `uv run python -c "from superclaude.cli.roadmap.models import RoadmapConfig; from pathlib import Path; c = RoadmapConfig(spec_file=Path('.')); print(c.input_type); assert c.input_type == 'spec'; assert c.tdd_file is None; print('PASS')"` and `uv run python -c "from superclaude.cli.tasklist.models import TasklistValidateConfig; c = TasklistValidateConfig(); print(c.tdd_file); assert c.tdd_file is None; print('PASS')"`, ensuring both print `PASS`. Write the verification results to `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/phase-outputs/test-results/phase2-verification.md` containing the command outputs and pass/fail status. If either verification fails, log the error in the Phase 2 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

---

## Phase 3: TDD Extract Prompt — Critical Path (6 items)

> **Purpose:** Create `build_extract_prompt_tdd()` — the single highest-impact change. The extract step is the chokepoint: all downstream generate, diff, debate, score, and merge steps receive ONLY extraction output. Content not surfaced here is permanently lost. Do NOT modify `build_extract_prompt()`. CRITICAL: the existing `build_extract_prompt()` ends with `+ _OUTPUT_FORMAT_BLOCK` (a module-level constant that forces Claude to start output with YAML frontmatter). The new function MUST also append this block or EXTRACT_GATE will fail.

- [x] **3.1** Read the file `prompts.py` at `src/superclaude/cli/roadmap/prompts.py` to understand the existing `build_extract_prompt(spec_file, retrospective_content=None)` function structure. Document in `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/phase-outputs/discovery/extract-prompt-structure.md`: (a) the exact line range of `build_extract_prompt()`, (b) the 8 existing body section names, (c) the 13 existing frontmatter fields, (d) the identifier language text, (e) the retrospective content block pattern, (f) the exact usage of `_OUTPUT_FORMAT_BLOCK` — how is it appended (string concatenation? f-string? what does the constant contain?), (g) whether `_INTEGRATION_ENUMERATION_BLOCK` or `_INTEGRATION_WIRING_DIMENSION` constants are used in the extract prompt (or only in other prompts), (h) what other module-level string constants exist in prompts.py that might be relevant. Also read `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/research/06-tdd-template-structure.md` for the 6 new TDD section extraction instructions. This discovery file is the reference for items 3.2-3.4. If unable to read either file, log the blocker in the Phase 3 Findings section of the Task Log, then mark this item complete. Once done, mark this item as complete.

- [x] **3.2** Read the discovery file at `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/phase-outputs/discovery/extract-prompt-structure.md`, then read `src/superclaude/cli/roadmap/prompts.py` and create the function shell for `build_extract_prompt_tdd(spec_file: Path, retrospective_content: str | None = None) -> str` inserted immediately AFTER `build_extract_prompt()`. This item creates the function with: (a) identical signature to `build_extract_prompt()`, (b) the `base` string variable opening with neutralized framing — "You are a requirements and design extraction specialist.\n\nRead the provided source specification or technical design document and produce a requirements and design extraction document.\n\n", (c) the YAML frontmatter instruction block retaining all 13 existing fields AND adding 6 new fields: `data_models_identified` (integer), `api_surfaces_identified` (integer), `components_identified` (integer), `test_artifacts_identified` (integer), `migration_items_identified` (integer), `operational_items_identified` (integer) — each described as "(integer) count of items identified, or 0 if section absent", (d) broadened identifier language: "Preserve exact identifiers from the source document including requirement IDs (FR-xxx, NFR-xxx), interface names, endpoint identifiers, component names, migration phase names, and test case IDs. If a source uses FR-EVAL-001.1, use FR-EVAL-001.1. If identifiers need sub-decomposition, use suffixes on the original ID.", (e) the instruction "Set `spec_source` to the filename of the input document" to preserve backward compatibility with all 5 gates that check `spec_source`. The function body at this point should contain ONLY the frontmatter instruction and identifier language — the body sections are added in items 3.3 and 3.4. End the base string with a comment marker `# Body sections follow` so items 3.3-3.4 know where to insert. Do NOT add `_OUTPUT_FORMAT_BLOCK` yet — that is added in item 3.5. If unable to complete, log the blocker in the Phase 3 Findings section. Once done, mark this item as complete.

- [x] **3.3** Read `src/superclaude/cli/roadmap/prompts.py` and locate the `build_extract_prompt_tdd()` function created in item 3.2. Append the 8 existing body sections to the `base` string variable, copying the EXACT instruction text from the existing `build_extract_prompt()` function for each section: `## Functional Requirements` (with the verbatim ID preservation and sub-decomposition instructions), `## Non-Functional Requirements` (with verbatim ID preservation), `## Complexity Assessment`, `## Architectural Constraints`, `## Risk Inventory`, `## Dependency Inventory`, `## Success Criteria`, `## Open Questions`. Copy the text character-for-character from the existing function — do NOT paraphrase or rewrite. The only difference is the broadened identifier language from item 3.2 which replaces the spec-specific FR/NFR examples. Verify by reading the function back that all 8 sections are present with instruction text. If unable to complete, log the blocker in the Phase 3 Findings section. Once done, mark this item as complete.

- [x] **3.4** Read `src/superclaude/cli/roadmap/prompts.py` and locate the `build_extract_prompt_tdd()` function. Append 6 new TDD-specific body sections to the `base` string variable AFTER the 8 existing sections: (1) `## Data Models and Interfaces` — "Extract all data entities, TypeScript/code interfaces, field definitions with types/constraints/required status, entity relationships, data-flow steps, and storage/retention/backup strategy from fenced code blocks and markdown tables. For each entity: name, fields, types, constraints, relationships.", (2) `## API Specifications` — "Extract endpoint inventory: HTTP method, URL path, auth requirements, rate limits, query parameters, request body schema, response schema, error codes and responses, versioning strategy, deprecation policy. Extract from endpoint tables and code examples even when no behavioral shall/must language is present.", (3) `## Component Inventory` — "Extract route/page tables, shared component tables with props/usage/locations, ASCII component hierarchy trees, state stores with shape/transitions/triggers/side effects. For each component: name, type, location, dependencies.", (4) `## Testing Strategy` — "Extract test pyramid breakdown with coverage levels/tooling/targets/ownership, concrete test case tables with test-name/input/expected-output/mocks for unit/integration/E2E levels, and test environment matrix.", (5) `## Migration and Rollout Plan` — "Extract migration phases with tasks/duration/dependencies/rollback, feature flags with purpose/status/cleanup-date/owner, rollout stages with audience/success-criteria/monitoring/rollback-triggers, and numbered rollback procedure steps. Preserve sequential ordering as it implies task dependencies.", (6) `## Operational Readiness` — "Extract runbook scenarios with symptoms/diagnosis/resolution/escalation/prevention, on-call expectations with page-volume/MTTD/MTTR/knowledge-prerequisites, capacity planning with current/projected/scaling-triggers, and observability including log formats, metric definitions, alert thresholds, trace sampling, and dashboard specifications." Then add the `if retrospective_content:` block mirroring the EXACT pattern from `build_extract_prompt()` (read it from the existing function). Finally, append `_OUTPUT_FORMAT_BLOCK` using the EXACT same concatenation pattern as `build_extract_prompt()` (e.g., `return base + _OUTPUT_FORMAT_BLOCK` or `base += _OUTPUT_FORMAT_BLOCK` — match whatever pattern the existing function uses). Verify by reading the function back that it ends with the output format block. If unable to complete, log the blocker in Phase 3 Findings. Once done, mark this item as complete.

- [x] **3.5** Verify that `build_extract_prompt_tdd` is importable and structurally correct by running `uv run python -c "from superclaude.cli.roadmap.prompts import build_extract_prompt_tdd, build_extract_prompt, _OUTPUT_FORMAT_BLOCK; from pathlib import Path; p = Path('test.md'); p.write_text('# Test'); result = build_extract_prompt_tdd(p); assert '## Data Models and Interfaces' in result; assert '## API Specifications' in result; assert '## Component Inventory' in result; assert '## Testing Strategy' in result; assert '## Migration and Rollout Plan' in result; assert '## Operational Readiness' in result; assert 'data_models_identified' in result; assert 'MUST begin with YAML frontmatter' in result or 'output_format' in result.lower() or _OUTPUT_FORMAT_BLOCK in result, 'CRITICAL: _OUTPUT_FORMAT_BLOCK missing — EXTRACT_GATE will fail'; old = build_extract_prompt(p); assert '## Data Models and Interfaces' not in old; assert 'specification file' in old.lower() or 'specification' in old.lower(), 'Old prompt was modified — must be unchanged'; p.unlink(); print('PASS')"`, ensuring it prints `PASS`. This verifies: (a) all 6 new TDD sections present, (b) `_OUTPUT_FORMAT_BLOCK` included, (c) new frontmatter fields present, (d) existing `build_extract_prompt()` is unmodified. Write results to `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/phase-outputs/test-results/phase3-verification.md`. If verification fails, log the error in Phase 3 Findings. Once done, mark this item as complete.

- [x] **3.6** Verify TDD extraction against a real TDD file by running `uv run python -c "from superclaude.cli.roadmap.prompts import build_extract_prompt_tdd; from pathlib import Path; tdd = Path('src/superclaude/examples/tdd_template.md'); assert tdd.exists(), 'TDD template not found'; result = build_extract_prompt_tdd(tdd); sections = ['## Functional Requirements', '## Non-Functional Requirements', '## Complexity Assessment', '## Architectural Constraints', '## Risk Inventory', '## Dependency Inventory', '## Success Criteria', '## Open Questions', '## Data Models and Interfaces', '## API Specifications', '## Component Inventory', '## Testing Strategy', '## Migration and Rollout Plan', '## Operational Readiness']; missing = [s for s in sections if s not in result]; assert not missing, f'Missing sections: {missing}'; assert 'spec_source' in result, 'spec_source field missing — gates will fail'; print(f'PASS: all {len(sections)} sections present, spec_source field present')"`, ensuring it prints `PASS` with all 14 sections confirmed. This uses the actual TDD template file, not a stub. Write results to `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/phase-outputs/test-results/phase3-tdd-template-test.md`. If verification fails, log the error in Phase 3 Findings. Once done, mark this item as complete.

---

## Phase 4: Executor Branching (3 items)

> **Purpose:** Route `--input-type tdd` to the new prompt builder. Two localized code changes in `executor.py` plus a documentation comment. No changes to anti-instinct or spec-fidelity wiring — `config.spec_file` IS the TDD file and passes through unchanged.

- [x] **4.1** Read the file `executor.py` at `src/superclaude/cli/roadmap/executor.py` focusing on the import block (approximately lines 1-55) and the `_build_steps()` method (approximately lines 775-930, specifically the extract step construction at approximately lines 809-820), then add `build_extract_prompt_tdd` to the existing import from `superclaude.cli.roadmap.prompts` (which already imports `build_extract_prompt` and other prompt builders), ensuring the import is added to the existing import statement rather than creating a duplicate import line. If unable to locate the import block or the function is not yet available (Phase 3 incomplete), log the blocker in the Phase 4 Findings section of the Task Log, then mark this item complete. Once done, mark this item as complete.

- [x] **4.2** Read the file `executor.py` at `src/superclaude/cli/roadmap/executor.py` focusing on the `_build_steps()` method's extract step construction (approximately lines 809-820 where `build_extract_prompt(config.spec_file, ...)` is called), then modify the extract prompt construction to branch on `config.input_type`: if `config.input_type == "tdd"`, call `build_extract_prompt_tdd(config.spec_file, retrospective_content=retrospective_content)` (or whatever the existing retrospective argument pattern is); otherwise call the existing `build_extract_prompt(config.spec_file, ...)` unchanged. Add an inline comment: `# TDD input routing: --input-type tdd uses dedicated TDD extraction sections`. Ensure: the branch uses the exact same arguments for both code paths (only the function name differs), no other step constructions in `_build_steps()` are modified, `config.spec_file` is used for both paths (the TDD file is passed as the positional `spec_file` argument), and the existing spec path remains byte-identical. If unable to complete due to unexpected `_build_steps()` structure, log the specific blocker in the Phase 4 Findings section of the Task Log, then mark this item complete. Once done, mark this item as complete.

- [x] **4.3** Read the file `executor.py` at `src/superclaude/cli/roadmap/executor.py` focusing on the `_run_structural_audit()` call site (approximately line 515-520) which runs after the extract step, then add a documentation comment above or near the structural audit call noting: `# NOTE: _run_structural_audit() is warning-only and uses spec heading patterns. TDD heading structure differs. Do not rely on structural audit results for TDD correctness. See open question C-2 (structural_checkers.py investigation needed).` Do NOT modify any code logic — this is documentation only. Ensure the comment does not break any existing code. If unable to locate the structural audit call, log the blocker in the Phase 4 Findings section of the Task Log, then mark this item complete. Once done, mark this item as complete.

---

## Phase 5: Fidelity Prompt Update (2 items)

> **Purpose:** Generalize `build_spec_fidelity_prompt()` so it works for both spec and TDD inputs. This prompt receives `spec_file` directly (which IS the TDD file in TDD mode) and compares it against the generated roadmap. The current language is spec-bound and must be broadened. No signature change — the function still takes `(spec_file: Path, roadmap_path: Path)`.

- [x] **5.1** Read the file `prompts.py` at `src/superclaude/cli/roadmap/prompts.py` focusing on the `build_spec_fidelity_prompt(spec_file, roadmap_path)` function, and also read the prompt language audit at `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/research/02-prompt-language-audit.md` (the `build_spec_fidelity_prompt()` section) to understand the exact spec-specific text that must change, then modify `build_spec_fidelity_prompt()` in place to: (a) change the analyst role from "specification fidelity analyst" to "source-document fidelity analyst", (b) change input label references from "specification file" to "source specification or TDD file" and from "requirements in the specification" to "requirements, design decisions, or commitments in the source document", (c) broaden identifier examples beyond `(FR-NNN)`, `(NFR-NNN)`, `(SC-NNN)` to also include `(interface-name)`, `(endpoint-path)`, `(component-name)`, `(migration-phase)`, `(test-case-id)`, (d) change "spec's priority ordering" to "source document's priority ordering or stated importance hierarchy", (e) add 5 new comparison dimensions to the fidelity analysis instructions: API endpoints and request/response contracts, component and module inventory, testing strategy and validation matrix, migration/rollout/rollback procedures, and operational readiness including runbooks and alerts. Ensure: the function signature `build_spec_fidelity_prompt(spec_file: Path, roadmap_path: Path) -> str` is NOT changed, all existing comparison dimensions are retained (only additions and text generalizations), and the changes work for both spec and TDD inputs (generalized language, not TDD-only). If unable to complete due to unexpected function structure, log the specific blocker in the Phase 5 Findings section of the Task Log, then mark this item complete. Once done, mark this item as complete.

- [x] **5.2** Verify the fidelity prompt update by running `uv run python -c "from superclaude.cli.roadmap.prompts import build_spec_fidelity_prompt; from pathlib import Path; p = Path('test.md'); p.write_text('# Test'); r = Path('roadmap.md'); r.write_text('# Roadmap'); result = build_spec_fidelity_prompt(p, r); assert 'source-document fidelity analyst' in result or 'source document fidelity analyst' in result.lower(); assert 'specification fidelity analyst' not in result; p.unlink(); r.unlink(); print('PASS')"`, ensuring it prints `PASS` confirming the role text has been generalized and the old spec-specific text is gone. Write results to `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/phase-outputs/test-results/phase5-verification.md`. If verification fails, log the error in the Phase 5 Findings section of the Task Log, then mark this item complete. Once done, mark this item as complete.

---

## Phase 6: Gate Schema Review and Pipeline Guardrail (4 items)

> **Purpose:** The 5 gates requiring `spec_source` need NO code changes — `build_extract_prompt_tdd()` instructs the LLM to emit `spec_source: <tdd_filename>`. DEVIATION_ANALYSIS_GATE is structurally incompatible with TDD (`routing_update_spec` field, `DEV-\d+` taxonomy). Rather than silently letting the pipeline fail at that step, this phase adds a guardrail that warns users upfront when running with `--input-type tdd` that deviation analysis will not work correctly.

- [x] **6.1** Read the file `gates.py` at `src/superclaude/cli/roadmap/gates.py` to confirm that EXTRACT_GATE, GENERATE_A_GATE, GENERATE_B_GATE, MERGE_GATE, and TEST_STRATEGY_GATE all require `spec_source` as a field name (not `source_document` or any alias), and confirm that DEVIATION_ANALYSIS_GATE has the `ambiguous_count` required field vs `ambiguous_deviations` semantic check mismatch (pre-existing bug B-1 from research). Write a gate compatibility review to `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/phase-outputs/reviews/gate-compatibility-review.md` containing: (a) confirmation that all 5 `spec_source` gates will pass when TDD extraction emits `spec_source: <tdd_filename>` as instructed by `build_extract_prompt_tdd()`, (b) confirmation of DEVIATION_ANALYSIS_GATE field mismatch bug (B-1), (c) note that DEVIATION_ANALYSIS_GATE redesign is deferred to separate future work, (d) note that ANTI_INSTINCT_GATE semantic checks are format-agnostic (pure Python) and need no changes, (e) ANTI_INSTINCT_GATE TDD performance hypothesis (I-5) is unverified. Ensure the review is evidence-based referencing specific gate field names and semantic check function names from the source code, and no content is fabricated. If unable to read gates.py, log the blocker in the Phase 6 Findings section of the Task Log, then mark this item complete. Once done, mark this item as complete.

- [x] **6.2** Read the file `commands.py` at `src/superclaude/cli/roadmap/commands.py` and locate the `run()` function body after `RoadmapConfig` construction and before `execute_roadmap()` is called. Add a warning block: `if config.input_type == "tdd": click.echo(click.style("WARNING: --input-type tdd is experimental. The pipeline's deviation-analysis step (DEVIATION_ANALYSIS_GATE) is not TDD-compatible and may fail. The extract→generate→diff→debate→score→merge→anti-instinct→test-strategy→spec-fidelity steps will work correctly. If the pipeline halts at deviation-analysis, this is a known limitation — not a bug in your TDD input.", fg="yellow"), err=True)`. This ensures users know upfront that TDD mode has a known pipeline limitation rather than encountering a cryptic gate failure mid-run. Ensure the warning is printed to stderr (not stdout) so it doesn't interfere with pipeline output. If unable to locate the insertion point, log the blocker in Phase 6 Findings. Once done, mark this item as complete.

- [x] **6.3** Read the gate compatibility review at `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/phase-outputs/reviews/gate-compatibility-review.md` to confirm the findings, then add a documentation comment at the top of `gates.py` at `src/superclaude/cli/roadmap/gates.py` (after existing module-level comments/docstrings) noting: `# TDD Compatibility Notes (TASK-RF-20260325-cli-tdd):` followed by `# - spec_source gates (EXTRACT, GENERATE_A/B, MERGE, TEST_STRATEGY): compatible — TDD prompt emits spec_source with TDD filename` and `# - DEVIATION_ANALYSIS_GATE: NOT TDD-compatible — deferred to separate work. Pre-existing bug: ambiguous_count/ambiguous_deviations field mismatch (B-1).` and `# - ANTI_INSTINCT_GATE: format-agnostic (pure Python). TDD performance hypothesis unverified (I-5).`. Ensure the comment block is placed after any existing module docstring and before the first import or gate definition, and no gate logic is modified. If unable to add the comment due to file structure, log the blocker in the Phase 6 Findings section of the Task Log, then mark this item complete. Once done, mark this item as complete.

---

- [x] **6.4** Read the file `prompts.py` at `src/superclaude/cli/roadmap/prompts.py` focusing on `build_generate_prompt(agent, extraction_path)` to understand which extraction frontmatter fields it references by name (the research audit found it references all 13 original fields: `spec_source`, `functional_requirements`, `nonfunctional_requirements`, etc.). Add a comment block inside `build_generate_prompt()` at the point where extraction frontmatter fields are listed, noting: `# TDD mode: extraction.md may contain additional frontmatter fields (data_models_identified, api_surfaces_identified, components_identified, test_artifacts_identified, migration_items_identified, operational_items_identified) and additional body sections (Data Models, API Specs, Component Inventory, Testing Strategy, Migration Plan, Operational Readiness) when generated by build_extract_prompt_tdd(). The roadmap should address these sections when present. Full TDD-aware generate prompt update is deferred — see TASK-RF-20260325-cli-tdd Deferred Work Items.` This is documentation only — no logic changes. The comment ensures a future implementer knows the generate prompt is not yet TDD-aware. If unable to locate the field reference block, log the blocker in Phase 6 Findings. Once done, mark this item as complete.

---

## Phase 7: Tasklist Validate TDD Enrichment — Optional (2 items)

> **Purpose:** When `--tdd-file` is passed to `superclaude tasklist validate`, enrich the validation with TDD-specific test case and rollback procedure coverage checks. This phase is optional and can be deferred without affecting the core roadmap pipeline TDD support. Depends on Phase 2 (config layer) being complete.

- [x] **7.1** Read the file `executor.py` at `src/superclaude/cli/tasklist/executor.py` focusing on the `_build_steps()` method to understand how validation step inputs are assembled (specifically the `all_inputs` or equivalent variable that collects input files for the fidelity step), then add a conditional block: if `config.tdd_file is not None`, append or include the TDD file path in the validation step's input file list so the fidelity prompt receives the TDD content alongside the roadmap and tasklist artifacts. Ensure: when `config.tdd_file is None` (the default), behavior is completely unchanged — no new inputs are added, and existing tasklist validation works identically. If unable to locate the input assembly logic or the file structure differs from expectations, log the specific blocker in the Phase 7 Findings section of the Task Log, then mark this item complete. Once done, mark this item as complete.

- [x] **7.2** Read the file `prompts.py` at `src/superclaude/cli/tasklist/prompts.py` focusing on the `build_tasklist_fidelity_prompt(roadmap_file: Path, tasklist_dir: Path)` function signature and its return value. The current function takes only `roadmap_file` and `tasklist_dir` — it has NO TDD parameter. To support TDD enrichment: (a) add an optional parameter `tdd_file: Path | None = None` to the function signature, (b) at the end of the function body (before the `return` or the `+ _OUTPUT_FORMAT_BLOCK` concatenation), add a conditional block: `if tdd_file is not None:` that appends additional comparison instructions to the prompt string: "## Supplementary TDD Validation (when TDD file is provided)\n\nA Technical Design Document (TDD) is included in the inputs alongside the roadmap and tasklist. Additionally check:\n1. Test cases from the TDD's Testing Strategy section (§15) should have corresponding validation or test tasks in the tasklist.\n2. Rollback procedures from the TDD's Migration & Rollout Plan section (§19) should have corresponding contingency or rollback tasks.\n3. Components listed in the TDD's Component Inventory (§10) should have corresponding implementation tasks.\nFlag missing coverage as MEDIUM severity deviations." Ensure: when `tdd_file is None` (the default), the prompt is byte-identical to the current version — zero behavioral change for existing callers. Then update the call site in `tasklist/executor.py` `_build_steps()` to pass `tdd_file=config.tdd_file` to the prompt builder if the config has a tdd_file attribute. If the function structure differs from expectations or the prompt uses a different concatenation pattern, log the specific blocker in the Phase 7 Findings section of the Task Log, then mark this item complete. Once done, mark this item as complete.

---

## Phase 8: Integration Testing and Final Verification (5 items)

> **Purpose:** Verify backward compatibility and TDD mode end-to-end. Create proper pytest tests (not just inline scripts). Add input-type validation. Run the full test suite.

- [x] **8.1** Add input-type validation to `src/superclaude/cli/roadmap/commands.py`. Read the file and locate the `run()` function body after the `RoadmapConfig` construction. Add a validation check: if `config.input_type == "tdd"`, read the first 500 bytes of `config.spec_file` and check if the YAML frontmatter contains `type:` with a value containing "Technical Design Document". If not found, print a warning: `click.echo(click.style("WARNING: --input-type tdd was specified but the input file does not appear to be a TDD (no 'type: Technical Design Document' in YAML frontmatter). Proceeding anyway, but extraction results may be suboptimal.", fg="yellow"), err=True)`. This is a warning, not a blocker — the pipeline proceeds regardless. Ensure: when `input_type == "spec"` (the default), no validation is performed and behavior is completely unchanged. If unable to locate the insertion point, log the blocker in Phase 8 Findings. Once done, mark this item as complete.

- [x] **8.2** Create a pytest test file at `tests/cli/test_tdd_extract_prompt.py` by reading the existing test patterns in `tests/` (use Glob to find `tests/**/*test*.py` and read one representative test file to understand the project's test conventions — imports, fixtures, assertion style). Create the test file with these test functions: (a) `test_build_extract_prompt_tdd_has_all_14_sections` — calls `build_extract_prompt_tdd()` with a dummy Path and asserts all 14 section headings are present in the returned string, (b) `test_build_extract_prompt_tdd_has_tdd_frontmatter_fields` — asserts the 6 new frontmatter field names appear in the returned string, (c) `test_build_extract_prompt_tdd_has_output_format_block` — imports `_OUTPUT_FORMAT_BLOCK` and asserts it appears in the returned string, (d) `test_build_extract_prompt_tdd_preserves_spec_source` — asserts "spec_source" appears in the returned string, (e) `test_build_extract_prompt_unchanged` — calls `build_extract_prompt()` and asserts "Data Models and Interfaces" is NOT in the output (proving the old function was not modified), (f) `test_build_extract_prompt_tdd_with_retrospective` — calls with a retrospective string and asserts it appears in output, (g) `test_roadmap_config_input_type_default` — constructs `RoadmapConfig(spec_file=Path("."))` and asserts `config.input_type == "spec"` and `config.tdd_file is None`. Run the tests with `uv run pytest tests/cli/test_tdd_extract_prompt.py -v` and write results to `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/phase-outputs/test-results/phase8-pytest-results.md`. If unable to create the file or tests fail, log in Phase 8 Findings. Once done, mark this item as complete.

- [x] **8.3** Run the existing test suite with `uv run pytest tests/ -v --tb=short 2>&1 | head -100` to verify no regressions were introduced by Phases 2-7. If any tests fail that were passing before this task, investigate whether the failure is related to the changes made in this task (check if the failing test references `RoadmapConfig`, `TasklistValidateConfig`, `build_extract_prompt`, `build_spec_fidelity_prompt`, `_build_steps`, or any of the modified files). Write the test results summary to `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/phase-outputs/test-results/phase8-regression-tests.md` containing: number of tests passed/failed/skipped, any failures with their test names and error summaries, and whether failures are related to this task's changes. If tests fail due to unrelated issues (pre-existing failures), note them but do not block. If tests fail due to this task's changes, log the specific failures in the Phase 8 Findings section of the Task Log, then mark this item complete. Once done, mark this item as complete.

- [x] **8.4** Run backward compatibility verification by executing `uv run python -c "from superclaude.cli.roadmap.prompts import build_extract_prompt; from pathlib import Path; p = Path('test-spec.md'); p.write_text('# Spec\\n## Requirements\\nFR-001: Test requirement'); result = build_extract_prompt(p); assert '## Functional Requirements' in result; assert '## Data Models and Interfaces' not in result; assert 'specification file' in result.lower() or 'specification' in result.lower(); p.unlink(); print('BACKWARD COMPAT PASS')"` to confirm the original `build_extract_prompt()` is completely unchanged (still has spec language, still has only 8 sections, no TDD sections leaked in). Also run `uv run python -c "from superclaude.cli.roadmap.models import RoadmapConfig; from pathlib import Path; c = RoadmapConfig(spec_file=Path('.')); assert c.input_type == 'spec'; assert c.tdd_file is None; print('CONFIG DEFAULT PASS')"` to confirm defaults. Write results to `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/phase-outputs/test-results/phase8-backward-compat.md`. If any check fails, log the error in the Phase 8 Findings section of the Task Log, then mark this item complete. Once done, mark this item as complete.

- [x] **8.5** Write a final integration report to `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/phase-outputs/reports/final-integration-report.md` by reading all verification files in `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/phase-outputs/test-results/` (use Glob to discover all `.md` files in that directory) and the gate compatibility review at `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/phase-outputs/reviews/gate-compatibility-review.md`, then synthesize a report containing: (a) Phase-by-phase completion status (all 8 phases), (b) verification results summary (all pass/fail from test-results files), (c) backward compatibility confirmation, (d) known risks and open questions carried forward (C-1, C-2, I-1, I-5, B-1 from research), (e) deferred work items (DEVIATION_ANALYSIS_GATE redesign, spec_source aliasing, build_generate_prompt TDD awareness, build_test_strategy_prompt TDD enrichment), (f) recommendation for next steps. Update this task file's YAML frontmatter `status` from `in-progress` to `done-cli-layer` — use `done-cli-layer` rather than `done` because open questions C-1 (semantic_layer.py) and C-2 (structural_checkers.py) remain unresolved, meaning full TDD pipeline support is not yet confirmed. Note this distinction in the report: "CLI layer changes are complete and tested. Full TDD pipeline support requires resolving C-1 and C-2." Ensure the report is evidence-based. If unable to read any verification file, note the gap. Once done, mark this item as complete.

---

## Task Log / Notes

### Execution Log

| Timestamp | Phase | Item | Status | Notes |
|-----------|-------|------|--------|-------|
| | | | | |

### Phase 2 Findings

_No findings yet._

### Phase 3 Findings

_No findings yet._

### Phase 4 Findings

_No findings yet._

### Phase 5 Findings

_No findings yet._

### Phase 6 Findings

_No findings yet._

### Phase 7 Findings

_No findings yet._

### Phase 8 Findings

_No findings yet._

### Open Questions Carried from Research

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| C-1 | Does `semantic_layer.py` read `spec_file` in active pipeline? If yes, 4th implementation point. | OPEN | Investigate before declaring TDD support complete. |
| C-2 | Does `structural_checkers.py` have spec-format assumptions? If yes, may need TDD changes. | OPEN | Investigate before relying on structural audit for TDD. |
| I-1 | Does `run_wiring_analysis` `wiring_config` reference `spec_file`? If yes, 5th implementation point. | OPEN | Investigate before declaring TDD support complete. |
| I-5 | ANTI_INSTINCT_GATE TDD performance hypothesis — unverified. | OPEN | Run empirical comparison with sample TDD vs spec. |
| B-1 | DEVIATION_ANALYSIS_GATE `ambiguous_count`/`ambiguous_deviations` field mismatch — pre-existing bug. | OPEN | File as separate defect. |

### Deferred Work Items

| Item | Rationale | Dependency |
|------|-----------|------------|
| DEVIATION_ANALYSIS_GATE redesign | Structurally incompatible with TDD; requires `routing_update_spec` rename and deviation taxonomy generalization. Separate scope. | None — independent future work. |
| `spec_source` field aliasing to `source_document` | Functionally deferrable — TDD prompt emits `spec_source` with TDD filename. Semantically desirable but not blocking. | Requires consumer enumeration (I-2). |
| `build_generate_prompt()` TDD awareness | Update to consume expanded TDD extraction frontmatter fields and explicitly plan roadmap sections around TDD artifacts. | Phase 3 complete (TDD extraction schema defined). |
| `build_test_strategy_prompt()` TDD enrichment | Strengthen to derive tests from TDD SS15 artifacts when present in extraction. | Phase 3 complete. |
| `spec_parser.py` TypeScript interface extraction | `extract_function_signatures()` only parses Python `def/class`. TypeScript `interface` not extracted. | Separate enhancement. |
| `fingerprint.py` API endpoint path extraction | URL paths like `/users/{id}` don't match identifier regex. | Separate enhancement. |
