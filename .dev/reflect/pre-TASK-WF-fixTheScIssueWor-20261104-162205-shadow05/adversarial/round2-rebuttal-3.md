# Round 2 — Rebuttal from Variant 3 advocate (refactorer/opus)

## Response to criticisms

1. **Severity inconsistency (F1 MAJOR vs F2 MINOR) — conceded, resolved upward.** R1's dichotomy is fair: F1 (plan:26/22 vs test:228) and F2 (plan:45 vs test:253) are the same root defect seen from two directions, and the Round-1 fold concession dissolves any blast-radius defense of split labels. The dichotomy has a correct arm and an incorrect arm, and the evidence picks the arm: resolve by raising F2 to MAJOR (or folding F2 into F1 at MAJOR), not by demoting F1. A label formed on the verified fact class ("pinned byte-exact text fails the plan's own pinned tests") is the consistent one; the MINOR on F2 was the labeling error, not the MAJOR on F1.

2. **Non-blocking MAJOR misdirects remediation — rejected, with a rider.** Severity and blocking are orthogonal fields in the schema all three cards use; all ten panel findings carry `blocking:false`, including R1's own three, so the schema demonstrably encodes two bits, not one. Severity grades materiality for the next reader; blocking grades remediation urgency — and "the audited reality" cuts both ways: the package is archived AND its Constraints block is provably contradictory with the tests it pins (plan:26 vs test:228). Collapsing severity into archival status erases the second half of that reality. Rider adopted: the merged card carries R1's archive-context sentence, so no reader mistakes MAJOR for act-now.

3. **MINOR merged with my test:228 citation — the merge, yes; the label, no.** The citation is not decoration; it is the fact that changes the finding's class. Once test:228/253 are in, "documentation-level only" is false: executing the pinned text yields a guaranteed red run, and copying it as template text reintroduces the #365 harness-refusal defect (test:216-220 documents the Write refusal that forced the rename). R2's C-001 vote: "winner R3 F1+F2 (disk-grounded at test:228/253), severity MAJOR, non-blocking retained."

4. **ACCEPT A-001 — maintain QUALIFY; R1's audibility goal is already met.** The diff analysis promoted A-001 to a [SHARED-ASSUMPTION] diff point, so the panel's non-blocking basis is on the record either way; ACCEPT adds nothing auditable — it asserts "will never be re-executed," which is a prediction, not an audited fact. QUALIFY records the consensus and its boundary (done/ packages are staged, re-read as records, and copied as templates). R2 independently QUALIFY'd on the same grounds. 2-1.

5. **F4/U-003 as INFO root-cause context, fold F2 into F1 — accepted, both.** These were my own Round 1 recommendations. F4 stays INFO — it is the causal explanation of C-001, not itself a deviation — and the fold happens at MAJOR per point 1.

## Final position on C-001/X-001 severity

MAINTAIN MAJOR. The finding rests on verified facts, not labels: the Constraints block pins byte-exact text whose operative contract is exactness itself (plan:22, plan:29, plan:34 "Do not touch any other wording"), and that pinned text contradicts the tests the same package pins (plan:26 vs test:228; plan:45 vs test:253) — a fresh execution following the tasklist literally fails its own Task 1 acceptance criteria, and template reuse of the pinned paragraph reintroduces the production bug the task existed to fix (test:216-220). R1's MINOR is anchored to an unverifiable prediction; a severity anchored to a verified contradiction beats one anchored to a forecast. Yes — for consistency, my F2 should be relabeled MAJOR; the cleaner fix, adopted, is folding F2 into F1 at MAJOR severity, `blocking:false`, with R1's archive-context sentence and the merged citation set (plan:26, plan:45, test:228, test:253).

## Final position on A-001

QUALIFY. Valid as the stated basis for the unanimous non-blocking call on an archived package; "never re-executed" remains unproven and the qualifier keeps the template-reuse exposure on the record (R2 concurs).

## Maintained vs conceded

Maintained: C-001/X-001 = MAJOR with `blocking:false` and R1's archive-context sentence (post-R2 unanimous); QUALIFY on A-001; F4/U-003 as INFO root-cause context; authorized-expansion convergence (INFO); fold F2 into F1 at MAJOR with merged citations.

Conceded: the F1-MAJOR/F2-MINOR inconsistency was real (resolved upward via the fold); the F1/F2 split double-counted one defect; R1's archive-context sentence belongs in the merged card; R1's audibility concern is legitimate — met by promotion + explicit disposition, not ACCEPT; F2's "cannot be met" overstatement — merged wording is "a fresh execution against the on-disk test constants fails Task 1's AC"; self-report/pin model-id discrepancy stands.

Skipped: re-running the test suite (severity turns on text-vs-text contradiction, not test execution).
