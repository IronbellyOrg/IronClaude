---
title: "Prompt 4: Eval Validation Gate"
sequence: 4 of 6
depends_on: prompt-3 (eval-e2e-design.md must exist)
produces: eval-validation-report.md (PASS or BLOCKED verdict)
next_prompt: prompt-5-parallel-execution.md
---

# Context (carry-forward from prior work)

## Critical Lessons
- **Rejected approach**: 168 pytest unit tests. No pipeline execution. No artifacts. Rejected.
- **This prompt exists because of that rejection.** It is the immune system of the eval suite. If it fails to catch the same pattern (mocked/simulated evals with no real execution), the entire corrective action is worthless.
- **Known escape hatches from adversarial debate**: Potemkin pipelines (real execution but trivial spec), copy-paste evals (run once, copy artifacts), checkpoint evals (real first stages, synthetic later stages), warm-cache evals (real execution but nothing to detect), timing-only deltas (measure duration, not quality).

## Pipeline Architecture
- 12 steps + deviation-analysis phase. v3.0 adds 5 new capabilities.
- Artifact provenance matters: files on disk don't prove they were produced by the pipeline.

## From Prompt 3 (Impact Analysis + Eval Design)
<!-- PLACEHOLDER: To be filled after Prompt 3 completes -->
- **eval-e2e-design.md location**: .dev/releases/current/v3.0_unified-audit-gating/eval-e2e-design.md
 ## From Prompt 3 (Impact Analysis + Eval Design)
  - **eval-e2e-design.md location**:
  .dev/releases/current/v3.0_unified-audit-gating/eval-e2e-design.md
  - **3 identified impacts**: (1) Deterministic wiring verification gate
  [executor.py:244-259, wiring_gate.py:313], (2) Convergence-controlled spec-fidelity with
  DeviationRegistry [convergence.py:50-226, executor.py:521], (3) Mode-aware rollout
  enforcement [wiring_gate.py:113-135, executor.py:248/537]
  - **3 pre-v3.0 issues mitigated**: (1) Documents pass but code modules are unwired (32
  symbols/14 files), (2) LLM severity noise indistinguishable from structural regressions,
  (3) New gates must deploy at full enforcement or not at all
  - **Eval scripts referenced**: scripts/eval_1.py, scripts/eval_2.py, scripts/eval_3.py
  (pseudocode in design doc, not yet extracted to files)
  - **Reflect findings**: D-1 convergence multi-run narrowing accepted with limitation
  noted; D-2 direct analyzer call accepted as improvement; G-1 missing multi-run regression
  phase (MEDIUM); G-2/G-3/G-4 minor clarification gaps (LOW)
  - **Build status**: Pseudocode only — complete Python in the design doc, NOT yet extracted
   to scripts/ as standalone files. Prompt 4 or 5 should extract.

---

# Prompt

```
/sc:reflect "Validate the eval designs at .dev/releases/current/v3.0_unified-audit-gating/eval-e2e-design.md"

Specifically verify each of these criteria with a PASS/FAIL verdict and evidence.

CRITICAL criteria (any FAIL = BLOCKED — do not proceed to Prompt 5 until resolved):

1. REAL EXECUTION: Does each eval invoke `superclaude roadmap run` (or equivalent pipeline execution) with actual Claude subprocess calls? Grep for subprocess, ClaudeProcess, roadmap_run_step, execute_pipeline, os.system, os.popen, Popen in the eval scripts. If any eval uses mock runners, synthetic gate-passing fixtures, or pre-written output files instead of real pipeline execution, FAIL it. Additionally, trace the eval's main() function to confirm the pipeline invocation is reachable without conditional bypasses or early returns that skip execution.

2. REAL ARTIFACTS (existence + content): Does each eval produce persistent disk artifacts (extraction.md, roadmap-*.md, diff-analysis.md, debate-transcript.md, base-selection.md, roadmap.md, test-strategy.md, spec-fidelity.md, wiring-verification.md) that exist after the eval completes? If artifacts are generated in-memory or in temp dirs that are cleaned up, FAIL it. Additionally, verify ARTIFACT CONTENT INTEGRITY: each artifact must (a) contain more than 10 non-empty lines, (b) contain at least one markdown section heading (## or ###), and (c) include domain-specific terms from the input spec (not just boilerplate template text). If any artifact is an empty file, a skeleton with only headings, or contains only generic placeholder content, FAIL it — this is the Potemkin pipeline escape hatch. Finally, if running both v3.0 and master branches, artifacts from the two runs must not be byte-identical (run `diff` on corresponding output directories); identical artifacts indicate template copying, not real pipeline execution.

3. THIRD-PARTY VERIFIABLE: Can someone who was not present during the eval run inspect the output directory and independently determine whether each pipeline stage produced valid output? If the eval's evidence is only pass/fail counts or log messages, FAIL it.

4. ARTIFACT PROVENANCE: The eval must write artifacts to a clean output directory (created at eval start, verified empty). After the eval completes, verify that artifact modification timestamps post-date the eval start time. If artifacts could have been pre-staged, copied from templates, or left over from a prior run, FAIL it.

5. MEASURABLE DELTA: Does each eval produce at least one quantitative quality metric (gate pass rate, deviation count, finding severity distribution) that differs between v3.0 and master? Timing alone is insufficient — it only proves v3.0 has more steps, not that the steps work correctly. If the eval only produces qualitative comparisons, FAIL it. Furthermore, the eval must declare its expected delta direction BEFORE execution (e.g., "v3.0 gate pass rate >= master gate pass rate" or "v3.0 deviation count > 0 when master deviation count = 0"). Post-hoc metric selection — choosing which metric to report after seeing results — is a form of p-hacking that can make any change look beneficial; if no pre-declared hypothesis exists, FAIL it.

BLOCKING GATE: If any of criteria 1, 2, 3, 4, or 5 receive a FAIL verdict, the overall validation status is BLOCKED. Do not proceed to Prompt 5 until all CRITICAL criteria are resolved and Prompt 4 is re-run to confirm.

REQUIRED criteria (FAIL = must fix before proceeding, but does not require Prompt 3 re-run):

6. A/B COMPARABLE: Does each eval support running against both v3.0 branch and master branch, producing output in separate directories that can be diff'd? If the eval only runs on one branch, FAIL it.

7. NO MOCKS: Grep all eval scripts for: mock, Mock, MagicMock, patch, monkeypatch, _gate_passing_content, synthetic, fake, stub, simulate. Any hits (excluding comments) are a FAIL.

Write the validation report to: .dev/releases/current/v3.0_unified-audit-gating/eval-validation-report.md

For any FAIL verdicts, include specific remediation instructions.
```

---

# Post-Run: Forward Context to Next Prompt

After this prompt completes, append the following to the **Context** section of `prompt-5-parallel-execution.md`:

```markdown
## From Prompt 4 (Eval Validation)
- **Validation report**: .dev/releases/current/v3.0_unified-audit-gating/eval-validation-report.md
- **Overall status**: [PASS / BLOCKED]
- **CRITICAL criteria results**: [1:PASS/FAIL, 2:PASS/FAIL, 3:PASS/FAIL, 4:PASS/FAIL, 5:PASS/FAIL]
- **REQUIRED criteria results**: [6:PASS/FAIL, 7:PASS/FAIL]
- **Remediation applied**: [list any fixes made to resolve FAILs]
- **Re-validation count**: [how many times P4 was run — 1 = first pass clean]
```
