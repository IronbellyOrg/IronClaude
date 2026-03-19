---
title: "Prompt 3: Impact Analysis + Eval Design"
sequence: 3 of 6
depends_on: prompt-1 (eval-spec.md), prompt-2 (stage review summary)
produces: eval-e2e-design.md, 3 impact analyses
next_prompt: prompt-4-eval-validation.md
---

# Context (carry-forward from prior work)

## Critical Lessons
- **Rejected approach**: Unit tests on gate functions. No pipeline execution. No real artifacts. Rejected.
- **What "real eval" means**: `superclaude roadmap run` invocation, persistent disk artifacts, third-party verifiable.
- **"Design and build"**: The original objective says "design and build 3 evals." The design must include complete pseudocode sufficient for direct implementation — not just a spec that requires further design decisions.

## Pipeline Architecture
- 12 discrete steps + deviation-analysis logical phase.
- v3.0 adds: spec-fidelity, wiring-verification, deviation-analysis, remediate, certify.
- remediate/certify are conditional on spec-fidelity FAIL.

## From Prompt 1 (Spec Generation)
- **eval-spec.md location**: .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md
- **spec_type used**: new_feature
- **EVAL-SEEDED-AMBIGUITY count**: 2 ambiguities placed targeting: (1) deviation sub-entry schema omission in FR-001.4 → BLOCKING, (2) "significant findings" undefined threshold in FR-001.5 → WARNING
- **Spec-panel findings applied**: N-1 atomic write mechanism, W-1 JSON/JSONL resolution, F-1 main.py row removal, N-3 overwrite behavior, N-2 concurrency risk clarification
- **Spec-panel findings preserved**: FR-001.4 and FR-001.5 EVAL-SEEDED items flagged by panel but intentionally kept
- **Dry-run result**: PASS (10 steps listed, no warnings)
- **Functional requirements count**: 6
- **Real files referenced**: executor.py, commands.py, gates.py, main.py, convergence.py, wiring_gate.py

## From Prompt 2 (Stage Review)
- **Stage review summary**: .dev/releases/current/v3.0_unified-audit-gating/adversarial/stage-review-summary.md
- **Stages flagged as "trivially passing"**: Stage 10 (wiring-verification — all detectors find zero targets), Stage 6 (score — no semantic checks)
- **Stages flagged as "likely to fail"**: Stage 9 (convergence-enabled path bypasses gate), Stage 11 (unreachable — trigger wiring missing), Stage 12 (unreachable — doubly conditional on stage 11)
- **Coverage gaps identified**: (1) CRITICAL: remediate/certify trigger wiring absent in _build_steps(), (2) HIGH: convergence loop unexercised, (3) HIGH: wiring analysis produces empty results, (4) MEDIUM: no finding parser for remediation input, (5) MEDIUM: seeded ambiguity detection depends on convergence mode
- **Recommendations for eval design**: R1: test convergence-enabled AND disabled paths; R2: use spec that deterministically triggers remediation; R3: include wiring-relevant codebase change; R4: verify seeded ambiguity propagation post-debate; R5: specify progress schema for conditional/trailing stages; R6: add CERTIFY_GATE arithmetic consistency check

---

# Prompt

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

# Post-Run: Forward Context to Next Prompt

After this prompt completes, append the following to the **Context** section of `prompt-4-eval-validation.md`:

```markdown
## From Prompt 3 (Impact Analysis + Eval Design)
- **eval-e2e-design.md location**: .dev/releases/current/v3.0_unified-audit-gating/eval-e2e-design.md
- **3 identified impacts**: [brief one-liner per impact with code reference]
- **3 pre-v3.0 issues mitigated**: [brief one-liner per issue]
- **Eval scripts referenced**: [list scripts/eval_1.py, eval_2.py, eval_3.py if produced, or note if design-only]
- **Reflect findings**: [any deviations flagged and whether they were accepted as improvements]
- **Build status**: Were actual Python scripts produced, or only pseudocode in the design doc?
```
