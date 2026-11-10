# Round 2 rebuttal: Variant 1 (reviewer-1, analyzer)

## Response to criticisms

### 1. "F1 / C-002 is a forward reference that read-ahead resolves" (V2 weakness 1, V3 weakness 1)

**Steelman.** The blocking test asks about the deliverable, not about per-task friction. Task 3 says `begin` must exit 5 "when the recomputed prior verdict differs from its last line" (plan:57), and its acceptance list names "prior-verdict mismatch" (plan:60). The verdict rule is fully written down later in the same plan (plan:77, `compute_verdict` per step 9) and in source.md step 9. An implementer who holds the whole plan writes `compute_verdict` during Task 3, and Task 5 then only adds `status`, `verdict` and `finalize` around it. After Task 6 the script and its tests are correct.

**Response: conceded, now minor.** My Round 1 case rested on per-task QA rejecting Task 3. That is a cost in rework and QA friction. It is not a wrong or missing deliverable. Nothing has to be invented: every rule Task 3 needs is defined in plan:77 and source.md step 9. The fix is still worth making: move `compute_verdict` into Task 3, or move the mismatch case into Task 5's acceptance list. But it is minor.

### 2. "F3 / C-003 is minor because tmp_path scaffolding gives the right files" (V3 weakness 1, V3 per-point C-003)

**Steelman.** The rule "no synthetic substitute is written" (plan:96) covers only missing control-r1 files, so it does not forbid a test that builds a prior review-2 report in tmp_path. A competent implementer would see that `begin` needs a review-2 sentinel and would build one, and then the replay asserts a real split.

**Response: not conceded. New evidence makes this a silent wrong deliverable, not just a blocked step.** Take the text exactly as written. The test "runs `begin` and `seal` (no grader) on the fixture with `spec-v2.md` as baseline" (plan:96), and it names only three fixture files with no prior report (plan:96, acceptance at plan:99). With no `--re-review`, `begin` sets N = 1 (plan:57, "1 without `--re-review`"; source.md:62). The ratchet runs only "for reviews 2 and 3" (plan:57), and "review 1 has no baseline (`ratchet=off`, recorded)" (source.md:243). So every claim comes out anchored: 8 anchored, 0 late-found. The plan then tells the test to assert "the computed split ... without forcing it to 5 and 3" (plan:96). The 8/0 run therefore passes every acceptance criterion in Task 7 and gets recorded in `t7-fixture-sources.txt` as the replay result. The deliverable is wrong: a replay fixture that never exercises the ratchet. Every listed check still passes. The other reading, passing `--re-review`, needs a sentinel-bearing review-2 report, and the control r1 reports have none (the folder holds only plain `spec-panel*.md` reports; V2 verified this independently). On that reading `begin` exits 5. V3's scaffolding route is possible, but the plan never asks for it. The scaffold also has to satisfy four checks: a `review=2/3` sentinel, a `spec=` hash equal to the sha256 of `spec-v2.md`, a matching rubric hash, and a verdict that can be recomputed from its ledger (source.md:62). That is a design task the plan never gives. Blocking stands. V2 agrees.

### 3. "F2 / C-001 overstated" (V2, V3)

Already conceded in Round 1 (now minor). No change.

### 4. "V1 misses the harness layer" (V3 weakness 2)

Conceded in Round 1: C-014, C-015, C-016 and C-020 belong to V3. No change.

### 5. "V1 missed the withdrawn-prior counting gap" (V2 weakness 5)

Conceded in Round 1: C-009 belongs to V2. No change.

### 6. C-005 / X-002: V3 holds that the missing counted-once case is blocking

**Steelman (V3).** source.md:128 makes "two claims on one prior counted once" a required case. No acceptance list contains it (plan:60, :71, :80, :90). The rule is never defined, so an implementer cannot write the test without inventing one. A per-task executor treats the acceptance lists as its definition of done, so the case goes missing.

**Response: still minor.** Two points. (a) The case is not out of Task 3's reach. Task 3's body imports "the begin and seal cases of source.md section 3.4" (plan:57). In source.md:128 the counted-once case sits right after "valid and invalid prior links", which is the `seal` ratchet, so an exact follower writes some test there. V3's real point is (b): the rule is undefined. That point is right, but its effect is limited. Two claims on one prior can change a count. They cannot change the verdict: one confirmed claim already gives FAIL `confirmed` (plan:77). What they can affect is the D1..Dk listing and the `m1_open_confirmed` count, and those are reporting and display (plan:22, "This is reporting only"). An under-specified count with no effect on the verdict is minor. The fix: state the rule in Task 3 (dedupe by prior id for the verdict counts, the D list and `m1`) and add the case to Task 3's acceptance. V3's naming of the three counters is the better fix text, so V3 wins on fix quality. V1 keeps the severity.

### 7. C-007: V2 grades it not-a-defect

**Steelman (V2).** The Task 14 file names are fixed in advance (plan:182-184). Task 13 explicitly says to write "a list of the brief templates written by Task 14" (plan:172), which tells the writer to read ahead. Task 14's check "INSTALL.md lists all eleven files" (plan:190) then passes.

**Response: conceded, now not-a-defect.** My own Round 1 A-001 position said read-ahead is fair when a later task only fixes names in advance, and I named C-007 as that case. Grading C-007 minor contradicted my own position. Task 13 is told to list the eleven names, and the names exist in the plan text. INSTALL.md is briefly ahead of the files between Tasks 13 and 14. The final deliverable is correct.

### 8. C-017: rubric hash literal

**Steelman (V2, V3).** "Equals the literal recorded in `./artifacts/t1-rubric-sha256.txt`" (plan:135) most naturally means that the test holds the hash as a constant, copied from the artifact. Nothing reads the plan folder at test time.

**Response: conceded, now not-a-defect.** Even the bad reading corrects itself. pytest runs from the repo root, where `./artifacts/` is not the plan's folder, so a runtime read would fail at once in Task 10's own acceptance run (plan:137). It would not pass silently and then break later at archive. No wrong deliverable survives.

### 9. S-002 and X-004: deviation classification, minor vs not-a-defect

**Steelman (V2: not-a-defect).** These rows compare how the cards classified the plan's declared deviations. As facts about the plan, the Unattended removal (owner ruling, plan:21) and the `_POST_REFRESH_ADDITIONS` edit (plan:135, which calls itself "a necessary deviation") are authorized and necessary. By definition, those classes need no change to the plan. The one real drift, the section-5 templates, has its own row (C-018).

**Response: conceded, now not-a-defect.** Grading S-002 or X-004 minor would count C-018 a second time. The plan defect lives in C-018 (minor, V3). V1 is still the superior card on these rows, because it alone ties each count to a named, cited deviation.

## Updated assessment of the other variants

- **V2.** Its Round 1 statement is well calibrated: it concedes QA-001 and QA-002 to minor, and it independently confirms that the control r1 report has no sentinel (C-003). Its read-ahead rule for A-001 is the right one, and I now apply it to C-002 and C-007. C-009 remains the only finding that touches M0's correctness, and it is a real addition. Its card coverage is still the thinnest: 2 findings.
- **V3.** It is strongest on the harness layer (C-014, C-015, C-016, C-020) and on the Usage lock-in argument (C-004, now minor by its own concession). It rightly says C-002 is minor, and I now agree. On C-003 its "minor" depends on an implementer building scaffolding the plan does not ask for. It also does not address the review-1 path, where the literal test passes with 8/0. On C-005 its blocking label confuses an undefined count with a wrong deliverable, because the verdict cannot change.

## New evidence

1. **C-003 silent pass.** plan:57 ("1 without `--re-review`", "ratchet for reviews 2 and 3") together with source.md:243 ("review 1 has no baseline (`ratchet=off`, recorded)") and plan:96 ("asserts the computed split ... without forcing it to 5 and 3"). Read literally, the replay test computes 0 late-found and passes all Task 7 acceptance criteria. That is a wrong deliverable no check catches.
2. **C-005 bounded effect.** plan:77: any `confirmed` claim gives FAIL `confirmed`, so a duplicated prior link cannot flip the verdict. Only counts and the D list change.
3. Re-checked: the control r1 review folder holds `spec-panel.md`, `spec-panel-round2.md`, `spec-panel-round3.md` and two disposition files. A grep for `stoprule` in them finds no match.

## Final per-point table (contested points only)

| id | severity | superior variant | changed since Round 1? |
|---|---|---|---|
| C-002 | minor | V1 | yes |
| C-003 | blocking | V1 | no |
| C-005 | minor | V1 (severity); V3 (fix text) | no |
| X-002 | minor | V1 | no |
| C-007 | not-a-defect | V2 | yes |
| C-017 | not-a-defect | V2 | yes |
| X-004 | not-a-defect | V1 | yes |
| S-002 | not-a-defect | V1 | yes |
