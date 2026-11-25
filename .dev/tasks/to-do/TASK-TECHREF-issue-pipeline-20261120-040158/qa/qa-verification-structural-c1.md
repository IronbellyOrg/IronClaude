# QA Report - Gate 3 Structural Verification, Cycle 1

**QA phase:** report-validation verification (structural), cycle 1
**Date:** 2026-11-20
**Status:** Complete
**Fix authorization:** false

Document: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md (2436 lines, read completely)
Previous BLOCKING list: /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/qa/qa-consolidated-findings.md (G3-1..G3-9)
Fix log: /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/qa/qa-fix-cycle1-report.md
Source root (read-only, nothing written there): /home/coder/.cache/ic-snap-20261120/master

---

## Previously BLOCKING findings

| ID | Location (live line) | FIXED-OK/STILL-OPEN | Evidence |
|----|----------------------|---------------------|----------|
| G3-1 | L522 (4.2 step 6), L1258-1260 (5.3), L1364 (5.4), L1377 and L1380 (Section 6), L2010 (Identifier map) | FIXED-OK | Grep of every `Q-`, `C-`, `O-`, `U-`, `D-` token in the document: no `C-36..38`, `C-64`, `O-2..O-4` remain; `Q-12`, `Q-13`, `Q-17` occur only in the Identifier map (L2010). Every replacement target exists: U-4 (L2001), U-5 (L2002), U-6 (L2003), U-7 (L2004), U-10 (L2007, lists Q-02..Q-09 and Q-18..Q-21), U-11 (L2008, Q-22..Q-24), D-13 (L1964), D-16 (L1967, contains Q-10), D-18 (L1969), D-21 (L1972), D-23 (L1974, contains Q-14), D-25 (L1976), 14.3 row at L1991 (contains Q-11). The Identifier map agrees with the gap log rows Q-10..Q-17 in gaps-and-questions.md (Q-12 = OB-H gate, Q-13 = caller of `pending`, Q-14 = `/sc:task`, Q-17 = `orca-ide`). Remaining `O-15`, `OD-1`, `OD-3`, `LIM-*` are design-document ids with a `docs/designs/sc-issue-launch-level-hook.md` citation; snapshot lines 83, 393, 534, 627 of that file contain them. |
| G3-2 | L718 (5.1.1) | FIXED-OK | Text now reads "except where marked in 5.1.8"; heading `5.1.8 Contradictions found and open questions` is at L952; the only other `5.1.9` strings are the ToC entry and the Extension points heading. |
| G3-3 | L759 (new `re-approved` paragraph), L921 (5.1.6), L1604, L1606, L1607 (10.2) | FIXED-OK | No "Section 9 / Appendix" text remains (Grep). L921 points to 5.1.1.1, 5.1.1.2, the 5.1.1 step table, 10.1, 10.2: all exist. Snapshot `cycle.py:646-661` read: `_issue_line`, `reapproved` condition 654-659, `note = "re-approved"` at 660; `audit.py:280-284` read: a reason of kind `note` is rejected as a reason and a note must be of kind `note`, so "note, not skip or stop reason" is true. 10.2 now cites `P/audit.py:26-102` and `P/cli.py:244-250` (read: `operator_reset` at 244 and 250, `reset_refused` at 248); no `research 01 section 8.2` or `8.4-8.5` text remains. Note/warning raise sites in L1606 verified: `cycle.py:660`, `:731` (dry_run_shadow_reset), `:775` (clock_skew), `:807` (discovery_count). |
| G3-4 | L2051 (15.2 check 11) | FIXED-OK | Reworded to guard twice (once per event), identity once. Matches L395, L326, 8.4 (L1490, L1494, L1495) and snapshot `hooks.json` lines 63-71, 115-124, 125-134 (read). The only other "once per event" text is Appendix A.2 L2239 (consistent). |
| G3-5 | L1838-1840 (13.1.8) | FIXED-OK | Skeleton is `RULE_PHRASES["<rule-name>"] = (None, [...])`. Snapshot `test_worker_contract.py:24` (comment "rule -> (identifier ...; phrases)"), `:25-32` (tuple shape), `:725` (`ident, phrases = RULE_PHRASES[rule]`), `:728-731` (identifier-on-line check) all read and match. |
| G3-6 | L2037-2103 (15.2) | FIXED-OK | Table has 3 columns and no command; all 18 commands are in one fenced `bash` block with `# n` comments. Check 7 is `grep -c -e 'WC-17' -e 'Issue pipeline duties'` plus `wc -l`; run read-only against the snapshot: `0` and `339`. Also ran #1, #2, #3, #5, #6, #8 (no output), #9 (count 0), #12 (identical), #13, #14 (10 paths), #15 (the `O_EXCL` lines), #16 (19), #17 (46), #18: all match the expected-result column. |
| G3-7 | L513 (4.2) | FIXED-OK | Now "NOT BUILT as code, prose rule only, D-20"; agrees with L1006 (5.2 status) and L1971 (D-20); no remaining "BUILT-ON" status for the default-level rule (Grep of "default level" lines). |
| G3-8 | L1448 (8.1 new row), L2138 (15.6) | FIXED-OK | New guard-stack row names `orca orchestration send/ask` with no `--to`, the allow-list and the ESCAPE rule; snapshot `launch-level-guard.sh:480-491` (allow-list 481-482, glob ESCAPE 484, send/ask 485, other verbs ESCAPE 489) and `:496-537` (8192 bytes 507, 64 args 511, `--to/--run/--environment/--pairing-code` 524, prefix rule 527) read and match. Pins `test_launch_level_guard_worker.py:74, 187, 213, 262` are test definitions of the stated behaviour. 15.6 first row now says the match includes this command and the allow-list. The new row has 5 cells like its table. |
| G3-9 | L1763 (13.1.1), L1843-1857 (Symbols table) | FIXED-OK | Both `test_df42_*` tests attributed to `T/test_record.py:1518, 1522` (read: both defs there, bodies check `REASONS`). All 13 symbols of the finding appear with file:line and each matches the snapshot: `_cond` 587-588, `_stopped` 590-592, `_issue_arg` 111, `_page_arg` 118, `_cursor_args` 141, `_trigger_arg` 150, `_login_arg` 168, `render_prompt` 746-761, `ll_deny` 135-139, `_FRESHNESS_SCRIPTS` 42-97, `test_tier_ids_appear_only_in_allowed_paths` `test_model_alias_policy.py:104`, `_check_never_as_worker` `:734` and its test `:881-882`. Pins `test_github.py:2077/2107/2132` are the three `pytest.raises(... match=...)` lines. |

## New BLOCKING findings

| ID | Location | Problem | Evidence | carried-over/new | previously-rated-PASS yes/no |
|----|----------|---------|----------|------------------|------------------------------|
| (none) | - | No new BLOCKING defect found in the edited regions or elsewhere in the structure | see Checks performed | - | - |

## MINOR notes (not rechecked later, no fix pass)

- M-1: Symbols table row for `render_prompt` (L1853) names `tests/skills/test_issue_protocol.py:295` as where it is pinned. That test (`test_st8_launch_prompt_has_exactly_the_four_blocks`, read) pins the template's four blocks, not `render_prompt`; no test file names `render_prompt` (Grep over `tests/`: 0 hits). Rendering is exercised only through the `prompt` verb in `test_issue_orca_worktree.py`. The same pointer already stood in 13.1.4. True for the template, imprecise for the function.
- M-2: 2.3 intro sentence (L319) lists "rows 1b, 7b and 9 to 18" as the additional rows but row 12b also exists. Not touched by the fix pass.
- M-3: Research-file gap-fill tags such as `F-1`, `F-2`, `B-1`, `B-3` in the Research-file column of 14.1.2 (L1902-1903, L1938) and L1712 name rows of research files listed in 15.4, not ids of this document. Not touched by the fix pass.

## Checks performed

1. Read the whole document (L1-2436) and the previous BLOCKING list, the fix log and the gap log rows Q-02..Q-24.
2. Structure: Grep of all headings: 16 numbered sections in template order (1 Overview .. 16 Glossary), Appendix A, Appendix B and Document History present, compared with the template's `## ` headings (Grep of the template). Every ToC entry maps to an existing heading (anchors for the `&` headings are `8-api--integration-points`, `9-configuration--environment`, `10-error-handling--edge-cases`, `14-known-limitations--technical-debt`, `15-verification--accuracy`, `12-conventions--patterns`, plus both appendices). No heading added, removed or renamed by the fix pass.
3. Placeholder scan (TBD, TODO, FIXME, XXX, lorem, fill): no match.
4. PR 686: Grep for `686`, "rewrite design", `docs/designs/orchestrator`: exactly one sentence (L218, "PR 686 and the rewrite design are out of scope for this reference."); every other `686` hit is a line range such as `685-686` or `654-686`, `669-686`. No mention of the rewrite design document.
5. Appendix A row count: counted A.1 = 21 (conftest, 19 test modules, fixtures dir), A.2 = 11, A.3 = 9, A.4 = 7; total 48, equals the closing statement (L2275); the 44 + 4 split also adds up (20 + 1 + 9 + 7 + 1 + 2 + 3 + 1 = 44; 2 hooks + 2 skills added).
6. Tables: new 8.1 row has 5 cells; Symbols table has 4 cells per row; 15.2 table has 3 cells per row; the escaped pipes inside code spans in checks 10 and 15 do not add cells.
7. Cross-references: no dangling `Q-`, `C-`, `O-2..4` id; all `U-`, `D-`, `KW-`, `X-` ids used exist as rows; section pointers 5.1.1.1, 5.1.1.2, 5.1.8, 10.1, 10.2, 14.2.1, 14.3.1, 15.4, Appendix A.1/A.3 exist.
8. Counts after the edits: 59 reason words (27 + 17 + 9 + 1 + 4 + 1) consistent in 5.1.6, 10.2, 12.1, 16; 19 fixtures (command run: 19); 46 audit tests (run: 46); 10 removed files (git ls-tree: 10); 339-line contract (wc: 339).
9. Citations re-read in the snapshot (more than 15 groups): `cycle.py` 587-592, 646-661, 722-737, 770-775, 803-808; `audit.py` 270-289; `cli.py` 238-253; `github.py` 108-177; `orca_worktree.py` 738-766; `launch-level-guard.sh` 130-140 and 454-540; `hooks.json` 60-135; `install_hooks.py` 38-99; `launch.py` 82-117; `test_record.py` 1500-1534; `test_model_alias_policy.py` 98-121; `test_worker_contract.py` 20-36, 720-750, 874-884; `test_github.py` 2077/2107/2132; `test_launch_level_guard_worker.py` test definitions; `test_issue_protocol.py` 285-310. All 18 spot-check commands of 15.2 were run read-only against the snapshot or with read-only git; all results match the expected-result column. Nothing was written under the snapshot.
10. Self-audit: I looked for new errors in every edited location (4.2, 5.1.1, 5.1.1.1, 5.1.6, 5.3/5.4, 6, 8.1, 10.2, 13.1.1, 13.1.8, Symbols table, 14.3.1, 15.2, 15.6); the only imprecision found is M-1 (minor).

Confidence: Verified: 9/9 previously BLOCKING items and 6/6 structural items | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 27 | Grep: 9 | Glob: 1 | Bash: 6 (all read-only; git show / ls-tree read-only)

## Verdict: PASS

Previously BLOCKING findings fixed: 9 of 9. New BLOCKING findings: 0.

Status: Complete

