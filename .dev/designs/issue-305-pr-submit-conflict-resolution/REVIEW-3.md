# REVIEW-3: DESIGN.md Revision 3 (issue #305 conflict resolution)

Verdict: **PASS** (0 BLOCKING, 9 MINOR).

N1 is fixed. Every resume path of an open conflict cycle now either restarts safely, settles a matched crash window, or halts and closes the cycle once. No path pushes twice, retries a push silently, skips VAL, or pushes anything but the recorded merge commit. All nine m-items from REVIEW-2 are addressed. Residual wording gaps on m1, m4 and m5 are listed as MINOR below.

Scope: N1, the Revision 3 edits for m1 to m9, and force-flag and `--repo` hygiene in the planned `.md` / `.sh` text. Items earlier reviews marked FIXED were rechecked only where Revision 3 touched them (the Branch C order and the closing table).

## N1 status: FIXED

**Mechanism.** `conflict_resume_plan` now takes `dangling = detect_crash_window(run_log)` (DESIGN.md:359-363, :591).

- Row 4b fires only when `dangling["cycle_id"]` equals the open cycle's id (:375).
- New row 4b' (:376) catches the remaining case: `push_initiated` without `push_completed`, and `dangling` is `None` or belongs to another cycle. It halts `resume_unrepresentable`, closes the cycle once, names `target_sha`, and plans no push.
- Rows 4, 4b and 4b' together cover every open cycle that has a `push_initiated`. The restart rows 5 and 7 therefore never run for an attempt that wrote a push record. That rules out pushing a second, different merge commit.

**Code basis.** `detect_crash_window` (recovery.py:63-80):

- keeps `finalized` as an unordered set, finalized only by `push_completed` and `push_aborted_or_not_landed`;
- returns the first unfinalized key, in insertion order.

Branch B appends `push_aborted_or_not_landed` with the key (recovery.py:149-159). So after Branch B, the re-drive's `push_initiated`, which reuses the key, is never returned again. This is exactly the case 4b' covers. Branch C appends `terminal_halted`, not a finalizer (recovery.py:161-171), so its key stays unfinalized.

**Paths traced** (each one is a resume of an open conflict cycle; "K" is the cycle's push key):

| Path | Next resume reaches | Result |
|---|---|---|
| Crash before `push_initiated` (merge in progress, or not started) | 5 / 7 restart (wave8a from step 1, c_initial from step 0, VAL rerun) or 6 / 8 halt | safe; closed `aborted` or `halted` once |
| First push: crash after `push_initiated`, or `push_failed` (no record) | 4b (dangling K matches) | three-way check through `resolve_crash_window_plan` |
| 4b, then Branch A | wrapper closes `pushed` (:402, :697-704) | no push; `wave8_ci_wait` or S5a / S5 |
| Crash between the recovered `push_completed` and the wrapper's append | 4c, then 4 `complete_after_push` | no push; closed once |
| 4b, then Branch C | wrapper appends `sync_concluded{halted}` after `terminal_halted` (:404) | halt; closed once (K stays unfinalized; see n3) |
| 4b, then a crash between the Branch B record and the re-drive's `push_initiated` (including a crash inside the wrapper) | 4b' (K finalized, so `dangling` is `None`) | halt; no push; closed once |
| Branch B, then a crash after the re-drive's `push_initiated` | 4b' | halt; no push; closed once (test :1337 `test_branch_b_crash_during_redrive_halts_and_closes_once`) |
| Branch B, then the re-drive ends `push_failed` | 4b' | halt; no push; closed once (test :1337 `..._push_failed_then_resume_...`) |
| Branch B, then the re-drive is rejected | record (key K) + `sync_concluded{halted}`; any later resume hits row 1 (sticky) | never re-driven (INV-035) |
| Crash between a rejected record and its `sync_concluded` | row 1, which closes the open cycle (m2) | closed once (test `test_resume_row_1_closes_an_open_cycle`) |
| Branch B re-drive lands, then a crash before the SKILL's `sync_concluded` | 4 `complete_after_push` | no push; closed once |
| Branch B guard failure | the halt's own rule, `sync_concluded{halted}` | no push record |

**Supporting text and tests.**

- Consistent across the Branch B row (:403), step 12 (:302), section 9 `push_failed` and the new 4b' row (:1121-1122), D-8 (:1220), 14 V8 (:1441), 16 V8 (:1480) and 8.2 row 10 (:995). The "exactly as in step 12" claim is gone.
- Tests asked for by REVIEW-2 (c) are present (:1337).

**Later fix-push crash in the same run.** It still resumes into its own crash window:

- After A, after a landed B (K finalized by `push_completed`), and after 4b' (K finalized), `detect_crash_window` skips K and returns the fix record.
- `test_conflict_crash_then_later_fix_crash_resumes_into_fix_window` (:1337) pins the Branch A case.
- The landed-B case holds by the same logic but has no test (n4).

## m-item status

| ID | Status | Evidence |
|---|---|---|
| m1 | FIXED (wording residual, n2) | The 4.7 invariant now names a crash and a `push_failed` halt as the only ways an attempt stays open (:316-321) |
| m2 | FIXED | Row 1 closes an open cycle (:369). The closing rule lists 1, 3b, 4c, 4b', 6 and 8 (:382). Test :1337 |
| m3 | FIXED | Helper `prior_conflict_cycles` (:585), exported (:743). Stated in the 4.4 guard (:218), 4.8 (:384), the `conflict_action` contract (:577) and the `evaluate_sync_decision` contract (:580). Tested in 12.1 (:1319) and in the 12.2 restart test (:1337). Hand-traced: Wave 8a Tier 1, `P`, L3 with 0 prior cycles gives `resolve_push`; with 1 prior cycle it gives `report` / `sync_cap` (:255-260) |
| m4 | FIXED (ordering residual, n6) | Row 5: a `c_initial` restart runs from step 0 at `S2_CLASSIFY`; `round_counter` is unchanged (:377). Row 7 refers to row 5 (:379) |
| m5 | FIXED (section 9 residual, n7) | The exception and why it is safe are stated (:404). `test_branch_c_event_order` (:1337). Matches recovery.py:161-171, followed by the wrapper append (:701-704) |
| m6 | FIXED | The fold copies `expect_checks` and stores `True` when missing or not a bool (:670, :672). Row 4 (:374), `ResumePlan.expect_checks` (:560), 5.3 (:591), test `test_resume_row_4_expect_checks_defaults_true` |
| m7 | FIXED | "after `clean` / `REPORT_ONLY`" in 4.2 (:166), E10 (:943) and 8.2 row 3 (:988) |
| m8 | FIXED | Row 4c checks `hook` and is ordered before 4, 4b, 4b', 5 and 7 (:373). The table is in evaluation order (:365). Test in 12.1 (:1319) |
| m9 | FIXED | Section 9 says `router_unreachable` always halts (:1126). The 5.2 overlap set is unchanged (:446-449) |

## New BLOCKING findings

None.

## MINOR notes

- **n1 (undefined field).** Row 4b' and 5.3 say the plan carries `target_sha` (:376, :591), and both 12.1 and the N1 test assert it (:1319, :1337). `ResumePlan` (:547-562) has no `target_sha` field; only `wait_sha` comes close. Add `target_sha: str | None = None` to 5.2.
- **n2 (4.7 invariant wording).**
  - "It comes at the latest in the first `--resume`" is false for this sequence: 4b, then Branch B, then a re-drive that ends `push_failed`. That cycle stays open after the first resume, and the second resume closes it through 4b'.
  - "Through row 4b or row 4b'" also leaves out the other closing rows: 1, 3b, 4c, 4 and 5 to 8.
  - Fix: say the attempt is closed by the resume that ends it. A Branch B re-drive that ends `push_failed` defers the close to the next resume (4b').
- **n3 (Branch B close needs an open-cycle guard).**
  - The guard "append only while the cycle is open" is stated for the wrapper (:407) and for the halt rows (:382). It is not stated for the SKILL's Branch B exit-0 close (:403).
  - A closed cycle can still have an unfinalized key: after Branch C (recovery.py:161-171), or after 4c / 3b closed a cycle whose dangling record matched.
  - A later `--resume` then reaches that key again through row 2 and `detect_crash_window`. A Branch B re-drive there appends a second `sync_concluded` for the attempt, and `sync_outcome` flips from `halted` to `pushed`.
  - The re-drive is a three-way-checked, guarded push of the recorded commit, not a double push. The fold's pop is a no-op, so routing is unaffected.
  - Fix: apply the same "still open" guard to the SKILL close, and say in one sentence that such a resume settles the push again by the three-way check.
- **n4 (test gap).** No test covers the Branch B exit-0 close. That close is the B2 guard against row 4 capturing a later fix crash window. Add: Branch B, re-drive `push_completed`, SKILL close, `open_conflict_cycle is None`, then a later fix crash resumes into the fix window. Optionally also pin the sentence in `test_conflict_sync_protocol.py`.
- **n5 (resume after a 4b' halt).**
  - The N1 test expects a third resume to return row 2 `none` (:1337). That hands control to the generic resume, and there the re-drive's `push_initiated` is undetectable (the V8 gap).
  - It is safe today:
    - when the merge did not land, the full `pr_head_ok` binding (SKILL.md:268) halts, because local HEAD is the merge commit and the PR head is not;
    - a new Wave 8a cycle gets `sync_cap`.
  - The design does not say this. State the guard that makes it safe, or note that after 4b' the supported path is a fresh `--pr <N>` run, as the 4b' message says.
- **n6 (m4 ordering).** Step 0 (`transition(S2_CLASSIFY, "conflicting")`) is listed before step 2's re-route (:290-292), but 4.2 routes before the transition (:165).
  - On a `c_initial` restart "at step 0", suppose the fresh probe no longer yields `resolve_push`, for example when the base moved and the conflict is now Tier 1 or Tier 0. The FSM is then left at `S3_FIXING` while the router says `none` / `report`.
  - Nothing is pushed, but the next transition is undefined.
  - Fix: the restart re-runs the hook's read, probe and route, and step 0 runs only after a `resolve_push` with `fsm_event="conflicting"`; or a route other than `resolve_push` after step 0 halts `resume_unrepresentable`. Also say how the SKILL sets the FSM to `S2_CLASSIFY`.
- **n7 (m5 residual).** The section 9 intro (:1099) still says every halt is "preceded by `sync_concluded` ... when a cycle had started", with no Branch C exception. Add "(except Branch C, section 4.8)" so an ordering test does not pin the wrong sequence.
- **n8 (4b' reason text).** The 4b' note says the key "was already finalized by an earlier Branch B record". The row also matches the case where `dangling` belongs to another cycle: `detect_crash_window` returns the first unfinalized key in insertion order (recovery.py:77-79), so an earlier record can hide this cycle's matchable record. Halting there is fail closed and correct; only the explanation is too narrow.
- **n9 (test wording, carried from Revision 2 next to the new m5 test).** `test_conflict_crash_recovery_closes_the_cycle` says "a second wrapper call appends nothing" (:1337).
  - `resolve_crash_window` always appends its recovery event (recovery.py:114, :152, :162).
  - On Branch A that second event is a second recovered `push_completed`, which also double-counts `sync_push_count`.
  - Reword to "appends no second `sync_concluded`".

**Safety scan (item 3): clean.**

- The force regex `\bgit push\b[^`\n]*?(\s--force\b|\s-f\b|\s\+\S)` (test_static_grep.py:763) was checked against every planned skill-folder line that contains "git push": step 12 (:302), 8.2 row 7 (:992), the pinned phrases (:1000) and E9 d (:935). The scan stops at the closing backtick or the line end, and no force form follows.
- Revision 3's new text (row 4b', 8.2 row 10, section 9 rows) contains no "git push" and no force flag. E13 removes the only force-push phrase (:968-976).
- Every planned `gh` line carries `--repo`, a `repos/` path, or the positional `gh repo view "$REPO"`, which `_REPO_RESOLVE` accepts (test_static_grep.py:35, :103-129). This includes the new 4b' operator hint `gh pr view <N> --repo "$REPO" --json headRefOid`.
- The 4b' message lives in the ref and the SKILL, not in `conflicts.py`, so T-N50 is unaffected.

## Self-Audit

What was traced in this session:

1. **Design sections.**
   - All of 0, 4.2 to 4.8, 5.1 to 5.3, 6.1 to 6.6, 8.1 to 8.7, 9, 10.5, 12.1 to 12.5, 13, 14 and 16.
   - Every row of the 4.8 `conflict_resume_plan` table in evaluation order (1, 2, 3, 3b, 4c, 4, 4b, 4b', 5, 6, 7, 8), the closing rule, the `prior_conflict_cycles` paragraph, `crash_resume_plan`, and the B2 closing table.
2. **Code.**
   - recovery.py:57-80 (finalized-set semantics, insertion-order return), :98-110 (key tuple), :112-171 (Branches A, B and C appends);
   - run_log.py:27-35, :108-131 (:111 "41"), :161-260 (current fold; `push_completed` at :238-241);
   - fsm.py:34-37, :173-175, :217-220, :227-229, :238-290 (common :259-267, predicates :273-279), :729-732, :741-749, :1118-1124, :1135-1139;
   - SKILL.md:268, :269, :274, :275 (head binding on resume, Branch B re-drive keying);
   - test_static_grep.py:35, :103-143, :758-776.
3. **N1 resume paths.**
   - The twelve paths in the N1 table, each followed to its next resume, including a crash inside `resolve_crash_window_plan` after each branch's append.
   - A third resume after 4b' (n5).
   - Re-settling the key after Branch C or a 4c / 3b closure (n3).
   - The later fix-push crash after A, a landed B, and 4b'.
   - Checked that rows 4, 4b and 4b' cover every attempt that has a `push_initiated`, so no restart re-merges after a push record.
4. **Revision 3 consistency.**
   - The `conflict_resume_plan` signature in 4.8 and 5.3 agrees; the `ResumePlan` fields were checked against every directive (n1).
   - The `prior_conflict_cycles` helper in 4.4, 4.8, 5.3, 6.6 and 12.1 / 12.2, with the router rows hand-evaluated.
   - The fold's `expect_checks` default in 6.3, against row 4 and 5.3.
   - The ordering and hook checks of row 4c.
   - The c_initial step-0 restart against 4.2 and the 4.6 step order (n6).
   - The Branch C order against recovery.py and section 9 (n7).
   - The section 9 overlap sentence against the 5.2 set and the router table.
   - The step 3 and step 7 split in section 13 against where each test lives.
5. **Safety.**
   - The force regex was applied by hand to each planned "git push" line.
   - The `gh` scoping of every planned `gh` occurrence (grep of DESIGN.md for backticked `gh` without `--repo` / `repos/`: only prose mentions and `gh repo view "$REPO"`).
   - No new path pushes without the recorded, VAL-passed `target_sha` plus the guard, and no planned directive retries a push without the three-way check.
