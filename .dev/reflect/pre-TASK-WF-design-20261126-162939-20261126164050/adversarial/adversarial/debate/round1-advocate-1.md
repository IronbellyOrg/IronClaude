# Round 1 advocate statement: Variant 1 (reviewer-1, analyzer, sonnet)

Paths: PLAN = TASK-WF-design-20261126-162939.md, DESIGN = source.md, REQ = merged-requirements.md. I made four read-only git checks (`ls-files`, `rev-parse`, `diff --quiet`, `merge-base`); nothing else was run.

## Position summary

V1 is the best card on severity consistency, the coordinator's 29-id coverage reading and several unique findings (C-011, C-015, C-018, C-019). It is not the best card overall: V3 found the three highest-impact defects (C-008, C-009, C-010) that V1 missed, and V1 under-graded C-002 and C-003.

## Steelman

V2: a QA reviewer who reads all 38 tasks against the design and asks what acceptance evidence is missing. Its strongest arguments are that a design invariant with no assertion can be weakened while the checks pass, and that T-04 (refused sidecar line, no same-run retry) is not asserted by Task 15 or 29. It is right on C-002 and C-003 and its single FAIL verdict is clear. My critique follows below.

V3: a refactorer who asks whether `/sc:implement` can execute the plan at all, by reading the existing tests that touch every file the plan edits. This found a byte-parity test, a pinned `_TRANSIENT` set and a header-less ledger reader, each of which breaks a task's acceptance. That is the right method and it won three High points.

## Strengths claimed

1. Grade and label agree on all 16 rows (Blocking=HIGH, Medium=MEDIUM, Note=LOW). V2 has six rows graded Blocking but labelled MEDIUM, and V3 has one (row 9).
2. C-011 is unique and verified in part. DESIGN:291 and REQ:551 define `commit skipped ... reason=mixed-authorization`. Task 12's closed action list (PLAN:156) has no action that records it, and Task 11 only says a mixed batch is "not eligible".
3. C-018 is verified. Task 14 (PLAN:180) lists seven tokens, its acceptance says "five" (PLAN:183), and its scenarios (PLAN:184) cover two.
4. C-015 is verified. `FORBIDDEN_FLAGS` bans `-A` (PLAN:60) while Task 15's second snapshot needs `add -A` in a private index, and Task 3's acceptance only tests that `add` without a private index is refused.
5. C-001 gives the most usable fix (deny-lists and refusal tests allowed). The Constraints are global and a quoted breach is blocking (`SKILL.md:106`, `refs/qa.md:52`).
6. C-004 and C-005 are verified. `test_routing_refresh.py:495-496` resolves `sc-git-protocol` to a SKILL.md that Task 20 creates. `git ls-files commands/sc-git.md` lists the file and `commands/` holds 21 tracked files, so after a plain delete the check in Task 25 still fails.
7. C-019 is now partly resolved. `origin/integration` resolves (`4ce9f14`) and the four paths are unchanged today. Fragility remains because it is not an ancestor of HEAD.
8. The "29 ids" section answers the coordinator's actual list. V2 accounted for a different 67-entry slice and V3 checked ten.

## Weaknesses in the other variants

1. V2 X-001: it lists FR-109 as "covered" by Tasks 11, 12, 14, 17, 29, 30. No listed task produces the mixed skip, and its own rows 3, 6 and 7 report FR-109/T-21/T-04 gaps, so the card contradicts itself.
2. V2 row 9: the 40-line cap is in FR-064 (REQ:501, "first 40 lines"), and Task 29 cites FR-054 to FR-067. "No implementation instruction" is wrong. Only the missing assertion is real, and that is a Note.
3. V2 row 10 (test-first) is a process preference. Row 2 asks for behavioural tests the design does not give: DESIGN:82 and 508 map I4 and FR-020 to FR-023 only to static T-13.
4. V2 missed C-004 and C-008 to C-010, and counted T-14 and AC-13 as covered by Tasks 19, 35, 36.
5. V3 X-006: "early copy would be work the plan reserves for Task 38" ignores PLAN:24, which already requires byte-identical plugin copies on every `src` edit. The defect is the plan contradicting itself, not a forced breach.
6. V3 C-016: FR-052 (REQ:409) limits "appears only in" to primitives and says docs are not primitives, and Task 34 cites FR-052. Note-level, not Medium.
7. V3's own notes list FR-109, NFR-013, NFR-015 and others as "not checked", so it could not find C-011. Row 13 labels `snapshot_lossless` "Authorized expansion" although the field is absent from DESIGN:192.

## Concessions

- C-002: PLAN:168-171 omits `.dev/implement/` (DESIGN:228 step 3, REQ:475, T-01); `.gitignore` has no `.dev/implement` entry; Blocking is right.
- C-003: `worktree_cleanup.py:2642` builds list-form `["git","branch","-d",branch]` and other files hit the textual patterns. T-17 (REQ:680) scopes the check to "new code or primitives", so Task 24 acceptance 2 as written is unsatisfiable; V3's Blocking stands. V3's grade was right and mine was Medium.
- C-008, C-009, C-010: V1 missed them. `test_workflow_command.py:204-220` requires byte-equal plugin copies. `test_task_workspace_lifecycle.py:682-688` forbids any `E-RESUME-NEEDED reason=` outside the four `_TRANSIENT` reasons; I checked only lines 778-791 of that file. `archive_workspace.py:44-46, 67, 203` and `refs/ledger.md:127, 238` show a header-only ledger and a trailing `ARCHIVE: failed` are valid last lines, so my "adherent" for Task 9 was wrong.
- X-002 / C-013: DESIGN:377, 431, 506 realise NFR-014 as the 600000 ms timeout plus the `commit-interrupted` stop. My "real gap" is overstated.
- "Fully adherent: 23 tasks" was overclaimed. Row 3's "tracked" UNVERIFIED is now verified. My Regression label on rows 1, 3 and 5 is a stretch for an unexecuted plan.

## Shared assumption responses

- A-001: QUALIFY. The review grading rule is not implement's halt model. Only the constraint rule (`qa.md:52`, B4) and failed acceptance checks map to implement halts. Grades reflect the review rule.
- A-002: ACCEPT. The plan itself puts existing tests in its acceptance universe (Task 26 names `test_workflow_command.py`; Tasks 34 and 38 run existing suites), and C-008/C-009 are real. V1 applied it unevenly.
- A-003: QUALIFY. DD-8 (DESIGN:102) and the archive-gate text (DESIGN:253) are where C-010 and C-014 start. PLAN:19 says "the design wins" for DD-n, so a plan-only fix needs an explicit override or a design amendment.
- A-004: QUALIFY. `origin/integration` is not an ancestor of HEAD (the branch sits on master), and the plan's cited line numbers (SKILL.md:129 and others) shift once Task 26 edits the file. Both will move before implementation.

## Per-point table

| point | superior | verified | reason |
|---|---|---|---|
| S-001 | TIE | verified | V2's extra tables show coverage; V1's 29-id section answers the brief; neither dominates |
| S-002 | TIE | verified | V2 is cleanest; V1 and V3 sub-labels are non-standard but readable |
| S-003 | V1 | verified | grade and label agree on all 16 rows (V2 has six mismatches) |
| C-001 | TIE | verified | all Blocking; PLAN:29 vs 60, 172, 193, 334; V1's fix is the most usable |
| C-002 | V3 | verified | rule absent in PLAN:168-171; V3 cites REQ/DESIGN/.gitignore; V1 under-graded |
| C-003 | V3 | verified | list-form argv at worktree_cleanup.py:2642; T-17 scopes to new code |
| C-004 | TIE | verified | V1 and V3 both right, V2 missed it |
| C-005 | TIE | verified | `ls-files` still lists the file after a plain delete; 21 tracked |
| C-006 | TIE | UNVERIFIED | open owner decision O1; whether the owner has confirmed it is unknown |
| C-007 | TIE | verified | all agree it has no execution effect |
| C-008 | V3 | verified | byte-parity test; severity qualified by PLAN:24 |
| C-009 | V3 | verified | `_TRANSIENT` pin at test_task_workspace_lifecycle.py:682-688 |
| C-010 | V3 | verified | `_HEADER`/`_ARCH` are valid last lines; Task 9 copies seven patterns |
| C-011 | V1 | verified | mixed-authorization skip has no producing action; empty skip only by FR-060 reference |
| C-012 | V2 | UNVERIFIED | broader (T-04 gap seen in PLAN:193); T-21 claim unchecked; V1 covers FR-109 only |
| C-013 | TIE | verified | V2 and V3 right (DESIGN:377, 431, 506); V1 overstated |
| C-014 | V3 | verified | NFR-018 (REQ:739) vs the archive gate calling reconcile without a `commits.md` check |
| C-015 | V1 | verified | most precise; Task 3 acceptance never tests a private-index `add` |
| C-016 | V3 | verified | only V3 raised it; Note-level given FR-052 |
| C-017 | TIE | UNVERIFIED | V1 on feasibility, V3 on `--stat` and stale line; neither checked line counts |
| C-018 | V1 | verified | seven tokens listed, "five" claimed, two tested |
| C-019 | V1 | verified | ref resolves; fragility real but Low |
| C-020 | V2 | verified | DESIGN:458; only V2; process note |
| C-021 | V2 | verified | only V2; DESIGN:82 maps I4 to static T-13, so design-origin, Medium |
| C-022 | V2 | verified | Task 6 acceptance never names `header_len` or `rule`; Low |
| C-023 | V2 | verified | acceptance absent; instruction carried by FR-064; Note |
| C-024 | V1 | UNVERIFIED | matches the 29-id list; NFR-013 and NFR-015 reading unchecked |
| X-001 | V1 | verified | FR-109 cannot be "covered" without a skip-producing action |
| X-002 | TIE | verified | V2 and V3 right; DESIGN:377 realises NFR-014 as timeout plus stop |
| X-003 | V3 | verified | Blocking for C-002/C-003 per the grading rule (acceptance check changes) |
| X-004 | V3 | verified | V1 wrong; `ledger.md:127, 238` and `archive_workspace.py:203` |
| X-005 | TIE | verified | plan carries the cap via the FR-064 citation; V2 overstated |
| X-006 | V3 | verified | contradiction is real: PLAN:24 vs Task 38; V3's reasoning misses PLAN:24 |
