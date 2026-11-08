# Adversarial Debate Transcript
## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel, Round 2 sequential) plus Round 2.5 invariant probe
- Convergence achieved: 100% of diff points agreed after Round 2 (17 of 17); convergence BLOCKED by 1 HIGH UNADDRESSED invariant (INV-001)
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3 (V1 sonnet, V2 haiku, V3 opus)
- Condensation note: Round 1 and Round 2 replies are condensed by the orchestrator, keeping each advocate's evidence, concessions and per-point positions.

# Round 1: Advocate Statements (condensed by the orchestrator; each advocate's full reply was read and its evidence kept)

Taxonomy tags (AD-5): L1 surface = S-002, S-003. L2 structural = S-001, C-002, C-004, C-006, X-004. L3 state/guard/invariant = C-001 (stop gate), C-003 (status state), C-005 (registration guard), X-001, X-002, X-003, A-001, A-002, A-003, A-004.

## Variant 1 advocate (analyzer card; sonnet)

Position: V1 is the only card that classifies against the audit lens (Drift unless working code is contradicted) and separates the design-mandated IR-7 refusal (Authorized) from plan defects.
Steelman of V2: the design says stop enforcement implementation when the distinction cannot be made and OB-H1 before the skeleton (DESIGN:359-360), while Task 1 only writes a verdict and Task 2 swaps synthetic fixtures in (PLAN:36). V2 alone audits the coverage matrix, T-MSG-4..6, F1-F8 sources and the adapter prerequisites; Task 18 tests missing, not present-but-ineffective, registrations (PLAN:291 vs DESIGN:342-352).
Steelman of V3: tracing the plan against existing tests is the most valuable pre-execution check: launch_scene writes "#!/bin/sh" (TOW:1011), so the Task 18 and 20 requirements break the "launched" tests; also enforcement_hook, the ten-key test and FakeOrca.env leakage.
Strengths: (1) IR-7 refusal correctly Authorized (DESIGN:355,514); (2) Task 19/20 conflict found (PLAN:305 vs 318); (3) marker predicate tied to DESIGN:512, Regression-class only if header-only; (4) test fallout traced (stub fixture TOW:1011, 31 uses, three warning tests TOW:1296-1324 vs the plan's two); (5) unique catches IR-3, issue.md, --pipeline none untestable at script level, superclaude.* forms; (6) honest evidence limits; (7) Task 1 defect scoped: nothing depends on the verdict, MEDIUM.
Weaknesses of others: V2 over-calls Regression (findings 1,3,5,6 are plan-text gaps); V2 finding 7 undercut by DESIGN:377; V2 finding 1 ignores PLAN:24 and DESIGN:506; V2 misses test fallout; V3 "about 12" is a subset and "no fixture adds an owned L2 hook" ignores PLAN:320; V3 finding 3 ignores the design text; V3 findings 1 and 2 overlap.
Concessions: V3 beats V1 on test fallout; V1 missed live_probe.py (exists), the coverage-matrix gap, T-MSG-4..6, adapter prerequisites and C-005; V1's empty HIGH tier may under-call Task 18 and 20.
Leanings: S-001 split 55% V3; C-001 V1 60%; C-002 split; C-003 V1 60%; C-004 V3 70%; C-005 V2 80%; C-006 V1 65%; X-001 V1 65%; X-002 V1 60%; X-003 split 55% V3; X-004 split.
Assumptions: A-001 QUALIFY; A-002 QUALIFY; A-003 QUALIFY; A-004 ACCEPT.

## Variant 2 advocate (qa card; haiku)

Position: V2 is strongest at false assurance (a gate that does not stop work, registrations that exist but may not fire, launch checks that omit runtime support); several Regression/HIGH labels overstate what a static audit shows.
Steelman of V1: an unspecified implementation is not automatically a regression; it separates an undefined ownership check from a header-only implementation and sees the refusal is design-authorized. Steelman of V3: the plan must stay executable against existing fixtures and return contracts (findings 1-2, 6-7).
Strengths: (1) Task 1 permits L1 despite blocked B-CTX and substitutes synthetic observations for the live gate (PLAN:36,51-55) against DESIGN:359-361; (2) effective registration vs present-but-ineffective matcher (PLAN:291-293 vs DESIGN:342-352); (3) identity-adapter preflight omitted (DESIGN:561-565); (4) concrete rejection cases for the L2 check (PLAN:318-320 vs DESIGN:355,512); (5) the successful owned-L2 branch would still print "absent" (PLAN:305 vs 320, DESIGN:354); (6) Task 21 drops L2 even on GO (PLAN:333-337 vs DESIGN:366,373-377).
Weaknesses of others: V1 underweights the gate defect; V3 does not address it; neither raises C-005 or runtime prerequisites; both reduce the L2-status defect to the absent branch; V3 conflates design authorization with operational approval; V1's marker repair (version string plus registration check) is too thin for exact owned content.
Concessions: V2 misses fixture and return-contract fallout; classification needs correction (predicted vs observed); finding 6 is real but HIGH is overstated; finding 7 needs qualification; "tasks 2-15 and 22 adequate" is too broad; its coverage claims were not independently re-verified.
Leanings: S-001 split; C-001 V2 96%; C-002 split; C-003 V2 95%; C-004 V3 88%; C-005 V2 97%; C-006 V2 84%; X-001 V1 98%; X-002 V2 94%; X-003 split; X-004 V3 85%.
Assumptions: A-001 ACCEPT; A-002 REJECT; A-003 QUALIFY; A-004 QUALIFY (absence is not proof of unrecoverability).

## Variant 3 advocate (refactorer card; opus)

Position: V3 is the only card showing with line numbers that the plan would break existing passing tests; it uses Regression only for predicted breakage of tests that pass today; it misses the Task 1 STOP verdict nothing acts on (V1) and the matcher-blind registration check (V2).
Strengths: (1) verified fixture and asserts: TOW:1011 stub; 12 "launched" asserts at TOW:1051,1124,1196,1210,1234,1265,1276,1301,1481,1534,1571,1594; la3 tests move because the check precedes publish_pending (OW:937 then 941), so TOW:1147 and 1165 would see W-ENFORCEMENT-ABSENT; (2) Task 20 refusal fans out to every launch test; (3) owner notice ordered after shipping (PLAN:320); (4) enforcement_hook is a pinned key (TIP:513; OW:871,947,972,1005) and TIP:467-468 requires the code in SKILL.md and claim.md; (5) FakeOrca.env copies os.environ (TOW:103); (6) live_probe.py exists; (7) classification discipline.
Weaknesses of others: V2 over-uses Regression and ignores PLAN:36's rationale and DESIGN:366; V2 ignores DESIGN:377 (U28 etc.) for C-006; V2 misses the biggest practical defect; V1 downgrades a deterministic break to MEDIUM; V1 #9 does not catch the notice ordering.
Concessions: V3 missed the Task 1 STOP-with-no-consumer; C-005 is right on substance (MEDIUM, not HIGH); U-003 correct; "no fixture adds an owned L2 hook" is too strong (Task 20 plans an owned case); finding 6 conditional on the docs gaining a key.
Leanings: S-001 V3 60%; C-001 V1 65%; C-002 split; C-003 split V1/V3; C-004 V3 85%; C-005 V2 70%; C-006 not a deviation 55%; X-001 V3 60% (notice order); X-002 V1 65%; X-003 V3 65%; X-004 split 55%.
Assumptions: A-001 QUALIFY; A-002 QUALIFY; A-003 QUALIFY; A-004 ACCEPT.

## Round 1 tally (orchestrator)

Agreed after Round 1: C-001 (V1 MEDIUM Drift, plus V2's OB-H1 ordering sub-point), C-002 (substance: define the predicate and negative cases, Drift MEDIUM), C-004 (V3), C-005 (V2, MEDIUM per V1/V3), C-006 (not a deviation), X-001 (refusal authorized), X-002 (MEDIUM), X-004 (compatible), A-001 QUALIFY, A-002 QUALIFY, A-003 QUALIFY, A-004 ACCEPT = 12 of 17.
Unresolved after Round 1: S-001, S-002, S-003, C-003, X-003 = 5 of 17. Convergence 12/17 = 0.71 (threshold 0.80).
Omission flags: none of the three advocates addressed S-002 or S-003 (L1 surface level has zero coverage; a forced address is added to Round 2).

# Round 2: Rebuttals (sequential; condensed by the orchestrator)

## Variant 1 advocate (rebuttal 1 of 3)

Concessions: the empty HIGH tier under-calls the launch-fixture break (no plan task updates the "#!/bin/sh" stub at TOW:1011; Task 18's "proceeds exactly as before" condition at PLAN:298 cannot hold for the ~12 "launched" tests), so that one finding is HIGH. C-005, the coverage-matrix gap and the adapter prerequisites were already conceded. Rebuttal: the "absent" status line is not always dead output, because Task 20 plans an owned-L2 case (PLAN:320); the defect is that Task 19 pins "absent" (PLAN:305,310), a wording defect not broken working code.
Final positions: S-001 merged set of about 15 findings, 0 Regression, 1 HIGH (launch-fixture fallout), keeping V3's fallout finding, V2's C-005 and gate-ordering sub-point, V1's unique catches. S-002 "LOW-MEDIUM" not acceptable; use HIGH, MEDIUM or LOW with a one-line rationale. S-003 extra sections acceptable as LOW supplements (evidence limits, per-task table as an appendix, fix list) that must not replace the findings table. C-003 Drift MEDIUM (Task 19 wrong only on the owned branch). X-003 Drift, HIGH only for the fixture break; predicted failures are not Regressions because nothing ran; note that it becomes Regression if the fixture is left unchanged at execution.
Leanings changed: S-001 (to the merged set); X-003 stays Drift; C-003 narrowed to the owned branch.

## Variant 2 advocate (rebuttal 2 of 3)

Concessions: Regression overused (findings 1, 3, 5, 6 are missing or contradictory plan instructions, not demonstrated regressions); the gate finding is MEDIUM not HIGH (a STOP verdict with no downstream stop condition and synthetic fixtures in place of the pre-skeleton observation remain ordering defects); finding 7 (Task 21 drops L2 on GO) withdrawn as a deviation because installation and observation prerequisites justify a follow-up; V3's fixture and return-contract analysis belongs in the merged findings; "Tasks 2-15 and 22 adequate" withdrawn. Retained: the ownership predicate gap (the design rejects header-only ownership proof, DESIGN:512); Task 19's "absent" is wrong on the owned-L2 branch (MEDIUM Drift).
Final positions (agrees with advocate 1 on every point): S-001 Drift findings, one HIGH, zero Regression, merged set of about 15, counts not a quota; S-002 Drift LOW, replace "LOW-MEDIUM" with one supported severity; S-003 Authorized expansion LOW, supplements allowed while the findings table stays primary; C-003 Drift MEDIUM; X-003 Drift HIGH (the plan omits the fixture migration needed to preserve existing launch tests; breakage predicted, not observed).
Leanings changed: S-001 to the merged set; X-003 to Drift; C-003 narrowed to the owned branch; C-001 severity from HIGH to MEDIUM; C-006 withdrawn.

## Round 2 (advocate 3, rebuttal 3 of 3)

Concessions: X-001 (owner decision before Task 20) conceded: the refusal is design-required (DESIGN:355,366) and O-22 is decided (DESIGN:377); Task 20's ir7-consequence.md is a notice (PLAN:320), so at most a LOW reporting note. "No fixture adds an owned L2 hook" overstated: Task 20 plans an owned case (PLAN:320); the narrower point stands, no task updates the shared stub (TOW:1009-1011) so the 12 existing launch tests still fail; V1's "findings 1 and 2 overlap" accepted: one HIGH finding.
Final positions (accepts advocates 1 and 2 on all five): S-001 merged set of about 15 Drift findings, 0 Regression, 1 HIGH; S-002 Drift LOW; S-003 Authorized expansion LOW; C-003 Drift MEDIUM; X-003 Drift HIGH (becomes Regression only if executed without the migration).
Leanings changed: X-003, C-003, X-001, S-001.

## Round 2.5: Invariant probe
See invariant-probe.md (10 findings; 1 HIGH UNADDRESSED: INV-001).

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| S-001 | Merged set (V3 base) | 90% | All three accept ~15 Drift findings, 0 Regression, 1 HIGH |
| S-002 | Single supported severity | 95% | V1 "LOW-MEDIUM" rejected by all three |
| S-003 | Supplements allowed | 95% | Findings table stays primary |
| C-001 | V1 (MEDIUM Drift) with V2 ordering sub-point | 85% | V2 conceded HIGH; PLAN:24 and DESIGN:506 scope the gate |
| C-002 | Split (all agree: define predicate and negative cases) | 85% | DESIGN:512 |
| C-003 | V1/V2 (MEDIUM Drift, owned branch) | 90% | PLAN:305 vs PLAN:320 |
| C-004 | V3 | 95% | TOW:1011 stub; 12 asserts confirmed by advocates 1 and 3 |
| C-005 | V2 (MEDIUM) | 90% | Only V2 raised it; V1 and V3 conceded |
| C-006 | Not a deviation | 80% | V2 withdrew; DESIGN:377 |
| X-001 | V1 (refusal authorized) | 95% | V2 and V3 conceded |
| X-002 | V1 (MEDIUM) | 85% | V2 lowered to MEDIUM |
| X-003 | Drift (becomes Regression only if executed unchanged) | 90% | Round 2 unanimous |
| X-004 | Compatible | 85% | hooks.json order; freshness test |
| A-001 | QUALIFY | 90% | Authorized, consequence surfaced |
| A-002 | QUALIFY | 90% | Predictions not observations |
| A-003 | QUALIFY | 95% | Regression only for contradicted working code |
| A-004 | ACCEPT | 80% | Files absent from tree |

## Convergence Assessment
- Points resolved: 17 of 17
- Alignment: 100%
- Threshold: 80%
- Status: BLOCKED_BY_INVARIANTS (HIGH UNADDRESSED INV-001); taxonomy levels L1 (S-002, S-003), L2, L3 all covered
- Unresolved points: none among the diff points; INV-001 is carried forward
