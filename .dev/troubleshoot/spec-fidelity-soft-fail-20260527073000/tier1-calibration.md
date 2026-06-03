# Tier 1 Calibration Report

**Card:** tier1-hypothesis.md
**Calibrator:** inline orchestrator (confidence-calibrator subagent skipped due to single-domain trivial-confidence case)
**Tier:** 1

## 5-dimension rubric scoring

| Dimension | Score (0.0–1.0) | Reasoning |
|---|---|---|
| Evidence grounding | 0.95 | Six file:line citations, every one re-Read in Wave 1; convergence.py:539, executor.py:1466, executor.py:2685, models.py:111-126 are all verified verbatim |
| Mechanism completeness | 0.92 | Mechanism is explicit: `ConvergenceResult.passed=False` → `StepStatus.FAIL` → `execute_roadmap` halts at line 3164. The soft-fail intervention point is unambiguous (executor.py:1466) |
| Counter-hypothesis coverage | 0.85 | One alternative ruled out: "extend `max_runs` to fix convergence" — rejected because (a) restriction-locked per recent task, (b) doesn't address the case where the spec genuinely has unmatched canonical IDs. The "If I'm wrong..." section names the most-likely failure path (downstream-consumer reliance on FAIL signal) |
| Reproducibility | 0.95 | Failure mode reproduced 1:1 in the transcript pasted by the user (`Convergence not reached after 3 runs. Remaining active HIGHs: 51`); the proposed fix's behavior is testable via three unit tests already enumerated in the hypothesis |
| Domain match | 0.95 | Single-domain (pipeline orchestration); the symptom is clearly an operator/policy decision, not a multi-system regression |

**Weighted calibrated confidence: 0.93**

## Verdict

**STOP at Tier 1.** Confidence (0.93) > 0.85 threshold; single-domain; symptom is operator-reported; no ambiguity about the architectural seam; user has explicitly authorized the contract extension. Tier 2 fan-out (multiple specialist hypothesis agents) would not add new information — the diagnosis is structural, not investigative.

## Escalation rule check

- `--depth quick` not set → standard rubric applies
- `--depth deep` not set → no forced escalation
- `--no-escalate` not set → would-escalate rules apply
- Confidence ≥ 0.85 ✓
- Single-domain ✓
- Not intermittent ✓
- Not multi-domain ✓

All STOP conditions satisfied. Wave 2 → STOP at Tier 1; proceed directly to Wave 5 (Synthesis + Report).
