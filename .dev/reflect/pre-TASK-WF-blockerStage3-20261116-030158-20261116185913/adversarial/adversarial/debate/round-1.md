# Round 1: advocate statements (parallel; both advocates sonnet class, general-purpose agent type, read-only)

Persisted verbatim by the orchestrator (harness indent removed). Advocate 1 argues for Variant 1 (reviewer-1, haiku, analyzer); Advocate 2 argues for Variant 2 (reviewer-2, opus, qa).

## Variant 1 Advocate

### Position summary

Variant 1 is accurate on both findings, but it is incomplete. It gives "fixed" verdicts on earlier findings that Variant 2 shows still carry defects, and it misses the unequal-panel threshold bias (V2 F1) and the unedited severity-floor lines (V2 F3). Variant 2 is the stronger card overall. Variant 1 still has two real unique points: R1b has no valid outcome word, and Task 5 names `verify` where the registered command is `verify-citations`.

### Steelman of Variant 2

- **F1.** The plan fixes the found threshold at more than half of each arm's valid reviewers (PLAN:82, "2 of 3 with three valid reviewers, 2 of 2 with two"). New-arm reviewers are the ones that become invalid (PLAN:82). At p=0.9, 2-of-3 gives 0.972 and 2-of-2 gives 0.81, so panel size alone can flip R2a, R2b and R3 without any owner ruling.
- **F2.** PLAN:168 requires "stays open for verification" and `consumer-unknown` after the rewrite. Both phrases already sit in the digest the same task inserts (SPEC:199, SPEC:201). The cap-sentence `grep -c` of "1 or more" (PLAN:147) is satisfied by the digest's last sentence (SPEC:207).
- **F3.** The following lines contradict the OD16(b) Rule 6 and are not in Task 8's list, and none of the stage 0 freeze patterns (S0:34) matches them.
  - rf-qa-qualitative.md:593: "Contradictions remain IMPORTANT or CRITICAL by default (cf. Critical Rule #6 below)".
  - rf-qa-qualitative.md:611: "Severity floor: IMPORTANT".
  - rf-qa-qualitative.md:616: ">= IMPORTANT".
  - rf-qa-qualitative.md:918: "Must resolve ALL CRITICAL and IMPORTANT issues".
- **F4 to F10.** These are mostly accurate, low-severity polish. Examples: "the two listed below" against three test files (PLAN:142 against PLAN:152), the missing R3 minimum n, and the fix-pass leak.

### Strengths of Variant 1

1. **R1b has no valid outcome word in the expected case.** PLAN:91 reads "one event, never advisory". PLAN:96 reads "PASS (the rule holds and the class is at or above its minimum n)", and only FAIL gets the exception "R1b fails at any n". S0:106 reads "the advisory fallback is the expected outcome". So the likely case (undersized safety class, every defect found-and-blocking) can be neither a plain PASS nor an advisory result. Variant 2 never saw this.
2. **The command-name mismatch is real.** PLAN:132 says the review help must still list `verify`. verify_cmd.py:76 reads `@click.command(name="verify-citations")`. Variant 2 does not mention it.
3. **The cross-stage checks held up.** I re-read the README:45 ledger fields, the S0 freeze pattern list and the stage 4 phrase "bold words of that line" (S4:39). All agree with Variant 1's "checked and sound" list.
4. **Its handling of R3 is defensible.** R3 at small n will most likely read NOT-MEASURABLE. That is a defined word, because the old rule already treats cosmetic as minor (pragmatic.md:225, "Minor is cosmetic"). So R1b's hole is a different kind from R3's.

### Weaknesses of Variant 2

1. **F2 is graded blocking, but the damage is small.** The negative lines still run: "claim is blocking", "it FAILS. Grade what you find" and "When in doubt, fail it" must each print 0 (PLAN:168). The replacement wording is already governed by the digest. The vacuous positive lines weaken the check but do not produce a wrong result. I grade this non-blocking.
2. **F10 is largely a non-issue.** rf-qa.md:389 ("blocking (CRITICAL or IMPORTANT)") and :476 already read as blocking through the scale map, so they need no acceptance line.
3. **F9 has no live effect.** Every current hit of the three merge-rule phrases lies in the folders the plan scans (grep of `src/superclaude/*.md`: agents, skills, templates only). Nothing lies in `core/`.
4. **F4 omits the R1b analogue.** It raises the minimum-n hole for R3 but not the stronger one for R1b.
5. **F1 states the direction of the bias with more certainty than it can support.** It depends on how many new-arm reviewers turn out invalid. The plan's own note (PLAN:80) is an opposite-direction bias from the confound. The net direction is unknown, but the defect still stands.

### Concessions

- **My own card.** Variant 1's table marks both findings MEDIUM, but the text marks both "Blocking: yes" (card lines 22 and 27). F2 is over-graded, since a loose substring check passes against `verify-citations`.
- **Earlier findings.** It calls earlier F2 and F3 "fixed". Variant 2 shows F2 introduced the panel-size bias and F3 left the unedited lines in place.
- **Coverage.** It has only two findings, and it missed F1, F2 and F3 of Variant 2.

### Shared assumptions

- **A-001: QUALIFY.** Running in order with one fix pass per task is the right frame. SKILL.md:145 reads "exactly one fix pass", followed by a repair round and a retry ladder. Task 6's self-check (PLAN:140) covers the gate case. The stage 0 to 2 outputs do not exist yet, so both cards judge them only against their producing plans. Ordering is safe; contents are a promise.
- **A-002: QUALIFY.** An owner ruling is an acceptable exit for an expected non-PASS line. It is not acceptable where the plan never defines the word: an undefined word (R1b) forces the executor to improvise a word, and a ruling cannot repair that.
- **A-003: ACCEPT.** The F4 to F16 items show as addressed in text. I checked README:45 and the S4:39 phrase. I did not verify execution, and "fixed" means only fixed in text.

### Per-point positions

| Point | Right | Defect grade | Conf | Evidence |
|---|---|---|---|---|
| S-001 | neither | not a defect (format only; V1's table says MEDIUM, its text says blocking) | 80 | card V1:22 and :27 |
| C-001 | V2 | blocking (earlier F2 and F3 are not clean) | 70 | PLAN:82, :168 |
| C-002 | V1 | blocking (R1b has no valid word in the expected case) | 60 | PLAN:91, :96; S0:106 |
| C-003 | V2 | blocking (the threshold shifts with panel size) | 72 | PLAN:82, :80 |
| C-004 | V1 | non-blocking (naming; a substring check still passes) | 75 | PLAN:132; verify_cmd.py:76 |
| C-005 | V2 | non-blocking (the negative lines still bite) | 68 | PLAN:168, :147; SPEC:199, :201, :207 |
| C-006 | V2 | blocking (the shipped agent contradicts its own Rule 6) | 72 | rf-qa-qualitative.md:593, :611, :616, :918, :990 |
| C-007 | V2 | non-blocking (PLAN:21 and PLAN:140 already say "edits nothing") | 55 | PLAN:21, :140; SKILL.md:145 |
| C-008 | V2 | non-blocking (stage 4 coupling, unpinned) | 60 | S4:39 phrase confirmed; PLAN:177 |
| C-009 | V2 | non-blocking (V2 itself hand-checked that the plan covers the rows) | 65 | card V2 F7 |
| C-010 | V2 | non-blocking (wording) | 90 | PLAN:142, :152 |
| C-011 | neither | not a defect now (no hits outside the scanned folders) | 65 | grep `src/superclaude/*.md`; SPEC:920 |
| C-012 | V1 | not a defect (the lines already read as blocking) | 60 | rf-qa.md:389, :476 |
| C-013 | both | non-blocking (observation only) | 60 | card V1 Checked and sound; card V2 T1 |
| X-001 | V1 | R1b hole blocking; R3 hole non-blocking, since NOT-MEASURABLE is likely and defined | 60 | PLAN:96; pragmatic.md:225; S0:106 |
| X-002 | V2 | blocking | 72 | PLAN:82 |
| X-003 | V2 | blocking | 72 | rf-qa-qualitative.md:593, :611, :918 |

## Variant 2 Advocate

### Position summary

Variant 2 is the stronger review. Its three blocking findings (F1 panel-size threshold, F2 vacuous positive greps, F3 unedited floor lines) all hold up against the live files, and Variant 1 saw none of them. Variant 1 is right on two points Variant 2 missed: R1b has no legal success word at small n, which is blocking, and the command is `verify-citations`, which is only a naming slip.

### Steelman of Variant 1

- **F1, strongest form.** PLAN:91 says "one event, never advisory". PLAN:96 says "PASS (the rule holds and the class is at or above its minimum n)". S0:106 says "the advisory fallback is the expected outcome". A short deliverable cannot hold the 83 to 140 defects per class, so the safety class is probably undersized. A perfect safety result then has no valid word, because PASS needs min n and ADVISORY-PASS is barred for R1b. This is the RT1 line Task 4 reads.
- **F2.** verify_cmd.py:76 is `@click.command(name="verify-citations")`, while PLAN:132 names `verify`. It is a precise, checkable slip.
- **Also right.** Its O4 reading ("those commands omit HEAD") is correct. Its cross-stage agreement check is useful.

### Strengths of Variant 2

1. **F1 is real.** PLAN:82 says "(2 of 3 with three valid reviewers, 2 of 2 with two)". At p=0.9 a 2-of-3 majority catches a defect 97% of the time and 2-of-2 catches it 81%, a gap of about 16 points. New-arm reviewers are the ones likely to be invalid (PLAN:82 "a new-arm reviewer whose quoted sentences come from the old rule is not valid"). So 3 old against 2 new is the expected case. It pushes R1 and R1b toward FAIL and R3 toward PASS, which reverses the bias PLAN:80 claims.
2. **F2 is real.** SPEC:199 says "An unverified safety claim stays open for verification". SPEC:201 says "tag the row `consumer-unknown`". SPEC:207 holds the cap sentence. PLAN:168 and PLAN:147 count with "1 or more", and the same tasks insert the digest. Only the zero-count lines do work.
3. **F3 is real.**
   - rf-qa-qualitative.md:593 reads "Contradictions remain IMPORTANT or CRITICAL by default (cf. Critical Rule #6 below)".
   - Line 611 reads "Severity floor: IMPORTANT" and line 616 reads ">= IMPORTANT."
   - None matches the S0:34 freeze patterns, none is in Task 8, and a grep of `tests/` for these strings found nothing, so they are safe to edit.
   - They contradict SPEC:203 "the label ... is information, never the grade".
4. **F6 is real.** S4:39 reads Rule 6 with awk `^6\. \*\*`. That prints nothing if Task 8 drops the bold heading.
5. **Its "line numbers hold" claim checks out.** rf-qa.md lines 83, 100, 402, 548 and 549 and rf-qa-qualitative.md lines 84, 99, 809, 990, 993 and 994 all match the plan's quotes.
6. **R3.** pragmatic.md:225 reads "Minor is cosmetic", so a NOT-MEASURABLE R3 is likely.

### Weaknesses of Variant 1

1. Its "Checked and sound" bullet 4 tests only the removal side ("claim is blocking" is absent from the digest). It misses that the digest supplies the positive phrases (SPEC:199, SPEC:201), so PLAN:168 and PLAN:185 pass vacuously.
2. It finds "no additional mandatory re-pin" and never reads rf-qa-qualitative.md:593, 611 or 616. The gap is in content, not in test pins.
3. It marks earlier F2 "fixed" without running the rule on unequal panels, although PLAN:80 makes directional claims that the 2-of-3 versus 2-of-2 rule can reverse.
4. It overgrades its F2. `grep -w verify` matches `verify-citations` (the hyphen is a non-word character), so the check can be met and the intent is clear. By rule 4 this is wording.
5. It is thin. It has 2 findings for 14 tasks, and F4 to F16 are "addressed in text" with one citation. Its "Drift" category fits spec divergence, not plan defects.

### Concessions

- V2 missed the R1b hole and the `verify-citations` slip.
- V2 F7 reviews the orchestrator's coverage-matrix.yaml (header: "Containment items: Constraints block + Tasks 1-14"), not the plan. V2 itself says everything is covered, so it is not a plan defect.
- V2 F10 says rf-qa.md:389 and :476 are "named in Task 7's body". A grep for `389|476` in the plan finds nothing, so that premise is wrong.
  - The gap still exists: line 389 reads "blocking (CRITICAL or IMPORTANT)" and line 476 reads "Must resolve ALL [N] blocking (CRITICAL/IMPORTANT)".
  - These are relay or read-back wording, so I grade them below F3.
- V2's 97% versus 81% figures assume independent reviewers at p=0.9 and are illustrative.
- F9 causes no miss today. All 11 `*.md` files in `src/superclaude` with merge-rule phrases sit inside the scanned folders.

### Shared assumptions

- **A-001: QUALIFY.** Order is fine, but "one fix pass" (SKILL.md:145 "exactly one fix pass") is the route for V2 F5. Stage 0 to 2 outputs are only specified, so the S0 inventory is not observed and will not list lines 593 to 616.
- **A-002: QUALIFY.** A ruling is acceptable when the word is true but not PASS (PLAN:98). It is not acceptable when the word set cannot express the true result (R1b) or when panel size manufactures the non-PASS (V2 F1). The ruling would then rest on a false word.
- **A-003: QUALIFY.** The text fixes hold where I checked them. F3's fix is incomplete and F2's fix creates a new defect, so "fixed" holds only at text level.

### Per-point positions

| point | right | defect grade | conf | evidence |
|---|---|---|---|---|
| S-001 | neither | not a defect | 80 | format only; V1 labels plan defects "Drift" |
| C-001 | V2 | blocking | 75 | PLAN:82; SPEC:199; PLAN:168 |
| C-002 | both | R1b blocking (soft), R3 non-blocking | 62 | PLAN:91, :96; S0:106; pragmatic.md:225 |
| C-003 | V2 | blocking | 72 | PLAN:82, :80 |
| C-004 | V1 on fact | non-blocking (wording) | 70 | verify_cmd.py:76; PLAN:132 |
| C-005 | V2 | blocking (rule 8/9 phrase lines), cap part minor | 58 | SPEC:199, :201, :207; PLAN:168, :147 |
| C-006 | V2 | blocking (593/611/616); 918 minor | 70 | rf-qa-qualitative.md:593, :611, :616, :918; S0:34 |
| C-007 | both | non-blocking | 60 | PLAN:21, :140; SKILL.md:145 |
| C-008 | V2 | non-blocking | 65 | S4:39 `^6\. \*\*` |
| C-009 | neither | not a plan defect | 80 | coverage-matrix.yaml:1 |
| C-010 | V2 | non-blocking (wording) | 85 | PLAN:142 "the two listed below"; PLAN:152 lists three |
| C-011 | V2 | non-blocking, no current miss | 60 | SPEC:920 "`src/` or `plugins/`" |
| C-012 | V2, with premise error | non-blocking | 55 | SPEC:270; PLAN:158; no 389/476 in plan |
| C-013 | both | not a defect | 70 | S2:122 |
| X-001 | both | R1b blocking, R3 non-blocking | 65 | R1b has "never advisory"; R3 has no min n |
| X-002 | V2 | blocking | 72 | PLAN:82 |
| X-003 | V2 | blocking | 70 | rf-qa-qualitative.md:593, :611 |
