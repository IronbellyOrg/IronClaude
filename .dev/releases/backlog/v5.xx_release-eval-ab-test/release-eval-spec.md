# Release Spec: Post-Release Eval & A/B Testing CLI Tool

```yaml
---
title: "Post-Release Eval & A/B Testing CLI Tool"
version: "1.0.0"
status: draft
feature_id: FR-EVAL
parent_feature: null
spec_type: new_feature
complexity_score: 0.75
complexity_class: HIGH
target_release: v4.0
authors: [user, claude]
created: 2026-03-19
quality_scores:
  clarity: 9.0
  completeness: 9.5
  testability: 9.0
  consistency: 9.0
  overall: 9.1
---
```

## 1. Problem Statement

Current testing infrastructure has a critical gap between unit tests and real-world system behavior. Unit tests (`tests/`) check internal Python logic but do not exercise actual system behavior. Smoke tests (`scripts/smoke-test-v2.sh`) check artifact existence but not functional correctness or quality. No quality measurement exists -- nothing scores output quality, measures consistency across runs, or compares before/after. The project lacks full runs of actual systems with proper evals that produce consistent scores across multiple runs and models.

This spec defines two complementary CLI commands sharing a scoring library:
- `superclaude ab-test` (v1.0): Command/skill regression and value testing -- "did this skill get better or worse?"
- `superclaude release-eval` (v2.0): Post-release validation against spec -- "did this release deliver what it promised?"

### 1.1 Evidence

| Evidence | Source | Impact |
|----------|--------|--------|
| No quality scoring exists for command outputs | Current test infrastructure audit | Cannot measure whether changes improve or degrade output quality |
| No statistical comparison between versions | Missing from CI/CD pipeline | Regressions in output quality go undetected until user complaints |
| No post-release validation against spec promises | Release workflow gap | Releases ship without evidence they deliver on stated requirements |
| Completed releases exist as a test corpus (10+) | `.dev/releases/complete/` | Retroactive evaluation capability is blocked by missing tooling |
| Existing prototype (`scripts/eval_runner.py`) covers ~40% of needed functionality | `scripts/eval_runner.py` | Proves the approach is viable but lacks multi-model, isolation, and quality scoring |

### 1.2 Scope Boundary

**In scope**:
- Shared scoring library (`src/superclaude/eval/`) with 9 modules
- `superclaude ab-test` CLI command with 3 tiers (regression, value validation, deprecation)
- `superclaude release-eval` CLI command with 4-layer failure model
- Judge agent integration via ClaudeProcess for quality scoring
- `.claude/` directory isolation with trap-safe restore
- Statistical aggregation (mean, stddev, p-values, Cohen's d)
- Report generation (report.md + scores.jsonl)
- Eval suite YAML schema and generation from release specs
- Vanilla-equivalent prompt library

**Out of scope**:
- Docker isolation for vanilla baseline (future enhancement)
- Pipeline-integrated evals (Phase 12 in sprint pipeline)
- CI-triggered A/B tests on PRs touching commands/skills
- Eval dashboard for historical score tracking
- Judge model experimentation and optimization
- Pairwise preference scoring as primary method (alternative only)
- Cross-command scoring normalization
- SQLite score persistence (JSONL sufficient for v1)
- The 6-prompt v3.0 eval workflow (manual procedure, not a release deliverable; informs design only)

## 2. Solution Overview

Build two separate CLI commands (`superclaude ab-test` and `superclaude release-eval`) sharing a Python scoring library at `src/superclaude/eval/`. The library handles the deterministic 80% of the system (scoring, aggregation, isolation, execution), while the CLI commands provide the user-facing orchestration.

The system implements a 4-layer failure model: structural (file presence, schema) produces hard PASS/FAIL; functional (CLI execution, exit codes) produces hard PASS/FAIL per test; quality (LLM judge scoring) produces scored results on 5 dimensions; regression (before/after comparison) produces scored results with statistical tests. Layers execute in order with fail-fast behavior -- structural failures halt evaluation before functional tests run.

### 2.1 Key Design Decisions

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| Build approach | CLI-first with Python library from day one | Skill-first with later portification; Pure CLI-first | The 6-prompt workflow proved direct CLI invocation works. Skill-first would build orchestration twice. The library captures the deterministic 80%; CLI wraps it directly. **DECISION OVERRIDE (D-08)**: conversation-decisions.md Section 2 specified "Hybrid Skill-First + Parallel Python Library." This spec overrides to CLI-first because: (1) the 6-prompt v3.0 eval workflow proved CLI pipeline invocation works without skill discovery, (2) the 20% orchestration cost of build-twice portification is avoidable, and (3) the existing `scripts/eval_runner.py` prototype demonstrates the CLI pattern is viable. |
| Spec approach | New spec from scratch | Refactor unified-audit-gating spec | Only 20-25% conceptual overlap. Refactoring 440 lines where 75-80% must be removed creates ghosts. Clean spec is purpose-built and self-consistent. |
| Version ordering | ab-test (v1.0) first, release-eval (v2.0) second | Single combined release; release-eval first | A/B infrastructure (multi-run, scoring, isolation) is the foundation release-eval builds on. Smaller scope proves the scoring library first. |
| Two commands, shared library | Separate `superclaude ab-test` and `superclaude release-eval` | Single command with modes | Different test subjects (command vs release), different workflows, different outputs. Shared infrastructure lives in the Python library. |
| Judge model | Always Opus, configurable via `--judge-model` | Fixed model; Cheapest available | Highest quality scoring. Easy to swap later via CLI flag. |
| Scoring method | Rubric-anchored (primary) | Pairwise preference | Rubric-anchored produces absolute scores comparable across runs. Pairwise is an alternative for future exploration. |
| Score persistence | JSONL primary, no SQLite in v1 | SQLite; Both | JSONL is the existing convention (workflow_metrics.jsonl). Simple to append, grep, and parse. SQLite deferred until cross-run querying becomes a real need. |
| Isolation mechanism | Worktree-first with env-var fallback | Directory rename primary; Docker | Worktree isolation is crash-safe by design (no filesystem mutation of .claude/). Env-var overrides provide supplementary skill-level toggling. Directory rename is a last resort only if other approaches prove insufficient. |
| Statistical minimums | Tiered: 5 runs regression, 10 value validation, 5 deprecation | Flat 5; Flat 20 | 5 runs detect large effects (Cohen's d > 0.8). Value validation tests subtler effects requiring more power. 20 ideal but expensive; 10 is pragmatic. Original source specified "5 each" for all tiers; overridden based on statistical power analysis. |
| Eval runner architecture | CLI pipeline invocation via subprocess (NOT pytest) | Pytest-based execution | The new runner must invoke `superclaude roadmap run` (or equivalent) via subprocess. The existing `scripts/eval_runner.py` (pytest-based) is a separate, complementary tool for rapid Python-level validation. |
| Concurrent isolation | File lock + worktree fallback | Queue only; Worktree only | File locking prevents the dangerous case (two processes renaming .claude/ simultaneously). Worktrees enable parallelism when needed via `--parallel` flag. |
| Vanilla prompt authoring | Hand-crafted library with peer review | Auto-generated | Fair vanilla prompts are critical to validity. Sandbagged prompts make commands look artificially good. Human authorship with review is the only way to ensure fairness. |

### 2.2 Workflow / Data Flow

**sc:ab-test workflow:**

```
USER invokes: superclaude ab-test --command sc:roadmap --tier regression --runs 5

  [1] PARSE command + tier + config
  [2] SETUP isolation (worktree for baseline, env-var for vanilla)
  [3] EXECUTE N runs per variant (parallel within variant)
      baseline: N runs of command on global/.claude state
      candidate: N runs of command on local/.claude state
      (vanilla: N runs with plain prompt, if tier=value/deprecation)
  [4] SCORE each run output via judge agent (ClaudeProcess -> Opus)
  [5] AGGREGATE per-dimension scores (mean, stddev, p-values, Cohen's d)
  [6] REPORT summary.md + scores.jsonl + verdict
  [7] TEARDOWN isolation (restore .claude/, remove worktrees)
```

**sc:release-eval workflow:**

```
USER invokes: superclaude release-eval run .dev/releases/complete/v2.25-cli-portify-cli/

  [1] PARSE spec -> extract ACs, FRs, NFRs (spec_parser.py)
  [2] GENERATE eval-suite.yaml with tests across 4 layers (suite_generator.py)
  [3] REVIEW -> present suite to user, wait for approval (--approve or two-step)
  [4] EXECUTE layers in fail-fast order:
      Layer 1 (Structural): file presence, schema validity -> hard PASS/FAIL
      Layer 2 (Functional): CLI execution, exit codes -> hard PASS/FAIL per test
      Layer 3 (Quality): LLM judge scoring, N runs per test -> scored 1-10
      Layer 4 (Regression): before/after comparison -> scored + p-values
  [5] SCORE aggregate across runs (aggregator.py)
  [6] REPORT report.md + scores.jsonl + verdict + recommendations
```

## 3. Functional Requirements

### FR-EVAL.1: Score Dataclass and Data Model

**Description**: Define core data model for scoring: Score (dimension, value, hard_fail, reasoning), RunResult (per-execution capture), TestVerdict (per-test aggregation), EvalReport (full evaluation summary), ABComparison (A/B tier result), and EvalConfig (execution configuration).

**Acceptance Criteria**:
- [ ] Score dataclass supports 5 named dimensions with values 1.0-10.0, hard_fail flag, and reasoning string
- [ ] RunResult captures test_id, run_number, model, scores, exit_code, tokens_used, wall_time_seconds, artifacts, stdout_path, stderr_path, steps_completed, steps_total
- [ ] TestVerdict aggregates across runs with per-dimension mean/stddev/min/max and includes past_failed_gate annotation (False by default; True when layer ran after a prior layer failed in eval-mode)
- [ ] EvalReport includes spec_hash (SHA-256), verdict (pass|conditional_pass|fail), blocked_layers, conditions, confidence_level, model_breakdown, recommendations
- [ ] ABComparison captures per-dimension p-values, effect sizes (Cohen's d), and tier-specific verdict
- [ ] All dataclasses support to_dict/from_dict for JSONL round-trip serialization

**Dependencies**: `pipeline/models.py` (PipelineConfig base class)

### FR-EVAL.2: Five-Dimension Scoring Rubric

**Description**: Define anchored scoring rubric with 5 dimensions: structure, completeness, accuracy, actionability, efficiency. Each dimension has anchor definitions at scores 1, 3, 5, 7, and 10.

**Acceptance Criteria**:
- [ ] Rubric defines 5 dimensions with human-readable descriptions
- [ ] Each dimension has 5 anchored score definitions (1, 3, 5, 7, 10)
- [ ] `render_rubric_for_prompt()` produces text suitable for injection into judge agent prompts
- [ ] `validate_scores()` returns validation errors for out-of-range values or missing dimensions
- [ ] Dimensions are configurable via rubric_focus parameter (select subset for specific test types)

**Dependencies**: FR-EVAL.1

### FR-EVAL.3: Judge Agent Integration

**Description**: Invoke a Claude subprocess as a quality judge. Build structured prompts embedding the rubric, test output, and context. Parse semi-structured JSON responses into Score objects.

**Acceptance Criteria**:
- [ ] Judge model defaults to Opus, configurable via `--judge-model` CLI flag
- [ ] `build_judge_prompt()` produces a structured prompt with rubric, test output, and context
- [ ] `parse_judge_response()` extracts Score objects from judge output text, with lenient fallback for unparseable responses
- [ ] `run_judge()` invokes ClaudeProcess with output_format="text", max_turns=15, configurable timeout (default 300s)
- [ ] Judge scores each run independently (no cross-contamination between runs)

**Dependencies**: FR-EVAL.1, FR-EVAL.2, `pipeline/process.py` (ClaudeProcess)

### FR-EVAL.4: Multi-Run Parallel Execution Engine

**Description**: Execute eval tests across multiple runs, models, and variants. The runner invokes CLI pipelines (e.g., `superclaude roadmap run`) via subprocess for functional and quality layers, NOT pytest. Structural tests use file-system checks only.

**Acceptance Criteria**:
- [ ] `execute_eval_suite()` runs all tests across configured models and repetitions
- [ ] Functional/quality tests spawn CLI commands via subprocess (not pytest)
- [ ] Supports N runs per test (configurable via `--runs`, minimum 5)
- [ ] Supports parallel execution of runs within the same test
- [ ] Per-run output captured to isolated directories: `runs/<timestamp>/<layer>/<test-id>/run-N/`
- [ ] Timeout enforcement per individual run (configurable, default 300s)
- [ ] Fail-fast (default): structural/functional layer failures halt evaluation before quality layer
- [ ] Eval-mode (`--eval-mode`): all layers execute regardless of earlier failures. Each layer's pass/fail verdict is recorded independently. Layers that ran past a failed gate are annotated with `past_failed_gate: true` in their TestVerdict. Overall verdict reflects all failures (eval-mode does not suppress FAIL verdicts).
- [ ] Partial runs (N of M steps completed) produce RunResult with `steps_completed` and `steps_total` fields populated. Partial runs are included in aggregation for their completed steps; uncompleted steps produce no scores for that run.
- [ ] State persistence to `.eval-state.json` for resumability

**Dependencies**: FR-EVAL.1, FR-EVAL.6 (isolation)

### FR-EVAL.5: Statistical Aggregation

**Description**: Compute per-dimension statistics from multi-run results: mean, stddev, coefficient of variation, p-values (Welch's t-test), and effect size (Cohen's d). Support within-model consistency checks and cross-variant comparison.

**Acceptance Criteria**:
- [ ] `aggregate_scores()` computes per-dimension mean, stddev, min, max, CV across runs
- [ ] `compare_variants()` produces per-dimension p-values and Cohen's d between two variant groups
- [ ] `check_consistency()` verifies within-variant reproducibility (target CV < 0.15)
- [ ] `compute_verdict()` produces ternary verdict based on configurable thresholds:
  - PASS: all layers executed and passed thresholds
  - CONDITIONAL_PASS: all executed layers passed, but one or more layers were blocked from executing; `blocked_layers` and `conditions` populated
  - FAIL: one or more executed layers failed thresholds
- [ ] Handles edge cases: zero runs (error), single run (no variance), identical results (CV=0)
- [ ] Cross-model results reported as separate rows, never aggregated into single score
- [ ] Confidence level annotation: "directional" for 5-run, "robust" for 20+ runs
- [ ] `aggregate_scores()` includes partial runs for steps they completed. Per-step aggregation reports the number of contributing runs (which may be less than total runs when some runs did not reach that step).

**Dependencies**: FR-EVAL.1, stdlib `statistics`, optional `scipy.stats`

### FR-EVAL.6: Isolation Mechanism

**Description**: Enable or disable `.claude/` directories to create clean vs enhanced variants for A/B comparison. Three isolation configurations compose two implementation mechanisms.

Isolation configurations (what to compare):
- **Vanilla**: All `.claude/` disabled -- raw Claude vs enhanced
- **Baseline**: Global `.claude/` only (pre-change state via worktree on master)
- **Candidate**: Local `.claude/` (current branch state)

Isolation mechanisms (how to isolate):
- **Worktree isolation** (primary): Git worktree on target branch. Crash-safe, concurrent-safe.
- **Env-var override** (supplementary): Set `CLAUDE_COMMANDS_DIR`, `CLAUDE_SKILLS_DIR` to empty directories. Crash-safe, process-local.
- **Directory rename** (fallback only): Rename `.claude/` with trap-safe restore via atexit + signal handlers. Used only if env-var overrides are insufficient.

Resolution of CONT-01 (three taxonomies): The spec distinguishes "configurations" (what) from "mechanisms" (how). Configurations are user-facing (`--variant vanilla|baseline|candidate`). Mechanisms are implementation details selected automatically based on configuration.

**Acceptance Criteria**:
- [ ] Worktree isolation: `setup_worktree(branch, base_dir) -> Path` creates or reuses git worktrees
- [ ] Worktree teardown: `teardown_worktree(path)` removes worktree cleanly
- [ ] Env-var isolation: returns dict of environment overrides for subprocess.Popen
- [ ] Directory rename fallback: trap-safe restore via atexit + signal.signal (SIGINT, SIGTERM)
- [ ] Concurrent access guard: file-based lock (`~/.superclaude-eval.lock`) prevents simultaneous .claude/ manipulation
- [ ] `--dry-run` validates isolation setup without executing any runs (AC-AB-08)
- [ ] Stale `.claude.disabled` detection: auto-restore at startup if found
- [ ] `--parallel` flag opts into worktree-based isolation for local runs too

**Dependencies**: pathlib, shutil, signal, atexit, fcntl

### FR-EVAL.7: Report Generation

**Description**: Produce human-readable `report.md` (YAML frontmatter + markdown body) and machine-readable `scores.jsonl` (one JSON line per run). Follow the `AggregatedPhaseReport.to_markdown()` pattern from sprint/executor.py.

**Acceptance Criteria**:
- [ ] `generate_report()` writes report.md with YAML frontmatter (release, timestamp, verdict: pass|conditional_pass|fail, confidence_level, blocked_layers, conditions) and markdown body
- [ ] When verdict is conditional_pass, report body includes "Conditions for Full Pass" section listing each condition with actionable remediation
- [ ] Report body includes: per-test verdict table, per-dimension score table, model breakdown, variance annotations, recommendations
- [ ] `write_scores_jsonl()` writes one JSON line per run with all scores and metadata
- [ ] Per-model breakdown table rendered with labeled "informational, not statistical" cross-model section
- [ ] Summary.json written with aggregate stats for programmatic consumption

**Dependencies**: FR-EVAL.1, FR-EVAL.5

### FR-EVAL.8: Spec Parser (release-eval)

**Description**: Extract acceptance criteria (ACs), functional requirements (FRs), and non-functional requirements (NFRs) from a release spec markdown file. Supports both feature and bug fix release types.

Resolution of CONT-02: This module was missing from Agent 3's infrastructure gap table. It is added as G-14 in the build order, required at P0 for slices 5-6.

**Acceptance Criteria**:
- [ ] Parses YAML frontmatter to extract spec_type, feature_id, complexity_class
- [ ] Extracts numbered FR sections with their acceptance criteria checkboxes
- [ ] Extracts NFR table entries with IDs, descriptions, targets, and measurements
- [ ] Detects release type (feature vs bug fix) from frontmatter or content heuristics
- [ ] Returns structured `ParsedSpec` dataclass with all extracted elements
- [ ] Handles malformed specs gracefully: returns partial results with warnings, never crashes

**Dependencies**: FR-EVAL.1, regex, YAML parser

### FR-EVAL.9: Eval Suite Generator (release-eval)

**Description**: Produce `eval-suite.yaml` from a parsed spec with tests across all 4 layers (structural, functional, quality, regression). Auto-generate fixtures appropriate to release type.

Resolution of CONT-02: This module was missing from Agent 3's infrastructure gap table. It is added as G-15 in the build order, required at P0 for slices 5-6.

**Acceptance Criteria**:
- [ ] Generates structural tests: file presence checks for all spec-referenced artifacts
- [ ] Generates functional tests: CLI execution with happy-path, empty-input, malformed, large-input fixtures
- [ ] Generates quality tests: LLM judge evaluations with rubric_focus derived from spec FRs
- [ ] Generates regression tests: before/after comparison for spec-claimed improvements
- [ ] Auto-generates fixture files: happy-path.md, empty-input.md, malformed.md, large-input.md, bug-repro.md (for patch releases)
- [ ] Output includes spec_hash (SHA-256) for version-lock validation (D-02)
- [ ] Suite includes `version` field (semver) for schema evolution
- [ ] Eval suite generation completes in < 60 seconds (NFR-01)
- [ ] Adapts test types based on release type (feature vs bug fix per Section 2.1 release type table)

**Dependencies**: FR-EVAL.8, FR-EVAL.1

### FR-EVAL.10: A/B Test Regression Tier

**Description**: Compare baseline (global/.claude state) vs candidate (local/.claude state) for a given command. N runs each, per-dimension statistical comparison. Detects whether a change regressed command quality.

**Acceptance Criteria**:
- [ ] Runs configurable N executions (minimum 5, default 5) per variant
- [ ] Baseline variant uses worktree on master branch; candidate uses current branch
- [ ] Per-dimension scores computed via judge agent for each run
- [ ] Regression acceptance: candidate must not score significantly lower than baseline on any dimension (p < 0.05)
- [ ] Produces scores.jsonl with per-dimension scores per run
- [ ] Produces summary.md with aggregate scores, variance, statistical comparison

**Dependencies**: FR-EVAL.3, FR-EVAL.4, FR-EVAL.5, FR-EVAL.6, FR-EVAL.7

### FR-EVAL.11: A/B Test Value Validation Tier

**Description**: Compare vanilla (plain prompt) vs baseline vs candidate for a given command. Measures whether the command adds value over a fair plain-language equivalent.

**Acceptance Criteria**:
- [ ] Three-way comparison: vanilla, baseline, candidate
- [ ] Vanilla prompts loaded from YAML library (`tests/ab/vanilla-prompts.yml`)
- [ ] Each vanilla prompt describes the GOAL not the METHOD
- [ ] Minimum 10 runs per variant for value validation (D-01 resolution)
- [ ] Value acceptance: command must outperform vanilla on >= 3 of 5 dimensions
- [ ] Reports confidence level: "directional" (5-10 runs) vs "robust" (20+ runs)

**Dependencies**: FR-EVAL.10

### FR-EVAL.12: A/B Test Deprecation Audit Tier

**Description**: Compare vanilla vs current command to identify commands that should be retired. Commands failing to beat vanilla on >= 2 dimensions are flagged for rework.

**Acceptance Criteria**:
- [ ] Vanilla vs current comparison with minimum 5 runs per variant
- [ ] Deprecation flag: commands scoring below vanilla on >= 2 dimensions marked for rework
- [ ] Report includes specific dimensions where command underperforms
- [ ] Does not auto-deprecate -- produces recommendation only

**Dependencies**: FR-EVAL.11

### FR-EVAL.13: Release Eval Executor

**Description**: Execute a generated eval suite against a release directory. Layers run in order with fail-fast. Human review pause between suite generation and execution.

Resolution of GAP-02 (human review pause): The CLI implements a two-step workflow. `superclaude release-eval generate <release-dir>` produces the eval suite and prints it. `superclaude release-eval run <release-dir>` executes it. The `--approve` flag on `run` skips the confirmation prompt for automation. Without `--approve`, the CLI prints the suite and asks for stdin confirmation before proceeding.

**Acceptance Criteria**:
- [ ] Layers execute in strict order: structural -> functional -> quality -> regression
- [ ] Structural failure halts before functional tests run (fail-fast) — unless `--eval-mode` is active
- [ ] Functional failure halts before quality tests run (fail-fast) — unless `--eval-mode` is active
- [ ] In eval-mode: failures are recorded in TestVerdict but execution continues to the next layer. Downstream layers annotated with `past_failed_gate: true`.
- [ ] A run that completes N of M pipeline steps due to an internal gate failure is classified as PARTIAL (not FAILED). PARTIAL runs contribute scores for completed steps. The fail-fast behavior applies across eval layers, not within pipeline-internal steps of a single layer.
- [ ] Quality and regression layers are scored, not hard-gated (configurable threshold)
- [ ] Overall verdict uses ternary model:
  - PASS: all structural/functional layers pass AND quality above thresholds AND all layers executed
  - CONDITIONAL_PASS: all executed structural/functional layers pass AND quality above thresholds AND one or more layers were blocked from executing
  - FAIL: any executed structural/functional layer fails OR quality below thresholds
- [ ] Two-step workflow: generate then execute, with `--approve` for automation
- [ ] Works on both feature releases and bug fix releases
- [ ] Can re-run evals on already-completed releases (retroactive)
- [ ] Read-only: never modifies release artifacts
- [ ] Validates spec_hash before execution; requires `--force` for stale suite

**Dependencies**: FR-EVAL.4, FR-EVAL.8, FR-EVAL.9

### FR-EVAL.14: Asymmetric Stage Handling

**Description**: When comparing branches with different pipeline stages (e.g., v3.0 has spec-fidelity, wiring-verification, remediate, certify stages that master lacks), the aggregator must handle missing baseline stages gracefully.

Resolution of GAP-06: Stages that exist on only one branch are scored as "not available" on the other branch, not as "failed." Delta computation accounts for this structural asymmetry. Reports include a "new capability" section for stages with no baseline comparison.

**Acceptance Criteria**:
- [ ] Missing stages produce "not available" status, not "failed"
- [ ] Delta computation excludes missing-baseline stages from regression calculations
- [ ] Report includes "new capability" section listing stages with no baseline
- [ ] No crash or misleading output when branches have different stage counts

**Dependencies**: FR-EVAL.5, FR-EVAL.7

### FR-EVAL.15: Cost Model Tracking

**Description**: Track and report estimated token consumption per tier and per run. Tokens are tracked via RunResult.tokens_used field, populated from subprocess output.

**Acceptance Criteria**:
- [ ] RunResult.tokens_used populated from subprocess metadata where available
- [ ] Report includes per-tier token estimates (30-80K regression, 50-150K value validation)
- [ ] Token counts are informational, not gating (no budget guardrails -- model selection controls cost)

**Dependencies**: FR-EVAL.1, FR-EVAL.7

## 4. Architecture

### 4.1 New Files

| File | Purpose | Dependencies |
|------|---------|-------------|
| `src/superclaude/eval/__init__.py` | Package init, public API exports | None |
| `src/superclaude/eval/models.py` | Score, RunResult, TestVerdict, EvalReport, ABComparison, EvalConfig, ParsedSpec dataclasses | `pipeline/models.py` |
| `src/superclaude/eval/rubric.py` | 5-dimension scoring rubric with anchored definitions, prompt rendering | `eval/models.py` |
| `src/superclaude/eval/judge.py` | Judge agent prompt construction, ClaudeProcess invocation, response parsing | `eval/models.py`, `eval/rubric.py`, `pipeline/process.py` |
| `src/superclaude/eval/runner.py` | Multi-run parallel execution engine, CLI subprocess invocation, worktree management | `eval/models.py`, `eval/isolation.py` |
| `src/superclaude/eval/isolation.py` | Worktree + env-var + directory-rename isolation with trap-safe restore | pathlib, shutil, signal, atexit, fcntl |
| `src/superclaude/eval/aggregator.py` | Statistical aggregation: mean, stddev, p-values, Cohen's d, consistency checks | `eval/models.py`, statistics, scipy.stats (optional) |
| `src/superclaude/eval/reporter.py` | report.md + scores.jsonl + summary.json generation | `eval/models.py`, `eval/aggregator.py` |
| `src/superclaude/eval/spec_parser.py` | Extract ACs, FRs, NFRs from release spec markdown | `eval/models.py`, regex |
| `src/superclaude/eval/suite_generator.py` | Generate eval-suite.yaml from parsed spec | `eval/models.py`, `eval/spec_parser.py` |
| `src/superclaude/cli/ab_test/__init__.py` | Click command group for ab-test | click |
| `src/superclaude/cli/ab_test/commands.py` | Click CLI: run, compare subcommands | `eval/*` |
| `src/superclaude/cli/ab_test/executor.py` | Tier orchestration (regression, value, deprecation) | `eval/runner.py`, `eval/isolation.py` |
| `src/superclaude/cli/ab_test/prompts.py` | Vanilla-equivalent prompt loader (reads YAML) | YAML |
| `src/superclaude/cli/release_eval/__init__.py` | Click command group for release-eval | click |
| `src/superclaude/cli/release_eval/commands.py` | Click CLI: generate, run, report subcommands | `eval/*` |
| `src/superclaude/cli/release_eval/executor.py` | 4-layer fail-fast execution orchestration | `eval/runner.py`, `eval/spec_parser.py` |
| `src/superclaude/pipeline/state.py` | Extracted `write_state()`/`read_state()` from roadmap/executor.py | json, pathlib, os |
| `tests/ab/vanilla-prompts.yml` | Vanilla-equivalent prompt library (YAML) | None |

### 4.2 Modified Files

| File | Change | Rationale |
|------|--------|-----------|
| `src/superclaude/cli/main.py` | Add `ab_test_group` and `release_eval_group` via `add_command()` | CLI registration for new commands |
| `src/superclaude/cli/roadmap/executor.py` | Replace `write_state()`/`read_state()` with imports from `pipeline/state.py` | Extract shared utility (6 call sites updated to new import path) |
| `pyproject.toml` | Add optional `scipy` dependency; add `eval` extra | Optional statistical testing dependency |

### 4.4 Module Dependency Graph

```
pipeline/models.py (PipelineConfig, StepStatus, GateCriteria, SemanticCheck)
pipeline/process.py (ClaudeProcess)
pipeline/gates.py (gate_passed)
pipeline/state.py (write_state, read_state)  <-- extracted from roadmap/executor.py
       |
       v
eval/models.py  <---+--- eval/rubric.py
       |             |
       v             v
eval/isolation.py   eval/judge.py (uses ClaudeProcess)
       |
       v
eval/runner.py  ---> eval/aggregator.py ---> eval/reporter.py

eval/spec_parser.py ---> eval/suite_generator.py
       |
       v
cli/ab_test/commands.py      cli/release_eval/commands.py
cli/ab_test/executor.py      cli/release_eval/executor.py
cli/ab_test/prompts.py
       |                            |
       +------- cli/main.py --------+
```

### 4.5 Data Models

```python
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
from typing import Any


@dataclass
class Score:
    """A single dimension score from a judge evaluation."""
    dimension: str          # structure|completeness|accuracy|actionability|efficiency
    value: float            # 1.0 - 10.0
    hard_fail: bool         # True = binary pass/fail (structural/functional layers)
    reasoning: str          # Judge's explanation

    def to_dict(self) -> dict:
        return {
            "dimension": self.dimension,
            "value": self.value,
            "hard_fail": self.hard_fail,
            "reasoning": self.reasoning,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Score":
        return cls(**d)


@dataclass
class RunResult:
    """Captures a single execution of an eval test."""
    test_id: str
    run_number: int
    model: str
    scores: list[Score]
    exit_code: int
    tokens_used: int
    wall_time_seconds: float
    artifacts: list[str]        # file paths produced
    stdout_path: Path           # path to stdout capture (not inline, avoids memory bloat)
    stderr_path: Path           # path to stderr capture
    steps_completed: int = 0    # number of pipeline steps that completed
    steps_total: int = 0        # total pipeline steps defined

    @property
    def completion_ratio(self) -> float:
        """Fraction of pipeline steps completed (0.0-1.0)."""
        return self.steps_completed / self.steps_total if self.steps_total > 0 else 0.0

    def to_dict(self) -> dict:
        return {
            "test_id": self.test_id,
            "run_number": self.run_number,
            "model": self.model,
            "scores": [s.to_dict() for s in self.scores],
            "exit_code": self.exit_code,
            "tokens_used": self.tokens_used,
            "wall_time_seconds": self.wall_time_seconds,
            "artifacts": self.artifacts,
            "stdout_path": str(self.stdout_path),
            "stderr_path": str(self.stderr_path),
            "steps_completed": self.steps_completed,
            "steps_total": self.steps_total,
        }


@dataclass
class TestVerdict:
    """Aggregated result for a single test across all runs."""
    test_id: str
    layer: str              # structural|functional|quality|regression
    passed: bool
    aggregate_scores: dict[str, dict[str, float]]
    # dimension -> {mean, stddev, min, max, cv}
    runs: list[RunResult]
    past_failed_gate: bool = False  # True when this layer ran after a prior layer failed (eval-mode only)


@dataclass
class EvalReport:
    """Full evaluation report for a release or A/B test."""
    release: str
    timestamp: str
    spec_hash: str              # SHA-256 of source spec (D-02)
    tests: list[TestVerdict]
    verdict: str                # "pass" | "conditional_pass" | "fail"
    blocked_layers: list[str] = field(default_factory=list)
                                # layers that could not execute (empty for pass/fail)
    conditions: list[str] = field(default_factory=list)
                                # upgrade requirements for conditional_pass → pass
    model_breakdown: dict[str, dict[str, float]]
    # model -> {dimension -> mean_score}
    recommendations: list[str]
    confidence_level: str       # "directional" (5-run) or "robust" (20-run) (D-01)


@dataclass
class ABComparison:
    """Result of an A/B tier comparison."""
    tier: str               # regression|value_validation|deprecation
    command: str
    baseline_scores: dict[str, dict[str, float]]
    # dimension -> {mean, stddev}
    candidate_scores: dict[str, dict[str, float]]
    # dimension -> {mean, stddev}
    p_values: dict[str, float]          # dimension -> p-value
    effect_sizes: dict[str, float]      # dimension -> Cohen's d
    verdict: str            # improved|regressed|neutral
    runs_per_variant: int


@dataclass
class EvalConfig:
    """Configuration for an eval run.

    Note: EvalConfig mirrors relevant PipelineConfig fields (work_dir,
    dry_run, max_turns, debug) but does NOT inherit from PipelineConfig.
    PipelineConfig includes fields irrelevant to eval (permission_flag,
    grace_period) and eval adds many domain-specific fields (judge_model,
    runs_per_test, isolation config). Composition-by-selection is used
    instead of inheritance to avoid carrying unused baggage.
    """
    work_dir: Path
    output_dir: Path
    eval_suite_path: Path | None = None
    release_dir: Path | None = None
    runs_per_test: int = 5
    models: list[str] = field(default_factory=lambda: ["claude-sonnet-4-6"])
    judge_model: str = "claude-opus-4-6"
    timeout_per_run: int = 300
    fail_fast: bool = True
    dry_run: bool = False
    debug: bool = False
    max_turns: int = 100
    force: bool = False             # run with stale spec_hash
    approve: bool = False           # skip human review prompt
    parallel: bool = False          # worktree isolation for local runs too
    eval_mode: bool = False         # when True, gate failures are recorded but do not halt execution


@dataclass
class ParsedSpec:
    """Structured extraction from a release spec markdown file."""
    title: str
    spec_type: str                  # new_feature|refactoring|portification|infrastructure
    feature_id: str
    complexity_class: str
    functional_requirements: list[dict[str, Any]]
    # [{id, title, description, acceptance_criteria: [str], dependencies: [str]}]
    non_functional_requirements: list[dict[str, Any]]
    # [{id, description, target, measurement}]
    release_type: str               # feature|bugfix
    spec_hash: str                  # SHA-256 of source file
    warnings: list[str]             # parsing warnings for malformed sections


@dataclass
class RubricDimension:
    """A single dimension in the scoring rubric."""
    name: str                       # e.g., "completeness"
    description: str                # what this dimension measures
    anchors: dict[int, str]         # score -> description (1, 3, 5, 7, 10)
    weight: float = 1.0             # relative importance


@dataclass
class EvalSuiteTest:
    """A single test definition within an eval suite."""
    id: str
    layer: str                      # structural|functional|quality|regression
    name: str
    test_type: str                  # file_presence|cli_execution|llm_judge|ab_comparison
    config: dict[str, Any]          # type-specific configuration


@dataclass
class EvalSuite:
    """Complete eval suite generated from a spec."""
    release: str
    release_type: str
    spec_path: str
    spec_hash: str
    version: str                    # semver for schema evolution
    generated_by: str
    tests: list[EvalSuiteTest]
```

### 4.6 Implementation Order

```
Phase 1 -- Foundations (no dependencies, parallelizable):
  1a. Extract write_state/read_state to pipeline/state.py       [S, G-09]
  1b. eval/__init__.py package init                              [S, G-01]
  1c. eval/models.py data model definitions                      [M, G-02]
  1d. eval/rubric.py scoring rubric                              [S, G-03]

Phase 2 -- Core modules (depends on Phase 1, partially parallelizable):
  2a. eval/isolation.py worktree + env-var + fallback            [M, G-05]
  2b. eval/aggregator.py statistical computation                 [M, G-07]
  2c. eval/judge.py judge agent integration                      [M, G-06]
      -- [2a, 2b, 2c parallel]

Phase 3 -- Execution engine (depends on Phase 2):
  3a. eval/runner.py multi-run parallel execution                [C, G-04]

Phase 4 -- Reporting + release-eval modules (depends on Phase 3, parallelizable):
  4a. eval/reporter.py report generation                         [M, G-08]
  4b. eval/spec_parser.py spec extraction                        [M, G-14]
  4c. eval/suite_generator.py eval suite creation                [M, G-15]
      -- [4a, 4b, 4c parallel]

Phase 5 -- CLI commands (depends on Phase 4):
  5a. cli/ab_test/ command group + executor + prompts            [M, G-10]
  5b. cli/release_eval/ command group + executor                 [M, G-10]
  5c. CLI registration in main.py                                [S, G-11]
      -- [5a, 5b parallel; 5c after both]

Phase 6 -- Integration + polish:
  6a. Eval gate criteria instances                               [S, G-12]
  6b. Vanilla prompt library initial set                         [S]
  6c. Refactor scripts/eval_runner.py references                 [M, G-13]

Critical path: 1c -> 2a -> 3a -> 5a -> 5c (5 steps across 5 phases)
Total: 5 Simple + 8 Medium + 1 Complex = 14 work items

Note: Phases 1-2 are internal milestones (not user-testable). Phase 5a
(ab-test CLI) is the first user-testable release (v1.0-alpha). This
resolves D-06: scoring library ships bundled with ab-test, not separately.
```

## 5. Interface Contracts

### 5.1 CLI Surface

**superclaude ab-test**

```
superclaude ab-test run <command> [OPTIONS]
superclaude ab-test compare <results-dir-a> <results-dir-b> [OPTIONS]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `command` | ARGUMENT | (required) | The command to test (e.g., `sc:roadmap`, `sc:explain`) |
| `--tier` | Choice | `regression` | Test tier: `regression`, `value`, `deprecation` |
| `--runs` | INT | 5 (regression/deprecation), 10 (value) | Number of runs per variant. Minimum enforced per tier. |
| `--models` | TEXT | `claude-sonnet-4-6` | Comma-separated list of runner models |
| `--judge-model` | TEXT | `claude-opus-4-6` | Model for quality scoring |
| `--output` | PATH | `.` | Output directory (results written to `<output>/ab-tests/<command>/<timestamp>/`) |
| `--args` | TEXT | `""` | Arguments to pass to the command under test |
| `--input` | PATH | None | Input file for the command under test |
| `--dry-run` | FLAG | False | Validate isolation setup without executing runs |
| `--parallel` | FLAG | False | Use worktree isolation for local runs (enables concurrent execution) |
| `--debug` | FLAG | False | Verbose output and debug logging |
| `--eval-mode` | FLAG | False | Record gate failures but continue execution past failed gates. Overall verdict still reflects failures. Use for comprehensive coverage measurement. |

**superclaude release-eval**

```
superclaude release-eval generate <release-dir> [OPTIONS]
superclaude release-eval run <release-dir> [OPTIONS]
superclaude release-eval report <results-dir> [OPTIONS]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `release-dir` | ARGUMENT | (required) | Path to the release directory containing the spec |
| `--runs` | INT | 5 | Number of runs per quality/regression test |
| `--models` | TEXT | `claude-sonnet-4-6` | Comma-separated list of runner models |
| `--judge-model` | TEXT | `claude-opus-4-6` | Model for quality scoring |
| `--layers` | Choice | `all` | Layers to execute: `all`, `structural`, `functional`, `quality`, `regression` |
| `--approve` | FLAG | False | Skip human review confirmation (for automation) |
| `--force` | FLAG | False | Run with stale spec_hash (overrides version-lock) |
| `--regenerate` | FLAG | False | Regenerate eval suite even if one exists |
| `--dry-run` | FLAG | False | Print execution plan without running |
| `--debug` | FLAG | False | Verbose output and debug logging |
| `--timeout` | INT | 300 | Timeout per individual run in seconds |
| `--eval-mode` | FLAG | False | Record gate failures but continue execution past failed gates. Overall verdict still reflects failures. Use for comprehensive coverage measurement. |

### 5.2 Gate Criteria

Eval layers map to the existing gate framework from `pipeline/models.py`:

| Layer | Gate Tier | Enforcement | Semantic Checks |
|-------|-----------|-------------|-----------------|
| Structural (L1) | STRICT | BLOCKING (hard fail) | `_file_exists()`, `_frontmatter_valid()`, `_schema_conforms()` |
| Functional (L2) | STRICT | BLOCKING (hard fail) | `_exit_code_zero()`, `_artifacts_produced()` |
| Quality (L3) | STANDARD | Scored (configurable threshold) | `_score_above_threshold(dimension, min_score)` |
| Regression (L4) | STANDARD | Scored (configurable threshold) | `_regression_significant(p_threshold=0.05)` |

**Note on GateCriteria compatibility**: The existing `GateCriteria` dataclass in `pipeline/models.py` uses `required_frontmatter_fields`, `min_lines`, and `SemanticCheck` functions — designed for markdown artifact validation. Eval layers need different gate semantics: score thresholds, p-value thresholds, and file-existence checks. A new `EvalGateCriteria` dataclass should be defined in `eval/models.py` that shares the `enforcement_tier` and `SemanticCheck` concepts but replaces frontmatter/line-count fields with eval-specific criteria (threshold values, layer type). This coexists with `GateCriteria` rather than extending it.

### 5.3 Eval Suite YAML Schema

Resolution of GAP-03 (formal schema specification):

```yaml
# eval-suite.yaml schema
release: string          # release name (required)
release_type: string     # "feature" | "bugfix" (required)
spec_path: string        # path to source spec (required)
spec_hash: string        # SHA-256 of source spec (required, for version-lock D-02)
version: string          # suite schema version, semver (required)
generated_by: string     # model that generated the suite (required)
generated_at: string     # ISO-8601 timestamp (required)

tests:                   # list of test definitions (required, non-empty)
  - id: string           # unique test ID, format: "<layer>-NNN" (required)
    layer: string        # "structural" | "functional" | "quality" | "regression" (required)
    name: string         # human-readable test name (required)
    type: string         # "file_presence" | "cli_execution" | "llm_judge" | "ab_comparison" (required)

    # Type-specific fields (varies by type):
    # file_presence:
    expected_files: list[string]    # file paths to check

    # cli_execution:
    command: string                 # CLI command to execute
    input: string                   # path to input fixture
    success_criteria:
      exit_code: int                # expected exit code (usually 0)
      artifacts_produced: list[string]  # expected output files

    # llm_judge:
    runs: int                       # number of runs (default: from config)
    models: list[string]            # models to test (default: from config)
    rubric_focus: list[string]      # subset of rubric dimensions
    min_scores: dict[string, float] # dimension -> minimum acceptable score

    # ab_comparison:
    baseline: string                # baseline variant description
    candidate: string               # candidate variant description
    runs: int                       # runs per variant
```

### 5.4 Vanilla Prompt YAML Schema

Resolution of GAP-05 (vanilla prompt format):

```yaml
# tests/ab/vanilla-prompts.yml
version: "1.0"

prompts:
  sc:roadmap:
    goal: "Generate a phased implementation roadmap for this specification"
    input_description: "A release specification markdown file"
    prompt: |
      Read this specification and create a detailed implementation roadmap.
      Break it into phases with dependencies, deliverables, and test criteria.
      Output as a structured markdown document.

  sc:explain:
    goal: "Explain what this code does"
    input_description: "A source code file"
    prompt: |
      Read this source code file and explain what it does.
      Include: purpose, key functions, data flow, and notable patterns.

  sc:tasklist:
    goal: "Break a roadmap into implementable tasks"
    input_description: "A roadmap markdown file"
    prompt: |
      Read this roadmap and break each phase into specific implementation tasks.
      Each task should be independently completable with clear acceptance criteria.
```

## 6. Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-EVAL.1 | Eval suite generation speed | < 60 seconds | Wall-clock time for `superclaude release-eval generate` |
| NFR-EVAL.2 | Token budget per test layer | Structural < 500, Functional < 5K, Quality < 20K per run | Token count from RunResult.tokens_used |
| NFR-EVAL.3 | Within-model variance | Coefficient of variation < 0.15 | CV computed by aggregator.py |
| NFR-EVAL.4 | Retroactive compatibility | Must work on 10+ completed releases | Boolean: successful eval of test corpus |
| NFR-EVAL.5 | Read-only operation | Never modifies release artifacts | Boolean: release dir unmodified after eval |
| NFR-EVAL.6 | Results directory convention | evals/ within release dir for release-eval; ab-tests/ within output dir for ab-test | Path structure verification |
| NFR-EVAL.7 | Isolation safety | Trap handler guarantees .claude/ restoration on exit/error/SIGINT | Boolean: .claude/ state correct after interrupted eval |
| NFR-EVAL.8 | Cost efficiency | Eval runners default to cheaper models; Opus for judge only | Model selection in defaults |
| NFR-EVAL.9 | Artifact provenance | Output directory created fresh; timestamps verified post-eval | Timestamp validation |
| NFR-EVAL.10 | Third-party verifiability | All eval output inspectable by absent third party | Persistent disk artifacts with structured data |
| NFR-EVAL.11 | No mocks in eval execution | grep for mock/Mock/MagicMock/patch/monkeypatch/stub/simulate yields 0 | grep check on eval source |
| NFR-EVAL.12 | Minimum runs for statistical validity | >= 5 per variant for all tiers | Run count enforcement |
| NFR-EVAL.13 | Statistical significance threshold | p < 0.05 for regression decisions | p-value computation by aggregator |
| NFR-EVAL.14 | Per-run execution time | Individual command-under-test run < 15 minutes (wall-clock per single run, not total eval time; total scales as runs × models) | Wall-clock per individual run |
| NFR-EVAL.15 | Concurrent safety | Lock file prevents simultaneous .claude/ manipulation | File lock verification |

## 7. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| LLM variance makes quality scores unreliable | High | Medium | Multi-run aggregation (minimum 5 runs); CV < 0.15 target; confidence level reporting ("directional" vs "robust"); within-model only comparisons |
| Token cost of multi-run quality evals | Medium | Medium | Default to cheaper models (Sonnet, Haiku) for runners; Opus only for judge; no budget guardrails -- model selection controls cost; report estimated tokens per tier |
| Isolation failure corrupts .claude/ directory | Low | High | Primary mechanism is worktree isolation (no filesystem mutation); env-var fallback is process-local; directory rename only as last resort with trap-safe restore (atexit + signal handlers + stale detection at startup); `--dry-run` validates isolation before execution |
| Worktree cleanup failure leaks disk space | Medium | Low | Explicit teardown in finally block; worktree registry in .eval-state.json; manual cleanup command (`superclaude release-eval cleanup`); worktree names include `-eval-` prefix for easy identification |
| Judge agent produces unparseable output | Medium | Low | Lenient JSON parsing with regex fallback; unparseable responses produce value=0.0 with reasoning="Judge output unparseable"; quality layer is scored (advisory), not hard-gated |
| Concurrent eval runs conflict | Low | Medium | File-based lock (`~/.superclaude-eval.lock`) prevents concurrent .claude/ manipulation; worktree isolation for parallel runs via `--parallel` flag; clear error message if lock acquired |
| Stale eval suite produces misleading results | Medium | Medium | spec_hash validation at execution time; `--force` required to run stale suite; `--regenerate` to create fresh suite; archived old suites to `evals/archive/<timestamp>/` |
| Asymmetric branch comparison (different stage counts) | Medium | Medium | Missing stages scored as "not available" not "failed"; delta computation excludes missing-baseline stages; "new capability" section in report |
| Vanilla prompts bias A/B results | Medium | High | Hand-crafted prompts with peer review requirement; prompts describe GOAL not METHOD; new commands must include vanilla-equivalent as deliverable; PRs modifying prompts require separate reviewer |
| Multi-run parallel execution resource exhaustion | Low | Medium | Configurable parallelism (not unbounded); default sequential within variant; `--parallel` opt-in for worktree-based concurrency; timeout per run prevents runaway processes |

## 8. Test Plan

### 8.1 Unit Tests

| Test | File | Validates |
|------|------|-----------|
| Score dataclass serialization | `tests/eval/test_models.py` | to_dict/from_dict round-trip for all dataclasses |
| Rubric dimension validation | `tests/eval/test_rubric.py` | Anchor definitions cover all 5 dimensions; validate_scores catches errors |
| Rubric prompt rendering | `tests/eval/test_rubric.py` | render_rubric_for_prompt produces non-empty, structured text |
| Judge prompt construction | `tests/eval/test_judge.py` | build_judge_prompt includes rubric, output, and context |
| Judge response parsing | `tests/eval/test_judge.py` | parse_judge_response extracts scores from JSON; fallback for malformed |
| Aggregation statistics | `tests/eval/test_aggregator.py` | mean, stddev, CV computation; edge cases (0 runs, 1 run, identical) |
| P-value computation | `tests/eval/test_aggregator.py` | Welch's t-test produces correct p-values for known distributions |
| Cohen's d effect size | `tests/eval/test_aggregator.py` | Effect size computation for known data |
| Consistency check | `tests/eval/test_aggregator.py` | Within-variant identical pass/fail detection |
| Verdict computation | `tests/eval/test_aggregator.py` | PASS/FAIL logic for structural + quality thresholds |
| Report formatting | `tests/eval/test_reporter.py` | YAML frontmatter + markdown body structure |
| JSONL serialization | `tests/eval/test_reporter.py` | One JSON line per run, all fields present |
| Spec parser extraction | `tests/eval/test_spec_parser.py` | FRs, NFRs, ACs extracted from sample spec |
| Spec parser malformed input | `tests/eval/test_spec_parser.py` | Partial results with warnings, no crash |
| Suite generator output | `tests/eval/test_suite_generator.py` | eval-suite.yaml has tests across 4 layers |
| Suite generator fixtures | `tests/eval/test_suite_generator.py` | Fixture files generated per release type |
| Spec hash validation | `tests/eval/test_suite_generator.py` | spec_hash in suite matches source file |
| Isolation env-var override | `tests/eval/test_isolation.py` | Returns correct env dict for vanilla/baseline/candidate |
| Isolation lock file | `tests/eval/test_isolation.py` | Lock acquired/released correctly; concurrent attempt blocked |
| State read/write round-trip | `tests/pipeline/test_state.py` | Atomic write; read handles missing/empty/malformed |
| EvalConfig defaults | `tests/eval/test_models.py` | Default values for runs_per_test, models, judge_model, timeouts |
| Vanilla prompt YAML loading | `tests/ab/test_prompts.py` | YAML parses correctly; all commands have goal + prompt fields |
| ABComparison verdict logic | `tests/eval/test_aggregator.py` | improved/regressed/neutral based on p-values and effect sizes |

### 8.2 Integration Tests

| Test | Validates |
|------|-----------|
| Single-run judge integration | ClaudeProcess invokes judge model, response parsed into Scores |
| Multi-run execution with aggregation | 3 runs of a simple command, aggregate scores computed correctly |
| Worktree setup and teardown | Git worktree created on master, used for baseline run, cleaned up |
| Fail-fast layer ordering | Structural failure prevents functional execution; functional failure prevents quality |
| End-to-end ab-test regression tier | Full regression comparison produces scores.jsonl + summary.md |
| End-to-end release-eval generate | Spec parsed, eval-suite.yaml generated with correct structure |
| End-to-end release-eval run | Suite executed, all layers produce output, report.md generated |
| State persistence and resume | Eval interrupted mid-run, restarted, resumes from last state |
| Spec hash mismatch detection | Modified spec triggers warning; `--force` allows execution |
| Lock file contention | Two eval processes, second gets clear error message |
| Asymmetric comparison | v3.0 vs master comparison with missing stages handled as "not available" |

### 8.3 Manual / E2E Tests

| Scenario | Steps | Expected Outcome |
|----------|-------|-----------------|
| Retroactive eval on v2.25-cli-portify-cli | `superclaude release-eval run .dev/releases/complete/v2.25-cli-portify-cli/` | Suite generated with tests across 4 layers; structural and functional pass; quality scores produced; report.md readable |
| A/B regression on sc:roadmap | `superclaude ab-test run sc:roadmap --tier regression --runs 5` | 5 baseline + 5 candidate runs; per-dimension scores; verdict (improved/regressed/neutral) |
| Isolation safety under SIGINT | Start ab-test, Ctrl+C during execution | .claude/ directory restored to pre-eval state; no .claude.disabled leftover |
| Dry-run validation | `superclaude ab-test run sc:roadmap --dry-run` | Isolation validated; execution plan printed; no runs executed |
| Value validation tier | `superclaude ab-test run sc:explain --tier value --runs 10` | Vanilla + baseline + candidate runs; value acceptance computed; report includes confidence level |
| Bug fix release eval | `superclaude release-eval run .dev/releases/complete/v2.25.7-Phase8HaltFix/` | Bug-repro fixture generated; regression tests target fix area |

## 10. Downstream Inputs

### For sc:roadmap

This spec is designed to be consumed by `superclaude roadmap run` to generate implementation roadmaps. Key themes for roadmap generation:

- **Theme 1: Scoring Foundation** (Slices 1-2) -- Build the eval library: data models, rubric, judge agent, multi-run engine, aggregation, isolation, reporting. This is the shared infrastructure used by both commands.
- **Theme 2: A/B Testing** (Slices 3-4) -- Build the ab-test CLI: regression tier, value validation tier, deprecation audit tier, vanilla prompt library. Depends on Theme 1.
- **Theme 3: Release Evaluation** (Slices 5-6) -- Build the release-eval CLI: spec parser, suite generator, 4-layer executor, two-step generate/run workflow. Depends on Theme 1.
- **Theme 4: Integration** (Slice 7) -- CLI registration, gate criteria instances, prototype refactor, end-to-end validation against test corpus.

Milestones map to the 7-slice delivery plan in Section 4.6. Each slice is independently testable against completed releases from the test corpus.

### For sc:tasklist

Task breakdown guidance:
- Phase 1 tasks are parallelizable (4 items, no interdependencies)
- Phase 2 tasks are parallelizable (3 items, all depend on Phase 1 completion)
- Phase 3 is a single complex task (runner.py) that should be broken into sub-tasks: single-run engine, multi-run loop, worktree integration, state persistence, fail-fast logic
- Phase 4 tasks are parallelizable (3 items, depend on Phase 3)
- Phase 5 tasks are partially parallelizable (ab-test and release-eval commands in parallel, CLI registration after both)
- Each task should include specific test file references from Section 8.1

## 11. Open Items

All open decisions from the original conversation-decisions.md have been resolved in this spec:

| Item | Original Question | Resolution | Section |
|------|-------------------|------------|---------|
| D-01: Min runs | 5 vs 20 for statistical significance | Tiered: 5 regression, 10 value, 5 deprecation; `--runs` override | Section 2.1 |
| D-02: Suite versioning | Stale suite behavior | spec_hash validation + `--force` + `--regenerate` | FR-EVAL.9, Section 5.3 |
| D-03: Concurrent isolation | Queue vs worktree | File lock + worktree fallback + `--parallel` flag | FR-EVAL.6 |
| D-04: Score format | JSONL vs SQLite | JSONL primary, no SQLite in v1 | Section 2.1 |
| D-05: Vanilla prompts | Auto vs hand-crafted | Hand-crafted with peer review; YAML library | Section 2.1, Section 5.4 |
| D-06: Slice 1-2 target | Separate or bundled | Ship with slice 3 as first user-testable release | Section 4.6 |
| D-07: Eval runner relationship | New vs existing | Coexist as complementary layers (pytest unit eval + CLI integration eval) | Section 1.2 |
| D-08: Skill vs CLI phasing | Skill-first then portify | CLI-first; skill is thin wrapper built alongside | Section 2.1 |
| D-09: Cross-model normalization | Within-model vs cross-model | Within-model only; cross-model informational | Section 2.1 |
| D-10: Docker isolation | In scope vs deferred | Out of scope for v1 | Section 1.2 |

No remaining open items.

## 12. Brainstorm Gap Analysis

This spec was produced by a 4-agent synthesis process followed by adversarial consistency debate. The agents analyzed: architecture decisions and data model (Agent 1), pipeline stages and automation (Agent 2), infrastructure gaps and reuse analysis (Agent 3), and consolidated requirements with contradiction resolution (Agent 4).

The adversarial debate identified 9 contradictions and 6 gaps. All have been resolved in this spec:

| Gap ID | Description | Severity | Affected Section | Resolution |
|--------|-------------|----------|-----------------|------------|
| CONT-01 | Three different taxonomies for isolation (modes vs layers vs configurations) | WARNING | Section 4, FR-EVAL.6 | Spec distinguishes "configurations" (what: vanilla/baseline/candidate) from "mechanisms" (how: worktree/env-var/rename). Both defined explicitly. |
| CONT-02 | spec_parser.py and suite_generator.py missing from infrastructure gap table | BLOCKING | Section 4.1, FR-EVAL.8, FR-EVAL.9 | Added as G-14 and G-15 in build order. Full FR definitions provided. |
| CONT-03 | Skill-first vs CLI-first build approach conflict | WARNING | Section 2.1 | Adopted CLI-first approach. Original skill-first decision documented with rationale for override (6-prompt workflow proved CLI works; avoids portification tax). |
| CONT-04 | Runner architecture conflation (pytest vs CLI pipeline) | BLOCKING | FR-EVAL.4 | Runner invokes CLI pipelines via subprocess, NOT pytest. Existing scripts/eval_runner.py preserved as complementary unit eval tool. |
| CONT-05 | Human review pause mechanism undefined | WARNING | FR-EVAL.13 | Two-step workflow: `generate` then `run`. `--approve` flag for automation. Stdin confirmation without flag. |
| CONT-06 | Value validation minimum runs (5 vs 10) | WARNING | FR-EVAL.11, Section 2.1 | Adopted 10-run minimum for value validation. Deviation from original "5 each" documented with statistical rationale. |
| CONT-07 | Module count discrepancy (7 vs 13 gaps) | INFO | Section 4.1 | Not a contradiction: 7 library modules + 2 CLI packages + infrastructure = 14+ work items. Consistent when properly scoped. |
| CONT-08 | RunResult stdout/stderr type (str vs Path) | INFO | Section 4.5 | Adopted Path internally (avoids memory bloat); serialized as str in JSONL. |
| CONT-09 | ab-test output directory convention undefined | INFO | Section 5.1 | `<output-dir>/ab-tests/<command>/<timestamp>/` with `--output` defaulting to cwd. |
| GAP-01 | spec_parser.py and suite_generator.py missing | HIGH | Section 4.1, FR-EVAL.8, FR-EVAL.9 | Resolved via CONT-02. |
| GAP-02 | Human review pause mechanism | MEDIUM | FR-EVAL.13 | Resolved via CONT-05. |
| GAP-03 | Eval suite YAML schema unspecified | MEDIUM | Section 5.3 | Formal schema defined with required fields, types, and type-specific configs. |
| GAP-04 | Cost estimation module ownership | LOW | FR-EVAL.15 | Absorbed into reporter.py; tokens tracked via RunResult.tokens_used. |
| GAP-05 | Vanilla prompt YAML format undefined | LOW | Section 5.4 | Formal schema defined: command -> {goal, input_description, prompt}. |
| GAP-06 | Asymmetric stage handling for cross-branch comparison | MEDIUM | FR-EVAL.14 | Missing stages scored as "not available"; delta excludes them; "new capability" section in report. |

---

## Appendix A: Glossary

| Term | Definition |
|------|-----------|
| Baseline | The pre-change version of a command, typically running from the master branch via git worktree |
| Candidate | The post-change version of a command, running from the current working branch |
| Vanilla | A fair plain-language prompt equivalent to a command, with all SuperClaude skills/commands disabled |
| Tier | One of three A/B test types: regression (baseline vs candidate), value validation (vanilla vs baseline vs candidate), deprecation audit (vanilla vs current) |
| Layer | One of four evaluation levels: structural (file checks), functional (execution checks), quality (judge scoring), regression (statistical comparison) |
| Judge agent | A Claude subprocess (default Opus) that scores eval outputs against the rubric |
| Rubric | The 5-dimension scoring framework: structure, completeness, accuracy, actionability, efficiency |
| CV | Coefficient of variation (stddev / mean). Target < 0.15 for within-model consistency |
| Cohen's d | Effect size measure for comparing two groups. d > 0.8 = large effect, d ~ 0.5 = medium |
| Fail-fast | Execution strategy where failure in an earlier layer prevents later layers from running |
| Spec hash | SHA-256 hash of the source spec file, used to detect stale eval suites |
| Eval suite | A YAML file defining all tests to run against a release, generated from the spec |

## Appendix B: Reference Documents

| Document | Relevance |
|----------|-----------|
| `.dev/releases/backlog/v5.xx_release-eval-ab-test/conversation-decisions.md` | Original decision record and context brief |
| `.dev/releases/backlog/v5.xx_release-eval-ab-test/spec-synthesis/` | 4-agent analysis documents (architecture, workflow, infrastructure, requirements) |
| `.dev/releases/backlog/v5.xx_release-eval-ab-test/spec-synthesis/consistency-debate.md` | Adversarial debate identifying contradictions and gaps |
| `.dev/releases/backlog/v3.1-ab-testing/release-plan.md` | A/B testing backlog spec (incorporated into sc:ab-test design) |
| `src/superclaude/examples/release-spec-template.md` | Template this spec conforms to |
| `scripts/eval_runner.py` | Existing prototype covering ~40% of runner functionality |
| `scripts/ab_test_workflows.py` | Statistical comparison engine (t-test, effect size, winner determination) |
| `docs/memory/WORKFLOW_METRICS_SCHEMA.md` | JSONL format convention for workflow metrics |
| `.dev/releases/complete/` | Test corpus of 10+ completed releases for retroactive evaluation |
| `src/superclaude/cli/pipeline/models.py` | PipelineConfig, StepStatus, GateCriteria, SemanticCheck (reusable base types) |
| `src/superclaude/cli/pipeline/process.py` | ClaudeProcess subprocess management (used for judge agent) |
| `src/superclaude/cli/pipeline/gates.py` | gate_passed() validation framework (reusable for eval gates) |
| `src/superclaude/cli/roadmap/executor.py` | write_state/read_state (to be extracted to pipeline/state.py) |
| `src/superclaude/cli/sprint/executor.py` | IsolationLayers pattern (env-var isolation precedent) |

## Appendix C: Scoring Rubric Anchored Definitions

### Structure (weight: 1.0)

| Score | Definition |
|-------|-----------|
| 1 | No discernible structure. Output is a wall of text or random fragments. |
| 3 | Minimal structure. Has sections but no hierarchy, inconsistent formatting. |
| 5 | Adequate structure. Clear sections with headers, basic organization. Some formatting inconsistencies. |
| 7 | Good structure. Hierarchical headings, consistent formatting, logical flow between sections. |
| 10 | Excellent structure. Professional document structure with table of contents, cross-references, consistent formatting throughout. Immediately navigable by a third party. |

### Completeness (weight: 1.0)

| Score | Definition |
|-------|-----------|
| 1 | Covers less than 20% of requested scope. Major sections missing entirely. |
| 3 | Covers 20-50% of scope. Several required sections present but shallow or incomplete. |
| 5 | Covers 50-75% of scope. All major sections present. Some subsections missing or stub-level. |
| 7 | Covers 75-90% of scope. All sections present with substantive content. Minor gaps in edge cases or examples. |
| 10 | Covers 100% of scope. Every requirement addressed with detail. Edge cases, examples, and cross-references included. |

### Accuracy (weight: 1.0)

| Score | Definition |
|-------|-----------|
| 1 | Contains factual errors, references non-existent files/functions, or contradicts the spec. |
| 3 | Mostly inaccurate. Some correct references but significant errors in logic or file paths. |
| 5 | Mixed accuracy. Core facts correct but contains errors in details, parameters, or dependencies. |
| 7 | Mostly accurate. Correct file paths, function names, and dependencies. Minor errors in edge-case behavior. |
| 10 | Fully accurate. Every file path, function reference, parameter name, and dependency is correct and verifiable. |

### Actionability (weight: 1.0)

| Score | Definition |
|-------|-----------|
| 1 | Output cannot be used without complete rewrite. No clear next steps. |
| 3 | Provides general direction but lacks specificity. Developer would need significant research to act. |
| 5 | Provides actionable items but missing details (file paths, parameter values, concrete examples). |
| 7 | Clearly actionable. Specific files, functions, and values identified. Developer can begin implementation. |
| 10 | Immediately actionable. Every task has concrete steps, file paths, expected inputs/outputs, and test criteria. Copy-paste ready where appropriate. |

### Efficiency (weight: 1.0)

| Score | Definition |
|-------|-----------|
| 1 | Extremely verbose. Repeats information extensively. Output-to-value ratio very low. |
| 3 | Verbose. Significant repetition or padding. Key information buried in unnecessary text. |
| 5 | Adequate density. Some repetition but key information accessible. |
| 7 | Good density. Concise without sacrificing clarity. Minimal repetition. |
| 10 | Optimal density. Every sentence adds value. No repetition, no filler. Information density maximized. |

## Appendix D: Seven-Slice Delivery Plan

| Slice | Deliverable | Test Against | Release |
|-------|-------------|--------------|---------|
| 1 | Scoring library (models, rubric, judge) + single-run judge | Score one output from v2.25-cli-portify-cli manually | Internal milestone |
| 2 | Multi-run engine (runner, isolation, aggregator, reporter) | Run sc:tasklist 5x on v2.25 roadmap, score each | Internal milestone |
| 3 | sc:ab-test regression tier (CLI) | Modify a skill, verify before/after comparison | **v1.0-alpha** (first user-testable) |
| 4 | sc:ab-test value + deprecation tiers + vanilla prompts | Vanilla vs sc:explain on a file | **v1.0** (feature-complete ab-test) |
| 5 | Spec parser + eval-suite generator | Point at v2.25-cli-portify-cli, generate suite | Internal milestone |
| 6 | Release eval executor + two-step workflow | Execute generated suite, get full report | **v2.0-alpha** |
| 7 | CLI polish + gate criteria + test corpus validation | Full eval of 6 completed releases from test corpus | **v2.0** (feature-complete release-eval) |

**Slice dependency chain**: 1 -> 2 -> 3 -> 4 (v1.0 path) and 1 -> 2 -> 5 -> 6 -> 7 (v2.0 path). Slices 3-4 and 5-6 can proceed in parallel after slice 2.

**Critical principle**: Build smallest functional slice, eval it against real completed releases from day one. The testing system is tested by testing real releases.
