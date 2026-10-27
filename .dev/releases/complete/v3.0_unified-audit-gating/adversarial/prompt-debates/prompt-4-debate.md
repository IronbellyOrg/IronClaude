---
title: "Adversarial Debate: Prompt 4 (Eval Validation Gate)"
date: 2026-03-19
depth: standard
prompt_under_review: "Prompt 4 from eval-prompts.md"
debate_axes: [fidelity, scope, grep-validity, evidence-quality, remediation, escape-hatches]
verdict: CONDITIONAL PASS — strong structural coverage with 3 critical blind spots
---

# Adversarial Debate: Prompt 4 — Eval Validation Gate

## Role of Prompt 4 in the Pipeline

Prompt 4 is the validation gate for the entire 6-prompt eval suite. It exists because the previous eval attempt (168 pytest tests) was rejected for producing zero real pipeline artifacts. If Prompt 4 fails to catch that exact failure pattern, the entire corrective action is compromised. This prompt is the immune system of the eval suite.

---

## Axis 1: Fidelity to Original Requirements

### Original (verbatim from 6PromptV3-Eval.md)

> "Use /sc:reflect to validate the evals generated, specifically that they perform real world tests, that those tests generate REAL eval generated evidence that they were run and not mocked or simulated, that a 3rd party can validate, and that the results they produce are also verifiable."

### Mapping to Generated Criteria

| Original Requirement | Generated Criterion | Coverage |
|---|---|---|
| (a) "real world tests" | Criterion 1: REAL EXECUTION | COVERED — checks for `superclaude roadmap run` invocation, subprocess calls |
| (b) "REAL eval generated evidence that they were run" | Criterion 2: REAL ARTIFACTS | PARTIAL — checks artifact existence but not evidence-of-execution |
| (c) "not mocked or simulated" | Criterion 5: NO MOCKS | COVERED — grep-based mock detection |
| (d) "a 3rd party can validate" | Criterion 3: THIRD-PARTY VERIFIABLE | COVERED — inspectable output directory requirement |
| (e) "results they produce are also verifiable" | Criterion 6: MEASURABLE DELTA | TANGENTIAL — measurability is not the same as verifiability |

### Verdict: 3 of 4 core requirements are well-covered. Requirement (b) is weakened.

**Argument FOR the generated prompt**: The original says "evidence that they were run." The generated prompt interprets this as "persistent disk artifacts exist." This is a reasonable operationalization. If `extraction.md`, `roadmap.md`, `debate-transcript.md` etc. exist on disk, that is evidence the pipeline ran.

**Argument AGAINST**: The original specifically says "REAL eval generated evidence" (emphasis on REAL, capitalized in the original). Artifacts existing on disk is necessary but not sufficient. A script could copy template artifacts to disk without running the pipeline. The generated prompt checks for mock patterns in the eval code but does not verify that the artifacts themselves carry evidence of real execution (timestamps, process metadata, Claude model signatures, unique content that could not have been pre-written).

**Resolution**: The combination of Criterion 1 (code must invoke real execution) and Criterion 2 (artifacts must exist) together are strong, but neither individually verifies the causal chain: "this specific artifact was produced by this specific pipeline run." This gap matters.

---

## Axis 2: Over-specification vs Under-specification

The original has 4 broad requirements. The generated prompt has 6 specific criteria. The two additions are:

### Criterion 4: A/B COMPARABLE
- **Source**: Not in the original Prompt 4 text. However, Prompt 3 requires evals be "runnable on both v3.0 branch and master branch." Prompt 5 runs 4 parallel agents (2 local, 2 global). Prompt 6 computes deltas.
- **Assessment**: This is not scope creep. It is a structural dependency. If Prompt 4 does not validate A/B comparability, Prompts 5 and 6 will fail at runtime. Including it here as a pre-flight check is defensive and correct.
- **Risk**: Minimal. An eval that passes criteria 1-3 and 5-6 but fails criterion 4 should indeed be flagged and fixed before Prompt 5.

### Criterion 6: MEASURABLE DELTA
- **Source**: Not in the original Prompt 4 text. Derived from Prompt 6's requirement to "compute deltas" and produce "per-stage scoring."
- **Assessment**: This is mild scope creep, but defensible. The original says "results they produce are also verifiable." A purely qualitative result ("v3.0 seems better") is technically verifiable but not rigorously so. Requiring at least one quantitative metric per eval raises the bar appropriately.
- **Risk**: Could over-constrain eval design. Some legitimate v3.0 improvements (e.g., "spec-fidelity stage now catches ambiguities that master misses") might be best demonstrated through qualitative artifact comparison rather than a single numeric metric. Forcing a number could lead to a meaningless metric (e.g., "word count of spec-fidelity.md") that passes the criterion but adds no signal.

### Verdict: Criteria 4 and 6 are justified additions, not scope creep. Criterion 6 carries a minor risk of metric gaming.

---

## Axis 3: Grep-based Validation — Sufficiency and Failure Modes

The prompt relies on two grep strategies:
1. **Positive grep** (Criterion 1): Search for `subprocess`, `ClaudeProcess`, `roadmap_run_step`, `execute_pipeline` to confirm real execution.
2. **Negative grep** (Criterion 5): Search for `mock`, `Mock`, `MagicMock`, `patch`, `monkeypatch`, `_gate_passing_content`, `synthetic`, `fake`, `stub`, `simulate` to detect mock usage.

### Strengths

- The positive grep terms are well-chosen. `ClaudeProcess` and `roadmap_run_step` are the actual implementation entry points (confirmed in `src/superclaude/cli/roadmap/executor.py` lines 1-26). An eval that calls these is almost certainly running the real pipeline.
- The negative grep term `_gate_passing_content` is a clever inclusion — it targets the specific anti-pattern of hand-crafting markdown that passes gate checks.
- Excluding comments from the negative grep avoids false positives from docstrings explaining what the eval does NOT do.

### Weaknesses

**Weakness 1: Indirection bypass.** An eval could import a wrapper function that internally calls `subprocess.run(["claude", ...])` but the eval script itself contains none of the grepped terms. The eval script might just call `run_evaluation()` imported from a helper module. The grep would miss this entirely.

**Mitigation**: The prompt could require that the grep be recursive across all files in the eval directory, not just the top-level scripts.

**Weakness 2: Dead code.** An eval script could contain `import subprocess` and `from superclaude.cli.pipeline.process import ClaudeProcess` at the top but never actually call them. The positive grep would pass. The eval could then read pre-staged artifacts from a fixtures directory.

**Mitigation**: Static grep cannot detect dead imports. This requires either (a) actually running the eval and observing execution, or (b) AST-based analysis to verify the imports are used in the execution path. Neither is specified.

**Weakness 3: Shell delegation.** An eval could use `os.system("superclaude roadmap run ...")` which would not match any of the grepped terms (`subprocess`, `ClaudeProcess`, etc.). Similarly, `os.popen`, `Popen` (without `subprocess.` prefix), or `shutil` wrappers would evade the grep.

**Mitigation**: Add `os.system`, `os.popen`, `Popen`, `shutil` to the positive grep, or more practically, require the eval to use the Python API (`execute_pipeline`) rather than shell commands.

### Verdict: Grep-based validation is a necessary heuristic but not a sufficient proof. It catches the obvious failure pattern (pure unit tests with mocks) but can be bypassed by moderately sophisticated eval designs. The prompt should acknowledge this limitation.

---

## Axis 4: Evidence Quality — "Run Evidence" vs "Artifact Existence"

### What the original requires
"REAL eval generated evidence that they were run"

### What the generated prompt checks
Criterion 2 checks that files like `extraction.md`, `roadmap.md`, etc. exist on disk after the eval completes.

### The gap

Artifact existence proves that files were written. It does not prove:
1. **When** they were written (could be pre-staged)
2. **By what** they were written (could be a `touch` command or template copy)
3. **During which run** they were written (could be leftover from a previous run)

### What would close the gap

The prompt should require at least one of:
- **Timestamp verification**: Artifact modification times must post-date the eval invocation time.
- **Content uniqueness**: Artifacts must contain content that could only have been generated by a Claude subprocess (e.g., model-specific reasoning, references to the eval spec's specific requirements).
- **Process correlation**: The eval must log the PID or session ID of the Claude subprocess, and the artifact must contain a matching identifier.
- **Fresh directory requirement**: The eval must write to a clean output directory (created at eval start), not an existing directory that might contain prior artifacts.

### The rejected eval pattern revisited

The 168 pytest tests that were rejected used "hand-crafted markdown fixtures." Criterion 2 as written would catch this only if the hand-crafted fixtures are not named with the exact artifact filenames. If someone hand-crafts an `extraction.md` and writes it to the output directory, Criterion 2 would PASS. Criterion 1 would need to catch that the extraction was not produced by `superclaude roadmap run`. But Criterion 1 only checks the eval code, not the artifacts themselves.

### Verdict: The prompt checks artifact existence but not artifact provenance. This is the single largest gap.

---

## Axis 5: Remediation Path

The generated prompt says: "For any FAIL verdicts, include specific remediation instructions."

### Strengths
- Requiring remediation instructions is better than just PASS/FAIL.
- Writing to a report file (`eval-validation-report.md`) creates an auditable record.

### Weaknesses

**No re-validation loop.** The prompt produces a report with remediation instructions, but does not trigger a re-design and re-validation cycle. If 2 of 6 criteria FAIL, the report is written and... then what? The user must manually re-run Prompt 3 to redesign the failing evals, then re-run Prompt 4 to re-validate.

**No severity weighting.** A FAIL on Criterion 1 (REAL EXECUTION) is catastrophic — it means the eval is fundamentally worthless. A FAIL on Criterion 6 (MEASURABLE DELTA) might mean the eval demonstrates impact qualitatively but lacks a numeric metric. These are not equivalent failures, but the prompt treats them identically.

**No blocking gate.** The prompt does not state that Prompt 5 must not proceed if Prompt 4 has any FAIL verdicts. This is arguably outside Prompt 4's scope (it is the responsibility of the human operator), but given the pipeline structure and the fact that this prompt exists because the previous evals were not validated, an explicit gate would be appropriate.

### Recommendation

Add: "If any of criteria 1, 2, or 3 FAIL, mark the overall validation as BLOCKED. Do not proceed to Prompt 5 until these are resolved. Criteria 4, 5, and 6 are REQUIRED but can be fixed in-place without re-running Prompt 3."

### Verdict: Remediation instructions are necessary but insufficient. A re-validation loop and severity tiering would strengthen the gate significantly.

---

## Axis 6: What Would This Prompt NOT Catch?

Five scenarios where a fake or insufficient eval could pass all 6 criteria:

### Scenario 1: "The Potemkin Pipeline"
An eval script imports `ClaudeProcess` and `execute_pipeline` (passes Criterion 1 grep), calls `superclaude roadmap run` against the eval spec (passes Criterion 1), produces all required artifacts (passes Criterion 2), writes them to an inspectable directory (passes Criterion 3), supports `--branch local` and `--branch global` flags (passes Criterion 4), contains no mock imports (passes Criterion 5), and outputs a timing metric (passes Criterion 6). However, the spec it runs against is trivially small (3 lines, zero requirements), causing every gate to auto-pass with minimal content. The artifacts exist and are "real" but contain no meaningful signal.

**Why not caught**: No criterion validates the quality or depth of the eval spec. The prompt assumes the spec from Prompt 1 is adequate.

### Scenario 2: "The Copy-Paste Eval"
An eval runs the pipeline once, saves the output. Then for the "second branch" run, it copies the same output to a different directory and adds random noise to the metrics. Both runs "complete," artifacts exist in both directories, and there is a measurable delta (the random noise).

**Why not caught**: No criterion verifies that both runs actually invoked the pipeline independently. Criterion 4 checks that the eval "supports" running on both branches, not that it actually does.

### Scenario 3: "The Checkpoint Eval"
An eval runs `superclaude roadmap run` but catches the first gate failure and falls back to a checkpoint that writes pre-baked artifacts for all subsequent stages. The first 3 stages are real; stages 4-13 are synthetic. The eval produces all required files and a delta metric for stages 1-3.

**Why not caught**: No criterion requires that ALL 13 stages executed. Criterion 2 checks file existence but not that each file was produced by its corresponding pipeline stage.

### Scenario 4: "The Warm-Cache Eval"
An eval runs the pipeline legitimately, but on a codebase that has no wiring issues, no spec ambiguities, and no callable patterns to analyze. All gates pass trivially. wiring-verification.md says "0 findings." spec-fidelity.md says "0 deviations." The eval technically demonstrates v3.0 by showing these stages run, but the output carries zero signal about whether the stages work correctly.

**Why not caught**: No criterion validates that the eval exercises the new stages in a way that produces non-trivial output. This is the same gap as Scenario 1 but from the codebase side rather than the spec side.

### Scenario 5: "The Timing-Only Delta"
An eval passes all criteria but its only quantitative metric is wall-clock time. The delta between v3.0 and master is "v3.0 takes 45 seconds longer because it runs 5 more stages." This is technically a measurable delta, but it proves nothing about quality, correctness, or impact. It merely proves v3.0 has more steps.

**Why not caught**: Criterion 6 requires "at least one quantitative metric that differs" but does not require the metric to be meaningful or to measure quality rather than quantity.

---

## Synthesis and Final Verdict

### Strengths of Generated Prompt 4
1. Correct use of `/sc:reflect` as the validation mechanism.
2. PASS/FAIL structure with evidence requirements creates an auditable gate.
3. The 6 criteria cover the original 4 requirements plus two useful structural checks.
4. Grep terms are well-chosen for the known failure pattern (unit tests with mocks).
5. Output to a named report file enables downstream reference.

### Critical Gaps (must fix)
1. **Artifact provenance is unchecked.** The prompt verifies artifact existence but not that artifacts were produced by the pipeline run rather than pre-staged, copied, or template-generated. Add a criterion: artifacts must be written to a clean (newly created) output directory, and their modification timestamps must post-date eval invocation.
2. **Grep is necessary but insufficient.** Dead imports, indirection, and shell delegation can bypass the grep checks. The prompt should require that the `/sc:reflect` agent actually trace the execution path (read the eval script's main function and verify it reaches a pipeline invocation), not just grep for terms.
3. **No blocking gate.** The prompt produces a report but does not block Prompt 5 execution on FAIL verdicts. Add an explicit gate: "If REAL EXECUTION, REAL ARTIFACTS, or THIRD-PARTY VERIFIABLE fail, the eval suite is NOT READY for execution."

### Recommended Improvements (should fix)
4. **Severity tiering.** Criteria 1-3 should be CRITICAL (hard block). Criteria 4-6 should be REQUIRED (fix before proceeding but do not require Prompt 3 re-run).
5. **Re-validation loop.** After remediation, the prompt should specify that Prompt 4 must be re-run to confirm fixes. One-shot validation is not a gate.
6. **Meaningful delta requirement.** Criterion 6 should specify that timing alone is insufficient; at least one quality metric (gate pass rate, deviation count, finding severity distribution) must differ.

### Acceptable As-Is (no change needed)
7. A/B COMPARABLE criterion is a valid pre-flight for Prompts 5-6.
8. The remediation instruction requirement is appropriate.
9. The specific artifact filenames listed in Criterion 2 match the actual pipeline outputs.

### Overall Assessment

| Dimension | Rating | Notes |
|---|---|---|
| Fidelity to original | 7/10 | Covers 3 of 4 requirements well; "evidence of execution" weakened to "artifact existence" |
| Scope appropriateness | 8/10 | Two additions are justified; minor risk of metric gaming on Criterion 6 |
| Detection power | 6/10 | Catches the specific rejected pattern (unit tests with mocks) but can be bypassed by moderate sophistication |
| Evidence rigor | 5/10 | Checks file existence, not provenance or causality |
| Remediation path | 5/10 | Instructions without re-validation loop or severity tiering |
| Escape hatch coverage | 4/10 | Five plausible bypass scenarios identified |

**Verdict: CONDITIONAL PASS.** The generated Prompt 4 would catch the specific failure pattern that triggered the corrective action (168 unit tests with no real execution). It would NOT catch more subtle forms of eval gaming. For a v3.0 release gate where the primary risk is "evals that look good but do not run the pipeline," this prompt is adequate. For a production-grade eval validation framework, the three critical gaps (artifact provenance, execution path tracing, blocking gate) must be addressed.

---

## Proposed Amendments to Prompt 4

If the critical gaps are to be addressed, the following additions to the generated prompt are recommended:

```
7. ARTIFACT PROVENANCE: The eval must write artifacts to a clean output directory
   (created at eval start, verified empty). After the eval completes, verify that
   artifact modification timestamps post-date the eval start time. If artifacts
   exist before the pipeline runs, or their timestamps predate the eval, FAIL.

8. EXECUTION PATH: Beyond grepping for import names, trace the eval's main()
   function to confirm it reaches a pipeline invocation without conditional
   bypasses, early returns, or fallback paths that skip execution. If the
   pipeline call is behind an unreachable conditional, FAIL.

BLOCKING GATE: If criteria 1, 2, 3, or 7 receive a FAIL verdict, the overall
validation status is BLOCKED. Do not proceed to Prompt 5 until all BLOCKED
criteria are resolved and Prompt 4 is re-run to confirm.
```
