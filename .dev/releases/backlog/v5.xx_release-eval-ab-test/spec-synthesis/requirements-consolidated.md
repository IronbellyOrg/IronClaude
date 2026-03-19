# Consolidated Requirements: Eval CLI & A/B Testing System

**Date**: 2026-03-19
**Sources**:
- [S1] `conversation-decisions.md` — Decision record & context brief (2026-03-17)
- [S2] `6PromptV3-Eval.md` — 6-prompt v3.0 eval strategy (undated)
- [S3] `eval-prompts.md` — Refactored eval prompts v2.0 (2026-03-19)
- [S4] `release-plan.md` — A/B testing backlog spec v3.1 (2026-02-21)
- [S5] `eval_runner.py` — Existing eval runner implementation

**Purpose**: Serve as the requirements section of a release specification. All functional and non-functional requirements extracted, deduplicated, contradictions resolved, and open decisions closed.

---

## Table of Contents

1. [Functional Requirements Matrix](#1-functional-requirements-matrix)
2. [Non-Functional Requirements](#2-non-functional-requirements)
3. [Contradictions and Resolutions](#3-contradictions-and-resolutions)
4. [Open Decision Resolutions](#4-open-decision-resolutions)
5. [Release Scope Recommendation](#5-release-scope-recommendation)
6. [Data Model Requirements](#6-data-model-requirements)
7. [Acceptance Criteria Summary](#7-acceptance-criteria-summary)

---

## 1. Functional Requirements Matrix

### 1.1 Shared Scoring Library (`src/superclaude/eval/`)

| FR-ID | Description | Source | Priority | Slice | Dependencies |
|-------|-------------|--------|----------|-------|--------------|
| FR-LIB-01 | Score dataclass: dimension (str), value (1.0-10.0), hard_fail (bool), reasoning (str) | S1 ss6 | P0 | 1 | None |
| FR-LIB-02 | RunResult dataclass: test_id, run_number, model, scores, exit_code, tokens_used, wall_time_seconds, artifacts, stdout, stderr | S1 ss6 | P0 | 1 | FR-LIB-01 |
| FR-LIB-03 | TestVerdict dataclass: test_id, layer, passed, aggregate_scores (dimension -> mean/stddev/min/max), runs | S1 ss6 | P0 | 1 | FR-LIB-02 |
| FR-LIB-04 | EvalReport dataclass: release, timestamp, tests, overall_passed, model_breakdown, recommendations | S1 ss6 | P0 | 1 | FR-LIB-03 |
| FR-LIB-05 | 5-dimension scoring rubric with anchored definitions: structure, completeness, accuracy, actionability, efficiency (each 1-10) | S1 ss3, S4 ss3 | P0 | 1 | None |
| FR-LIB-06 | Rubric-anchored scoring method (primary) with pairwise preference as alternative | S4 ss3 | P1 | 1 | FR-LIB-05 |
| FR-LIB-07 | Automated scoring supplements: heading_count_and_depth, structural_element_detection, token_efficiency_ratio | S4 ss3 | P2 | 4 | FR-LIB-05 |
| FR-LIB-08 | Judge agent prompt template with structured output parser | S1 ss5 | P0 | 1 | FR-LIB-05 |
| FR-LIB-09 | Judge model defaults to Opus, configurable via `--judge-model` | S1 ss3 | P0 | 1 | FR-LIB-08 |
| FR-LIB-10 | Multi-run parallel execution engine using subprocess | S1 ss5 | P0 | 2 | FR-LIB-02 |
| FR-LIB-11 | Aggregation: mean, stddev, p-values, effect size (Cohen's d) | S1 ss5, S4 | P0 | 2 | FR-LIB-10 |
| FR-LIB-12 | `.claude/` directory isolation with trap-safe restore on exit/error/SIGINT | S1 ss3, S4 ss1 | P0 | 2 | None |
| FR-LIB-13 | Three isolation modes: vanilla (all .claude disabled), baseline (global only), candidate (global + local) | S4 ss2 | P0 | 2 | FR-LIB-12 |
| FR-LIB-14 | Report renderer: produce report.md (human-readable) and scores.jsonl (machine-readable) | S1 ss5 | P0 | 2 | FR-LIB-03 |
| FR-LIB-15 | Results stored in `evals/` directory within release dir or `<timestamp>/` within output dir | S1 ss5 | P0 | 2 | None |

### 1.2 sc:ab-test (Command/Skill A/B Testing)

| FR-ID | Description | Source | Priority | Slice | Dependencies |
|-------|-------------|--------|----------|-------|--------------|
| FR-AB-01 | Tier 1 Regression: baseline (global) vs candidate (local), N runs each; detects change regressions | S1 ss5, S4 | P0 | 3 | FR-LIB-10, FR-LIB-12 |
| FR-AB-02 | Tier 2 Value Validation: vanilla vs baseline vs candidate, N runs each; measures command value-add | S1 ss5, S4 | P0 | 4 | FR-AB-01 |
| FR-AB-03 | Tier 3 Deprecation Audit: vanilla vs current, N runs each; identifies commands to retire | S1 ss5, S4 | P1 | 4 | FR-AB-02 |
| FR-AB-04 | CLI interface: `--command`, `--args`, `--tier`, `--runs`, `--output`, `--dry-run` | S4 ss1 | P0 | 3 | None |
| FR-AB-05 | `--dry-run` validates isolation setup without executing runs | S1 ss9 | P0 | 3 | FR-LIB-12 |
| FR-AB-06 | Per-dimension scores per run written to scores.jsonl | S1 ss9 | P0 | 3 | FR-LIB-14 |
| FR-AB-07 | Summary.md with aggregate scores, variance, and statistical comparison | S1 ss9 | P0 | 3 | FR-LIB-11, FR-LIB-14 |
| FR-AB-08 | Model selection: run same test on different models via `--models` | S1 ss9, S3 | P1 | 3 | FR-LIB-10 |
| FR-AB-09 | Reproducibility: same model + input produces scores within 1 stddev across runs | S1 ss9 | P0 | 3 | FR-LIB-11 |
| FR-AB-10 | Vanilla-equivalent prompt library (YAML): each command has a fair plain-language equivalent | S4 ss2 | P0 | 4 | None |
| FR-AB-11 | Vanilla prompts describe the GOAL not the METHOD; reviewed for fairness | S4 ss2 | P1 | 4 | FR-AB-10 |
| FR-AB-12 | Regression acceptance: candidate must not score significantly lower than baseline on any dimension (p < 0.05) | S4 | P0 | 3 | FR-LIB-11 |
| FR-AB-13 | Value validation acceptance: command must outperform vanilla on >=3 of 5 dimensions | S4 | P0 | 4 | FR-LIB-11 |
| FR-AB-14 | Deprecation acceptance: commands failing to beat vanilla on >=2 dimensions flagged for rework | S4 | P1 | 4 | FR-LIB-11 |
| FR-AB-15 | Cost model tracking: report estimated tokens per tier (30-80K regression, 50-150K value validation) | S4 | P2 | 4 | FR-LIB-02 |

### 1.3 sc:release-eval (Post-Release Validation)

| FR-ID | Description | Source | Priority | Slice | Dependencies |
|-------|-------------|--------|----------|-------|--------------|
| FR-RE-01 | Spec parser: extract ACs, FRs, and NFRs from a release spec markdown file | S1 ss5 | P0 | 5 | None |
| FR-RE-02 | Eval suite generator: produce eval-suite.yaml from parsed spec with tests across 4 layers | S1 ss5, S1 ss10 | P0 | 5 | FR-RE-01 |
| FR-RE-03 | Auto-generate fixtures per release type: happy-path, empty-input, malformed, large-input, bug-repro | S1 ss3 | P0 | 5 | FR-RE-01 |
| FR-RE-04 | Human review pause: present generated eval suite for approval before execution | S1 ss5, S1 ss10 | P0 | 6 | FR-RE-02 |
| FR-RE-05 | 4-layer execution in order with fail-fast: structural -> functional -> quality -> regression | S1 ss3, S1 ss10 | P0 | 6 | FR-RE-02 |
| FR-RE-06 | Layer 1 Structural: file presence checks, schema validity — hard PASS/FAIL | S1 ss3 | P0 | 6 | None |
| FR-RE-07 | Layer 2 Functional: CLI execution, exit codes, artifact production — hard PASS/FAIL per test | S1 ss3 | P0 | 6 | FR-RE-06 |
| FR-RE-08 | Layer 3 Quality: LLM judge scoring against rubric, scored 1-10 per dimension | S1 ss3 | P0 | 6 | FR-LIB-08, FR-RE-07 |
| FR-RE-09 | Layer 4 Regression: before/after statistical comparison with p-values and effect sizes | S1 ss3 | P1 | 6 | FR-LIB-11, FR-RE-08 |
| FR-RE-10 | Overall verdict: PASS requires all structural/functional pass AND quality above configurable thresholds | S1 ss3 | P0 | 6 | FR-RE-05 |
| FR-RE-11 | Judge model scores each run independently (no cross-contamination) | S1 ss10 | P0 | 6 | FR-LIB-08 |
| FR-RE-12 | Per-model score breakdowns in report | S1 ss10 | P1 | 6 | FR-LIB-14 |
| FR-RE-13 | Human-readable report.md with verdict + recommendations | S1 ss10 | P0 | 6 | FR-LIB-14 |
| FR-RE-14 | Works on both feature releases and bug fix releases with adapted test types | S1 ss3, S1 ss10 | P0 | 5 | FR-RE-01 |
| FR-RE-15 | Retroactive: can run evals on already-completed releases | S1 ss10 | P0 | 6 | None |
| FR-RE-16 | Read-only: never modifies release artifacts | S1 ss8 | P0 | 6 | None |

### 1.4 v3.0 Eval Workflow (6-Prompt Pipeline)

| FR-ID | Description | Source | Priority | Slice | Dependencies |
|-------|-------------|--------|----------|-------|--------------|
| FR-V3-01 | Generate lightweight eval-purpose release spec conforming to release-spec-template.md | S2 P1, S3 P1 | P0 | N/A (manual) | None |
| FR-V3-02 | Eval spec must include seeded ambiguities (EVAL-SEEDED-AMBIGUITY comments) to trigger remediate/certify stages | S3 P1 | P0 | N/A (manual) | None |
| FR-V3-03 | Per-stage adversarial review of eval spec against pipeline steps (12 agents) | S2 P2, S3 P2 | P1 | N/A (manual) | FR-V3-01 |
| FR-V3-04 | Impact analysis: top 3 v3.0 impacts with code references and testable metrics | S2 P3, S3 P3 | P0 | N/A (manual) | None |
| FR-V3-05 | 3 end-to-end evals, each targeting one v3.0 impact, each running `superclaude roadmap run` | S2 P3, S3 P3 | P0 | N/A (manual) | FR-V3-04 |
| FR-V3-06 | Eval validation: 7 criteria (4 CRITICAL, 3 REQUIRED) with PASS/FAIL verdicts | S3 P4 | P0 | N/A (manual) | FR-V3-05 |
| FR-V3-07 | Parallel execution: 4 runners (2 local, 2 global via worktrees), minimum 1+1 to proceed | S2 P5, S3 P5 | P0 | N/A (manual) | FR-V3-06 |
| FR-V3-08 | Scoring framework designed to demonstrate v3.0-vs-master delta | S2 P5, S3 P5 | P0 | N/A (manual) | FR-V3-07 |
| FR-V3-09 | Troubleshoot analysis instructions for negative deltas: map stage to spec section and code path | S2 P5, S3 P5 | P1 | N/A (manual) | FR-V3-08 |
| FR-V3-10 | Conditional improvement proposals: 5 actionable code changes if deltas are negative/inconsistent | S2 P6, S3 P6 | P1 | N/A (manual) | FR-V3-08 |

### 1.5 Existing Eval Runner (eval_runner.py)

| FR-ID | Description | Source | Priority | Slice | Dependencies |
|-------|-------------|--------|----------|-------|--------------|
| FR-ER-01 | Modes: local, global, full; local runs on current branch, global via git worktree from master | S5 | P0 | Exists | None |
| FR-ER-02 | Runs pytest eval files, parses JUnit XML for pass/fail/skip/error counts | S5 | P0 | Exists | None |
| FR-ER-03 | Consistency check: local run A vs B should produce identical pass/fail with duration variance tracking | S5 | P0 | Exists | None |
| FR-ER-04 | A/B comparison: regressions (pass->fail), improvements (fail->pass), new test count | S5 | P0 | Exists | None |
| FR-ER-05 | JSON report output to eval-results/eval-report.json | S5 | P0 | Exists | None |
| FR-ER-06 | Non-zero exit code if any local failures | S5 | P0 | Exists | None |

---

## 2. Non-Functional Requirements

| NFR-ID | Description | Source | Priority | Metric |
|--------|-------------|--------|----------|--------|
| NFR-01 | Eval suite generation completes in < 60 seconds (spec analysis, not execution) | S1 ss8 | P0 | Wall-clock < 60s |
| NFR-02 | Token budget per test layer: structural < 500, functional < 5K, quality < 20K per run | S1 ss8 | P1 | Token count |
| NFR-03 | Within-model variance target: coefficient of variation < 0.15 | S1 ss8 | P0 | CV < 0.15 |
| NFR-04 | Must work retrospectively on already-completed releases (10+ in test corpus) | S1 ss8, S1 ss4 | P0 | Boolean |
| NFR-05 | Read-only operation: never modifies release artifacts | S1 ss8 | P0 | Boolean |
| NFR-06 | Results stored in evals/ directory within release directory | S1 ss8 | P1 | Path convention |
| NFR-07 | Safety: trap handler guarantees .claude/ directory restoration on exit/error/SIGINT | S1 ss9, S4 | P0 | Boolean |
| NFR-08 | Cost efficiency: eval runners default to cheaper models (Sonnet, Haiku); Opus for judge only | S1 ss3 | P1 | Model selection |
| NFR-09 | No budget guardrails needed; model selection controls cost | S1 ss3 | P2 | Design constraint |
| NFR-10 | Artifact provenance: output directory created fresh, timestamps verified post-eval | S3 P4 | P0 | Timestamp validation |
| NFR-11 | Third-party verifiability: all eval output inspectable by someone not present during the run | S3 P4 | P0 | Artifact persistence |
| NFR-12 | No mocks in eval execution: grep for mock/Mock/MagicMock/patch/monkeypatch/stub/simulate must yield zero hits | S3 P4 | P0 | Boolean |
| NFR-13 | Minimum 5 runs per variant for statistical validity (see Decision D-01 for full resolution) | S1 ss13, S4 | P0 | Run count >= 5 |
| NFR-14 | Statistical significance threshold: p < 0.05 for regression decisions | S4 | P0 | p-value threshold |
| NFR-15 | Eval spec must complete a full roadmap run in < 15 minutes | S3 P1 | P1 | Wall-clock < 15min |

---

## 3. Contradictions and Resolutions

### C-01: Minimum Runs for Statistical Significance

| Position | Source | Detail |
|----------|--------|--------|
| 5 runs per variant | S1 ss7, S4 | "5 each" stated for all tiers |
| 20 runs minimum | Workflow metrics schema (WORKFLOW_METRICS_SCHEMA.md) | Schema specifies 20-run minimums for metrics |

**Resolution**: Use a **tiered approach**. 5 runs for quick regression (Tier 1) where the question is "did this obviously regress?" and the effect size is expected to be large. 20 runs for value validation (Tier 2) and deprecation audit (Tier 3) where effect sizes are subtler and statistical power matters. Configurable via `--runs N` with minimums enforced: `--runs` must be >= 5 for regression, >= 10 for value-validation (compromise), >= 5 for deprecation. Document that 5-run results have lower statistical power and should be treated as directional, not definitive.

### C-02: Eval Runner Architecture (Pytest vs Pipeline)

| Position | Source | Detail |
|----------|--------|--------|
| Evals run actual `superclaude roadmap run` pipeline end-to-end | S1, S2, S3 | "Full runs of the actual systems," "invoke `superclaude roadmap run`" |
| Existing eval_runner.py runs pytest test files | S5 | Executes 5 pytest eval files via `uv run pytest` |

**Resolution**: These are **two different eval systems** that should coexist. The existing eval_runner.py (S5) runs Python test files that validate gate logic and finding lifecycles -- this is the "unit eval" layer. The new system (S1, S2, S3) runs actual CLI pipelines end-to-end -- this is the "integration eval" layer. The new `src/superclaude/eval/runner.py` must invoke `superclaude roadmap run` (or equivalent CLI commands) via subprocess, NOT pytest. The existing `scripts/eval_runner.py` should be preserved as a complementary tool for rapid Python-level validation, clearly documented as distinct from the new eval system. Rename or namespace to avoid confusion: existing stays as `scripts/eval_runner.py` (unit eval runner), new lives at `src/superclaude/eval/runner.py` (integration eval runner).

### C-03: Shell Script vs Python Library for Orchestration

| Position | Source | Detail |
|----------|--------|--------|
| Shell script orchestrator: `scripts/ab_test_commands.sh` (~200 lines) | S4 | Deliverable 1 is a shell script |
| Python library orchestrator: `src/superclaude/eval/runner.py` | S1 ss5 | Runner is a Python module in the eval package |

**Resolution**: **Python library wins**. S1 is the later, more considered decision and explicitly states "80% of the system is deterministic Python." The shell script in S4 was designed before the hybrid skill-first + Python library approach was decided. Build the orchestration in Python (`src/superclaude/eval/`). The shell script is unnecessary -- Python subprocess calls provide the same isolation capabilities with better error handling, testability, and cross-platform support. A thin shell wrapper can exist for convenience but is not a deliverable.

### C-04: Output Directory Structure

| Position | Source | Detail |
|----------|--------|--------|
| `<release-dir>/evals/` with runs/<timestamp>/ | S1 ss5 | Results structure defined under release dir |
| `docs/generated/ab-tests/<timestamp>/` | S4 ss1 | Shell script outputs to docs/generated/ |
| `.dev/releases/current/.../eval-runs/` | S3 P5 | Prompt 5 writes to eval-runs/ in release dir |
| `.dev/releases/current/.../eval-results/` | S5 | Existing runner writes to eval-results/ |

**Resolution**: Standardize on **`<release-dir>/evals/`** per S1 for release-eval results. For ab-test results (not tied to a release), use **`<output-dir>/ab-tests/<command>/<timestamp>/`** with `--output` defaulting to the current working directory. The existing eval_runner.py path (eval-results/) should be preserved for backward compatibility but documented as the unit eval output path. The `docs/generated/` path from S4 is deprecated in favor of the `--output` flag.

### C-05: Eval Prompt Count and Pipeline Stages

| Position | Source | Detail |
|----------|--------|--------|
| 13 pipeline stages | S2 title | "13 pipeline stages" |
| 12 pipeline steps + deviation-analysis as logical phase | S3 | 12 discrete steps; deviation-analysis is within convergence loop, not a separate step |

**Resolution**: **12 steps** is correct per S3, which is the corrective refactoring of S2 and was written after careful code analysis. The 12 steps are: extract, generate-A, generate-B, diff, debate, score, merge, test-strategy, spec-fidelity, wiring-verification, remediate, certify. Deviation-analysis runs inside the spec-fidelity convergence loop, not as an independent step. S2 was written before the code was fully analyzed.

### C-06: Build Approach for Initial Delivery

| Position | Source | Detail |
|----------|--------|--------|
| Hybrid skill-first + Python library from day one | S1 ss2 | "Build the Python scoring library from day one AND orchestration as skills first" |
| Direct CLI pipeline execution | S3 | All prompts invoke `superclaude roadmap run` directly, no skill intermediary |

**Resolution**: **Python library first, skill second**. S3 is a manual eval workflow (6 prompts run by a human operator), not the reusable tooling. The reusable tooling should follow S1's hybrid approach: build the Python library (scoring, aggregation, isolation, runner) as the foundation, then build skill orchestration on top. The 6-prompt workflow in S3 serves as a proof-of-concept that validates the library's design before skill/CLI portification.

---

## 4. Open Decision Resolutions

These resolve the 6 explicitly listed decisions from S1 ss13 plus additional implicit open decisions identified across all sources.

### D-01: Minimum Runs for Statistical Significance

**Context**: S1 says 5, metrics schema says 20.

**Decision**: **Tiered minimums with `--runs` override.**
- Tier 1 Regression: minimum 5, default 5
- Tier 2 Value Validation: minimum 10, default 10
- Tier 3 Deprecation Audit: minimum 5, default 5
- Release eval quality layer: minimum 5, default 5
- Release eval regression layer: minimum 5, default 5
- `--runs N` flag allows increasing above minimums
- Report confidence level alongside results: "5-run (directional)" vs "20-run (statistically robust)"

**Rationale**: 5 runs detect large effect sizes (Cohen's d > 0.8) at p < 0.05 with adequate power. Value validation tests for subtler effects (d ~ 0.5) and needs more runs for power. 20 runs is ideal but expensive; 10 is the pragmatic minimum for medium effect sizes.

### D-02: Eval Suite Versioning

**Context**: What happens when the release spec changes after an eval suite is generated?

**Decision**: **Version-lock with regeneration.**
- Each eval-suite.yaml includes a `spec_hash` field (SHA-256 of the source spec)
- On execution, the runner validates `spec_hash` matches the current spec
- If mismatch: warn and require `--force` to run stale suite, or regenerate with `--regenerate`
- Old suites archived to `evals/archive/<timestamp>/`
- Suite format includes a `version` field (semver) for schema evolution

**Rationale**: Stale eval suites produce misleading results. Hash validation is cheap and prevents silent drift. Regeneration is the default corrective action.

### D-03: Concurrent Eval Isolation

**Context**: Two evals touching .claude/ simultaneously.

**Decision**: **Queue with worktree-based fallback.**
- Default: file-based lock (`~/.superclaude-eval.lock`) prevents concurrent .claude/ manipulation. Second eval waits or fails with clear message.
- For parallel global runs: git worktree isolation (as S3 P5 already specifies). Each global run gets its own worktree. Local runs share the project .claude/ with the lock.
- `--parallel` flag explicitly opts into worktree-based isolation for local runs too (creates temporary worktrees)

**Rationale**: File locking is simple and safe for the common case (one eval at a time). Worktrees are the proven mechanism for parallel isolation (already used in S3 P5 and S5). The lock prevents the dangerous case (two processes renaming .claude/ simultaneously) while worktrees enable parallelism when needed.

### D-04: Score Persistence Format

**Context**: JSONL vs SQLite vs both.

**Decision**: **JSONL primary, no SQLite in v1.**
- All scores written as JSONL (one JSON object per line): `scores.jsonl`
- Schema matches RunResult dataclass: test_id, run_number, model, dimension, value, hard_fail, reasoning, tokens_used, wall_time
- Aggregated results written to `summary.json` (single JSON object with aggregate stats)
- Human-readable report to `report.md`
- SQLite deferred to future release when querying across many eval runs becomes a real need

**Rationale**: JSONL is the existing convention (workflow_metrics.jsonl), is simple to append, grep, and parse, and avoids adding a sqlite3 dependency. The aggregator already computes everything needed in-memory. SQLite adds complexity for a querying need that does not yet exist.

### D-05: Vanilla Prompt Authoring

**Context**: Auto-generated or hand-crafted?

**Decision**: **Hand-crafted library with review requirement.**
- Vanilla prompts live in `tests/ab/vanilla-prompts.yml` (per S4)
- Each prompt is hand-written to describe the GOAL, not the METHOD
- New commands must include a vanilla-equivalent prompt as a deliverable (part of the command definition checklist)
- PRs modifying vanilla prompts require review from someone other than the prompt author
- Auto-generation is a future enhancement (generate draft -> human review -> approve)

**Rationale**: Fair vanilla prompts are critical to the validity of value-validation tests. A sandbagged prompt (too vague) makes the command look artificially good. An enhanced prompt (containing the command's internal instructions) makes the test meaningless. Human authorship with peer review is the only way to ensure fairness until a validated auto-generation approach exists.

### D-06: Slice 1-2 Release Target

**Context**: Ship scoring library separately or with ab-test?

**Decision**: **Ship slices 1-2 together as v1.0-alpha of the eval library.** Do NOT ship them as a standalone release.
- Slices 1-2 (scoring library + multi-run engine) are the foundation but have no user-facing surface area
- Ship them alongside slice 3 (ab-test regression tier) as the first user-testable release
- Internal milestone: slices 1-2 pass their own tests (score one output, run 5x and aggregate) before starting slice 3
- External release: v1.0 = slices 1-3 (scoring library + multi-run + regression tier)

**Rationale**: A library with no CLI or skill surface is not testable by users. Slices 1-2 are prerequisites, not products. Bundling with slice 3 gives users something they can actually run: `sc:ab-test --tier regression --command sc:roadmap`.

### D-07: Eval Runner Relationship (Implicit)

**Context**: The existing `scripts/eval_runner.py` runs pytest-based eval files. The new system runs actual CLI pipelines. What is their relationship?

**Decision**: **Coexist as complementary layers.**
- `scripts/eval_runner.py` remains as-is for pytest-based unit evals (fast, deterministic, validates Python logic)
- `src/superclaude/eval/runner.py` is the new integration eval runner (slower, stochastic, validates pipeline behavior)
- Both can be orchestrated together: unit evals as a pre-flight check before integration evals
- No code sharing between them; they solve different problems

### D-08: Skill vs CLI Phasing (Implicit)

**Context**: S1 says "skill first, then portify to CLI." S3's prompts invoke CLI directly. When does each phase happen?

**Decision**: **Python library + CLI from the start. Skill is a thin wrapper.**
- The Python library (`src/superclaude/eval/`) is built first (slices 1-2)
- The CLI (`superclaude ab-test`, `superclaude release-eval`) wraps the library (slice 3+)
- The skill (`.claude/skills/sc-ab-test/`, `.claude/commands/sc/ab-test.md`) is a thin orchestration layer that calls the CLI or library
- There is no separate "skill-only" phase; the skill and CLI are developed together
- Portification cost is minimized because the library does the heavy lifting

**Rationale**: The v3.0 eval workflow (S3) proved that direct CLI invocation works. The "skill-first for discovery" rationale in S1 is valid but the discovery has already happened through the 6-prompt workflow. Building CLI first avoids the portification tax.

### D-09: Cross-Model Scoring Normalization (Implicit)

**Context**: S1 says "within-model consistency, not cross-model." S4 mentions "cross-command scoring normalization" as an open question.

**Decision**: **Within-model only. Cross-model and cross-command are informational.**
- Statistical comparisons (p-values, effect sizes) are only valid within the same model
- Cross-model results are reported as separate rows, never aggregated into a single score
- Cross-command normalization is out of scope for v1; each command has its own quality ceiling
- Report includes a "model comparison" section that is explicitly labeled "informational, not statistical"

### D-10: Docker Isolation (Implicit)

**Context**: S4 and S1 ss12 both mention Docker as a safer vanilla baseline mechanism.

**Decision**: **Out of scope for v1. File-based isolation with trap handlers is sufficient.**
- Docker isolation is a future enhancement (S1 ss12 explicitly marks it as out of scope)
- Current approach: rename `.claude/` directories with trap-safe restore
- Risk is mitigated by `--dry-run` validation and lock files

---

## 5. Release Scope Recommendation

### Recommendation: Option B (Modified) -- Two releases with a shared foundation

**v1.0: sc:ab-test** (Slices 1-4)
- Shared scoring library (`src/superclaude/eval/`)
- Multi-run engine with isolation
- sc:ab-test command/skill with all 3 tiers
- Vanilla prompt library (initial set)
- CLI: `superclaude ab-test --tier regression --command sc:roadmap`

**v2.0: sc:release-eval** (Slices 5-7)
- Spec parser and eval suite generator
- Release eval executor with 4-layer fail-fast
- CLI portification of both commands
- CLI: `superclaude release-eval .dev/releases/complete/v2.25-cli-portify-cli/`

### Rationale

1. **Dependency direction is clear**: sc:release-eval depends on the scoring library and multi-run engine, but sc:ab-test does not depend on the spec parser or suite generator. Building ab-test first validates the shared foundation before release-eval builds on it.

2. **Scope containment**: v1.0 (slices 1-4) is approximately 7 Python modules + 2 YAML files + 1 skill definition + 1 CLI command. v2.0 (slices 5-7) adds 4 more Python modules + 1 skill + 1 CLI command. Each release is approximately 2-3 weeks of focused work.

3. **Incremental validation**: v1.0 can be tested immediately against any command (sc:roadmap, sc:analyze, sc:explain). v2.0 can be tested against the 10+ completed releases in the test corpus. Neither release requires the other to deliver value.

4. **The 6-prompt workflow (S2, S3) is NOT a release**: It is a manual evaluation procedure for v3.0 specifically. It informs the design of the reusable tooling but is not itself a deliverable. The prompts should be treated as design artifacts, not product requirements. They validate that the approach works; the releases (v1.0, v2.0) productize it.

5. **Why not Option A (single release)**: Combined scope of slices 1-7 plus the 6-prompt workflow is too large for a single release. It mixes reusable tooling (slices 1-7) with one-off v3.0 evaluation (prompts 1-6). The v3.0 eval can be run manually at any time and does not need to wait for or be bundled with the reusable tooling.

6. **Why not Option C**: No compelling reason to split differently. Slices 1-4 form a natural unit (scoring + ab-test). Slices 5-7 form a natural unit (spec-parsing + release-eval + CLI polish). The boundary is clean.

### Release Timeline

| Release | Content | Prerequisite | Estimated Effort |
|---------|---------|--------------|-----------------|
| v1.0 sc:ab-test | Slices 1-4: scoring lib + multi-run + ab-test (3 tiers) + vanilla prompts | None | 2-3 weeks |
| v2.0 sc:release-eval | Slices 5-7: spec parser + suite gen + release eval + CLI portify | v1.0 complete | 2-3 weeks |
| (Manual) v3.0 eval | Run 6-prompt workflow using v1.0 library or directly | v3.0 branch merged; v1.0 recommended but not required | 1-2 days |

---

## 6. Data Model Requirements

All dataclasses live in `src/superclaude/eval/models.py`. Consolidated from S1 ss6 with additions from S3 and S4.

```python
@dataclass
class Score:
    dimension: str          # structure|completeness|accuracy|actionability|efficiency
    value: float            # 1.0 - 10.0
    hard_fail: bool         # True = binary pass/fail (structural/functional layers)
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
    artifacts: list[str]    # File paths produced
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
    spec_hash: str          # SHA-256 of source spec (added per D-02)
    tests: list[TestVerdict]
    overall_passed: bool
    model_breakdown: dict   # model -> {dimension -> mean_score}
    recommendations: list[str]
    confidence_level: str   # "directional" (5-run) or "robust" (20-run) (added per D-01)

@dataclass
class ABComparison:
    tier: str               # regression|value_validation|deprecation
    command: str
    baseline_scores: dict   # dimension -> {mean, stddev}
    candidate_scores: dict  # dimension -> {mean, stddev}
    p_values: dict          # dimension -> p-value
    effect_sizes: dict      # dimension -> Cohen's d
    verdict: str            # improved|regressed|neutral
    runs_per_variant: int
```

Note: `ABComparison` is new -- not in S1 but required by FR-AB-07 and FR-AB-12. It captures the A/B comparison result as a first-class object.

---

## 7. Acceptance Criteria Summary

### v1.0 sc:ab-test (from S1 ss9, augmented)

| AC-ID | Criterion | Validates |
|-------|-----------|-----------|
| AC-AB-01 | Can run regression test comparing global vs local version of any command | FR-AB-01 |
| AC-AB-02 | Can run value-validation test comparing vanilla vs baseline vs candidate | FR-AB-02 |
| AC-AB-03 | Produces scores.jsonl with per-dimension scores per run | FR-AB-06 |
| AC-AB-04 | Produces summary.md with aggregate scores, variance, statistical comparison | FR-AB-07 |
| AC-AB-05 | Handles model selection (run same test on different models) | FR-AB-08 |
| AC-AB-06 | Results reproducible: same model + input produces scores within 1 stddev | FR-AB-09 |
| AC-AB-07 | Safety: trap handler guarantees .claude/ directories restored on exit/error/SIGINT | FR-LIB-12 |
| AC-AB-08 | `--dry-run` validates isolation without executing any runs | FR-AB-05 |
| AC-AB-09 | Lock file prevents concurrent .claude/ manipulation | D-03 |
| AC-AB-10 | Regression tier: candidate not significantly worse than baseline on any dimension (p < 0.05) | FR-AB-12 |

### v2.0 sc:release-eval (from S1 ss10, augmented)

| AC-ID | Criterion | Validates |
|-------|-----------|-----------|
| AC-RE-01 | Given a release directory, parses spec and extracts ACs/FRs/NFRs | FR-RE-01 |
| AC-RE-02 | Generates eval-suite.yaml with tests across all 4 layers | FR-RE-02 |
| AC-RE-03 | Auto-generates fixtures appropriate to release type | FR-RE-03 |
| AC-RE-04 | Presents generated suite for human review before execution | FR-RE-04 |
| AC-RE-05 | Executes layers in order with fail-fast (structural failure stops early) | FR-RE-05 |
| AC-RE-06 | Judge model scores each run independently | FR-RE-11 |
| AC-RE-07 | Produces per-model score breakdowns | FR-RE-12 |
| AC-RE-08 | Produces human-readable report.md with verdict + recommendations | FR-RE-13 |
| AC-RE-09 | Works on both feature releases and bug fix releases | FR-RE-14 |
| AC-RE-10 | Can re-run evals on already-completed releases (retroactive) | FR-RE-15 |
| AC-RE-11 | Eval suite includes spec_hash; runner validates hash before execution | D-02 |
| AC-RE-12 | Read-only: no modification of release artifacts | FR-RE-16 |

---

## Appendix A: Source Document Index

| Source ID | File | Key Sections Referenced |
|-----------|------|----------------------|
| S1 | `conversation-decisions.md` | ss2: build approach, ss3: design decisions, ss5: architecture, ss6: data model, ss7: delivery plan, ss8: NFRs, ss9: AC ab-test, ss10: AC release-eval, ss13: open decisions |
| S2 | `6PromptV3-Eval.md` | P1-P6: six prompt definitions |
| S3 | `eval-prompts.md` | Review of rejected approach, P1-P6: refactored prompts with validation criteria |
| S4 | `release-plan.md` | Three-tier model, isolation modes, deliverables, scoring rubric, cost model |
| S5 | `eval_runner.py` | Existing implementation: modes, pytest runner, comparison logic |

## Appendix B: Requirements Not Carried Forward

The following items from source documents are explicitly **excluded** from these requirements:

| Item | Source | Reason for Exclusion |
|------|--------|---------------------|
| Docker isolation for vanilla baseline | S1 ss12, S4 | Explicitly marked future/out-of-scope in all sources |
| Pipeline-integrated evals (Phase 12 in sprint pipeline) | S1 ss12 | Future vision, out of scope |
| CI-triggered A/B tests on PRs | S1 ss12, S4 | Future vision, out of scope |
| Eval dashboard (historical score tracking) | S1 ss12 | Future vision, out of scope |
| Judge model experimentation | S1 ss12 | Future vision, out of scope |
| Pairwise preference scoring (as primary method) | S4 | Listed as alternative, not primary; deferred |
| `/sc:test --type ab` integration | S4 | Open question in S4, premature before tooling exists |
| Cross-command scoring normalization | S4 | Open question, explicitly out of scope per D-09 |
| SQLite score persistence | S1 ss13 | Deferred per D-04; JSONL sufficient for v1 |
