# Research: PRD Implementation Task Mapping

**Researcher**: researcher-2
**Status**: Complete
**Source**: `.dev/tasks/to-do/TASK-RF-20260327-prd-pipeline/TASK-RF-20260327-prd-pipeline.md`
**Goal**: Map all 10 phases (61 items) to specific E2E test scenarios

---

## Summary

The PRD pipeline implementation task (TASK-RF-20260327-prd-pipeline) modifies **12 target files** across 10 phases / 61 checklist items. It adds `--prd-file` as a supplementary input to both `roadmap run` and `tasklist validate` pipelines, wires the dead `tdd_file` field end-to-end, refactors 4 prompt builders to base pattern, adds PRD supplementary blocks to 9 builders, stores supplementary paths in `.roadmap-state.json`, and implements auto-wire logic in the tasklist pipeline.

---

## Phase-by-Phase Analysis

### Phase 1: Setup and Prerequisites (3 items: 1.1-1.3)

**What it implements**: Administrative setup -- reads task file, creates handoff directories, verifies research files.

**Files modified**: Task file itself (frontmatter status update only)

**New behaviors**: None (administrative only)

**Derived E2E test scenario**: NONE -- no testable behavior changes.

---

### Phase 2: CLI Plumbing -- Roadmap Pipeline (6 items: 2.1-2.6)

**What it implements**: Adds `prd_file` data path through the roadmap CLI pipeline.

**Files modified**:
- `src/superclaude/cli/roadmap/models.py` -- add `prd_file: Path | None = None` field to `RoadmapConfig` (after `tdd_file` at line 115)
- `src/superclaude/cli/roadmap/commands.py` -- add `--prd-file` Click option, `prd_file` function parameter, `prd_file` entry in `config_kwargs` dict
- `src/superclaude/cli/roadmap/executor.py` -- add `config.prd_file` to step inputs (extract, generate-A, generate-B, spec-fidelity, test-strategy)

**New CLI flags**:
- `--prd-file` on `roadmap run`: `type=click.Path(exists=True, path_type=Path), default=None, help="Path to a PRD file for supplementary business context enrichment."`

**New model fields**:
- `RoadmapConfig.prd_file: Path | None = None`

**Note**: Item 2.6 is deferred to Phase 4 (kwargs to builders deferred until signatures updated)

**Derived E2E test scenarios**:
1. `roadmap run spec.md --prd-file prd.md` accepts the flag and resolves to absolute path in `RoadmapConfig`
2. `roadmap run spec.md` (no `--prd-file`) results in `config.prd_file = None`
3. `roadmap run spec.md --prd-file nonexistent.md` produces Click error "does not exist"
4. PRD file appears in step input lists when provided (executor wiring)

---

### Phase 3: CLI Plumbing -- Tasklist Pipeline (5 items: 3.1-3.5)

**What it implements**: Adds `prd_file` data path through the tasklist CLI pipeline.

**Files modified**:
- `src/superclaude/cli/tasklist/models.py` -- add `prd_file: Path | None = None` field to `TasklistValidateConfig` (after `tdd_file` at line 25)
- `src/superclaude/cli/tasklist/commands.py` -- add `--prd-file` Click option, `prd_file` function parameter, `prd_file` entry in `TasklistValidateConfig(...)` construction
- `src/superclaude/cli/tasklist/executor.py` -- add `config.prd_file` to `all_inputs` list

**New CLI flags**:
- `--prd-file` on `tasklist validate`: `type=click.Path(exists=True, path_type=Path), default=None, help="Path to the PRD file used as an additional validation input."`

**New model fields**:
- `TasklistValidateConfig.prd_file: Path | None = None`

**Note**: kwarg wiring to `build_tasklist_fidelity_prompt()` deferred to item 4.7b

**Derived E2E test scenarios**:
5. `tasklist validate --prd-file prd.md` accepts the flag in `TasklistValidateConfig`
6. `tasklist validate` (no `--prd-file`) results in `config.prd_file = None`
7. `tasklist validate --prd-file nonexistent.md` produces Click error

---

### Phase 4: Prompt Builder Refactoring + P1 Enrichment (10 items: 4.1-4.8b)

> **QA NOTE (2026-03-27):** The tasklist fidelity PRD wiring described in items 4.7b and the `build_tasklist_fidelity_prompt` entry below is **already implemented** on this branch. Specifically: `prd_file: Path | None = None` parameter exists at `prompts.py` line 21, the conditional PRD validation block exists at lines 126-139, and `prd_file=config.prd_file` is passed at `executor.py` line 206. These items can be treated as complete for E2E test planning purposes.

**What it implements**: Refactors 4 prompt builders from single-return to `base = (...)` pattern, adds `prd_file` parameter to 6 builders, adds PRD supplementary blocks to 6 builders, wires executor kwargs.

**Files modified**:
- `src/superclaude/cli/roadmap/prompts.py` -- 5 builders modified:
  - `build_extract_prompt` (line 82): add `prd_file` param + PRD block (5 checks: S6, S7, S12, S17, S19 + advisory guardrail)
  - `build_generate_prompt` (line 288): REFACTOR to base pattern + add `prd_file` param + PRD block (4 checks: S5, S7, S12, S17, S19, S22 + guardrail "do NOT let PRD override technical sequencing")
  - `build_spec_fidelity_prompt` (line 448): REFACTOR to base pattern + add `prd_file` param + PRD block (dimensions 12-15: Persona Coverage S7, Business Metric Traceability S19, Compliance/Legal S17 HIGH, Scope Boundary S12)
  - `build_test_strategy_prompt` (line 586): REFACTOR to base pattern + add `prd_file` param + PRD block (5 checks: S7, S17, S19, S22, S23)
  - `build_score_prompt` (line 390): REFACTOR to base pattern + add `prd_file` param + PRD block (3 dimensions: business value S19, persona coverage S7, compliance S17)
- `src/superclaude/cli/tasklist/prompts.py` -- 1 builder modified:
  - `build_tasklist_fidelity_prompt` (line 17): add `prd_file` param + PRD block (3 checks: S7, S12, S19, S22 MEDIUM severity)
- `src/superclaude/cli/roadmap/executor.py` -- item 4.8b: add `prd_file=config.prd_file` to 7 call sites
- `src/superclaude/cli/tasklist/executor.py` -- item 4.7b: add `prd_file=config.prd_file` to `build_tasklist_fidelity_prompt()` call

**New prompt builder parameters**:
- `prd_file: Path | None = None` added to: `build_extract_prompt`, `build_generate_prompt`, `build_score_prompt`, `build_spec_fidelity_prompt`, `build_test_strategy_prompt`, `build_tasklist_fidelity_prompt`

**PRD block conditional pattern** (all builders):
```python
if prd_file is not None:
    base += (...)  # PRD supplementary block with specific section checks
```

**Critical design invariant**: When `prd_file=None`, output is byte-identical to pre-change behavior.

**Derived E2E test scenarios**:
8. Each refactored builder (`generate`, `score`, `spec_fidelity`, `test_strategy`) produces IDENTICAL output when `prd_file=None` (refactoring regression test)
9. Each builder with PRD block includes `"## Supplementary PRD Context"` heading ONLY when `prd_file` is provided
10. `build_extract_prompt(spec, prd_file=Path("p.md"))` includes advisory guardrail text
11. `build_spec_fidelity_prompt` with PRD adds dimensions 12-15; compliance dimension 14 is HIGH severity, others are MEDIUM
12. `build_test_strategy_prompt` with PRD includes 5 specific check items (persona-based acceptance, customer journey E2E, KPI validation, compliance test category, edge case coverage)
13. `build_tasklist_fidelity_prompt` with PRD includes block after existing TDD block, before return
14. All 6 modified builders accept `prd_file=None` default without error (import verification)

---

### Phase 5: P2 Prompt Enrichment + P3 API Stubs (4 items: 5.1-5.4)

**What it implements**: PRD enrichment for `build_extract_prompt_tdd` (P2), plus `prd_file` parameter-only stubs (no blocks) for 3 P3 builders.

**Files modified**:
- `src/superclaude/cli/roadmap/prompts.py`:
  - `build_extract_prompt_tdd` (line 161): add `prd_file` param + PRD block (3 checks: S7, S17, S19 + guardrail "do NOT treat PRD content as hard requirements unless also stated in the TDD")
  - `build_diff_prompt` (line 338): add `prd_file: Path | None = None` param only (no block, P3 stub)
  - `build_debate_prompt` (line 363): add `prd_file: Path | None = None` param only (no block, P3 stub)
  - `build_merge_prompt` (line 416): add `prd_file: Path | None = None` param only (no block, P3 stub)

**Derived E2E test scenarios**:
15. `build_extract_prompt_tdd` with `prd_file` includes advisory guardrail about not treating PRD as hard requirements
16. P3 stubs (`diff`, `debate`, `merge`) accept `prd_file` kwarg without error but do not modify output

---

### Phase 6: Fix Dead tdd_file in Roadmap Pipeline (6 items: 6.1-6.5)

**What it implements**: Wires the existing dead `tdd_file` field on `RoadmapConfig` end-to-end: CLI flag, executor wiring, prompt builder params, and a REDUNDANCY GUARD.

**Files modified**:
- `src/superclaude/cli/roadmap/commands.py`:
  - New `--tdd-file` Click option: `type=click.Path(exists=True, path_type=Path), default=None, help="Path to a TDD file for supplementary technical context enrichment."`
  - New `tdd_file: Path | None` function parameter
  - New `tdd_file` entry in `config_kwargs`
  - Option ordering: `--input-type`, `--tdd-file`, `--prd-file`, `@click.pass_context`
- `src/superclaude/cli/roadmap/executor.py`:
  - Conditional append of `config.tdd_file` to step inputs BEFORE `config.prd_file` (ordering: `[spec_file, tdd_file, prd_file]`)
  - **REDUNDANCY GUARD** (item 6.3): When `config.input_type == "tdd"` AND `config.tdd_file is not None`, emits warning and sets `tdd_file = None` via `dataclasses.replace(config, tdd_file=None)`
  - Warning message: `"[roadmap] WARNING: Ignoring --tdd-file: primary input is already a TDD document. The --tdd-file flag is for supplementary context when the primary input is a spec."`
  - Item 6.4b: add `tdd_file=config.tdd_file` kwarg to all 7 builder call sites
- `src/superclaude/cli/roadmap/prompts.py`:
  - `tdd_file: Path | None = None` added to ALL 9 builders that accept `prd_file` (placed BEFORE `prd_file`)
  - NO TDD supplementary blocks added (only the parameter, for API consistency)

**Redundancy guard behavior (DETAILED)**:
- **When**: Primary input IS a TDD (`input_type == "tdd"`) and user ALSO passed `--tdd-file`
- **What happens**: Warning emitted to stderr, `config.tdd_file` silently set to `None`
- **Why**: Prevents the LLM from receiving the same TDD content twice (once as primary input, once as supplementary)
- **Location**: After input type detection, before step construction in `_build_steps()`

**Derived E2E test scenarios**:
17. `roadmap run spec.md --tdd-file tdd.md` accepts the flag and wires to `RoadmapConfig.tdd_file`
18. **Scenario F (redundancy guard)**: `roadmap run tdd.md --tdd-file tdd.md` with auto-detected `input_type="tdd"` emits warning and sets `tdd_file=None`
19. Step inputs ordering is `[spec_file, tdd_file (if set), prd_file (if set)]`
20. All 9 builders accept `tdd_file` kwarg (placed before `prd_file`)

---

### Phase 7: Skill and Reference Layer Updates (5 items: 7.1-7.5)

**What it implements**: Updates 4 skill/reference documents for inference-based workflows.

**Files modified**:
- `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` -- new "PRD-Supplementary Extraction Context" section with 7 storage keys: `user_personas`, `user_stories`, `success_metrics`, `market_constraints`, `release_strategy`, `stakeholder_priorities`, `acceptance_scenarios`
- `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` -- new "PRD Supplementary Scoring" section + `product` type in Type Match Lookup table (Exact=product/feature, Related=improvement, Unrelated=docs/security/migration)
- `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` -- new Section 4.1b "Supplementary PRD Context" (6 extraction keys, abort-on-missing-file) + Section 4.4b "Supplementary PRD Task Generation" (task patterns for user stories, success metrics, acceptance scenarios)
- `src/superclaude/commands/spec-panel.md` -- Step 6c "PRD Input Detection", Step 6d "Downstream Roadmap Frontmatter for PRD", "Output -- When Input Is a PRD" section
- Item 7.5: `make verify-sync` to confirm src/ and .claude/ are in sync

**Derived E2E test scenarios**:
21. `make verify-sync` passes after skill layer updates (sync integrity)
22. Skill documents contain expected new sections (content validation, not E2E per se)

---

### Phase 8: Auto-Wire from .roadmap-state.json (5 items: 8.1-8.5)

**What it implements**: State persistence + downstream auto-detection of supplementary files.

**Files modified**:
- `src/superclaude/cli/roadmap/executor.py`:
  - `_save_state()` at line 1361: adds 3 new keys to state dict: `"tdd_file"`, `"prd_file"`, `"input_type"`
  - `_restore_from_state()` at line 1661: auto-wire `tdd_file` and `prd_file` from state on `--resume` when CLI flags absent; checks file existence on disk; emits warning if file missing
- `src/superclaude/cli/tasklist/commands.py`:
  - Auto-wire logic in `validate()` function between default resolution (line 104) and config construction (line 106)
  - Uses `from ..roadmap.executor import read_state` to read `.roadmap-state.json`
  - Precedence rule: explicit CLI flag > auto-wired from state > None
  - Info messages emitted: `"[tasklist validate] Auto-wired --tdd-file from .roadmap-state.json: {path}"`
  - Warning on missing file: emits warning, leaves as None
- Skill docs updated (8.4): tasklist SKILL.md + extraction-pipeline.md with auto-wire documentation

**New state file fields**:
```json
{
  "tdd_file": "<absolute path or null>",
  "prd_file": "<absolute path or null>",
  "input_type": "<spec|tdd>"
}
```

**Auto-wire precedence rules**:
1. Explicit CLI flag always wins
2. Auto-wired from `.roadmap-state.json` when flag is None AND file exists on disk
3. None (no enrichment)

**Auto-wire messages**:
- Info: `[tasklist validate] Auto-wired --tdd-file from .roadmap-state.json: {path}`
- Info: `[tasklist validate] Auto-wired --prd-file from .roadmap-state.json: {path}`
- Warning (stderr): when auto-wired file path does not exist on disk

**Derived E2E test scenarios**:
23. After `roadmap run spec.md --tdd-file t.md --prd-file p.md`, `.roadmap-state.json` contains `tdd_file`, `prd_file`, `input_type` keys
24. `tasklist validate output-dir/` auto-wires `tdd_file` and `prd_file` from state when CLI flags absent
25. Explicit `tasklist validate --tdd-file other.md output-dir/` overrides auto-wired value (precedence test)
26. Auto-wire with non-existent file on disk emits warning and leaves field as None
27. Auto-wire with no `.roadmap-state.json` produces no error and no auto-wiring
28. `roadmap run --resume` auto-wires `tdd_file`/`prd_file` from state when flags absent

---

### Phase 9: Enrich Tasklist Generation with TDD/PRD Content (4 items: 9.1-9.4)

**What it implements**: Generation enrichment (not just validation) with TDD/PRD content.

**Files modified**:
- `src/superclaude/cli/tasklist/executor.py` -- wire `tdd_file`/`prd_file` to generation prompt builder if CLI generate command exists
- `src/superclaude/cli/tasklist/prompts.py` -- either modify existing or create new `build_tasklist_generate_prompt` with:
  - TDD generation enrichment block (5 checks): test cases, API schemas, components, rollback steps, data models
  - PRD generation enrichment block (5 checks): persona context, acceptance scenarios, success metrics, stakeholder priorities, scope boundaries
  - Guardrail: "PRD context informs task descriptions and priorities but does NOT generate standalone implementation tasks"
  - Combined TDD+PRD interaction note
- `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` -- expand Sections 4.4a/4.4b with generation enrichment; add Section 3.x "Source Document Enrichment"

**Enrichment content that should appear in tasklists**:
- From TDD: component inventory -> implementation tasks with named components; test strategy -> validation tasks with named test cases; migration plan -> deployment tasks with rollback steps
- From PRD: user stories -> implementation tasks tagged with persona; success metrics -> instrumentation subtasks; acceptance scenarios -> verification tasks with specific criteria

**Derived E2E test scenarios**:
29. Tasklist generation prompt with `tdd_file` includes TDD enrichment block (5 check items)
30. Tasklist generation prompt with `prd_file` includes PRD enrichment block (5 check items) + guardrail text
31. Generation prompt with both `tdd_file` and `prd_file` includes combined interaction note
32. Generation prompt with neither file has no enrichment blocks
33. Item 9.1 discovery: does `tasklist generate` CLI command exist? (assessment output at `phase-outputs/discovery/tasklist-generate-assessment.md`)

---

### Phase 10: Testing and Final Verification (13 items: 10.1-10.12)

**What it implements**: Comprehensive test suite for all 6 interaction scenarios.

**Files created/modified**:
- `tests/roadmap/test_prd_cli.py` (new) -- CLI flag tests for roadmap
- `tests/roadmap/test_prd_prompts.py` (new) -- prompt builder tests for roadmap
- `tests/roadmap/test_spec_fidelity.py` (extend) -- refactoring regression test
- `tests/tasklist/test_prd_cli.py` (new) -- CLI flag tests for tasklist
- `tests/tasklist/test_prd_prompts.py` (new) -- prompt builder tests for tasklist
- `tests/tasklist/test_autowire.py` (new) -- auto-wire from state file tests

**The 6 Interaction Scenarios (A-F)**:

| Scenario | Description | Primary Input | tdd_file | prd_file | Key Behavior | Test Items |
|----------|-------------|---------------|----------|----------|--------------|------------|
| A | Neither flag (baseline) | spec | None | None | Output unchanged from pre-change | 10.2, 10.7 |
| B | TDD primary only | tdd (auto-detected) | None | None | TDD extraction, zero supplementary blocks | 10.3b |
| C | PRD only | spec | None | Path | PRD supplementary block appears with guardrail | 10.2, 10.7 |
| D | TDD primary + PRD | tdd | None | Path | TDD extraction + PRD block | 10.2, 10.7 |
| E | Spec + TDD supp + PRD | spec | Path | Path | Both supplementary blocks present, non-overlapping | 10.3b |
| F | TDD primary + --tdd-file (redundancy) | tdd | Path | any | Redundancy guard warns and sets tdd_file=None | 10.8 |

---

## Cross-Phase Test Mapping: All Derived E2E Test Scenarios

Below is the complete list of E2E test scenarios derived from the implementation phases. Each is numbered and tagged with the phase it originates from.

### CLI Flag Tests

| # | Scenario | Pipeline | Test |
|---|----------|----------|------|
| 1 | `--prd-file` accepted on `roadmap run` | roadmap | Flag parsing + path resolution |
| 2 | `--prd-file` defaults to None when absent | roadmap | Default behavior |
| 3 | `--prd-file` with invalid path errors | roadmap | Click validation |
| 5 | `--prd-file` accepted on `tasklist validate` | tasklist | Flag parsing + path resolution |
| 6 | `--prd-file` defaults to None when absent | tasklist | Default behavior |
| 7 | `--prd-file` with invalid path errors | tasklist | Click validation |
| 17 | `--tdd-file` accepted on `roadmap run` | roadmap | Flag parsing + path resolution |

### Prompt Builder Tests (Scenario A-E coverage)

| # | Scenario | Builder | Assertion |
|---|----------|---------|-----------|
| 8 | Refactoring regression | generate, score, spec_fidelity, test_strategy | Output identical when prd_file=None |
| 9 | PRD block conditional | All 6 enriched builders | `"## Supplementary PRD Context"` present only when prd_file provided |
| 10 | Extract guardrail | build_extract_prompt | Advisory guardrail text present with PRD |
| 11 | Fidelity dimensions | build_spec_fidelity_prompt | Dimensions 12-15 only with PRD; dim 14 = HIGH |
| 12 | Test strategy checks | build_test_strategy_prompt | 5 specific PRD check items present |
| 13 | Tasklist fidelity ordering | build_tasklist_fidelity_prompt | PRD block after TDD block, before return |
| 14 | Import verification | All modified builders | Accept prd_file=None without error |
| 15 | TDD extract guardrail | build_extract_prompt_tdd | "do NOT treat PRD content as hard requirements" guardrail |
| 16 | P3 stubs | diff, debate, merge | Accept prd_file kwarg, output unchanged |
| 20 | tdd_file parameter | All 9 builders | Accept tdd_file kwarg before prd_file |

### Redundancy Guard Tests (Scenario F)

| # | Scenario | Test |
|---|----------|------|
| 18 | Redundancy guard fires | input_type="tdd" + tdd_file provided -> warning + tdd_file=None |
| 19 | Input ordering | Step inputs are [spec_file, tdd_file, prd_file] |

### Auto-Wire Tests

| # | Scenario | Test |
|---|----------|------|
| 23 | State persistence | .roadmap-state.json contains tdd_file, prd_file, input_type after run |
| 24 | Auto-wire from state | tasklist validate auto-detects from state when flags absent |
| 25 | Explicit flag precedence | CLI flag overrides auto-wired value |
| 26 | Missing file handling | Auto-wired path that doesn't exist -> warning + None |
| 27 | No state file | No .roadmap-state.json -> no auto-wire, no error |
| 28 | Resume auto-wire | roadmap --resume auto-wires from state |

### Generation Enrichment Tests

| # | Scenario | Test |
|---|----------|------|
| 29 | TDD generation enrichment | Generation prompt with tdd_file includes 5 TDD checks |
| 30 | PRD generation enrichment | Generation prompt with prd_file includes 5 PRD checks + guardrail |
| 31 | Combined enrichment | Both files -> combined interaction note present |
| 32 | No enrichment | Neither file -> no enrichment blocks |
| 33 | Generate command discovery | Does `tasklist generate` CLI exist? (may be inference-only) |

### Full Pipeline Integration

| # | Scenario | Test |
|---|----------|------|
| 34 | Full pipeline chain | `roadmap run spec.md --tdd-file t.md --prd-file p.md` followed by `tasklist validate output/` with auto-wire |
| 35 | Full regression | `uv run pytest tests/ -v` -- no pre-existing test failures introduced |

---

## Key Implementation Details for E2E Test Design

### 1. All Changes Are Additive with None Defaults
Every new field (`prd_file`, `tdd_file` on tasklist config) defaults to `None`. Every conditional block uses `if X is not None:`. This means ALL existing behavior is preserved when the new flags are absent. E2E tests MUST verify this invariant.

### 2. Builder Refactoring Creates a Testable Seam
The single-return to base-pattern refactoring in Phase 4 creates a testable seam: you can call any builder with `prd_file=None` and compare output to a baseline. This is the regression test.

### 3. Redundancy Guard Is in the Executor, Not the Builder
The redundancy guard (Phase 6 item 6.3) lives in `_build_steps()` in the roadmap executor. Testing it requires constructing a `RoadmapConfig` with `input_type="tdd"` and `tdd_file=Path(...)`, then either calling the guard logic directly or mocking the executor. Item 10.8 acknowledges this may need an integration test approach.

### 4. Auto-Wire Uses `read_state()` from Roadmap Module
The tasklist auto-wire (Phase 8 item 8.3) imports `read_state` from `superclaude.cli.roadmap.executor`. This cross-module dependency should be tested with real temp files and `.roadmap-state.json` fixtures.

### 5. PRD Section References (S-numbers)
The PRD blocks reference specific PRD template sections. These are:
- S5: Scope & boundaries
- S6: Target users/personas (used in extract)
- S7: User personas (used in MOST builders)
- S12: Scope boundary enforcement
- S17: Compliance/legal requirements (HIGH severity in spec-fidelity)
- S19: Success metrics/KPIs
- S22: User stories
- S23: Edge cases

### 6. Tasklist Generate May Be Inference-Only
Phase 9 item 9.1 explicitly investigates whether a `tasklist generate` CLI command exists. If it doesn't, generation enrichment is skill-layer only (not testable via CLI E2E). The E2E test task should handle both cases.

---

## Files Modified Summary (All Phases)

| File | Phases | Changes |
|------|--------|---------|
| `src/superclaude/cli/roadmap/models.py` | 2 | +prd_file field |
| `src/superclaude/cli/roadmap/commands.py` | 2, 6 | +--prd-file flag, +--tdd-file flag, +params, +config_kwargs |
| `src/superclaude/cli/roadmap/executor.py` | 2, 4, 6, 8 | +step inputs, +builder kwargs, +redundancy guard, +state persistence, +resume auto-wire |
| `src/superclaude/cli/roadmap/prompts.py` | 4, 5, 6 | 4 refactors, 6 PRD blocks, 9 tdd_file params, 3 P3 stubs |
| `src/superclaude/cli/tasklist/models.py` | 3 | +prd_file field |
| `src/superclaude/cli/tasklist/commands.py` | 3, 8 | +--prd-file flag, +auto-wire logic |
| `src/superclaude/cli/tasklist/executor.py` | 3, 4, 9 | +prd_file input, +builder kwargs, +generation wiring |
| `src/superclaude/cli/tasklist/prompts.py` | 4, 9 | +prd_file param+block on fidelity, +generation enrichment |
| `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` | 7, 8 | +PRD extraction section, +auto-wire docs |
| `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` | 7 | +PRD scoring section, +product type row |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | 7, 8, 9 | +4.1b, +4.4b, +auto-wire docs, +3.x source enrichment |
| `src/superclaude/commands/spec-panel.md` | 7 | +6c, +6d, +PRD output section |
