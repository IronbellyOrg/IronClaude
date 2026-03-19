---
title: "Architecture Extraction: Release Eval & A/B Testing System"
date: "2026-03-19"
source_documents:
  - ".dev/releases/backlog/v5.xx_release-eval-ab-test/conversation-decisions.md"
  - "src/superclaude/cli/roadmap/executor.py"
  - "src/superclaude/cli/roadmap/commands.py"
  - "src/superclaude/cli/sprint/executor.py"
  - "src/superclaude/cli/roadmap/models.py"
  - "src/superclaude/cli/sprint/models.py"
  - "src/superclaude/cli/roadmap/gates.py"
  - "src/superclaude/cli/pipeline/models.py"
  - "src/superclaude/cli/pipeline/executor.py"
extraction_type: architecture
---

# Architecture Extraction: Release Eval & A/B Testing System

## 1. Locked Architecture Decisions (SS2-SS3)

### 1.1 Build Approach: Hybrid Skill-First + Parallel Python Library

**Decision**: Build the Python scoring library from day one AND build orchestration as Claude Code skills first. When proven, portify orchestration to CLI.

**Rationale**:
- Pure skill-first risks building it twice (portification cost)
- Pure CLI-first risks designing in the dark (no interactive iteration)
- 80% of the system (scoring, aggregation, isolation, runner) is deterministic Python -- no inference needed
- 20% (eval-suite generation, judge agent, orchestration) benefits from skill-first iteration
- Follows proven pattern from v2.25-cli-portify-cli

**What gets built once (Python library)**: models.py, rubric.py, aggregator.py, isolation.py, runner.py, judge.py, reporter.py

**What gets built twice (orchestration, ~20%)**: Pipeline step ordering, error handling, state management

### 1.2 Spec Approach: New Spec From Scratch

**Decision**: Write a new spec. Do NOT refactor unified-audit-gating-v1.2.1-release-spec.md.

**Rationale**:
- Only ~20-25% conceptual overlap between audit-gating and eval systems
- Different consumers, execution models, and cost profiles
- Refactoring 440 lines where 75-80% must be removed creates "ghosts"
- Cherry-pick methodology patterns (evidence model, locked decisions, contradictions table, pass/fail rules, evidence requirements, checklist closure matrix) but reference domain models as "Related Work" only

### 1.3 Version Ordering

**Decision**: Build `sc:ab-test` (v1.0) first, then `sc:release-eval` (v2.0).

**Rationale**: A/B testing already has a detailed backlog spec; A/B infrastructure (multi-run, scoring, isolation) is foundation for release-eval; smaller scope proves scoring library first.

### 1.4 Two Separate Skills, Shared Library

**Decision**: Two separate top-level skills/commands sharing a scoring library -- NOT one skill with different modes.

**Rationale**: Different test subjects (command vs release), different workflows, different outputs. Shared infrastructure lives in the Python library. When portified to CLI: `superclaude ab-test` and `superclaude release-eval`.

### 1.5 Scoring & Judging Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Judge model | Always Opus (configurable via `--judge-model`) | Highest quality scoring |
| Eval runner models | Cheaper models (Sonnet, Haiku) by default | Cost efficiency |
| Scoring dimensions | 5: structure, completeness, accuracy, actionability, efficiency | From v3.1 A/B spec |
| Consistency target | Within-model consistency (not cross-model) | Cross-model is informational only |
| Budget guardrails | None -- model selection controls cost | Eval runs use cheap models |

### 1.6 Failure Model (Four Layers)

| Layer | Type | Verdict |
|---|---|---|
| Layer 1 -- Structural | File presence, schema validity | **Hard PASS/FAIL** |
| Layer 2 -- Functional | CLI execution, exit codes, artifacts | **Hard PASS/FAIL** per test |
| Layer 3 -- Quality | LLM judge scoring against rubric | **Scored** (1-10 per dimension) |
| Layer 4 -- Regression | Before/after statistical comparison | **Scored** + statistical test |

Overall verdict: PASS requires all structural/functional pass AND quality above configurable thresholds.

### 1.7 Before/After Mechanism

Three modes using `.claude/` directory isolation:
1. **Global vs Local**: Skip `make sync-dev` -- global = old, local = new
2. **Vanilla vs Skill**: Disable all `.claude/` -- compare raw Claude vs skill
3. **Example**: Vanilla prompt vs `sc:tasklist roadmap.md`

### 1.8 Fixture Generation

Auto-generated from spec analysis by Claude, human reviews before execution. Standard fixtures: happy-path.md, empty-input.md, malformed.md, large-input.md, bug-repro.md (for patch releases).

### 1.9 Cross-Model Testing

Run same eval suite across multiple models. Scores reported per-model. Not compared across models unless explicitly requested.

### 1.10 Trigger Model

Manual invocation for now. Future: integrate into release pipeline (Phase 12) and CI.

### 1.11 Release Type Handling

Same interface for feature and bug fix releases. Eval-suite generator adapts test types based on release type (structural tests, functional tests, quality tests, regression tests vary by type).

---

## 2. Complete Data Model (SS6)

```python
@dataclass
class Score:
    dimension: str          # structure|completeness|accuracy|actionability|efficiency
    value: float            # 1.0 - 10.0
    hard_fail: bool         # True = binary failure
    reasoning: str          # Judge's explanation

@dataclass
class RunResult:
    test_id: str
    run_number: int
    model: str
    scores: list[Score]
    exit_code: int
    tokens_used: int
    wall_time_seconds: float
    artifacts: list[str]
    stdout: str
    stderr: str

@dataclass
class TestVerdict:
    test_id: str
    layer: str              # structural|functional|quality|regression
    passed: bool
    aggregate_scores: dict  # dimension -> {mean, stddev, min, max}
    runs: list[RunResult]

@dataclass
class EvalReport:
    release: str
    timestamp: str
    tests: list[TestVerdict]
    overall_passed: bool
    model_breakdown: dict   # model -> {dimension -> mean_score}
    recommendations: list[str]
```

---

## 3. Shared Library Structure (SS5)

```
src/superclaude/eval/
    __init__.py
    models.py         <- Score, RunResult, TestVerdict, EvalReport dataclasses
    rubric.py         <- 5-dimension scoring rubric + anchored definitions
    judge.py          <- Judge-agent prompt template + response parser
    runner.py         <- Multi-run parallel execution engine (subprocess)
    isolation.py      <- .claude/ directory toggling with trap-safe restore
    aggregator.py     <- Mean, stddev, p-values, effect size, Cohen's d
    reporter.py       <- report.md + scores.jsonl template rendering
```

### sc:ab-test (v1.0) Layout

```
# Skill phase
.claude/skills/sc-ab-test/SKILL.md
.claude/commands/sc/ab-test.md

# CLI phase (after portification)
src/superclaude/cli/ab_test/
    __init__.py
    main.py           <- Click command group
    executor.py       <- Orchestrates tiers
    prompts.py        <- Vanilla-equivalent prompt library
```

Three tiers:
1. **Regression**: baseline (global) vs candidate (local) -- 5 runs each
2. **Value Validation**: vanilla vs baseline vs candidate -- 5 runs each
3. **Deprecation Audit**: vanilla vs current -- 5 runs each

### sc:release-eval (v2.0) Layout

```
# Skill phase
.claude/skills/sc-release-eval/SKILL.md
.claude/commands/sc/release-eval.md

# CLI phase (after portification)
src/superclaude/cli/release_eval/
    __init__.py
    main.py           <- Click command group
    spec_parser.py    <- Extract ACs, FRs, NFRs from release spec
    suite_generator.py <- Generate eval-suite.yaml from parsed spec
    executor.py       <- Run eval suite (structural -> functional -> quality -> regression)
    reporter.py       <- Produce validation report + scores
```

Workflow: PARSE spec -> GENERATE eval suite -> REVIEW (human pause) -> EXECUTE (layers 1-4, fail-fast) -> SCORE (judge model) -> REPORT

---

## 4. Seven-Slice Incremental Delivery Plan (SS7)

| Slice | Deliverable | Tested Against |
|---|---|---|
| 1 | Scoring library + single-run judge | Score one output from v2.25-cli-portify-cli manually |
| 2 | Multi-run engine + aggregation | Run sc:tasklist 5x on v2.25 roadmap, score each |
| 3 | sc:ab-test regression tier | Modify a skill, verify before/after comparison |
| 4 | sc:ab-test value + deprecation tiers | Vanilla vs sc:explain on a file |
| 5 | Spec parser + eval-suite generator | Point at v2.25-cli-portify-cli, generate suite |
| 6 | Release eval executor | Execute generated suite, get full report |
| 7 | CLI portification | superclaude ab-test / superclaude release-eval |

**Critical principle**: Build smallest functional slice, eval it against real completed releases from day one.

---

## 5. Acceptance Criteria

### 5.1 sc:ab-test v1.0 (SS9)

- **AC-01**: Can run regression test comparing global vs local version of any command
- **AC-02**: Can run value-validation test comparing vanilla vs baseline vs candidate
- **AC-03**: Produces scores.jsonl with per-dimension scores per run
- **AC-04**: Produces summary.md with aggregate scores, variance, statistical comparison
- **AC-05**: Handles model selection (run same test on different models)
- **AC-06**: Results reproducible -- same model + input produces scores within 1 stddev
- **AC-07**: Safety: trap handler guarantees .claude/ directories restored on exit/error/SIGINT
- **AC-08**: --dry-run validates isolation without executing any runs

### 5.2 sc:release-eval v2.0 (SS10)

- **AC-01**: Given a release directory, parses spec and extracts ACs/FRs/NFRs
- **AC-02**: Generates eval-suite.yaml with tests across all 4 layers
- **AC-03**: Auto-generates fixtures appropriate to release type
- **AC-04**: Presents generated suite for human review before execution
- **AC-05**: Executes layers in order with fail-fast (structural failure stops early)
- **AC-06**: Judge model scores each run independently
- **AC-07**: Produces per-model score breakdowns
- **AC-08**: Produces human-readable report.md with verdict + recommendations
- **AC-09**: Works on both feature releases and bug fix releases
- **AC-10**: Can re-run evals on already-completed releases (retroactive)

---

## 6. Open Decisions (SS13) -- 6 Documented, Spec Must Resolve

| # | Decision | Context | Options |
|---|---|---|---|
| 1 | Minimum runs for statistical significance | v3.1 spec says 5, metrics schema says 20 | Reconcile: 5 for quick regression, 20 for value validation? |
| 2 | Eval suite versioning | What happens when spec changes? | Re-generate suite? Version-lock? |
| 3 | Concurrent eval isolation | Two evals touching .claude/ simultaneously | Queue or worktree-based isolation? |
| 4 | Score persistence format | JSONL vs SQLite vs both | JSONL for simplicity, SQLite for querying? |
| 5 | Vanilla prompt authoring | Auto-generated or hand-crafted? | v3.1 spec has library; need maintenance model |
| 6 | Slice 1-2 release target | Ship scoring library separately or with ab-test? | Single release or multiple? |

**Note**: The conversation-decisions.md lists these as "13 open decisions" in the section header but the table contains exactly 6 entries. The spec must reconcile whether additional open decisions were intended but omitted, or whether the section header is a typo.

---

## 7. Cross-Reference Against Existing CLI Infrastructure

### 7.1 Eval Executor vs roadmap/executor.py

**Pattern Analysis: `execute_roadmap()` (roadmap/executor.py lines 1256-1383)**

The roadmap executor follows this pattern:
1. Config validation and defaults application
2. `_build_steps(config)` returns `list[Step | list[Step]]` -- sequential steps and parallel groups
3. Optional `_apply_resume()` to skip already-passing steps
4. Delegate to `execute_pipeline()` from `pipeline/executor.py` with a `StepRunner` callable (`roadmap_run_step`)
5. State persistence via `_save_state()` using atomic `write_state()` (tmp + os.replace)
6. Failure analysis and diagnostic output via `_format_halt_output()`
7. Post-completion auto-invocation of validation

**Mapping to Eval Executor**:

| Roadmap Pattern | Eval Equivalent | Reuse/Build |
|---|---|---|
| `_build_steps()` returns `list[Step \| list[Step]]` | Eval builds test execution plan from eval-suite.yaml | **New** -- tests are YAML-driven, not hardcoded |
| `execute_pipeline()` generic sequencer | Layer-ordered test execution (structural -> functional -> quality -> regression) | **Reuse** -- `execute_pipeline()` handles step ordering, retry, gates, parallel dispatch |
| `roadmap_run_step()` as StepRunner | Eval needs a `run_eval_step()` StepRunner that handles multi-run logic | **New** -- fundamentally different (N runs per test, not 1 subprocess per step) |
| `_apply_resume()` skip-passing-steps | Eval likely needs resume for long-running suites | **Reuse pattern** -- same gate-check-and-skip logic applies |
| `_save_state()` atomic state writes | Eval needs `.eval-state.json` state tracking | **Reuse** -- `write_state()` / `read_state()` are generic |
| `_sanitize_output()` preamble stripping | Not needed -- eval outputs are structured (JSONL/YAML) | **N/A** |
| `_format_halt_output()` failure diagnostics | Eval needs failure reporting with which layer/test failed | **New** -- different failure semantics (layers, not steps) |

**Key Structural Difference**: The roadmap executor runs each step exactly once (with retry). The eval executor must run each test N times (multi-run) and aggregate results. This means `runner.py` in the eval library must wrap `ClaudeProcess` in a loop, which is architecturally different from `roadmap_run_step()` calling `ClaudeProcess` once.

### 7.2 Eval Runner vs sprint/executor.py

**Pattern Analysis: `execute_phase_tasks()` (sprint/executor.py lines 506-606)**

The sprint executor runs a list of tasks sequentially within a phase:
1. Budget check via `TurnLedger.can_launch()` before each task
2. Debit minimum allocation upfront
3. Spawn subprocess (via factory or `ClaudeProcess`)
4. Wait for completion, capture exit_code/turns/output_bytes
5. Reconcile budget (debit actual, credit back pre-allocation overage)
6. Post-task wiring hook (`run_post_task_wiring_hook()`)
7. Return `(list[TaskResult], list[remaining_task_ids])`

**Mapping to Eval Runner**:

| Sprint Pattern | Eval Equivalent | Reuse/Build |
|---|---|---|
| `TurnLedger` budget tracking | Eval has no turn budget -- model selection controls cost | **Not needed** |
| `execute_phase_tasks()` sequential task loop | `runner.py` multi-run parallel execution | **New** -- eval runs same test N times in parallel, sprint runs different tasks sequentially |
| `_run_task_subprocess()` spawning ClaudeProcess | Eval subprocess spawning for functional/quality tests | **Reuse** -- `ClaudeProcess` from pipeline.process is the shared primitive |
| `IsolationLayers` 4-layer subprocess isolation | `isolation.py` .claude/ directory toggling | **Partially reuse pattern** -- different isolation needs (env vars vs directory swapping) |
| `AggregatedPhaseReport` runner-constructed report | `aggregator.py` mean/stddev/p-values | **New** -- fundamentally different aggregation (statistical vs count-based) |
| `run_post_task_wiring_hook()` post-task analysis | Judge agent scoring after each run | **Pattern reuse** -- same hook-after-execution concept, different implementation |
| `SprintGatePolicy.build_remediation_step()` | Not applicable -- eval does not remediate, it reports | **Not needed** |

**Key Structural Difference**: Sprint execution is a linear sequence of tasks with budget tracking and early termination. Eval execution is a layered structure where each layer runs N parallel instances of the same test. The eval runner has more in common with `_run_parallel_steps()` from pipeline/executor.py than with sprint's sequential task loop.

### 7.3 Reusable Infrastructure (Build Once)

#### Directly Reusable (Import and Use)

| Component | Location | How Eval Uses It |
|---|---|---|
| `PipelineConfig` | `pipeline/models.py` | `EvalConfig(PipelineConfig)` inherits work_dir, dry_run, max_turns, model, permission_flag, debug |
| `Step` dataclass | `pipeline/models.py` | Each eval test becomes a Step with gate criteria |
| `StepResult` dataclass | `pipeline/models.py` | Eval step outcomes use same status tracking |
| `StepStatus` enum | `pipeline/models.py` | PASS/FAIL/TIMEOUT/CANCELLED/SKIPPED applies directly |
| `GateCriteria` | `pipeline/models.py` | Structural tests define gates with required_frontmatter_fields and min_lines |
| `SemanticCheck` | `pipeline/models.py` | Quality threshold checks can use the semantic check framework |
| `GateMode` (BLOCKING/TRAILING) | `pipeline/models.py` | Layer 1-2 are BLOCKING; Layer 3-4 could be TRAILING |
| `execute_pipeline()` | `pipeline/executor.py` | Orchestrate layer execution with retry and gate logic |
| `_run_parallel_steps()` | `pipeline/executor.py` | Run N copies of same test in parallel |
| `gate_passed()` | `pipeline/gates.py` | Validate structural test outputs against gate criteria |
| `ClaudeProcess` | `pipeline/process.py` | Subprocess management for functional/quality tests |
| `write_state()` / `read_state()` | `roadmap/executor.py` | Atomic state persistence for eval runs (should be lifted to pipeline/) |
| `_parse_frontmatter()` | `roadmap/gates.py` | Parse YAML frontmatter from eval outputs (should be lifted to pipeline/) |

#### Pattern Reuse (Adapt, Don't Import)

| Pattern | Source | Adaptation Needed |
|---|---|---|
| `_build_steps()` step construction | `roadmap/executor.py` | Eval builds steps from YAML, not hardcoded |
| `_apply_resume()` gate-check skip | `roadmap/executor.py` | Same logic: skip tests whose outputs pass gates |
| `_embed_inputs()` inline prompt embedding | `roadmap/executor.py` | Eval prompts embed fixture content same way |
| `AgentSpec.parse()` model:persona parsing | `roadmap/models.py` | Eval needs model specification for `--judge-model` and `--runner-models` |
| `_dry_run_output()` plan printing | `roadmap/executor.py` | Eval --dry-run prints test plan and isolation checks |
| `_format_halt_output()` failure diagnostics | `roadmap/executor.py` | Eval failure output shows which layer/test/run failed |
| `AggregatedPhaseReport.to_yaml()` | `sprint/executor.py` | Eval report rendering follows same structured output pattern |

#### Must Build New

| Component | Why Not Reusable |
|---|---|
| `models.py` (Score, RunResult, TestVerdict, EvalReport) | Domain-specific data model for scoring, not pipeline steps |
| `rubric.py` (5-dimension scoring rubric) | New concept -- no existing scoring rubric in codebase |
| `judge.py` (LLM judge prompt + parser) | New concept -- no judge agent pattern exists |
| `runner.py` (multi-run parallel engine) | Different from both roadmap (1 run per step) and sprint (sequential tasks) -- runs same test N times |
| `isolation.py` (.claude/ directory toggling) | Sprint has IsolationLayers but different mechanism (env vars vs directory swap with trap-safe restore) |
| `aggregator.py` (statistics: p-values, Cohen's d) | Partially exists in scripts/ab_test_workflows.py but needs proper packaging |
| `reporter.py` (report.md rendering) | New template; existing report formats are phase-reports, not eval reports |
| `spec_parser.py` (extract ACs/FRs/NFRs) | New concept -- no existing spec parsing in pipeline |
| `suite_generator.py` (generate eval-suite.yaml) | New concept -- no existing test generation |
| Eval-suite YAML schema | New artifact format |
| Results directory structure (`<release>/evals/runs/<timestamp>/`) | New output structure |

### 7.4 Infrastructure Gaps Requiring Lifting

Several utilities currently live in roadmap/ or sprint/ but should be promoted to pipeline/ for eval to reuse:

1. **`write_state()` / `read_state()`** -- Currently in `roadmap/executor.py`. Generic atomic JSON state persistence. Eval needs `.eval-state.json` with the same pattern. Should live in `pipeline/state.py`.

2. **`_parse_frontmatter()`** -- Currently in `roadmap/gates.py`. Generic YAML frontmatter parser. Eval structural tests need to parse frontmatter. Should live in `pipeline/frontmatter.py` or be a utility in `pipeline/gates.py`.

3. **`_sanitize_output()` atomic write pattern** -- The tmp-file + os.replace() pattern appears in both `roadmap/executor.py` and `write_state()`. Should be a shared `atomic_write()` utility.

4. **`AgentSpec` model parsing** -- Currently in `roadmap/models.py`. Eval needs `--judge-model opus` and `--runner-models sonnet,haiku` parsing. Could be generalized.

### 7.5 Click Command Integration Pattern

From `roadmap/commands.py`, the established CLI pattern is:

```python
@click.group("eval")          # Top-level group
def eval_group(): ...

@eval_group.command()          # Subcommand
@click.argument(...)
@click.option(...)
def run(...):
    from .executor import execute_eval
    config = EvalConfig(...)
    execute_eval(config, ...)
```

The eval system should follow this exact pattern:
- `superclaude ab-test run <command> [--tier regression|value|deprecation]`
- `superclaude release-eval run <release-dir> [--layers all|structural|quality]`

Both share `--dry-run`, `--model`, `--max-turns`, `--debug` from PipelineConfig convention. New flags: `--judge-model`, `--runs`, `--models` (runner models).

### 7.6 Subprocess Management via ClaudeProcess

Both roadmap and sprint executors use `ClaudeProcess` from `pipeline/process.py` for subprocess management. The eval runner must use the same primitive but with a key difference:

- **Roadmap**: `ClaudeProcess(prompt=..., output_file=..., output_format="text")` -- one process per step
- **Sprint**: `ClaudeProcess(prompt=..., output_format="stream-json")` -- one process per task with NDJSON monitoring
- **Eval**: Must run `ClaudeProcess` N times per test, potentially in parallel, with `output_format="text"` for artifact collection and `"stream-json"` for token counting

The eval `runner.py` wraps `ClaudeProcess` in a loop/pool pattern, collecting `RunResult` per execution.

### 7.7 Gate Framework Applicability

The existing gate framework (`GateCriteria` + `gate_passed()` + `SemanticCheck`) maps naturally to eval layers:

| Eval Layer | Gate Type | Implementation |
|---|---|---|
| Structural (L1) | `GateCriteria` with `required_frontmatter_fields` and file existence | **Direct reuse** of existing gate framework |
| Functional (L2) | Exit code check + artifact presence | Lightweight gate (exit_code == 0 + file exists) |
| Quality (L3) | Score threshold check | New `SemanticCheck` functions: `_score_above_threshold(content) -> bool` |
| Regression (L4) | Statistical significance check | New check: `_regression_significant(content) -> bool` |

The `enforcement_tier` concept (STRICT/STANDARD/LIGHT/EXEMPT) could map to layer severity: L1-L2 are STRICT (hard fail), L3-L4 are STANDARD (scored, configurable threshold).

---

## 8. Non-Functional Requirements (SS8)

- **NFR-01**: Eval suite generation < 60 seconds (spec analysis, not execution)
- **NFR-02**: Structural tests < 500 tokens, functional < 5K, quality < 20K per run
- **NFR-03**: Within-model variance measured (target CV < 0.15)
- **NFR-04**: Must work retrospectively on already-completed releases
- **NFR-05**: Read-only -- never modifies release artifacts
- **NFR-06**: Results stored in evals/ directory within release dir

---

## 9. Existing Assets to Build On (SS4)

| Asset | Location | Relevance |
|---|---|---|
| A/B testing spec | `.dev/releases/backlog/v3.1-ab-testing/release-plan.md` | Full design for sc:ab-test -- 3 tiers, isolation, rubric, vanilla prompts |
| Statistical comparison engine | `scripts/ab_test_workflows.py` | Can compute p-values, effect sizes |
| Metrics aggregation | `scripts/analyze_workflow_metrics.py` | Aggregates JSONL metrics |
| Workflow metrics schema | `docs/memory/WORKFLOW_METRICS_SCHEMA.md` | JSONL format, 20-run minimums |
| Completed releases (test corpus) | `.dev/releases/complete/` | 10+ releases to test against retroactively |

### Test Corpus (Priority Releases for Retroactive Evaluation)

| Release | Type | Best For |
|---|---|---|
| v2.25-cli-portify-cli | Feature (large, 60+ deliverables) | Full eval suite generation, quality scoring |
| v2.25.7-Phase8HaltFix | Bug fix (patch) | Bug repro tests, regression verification |
| v2.25.5-PreFlightExecutor | Feature (medium) | Functional tests, artifact checks |
| v2.24.5-SpecFidelity | Feature | Structural + quality validation |
| v2.24.2-Accept-Spec-Change | Feature | Gate validation, schema compliance |
| v2.20-WorkflowEvolution | Feature (large) | Complex multi-phase eval |

---

## 10. Architecture Risk Assessment

### High Risk: Multi-Run Parallel Execution

The eval runner must execute the same test N times in parallel. No existing component does this. `_run_parallel_steps()` runs *different* steps in parallel. The eval runner needs to run the *same* step N times with isolated output directories per run. This is the most novel infrastructure requirement.

### Medium Risk: .claude/ Directory Isolation

The before/after mechanism requires swapping `.claude/` contents mid-evaluation. Sprint's `IsolationLayers` uses environment variables. Eval's `isolation.py` must physically move/symlink directories with a trap-safe restore guarantee (AC-07). Signal handling and crash recovery are critical -- a failed eval that leaves `.claude/` in a dirty state corrupts the development environment.

### Medium Risk: Judge Agent Reliability

No existing judge agent pattern exists in the codebase. `judge.py` must produce parseable, consistent scores from a prompt template. The prompt must be robust enough that Opus returns structured JSON/YAML scores, not conversational text. This is inference-dependent and requires iteration.

### Low Risk: State Management

`write_state()` / `read_state()` with atomic writes is proven in roadmap. Lifting to pipeline/ is mechanical.

### Low Risk: Click CLI Integration

The Click command group pattern is well-established across roadmap and sprint. Adding `ab_test/` and `release_eval/` command groups follows the exact same structure.
