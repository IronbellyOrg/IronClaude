---
spec_source: spec-roadmap-validate.compressed.md
generated: 2026-06-03T02:48:30Z
generator: requirements-extraction-specialist
functional_requirements: 7
nonfunctional_requirements: 5
total_requirements: 12
complexity_score: 0.65
complexity_class: MEDIUM
domains_detected: [backend, cli, testing, devops, validation]
risks_identified: 8
dependencies_identified: 7
success_criteria_count: 10
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 108.0, started_at: "2026-06-03T02:47:57.287855+00:00", finished_at: "2026-06-03T02:49:45.301971+00:00"}
---

## Functional Requirements

The spec uses verbatim identifiers `FR-050.N`. These are preserved exactly. Seven top-level functional requirements are defined (FR-050.1 through FR-050.7).

**FR-050.1 — `superclaude roadmap validate` Subcommand**
- Accepts `<output-dir>` positional argument (path to directory containing roadmap pipeline outputs).
- Required input files in output-dir: `roadmap.md`, `test-strategy.md`, `extraction.md`.
- Validates presence of all 3 required files, then runs the validation pipeline.
- **CLI surface (verbatim):** `superclaude roadmap validate <output-dir> [--agents model:persona,...] [--model MODEL] [--max-turns N] [--debug]`
- Click signature: positional `output_dir` (`type=click.Path(exists=True, path_type=Path)`); options `--agents` (default `opus:architect`), `--model` (default `""`), `--max-turns` (`type=int, default=50`), `--debug` (`is_flag`).

**FR-050.2 — Single-Agent Validation (default)**
- Triggered when `--agents` is unspecified or has exactly 1 agent.
- Step layout: `reflect` (sequential, single subprocess).
- **Output path (verbatim):** `<output-dir>/validate/validation-report.md`

**FR-050.3 — Multi-Agent Adversarial Validation**
- Triggered when `--agents` specifies 2+ agents (e.g., `--agents opus,haiku`).
- Step layout: `[reflect-opus, reflect-haiku]` (parallel) → `adversarial-merge` (sequential).
- **Output paths (verbatim):** `<output-dir>/validate/reflect-opus-architect.md`, `<output-dir>/validate/reflect-haiku-architect.md`, `<output-dir>/validate/validation-report.md`
- Per-agent reflect output filename pattern: `reflect-{agent.id}.md`.

**FR-050.4 — Auto-Invocation from `roadmap run`**
- After the 8-step pipeline succeeds, `execute_roadmap()` automatically invokes `execute_validate()` unless `--no-validate` is passed.
- Validate step inherits `--agents`, `--model`, `--max-turns`, `--debug` from the parent `roadmap run`.
- **CLI surface (verbatim):** `superclaude roadmap run <spec-file> [--no-validate] [...]` (validate ON by default).
- Resume interaction (I-002 resolution): if `--resume` skipped steps but all gates pass, validation still runs on final artifacts; if the pipeline halts on a failed step, validation is skipped (no artifacts to validate).
- FR-050.4a: Validation only runs after full pipeline success.
- FR-050.4b: Inheritance of parent invocation flags into the validate sub-pipeline.

**FR-050.5 — Validation Dimensions (7 dimensions)**
- The reflection prompt covers 7 dimensions; each finding classified by severity:
  - FR-050.5a: **Schema** — YAML frontmatter fields present, non-empty, correctly typed → BLOCKING.
  - FR-050.5b: **Structure** — milestone DAG acyclic, all refs resolve, no duplicate deliverable IDs, heading hierarchy valid → BLOCKING.
  - FR-050.5c: **Traceability** — every deliverable → requirement AND every requirement → deliverable (bidirectional) → BLOCKING.
  - FR-050.5d: **Cross-file** — test-strategy milestone refs match roadmap milestones → BLOCKING.
  - FR-050.5e: **Interleave** — `interleave_ratio` in `[0.1, 1.0]`, test activities not back-loaded → WARNING.
  - FR-050.5f: **Decomposition** — no compound deliverables needing split by sc:tasklist → WARNING.
  - FR-050.5g: **Parseability** — content parseable into items via headings, bullets, numbered lists → BLOCKING.

**FR-050.6 — Validation Report Schema**
- `validation-report.md` must carry YAML frontmatter: `blocking_issues_count` (int), `warnings_count` (int), `info_count` (int), `tasklist_ready` (true|false), `validation_agents` (comma-separated agent IDs), `validation_mode` (single|adversarial).
- Body sections required: `# Validation Report`, `## Summary`, `## Blocking Issues` (entries `B-NNN` with Dimension/Location/Detail/Fix), `## Warnings` (`W-NNN`), `## Info` (`I-NNN`), `## Validation Metadata`.
- Finding entries must cite Dimension ∈ {schema|structure|traceability|cross-file|parseability} and Location as `file:line` or `file:section`.

**FR-050.7 — Adversarial Merge Report (Multi-Agent Only)**
- Merge step adds `## Agent Agreement Analysis` table.
- Resolution categories: `BOTH_AGREE` (high confidence), `ONLY_A` (review recommended), `ONLY_B` (likely structural), `CONFLICT` (severity conflict → escalated to higher/BLOCKING).
- Merge recalculates `blocking_issues_count` and `tasklist_ready` from merged findings.

## Non-Functional Requirements

Verbatim spec identifiers `NFR-050.N` preserved. Five NFRs defined.

| ID | Requirement | Target | Category |
|---|---|---|---|
| NFR-050.1 | Validate step adds ≤10% wall time to pipeline | ≤2 min for single agent | Performance |
| NFR-050.2 | No imports from `validate_*` in `pipeline/*` modules (maintains NFR-007) | Zero forbidden imports | Maintainability / Architecture |
| NFR-050.3 | `validate` subcommand works independently of `roadmap run` | Standalone invocation | Usability / Modularity |
| NFR-050.4 | Reuses existing pipeline infra (`execute_pipeline`, `ClaudeProcess`, `gate_passed`) | Zero new infra | Maintainability |
| NFR-050.5 | Single-agent and multi-agent share identical code path | List of 1 vs list of N | Maintainability |

Implicit NFRs (not separately ID'd in spec, surfaced here):
- NFR-IMP-1 (Reliability): Blocking issues warn but do NOT exit non-zero — non-blocking UX contract.
- NFR-IMP-2 (Precision): "Be thorough but precise — false positives waste user time" — low false-positive rate constraint on reflection prompt.
- NFR-IMP-3 (Timeout): Each step `timeout_seconds=300`, `retry_limit=1`.

## Complexity Assessment

**complexity_score: 0.65 — complexity_class: MEDIUM** (spec self-declares 0.65 / moderate; retained after independent assessment).

Scoring rationale:
- **Surface area (moderate):** 3 new modules + 3 modified modules; 1 new subcommand + 1 new flag. Bounded blast radius.
- **Branching logic (moderate):** single-vs-multi agent dispatch (list-of-1 vs list-of-N), auto-invoke vs standalone, resume-vs-halt validation gating. Several conditional paths but all enumerated.
- **Subprocess orchestration (elevated):** parallel reflect group + sequential adversarial merge; subprocess context-independence introduces non-determinism and timeout/retry handling.
- **Semantic validation depth (elevated):** 7 validation dimensions including DAG acyclicity, bidirectional traceability, cross-file reference matching, and parseability simulation — non-trivial graph/consistency logic.
- **Architectural constraint (moderate):** one-directional dependency rule (validate → roadmap, never reverse) must be enforced to preserve NFR-007.
- **Reducing factors:** zero new infrastructure (reuses `execute_pipeline`, gates, `ClaudeProcess`); no schema migration; no breaking changes; additive only.

Net: above LOW due to multi-dimensional semantic validation + adversarial merge; below HIGH due to heavy reuse, additive scope, and absence of state/schema migration.

## Architectural Constraints

1. **One-directional dependency (hard):** `validate_*` modules may import from `pipeline/*` and `roadmap/gates.py`, but `pipeline/*` MUST NOT import from `validate_*` (NFR-050.2 / NFR-007). Stated rationale: "no circular dependency: validate → roadmap, not vice versa."
2. **Infrastructure reuse mandate:** Must reuse `execute_pipeline`, `ClaudeProcess`, `gate_passed`, and `GateCriteria`/`SemanticCheck` primitives — no new pipeline infra (NFR-050.4).
3. **Subprocess isolation (design decision):** Validation runs as a Claude subprocess, not in-session, specifically to eliminate confirmation bias ("context independence").
4. **Shared code path:** Single-agent and multi-agent must traverse identical code (`_build_validate_steps` returns list of 1 or list of N) (NFR-050.5).
5. **`ValidateConfig` extends `PipelineConfig`:** dataclass inheritance is mandated.
6. **Gate reuse:** `_frontmatter_values_non_empty` imported from `.gates` (roadmap/gates.py), not duplicated (W-001 resolution).
7. **Agent spec format consistency:** `model:persona` format identical to `roadmap run` for code reuse.
8. **Non-blocking exit contract:** validation never exits non-zero on blocking findings; only warns.
9. **State separation:** `.roadmap-state.json` unchanged; validate state is separate (no schema migration).
10. **Implementation order (mandated, section 4.6):** `models.py` → (`validate_gates.py` ∥ `validate_prompts.py`) → `validate_executor.py` → (`commands.py` ∥ `executor.py`).

## Component Inventory

### Services / Modules / Middleware (COMP)

**COMP-001 — validate_executor.py** (NEW)
- Path: `src/superclaude/cli/roadmap/validate_executor.py`
- Role: Builds validate step layout and executes the validate sub-pipeline.
- Methods: `execute_validate(config: ValidateConfig)`, `_build_validate_steps(config: ValidateConfig) -> list[Step | list[Step]]`.
- Dependencies: COMP-005 (pipeline/executor `execute_pipeline`, reused), COMP-002 (validate_gates), COMP-003 (validate_prompts), DM-001 (ValidateConfig).
- Source: §4.1, §4.3, §6.1, §6.2.

**COMP-002 — validate_gates.py** (NEW)
- Path: `src/superclaude/cli/roadmap/validate_gates.py`
- Role: Defines gate criteria and semantic check functions for the validate steps.
- Members: `REFLECT_GATE` (GateCriteria), `ADVERSARIAL_MERGE_GATE` (GateCriteria), `_has_agreement_table(content: str) -> bool`; imports `_frontmatter_values_non_empty` from `.gates`.
- Dependencies: `pipeline/models` (GateCriteria, SemanticCheck), `roadmap/gates.py`.
- Source: §4.1, §4.5.

**COMP-003 — validate_prompts.py** (NEW)
- Path: `src/superclaude/cli/roadmap/validate_prompts.py`
- Role: Builds reflection and adversarial-merge prompts.
- Methods: `build_reflect_prompt(agent, roadmap_file, test_strategy_file, extraction_file) -> str`, `build_adversarial_merge_prompt(reflect_files: list[Path], roadmap_file: Path) -> str`.
- Dependencies: `models` (AgentSpec).
- Source: §4.1, §5.1, §5.2.

**COMP-004 — commands.py** (MODIFIED)
- Path: `src/superclaude/cli/roadmap/commands.py`
- Role: CLI dispatch; adds `validate` subcommand and `--no-validate` flag on `run`.
- Dependencies: COMP-001 (execute_validate), COMP-006 (executor.execute_roadmap).
- Source: §4.2, §7.1, §7.2.

**COMP-005 — pipeline/executor.py** (REUSED, existing)
- Path: `src/superclaude/cli/roadmap/pipeline/executor.py`
- Role: Generic step execution engine (`execute_pipeline`).
- Source: §4.3.

**COMP-006 — executor.py** (MODIFIED)
- Path: `src/superclaude/cli/roadmap/executor.py`
- Role: Orchestrates `execute_roadmap`; calls `execute_validate()` after pipeline success.
- Dependencies: COMP-005, COMP-001.
- Source: §4.2, §4.3.

**COMP-007 — ClaudeProcess** (REUSED, existing)
- Role: Subprocess launcher for Claude agent steps (referenced by NFR-050.4).
- Source: §9 (NFR-050.4).

### Data Models / DTOs / Type Definitions (DM)

**DM-001 — ValidateConfig** (dataclass, extends `PipelineConfig`)
- Path: `src/superclaude/cli/roadmap/models.py` (MODIFIED to add)
- Role: Configuration for the validate sub-pipeline.
- Fields:
  - `output_dir: Path` — parent dir containing roadmap.md etc.
  - `validate_dir: Path` — `output_dir / "validate"`
  - `agents: list[AgentSpec]`
  - `roadmap_file: Path` — `output_dir / "roadmap.md"`
  - `test_strategy_file: Path` — `output_dir / "test-strategy.md"`
  - `extraction_file: Path` — `output_dir / "extraction.md"`
  - (inherited) all `PipelineConfig` fields.
- Source: §4.2, §4.4.

**DM-002 — ValidationReport frontmatter** (schema / type contract)
- Role: YAML frontmatter contract for `validation-report.md`.
- Fields:
  - `blocking_issues_count: int`
  - `warnings_count: int`
  - `info_count: int`
  - `tasklist_ready: bool` (true|false)
  - `validation_agents: str` (comma-separated agent IDs)
  - `validation_mode: str` (single|adversarial)
- Source: §FR-050.6.

**DM-003 — GateCriteria instances** (REFLECT_GATE, ADVERSARIAL_MERGE_GATE)
- Role: Gate configuration DTOs.
- REFLECT_GATE fields: `required_frontmatter_fields=[blocking_issues_count, warnings_count, tasklist_ready]`, `min_lines=20`, `enforcement_tier="STANDARD"`, `semantic_checks=[frontmatter_values_non_empty]`.
- ADVERSARIAL_MERGE_GATE fields: `required_frontmatter_fields=[blocking_issues_count, warnings_count, tasklist_ready, validation_mode, validation_agents]`, `min_lines=30`, `enforcement_tier="STRICT"`, `semantic_checks=[frontmatter_values_non_empty, has_agreement_table]`.
- Source: §4.5.

**DM-004 — SemanticCheck** (existing type, instantiated)
- Fields used: `name: str`, `check_fn: Callable[[str], bool]`, `failure_message: str`.
- Source: §4.5.

**DM-005 — Step** (existing type, instantiated)
- Fields used: `id: str`, `prompt: str`, `output_file: Path`, `gate: GateCriteria`, `timeout_seconds: int` (300), `inputs: list[Path]`, `retry_limit: int` (1), `model: str` (optional).
- Source: §6.1, §6.2.

**DM-006 — AgentSpec** (existing type)
- Fields used: `id: str`, `model: str`, `persona` (from `model:persona` format).
- Source: §6.2, §7.2.

**DM-007 — Agreement Analysis row** (table contract)
- Columns: `Finding`, `Agent A`, `Agent B`, `Resolution` (BOTH_AGREE | ONLY_A | ONLY_B | CONFLICT).
- Source: §FR-050.7.

## Risk Inventory

1. **(High) Validation false positives** — reflection subprocess flags non-issues, eroding user trust and wasting review time. *Mitigation:* prompt constraint "Be thorough but precise — false positives waste user time"; every finding must cite a specific location; adversarial multi-agent mode cross-checks via BOTH_AGREE.
2. **(High) Circular dependency regression** — accidental import from `validate_*` into `pipeline/*` breaks NFR-007/NFR-050.2. *Mitigation:* one-directional import rule; reuse-via-`.gates`-import pattern; should be enforced by an import-lint/architecture test.
3. **(Medium) Subprocess non-determinism / flakiness** — Claude subprocess may produce malformed frontmatter, causing gate failure (§8.3). *Mitigation:* `retry_limit=1`, gate enforcement, explicit warn-and-continue on gate failure.
4. **(Medium) Wall-time budget breach** — multi-agent parallel + merge could exceed the ≤10%/≤2min NFR-050.1 target on large roadmaps. *Mitigation:* `timeout_seconds=300` per step; parallel reflect group; single-agent default for standalone.
5. **(Medium) Default agent-count mismatch between invocation modes** — standalone `validate` defaults to single-agent (`opus:architect`) while auto-invoke inherits `roadmap run` default (`opus:architect,haiku:architect` = adversarial), producing different report shapes for the same artifacts. *Mitigation:* documented in §7.2 (W-003 resolution); note in CLI help.
6. **(Medium) Silent miss of real issues** — warn-don't-fail contract means users may proceed past genuine BLOCKING findings. *Mitigation:* prominent CLI warning lines enumerating B-IDs (§8.2); `tasklist_ready: false` flag.
7. **(Low) Adversarial merge severity escalation conflicts** — CONFLICT resolution always escalates to higher/BLOCKING, risking over-blocking. *Mitigation:* evidence-evaluation step before escalation (§5.2).
8. **(Low) Missing-file UX** — running `validate` against a dir lacking `roadmap.md`/`test-strategy.md`/`extraction.md`. *Mitigation:* FR-050.1 presence check + integration test `test_validate_missing_files` expecting clear error exit.

## Dependency Inventory

1. **Claude subprocess runtime (`ClaudeProcess`)** — internal infra; launches validation agent subprocesses. (NFR-050.4)
2. **`pipeline/executor.py` → `execute_pipeline`** — internal reused step engine. (§4.3)
3. **`roadmap/gates.py` → `_frontmatter_values_non_empty`, `GateCriteria`, `SemanticCheck`, `gate_passed`** — internal reused gate primitives. (§4.5, NFR-050.4)
4. **`models.py` → `PipelineConfig`, `AgentSpec`, `Step`** — internal base types ValidateConfig/steps depend on. (§4.4, §6)
5. **Click (`click`)** — CLI framework for subcommand/option/argument definitions. (§7)
6. **Roadmap pipeline output artifacts** — runtime data dependency: `roadmap.md`, `test-strategy.md`, `extraction.md` must pre-exist. (FR-050.1)
7. **Model backends (opus, haiku, configurable via `--model`/`--agents`)** — external model availability for reflect/merge steps. (§2.1, §7.2)

## Success Criteria

1. `roadmap validate <dir>` with all 3 files present runs to completion and writes `<dir>/validate/validation-report.md`. (FR-050.1/2; E2E #1)
2. Multi-agent mode (`--agents opus,haiku`) produces `reflect-opus-architect.md` + `reflect-haiku-architect.md` + merged `validation-report.md` with an `## Agent Agreement Analysis` table. (FR-050.3/7; E2E #2; `test_build_validate_steps_multi`)
3. Single-agent mode produces exactly 1 step; multi-agent produces parallel group + merge — verified by `test_build_validate_steps_single` / `test_build_validate_steps_multi`.
4. A known injected issue (duplicate D-ID) appears as a BLOCKING `B-xxx` finding in the report. (FR-050.5b; E2E #3)
5. `--no-validate` skips the validation step; default `roadmap run` invokes validation after pipeline success. (FR-050.4; `test_run_with_no_validate`, `test_run_auto_validates`)
6. `tasklist_ready: true` is set only when `blocking_issues_count == 0`. (§5.1, FR-050.6)
7. REFLECT_GATE enforces `[blocking_issues_count, warnings_count, tasklist_ready]` frontmatter + non-empty values; ADVERSARIAL_MERGE_GATE additionally enforces `validation_mode`, `validation_agents`, and presence of agreement table. (`test_reflect_gate_criteria`, `test_merge_gate_has_agreement_table`)
8. Reflect prompt contains all 7 dimensions; merge prompt contains BOTH_AGREE/ONLY_A/ONLY_B categories. (`test_reflect_prompt_contains_dimensions`, `test_merge_prompt_contains_categories`)
9. Validate adds ≤10% wall time (≤2 min single agent). (NFR-050.1)
10. No `validate_*` import appears in any `pipeline/*` module. (NFR-050.2 — verifiable via static import scan)

Additional verifiable gates: `test_validate_dry_run` (plan printed without launching subprocesses), `test_validate_missing_files` (clear error on missing inputs), gate-failure path warns rather than exits non-zero (§8.3).

## Open Questions

The spec §12 declares "None — all questions resolved" and lists v1.0.1 fixes (B-004, W-001, W-002, W-003, I-002). Residual ambiguities surfaced during extraction:

1. **Agent ID → filename derivation.** §6.2 names files `reflect-{agent.id}.md`, but §FR-050.3 examples show `reflect-opus-architect.md`. Confirm `agent.id` resolves to `{model}-{persona}` (e.g., `opus-architect`) and how collisions (two `opus:architect` specs) are disambiguated.
2. **`info_count` gate coverage.** DM-002 includes `info_count` in the report schema, but neither REFLECT_GATE nor ADVERSARIAL_MERGE_GATE lists it in `required_frontmatter_fields`. Intentional (optional) or omission?
3. **Decomposition (dim 6) location in report.** §FR-050.6 enumerates report Dimension values as {schema|structure|traceability|cross-file|parseability} — `interleave` and `decomposition` (the two WARNING dims) are absent from that enumeration. Confirm WARNING findings carry a Dimension value and what string is used.
4. **`--model` vs `--agents` precedence.** When both `--model MODEL` (override all steps) and per-agent models in `--agents model:persona` are supplied, which wins? Spec defines both but not the resolution order.
5. **Adversarial merge with >2 agents.** §FR-050.7 table is strictly A/B (two-agent). Behavior for 3+ agents (column layout, ONLY_C category) is unspecified.
6. **`validation_mode` value for N≥2.** Frontmatter `validation_mode` ∈ {single|adversarial}; confirm any 2+ agent run is `adversarial` regardless of N.
7. **Gate-failure artifact state.** §8.3 warns "validation-report.md may be incomplete" — is a partial/zero-byte report still written, and does downstream `sc:tasklist` treat a missing/incomplete report as `tasklist_ready: false` or as "unknown"?
