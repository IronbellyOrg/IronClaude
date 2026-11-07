# Adversarial Debate Transcript

## Metadata

- Depth: standard
- Rounds completed: 2 (+ Round 2.5 invariant probe)
- Convergence achieved: 100%
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3 (Variant 1 sonnet/analyzer, Variant 2 haiku/qa, Variant 3 opus/refactorer); all general-purpose Task agents, read-only
- Agent failures: none

## Round 1: Advocate Statements

Full statements, persisted verbatim in substance on receipt:

### Variant 1 Advocate (sonnet:analyzer)
`rounds/round-1-variant-1.md`. Claims R1-1 (only card to find the "exited 0" check passing with the old sentence) and R1-5 (only card to verify init_lite.py exit paths); concedes QA-1, R3-1, the :792 interaction; A-001 QUALIFY, A-002 QUALIFY.

### Variant 2 Advocate (haiku:qa)
`rounds/round-1-variant-2.md`. Claims QA-1 (Task 4 pin admits a clause without the exclusion) at P1; concedes QA-2 to P3 and the report-location duplication; A-001 QUALIFY (workflow SKILL.md:60-62 forbids plan edits), A-002 QUALIFY.

### Variant 3 Advocate (opus:refactorer)
`rounds/round-1-variant-3.md`. Claims R3-1 (design-spec copy), R3-4, R3-5, R3-3; concedes R1-1, QA-1, R1-3 superior; proposes one grade for the "assertion weaker than its AC" class; A-001 QUALIFY, A-002 QUALIFY.

No [OMISSION]: every advocate answered A-001 and A-002.

## Round 2: Rebuttals

Sequential, in input order; each advocate saw all Round 1 statements and earlier rebuttals.

- `rounds/round-2-variant-1.md`: concedes R1-6, the narrow mirror claim, one grade per class; narrows R1-2 to "Task 2 arranges no compliance"; proposes grading rule (negate / displace / vacuous); new evidence: SKILL.md:61 `worker_status` precedes `artifacts`; input-parse.md:16 pointer precedent; :517 guards command sections.
- `rounds/round-2-variant-2.md`: withdraws the Task 5 clean claim and the report-location demand; QA-1 P1 narrowed to "left out"; amends the grading rule (P1 = shown false pass or blocker; P2 = ambiguity without shown false pass); static QA-1 witness.
- `rounds/round-2-variant-3.md`: concedes R3-A1 to gating P2; keeps R3-1 at P2 with a recorded-decision fix; adopts V2's rule tightened (false pass under the literal instruction = P1; needs a reading choice = P2).

## Round 2.5: Invariant Probe

`invariant-probe.md`: 16 findings, 0 HIGH unaddressed, 5 MEDIUM unaddressed (INV-001, INV-003, INV-005, INV-006, INV-007), 7 LOW unaddressed, 4 addressed.

## Round 3

Skipped: depth=standard.

## Taxonomy coverage

| Level | Points | Covered |
|-------|--------|---------|
| L1 surface | S-001, C-007 | yes |
| L2 structural | C-003, C-006, C-008, C-010, X-003, A-001 | yes |
| L3 state mechanics | C-001, C-002, C-004, C-005, C-009, X-001, X-002, A-002 | yes |

No forced round needed.

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | Tie (no winner) | 80% | All three agree card shape changes no finding; V3 conceded its advisory block hid R3-A1 |
| C-001 | Variant 1 | 85% | R1-3 rebinds AC3 to a contract-reading check; all agree P3; INV-009 notes the replacement test is also near-vacuous, so the WC-4 pins are the real guard |
| C-002 | Variant 1 / Variant 3 (shared) | 88% | Same slice; adopted rule grades P2 (needs a reading choice); markers verified (INV-008) |
| C-003 | Variant 1 | 90% | R1-2 gating P2, narrowed; V3 conceded R3-A1 merges into it |
| C-004 | Variant 2 (narrowed by V3) | 92% | QA-1 P1 unanimous; pin "left out" + WC-4 + `[]`; V2 conceded report-location wording; INV-003 shows "left out" alone is gameable |
| C-005 | Variant 1 | 95% | R1-1 P1 unanimous; V2 withdrew its clean claim (concession boost) |
| C-006 | Variant 3 | 90% | Spec :72 restates WC-4; V1 conceded; fix is a recorded decision, P2 |
| C-007 | Variant 3 | 80% | Valid P3 against the plan's goal line; no AC violated |
| C-008 | Variant 3 | 78% | Narrowed to return-contract.md (command sections guarded at :517) |
| C-009 | Variant 1 | 85% | Only card that verified init_lite.py exit paths |
| C-010 | Tie (advisory) | 75% | Out of the brief |
| X-001 | Variant 2 / Variant 3 (synthesis) | 88% | Pin the exclusion; WC-4 owns report-location (INV-005 qualifies this) |
| X-002 | Variant 1 / Variant 3 | 92% | P3; V2 conceded |
| X-003 | Variant 3 | 92% | Tracked spec copy; V1 conceded |
| A-001 | Tie (all QUALIFY) | 85% | Corrections need the owner to revise the plan (INV-006) or in-task application |
| A-002 | Tie (all QUALIFY) | 85% | AC review is a second guard; does not lower grades |

Points won (shared points count 0.5): Variant 1 5.0 (C-001, C-003, C-005, C-009, half C-002, half X-002); Variant 2 1.5 (C-004, half X-001); Variant 3 5.5 (C-006, C-007, C-008, X-003, half C-002, half X-002, half X-001).

Adopted grading rule (2 of 3 advocates, V1 agrees in substance): P1 = false pass shown under the plan's literal instruction, or a blocker; P2 = needs a reading choice, or a coverage or rule-text defect without a literal false pass; P3 = vacuous, cosmetic or owner note. Per-task AC review does not lower grades.

## Convergence Assessment

- Points resolved: 16 of 16
- Alignment: 100%
- Threshold: 80%
- Taxonomy gate: all three levels covered
- Invariant gate: 0 HIGH unaddressed; 5 MEDIUM warnings (INV-001, INV-003, INV-005, INV-006, INV-007)
- Status: CONVERGED (stable majority, max rounds for depth standard)
- Unresolved points: none
