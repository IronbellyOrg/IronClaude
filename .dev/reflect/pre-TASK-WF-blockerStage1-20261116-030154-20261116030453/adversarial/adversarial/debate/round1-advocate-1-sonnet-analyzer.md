# Round 1: Advocate for Variant 1 (sonnet class, analyzer)

## Position summary
The plan has two defects that block it. The stoprule/`finding-grader` family has no defining file in the checkout, and Task 7's grep line becomes false once Tasks 10 and 12 reuse the reader, with no end point. Variant 1 makes the stronger case on the first and equals the others on the second. Most of its non-blocking findings are real minors, but two of its grades overshoot, which I concede below.

## Steelman
Variant 2 (qa): it keeps to the acceptance line's own narrowing text. Its F3 is right that the spec hands a `review-ledger/1` mapping to "the /sc:workflow plan" (SPEC:404) and that Task 7 never states one. It also sees that substituting an unrelated file for the stoprule row would misrepresent the scale. But no stated check needs the mapping. Task 7's narrowing sentence is "passes and covers each T7 failure condition above" (PLAN:113), and none of those conditions is a mapping. SPEC:879 calls the mapping "a plan decision", which can be "none in version 1". The stage exit tests T1–T4, T6–T8, T11–T13 and T17 (SPEC:945) do not exercise it. Blocking is an overgrade; V1's "minor" is the right grade.

Variant 3 (refactorer): the cleanest on the grep line. It cites the plan's own rule at PLAN:24 and source.md:17 and adds `__pycache__` matches. For the stoprule row it adds that OD10 is undecided, so the executor cannot bring the files into the repo (SPEC:1038). Its two minors are plausible but speculative: "may contain" fence text in `doctor.py`, and where the sketch test lives. Neither makes any check fail. It misses the allow-list gap, the scale-map layout gap and the `.dev/` conflict.

## Strengths claimed
1. Stoprule row. Only V1 shows that Task 3 (PLAN:62), Task 5 (PLAN:87) and T4 cannot all pass. I checked `git ls-files`: stoprule and `finding-grader` files exist only under `.dev/experiments/...` and `.dev/research/...`. Task 5 says `grep -rn "\.dev/\|artifacts/"` over the skill folder "prints nothing", and `scale-map.md` is in that folder. Naming an installed `~/.claude` path fails "exists in the repository".
2. Task 7 grep line. V1 notes that no `follow_ups` command wiring exists in any task, so the phrase "its command wiring" (PLAN:115) has no referent. Task 12 (PLAN:169, 171) must write into the ledger row through the Task 7 writer, so it also adds a match. This makes the line false even if Task 10 avoided importing the reader.
3. Citations. Every PLAN and SPEC line V1 cites matches the file: 62, 65, 87, 115, 134, 136, 146 and 148 in the plan, and 582, 920 and 945 in the spec.
4. Non-blocking findings. V1 grades C-004 to C-007 correctly as minor or non-blocking; the spec leaves the mapping to the plan, and Task 9 depends only on Task 5 (PLAN:134).

## Weaknesses identified in the other variants
1. V2 F3 is graded blocking. No acceptance line or exit test fails without the mapping, and source.md never mentions adapters or a mapping.
2. V2 and V3 name only Task 10, so they miss that Task 12 also falsifies the line.
3. V2's header identifies its model as ChatGPT despite the haiku pin.
4. V3 F3 and F4 are speculative ("may contain", a test no task requires). Task 9's sketch check is a one-off `uv run python -c` command (PLAN:139), not a committed test.
5. Neither V2 nor V3 notices that Task 3's allow-list is narrower than the T5 scan.

## Concessions
1. F2 is blocking-graded but the plan follows source.md:12 word for word: "it lists the auggie file, `refs/rule.md` and the six stage 4 files". SPEC:845 calls `remediate_parser.py` out of scope. T5 is not a stage 1 exit test. The gap is real (`remediate_parser.py:55,301,365` and `fmea_classifier.py:304,323` hold the phrases) but it bites at stage 3 and starts in the spec. It is not blocking for this plan.
2. The `verify-sync` half of F3 is wrong. PLAN:25 requires `make sync-dev` after every edit, and the Task 1 line is conditioned "After `make sync-dev`".
3. "Tasks 12 and 13 likely" was hedged. Task 12 is certain, Task 13 is not shown.
4. I did not verify `origin_repo.py`, and V3 did.

## Per-point positions
S-001 | winner: tie | verdict: N/A | all three cards separate blocking from minor and list what they checked
S-002 | winner: tie | verdict: N/A | V1's repo-relative cites verified line by line; V2's absolute paths are cosmetic
C-001 | winner: tie | verdict: BLOCKING-REAL | PLAN:115 "only the new module and its command wiring" is false after PLAN:148; PLAN:24 requires an end point
C-002 | winner: variant 1 | verdict: BLOCKING-REAL | PLAN:62 against PLAN:87, with the only tracked copies under `.dev/`
C-003 | winner: variant 1 | verdict: REAL-NOT-BLOCKING | PLAN:65 matches source.md:12; the gap shows at stage 3 (`remediate_parser.py:55`)
C-004 | winner: variant 1 | verdict: REAL-NOT-BLOCKING | SPEC:404 and 879 leave a plan decision; no check needs it
C-005 | winner: variant 1 | verdict: REAL-NOT-BLOCKING | PLAN:136 reads "through the scale map"; no acceptance line tests it
C-006 | winner: variant 1 | verdict: REAL-NOT-BLOCKING | SPEC:485 `.dev/pr-monitor/` against PLAN:87; the grep would catch a verbatim copy
C-007 | winner: variant 1 | verdict: REAL-NOT-BLOCKING | PLAN:146 "Depends on: Task 9" while PLAN:148 reuses Task 7
C-008 | winner: variant 3 | verdict: REAL-NOT-BLOCKING | speculative, and the scan implementation is the executor's to align
C-009 | winner: variant 3 | verdict: REAL-NOT-BLOCKING | the check is a one-off at PLAN:139; the sketch moves when the folder archives
C-010 | winner: none (V2 and V3 right to omit) | verdict: NOT-A-DEFECT | PLAN:25 requires `make sync-dev` after each edit
X-001 | winner: variant 1 | verdict: REAL-NOT-BLOCKING | PLAN:113 narrowing does not include a mapping
X-002 | winner: tie | verdict: BLOCKING-REAL | the plan breaks a stated requirement (source.md:17, PLAN:24), whatever the fix cost
A-001 | winner: tie | verdict: N/A | see below
A-003 | winner: tie | verdict: N/A | see below

## Shared assumptions
A-001: QUALIFY. A tracked `.dev/experiments` file does exist in the repository. The conflict comes from pairing PLAN:62 with PLAN:87, not from the word "repository". The conclusion (unpassable together) holds under either reading.
A-002: ACCEPT. PLAN:24 and source.md:17 both contemplate a later task falsifying an earlier line, which is why an end point is required.
A-003: QUALIFY. Fix cost does not set the grade in general. Here the grade is blocking because the plan omits an end point that its own rule and the source request require. A wording nit with no such rule stays minor.
