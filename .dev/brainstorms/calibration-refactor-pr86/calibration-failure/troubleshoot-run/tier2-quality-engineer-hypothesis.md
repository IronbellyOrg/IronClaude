# Tier 2 — quality-engineer hypothesis (H-QE)

**Author**: quality-engineer (inline)
**Tier**: 2
**Type**: bug

## Claim

**Root cause: silent-green calibration tests.** The calibrator was shipped with a "Test Results (2025-10-21): Precision 1.000, Recall 1.000" claim in `confidence-check/SKILL.md:14-18`, but pr86 demonstrates the test corpus does NOT exercise the runtime-verification-impossible scenario. The pass/fail evals score the calibrator on cases it CAN ground; cases where grounding is structurally impossible (sha-pinned PR, Rust runtime behavior from source) never appeared in the eval set. The calibrator passes its tests for the wrong reason — same shape as the V3 (QE) Wave 3 finding in pr86 itself (`adversarial/debate-transcript.md:69`: "test_t1/t6/t7 silently green-bar on substring containment").

## Evidence

- `/config/.claude/skills/confidence-check/SKILL.md:14-18`: blanket claim of 1.000/1.000 with no breakdown of failure-mode coverage.
- `confidence-calibrator.md:117-118` — Placebo risk surfaced in spec but no eval coverage gate: "if calibrated score consistently matches inline calibration to within ±0.05, the agent is not earning its overhead. The orchestrator should periodically run head-to-head meta-evals" — *periodically* and *should* are not eval-suite contracts.
- pr86 substrate: 3 Tier 2 calibrations all hit `evidence_grounding=0.5` with identical reason. No eval case in the calibrator's test suite reproduces a structurally-unverifiable predicate to assert the calibrator returns < 0.85.
- Wave 4 in pr86 converged at 0.81 yet missed the helper-not-uppercasing runtime defect that rf-qa-qualitative caught only in A.10.5 cycle 1 (`REPORT.md` summary). Same "tests passed but ran wrong invariant" shape recurring at a different scope.

## Proposed Fix

**Add pin-tests for the structurally-unverifiable predicate scenario.** Specifically:
1. A regression eval case where the hypothesis card cites `git show <sha>:<path>` and the calibrator (without Bash) must return calibrated ≤ 0.84.
2. A regression eval where the hypothesis predicts runtime behavior from source reads only and the calibrator must return ≤ 0.84.
3. A property-based test: for any card where the calibrator marks `evidence_grounding ≤ 0.5`, calibrated MUST be ≤ 0.85 regardless of other dimensions.

This is the analog of V3-pr86's pin-tests-first sequencing: red-bar the silent-green scenarios before changing the rubric.

## Confidence

**Self-reported: 0.78**. The silent-green pattern is well-attested in pr86's own debate; applying the same diagnostic lens to the calibrator that the calibrator applied to pr86 is fair game.

## Risks

- Treats the test suite as the bug rather than the rubric. If the rubric is fundamentally flawed (H-RCA's claim), pin-tests just freeze a known-bad behavior.
- Eval cases for "structurally unverifiable" are themselves hard to construct without execution.

## If I'm wrong...

...the rubric arithmetic is the load-bearing defect (H-RCA) and tests just paper over it. Pin-tests are still useful but as a guardrail, not the fix.
