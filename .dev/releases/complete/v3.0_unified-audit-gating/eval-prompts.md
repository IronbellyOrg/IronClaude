---
title: v3.0 Eval Prompts — Corrective Action (Refactored)
date: 2026-03-19
revision: 2.0 — refactored per 6 adversarial debates, 31 findings applied
context: Generated after rejection of unit-test-only evals that produced no real artifacts
---

# Conversation Review

## What was asked for (verbatim)

> "@.dev/releases/current/v3.0_unified-audit-gating/ Is complete. Create me a set of real world evals that I can run to test and validate it is functioning as expected and evaluate the impact"
>
> "Afterwards invoked /sc:adversarial and debate the strengths and weaknesses of each and refactor accordingly"
>
> "Confirm with verifiable evidence how many of the actual processes and stages of the superclaude roadmap run workflow these evals triggered and produced real world results for. Show me the output of the eval, ie: actual roadmaps that can be verified and evaluated by a third party to compare the local vs global results"

## What was generated and why it was rejected

168 pytest unit/integration tests across 5 files that:
- Tested gate validation functions (`gate_passed()`) with hand-crafted markdown fixtures
- Tested `Finding` dataclass construction and status enums
- Tested `DeviationRegistry` save/load/merge in isolation
- Tested `_build_steps()` output structure without executing any steps
- Tested wiring analyzer AST parsing on toy fixture projects

**Why rejected**: Zero of the 13 pipeline stages were actually executed. No Claude subprocess was invoked. No real extraction, roadmap, diff, debate, score, merge, test-strategy, spec-fidelity, wiring-verification, deviation-analysis, remediation, or certification artifacts were produced. There was nothing a third party could inspect or compare. The evals tested plumbing logic, not the actual workflow running. The "168/168 passed" metric was misleading — it validated Python function behavior, not roadmap pipeline behavior.

**Pattern to avoid going forward**: Any eval that:
- Uses `gate_passed()` on hand-written markdown instead of on actual pipeline output
- Tests data models in isolation instead of through the pipeline that produces them
- Claims coverage of pipeline stages without invoking `superclaude roadmap run`
- Produces no inspectable artifacts (roadmaps, diffs, debates, reports)
- Cannot be validated by a third party who wasn't present for the test run

## Pipeline Architecture Clarification

The `superclaude roadmap run` pipeline has **12 discrete steps** (produced by `_build_steps()` in executor.py) plus **deviation-analysis as a logical phase** within the spec-fidelity convergence loop (run inside `validate_executor.py`, not through `roadmap_run_step()`). The 12 steps are: extract, generate-A, generate-B, diff, debate, score, merge, test-strategy, spec-fidelity, wiring-verification, remediate, certify. Steps 11-12 (remediate, certify) are **conditional** — they only execute if spec-fidelity produces FAIL with HIGH findings.

---

# Prompt 1: Spec Generation + Panel Review

```
/sc:brainstorm "Generate a lightweight eval-purpose release specification for testing the superclaude roadmap run pipeline" --codebase --depth deep

Context: I need a small, focused spec that is specifically designed to exercise all 12 pipeline steps of the `superclaude roadmap run` pipeline (extract, generate-A, generate-B, diff, debate, score, merge, test-strategy, spec-fidelity, wiring-verification, remediate, certify) plus the deviation-analysis logical phase within the convergence loop. The spec must:

1. Conform exactly to the template at /config/workspace/IronClaude/src/superclaude/examples/release-spec-template.md
2. Set `spec_type: new_feature` to ensure correct conditional section inclusion (Section 4.5 Data Models, Section 5.1 CLI Surface)
3. Be small enough to complete a full roadmap run in < 15 minutes
4. Target real code in this repository — specifically reference these files:
   - `src/superclaude/cli/roadmap/executor.py`
   - `src/superclaude/cli/roadmap/commands.py`
   - `src/superclaude/cli/roadmap/gates.py`
   - `src/superclaude/cli/main.py`
5. Include at least 5 functional requirements with testable acceptance criteria
6. Include at least 2 intentional ambiguities designed to produce BLOCKING or WARNING findings (not INFO) in spec-fidelity — these are required to trigger the remediate and certify stages which only run on spec-fidelity FAIL. Mark each with an `<!-- EVAL-SEEDED-AMBIGUITY: description -->` HTML comment so the spec-panel preserves them during critique
7. Include a data model and architecture section that references the real files listed above
8. Set complexity_class to MEDIUM so interleave_ratio maps to 1:2

The spec's purpose is NOT to describe real work — it is an eval harness. It should be realistic enough to produce meaningful pipeline artifacts but constrained enough to keep runs fast and artifacts small.

Write the completed spec to: .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md

After the spec is written, invoke:
/sc:spec-panel --focus correctness,testability,architecture --mode critique

IMPORTANT: This spec is an eval harness. Sections marked with `<!-- EVAL-SEEDED-AMBIGUITY -->` are intentional and must be preserved — they exercise the deviation-analysis, remediation, and certification pipeline stages. Assess the spec's fitness for exercising all 12 pipeline steps, not just its quality as a release spec.

Apply any critical findings from the panel EXCEPT those targeting EVAL-SEEDED-AMBIGUITY sections. Then:
1. Verify zero remaining sentinels: `grep -c '{{SC_PLACEHOLDER:' .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md`
2. Run `superclaude roadmap run .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md --dry-run` to verify the spec is accepted by the pipeline
```

---

# Prompt 2: Per-Stage Adversarial Review

```
/sc:spawn "Review each of the 12 roadmap pipeline steps against the eval spec for testing effectiveness" --strategy parallel

Precondition: Verify .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md exists and is non-empty before spawning agents.

Spawn 12 agents. Each agent's individual prompt MUST begin with the literal text `/sc:adversarial --depth quick` followed by their assignment.

Context for all agents:
- The eval spec is at: .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md
- The v3.0 release spec is at: .dev/releases/current/v3.0_unified-audit-gating/merged-spec.md
- The pipeline implementation is at: src/superclaude/cli/roadmap/executor.py (function _build_steps, lines 396-541)
- The gate definitions are at: src/superclaude/cli/roadmap/gates.py
- Master branch diff: run `git diff master -- src/superclaude/cli/roadmap/ src/superclaude/cli/audit/` and include relevant output

Each agent must:
1. Read their gate's SemanticCheck functions from gates.py before debating
2. Address ALL 5 debate questions below

Debate questions (all 5 required per agent):
1. Will the eval spec produce meaningful output at this stage, or will the gate trivially pass/fail?
2. What does v3.0 specifically change about this stage compared to master? (For stages 1-7 which are unchanged: "Do any upstream or downstream v3.0 changes indirectly affect this stage's behavior?")
3. What artifact does this stage produce and how can a third party verify its quality?
4. What is the single most likely failure mode at this stage with this eval spec?
5. How does v3.0's change to this stage alter what the eval spec must exercise, and does the eval spec account for this?

Agent assignments (12 agents for 12 pipeline steps):
- Agent 1: `/sc:adversarial --depth quick` — extract (gate: EXTRACT_GATE, file: extraction.md)
- Agent 2: `/sc:adversarial --depth quick` — generate-A (gate: GENERATE_A_GATE, file: roadmap-{agent-a}.md)
- Agent 3: `/sc:adversarial --depth quick` — generate-B (gate: GENERATE_B_GATE, file: roadmap-{agent-b}.md)
- Agent 4: `/sc:adversarial --depth quick` — diff (gate: DIFF_GATE, file: diff-analysis.md)
- Agent 5: `/sc:adversarial --depth quick` — debate (gate: DEBATE_GATE, file: debate-transcript.md)
- Agent 6: `/sc:adversarial --depth quick` — score (gate: SCORE_GATE, file: base-selection.md)
- Agent 7: `/sc:adversarial --depth quick` — merge (gate: MERGE_GATE, file: roadmap.md)
- Agent 8: `/sc:adversarial --depth quick` — test-strategy (gate: TEST_STRATEGY_GATE, file: test-strategy.md)
- Agent 9: `/sc:adversarial --depth quick` — spec-fidelity + deviation-analysis (gate: SPEC_FIDELITY_GATE + DEVIATION_ANALYSIS_GATE, file: spec-fidelity.md — NOTE: deviation-analysis runs as a logical phase within the convergence loop, not as a separate Step. This agent covers both.)
- Agent 10: `/sc:adversarial --depth quick` — wiring-verification (gate: WIRING_GATE, file: wiring-verification.md — NOTE: this runs real static analysis via `run_wiring_analysis()`, NOT an LLM subprocess)
- Agent 11: `/sc:adversarial --depth quick` — remediate (gate: REMEDIATE_GATE — NOTE: only runs if spec-fidelity produces FAIL)
- Agent 12: `/sc:adversarial --depth quick` — certify (gate: CERTIFY_GATE — NOTE: only runs if remediate completes)

Each agent writes its debate to: .dev/releases/current/v3.0_unified-audit-gating/adversarial/stage-{N}-{stage-name}.md

After all 12 complete, synthesize a single summary (NOTE: this synthesis is an additive enhancement beyond the original objective): .dev/releases/current/v3.0_unified-audit-gating/adversarial/stage-review-summary.md
```

---

# Prompt 3: Impact Analysis + Eval Design

```
/sc:analyze @.dev/releases/current/v3.0_unified-audit-gating/merged-spec.md @src/superclaude/cli/roadmap/gates.py @src/superclaude/cli/roadmap/executor.py @src/superclaude/cli/roadmap/convergence.py @src/superclaude/cli/audit/wiring_gate.py --depth deep

Determine the top 3 biggest impacts of the v3.0 Unified Audit Gating release on the roadmap pipeline. For each impact:
1. What specific pipeline behavior changed (before v3.0 vs after) — cite specific function names, file paths, and line numbers
2. What failure mode does it mitigate — provide a standalone summary of the pre-v3.0 issue: what went wrong, how frequently, and what evidence existed of the failure
3. What measurable evidence would demonstrate the impact — must be a concrete, testable metric, not a generic statement like "improves quality"

Additionally, summarize the top 3 issues that v3.0 mitigates against the most, framed as problems (not solutions). This is a distinct deliverable from the impacts — the impacts describe what v3.0 adds, the issues describe what was broken before.

Before proceeding to brainstorm, verify: does each of the 3 impacts have a concrete code reference (file:line) and a testable failure condition? If not, refine until they do.

After the analysis completes, invoke:

/sc:brainstorm "Design the best ways to produce real-world measurable results of the superclaude roadmap run CLI pipeline running against the eval spec" --codebase --depth normal

The brainstorm should assume all evals invoke the real pipeline and produce real artifacts. Explore HOW to best demonstrate v3.0's impact — do not prescribe implementation details like subprocess calls or output paths. Those are for the design step.

Requirements:
- The eval spec from Prompt 1 (.dev/releases/current/v3.0_unified-audit-gating/eval-spec.md) is the input
- Brief spec only, not the full design

After the brainstorm, invoke:

/sc:design "Build 3 end-to-end evals that demonstrate the top 3 v3.0 impacts" --type component --format spec

The 3 evals must:
1. Each target one of the 3 identified impacts
2. Each run `superclaude roadmap run` end-to-end (not unit tests, not mocked steps)
3. Each produce artifacts that can be inspected: the actual roadmap files, gate pass/fail logs, timing data
4. Each be runnable as: `uv run python scripts/eval_{N}.py --branch local` and `--branch global`
5. Each output a structured comparison report
6. Each design must include: complete Python pseudocode, expected CLI invocations, artifact schemas, and assertion criteria — sufficient for direct implementation without further design decisions

Write the design to: .dev/releases/current/v3.0_unified-audit-gating/eval-e2e-design.md

After the design is complete, invoke:

/sc:reflect "Verify the 3 eval designs do not deviate from the brainstorm spec, and that any deviations are improvements" @.dev/releases/current/v3.0_unified-audit-gating/eval-e2e-design.md @.dev/releases/current/v3.0_unified-audit-gating/eval-spec.md
```

---

# Prompt 4: Eval Validation

```
/sc:reflect "Validate the eval designs at .dev/releases/current/v3.0_unified-audit-gating/eval-e2e-design.md"

Specifically verify each of these criteria with a PASS/FAIL verdict and evidence.

CRITICAL criteria (any FAIL = BLOCKED — do not proceed to Prompt 5 until resolved):

1. REAL EXECUTION: Does each eval invoke `superclaude roadmap run` (or equivalent pipeline execution) with actual Claude subprocess calls? Grep for subprocess, ClaudeProcess, roadmap_run_step, execute_pipeline, os.system, os.popen, Popen in the eval scripts. If any eval uses mock runners, synthetic gate-passing fixtures, or pre-written output files instead of real pipeline execution, FAIL it. Additionally, trace the eval's main() function to confirm the pipeline invocation is reachable without conditional bypasses or early returns that skip execution.

2. REAL ARTIFACTS: Does each eval produce persistent disk artifacts (extraction.md, roadmap-*.md, diff-analysis.md, debate-transcript.md, base-selection.md, roadmap.md, test-strategy.md, spec-fidelity.md, wiring-verification.md) that exist after the eval completes? If artifacts are generated in-memory or in temp dirs that are cleaned up, FAIL it.

3. THIRD-PARTY VERIFIABLE: Can someone who was not present during the eval run inspect the output directory and independently determine whether each pipeline stage produced valid output? If the eval's evidence is only pass/fail counts or log messages, FAIL it.

4. ARTIFACT PROVENANCE: The eval must write artifacts to a clean output directory (created at eval start, verified empty). After the eval completes, verify that artifact modification timestamps post-date the eval start time. If artifacts could have been pre-staged, copied from templates, or left over from a prior run, FAIL it.

REQUIRED criteria (FAIL = must fix before proceeding, but does not require Prompt 3 re-run):

5. A/B COMPARABLE: Does each eval support running against both v3.0 branch and master branch, producing output in separate directories that can be diff'd? If the eval only runs on one branch, FAIL it.

6. NO MOCKS: Grep all eval scripts for: mock, Mock, MagicMock, patch, monkeypatch, _gate_passing_content, synthetic, fake, stub, simulate. Any hits (excluding comments) are a FAIL.

7. MEASURABLE DELTA: Does each eval produce at least one quantitative quality metric (gate pass rate, deviation count, finding severity distribution) that differs between v3.0 and master? Timing alone is insufficient — it only proves v3.0 has more steps, not that the steps work correctly. If the eval only produces qualitative comparisons, FAIL it.

BLOCKING GATE: If any of criteria 1, 2, 3, or 4 receive a FAIL verdict, the overall validation status is BLOCKED. Do not proceed to Prompt 5 until all CRITICAL criteria are resolved and Prompt 4 is re-run to confirm.

Write the validation report to: .dev/releases/current/v3.0_unified-audit-gating/eval-validation-report.md

For any FAIL verdicts, include specific remediation instructions.
```

---

# Prompt 5: Parallel Execution + Scoring Framework

```
/sc:spawn "Execute v3.0 eval suite: 4 parallel eval runners + scoring framework + adversarial review" --strategy adaptive

Precondition: Verify .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md exists and eval-validation-report.md shows no BLOCKED criteria.

## Phase 1: Spawn 4 parallel eval runners

If Prompt 3 produced executable eval scripts (scripts/eval_1.py, eval_2.py, eval_3.py), run those. Otherwise, run `superclaude roadmap run` directly against the eval-spec as the eval mechanism — this is justified because the eval scripts may only exist as design documents at this point.

Agent 1 (Local Run A):
Run `superclaude roadmap run .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md --output .dev/releases/current/v3.0_unified-audit-gating/eval-runs/local-A/`
After completion, list all files produced and their sizes. Record wall-clock time.

Agent 2 (Local Run B):
Run `superclaude roadmap run .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md --output .dev/releases/current/v3.0_unified-audit-gating/eval-runs/local-B/`
After completion, list all files produced and their sizes. Record wall-clock time.

Agent 3 (Global Run A):
Create git worktree from master at `../IronClaude-eval-global-A`. Install superclaude in the worktree with `uv pip install -e .`.
Run `superclaude roadmap run .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md --output .dev/releases/current/v3.0_unified-audit-gating/eval-runs/global-A/`
NOTE: Master lacks spec-fidelity, wiring-verification, deviation-analysis, remediate, and certify stages. These should be scored as "stage not available on master" rather than "stage failed." The pipeline will produce fewer artifacts — this is expected, not an error.
After completion, list all files produced and their sizes. Record wall-clock time. Clean up worktree.

Agent 4 (Global Run B):
Create git worktree from master at `../IronClaude-eval-global-B`. Install superclaude in the worktree with `uv pip install -e .`.
Run `superclaude roadmap run .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md --output .dev/releases/current/v3.0_unified-audit-gating/eval-runs/global-B/`
Same notes as Agent 3 regarding expected missing stages.
After completion, list all files produced and their sizes. Record wall-clock time. Clean up worktree.

Partial-failure policy: Minimum 1 local + 1 global run must complete successfully to proceed. If fewer complete, report which runs failed and why. Do not block scoring if at least 2 runs (1 local + 1 global) are available.

## Phase 2: While runners are executing, generate scoring framework

While the 4 runners are in progress, the main agent must produce a scoring framework at:
.dev/releases/current/v3.0_unified-audit-gating/scoring-framework.md

The scoring framework must be DESIGNED TO DEMONSTRATE THE DELTA before and after v3.0. Lead with delta-focused requirements:

1. Define how to compute v3.0-vs-master delta for each metric — this is the framework's primary purpose
2. Define scoring thresholds: what constitutes a positive delta, neutral, negative
3. Specifically address the 5 new v3.0 pipeline stages (spec-fidelity, wiring-verification, deviation-analysis, remediate, certify) and how to score stages that don't exist on master (expected absence vs failure)
4. Define per-stage metrics (gate pass/fail, artifact size, artifact quality indicators) as supporting data for delta computation
5. Include instructions for a human evaluator to use the framework
6. Define reproducibility thresholds for run-to-run consistency
7. Include /sc:troubleshoot analysis instructions: for any negative or inconsistent deltas, the evaluator should:
   a. Identify which stage produced the delta
   b. Map the stage to the relevant section in the release spec (.dev/releases/current/v3.0_unified-audit-gating/merged-spec.md)
   c. Map the stage to the relevant source code (src/superclaude/cli/roadmap/ and src/superclaude/cli/audit/)
   d. Propose potential root causes for the negative delta
   e. Run /sc:troubleshoot on the specific code path to diagnose

## Phase 3: Adversarial review of scoring framework

After the scoring framework is written, spawn a parallel agent whose prompt begins with:

/sc:adversarial --depth standard "Review the scoring framework at .dev/releases/current/v3.0_unified-audit-gating/scoring-framework.md"

Provide it with:
- The scoring framework document
- The v3.0 release spec (.dev/releases/current/v3.0_unified-audit-gating/merged-spec.md)
- The eval spec (.dev/releases/current/v3.0_unified-audit-gating/eval-spec.md)
- The pipeline implementation (src/superclaude/cli/roadmap/executor.py, specifically _build_steps lines 396-541)
- The gate definitions (src/superclaude/cli/roadmap/gates.py)
- The convergence subsystem (src/superclaude/cli/roadmap/convergence.py)

The adversarial debate must evaluate:
1. Does the scoring framework actually measure what v3.0 changed, or does it measure generic pipeline health?
2. Are the thresholds defensible or arbitrary?
3. Can the framework distinguish "v3.0 made this better" from "LLM variance between runs"?
4. Does the troubleshoot path lead to actionable diagnosis or vague suggestions?

Write debate output to: .dev/releases/current/v3.0_unified-audit-gating/adversarial/scoring-framework-debate.md

Apply any critical findings to the scoring framework before Phase 4.

## Phase 4: Collect results

After all 4 runners and the adversarial review complete, produce a summary at:
.dev/releases/current/v3.0_unified-audit-gating/eval-runs/execution-summary.md

Include: artifact inventory per run, timing, any errors or partial failures, file size comparison table.
```

---

# Prompt 6: Scoring + Conditional Improvement Proposals

```
## Step 0: Precondition validation

Before proceeding, verify:
- .dev/releases/current/v3.0_unified-audit-gating/scoring-framework.md exists and is non-empty
- At least 2 eval-run directories exist (minimum 1 local + 1 global) under eval-runs/
- Each existing eval-run directory contains at least extraction.md and roadmap.md

If any precondition fails, STOP and report which prerequisites are unmet.

## Step 1: Score all runs

Read the scoring framework at .dev/releases/current/v3.0_unified-audit-gating/scoring-framework.md and apply its methodology to the eval run results. Follow the framework's instructions for metric computation, delta calculation, and threshold application — do not override the framework with ad-hoc formulas.

For each available eval run (local-A, local-B, global-A, global-B):
1. Inventory every artifact file produced (name, size, line count)
2. For each of the 12 pipeline steps, determine: gate passed/failed, artifact exists/missing, artifact line count
3. Apply the scoring framework metrics to compute per-stage scores

## Step 2: Compute deltas

Apply the delta computation method defined in the scoring framework. Use the framework's thresholds for what constitutes positive, neutral, and negative deltas. Use the framework's reproducibility thresholds for consistency assessment. Do not substitute hardcoded formulas.

## Step 3: Produce exhaustive report

Write to: .dev/releases/current/v3.0_unified-audit-gating/eval-runs/eval-report.md

The report must contain:
1. Per-stage scoring table (12 rows x metrics columns x available runs)
2. Delta summary table (12 rows: local avg, global avg, delta, verdict — using framework thresholds)
3. Overall v3.0 impact score (weighted per the framework's weighting scheme)
4. Reproducibility assessment (run-to-run variance for local pair and global pair, compared against framework thresholds)
5. Artifact inventory with file paths so a third party can inspect each one
6. For each stage where v3.0 adds new capability (spec-fidelity, wiring-verification, deviation-analysis, remediate, certify): explicit before/after comparison showing what master lacks
7. Errors and partial failures: any runs that did not complete all stages, with details on what failed and why
8. Wall-clock timing: per-run total and per-stage if available

## Step 4: Conditional improvement proposals

Evaluate the trigger conditions defined in the scoring framework. If the framework does not define specific trigger conditions, use these defaults:

IF any of the following conditions are true:
- Overall delta is negative (v3.0 measurably worse)
- Any new v3.0 stage (spec-fidelity, wiring, deviation, remediate, certify) produced no meaningful output
- Reproducibility falls below the framework's threshold for either local or global pair

THEN invoke:
/sc:brainstorm "Propose 5 actionable code improvements to address the poor eval results" --codebase --depth deep

The brainstorm must:
1. Reference specific files and line numbers in the superclaude package (particularly src/superclaude/cli/roadmap/ and src/superclaude/cli/audit/, but also src/superclaude/execution/ and src/superclaude/pm_agent/ if root causes are found there)
2. Each proposal must target a specific negative delta from the eval report
3. Each proposal must include: what to change, expected impact on the specific metric, and a testable acceptance criterion
4. Proposals must be ordered by expected impact (highest first)
5. Write proposals to: .dev/releases/current/v3.0_unified-audit-gating/eval-runs/improvement-proposals.md

IF all deltas are positive and reproducibility meets the framework's threshold:
Report "v3.0 Unified Audit Gating validated" with specific evidence: cite the overall delta value, per-stage delta range, reproducibility percentages for both local and global pairs, and the number of stages that produced new v3.0 capabilities. Skip the brainstorm.
```
