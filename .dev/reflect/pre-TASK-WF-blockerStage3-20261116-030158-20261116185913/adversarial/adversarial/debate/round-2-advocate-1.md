# Round 2: rebuttal of the Variant 1 advocate (sequential, first; sonnet, general-purpose, read-only)

Persisted verbatim by the orchestrator (harness indent removed).

## Response to criticisms

**(1) C-005, vacuous positive greps.** V2's advocate is right that the checks are vacuous.
- Today's `rf-qa.md` and `rf-qa-qualitative.md` contain neither "stays open for verification" nor "consumer-unknown". My grep of both files for those strings found no hit in either.
- The digest inserted by the same task supplies both strings (SPEC:199 "An unverified safety claim stays open for verification"; SPEC:201 "tag the row `consumer-unknown`"). So PLAN:168 and PLAN:185 pass with no rewrite at all.
- The zero-count lines (PLAN:168 "claim is blocking", "it FAILS. Grade what you find", "When in doubt, fail it") do force the old doubt-grading text out. A task that deletes principle 8 and rule 9 outright passes every acceptance line. Task 12 then re-pins the Critical Rules hash to whatever text remains.
- The consequence is lost prose: the "benefit of the doubt, verify" anchor and "A false PASS is worse than a false FAIL". No contradicting grade survives, because the digest already governs doubt through "Unknown is not no".
- The cap-sentence check (PLAN:147) is harmless: SPEC:213 makes the digest's last sentence the cap bullet "word for word", so deleting the bullet changes nothing. The own-model bullet check is not vacuous, because the digest words that idea differently.
- I still grade this non-blocking, because no wrong verdict or gate result can come from it. It deserves a one-line fix: `grep -n "NO LENIENCY" file | grep -c "stays open for verification"`, and the same pairing for "Report honestly" with "consumer-unknown".

**(2) C-012.** I moved from "not a defect" to "defect, non-blocking". SPEC:853 assigns rf-qa.md lines 389 and 476 to stage 3. The live lines read "For each blocking (CRITICAL or IMPORTANT) issue" (389) and "Must resolve ALL [N] blocking (CRITICAL/IMPORTANT) issues" (476). Task 7's body names "the count-CRITICAL-and-IMPORTANT-as-blocking lines" only as a subset of the stage 0 inventory (PLAN:158). The S0:34 freeze patterns (`= FAIL`, `never minor`, `Any CRITICAL or IMPORTANT issue exists` and similar) match neither line, so the inventory will not list them. V2's premise error is smaller than conceded: the body names the category, just not the line numbers. Consequence: the lines are a relay count and a re-verify scope, set after the verdict. The verdict comes from the reworded PASS/FAIL bullets. The L1 text at PLAN:158 omits the `reasked` flag and "listed first" (SPEC:270), but the digest in the same file already carries the terminal rule (SPEC:201). Non-blocking.

**(3) C-006.** I moved from blocking to non-blocking for the group.
- The lines at 593, 611 and 616 assign a label only.
  - 593: "Contradictions remain IMPORTANT or CRITICAL by default (cf. Critical Rule #6 below)".
  - 611: "Severity floor: IMPORTANT".
  - 616: "severity >= IMPORTANT".
  - Under SPEC:203 the label is "information, never the grade".
  - Both QA agents already carry line 111 "grade by the definition above, not by the label, so a finding labelled IMPORTANT that is only wording is minor", next to those floors today.
  - A floor label affects the outcome only when the consumer is unknown. There the reviewer's label stands and reads blocking, which matches the digest's `consumer-unknown` row (SPEC:229).
- The stale "cf. Rule #6" cross-reference is real. Task 8 should reword all three lines.
- Line 918 ("Must resolve ALL CRITICAL and IMPORTANT issues") and rf-qa.md:476 are relay strings sent after a FAIL. They are the only ones that could prompt a fix of a mislabelled Medium row. That is rare, because it needs a Medium row labelled IMPORTANT. Treat them as one small group with 389.

**(4) C-003.** I still grade it blocking. The unequal-panel artifact is large against the test's resolution. At p=0.9, a 2-of-3 majority finds 0.972 and 2-of-2 finds 0.81, a 16-point gap against a 5-point design margin (S0:106). PLAN:80 asserts the bias directions, and unequal panels reverse them. The mitigations hold but are partial.
- The as-run variant sits beside each word.
- On R1, R1b, R2a and R2b the artifact errs toward FAIL, which forces a ruling (the safe side).
- RT3 reads R1, R2a and R2b (SPEC:987), so it is judged on the conservative side.
- R3 is the exception. It errs toward PASS, so a false PASS needs no ruling. It is not a revert trigger, so this is an assurance failure and not a safety failure.
- The words the owner rules on are therefore computed from a known artifact. Minimal fix: score both arms on the same k, the smaller valid count, and list the dropped reviewers.

**(5) C-002/X-001.** Confirmed. PLAN:91 says R1b is "one event, never advisory". PLAN:96 PASS needs "the class is at or above its minimum n". ADVISORY-PASS is barred for R1b. FAIL needs "the rule does not hold". NOT-MEASURABLE lists R1, R2a, R2b, R3 or an arm with fewer than 2 valid reviewers, not R1b. S0:106 makes an undersized safety class the expected outcome. In that case no word fits. An executor could improvise a false FAIL, which Task 14 would then report as RT1 tripped (PLAN:257). It could also pick ADVISORY-PASS, which forces a ruling in the expected case. Minimal fix, appended to PLAN:96: "R1b has no minimum n and is never advisory: PASS when every planted safety defect is found-and-blocking under the new text, FAIL otherwise; show n and the interval beside it." The R3 gap stays non-blocking: NOT-MEASURABLE is likely and defined.

**(6) A-003.** ACCEPT. The assumption covers earlier F4 to F16 only. The earlier report shows F13 is cap placement and F15 is the missing-command clause (REPORT.md lines 132 and 143). The V2 defects sit in earlier F1 to F3 and are handled under C-003, C-005 and C-006. "Fixed" still means fixed in text only.

## Updated assessment

- C-006 went from blocking to non-blocking.
- C-012 went from "not a defect" to a non-blocking defect.
- C-005 is conceded as a real defect and stays non-blocking.
- C-003, C-002 and X-001 hold at blocking.

## New evidence

- rf-qa.md:100, rf-qa.md:548, rf-qa-qualitative.md:99 and :993 (live grep): the old principle 8 and rule 9 contain neither positive phrase, so the PLAN:168 and PLAN:185 counts come only from the digest.
- S0:34: the freeze patterns do not match rf-qa.md:389 or :476.
- SPEC:987: RT3 reads recall lines R1, R2a and R2b only.
- Both QA agents carry line 111 "grade by the definition above, not by the label".

| point | final position of V1 advocate | blocking or non-blocking | confidence |
|---|---|---|---|
| C-002 | R1b has no valid outcome word in the expected small-n case. Add an explicit R1b PASS/FAIL rule. | blocking (R1b); R3 non-blocking | 62 |
| C-003 | Unequal-panel threshold is a 16-point artifact against a 5-point margin. Score both arms on the same k. | blocking | 68 |
| C-005 | The two phrase checks and the cap check pass vacuously. The zero-count lines still force out the doubt text. The consequence is lost prose, not a wrong grade. | non-blocking | 62 |
| C-006 | The floor lines assign a label only. Lines 918, 476 and 389 are relay strings. Reword all of them in Task 8. | non-blocking | 60 |
| C-012 | Lines 389 and 476 are a real coverage gap (not in the freeze, no acceptance line). The L1 omissions are covered by the digest. | non-blocking | 58 |
| X-001 | R1b hole blocking, R3 hole non-blocking | blocking (R1b only) | 62 |
| A-003 | ACCEPT, scoped to earlier F4 to F16 and fixed in text only | non-blocking | 70 |
