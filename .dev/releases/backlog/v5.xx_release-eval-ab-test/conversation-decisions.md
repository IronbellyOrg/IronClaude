# Release Eval & A/B Testing System — Decision Record & Context Brief

**Created**: 2026-03-17
**Source**: Brainstorm + adversarial debate conversation
**Purpose**: Input for BMAD to generate the full release specification
**Status**: Pre-spec decisions locked

---

## 1. What We're Building

Two complementary skills/commands that share a scoring library:

| Component | Name | Purpose |
|---|---|---|
| **Shared Library** | `src/superclaude/eval/` | Scoring rubric, judge agent, multi-run engine, isolation, aggregation |
| **Skill/Command 1** | `sc:ab-test` (v1.0) | Command/skill regression & value testing — "did this skill get better or worse?" |
| **Skill/Command 2** | `sc:release-eval` (v2.0) | Post-release validation against spec — "did this release deliver what it promised?" |

### The Problem Being Solved

Current testing infrastructure has a critical gap:
- **Unit tests** (`tests/`) check internal Python logic but don't exercise real system behavior
- **Smoke tests** (`scripts/smoke-test-v2.sh`) check artifact *existence* but not functional correctness or quality
- **No quality measurement** exists — nothing scores output quality, measures consistency across runs, or compares before/after

We need **full runs of the actual systems** with **proper evals** that produce **consistent scores** across multiple runs and models.

### The Two Distinct Test Purposes

| | sc:ab-test | sc:release-eval |
|---|---|---|
| **Subject** | A command/skill (e.g., `sc:roadmap`) | A completed release (e.g., v2.25-cli-portify-cli) |
| **Question** | Is version B better than version A? | Did the release deliver what the spec promised? |
| **Output** | Statistical comparison (p-values, effect sizes) | Pass/fail verdict + quality scores |
| **Trigger** | After modifying a command/skill | After completing a release |

---

## 2. Why We're Building It This Way

### Build Approach: Hybrid Skill-First + Parallel Python Library

**Decision**: Build the Python scoring library from day one AND build the orchestration as Claude Code skills first. When proven, portify orchestration to CLI.

**Source**: Adversarial debate (Skill-First vs CLI-First)

**Rationale**:
- Pure skill-first risks building it twice (portification cost)
- Pure CLI-first risks designing in the dark (no interactive iteration)
- The hybrid captures both: Python library is deterministic/testable/reusable; skills enable rapid discovery
- 80% of the system (scoring, aggregation, isolation, runner) is deterministic Python that doesn't benefit from inference
- 20% (eval-suite generation, judge agent, orchestration) benefits from skill-first iteration
- Proven pattern: v2.25-cli-portify-cli followed exactly this trajectory

**What gets built once** (Python library — used by both skill and CLI):
- `models.py` — dataclasses (Score, RunResult, TestVerdict, EvalReport)
- `rubric.py` — 5 scoring dimensions with anchored definitions
- `aggregator.py` — mean, stddev, p-values, effect size
- `isolation.py` — .claude/ directory toggling with trap-safe restore
- `runner.py` — multi-run parallel execution (subprocess)
- `judge.py` — judge agent prompt template + response parser
- `reporter.py` — report.md template rendering

**What gets built twice** (orchestration — small, ~20%):
- Pipeline step ordering (skill prompt → Python executor)
- Error handling ("if X fails, do Y" → try/except)
- State management (conversation context → .eval-state.json)

### Spec Approach: New Spec From Scratch (Not Refactoring Existing)

**Decision**: Write a new spec. Do NOT refactor `unified-audit-gating-v1.2.1-release-spec.md`.

**Source**: Adversarial debate (Refactor vs New Spec)

**Rationale**:
- Only ~20-25% conceptual overlap between audit-gating and eval systems
- Different consumers (sprint pipeline vs developer), different execution models (once deterministic vs N-times measuring variance), different cost profiles (near-zero vs token-intensive)
- Refactoring 440 lines where 75-80% must be removed/replaced creates "ghosts" — vestigial concepts that confuse readers
- A clean spec is purpose-built, self-consistent, and doesn't require understanding the original domain

**Cherry-pick these methodology patterns** from the existing spec:
1. Evidence Model and Decision Method (existing §0) — deterministic vs heuristic distinction
2. Locked Decisions pattern (existing §2.1) — explicit list of what's decided
3. Contradictions table format (existing §2.3) — when sources disagree, document resolution
4. Pass/fail rules pattern (existing §5.2) — binary decision model for structural/functional layers
5. Evidence requirements pattern (existing §5.3) — every failure must cite evidence
6. Checklist closure matrix format (existing §11) — readiness tracking table

**Reference as Related Work** (don't copy):
- GateResult schema (existing §6.1) — informs EvalReport dataclass
- Release Decision Gate (existing §12) — eval system automates this concept

### Version Ordering

**Decision**: Build `sc:ab-test` (v1.0) first, then `sc:release-eval` (v2.0).

**Rationale**:
- A/B testing already has a detailed backlog spec (`.dev/releases/backlog/v3.1-ab-testing/release-plan.md`)
- A/B infrastructure (multi-run, scoring, isolation) is foundation for release-eval
- Smaller scope = faster to prove the scoring library works

### Two Separate Skills, Shared Library

**Decision**: Two separate top-level skills/commands that share a scoring library. NOT one skill with different modes.

**Rationale**: Different test subjects (command vs release), different workflows, different outputs. Shared infrastructure lives in the Python library, not the skill layer. When portified to CLI, they share even more infrastructure as `superclaude ab-test` and `superclaude release-eval`.

---

## 3. Key Design Decisions

### Scoring & Judging

| Decision | Choice | Rationale |
|---|---|---|
| Judge model | Always Opus (configurable via `--judge-model`) | Highest quality scoring; easy to swap later |
| Eval runner models | Cheaper models (Sonnet, Haiku) by default | Cost efficiency; Opus only for validation |
| Scoring dimensions | 5: structure, completeness, accuracy, actionability, efficiency | From v3.1 A/B spec, proven rubric |
| Consistency target | Within-model consistency (not cross-model) | Cross-model comparison is informational, not statistical |
| Budget guardrails | None — model selection controls cost | Eval runs use cheap models; no need for token caps |

### Failure Model

| Layer | Type | Verdict |
|---|---|---|
| Layer 1 — Structural | File presence, schema validity | **Hard PASS/FAIL** |
| Layer 2 — Functional | CLI execution, exit codes, artifacts | **Hard PASS/FAIL** per test |
| Layer 3 — Quality | LLM judge scoring against rubric | **Scored** (1-10 per dimension) |
| Layer 4 — Regression | Before/after statistical comparison | **Scored** + statistical test |

Overall verdict: PASS requires all structural/functional pass AND quality above configurable thresholds.

### Before/After Mechanism

Three modes, all using `.claude/` directory isolation:
1. **Global vs Local**: Don't run `make sync-dev` → global = old, local = new. Simplest.
2. **Vanilla vs Skill**: Disable all `.claude/` → compare raw Claude prompt vs skill invocation
3. **Example**: `"build me a tasklist for this roadmap"` (vanilla) vs `sc:tasklist roadmap.md` (skill)

### Fixture Generation

**Decision**: Auto-generated from spec analysis by Claude. Human reviews before execution.

Fixtures generated per release:
- `happy-path.md` — minimal valid input
- `empty-input.md` — empty/missing file
- `malformed.md` — invalid YAML, broken markdown
- `large-input.md` — stress test (if applicable)
- `bug-repro.md` — for patch releases, input that triggered the original bug

### Cross-Model Testing

**Decision**: Run same eval suite across multiple models. Scores reported per-model. Not compared across models unless explicitly requested.

**Purpose**: Score cheaper/faster models to see if skill/harness improvements can bring them close enough to Opus to enable cost savings.

### Trigger Model

**Decision**: Manual invocation for now. Both skills triggered by developer after release completion or skill modification.

**Future**: Eventually integrate into release pipeline (Phase 12) and CI (auto-trigger on PRs touching commands/skills).

### Release Type Handling

**Decision**: Same interface for both feature releases and bug fix releases. The eval-suite generator adapts test types based on release type.

| Release Type | Structural Tests | Functional Tests | Quality Tests | Regression Tests |
|---|---|---|---|---|
| Feature | Artifact presence, schema | Run command on samples | Judge output quality | Compare vs vanilla/pre-release |
| Bug fix | Fix artifacts exist | Reproduce bug, confirm fixed | Judge fix area quality | Verify no adjacent regressions |

---

## 4. Existing Infrastructure to Build On

### Already Exists

| Asset | Location | Relevance |
|---|---|---|
| A/B testing spec | `.dev/releases/backlog/v3.1-ab-testing/release-plan.md` | Full design for sc:ab-test — 3 tiers, isolation, rubric, vanilla prompts |
| Statistical comparison engine | `scripts/ab_test_workflows.py` | Can compute p-values, effect sizes |
| Metrics aggregation | `scripts/analyze_workflow_metrics.py` | Aggregates JSONL metrics |
| Workflow metrics schema | `docs/memory/WORKFLOW_METRICS_SCHEMA.md` | JSONL format, 20-run minimums |
| Completed releases (test corpus) | `.dev/releases/complete/` | 10+ releases to test against retroactively |

### Test Corpus (Completed Releases)

| Release | Type | Best Used For |
|---|---|---|
| `v2.25-cli-portify-cli` | Feature (large, 60+ deliverables) | Full eval suite generation, quality scoring |
| `v2.25.7-Phase8HaltFix` | Bug fix (patch) | Bug repro tests, regression verification |
| `v2.25.5-PreFlightExecutor` | Feature (medium) | Functional tests, artifact checks |
| `v2.24.5-SpecFidelity` | Feature | Structural + quality validation |
| `v2.24.2-Accept-Spec-Change` | Feature | Gate validation, schema compliance |
| `v2.20-WorkflowEvolution` | Feature (large) | Complex multi-phase eval |

**Critical decision**: Use these completed releases retroactively to test the eval system as we build it. The testing system is tested by testing real releases.

---

## 5. Architecture

### Shared Scoring Library (`src/superclaude/eval/`)

```
src/superclaude/eval/
├── __init__.py
├── models.py         ← Score, RunResult, TestVerdict, EvalReport dataclasses
├── rubric.py         ← 5-dimension scoring rubric + anchored definitions
├── judge.py          ← Judge-agent prompt template + response parser
├── runner.py         ← Multi-run parallel execution engine (subprocess)
├── isolation.py      ← .claude/ directory toggling with trap-safe restore
├── aggregator.py     ← Mean, stddev, p-values, effect size, Cohen's d
└── reporter.py       ← report.md + scores.jsonl template rendering
```

### sc:ab-test (v1.0)

```
# Skill phase
.claude/skills/sc-ab-test/SKILL.md
.claude/commands/sc/ab-test.md

# CLI phase (after portification)
src/superclaude/cli/ab_test/
├── __init__.py
├── main.py           ← Click command group
├── executor.py       ← Orchestrates tiers
└── prompts.py        ← Vanilla-equivalent prompt library
```

**Three Tiers**:
1. **Regression**: baseline (global) vs candidate (local) — 5 runs each — "did this change regress?"
2. **Value Validation**: vanilla vs baseline vs candidate — 5 runs each — "does this command earn its keep?"
3. **Deprecation Audit**: vanilla vs current — 5 runs each — "should this command still exist?"

### sc:release-eval (v2.0)

```
# Skill phase
.claude/skills/sc-release-eval/SKILL.md
.claude/commands/sc/release-eval.md

# CLI phase (after portification)
src/superclaude/cli/release_eval/
├── __init__.py
├── main.py           ← Click command group
├── spec_parser.py    ← Extract ACs, FRs, NFRs from release spec
├── suite_generator.py ← Generate eval-suite.yaml from parsed spec
├── executor.py       ← Run eval suite (structural → functional → quality → regression)
└── reporter.py       ← Produce validation report + scores
```

**Workflow**: PARSE spec → GENERATE eval suite → REVIEW (human pause) → EXECUTE (layers 1-4, fail-fast) → SCORE (judge model) → REPORT

### Eval Suite Format

```yaml
release: v2.25-cli-portify-cli
release_type: feature
spec_path: portify-release-spec.md
generated_by: claude-sonnet-4-6

tests:
  - id: structural-001
    layer: structural
    name: "All 12 pipeline step files exist"
    type: file_presence
    expected_files: [...]

  - id: functional-001
    layer: functional
    name: "Happy path execution"
    type: cli_execution
    command: "superclaude cli-portify run"
    input: fixtures/happy-path.md
    success_criteria:
      - exit_code: 0
      - artifacts_produced: [...]

  - id: quality-001
    layer: quality
    type: llm_judge
    runs: 5
    models: [claude-sonnet-4-6, claude-haiku-4-5]
    rubric_focus: [completeness, accuracy, structure]
    min_scores: {completeness: 7.0, accuracy: 8.0}

  - id: regression-001
    layer: regression
    type: ab_comparison
    baseline: "vanilla prompt"
    candidate: "superclaude command"
    runs: 5
```

### Results Structure

```
<release-dir>/evals/
├── eval-suite.yaml
├── fixtures/
├── runs/<timestamp>/
│   ├── structural/results.jsonl
│   ├── functional/<test-id>/run-N/
│   ├── quality/<test-id>/scores.jsonl
│   ├── regression/comparison.jsonl
│   ├── scores.jsonl          ← all scores, all tests
│   └── report.md             ← human-readable summary
```

---

## 6. Data Model

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
    aggregate_scores: dict  # dimension → {mean, stddev, min, max}
    runs: list[RunResult]

@dataclass
class EvalReport:
    release: str
    timestamp: str
    tests: list[TestVerdict]
    overall_passed: bool
    model_breakdown: dict   # model → {dimension → mean_score}
    recommendations: list[str]
```

---

## 7. Incremental Delivery Plan

Each slice is independently testable against completed releases:

| Slice | Deliverable | Test It Against |
|---|---|---|
| 1 | Scoring library + single-run judge | Score one output from v2.25-cli-portify-cli manually |
| 2 | Multi-run engine + aggregation | Run sc:tasklist 5x on v2.25 roadmap, score each |
| 3 | sc:ab-test regression tier | Modify a skill, verify before/after comparison |
| 4 | sc:ab-test value + deprecation tiers | Vanilla vs sc:explain on a file |
| 5 | Spec parser + eval-suite generator | Point at v2.25-cli-portify-cli, generate suite |
| 6 | Release eval executor | Execute generated suite, get full report |
| 7 | CLI portification | superclaude ab-test / superclaude release-eval |

**Critical principle**: Build smallest functional slice, eval it, iterate. Test the testing system using real completed releases as corpus from day one.

---

## 8. Non-Functional Requirements

- NFR-01: Eval suite generation < 60 seconds (spec analysis, not execution)
- NFR-02: Structural tests < 500 tokens, functional < 5K, quality < 20K per run
- NFR-03: Within-model variance measured (target CV < 0.15)
- NFR-04: Must work retrospectively on already-completed releases
- NFR-05: Read-only — never modifies release artifacts
- NFR-06: Results stored in evals/ directory within release dir

---

## 9. Acceptance Criteria (sc:ab-test v1.0)

- AC-01: Can run regression test comparing global vs local version of any command
- AC-02: Can run value-validation test comparing vanilla vs baseline vs candidate
- AC-03: Produces scores.jsonl with per-dimension scores per run
- AC-04: Produces summary.md with aggregate scores, variance, statistical comparison
- AC-05: Handles model selection (run same test on different models)
- AC-06: Results reproducible — same model + input produces scores within 1 stddev
- AC-07: Safety: trap handler guarantees .claude/ directories restored on exit/error/SIGINT
- AC-08: --dry-run validates isolation without executing any runs

---

## 10. Acceptance Criteria (sc:release-eval v2.0)

- AC-01: Given a release directory, parses spec and extracts ACs/FRs/NFRs
- AC-02: Generates eval-suite.yaml with tests across all 4 layers
- AC-03: Auto-generates fixtures appropriate to release type
- AC-04: Presents generated suite for human review before execution
- AC-05: Executes layers in order with fail-fast (structural failure stops early)
- AC-06: Judge model scores each run independently
- AC-07: Produces per-model score breakdowns
- AC-08: Produces human-readable report.md with verdict + recommendations
- AC-09: Works on both feature releases and bug fix releases
- AC-10: Can re-run evals on already-completed releases (retroactive)

---

## 11. Related Specs and Assets

| Document | Location | Relationship |
|---|---|---|
| A/B Testing v3.1 Spec | `.dev/releases/backlog/v3.1-ab-testing/release-plan.md` | **Incorporated** — forms basis of sc:ab-test design |
| Unified Audit Gating v1.2.1 | `.dev/releases/backlog/unified-audit-gating-v1.2.1/unified-audit-gating-v1.2.1-release-spec.md` | **Referenced** — methodology patterns cherry-picked, domain model NOT reused |
| Workflow Metrics Schema | `docs/memory/WORKFLOW_METRICS_SCHEMA.md` | **Referenced** — JSONL format for scores |
| Statistical Engine | `scripts/ab_test_workflows.py` | **Dependency** — p-value and effect size computation |

---

## 12. Future Vision (Out of Scope, Noted for BMAD)

- Pipeline-integrated evals: release eval as Phase 12 in sprint pipeline
- CI-triggered A/B tests: auto-run regression on PRs touching commands/skills
- Eval-driven development: roadmap generates releases in functional slices that are eval'd as they land
- Docker isolation: safer vanilla baseline via clean container
- Eval dashboard: historical score tracking across releases and models
- Judge model experimentation: test different judge models to optimize cost vs scoring quality

---

## 13. Open Decisions (For BMAD to Address in Full Spec)

| Decision | Context | Options |
|---|---|---|
| Minimum runs for statistical significance | v3.1 spec says 5, metrics schema says 20 | Reconcile: 5 for quick regression, 20 for value validation? |
| Eval suite versioning | What happens when spec changes? | Re-generate suite? Version-lock? |
| Concurrent eval isolation | Two evals touching .claude/ simultaneously | Queue or worktree-based isolation? |
| Score persistence format | JSONL vs SQLite vs both | JSONL for simplicity, SQLite for querying? |
| Vanilla prompt authoring | Auto-generated or hand-crafted? | v3.1 spec has library; need to decide maintenance model |
| Slice 1-2 release target | Ship scoring library separately or with ab-test? | Single release or multiple? |
