# Round 1: Variant 2 (reviewer-2, qa persona)

## Position summary

V2 is the narrowest card, but it holds the only finding about whether the plan's `count` subcommand computes the owner's pre-registered measure correctly (QA-002 / C-009), and none of the other cards raised it. I concede that V2's other finding (QA-001 / C-008) is overgraded and that V2 did not classify the plan's declared deviations. On severity, V1 is the best-calibrated card. V3 is the strongest on test hygiene and on why the Usage-line defect cannot be fixed at implementation time.

## Steelman

**V1 (analyzer).** V1's strongest argument is that the plan cannot be run in order as written. Task 3's acceptance requires `begin` to exit 5 on a prior-verdict mismatch (plan:60), but `compute_verdict` only arrives in Task 5 (plan:77). Task 5's label-count line points at Task 6's `count` (plan:77, plan:87). Task 7's replay calls `begin`/`seal` on a review-3 fixture whose prior report has no sentinel. `begin` exits 5 on exactly that (plan:57, source.md:62), and the plan names no prior-report fixture (plan:96). I verified the control-r1 review folder. It holds only plain `spec-panel*.md` reports, so the replay test as described hits exit 5. V1 also grades my measurement-copy item correctly (F12: section 3 does not list it, and only the INSTALL.md sentence is unverified). It is the only card that classifies the declared deviations (A2 authorized, A3 necessary; plan:21, plan:135). **Critique:** F1 and F2 are forward references. An executor that holds the whole plan resolves them by reading ahead, so "blocking" overstates them (its own calibrator gave 0.60 and 0.50). V1 also missed the withdrawn-prior counting edge case.

**V3 (refactorer).** V3's strongest argument is that the Usage-line contradiction is locked in by the plan. Task 9 allows "exactly these changes" (plan:123). Task 10's equality test treats the Usage line as inherited except for name changes (plan:135). So the variant must ship `[--unattended] [--report-dir <dir>] [--improve]` (spec-panel.md:23) while also saying it does not accept `--unattended` (plan:21, plan:123). V3 is also uniquely right on test-ordering hygiene. `test_review_severity_rule.py` sweeps only `git ls-files` output (tests/skills/test_review_severity_rule.py:36-39, verified), and Tasks 10 and 12 run it before staging (plan:140, plan:161-165), so the new files pass unscanned. **Critique:** V3 overgrades R3-1 and R3-2 as blocking. The variant's behaviour still matches the owner ruling because the section is removed, and the missing counted-once test is one test case. R3-11 is not a plan defect, because source.md:124 lists the exact frontmatter keys without `category:`. R3-7 rests on an unlikely reading of "the literal recorded in" (plan:135). V3's deviation counts are not tied to finding ids.

## Strengths claimed

1. **QA-002 is the only finding that touches the correctness of M0.** The owner decision keeps a critical or major finding that was dropped between the first and second `seal` in the count (plan:22). M0 excludes carried priors (source.md:173). Task 3's first-pass `form` line records only `id` and `claimed` (plan:57). Task 6's `count` needs "`prior` is null" and adds claims "present only in a first-pass `form` line" (plan:87). A dropped claim that was a carried prior therefore cannot be told apart from a dropped new claim, and it is counted as new. The Task 6 fixture (plan:90) has no withdrawn-carried-prior case. M0 is the pre-registered headline measure, and its bar is "<= 3 in both" (source.md:185), so a single miscount can flip it. Neither V1 nor V3 raised this.
2. **Coverage denominator.** V2 alone reports how many spec units it audited and how many were fully adherent (35 / 33), and it names the three lexical misses confirmed covered (INF-003 in Task 9, INF-009 in Task 3, INF-034 in Task 6). V1 confirms the same point in one line. V3 does not address it.
3. **The V2 calibration notes record coverage gaps that no other card raised, and I verified them with Grep.** The plan never mentions `same-class` (source.md:66, the sentinel's `grader_model=` marker) or the script-computed `origin=changed|unchanged` (source.md:111). The grep also confirms that "counted once" (source.md:128) and `parent=` (source.md:73) appear nowhere in the plan. V1 does cover those two (C-005, C-010).
4. **Deviation classification for the plan's own gaps.** Labelling QA-002 as drift is defensible. The plan departs from source.md:173 (carried priors excluded) without an owner ruling that authorizes it.

## Weaknesses identified in others

1. **V1 F1 and F2 (C-002, C-001) are graded blocking, but read-ahead resolves them.** The names and behaviour are fully specified later in the same plan (plan:77, plan:87). The deliverable after Task 6 is correct. These are ordering defects that cost per-task QA friction, not a wrong deliverable.
2. **V3 R3-1 (C-004) is graded blocking, but the variant's behaviour is right.** With `## Unattended mode` removed (spec-panel.md:451-462), nothing implements the advertised flags. The defect is a stale Usage token, and the S1 briefs never pass `--unattended` (plan:21). It is a real defect that the plan must fix itself (V3's lock-in point), but it is minor.
3. **V3 R3-2 (C-005) is graded blocking for one missing test case.** The rule is unstated in source.md too (source.md:128 is only a test name), so the right fix is to state it and add the test, not to halt.
4. **V3 R3-11 (C-019) cites the confidence-calibrator pattern (confidence-calibrator.md:4 has `category: analysis`), but the spec lists the exact keys (source.md:124), and the plan follows the spec (plan:44).** This is not a defect.
5. **V1 and V3 both missed QA-002.** Neither card checks the `count` rule against the M0 definition at source.md:173.

## Concessions

- **QA-001 (C-008) is overgraded.** Section 3 does not list the measurement copy. It is an experiment-install step (source.md:163), and the plan installs nothing (plan:20). What remains is V1's point: the INSTALL.md sentence "the measurement copy and the repo copy differ only in the lines that came from master" (plan:172) is asserted, not checked. Minor. V1 is superior on this point.
- **QA-002 should be minor, not blocking.** It is reporting only (plan:22), and the case is rare: a carried prior withdrawn during the one repair. The fix is one field on the `form` line plus one fixture row.
- **V2 did not classify the declared deviations:** the Unattended removal (owner-authorized, plan:21) and the `_POST_REFRESH_ADDITIONS` edit (necessary, plan:135). V1's classification is correct.
- **V2 missed C-003 (the replay prior-report gap).** It is the most consequential finding in the debate.
- V2 also missed the Usage-line contradiction, the staging gap after Task 12, and V3's test-ordering items.

## Per-point positions

| id | finding real? | correct severity | superior variant |
|---|---|---|---|
| S-001 | yes (V2 under-reports: 2 findings against 12/12+1) | not-a-defect | tie (V1/V3) |
| S-002 | yes (V2 omits the declared deviations; V3 counts are unmapped) | not-a-defect | V1 |
| S-003 | partly (an explicit verdict field helps triage; it does not change the plan) | not-a-defect | V3 |
| C-001 | yes (plan:77 forward-references Task 6 `count`) | minor | V1 |
| C-002 | yes (plan:60 needs `compute_verdict` and prior statuses from Task 5) | minor | V1 |
| C-003 | yes (control-r1 review folder has no sentinel report; `begin` exits 5, plan:57; no prior fixture named, plan:96) | blocking | V1 |
| C-004 | yes (spec-panel.md:23 advertises `--unattended`; plan:123/135 lock it in) | minor | V3 (analysis; V1 has the severity right) |
| C-005 | yes (source.md:128 is in no acceptance list; "counted once" is absent from the plan) | minor | V1 |
| C-006 | yes (Tasks 13 and 14 create files after Task 12's staging; plan:27 requires `.dev/tasks` staged) | minor | tie (V1/V3) |
| C-007 | partly (the Task 14 names are fixed in advance at plan:182-184; plan:190 checks the list) | not-a-defect | tie |
| C-008 | partly (not a deliverable; the INSTALL.md claim at plan:172 is unverified) | minor | V1 |
| C-009 | yes (plan:57 `form` has no `prior`; plan:87 needs `prior` null; source.md:173 excludes carried priors) | minor | V2 |
| C-010 | yes (source.md:34 `final`/`verdict` writers, `grader_model=` source, `parent=` at source.md:73 absent from the plan) | minor | V1 |
| C-011 | yes (source.md:68 defines `real:true` reinstatement only for claims) | minor | V1 |
| C-012 | yes (plan:96 leaves the quote line unspecified; the anchored/late split depends on it) | minor | V1 |
| C-013 | partly (the import grep runs only in Task 3, plan:61; Task 10's worker-contract run catches write verbs) | minor | tie (V1/V3) |
| C-014 | yes (the equality test excludes the replaced blocks, plan:135; no positive wording check) | minor | V3 |
| C-015 | yes (`git ls-files` sweep at test_review_severity_rule.py:36-39; run before staging, plan:140/161) | minor | V3 |
| C-016 | partly (the omitted suites read new files; likely pass) | minor | V3 |
| C-017 | partly ("the literal recorded in" most likely means a constant in the test) | not-a-defect | V3 (raised; low value) |
| C-018 | partly (plan:19 exception is circular through plan:172; 5.1 and 5.3 procedures are not owner-authorized) | minor | V3 |
| C-019 | no (source.md:124 lists exact keys without `category:`) | not-a-defect | tie (V1/V2 correctly silent) |
| C-020 | yes (comment at test_routing_refresh.py:29-32 names only #323/#302; plan:141 forbids touching it) | minor | V3 |
| C-021 | yes (spec-panel.md:430-436 critique examples stay plain; this follows source.md:104 literally) | minor | V3 |
| X-001 | yes (the conflict is real) | minor | V1 |
| X-002 | yes (the conflict is real) | minor | V1 |
| X-003 | yes (V1's reading holds) | minor | V1 |
| X-004 | yes (V2 left the declared deviations unclassified) | not-a-defect | V1 |

## Shared assumptions

- **A-001: QUALIFY.** Read-ahead within the one plan is allowed, because the executor holds the whole plan. A forward reference is blocking only when no later task supplies what is missing. C-003 is that case: nothing in the plan supplies a sentinel-bearing prior report. C-001 and C-002 are not.
- **A-002: ACCEPT.** The dated owner rulings in the plan's Constraints (plan:21-24) settle questions that source.md left to the owner (source.md:248, 256), so they outrank the source text. V2's failure to classify them is a card weakness.
- **A-003: QUALIFY.** The inputs exist at debate time: `exp346-ab-ctl-r1/.dev/orca-command-refactor/review/spec-panel-round3.md` and `specs/history/spec-v2-after-round1.md` / `spec-v3-after-round2.md`, the T05-T10 briefs under `exp346-p1-logs`, and `/tmp/impl/exp/s1/filled-flg-r1-T07.txt` / `T09.txt`. But `/tmp` is volatile. Tasks 7 and 14 already stop as blocked or check sha256 (plan:96, plan:182), so a missing input surfaces at execution time. It is not a plan defect.
