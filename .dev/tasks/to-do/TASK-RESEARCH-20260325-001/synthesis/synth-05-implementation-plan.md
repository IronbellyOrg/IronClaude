# §8 Implementation Plan — CLI TDD Integration (Option A: Explicit --input-type Flag)

**Report:** Technical Research Report — CLI TDD Integration
**Section:** §8 Implementation Plan
**Option:** A — Explicit `--input-type [spec|tdd]` flag
**Date:** 2026-03-25
**Status:** Synthesis complete; open questions noted inline

---

> **Scope of Option A:** Add `--input-type [spec|tdd]` to `superclaude roadmap run`. When `--input-type tdd` is passed, the pipeline routes through a new `build_extract_prompt_tdd()` builder instead of the existing `build_extract_prompt()`. All other pipeline steps are unchanged. Backward compatibility is preserved: the default value is `spec`, making the existing behavior unchanged for callers who do not pass the flag.

---

## Phase 1: CLI and Config Layer

**Prerequisite for everything else. No logic changes — pure wiring.**

### 1.1 `roadmap/commands.py` — Add `--input-type` flag to `roadmap run`

| Step | Action | File | Details |
|------|--------|------|---------|
| 1.1.1 | Add Click option decorator before `run()` function | `src/superclaude/cli/roadmap/commands.py` | Insert `@click.option` block using exact pattern from research file 05 (see below). Place after existing `--retrospective` option, before the `def run(...)` signature line. |
| 1.1.2 | Add `input_type: str` to `run()` function signature | `src/superclaude/cli/roadmap/commands.py` | Add as keyword argument alongside other Click-bound params. |
| 1.1.3 | Add `"input_type": input_type` to `config_kwargs` dict | `src/superclaude/cli/roadmap/commands.py` | The `config_kwargs` dict is assembled before `RoadmapConfig(**config_kwargs)` is called. Add the key there. |

**Exact Click decorator (from research file 05):**
```
@click.option(
    "--input-type",
    type=click.Choice(["spec", "tdd"], case_sensitive=False),
    default="spec",
    help="Type of input file for roadmap generation. Default: spec.",
)
```

### 1.2 `roadmap/models.py` — Extend `RoadmapConfig`

| Step | Action | File | Details |
|------|--------|------|---------|
| 1.2.1 | Add `input_type` field to `RoadmapConfig` dataclass | `src/superclaude/cli/roadmap/models.py` | `input_type: Literal["spec", "tdd"] = "spec"` — add after existing `allow_regeneration` field, following the established defaulted-field extension pattern (confirmed by `convergence_enabled`, `allow_regeneration`). Requires adding `Literal` to the `typing` import if not already present. |
| 1.2.2 | Add `tdd_file` field to `RoadmapConfig` dataclass | `src/superclaude/cli/roadmap/models.py` | `tdd_file: Path \| None = None` — add after `input_type`. This field is reserved for future use (Phase 6); adding it now costs nothing and avoids a second models.py change. |

### 1.3 `tasklist/commands.py` — Add `--tdd-file` flag to `tasklist validate`

| Step | Action | File | Details |
|------|--------|------|---------|
| 1.3.1 | Add Click option decorator before `validate()` function | `src/superclaude/cli/tasklist/commands.py` | Insert `@click.option` block (see below). Place after existing `--debug` option. |
| 1.3.2 | Add `tdd_file: Path \| None` to `validate()` signature | `src/superclaude/cli/tasklist/commands.py` | Add as keyword argument. |
| 1.3.3 | Add `tdd_file` to config construction | `src/superclaude/cli/tasklist/commands.py` | `tdd_file=tdd_file.resolve() if tdd_file is not None else None` — add to the `TasklistValidateConfig(...)` constructor call. |

**Exact Click decorator (from research file 05):**
```
@click.option(
    "--tdd-file",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Path to the TDD file used as an additional validation input.",
)
```

### 1.4 `tasklist/models.py` — Extend `TasklistValidateConfig`

| Step | Action | File | Details |
|------|--------|------|---------|
| 1.4.1 | Add `tdd_file` field to `TasklistValidateConfig` dataclass | `src/superclaude/cli/tasklist/models.py` | `tdd_file: Path \| None = None` — add after existing `tasklist_dir` field. |

**Verification after Phase 1:** `uv run python -c "from superclaude.cli.roadmap.models import RoadmapConfig; c = RoadmapConfig(spec_file=Path('.')); print(c.input_type)"` must print `spec`.

---

## Phase 2: TDD Extract Prompt (Critical Path)

**This is the single highest-risk change and the unblocking dependency for all downstream behavior. All generate-*, diff, debate, score, and merge steps receive only the extraction output — making the extract step the sole chokepoint for TDD content coverage.**

### 2.1 `roadmap/prompts.py` — Create `build_extract_prompt_tdd()`

| Step | Action | File | Details |
|------|--------|------|---------|
| 2.1.1 | Add new function `build_extract_prompt_tdd()` | `src/superclaude/cli/roadmap/prompts.py` | Insert immediately after the existing `build_extract_prompt()` function. Do NOT modify `build_extract_prompt()`. |
| 2.1.2 | Function signature | `src/superclaude/cli/roadmap/prompts.py` | `def build_extract_prompt_tdd(spec_file: Path, retrospective_content: str \| None = None) -> str:` — identical signature to `build_extract_prompt()` for drop-in executor substitution. |
| 2.1.3 | Neutralize source framing | `src/superclaude/cli/roadmap/prompts.py` | Change "Read the provided specification file" → "Read the provided source specification or technical design document". Change "requirements extraction specialist" → "requirements and design extraction specialist". |
| 2.1.4 | Broaden identifier language | `src/superclaude/cli/roadmap/prompts.py` | Change "Use the spec's exact requirement identifiers verbatim... FR-EVAL-001.1, FR-EVAL-001.1a/b" → "Preserve exact identifiers from the source document including requirement IDs (FR-xxx, NFR-xxx), interface names, endpoint identifiers, component names, migration phase names, and test case IDs. Do not paraphrase or normalize them." |
| 2.1.5 | Retain all 8 existing body sections unchanged | `src/superclaude/cli/roadmap/prompts.py` | Keep: Functional Requirements, Non-Functional Requirements, Complexity Assessment, Architectural Constraints, Risk Inventory, Dependency Inventory, Success Criteria, Open Questions — with identical instruction text. |
| 2.1.6 | Add 6 new TDD-specific body sections | `src/superclaude/cli/roadmap/prompts.py` | Add after Open Questions. See section names and instructions in 2.1.7–2.1.12 below. |
| 2.1.7 | New section: `## Data Models and Interfaces` | `src/superclaude/cli/roadmap/prompts.py` | Instruction: "Extract every entity, field, type, constraint, and relationship defined in TypeScript interfaces in fenced code blocks and markdown tables in §7 (Data Models). Include: entity name, all field names with types and constraints, required vs. optional status, storage/retention/backup strategy from the storage table, and data-flow steps from mermaid flowcharts. If TypeScript interface bodies are present, list every field and its type verbatim." |
| 2.1.8 | New section: `## API Specifications` | `src/superclaude/cli/roadmap/prompts.py` | Instruction: "Extract the complete API surface from §8 (API Specifications). For every endpoint in the endpoint overview table, capture: HTTP method, URL path, authentication requirement, rate limit, and description. For per-endpoint detail sections, capture: all query parameters (name, type, required, default), request body schema (field names and types), response schema (status code, body shape), error response table (code, message, cause), versioning policy, and deprecation schedule. Extract from both tables and fenced code block examples." |
| 2.1.9 | New section: `## Component Inventory` | `src/superclaude/cli/roadmap/prompts.py` | Instruction: "Extract the complete component surface from §10 (Component Inventory) and §9 (State Management) if present. From the route table: route paths, associated components, auth requirements. From the shared component table: component names, props interfaces, usage context, source file locations. From the ASCII component hierarchy tree: parent-child relationships and nesting structure. From §9 state management tables: state stores (tool/library), state shape interfaces, transition names, trigger conditions, and side effects." |
| 2.1.10 | New section: `## Testing Strategy` | `src/superclaude/cli/roadmap/prompts.py` | Instruction: "Extract the full testing specification from §15 (Testing Strategy). From the test pyramid table: coverage level (unit/integration/E2E), tooling, coverage target percentage, ownership. From unit, integration, and E2E test case tables: test case name/ID, input conditions, expected output, required mocks or fixtures. From the environment matrix: environment name, configuration, and deployment requirements. These artifacts are the primary source of truth for test-related tasks in the generated roadmap." |
| 2.1.11 | New section: `## Migration and Rollout Plan` | `src/superclaude/cli/roadmap/prompts.py` | Instruction: "Extract the migration and deployment sequencing from §19 (Migration and Rollout Plan). From the migration phase table: phase name, tasks, estimated duration, inter-phase dependencies, rollback option. From the feature flag table: flag name, purpose, initial status, cleanup date, owner. From the rollout stage table: stage name, target audience or percentage, success criteria, monitoring requirements, rollback trigger conditions. Extract the numbered rollback procedure as an ordered step sequence. Preserve all ordering and dependency information — these encode task sequencing for the roadmap." |
| 2.1.12 | New section: `## Operational Readiness` | `src/superclaude/cli/roadmap/prompts.py` | Instruction: "Extract production operations requirements from §25 (Operational Readiness) and §14 (Observability and Monitoring) if present. From the runbook scenario table: scenario name, symptom description, diagnosis steps, resolution steps, escalation path, prevention measures. From the on-call expectations table: scenario, expected page volume, MTTD target, MTTR target, knowledge prerequisites. From the capacity planning table: metric, current baseline, 3-month and 6-month projections, scaling trigger conditions, required action. From §14: log format/retention requirements, metric names and alert thresholds, trace sampling policy, dashboard requirements." |
| 2.1.13 | Expand YAML frontmatter fields | `src/superclaude/cli/roadmap/prompts.py` | Retain all 13 existing fields unchanged. Add 6 optional TDD-specific count fields after `extraction_mode`: `data_models_identified`, `api_surfaces_identified`, `components_identified`, `test_artifacts_identified`, `migration_items_identified`, `operational_items_identified`. Instruct: "Set each count field to 0 if the corresponding section is absent from the source document." |
| 2.1.14 | Keep `spec_source` field in frontmatter | `src/superclaude/cli/roadmap/prompts.py` | Instruct: "Set `spec_source` to the filename of the TDD file (e.g., `my-feature-tdd.md`). This field is used for gate provenance tracking and must always be present." This preserves backward compatibility with all 5 gates that require `spec_source` without any gate code changes. |
| 2.1.15 | Add retrospective_content handling | `src/superclaude/cli/roadmap/prompts.py` | Mirror the same `if retrospective_content:` block from `build_extract_prompt()` — append retrospective as supplemental context after the main prompt body. |

**Why this is the critical path:** Research file 01 confirms that `generate-{agent_a}`, `generate-{agent_b}`, `diff`, `debate`, `score`, and `merge` steps receive ONLY the extraction output. Any TDD content not captured here is unrecoverable downstream. Research file 02 confirms that 8 of 28 TDD sections are entirely MISSED by the current prompt, including §7 Data Models (TypeScript interfaces), §8 API Specifications (endpoint tables), §10 Component Inventory, §15 Testing Strategy, §25 Operational Readiness, §26 Cost Estimation, §28 Glossary.

---

## Phase 3: Executor Branching

**Routes `--input-type tdd` to the new prompt builder. Two localized changes in executor.py.**

### 3.1 `roadmap/executor.py` — Branch on `config.input_type` in `_build_steps()`

| Step | Action | File | Details |
|------|--------|------|---------|
| 3.1.1 | Add import for `build_extract_prompt_tdd` | `src/superclaude/cli/roadmap/executor.py` | The existing import block at lines 42–52 imports `build_extract_prompt` from `roadmap.prompts`. Add `build_extract_prompt_tdd` to the same import statement. |
| 3.1.2 | Branch extract prompt selection in `_build_steps()` | `src/superclaude/cli/roadmap/executor.py` | At executor.py:809–820 (extract step construction), replace the direct call `build_extract_prompt(config.spec_file, ...)` with a conditional: if `config.input_type == "tdd"` call `build_extract_prompt_tdd(config.spec_file, retro_content)`, else call `build_extract_prompt(config.spec_file, retro_content)`. The `step.inputs`, `step.output_file`, and all other step fields remain identical. |
| 3.1.3 | No changes to anti-instinct wiring | `src/superclaude/cli/roadmap/executor.py` | `_run_anti_instinct_audit(spec_file, roadmap_file, output_file)` at executor.py:401–408 passes `config.spec_file` directly. For TDD input, `config.spec_file` IS the TDD file. `integration_contracts.py` and `fingerprint.py` are format-agnostic text scanners — no branching needed. |
| 3.1.4 | No changes to spec-fidelity wiring | `src/superclaude/cli/roadmap/executor.py` | `build_spec_fidelity_prompt(config.spec_file, merge_file)` at executor.py:905–913 passes the TDD file as `spec_file`. The prompt will receive TDD content directly. Phase 5 updates the prompt text; no executor change needed here. |

### 3.2 `roadmap/executor.py` — Note on `_run_structural_audit()` for TDD inputs

| Step | Action | File | Details |
|------|--------|------|---------|
| 3.2.1 | Document TDD structural indicator mismatch | `src/superclaude/cli/roadmap/executor.py` | `_run_structural_audit(spec_file, extraction_file)` at executor.py:220–262 calls `check_extraction_adequacy(spec_text, total_req)`, which computes `ratio = total_req / audit.total_structural_indicators`. The `total_structural_indicators` count is derived from spec-oriented heading patterns (e.g., FR heading count). A TDD document has a different heading structure — more total headings per section, lower FR heading density — so the ratio denominator will differ. This audit is **warning-only** (never blocks the pipeline), so no code change is required for Phase 1 TDD support. Add an inline comment at executor.py:250 noting the TDD heading-count divergence for future calibration. |

**Open Investigation Item (Critical Gap C-2 from gaps-and-questions.md):** `structural_checkers.py` (~200 lines) was not investigated in this research cycle. Its relationship to `spec_structural_audit.py` and whether it introduces additional spec-oriented heading assumptions is UNVERIFIED. Treat as open question — do not rely on structural audit behavior for TDD correctness assertions until C-2 is resolved.

---

## Phase 4: Gate Schema Updates

**The gate enforcement engine in `pipeline/gates.py` is format-agnostic. All incompatibilities are in field names and semantic assumptions within individual gate definitions in `roadmap/gates.py`.**

### 4.1 Gates requiring `spec_source` — No code changes needed for Option A

| Gate | Required `spec_source` field | Action | Rationale |
|------|------------------------------|--------|-----------|
| EXTRACT_GATE | Yes (1 of 13 required fields) | No change | `build_extract_prompt_tdd()` (Phase 2, step 2.1.14) explicitly instructs Claude to emit `spec_source: <tdd_filename>`. Gate passes without modification. |
| GENERATE_A_GATE | Yes (1 of 3 required fields) | No change | `build_generate_prompt()` references `spec_source` from extraction frontmatter; if extraction emits it (per above), generate output will propagate it. |
| GENERATE_B_GATE | Yes (1 of 3 required fields) | No change | Same as GENERATE_A_GATE. |
| MERGE_GATE | Yes (1 of 3 required fields) | No change | Merge prompt outputs `spec_source` derived from generate inputs. |
| TEST_STRATEGY_GATE | Yes (1 of 9 required fields) | No change | Test strategy prompt references `spec_source` from extraction. |

**Design decision:** Preserve `spec_source` field name for backward compatibility. The semantic meaning shifts to "source document filename" for TDD inputs, but the field name is unchanged. This avoids touching 5 gate definitions and any downstream consumers of the extraction frontmatter for the initial Option A delivery.

### 4.2 DEVIATION_ANALYSIS_GATE — Requires redesign if TDD support extends to full pipeline

| Step | Action | File | Details |
|------|--------|------|---------|
| 4.2.1 | Phase 1 TDD: no change | `src/superclaude/cli/roadmap/gates.py` | DEVIATION_ANALYSIS_GATE is not in the primary roadmap pipeline path for initial TDD support. No change required for the `--input-type tdd` flag to work end-to-end. |
| 4.2.2 | Future work: rename `routing_update_spec` | `src/superclaude/cli/roadmap/gates.py` | When TDD support extends to the full deviation analysis pipeline, rename `routing_update_spec` → `routing_update_source` in the gate's required fields and semantic check `_routing_ids_valid`. Also assess whether `DEV-\d+` routing ID pattern applies to TDD deviations or requires a parallel namespace. |
| 4.2.3 | Pre-existing bug: note for awareness | `src/superclaude/cli/roadmap/gates.py` | Required field is `ambiguous_count` but semantic check `_no_ambiguous_deviations` reads `ambiguous_deviations`. This is a pre-existing field name mismatch unrelated to TDD work. Do not fix in this change set; file as a separate defect. |

### 4.3 ANTI_INSTINCT_GATE — No code changes needed

| Step | Action | File | Details |
|------|--------|------|---------|
| 4.3.1 | No gate code changes | `src/superclaude/cli/roadmap/gates.py` | The three semantic checks (`_no_undischarged_obligations`, `_integration_contracts_covered`, `_fingerprint_coverage_check`) operate on pure-Python module outputs that are format-agnostic. `obligation_scanner.py` scans roadmap text only. `integration_contracts.py` and `fingerprint.py` are text scanners that work on any markdown. Research file 03 shows TDD documents may produce MORE backtick identifiers (TypeScript type names, component names, constants) than spec documents, potentially improving fingerprint coverage above the 0.7 threshold. |
| 4.3.2 | Hypothesis — verify empirically | `src/superclaude/cli/roadmap/gates.py` | The claim that ANTI_INSTINCT_GATE will perform better for TDD inputs is a hypothesis (Important Gap I-5 from gaps-and-questions.md). It is not empirically verified. Do not assert this as a guarantee in documentation. Run `check_fingerprint_coverage(tdd_text, roadmap_text)` against a real TDD file to validate before claiming coverage improvement. |

**Open Investigation Item (Critical Gap C-1 from gaps-and-questions.md):** `semantic_layer.py` (~400 lines) was not investigated. It is unclear whether it participates in the active pipeline, reads spec content, or enforces spec-oriented semantic constraints. Until C-1 is resolved, do not assert that all gate semantics are TDD-safe. Flag in integration testing as requiring explicit verification.

---

## Phase 5: `build_spec_fidelity_prompt()` Update

**The spec-fidelity step receives the TDD file directly as `spec_file` input (confirmed via executor.py:905–913 and `_embed_inputs()`). The prompt body must be generalized to compare roadmap coverage against TDD artifacts, not just spec requirements.**

### 5.1 `roadmap/prompts.py` — Generalize `build_spec_fidelity_prompt()`

| Step | Action | File | Details |
|------|--------|------|---------|
| 5.1.1 | Generalize analyst role | `src/superclaude/cli/roadmap/prompts.py` | Change "You are a specification fidelity analyst" → "You are a source-document fidelity analyst". |
| 5.1.2 | Generalize input label | `src/superclaude/cli/roadmap/prompts.py` | Change "Read the provided specification file" → "Read the provided source specification or TDD file". Change "diverges from or omits requirements in the specification" → "diverges from or omits requirements, design decisions, or commitments in the source document". |
| 5.1.3 | Generalize identifier examples | `src/superclaude/cli/roadmap/prompts.py` | Change example identifiers from `(FR-NNN)`, `(NFR-NNN)`, `(SC-NNN)` only → add `(interface-name)`, `(endpoint-path)`, `(component-name)`, `(migration-phase)`, `(test-case-id)`. Present these as non-exhaustive examples of what may need tracing. |
| 5.1.4 | Generalize priority language | `src/superclaude/cli/roadmap/prompts.py` | Change "spec's priority ordering" → "source document's priority ordering or stated importance hierarchy". |
| 5.1.5 | Add TDD comparison dimensions | `src/superclaude/cli/roadmap/prompts.py` | Append to the existing comparison dimensions list: (1) API endpoints and request/response contracts defined in the source — verify the roadmap includes implementation tasks for each. (2) Component and module inventory — verify named components from the source have corresponding build/integration tasks. (3) Testing strategy and validation matrix — verify that test cases from §15 are represented as roadmap validation milestones. (4) Migration and rollout procedures — verify rollout stages and rollback steps are addressed. (5) Operational readiness — verify runbook scenarios and capacity planning are addressed by post-launch tasks. |
| 5.1.6 | No signature change | `src/superclaude/cli/roadmap/prompts.py` | `build_spec_fidelity_prompt(spec_file: Path, roadmap_path: Path) -> str` — signature unchanged. The function receives whatever file is at `config.spec_file` (spec or TDD) via the executor's unchanged wiring. |

**Note:** Research file 02 rates `build_spec_fidelity_prompt()` as HIGH severity for TDD adaptation. The changes in 5.1.1–5.1.5 are prompt text changes only — no structural changes to how the function reads files or builds its return value.

---

## Phase 6: Tasklist Validate TDD Enrichment (Optional — Phase 2 of Broader TDD Work)

**Phase 6 is deferred. It depends on Phase 2 and Phase 3 being complete and validated first. Tasklist validate is artifact-based and does not currently reference the original spec or TDD source file at all.**

### 6.1 `tasklist/executor.py` — Add TDD file to validation inputs

| Step | Action | File | Details |
|------|--------|------|---------|
| 6.1.1 | Locate `_build_steps(config)` | `src/superclaude/cli/tasklist/executor.py` | Find the step that builds the fidelity validation prompt and its `inputs` list (the tasklist equivalent of the roadmap's spec-fidelity step). |
| 6.1.2 | Add TDD file to `all_inputs` conditionally | `src/superclaude/cli/tasklist/executor.py` | In the fidelity step construction: if `config.tdd_file is not None`, append `config.tdd_file` to the step's `inputs` list. This causes `_embed_inputs()` to include TDD file content in the prompt context. |

### 6.2 `tasklist/prompts.py` — Update `build_tasklist_fidelity_prompt()`

| Step | Action | File | Details |
|------|--------|------|---------|
| 6.2.1 | Add TDD-aware fidelity instructions | `src/superclaude/cli/tasklist/prompts.py` | When a TDD file is available (pass a `tdd_file: Path \| None` parameter to the prompt builder), add instructions to verify: (1) that test cases from TDD §15 appear as validation tasks in the tasklist, and (2) that rollback procedures from TDD §19 appear as rollback or contingency tasks. This makes the tasklist fidelity check aware of the full TDD validation matrix, not only the roadmap's distilled version. |
| 6.2.2 | Keep existing behavior unchanged when `tdd_file is None` | `src/superclaude/cli/tasklist/prompts.py` | The `tdd_file` parameter defaults to `None`. When `None`, prompt text is identical to current behavior. No regression. |

**Dependency:** Phase 6 requires Phase 1 (CLI/models changes for `--tdd-file` and `tdd_file` field) to be complete. It does not require Phases 2–5 to be complete, but is lower value without them because the roadmap being validated will be spec-derived if Phase 2 has not run.

---

## Phase Dependencies and Sequencing

```
Phase 1 (CLI + Config)
    |
    |——> Phase 2 (TDD Extract Prompt)   <— Critical path; unblocks all LLM behavior
    |       |
    |       |——> Phase 3 (Executor Branching)  <— Wires Phase 2 into the pipeline
    |               |
    |               |——> Phase 4 (Gate Schema Review)   <— Verify no gate regressions
    |               |——> Phase 5 (Fidelity Prompt)       <— Independent; can run in parallel with Phase 4
    |
    |——> Phase 6 (Tasklist Validate)    <— Optional; deferred; depends only on Phase 1
```

**Minimum viable delivery:** Phases 1 + 2 + 3. With these three phases complete, `superclaude roadmap run tdd.md --input-type tdd` will route through the TDD-aware extraction prompt and produce a TDD-informed extraction document. The rest of the pipeline (generate, diff, debate, merge, anti-instinct, spec-fidelity) will then work on TDD-derived content, even before Phases 4 and 5 are completed — though with some residual spec-language in gate error messages and the fidelity prompt.

---

## Integration Checklist

- [ ] `superclaude roadmap run spec.md` continues to work unchanged — `config.input_type` defaults to `"spec"`, executor branches to `build_extract_prompt()`, behavior identical to pre-change. **Backward compatibility test.**
- [ ] `superclaude roadmap run tdd.md --input-type tdd` produces `extraction.md` containing a `## Data Models and Interfaces` section with extracted TypeScript entity names. **Core TDD extraction test.**
- [ ] `extraction.md` YAML frontmatter produced by TDD run contains `spec_source: tdd.md` (or the actual TDD filename). **EXTRACT_GATE frontmatter compatibility test.**
- [ ] EXTRACT_GATE passes for TDD-derived `extraction.md` — all 13 required frontmatter fields present and semantic checks pass. **Gate regression test.**
- [ ] ANTI_INSTINCT_GATE `fingerprint_coverage` value is at or above 0.7 for a reference TDD input. **Hypothesis validation test — see Important Gap I-5; do not treat as guaranteed.**
- [ ] `superclaude tasklist validate <output_dir>` continues to work unchanged without `--tdd-file`. **Backward compatibility test.**
- [ ] `superclaude roadmap run spec.md --dry-run` output shows `extract` step using `build_extract_prompt` (spec path). `superclaude roadmap run tdd.md --input-type tdd --dry-run` shows `extract` step using `build_extract_prompt_tdd` (TDD path). **Dry-run routing verification.**
- [ ] `RoadmapConfig(spec_file=Path("x.md"))` instantiates without error with `input_type="spec"` as default. **Model field backward compatibility test.**

---

## Open Questions and Unverified Items

The following items MUST be investigated before asserting full TDD pipeline correctness. They are flagged here per the synthesis guidance in gaps-and-questions.md.

| # | Item | Gap Ref | Blocking? | Required Action |
|---|------|---------|-----------|-----------------|
| OQ-1 | `semantic_layer.py` (~400 lines) — does it read spec content in the active pipeline? Does it enforce spec-oriented semantic constraints that would reject TDD-derived outputs? | Critical Gap C-1 | Potentially yes | Read `src/superclaude/cli/roadmap/semantic_layer.py` fully; trace all call sites from executor.py; document whether it is in the active pipeline path. |
| OQ-2 | `structural_checkers.py` (~200 lines) — relationship to `spec_structural_audit.py` unknown; may introduce additional spec-oriented heading assumptions beyond `check_extraction_adequacy` | Critical Gap C-2 | Potentially yes for structural audit | Read `src/superclaude/cli/roadmap/structural_checkers.py`; determine if it is called from executor.py or `_run_structural_audit()`; document TDD heading compatibility. |
| OQ-3 | `run_wiring_analysis(wiring_config, source_dir)` at executor.py:421–433 — does `wiring_config` reference `spec_file`? If so, TDD input must be handled there too. | Important Gap I-1 | Possibly, for wiring step | Read the wiring config construction at executor.py:421–433 and trace `wiring_config` field population. |
| OQ-4 | Which downstream code reads `spec_source` or `functional_requirements` keys from the extraction frontmatter? Enumeration is incomplete — only prompt builders and gates were surveyed. | Important Gap I-2 | No (gates covered; risk is in unenumerated consumers) | Search codebase for string literals `"spec_source"` and `"functional_requirements"` to find any non-gate, non-prompt consumers. |
| OQ-5 | ANTI_INSTINCT_GATE TDD fingerprint performance is a hypothesis — TDD's richer backtick identifier density may improve `fingerprint_coverage`, but this is untested. | Important Gap I-5 | No (gate is not blocked; hypothesis is about improvement, not failure) | Run `check_fingerprint_coverage(tdd_text, roadmap_text)` against a real TDD file + generated roadmap; measure actual ratio. |

---

*End of §8 Implementation Plan*
