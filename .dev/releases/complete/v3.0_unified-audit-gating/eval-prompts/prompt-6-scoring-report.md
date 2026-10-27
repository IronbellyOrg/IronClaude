---
title: "Prompt 6: Scoring + Conditional Improvement Proposals"
sequence: 6 of 6
depends_on: prompt-5 (eval-runs/, scoring-framework.md)
produces: eval-report.md, optionally improvement-proposals.md
next_prompt: none (final prompt)
---

# Context (carry-forward from prior work)

## Critical Lessons
- **Rejected approach**: Unit tests, no pipeline execution, no artifacts. This prompt scores REAL pipeline run artifacts.
- **Scoring framework is authoritative**: The framework was generated in Prompt 5 and adversarially reviewed. Do NOT override its methodology with ad-hoc formulas. Follow its delta computation, thresholds, and reproducibility definitions exactly.
- **Master lacks 5 stages**: Global runs will have fewer artifacts. This is expected behavior, not a defect. Score missing stages as "not available on master."

## Pipeline Architecture
- 12 discrete steps + deviation-analysis phase.
- New in v3.0: spec-fidelity, wiring-verification, deviation-analysis, remediate, certify.

## From Prompt 5 (Parallel Execution + Scoring)
<!-- PLACEHOLDER: To be filled after Prompt 5 -->
- **Scoring framework**: .dev/releases/current/v3.0_unified-audit-gating/scoring-framework.md
- **Execution summary**: .dev/releases/current/v3.0_unified-audit-gating/eval-runs/execution-summary.md
- **Runs completed**: [pending P5]
- **Scoring framework delta methodology**: [pending P5 — THIS IS AUTHORITATIVE, follow it exactly]
- **Scoring framework reproducibility threshold**: [pending P5]

---

# Prompt

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
7. Errors and partial failures: any runs that did not complete all stages, with details
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

---

# Post-Run: Final Output

This is the last prompt. No forward context needed. The final deliverables are:
- `.dev/releases/current/v3.0_unified-audit-gating/eval-runs/eval-report.md` — exhaustive scoring report
- `.dev/releases/current/v3.0_unified-audit-gating/eval-runs/improvement-proposals.md` — only if poor results
- All eval-run artifact directories remain on disk for third-party inspection
