---
title: "Prompt 1: Eval Spec Generation + Panel Review"
sequence: 1 of 6
depends_on: none
produces: eval-spec.md
next_prompt: prompt-2-stage-review.md
---

# Context (carry-forward from prior work)

## Critical Lessons
- **Rejected approach**: 168 pytest unit tests were built that tested gate validation functions on synthetic markdown. Zero pipeline stages were executed. No real artifacts produced. This was rejected because it tested plumbing, not the workflow.
- **What "real eval" means**: Every eval must invoke `superclaude roadmap run`, produce disk artifacts (roadmaps, diffs, debates), and be verifiable by a third party inspecting the output directory.

## Pipeline Architecture
- The `superclaude roadmap run` pipeline has **12 discrete steps** produced by `_build_steps()` in `src/superclaude/cli/roadmap/executor.py`: extract, generate-A, generate-B, diff, debate, score, merge, test-strategy, spec-fidelity, wiring-verification, remediate, certify.
- **deviation-analysis** is a logical phase within the spec-fidelity convergence loop (runs inside `validate_executor.py`), NOT a discrete pipeline Step.
- **remediate and certify are conditional** — they only execute if spec-fidelity produces FAIL with HIGH findings. Without guaranteed failures in the eval spec, 3 of 5 new v3.0 stages go untested.

## v3.0 Release Context
- v3.0 adds 5 new capabilities: spec-fidelity gate, wiring-verification (static analysis), deviation-analysis, remediation tasklist, certification report.
- Release spec: `.dev/releases/current/v3.0_unified-audit-gating/merged-spec.md`
- Spec template: `/config/workspace/IronClaude/src/superclaude/examples/release-spec-template.md`

## Context to be added by this prompt's execution
<!-- APPEND-AFTER-RUN: After completing this prompt, append the following to prompt-2-stage-review.md's context section:
1. Path to the generated eval-spec.md
2. What spec_type was used
3. How many EVAL-SEEDED-AMBIGUITY tags were placed and what they target
4. Any critical findings from the spec-panel that were applied
5. Dry-run output (did the pipeline accept the spec?)
-->

---

# Prompt

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

# Post-Run: Forward Context to Next Prompt

After this prompt completes, append the following to the **Context** section of `prompt-2-stage-review.md` AND `prompt-3-impact-analysis.md`:

```markdown
## From Prompt 1 (Spec Generation)
- **eval-spec.md location**: .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md
- **spec_type used**: [record what was chosen]
- **EVAL-SEEDED-AMBIGUITY count**: [N] ambiguities placed targeting [list what they target]
- **Spec-panel findings applied**: [list any critical findings that changed the spec]
- **Spec-panel findings preserved**: [list EVAL-SEEDED items the panel flagged but were kept]
- **Dry-run result**: [PASS/FAIL and any warnings]
- **Functional requirements count**: [N]
- **Real files referenced**: [list the src/ files the spec points to]
```
