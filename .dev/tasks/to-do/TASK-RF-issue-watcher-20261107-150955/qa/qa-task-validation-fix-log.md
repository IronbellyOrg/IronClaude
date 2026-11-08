# QA Fix Log - Task Integrity (task file TASK-RF-issue-watcher-20261107-150955)

**Date:** 2026-11-08
**Phase:** task-integrity, fix cycle 1 (fix_authorization: true)
**Input:** `qa/qa-task-validation-consolidated.md` (15 blocking findings B-01..B-15, 38 minor notes N-01..N-38)
**Method:** targeted `Edit` calls only on the task file (no rewrite, no script); the file was backed up to `/tmp/task-before-fixes.md` before the first edit and compared at the end (229 changed lines in a diff, frontmatter lines 1-64 identical).
**Result:** item count 176 -> 209 (+4 from the two splits, +30 conditional cycle-2 gate items, -1 for the folded Step 10.8); gate lens agents still 6+6+6+6+7+3 = 34; no nested checkbox, no TBD/TODO/FIXME; POST reflect (10.6) penultimate and Done (10.7) last in P10.

## Blocking findings

| id | what changed | where (step ids) |
|---|---|---|
| B-01 | `OPERATION_ID_PATHS` holds the success path and the error path; for every `unknown` outcome the id is looked up in the JSON object parsed from stdout, then from stderr; plain text never yields an id (`operation_id` None, no retry command in `status`); `orca_launch_unknown.json` now carries JSON text in `stderr` with the id at the error path; Step 5.5 asserts the fixture id plus the negative plain-text case; new Open Question OQ-47 (the design says only "from the error", D 636) | 5.1, 5.2, 5.5, Open Questions D |
| B-02 | `PendingContext` defined (six fields: `approver_id`, `approval_event_id`, `approved_at`, `launch_cwd`, `launch_login`, `launch_account_id`; neither design nor spec defines the type, so derived from D 426-433 and T-4 at D 481); `mark_pending` effect spelled out (`consumed_at` and `pending_at` = `now`, `launches` 1); Step 6.2 lists the fields where it builds the context; new OQ-48 | 4.1a, 4.1c, 6.2, Open Questions D |
| B-03 | In all six gates the cycle-2 clause of the decision item now writes `CYCLE2=run` plus `F_n=<n>` to `phase-outputs/plans/<gate>-cycle-decision.md` (or `CYCLE2=not-needed` on PASS, with the post-fix re-run now including `make lint`) and hands over to five new compact conditional items per gate with full embedded prompts and `-cycle2` file names: consolidate, fix agent, structural verifier, content verifier, and a decision item that applies the guards in order (regression message, `[HALT-MONOTONICITY] \|F\|=<n>`, 2-cycle hard cap with escalation, no third cycle); the M4 variant keeps the NEEDS OWNER DECISION halt. Gate intros say the gate now has 17 items (Final 18, M4 13) | 3.G12-3.G17, 5.G12-5.G17, 7.G12-7.G17, 8.G12-8.G17, 9.F13-9.F18, 9.M8-9.M13 |
| B-04 | Corrected the false claim: the original `_find_orca` skips a top-level JSON list (the `AttributeError` is caught at `install_user_setup.py:216-217`); `find_orca` mirrors that; the parity test asserts equal results for that shape and only the "rejects without raising" check for the shapes where the original raises (`topics` null, int, str, dict, non-dict element) | 5.1, 5.6 |
| B-05 | Step 3.1 split into 3.1a (constants, jq and GraphQL text, argv builders), 3.1b (classification, rate-limit time, call budget), 3.1c (typed reads and paging); Step 4.1 split into 4.1a (errors, dataclasses, validation, migration), 4.1b (`Store`, `FileStore`, lock), 4.1c (transitions, sweep, day cap, `init_state`, dry-run helpers); each part has its own evidence-absence comment and a Grep import check; TB-Add-5 single-item justification comments added to 2.2, 2.3 and 5.1; Phase 3 and Phase 4 intros describe the split | 2.2, 2.3, 3.1a-c, 4.1a-c, 5.1, Phase 3/4 intros |
| B-06 | The unsatisfiable "no argv contains title, body" replaced by the design rule "no argv requests `title` or `body` as an output field" with the `MARKER_JQ` exception spelled out | 3.6, 3.1a |
| B-07 | Staging of `.dev/tasks` folded into Step 10.7 as its final action (both branches, never reverts Done); Step 10.8 deleted; Task Overview now says the POST reflect is followed only by the Done item and gives the new total 209; Reflect Depth Derivation records 176 -> 209 | 10.7, deleted 10.8, Task Overview, Reflect Depth Derivation |
| B-08 | `cycle.py` reaches the Orca names as `launch._ORCA_CLIS`; the Read list marks `install_user_setup.py:35` as background only; `launch_cwd` identified as the stored entry field | 6.3 |
| B-09 | False claim removed: `test_retired_docs_absent.py` covers the runbook's links, `test_model_alias_policy.py` scans only `src/superclaude` (SRC/TIER_TEXT_DIRS at lines 23 and 48), the runbook's model-alias check is the grep of Step 9.3 | 9.5 |
| B-10 | Step 5.8 now has ONE non-parametrized test looping over the marker copies that exist (src copies required, project `.claude/` and `~/.claude` copies compared only when present, no skip); Step 8.2 loses its conditional skip (a deny-listed `tmp_path` fails an assertion with an explicit message instead); the Phase 2 and Phase 8 headers forbid `pytest.skip`, `skipif` and `xfail`; the existing "zero skipped" statements in 8.9, 8.10, 9.4, 9.6 and the gate prompts are now satisfiable and unchanged | 5.8, 8.2, Phase 2/8 headers |
| B-11 | Chosen option: one explicit re-run list. After any fix in 9.17 or 9.18, Steps 9.4 to 9.16 (G-1..G-11; 9.3 first when the runbook changed) are re-run and the `p9-*` files overwritten; 9.19 states it records only results that postdate the fixes | 9.17, 9.18, 9.19 |
| B-12 | OQ references: 10.2 (full wording), 10.3 and 10.4 cite OQ-7 and OQ-35 with the skip-if-withdrawn rule; 10.7 Done condition says OQ-7/OQ-35 are not blocking unless the commit was withdrawn; 6.2 cites OQ-36 and OQ-39; 2.2 cites OQ-37 and OQ-38; 5.1 cites OQ-40 and OQ-47; Open Questions D heading and both M4 exemption sentences name OQ-36 (departs from S 103), OQ-41a (departs from D 614), OQ-47 and OQ-48 | 2.2, 5.1, 6.2, 9.M1, 9.M2, 10.2, 10.3, 10.4, 10.7, Open Questions D |
| B-13 | A REST page longer than 100 now gives `events_unreadable` (events) / `marker_unreadable` (marker) per DF-19; `events_incomplete` only for the sixth page and a repeated id; Step 3.7 asserts both reasons for the 99/100/101, repeated-id and page-cap cases | 3.1c, 3.7 |
| B-14 | `exit_for(reason)` added to Step 6.1 (reads `audit.REASON_TABLE[reason][1]`; every exit condition in `run_cycle` is `exit_for(...)`); Step 6.2 uses it; Step 6.6 gets the table-driven test `test_exit_and_kind_follow_reason_table` (exit and line kind against the table) | 6.1, 6.2, 6.6 |
| B-15 | Naming rule (ids AC-nn / FR-nnn / NFR-nnn in test names or first docstring line) added to the Phase 2 and Phase 8 headers; Step 9.17 reads the FR/NFR rows of design section 18, greps by id, adds the Ids column and a second table for FR-001..FR-029 and NFR-001..NFR-014 (NFR-012 gate-only) | Phase 2/8 headers, 9.17 |

## Minor notes applied (one-line fixes)

| id | change |
|---|---|
| N-01 | 1.6 cites design line 751 (section 11) only |
| N-02 | 1.2 verifies directories with `ls -d`, not Glob |
| N-03 | 3.G2 prompt re-runs `make lint` |
| N-14 | 8.2 cites the `__main__` guard by position (564 before Step 7.3, about 568 after) and marks `-m superclaude.cli.main` as test internals |
| N-15 | 9.F1 says "four verdict files"; 10.5 says "six gate verdicts" |
| N-16 | Phase 8 intro reads `gate-c-verdict.md` before Step 8.1 |
| N-17 | 6.1 constants wording ("listed here", `THRESHOLDS` must not be bound); 6.3 names the entry field `launch_cwd` |
| N-18 | 9.1 and 9.3 read `.markdownlint.json` and check blank lines around headings, fences and lists, double blank lines and the first heading |
| N-19 | 6.7 cites the DF-50 row instead of research/05 lines; 10.4 reads BASE from `base-sha.txt` (9.17 rewritten by B-11/B-15) |
| N-24 | 7.7 states that its run also serves as the Phase 7 G-1 record |
| N-26 | The cycle-1 post-fix re-run in 3.G12, 5.G12 and 8.G12 (and the new cycle-2 decision items) include `make lint` |
| N-36 | OQ-36 and OQ-41a named as authorized readings in Open Questions D and in the M4 exemption sentences (the count of 29 DEVIATION rows is unchanged) |
| extra | 5.G1, 7.G1 and 8.G1 also read the earlier gates' `-cycle2` fix reports; 9.M intro adds a Final-verdict pre-check |

All other minor notes (N-04..N-13, N-20..N-23, N-25, N-27..N-35, N-37, N-38) are left as notes in `qa/qa-task-validation-consolidated.md`.

## Findings not fixed

None of the 15 blocking findings is open. Judgment calls the coordinator may want to review:

- B-10 (Step 8.2): the conditional skip of research/05 T-C was replaced by a failing precondition instead of an exemption in G-1/G-3; this departs from research/05 but not from any DF row, and avoids touching six gate prompts. A host whose `tmp_path` is on a network filesystem now fails the e2e test instead of skipping it.
- B-11: the "single explicit re-run list" option was chosen over moving 9.17/9.18 ahead of 9.4, because it keeps all step numbers stable.
- B-03: cycle-2 prompts reuse the cycle-1 prompt text with `-cycle2` names, an added "do not undo cycle 1" sentence for the fix agent and an added regression clause for the verifiers; a `CYCLE2=run|not-needed` decision file (`phase-outputs/plans/<gate>-cycle-decision.md`) is the only new artifact name.
- The task folder changes are unstaged working-tree edits on top of the already staged files; `git add .dev/tasks` was not run by this agent.
