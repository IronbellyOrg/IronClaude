# Research: 02 - Roadmap and Tasklist Pipelines
**Investigation type:** Code Tracer / Architecture Analyst
**Scope:** `src/superclaude/cli/roadmap/`, `src/superclaude/cli/tasklist/`, `src/superclaude/skills/sc-roadmap-protocol/`, `src/superclaude/skills/sc-tasklist-protocol/`, `src/superclaude/commands/roadmap.md`, `src/superclaude/commands/tasklist.md`
**Status:** Complete
**Date:** 2026-06-02
---

## Files Found and Initial Scope Inventory

### Roadmap CLI files
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/commands.py` — Click command group for `superclaude roadmap`; defines `run`, `validate`, and `accept-spec-change` commands (402 lines read).
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py` — Main roadmap orchestration implementation; builds and executes the roadmap pipeline via shared pipeline executor, with deterministic side steps for anti-instinct, convergence, deviation analysis, remediation, resume, and validation auto-invocation (3,702 lines read).
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/models.py` — Dataclasses for `Finding`, `AgentSpec`, `RoadmapConfig`, and `ValidateConfig` (144 lines read).
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/gates.py` — Roadmap gate definitions and semantic check functions; includes `ALL_GATES` reference list (1,441 lines read).

### Tasklist CLI files
- `/config/workspace/IronClaude/src/superclaude/cli/tasklist/commands.py` — Click command group for `superclaude tasklist validate`; resolves roadmap/tasklist paths and auto-wires TDD/PRD files from `.roadmap-state.json` (186 lines read).
- `/config/workspace/IronClaude/src/superclaude/cli/tasklist/executor.py` — Single-step tasklist validation pipeline; uses shared `execute_pipeline()` plus `ClaudeProcess` (277 lines read).
- `/config/workspace/IronClaude/src/superclaude/cli/tasklist/gates.py` — `TASKLIST_FIDELITY_GATE` definition; reuses roadmap gate semantic checks (47 lines read).
- `/config/workspace/IronClaude/src/superclaude/cli/tasklist/models.py` — `TasklistValidateConfig` dataclass (31 lines read).

### Skill and command files found
- `/config/workspace/IronClaude/src/superclaude/skills/sc-roadmap-protocol/SKILL.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-roadmap-protocol/refs/templates.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-roadmap-protocol/refs/validation.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-tasklist-protocol/SKILL.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-tasklist-protocol/rules/file-emission-rules.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-tasklist-protocol/rules/tier-classification.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-tasklist-protocol/templates/index-template.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md`
- `/config/workspace/IronClaude/src/superclaude/commands/roadmap.md`
- `/config/workspace/IronClaude/src/superclaude/commands/tasklist.md`

### Initial Key Takeaways
- Roadmap is not purely bespoke: `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:26` imports shared `execute_pipeline`, and `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:3124-3131` delegates execution to it with roadmap-specific `roadmap_run_step`.
- Tasklist validation also uses the shared pipeline layer: `/config/workspace/IronClaude/src/superclaude/cli/tasklist/executor.py:23-25` imports `execute_pipeline`, `Step`, `StepResult`, `StepStatus`, and `ClaudeProcess`; `/config/workspace/IronClaude/src/superclaude/cli/tasklist/executor.py:259-263` calls `execute_pipeline`.
- Roadmap has a much richer orchestration surface than tasklist validation: it has LLM steps, parallel generate steps, deterministic audit/remediation steps, convergence mode, resume state, compression sidecars, cosmetic remediation, post-run validation, and spec-patch resume logic.
- Tasklist validation is currently a single LLM fidelity-check step with a strict gate, not a tasklist generator.

## Shared Pipeline Architecture and Data Flow

### Shared pipeline primitives
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/models.py:40-48` defines `StepStatus` (`PENDING`, `PASS`, `FAIL`, `TIMEOUT`, `CANCELLED`, `SKIPPED`).
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/models.py:69-78` defines `GateMode` (`BLOCKING`, `TRAILING`).
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/models.py:81-87` defines `SemanticCheck(name, check_fn, failure_message)`.
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/models.py:90-105` defines `GateCriteria(required_frontmatter_fields, min_lines, enforcement_tier, semantic_checks)` with support for OR-group frontmatter aliases via tuple entries.
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/models.py:108-122` defines `Step(id, prompt, output_file, gate, timeout_seconds, inputs, retry_limit, model, gate_mode, tool_write_mode, template_path)`.
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/models.py:125-144` defines `StepResult`, including `remediated` and `remediations` for the cosmetic auto-remediation lane.
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/models.py:212-234` defines shared `PipelineConfig` fields: `work_dir`, `dry_run`, `max_turns`, `model`, `permission_flag`, `debug`, `grace_period`, `allow_cosmetic_remediation`, and pluggable `cosmetic_remediator`.

### Shared executor behavior
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py:63-72` defines `execute_pipeline(steps, config, run_step, ...)`, accepting a roadmap/tasklist-specific `StepRunner` callable.
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py:75-96` documents the core state machine: sequential or parallel steps, runner invocation, gate checks, retries, and halt behavior.
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py:108-123` handles parallel groups with `_run_parallel_steps`; `/config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py:402-452` runs each parallel step in a Python thread and cross-cancels on non-PASS.
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py:191-399` implements single-step retry and gate evaluation. The gate is checked after the consumer-specific runner returns `StepStatus.PASS`; failures retry until `retry_limit` is exhausted.
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py:250-262` implements `TRAILING` gate mode when `grace_period > 0`; `/config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py:175-187` waits for pending trailing gate results and logs failures.
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py:286-365` implements the generic cosmetic-remediation hook, but the hook body is supplied by the roadmap layer.

### Shared gate behavior
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/gates.py:20-76` implements `gate_passed(output_file, criteria)`.
- Gate tiers are code-enforced as follows: `EXEMPT` always passes (`pipeline/gates.py:28-30`); `LIGHT` requires file exists and non-empty (`pipeline/gates.py:32-43`); `STANDARD` also requires `min_lines` and required frontmatter (`pipeline/gates.py:45-63`); `STRICT` additionally runs `semantic_checks` (`pipeline/gates.py:65-76`).
- Frontmatter matching is deterministic and top-level only: `/config/workspace/IronClaude/src/superclaude/cli/pipeline/gates.py:79-142` scans YAML delimiter pairs, rejects horizontal rules with no top-level keys, and supports tuple OR-groups.

### Key Takeaways
- The portable unit is not only prompts: the verified behavior depends on `Step`, `GateCriteria`, `StepResult`, `execute_pipeline`, `gate_passed`, and consumer-specific `run_step` implementations.
- Mastra can map naturally to `Step` nodes and workflow edges, but must preserve SuperClaude’s post-step gate semantics, retry semantics, parallel-group cancellation, and optional trailing/advisory gates if behavior parity matters.
- Backlog.md/Beads are better fits for generated tasks and state records than for enforcing runtime gates unless the gate results are encoded as explicit issue/task statuses or artifacts.

## Roadmap CLI Pipeline Trace

### CLI command surface
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/commands.py:14-29` defines `roadmap_group()` and describes a roadmap pipeline with extract/generate/diff/debate/score/merge/test-strategy style orchestration.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/commands.py:32-298` defines `run(...)` with input file routing, `--agents`, `--output`, `--depth`, `--resume`, `--dry-run`, `--model`, `--max-turns`, `--debug`, `--no-validate`, `--allow-regeneration`, `--no-convergence`, `--retrospective`, `--input-type`, `--tdd-file`, `--prd-file`, `--no-compress`, and cosmetic-remediation flags.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/commands.py:212-221` calls `_route_input_files(...)`, and `/config/workspace/IronClaude/src/superclaude/cli/roadmap/commands.py:260-282` builds `RoadmapConfig`.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/commands.py:292-298` calls `execute_roadmap(config, resume=..., no_validate=..., agents_explicit=..., depth_explicit=...)`.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/commands.py:327-383` defines `roadmap validate`, builds `ValidateConfig`, and calls `execute_validate`.

### Input detection and routing
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:74-211` implements `detect_input_type(spec_file)` using PRD score first, then TDD score, else spec.
- PRD detection uses frontmatter text, PRD-specific section names, user-story/JTBD patterns, and `prd` tags (`executor.py:101-148`).
- TDD detection uses numbered heading count, TDD-exclusive frontmatter fields, TDD-specific section names, and `Technical Design Document` type text (`executor.py:150-211`).
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:214-335` implements `_route_input_files(...)`: validates 1-3 inputs, classifies by content, rejects duplicates, requires spec or TDD primary input, permits supplementary PRD/TDD, applies explicit flags, guards same-file collisions, and returns `spec_file`, `tdd_file`, `prd_file`, `input_type`.

### Roadmap pipeline construction
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:1947-2208` builds the roadmap step list in `_build_steps(config)`.
- Wired step order in `_build_steps`: `extract` (`executor.py:2003-2027`), parallel `generate-{agent_a.id}` and `generate-{agent_b.id}` (`executor.py:2029-2066`), `diff` (`executor.py:2068-2076`), `debate` (`executor.py:2078-2086`), `score` (`executor.py:2088-2105`), `merge` (`executor.py:2107-2128`), `anti-instinct` (`executor.py:2130-2138`), `test-strategy` (`executor.py:2140-2156`), `spec-fidelity` (`executor.py:2158-2173`), `wiring-verification` (`executor.py:2175-2184`), `deviation-analysis` (`executor.py:2186-2194`), and `remediate` (`executor.py:2196-2204`).
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:1899-1944` defines `build_certify_step(...)`, but `_build_steps` does not include it; the comment at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:2205` says certifying is constructed dynamically, yet no call to `build_certify_step` was found in the read executor flow. This is a **defined-only / not obviously wired** gate pending broader grep confirmation.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:2283-2302` lists all expected step IDs including `certify`; this list is used for halt diagnostics, not direct step execution.

### Roadmap execution
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:955-1250` defines `roadmap_run_step(step, config, cancel_check)`.
- Roadmap step execution is hybrid: most steps launch `ClaudeProcess` after inline input embedding (`executor.py:1033-1118`), while special step IDs execute deterministic Python paths.
- Deterministic/special cases are wired for `anti-instinct` (`executor.py:977-992`), convergence-mode `spec-fidelity` (`executor.py:994-1001`), `deviation-analysis` (`executor.py:1003-1005`), `remediate` (`executor.py:1007-1009`), and `wiring-verification` (`executor.py:1011-1031`).
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:2985-3187` defines `execute_roadmap(...)`: creates output dir, restores resume state, routes inputs, compresses inputs, builds steps, handles dry-run, applies resume, installs cosmetic remediator, executes shared pipeline, saves state, handles failures/spec-patch resume, and auto-invokes validation unless skipped.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:3124-3131` is the core shared-pipeline handoff: `execute_pipeline(steps=steps, config=config, run_step=roadmap_run_step, ...)`.

### Roadmap validation subsystem
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/validate_executor.py:39-40` requires `roadmap.md`, `test-strategy.md`, and `extraction.md` for validation.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/validate_executor.py:183-236` resolves those outputs plus original `spec_file`, `tdd_file`, and `prd_file` from `.roadmap-state.json`.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/validate_executor.py:239-275` builds a single-agent validation pipeline: one `reflect` step producing `validate/validation-report.md` gated by `REFLECT_GATE`.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/validate_executor.py:278-339` builds a multi-agent validation pipeline: parallel `reflect-{agent.id}` steps, then `adversarial-merge` producing `validate/validation-report.md` gated by `ADVERSARIAL_MERGE_GATE`.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/validate_executor.py:442-519` executes validation via shared `execute_pipeline`, writes degraded report on partial multi-agent failure, and returns parsed counts.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:3409-3447` auto-invokes validation after successful `roadmap run`, defaulting to up to two roadmap agents and saving validation status as pass/fail/skipped.

### Key Takeaways
- Roadmap run/validate is a shared-pipeline workflow with roadmap-specific step runners, prompt builders, gates, and state management.
- The adversarial workflow in CLI is wired inline as `diff → debate → score → merge`; it does not call `sc:adversarial-protocol`.
- Convergence/remediation is partly deterministic Python, partly LLM/Claude-process based, and is stateful through `deviation-registry.json`, `spec-deviations.*`, `remediation-tasklist.*`, and `.roadmap-state.json`.

## Wired Versus Defined-Only Gates

### Roadmap gates defined in code
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/gates.py:1020-1050` defines `EXTRACT_GATE` with strict frontmatter/semantic checks.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/gates.py:1052-1090` defines `EXTRACT_TDD_GATE` with standard extraction fields plus six TDD-specific fields.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/gates.py:1092-1147` defines `GENERATE_A_GATE`; `GENERATE_B_GATE = GENERATE_A_GATE`.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/gates.py:1149-1153` defines `DIFF_GATE`.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/gates.py:1155-1166` defines `DEBATE_GATE` and validates only `convergence_score` shape/range plus `rounds_completed`, not threshold-based pass/partial/fail.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/gates.py:1168-1172` defines `SCORE_GATE`.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/gates.py:1174-1229` defines `MERGE_GATE` with heading, cross-reference, duplicate-heading, deliverable-row, schema, sentinel, and template-section checks.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/gates.py:1231-1272` defines `TEST_STRATEGY_GATE` with complexity/interleave/milestone/philosophy/policy semantic checks.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/gates.py:1274-1297` defines `SPEC_FIDELITY_GATE`.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/gates.py:1299-1322` defines `REMEDIATE_GATE`.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/gates.py:1324-1351` defines `CERTIFY_GATE`.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/gates.py:1353-1378` defines `ANTI_INSTINCT_GATE`.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/gates.py:1390-1423` defines `DEVIATION_ANALYSIS_GATE`.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/gates.py:1425-1441` defines `ALL_GATES`, a reference list including `certify`.

### Roadmap gates wired into `_build_steps`
- `extract` is wired with `EXTRACT_GATE` or `EXTRACT_TDD_GATE` depending on `config.input_type` at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:2003-2027`.
- `generate-{agent_a.id}` and `generate-{agent_b.id}` are wired with `GENERATE_A_GATE` and `GENERATE_B_GATE` at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:2029-2066`.
- `diff` is wired with `DIFF_GATE` at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:2068-2076`.
- `debate` is wired with `DEBATE_GATE` at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:2078-2086`.
- `score` is wired with `SCORE_GATE` at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:2088-2105`.
- `merge` is wired with `MERGE_GATE` at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:2107-2128`.
- `anti-instinct` is wired with `ANTI_INSTINCT_GATE` at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:2130-2138` and executes deterministic `_run_anti_instinct_audit` at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:977-992`.
- `test-strategy` is wired with `TEST_STRATEGY_GATE` at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:2140-2156`.
- `spec-fidelity` has a split behavior: when `config.convergence_enabled` is true, the step gate is `None` (`executor.py:2158-2173`) and the step result is pass/fail from `_run_convergence_spec_fidelity` (`executor.py:994-1001`); when convergence is disabled, it uses `SPEC_FIDELITY_GATE` (`executor.py:2167`).
- `wiring-verification` is wired with imported `WIRING_GATE` at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:2175-2184`, `gate_mode=GateMode.TRAILING`, and deterministic `run_wiring_analysis` at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:1011-1031`.
- `deviation-analysis` is wired with `DEVIATION_ANALYSIS_GATE` at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:2186-2194` and deterministic `_run_deviation_analysis` at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:1003-1005`.
- `remediate` is wired with `REMEDIATE_GATE` at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:2196-2204` and deterministic `_run_remediate_step` at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:1007-1009`.

### Defined-only or partially wired gates
- `CERTIFY_GATE` is **defined** (`gates.py:1324-1351`) and `build_certify_step` creates a `Step` using it (`executor.py:1899-1944`), but `_build_steps` does not append a `certify` step (`executor.py:1947-2208`). A grep for `build_certify_step` found only the definition and tests, not production invocation. This is **defined-only / not wired in production roadmap run** based on current code search.
- `check_certify_resume` is defined at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:3483-3502`, but grep did not find production calls. This reinforces that certification resume support is currently not wired into `execute_roadmap`.
- `ALL_GATES` includes `("certify", CERTIFY_GATE)` at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/gates.py:1440`, but that list is a data/reference inventory and is not used by `_build_steps`.
- The docstring/comments say “Step 12 (certify) constructed dynamically” at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:2205`, but the read production path did not reveal dynamic construction. Treat this as a current implementation gap.

### Tasklist gates
- `/config/workspace/IronClaude/src/superclaude/cli/tasklist/gates.py:23-46` defines `TASKLIST_FIDELITY_GATE`, reusing `_high_severity_count_zero` and `_tasklist_ready_consistent` from roadmap gates.
- `/config/workspace/IronClaude/src/superclaude/cli/tasklist/executor.py:202-218` wires the single `tasklist-fidelity` step to `TASKLIST_FIDELITY_GATE`.
- `/config/workspace/IronClaude/src/superclaude/cli/tasklist/executor.py:251-276` executes the single-step pipeline and separately parses `high_severity_count` to decide CLI pass/fail.

### Key Takeaways
- Most roadmap gates are wired through `_build_steps` and enforced by shared `execute_pipeline`; the certification gate is the major defined-only/partially wired exception.
- `SPEC_FIDELITY_GATE` is wired only in single-shot LLM mode (`--no-convergence`); convergence mode replaces gate enforcement with deterministic pass/fail from `_run_convergence_spec_fidelity` and writes a gate-shaped report.
- `WIRING_GATE` is trailing/advisory in step config, but because `PipelineConfig.grace_period` defaults to `0`, shared executor logic forces `GateMode.BLOCKING` unless a non-zero grace period is configured (`pipeline/executor.py:211-214`). No roadmap CLI flag for grace period was found in `commands.py`, so the current roadmap CLI likely runs it synchronously/blocking when reached, despite `gate_mode=TRAILING`.

## Convergence and Remediation Trace

### Convergence engine
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:1290-1478` defines `_run_convergence_spec_fidelity(...)` and wires structural checkers, semantic layer, fidelity checker, deviation registry, `TurnLedger`, and remediation.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/convergence.py:90-136` defines `DeviationRegistry.load_or_create(...)`, which resets on spec hash mismatch and preserves findings on matching spec hash.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/convergence.py:153-207` merges structural and semantic findings into stable registry entries with status `ACTIVE` and `first_seen_run`/`last_seen_run` metadata.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/convergence.py:434-482` defines `execute_fidelity_with_convergence(...)`, describing up to three checker/remediation cycles: catch, verify, backup.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/convergence.py:488-557` checks budget, starts runs, executes checkers, and passes when active HIGH count reaches zero.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/convergence.py:581-618` detects structural regression and can call `handle_regression`.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/convergence.py:632-651` debits remediation budget and calls `run_remediation(registry)` before the next run.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/convergence.py:653-668` fails with a diagnostic halt message if max runs are exhausted.

### Remediation artifacts and execution
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/remediate.py:177-288` defines `generate_remediation_tasklist(...)`, producing `remediation-tasklist.md` frontmatter and status-grouped findings.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:1804-1897` defines `_run_remediate_step(...)`, which reads `spec-deviations.json`, converts records to `Finding`, generates remediation tasklist markdown, and writes a JSON sidecar.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/remediate_executor.py:735-755` defines `execute_remediation(...)` as parallel per-file remediation with snapshots, agent retries, diff-size guard, per-file rollback, cross-file coherence, and pass/partial/fail return.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:1395-1448` converts active registry HIGH findings to `Finding` objects and calls `execute_remediation(...)` grouped by affected file.

### Cosmetic remediation lane
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/commands.py:153-172` exposes `--allow-cosmetic-remediation` and `--strict-no-remediation`.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:3092-3122` injects a roadmap-specific cosmetic remediator into shared `PipelineConfig`.
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py:286-365` invokes the remediator after gate failure and before normal failure/retry handling.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/cosmetic_remediator.py:682-724` defines `classify_gate_failure(...)`.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/cosmetic_remediator.py:1020-1096` defines `apply_cosmetic_remediations(...)`.

### Key Takeaways
- Porting convergence requires more than an LLM comparison step: it requires a file-backed deviation registry, stable IDs, budget accounting, iterative checker/remediator loops, rollback behavior, and pass/fail semantics based on active HIGH findings.
- Porting remediation to Backlog.md/Beads is feasible if each finding can be represented as an issue/task with stable ID, status, affected file(s), source layer, and run metadata, but exact behavior parity also requires snapshot/rollback and diff-size guards.
- The current classifier for deviation classes is explicitly unwired: `_run_deviation_analysis` notes all records currently render as `UNCLASSIFIED` (`executor.py:1603-1609`), and `DEVIATION_ANALYSIS_GATE` checks `unclassified_count == total_analyzed` (`gates.py:1390-1422`).

## Tasklist Pipeline Trace and Sprint-Compatible Output Adjacency

### Tasklist CLI command surface
- `/config/workspace/IronClaude/src/superclaude/cli/tasklist/commands.py:15-28` defines `tasklist_group()` with validation-only examples.
- `/config/workspace/IronClaude/src/superclaude/cli/tasklist/commands.py:31-82` defines only the `validate` subcommand, not `generate`.
- `/config/workspace/IronClaude/src/superclaude/cli/tasklist/commands.py:99-111` resolves `output_dir`, `roadmap_file`, and `tasklist_dir` defaults.
- `/config/workspace/IronClaude/src/superclaude/cli/tasklist/commands.py:113-160` auto-wires TDD/PRD paths from `.roadmap-state.json`, including the `input_type=tdd` fallback where `spec_file` is the TDD.
- `/config/workspace/IronClaude/src/superclaude/cli/tasklist/commands.py:161-173` builds `TasklistValidateConfig` and calls `execute_tasklist_validate`.
- `/config/workspace/IronClaude/src/superclaude/cli/tasklist/commands.py:181-185` exits non-zero when validation fails.

### Tasklist validate execution
- `/config/workspace/IronClaude/src/superclaude/cli/tasklist/executor.py:40-52` collects all `*.md` files in the tasklist directory and fails if none exist.
- `/config/workspace/IronClaude/src/superclaude/cli/tasklist/executor.py:92-188` defines `tasklist_run_step(...)`, a Claude subprocess runner that embeds inputs inline, supports cancellation, handles timeout/non-zero exits, sanitizes output, and returns `StepResult`.
- `/config/workspace/IronClaude/src/superclaude/cli/tasklist/executor.py:191-218` builds a single `tasklist-fidelity` step over `[roadmap.md] + tasklist_files + optional TDD/PRD`.
- `/config/workspace/IronClaude/src/superclaude/cli/tasklist/executor.py:221-248` parses `high_severity_count` from the generated report frontmatter; missing/unparseable report means failure.
- `/config/workspace/IronClaude/src/superclaude/cli/tasklist/executor.py:251-276` executes the shared pipeline and returns true only when there are no HIGH-severity deviations.

### Tasklist prompt builders
- `/config/workspace/IronClaude/src/superclaude/cli/tasklist/prompts.py:17-148` defines `build_tasklist_fidelity_prompt(...)`, scoped explicitly to roadmap→tasklist alignment only.
- `/config/workspace/IronClaude/src/superclaude/cli/tasklist/prompts.py:29-31` states that spec→tasklist validation is out of scope for tasklist fidelity and handled by the roadmap `spec-fidelity` step.
- `/config/workspace/IronClaude/src/superclaude/cli/tasklist/prompts.py:111-146` adds optional TDD/PRD supplementary validation dimensions when those files are provided.
- `/config/workspace/IronClaude/src/superclaude/cli/tasklist/prompts.py:151-234` defines `build_tasklist_generate_prompt(...)`, but its docstring states it is used by `/sc:tasklist` skill workflows and is not called by CLI `tasklist validate`; there is no `tasklist generate` CLI subcommand (`prompts.py:156-162`).

### Sprint-compatible output adjacency in skill protocol
- `/config/workspace/IronClaude/src/superclaude/commands/tasklist.md:12-18` describes `/sc:tasklist` as roadmap-to-tasklist conversion for execution via `superclaude sprint run`.
- `/config/workspace/IronClaude/src/superclaude/commands/tasklist.md:70-85` mandates invoking `sc:tasklist-protocol` and says the command file itself does not implement generation.
- `/config/workspace/IronClaude/src/superclaude/skills/sc-tasklist-protocol/SKILL.md:31-44` defines the output goal: deterministic, deliverable-centric, phase-consistent, multi-file, tier-classified, verification-aligned, and roadmap-validated.
- `/config/workspace/IronClaude/src/superclaude/skills/sc-tasklist-protocol/SKILL.md:91-123` defines file emission: exactly `N+1` files for generation (`tasklist-index.md` plus `phase-N-tasklist.md`), plus optional validation artifacts under `validation/`.
- `/config/workspace/IronClaude/src/superclaude/skills/sc-tasklist-protocol/SKILL.md:98-104` requires literal `phase-N-tasklist.md` filenames in the index and phase-local content only.
- `/config/workspace/IronClaude/src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1062-1117` defines the Sprint compatibility self-check, including phase file references, contiguous phase numbers, `T<PP>.<TT>` task IDs, phase heading format, end-of-phase checkpoints, and no registries in phase files.
- `/config/workspace/IronClaude/src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1170-1387` defines post-generation validation stages 7-10 using 2N validation agents, patch-plan artifacts, `sc:task` patch execution, and spot-check verification.

### Key Takeaways
- The CLI has tasklist validation only; tasklist generation is a skill/protocol behavior, not a `superclaude tasklist generate` implementation.
- Sprint-compatible output constraints are specified in the skill protocol and template docs, not currently enforced by a Python CLI generator.
- For Mastra + Backlog.md + Beads, the tasklist generator would need to be recreated as a deterministic workflow node or set of workflow nodes; existing Python code can validate its output but cannot generate it from the CLI today.

## Documentation Staleness and Code-Validation Matrix

### Roadmap command and skill docs
- `/config/workspace/IronClaude/src/superclaude/commands/roadmap.md:84-92` says `/sc:roadmap` must invoke `sc-roadmap-protocol`; **[CODE-VERIFIED]** command file itself is a slash-command wrapper and not the Python CLI, but the command activation rule is present in the command file.
- `/config/workspace/IronClaude/src/superclaude/commands/roadmap.md:92-98` says CLI is deterministic counterpart and command mirrors CLI run surface; **[CODE-VERIFIED]** for most listed run flags via `/config/workspace/IronClaude/src/superclaude/cli/roadmap/commands.py:32-298`, including convergence, compression, validation, source enrichment, and cosmetic remediation.
- `/config/workspace/IronClaude/src/superclaude/commands/roadmap.md:38` lists `--input-type auto|tdd|spec`; **[CODE-CONTRADICTED]** current CLI accepts `auto`, `tdd`, and `spec` in `commands.py:113-118`, but the help text says PRD files are auto-detected and `RoadmapConfig.input_type` includes `prd` in `models.py:117-119`. The command doc omits `prd` in the flag table even though PRD can be auto-detected positionally.
- `/config/workspace/IronClaude/src/superclaude/skills/sc-roadmap-protocol/SKILL.md:107-138` provides a wave-to-CLI-step crosswalk and explicitly distinguishes inference-only behavior; **[CODE-VERIFIED]** for the inline CLI chain `diff → debate → score → merge` in `_build_steps` (`executor.py:2068-2128`) and for lack of multi-spec consolidation in `_build_steps`.
- `/config/workspace/IronClaude/src/superclaude/skills/sc-roadmap-protocol/SKILL.md:111` says `_get_all_step_ids` is at `executor.py:2281-2300`; **[CODE-CONTRADICTED]** in the current file it appears at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:2283-2302` due to line drift.
- `/config/workspace/IronClaude/src/superclaude/skills/sc-roadmap-protocol/SKILL.md:111-126` lists `certify` as CLI step 14; **[CODE-CONTRADICTED]** `_get_all_step_ids` includes `certify` (`executor.py:2283-2302`), but `_build_steps` only constructs through `remediate` (`executor.py:1947-2208`), and grep found no production call to `build_certify_step`.
- `/config/workspace/IronClaude/src/superclaude/skills/sc-roadmap-protocol/SKILL.md:140-146` states convergence-score thresholds are inference-only and not CLI gate behavior; **[CODE-VERIFIED]** `DEBATE_GATE` only validates score shape/range (`gates.py:1155-1166`), and `build_debate_prompt` embeds round count but no threshold routing (`prompts.py:879-903`).
- `/config/workspace/IronClaude/src/superclaude/skills/sc-roadmap-protocol/SKILL.md:150-155` documents cosmetic remediation flags; **[CODE-VERIFIED]** flags exist in `commands.py:153-172`, remediator injection in `executor.py:3092-3122`, generic remediator lane in `pipeline/executor.py:286-365`.
- `/config/workspace/IronClaude/src/superclaude/skills/sc-roadmap-protocol/SKILL.md:181-204` says multi-spec consolidation invokes `sc:adversarial-protocol` in skill mode; **[CODE-VERIFIED as inference-only / no CLI counterpart]** because `_build_steps` has no multi-spec consolidation step and the skill itself labels this distinction in its crosswalk (`SKILL.md:130-137`).
- `/config/workspace/IronClaude/src/superclaude/skills/sc-roadmap-protocol/SKILL.md:288-305` describes validation with quality-engineer/self-review and aggregate thresholds; **[CODE-CONTRADICTED for CLI]** current CLI validation is `reflect` or parallel `reflect-{agent}` plus `adversarial-merge`, gated by `REFLECT_GATE`/`ADVERSARIAL_MERGE_GATE` (`validate_executor.py:239-339`, `validate_gates.py:31-70`), with no aggregate score thresholds or REVISE loop in `execute_validate` (`validate_executor.py:442-519`). The skill itself notes these thresholds are inference-only at `SKILL.md:140-146`.

### Tasklist command and skill docs
- `/config/workspace/IronClaude/src/superclaude/commands/tasklist.md:12-18` says `/sc:tasklist` generates sprint-compatible bundles; **[CODE-VERIFIED as skill behavior]** generation is specified in `sc-tasklist-protocol/SKILL.md:31-44` and file emission rules in `SKILL.md:91-123`.
- `/config/workspace/IronClaude/src/superclaude/commands/tasklist.md:28-30` says the command itself does not execute generation logic; **[CODE-VERIFIED]** the command file mandates skill invocation at `commands/tasklist.md:70-85`.
- `/config/workspace/IronClaude/src/superclaude/commands/tasklist.md:102-112` says validation artifacts are produced under `TASKLIST_ROOT/validation/`; **[CODE-VERIFIED as skill behavior]** stages 7-10 write `ValidationReport.md` and `PatchChecklist.md` under `validation/` (`sc-tasklist-protocol/SKILL.md:1242-1338`).
- `/config/workspace/IronClaude/src/superclaude/skills/sc-tasklist-protocol/SKILL.md:127-130` says CLI `superclaude tasklist validate` only performs fidelity validation; **[CODE-VERIFIED]** tasklist CLI defines only `validate` (`commands.py:31-82`), and prompt docstring confirms no `tasklist generate` CLI subcommand (`prompts.py:156-162`).
- `/config/workspace/IronClaude/src/superclaude/skills/sc-tasklist-protocol/SKILL.md:196-211` says `.roadmap-state.json` auto-wires `tdd_file` and `prd_file`; **[CODE-VERIFIED]** in CLI validation at `tasklist/commands.py:113-160`.
- `/config/workspace/IronClaude/src/superclaude/skills/sc-tasklist-protocol/rules/file-emission-rules.md:1-4` says the rules are read-only extracted references and skill uses inline copy; **[CODE-VERIFIED]** same rules appear inline in `SKILL.md:91-123`.

### Key Takeaways
- The strongest stale-doc risk is `certify`: documentation and tests describe it as part of the full pipeline, but production `_build_steps` does not currently wire it.
- The skill docs are increasingly explicit about inference-only versus CLI-canonical behavior; port work should preserve that distinction rather than treating every skill wave as Python CLI behavior.
- Tasklist generation exists as a protocol/skill, not as a Python CLI implementation. Any Mastra recreation that claims CLI parity must separate “validate existing tasklists” from “generate tasklists.”

## Mastra + Backlog.md + Beads Port Feasibility Mapping

### Section 2 mapping — Current pipeline assets to port
- Roadmap pipeline assets to port directly: step DAG (`executor.py:1947-2208`), gate definitions (`gates.py:1020-1441`), shared `execute_pipeline` semantics (`pipeline/executor.py:63-188`), prompt builders (`prompts.py`), resume state (`executor.py:2567-2683`, `executor.py:2870-2982`, `executor.py:3601-3701`), convergence registry (`convergence.py:90-207`), and validation executor (`validate_executor.py:239-519`).
- Tasklist validation assets to port directly: `TASKLIST_FIDELITY_GATE` (`tasklist/gates.py:23-46`), one-step validation DAG (`tasklist/executor.py:191-218`), and fidelity prompt (`tasklist/prompts.py:17-148`).
- Tasklist generation assets are protocol/spec assets, not executable Python generation code: `sc-tasklist-protocol/SKILL.md:148-1127`, templates, and rules.

### Section 4 mapping — Mastra orchestration shape
- Mastra workflow nodes can mirror `Step` objects: `id`, prompt/tool body, inputs, output artifact path, timeout, retry limit, model, and gate.
- Parallel generate and validation reflect groups map cleanly to Mastra parallel branches, but must preserve SuperClaude’s “if any parallel branch fails, cancel/halt group” behavior from `/config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py:91-95` and `/config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py:402-452`.
- Deterministic steps (`anti-instinct`, convergence checkers, deviation analysis, remediation tasklist generation, wiring verification) should remain code/tool nodes, not LLM prompt nodes, because current behavior is Python-enforced at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:977-1031` and `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:1290-1897`.
- Gates should be first-class Mastra validators after each node, with tier-specific enforcement equivalent to `/config/workspace/IronClaude/src/superclaude/cli/pipeline/gates.py:20-76`.

### Section 6 mapping — Backlog.md / Beads state model opportunities
- `.roadmap-state.json` can be represented in Backlog.md/Beads as a release-level state record: spec path/hash, input type, TDD/PRD paths, agents, depth, step statuses, validation status, fidelity status, remediate metadata, and certify metadata as currently written by `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:2627-2682`.
- `DeviationRegistry.findings` can become Beads issues keyed by `stable_id`, with fields for severity, dimension, description, location, source layer, status, first/last seen run, and files affected from `/config/workspace/IronClaude/src/superclaude/cli/roadmap/convergence.py:153-207`.
- `remediation-tasklist.md` items can map to Backlog/Beads remediation tasks with `ACTIVE`, `FIXED`, `FAILED`, `SKIPPED` lifecycle states. Current gate expects terminal statuses for actionable items via `_all_actionable_have_status` (`gates.py:245-267`) and `REMEDIATE_GATE` (`gates.py:1299-1322`).
- Sprint-compatible tasklist bundles map naturally to Backlog.md epics/phases and Beads tasks, but to preserve `superclaude sprint run` compatibility, the literal files (`tasklist-index.md`, `phase-N-tasklist.md`) should still be emitted or exported exactly as specified by `sc-tasklist-protocol/SKILL.md:91-123` and `SKILL.md:1062-1117`.

### Section 8 mapping — Feasibility conclusions and risk controls
- Feasibility is high for recreating orchestration shape in Mastra because current pipeline is already declarative-ish (`Step` data plus shared executor), but fidelity depends on porting gates and state semantics, not merely prompt order.
- Feasibility is medium for replacing `.roadmap-state.json`/`deviation-registry.json` with Backlog.md/Beads because stable IDs and statuses map well, but concurrency, atomic writes, and resume semantics must be carefully recreated.
- Feasibility is lower for tasklist generation parity if relying only on Python CLI code, because generation is currently a skill protocol. A Mastra port would need to implement the `sc-tasklist-protocol` algorithm as real workflow logic or preserve it as an LLM skill-equivalent node with strict output validation.
- Highest behavior-preservation risks: certification gate currently defined-only; CLI/skill divergence around validation thresholds and adversarial delegation; `WIRING_GATE` trailing mode effectively blocked by default `grace_period=0`; tasklist generation not executable in CLI.

### Key Takeaways
- Port roadmap as a workflow + gate/state machine, not as a monolithic prompt.
- Port tasklist validation from Python; port tasklist generation from protocol docs with explicit tests because no Python generator exists.
- Use Backlog.md/Beads to store stable, inspectable state (runs, findings, tasks), but keep export/import compatibility with existing markdown artifacts.

## Gaps and Questions

1. **Certification gate production wiring gap.** `CERTIFY_GATE`, `build_certify_step`, and `check_certify_resume` exist, tests reference them, and docs list `certify` as a pipeline step, but production `_build_steps` does not append a certify step and grep found no production call to `build_certify_step`. Question: is certification intentionally deferred, accidentally unwired, or invoked by another layer outside `execute_roadmap`?
2. **Trailing gate behavior mismatch.** `wiring-verification` is configured as `GateMode.TRAILING`, but shared executor forces blocking behavior when `config.grace_period == 0`; roadmap CLI exposes no grace-period flag. Question: should Mastra reproduce current effective blocking behavior or intended trailing/shadow behavior?
3. **Tasklist generation lacks Python CLI implementation.** The protocol and prompts define generation, but CLI exposes only validation. Question: should Mastra implement generation directly from the protocol, invoke a skill-like LLM node, or wait for a Python generator?
4. **Deviation classifier is not implemented.** Current code writes all deviations as `UNCLASSIFIED`, and the gate pins that invariant. Question: should a port preserve the current unclassified behavior or implement classification as a deliberate behavior change?
5. **Skill-vs-CLI divergence requires explicit product decision.** Roadmap skill docs include inference-only waves, thresholds, and skill-to-skill adversarial invocation that are not CLI-canonical. Question: should the Mastra port target CLI parity only, skill parity, or a merged future-state design?
6. **Backlog.md/Beads exact schema unknown in local code.** This investigation mapped conceptual state/task opportunities, but did not inspect a concrete Backlog.md/Beads schema in this repo. Question: what canonical fields and lifecycle statuses must be used for a real port?

## Stale Documentation Found

- **[STALE DOC]** `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` line-reference drift: the skill cites `_get_all_step_ids` at `cli/roadmap/executor.py:2281-2300`, while current code places it at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:2283-2302`.
- **[STALE DOC]** Roadmap skill/docs list `certify` as a CLI step, but current production `_build_steps` does not wire it. This is a substantive docs/code mismatch, not only line drift.
- **[STALE DOC]** `src/superclaude/commands/roadmap.md` flag table lists `--input-type auto|tdd|spec` but omits `prd` despite PRD auto-detection and `RoadmapConfig.input_type` allowing `prd`.
- **[STALE DOC]** Roadmap skill validation wave describes aggregate score thresholds and a REVISE loop; current CLI validation does not implement aggregate score routing or REVISE loops. The skill partially self-corrects by labeling thresholds as inference-only, but any consumer reading Wave 4 alone could infer stale CLI behavior.

## Summary

SuperClaude’s roadmap pipeline is a hybrid deterministic/LLM orchestration system built on reusable pipeline primitives (`Step`, `GateCriteria`, `StepResult`, `PipelineConfig`, `execute_pipeline`, `gate_passed`). The roadmap CLI wires a multi-step pipeline with parallel generation, inline adversarial diff/debate/score/merge, deterministic anti-instinct and wiring audits, convergence-mode spec fidelity, deviation analysis, remediation tasklist output, resume state, compression, cosmetic remediation, and optional post-run validation. Most gates are wired and enforced; `CERTIFY_GATE` is the notable defined-only/partially wired exception.

Tasklist CLI support is validation-only: `superclaude tasklist validate` builds one `tasklist-fidelity` step over roadmap + tasklist markdown files and optional TDD/PRD context. Tasklist generation exists in `/sc:tasklist` protocol docs and prompt builders, not as a Python CLI subcommand. Sprint-compatible output adjacency is specified by protocol rules: `tasklist-index.md`, literal `phase-N-tasklist.md` references, contiguous phases, `T<PP>.<TT>` tasks, deliverable registries, traceability matrices, and checkpoint tasks.

For Mastra + Backlog.md + Beads, the most faithful port strategy is to model roadmap execution as a workflow DAG with first-class gate validators and persistent state records. Backlog.md/Beads can represent runs, findings, remediation work, and sprint tasks, but behavior parity requires preserving stable IDs, status lifecycles, retry/rollback semantics, artifact exports, and gate enforcement. Tasklist generation needs explicit implementation from the skill protocol or an LLM-protocol node with strict validation, because the current CLI does not generate tasklists.
