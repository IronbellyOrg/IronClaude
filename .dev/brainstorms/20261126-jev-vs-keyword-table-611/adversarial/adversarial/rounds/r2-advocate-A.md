# Round 2 rebuttal: advocate A (analyzer)

## 1. Responses to the strongest criticisms of A

- **A hard-codes policy (X-001, X-002).** Conceded on retries: the rule's one rerun per failed prompt contradicts A FR-016. Countered on content: a twice-failed prompt scores not right for Jev and stays in the denominator, which is A FR-018. B's no-default rule file is the container; A's text is its content.
- **No table-before-Jev ordering, no rescore model (U-005, U-007).** Conceded; adopt B's, with table answers stored after the gate (C's U-005 note).
- **A's gate covers network, not comparison (C-004).** Conceded; the seed blocks both.
- **FR-024 stops at coordinator delivery (C section 4.2).** Conceded; add issue updates and U-009.

**How each variant absorbs the rule.** A: the sign test's b and c are A's paired breakdown (U-002), now the decision statistic; the rule's validity conditions are A's RUN_INVALID list (U-003); "unset is right for both arms" needs a table no-answer rule, which only A has (U-004). A must edit FR-016 and FR-019. B: its rule file takes the rule without code edits, but lacks a latency basis and no-answer rule. C: its frozen rule document takes it, but lacks the b/c breakdown.

**A gap the rule leaves.** Its median is over "the final answered attempt of each prompt"; a prompt failing twice has none. A FR-019 (count it at the 10-second timeout) closes that gap.

## 2. Changed positions

C-002 | MERGE | 65 | rule has two verdicts; keep A's invalid reason as a field under "not clearly"
C-003 | MERGE | 70 | rule now supplies the basis; A adds timeout value for twice-failed prompts
C-005 | MERGE | 75 | rule adopts A's not-right-in-denominator; B's rule file holds it
X-001 | B | 80 | rule permits one logged rerun counted against the cap
X-002 | MERGE | 75 | rule is PROPOSED and may change, so no-default rule file carrying A's text

## 3. Unresolved points

C-006 | MERGE | 80 | B's pre-written retry policy plus C's separately visible attempts; drop A FR-016
C-009 | B | 65 | `.dev/README.md` lines 23 and 38 put decision-informing analysis under `research/`; `experiments/` is undocumented
C-010 | MERGE | 80 | proposal's 8-2 example contradicted its formula (p 0.0547); A's restate-and-return loop caught it, C's block keeps the gate shut while PROPOSED

## 4. Round 1 majorities

Accepted: S-001 to S-003 B; C-001 A; C-004, C-005, C-008 MERGE; C-007 C; X-001 B; X-002 MERGE; A-001, A-003 MERGE; A-002, A-004 C; A-005 B. C-004's merge must use C's comparison-scope gate. Disputed, against my own variant: C-002 and C-003 should be MERGE, since the rule now supplies that content.
