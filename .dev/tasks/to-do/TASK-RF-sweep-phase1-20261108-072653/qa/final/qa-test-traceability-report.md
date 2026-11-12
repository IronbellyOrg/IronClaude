# QA Report - Test-traceability lens (final gate)

**Date:** 2026-11-12
**Phase:** final gate, test-traceability lens (fix_authorization: false)
**Reviewer:** rf-qa (T317)

## Summary

Result: FAIL with 1 blocking finding (T317-F1, MAJOR) and 3 minor notes (T317-F2 to T317-F4). The final `Verdict:` and `Blocking count:` lines are at the end of this file.

What was traced: all 33 test names in DESIGN section 11, every row of the DESIGN section 12 trace (FR-001 to FR-026, NFR-001 to NFR-015, G-1, the SPEC section 11 and section 7 rows), the three new/edited test families, the scoped addendum cases and the seven canonical-style obligations. 32 of the 33 names resolve (29 in `tests/sweep/`, 3 in `tests/skills/` and `tests/core/`; the 33rd is the OLD name `test_never_as_worker_list_names_all_seven_commands`, which DESIGN section 8 renames, so its absence is correct).

What was run (read-only, from the repository; no live Orca, ccsession or Claude command):

- `uv run pytest tests/sweep tests/commands/test_sweep_command.py tests/commands/test_routing_plugin_parity.py tests/skills/test_worker_contract.py tests/core/test_how_we_work_routing_table.py tests/recommend/test_routing_refresh.py tests/skills/test_review_severity_rule.py tests/skills/test_implement_severity_static.py -q -rs`: 1858 passed, 0 skipped (no `SKIPPED` line, so the real-git test and `test_binding_4` ran).
- `uv run pytest tests/sweep -q`: 573 passed. `tests/commands/test_sweep_command.py`: 121 passed. `tests/commands tests/recommend` plus the two severity modules: 729 passed.
- `uv run ruff check` and `ruff format --check` over the sweep source, `tests/sweep` and the 4 touched test files: clean (19 files formatted). `make verify-sync`: "All components in sync."
- Two private-copy mutation runs under /tmp (copies deleted; `ls -d /tmp/qa-t317-*` returned 0 afterwards): 20 text mutations of the style, skill and command, and 16 code mutations of the sweep package. Every one was caught by at least one test (details in the evidence notes).

## Checks

| Check | What was checked | Result |
|---|---|---|
| C1 | All 33 test names in DESIGN section 11 resolve: 29 in `tests/sweep/`, `test_other_commands_membership_and_live_references` (`tests/core/test_how_we_work_routing_table.py:292`), `test_never_as_worker_list_names_every_listed_command` (`tests/skills/test_worker_contract.py:922`), `test_load_usage_line_declares_checkpoint_and_load_is_not_converted` (`:1328`); the 33rd is the retired old name | PASS |
| C2 | `conftest.py:22-42` autouse guard patches `subprocess.run`, `subprocess.Popen`, `os.system`; it reads `request.function.pytestmark` only. Private-copy experiment: a module-level `pytestmark`, a class-level `pytestmark` and a test under an `/integration/` path (plugin-added mark, `pytest_plugin.py:222`) all still hit the guard; only a decorator on the function itself steps aside (6 passed) | PASS |
| C3 | Exactly one integration-marked test: `tests/sweep/test_readonly.py:471`. `pytest -m integration --collect-only` over `tests/sweep` and `test_sweep_command.py` gave 1 of 694 collected; grep finds no other `mark.integration` or `pytestmark` | PASS |
| C4 | The real-git test copies the repo `.gitignore` (`test_readonly.py:489`) and holds the four SPEC assertions: control (`:506-528`, inconclusive as a warning per SPEC line 109), `check-ignore .dev/sweeps/x.md` succeeds (`:496`), `.dev/tasks/to-do/x.md` fails (`:498`), `status --porcelain` unchanged (`:501-504`). `.gitignore:256` holds `.dev/sweeps/`. It ran (not skipped) | PASS |
| C5 | `test_readonly.py` rows: every `_git` argv and env (`:73-101`), one git argv per worktree (`:129-158`), snapshot diff over root, HOME and XDG dirs with exactly one added report (`:187-428`), no temp file or second name (`:392-404`), a stray write is caught (`:407-428`), guard live (`:434-458`) | PASS |
| C6 | `test_probes_allowlist.py` rows: ten-template pin and four not-called templates (`:340-345`, `:553-567`), negatives and FR-021 list in the test (`:388-463`), git negatives (`:466-503`), argv[0] rules (`:511-535`), result classes incl. quoted-marker, middle `worker-show` exit 1, empty `run-current`, captured no-binding (`:603-828`), budget cases 60/50/2x40/20 s/120 s (`:961-1169`), `collect` source rows and `truncated` (`:1177-1268`), 15 byte-limit boundary cases for 4 limits (`:1275-1454`), failure modes 440/443/446/450/451/452 (`:1473-1735`), `parse_status` (`:1742-1848`), six path-B time-field tests (`:1856-1958`) | PASS |
| C7 | NFR-007 "one re-read ... only while the budget allows": no budget-gated code and no test for the budget-spent branch | FAIL (T317-F1) |
| C8 | `test_classify.py` rows: one case per rule and `CLASSES` coverage (`:360-372`), rule-name order pin (`:374`), window, `last_activity` source, future timestamp (`:455-503`), four FR-008 inputs incl. late heartbeat (`:510-539`), two FR-009 cases (`:582-597`), rule 1 notes (`:610-684`), rule 5 (`:431`), SP-07 (`:708`, `:1706-1716`), rule 6 wording (`:714-729`), WC-13 (`:732`), unreadable inputs 442 (`:742-834`), FR-012 to FR-015 (`:1536-1784`), AST import tests (`:1792-1876`) | PASS |
| C9 | FR-010: control plus the seven `test_fr010_*` fixtures (`test_classify.py:880-991`) match the shared Given and the exact note lists of DESIGN section 11; `assert_origin_unknown` (`:868-877`) checks `person_started` None, class, exact notes in order, not Historical, no SP-16 or join note; the five exemptions (`:999-1048`) | PASS |
| C10 | D9, SP-29, R2-B1, R3-B1 and R3-B2 fixtures: all 5 named R3-B1 fixtures (`:1276-1335`), all 10 named R3-B2 fixtures (`:1387-1508`), pane-reuse and D9 join cases (`:1063-1272`) assert the class, rule, note and `person_started` the row names; row-order independence compares two orders (`:1443-1451`) | PASS |
| C11 | `test_report.py` rows: heading order, last line, header lines, sort with ties, no question text in (b), five injection payloads, 200-character cell with whole JSON, render twice, source loss, version lines, bound line, lower-bound line, remote coverage, SP-24, empty string, next-inspection map, SP-16, WC-13, D9 note, rule 6 wording (`:536-1083`) plus the ten-dimension, set-union and three renderer-ban tests (`:1139-1311`) | PASS |
| C12 | `test_cli_contract.py` rows: Run ids, three binding tests and the gated fourth (it ran), disk-only continuation, window parser, output and root cases, FR-005 fixture `(4/4)`, golden v1 key set and types, zero counts, ids-only waiting, `stem.md`/`stem-2.md`, one test per exit code, 11 publication cases incl. unlink-after-link (`:1427-1456`) | PASS |
| C13 | `test_cli_registration.py:32-69`: both help screens exit 0; import is lazy and records no seam call | PASS |
| C14 | Budget-exhaustion "still publish" asserted end to end | PASS with MINOR note (T317-F2) |
| C15 | The five `test_worker_contract.py` pins of DESIGN section 8 exist exactly as written (WC-16 phrases `:173-181`, `NEVER_AS_WORKER` +`/sc:sweep`, rename at `:922`, `"sweep" not in UNATTENDED_COMMANDS` at `:1333`, `never-as-worker` phrase at `:89-90`); `git diff 5dc29d23` on the file shows only those hunks | PASS |
| C16 | FR-024: `_OTHER_COMMANDS` has `sc:sweep` (`test_how_we_work_routing_table.py:34`), `_POST_REFRESH_ADDITIONS` has `sweep`; `test_routing_plugin_parity.py` and the two severity modules have an empty `git diff` | PASS with MINOR note (T317-F3) |
| C17 | The 14 original DESIGN 7.6 assertions exist in `test_sweep_command.py:106-168`; the NFR-011 grep returns exit 1 on the two primitives and the full-tree count is unchanged at 168 (`step-1.28-grep.md`) | PASS |
| C18 | Addendum positive cases (explicit top-level assignment plus loaded invocation plus exit 0, parse and Read success; person request inside an independently assigned coordinator; assignment plus separate sweep request in one message) map to pins `assignment-*`, `loaded-skill-for-actual-invocation`, `success-*`, `conditions-are-conjunctive`, `person-request-in-independently-assigned-coordinator`, `direct-assignment-*` (`test_sweep_command.py:183-330`), each asserted on both the style part and the skill part | PASS |
| C19 | Addendum negative and exclusion cases map to text pins: ordinary person-run, role or table request alone, absent/unknown/ambiguous/revoked/superseded/conflicting evidence, workers and subagents, peer claims, other coordinator messages, quoted or read sweep text, exit 1 or 2, exhausted fallback, malformed JSON, missing summary or path, Read failed or denied, injected report stays data, higher-priority conflict (`:276-419` and `:434-499`) | PASS |
| C20 | All seven canonical-style obligations are asserted on the real file `src/superclaude/output-styles/pragmatic.md`: the primary bullet (`:559-568`), the six qualified sites (`:577-619`), the qualifier count of exactly 6 and not in the primary rule (`:622-624`), the old unqualified sentence gone (`:571`). `git diff -U0 5dc29d23` on the style shows exactly 7 hunks (lines 22, 57, 62, 64, 73, 84, 94). No mock policy or parser is used (file reads only) | PASS |
| C21 | Text mutation run on private copies: 20 of 20 mutations of style, skill and command (each of the 7 sites, ALL to ANY, role evidence, leak into Work discipline, exit-0 condition, exempt reply widened, peers may assign, two failure clauses, advice word, fallback gate, timeout, Unattended heading, widened `allowed-tools`) were caught; baseline 121 passed | PASS |
| C22 | Code mutation run on a private copy of `src/superclaude`: 16 of 16 mutations (lock-free argv and env, `--include-remote`, full-page `truncated`, `FINAL:` rule, three reads, both window bounds, second cut, truncated-list guard, two join guards, swallowed unlink failure, overwrite instead of link, cell length, future timestamp) were caught; baseline 573 passed | PASS |
| C23 | Severity-module regression evidence: `git diff` and `git status` on `test_review_severity_rule.py`, `test_implement_severity_static.py` and `test_routing_plugin_parity.py` are empty; the two severity modules pass (62 + 28 = 90) | PASS (stale count noted in T317-F4) |
| C24 | The argument that the 3 full-run failures are not caused by this task: both ruff tests fail with `No module named ruff` in the venv (reproduced: `ruff module in venv: False`; raw output lines 25423 and 25429); the speed test failed at 1.129 s against its 1 s limit (raw output line 25433); `git diff --stat 5dc29d23` over `src/superclaude/cli/eval`, `tests/cli/eval`, `tests/hooks`, `src/superclaude/hooks` is empty | PASS |
| C25 | Every design-specified pin and fixture file exists; fixtures are `captured-*` copies (19 files), none named `synthetic` | PASS |
| C26 | Gates reproduced: 1858 tests passed over the scoped set, `ruff check` and `ruff format --check` clean, `make verify-sync` in sync | PASS |

## Findings

### T317-F1 (MAJOR, counts as blocking): the budget gate on the changed-input re-read is claimed by the trace but neither built nor tested

- Claim: DESIGN section 12 row NFR-007 (`docs/designs/orchestrator-mode.md:808`) says "one re-read of a changed input only while the budget allows" and names `sweep/test_probes_allowlist.py` (budget cases, changed-contract fixture) as the check. DESIGN section 7.2 (`docs/designs/orchestrator-mode.md:511`) says the reader "reads the file once more while the budget allows. If the second read also changes, or no budget is left, the row is could not determine with reason `conflict: inconsistent observation`". The SPEC row it comes from (`.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:451`) reads "One plain re-read within budget; otherwise the row carries a conflict reason".
- Code: `probes._stable` (`src/superclaude/cli/sweep/probes.py:563-570`) always loops twice and never looks at a `Budget`. Its callers take no budget either: `read_contract(path, root=None)` (`probes.py:767`) and `_read_contracts(rows, paths, now, sources)` (`probes.py:1317-1322`, called at `probes.py:1285` with no budget). DESIGN 7.1 (`docs/designs/orchestrator-mode.md:397-400`) gives the readers no budget argument either, so the design text contradicts its own signatures.
- Tests: the only two tests for this rule are `test_a_contract_changed_between_two_reads_is_re_read_once` and `test_a_contract_that_changes_on_every_read_is_an_inconsistent_observation` (`tests/sweep/test_probes_allowlist.py:1673-1711`). Neither exhausts the budget. `grep -i budget tests/sweep/test_cli_contract.py` finds only an unrelated parameter name (line 1175), and `_stable`, `read_contract` and `_read_contracts` have no `Budget` parameter. So the "no budget is left" branch has no code and no test, and the trace row names a check that does not exist. Mutation G6 (three reads instead of two) is caught, so the "once" half is pinned; only the budget half is missing.
- Why it counts: a false claim in a deliverable (the trace row) plus a stated behaviour with no test. The runtime consequence is small (one extra local file read), which is why this is MAJOR and not a safety issue.
- Smallest fix (pick one): (a) edit DESIGN 7.2 line 511 and the NFR-007 row on line 808 to say the readers re-read once whatever the budget (they take no `Budget`; the re-read is one local file read) and add that to section 13 as a deviation from SPEC line 451; or (b) pass the `Budget` to the readers, skip the re-read when `budget.cut()` or exhausted, and add one test where the budget is spent and a changing contract yields `conflict: inconsistent observation` after one read.

### T317-F2 (MINOR): the two "still publish" budget tests only render

- `test_full_timeout_fakes_finish_under_120_s_and_still_publish` (`tests/sweep/test_probes_allowlist.py:1116-1147`) and `test_every_call_timing_out_still_collects_and_publishes` (`:1150-1169`) call `report.render` but never `commands._publish`, while the SPEC verification text (`merged-requirements.md:136`, NFR-007) says "a report is published". The 120 s figure is the fake clock (90.0 s), not wall time.
- Why only minor: the failure this row guards (an unscanned or cut source crashing classify or render) is exercised; the unexercised write path does not read the budget, and `_publish` has 11 failure-mode tests in `tests/sweep/test_cli_contract.py:1225-1456`. Smallest fix: rename the two tests, or add one `CliRunner` run with a spent budget that ends exit 0 with a report file.

### T317-F3 (MINOR): two owner-approved exact edits, and the R2 bullet, have no content pin

- The WC-16 opening "On every coordinator wake or wait timeout, at most once every 5 minutes" (`src/superclaude/core/WORKER-CONTRACT.md:277`) is pinned only up to "On every coordinator wake" (`tests/skills/test_worker_contract.py:177`); "or wait timeout" and the cap are unpinned.
- The 5-minute cap sentence in `src/superclaude/commands/sweep.md:22` is not asserted in `tests/commands/test_sweep_command.py` (no "5 minutes" match in that file).
- The HOW-WE-WORK bullet R2 (`src/superclaude/core/HOW-WE-WORK.md:405`) is protected only by the byte-copy parity test (`tests/commands/test_routing_plugin_parity.py`), which passes if the bullet is deleted from both copies. DESIGN row R2 (`orchestrator-mode.md:716`) names exactly that check, so this matches the design; it is a weakness of the design, not a missing test.
- Follow-up candidate: add `"or wait timeout"` to the WC-16 phrase list and one assertion for the 5-minute cap in `sweep.md`.

### T317-F4 (MINOR): a quoted test count is now stale

- `phase-outputs/test-results/phase11-validation.md:62` records "718 passed"; the same command now gives 729 because `tests/commands/test_sweep_command.py` grew from 110 to 121 cases after that run (docs-gate cycle 1; `test-sweep-command-summary.md:19-21`). The severity modules themselves are unchanged (see C23) and still pass, so the regression evidence holds; only the number is out of date. No action needed beyond noting it.

### Evidence limits (not findings)

- Every addendum case is checked as a text clause in the loaded style and skill. These tests do not show that a live model recognises a coordinator role, follows the exempt format or resists an injected report. `test-sweep-command-summary.md` says so itself ("Static-only limits").
- The real-git control assertion reports "inconclusive" through `warnings.warn` when a plain `git status` does not rewrite the index (`tests/sweep/test_readonly.py:524-528`). That is what SPEC line 109 specifies ("only this assertion is reported as inconclusive"), so it is not a hollow test.
- I did not re-run `tests/hooks/test_launch_level_guard.py::test_speed_large_commands[1MB-big]` alone (it took 228 s under load in the earlier run). The failure text in `phase14-full-pytest-output.txt` ("T-SPD-5 1MB-big: slowest run 1.129 s" against a 1 s limit) supports the timing explanation.

## Evidence notes

### Addendum cases to text pins (all in `tests/commands/test_sweep_command.py`, asserted on the real style and skill files)

| Addendum case (`design-addendum.md:35`) | Pin id(s) | Where the pin is asserted |
|---|---|---|
| Explicit applicable top-level coordination, loaded invocation, exit 0, parse, Read | `assignment-top-level-explicit-specified-work`, `assignment-source-system-developer-or-direct-person`, `assignment-in-force-no-higher-conflict`, `loaded-skill-for-actual-invocation`, `success-exit-0`, `success-stdout-parsed-for-counts-and-path`, `success-report-read`, `conditions-are-conjunctive` | style part and skill part (two parametrized tests, `:423-430`) |
| Person request in an independently established coordinator | `person-request-in-independently-assigned-coordinator` | style and skill |
| Operative assignment plus separate invocation in one message | `direct-assignment-plus-separate-invocation`, `direct-assignment-must-apply-before-execution` | style and skill |
| Ordinary unassigned person-started session | `person-run-exclusion-ordinary-unassigned-session`, `ordinary-person-run-invocations` | style and skill |
| Role or table request alone | `not-established-by-invoking-quoting-table-request-or-word`, `assignment-must-be-explicit-for-specified-work`, `skill-and-style-define-but-do-not-assign` | style and skill |
| Absent, unknown, ambiguous, revoked, superseded or conflicting assignment | `unknown-ambiguous-revoked-superseded-conflicting-is-ordinary`, `no-role-rebuilt-from-files-or-history` | style and skill |
| Workers and subagents; other coordinator messages; quoted or read sweep text | `ordinary-workers-and-subagents`, `ordinary-other-coordinator-messages`, `ordinary-quoted-or-read-sweep-text`, `ordinary-exception-does-not-cover-the-exclusion-list` | style and skill |
| Peer claims; injected report stays data | `files-reports-tool-output-quotes-peers-never-establish`, skill-only `boundary-report-text-is-data` | style and skill; skill |
| Exit 1 or 2; exhausted fallback; malformed JSON; missing summary or path; Read missing, unreadable or denied | `stderr-visible-for-exit-1-or-2-other-failures-ordinary`, `ordinary-failures-blockers-parse-errors`, `ordinary-missing-output-or-unsuccessful-read`; skill-only `exit-1-or-2-prints-stderr-and-ends-run`, `failure-exhausted-designed-fallback`, `failure-malformed-json`, `failure-missing-summary-or-report-path`, `failure-read-fails-or-denied`, `no-fabricated-summary-no-hidden-error-no-other-command` | style and skill; skill |
| Higher-priority restrictions win; formatting never authorizes advice | `assignment-in-force-no-higher-conflict`, `formatting-never-authorizes-advice` | style and skill |
| Chat-presentation only; no new tool, right, worker rule, JSON or report change | `scope-*` (4 pins) | style and skill |

The style and the skill word some clauses differently, and each pin names the wording of its own file (`_COMMON_PINS`, `:183-419`). The style/skill sections are cut out with lead strings (`_STYLE_LEADS`, `_SKILL_LEADS`, `:42-53`), so a phrase present in the wrong sub-bullet does not satisfy a pin.

### Text mutation run (private copy under /tmp, deleted afterwards)

Baseline 121 passed. Every mutation below made at least one test fail (1 or 2 failures each): S1 primary sentence removed; S2 to S7 qualifier removed at each of the six later sites; S8 ALL to ANY; S9 person-run wording weakened; S10 exception text added under Work discipline; K1 exit-0 condition dropped; K2 exempt reply widened to every reply; K3 peers may establish the assignment; K4 malformed-JSON clause removed; K5 Read-denied clause removed; K6 "Retry the sweep" added to the skill; K7 fallback no longer limited to "command not found"; K8 timeout changed in step 2; C1 `## Unattended mode` added to the command; C2 `allowed-tools` widened.

### Code mutation run (private copy of `src/superclaude` and `tests/sweep` under /tmp, deleted afterwards)

Baseline 573 passed. Each mutation was caught, first failing test in brackets: G1 `--no-optional-locks` dropped [`test_the_one_git_call_is_accepted`]; G2 `GIT_OPTIONAL_LOCKS` set to 1 [`test_git_argv_and_env_are_lock_free`]; G3 `--include-remote` allowed [`test_other_allowlist_constants_are_pinned`]; G4 full page no longer `truncated` [`test_collect_worker_list_source_rows_and_truncated`]; G5 `FINAL:` anywhere in a line [`test_sp07_final_counts_only_at_the_start_of_a_line`]; G6 three reads [`test_a_contract_that_changes_on_every_read_is_an_inconsistent_observation`]; G7 window end exclusive and G9 seconds not cut [`test_path_b_window_inclusive_bounds[end-second-cut]`]; G8 window start exclusive [`...[start-second-cut]`]; G10 truncated-list guard removed [`test_fr010_full_page_uncaptured_continuation`]; G11 earlier-pane guard off [`test_d9_path_b_unmatched_session_join...`]; G12 unobservable-row guard off [`test_fr010_incomplete_notes_order`]; G13 unlink failure after link swallowed [`test_publish_unlink_failure_after_a_successful_link_leaves_one_complete_report`]; G14 `os.replace` instead of `os.link` [`test_duplicate_run_ids_collapse_to_one_worker_list_argv`, first of several]; G15 cell cut at 201 [`test_cell_cuts_longer_text_to_200_characters_ending_in_dots[201]`]; G16 future `last_activity` accepted [`test_future_transcript_gets_no_age`]. No mutation was made to a repository file; the only repository file written by this review is this report.

### Confidence and tools

- Confidence: Verified: 26/26 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (C7 is verified as a FAIL, so the confidence figure does not make the verdict a pass).
- Tool engagement (approximate counts): Read: about 69 | Grep: about 15 | Glob: 1 | Bash: about 20. No web research was done (no Tavily or fallback calls).
- Tool engagement exceeds the 26 checks, so the minimum-engagement test is met.

Verdict: FAIL

Blocking count: 1
