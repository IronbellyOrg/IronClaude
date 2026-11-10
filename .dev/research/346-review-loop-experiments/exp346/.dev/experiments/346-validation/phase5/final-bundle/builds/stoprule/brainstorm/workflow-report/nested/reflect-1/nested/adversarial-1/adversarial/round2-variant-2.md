# Round 2 rebuttal: Variant 2 (reviewer-2, qa persona)

## Response to criticisms

### 1. "V2's coverage is thin: 2 findings against 12 and 12+1" (V1 weakness 3, V3 weakness 5, V1 Round 2 assessment)

**Steelman.** A card that audits 35 units, calls 33 adherent and reports 2 findings missed real defects that the other cards verified. These include C-003 (the replay prerequisite), C-004 (the Usage-line lock-in), C-006 (staging after Task 12) and the harness layer (C-014, C-015, C-016, C-020). Its own calibrator then listed further unchecked spec items, one of them the counted-once case (C-005). A reader who relied on V2 alone would ship a plan with a blocking defect.

**Response: conceded in full.** This is the main weakness of V2. I do not claim that V2's 33/35 adherence figure is accurate, because C-003 alone falls inside a unit V2 marked adherent (the section 3.4 replay fixture). What V2 still adds is narrow: the only check of the `count` rule against the M0 definition (C-009), which V1 Round 2 accepts as "a real addition".

### 2. "QA-001 misreads scope; the measurement copy is not a deliverable" (V1 weakness 1, V3 weakness 3)

**Response: conceded in Round 1, no change.** plan:20 says nothing is installed, and source.md:163 is an install step. Only the INSTALL.md sentence at plan:172 ("differ only in the lines that came from master") is asserted without a check. Minor. V1 is superior on C-008.

### 3. "QA-002 is overgraded as blocking" (V1 weakness 1)

**Response: conceded in Round 1, no change.** The count is reporting only (plan:22). The finding itself stands, and both other cards now accept it. I re-checked it. Task 3's first-pass `form` line records `id` and `claimed` only (plan:57). Task 6's `m0_label_cm` needs "`prior` is null" (plan:87). So a carried prior withdrawn between seals cannot be excluded, as M0 requires (source.md:173). Minor, V2.

### 4. "V2's deviation counts are wrong: authorized 0, necessary 0" (V1 weakness 2, V3 weakness 4)

**Response: conceded in Round 1, no change.** plan:21 is an owner ruling (authorized). plan:135 calls its own edit "a necessary deviation". V1's mapping is correct, which settles S-002 and X-004 in V1's favour.

### 5. "V2 missed C-003" (V2 self-concession, V1)

**Response: conceded.** I add evidence on C-003 below, and the evidence changes how the defect shows up but not its severity.

## Updated assessment of the other variants

- **V1.** Its Round 2 concessions on C-002, C-007, C-017, S-002 and X-004 apply the read-ahead rule that V2 and V3 proposed for A-001, so V1's table and mine now agree on every contested severity. Its C-003 severity is right. Its new "silent pass" argument is wrong on the text (New evidence 1). The steelman is that "the test asserts the computed split ... without forcing it to 5 and 3" (plan:96) could be read as "assert whatever split comes out". That reading drops the clause just before it, which tells the test what to assert for each claim: claims quoting changed lines "are not `late-found`", and claims on unchanged text "are `late-found`". So C-003 is a loud failure, not a silent wrong deliverable. It is still blocking, because the Task 7 deliverable cannot be produced from the plan's text. V1's bounded-effect argument on C-005 is correct, and I extend it below.
- **V3.** It is strongest on the harness layer and on the Usage lock-in. On C-005 it argues that the case is in no acceptance list and the rule is undefined. That is accurate, but it does not meet the blocking test. Task 3's body imports "the begin and seal cases of source.md section 3.4" (plan:57), and source.md:128 lists the counted-once case among those seal-adjacent cases, between "valid and invalid prior links" and "uncovered hunk". The undefined rule cannot change the verdict or M0 (New evidence 2). On C-003, V3's "minor" depends on tmp_path scaffolding the plan never asks for. A strict follower could also read plan:96's "no synthetic substitute is written" as forbidding it, since a sentinel-bearing review-2 report would be a synthetic stand-in for a control-r1 file that does not exist in that form.

## New evidence

1. **C-003: the literal review-1 run fails loudly; it does not pass vacuously.** Without `--re-review`, `begin` sets N = 1 (plan:57; source.md:62), and the ratchet runs only "for reviews 2 and 3" (plan:57; source.md:64, :243). V1 is right that every claim then comes out anchored. But plan:96 makes the test assert two things for each claim. Claims quoting lines changed between v2 and v3 must not be `late-found`, and claims on text unchanged since v2 must be `late-found`. The expected set comes from the v2/v3 diff (`changed_lines`, plan:57), so it does not depend on `seal`'s output. source.md:193 records that 3 of the 8 control-r1 claims "sit on text the previous review already saw". Those 3 come out anchored at review 1, so the second assertion fails, and Task 7's acceptance check `uv run pytest ... -k replay` passes (plan:101) cannot be met. The only case where the review-1 run passes is the one where all 8 claims quote changed lines. In that case ratchet on and ratchet off give the same result, so even that pass is not a wrong deliverable. Two literal paths remain, and both block: no `--re-review` (the assertion fails) or `--re-review` on the plain control-r1 report (exit 5). The only way through is a hand-built review-2 report with its own checks, which the plan neither specifies nor clearly permits. Result: blocking (missing deliverable), V1 superior, mechanism corrected.
2. **C-005: neither the verdict nor M0 can change.** A frozen prior that is still open already gives FAIL `unresolved-prior` (plan:77), and any `confirmed` claim gives FAIL `confirmed` (plan:77). So a second claim on the same prior cannot flip the verdict, however it is counted. `m0_label_cm` counts only claims "whose `prior` is null" (plan:87), so claims carrying a prior link are outside M0 by definition. What remains is `m1_open_confirmed` and a possible duplicate entry in the D1..Dk listing. Both are reporting or display. Minor. V1 has the severity right. V3's naming of the three counters gives the better fix text.

## Final per-point table (contested points only)

| id | severity | superior variant | changed since Round 1? |
|---|---|---|---|
| C-002 | minor | V1 | no |
| C-003 | blocking | V1 | no |
| C-005 | minor | V1 (severity); V3 (fix text) | no |
| X-002 | minor | V1 | no |
| C-007 | not-a-defect | V2 | no |
| C-017 | not-a-defect | tie (V2/V3) | no |
| X-004 | not-a-defect | V1 | no |
| S-002 | not-a-defect | V1 | no |
