# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 plus Round 2.5 (invariant probe) plus one extra resolution round (Round 3, triggered by the invariant-probe gate)
- Convergence achieved: 100% on the protocol's majority-agreement basis (20 of 20 diff points); 75% on the unanimous basis (15 of 20)
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3 (V1 sonnet class, V2 haiku class, V3 opus class; general-purpose agents, read-only)
- Advocate failures: none. Reviewers 1 and 3 hit the 50-turn limit before returning their cards (Wave 3, not this step) and were resumed once.

The full statements are kept in separate files so that nothing is paraphrased:
- Round 1: `debate/round1-advocates.md` (three advocate statements, run in parallel)
- Round 2: `debate/round2-rebuttals.md` (three rebuttals, run in sequence V1, V2, V3; each advocate had the Round 1 transcripts and the earlier rebuttals)
- Round 2.5: `invariant-probe.md` (fault-finder, 12 findings)
- Round 3 (extra): `debate/round3-invariant-resolution.md` (three advocates in parallel on INV-001 and INV-002, plus the orchestrator's ruling)

## Round 1: Advocate Statements
See `debate/round1-advocates.md`. Summary of the positions: V1 graded the strict-T2 gap (C-001) and the spec 10.5 gap (C-002) minor and said no blocking defect exists; V2 graded C-002 blocking and C-001 minor; V3 graded C-001 MEDIUM and C-002 MEDIUM and conceded its own blocking grade on C-001. All three answered ACCEPT, QUALIFY, QUALIFY (V2: REJECT on A-003) on the shared assumptions; no omission flagged.

## Round 2: Rebuttals
See `debate/round2-rebuttals.md`. Positions after Round 2: V1 and V3 graded C-001, C-002 and C-009 MEDIUM; V2 graded C-001 and C-009 MEDIUM and kept C-002 blocking (spec line 867 names the roadmap pointer; roadmap SKILL.md line 563 holds the escalation instruction, which spec line 861 describes as "escalates"). C-011 was dropped by all three.

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| S-001 | none (Low, cosmetic) | 60% | depth of the Checked section differs; no effect on a grade |
| C-001 | settled MEDIUM (V1 and V2 moved up from minor, V3 moved down from blocking) | 95% | P4:112 example already fails under S1:223's non-strict T2, but P4:108 and P4:112 require strict mode; unanimous after Round 2 |
| C-002 | MEDIUM (V1, V3) | 75% | SPEC:867 row names roadmap and tech-research; no task or recorded exclusion; no wrong result; V2 dissents (blocking) |
| C-003 | minor (all) | 95% | P4:41 passes and fails the all-complete archive-blocked package; intent stated |
| C-004 | minor (V1, V3; V2 did not raise) | 90% | P4:37 grep returns about ten lines; line 990 is Critical Rule 6 |
| C-005 | minor (V1 raised; V2, V3 agree) | 85% | SPEC:739 both maps CRITICAL to Blocking and says narrow it; plan records the pin as reason |
| C-006 | minor (V1 raised; V2, V3 agree) | 85% | cap-sentence greps already print 1 today; the `v2 begin` grep discriminates |
| C-007 | minor (V3 raised; V1, V2 agree) | 85% | MAP:102 pins only "otherwise it is Medium" in the FR-8 line; P4:96 grep needs the edit anyway |
| C-008 | minor (V3 raised; V1, V2 agree) | 85% | S3:214 stale text about a plugin mirror; belongs to the stage 3 plan |
| C-009 | MEDIUM (all, after Round 2) | 85% | P4:108 may reword doctor.py; P4:113 omits the doctor tests |
| C-010 | minor (V3 raised; V1, V2 agree) | 85% | P4:116 cites the Task 6 summary |
| C-011 | drop (all, after Round 2) | 90% | defect of the review's coverage record, not of the plan |
| X-001 | MEDIUM | 95% | follows C-001 |
| X-002 | MEDIUM (V1, V3) | 75% | follows C-002; V2 dissents |
| X-003 | no blocking finding (V1, V3) | 75% | verdict follows C-002 only for V2 |
| X-004 | minor | 95% | V1's Checked cites P4:87 for the plugin decision; it is at P4:23 and P4:91 |
| X-005 | minor (V2, V3; V1 said drop) | 80% | V3's paraphrase of SPEC:867 is incomplete, not false |
| A-001 | ACCEPT (all) | 95% | S1:223 states non-strict T2 and "strict mode is a switch, off in this phase" |
| A-002 | QUALIFY (all) | 90% | cross-stage facts are plan text; Task 1 checks only the stage 3 state |
| A-003 | QUALIFY (V1, V3; V2 REJECT) | 70% | no test has run; the 12-test list also omits the doctor tests |
| INV-001 (probe) | MEDIUM (V1 MEDIUM, V2 minor, V3 blocking; orchestrator ruling: median MEDIUM) | 55% | S5 bullet at `agent_template_qa.md:140` not named by Task 1, no check |
| INV-002 (probe) | MEDIUM (V1, V3; V2 minor) | 70% | Task 4's Unattended line vs the Contract bullet's `artifacts` clause |

## Convergence Assessment
- Points resolved: 20 of 20 (majority basis); unanimous on 15 (S-001, C-001, C-003, C-004, C-005, C-006, C-007, C-008, C-009, C-010, C-011, X-001, X-004, A-001, A-002)
- Alignment: 100% (majority basis, the protocol definition); 75% (unanimous basis, reported in the contract as the conservative figure)
- Threshold: 80% (majority basis passes; the unanimous basis is at the 0.75 PASS line of the reflect convergence routing)
- Taxonomy coverage gate: L1 (naming and wording: C-003, C-004, C-006, C-008), L2 (structure: C-001, C-002, C-007), L3 (state mechanics and guards: C-001 strict switch, C-009, INV-001, INV-002) all covered
- Invariant probe gate: BLOCKED by INV-001 (HIGH, UNADDRESSED) after Round 2.5; resolved by Round 3 (debated by all three advocates, graded MEDIUM by median); no HIGH UNADDRESSED item remains; INV-002 (MEDIUM) is a warning and did not block
- Status: CONVERGED
- Unresolved points (dissent recorded, not blocking convergence): C-002/X-002/X-003 (V2 advocate: blocking), A-003 (V2: REJECT), INV-001 (three different grades; median applied)
