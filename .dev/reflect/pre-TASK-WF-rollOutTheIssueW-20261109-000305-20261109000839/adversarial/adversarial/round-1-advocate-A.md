### Variant A Advocate (sonnet:analyzer-advocate)
**Position**: Variant A is the better card on correctness and verifiability, not on raw impact. Its lead finding (F1) is a deterministic defect in an executable acceptance criterion, its calibration gap is smaller (0.14 vs 0.23), and its self_audit makes every anchor traceable. Variant B has the higher-impact Task 5 findings and I concede that where it is true. The best merge keeps both; as a standalone card A is the sounder one.

**Steelman of Variant B**: B went to the plan's riskiest task, the only one that edits tests, and read the consuming code. QA-03 is true: 8 of 19 fixtures have no `payload` key, and the two `gh_api_user_include*` fixtures keep their data in `raw` (gh_api_user_include.json:4), yet plan:110 says "replace the `payload` value" and test_github.py:563 reads `fixture["raw"]`. QA-02 is a real internal contradiction: plan:108 requires one capture per fixture, plan:110 lets uncaptured fixtures stay `_assumed_shape: true`, and source.md:22 says "every". QA-04 is a runtime failure: test_github.py:566-567 hardcodes the guessed Date `2026-11-07 12:00:00`, so a real capture fails the test even if the parser is fine, and plan:112 budgets only the metadata test. F2 notes plan:29 stores owner captures in an always-staged folder while plan:118 greps only `tests/issue_watch/fixtures/`. B's findings would change what an implementer does in the phase that matters most.

**Key strengths claimed**:
1. F1 is mechanically verifiable and fails today. The Task 2 AC at plan:65 loops over every backticked name in the 4.3 table. issue-watcher.md:163 (checked) has `failed`, `unknown`, `abandoned` in its Meaning cell. Grepping audit.py for `"failed":`, `"unknown":`, `"abandoned":`, `"once":` returned 0 matches. The AC cannot reach "zero misses" as written, and the plan's own new row (plan:59, "`once` only") adds a fourth. B has no finding that fails this deterministically.
2. A's anchors all hold. I checked setup.md:5 (section map "8 to 15"), :202 (scheduler sentence), :224 ("8. Before cron"), :282 (schedule), :637 (FU-2 row), and audit.py:57 `cycle_crashed`, :64 `cycle_complete`, :87 `spawn_error`. A's self_audit records these checks; B's `note` field gives only the plan path.
3. F4 is a true consistency defect a literal implementer would ship: Task 4 (plan:93) adds section 16 and 8.7, but the line-5 map stops at 15 and nothing in plan:92-100 touches line 5.
4. Calibration: A's gap is 0.14 with one low finding judged overstated. B's gap is 0.23, its high finding was cut to medium, and that finding bundles three claims.
5. A's severity spread (1 medium, 3 low) matches what each finding can break.

**Weaknesses identified in Variant B**:
1. QA-02 bundles three claims (weakened gate, plan:108/110 contradiction, matrix overstatement) under one `high`, and the calibrator downgraded it. Part of it is a source defect: source.md:22 says "every" but :24 says "about 12+ fixtures", so the plan's 19 plus its uncaptured path (plan:78, plan:110) follows the source's own tension. B labels it plan-gap only.
2. F2 is self-described as "a validation gap (not an actual leak)". plan:78 already requires redaction before handover, so a second grep is hardening, not a defect.
3. QA-03's scope is misstated and partly mitigated. plan:110 also says "or the stderr text in the same field layout the fixture already uses", which covers the `gh_stderr_*` fixtures. The real gap is the two `raw` fixtures plus `orca_launch_unknown`; B names one fixture.
4. B's 0.95 self-confidence against 0.72 calibrated is the larger overreach, and B has no self_audit to show what it checked.
5. B's mixed ID scheme (F2, QA-02..04) makes reconciliation with Tier 1 and with A's F-series harder.

**Concessions**:
- QA-03 and QA-04 are real and consequential; I verified both. They outrank A's F3 to F5 in impact.
- A's F3 is overstated: plan:96 says "one in 8.7 plus the unchanged FU-2 row of 15.3", which implies 2. The calibrator was right. F5 is minor: plan:92 says "keep the existing sentence", and that sentence (setup.md:202, section 7) is not edited by Task 4.
- A covers only Tasks 2 and 4, so the riskiest phase (Task 5) is unreviewed in A alone.
- Neither card reviews Task 3.

**Per-point positions**:

| Diff Point | Superior | Reason |
|---|---|---|
| S-001 | A | self_audit lists the anchors checked; B's `note` gives only the plan path |
| S-002 | TIE | ID scheme is cosmetic; B's mixed IDs only slightly hurt reconciliation |
| S-003 | B | B's top finding carries more impact (QA-03 verified); A's spread is accurate but low-stakes |
| C-001 | TIE | Disjoint tasks: B holds the riskier Task 5, A holds a deterministic AC failure in Task 2; both are needed |
| C-002 | A | A's confirmed F1 is a hard defect; B's confirmed F2 is "not an actual leak" by its own words |
| C-003 | TIE | A's design/runbook/audit.py lines are exact (checked); B's test and fixture evidence is stronger on runtime behavior |
| C-004 | A | Gap 0.14 vs 0.23; B's top finding was downgraded and is a bundle |
| A-001 | TIE | Both share the plan-gap label; neither separates the source-vs-plan split |
| A-002 | TIE | Both cite fixed lines; A's design anchors are somewhat more exposed to drift after Task 2 |
| A-003 | TIE | Both accept the enable guard; no difference |
| A-004 | TIE | Neither reviews Task 3; no difference |

**Shared-assumption responses**:

| ID | ACCEPT/REJECT/QUALIFY | Reason |
|---|---|---|
| A-001 | QUALIFY | `plan-gap` fits most findings, but QA-02 partly rests on source.md:22 "every" vs :24 "about 12+", a source inconsistency |
| A-002 | QUALIFY | Plan line anchors are stable; design/runbook anchors (issue-watcher.md:163, setup.md:5) shift after Tasks 2 and 4, so cite by section or row name |
| A-003 | ACCEPT | plan:20 and plan:28 keep `enabled` false and the live test owner-run; neither card contradicts this |
| A-004 | QUALIFY | Unreviewed is not sound: plan:82 ("every argv matches a builder") names no check method, unlike Task 2's loop |
