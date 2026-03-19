---
title: "v3.0 Eval Improvement Proposals"
date: 2026-03-19
prompt_sequence: 6 of 6
trigger: "CONDITIONAL_PASS — spec-fidelity gate FAIL blocks wiring-verification; R-8 N/A"
proposals: 3
priority_order: [IP-1, IP-2, IP-3]
---

# v3.0 Eval Improvement Proposals

These proposals address the structural issues that prevent the eval from achieving a full PASS.

---

## IP-1: Fix LLM Requirement ID Fabrication in Generate Prompts

**Priority**: HIGH (blocks spec-fidelity gate, which blocks wiring-verification execution)

**Problem**: Both local eval runs produced roadmaps where the LLM fabricated requirement IDs (FR-001..FR-010, NFR-001..NFR-005, OQ-001..OQ-005) instead of using the spec's actual IDs (FR-EVAL-001.1..FR-EVAL-001.6, NFR-EVAL-001.1..NFR-EVAL-001.3). This is a reproducible behavior -- both local-A and local-B exhibited the same pattern. The spec-fidelity gate correctly flagged these as 3 HIGH severity deviations.

**Root cause**: The generate prompt (`build_generate_prompt()` in `src/superclaude/cli/roadmap/prompts.py`) does not instruct the LLM to preserve the spec's exact requirement ID scheme. LLMs naturally renumber and relabel when generating structured documents.

**Proposed fix**: Add an explicit instruction to the generate prompt template:

```
CRITICAL: You MUST use the exact requirement identifiers from the spec.
Do NOT renumber, relabel, or create new requirement IDs.
If the spec defines "FR-EVAL-001.1", use "FR-EVAL-001.1" verbatim.
Do NOT create your own numbering scheme (e.g., FR-001, NFR-001, OQ-001).
```

**Expected impact**: Eliminates the 3 HIGH deviations that cause spec-fidelity to FAIL, allowing the pipeline to reach wiring-verification. This would convert 3 metrics (W-1, W-8, W-9) from code-analysis evidence to pipeline-execution evidence, and make R-8 scorable.

**Validation**: Re-run local eval after prompt fix. spec-fidelity gate should PASS with 0 HIGH deviations (MEDIUM and LOW deviations are acceptable -- the gate only blocks on HIGHs).

---

## IP-2: Add Spec-Fidelity Bypass for Eval Runs

**Priority**: MEDIUM (operational improvement for eval execution)

**Problem**: The spec-fidelity gate is a blocking gate that prevents wiring-verification from executing. In eval contexts, this creates a chicken-and-egg problem: we cannot score wiring-verification metrics from pipeline execution because the LLM consistently fabricates requirement IDs.

**Root cause**: The pipeline treats spec-fidelity as a hard blocker for all subsequent steps. While this is correct behavior for production use (you should not generate tasklists from a roadmap with HIGH deviations), it is overly restrictive for eval scenarios where we want to exercise all pipeline steps.

**Proposed fix**: Add an `--eval-mode` flag to `superclaude roadmap run` that:
1. Runs spec-fidelity normally (produces the artifact and gate verdict)
2. Records the gate verdict in .roadmap-state.json
3. Logs a WARNING if the gate FAILS but continues to the next step
4. Does NOT affect the final pipeline status (still reports FAIL)

This is different from `--no-validate` (which skips spec-fidelity entirely). Eval mode runs the gate, records the failure, but does not block subsequent steps.

**Expected impact**: Allows full pipeline execution in eval runs, enabling all 31 metrics to be scored from pipeline evidence rather than code analysis.

**Risk**: Low. The eval-mode flag is opt-in and does not change production behavior. The gate failure is still recorded and reported.

---

## IP-3: Add Pipeline Stdout/Stderr Capture for R-8 Scoring

**Priority**: LOW (affects 1 metric)

**Problem**: Metric R-8 ("Pipeline output references trailing/shadow") requires evidence from pipeline stdout/stderr, but the eval runs do not capture stdout/stderr to files.

**Root cause**: The pipeline executor writes step output to .md files and state to .json, but does not capture the pipeline's own stdout/stderr stream. The `--progress-file` feature (from the eval-spec itself) would address this, but it is the feature being evaluated -- circular dependency.

**Proposed fix**: Add a `--log-file` option to `superclaude roadmap run` that captures pipeline-level log output (step transitions, gate verdicts, timing) to a structured file. This would provide:
- Evidence for R-8 (grep for "trailing" or "shadow" in the log)
- General observability improvement for all pipeline runs
- Audit trail for eval scoring

**Expected impact**: R-8 becomes scorable, converting it from N/A to PASS/FAIL. Overall impact on the delta score is minimal (1 metric out of 31).

---

## Summary

| Proposal | Priority | Effort | Impact on Score |
|----------|----------|--------|----------------|
| IP-1: Fix requirement ID fabrication | HIGH | Low (prompt edit) | Converts CONDITIONAL_PASS to full PASS path |
| IP-2: Add eval-mode bypass | MEDIUM | Medium (CLI flag + executor logic) | Enables complete pipeline execution in evals |
| IP-3: Add log-file capture | LOW | Low (logging addition) | Scores 1 additional metric (R-8) |

**Recommended action**: Implement IP-1 first. If the generate prompts produce roadmaps with correct requirement IDs, spec-fidelity will PASS and wiring-verification will execute naturally without needing IP-2. IP-3 is a nice-to-have for observability but does not affect the release decision.
