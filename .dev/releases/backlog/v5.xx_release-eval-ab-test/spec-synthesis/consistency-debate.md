---
title: "Adversarial Consistency Debate: Eval CLI Spec Synthesis"
date: 2026-03-19
documents_analyzed: 4
contradictions_found: 9
gaps_found: 6
blocking_issues: 2
---

# Adversarial Consistency Debate: Eval CLI Spec Synthesis

**Debaters**: Architecture Extraction (Agent 1) vs Workflow Analysis (Agent 2) vs Infrastructure Gap Analysis (Agent 3) vs Requirements Consolidated (Agent 4)

**Ground Truth**: conversation-decisions.md (Source of Record)

---

## Consistency Check 1: Architecture <> Workflow

**Question**: Do the architecture decisions (Agent 1) support the operational workflow (Agent 2)?

### 1.1 Seven-Module Library vs 14-Stage Pipeline

Agent 1 defines a 7-module library: `models.py`, `rubric.py`, `judge.py`, `runner.py`, `isolation.py`, `aggregator.py`, `reporter.py`. Agent 2 defines a 14-stage pipeline across 6 phases (eval-spec-generate through conditional-improvement).

**Finding**: The 7 modules are a *library*, not a pipeline orchestrator. The 14-stage pipeline described in Agent 2 is the 6-prompt v3.0 eval workflow -- a *manual evaluation procedure*, not the reusable tooling. These are different systems at different levels of abstraction. Agent 1's library supports the reusable `sc:ab-test` and `sc:release-eval` commands. Agent 2's pipeline describes a one-time v3.0 validation workflow.

**Assessment**: CONSISTENT but confusing. The spec must clearly separate "reusable eval library" (7 modules) from "v3.0 eval workflow" (14 stages). Agent 4 (Requirements) correctly identifies this in Section 5: "The 6-prompt workflow (S2, S3) is NOT a release."

### 1.2 Failure Model Mapping to Workflow Stages

Agent 1's 4-layer failure model (Structural -> Functional -> Quality -> Regression) maps to Agent 2's phases as follows:

- Structural (L1): exercised in Phase 5 eval-execute (file presence checks)
- Functional (L2): exercised in Phase 5 eval-execute (CLI exit codes)
- Quality (L3): exercised in Phase 6 score-runs (judge scoring)
- Regression (L4): exercised in Phase 6 compute-deltas (statistical comparison)

**Assessment**: CONSISTENT. The failure layers map cleanly to workflow execution phases.

### 1.3 Missing Pipeline Components

Agent 2 identifies stages that have no corresponding Agent 1 architecture component:

- `eval-spec-generate` and `eval-spec-validate` (Phase 1): No library module handles spec generation. This is expected -- spec generation is an LLM skill task, not a Python library function.
- `adversarial-stage-review` and `adversarial-synthesis` (Phase 2): No library module handles adversarial review. Again, these are LLM tasks.
- `scoring-framework-generate` and `scoring-adversarial-review` (Phase 5): No library module for the scoring framework meta-design.
- `conditional-improvement` (Phase 6): No library module for improvement proposals.

**Assessment**: CONSISTENT. Agent 1 explicitly states the library handles "80% of the system" (deterministic Python) while "20% (eval-suite generation, judge agent, orchestration) benefits from skill-first iteration." The unmatched stages are exactly the 20% skill-first components.

### 1.4 Workflow Stage Ordering vs Slice Dependencies

Agent 2's 6 phases are sequential. Agent 1's 7 slices have a different ordering:

- Slices 1-2 (library) map to no specific workflow phase -- they are infrastructure.
- Slices 3-4 (ab-test) map to Phase 5's eval-execute concept but for A/B testing, not the 6-prompt workflow.
- Slices 5-6 (release-eval) map to Phases 1, 4, 5, 6 but in a different decomposition.
- Slice 7 (CLI portification) is post-workflow.

**Assessment**: CONSISTENT. The slices build the reusable tool incrementally; the workflow phases describe a usage scenario. They are orthogonal, not conflicting.

---

## Consistency Check 2: Infrastructure <> Requirements

**Question**: Does the infrastructure gap analysis (Agent 3) account for everything the requirements (Agent 4) need?

### 2.1 P0 Requirements Coverage

Cross-referencing Agent 4's P0 requirements against Agent 3's gap table:

| FR-ID | Requirement | Agent 3 Gap | Covered? |
|-------|-------------|-------------|----------|
| FR-LIB-01 through FR-LIB-04 | Data model dataclasses | G-02 (eval/models.py) | YES |
| FR-LIB-05 | 5-dimension rubric | G-03 (eval/rubric.py) | YES |
| FR-LIB-08 | Judge agent prompt template | G-06 (eval/judge.py) | YES |
| FR-LIB-09 | Judge model configurable | G-06 (eval/judge.py) | YES |
| FR-LIB-10 | Multi-run parallel engine | G-04 (eval/runner.py) | YES |
| FR-LIB-11 | Statistical aggregation | G-07 (eval/aggregator.py) | YES |
| FR-LIB-12 | .claude/ isolation with trap-safe restore | G-05 (eval/isolation.py) | YES |
| FR-LIB-13 | Three isolation modes | G-05 (eval/isolation.py) | PARTIAL -- see CONT-01 |
| FR-LIB-14 | Reporter: report.md + scores.jsonl | G-08 (eval/reporter.py) | YES |
| FR-LIB-15 | Results in evals/ directory | G-08 output dir convention | YES |
| FR-AB-01 | Tier 1 Regression | G-04 (runner.py) + G-10 (commands.py) | YES |
| FR-AB-04 | CLI interface flags | G-10 (eval/commands.py) | YES |
| FR-AB-05 | --dry-run | G-10 | YES |
| FR-RE-01 | Spec parser | NOT in gap table | NO -- see GAP-01 |
| FR-RE-02 | Eval suite generator | NOT in gap table | NO -- see GAP-01 |
| FR-RE-04 | Human review pause | NOT in gap table | NO -- see GAP-02 |

### 2.2 Gaps Without Requirements (Over-Engineering Risk)

- G-09 (Extract write_state/read_state to pipeline/state.py): Not directly required by any FR but supports resume capability. **Low risk** -- it is a refactoring, not a new feature.
- G-12 (Eval gate criteria instances): Not a direct FR but enables structural validation. **Low risk** -- pure data definitions.
- G-13 (Refactor scripts/eval_runner.py): Explicitly marked as "code hygiene." No FR demands it. **Low risk** -- optional.

**Assessment**: No over-engineering risk. All gaps are motivated by either direct FRs or infrastructure cleanliness.

### 2.3 Requirements Without Infrastructure (Missing Infrastructure Risk)

See GAP-01 and GAP-02 below.

---

## Consistency Check 3: Requirements <> Architecture

**Question**: Are there requirements that no architecture component addresses?

### 3.1 FR-ID to Module Cross-Reference

| FR Group | Module(s) | Coverage |
|----------|-----------|----------|
| FR-LIB-* (15 FRs) | models.py, rubric.py, judge.py, runner.py, isolation.py, aggregator.py, reporter.py | Full |
| FR-AB-* (15 FRs) | ab_test/executor.py, ab_test/main.py, ab_test/prompts.py + library | Full |
| FR-RE-* (16 FRs) | release_eval/spec_parser.py, release_eval/suite_generator.py, release_eval/executor.py, release_eval/reporter.py + library | Full |
| FR-V3-* (10 FRs) | No architecture module | INTENTIONAL -- these are manual workflow steps (Agent 4, Section 5: "NOT a release") |
| FR-ER-* (6 FRs) | scripts/eval_runner.py (existing) | Full (already exists) |

### 3.2 Acceptance Criteria Path Check

**sc:ab-test (AC-AB-01 through AC-AB-10)**:

- AC-AB-01 through AC-AB-02: Implemented by ab_test/executor.py orchestrating runner.py with isolation.py. Clear path.
- AC-AB-03 through AC-AB-04: Implemented by reporter.py. Clear path.
- AC-AB-05: Implemented by runner.py multi-model support. Clear path.
- AC-AB-06: Implemented by aggregator.py consistency checks. Clear path.
- AC-AB-07: Implemented by isolation.py trap handlers. Clear path.
- AC-AB-08: Implemented by runner.py --dry-run mode. Clear path.
- AC-AB-09: Implemented by isolation.py lock file. Clear path.
- AC-AB-10: Implemented by aggregator.py p-value computation. Clear path.

**sc:release-eval (AC-RE-01 through AC-RE-12)**:

- AC-RE-01: Implemented by spec_parser.py. Clear path.
- AC-RE-02: Implemented by suite_generator.py. Clear path.
- AC-RE-03: Implemented by suite_generator.py fixture generation. Clear path.
- AC-RE-04: Implemented by release_eval/executor.py human pause. **Needs design** -- how does a CLI tool pause for human review? See CONT-05.
- AC-RE-05: Implemented by release_eval/executor.py layer ordering. Clear path.
- AC-RE-06 through AC-RE-08: Implemented by judge.py + reporter.py. Clear path.
- AC-RE-09 through AC-RE-10: Implemented by spec_parser.py release type detection + runner.py. Clear path.
- AC-RE-11: Implemented by runner.py spec_hash validation per D-02. Clear path.
- AC-RE-12: Design constraint, not implementation. Clear path.

**Assessment**: All ACs have implementation paths. AC-RE-04 (human review pause) needs CLI UX design but is not architecturally blocked.

### 3.3 FRs Outside Module Boundaries

- FR-AB-10 (vanilla prompt library in YAML): Lives at `tests/ab/vanilla-prompts.yml`, not inside any Python module. Agent 1 places it in `ab_test/prompts.py`. Agent 4 places it in a YAML file. These are compatible -- prompts.py loads the YAML. No conflict.
- FR-AB-15 (cost model tracking): No module explicitly owns cost reporting. It can be absorbed into reporter.py. Minor gap.

---

## Consistency Check 4: Delivery Slicing

**Question**: Is the delivery slicing consistent across all 4 analyses?

### 4.1 Seven-Slice Plan Comparison

Agent 1 (Architecture) defines 7 slices. Agent 4 (Requirements) maps each FR to a slice. Agent 3 (Infrastructure) defines a 7-phase build order. Agent 2 (Workflow) defines 6 phases.

| Agent 1 Slice | Agent 4 FR Slice Assignment | Agent 3 Build Phase | Consistent? |
|---------------|----------------------------|---------------------|-------------|
| 1: Scoring lib + single-run judge | FR-LIB-01 through FR-LIB-09 -> Slice 1 | Phase 1-2 (G-01, G-02, G-03) | YES |
| 2: Multi-run engine + aggregation | FR-LIB-10 through FR-LIB-15 -> Slice 2 | Phase 3-4 (G-04, G-05, G-07) | YES |
| 3: ab-test regression tier | FR-AB-01, FR-AB-04 through FR-AB-09, FR-AB-12 -> Slice 3 | Phase 5 (G-10, G-11) | YES |
| 4: ab-test value + deprecation | FR-AB-02, FR-AB-03, FR-AB-10 through FR-AB-14 -> Slice 4 | Phase 5 (G-10 extended) | YES |
| 5: Spec parser + suite gen | FR-RE-01 through FR-RE-03, FR-RE-14 -> Slice 5 | NOT in Agent 3 gap table | NO -- see CONT-02 |
| 6: Release eval executor | FR-RE-04 through FR-RE-16 -> Slice 6 | NOT in Agent 3 gap table | NO -- see CONT-02 |
| 7: CLI portification | No specific FRs | Phase 5 (G-10, G-11) | PARTIAL |

### 4.2 Agent 2 Stage Ordering vs Slice Dependencies

Agent 2's 6-phase pipeline (spec generation -> adversarial -> impact analysis -> validation -> execution -> scoring) is a *usage workflow*, not a *build plan*. It does not align with slices because it assumes all infrastructure already exists. This is correct -- the workflow describes how to *use* the tool, not how to *build* it.

### 4.3 Agent 3 Critical Path vs Slice Order

Agent 3 critical path: G-09 -> G-02 -> G-05 -> G-04 -> G-10 -> G-11 (6 steps, 4 phases).

This maps to Agent 1 slices: Slice 1 (G-02) -> Slice 2 (G-04, G-05) -> Slice 3 (G-10, G-11). The critical path aligns with slices 1-3.

However, Agent 3's critical path stops at G-11 (CLI registration). It does not include slices 5-6 (spec parser, release eval). This is because Agent 3's gap table omits `spec_parser.py` and `suite_generator.py` entirely (see CONT-02).

---

## Consistency Check 5: Open Decision Resolution

**Question**: Did all analyses agree on the open decisions?

### 5.1 Decision Count Discrepancy

The ground truth (conversation-decisions.md) section 13 header says "13. Open Decisions" but the table contains exactly **6** entries. Agent 1 correctly identifies this: the "13" is a section number, not a decision count. Agent 4 lists 10 decisions (D-01 through D-10), resolving the 6 original plus 4 implicit ones found across sources.

**Assessment**: All agents agree the section number is not a count. Agent 4's expansion to 10 decisions is additive, not contradictory.

### 5.2 Decision Resolution Consistency

| Decision | Agent 1 Position | Agent 4 Resolution | Consistent? |
|----------|-----------------|-------------------|-------------|
| D-01 (Min runs) | "Reconcile: 5 for quick regression, 20 for value validation?" (question) | Tiered: 5 regression, 10 value validation, 5 deprecation | YES (Agent 4 resolves the question) |
| D-02 (Suite versioning) | "Re-generate suite? Version-lock?" (question) | Version-lock with spec_hash + --regenerate | YES |
| D-03 (Concurrent isolation) | "Queue or worktree-based isolation?" (question) | File lock + worktree fallback | YES |
| D-04 (Score persistence) | "JSONL for simplicity, SQLite for querying?" (question) | JSONL primary, no SQLite in v1 | YES |
| D-05 (Vanilla prompts) | "v3.1 spec has library; need maintenance model" (question) | Hand-crafted with review requirement | YES |
| D-06 (Slice 1-2 target) | "Single release or multiple?" (question) | Ship with slice 3 as v1.0 | YES |
| D-07 (Eval runner relationship) | Not addressed | Coexist as complementary layers | N/A (Agent 1 did not cover) |
| D-08 (Skill vs CLI phasing) | "Skill first, then portify" (from source) | Python library + CLI from start | TENSION -- see CONT-03 |
| D-09 (Cross-model normalization) | "Within-model consistency, not cross-model" | Within-model only, cross-model informational | YES |
| D-10 (Docker isolation) | Not addressed | Out of scope for v1 | YES (matches source) |

### 5.3 Conflict on D-08 (Skill vs CLI Phasing)

Agent 1 (Section 1.1) faithfully reproduces the source decision: "Build the Python scoring library from day one AND build orchestration as Claude Code skills first. When proven, portify orchestration to CLI."

Agent 4 (D-08) overrides this: "Python library + CLI from the start. Skill is a thin wrapper." Agent 4 justifies this by citing the 6-prompt workflow as proof that "direct CLI invocation works" and the skill-first discovery phase is no longer needed.

Agent 3 (Section 1.4) implicitly sides with Agent 4 by specifying ClaudeProcess usage for judge agents (CLI-based, not skill-based) and never mentioning skill orchestration.

**Assessment**: See CONT-03.

---

## Contradictions Found

### CONT-01: Isolation Mechanism -- Three Modes vs Three Layers

- **Agent 1** (Section 1.7) describes three *modes*: (1) Global vs Local (skip make sync-dev), (2) Vanilla vs Skill (disable .claude/), (3) Example comparison.
- **Agent 3** (Section 5.3) describes three *layers*: (1) Worktree isolation, (2) Env-var override, (3) Directory rename.
- **Agent 4** (FR-LIB-13) requires three *isolation modes*: vanilla (all disabled), baseline (global only), candidate (global + local).
- **Severity**: WARNING
- **Resolution**: These are different taxonomies for the same concept. Agent 1's "modes" describe *what* to compare. Agent 3's "layers" describe *how* to isolate. Agent 4's "modes" describe *isolation states*. The spec should define both: isolation *mechanisms* (worktree, env-var, directory rename) and isolation *configurations* (vanilla, baseline, candidate) that compose the mechanisms. No actual conflict, but the terminology collision will confuse implementors if not clarified.

### CONT-02: Infrastructure Gap Table Omits release-eval Modules

- **Agent 1** (Section 3) specifies `spec_parser.py` and `suite_generator.py` as new modules for sc:release-eval.
- **Agent 3** (Section 3, Gap Table) lists 13 gaps (G-01 through G-13). None cover `spec_parser.py` or `suite_generator.py`.
- **Agent 4** (FR-RE-01, FR-RE-02) requires both modules at P0.
- **Severity**: BLOCKING
- **Resolution**: Agent 3's gap table is incomplete. It covers the shared eval library and the ab-test CLI but stops short of release-eval-specific modules. The spec must add at minimum: G-14 (`eval/spec_parser.py`), G-15 (`eval/suite_generator.py`). These should appear in Phase 5 of Agent 3's build order, after the shared library is complete.

### CONT-03: Skill-First vs CLI-First Build Approach

- **Agent 1** (Section 1.1): "Build orchestration as Claude Code skills first. When proven, portify to CLI."
- **Agent 4** (D-08): "Python library + CLI from the start. Skill is a thin wrapper."
- **Ground truth** (conversation-decisions.md Section 2): "Build the Python scoring library from day one AND build the orchestration as Claude Code skills first."
- **Severity**: WARNING
- **Resolution**: Agent 4's resolution is a deliberate override of the source decision, justified by subsequent evidence (the 6-prompt workflow proving CLI works). This is a legitimate decision evolution, not a contradiction. The spec should acknowledge the original decision and document the rationale for the shift. Recommend adopting Agent 4's position (CLI-first) because the 20% orchestration cost of building twice is avoidable.

### CONT-04: Runner Architecture -- pytest vs superclaude roadmap run

- **Agent 3** (Section 1.1): "The eval tool does NOT execute Claude subprocesses -- it runs `uv run pytest` via `subprocess.run()`."
- **Agent 1** (Section 7.6): "The eval runner must use ClaudeProcess... wraps ClaudeProcess in a loop/pool pattern."
- **Agent 4** (C-02 Resolution): "Two different eval systems that should coexist. Existing eval_runner.py runs pytest. New system runs actual CLI pipelines via subprocess."
- **Severity**: BLOCKING
- **Resolution**: Agent 3 conflates the existing `scripts/eval_runner.py` (pytest-based) with the new `src/superclaude/eval/runner.py` (CLI pipeline-based). The new runner must invoke `superclaude roadmap run` (or equivalent CLI commands) via subprocess, NOT pytest. Agent 1's ClaudeProcess usage is correct for judge agents and quality-layer runs. Agent 4's resolution (two coexisting systems) is the correct framing. Agent 3's gap analysis must be corrected: runner.py spawns CLI pipelines via subprocess (or ClaudeProcess for judge), not pytest.

### CONT-05: Human Review Pause in CLI

- **Agent 1** (Section 3, release-eval workflow): "REVIEW (human pause)" as a pipeline stage.
- **Agent 2** (Phase 3): "Yes -- review design before P4" as a human checkpoint.
- **Agent 3**: No mechanism described for pausing CLI execution for human review.
- **Agent 4** (FR-RE-04, AC-RE-04): "Presents generated suite for human review before execution" at P0.
- **Severity**: WARNING
- **Resolution**: The CLI needs a `--approve` or `--interactive` mode where it generates the eval suite, prints it, and waits for user confirmation (stdin prompt or a follow-up `superclaude release-eval execute` command). Agent 3's gap table should include this as a design consideration in G-10 (CLI commands). Not architecturally complex but must be explicitly designed.

### CONT-06: Value Validation Minimum Runs

- **Agent 4** (D-01): "Tier 2 Value Validation: minimum 10, default 10"
- **Agent 1** (Section 1.5): "Budget guardrails: None -- model selection controls cost"
- **Ground truth** (conversation-decisions.md Section 7): "5 runs each" for all tiers
- **Severity**: WARNING
- **Resolution**: Agent 4 increases the minimum from 5 to 10 for value validation based on statistical power analysis. This conflicts with the source's "5 each" but is a well-reasoned override. Agent 1 does not address this directly. The spec should adopt Agent 4's tiered approach but document the deviation from the original "5 each" decision with rationale.

### CONT-07: Number of Modules -- 7 vs 13 Gaps

- **Agent 1** (Section 3): 7 modules in the shared library.
- **Agent 3** (Section 7): 13 gaps (G-01 through G-13).
- **Severity**: INFO
- **Resolution**: Not a contradiction. The 7 modules are the eval library. The 13 gaps include: the 7 modules + package init (G-01) + state extraction (G-09) + CLI commands (G-10) + CLI registration (G-11) + gate criteria (G-12) + prototype refactor (G-13). The gap count exceeds the module count because it includes infrastructure work beyond the library. Consistent when properly scoped.

### CONT-08: RunResult stdout/stderr -- String vs Path

- **Agent 1** (Section 2, data model): `stdout: str`, `stderr: str` (inline content)
- **Agent 3** (Section 3.1, data model): `stdout_path: Path`, `stderr_path: Path` (file references)
- **Agent 4** (Section 6, data model): `stdout: str`, `stderr: str` (inline content)
- **Ground truth** (conversation-decisions.md Section 6): `stdout: str`, `stderr: str`
- **Severity**: INFO
- **Resolution**: Agent 3 changed the field types to avoid memory bloat, noting "(path, not content (avoid memory bloat))." This is a sensible engineering decision but deviates from the source. The spec should adopt Agent 3's `Path` approach for the implementation while maintaining `str` in the serialized JSONL (read content at serialization time). Both can coexist -- the dataclass uses `Path` internally but serializes to `str`.

### CONT-09: Output Directory for ab-test

- **Agent 1** (Section 3, ab-test layout): No explicit output directory convention for ab-test results.
- **Agent 4** (C-04 Resolution): "For ab-test results (not tied to a release), use `<output-dir>/ab-tests/<command>/<timestamp>/`"
- **Agent 3** (Section 4.3): Only describes release-eval output dir convention (`<release_dir>/evals/`).
- **Severity**: INFO
- **Resolution**: Agent 4's convention is well-reasoned and fills a gap. The spec should adopt it. No agent contradicts it.

---

## Gaps Found

### GAP-01: spec_parser.py and suite_generator.py Missing from Infrastructure

- **What's missing**: Agent 3's gap table has no entries for `src/superclaude/eval/spec_parser.py` (extract ACs/FRs/NFRs from spec markdown) or `src/superclaude/eval/suite_generator.py` (produce eval-suite.yaml from parsed spec).
- **Which document should have covered it**: Agent 3 (Infrastructure Gap Analysis)
- **Impact**: These are P0 requirements (FR-RE-01, FR-RE-02). Without them in the gap table, the build order is incomplete and effort estimation is understated. The critical path should extend through these modules for slices 5-6.

### GAP-02: Human Review Pause Mechanism

- **What's missing**: No analysis describes how the CLI pauses for human review of the generated eval suite (FR-RE-04, AC-RE-04). Is it stdin-based? Two-command workflow (generate then execute)? Interactive prompt?
- **Which document should have covered it**: Agent 3 (Infrastructure Gap Analysis) under G-10 (CLI commands) or Agent 1 (Architecture) under release-eval workflow.
- **Impact**: Minor -- UX design question, not architectural. But it is a P0 acceptance criterion, so it must be designed before implementation.

### GAP-03: Eval Suite YAML Schema Specification

- **What's missing**: Agent 1 shows an example eval-suite.yaml (Section 5, ground truth). Agent 4 references it (FR-RE-02). But no analysis formally specifies the schema -- required fields, field types, validation rules, version field.
- **Which document should have covered it**: Agent 1 (Architecture) lists "Eval-suite YAML schema" in the "Must Build New" table but does not specify it. Agent 3 does not include it as a gap item.
- **Impact**: Medium -- the suite generator needs a schema to validate against. Without formal specification, implementations may diverge.

### GAP-04: Cost Estimation and Reporting

- **What's missing**: FR-AB-15 requires cost model tracking (estimated tokens per tier). No architecture module owns cost computation. No infrastructure gap addresses it.
- **Which document should have covered it**: Agent 1 (Architecture) or Agent 3 (Infrastructure)
- **Impact**: Low -- FR-AB-15 is P2 (Slice 4). Can be absorbed into reporter.py. But it requires RunResult.tokens_used to be reliably populated, which depends on the subprocess output format.

### GAP-05: Vanilla Prompt YAML Format

- **What's missing**: FR-AB-10 requires a vanilla-equivalent prompt library in YAML. Agent 4 (D-05) specifies the file location (`tests/ab/vanilla-prompts.yml`) and authoring policy. But no analysis defines the YAML schema for this file -- how are prompts keyed? Is it command -> prompt mapping? Does it include input fixtures?
- **Which document should have covered it**: Agent 1 (Architecture) under ab-test design, or Agent 4 (Requirements) as part of FR-AB-10.
- **Impact**: Low for spec, but implementors need this before building ab_test/prompts.py.

### GAP-06: Cross-Agent Test Coverage for v3.0-Only Stages

- **What's missing**: Agent 2 (Section 7) identifies a critical coverage gap: stages 9-13 (spec-fidelity through certify) only exist on v3.0 branch. Global eval runs produce nothing for these stages. The scoring framework must handle this asymmetry. Agent 4's requirements do not include an explicit FR for "handle missing baseline stages gracefully."
- **Which document should have covered it**: Agent 4 (Requirements) should have an FR under FR-RE-* or FR-LIB-* for asymmetric stage handling.
- **Impact**: Medium -- without this, the aggregator may produce misleading comparisons or crash on missing data. Agent 2's observation is correct but not formalized as a requirement.

---

## Summary

| Category | Count | Blocking |
|----------|-------|----------|
| Contradictions | 9 | 2 (CONT-02, CONT-04) |
| Gaps | 6 | 0 (but GAP-01 is high-priority) |
| Total issues | 15 | 2 |

### Blocking Issues Requiring Resolution Before Spec

1. **CONT-02**: Agent 3's gap table must be extended with `spec_parser.py` and `suite_generator.py` entries (G-14, G-15). Without these, slices 5-6 have no infrastructure plan.

2. **CONT-04**: Agent 3's runner.py description must be corrected. The new eval runner invokes CLI pipelines (`superclaude roadmap run`) via subprocess, NOT pytest. The existing `scripts/eval_runner.py` (pytest-based) is a separate, complementary tool.

### Recommended Pre-Spec Actions

1. Amend Agent 3's gap table with G-14 (spec_parser.py, Medium effort) and G-15 (suite_generator.py, Medium effort).
2. Amend Agent 3's runner.py description to clarify it spawns CLI commands, not pytest.
3. Adopt Agent 4's D-08 resolution (CLI-first, not skill-first) as the build approach, with rationale documented.
4. Define the eval-suite.yaml schema formally before implementation begins (GAP-03).
5. Design the human review pause UX for release-eval (GAP-02).

### Overall Consistency Assessment

The 4 analyses are **substantially consistent** on architecture, data model, failure model, delivery ordering, and open decision resolution. The two blocking issues are scoping omissions in Agent 3 (infrastructure gaps), not fundamental disagreements. The non-blocking contradictions are primarily terminology differences (CONT-01, CONT-07) and deliberate decision evolution (CONT-03, CONT-06). The spec author can proceed with confidence after resolving the 2 blocking items.
