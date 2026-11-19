# Adversarial Debate Transcript

Assembled from `round1-advocate-1.md`, `round1-advocate-2.md`, `round1-advocate-3.md` (same folder) and `round2-rebuttals.md`. Quotes are copied from those files; nothing here is new evidence. Variants: V1 = `reviewer-cards/reviewer-1-card.md` (analyzer, sonnet), V2 = `reviewer-2-card.md` (qa, haiku), V3 = `reviewer-3-card.md` (refactorer, opus). Plan under review: `.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md`.

## Metadata
- Depth: standard
- Rounds completed: 2 (round 1 advocate statements; round 2 orchestrator-verified rebuttals and verdicts; no round 3)
- Convergence achieved: 78.4% (13.33 of 17 points, grade agreement of the three advocates with the final grade)
- Convergence threshold: 80%
- Focus areas: C-001 to C-014, X-001 to X-003, shared assumptions A-001 to A-005
- Advocate count: 3

## Round 1: Advocate Statements

### Variant 1 Advocate (`round1-advocate-1.md`)
**Position**: card 1's line cites hold (guard lines 10, 444, 653, 764, 786, 790; `cycle.py` order); C-007, C-009, C-008 are correct. Concedes it "missed C-001, C-003 and C-005" and that Q-1 is PARTIAL because "the `p.complete.run()` case is unmatchable (X-001)".
**Steelman of the others**: card 2's QA-2 and QA-1 "are real"; card 3's B-1 is "the strongest" (`stage-status` calls `gh.reread` with no repo, `github.py:37`).
**Weaknesses identified**: card 2's severity column contradicts its prose (S-002) and it calls the Task 10/11 order sound; card 3 over-grades C-002 ("a wording gap that a parse test would catch") and C-006.
**Concessions**: C-001 Blocking (Safety, 0.65), C-003 Blocking (Decision, 0.7), C-009 downgraded to Note, Q-1 PARTIAL.
**Net position**: Blocking C-001 and C-003; Medium C-002, C-004, C-005, C-006, C-007, C-008, C-011, C-014; Note C-009, C-010, C-012, C-013.

### Variant 2 Advocate (`round1-advocate-2.md`)
**Position**: QA-1, QA-2 and QA-3 are all Blocking under the rule; "I withdraw the card's inconsistent severity presentation."
**Steelman of the others**: card 1 sees that "a retry cannot reconstruct a Status-specific launch from data it never saved" (C-007); card 3's cross-repo finding "is the strongest new safety finding".
**Key claims**: C-004 "is a literal mismatch, not speculation about an exotic bypass"; C-005 "is V2/U-004's strongest missing-deliverable finding"; seven Blocking positions (C-001 to C-006 plus C-014) and X-002.
**Concessions**: C-001, C-002, C-006 adopted from card 3; C-007 and C-008 from card 1; C-010 narrowed ("the first clause of `:30` already says all tasks editing the same file run in plan order"); A-002 and A-005 rejected.

### Variant 3 Advocate (`round1-advocate-3.md`)
**Position**: only card 3 traced the coordinator's approval read end to end (B-1) and put Task 3 and Task 5 side by side (B-2).
**Weaknesses identified in the others**: C-003 is "true but overstated. An enforcement point does exist ... `stage_predicates._label_channel` ... `label-before-plan` (`stage_predicates.py:161-170`)"; C-004 "QA-3 is mostly false: the reading is too literal"; C-005 "is Medium rather than Blocking".
**Concessions**: C-009 to Medium (card 1's grade), "C-014 is card 2's find, missed by card 3", X-002 "I concede it is FIXED", C-012 and C-013 Note.
**Net position**: Blocking C-001 (Safety, 0.8), C-002 (Decision, 0.65), C-006 (Decision, 0.6); Medium C-003, C-004, C-005, C-007, C-008, C-009, C-010, C-011, C-014; Note C-012, C-013.

## Round 2: Rebuttals
Full text in `round2-rebuttals.md`. One rebuttal per side was drawn from the advocates' own Round 1 evidence for C-003 and C-004 (the two disputes the orchestrator settled by reading and running a `case` test), with verdicts on C-001, C-002, C-005, C-006, C-007, C-008, C-009 to C-014 and X-001 to X-003.

### Final positions after Round 2
- C-001: V1, V2, V3 agree Blocking (Safety); the orchestrator confirmed it in `cli.py:279,282`, `reads.py:67,142,148`, `github.py:37`.
- C-003: V1 and V2 Blocking, V3 Medium; verdict Blocking (Decision) because the check as written cannot pass (`approval_record.py:313-359`), while the rule exists at `stage_predicates.py:161-170`.
- C-004: V2 Blocking, V1 and V3 Medium; verdict Blocking (Decision) after the case run showed bare `p.complete.run()` allowed and `plan-hash` with a `completed` path refused.
- C-002 and C-006: V2 and V3 Blocking, V1 Medium; verdict Blocking (Decision).

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | V3 | 60% | B-/M-/N- with evidence and fix is the most usable shape for the merge |
| S-002 | V3 | 80% | V3 carries the category and the affected action; V2's label contradicts its column |
| S-003 | V3 | 55% | V2 marks Q-1 PARTIAL correctly but V3 marks Q-6 and Q-10 PARTIAL; mixed |
| C-001 | V3 | 80% | `cli.py:279`, `reads.py:142,148`, `github.py:37` |
| C-002 | V3 | 70% | `github.py:764-775`, plan:61, plan:84 |
| C-003 | V2 | 60% | V2 saw the unsatisfiable check; V3 located the real rule |
| C-004 | V2 | 65% | case run: bare case allowed, `plan-hash`/`completed` refused; V1/V3 added over-matches |
| C-005 | V2 | 60% | `source.md:36,40` lifecycle missing from plan:356 (graded Medium) |
| C-006 | V3 | 65% | `brief.py:51-74` has no level parameter |
| C-007 | V1 and V3 | 85% | `cycle.py:1308-1314`, `record.py:68-88` |
| C-008 | V1 | 80% | helper order; zero/several items unsaid |
| C-009 | V1 | 70% | `cycle.py:767-768` runtime value; graded Note |
| C-010 | V3 | 70% | plan:30 incomplete; graded Note because the general rule covers it |
| C-011 | V3 | 60% | guard blind to scripts, refuses inline forms; overstated but real |
| C-012 | V3 | 70% | plan:15 vs plan:24-25 |
| C-013 | V1 | 50% | inferred budget cost |
| C-014 | V2 | 70% | plan:268 vs plan:323 |
| X-001 | V2 | 80% | PARTIAL |
| X-002 | V3 | 60% | PARTIAL at Note level (V2's Blocking and V3's FIXED both overruled) |
| X-003 | V3 | 80% | PARTIAL (same as C-010) |

Wins by point (20 rows; C-007 shared V1/V3, counted half each): V3 11.5, V2 5 (C-003, C-004, C-005, C-014, X-001), V1 3.5 (C-007 half, C-008, C-009, C-013).

## Convergence Assessment
- Points resolved: 17 of 17 settled by the orchestrator; agreed by advocates on the final grade: 7 at 3/3, 9 at 2/3, 1 at 1/3.
- Alignment: 13.33 / 17 = 78.4%
- Threshold: 80%
- Status: NOT_CONVERGED (by 1.6 points; C-004 alone decides it)
- Unresolved points: C-004 (1/3); partially agreed (2/3): C-002, C-003, C-005, C-006, C-009, C-010, C-014, X-001, X-002.
