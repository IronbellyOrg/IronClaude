# QA Final Gate: Numbers / Metrics Lens

Reviewer: qa-final-numbers (adversarial, fix_authorization: false)
Date: 2026-11-12
Scope: recount every countable item in the change set against the text or code that states it.

## Method

Every count below was recomputed from the files on disk on 2026-11-12 (Read in chunks of at most 150 lines, `grep`, `wc -l`, `git diff --numstat`, `uv run pytest --collect-only`, one read-only scoped `uv run pytest`, `cmp`, `make verify-sync`, and `uv run python -I -c` readers over saved JSON). No repository file was changed. No live Orca, ccsession or Claude command was run. The only repository file written is this report.

## Findings

No BLOCKING or MAJOR finding. Every count the lens names matches the text and the code that state it. Eight MINOR findings (stated counts or wording that do not match the delivered files); they never fail the gate.

| id | severity | evidence | what is wrong | smallest fix |
|---|---|---|---|---|
| N1 | MINOR | `docs/designs/orchestrator-mode.md:759` ("nine boundary fixtures"), `:795` ("the nine byte-limit boundary fixtures"), `:1025`; `tests/sweep/test_probes_allowlist.py:1272` (header "the nine boundary fixtures"); collected cases: `test_contract_size_boundary` 3, `test_ledger_size_boundary` 3, `test_transcript_tail_boundary` 3, `test_subprocess_output_boundary_for_orca` 3, `test_subprocess_output_boundary_for_git` 3 | The text counts 3 limits x 3 cases = 9 (contract and ledger as one 1 MiB limit, orca and git as one 8 MiB limit). The delivered tests run 5 test functions x 3 = 15 boundary cases (`uv run pytest tests/sweep --collect-only -q`). The "nine" is a floor, not the count the tests have. | Say "at least nine" or "fifteen" in the DESIGN rows and the test header; no code change. |
| N2 | MINOR | `tests/sweep/fixtures/SOURCES.md:11` ("the 266-300 character terminal preview"); `tests/sweep/fixtures/captured-worker-show-{1..5}.json` `result.terminal.preview` lengths 266, 248, 251, 300, 282; raw capture `artifacts/readonly-probe-raw/a-ws-*.json` gives the same 266, 248, 251, 300, 282 | The stated range is wrong at the low end: the shortest kept preview is 248 characters, not 266. | Change "266-300" to "248-300". |
| N3 | MINOR | `docs/designs/orchestrator-mode.md:62` (GQ-105: head 512 KiB and tail 512 KiB are read) and `:398` (`read_ledger ... head 512 KiB + tail 512 KiB over 1 MiB`); `tests/sweep/test_probes_allowlist.py:1328` (`test_ledger_over_the_limit_is_read_as_head_and_tail`); `src/superclaude/cli/sweep/probes.py:576-581` | For a ledger over 1 MiB the code reads only the last `LEDGER_SPLIT` (512 KiB) bytes; no head is read. The result is the same as the DESIGN's "the tail is searched", and the test at `:1336` pins that behaviour, so only the "head 512 KiB read" in the text and the test name is not true of the code. | Reword to "the last 512 KiB is read" (DESIGN 2.2 GQ-105, 7.1) or rename the test; no code change. |
| N4 | MINOR | `docs/designs/orchestrator-mode.md:760` and `:785` ("seven `test_fr010_*` in all", "seven `test_fr010_*` fixtures plus the control"); `tests/sweep/test_classify.py:880, 894, 903, 915, 925, 938, 948, 960, 1044, 1051` | `grep -c 'def test_fr010_'` is 10: the control, the 7 named fixtures, and two more (`test_fr010_exemptions_never_become_idle`, `test_fr010_exemption_orca_rows_never_go_to_historical`) that the DESIGN lists separately as "the five exemptions". Read literally, "seven in all" is wrong. | Say "seven list-incomplete fixtures plus the control and the exemption tests". |
| N5 | MINOR | `phase-outputs/test-results/phase11-validation.md:62` ("718 passed"); the same command's collection today is 729 tests | The saved Phase 11 count is 11 lower than the tree today: cycle-1 QA fixes later added 5 (110 to 115) and 6 (115 to 121) cases to `tests/commands/test_sweep_command.py` (`test-sweep-command-summary.md:19-21`). The file is a dated snapshot; the later run `phase14-scoped-pytest.md` (3220 passed) matches the tree (re-run now: 3220 passed). Already in `followups.md:7`. | None beyond the existing follow-up. |
| N6 | MINOR | `revisions/chat-output-exception-20261109-133150/design-addendum.md` ("add all seven restatement checks"), `delta-manifest.md:45` ("seven restatements"); the same addendum says "the six independent later obligations"; `test-sweep-command-summary.md:115-120` ("restatement 1 of 6") | "Seven restatements" counts the primary rule plus its six restatements (seven table sites); the style and the tests have six restatements. The same files use both words. | Say "seven sites" or "six restatements plus the primary rule". |
| N7 | MINOR | `docs/designs/orchestrator-mode.md:340` ("Orca argv total: at most `1 + 3R + 1 + 50` ... NFR-003 recording test"); `tests/sweep/test_probes_allowlist.py:548` (`== 1 + 2 + 5 + 1`), `:1075` (50 shows), `:1133` (9 calls under the 90 s budget) | The code satisfies the bound (3 list calls per Run, one `worktree ps`, at most 50 shows, one `run-current`). No test asserts the total against `1 + 3R + 1 + 50`; its parts are pinned separately. | Add one assertion on the total in the 60-row test, or word the row "parts pinned by". |
| N8 | MINOR | `docs/designs/orchestrator-mode.md:5` ("Owner approval of the WC-16 text ... is still required"), `:7-11` ("Three blocking findings were still open"); `:1037-1045` (Fix cycle 3 records the R3-B1 to R3-B3 changes); `phase-outputs/plans/OQ-3-addendum-wc16-wait-timeout-decision.md`, `artifacts/owner-decisions.md` row OQ-3 (WC-16 approved) | The Status banner still counts three open findings and a pending approval that section 18 and the owner records show as done. The banner is base text that Phases 2 to 6 did not change (not in `git diff --no-index` hunks at lines 5 to 11 except line 5). | Update the banner to say the three findings were fixed in cycle 3 and WC-16 was approved. |


## Count evidence (what was recounted and the number found)

- Never-as-worker list: `src/superclaude/core/WORKER-CONTRACT.md:23` names 8 commands (`agent, git, help, issue, pm, spawn, sweep, swarm-wizard`) plus `pr-submit` while D3 holds = 9; `tests/skills/test_worker_contract.py:391-401` `NEVER_AS_WORKER` has 9 entries; DESIGN 8 (line 687) says "giving 9 entries"; developer guide line 991 and `sweep.md:18` agree; `sweep` is absent from `UNATTENDED_EXPECT` (assertion added at the `load` check).
- `ALLOWED_ORCA`: `probes.py:47-58` has 10 tuples, 7 distinct verbs (`run-current, worker-list, worker-show, task-list, ps, list, current`), 4 marked "not called" (list, current, two `--agent-wait`); DESIGN lines 181, 196, 537, 555, 815, 837, 851, 895 and `test_probes_allowlist.py:342` (`len(set(...)) == 10`) agree; templates 1 to 8 are the first eight in code order, as DESIGN 15.1 says.
- `UNATTENDED_EXPECT`: 31 keys by count (`test_worker_contract.py:448-756`), 16 P1 plus 15 P2 (`P1_COMMANDS`, `P2_COMMANDS`, and `WORKER-CONTRACT.md:307-308` lists 16 and 15 names); `_check_p2_set` asserts 31 at `:1575`; the contract's "17 rows" table (line 311) has 17 rows (16 read plus `/sc:workflow` at line 331).
- Routing rows R1 to R8: R1 (`HOW-WE-WORK.md:334`), R2 (`:405`), R3 (plugin copy `cmp` byte-equal), R4 (`_OTHER_COMMANDS` +1), R5 (`_POST_REFRESH_ADDITIONS` +1), R6 (`commands.md:116`), R7 (developer guide `:991`), R8 (`CHANGELOG.md:7-15`): 8 of 8 present in `git diff`; `make verify-sync` passes.
- Six sweep modules: `src/superclaude/cli/sweep/` holds `__init__, classify, commands, models, probes, report` = 6 files (DESIGN 3.1 "a seventh module" and the inventory agree).
- `[sweep publish]` messages: DESIGN 3.2 names 6 literals (`<error>`, `output dir escaped`, `temp file exists`, `cannot link report`, `report name space exhausted`, `could not remove temp file`); `commands.py:153-208` emits those 6 plus the second line `left temp file` that DESIGN names only as "a second stderr line"; exit codes 0, 1, 2 (`commands.py:279-288`) match DESIGN 3.4, `sweep.md`, SKILL step 5 and the three `test_exit_code_*` tests.
- `Total: 10 deviations.` (`orchestrator-mode.md:839`): rows D1 to D10 = 10. `Total: 23 open items.` (`:1015`): rows 1 to 23 = 23.
- 256 KiB tail: `TRANSCRIPT_TAIL = 256 * 1024` (`probes.py:72`), used at `:827-829`; DESIGN 6, 7.1, 7.2, 7.3 and `test_byte_limits_are_pinned` agree; 8 MiB and 1 MiB limits and 512 KiB split also agree (`probes.py:69-71`).
- 50-call cap: `Budget(shows=50, total_s=90.0, per_call_s=10.0)` (`probes.py:111-117`); `show_cap_reason()` gives `show cap reached (50)`, `budget_reason()` gives `time budget reached (90 s)`; tests: 60 rows give 50 shows and `bound_reached` 10, 50 rows give 0, 2 Runs of 40 give 25 each and 30; 9 calls x 10 s = 90 s.
- `-99` limit: `MAX_SUFFIX = 99` (`commands.py:29`), names `stem.md` then `stem-2.md` to `stem-99.md` (`:182`) = 99 names; test `test_cli_contract.py:1330-1352` takes all 99 and then the last name.
- Window: regex `[1-9][0-9]{0,3}[hd]` plus `hours <= 720` (`commands.py:43-52`) = 1 to 9999, at most 720h or 30d, as `sweep.md:38` says; default `6h` (`:27`); Run id `run_` plus 12 hex digits (`probes.py:44`) as `sweep.md:37` says; skill timeout 120000 ms is above the 90 s budget and below the contract's 4-minute WC-10 limit.
- Classes and sections: `CLASSES` 8 (`models.py:31-40`, "eight classes" in `sweep.md:14`); `PACKAGE_STATES` 6; `SAFE_VALUES` 3; `RULES` 9 (`classify.py:337-347`, `NEXT_INSPECTION` has 9 keys); `SECTIONS` 12 (`report.py:523-536`); ten session dimensions (9 `SessionRow` fields plus `policy`, `report.py:57-68`); `CELL_MAX = 200`; `CHECKED_ORCA_VERSION = "1.4.245"`.
- Size and diff: inventory `final-inventory.md` 37 new files, 14069 lines (recounted: 3617 + 136 + 8184 + 2132 = 14069); DESIGN 1051 lines; 12 edited files, 54 insertions + 13 deletions = 67 (`git diff --numstat`); total 15187; `git diff --no-index --stat` DESIGN 112 + / 74 - as stated; 14 prompts in `qa/final/prompts` = 14 agents (over 3000 lines).
- Tests: 694 sweep and command tests collected = 161 + 94 + 3 + 243 + 24 + 48 + 121; `test_sweep_command.py` 121 = 14 + 74 + 15 + 12 + 6 (37 style/skill pins x 2, as `test-sweep-command-summary.md` states); style file has the qualifier 6 times, 4 `non-exempt example`, 4 `| Status | Result |`, 3 `| NEXT | None. |` (`pragmatic.md:57-99`), 238 lines, +11/-7, `## Work discipline` at line 107; scoped run 3220 collected and 3220 passed (re-run); `phase14-sync.md` counts (40 skills, 48 agents, 47 commands) match `ls` minus `README.md`; `phase14-full-pytest.md` 3 failed / 25252 passed matches the saved output file's last line, and its cause holds (`find_spec('ruff')` is `None` in the venv, `pyproject.toml:54` pins `ruff==0.15.20`, `git diff --stat` over `src/superclaude/cli/eval`, `tests/cli/eval`, `tests/hooks`, `src/superclaude/hooks` is empty); `step-1.28-grep.md` 168 hits now equals 168 recounted.
- Live-check JSON: `sweep-live-check-1.4.json` 180 rows (5 Orca + 175 transcripts), 71 sources, 0 unscanned, `bound_reached` 0; re-run 182 rows, `total_is_lower_bound` true, as the two `.md` files state; 9 Orca reads = 1 + 2 + 5 + 1.
- Fixtures: 19 `captured-*.json` plus `SOURCES.md` (SOURCES table 19 rows); 5 workers, 5 tasks, `ps` 3 and `list` 2 worktrees with `totalCount` set to match; 3-line tab-map files; (preview range wrong, see N2).
- `owner-decisions.md` "eight rows" (OQ-1 to OQ-7 and OQ-17); `APPROVED.md` 90 lines; `merged-requirements.md` 653 lines; GAPS line 138 "113 rows" and 113 `GQ-` rows.

## Checks

| id | check | result |
|---|---|---|
| C1 | Never-as-worker list is 9 entries in the contract text, the test tuple, DESIGN 8, the developer guide and `sweep.md` | PASS |
| C2 | `ALLOWED_ORCA` has 10 templates and 7 verbs; 4 marked not called; templates 1 to 8 are the capture set; all texts agree | PASS |
| C3 | `UNATTENDED_EXPECT` has 31 entries (16 + 15) and `sweep` is not one | PASS |
| C4 | Routing rows R1 to R8 are all delivered and R3 is byte-equal to R1 plus R2 | PASS |
| C5 | Six sweep modules | PASS |
| C6 | Six `[sweep publish]` messages and exit codes 0, 1, 2 match DESIGN, command, skill and tests | PASS |
| C7 | `Total: 10 deviations.` | PASS |
| C8 | `Total: 23 open items.` | PASS |
| C9 | 256 KiB tail (and the 8 MiB, 1 MiB, 512 KiB limits) match text and code | PASS |
| C10 | 50-call (show) cap, 90 s budget and 10 s per call match text, code and tests | PASS |
| C11 | `-99` report-name limit matches text, code and test | PASS |
| C12 | Window, Run id and timeout numbers in `sweep.md` and SKILL match the code | PASS |
| C13 | Eight classes, 6 package states, 9 rules, 12 sections, ten dimensions match | PASS |
| C14 | Final-inventory sizes (37 files, 14069, 1051, 12 files, 67, 15187, 14 agents) recount exactly | PASS |
| C15 | Test counts: 694, 121 = 14 + 74 + 15 + 12 + 6, scoped 3220 (re-run) | PASS |
| C16 | Style-exception counts (6 qualifiers, 4 labels, 4 headers, 3 None rows, +11/-7, 238 lines) | PASS |
| C17 | Phase 14 numbers: sync counts, lint, 168 grep hits, full run 3 failed / 25252 passed, and the 3-failure argument | PASS |
| C18 | Live-check numbers (180/182 rows, 5 workers, 71 sources, 9 reads) match the saved JSON | PASS |
| C19 | Fixture counts (19 files, 5 workers, 5 tasks, 3 and 2 worktrees) match `SOURCES.md` (range of preview length excepted, N2) | PASS |
| C20 | DESIGN boundary-fixture count "nine" matches the tests | FAIL (N1, MINOR) |
| C21 | `SOURCES.md` preview length range matches the fixtures | FAIL (N2, MINOR) |
| C22 | Ledger "head 512 KiB + tail 512 KiB read" matches the code | FAIL (N3, MINOR) |
| C23 | "seven `test_fr010_*`" matches the test names | FAIL (N4, MINOR) |
| C24 | Saved Phase 11 count (718) matches the tree today | FAIL (N5, MINOR, snapshot) |
| C25 | "seven restatements" vs six restatements in the addendum and manifest | FAIL (N6, MINOR) |
| C26 | DESIGN argv-total bound has a test that asserts it | FAIL (N7, MINOR) |
| C27 | DESIGN Status banner counts match the later sections | FAIL (N8, MINOR) |

Self-check: I found 8 MINOR count or wording mismatches and no BLOCKING or MAJOR one. The lens-named counts (C1 to C13) were each recounted from the source files, not from earlier gate reports. Items not checked: counts inside `.dev/tasks/**` bookkeeping that are not part of the change set (for example the task file's 355 items, which I did confirm: 355 checkbox lines at baseline and now, 137 done at baseline); and I did not run the 3 failing full-suite tests, because `tests/cli/eval` and `tests/hooks` are outside the folders this gate may run.

Verdict: PASS

Blocking count: 0

