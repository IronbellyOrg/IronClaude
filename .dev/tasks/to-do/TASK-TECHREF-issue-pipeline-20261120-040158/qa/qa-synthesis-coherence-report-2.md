# QA Report - Synthesis Coherence (Partition 2 of 2)

**QA phase:** synthesis-gate (qualitative)
**Lens:** synthesis-coherence
**Partition:** 2
**Date:** 2026-11-20
**Assigned files:** synth-04, synth-05, synth-06 (cross-partition reading: synth-01, synth-02, synth-03)
**BLOCKING findings:** 4 (F-1 to F-4); MINOR notes: 7 (M-1 to M-7)

## Verdict: FAIL

## Working notes
(appended incrementally below)

### Step A: files read in full (synth-04, synth-05, synth-06, synth-01, synth-02, synth-03)
Check 2 ledger comparison (synth-01 Section 2.3 vs synth-06 Section 14.2):
- Row 1 BUILT-OFF -> D-06 BUILT-OFF: match. Rows 7, 15, 17 NOT BUILT -> D-16 NOT BUILT: match. Row 8 REMOVED -> D-17 REMOVED: match. Row 9 REMOVED -> D-27 REMOVED (route B D-26 NOT BUILT): match. Row 11 -> D-22: match. Row 12 BUILT-OFF -> D-19 BUILT-OFF: match. Row 13 -> D-21: match. Row 14 -> D-04: match. Row 16 -> D-05: match.
- Row 10 (caller of `orca_worktree.py pending`) NOT BUILT and row 18 (binding of coordinator-started workers) NOT BUILT -> D-18 status word is "BUILT-ON (verb), no production caller": MISMATCH (F-1).
### Step B: facts spot-verified in snapshot (read-only)
- launch-prompt.md:23 lists `/sc:task`; launch-level-guard.sh:347 regex accepts only `/sc:implement` and `/task` (confirmed).
- Guard :363-365 (no marker, exit 0) and :391 (tool event, unbound, exit 0) both exist (synth-01 cites 363-365, synth-04 cites 391: both true).
- Section 13 names `_cond` :587, `_stopped` :590, `exit_for` :480, `resolve_exit` :466, `_issue_arg` etc., `_check_never_as_worker` :734, test names and line numbers exist in the snapshot.
- WORKER-CONTRACT.md: headings :9, :27, :49, :68, :299; WC-3 :53, WC-7 :60, WC-8 :40, WC-9 :41, WC-13 :62, WC-14 :63; zero hits for claim|adopt|watcher|dispatcher|zero-setup and COORD- (snapshot).
- `pending` is run by TWO test files: tests/hooks/test_launch_level_guard_worker.py:287 and tests/skills/test_issue_orca_worktree.py:2475, :2488-2489, :2497-2498 (F-3).
- Sums re-computed: watcher tests 19,801 lines / 867 tests (A.1); guard-stack 17 files 24,388 lines / 920 strict tests; removed package 1,597 lines, 116 tests / 2,391 lines; A.1 21 + A.2 11 + A.3 9 + A.4 7 = 48 rows. All agree with synth-01.
- tests/hooks/test_launch_level_pre_push.py runs real `git push` against a local bare remote (lines 82, 128, 135, 507), which contradicts the Appendix A intro sentence "none calls a real `gh`, `git` push or Orca" (F-4).
- Source of the quote at SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:268 reads "the orchestrator design replaces them, and until it lands ..."; synth-04 5.4 rewrites it as "until [its replacement] lands" (MINOR note M-3).
- PR 686 / rewrite grep over synthesis/: the only hit is synth-01 line 44 (the one sentence BUILD-REQUEST (g) requires). synth-04, synth-05, synth-06: zero hits ("685-686", "654-686" are line ranges; "rewrites" in synth-04 lines 182, 201, 289 describes the Bash-hook command rewriter, not the rewrite design; "PR 682" is the removal commit).

## Cross-section fact table (Fact | Where stated | Identical yes/no)

| # | Fact | Where stated | Identical |
|---|------|--------------|-----------|
| 1 | Watcher real cycle BUILT-OFF (enabled:false), `enabled` default false, `once --dry-run` ignores it | synth-01 rows 1, 1b; synth-03 5.1; synth-05 9.1 and 8.1 header; synth-06 14.1.1 row 1, D-06 | yes |
| 2 | 59 reason words = 27 + 17 + 9 + 1 + 4 + 1 (arithmetic re-checked), five words never leave `run_cycle` | synth-01; synth-03 5.1.6; synth-05 10.2; synth-06 12.1, 13.1.1 | yes |
| 3 | Exit precedence 2, 6, 7, 5, 3, 4; 75 only when sole condition; exit-code groups and member words | synth-03 5.1.1 and 5.1.4; synth-05 10.1; synth-06 12.2 | yes |
| 4 | Seven read-only `gh` argv G1-G7; call cap 35 = 32 + 3 reserved; ceiling 37; idle 2 | synth-01; synth-02 4.1, 4.5; synth-03 5.1.2; synth-05 8.1, 11.1 | yes |
| 5 | Watcher launch argv has 12 elements; retry argv 14; prompt `/sc:issue --claim <N> --pipeline none` | synth-02 4.5; synth-03 5.1.3; synth-05 8.1, 8.3, 9.4 | yes |
| 6 | Clock-skew warning 60 s (`SKEW_WARN_S`, cycle.py:44); claim-marker window 300 s (`SKEW_TOLERANCE_S`, predicates.py:17) | synth-02 4.1/4.2; synth-03 5.1.8; synth-05 11.1; synth-06 KW-1 | yes |
| 7 | `MAX_LAUNCHES_PER_CYCLE` dead; 14 constants, 13 read; cap enforced by `_Cand.launching` + `halt` (833-834) | synth-03 5.1.7; synth-05 11.1; synth-06 KW-2, D-01, 12.3 | yes |
| 8 | `dispatch.json`: 7 top-level keys, 17-field entries, 6 states, `claimed` terminal | synth-01; synth-02 6; synth-03 5.1.3; synth-05 10.2; synth-06 12.1 | yes |
| 9 | Claim writes C1-C4 (exact commands), ClickUp PUT at clickup_claim.py:232-237 | synth-02 4.5; synth-04 5.2; synth-05 8.1 | yes |
| 10 | 13 STOP codes; 8 + 4 warning codes; script exit codes (orca_worktree 0/2, origin_repo 0/1/2/3/4, clickup 0/2) | synth-04 5.2; synth-05 8.2, 10.2, 10.4; synth-06 12.1 | yes |
| 11 | Launch argv `[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it.`, level words worktree/full/full-submit, pending file 0600 / dir 0700 | synth-02 4.3, 6; synth-04 5.2, 5.3; synth-05 8.1, 8.3 | yes |
| 12 | 18 `LL-*` block words and block precedence BIG TAMPER MERGE GHWRITE PROTECTED ESCAPE MCP UNKNOWN SUBMIT REPO PUSH PUSHFORM COMMIT TURN IMPL SKILL | synth-04 5.3; synth-05 10.2; synth-06 12.1, 13.1.5 | yes |
| 13 | Level grid: IMPL and TURN blocked at W only; COMMIT, PUSH, SUBMIT, SKILL blocked at W, WA, F, allowed at FS | synth-02 4.6; synth-04 5.3; synth-05 10.2 | yes |
| 14 | Typed approval = first line `/sc:implement` or `/task` (regex GD:347); `/sc:task` NOT accepted | synth-02 4.3, 4.6; synth-04 5.3; synth-05 10.2; synth-06 X-21, D-23 | yes, EXCEPT synth-04 5.2 level table `worktree` row, which lists `/sc:task` with no tag (F-2) |
| 15 | L2 exit codes 0 / 1 (`L2-PROTECTED`, `L2-UNKNOWN`) / 2 (`L2-MALFORMED`); protected refs main and master | synth-02 4.6; synth-04 5.3; synth-05 8.1, 9.2, 10.4; synth-06 12.1 | yes |
| 16 | Hook timeouts 5 s (guard, identity), `timeout 10` (L2 identity lookup); hooks.json 192 lines, plugin copy 154 | synth-02 3.1; synth-04 5.3; synth-05 8.4, 11.1 | yes |
| 17 | Plugin `hooks.json` differs in three ways (no ccsession-tag entries, no pragmatic-subagent.js, `async` on freshness-subagent-start.sh); three scripts byte-identical | synth-04 5.3; synth-05 8.4; synth-06 12.1, 13.1.6, X-27 | yes |
| 18 | WORKER-CONTRACT.md 339 lines; WC-2..WC-16 = 15 rules; no WC-17; no "Issue pipeline duties"; "grant row" once at :57; headings :9 :27 :49 :68 :299 (re-read in snapshot) | synth-01 rows 7, 7b; synth-04 5.4; synth-06 D-16, D-31, X-28, B.5 | yes |
| 19 | Removed package: 10 files, 1,597 lines (re-added), 10 verbs, 116 tests in 10 files / 2,391 lines (re-added) + 1 registration test, commit 01e7a9e23 PR 682 dated 2026-11-19 18:02 -0600 = 2026-11-20 00:02 UTC | synth-01; synth-02 3; synth-06 B.1, B.2, B.8 | yes |
| 20 | Guard-stack tests: 14 table files + 3 claim-side = 17 files, 24,388 lines (re-added), 920 strict / 921 plain tests; main guard file 4,631 lines / 162 tests | synth-01; synth-04 5.3 test table; synth-05 A.2-A.4 | yes |
| 21 | Watcher tests: 20 files, 19,801 lines (re-added), 867 tests (re-added), 19 `_assumed_shape` fixtures | synth-01; synth-05 A.1; synth-06 D-05 | yes |
| 22 | Appendix A has 48 rows (21 + 11 + 9 + 7); 44 required + 4 added (counts re-derived) | synth-05 A closing line | yes (internal) |
| 23 | IR-7 refusal BUILT-OFF as constant `IR7_REFUSE = False` (OW:822, 1757-1758), pinned test_issue_l2_install.py:639 | synth-01 row 12; synth-02 4.3, 4.4, 4.6; synth-04 5.2, 5.3; synth-05 9.2; synth-06 D-19 | yes |
| 24 | IR-3 `pipeline.json` NOT BUILT; OB-H ship gate NOT BUILT (prose); 12 skipped observation tests | synth-01 rows 11, 13; synth-02 4.6; synth-04 5.2, 5.3; synth-06 D-21, D-22 | yes |
| 25 | `orca-ide` not recognised by guard (basename `orca` only, GD:457); observed exit 0 | synth-04 5.3; synth-05 8.1 (Orca CLI order); synth-06 D-25, 13.1.5 | yes |
| 26 | `orca_worktree.py pending` status word | synth-01 rows 10, 18: NOT BUILT; synth-04 5.2: NOT BUILT (caller) / BUILT-ON (verb); synth-02 4.4, synth-05 8.3, synth-06 D-18: BUILT-ON (verb) | NO (F-1): D-18 gives BUILT-ON for the capability that synth-01 row 18 titles identically and marks NOT BUILT |
| 27 | Test callers of `pending` | synth-01 row 10 and synth-06 D-18: two files (guard_worker.py:287, test_issue_orca_worktree.py:2472-2498); synth-05 A.3: orca_worktree test pins `pending` :2472-2498; synth-05 A.2 and 8.3, synth-02 4.3/4.4: "only" the guard-worker test :287 | NO (F-3) |
| 28 | Appendix A intro "none calls a real `gh`, `git` push or Orca" | synth-05 A intro vs synth-05 A.2 pre-push row ("real git and a bare remote") and test file lines 82, 135, 507 | NO (F-4) |
| 29 | FU-1 status | synth-03 5.1.7, synth-06 D-05, 14.3: NOT BUILT (live-test record); synth-04 5.3 ledger: REMOVED (runbook); synth-06 D-28: REMOVED (the commands) | partly: two different artefacts share the label (MINOR M-1) |
| 30 | Default `--pipeline` pick | synth-02 4.2: "BUILT-ON as text only"; synth-04 5.2, synth-06 D-20: "NOT BUILT (as code)"; synth-05 9.2: "model-applied prose, not code" | wording differs, fact identical (MINOR M-2) |
| 31 | Worker tier pins t1 tier1b, t2 tier2, t3 tier2b on line 6; agent files 35 lines; 15 templates | synth-01; synth-02 3.1; synth-04 5.2; synth-05 A.3; synth-06 13.1.7, KW-7 | yes |
| 32 | Guard binding cites: no-marker exit at GD:363-365 (synth-01) and tool-event unbound exit at GD:391 (synth-04) | snapshot lines 363-365 and 390-391 both exist and say what each file claims | yes (different true citations) |

## Findings

| ID | Severity | Location(s) | Problem | Evidence | Required fix |
|----|----------|-------------|---------|----------|--------------|
| F-1 | BLOCKING | synth-06 Section 14.2 row D-18 (status word) vs synth-01 Section 2.3 rows 10 and 18; synth-04 5.2 status line "Any caller of `orca_worktree.py pending`" and 5.3 G1 row; cross-partition with synth-02 4.4 row `orca_worktree.py pending` | The same capability, "Binding of coordinator-started workers" / "caller of `orca_worktree.py pending`", carries two status words. Ledger rows 10 and 18 and synth-04 (5.2 caller row, 5.3 G1 row, ledger of guard items) say NOT BUILT; D-18 says "BUILT-ON (verb), no production caller", and synth-02 4.4 / synth-05 8.3 say "BUILT-ON as a verb". Check 2 requires the same status word in 14.2 as in the synth-01 ledger. | synth-01 lines 159 and 168 (NOT BUILT); synth-06 line 238 (BUILT-ON (verb)); synth-04 lines 28, 192, 315; synth-02 line 218; synth-05 line 88. Code: `cmd_pending` exists (OW:1515-1523, 1886-1893), no production caller. | Pick one scheme and apply it everywhere: for example D-18 status word "NOT BUILT (binding and caller); the `pending` verb itself is BUILT-ON", and give synth-02 4.4 and synth-05 8.3 the same split wording as synth-04 5.2 already uses. |
| F-2 | BLOCKING | synth-04 5.2 table "`--pipeline` levels", row `worktree` (line 111) vs synth-04 5.3 "Typed approval versus the `/sc:task` mismatch" (line 268), synth-05 8.2 (line 69) and 10.2 (line 223), synth-02 4.3/4.6 | The 5.2 row states as fact that a person approves by a first line starting `/sc:implement`, `/sc:task` or `/task`. The guard accepts only `/sc:implement` and `/task`; a typed `/sc:task` creates no `.ok`. The cell carries no [CODE-CONTRADICTED] tag or pointer, so one subsection says `/sc:task` approves and the next, plus synth-05, says it does not. This also breaks the CROSS_VALIDATION requirement that every doc-sourced claim carry a tag. | Snapshot launch-prompt.md:23 contains `/sc:task`; launch-level-guard.sh:347 `LL_RE_APR='^[[:space:]]*/(sc:implement\|task)([[:space:]]\|$)'` (read in snapshot); synth-04 line 111 vs lines 268, 389; synth-05 lines 69, 223. | In the 5.2 `worktree` row write "`/sc:implement` or `/task` (the template at `launch-prompt.md:23` also names `/sc:task`; [CODE-CONTRADICTED], see 5.3 and D-23)". |
| F-3 | BLOCKING | synth-05 Appendix A.2 row `test_launch_level_guard_worker.py` ("the only test caller of `orca_worktree.py pending` (`:287`)") and Section 8.3 last row ("only test caller ... `:287`"); cross-partition synth-02 4.3 and 4.4 ("only `...worker.py:287`", "only caller is a test") | False and self-contradicting claim. A second test file also runs the verb: `tests/skills/test_issue_orca_worktree.py:2475` (`run_json("pending", "--level", "worktree")`), `:2488-2489`, `:2497-2498`. synth-05 A.3 line 354 itself lists "`pending` verb (`:2472-2498`)", synth-01 row 10 and synth-06 D-18 list both files. | Grep of tests/hooks/test_launch_level_guard_worker.py finds one call (line 287); Read of test_issue_orca_worktree.py lines 2472-2501 shows three tests calling `pending`. synth-05 lines 88, 341, 354; synth-01 line 159; synth-06 line 238. | Replace "the only test caller" with "test callers: `tests/hooks/test_launch_level_guard_worker.py:287` and `tests/skills/test_issue_orca_worktree.py:2472-2498`" in synth-05 A.2 and 8.3 (and synth-02 4.3/4.4). |
| F-4 | BLOCKING | synth-05 Appendix A intro (line 305) vs synth-05 A.2 row `test_launch_level_pre_push.py` (line 343) | The intro says "All tests below use fakes, stubs or temporary homes; none calls a real `gh`, `git` push or Orca". The pre-push tests run real `git push` commands against a local bare remote, which the A.2 row itself says ("with real git and a bare remote (create/update/delete/force/mixed/linked worktree)"). The blanket sentence is false for this file and tells the owner the L2 hook was never exercised by a real push. | tests/hooks/test_launch_level_pre_push.py:82 `shlex.join(["git", "push", "origin", *args])`, :128 `git init --bare`, :135 `push -q origin HEAD:refs/heads/main ...`, :507 `repo.run(actor, ["git push origin"])` (snapshot). | Reword to "none calls the real GitHub (`gh`) or Orca; the pre-push and L2-install tests run real `git` against temporary local repositories and a local bare remote". |
| M-1 | MINOR | synth-04 5.3 ledger row "FU-1 ... REMOVED"; synth-06 D-05 / 14.3 "FU-1 live test ... NOT BUILT"; D-28 "REMOVED (the commands)" | One label, two artefacts (live-test record vs. the runbook `issue-pipeline-fu1.md`, which still exists as a file), two status words. Wording only: the parentheticals say which is meant. | synth-04 line 318; synth-06 lines 225, 248, 257. | Write "FU-1 runbook (file present; its run commands REMOVED)" in synth-04 and keep D-28 wording. |
| M-2 | MINOR | synth-02 4.2 line 159 ("BUILT-ON as text only") vs synth-04 5.2 line 29 and synth-06 D-20 ("NOT BUILT (as code)") | Same capability (default `--pipeline` pick), two status words, each qualified; the underlying fact (prose rule, no code) is identical. | lines cited | Use "NOT BUILT as code (prose rule only)" in synth-02 too. |
| M-3 | MINOR | synth-04 5.4 (line 383) quote "until [its replacement] lands" | The source (SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:268) reads "the orchestrator design replaces them, and until it lands ..."; the bracketed rewording hints at a planned replacement without naming it. Not a PR 686 mention, but it is the only place in the three files that gestures at one. | snapshot line 268 | Quote the clause as written or cut it to "no contract rule says who starts that worker". |
| M-4 | MINOR | synth-04 5.2 line 28, 5.3 line 192, line 389; synth-04 lines 283, 389 | Dangling identifiers: Q-11, Q-12, Q-13, Q-17 and C-36, C-38, C-64 are said to be "listed in Section 14", but Section 14 (synth-06) never uses those ids; they exist only in the gap log. Q-14 is used in D-23; Q-02..Q-10, Q-18..Q-24 are used in synth-06. | grep of synthesis/ for `Q-1[0-9]|C-3[0-9]|C-64` | Map each id to its D-xx or U-x row, or drop the ids in the assembled document. |
| M-5 | MINOR | synth-06 Section 13 intro and 13.1.x vs check 4 | Section 13 names functions and tests that appear in none of synth-03, synth-04, synth-05 (for example `_cond`, `_stopped`, `exit_for`, `_issue_arg`, `_page_arg`, `_cursor_args`, `_trigger_arg`, `_login_arg`, `_check_never_as_worker`, `_FRESHNESS_SCRIPTS`, `test_grid_complete`, `test_tier_ids_appear_only_in_allowed_paths`, `df42_*` tests). All were found in the snapshot (cycle.py:480, 587, 590; github.py:111, 118, 141, 150, 168; test_worker_contract.py:734; install_hooks.py:42; test_launch_level_guard.py:3401; test_model_alias_policy.py:104; test_record.py has 2 `df42` tests), so nothing is invented. | Grep results listed in Working notes | No fix needed; optionally list these names once in Section 5 so the evidence chain is closed. |
| M-6 | MINOR | synth-05 11.1 row `DEADLINE_TOTAL_S` ("sized for a 5 minute cadence") | A design statement (DES says 300 s cadence) in a table of code constants, untagged; no scheduler exists (synth-05 9.3 says NOT BUILT). | synth-05 lines 167, 274 | Tag "[doc-sourced, UNVERIFIED]" or delete the parenthetical. |
| M-7 | MINOR (cross-partition, informational) | synth-01 line 44 | Contains the one allowed sentence "PR 686 and the rewrite design are out of scope for this reference." BUILD-REQUEST (g) requires exactly this; nothing else in synthesis/ mentions PR 686. No action. | grep above | none |

Count: 4 BLOCKING (F-1 to F-4), 7 MINOR (M-1 to M-7). The adversarial stance is not a quota; no other defect could be evidenced.

## Checks performed

1. Story connects across files, names/counts/status words/constants/commands/exit codes identical: FAIL. 32 facts compared in the table above; 26 identical, rows 14 (F-2), 26 (F-1), 27 (F-3), 28 (F-4) differ; rows 29 and 30 (M-1, M-2) are wording-level. Counts were re-derived by arithmetic (59 reason words, 867 / 19,801 watcher tests, 920 guard-stack tests over 24,388 lines, 1,597 removed lines, 116 removed tests over 2,391 lines, 48 matrix rows).
2. Every synth-01 ledger row marked BUILT-OFF, NOT BUILT or REMOVED has a synth-06 14.2 row with the same status word: FAIL for rows 10 and 18 only (D-18). Rows 1, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17 and the route-B note in row 9 map to D-06, D-16, D-17, D-27, D-22, D-19, D-21, D-04, D-16, D-05, D-16, D-26 with identical status words.
3. Commands, argv, constants, exit codes in synth-05 Sections 8, 10, 11 identical to synth-03 and synth-04: PASS. G1-G7 argv and call sites, launch argv (12 / 14 elements), claim C1-C4, worktree-step argv, governed launch argv, exit-code tables (0,1,2,3,4,5,6,7,75, precedence), STOP and warning codes, timeouts (120 / 30 / 15, 5 tries x 2.0 s, hook timeouts 5 and 10), L2 exit codes, 18 guard words and precedence, level grid, byte limits (65536, 8192, 64 args, 1 MiB) all agree. Only the F-2 and F-3 items are exceptions, and they sit in synth-04 5.2 and synth-05 A/8.3.
4. Section 13 scenarios refer only to evidenced files, functions, tests: PASS with note M-5 (names come from the research files, not from synth-03/04/05; each was found in the snapshot, none is invented). The eight scenarios (13.1.1 to 13.1.8) each name a pinned test file; 13.1.8 states "whether a plugin copy of the contract exists: not determinable from research".
5. Appendix B agrees with 5.4 and 14.2 on the removed package and the retired G2 rule 1 / route A: PASS. Commit id, PR 682, timestamps, 10 files / 1,597 lines, 10 verbs, WC-17 and "Issue pipeline duties", 116 tests, test_worker_contract.py 3,181 to 3,135 lines (+8/-54) and 61 to 59 tests, guard 811 to 808 lines, WORKER-CONTRACT 350 to 339 lines, guard comment at GD:496-497, `.ok` writer at GD:347-359, B.9 mapping to D-16, D-17, D-18, D-27, D-31 all agree with 5.4, 14.2 and synth-01 rows 8 and 9.
6. Contradictions between research files surfaced, not silently resolved: PASS. Applied errata (agent files 35 lines, 17 guard-stack test files, 15 templates, "seven" repository-wide alias tests, 14 constants / 13 read, DES:827 re-tagged CODE-VERIFIED) are each stated and, where they overturn an earlier claim, named (KW-1, B.8 "-56 vs -30", X-27, U-8 "739 tests").
7. Verified fact, [UNVERIFIED] statements and evidence limits separated: PASS. Section 14.3.1 (U-1 to U-11) holds the limits; per-row tags are used consistently; the observed-versus-read distinction is explicit in 5.3. M-6 is the one untagged design statement.
8. No aspirational content described as current: PASS with M-3 and M-6. Planned items (FU-2, FU-8, scheduler, dispatcher, COORD-) are labelled NOT BUILT / "not found in snapshot".
9. No mention of PR 686 or the rewrite design in the three files: PASS (grep, zero hits; see working notes). M-3 notes one quote that gestures at a replacement.
10. Written for the owner (tables first, no unexplained jargon): PASS with notes. 5.2 / 5.3 / 14.2 are dense but table-first; L1/L2, W/WA/F/FS, IR-3/4/7, OB-H are glossed on first use in synth-01 and synth-04; dangling ids are M-4.

## Self-Audit

**(a) Reliance list:** no Inherited Structural Verdict was supplied in the prompt, so no structural PASS item was skipped. Standalone behaviour applied.

**(b) Independent semantic checks (>=1 required, INV-019):**
- Level-approval wording: Read launch-level-guard.sh lines 340-395 and grep of launch-prompt.md:23 in the snapshot; confirmed regex accepts only `/sc:implement` and `/task` while the template names `/sc:task` (F-2).
- Test callers of `pending`: Grep of tests/hooks/test_launch_level_guard_worker.py (one hit, :287) and Read of tests/skills/test_issue_orca_worktree.py:2468-2501 (three tests call it) (F-3).
- Real `git push` in pre-push tests: Grep of tests/hooks/test_launch_level_pre_push.py lines 82, 128, 135, 507 (F-4).
- Ledger-to-14.2 status mapping built row by row from synth-01 lines 148-168 against synth-06 lines 221-251 (F-1).
- Section 13 names: Grep of the snapshot for `_cond`, `_stopped`, `exit_for`, `resolve_exit`, `_issue_arg` family, `_check_never_as_worker`, the grid tests, `_FRESHNESS_SCRIPTS`, `df42` tests.
- WORKER-CONTRACT.md headings and WC line numbers; zero hits for claim|adopt|watcher|dispatcher|zero-setup and for COORD- (snapshot).
- Research errata (R01 B-1, R03 F-1, R04 B-2 / F-2 / N-1, R05 B-3) read and compared with how synth-01, 03, 04, 05, 06 applied them.
- Source of the :268 quote read in the snapshot (M-3).

Web research: none performed (no external lookup needed; Tavily not used, not required).

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 24 | Grep: 21 | Glob: 2 | Bash: 0 (Read + Grep + Glob = 47 >= 10 checks)

Out-of-scope note: the snapshot was only read (Read, Grep); nothing under /home/coder/.cache/ic-snap-20261120/master was written. Only this report file was written.

Status: Complete
