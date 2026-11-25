# Base Selection

## Quantitative Scoring (50% weight)

The five metrics were counted by the orchestrator by reading the variants. Counts are approximate (about 3 either way); the brief has no formal requirement ids, so requirement coverage uses section-level matching against the brief's five success criteria.

| Metric | Weight | Variant 1 | Variant 2 | Computation notes |
|--------|--------|-----------|-----------|-------------------|
| Requirement coverage (RC) | 0.30 | 1.00 | 1.00 | Brief success criteria: default, closed triggers, cost table, merge rules, trial plan. All 5 present in both |
| Internal consistency (IC) | 0.25 | 0.97 | 0.91 | V1: about 60 claims, 2 contradictions (option 3 complex 31 vs option 2 complex 30; T1 fires on new files that the story itself lists). V2: about 55 claims, 5 contradictions (complex option 2 stated 18, formula gives 17, twice; spec-panel call lacks `--report-dir`; workflow call lacks `--unattended --report-dir`; R4 continues past an incomplete task against Q8) |
| Specificity ratio (SR) | 0.15 | 0.97 | 0.97 | V1: about 120 concrete, 4 vague ("small", "nearly always", "mostly"). V2: about 105 concrete, 3 vague |
| Dependency completeness (DC) | 0.15 | 1.00 | 0.96 | V1: all T and R references resolve. V2: `ac-map.md` has no stated producer; `check-story` named but not defined as new |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 8 H2 sections each |

quant_score V1 = 0.30 + 0.2418 + 0.1455 + 0.15 + 0.15 = **0.987**
quant_score V2 = 0.30 + 0.2273 + 0.1458 + 0.144 + 0.15 = **0.967**

## Qualitative Scoring (50% weight): Additive Binary Rubric

Pass 1 was done by the orchestrator in order V1, V2. Pass 2 was an independent agent (sonnet) in reverse order V2, V1, blind to pass 1. Each cell shows pass 1 / pass 2; the final column is the final verdict. Evidence is short; the full pass 2 table is in the debate record of this run.

### Completeness

| Criterion | V1 (p1/p2) | V2 (p1/p2) | Evidence |
|---|---|---|---|
| C1 covers every part the brief asks for | MET / MET | MET / MET | Both have recommendation, triggers, cost table, merge rules, trial plan |
| C2 edge cases and failure scenarios | MET / MET | MET / MET | V1 R6 stops the hand-off; V2 R4, review-3 halt |
| C3 dependencies and prerequisites | MET / MET | NOT MET / NOT MET | V1 "Two scripts ... do not exist yet"; V2 names `check-story` and `ac-map.md` without a producer |
| C4 completion criteria | MET / MET | MET / MET | V1 gates R1 and R4; V2 R9 |
| C5 out of scope | MET / MET | MET / MET | Section "Out of scope" in both |

### Correctness

| Criterion | V1 (p1/p2) | V2 (p1/p2) | Evidence |
|---|---|---|---|
| K1 no factual errors | MET / MET | MET / MET | Cap of 2 fix cycles, line 98 AC block, chains.md simple row all verified for both |
| K2 feasible for workers that cannot ask, under `--unattended` | MET / MET | NOT MET / MET | Disagreement on V2, resolved below to NOT MET |
| K3 consistent terminology | MET / MET | NOT MET / NOT MET | V2 uses R for both merge rules and the panel review count |
| K4 no internal contradictions | MET / MET | NOT MET / NOT MET | V2 18 vs 17 (twice); V1's 31 is explained in its text |
| K5 claims supported | MET / MET | MET / MET | Both tag ESTIMATE and UNVERIFIED |

### Structure

| Criterion | V1 | V2 | Evidence |
|---|---|---|---|
| ST1 logical order | MET / MET | MET / MET | Same eight-part order |
| ST2 consistent hierarchy | MET / MET | MET / MET | |
| ST3 separation of concerns | MET / MET | MET / MET | |
| ST4 cross-references | MET / MET | MET / MET | |
| ST5 spec conventions, testable statements | MET / MET | MET / MET | V1 "Test: a diff ... is empty"; V2 "Failure:" lines |

### Clarity

| Criterion | V1 | V2 | Evidence |
|---|---|---|---|
| CL1 unambiguous language | MET / MET | MET / MET | |
| CL2 concrete | MET / MET | MET / MET | Exact flags, paths, regex |
| CL3 clear section purpose | MET / MET | MET / MET | |
| CL4 terms defined on first use | NOT MET / NOT MET | MET / MET | V1 never expands AC, E-HALT-QA, E-NO-AC |
| CL5 actionable decisions | MET / MET | MET / MET | |

### Risk Coverage

| Criterion | V1 | V2 | Evidence |
|---|---|---|---|
| R1 at least 3 risks with likelihood or impact signal | MET / MET | NOT MET / NOT MET | V1 risks 4, 5, 6 state consequences; V2 risks have none |
| R2 mitigation per risk | MET / MET | MET / MET | "Guard:" in both |
| R3 failure modes and recovery | MET / MET | MET / MET | |
| R4 external dependencies | MET / MET | MET / MET | Workflow tokens, brainstorm convergence, panel review 3 |
| R5 monitoring or validation | MET / MET | MET / MET | V1 `gate.json`, shadow runs; V2 M1 to M4 |

### Invariant and Edge Case Coverage

| Criterion | V1 | V2 | Evidence |
|---|---|---|---|
| E1 boundary conditions for counts | MET / MET | MET / MET | V1 T7 zero paths; V2 T4 zero AC |
| E2 state interactions across components | MET / MET | MET / MET | V1 R7; V2 R8 after the reviser |
| E3 guard-condition gaps | NOT MET / NOT MET | NOT MET / NOT MET | V1: zero-criteria story passes `story-gate`; V2: no guard for a story with no commit |
| E4 count divergence, thresholds | MET / MET | NOT MET / NOT MET | V2 fire-rate band 40% to 50% unassigned; 18 vs 17 |
| E5 interaction effects | MET / MET | MET / MET | |

### Qualitative Summary

| Dimension | V1 | V2 |
|---|---|---|
| Completeness | 5/5 | 4/5 |
| Correctness | 5/5 | 2/5 (K2 final NOT MET) |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 5/5 |
| Risk Coverage | 5/5 | 4/5 |
| Invariant and Edge Case | 4/5 | 3/5 |
| **Total** | **28/30** | **23/30** |

qual_score V1 = 28/30 = **0.933**; qual_score V2 = 23/30 = **0.767**

### Edge Case Floor Check

Threshold 1/5 on the invariant dimension. V1 4/5 and V2 3/5: both eligible as base.

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| K2 | V2 | NOT MET | MET | no | NOT MET |

All 59 other criterion-variant pairs agreed. Disagreements found: 1. Verdicts changed by re-evaluation: 1 (pass 2 MET to NOT MET).

Re-evaluation of K2 for V2, with both pieces of evidence: pass 1 cited the R4 rule that has the worker "continue the other tasks", which `/sc:implement` Q8 (`~/.claude/skills/sc-implement-protocol/SKILL.md` line 150, "Only if complete ... Else STOP") does not allow, and the spec-panel call without `--report-dir` (refused, `~/.claude/commands/sc/spec-panel.md` line 458). Pass 2 saw only that R4 avoids asking a person. Both facts were read by the orchestrator after the debate. Final verdict: NOT MET.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | Combined |
|---------|---------------|--------------|----------|
| V1 (opus:architect) | 0.494 | 0.467 | **0.960** |
| V2 (sonnet:analyzer) | 0.484 | 0.383 | **0.867** |

Margin: 9.3 points (more than the 5% tiebreaker band). Tiebreaker applied: no.

## Selected Base: Variant 1 (opus:architect)

**Selection rationale.** V1 scores higher on correctness and consistency. Three of its design choices are verified against the installed commands and are what a worker run needs: it passes `--report-dir` where spec-panel and workflow require it, its conflict policy stops before the executor starts (the executor stops at an incomplete task, Q8), and the adversarial merge output is never the spec (R7).

**Strengths to preserve from V1.**
- R7: discard and rebuild the merged criteria section from the story.
- The AC change log with `proposed` and `approved` status and the route through `bmad-correct-course`.
- `story-gate` inlining the full criterion text in place of `(AC: #)`.
- Shadow runs, trigger-removal rule and the 60% collapse rule.
- Panel trigger tied to the location of the blocking finding (T6) and the ungrounded-story trigger (T7).
- Flags that fit `--unattended` (`--report-dir` everywhere).
- Explicit statement that `/sc:design` is not run.

**Strengths to incorporate from V2 (and from the debate).**
- T1 and T2 skip paths the story marks as new (X-005 conceded by V1), using the BMAD UPDATE versus NEW split.
- T4 shape gate for stories that are not executable as written (A-004).
- V2's higher size thresholds (more than 8 criteria, more than 12 tasks) in place of 6 and 6, and V2's narrower regex, so the complexity triggers over-fire less.
- Byte-exact `source-story.md` and the R9 completion closure; `ac-map.md` as data.
- Cost formulas and counting rule, split of option 3 into default arm and alternate arm rows, arithmetic corrected, reviser call counted, script build cost and owner named, tokens logged (A-003, A-007).
- Metrics M1 to M4 including the missed-conflict metric and the AC-loss stop rule for option 2; trigger list frozen during a release.
- Numbered section headings.
- From the debate: define every acronym on first use; add a guard for a story with zero criteria; state likelihood or impact for risks; name the optional accuracy-check input (A-005).
