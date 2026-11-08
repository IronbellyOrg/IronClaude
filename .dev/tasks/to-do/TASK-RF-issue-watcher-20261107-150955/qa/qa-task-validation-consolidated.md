# QA Consolidated Findings - Task Integrity (task file TASK-RF-issue-watcher-20261107-150955)

**Date:** 2026-11-08
**Phase:** task-integrity, consolidation of the four validation reports (fix cycle 1)
**Sources:**

- P1: `qa-task-validation-b2-report-part1.md` (b2-self-containment, Phases 1-5): IMP-1..IMP-6, MIN-1..MIN-13
- P2: `qa-task-validation-b2-report-part2.md` (b2-self-containment, Phases 6-10): Issues 1-4 IMPORTANT, 5-14 MINOR
- ST: `qa-task-validation-structure-report.md` (phase-structure): I-1..I-3 IMPORTANT, M-5..M-17 MINOR
- AL: `qa-task-research-alignment-report.md` (task-research-alignment): I-1..I-3 IMPORTANT, m-1..m-13 MINOR

Every finding appears once. A finding raised by several reports carries all source ids. Checks that a reviewer marked FAIL are covered by the blocking findings below (P1 checks 2, 3, 6, 7; P2 checks 2, 3, 8, 10; ST checks 11, 18; AL none beyond its three issues). Count line: blocking: 15, minor: 38 grouped notes (the reviewers listed 49 minor findings in total; duplicates across reports and findings folded into a blocking fix are merged here; the one-line ones the coordinator listed were applied, the rest stay as notes).

## Blocking findings

| id | source ids | severity | blocking | items affected | fix |
|---|---|---|---|---|---|
| B-01 | P1 IMP-1 | IMPORTANT | yes | 5.1, 5.2, 5.5 | Define the operation-id source for an `unknown` reply: look the id up through `OPERATION_ID_PATHS` in the JSON object parsed from stdout, then in the JSON object parsed from stderr; plain text never yields an id (`operation_id` None, `status` prints no retry command); design 8.4 (D 636, 687-689) only says the id comes "from the error", so record the rule as new Open Question OQ-47; Step 5.2 builds the unknown fixture as JSON text in `stderr`; Step 5.5 asserts the negative plain-text case |
| B-02 | P1 IMP-2 | IMPORTANT | yes | 4.1 (now 4.1a), P6 cycle item 6.2 | Define `PendingContext` (frozen dataclass: `approver_id`, `approval_event_id`, `approved_at`, `launch_cwd`, `launch_login`, `launch_account_id`) derived from D 417-437 and T-4 (D 481); list the fields in Step 6.2 where `mark_pending` is called; record as new Open Question OQ-48 (the design has no list) |
| B-03 | P1 IMP-3, P2 Issue 2, ST (gate prose) | IMPORTANT | yes | 3.G12, 5.G12, 7.G12, 8.G12, 9.F13, 9.M8 | Replace "perform Steps X again" by explicit cycle-2 items per gate (consolidate-cycle2, fix agent cycle 2, two verifiers cycle 2, decision) with full prompts, `-cycle2` file names, regression check first, then `[HALT-MONOTONICITY] \|F\|=<n>`, then the 2-cycle hard cap (HALT and escalate, no third cycle); each cycle-2 item is a compact conditional item ("run only if the cycle-1 decision selected cycle 2"); new steps 3.G13-3.G17, 5.G13-5.G17, 7.G13-7.G17, 8.G13-8.G17, 9.F14-9.F18, 9.M9-9.M13 (30 items) |
| B-04 | P1 IMP-4 | IMPORTANT | yes | 5.6, 5.1 | Correct the false claim: `install_user_setup.py:216-217` catches a top-level JSON list (`AttributeError` inside the `try`) and skips the candidate; the new `find_orca` mirrors that; the parity test also covers the top-level list; the original raises only for `topics` null, int, str, dict and a non-dict element (line 219 outside the `try`) |
| B-05 | P1 IMP-5, ST M-13 | IMPORTANT | yes | 2.2, 2.3, 3.1, 4.1, 5.1 (6.2, 6.7 noted) | Split Step 3.1 into 3.1a/3.1b/3.1c and Step 4.1 into 4.1a/4.1b/4.1c (other numbers stay stable); add a TB-Add-5 single-item justification comment to Steps 2.2, 2.3 and 5.1; update the phase intros and counts |
| B-06 | P1 IMP-6 | IMPORTANT | yes | 3.6 | Replace "no argv contains `title`, `body`" by the design rule "no argv requests `title` or `body` as an output field" (the G4 `--jq` value `MARKER_JQ` legitimately contains `.body`); adjust the test text |
| B-07 | P2 Issue 1, ST M-5 | IMPORTANT | yes | 10.6, 10.7, 10.8, Task Overview, Key Objective 6, Reflect Depth Derivation | Fold the staging of Step 10.8 into Step 10.7 as its final action, delete Step 10.8; POST reflect (10.6) stays penultimate and the Done item (10.7) last; item count 176 becomes 175 before the other changes |
| B-08 | P2 Issue 3, ST M-12 | IMPORTANT | yes | 6.3 | Use `launch._ORCA_CLIS` (not an import from `install_user_setup`) so `cycle.py` keeps the design line 241 import rule and Step 8.8 passes |
| B-09 | P2 Issue 4 | IMPORTANT | yes | 9.5 | Remove the false claim that `tests/skills/test_model_alias_policy.py` scans the runbook; the only model-alias check on the runbook is the grep of Step 9.3 |
| B-10 | ST I-1, AL m-12 | IMPORTANT | yes | 5.8, 8.2 (8.9, 8.10, 9.4, 9.6 and the gate prompts become consistent) | Replace the two conditional skip parametrizations of Step 5.8 by ONE non-skipping loop over the marker copies that exist (src copies required; project `.claude/` and `~/.claude` copies compared only when present); remove the conditional skip of Step 8.2 so the "no SKIP / zero skipped" rule of G-1/G-3 and the gate prompts can be met |
| B-11 | ST I-2 | IMPORTANT | yes | 9.17, 9.18, 9.19 | After any post-gate fix in 9.17 or 9.18, re-run Steps 9.4 to 9.16 (G-1 to G-11, and 9.3 first when the runbook changed) in one explicit list, overwriting the p9 result files; 9.19 records only the results that postdate the fixes |
| B-12 | ST I-3, AL m-11 | IMPORTANT | yes | 10.2, 10.3, 10.4, 10.7, 6.2, 2.2, 5.1, Open Questions D | Add Open Question references: 10.2 to 10.4 cite OQ-7 and OQ-35 (commit authority inferred), 10.7 Done condition says when they block; 6.2 cites OQ-36 and OQ-39; 2.2 cites OQ-37 and OQ-38; 5.1 cites OQ-40; the M4 exemption sentence names OQ-36 and OQ-41a |
| B-13 | AL I-1 | IMPORTANT | yes | 3.1 (3.1c), 3.7 | A REST page longer than 100 gives `events_unreadable` (events) / `marker_unreadable` (marker) per DF-19, not `events_incomplete`; Step 3.7 names both reasons for the 100/101 cases and the sixth-page/repeated-id case |
| B-14 | AL I-2 | IMPORTANT | yes | 6.1, 6.6 | Add `exit_for(reason)` (table read of `audit.REASON_TABLE`) to Step 6.1 and a table-driven exit-and-kind test to Step 6.6 (DF-41) |
| B-15 | AL I-3 | IMPORTANT | yes | Phase 2 and Phase 8 headers, 9.17 | Add the naming rule (test names or docstrings carry the AC-nn / FR-nnn / NFR-nnn ids they assert) to the Phase 2 and Phase 8 headers; add an Ids column and an FR/NFR table to the AC trace item |

## Minor findings (notes; never rechecked)

Disposition: "applied" = a one-line fix was made in this round because it was on the coordinator's list or sits in an item edited anyway; "note" = left as a note.

| id | source ids | items | issue (short) | disposition |
|---|---|---|---|---|
| N-01 | P1 MIN-1, ST none, AL m-1 | 1.6 | Cites design "line 11"; the quoted text is at line 751 (line 11 is a heading) | applied |
| N-02 | P1 MIN-2 | 1.2 | Verification uses Glob, which lists files not empty directories | applied (`ls -d`) |
| N-03 | P1 MIN-3 | 3.G2 | Gate A command prompt omits `make lint` but compares `p3-g4` | applied |
| N-04 | P1 MIN-4 | 2.8 | 57-name table pinned "from Step 2.3" by reference | note |
| N-05 | P1 MIN-5 | 2.2, 4.1, 5.1 | OQ index not cited (TB-Add-3) | applied through B-12 for 2.2, 5.1, 6.2, 10.x; 4.1 note |
| N-06 | P1 MIN-6 | 3.4, 3.1 | `pageInfo` placeholder and elided signatures | note |
| N-07 | P1 MIN-7, ST M-14 | 2.10, 3.8, 4.6, 5.9, 6.10, 8.9 | "re-run until PASSED" has no iteration bound | note |
| N-08 | P1 MIN-8 | 1.1 | No verification clause or blocker clause | note |
| N-09 | P1 MIN-9 | 3.9, 5.10 | "ensuring exit 0" vs untouched-file finding | note |
| N-10 | P1 MIN-10 | 2.3 | `ts=None`, `host=None` meaning undefined | note |
| N-11 | P1 MIN-11 | 2.5 | "well under 5 seconds" not measurable | note |
| N-12 | P1 MIN-12 | 4.1 | Predicates import vs D 239 "types only" not recorded as departure | note |
| N-13 | P1 MIN-13, ST M-15 | all creation items | Verification fields are "ensuring" prose, no `Verify:` prefix | note |
| N-14 | P2 Issue 5 | 8.2 | `main.py:564-565` citation stale after Step 7.3 | applied |
| N-15 | P2 Issue 6, ST M-6 | 9.F1, 10.5 | Count slips: "five verdict files" (four), "five gate verdicts" (six) | applied |
| N-16 | P2 Issue 7, ST M-8 | Phase 8 intro | No gate-c verdict pre-check | applied |
| N-17 | P2 Issue 8 | 6.1, 6.3 | "named exactly in design section 14" / `LIMITS`-style wording; `launch_cwd` not identified as the Entry field | applied (items edited anyway) |
| N-18 | P2 Issue 9 | 9.1, 9.3 | markdownlint rules live in `.markdownlint.json`, not `.pre-commit-config.yaml:74-88` | applied |
| N-19 | P2 Issue 10 | 6.7, 9.17, 10.4 | research X1 id cited; "re-running Step 9.4"; `<BASE SHA>` without pointer | applied (6.7 cites the DF-50 row, 9.17 rewritten by B-11/B-15, 10.4 reads BASE from `base-sha.txt`) |
| N-20 | P2 Issue 11 | 6.2, 6.7 | Very large single items | note (see B-05 for the split of other files; 6.2 stays one item, run_cycle shares local state) |
| N-21 | P2 Issue 12 | 6.11, 7.9, 8.12, 9.8 | Gate-run items without evidence-absence comment (TB-Add-8) | note |
| N-22 | P2 Issue 13 | 10.6 | Missing sentence on illegal `merge_method`; no `git status` after the POST run | note |
| N-23 | P2 Issue 14, ST M-17, AL m-7 | Execution Context | TB-Add-7 consumer spot check hits the verbatim GOAL line | note (tolerated, GOAL must be verbatim) |
| N-24 | ST M-7 | Phase 7 | No G-1 record at P7 | applied (sentence in 7.7) |
| N-25 | ST M-9 | Gate A / C placement | OQ-34 does not record the two-phase placement | note |
| N-26 | ST M-10 | 3.G12, 5.G12, 8.G12 | Post-fix re-run omits `make lint` | applied (rewritten gate items include `make lint`) |
| N-27 | ST M-11, AL m-2 | 1.3 | Baseline not written to the Task Log | note |
| N-28 | ST M-16 | 9.4, 9.5 | `tests/issue_watch/` runs twice | note (required by Table 1.2) |
| N-29 | AL m-3 | 5.2 | Orca fixtures created in P5, research/06 P3 row says P3 | note |
| N-30 | AL m-4 | 7.5 | DF-57 branches untested: reset with invalid config, Click parse error | note |
| N-31 | AL m-5 | 6.7 | AC-9 first half: no case for "no automatic retry of an unknown entry" | note |
| N-32 | AL m-6 | 2.3 | `clock_skew_s` optional vs design 10.1 | note |
| N-33 | AL m-8 | 6.3 | SLO (c) denominator is a builder rule | note |
| N-34 | AL m-9 | 3.1, 3.7, 8.2, 10.3 | r3 minors not folded (G5 null author, `-m superclaude.cli.main` note, `--cached`) | note |
| N-35 | AL m-10 | 6.6 | `test_shared_failure_matrix` not named | note |
| N-36 | AL m-11 | Open Questions D | OQ-36 and OQ-41a are departures outside the 29 | applied through B-12 (named in the M4 exemption sentence and in section D) |
| N-37 | AL m-13 | 8.5 | Foreign-owner lock only at record level | note |
| N-38 | AL m-12 | 8.2 | Only conditional skip in the suite | covered by B-10 |
