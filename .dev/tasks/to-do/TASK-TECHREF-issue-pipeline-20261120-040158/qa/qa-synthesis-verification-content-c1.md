# QA Report - Synthesis-gate verification (qualitative), cycle 1

**Topic:** IronClaude issue-to-work pipeline technical reference (six synth files)
**Date:** 2026-11-20
**Phase:** tech-ref-qualitative / synthesis-gate verification, cycle 1 (fix_authorization false)
**Fix cycle:** 1
**Status:** Complete (see the final line)

Note: the task prompt names the fix report `qa-synthesis-fix-c1-report.md`; the file that exists, and that the spawn message named, is `qa-synthesis-fix-cycle1-report.md`. That one was read.

---

Inputs fully read: the consolidated findings (G2-1..G2-9), the fix log, and all six synth files (synth-01 198 lines, synth-02 347, synth-03 331, synth-04 390, synth-05 375, synth-06 458). Source claims were re-read only under `/home/coder/.cache/ic-snap-20261120/master` (read-only; nothing written there).

## Progress notes (read-through, before source checks)

- Whole-file greps: "PR 686" / "rewrite design" appear only at synth-01 line 44; `orchestrator.md` has zero hits in all six files; "unif*", "dashboard", "orchestrator design/v2" have zero hits ("rewrite" appears only as the verb in "rewrites governed Bash calls").
- Arithmetic cross-checks that passed: watcher modules 4,795 lines; watcher tests 19,801 lines / 867 functions (A.1 sums); guard tests 24,388 lines / 920 strict (A.2 + synth-04 pins + 3 claim-side files); reason table 59 = 27+17+9+1+4+1 (synth-03 5.1.6 and synth-05 10.2 agree); 18 block words = 16 classes + LL-NOBIND + LL-BROKEN; 13 STOP codes, 12 warning codes; 8 config keys; Appendix A 48 rows = 21+11+9+7.
- Source re-reads so far (snapshot): `launch-level-guard.sh:347` regex accepts only `/sc:implement` and `/task`; `sc:task` and `orca-ide` have zero hits in the guard; `:457` is `orca)` (basename match); `CHANGELOG.md:17` records the removal of the plan-approval gate; `docs/designs/sc-issue-launch-level-hook.md:23` says the guard does not govern a coordinator-started worker; `cycle.py:1026-1112` `_launch` order is dry-run return (1029-1035), probe, prompt, re-read, day cap, DISABLED, cut-off, origin, cut-off, pending save, launch. This matches synth-02 row 11 and synth-03 5.1.1.2.
- More source re-reads (snapshot): `github.py:437-463` (`CallBudget`: per-issue calls share `CALL_CAP` 35, reserved last 3, G1/G2 counted apart and never refused) and `cycle.py:576-585`; `test_issue_orca_worktree.py:2472-2501` (three tests run `pending`); `test_launch_level_guard_worker.py:287`; `test_issue_l2_install.py:1-7` (real git, bare remote); `launch-level-guard.sh:264-269, 783-808` (level table, grid, `ll_deny LL-BROKEN` default); `orca_worktree.py:743, 756, 822, 1873, 1883, 1891`; `hooks.json:115-134`; `install_hooks.py:86-97`; `issue-worker-t3.md:1-8`; `test_issue_worker_agents.py:21-26`; `ccsession-models.json` tier keys at 85, 93, 104, 113; `launch-prompt.md:23` (names `/sc:task`); `claim.md:81, 96`; `docs/designs/sc-issue-launch-level-hook.md:23, 534, 542`.

---

## Verdict: FAIL

One new BLOCKING finding (N-1). All nine previous BLOCKING findings are FIXED-OK.

## Previous BLOCKING findings (G2-1 to G2-9)

| ID | Location | FIXED-OK / STILL-OPEN | Evidence |
|---|---|---|---|
| G2-1 | synth-01 158/160, synth-02 198/228, synth-04 192/213/315/316/378, synth-06 240-274 | FIXED-OK | Grep over all six files: zero hits for `orchestrator.md`. Replacement citations are true in the snapshot: `CHANGELOG.md:17` records removal of the `issue-pipeline` group, WC-17 and the guard's block of those commands; `docs/designs/sc-issue-launch-level-hook.md:23` says a coordinator-started worker "is not launched by the claim script, so this guard does not govern it". D-18, D-27, D-31 now say "No decision found in the files this reference cites" or cite only those two files. (A related leftover in 14.3 is reported as N-1.) |
| G2-2 | synth-02 4.1 rows 11-13 and line 138 vs synth-03 5.1.1 | FIXED-OK | `cycle.py:1026-1112` order is dry-run return (1029-1035), probe, prompt, `_revalidate`, day cap, DISABLED, cut-off, origin, cut-off, pending save, launch. synth-02 row 11 lists exactly that; synth-03 5.1.1.2 table lists the same; both say a dry-run runs steps 1-10 and returns at the top of step 11. Step numbers 0-13 are identical in synth-02 and synth-03. |
| G2-3 | synth-06 13.1.4-13.1.7 | FIXED-OK | Skeletons present. Checked against source: `BLOCK_MARKER` `[a-z]+` (`OW:743`) and `render_prompt` keeping `common` plus the level block (`OW:756`); `choices` at `OW:1873/1883` (worktree, full) and `OW:1891` (adds full-submit); level word case `GD:264-269`; one `CLASS:LEVEL` case per class, default `LL-BROKEN` (`GD:785-801`) and the precedence list at `GD:783`; hooks.json group shape (`:115-134`); `_FRESHNESS_SCRIPTS` entries at `install_hooks.py:90, 93, 96`; worker frontmatter lines 5-6 and `WORKERS` dict (`test_issue_worker_agents.py:21-26`). Gaps that research cannot fill carry "not determinable from research". |
| G2-4 | synth-01 line 34 | FIXED-OK | Now "per-issue call cap 35 (32 ordinary plus 3 reserved) plus the two shared calls G1 and G2, so at most 37 gh calls per cycle (2 when idle)". Matches `github.py:437-463`, synth-03 5.1.2, synth-05 11.1 and synth-06 13.1.3. |
| G2-5 | synth-01 106, 152, 155, 180; synth-02 291 | FIXED-OK | Caveat present in all five places with the Section 5.3 / D-25 pointer and "observed exit 0". Source: `GD:457` is `orca)` (basename match), grep for `orca-ide` in the guard returns nothing. Same fact as synth-04 line 283 and D-25. |
| G2-6 | synth-01 160, 169; synth-02 217; synth-04 28; synth-05 88; synth-06 261 | FIXED-OK | Identical wording in all six places: "NOT BUILT (binding and caller); the `pending` verb itself is BUILT-ON". synth-04 5.3 G1 rows keep "NOT BUILT (as a guard)", a different item. |
| G2-7 | synth-04 line 111 | FIXED-OK | Cell now says `/sc:implement` or `/task`, flags the template's `/sc:task` as [CODE-CONTRADICTED] with pointer to 5.3 and D-23. `GD:347` regex `^[[:space:]]*/(sc:implement\|task)([[:space:]]\|$)`; `launch-prompt.md:23` does name `/sc:task`; zero `sc:task` hits in the guard. Agrees with synth-02 4.3/4.6, synth-04 line 268, synth-05 10.2, synth-06 D-23/X-21. |
| G2-8 | synth-01 160, synth-02 198/217, synth-04 28, synth-05 88/341, synth-06 261 | FIXED-OK | Both callers named everywhere: `test_launch_level_guard_worker.py:287` and `test_issue_orca_worktree.py:2472-2498` (three tests call `pending`; the last test ends at :2501, MINOR range note). |
| G2-9 | synth-05 line 305 | FIXED-OK | Intro now says none calls real `gh` or Orca and that pre-push and L2-install tests run real git against local repositories. True: `test_issue_l2_install.py:1-7` ("Real git ... a bare remote and a clone"), A.2 row for `test_launch_level_pre_push.py`. (MINOR wording note M-3.) |

## New BLOCKING findings

| ID | Location | Problem | Evidence | carried-over / new | previously-rated-PASS |
|---|---|---|---|---|---|
| N-1 | synth-06 14.3 "Future Considerations", row at line 283 ("Binding coordinator-started workers (D-18) and the OB-H gate as code (D-21)") versus D-18 (line 261), D-21 (line 264) and 14.1.1 row at line 186 | Two places state different facts about whether a decision exists. 14.3 says these items are deferred because of "Owner decisions (OD-1 `docs/designs/sc-issue-launch-level-hook.md:534`; OD-3 `OW:818-822`)" and revisits "After the #442 observations (`OW:822`)". D-18 says "No decision found in the files this reference cites"; 14.1.1 says Planned Fix "none recorded (D-18)"; D-21 says "no decision lets the gate stay unenforced in code". The two cited decisions do not concern D-18: OD-1 is the declared limits of L2 (`design:534`, "Limits (OD-1). L2 is a same-user guard for the tested local Bash surface"), OD-3 is the IR-7 refusal staying off (`OW:818-822`; design :542 "W-L2-ABSENT warning only (OD-3)"). So the 14.3 cell attributes a deferral decision that no read file records for D-18. | Read synth-06 lines 261, 264, 186, 283; Read `design:534` and grep `OD-1\|OD-3` in the design; Read `OW:814-826`. Neither `OD-1` nor `OD-3` text mentions binding a coordinator-started worker. | New. It is the same class as G2-1 (a decision claimed that is not in a file the reference cites); it surfaced because the G2-1 fix reworded D-18 to "No decision found" and left the 14.3 row untouched. | No. Review 1 (coherence 2, check 29) examined 14.3 only for the FU-1 label (MINOR M-1); the D-18 / OD-1 / OD-3 cell was not rated. |

Required fix for N-1: in the 14.3 row, split D-18 from D-21. For D-18 write "No decision found in the files this reference cites (D-18); the guard design says it does not govern such a worker (`docs/designs/sc-issue-launch-level-hook.md:23`)" and drop OD-1 and OD-3 and the `OW:822` revisit trigger from it. Keep OD-3 and `OW:822` only if the D-21 half is rephrased to say what they actually decide (IR-7 stays off until the #442 observations pass), without calling it a decision to leave the gate prose-only.

## MINOR notes (not blocking, not rechecked)

| ID | Location | Note |
|---|---|---|
| M-1 | synth-06 13.1.3 line 94 | "per-issue budget is 32 plus 3 reserved (37 per cycle)" reads as 32+3=37; the 37 includes the two shared calls. True, but reword as in synth-01 line 34. |
| M-2 | synth-06 D-19 vs synth-01 row 12 / synth-02 4.4 / 4.6 | Same status word BUILT-OFF; the parenthetical is "(enabled:false)" in synth-01/02 and "not `enabled:false`" in D-19. Synth-01 line 145 explains the label, so only the D-19 phrase reads as a clash. |
| M-3 | synth-05 line 305 | "so they prove self-consistency with assumed reply shapes" now follows the real-git clause; for the real-git tests no reply shape is assumed. Wording only. |
| M-4 | synth-02 4.3 launch diagram (steps 1-7) vs synth-04 launch-order table (steps 1-9) | Same order and same line ranges, different numbering granularity (synth-02 merges record, already-launched, stale-prompt into step 1). No fact differs. |
| M-5 | synth-01 line 145 | "rows 1b, 7b and 9 to 18 are additional rows" omits row 12b; synth-01 intro says "four pieces plus a fifth" while the ledger says "the eight pieces" (different segmentations of the word "piece"). |
| M-6 | synth-03 5.1.1 diagram line 65 | Step 11 box omits the probe and prompt build that the table below it and synth-02 list first. Abbreviation only. |
| M-7 | synth-04 line 191 and ledger line 317 | G2 rule 2 is "BUILT-ON" with no orca-ide caveat in those two cells (caveat is in the paragraph at line 283 and in D-25); G2-5 asked only for synth-01 and synth-02 locations. |
| M-8 | synth-03 5.1.7 lines 296-297 | Status column uses "dead or write-only" and "practically unreachable" instead of the four status words; synth-06 D-07, D-09, D-10, D-11 say BUILT-ON with the same meaning in brackets. |
| M-9 | synth-04 lines 389, synth-05 none | Dangling ids Q-11, Q-12, Q-13, Q-17 are not defined in synth-06 (already MINOR M-4 in review 1). |
| M-10 | synth-04 line 111 | "first line starts `/sc:implement`" - the regex needs whitespace or end of line after the word; "starts" is loose. |

## Checks performed

1. Previous BLOCKING list: all nine rows re-checked in the live synth text and against the snapshot (table above). 9 of 9 FIXED-OK.
2. Same fact, same wording and numbers across the six files. Re-derived by arithmetic: watcher modules 4,795 lines; watcher tests 19,801 lines, 867 functions, 19 test files plus conftest; guard-stack tests 24,388 lines and 920 strict functions (14 table files plus 3 claim-side files); reason table 59 (4+7+5+2+2+5+1+1 cycle = 27, plus 17, 9, 1, 4, 1); 18 block words = 16 classes + LL-NOBIND + LL-BROKEN; 13 STOP and 12 warning codes; 8 config keys; Appendix A 48 rows (21+11+9+7), 44 named plus 4 added; `gh` budget 35/32/3/37/2; launch argv 12 (retry 14); exit codes 0-7 and 75 with precedence 2,6,7,5,3,4; 23 governed tools; hook timeouts 5/10. No disagreement.
3. Ledger (synth-01 2.3) versus Section 5 status lines, synth-02 trigger and writes tables, and synth-06 14.2 rows: mapped row 1 to D-06, 7 to D-16, 8 to D-17, 9 to D-27 (route B to D-26), 10 and 18 to D-18, 11 to D-22, 12 to D-19, 13 to D-21, 14 to D-04, 15 and 17 to D-16, 16 to D-05; status words agree (only the M-2 parenthetical differs).
4. Dry-run and launch-step ordering: synth-02 4.1, synth-03 5.1.1/5.1.1.2 and `cycle.py:1026-1112` agree.
5. PR 686: exactly one sentence (synth-01 line 44); no other mention of PR 686, the rewrite design, `orchestrator.md`, unify or dashboard in any file.
6. Aspirational content: scheduler, dispatcher, `COORD-`, zero-setup install, grant row, hand-off, live-test record, OB-H gate, SLO verb, auto-retry are all NOT BUILT, REMOVED or "not found in snapshot"; the 5-minute cadence mention in synth-05 11.1 is a sizing note, not a claim that a scheduler exists.
7. [UNVERIFIED] versus evidence limits: synth-01 "Evidence limits", synth-04 observation-run paragraph, synth-06 U-1 to U-11 agree (guard script run once on 44 payloads; everything else read, not run).
8. Fix-introduced defects hunted at every edited location (listed in the fix log); one found (N-1), minor notes M-1 to M-10.
9. Skeleton content (new in 13.1.4-13.1.7) verified line by line against source.
10. Decision claims: every "Decision:" cell in 14.2 and 14.3 checked against a cited file (CHANGELOG.md:17, design :23/:534/:542, `OW:818-822`, DES:33/28/30, SET:288); only the 14.3 D-18/D-21 cell fails.

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- No Inherited Structural Verdict block was in the spawn prompt (the structural verification file `qa-synthesis-verification-structural-c1.md` was not read), so no structural PASS item was skipped. Standalone behaviour applied.

**(b) Independent semantic checks (>=1 required, INV-019):**
- `_launch` ordering and dry-run extent - verified by reading `cycle.py:1026-1112` and `:1112-1144` in the snapshot against synth-02 row 11 and synth-03 5.1.1.2 (G2-2).
- 35 / 37 call budget - verified by reading `github.py:437-463` and `cycle.py:576-585` (G2-4).
- `/sc:task` versus the approval regex - verified by reading `launch-level-guard.sh:347` and `launch-prompt.md:23`; grep for `sc:task` and `orca-ide` in the guard (G2-5, G2-7).
- Two test callers of `pending` - verified by reading `test_issue_orca_worktree.py:2466-2501` and grep of `test_launch_level_guard_worker.py` (G2-8).
- Extension skeletons - verified by reading `launch-level-guard.sh:260-273, 778-808`, `orca_worktree.py:740-761, 1873-1891`, `hooks.json:112-137`, `install_hooks.py:86-99`, `issue-worker-t3.md:1-10`, `test_issue_worker_agents.py:18-29` (G2-3).
- Decision claims in 14.3 - verified by reading `docs/designs/sc-issue-launch-level-hook.md:532-542` and `orca_worktree.py:814-826`; led to N-1.

**Confidence:** Verified: 12/12 checklist items (tech-ref-qualitative 12, adapted) plus the 6 required checks of the task prompt | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. Limit: line-number citations that were not inside an edited location were not re-read one by one (the cited ranges that were re-read all matched; line-number drift would be MINOR).

**Tool engagement:** Read: 38 | Grep: 22 | Glob: 0 | Bash: 1 (listing). Each call maps to a check above. No web research was done (Tavily not used; none was needed).

## Recommendations

1. Fix N-1 (one table cell in synth-06 14.3, text above) before assembly; no other blocking item is open.
2. M-1, M-2 and M-3 are one-line wording edits that can ride along; the other notes can stay.
3. Review cycle 2 only needs to re-check N-1.

Status: Complete
