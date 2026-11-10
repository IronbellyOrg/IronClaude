# Round 2 rebuttal: Variant 3 (reviewer-3, refactorer persona)

## Response to criticisms

### 1. "C-003 is blocking, not minor: V3's minor depends on scaffolding the plan never asks for" (V1 Round 2 item 2, V2 Round 2 assessment and new evidence 1)

**Steelman of my Round 1 position.** The phrase "no synthetic substitute is written" (plan:96) applies only when the control-r1 files cannot be found. Task 3 already builds every test on tmp_path fixtures (plan:57, source.md:128). A tmp_path prior report is therefore allowed, and a capable implementer would build one. The cheapest version is a review-2 PASS report with an empty sealed ledger whose sentinel carries `spec=` (the sha256 of `spec-v2.md`) and the rubric hash. `begin` accepts a prior PASS (source.md:62), sets N = 3, and the ratchet runs.

**Response: conceded, now blocking.** Taken as written, both paths fail, and V2's mechanism is the right one:

- **No `--re-review`.** `begin` sets N = 1 (plan:57, "1 without `--re-review`"). The ratchet runs only "for reviews 2 and 3" (plan:57, source.md:64), and "review 1 has no baseline (`ratchet=off`, recorded)" (source.md:243). Every claim comes out anchored. plan:96 then makes the test assert, for each claim, that claims on text unchanged since v2 "are `late-found`". The expected set comes from the v2/v3 diff, not from `seal`'s output. source.md:193 records that 3 of the 8 claims sit on unchanged text, so that assertion fails, and the acceptance check `-k replay passes` (plan:101) cannot be met.
- **With `--re-review` on the real control-r1 report.** That report has no sentinel (V1 and V2 both checked), so `begin` exits 5 (plan:57, source.md:62).

My scaffolding route works only if the implementer designs something the plan never describes (New evidence 1). A deliverable that cannot pass its own acceptance check without unplanned design work is a missing deliverable. V1 found the defect, so V1 is the superior variant. On mechanism, V2's "loud failure" reading is right and V1's "silent 8/0 pass" is not, because plan:96 says what to assert for each claim, not just "whatever split comes out".

### 2. "C-005 / X-002 is minor: an open frozen prior already fails the verdict, and M0 counts only prior-null claims" (V1 Round 2 item 6, V2 new evidence 2)

**Steelman of my Round 1 position.** source.md:128 makes "two claims on one prior counted once" a required case. The plan never states the rule; the word "once" in that sense appears nowhere in it. A per-task executor treats the acceptance lists (plan:60, :80, :90) as its definition of done, and the case is in none of them. Nobody can write the test without inventing the rule.

**Response: conceded, now minor.** Three points decide it:

- Both verdict facts are correct. Any `confirmed` claim gives FAIL `confirmed`, and an open frozen prior gives FAIL `unresolved-prior` (plan:77). A second claim on the same prior therefore cannot flip the verdict.
- `m0_label_cm` counts only claims "whose `prior` is null" (plan:87), so prior-linked claims are outside M0 by definition.
- **Parity with C-009.** C-009 is V2's withdrawn-prior gap. It can miscount M0, the headline measure with a "<= 3" bar (source.md:185), in a rare edge case. All three of us, me included (Round 1 table), graded it minor. C-005 can miscount M1, also in a rare edge case (two claims linking the same prior). Grading C-005 blocking while C-009 stays minor would be inconsistent.

The undefined rule is also inherited from the spec: source.md:128 names the case without a rule. Task 3's body imports "the begin and seal cases of source.md section 3.4" (plan:57), so an exact follower writes some test there.

One correction to the reasoning on the other side (New evidence 2): M1 is not "reporting or display" in the cosmetic sense. It is a pre-registered measure with a stop rule. The fix therefore matters more than V1's wording suggests. It remains minor.

### 3. "R3-1 and R3-2 overgraded as blocking" (V1 Round 1 weakness 4, V2 Round 1 weaknesses 2-3)

R3-1 was conceded in Round 1. R3-2 is conceded above. No V3 finding remains blocking.

### 4. "V3's deviation counts are not tied to ids" (V1 Round 1 weakness 5, V2 Round 1 critique)

This was conceded in Round 1. It is a defect in the review card, not in the plan, so it supports the not-a-defect grade for S-002 and X-004 in item 6 below.

### 5. "R3-7 / C-017 rests on an unlikely reading" (V2 Round 1 critique)

This was conceded in Round 1 (not-a-defect). V1 Round 2 adds that even the bad reading fails at once: pytest runs from the repo root, where `./artifacts/` is not the plan folder. The failure would therefore be loud during Task 10's own run, and nothing silently breaks at archive. I accept that. My card raised a non-defect, and V1 and V2 were right to stay silent, so the superior variant moves away from V3.

### 6. C-007, S-002, X-004: Round 1 minor, now not-a-defect

**Steelman of minor.** V1's F7 point: Task 14 never says to update INSTALL.md, yet its check needs INSTALL.md to list all eleven files (plan:190). For S-002 and X-004: the plan really does carry three deviations, and V1 counted two.

**Response: conceded on all three.**

- **C-007.** Task 13 itself tells the writer to list the brief templates "written by Task 14" (plan:172; the phrase is there). The names are fixed in advance at plan:182-184, and plan:190 checks them. That is the read-ahead case I accepted under A-001 in Round 1, so the final deliverable is correct.
- **S-002 and X-004.** The declared deviations are authorized (plan:21, an owner ruling) and necessary (plan:135, which calls itself "a necessary deviation"). Neither needs a plan change. The one drift, the section-5 templates, already has its own row (C-018, minor). Grading these rows minor would count it twice. V1 remains the superior card here because it ties each count to a cited deviation.

### 7. C-002: no change

I graded it minor in Round 1, and V1 now agrees. All three variants hold minor, and V1 is superior.

## Updated assessment of the other variants

- **V1.** It is the strongest card on executability. C-003 is the one blocking defect in the plan, and only V1 found it. Its Round 2 concessions on C-002, C-007, C-017, S-002 and X-004 apply the read-ahead rule consistently. Two weak spots remain: its "silent 8/0 pass" mechanism for C-003 is wrong (V2's correction holds), and calling M1 "reporting only" stretches plan:22, whose "reporting only" sentence covers the owner's label-count measure.
- **V2.** It is the best calibrated on severity. Its C-003 mechanism is the correct one, and its C-005 argument is right on the verdict and on M0. Its coverage is still the thinnest, and it concedes that in full.
- **V3 (self).** It keeps the harness layer: C-014, C-015, C-016 and C-020. It also keeps the Usage lock-in analysis (C-004), the fix text for C-005 (dedupe by prior id in the verdict counts, the D1..Dk list and `m1_open_confirmed`), and the one drift finding (C-018). All of its blocking labels are withdrawn.

## New evidence

1. **C-003: even the cheapest scaffold forces a design choice the plan does not make.** A prior PASS is accepted, but source.md:62 says that after a PASS "the fix cycle before it gets the `NONE` brief, so the spec does not change". The fixture's baseline-to-review-3 step is a real spec change (v2 to v3), so a PASS-prior scaffold contradicts that rule. A FAIL-prior scaffold instead needs a ledger whose verdict `begin` can recompute (plan:57), with grade lines and a seal. That brings in Task 4/5 structures that the "no grader" replay (plan:96) does not set up. Either way the implementer has to invent a review-2 report shape. **Fix:** Task 7 should specify the prior report. For example: a tmp_path review-2 FAIL report produced by running the script's own `begin`/`seal`/`apply-grades`/`finalize` on `spec-v2.md` with fixture grader replies. Then add it to plan:99's file list.
2. **C-005: M1 is a decision measure, not display.** `m1_open_confirmed` is "sentinel `confirmed` plus frozen `unresolved-prior`" (plan:87, source.md:174). It is pre-registered with a "<= 3 in both" bar (source.md:186), and F1a stops the experiment at "M1 >= 4 in either replicate" (source.md:201). Task 14's recorder template records it (plan:184). Two confirmed claims linking one prior, plus that prior frozen open, could count one defect up to three times. That makes the C-005 fix higher priority than the other minors. It does not make it blocking (parity with C-009, item 2).

## Final per-point table (contested points only)

| id | severity | superior variant | changed since Round 1? |
|---|---|---|---|
| C-002 | minor | V1 | no |
| C-003 | blocking | V1 (finding); V2 (mechanism) | yes |
| C-005 | minor | V1 (severity); V3 (fix text) | yes |
| X-002 | minor | V1 | yes |
| C-007 | not-a-defect | V2 | yes |
| C-017 | not-a-defect | V1/V2 (correctly silent) | yes |
| X-004 | not-a-defect | V1 | yes |
| S-002 | not-a-defect | V1 | yes |
