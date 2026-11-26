# Refactor Plan (merge of the three reviewer cards onto the base card)

## Overview

- Base variant: Variant 3 (`variant-3-original.md`, reviewer 3, refactorer, opus class), selected in `base-selection.md` (combined 0.8282, 11 debate points).
- Incorporated: Variant 1 (`variant-1-original.md`), Variant 2 (`variant-2-original.md`), the debate (`debate/round1-*.md`, `debate/round2-*.md`, final tally `scoring/round2-votes.json`) and the invariant probe (`invariant-probe.md`).
- Output to produce: `merged-output.md` in this folder (one consolidated reviewer card in the reflect-reviewer Output Format: header, Deviations table, Adherence summary, Notes, plus a `## Repairs` section) and `merge-log.md`.
- Grading rule used: Blocking only if correcting the text changes a named decision, a required behavior, an acceptance check or a quoted number the plan or a later step rests on, or a required deliverable or behavior is absent in substance, or the text would lose data or break a safety boundary; Medium = real defect nothing named rests on; Note = form only.
- Final grades follow the debate majority (37 of 37 diff points agreed); where advocates split on a grade the majority grade is used and the minority view is noted in the row.
- Approval: auto-approved (non-interactive).

## Planned Changes

### The merged findings table (the content of the Deviations table in `merged-output.md`)

Columns: `# | Category | Location | What diverged (grade first) | Evidence (file:line) | Severity label | Sources`. Severity label: HIGH for every Blocking row, MEDIUM for Medium rows, LOW for Notes. `PLAN` = `.dev/tasks/to-do/TASK-WF-design-20261126-162939/TASK-WF-design-20261126-162939.md`; `DESIGN` = `.dev/tasks/to-do/TASK-WF-design-20261126-162939/source.md`; `REQ` = `.dev/brainstorms/20261126-115614-git-pm-workflows-skills/merged-requirements.md`. Copy each row's evidence (file:line) from the source card row named in Sources; keep the wording of the base card where it exists.

**Blocking (11). Each row ends with its repair, copied into the `## Repairs` section too.**

| # | Topic (diff ids) | Location | Sources | Repair |
|---|---|---|---|---|
| M-01 | Constraint line 29 forbids text that Tasks 3, 13, 15, 21, 24, 29, 34 must write (C-001) | PLAN:29 vs 60, 172, 193, 252, 334 | V1 row 2, V2 row 1, V3 row 4 | Reword to: no command or argv the code or a primitive tells an agent to run uses the tokens, and no recommendation uses them; deny-lists, refusal text and tests of refusals may name them |
| M-02 | Task 19 edits S23 and runs the routing test before Task 20 creates `SKILL.md`; with S23 unchanged the test also fails on the `self-contained` rule (C-004, INV-011) | PLAN:232-236, 240-242 | V1 row 1, V3 row 2, probe INV-011 | Move the S23 edit AND the routing-test run out of Task 19's acceptance into Task 20 (not only the fixture edit); Task 19's acceptance checks the `git.md` text only |
| M-03 | Task 24 acceptance 2 (only `worktree_cleanup.py` runs a branch deletion, repo-wide scan) cannot pass (C-003) | PLAN:282, 286 | V1 row 10, V2 row 5, V3 row 7 | Scan only the files this work adds (REQ:631 "No new code") and accept list-form argv as the existing form |
| M-04 | Task 25 acceptance uses `git ls-files` after a plain delete (C-005) | PLAN:292, 295 | V1 row 3, V3 row 5 | Check `test ! -e commands/sc-git.md` and the work-tree file count (Glob); tracked state stays UNVERIFIED |
| M-05 | Plugin copies of the implement protocol are left to Task 38 while existing byte-parity tests run in Tasks 26 to 34; Constraint 24 already requires the copy (C-008, X-006, INV-012) | PLAN:24, 307, 358, 388, 426, 429 | V3 row 1, debate | Each of Tasks 26, 27, 28, 29, 30, 31, 32 copies the plugin twin of every file it changed and compares it (`cmp`); Task 26 acceptance gains `cmp` for `implement.md` and `SKILL.md`; Task 38 only verifies (`cmp`, `diff -r`, `make sync-dev`, `make verify-sync`) |
| M-06 | Task 31 adds `E-RESUME-NEEDED` reasons that the existing `_TRANSIENT` test pin forbids (C-009) | PLAN:354, 358 | V3 row 3 | List both reasons in `refs/commit-step.md` only (that file is not scanned, `tests/skills/test_task_workspace_lifecycle.py:686-688`), or update `_TRANSIENT` and record the override of T-16 / NFR-005 in the plan |
| M-07 | Tasks 26, 30, 31, 32 add halt, Ruling or `E-ARCHIVE-BLOCKED` lines that match no `_ALLOW` entry of the existing static test; the verify-only gates fail (INV-014) | `tests/skills/test_implement_severity_static.py:296, 331-335, 420-434`; PLAN:358, 364, 388, 430 | probe INV-014 | Keep new halt and Ruling wording in `refs/commit-step.md`; for lines that must sit in the scanned files (Task 32 step 1) add the `_ALLOW` entries in the same task and record the T-16 / NFR-005 override; add this test file to the acceptance of Tasks 26, 30, 31, 32 |
| M-08 | Task 9 copies seven line patterns, omits `_HEADER` and `_ARCH`, and treats an unparseable last line as corrupt, so a header-only ledger and `ARCHIVE: failed` last lines are refused (C-010, INV-006) | PLAN:126, 129 | V3 row 6, probe INV-006 | Copy all nine patterns; AC says "the nine copied patterns"; extend Task 1's `ledger_builder` with `blocked`, `retry` and `ARCHIVE:` forms; record the override of DD-8 |
| M-09 | `skipped` settlement (empty or mixed-authorization boundary) has no action in Task 12's list and no acceptance (C-011, X-001) | PLAN:146-150, 156, 213 | V1 row 4 | Add a `record-skipped` action to Task 12 and a case to Task 17; Task 29 assigns the `empty` skip to a procedure step |
| M-10 | Executor-side T-04 (refused line, no same-run retry) and T-21 (crash after the resolution append, two resumes, surviving pins, no-key reply, redisplay) cases are absent from Tasks 15, 18, 28 acceptance (C-012) | PLAN:193, 213, 223, 324, 327-328, 431 | V2 rows 3 and 6, V1 row 11 | Add the cases to Tasks 15 and 18 and a static pin of the matching `refs/commit-step.md` text in Task 28 |
| M-11 | Task 13's path rules omit the `.dev/implement/` exclusion (not gitignored), so legacy run files could be staged (C-002) | PLAN:168-174, 180, 183-184 | V1 row 8, V2 row 4, V3 row 8 | Add the exclusion as the first path rule of Task 13 and a case in Task 13 and Task 14 |

**Medium (14)**

| # | Topic | Location | Sources | Note |
|---|---|---|---|---|
| M-12 | NFR-014 stop-rather-than-wait on a credential prompt not realized; runner does not drop inherited `GIT_*` variables or set `GIT_TERMINAL_PROMPT=0`, and `GIT_INDEX_FILE` set-check does not prove a private index (C-013, X-002, INV-005) | PLAN:70, 73, 252, 334 | V1 row 13, probe INV-005 | Task 4: build the environment from scratch; Tasks 21, 29: add the stop rule. V2 graded the NFR part Blocking, majority Medium |
| M-13 | Task 32 archive gate calls `vcs reconcile` without checking `commits.md` exists (NFR-018) (C-014) | PLAN:364 | V3 row 9 | Condition the call on the sidecar existing |
| M-14 | Allow-list forbids `-A` while the snapshot method runs `add -A` in a private index; no rule says when (C-015) | PLAN:60, 190, 200 | V1 row 5, V3 advisory | State in Task 3 that `-A` is allowed only with a private `GIT_INDEX_FILE` |
| M-15 | "`--commit-tasks` appears only in primitives" scan conflicts with Task 37 docs and sync-dev copies (C-016) | PLAN:384, 416 | V3 row 10 | Limit the scan to primitive folders |
| M-16 | SKILL.md +15 net lines budget shared by Tasks 26 and 30, measured with `git diff --stat` (insertions plus deletions), never re-checked (C-017) | PLAN:304-308, 344-348 | V1 row 9, V3 row 12 | Measure net growth after each task; Task 30 re-checks |
| M-17 | Task 14 lists seven refusal tokens but says "five" and tests two (C-018) | PLAN:180, 183-184 | V1 row 7 | Test all seven |
| M-18 | "Unchanged against `origin/integration`" checks drift: `origin/integration` is already ahead of HEAD and the `/sc:git` routing row moved from line 293 to 298 upstream (C-019, INV-002) | PLAN:130, 364, 396, 432 | V1 row 12, probe INV-002 | Record the merge-base SHA in Task 1 and compare to it |
| M-19 | Person-only commit authority (invariant I4) has no assertion in Tasks 20 and 24 (C-021) | DESIGN:75, 82, 155; PLAN:245, 282 | V2 row 2 | Add a static assertion |
| M-20 | The design's test-first order inside each phase is not carried into the plan (C-020) | DESIGN:458; PLAN:27 | V2 row 10 | Add to Constraints. V2 graded Blocking; majority Medium (changes no acceptance check) |
| M-21 | `refs/retry.md:437` still deletes the Q0 pin at `complete` while the boundary is unsettled; Task 30 edits only `SKILL.md:129` and `refs/ledger.md` (INV-001) | `refs/retry.md:437`; PLAN:344, 347 | probe INV-001 | Add it to Task 30 and widen its grep |
| M-22 | Task 5 needs `git --version` but the Task 3 allow-list has no version form; constraint PLAN:23 forbids git outside the runner (INV-004) | PLAN:60, 81, 84 | probe INV-004 | Add a `version` form to the allow-list |
| M-23 | Task 30 edits a line that already has a `wc9-allowed` classification row but gives no row update; Task 36's `deferred:P4` rule would relabel it (INV-013) | PLAN:344, 348, 406 | probe INV-013 | Task 30 re-keys the row; Task 36 limits `deferred:P4` to commit-step lines |
| M-24 | Task 38 AC2 demands a clean pass though Task 1 records pre-existing failures; `pre-commit` is not installed so real-framework cases are skipped (INV-015) | PLAN:36, 40, 51, 204, 430-431 | probe INV-015 | State that recorded baseline failures stay and skipped real-framework cases with passing emulator cases count |
| M-25 | DD-11 / open item O1 (owner confirmation of "pending, attempt n+1") is built into Tasks 12 and 17 without confirmation (C-006) | DESIGN:333, 523; PLAN:156, 213 | V1 row 6, V3 row 11 | Owner decision; both readings fail closed. Report, no plan edit |

**Note (10)**: M-26 incomplete `Depends on:` lines of Tasks 6, 8 to 12, 15 (C-007; implement runs source order); M-27 helper field-level assertions `header_len`, `rule`, `runs`, `segments` (C-022, V2 row 8); M-28 the 40-line refusal-log cap has no assertion (C-023, V2 row 9; FR-064 is cited in Tasks 21 and 29); M-29 the project `.claude/` dev copies are first created by Task 25's `make sync-dev` (INV-003); M-30 `WRITE_VERB_RE` also matches `/sc:git add`, `/sc:git commit`, `gh pr`, `gh api`, `git worktree add/remove` lines (INV-007); M-31 the managed-workspace archive gate has six steps and tests pin step 6 by text; add the refusal inside step 1 without renumbering (INV-008); M-32 token-ban scans collide with prose that must name the tokens in Tasks 22, 24, 34 (INV-009); M-33 CI runs `ruff check`/`ruff format --check` and `--strict-markers`, and `git ls-files` based checks see new files only after commit (INV-010); M-34 stale anchors: `SKILL.md:129` after Task 26 inserts lines, `README.md:9` "four" should be five, `flags.md:136-141` range (V3 rows 12 and 14); M-35 `snapshot_lossless` added to `preflight` is a placement choice, `core.autocrlf` trigger is conservative (V3 row 13, V1 row 14).

### Other planned changes to the base card

- CH-A: Replace the base card's 15 rows by the 35 rows above, ordered Blocking, Medium, Note.
- CH-B: In the Adherence summary give the counts: Blocking 11, Medium 14, Note 10; spec units audited 38 tasks plus Constraints plus 29 coverage ids; the base card's "Fully adherent 20" is dropped (unsupported across all three cards).
- CH-C: Correct two base-card errors: row 1 (Task 27 runs no tests; the "early copy would breach `qa.md:52`" premise is withdrawn because Constraint 24 requires the copy, per X-006) and row 9 (its "Blocking (Decision)" grade disagreed with its MEDIUM label; the debate grades it Medium, so it becomes M-13).
- CH-D: Add a `## Repairs` section: one numbered line per Blocking row (M-01 to M-11) with the task numbers to change, copied from the table above, plus "Medium repairs, not applied by the plan repair step" listing M-12 to M-25 as follow-up candidates.
- CH-E: Add a `## Coverage` section: of the 29 design ids not named in the plan, 18 are not active requirements (FR-024 to FR-029, FR-083 to FR-089, FR-119, FR-068, FR-069 per REQ:520), the others are covered by a named task, and real gaps are the NFR-014 prompt half (M-12), NFR-013 refusal reporting and NFR-015 trust-limits text (V1; Note level, folded into M-27).
- CH-F: Add a `## Unresolved` section with: invariant INV-014 was UNADDRESSED HIGH at the end of Round 2.5 and is now carried as M-07; sufficiency challenge (Category 6): the claim that the 13 original repairs alone let `/sc:implement` finish without halting is falsified by INV-014 and by INV-011 (moving only the fixture edit), so the repair set is M-01 to M-11 as written, not the shorter Round 2 list.

## Changes NOT Being Made (rejected alternatives)

- V2's Blocking grades for C-013 (M-12), C-017 (M-16), C-020 (M-20), C-022 (M-27), C-023 (M-28): rejected; correcting them changes no named acceptance check or required behavior in a way a later step rests on (debate majority, Round 2 advocates 1 and 3).
- V1's Medium grades for C-002 and C-003 (now M-11 and M-03): rejected; both advocates conceded Blocking in Round 2.
- V3's row 1 premise that an early plugin copy "breaches `qa.md:52`": withdrawn by advocate 3 in Round 2 (Constraint 24 requires the copy).
- V2's claim that FR-109 is covered and NFR-014 is covered by Tasks 4, 5, 16, 21, 29: rejected (X-001, X-002).
- Treating FR-024 to FR-029, FR-083 to FR-089, FR-119 as missing requirements: rejected; no active definition exists.
- Editing `source.md` (the design) in the repair: not planned; where the plan departs from a DD (DD-8, DD-9 table, T-16 wording) the repair records an explicit override in the plan (A-003, REJECT majority).

## Risk Summary

| Change | Risk |
|---|---|
| Replacing 15 base rows by 35 | Low (additive, every row traced to a source card or probe row) |
| Regrading V2's Blocking rows to Medium or Note | Medium (judgement calls decided by the debate majority; minority view noted in the row) |
| Dropping "Fully adherent 20" | Low |

## Review Status

Auto-approved (non-interactive).
