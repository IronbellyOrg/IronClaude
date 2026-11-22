# Gate 3 fix log, cycle 1

**Date:** 2026-11-20
**Status:** Complete
**Document:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md
**Work list:** /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/qa/qa-consolidated-findings.md (G3-1 to G3-9)

## Entries

Line numbers are those of the document after the edits (the finding line numbers shifted by up to about +85 lines).

### G3-1 (dangling Q-12, Q-13, Q-17, C-36..C-38, C-64, O-2..O-4)
- Section 4.2 step 6 (L522): `open item O-2` replaced by `open question Q-02 in U-10, Section 14.3.1`.
- Section 5.3 orca-ide paragraph (L1258): `(Q-17, see Section 14)` replaced by `(D-25, Section 14.2.1)`.
- Section 5.4 open items (L1362): Q-12/Q-13/Q-14/Q-11/Q-17 and C-36 to C-38, C-64 replaced by existing rows: U-4 and D-21; U-6 and D-18; D-23; D-18; D-25; U-5 and U-7. The statement "all listed in Section 14" is now true.
- Section 6 (L1375, L1378 area): `open item O-3` replaced by `open question Q-08 in U-10, Section 14.3.1`; `open item O-4` replaced by `open question Q-06 in U-10, Section 14.3.1; D-13`.
- 14.3.1 (after U-11, L2010): added one `Identifier map` paragraph (no new heading, ToC unchanged) mapping Q-10, Q-11, Q-12, Q-13, Q-14, Q-17 to D-/U- rows, Q-02..Q-09 and Q-18..Q-21 to U-10, Q-22..Q-24 to U-11.
- Evidence: gaps-and-questions.md rows C-36..C-38, C-64, Q-10..Q-17; synth-02-directory-dataflow.md:340-342 (O-2..O-4).

### G3-2 (5.1.9 pointer)
- Section 5.1.1 L718: `except where marked in 5.1.9` changed to `5.1.8` (5.1.8 holds the contradictions).

### G3-3 (dangling per-word raise-site pointer, external citation, `re-approved`)
- 5.1.6 L919: sentence "Full per-word raise sites are in Section 9 / Appendix." replaced by pointers to 5.1.1.1, 5.1.1.2, the 5.1.1 step table, 10.1 and 10.2, and a statement that `re-approved` is set in `_issue_line`.
- 5.1.1.1 (new paragraph after the gate table, L759): `re-approved` raise site `_issue_line` cycle.py:646-661 (note set at 660; condition 654-659); a note word, not a skip or stop reason (`audit.py:280-284`).
- 10.2 skip-kind and total rows: external `research 01 section 8.2` and `8.4-8.5` citations replaced by `P/audit.py:26-102` (plus raise sites in 5.1.1.1; `P/cli.py:244-250`).
- Evidence: snapshot cycle.py:646-661, audit.py:274-285 (read).

### G3-4 (guard registered once vs twice)
- 15.2 row 11 claim reworded to "The guard hook is registered twice (once per event) and the identity hook once (Sections 5.3, 8.4)".

### G3-5 (RULE_PHRASES skeleton)
- 13.1.8 (L1838): skeleton is now `RULE_PHRASES["<rule-name>"] = (None, [...])`; new bullet explains the 2-tuple (identifier-or-None, phrases) with `test_worker_contract.py:24, 25-32, 725, 728-731`.

### G3-6 (pipes inside table cells)
- 15.2: table now has columns `#`, claim, expected result; all 18 commands moved into one fenced `bash` block with `# n` comments; check 7 rewritten as `grep -c -e 'WC-17' -e 'Issue pipeline duties' ...` plus a separate `wc -l`; intro sentences adjusted. Ran #7 (0 and 339), #16 (19) and #15 (the O_EXCL lines) read-only against the snapshot and git: results match.

### G3-7 (default --pipeline level status word)
- 4.2 (L513): `(BUILT-ON as text only)` changed to `(NOT BUILT as code, prose rule only, D-20)`.

### G3-8 (G2 rule 2 missing from Section 8)
- 8.1 guard-stack table (L1448): new row for the worker `orca orchestration send` / `ask` rule and the `orca` allow-list, with `HK/launch-level-guard.sh:480-491, 485, 496-537` and the four pin tests; status: rule BUILT-ON, binding of coordinator-started workers D-18.
- 15.6 first row (L2138): added that the match includes this command and allow-list.
- Evidence: snapshot launch-level-guard.sh:455-537 (read).

### G3-9 (Section 13 symbols missing from Section 5 / Appendix A)
- 13.1.1 pin sentence: the `df42_` tests are now attributed to `T/test_record.py:1518, 1522` (not `T/test_audit.py`).
- New table `Symbols used in 13.1` (after 13.1.8, before 13.2; no new heading): `_cond`, `_stopped`, the two df42 tests, `_issue_arg`, `_page_arg`, `_cursor_args`, `_trigger_arg`, `_login_arg`, `render_prompt`, `ll_deny`, `_FRESHNESS_SCRIPTS`, `test_tier_ids_appear_only_in_allowed_paths`, `_check_never_as_worker`, each with file:line, role and where pinned (only pins found by grep are named; "no test names them" where none exists).
- Evidence: snapshot cycle.py:587-592, github.py:111-172, orca_worktree.py:746-761, launch-level-guard.sh:135-139, install_hooks.py:42, test_record.py:1518-1522, test_model_alias_policy.py:104, test_worker_contract.py:734 and :881-882; test_github.py:2077, 2107, 2132.

## Checks after the edits
- Exactly one sentence about PR 686 and the rewrite design remains (Section 1, L218); no other mention; `docs/designs/orchestrator.md` not cited.
- No heading added, removed or renamed; Table of Contents unchanged.
- Remaining `Q-12`, `Q-13`, `Q-17` occurrences are only in the new Identifier map.
- Nothing written under the snapshot; no file other than the document and this log edited.

Status: Complete
