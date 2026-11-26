VERDICT: PASS
#811: PASS
#812: PASS
#814: PASS

## Your independent closest-overlap picks

Fixed before opening any "## Closest overlap" section (from the scan lists and `gh issue view` text).

- #811 (W3 poll interval): 1. #717 (umbrella; holds the W3 text verbatim), 2. #761 (gap list that raised the cadence question), 3. #812 (W4; same call-rate question). I did not look at #774 or #757 until after my picks. After reading its body I find #774 item 8 (poll cadence, "crontab -l", Coder PR 526 changed the entry to every minute) is a real overlap, so the findings' choice of #774 is defensible. It is the best non-umbrella, non-sibling match. Not a defect.
- #812 (W4 backoff): 1. #817 (W9 conditional reads, same call-budget problem), 2. #717, 3. #819 (W11 launch retry). Matches the findings' #1 (#817).
- #814 (W6 shadow-run acceptance): 1. #816 (W8; reads audit log exits), 2. #717 or #820 (W12, exit-0 share SLO), 3. #531 only as a false friend (it is a different "Shadow Run Module" for reflect pipelines; unrelated). Matches the findings' #1 (#816) and #2 (#820).

## Notes (non-blocking)

- #811 and #812 both rest on "Clay-origin, R38 adopts nothing", yet one is closed (not planned) and the other kept open. The reasons differ (W3's premise is gone since cron is rewritten each boot; W4 reopens the open owner question Q3), and both say "the owner decides", so the actions are not contradictory. A reader may still want that stated in one line.
- "4689 cycle lines" (812, 814, 811) counts only full-shape cycle lines. Today the audit logs hold 4699 `kind":"cycle"` lines (10 are short-shape). Cron log `exit=` counts grew from 4382 to 4400 in the meantime. These are live numbers, so drift is expected. The non-zero breakdown (gh_timeout 3, lock_held 3, lock_missing 2, launch_unknown 2) is exact.
- 811 says "Complexity medium, size S in this repository ... M overall". The two sizes are explained but a single answer would read better.
- 814 says `slo_numbers` has "5 callers, all tests". I see 6 call sites in `tests/issue_watch/test_slo_helper.py` and none in production. The conclusion holds.
- 811, 812 and 814 each say the body contains a copy of later W items (142, 134, 108 lines). Confirmed by `gh issue view` (811: 142, 812: 134, 814: 108 lines; #823 is 25).
- 814 merges W6 into #816. The findings flag that W8 may be dropped by the owner. The fallback ("keep W6 alone, P3, simple") is stated, so the risk is covered.

## What I checked

Safety. All three findings are read-only. Every close, merge, trim or keep is a recommendation that says the owner decides. No finding asks for a push, a comment, a label, or a GitHub write. The checks they list (`crontab -l`, audit log counts, `gh issue view`) are read-only.

Order. STEP 1 was done first, then 2 and 3. One `gh` rate-limit warning arrived on my first call. `gh api rate_limit` showed 4296 of 5000 left, so I carried on with few calls.

Alignment citations, each opened and confirmed:
- 811. REQ R6 (:36), R16 (:37), R17/R18 (:43-44), R38 (:64; the tail confirms "(B) scheduler stays cron with one dispatcher, installed by the Coder image; Clay's Orca automation not adopted"). SPEC rows at :171, :196, :200, :201, :217, :218 (cron `*/5` under `flock -n`, 270 s cap, FR-10, FR-11, NFR-04, FR-82). `dispatch.py:54-55` (`LOOP_CAP_S = 270`, `CHILD_TIMEOUT_S = 255`) and `:466-470` (the "270 + 255 s, flock skips a tick" comment). `cycle.py:1464-1473` (eight keys, no interval). D02 verdict :67 ("about 525 seconds"). DEC:175 (D02 heading). `crontab -l` on this host shows `* * * * * ... flock -n ... issue-watch run-all`, under "managed: rewritten on every boot". #655 body: "Every 5 minutes (configurable)" (lines 23 and 110). #774 item 8 text confirms the 1 minute versus 5 minute conflict. #813 and #809 are closed not planned with owner-decision comments on 2026-11-24.
- 812. DES `docs/designs/issue-watcher.md:109` (C22), `:873` (Q3), `:930` (FR-028 row). `github.py:469` and `:519-524` (`RATE_LIMIT_MAX_WAIT_S = 3600`, header, reset and clamp branches). `audit.py:26` and `:52`. `record.py:31` (`SCHEMA_VERSION = 1`) and `:120-131` (key set). `dispatch.py:60`, `:243-266`, `:478-483` (`account-rate-wait.json`; plain `rate_limited` only). `cli.py:380` (`_CHILD_OK_EXITS = (0, 5, 75)`). SPEC :210 (FR-20), :212 (FR-22), :343 (NFR-05), :705 (cron shadow run, "real replies captured"). `docs/designs/issue-watcher-setup.md:336` and `:396-397`. `tests/issue_watch/fixtures/_assumed_shape/` exists.
- 814. REQ R7 (:38), R18 (:44), R28 (:54), Task 21 (:93), :106-107. `cli.py:131-135` (crash goes to stderr only), `:380`, `:392`, `:418-423`. `audit.py:57` (`cycle_crashed`, exit 1). `repos.py` `list_failed` and `unreadable_list`. `cycle.py:508-509`, `:1416-1418` ("audit is accepted ... not read"), `:1497` (`slo_numbers`, no production caller). `REASON_TABLE` in `audit.py:26-104` has 59 entries (I counted 59). SPEC :45, :213 (FR-23); DEC:1119 ("proposal, not an owner rule"). `docs/designs/issue-watcher-setup.md:223-233` (section 8.1 manual grep). `first_run.py` exists. #809 closure comment says "Merged into #716".

Host numbers: `~/.local/state/superclaude/issue-watch/*/audit.jsonl` (4 repos): 4699 cycle lines (4689 full-shape plus 10 short), mean `gh_calls` 5.08, max 15, zero lines containing `rate_limit`. Non-zero exits: 10, split as given above. Cron log `~/.aidev/logs/issue-watch.log`: `exit=0` 4393, `exit=3` 3, `exit=6` 2, `exit=7` 2, `sweep: error list_failed` 3, `list_timeout` 2, `sweep: unhealthy` 7, no `exit=75`, no `.1` file. All match the findings, allowing for live growth. The arithmetic 5.08 x 4 x 60 = about 1219 calls an hour (24% of 5000) is right and is labelled UNVERIFIED as a rate.

Standalone-or-merge reasoning: 811 (close, owner decides; not merged into #774 because docs-only versus code plus a second repo) holds. 812 (standalone from #817; different mechanism, test and risk) holds. 814 (merge into #816; the shared reader of `audit.jsonl`; premise removed by R18, R28 and the #813 closure) holds, and its fallback is stated. Priorities (P3, P3, P3), complexities (medium, medium, simple) and sizes (S/M, M, S) are consistent with the evidence.
