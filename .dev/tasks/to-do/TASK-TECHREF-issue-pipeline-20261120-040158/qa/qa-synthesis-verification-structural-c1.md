# QA Report - Synthesis Gate Verification (Structural), Cycle 1

**Topic:** IronClaude issue-to-work pipeline technical reference
**Date:** 2026-11-20
**Phase:** synthesis-gate verification (structural), fix cycle 1
**Status:** Complete (see the final `Status: Complete` line)
**fix_authorization:** false (report only)

---

## Previously BLOCKING findings (G2-1 to G2-9), each re-read in the live synth file and compared with the snapshot `/home/coder/.cache/ic-snap-20261120/master` (read only; nothing written there)

| ID | Synth location | FIXED-OK / STILL-OPEN | Evidence |
|---|---|---|---|
| G2-1 | synth-04 lines 192, 213, 315, 316, 378; synth-06 14.2 intro (line 240), D-17, D-18, D-27, D-31; (fix report also cleaned synth-01 and synth-02) | FIXED-OK | Grep `orchestrator\.md` over all six synth files: 0 hits. Replacement citations checked in the snapshot: `docs/designs/sc-issue-launch-level-hook.md:23` reads "A worker that a coordinator starts after a `--pipeline none` claim ... is not launched by the claim script, so this guard does not govern it" (supports every use); `CHANGELOG.md:17` reads "The `superclaude issue-pipeline` command group and its plan-approval flow are removed ... no longer has rule WC-17 or the 'Issue pipeline duties' section, and the launch-level guard no longer blocks those commands" (supports "records the removal"); `launch-level-guard.sh:496` comment says the rule 1 text "is retired" (supports `GD:496-497`). The "grant row" lines (synth-04 378, synth-06 D-31) now say "no decision found in the files this reference cites"; `WORKER-CONTRACT.md:57` holds the phrase once (read). The only PR 686 text is synth-01 line 44. No fact that rested on code was dropped. |
| G2-2 | synth-02 4.1 rows 11-13 and dry-run bullet (lines 127-129, 138) vs synth-03 5.1.1 | FIXED-OK | `cycle.py:1026-1112` read in full: `_launch` order is `launching=True` (1028), dry-run return (1029-1035), probe `find_orca` (1048), `build_claim_prompt` (1054), `_revalidate` (1058), day cap (1061), DISABLED (1063), cut-off (1069), origin (1074), `mark_pending` + `_save` (1091-1092), launch (1099). synth-02 row 11 lists exactly this order; row 12 is Commit, row 13 Conclude; synth-03 5.1.1 table has 11 `_launch`, 12 `_commit`, 13 `_conclude`. The two files now number the same steps the same way. Bullet reads "runs steps 1 to 10 and returns at the top of step 11 (`P/cycle.py:1029-1035`)", equal to synth-03 line 129 "steps 1-10". Grep for `L2 to L14`, `at L1`, `steps 1 to 11`, `step 12`: 0 hits (no stale label left). Rewritten row has 5 cells, matching the 5-column header. |
| G2-3 | synth-06 13.1.4, 13.1.5, 13.1.6, 13.1.7 | FIXED-OK | Skeletons now present and checked against the snapshot: 13.1.4 `choices=` at `orca_worktree.py:1873` (prompt), `:1883` (launch), `:1891` (pending adds `full-submit`); `BLOCK_MARKER` `[a-z]+` at `:743`; `render_prompt` keeps `common` + level at `:756`; level case `launch-level-guard.sh:264-269` (`worktree \| worktree$'\n') LL_LEVEL=W ;;` shape matches the skeleton); grid `:785-803` with `*) ll_deny LL-BROKEN` at 801 (a missing cell becomes LL-BROKEN, true). 13.1.5 skeleton plus the phrase "not determinable from research" for the classifier. 13.1.6 hooks.json group shape equals `hooks.json:125-134` (matcher, hooks[type, command, timeout]); `_FRESHNESS_SCRIPTS` spans `install_hooks.py:42-97` with the launch scripts at :90, :93, :96 (read). 13.1.7 frontmatter `name`, `tools` (line 5), `model` (line 6) equal `issue-worker-t3.md:1-8`; `WORKERS` entry shape `("claude-gw-<tier>", "<tier>")` equals `test_issue_worker_agents.py:21-26`; selection logic marked "not determinable from research". |
| G2-4 | synth-01 section 1 Key statistics, Watcher surface row (line 34) | FIXED-OK | Line 34 now reads "per-issue call cap 35 (32 ordinary plus 3 reserved) plus the two shared calls G1 and G2, so at most 37 `gh` calls per cycle (2 when idle)". `github.py:437-463` read: `spend` counts `self.calls` against `CALL_CAP` or `CALL_CAP - RESERVED_CALLS`; `spend_shared` "never refused"; `total = calls + shared_calls`. Equals synth-03 5.1.2 line 151, synth-05 line 264, synth-06 line 94. Grep for `per-cycle call cap`: 0 hits. |
| G2-5 | synth-01 2.1 (line 106), 2.3 rows 3 and 6 (152, 155), 2.4 row 6 (180); synth-02 4.6 level-grid row (291) | FIXED-OK | Each place now says the command word `orca` only, `orca-ide` not constrained, observed exit 0, pointer to Section 5.3 and D-25. Snapshot: `launch-level-guard.sh:457` is the only `orca)` case; grep `orca-ide` in the guard: 0 hits. Pointers resolve: synth-04 line 283 (gap paragraph) and synth-06 D-25 (line 268) exist. |
| G2-6 | synth-01 rows 10 and 18; synth-02 4.4 `pending` row; synth-04 5.2 "Any caller" row; synth-05 8.3 last row; synth-06 D-18 | FIXED-OK | All six places carry the same scheme "NOT BUILT (binding and caller); the `pending` verb itself is BUILT-ON". Grep for `BUILT-ON \(verb\)` and `BUILT-ON as a verb`: 0 hits. The synth-04 5.3 G1 rows keep "NOT BUILT (as a guard)", a different item (the guard, not the caller). |
| G2-7 | synth-04 5.2 `--pipeline` table, `worktree` row (line 111) | FIXED-OK | Cell now names `/sc:implement` or `/task`, says the template at `launch-prompt.md:23` also names `/sc:task`, tags it [CODE-CONTRADICTED] and points to 5.3 and D-23. Snapshot: `launch-prompt.md:23` contains "`/sc:implement`, `/sc:task` or `/task`"; `launch-level-guard.sh:347` is `LL_RE_APR='^[[:space:]]*/(sc:implement|task)([[:space:]]|$)'`. Every other `sc:task` hit in the synth files (synth-02 200, 347; synth-04 268, 389; synth-05 223; synth-06 229, 266) is tagged or is an open question. |
| G2-8 | synth-05 A.2 worker-test row (line 341) and 8.3 last row (88); synth-02 4.3 (198) and 4.4 (217) | FIXED-OK | Snapshot grep of `tests/` for the `pending --level` call: exactly `tests/hooks/test_launch_level_guard_worker.py:287` and `tests/skills/test_issue_orca_worktree.py:2475, 2488, 2489, 2498`. All four places now name both files (`:287` and `:2472-2498`); grep for `only test caller`, `only caller is a test`: 0 hits ("only callers are two tests" in synth-02 line 217 is the corrected wording and names both). |
| G2-9 | synth-05 Appendix A intro (line 305) | FIXED-OK | Intro now reads "none calls the real GitHub (`gh`) or Orca, and the pre-push and L2-install tests run real `git` against temporary local repositories and a local bare remote". Snapshot `test_issue_l2_install.py:3-7` ("Real git under a temporary HOME ... a bare remote and a clone") and `:72-73` (`git init --bare`, `git clone`) confirm it; the A.2 pre-push row already says real git and a bare remote. Grep `none calls a real`: 0 hits. |

Result: 9 of 9 FIXED-OK, 0 STILL-OPEN (the fix report marked none UNFIXABLE-FROM-EVIDENCE).

## New BLOCKING findings

| ID | Location | Problem | Evidence | carried-over / new | previously-rated-PASS |
|---|---|---|---|---|---|
| (none) | - | No new BLOCKING finding was found in the six synth files or in the edits made by the fix report | See "Checks performed" below; each fixed place was re-read, each new citation or skeleton was compared with the snapshot, and the structural greps returned the expected results | n/a | n/a |

## MINOR notes (not graded as blocking, not rechecked in later rounds)

- synth-06 13.1.4 skeleton comment says the level word at `GUARD:264-269` is "read from the pending record"; the guard reads `sessions/<sid>` (`launch-level-guard.sh:259-262`), which is the same inode as the pending record after the hard link. Wording only.
- synth-04 line 383 still quotes `SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:268` with the bracket "[its replacement]" in place of "the orchestrator design replaces them"; carried over from review 1 (rated MINOR there). It is not a PR 686 or rewrite-design sentence.
- synth-03 5.1.7 two Status cells use "dead or write-only" and "practically unreachable" (synth-03 was not touched by the fix cycle; carried over from review 1 as MINOR).
- synth-02 4.1 gives the commit step as `cycle.py:1116-1144` and synth-03 gives `_commit` as 1116-1126; both are true (`_commit` and `_commit_store`), range drift only.

## Checks performed

1. Every previously BLOCKING finding (G2-1 to G2-9): live synth location re-read, compared with snapshot lines (table above). 9 FIXED-OK.
2. New-problem scan on the fix edits (process step 2):
   - PR 686 and rewrite design: grep `686` over the six files finds only synth-01 line 44 (the one allowed sentence); other hits are line ranges such as `685-686` and `654-686`. Grep `orchestrator\.md`: 0 hits. Grep `rewrit`: hits are the Bash-hook word "rewrites" (synth-02 80, 193; synth-04 182, 201, 289; synth-05 54) and synth-01 line 44. Grep `PR #?68[0-9]`: only PR 682 (removal commit) and PR 686 in synth-01 line 44.
   - Placeholders: grep `TBD|TODO|FIXME|PLACEHOLDER` over the six files: 0 hits.
   - Status words: all new or changed Status cells use BUILT-ON / BUILT-OFF (enabled:false) / NOT BUILT / REMOVED with a parenthetical qualifier; no new word outside the four.
   - Table structure: the rewritten or extended rows were counted cell by cell against their headers (synth-01 ledger rows 3, 6, 10, 18 = 6 cells; 2.4 row 6 = 5; synth-02 4.1 rows 11-13 = 5, 4.4 rows = 6, 4.6 row = 5; synth-04 5.2 status row = 3, `worktree` row = 4; synth-05 8.3 = 5, A.2 = 5; synth-06 D-17, D-18, D-27, D-31 = 7). No broken header, no unescaped pipe in a new cell.
   - New citations: `sc-issue-launch-level-hook.md:23`, `CHANGELOG.md:17`, `launch-level-guard.sh:496`, `:457`, `:347`, `launch-prompt.md:23`, the two test callers, `test_issue_l2_install.py:3, 72-73`, `github.py:437-463`, `cycle.py:1026-1112`, `orca_worktree.py:743, 756, 1873, 1883, 1891`, `hooks.json:125-134`, `install_hooks.py:42-97`, `issue-worker-t3.md:1-8`, `test_issue_worker_agents.py:21-26`: all read and all say what the synth text claims.
3. 12-item synthesis checklist, spot-check depth on the five touched files (synth-01, 02, 04, 05, 06; synth-03 was not touched):
   1 headers: `## 1.`, `## 2.`, `## 3.`, `## 4.`, `## 6.`, `## 7.`, `### 5.2` to `### 5.4`, `## 8.` to `## 11.`, `## Appendix A`, `## 12.` to `## 14.`, `## Appendix B` intact. PASS.
   2 table columns: see step 2. PASS.
   3 no fabrication: every changed claim traced to a snapshot line (step 2). PASS.
   4 citations use real paths: all new paths exist (read). PASS.
   5 depth budget: form only (carried-over MINOR notes of review 1). PASS (note).
   6 extension guide actionable: 13.1.4 to 13.1.7 now carry skeletons or the words "not determinable from research" (G2-3). PASS.
   7 cross-section consistency: call cap (G2-4), step numbering (G2-2), status scheme (G2-6), `/sc:task` (G2-7), test callers (G2-8), orca-ide caveat (G2-5) agree across files by grep. PASS.
   8 no doc-only claim presented as current in Sections 2, 4, 8: the new text adds only code-backed statements or tagged ones. PASS.
   9 stale-doc discrepancies surfaced in Section 14: unchanged (KW-1 to KW-8, X-1 to X-28, D-rows); the `/sc:task` and `orca-ide` items still map to X-21/D-23 and D-25. PASS.
   10 content rules: tables over prose, no source reproduction (skeletons are short and name-level). PASS.
   11 no placeholders: grep 0 hits. PASS.
   12 no hallucinated paths: every path in the edits exists in the snapshot. PASS.
4. For new BLOCKING findings: none, so no carried-over/new or previously-rated-PASS classification is needed. All nine previously blocking items were carried over from review 1 and each is now closed; review 1 had rated none of those nine areas PASS (analyst report 1 rated partition 1 PASS only on accuracy, and its finding set did not cover G2-2, G2-4, G2-5).

Confidence: Verified: 21/21 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 33 | Grep: 16 | Glob: 1 | Bash: 0 (Read + Grep + Glob = 50, above the 21 checklist items). Web tools: not used (no external lookup needed).

Limits: no test or hook was executed; "observed exit 0" for `orca-ide` is taken from research file 05 and the unchanged synth-04 line 283, as accepted in review 1; nothing under `/home/coder/.cache/ic-snap-20261120/master` was written, no synth file was modified, and the only file written is this report.

## Verdict: PASS

BLOCKING findings: 0 (9 of 9 previous findings FIXED-OK; 0 new). MINOR notes: 4.

Status: Complete

