# Adversarial Debate Transcript

## Metadata
- Depth: standard (Round 1 parallel, Round 2 sequential, Round 2.5 invariant probe)
- Advocates: 3 (one per reviewer card; all general-purpose agents on the sonnet alias)
- Focus areas: correctness, coverage, deviation-classification
- Round 1 statements below are condensed by the orchestrator from the advocates' returned text; positions, concessions, and A-NNN responses are unchanged, evidence refs kept.

## Round 1: Advocate Statements

### Variant 1 Advocate (analyzer card)
- Position: variant 1 alone tests the plan against what the scripts do when a step fails. Blocking call F1 verified: ccsession:1649-1650 `TOPIC=$(validate_label "$NAME_ARG") || exit 2`; ccsession-orca:20-24 promises "never ends up at a dead prompt"; ccsession-orca:34 and ccsession:98 are `set -e`; `CCSESSION_NAME` appears nowhere in the skill today (grep: no matches); Claude `--name` currently passes through (ccsession-orca:115-117).
- Steelman of V2: coverage mapping and `matrix_gaps: []`; its F1 timer-criterion contradiction is real (plan:46, default 0 at ccsession:1471); F3 README `--session-id` valid; V2 never touched failure paths and its F5 citation (session-name.sh:10-12) shows no `-2`.
- Steelman of V3: scope_additions governance list; finds the two Enter reopen tests that contradict plan:84; F5 hint regression is real; V3 F4 finds the same mechanism but rates it minor/"authorized" although plan:23 only says "to be reported".
- Strengths: F2 (`read -r` without IFS, ccsession:1482), F4 (python drain, ccsession:1426), F5 (`--` before text starting with `-`), F12/F1 (auto-name placement vs argument loop ccsession:648-723), F6/F7 concrete test-suite catches, F11/F10 classification edges.
- Concessions: the auto-name half of F1 is weak (Task 1 requires validate_label); F3, F8, F9, F13 have `evidence: null`; F14 window is narrow; F10 overreaches; 13 minor findings are noisy; said nothing on coverage.
- A-002 QUALIFY (hook records via session-name.sh:166-170; only sessions with a first message persist, ccsession:1677-1687). A-003 QUALIFY (test-list fixes can ride as notes; F1 needs a plan edit). A-004 QUALIFY (task 3 must cover `=` forms and a trailing `--name`, ccsession:657-660 exits 2). A-005 QUALIFY (a single os.write paste proves only the arrived case).
- Contradiction calls: X-001 V1 correct, BLOCKING for Tasks 3 and 4 until each has an acceptance criterion that an invalid lifted/env name still reaches Claude. X-002 minor (sync_name renames the list only). X-003 lean to drop the argument lift; `CCSESSION_NAME` still needs a validated path.

### Variant 2 Advocate (qa card)
- Position: coverage and acceptance-precision card; F2 and F3 re-verified; honest gap: it never examined the failure paths of the new `ccsession --name`/`--auto-name` calls.
- Steelman of V1: lift creates a path where Claude never starts (validate_label ccsession:282-300, exit 2 at 1650, set -e at ccsession-orca:34); F6 finds the Ctrl+C test launches with "the prompt" (test:1543) which is never asked under the new rule; F2-F5 shell mechanics.
- Steelman of V3: F2 confirmed (test:1801-1803 asserts topic None after Enter); F4 same mechanism but a reported author decision (plan:23); scope_additions organise classification.
- Strengths: F1 timer criterion (plan:46 vs default 0), F2 invalid-name test, F3 README:266, F4 negative result on matrix gaps.
- Weaknesses of others: V1 F1 overstated for the auto-name half (leading dot is encoded, not rejected); V1 F12/V3 F1 low severity; V3 F3 partly overstated.
- Concessions: F5 citation wrong (session-name.sh has no `-2`); the mechanism exists in sync_name_locked (ccsession:336-337, 391-398) and frees a name when the earlier conversation is not saved (line 395), so the collision risk is real but narrow; not examining the invalid-name fallback is a genuine gap.
- A-002..A-005: QUALIFY each (hook lists auto-names; collision protection only for saved conversations; fallback needs an explicit acceptance case; add `=` forms and trailing `--name`; paste race not provable with one os.write).
- Contradiction calls: X-001 V1 right on mechanism, V3 right on severity: MINOR with a required acceptance case (loud stderr, narrow trigger, fixable in executor, plan:23 flags the lift). X-002 neither fully right; add seconds/random suffix. X-003 V3 wins: keep the lift as a reported decision, add V1's guards (skip for resume-like and `--session-id`, validate before lifting).

### Variant 3 Advocate (refactorer card)
- Position: only card that checks the plan's test instructions against the test file and separates source-authorized from plan-author additions. Main error: F4 found the same exit-2 mechanism as V1 but rated it minor/"authorized"; now sides with V1 on severity.
- Steelman of V1: ccsession-orca:20-24 promise; `set -e`; `CCSESSION_NAME` has no consumer today; F2/F5/F13 mechanics (ccsession:1482, ccsession-orca:107-109 `|| name=""` discards 130); F8 env unset. Weaknesses: 12 of 14 minor, F8/F9 `evidence: null`, auto-name half unlikely, missed the two Enter reopen tests.
- Steelman of V2: F1 timer criterion gap, `matrix_gaps: []`, F3 README. Weaknesses: only card with no matrix gap; matcher cannot see Constraints; missed Task 5 contradiction and invalid-name path; F5 citation.
- Strengths: F2 verified (plan:84 vs test:1795-1804, 1855-1863); F1 verified (`--ask` after the argument loop ccsession:648-723, exit 2 on bare `--model` at 702-705); scope list accurate (source names CCSESSION_NAME and `--fork-session`/`--session-id`; Claude `--name` lift only in plan:23); F5 hint regression (ccsession:1421, plan:19).
- Weaknesses of own card: F4 mis-rated; F8 overstated (window of seconds); F7 `evidence: null`; no shell-mechanics findings; never used "regression" or "blocking".
- Concessions: V1's blocking call is stronger than V3's minor call; V1's F2/F5/F13 real; V2's F1 real; own F3 is only a wording ambiguity (plan:108).
- A-002..A-005: QUALIFY each (list name gets `-2`, Claude `--name` stays unsuffixed; wording notes ride as notes but fallback and `--auto-name` placement change task behaviour and must be written into the plan; `=` forms at ccsession-orca:75; single os.write cannot reproduce chunked arrival).
- Contradiction calls: X-001 BLOCKING for the lifted and `CCSESSION_NAME` path (supervised worker has no human to retry, 60 s readiness limit, ccsession-orca:30-32). X-002 minor. X-003 drop the lift by default (source authorizes only `CCSESSION_NAME`); lift only if owner confirms.

## Round 1 position tally (before rebuttals)
- X-001: blocking 2 (V1, V3), minor 1 (V2). X-002: minor 3 of 3. X-003: drop-lift-by-default 2 (V1, V3), keep-with-guards 1 (V2).
- A-002, A-003, A-004, A-005: QUALIFY 3 of 3 each.

## Round 2: Rebuttals

### Variant 1 Advocate rebuttal (condensed by the orchestrator)
- Conceded: the auto-name half of F1 (Task 1 requires validate_label, plan:31); F3, F8, F9, F13 have no evidence and are notes at most. Not conceded: F2 (ccsession:1482), F4 (ccsession:1426), F5 carry evidence.
- X-001 stays BLOCKING until Tasks 3 and 4 carry an acceptance criterion: when CCSESSION_NAME or a lifted --name is invalid (control character, over 245 bytes, rejected by validate_label), ccsession-orca still starts Claude (exit status other than 2, name dropped, stderr warning, fake-Claude record present). With that criterion the point is non-blocking. Reasons: ccsession:1650 exits 2 before any Claude exec; `set -e` at ccsession-orca:34 and ccsession:98; ccsession-orca:24 header; supervised workers have no human to retry (60 s limit, ccsession-orca:30-32); plan:59-63 and plan:71-76 contain no invalid-name case.
- X-003: drop the --name/-n lift by default (source authorizes only CCSESSION_NAME; plan:23 calls the lift an author decision). If the owner confirms, accept V2's guards: validate before lifting, skip for resume-like and --session-id launches, cover the `=` forms (ccsession-orca:75) and a trailing --name (ccsession:657-660 exits 2).
- Winners: C-002 V3 (plus V1/V2 invalid-name test and CCSESSION_NAME env exclusion); C-003 V1 seconds/random suffix plus V2 same-minute test (sync_name renames the list only, ccsession:336-337, 391-398); C-004 V1; C-008 V3 scope list with F9 downgraded to a verification note.

### Variant 2 Advocate rebuttal (condensed by the orchestrator)
- X-001: accepts V1's framing and moves from MINOR to BLOCKING-until-criterion. The failure is not just a message: ccsession:1650 `|| exit 2` plus `set -e` (ccsession-orca:34) means Claude never starts; ccsession-orca:108 `|| name=""` today swallows an --ask failure and Task 3 (plan:57) removes that; a bad CCSESSION_NAME inherited from the environment would fail every launch in that shell; plan:60-63 and plan:72-76 have no invalid-name case. Required plan note: add one criterion to each of Tasks 3 and 4 (an invalid CCSESSION_NAME or lifted --name still starts Claude, exits with a status other than 2, prints a stderr warning, leaves a fake-Claude record); with it the finding is non-blocking.
- Own weaknesses; would add two findings: (a) Task 4 (plan:69) maps only --ask statuses 0, 1, 3, 130; any other status (2, a crash) hits `set -e` at ccsession-orca:34, and the old `|| name=""` at ccsession-orca:108 discards 130, so the 130 mapping needs a proving test; (b) --auto-name is a new call under set -e; if it fails (for example an unwritable topics directory) Claude should start untagged; add a Task 1 or Task 4 criterion. Keeps F1 timer criterion, F3 README, negative matrix result.
- X-003: sides with V1 and V3: drop the --name/-n lift by default; if the owner confirms keep guards (validate first; skip for resume-like and --session-id; cover `--name=`, ccsession-orca:75; trailing --name, ccsession:657-660).
- Winners: C-002 V3 plus invalid-name test and timer criterion; C-003 V1 (seconds/random suffix) plus same-minute test; C-004 V1; C-008 V3 with F9 as a verification note.

### Variant 3 Advocate rebuttal (condensed by the orchestrator)
- X-001: confirms BLOCKING until Tasks 3 and 4 carry the invalid-name criterion. Adds: a --name or CCSESSION_NAME equal to a saved label does not start a new session, it resumes that conversation (ccsession:1681-1706, `--resume "$SESSION_ID"`); that case also needs a criterion. X-003: confirms dropping the lift by default (Claude's own `--name x` would silently become a resume of a saved `x`).
- C-001/C-006: required plan notes are F2 (`read -r` without IFS=, ccsession:1482, strips leading/trailing tab so the Task 2 tab criterion can fail silently) and F5 (`--` before pasted text starting with `-`, precedent test_plain_double_dash_still_reaches_claude test:1292-1298). F3, F4, F13 are executor notes (the 130 mapping is already pinned by Task 4 criteria).
- C-005: test code must not write launch-paths.md (plan:108 vs Constraints plan:25); the executor writes it from the final `pytest -k orca -v` output. C-007: leave the default hint alone for other callers; only ccsession-orca passes the auto-name wording (ccsession-orca:100,108); ask_session_name appends the actual limit; report the new 30 s default for the Coder New Terminal hook in the handoff (CHANGELOG:250).
- New, not yet examined: (1) Task 4 contradicts itself (plan:72): the one-second timeout test must set CCSESSION_ASK_TIMEOUT=1 (test:1682) while the same sentence requires that variable absent from Claude's environment (test:1520), so ccsession-orca needs `unset CCSESSION_ASK_TIMEOUT` before the final exec. (2) test_orca_saved_name_is_listed_and_resumes_before_the_prompt (test:1494-1509) is not named in Task 5: it runs with the prompt `fix it` and expects the question; `_orca_tty` asserts the question appears (test:1452); rewrite as `--name demo "fix it"`. (3) The 80-character cap (plan:31) does not say which end is cut; a long worktree folder name would drop the stamp; truncate the folder name and words first and keep the stamp.

## Scoring Matrix (per diff point; winner = card whose recommendation the executor should follow)

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| S-001 | none (cosmetic) | 90% | card shape differs only by lens |
| S-002 | Variant 1 | 85% | severity vocabulary: after Round 2 all three call the invalid-name path blocking-until-criterion |
| C-001 | Variant 1 and Variant 3 (tie, same fix) | 95% | both put --auto-name in the early fast-path (ccsession:597-628) |
| C-002 | Variant 3, extended by Variant 1 and Variant 2 | 90% | Enter reopen tests plus test_orca_invalid_name_asks_again, Ctrl+C prompt argument, CCSESSION_NAME env exclusion, saved-name test (test:1494-1509) |
| C-003 | Variant 1 | 85% | seconds/random suffix plus same-minute test; sync_name renames the list only |
| C-004 | Variant 1 | 85% | drop the --name lift by default; V2 and V3 conceded |
| C-005 | Variant 3 | 70% | only V3 argued it in Round 2; V1/V2 did not dispute |
| C-006 | Variant 1 (F2, F5 required; F3, F4, F13 executor notes) | 70% | V3 narrowed the required set; V1 originated |
| C-007 | Variant 3 | 80% | keep the old default hint for other callers; report the 30 s default in the Coder handoff |
| C-008 | Variant 3 | 80% | keep print mode and AUTOSTART=0; F9 as a verification note |
| C-009 | Variant 2 and Variant 3 | 80% | timer-default criterion, README session-id row, rule wording |
| X-001 | Variant 1 | 90% | blocking until a Task 3/4 invalid-name criterion exists; V2 and V3 moved to it |
| X-002 | Variant 1 and Variant 3 | 90% | minor; sync_name renames the list only |
| X-003 | Variant 1 | 85% | drop the lift by default |
| A-002 | QUALIFY (unanimous) | 85% | hook records only sessions with a first message; collision handling covers saved conversations only |
| A-003 | QUALIFY (unanimous) | 85% | wording notes ride as notes; the fallback and --auto-name placement change behaviour and must be required notes |
| A-004 | QUALIFY (unanimous) | 85% | `=` forms and a trailing --name must be covered |
| A-005 | QUALIFY (unanimous) | 85% | a single os.write paste proves only the already-arrived case |

## Convergence Assessment (before the invariant probe)
- Points resolved: 16 of 18 with unanimous direction; C-005 and C-006 are supported by one advocate and undisputed by the others (counted as not agreed).
- Alignment: 0.8889. Threshold: 0.80.
- Taxonomy coverage: L1 (S-001, C-005, C-009), L2 (S-002, C-001, C-002, C-004, C-007, C-008, X-003, A-003, A-004) and L3 (C-003, C-006, X-001, X-002, A-002, A-005) all addressed.
- Status before Round 2.5: CONVERGED pending the invariant-probe gate.
