---
title: 6-Prompt Eval Workflow Analysis -- CLI Pipeline Stage Extraction
date: 2026-03-19
source_documents:
  - .dev/releases/backlog/v5.xx_release-eval-ab-test/6PromptV3-Eval.md
  - .dev/releases/backlog/v5xx-ab-testing/eval-prompts.md
  - src/superclaude/cli/roadmap/executor.py
  - src/superclaude/cli/roadmap/gates.py
analysis_depth: deep
---

# 6-Prompt Eval Workflow Analysis

## 1. Per-Prompt Decomposition

### Prompt 1: Spec Generation + Panel Review

| Field | Value |
|-------|-------|
| **Title** | Eval Spec Generation and Panel Critique |
| **SuperClaude commands** | `/sc:brainstorm` (spec generation), `/sc:spec-panel` (critique) |
| **Input artifacts** | Release spec template (`src/superclaude/examples/release-spec-template.md`), v3.0 release spec (`merged-spec.md`) |
| **Output artifacts** | `eval-spec.md` (the eval harness spec), dry-run validation output |
| **Human-driven or automatable** | **Automatable** -- the spec generation follows a deterministic template and the panel critique applies mechanistic rules. The only human judgment is whether seeded ambiguities are preserved, but the `EVAL-SEEDED-AMBIGUITY` HTML comment convention makes this automatable via grep. |
| **CLI pipeline stage(s)** | `eval-spec-generate`, `eval-spec-validate` |

**Key requirements extracted:**
- Spec must conform to release-spec-template.md
- Must set `spec_type: new_feature`, `complexity_class: MEDIUM`
- Must include 5+ functional requirements with testable acceptance criteria
- Must include 2+ seeded ambiguities (marked with HTML comments) to trigger remediate/certify stages
- Must target real repository code (executor.py, commands.py, gates.py, main.py)
- Post-generation validation: zero sentinel placeholders (`{{SC_PLACEHOLDER:`), successful dry-run

---

### Prompt 2: Per-Stage Adversarial Review

| Field | Value |
|-------|-------|
| **Title** | 12-Agent Adversarial Review of Eval Spec vs Pipeline Stages |
| **SuperClaude commands** | `/sc:spawn` (orchestrator), `/sc:adversarial --depth quick` (per agent, x12) |
| **Input artifacts** | `eval-spec.md`, `merged-spec.md`, `executor.py` (lines 396-541), `gates.py`, git diff master output |
| **Output artifacts** | 12 per-stage debate files (`adversarial/stage-{N}-{stage-name}.md`), synthesis summary (`adversarial/stage-review-summary.md`) |
| **Human-driven or automatable** | **Automatable with caveats** -- the spawn and adversarial commands are CLI-invocable. The 5 debate questions are fixed. However, the quality of adversarial debate output is LLM-dependent and the synthesis step requires judgment. A CLI stage can orchestrate this but cannot guarantee debate quality. |
| **CLI pipeline stage(s)** | `adversarial-stage-review` (parallel, 12 agents), `adversarial-synthesis` (sequential, post-review) |

**Key requirements extracted:**
- Precondition gate: eval-spec.md must exist and be non-empty
- Each agent must read its gate's SemanticCheck functions from gates.py before debating
- All 5 debate questions are mandatory per agent (completeness check)
- Agent assignments map 1:1 to the 12 pipeline steps (extract through certify)
- Agent 9 covers both spec-fidelity AND deviation-analysis (logical phase, not separate step)
- Agent 10 (wiring-verification) runs real static analysis, not LLM subprocess
- Agents 11-12 (remediate, certify) are conditional -- only run if spec-fidelity produces FAIL

---

### Prompt 3: Impact Analysis + Eval Design

| Field | Value |
|-------|-------|
| **Title** | v3.0 Impact Analysis, Brainstorm, and 3-Eval Design |
| **SuperClaude commands** | `/sc:analyze --depth deep` (impact analysis), `/sc:brainstorm --depth normal` (eval approach), `/sc:design --type component --format spec` (eval design), `/sc:reflect` (deviation check) |
| **Input artifacts** | `merged-spec.md`, `gates.py`, `executor.py`, `convergence.py`, `wiring_gate.py`, `eval-spec.md` |
| **Output artifacts** | Impact analysis (inline), brainstorm spec (inline), `eval-e2e-design.md` (3 eval designs), reflection validation (inline) |
| **Human-driven or automatable** | **Partially human-driven** -- the analysis, brainstorm, and design steps are LLM-intensive and produce qualitative artifacts. The `/sc:reflect` step at the end is a validation gate that could be automated, but the design quality itself requires human review before proceeding. This is the most judgment-heavy prompt in the workflow. |
| **CLI pipeline stage(s)** | `impact-analysis`, `eval-brainstorm`, `eval-design`, `design-validation` |

**Key requirements extracted:**
- Top 3 impacts must have: specific code references (file:line), testable failure conditions
- Top 3 mitigated issues must be framed as problems, not solutions
- Pre-brainstorm checkpoint: verify each impact has concrete code reference + testable failure condition
- 3 evals must each: target one impact, run `superclaude roadmap run` e2e, produce inspectable artifacts
- Eval scripts runnable as: `uv run python scripts/eval_{N}.py --branch local|global`
- Each design must include: complete Python pseudocode, CLI invocations, artifact schemas, assertion criteria
- `/sc:reflect` serves as a fidelity gate between brainstorm spec and design output

---

### Prompt 4: Eval Validation

| Field | Value |
|-------|-------|
| **Title** | 7-Criteria Eval Validation with PASS/FAIL Gates |
| **SuperClaude commands** | `/sc:reflect` (validation) |
| **Input artifacts** | `eval-e2e-design.md` |
| **Output artifacts** | `eval-validation-report.md` |
| **Human-driven or automatable** | **Automatable** -- all 7 criteria have deterministic checks (grep for mocks, verify artifact paths, check subprocess invocations). This is a pure validation gate with binary PASS/FAIL outcomes. |
| **CLI pipeline stage(s)** | `eval-validation-gate` |

**7 validation criteria (detailed extraction in Section 4 below):**
- Criteria 1-4: CRITICAL (any FAIL = BLOCKED)
- Criteria 5-7: REQUIRED (FAIL = must fix, does not require Prompt 3 re-run)

---

### Prompt 5: Parallel Execution + Scoring Framework

| Field | Value |
|-------|-------|
| **Title** | 4-Runner Parallel Execution, Scoring Framework Design, Adversarial Review |
| **SuperClaude commands** | `/sc:spawn --strategy adaptive` (orchestrator), `/sc:adversarial --depth standard` (scoring framework review), `/sc:troubleshoot` (referenced in scoring framework instructions) |
| **Input artifacts** | `eval-spec.md`, `eval-validation-report.md` (must show no BLOCKED criteria), eval scripts or direct pipeline invocation |
| **Output artifacts** | 4 eval run directories (`eval-runs/local-A/`, `local-B/`, `global-A/`, `global-B/`), `scoring-framework.md`, `adversarial/scoring-framework-debate.md`, `eval-runs/execution-summary.md` |
| **Human-driven or automatable** | **Mixed** -- The 4 parallel eval runners are fully automatable (CLI invocations). The scoring framework generation is LLM-driven but follows a fixed structure. The adversarial review of the scoring framework is automatable as a command invocation but produces qualitative output. Phase 4 (result collection) is automatable. **Human checkpoint recommended** between Phase 2 (scoring framework) and Phase 3 (adversarial review) to validate the framework before debate. |
| **CLI pipeline stage(s)** | `eval-execute` (parallel, 4 runners), `scoring-framework-generate`, `scoring-adversarial-review`, `execution-summary` |

**Key requirements extracted:**
- Precondition gate: eval-spec.md exists AND eval-validation-report.md shows no BLOCKED criteria
- 4 parallel runners: 2 local (v3.0 branch), 2 global (master branch via git worktree)
- Global runners must create git worktrees, install superclaude, and clean up after
- Master lacks 5 stages (spec-fidelity, wiring, deviation, remediate, certify) -- scored as "not available" not "failed"
- Partial-failure policy: minimum 1 local + 1 global must complete to proceed
- Scoring framework must define: delta computation method, thresholds (positive/neutral/negative), per-stage metrics, reproducibility thresholds, troubleshoot instructions
- Adversarial debate must evaluate 4 specific questions about the scoring framework
- Apply critical findings from adversarial review before Phase 4

---

### Prompt 6: Scoring + Conditional Improvement Proposals

| Field | Value |
|-------|-------|
| **Title** | Score Computation, Delta Analysis, Report Generation, Conditional Improvements |
| **SuperClaude commands** | `/sc:brainstorm --depth deep` (conditional, only on poor results) |
| **Input artifacts** | `scoring-framework.md`, eval run directories (minimum 1 local + 1 global), `merged-spec.md` |
| **Output artifacts** | `eval-runs/eval-report.md`, conditionally `eval-runs/improvement-proposals.md` |
| **Human-driven or automatable** | **Mostly automatable** -- scoring application follows the framework's methodology. Delta computation is formulaic. The conditional brainstorm is the only LLM-intensive step, and it only triggers on poor results. **Human checkpoint recommended** after report generation to validate conclusions before improvement proposals are acted upon. |
| **CLI pipeline stage(s)** | `score-runs`, `compute-deltas`, `generate-report`, `conditional-improvement` |

---

## 2. Human-Driven vs Automatable Classification Summary

| Prompt | Classification | Rationale |
|--------|---------------|-----------|
| P1 | **Automatable** | Template-conformant generation + deterministic validation |
| P2 | **Automatable** | Fixed spawn pattern, fixed debate questions, deterministic synthesis |
| P3 | **Human-driven** | Qualitative impact analysis, design judgment, brainstorm creativity |
| P4 | **Automatable** | Binary PASS/FAIL criteria, grep-based checks |
| P5 | **Mixed** | Runners automatable; scoring framework needs review; adversarial automatable |
| P6 | **Mostly automatable** | Framework-driven scoring; conditional brainstorm is LLM-driven |

**Human checkpoints required:**
1. After Prompt 3 (eval design review before proceeding to validation)
2. After Prompt 5 Phase 2 (scoring framework review before adversarial debate)
3. After Prompt 6 Step 3 (report review before acting on improvement proposals)

---

## 3. CLI Pipeline Stage Map

The 6-prompt workflow codifies into 14 CLI pipeline stages organized in 6 phases.

### Phase 1: Spec Generation (from Prompt 1)

| Stage | Input(s) | Output(s) | Gate Criteria | Execution | Human Checkpoint |
|-------|----------|-----------|--------------|-----------|-----------------|
| `eval-spec-generate` | release-spec-template.md, merged-spec.md | eval-spec.md | Template conformance, 5+ FRs, 2+ seeded ambiguities, zero sentinels | Sequential | None |
| `eval-spec-validate` | eval-spec.md | dry-run output (pass/fail) | `superclaude roadmap run --dry-run` succeeds | Sequential | None |

### Phase 2: Adversarial Review (from Prompt 2)

| Stage | Input(s) | Output(s) | Gate Criteria | Execution | Human Checkpoint |
|-------|----------|-----------|--------------|-----------|-----------------|
| `adversarial-stage-review` | eval-spec.md, merged-spec.md, executor.py, gates.py | 12x stage-{N}-{name}.md | All 5 debate questions answered per agent, gate SemanticChecks read | **Parallel** (12 agents) | None |
| `adversarial-synthesis` | 12x stage debate files | stage-review-summary.md | Summary covers all 12 stages | Sequential | None |

### Phase 3: Impact Analysis + Eval Design (from Prompt 3)

| Stage | Input(s) | Output(s) | Gate Criteria | Execution | Human Checkpoint |
|-------|----------|-----------|--------------|-----------|-----------------|
| `impact-analysis` | merged-spec.md, gates.py, executor.py, convergence.py, wiring_gate.py | Impact analysis (embedded or standalone) | 3 impacts with code refs + testable conditions; 3 issues framed as problems | Sequential | None |
| `eval-brainstorm` | Impact analysis, eval-spec.md | Brainstorm spec (embedded or standalone) | Assumes real pipeline invocation, no mocks | Sequential | None |
| `eval-design` | Brainstorm spec, eval-spec.md | eval-e2e-design.md | 3 evals, each with: pseudocode, CLI invocations, artifact schemas, assertions | Sequential | None |
| `design-validation` | eval-e2e-design.md, brainstorm spec, eval-spec.md | Reflection output (inline) | No unwarranted deviations from brainstorm spec | Sequential | **Yes** -- review design before P4 |

### Phase 4: Validation Gate (from Prompt 4)

| Stage | Input(s) | Output(s) | Gate Criteria | Execution | Human Checkpoint |
|-------|----------|-----------|--------------|-----------|-----------------|
| `eval-validation-gate` | eval-e2e-design.md | eval-validation-report.md | 7 criteria: 4 CRITICAL (blocking), 3 REQUIRED. See Section 4 for details. | Sequential | None (gate is binary) |

### Phase 5: Execution + Scoring (from Prompt 5)

| Stage | Input(s) | Output(s) | Gate Criteria | Execution | Human Checkpoint |
|-------|----------|-----------|--------------|-----------|-----------------|
| `eval-execute` | eval-spec.md (or eval scripts) | 4x eval run directories with pipeline artifacts | Min 1 local + 1 global complete successfully | **Parallel** (4 runners) | None |
| `scoring-framework-generate` | merged-spec.md, eval-spec.md, executor.py, gates.py, convergence.py | scoring-framework.md | Defines delta computation, thresholds, per-stage metrics, reproducibility, troubleshoot path | Sequential (concurrent with eval-execute) | **Yes** -- review framework |
| `scoring-adversarial-review` | scoring-framework.md, merged-spec.md, eval-spec.md, executor.py, gates.py, convergence.py | scoring-framework-debate.md | 4 adversarial questions answered | Sequential (after framework) | None |
| `execution-summary` | 4x eval run directories, adversarial debate | execution-summary.md | Artifact inventory, timing, errors documented | Sequential (after all Phase 5 stages) | None |

### Phase 6: Scoring + Reporting (from Prompt 6)

| Stage | Input(s) | Output(s) | Gate Criteria | Execution | Human Checkpoint |
|-------|----------|-----------|--------------|-----------|-----------------|
| `score-runs` | scoring-framework.md, eval run directories | Per-run scoring data (embedded in report) | Framework methodology applied consistently | Sequential | None |
| `compute-deltas` | Per-run scoring data | Delta tables (embedded in report) | Framework thresholds applied | Sequential | None |
| `generate-report` | All scoring + delta data | eval-report.md | 8 required report sections (see Section 5) | Sequential | **Yes** -- review before acting |
| `conditional-improvement` | eval-report.md, merged-spec.md | improvement-proposals.md (conditional) | Only triggers if: negative delta, empty v3.0 stage output, or below reproducibility threshold | Sequential (conditional) | None |

---

## 4. Validation Criteria Extraction (Prompt 4 -- 7 Criteria)

### CRITICAL Criteria (any FAIL = BLOCKED)

**Criterion 1: REAL EXECUTION**
- Check: Each eval invokes `superclaude roadmap run` (or equivalent) with actual Claude subprocess calls
- Grep targets: `subprocess`, `ClaudeProcess`, `roadmap_run_step`, `execute_pipeline`, `os.system`, `os.popen`, `Popen`
- Additional: Trace `main()` to confirm pipeline invocation is reachable without conditional bypasses or early returns
- FAIL condition: Mock runners, synthetic gate-passing fixtures, or pre-written output files

**Criterion 2: REAL ARTIFACTS**
- Check: Each eval produces persistent disk artifacts that exist after completion
- Required artifacts: extraction.md, roadmap-*.md, diff-analysis.md, debate-transcript.md, base-selection.md, roadmap.md, test-strategy.md, spec-fidelity.md, wiring-verification.md
- FAIL condition: Artifacts generated in-memory or in temp dirs that are cleaned up

**Criterion 3: THIRD-PARTY VERIFIABLE**
- Check: An absent third party can inspect the output directory and determine whether each stage produced valid output
- FAIL condition: Evidence is only pass/fail counts or log messages (no inspectable artifacts)

**Criterion 4: ARTIFACT PROVENANCE**
- Check: Clean output directory created at eval start (verified empty), artifact modification timestamps post-date eval start time
- FAIL condition: Pre-staged artifacts, copied templates, or leftover artifacts from prior runs

### REQUIRED Criteria (FAIL = must fix, does not block Prompt 3 re-run)

**Criterion 5: A/B COMPARABLE**
- Check: Each eval supports `--branch local` and `--branch global`, producing output in separate directories
- FAIL condition: Eval only runs on one branch

**Criterion 6: NO MOCKS**
- Check: Grep all eval scripts for: `mock`, `Mock`, `MagicMock`, `patch`, `monkeypatch`, `_gate_passing_content`, `synthetic`, `fake`, `stub`, `simulate`
- FAIL condition: Any hits (excluding comments)

**Criterion 7: MEASURABLE DELTA**
- Check: Each eval produces at least one quantitative quality metric (gate pass rate, deviation count, finding severity distribution) that differs between v3.0 and master
- FAIL condition: Only timing differences or only qualitative comparisons

---

## 5. Scoring Framework Requirements (Prompt 5-6)

### Framework Structure (from Prompt 5)

The scoring framework must define:

1. **Delta computation method** -- how to compute v3.0-vs-master delta per metric (this is the framework's primary purpose)
2. **Thresholds** -- what constitutes positive, neutral, negative delta values
3. **New-stage handling** -- how to score the 5 v3.0-only stages (spec-fidelity, wiring-verification, deviation-analysis, remediate, certify) when they do not exist on master ("expected absence" vs "failure")
4. **Per-stage metrics** -- gate pass/fail, artifact size, artifact quality indicators (supporting data for delta)
5. **Human evaluator instructions** -- how to use the framework manually
6. **Reproducibility thresholds** -- run-to-run consistency requirements
7. **Troubleshoot instructions** -- for negative or inconsistent deltas:
   - Identify which stage produced the delta
   - Map stage to release spec section
   - Map stage to source code (src/superclaude/cli/roadmap/ and src/superclaude/cli/audit/)
   - Propose potential root causes
   - Run `/sc:troubleshoot` on the specific code path

### Report Requirements (from Prompt 6)

The eval report must contain 8 sections:
1. Per-stage scoring table (12 rows x metrics x available runs)
2. Delta summary table (12 rows: local avg, global avg, delta, verdict)
3. Overall v3.0 impact score (weighted per framework)
4. Reproducibility assessment (run-to-run variance for local pair and global pair)
5. Artifact inventory with file paths for third-party inspection
6. Before/after comparison for 5 new v3.0 stages
7. Errors and partial failures
8. Wall-clock timing (per-run total and per-stage if available)

### Conditional Improvement Trigger Conditions (from Prompt 6)

Improvement proposals (via `/sc:brainstorm --depth deep`) trigger if ANY of:
- Overall delta is negative (v3.0 measurably worse than master)
- Any new v3.0 stage produced no meaningful output
- Reproducibility falls below the framework's threshold for either local or global pair

If all deltas are positive and reproducibility meets threshold: report "v3.0 Unified Audit Gating validated" with specific evidence (overall delta value, per-stage delta range, reproducibility percentages, number of new-capability stages).

Improvement proposals must:
- Reference specific files and line numbers in superclaude package
- Target a specific negative delta from the eval report
- Include: what to change, expected metric impact, testable acceptance criterion
- Be ordered by expected impact (highest first)

---

## 6. Per-Stage Adversarial Review Structure (12 Agents from Prompt 2)

### Agent Assignments

| Agent | Pipeline Step | Gate | Artifact | Notes |
|-------|-------------|------|----------|-------|
| 1 | extract | EXTRACT_GATE | extraction.md | |
| 2 | generate-A | GENERATE_A_GATE | roadmap-{agent-a}.md | |
| 3 | generate-B | GENERATE_B_GATE | roadmap-{agent-b}.md | |
| 4 | diff | DIFF_GATE | diff-analysis.md | |
| 5 | debate | DEBATE_GATE | debate-transcript.md | |
| 6 | score | SCORE_GATE | base-selection.md | |
| 7 | merge | MERGE_GATE | roadmap.md | |
| 8 | test-strategy | TEST_STRATEGY_GATE | test-strategy.md | |
| 9 | spec-fidelity + deviation-analysis | SPEC_FIDELITY_GATE + DEVIATION_ANALYSIS_GATE | spec-fidelity.md | Deviation-analysis is a logical phase within convergence loop, not a separate step |
| 10 | wiring-verification | WIRING_GATE | wiring-verification.md | Runs real static analysis via `run_wiring_analysis()`, not LLM subprocess |
| 11 | remediate | REMEDIATE_GATE | remediation-tasklist.md | Conditional: only runs if spec-fidelity FAIL |
| 12 | certify | CERTIFY_GATE | certification-report.md | Conditional: only runs if remediate completes |

### Required Debate Questions (all 5 mandatory per agent)

1. Will the eval spec produce meaningful output at this stage, or will the gate trivially pass/fail?
2. What does v3.0 specifically change about this stage compared to master? (For unchanged stages 1-7: "Do any upstream or downstream v3.0 changes indirectly affect this stage's behavior?")
3. What artifact does this stage produce and how can a third party verify its quality?
4. What is the single most likely failure mode at this stage with this eval spec?
5. How does v3.0's change to this stage alter what the eval spec must exercise, and does the eval spec account for this?

---

## 7. Roadmap Pipeline Stage to Eval Coverage Map

This maps each of the 13 pipeline stages (12 steps + deviation-analysis logical phase) to how they are tested across the 6-prompt workflow.

| Pipeline Stage | Gate | v3.0 New? | Eval Coverage | Tested By |
|---------------|------|-----------|---------------|-----------|
| extract | EXTRACT_GATE | No | Direct -- eval spec runs through extraction | P5 eval runners, P2 Agent 1 adversarial |
| generate-A | GENERATE_A_GATE | No | Direct -- produces roadmap-A artifact | P5 eval runners, P2 Agent 2 adversarial |
| generate-B | GENERATE_B_GATE | No | Direct -- produces roadmap-B artifact | P5 eval runners, P2 Agent 3 adversarial |
| diff | DIFF_GATE | No | Direct -- compares two roadmaps | P5 eval runners, P2 Agent 4 adversarial |
| debate | DEBATE_GATE | No | Direct -- adversarial debate on diffs | P5 eval runners, P2 Agent 5 adversarial |
| score | SCORE_GATE | No | Direct -- scores and selects base variant | P5 eval runners, P2 Agent 6 adversarial |
| merge | MERGE_GATE | No | Direct -- produces final merged roadmap | P5 eval runners, P2 Agent 7 adversarial |
| test-strategy | TEST_STRATEGY_GATE | No | Direct -- generates test strategy | P5 eval runners, P2 Agent 8 adversarial |
| spec-fidelity | SPEC_FIDELITY_GATE | **Yes** | Direct -- validates merged roadmap against spec. Seeded ambiguities in eval spec designed to trigger FAIL. | P5 eval runners (local only), P2 Agent 9 adversarial |
| deviation-analysis | DEVIATION_ANALYSIS_GATE | **Yes** | Indirect -- logical phase within convergence loop, exercised when spec-fidelity finds deviations | P5 eval runners (local only), P2 Agent 9 adversarial |
| wiring-verification | WIRING_GATE | **Yes** | Direct -- runs real static analysis via `run_wiring_analysis()` | P5 eval runners (local only), P2 Agent 10 adversarial |
| remediate | REMEDIATE_GATE | **Yes** | Conditional -- only triggers on spec-fidelity FAIL (seeded ambiguities designed to cause this) | P5 eval runners (local only, conditional), P2 Agent 11 adversarial |
| certify | CERTIFY_GATE | **Yes** | Conditional -- only triggers after remediate completes | P5 eval runners (local only, conditional), P2 Agent 12 adversarial |

**Master branch coverage gap:** Stages 9-13 (spec-fidelity through certify) do not exist on master. Global eval runs will produce 0 artifacts for these stages. The scoring framework must handle this as "stage not available" rather than "stage failed," and the delta computation must account for this structural asymmetry (v3.0 has 5 additional stages that master cannot produce).

**Conditional stage risk:** If the eval spec's seeded ambiguities are not severe enough to trigger spec-fidelity FAIL, then remediate (stage 11) and certify (stage 12) will never execute. The eval spec design in Prompt 1 is critical to ensuring these stages are exercised. This is the primary reason for the 2+ seeded ambiguity requirement.

---

## 8. Pipeline Dependency Graph

```
Phase 1: Spec Generation
  eval-spec-generate --> eval-spec-validate
                              |
Phase 2: Adversarial Review   |
  adversarial-stage-review ---+--- (parallel, 12 agents)
           |
  adversarial-synthesis
           |
Phase 3: Impact Analysis + Design
  impact-analysis --> eval-brainstorm --> eval-design --> design-validation
                                                              |
Phase 4: Validation Gate                                      |
  eval-validation-gate  <-------------------------------------+
           |
           | (BLOCKED if any CRITICAL criterion fails)
           |
Phase 5: Execution + Scoring
  eval-execute  --------+--- (parallel, 4 runners)
  scoring-framework  ---+--- (concurrent with eval-execute)
           |
  scoring-adversarial-review
           |
  execution-summary
           |
Phase 6: Scoring + Reporting
  score-runs --> compute-deltas --> generate-report
                                        |
                                        +--> conditional-improvement (only on poor results)
```

**Parallelism opportunities:**
- Phase 2: 12 agents run in parallel
- Phase 5: 4 eval runners + scoring framework generation run concurrently
- Phases 2 and 3 are independent and could theoretically run in parallel, but Phase 3 benefits from Phase 2's findings

**Sequential dependencies:**
- Phase 4 blocks on Phase 3 (eval designs must exist before validation)
- Phase 5 blocks on Phase 4 (validation must pass before execution)
- Phase 6 blocks on Phase 5 (runs must complete before scoring)

**Blocking gates:**
- `eval-spec-validate`: dry-run must succeed
- `eval-validation-gate`: 4 CRITICAL criteria must PASS
- `eval-execute`: minimum 1 local + 1 global run must complete
- `conditional-improvement`: only triggers on negative/inconsistent results

---

## 9. Observations and Risks

### Structural observations

1. **The workflow is a meta-eval** -- it generates the eval spec (P1), validates the spec's fitness (P2), designs the evals (P3), validates the eval designs (P4), runs the evals (P5), and scores the results (P6). This is a full eval lifecycle, not just eval execution.

2. **Prompt 3 is the bottleneck** -- it is the only prompt classified as human-driven and it produces the eval designs that everything downstream depends on. If the designs are poor, Prompt 4 will catch them but remediation loops back to Prompt 3.

3. **The A/B comparison is structurally asymmetric** -- v3.0 has 13 stages, master has 8. The scoring framework must handle 5 stages that produce artifacts on one branch and nothing on the other. This is not a typical A/B test where both branches run the same pipeline.

4. **Seeded ambiguities are the only mechanism for testing conditional stages** -- if the ambiguities do not trigger spec-fidelity FAIL, stages 11-12 go untested. This is a single point of failure in eval coverage.

### Risks for CLI codification

1. **LLM variance** -- Prompts 1, 2, 3, 5 (scoring framework), and 6 (conditional brainstorm) all involve LLM generation. Run-to-run variance means the CLI pipeline's output will not be deterministic. The reproducibility thresholds in the scoring framework are the only mitigation.

2. **Cost** -- 4 parallel `superclaude roadmap run` invocations, each spawning Claude subprocesses for 12 pipeline steps, plus 12 adversarial agents, plus scoring framework generation, plus adversarial review. This is a significant compute cost per eval run.

3. **Time** -- Each roadmap run takes ~15 minutes minimum. With 4 parallel runs + setup/teardown, Phase 5 alone is 20-30 minutes. The full 6-prompt workflow is likely 60-90 minutes end-to-end.

4. **Git worktree management** -- Global runs require creating, installing into, and cleaning up git worktrees. Failure to clean up worktrees leaks disk space and can cause git state issues.
