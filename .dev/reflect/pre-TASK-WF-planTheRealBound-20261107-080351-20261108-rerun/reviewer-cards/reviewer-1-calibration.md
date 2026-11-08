# Calibration Report (reviewer 1 card)

(Returned by the confidence-calibrator agent, sonnet class; persisted by the parent on receipt at 2026-11-08T02:08Z.)

**Card**: reviewer-cards/reviewer-1-card.md   **Rubric**: reflection-rubric.md (5 dimensions, C = arithmetic mean)   **Tier**: 2   **Mode**: pre   **Timestamp**: 2026-11-08T02:06:28Z

## Citation spot-check (12 checked, 11 match, 1 matches with an overstatement)

plan:22 (0.25 cap; 1+4+4+3 budget) match; plan:31 survivor rule versus sweep conflict match; plan:35 match; plan:55 match but overstated: the card says Task 3 "requires" a pty session while the plan says "attempt" with an unavailable fallback "if ... cannot be driven within the budget" (the phrase "within the budget" is ambiguous between the dollar cap and the run count); plan:44 match; plan:90 match; plan:117 match, and plan:23 says a case counts as observed when a real Git process produced it, which cuts against the card's reading that Task 6's real Git pushes can never be observed (the card does not weigh this); plan:66 and :69 match (nothing verifies a changed PPID at sampling time); helper:219-234 match; helper:292-295 match (setsid at 292, prctl(36,1,...) at 295); design:504 match; claude-help.txt:131-132 match. Unverified: INF coverage verdicts and cross-references to Tier 1 (the INF list and the Tier 1 card were not supplied; graded blind).

## Per-dimension scores

| Dimension | Score | Justification |
|---|---|---|
| Citation grounding | 0.90 | every finding has plan_line and quoted evidence; all 12 checked citations resolve; loses points for the overstated "requires" in A-02 and an INF coverage paragraph with few citations |
| Coverage completeness | 0.88 | all ten INF items get an explicit Covered or Partial verdict; findings touch Tasks 1, 2, 3, 4, 6, 8, coverage paragraph handles 5 and 7; no coverage percentage; misses the plan:23 versus Task 6 observed/controlled tension |
| Deviation-classification clarity | 0.80 | one category and one severity per finding (four MEDIUM, one LOW), none hedged; weakness is discrimination and rationale: all five are "Drift", no stated reason why Drift rather than Refinement, no stated basis for severity; A-02 cites an external CLI fact rather than a spec requirement so "Drift" is a loose fit |
| Risk surface coverage | 0.78 | covers survivor children killed by timeout cleanup, an uncapped interactive run, an unproven reused-process topology, unsupported tree-row claims; blast-radius reasoning thin; does not say how mislabelled "observed" rows would carry into the B-CTX gate; does not flag that the Task 1 self-check omits a refused-thirteenth-run test |
| Recommendation actionability | 0.80 | most recommendations are concrete edits to named sections (A-01 adds a checkable self-check; A-04, A-05 name fields and steps); A-02 offers two alternatives without choosing; only A-01 states a success criterion |

## Confidence

Self-reported 0.90; **calibrated 0.83** = 4.16 / 5 = 0.832. Delta -0.07. Sits 0.02 below the 0.85 floor.

## Escalation recommendation

ESCALATE, reason low_confidence (rubric: C < 0.85). No structural signals supplied (tasklist-item count 8). No execution restriction. The orchestrator should weight A-01 and A-03 highest in Wave 4.

## Notes

Absent inputs: assertions_path (C1-C8 skipped), claim_class/evidence_class/verdict_direction (not used by this rubric), behaviour_definitions_path, tasklist_path, locus_path. card_mtime 02:05:19Z agrees with the card. A-01, A-03 and A-05 hold up on the files read; A-02 and A-04 hold but are slightly overstated. The card's refutation of N-1 (thirteen runs not forced) is consistent with plan:22 and plan:31; it could not be checked against the Tier 1 card.
