# Base Selection Report

## Metadata

- Generated: 2026-11-25T19:10:00Z (Step 3 of sc:adversarial Mode A)
- Variants scored:
  - **V1**: `variant-1-original.md`, reviewer 1, analyzer lens, model class haiku. 4 rows (all graded Blocking in the text), verdict FAIL, calibrated C 0.76.
  - **V2**: `variant-2-original.md`, reviewer 2, qa lens, model class opus. 13 rows (3 Blocking, 3 Medium, 7 Note), verdict FAIL, calibrated C 0.77.
- Inputs read: both variants, `diff-analysis.md`, `debate-transcript.md`, the four advocate statements, `invariant-probe.md`, the plan (103 lines) and the spec (38 lines).
- Debate status carried in: 88.89% agreement on 18 diff points; status **CONVERGED** (no HIGH UNADDRESSED invariant; 7 MEDIUM warnings carried to the merged card).
- What is being scored: each variant as a **base for the merged reviewer card** (header to the end of `## Notes`; the appended calibration is evidence, not scored text).
- Limit recorded: the scorer is the orchestrating session, whose model class (sonnet) is the executor class of the plan under review. Both variants were written by other classes (haiku, opus) and the advocates by haiku and opus, so the scorer is not a debater class (Khan et al.), but executor-class independence is not met.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (analyzer, haiku) | V2 (qa, opus) |
|--------|--------|----------------------|---------------|
| requirement_coverage (RC) | 0.30 | **0.308** (4 of 13 agreed findings in V1's rows) | **0.615** (8 of 13 in V2's rows) |
| internal_consistency (IC) | 0.25 | **0.944** (2 contradictions in about 36 scorable claims) | **0.965** (3 contradictions in about 85 scorable claims) |
| specificity_ratio (SR) | 0.15 | **0.952** (about 120 concrete, 6 vague) | **0.974** (about 300 concrete, 8 vague) |
| dependency_completeness (DC) | 0.15 | **1.000** (internal references resolve) | **1.000** ("see row 5", "rows 8-10" resolve) |
| section_coverage (SC) | 0.15 | **1.000** (3 of 3 H2 sections) | **1.000** (3 of 3) |
| **quant_score** | | **0.771** | **0.872** |

Formula: `quant_score = (RC x 0.30) + (IC x 0.25) + (SR x 0.15) + (DC x 0.15) + (SC x 0.15)`.

- V1: 0.0924 + 0.2360 + 0.1428 + 0.1500 + 0.1500 = **0.7712**
- V2: 0.1845 + 0.2413 + 0.1461 + 0.1500 + 0.1500 = **0.8719**

The IC and SR counts are hand counts of scorable claims and concrete versus vague indicators (about plus or minus 10 percent); RC is exact. A 10 percent error in either hand count moves a quant score by less than 0.01, which does not change the ranking.

### RC: stand-in for source requirements

The source is not a requirements document that the cards must restate. As in the earlier runs, RC counts how many of the **13 agreed merged findings** (the final list of `refactor-plan.md`) each variant already carries in a Deviations row. A mention in Notes, or a defect a card dismissed, does not count.

| # | Agreed finding (final grade) | In V1 rows | In V2 rows |
|---|---|---|---|
| 1 | Full pytest suite and `make lint` not run (Blocking (Missing)) | row 4 | row 1 |
| 2 | Changed launcher not connected to the live route (Blocking (Missing)) | row 1 | row 2 |
| 3 | Task 6 environment check not tied to the coordinator's PID (Blocking (Decision)) | no | row 3 |
| 4 | Prescribed wrapper fake contradicts switch-only capture (Blocking (Decision)) | no | row 5 |
| 5 | Raw-resume cases missing (Blocking (Missing)) | row 3 | row 13 (as a Note) |
| 6 | Header line placed where `--help` never prints it (Medium) | row 2 | row 4 |
| 7 | Tab-reopen execs missing from the route trace (Medium) | no | row 11 |
| 8 | Scope-decision line numbers go stale after Task 2 (Medium) | no | no |
| 9 | `verify-sync` needs `uv` and `jq`; baseline clause omits it (Medium) | no | no |
| 10 | Ruff acceptance wording says two files but the commands are repo-wide (Medium) | no | no |
| 11 | `git status` check cannot show ignored mirror changes (Note) | no | row 7 |
| 12 | Spec links unresolved inside the package (Note) | Notes only: no | no |
| 13 | Counts: 21 (case-sensitive) or 24 test files; "16" wrong (Note) | no | row 1 (wrong number): no |

V1 carries findings 1, 2, 5, 6 = 4 of 13 = 0.308. V2 carries findings 1, 2, 3, 4, 5, 6, 7, 11 = 8 of 13 = 0.615.

## Qualitative Scoring (50% weight): Additive Binary Rubric

Each criterion is MET (1) or NOT MET (0) with a claim, evidence and verdict (CEV). Evidence is a card row, line or section.

### Completeness (5 criteria)

| # | Criterion | V1 | V2 |
|---|-----------|----|----|
| 1 | Covers all explicit requirements from the source | NOT MET: no row for the coordinator's own PID (spec lines 7, 31); its summary lists INF-009 as incompletely planned with no row | MET: 42 units audited incl. `source.md:25`; coordinator proof in row 3 |
| 2 | Edge cases and failure scenarios | MET: row 3 raw-resume edge, row 1 deploy-path failure | MET: row 12 no-argument wrapper, row 6 inheritance |
| 3 | Dependencies and prerequisites | MET: `Makefile:111-123`, install test | MET: `install_ccsession.py:13-16, 61-71`, the pinning test |
| 4 | Success/completion criteria | MET: verdict FAIL when any Blocking row stands | MET: same |
| 5 | Out of scope stated | MET: "No commands ... were performed" | MET: "Not checked" list |
| | **Subtotal** | **4** | **5** |

### Correctness (5 criteria)

| # | Criterion | V1 | V2 |
|---|-----------|----|----|
| 1 | No factual errors | MET: 17 citations, 0 failed (calibrator) | NOT MET: "16 test files" (live count 21), "does not copy anything" overstated (calibrator caveats) |
| 2 | Feasible approaches | MET | MET |
| 3 | Terminology consistent | NOT MET: text says Blocking, label says MEDIUM on every row; header says haiku, footer says OpenAI | MET: HIGH on the three Blocking rows, MEDIUM, LOW |
| 4 | No internal contradictions | NOT MET: INF-009 counted incomplete with no row; label contradiction | NOT MET: 7 versus 6 estimate rows (lines 20, 26); INF-023 counted adherent while row 13 flags it |
| 5 | Claims supported by evidence | MET | MET (rows 8-10 weakest) |
| | **Subtotal** | **3** | **3** |

### Structure (5 criteria)

| # | Criterion | V1 | V2 |
|---|-----------|----|----|
| 1 | Logical ordering | MET | MET |
| 2 | Consistent hierarchy | MET | MET |
| 3 | Separation of concerns | MET: only plan defects in the table | NOT MET: rows 8-10 audit the brief and the first-pass card inside the plan table |
| 4 | Navigation aids | NOT MET: no path key, no cross references | MET: path key, "see row 5" |
| 5 | Follows the artifact convention | MET | MET |
| | **Subtotal** | **4** | **4** |

### Clarity (5 criteria)

| # | Criterion | V1 | V2 |
|---|-----------|----|----|
| 1 | Unambiguous language | MET | MET |
| 2 | Concrete, not abstract | MET | MET |
| 3 | Each section has a clear purpose | MET | MET |
| 4 | Terms defined on first use | NOT MET: "INF-005..041" undefined | NOT MET: "INF-041" undefined (PLAN/SPEC are defined) |
| 5 | Actionable next steps | MET: each row ends in a fix ("Specify insertion before the cutoff and require ...") | NOT MET: rows 2, 6, 8-13 name no concrete fix ("The plan must decide this") |
| | **Subtotal** | **4** | **3** |

### Risk Coverage (5 criteria)

| # | Criterion | V1 | V2 |
|---|-----------|----|----|
| 1 | At least 3 risks with probability and impact | NOT MET: no probabilities | NOT MET: no probabilities |
| 2 | Mitigation for each risk | MET: a fix in every row | NOT MET: rows 6-13 carry no fix |
| 3 | Failure modes and recovery | MET: row 1 names the dependent check | MET: row 2 names the failing check and the global-install risk |
| 4 | External dependencies and their failure | NOT MET: installed contents listed as unverified, no failure scenario | MET: installed copy, 13 other test files |
| 5 | Validation mechanism for risk detection | NOT MET: none named | MET: names the full suite, `-k reap`, `verify-sync` |
| | **Subtotal** | **2** | **3** |

### Invariant and Edge Case Coverage (5 criteria)

| # | Criterion | V1 | V2 |
|---|-----------|----|----|
| 1 | Collection boundaries | NOT MET | MET: row 12 no-argument wrapper launch |
| 2 | State variable interactions across components | NOT MET | MET: row 5 fake record versus acceptance, row 6 inheritance |
| 3 | Guard condition gaps | MET: row 2 help cutoff guard | MET: row 2 deploy guard, row 3 PID guard |
| 4 | Count divergence | MET: row 3 20-case count | MET: row 10 arithmetic, row 12 test counts |
| 5 | Interaction effects | NOT MET | MET: row 1 README edit versus the pinning test |
| | **Subtotal** | **2** | **5** |

### Qualitative Summary

| Dimension | V1 | V2 |
|-----------|----|----|
| Completeness | 4 | 5 |
| Correctness | 3 | 3 |
| Structure | 4 | 4 |
| Clarity | 4 | 3 |
| Risk Coverage | 2 | 3 |
| Invariant and Edge Case | 2 | 5 |
| **Total** | **19 / 30 = 0.633** | **23 / 30 = 0.767** |

### Edge Case Floor Check

Both variants score at least 1 of 5 on Invariant and Edge Case Coverage (V1 2, V2 5): both eligible as base.

## Position-Bias Mitigation

- Pass 1: V1 then V2 (table above). Pass 2: V2 then V1, criterion by criterion, with the evidence re-read.
- Pass 2 changed no verdict. One criterion was close and was re-evaluated with both pieces of evidence: V1 Risk Coverage 4 (the Notes name the installed executable, Orca configuration and live access as unverified, but state no failure scenario), which stays NOT MET.
- **Limit:** both passes were run by the same evaluator, so pass 2 reduces order effects but is not an independent evaluation.
- disagreements_found: 1; verdicts_changed: 0.

## Combined Scoring

| | quant (0.50) | qual (0.50) | variant_score |
|---|---|---|---|
| V1 | 0.7712 | 0.6333 | 0.5 x 0.7712 + 0.5 x 0.6333 = **0.7023** |
| V2 | 0.8719 | 0.7667 | 0.5 x 0.8719 + 0.5 x 0.7667 = **0.8193** |

Margin: 0.117 (11.7 points), above the 5 percent tiebreaker band: no tiebreaker applied.

## Selected Base: Variant 2 (reviewer 2, qa lens, opus class)

- **Selection rationale**: V2 carries 8 of the 13 agreed findings against V1's 4, it alone has the coordinator-PID, wrapper-capture and tab-reopen findings, and it scores 5 of 5 on invariant and edge-case coverage. Its calibrated confidence (0.77) is level with V1's (0.76); the debate, not the calibration, separates them.
- **Strengths to preserve from V2**: the path key and absolute-path evidence; the Blocking (Decision) and (Missing) reasoning with named consequences in rows 1-3 and 5; label-to-grade consistency (HIGH on Blocking rows); the "Confirmed correct" and "Not checked" lists.
- **Strengths to incorporate from V1**: concrete fix sentences (rows 1-4); the narrower and correct wording of the live-route finding ("does not establish which launcher the live check exercises", not "the coordinator necessarily runs an old copy"); the Blocking (Missing) grade for raw-resume coverage (V2 conceded it); the explicit dismissal of the first-pass card's `_label_run` wording point; the unresolved-relative-link note.
- **Weaknesses of the base to repair**: rows 8-10 (they audit inputs, not the plan) move to Notes; rows with no fix get one; the "16 test files" number is corrected; the Medium and Note rows that the debate upgraded or dropped are re-graded; the seven MEDIUM probe findings are added or folded.
