# Verify cycle 1: rf-qa-qualitative (T333)

Fix authorization: false. Inputs: consolidated-findings-cycle0.md (F_0), fix-log-cycle1.md, cycle-ledger.md (238 cycle-0 PASS ids).
Judged against live files on disk, not the fix log.

## Findings

Edit-set check (independent of the fix log): `find . -newer phase14-full-pytest.md` over the repository (outside `.git`, `.venv`, caches, `.dev`, `.claude`) lists exactly `classify.py`, `probes.py`, `report.py`, `SKILL.md`, `test_classify.py`, `test_cli_contract.py`, `test_probes_allowlist.py`, `test_report.py` and `test_sweep_command.py`, plus three files whose content equals HEAD (`src/superclaude/cli/install_hooks.py`, `src/superclaude/hooks/hooks.json`, `src/superclaude/hooks/scripts/auggie-flag-clear.sh`: mtime 16:32 on 2026-11-12, `git status` and `git diff HEAD` empty, so not a content change). `models.py`, `commands.py`, DESIGN, SPEC, `pragmatic.md`, `sweep.md`, the guide, CHANGELOG and the fixtures are not in the list. `sha256sum` of the four immutable inputs equals the four sums recorded at the top of the fix log; `cmp` of the two HOW-WE-WORK copies is clean; `cmp` of `src/.../sc-sweep-protocol/SKILL.md` against `.claude/skills/sc-sweep-protocol/SKILL.md` is clean.

Gates re-run by me on the live tree: `uv run ruff check .` clean; `uv run ruff format --check` on `src/superclaude/cli/sweep`, `tests/sweep` and `tests/commands/test_sweep_command.py`: 16 files already formatted; `uv run pytest tests/sweep tests/commands tests/core tests/skills tests/recommend -q`: 3242 passed; `make verify-sync`: in sync; scoped `grep -rn 'src/superclaude'` over the sweep primitives: no output, exit 1; full-tree count 168; `git diff --cached --name-only -- .claude/`: 0. Two mutations on a private /tmp copy (deleted afterwards): `range(2)` to `range(3)` in `probes._stable` failed `test_a_contract_that_changes_on_every_read_is_an_inconsistent_observation` (`assert 3 == 2`); replacing the `budget.spent()` break with `if False:` failed `test_a_changed_contract_is_re_read_only_while_the_budget_allows[spent]`.

### FIN-F1 (BLOCKING): RESOLVED

- `src/superclaude/cli/sweep/probes.py:422-445` (`parse_worker_show`) reads no `agentWait` field; the comment at `:432-434` says why. `grep -n 'agentWait|_WAIT_TIME_KEYS|_wait_since|_agent_wait_present'` over the package finds only comments and one evidence string (`probes.py:432`, `classify.py:231`, `:253`, `report.py:116`); the guessed lookup and the six guessed time keys are gone.
- `classify.py:251-257`: `_rule_working` returns `None` always, with the four DESIGN 7.2 conditions kept in a comment. A live row that would have reached Rule 5 falls to `fallback`, which is what DESIGN open item 6 (`docs/designs/orchestrator-mode.md:996`) says.
- Rule 4(a) is kept (`classify.py:228-236`), but nothing sets `agent_wait` in production now, so no guessed key can produce a false `waiting on a person` row. Pin: `tests/sweep/test_probes_allowlist.py:1552`.
- The defect this finding named (code treating unverified names as facts) is gone. Residual, known and not new: the report caveat (`report.py:36-39`, `sweep.md:16`, SKILL step 4) still names only stalled and fenced, so `working: 0` and a missing waiting (a) from Orca can be misread. It is `qa-design-conformance-report` F6 (MINOR, follow-up candidate) and the fix log's own "OPEN (documentation gap)". Not blocking.

### FIN-F2 (MAJOR): RESOLVED

- `report.py:425-426` prints `<terminal> / <worktree> (<reason>)` from `r.safe.reason`, through `cell()`; `report.py:40-43` and `:400` print `SAFE_TO_CLOSE_LINE` once under the Sessions heading. `classify.safe_to_close` (`classify.py:467-492`) never returns `yes`, and always sets a reason, so the sentence is true.
- Pin: `tests/sweep/test_report.py:1046-1077` asserts both cells byte for byte and the single line. Longest live shape by hand count: `could not determine / could not determine (terminal: result read not observable (terminal_state=reclaimable, next_action=release); worktree: report read, open PR and unmerged commits not observable)` is about 198 characters, under `CELL_MAX` 200 (hand count, not run).

### FIN-F3 (MAJOR): RESOLVED

- `report.py:54-55` (`waiting_signal`) and `:60-61` (`fallback`) are true for every outcome of their rule (an agent wait, a frozen plan, a ready Task; a fallback row with or without an unscanned source). The map is still keyed by rule name (`NEXT_INSPECTION`, `report.py:48`), as DESIGN 7.5 `:643` says. Pin: `tests/sweep/test_report.py:1035-1043`; the old map test (`:1010`) still passes. Wording notes are under "Passage re-read" below.

### FIN-F4 (MAJOR): RESOLVED

- `classify.py:86` (`NOTE_NO_CONTRACT`) and `:328-330`: the fallback rule adds it when the Orca row is settled (`_settled`, `:113-114`) and `row.contract is None`. Pins: `tests/sweep/test_classify.py:607` (live shape: exited, completed, succeeded, no contract; also partial and failed) and `:634` (the negative cases). The note and the two other live notes together are about 159 characters, under the 200 cell cut (hand count).

### FIN-F5 (MAJOR): OPEN (valid reason, owner decision)

- Unchanged: `report.py:33` and `:163-166` (`_discovery_incomplete` is true for any unscanned `orca worktree ps`), banner pinned by DESIGN `:614`, `tests/sweep/test_report.py:66` and `tests/sweep/test_cli_contract.py:443`. DESIGN is immutable for the fix agent; the fix needs the owner to move all four together. Counts toward F_1.

### FIN-F6 (MAJOR): RESOLVED

- `report.py:513-516` now says `- Orca became unavailable; the Orca sources marked unscanned above were not read`; the unscanned source lines it refers to are appended earlier in the same section (`:508-512`). Pin: `tests/sweep/test_report.py:1080-1091`.

### FIN-F7 (MAJOR): OPEN (exempt reply: valid reason; ordinary reply: delivered, but see FIN-N1)

- Ordinary reply: `SKILL.md:25-26` takes `orca_available` and prints `Orca was unavailable; the counts may be missing Orca data (see Source coverage in the report).` when it is false. The sentence is true after a full outage and after a mid-run drop (`report.py:164`, `:513`; `to_json` `report.py:621` carries the key). Pins: `tests/commands/test_sweep_command.py:526-531`, `:559-569`.
- Exempt reply: unchanged, still counts and path alone (`pragmatic.md:23`, `SKILL.md:35`, `:43`). An exit 0 outage run still reaches the coordinator with no outage line. Allowing one line needs `pragmatic.md` and the addendum, both revision authority, so this part stays OPEN for the owner. Counts toward F_1.

### FIN-F8 (MAJOR): RESOLVED

- `probes.py:182-184` (`Budget.spent`), `:540-554` (`_stable` stops after one read when the file changed and the budget is spent, giving `conflict: inconsistent observation`), and the budget is passed at every `_stable` caller (`:577`, `:652`, `:720`, `:801`, `:922`, `:946`, `:1251-1252`, `:1306`, `:1355`). Pins: `tests/sweep/test_probes_allowlist.py:1788-1818` (both cases) and the two older tests (`:1690`, `:1707`); my mutations above fail them. The ledger and transcript threading is exercised only through the same `_stable` call (the fix log says so).

### FIN-F9 (MAJOR): RESOLVED

- `probes.py:22` imports `yaml`; `:672-684` `_yaml_top` is `yaml.safe_load` inside `try/except (yaml.YAMLError, RecursionError, ValueError)` and treats a non-mapping as `{}`; `:687-710` reads string values only. The three divergent inputs of the finding are now cases of `tests/sweep/test_probes_allowlist.py:1731-1784` (8 cases). The read stays bounded and read-only (`CONTRACT_LIMIT` check at `:718-719` before the parse; no new `open`, write or subprocess: my grep of the package shows `open(` only in mode `rb`). The DESIGN `:211` import-list line stays a documentation gap (the fix log says OPEN; it does not fail anything).

### FIN-N1 (MAJOR): OPEN (new, introduced by the FIN-F7 fix)

- `SKILL.md:25` now says "take only `report_path`, `summary` and `orca_available`" and `SKILL.md:26` prints a third item. DESIGN 7.6 step 3 (`docs/designs/orchestrator-mode.md:662`) says "take `report_path` and `summary` only", and the scoped addendum (`.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/revisions/chat-output-exception-20261109-133150/design-addendum.md:29`) tells the implementer to "Preserve ... only summary/report_path parsed" and says (`:37`) that "fixers may fix delivery only, never rewrite this authority to bless a failure". Both files hash to the recorded sums (unchanged). The skill and the two authority texts now state incompatible parse rules for the same step.
- The pin that held the old rule was rewritten to match the new text (`tests/commands/test_sweep_command.py:437`, `success-parse-takes-only-report-path-summary-and-orca-available`), so no test fails on the departure. The fix log (`fix-log-cycle1.md`, FIN-F7 block) records the step 3 change but not that it conflicts with DESIGN 7.6 and the addendum; the consolidation's scope note for FIN-F7 named only the exempt reply as needing the owner.
- Why blocking: two authority-level texts contradict the delivered skill on the same step, and rf-qa-qualitative rule 6 grades a contradiction IMPORTANT at the least. The behaviour is harmless (one boolean), so the remedy is an owner choice, not a code defect: (a) revert step 3 and the added step 4 sentence (the pin moves back) and leave FIN-F7 whole OPEN with FIN-F5, or (b) the owner amends DESIGN 7.6 step 3 and addendum `:29` to allow `orca_available` and records it in DESIGN section 13. Counts toward F_1. Also makes `qa-design-conformance-report:C13` and `qa-completeness-report:C4` FAIL below.

### Notes (MINOR or Medium follow-up; never blocking, not rechecked)

- FIN-N2 (MINOR): Rule 5 is inert, so DESIGN 7.2 `:491` ("All four must hold") and the DESIGN section 11 test row (`:760`: "reaching every name in `CLASSES`", "rule 5 four-condition case") are no longer met literally; `test_classify.py:372-376` excludes `working`. The code follows DESIGN open item 6 (`:996`), which DESIGN itself gives for uncaptured names, so this is MINOR. Makes `qa-design-conformance-report:C5` and `qa-test-traceability-report:C8` FAIL on the literal claim.
- FIN-N3 (MINOR): stale comments. `models.py:89` ("The agentWait time, parsed once by `probes.parse_worker_show`") and `classify.py:229` ("parsed once, in probes.parse_worker_show") are false now; `agent_wait`, `agent_wait_present` and `agent_wait_since` (`models.py:78-79`, `:90`) are set by no production code. Makes `qa-maintainability-report:C9` FAIL.
- FIN-N4 (MINOR, follow-up candidate): a contract that is not valid YAML now becomes a record with no fields and its source row still says `read` (`probes.py:680-684`, test id `invalid-yaml`); no note names the parse failure. A plain scalar with `: ` inside (for example `reason: E-QA-FAIL: two tests fail`, and `command:` lines with `Code: src/...`) is invalid YAML. Measured on this repository: 399 of 400 `return-contract.yaml` files parse with `yaml.safe_load`; the one failure is a `ComposerError` in `.dev/brainstorms/20260924-195455-ci-monitor-until-all-checks/return-contract.yaml`. Low risk today, silent when it happens.
- FIN-N5 (MINOR): `yaml.safe_load` (pure Python loader) took 1.7 s for a 1.07 MB flat mapping and 2.9 s for a 1.2 MB flow list on this machine; the per-file cap is 1 MiB but nothing bounds the total over many contracts. Real contracts are a few hundred bytes.
- FIN-N6 (MINOR): `SKILL.md:15` ("relays two facts") and `:57` ("print the counts and the report path") now understate the ordinary reply, which can carry a third item.

## Passage re-read (intended reader)

Read as the coordinator who opens the report (and the person who reads the chat reply). Each passage below was read in the live file; none makes a claim the code does not prove, except where a nit says so. All are MINOR and grouped under FIN-N7.

1. Safe to close cell and the Sessions line (`report.py:40-43`, `:425-426`). A coordinator now sees why a row is or is not safe to close. The line "never prints yes in Phase 1" is true (`classify.py:467-492`). Nit: for a released worker the reason reads `not releasable (terminal_state=released, next_action=none)` with terminal value `no` (`classify.py:483`). "Not releasable" next to `released` still reads as "keep this terminal", the same confusion cycle 0 described; the raw values are printed, so a careful reader can tell, but the phrase does not say "already released".
2. Next inspection, `waiting_signal` (`report.py:54-55`). Each alternative is true for some outcome. Nit: "the Orca agent-wait entry and the worker's last transcript lines" names an input no Phase 1 row can have (`agent_wait` is never set), and for a frozen plan "the contract" is not named by path in the Evidence cell (`classify.py:240-243`), so the reader still has to find it.
3. Next inspection, `fallback` (`report.py:60-61`). A waiting or unknown row now always has a place to look: its own Evidence and Notes, then unscanned sources, then the transcript tail. Never an empty list.
4. No-contract note (`classify.py:86`). A coordinator reading a completed worker row now sees `no contract read for this row; finished needs a parsed contract`, which is the true reason (rule 6 needs a parsed contract; `classify.py:260-280`). Nit: rule 6 also finishes a row on a `guard refused:` body line with no contract (`classify.py:262-266`); that path does not reach the fallback, so the note is not false where it appears.
5. Orca outage line in the report (`report.py:514-516`). True after a mid-run drop. Nit: "became unavailable" is slightly off when Orca never answered (first call failed, `probes.py:350-357`); the sentence stays true because those sources are marked unscanned.
6. Skill ordinary-reply line (`SKILL.md:26`). "Orca was unavailable; the counts may be missing Orca data (see Source coverage in the report)." is true for a full outage and for a mid-run drop, and says "may", not "is". Not advice, no stop, retry, release, merge or removal word (the skill test passes). It conflicts with DESIGN 7.6 and the addendum on the parse rule (FIN-N1) and leaves the exempt reply silent (FIN-F7).
7. Test names. `test_rule_5_never_matches_while_the_agent_wait_names_are_uncaptured`, `test_every_class_name_but_working_is_reached` and `test_sessions_safe_to_close_cell_carries_its_reason` say what they pin. `test_next_inspection_waiting_signal_and_fallback_fit_every_outcome` overclaims: it pins substrings of the two sentences (`test_report.py:1035-1043`), not fit to a row.

- FIN-N7 (MINOR): the nits in points 1, 2, 4, 5 and 7 above.

## Checks

238 check ids of the cycle-0 PASS set, one row each. Result: 232 PASS, 6 FAIL. The six FAIL rows are `qa-design-conformance-report:C5` (FIN-N2), `:C13` and `:C22` (FIN-N1), `qa-test-traceability-report:C8` (FIN-N2), `qa-completeness-report:C4` (FIN-N1) and `qa-maintainability-report:C9` (FIN-N3). A line number that moved, or a count that grew because tests were added, is PASS when the claim still holds. Checks that describe cycle-0 scratch runs or saved artifacts cannot be re-run; for those the row says which relied-on file I confirmed unchanged (edit-set check above).

| Check id | Result |
|---|---|
| qa-design-conformance-report:C1 | PASS: every DESIGN 7.1 name still exists (`parse_worker_show` `probes.py:422`, `Budget`, `_stable`); the deleted helpers were private. |
| qa-design-conformance-report:C2 | PASS: public signatures unchanged; `Budget.spent` (`probes.py:182`) and the optional `budget` argument on private readers are additions, no stated name changed. |
| qa-design-conformance-report:C3 | PASS: `models.py` is not in the edit set. |
| qa-design-conformance-report:C4 | PASS: `models.py` not in the edit set. |
| qa-design-conformance-report:C5 | FAIL (MINOR, FIN-N2): the claim "Rule 5 holds the four conditions one per line" is now false; `classify.py:251-257` returns None and keeps the conditions in a comment. DESIGN open item 6 (`:996`) supports the new behaviour, DESIGN `:491` does not. |
| qa-design-conformance-report:C6 | PASS: the 10 templates are unchanged (`probes.py:47-59`, two `--agent-wait` forms still marked not called); `FORBIDDEN_TOKENS` at `:62`, `ALLOWED_GIT` at `:65`. |
| qa-design-conformance-report:C7 | PASS: `to_json` (`report.py:602-684`) key set unchanged. |
| qa-design-conformance-report:C8 | PASS: section order, header lines, columns, `cell`, `sanitize` and footer unchanged; one fixed line added under the Sessions heading (`report.py:400`), pinned by `test_report.py:1076`, contradicts no stated name or column. |
| qa-design-conformance-report:C9 | PASS: `commands.py` not in the edit set. |
| qa-design-conformance-report:C10 | PASS: `subprocess` only at `probes.py:257`, `:308`; no write verb outside `commands.py` (grep, no output); `yaml` is imported only by `probes.py`; the `classify`/`report` import-ban test passes. |
| qa-design-conformance-report:C11 | PASS: `__init__.py` not in the edit set; registration test passes. |
| qa-design-conformance-report:C12 | PASS: `main.py` not in the edit set. |
| qa-design-conformance-report:C13 | FAIL (FIN-N1): the claim "only `report_path` and `summary` taken" is now false; `SKILL.md:25` takes `orca_available` too, against DESIGN `:662` and addendum `:29`. |
| qa-design-conformance-report:C14 | PASS: the DESIGN 7.6 Test list (`:666`) is unchanged and every item on it still has its test; the moved pin (`test_sweep_command.py:437`) is not on that list. Cycle-0 mutation runs cannot be re-run; the tests they relied on still exist and pass. |
| qa-design-conformance-report:C15 | PASS: the exempt-reply rule is unchanged (`SKILL.md:35-51`; `pragmatic.md` not in the edit set; 124 command tests pass). The step 3 departure is FIN-N1, outside this check's claim (style edit, exempt rule, pins). |
| qa-design-conformance-report:C16 | PASS: `WORKER-CONTRACT.md` not in the edit set. |
| qa-design-conformance-report:C17 | PASS: `cmp` of the guide and its plugin copy is clean; neither is in the edit set. |
| qa-design-conformance-report:C18 | PASS: `.gitignore` not in the edit set; `git check-ignore` of `.dev/tasks` paths prints nothing. |
| qa-design-conformance-report:C19 | PASS: the DESIGN-named tests (`test_fr010_*`, `test_path_b_*`, the transcript and `worker_show` time tests, `test_collect_worker_list_source_rows_and_truncated`) all still exist; the two renamed tests were not named by DESIGN (grep of DESIGN finds neither old name). |
| qa-design-conformance-report:C20 | PASS: I re-ran lint, scoped pytest (3242 passed), verify-sync; the three full-run failures sit in files the fix did not touch. |
| qa-design-conformance-report:C21 | PASS: `OQ-10-pipx-decision.md` and `sweep-help-pipx.txt` not in the edit set. |
| qa-design-conformance-report:C22 | FAIL (FIN-N1): a scan for departures with no owner decision now finds one that is not MINOR (skill step 3 against DESIGN `:662` and addendum `:29`); the cycle-0 result "all graded MINOR" no longer holds. |
| qa-design-conformance-report:C23 | PASS: the saved live-check JSON is unchanged (not in the edit set); no live run made. |
| qa-design-conformance-report:C24 | PASS: `WorktreeState.frozen` and `removable` unchanged; rule 5 reachability is still the F6 note. |
| qa-design-conformance-report:C25 | PASS: 0 `.claude/` paths staged; `.dev/tasks` not ignored; my /tmp copies are deleted (`ls -d /tmp/t333-mut` fails); the cycle-0 copies cannot be re-checked. |

| qa-test-traceability-report:C1 | PASS: the DESIGN-named tests still resolve; the two tests the fix renamed (`test_every_class_name_but_working_is_reached` `test_classify.py:372`, `test_rule_5_never_matches_...` `:436`) are not named in DESIGN. |
| qa-test-traceability-report:C2 | PASS: `tests/sweep/conftest.py` is not in the edit set; the guard still applies to the new tests (they pass). |
| qa-test-traceability-report:C3 | PASS: `test_readonly.py` not in the edit set; no new integration-marked test. |
| qa-test-traceability-report:C4 | PASS: `test_readonly.py` not in the edit set. |
| qa-test-traceability-report:C5 | PASS: `test_readonly.py` not in the edit set. |
| qa-test-traceability-report:C6 | PASS: the ten-template pin and negatives are untouched; three tests were added at `test_probes_allowlist.py:1552`, `:1731`, `:1788`. |
| qa-test-traceability-report:C8 | FAIL (MINOR, FIN-N2): the claim "one case per rule and `CLASSES` coverage, rule 5" is false for `working` now; `test_classify.py:372-376` expects every class except `working`, and the rule 5 test (`:436`) pins non-matching. |
| qa-test-traceability-report:C9 | PASS: the FR-010 fixtures are unchanged and `test_classify.py` passes (166 passed); no exact note list changed. |
| qa-test-traceability-report:C10 | PASS: D9, SP-29, R2-B1, R3-B1 and R3-B2 fixtures unchanged; 166 passed. |
| qa-test-traceability-report:C11 | PASS: `test_report.py` 51 passed; the next-inspection map test (`:1010`) and SP-24 pins still pass; three tests added (`:1035`, `:1046`, `:1080`). |
| qa-test-traceability-report:C12 | PASS: `test_cli_contract.py` 94 passed; `test_waiting_lists_hold_row_ids_only` (`:1065`) now builds waiting (a) from a blocked contract and still pins both lists as row ids. |
| qa-test-traceability-report:C13 | PASS: `test_cli_registration.py` not in the edit set. |
| qa-test-traceability-report:C14 | PASS: the budget-exhaustion publish test is untouched; the new budget test is separate. |
| qa-test-traceability-report:C15 | PASS: `tests/skills/test_worker_contract.py` not in the edit set. |
| qa-test-traceability-report:C16 | PASS: routing-table tests not in the edit set. |
| qa-test-traceability-report:C17 | PASS: the DESIGN 7.6 assertions in `test_sweep_command.py` still exist; only a skill-only pin moved (FIN-N1 covers that pin). |
| qa-test-traceability-report:C18 | PASS: the exempt-reply positive-case pins are unchanged (`_PIN_PARAMS`, 124 passed). |
| qa-test-traceability-report:C19 | PASS: the negative and exclusion pins are unchanged. |
| qa-test-traceability-report:C20 | PASS: the style bullets are asserted on the real `pragmatic.md`, which is not in the edit set. |
| qa-test-traceability-report:C21 | PASS: scratch mutation run, cannot be re-run; style, command and exempt-reply text it mutated are unchanged, and the one skill sentence the fix changed (step 3) was not among the 20 mutations. |
| qa-test-traceability-report:C22 | PASS: scratch run, cannot be re-run as a whole; I re-ran the "three reads" mutation on a private copy and it is still caught (`assert 3 == 2`); the other mutated code (argv and env, full page, `FINAL:` rule, window bounds, join guards, publish) is not in the edit set apart from `_ledger_has_final`, which is unchanged. |
| qa-test-traceability-report:C23 | PASS: the two severity modules are not in the edit set (`git status` on both prints nothing). |
| qa-test-traceability-report:C24 | PASS: the ruff-module argument concerns `tests/cli/eval`, not in the edit set. |
| qa-test-traceability-report:C25 | PASS: `tests/sweep/fixtures` not in the edit set. |
| qa-test-traceability-report:C26 | PASS: gates reproduced: 3242 passed over the wider scoped set (count grew), `ruff check` clean, `ruff format --check` clean on the sweep files, `make verify-sync` in sync. |
| qa-validation-evidence-report:C1 | PASS: `make verify-sync` re-run by me: "All components in sync." |
| qa-validation-evidence-report:C2 | PASS: `uv run ruff check .` re-run: "All checks passed!" |
| qa-validation-evidence-report:C3 | PASS: `ruff format --check src/ tests/` re-run: the same 12 Markdown files as the fix log, compared by path. |
| qa-validation-evidence-report:C4 | PASS: none of the 12 is in the edit set. |
| qa-validation-evidence-report:C5 | PASS: the 16 sweep Python files (source, tests, command test) are already formatted. |
| qa-validation-evidence-report:C6 | PASS: scoped pytest re-run: 3242 passed, exit 0 (recorded 3220; the count grew with the added tests). |
| qa-validation-evidence-report:C7 | PASS (note): the Phase 14 records are older than the fix, but the gates were re-run on the current tree (lint, 3242 passed, verify-sync) by me and by the fix log (sections 2 to 4 and the repair pass); the claim that recorded evidence matches the delivered content holds through those re-runs. |
| qa-validation-evidence-report:C8 | PASS: the two ruff-module failures are in `tests/cli/eval`, not in the edit set; the venv still has no ruff module for them (fix log section 4). |
| qa-validation-evidence-report:C9 | PASS: the timing test is in an untouched hook suite; it passed in the fix run (fix log); not re-run by me. |
| qa-validation-evidence-report:C10 | PASS: scoped grep re-run: no output, exit 1. |
| qa-validation-evidence-report:C11 | PASS: full-tree count re-run: 168. |
| qa-validation-evidence-report:C12 | PASS: `sweep-help-pipx.txt` and the owner record are not in the edit set. |
| qa-validation-evidence-report:C13 | PASS: the saved help output still matches the build: `commands.py` (options) is not in the edit set. |
| qa-validation-evidence-report:C14 | PASS: 0 `.claude/` paths staged; `git status --short -- .claude` prints nothing. |
| qa-scope-report:C1 | PASS: untracked files under `src tests docs plugins` (without `__pycache__`) are 41 = the 4 baseline entries plus 37 (`comm` against `baseline-untracked.txt`); no file was added. |
| qa-scope-report:C2 | PASS: no tracked file is in the edit set. |
| qa-scope-report:C3 | PASS: the fix added no file; the six modules and test files are the same set. |
| qa-scope-report:C4 | PASS: the only files changed after the Phase 14 record are the nine listed in the edit-set check, plus three with HEAD-identical content. |
| qa-scope-report:C5 | PASS: the WC-9 grep over the sweep package and primitives prints nothing. |
| qa-scope-report:C6 | PASS: `WORKER-CONTRACT.md` not in the edit set. |
| qa-scope-report:C7 | PASS: `tests/skills/test_worker_contract.py` not in the edit set. |
| qa-scope-report:C8 | PASS: `commands.py` not in the edit set; no option added. |
| qa-scope-report:C9 | PASS: 10 templates unchanged. |
| qa-scope-report:C10 | PASS: the one guessed-key heuristic (S-m2) is deleted (`probes.py:432-434`); the new budget thread and `yaml.safe_load` implement DESIGN NFR-007 and the FIN-F9 fix, not speculation. |
| qa-scope-report:C11 | PASS: `pragmatic.md` not in the edit set. |
| qa-scope-report:C12 | PASS: WC-16 text not in the edit set. |
| qa-scope-report:C13 | PASS: routing rows untouched; `cmp` clean. |
| qa-scope-report:C14 | PASS: grep for `chat-summary|exempt|coordinator assignment` over `src/superclaude/cli` hits only roadmap, recommend and sprint code, none in `cli/sweep`. |
| qa-scope-report:C15 | PASS: the DESIGN hash equals the recorded sum. |
| qa-scope-report:C16 | PASS: scoped pytest re-run by me (3242 passed vs recorded 3220). |
| qa-scope-report:C17 | PASS: the files behind the three full-run failures are not in the edit set. |
| qa-scope-report:C18 | PASS: pipx record and help output not in the edit set. |
| qa-scope-report:C19 | PASS: 0 `.claude/` staged; the project `.claude/` skill copy equals the source (`cmp` clean). |

| qa-readonly-safety-report:C1 | PASS: process starts only at `probes.py:257` and `:308` (`subprocess.run`, list argv); grep finds no `Popen`, `os.system` or `shell=` outside docstrings. |
| qa-readonly-safety-report:C2 | PASS: `check_orca_argv` runs at `probes.py:254` before the process; `_orca` is still the one Orca seam. |
| qa-readonly-safety-report:C3 | PASS: allowlist templates unchanged (`probes.py:47-59`). |
| qa-readonly-safety-report:C4 | PASS: `FORBIDDEN_TOKENS` at `probes.py:62`, checked at `:217`. |
| qa-readonly-safety-report:C5 | PASS: the binary rule is untouched by the edits. |
| qa-readonly-safety-report:C6 | PASS: `ALLOWED_GIT` (`:65`), `check_git_args` (`:227-230`) and the `git --no-optional-locks -C` prefix with `GIT_OPTIONAL_LOCKS=0` (`:305-306`) are intact. |
| qa-readonly-safety-report:C7 | PASS: scratch run on a /tmp repo, cannot be re-run; `_git` and `ALLOWED_GIT` are intact (read above), so what the run relied on is unchanged. |
| qa-readonly-safety-report:C8 | PASS: grep of `classify`, `probes`, `report`, `models`, `__init__` for write verbs prints nothing; the only write is `commands.py:170`. |
| qa-readonly-safety-report:C9 | PASS: `open(` only at `probes.py:559`, `:792`, `:856`, all `"rb"` (lines moved); `yaml.safe_load` reads a string already read. |
| qa-readonly-safety-report:C10 | PASS: `commands.py` not in the edit set. |
| qa-readonly-safety-report:C11 | PASS: the new `except (yaml.YAMLError, RecursionError, ValueError)` (`probes.py:682`) wraps only `yaml.safe_load`; no allowlist call sits inside any `ValueError` handler. |
| qa-readonly-safety-report:C12 | PASS: `main.py` not in the edit set. |
| qa-readonly-safety-report:C13 | PASS: tests, lint and sync re-run: 3242 passed, ruff clean, verify-sync in sync. |
| qa-readonly-safety-report:C14 | PASS: `test_readonly.py` not in the edit set; it passes. |
| qa-readonly-safety-report:C15 | PASS: skill frontmatter `allowed-tools` literal unchanged (`SKILL.md:4`); the command is unchanged. |
| qa-readonly-safety-report:C18 | PASS: the files behind the three full-run failures are not in the edit set. |
| qa-readonly-safety-report:C19 | PASS: scratch runs of cycle 0, cannot be re-run; no repository file differs unexpectedly (edit-set check). |
| qa-fork-never-commit-report:C1 | PASS: `git rev-parse HEAD` equals `artifacts/base-commit.txt` (`5dc29d23b15eb7db4ead50623bb409f696a0d7d3`). |
| qa-fork-never-commit-report:C2 | PASS: `git diff --cached --name-only -- .claude/` counts 0. |
| qa-fork-never-commit-report:C3 | PASS: `git check-ignore -v` on `.dev/tasks`, `.dev/tasks/to-do`, the package and `base-commit.txt` prints nothing (exit 1). |
| qa-fork-never-commit-report:C4 | PASS: `grep -nw gh` over the command, skill and package prints nothing. |
| qa-fork-never-commit-report:C5 | PASS: no `{owner}` or `{repo}` placeholder; the only `:repo` hit is the regex `(?:report-dir` at `models.py:23`, which the fix did not touch. |
| qa-fork-never-commit-report:C6 | PASS: no push, fetch or PR reference to SuperClaude-Org; the only hits are `projectId` strings in captured Orca fixtures (`tests/sweep/fixtures/captured-worktree-*.json`), unchanged. |
| qa-fork-never-commit-report:C7 | PASS: the `SKILL.md` edit adds no staging instruction. |
| qa-fork-never-commit-report:C8 | PASS: the autouse guard in `conftest.py` is unchanged; the new tests call no git and pass under it. |
| qa-fork-never-commit-report:C9 | PASS: pipx record and output not in the edit set. |
| qa-fork-never-commit-report:C10 | PASS: the failing tests live in `tests/cli/eval` and a hook suite, outside the edit set. |
| qa-fork-never-commit-report:C11 | PASS: `make verify-sync` in sync; ruff clean. |
| qa-fork-never-commit-report:C12 | PASS: scoped folders pass (3242). |
| qa-fork-never-commit-report:C13 | PASS: cycle-0 agent's own runs, cannot be re-run; HEAD still equals base and nothing unexpected changed. |
| qa-fork-never-commit-report:C14 | PASS (note F1 stays): `.dev/tasks` is not ignored; files under it, including this cycle's QA files, are still untracked or unstaged until the orchestrator runs `git add .dev/tasks`. |
| qa-coordinator-usefulness-report:C1 | PASS: `NO_RECORDS` ("not an all-clear", `report.py:29`) and the waiting sections are unchanged. |
| qa-coordinator-usefulness-report:C10 | PASS: coverage lines (remote hosts, Messages, lower bounds, `WORKTREES_LINE`) unchanged (`report.py:29-35`, `:521-525`). |
| qa-coordinator-usefulness-report:C11 | PASS (note): the exempt reply is still counts and path alone; the ordinary reply may add one fact line (`SKILL.md:26`), no advice word; FIN-N1 and FIN-N6 cover the departure. |
| qa-coordinator-usefulness-report:C12 | PASS: failure attribution holds (files untouched); the sweep and command tests pass. |
| qa-failure-clarity-report:C1 | PASS: `commands.py` not in the edit set. |
| qa-failure-clarity-report:C2 | PASS: `commands.py` not in the edit set. |
| qa-failure-clarity-report:C3 | PASS: no-`--run` outage exit 2 path is in `commands.py`/`probes.bind_run`, unchanged. |
| qa-failure-clarity-report:C6 | PASS: `PAGE_LINE` unchanged (`report.py:32`). |
| qa-failure-clarity-report:C8 | PASS: a `call_failed` source still gives an unscanned row and `could not determine`; tests pass. |
| qa-failure-clarity-report:C9 | PASS: missing-folder behaviour unchanged. |
| qa-failure-clarity-report:C10 | PASS: an unreadable transcript still gives `NOTE_TRANSCRIPT_UNREADABLE` (`classify.py:83`); `_transcript` now takes the budget (`probes.py:1355`), tests pass. |
| qa-failure-clarity-report:C11 | PASS: `_publish` unchanged. |
| qa-failure-clarity-report:C12 | PASS: `_publish` unchanged. |
| qa-failure-clarity-report:C15 | PASS: exit codes live in `commands.py` (unchanged); skill step 5 unchanged. |
| qa-failure-clarity-report:C16 | PASS: `commands.py` not in the edit set. |
| qa-failure-clarity-report:C17 | PASS: header "READ ONLY" line and "Inspection only." footer unchanged (`report.py:181`, `:531`). |
| qa-failure-clarity-report:C18 | PASS: failure-path tests pass (3242); the count grew. |
| qa-failure-clarity-report:C19 | PASS: argument unchanged and still holds. |
| qa-failure-clarity-report:C20 | PASS: `ruff check` and `ruff format --check` on the sweep files re-run: clean, 16 files formatted. |

| qa-maintainability-report:C2 | PASS: `_remaining` is shared by `call_timeout` and `spent` (`probes.py:171-184`); the budget argument is threaded, not copied. |
| qa-maintainability-report:C3 | PASS: `NOTE_NO_CONTRACT` has one definition (`classify.py:86`) and one test literal (`test_classify.py:94`); `_OUTAGE_SENTENCE` is the pin of the skill sentence. |
| qa-maintainability-report:C4 | PASS: no path or environment rule added. |
| qa-maintainability-report:C5 | PASS: the new comments give reasons (`classify.py:252-256`, `:328`, `probes.py:432-434`). |
| qa-maintainability-report:C6 | PASS (note): new comments point at DESIGN open item 6 and step 1.0a; test comments cite `FIN-F1`, `FIN-F3`, `FIN-F7`, `FIN-F8`, which sit in `consolidated-findings-cycle0.md` on disk. |
| qa-maintainability-report:C7 | PASS: each new decision has a why line: `_yaml_top` docstring (`probes.py:673-679`), `_stable` docstring (`:543-545`), `spent` docstring (`:183`). |
| qa-maintainability-report:C8 | PASS: names say what the code does; `_rule_working` returns None, which its comment states (`classify.py:252-256`). |
| qa-maintainability-report:C9 | FAIL (MINOR, FIN-N3): `agent_wait`, `agent_wait_present` and `agent_wait_since` are now set by no production code, and the comments at `models.py:89` and `classify.py:229` still say `parse_worker_show` parses the wait time. |
| qa-maintainability-report:C10 | PASS: no `type: ignore` was added; the eight in the package are the coded ones that existed (`report.py:86`, `:90`, `:150`, `:196`, `:365`, `:676`, `classify.py:513`, `probes.py:811`). |
| qa-maintainability-report:C11 | PASS: `main.py` and `__init__.py` not in the edit set. |
| qa-maintainability-report:C12 | PASS: the duplicated style and skill text is still pinned; the new skill sentences are pinned at `test_sweep_command.py:526-531`, `:559-569`. |
| qa-maintainability-report:C13 | PASS: new tests reuse `_change_on_read`, `_stock_contract_run`, `_collect` and `sweep_root.contract`. |
| qa-maintainability-report:C14 | PASS: ruff check clean; "16 files already formatted". |
| qa-maintainability-report:C15 | PASS: `make verify-sync` in sync. |
| qa-maintainability-report:C16 | PASS: sweep and command tests pass (166, 51, 254, 94, 124 in the five edited modules; 3242 in the wider run). |
| qa-maintainability-report:C17 | PASS: cycle-0 scratch copy, cannot be re-run; no repository file differs unexpectedly (edit-set check). |
| qa-cross-artifact-report:C1 | PASS: WC-16 files not in the edit set. |
| qa-cross-artifact-report:C2 | PASS: `WORKER-CONTRACT.md` and DESIGN unchanged (hash and edit-set check). |
| qa-cross-artifact-report:C3 | PASS: `WORKER-CONTRACT.md`, `sweep.md` not in the edit set. |
| qa-cross-artifact-report:C4 | PASS: `sweep.md:22` and WC-16 unchanged. |
| qa-cross-artifact-report:C5 | PASS: the four flags are unchanged in `commands.py`, `sweep.md` and `SKILL.md:19`. |
| qa-cross-artifact-report:C6 | PASS: limits, defaults and the Run id regex are in unchanged code and text. |
| qa-cross-artifact-report:C7 | PASS: `commands.py` unchanged. |
| qa-cross-artifact-report:C8 | PASS: `to_json` unchanged; the skill's step 3 reads one more existing key, `orca_available` (`report.py:621`). |
| qa-cross-artifact-report:C9 | PASS: owner decision records not in the edit set. |
| qa-cross-artifact-report:C10 | PASS: the exempt-reply decision chain (decision, addendum, style, skill, test) is unchanged. |
| qa-cross-artifact-report:C11 | PASS: the common-rule pins on both files pass (124 passed). |
| qa-cross-artifact-report:C12 | PASS: the seven table sites and the single exception are in `pragmatic.md` (unchanged) and pinned. |
| qa-cross-artifact-report:C13 | PASS: exclusion pins unchanged. |
| qa-cross-artifact-report:C14 | PASS: error codes and authority live in `commands.py` (unchanged); the exception itself still changes no Python. |
| qa-cross-artifact-report:C15 | PASS: no text claims a HOME activation. |
| qa-cross-artifact-report:C16 | PASS: routing rows and plugin copy unchanged; `cmp` clean. |
| qa-cross-artifact-report:C17 | PASS: `CHANGELOG.md:11-15` still true; the skill prints the counts and path and recommends nothing (the extra outage line is FIN-N6). |
| qa-cross-artifact-report:C18 | PASS: docs not in the edit set. |
| qa-cross-artifact-report:C19 | PASS: never-as-worker list copies unchanged. |
| qa-cross-artifact-report:C20 | PASS: pytest, ruff and verify-sync reproduced by me. |
| qa-cross-artifact-report:C21 | PASS: failure argument unchanged. |
| qa-cross-artifact-report:C22 | PASS: inventory equals disk (37 untracked plus 4 baseline). |
| qa-cross-artifact-report:C23 | PASS: the skill's failure handling matches the code (exit 0/1/2 in `commands.py`); the skill does not say what to do when `orca_available` is missing from the JSON (nit, covered by FIN-N1). |
| qa-cross-artifact-report:C24 | PASS: pipx evidence not in the edit set. |
| qa-completeness-report:C1 | PASS: the Phase 1 pre-step output files exist (`artifacts/readonly-probe.md`, `pr422-409-check.md`, `owner-decisions.md`). |
| qa-completeness-report:C2 | PASS: the six modules exist with every DESIGN 7.1 name. |
| qa-completeness-report:C3 | PASS: conftest, fixtures and test modules exist; every DESIGN-named test exists. |
| qa-completeness-report:C4 | FAIL (FIN-N1): the skill no longer matches DESIGN 7.6 step 3 ("`report_path` and `summary` only", `docs/designs/orchestrator-mode.md:662`). |
| qa-completeness-report:C5 | PASS: `artifacts/pr422-409-check.md` exists. |
| qa-completeness-report:C6 | PASS: WC-16 and the never-as-worker line are in untouched files. |
| qa-completeness-report:C7 | PASS: routing rows R1 to R8 untouched; parity `cmp` clean. |
| qa-completeness-report:C8 | PASS: sync and verify-sync re-run in sync; nothing staged under `.claude/`. |
| qa-completeness-report:C9 | PASS: the same 12 pre-existing format failures, none in the change set. |
| qa-completeness-report:C10 | PASS: scoped run passes (3242); the failure argument unchanged. |
| qa-completeness-report:C11 | PASS: step 1.28 grep re-run: no output. |
| qa-completeness-report:C12 | PASS: `artifacts/sweep-help-pipx.txt` exists, unchanged. |
| qa-completeness-report:C13 | PASS: `.gitignore` unchanged; `.dev/sweeps/` lines intact. |
| qa-completeness-report:C14 | PASS: every file, constant set and JSON key DESIGN section 7 names is still delivered. |
| qa-completeness-report:C15 | PASS: the canonical style edit and its seven sites unchanged. |
| qa-completeness-report:C16 | PASS: the skill still carries the same exempt rule (`SKILL.md:35-51`). |
| qa-completeness-report:C17 | PASS: no new module, detector or hook; the fix edits existing files only. |
| qa-completeness-report:C18 | PASS: the evidence files exist and say what was run; the five regenerated result files carry the live counts (166, 51, 254, 94, 124), which I re-ran. |
| qa-completeness-report:C19 | PASS: historical approval records unchanged. |
| qa-completeness-report:C20 | PASS: the two owner-approved contract edits are in untouched files. |
| qa-completeness-report:C21 | PASS: 37 untracked files equal the inventory's new list; the 12 edited tracked files are unchanged. |
| qa-completeness-report:C22 | PASS: no step recorded as done lost an output file (the fix only rewrote five result files in place and kept all names). |

| qa-operator-actionability-report:C1 | PASS: command, WC-16 and guide text unchanged. |
| qa-operator-actionability-report:C2 | PASS: flags and defaults in `sweep.md` still match `commands.py` and `probes.py` (both unchanged where they carry them). |
| qa-operator-actionability-report:C3 | PASS: report location rules live in `commands.py` (unchanged). |
| qa-operator-actionability-report:C7 | PASS: no text about messaging or closing person-started sessions changed. |
| qa-operator-actionability-report:C8 | PASS: style and skill assignment rule unchanged on both sides. |
| qa-operator-actionability-report:C9 | PASS: exclusion contexts unchanged; only an assigned coordinator's final success drops the table. |
| qa-operator-actionability-report:C11 | PASS: no text claims live recognition; the step-7.10 evidence file is unchanged. |
| qa-operator-actionability-report:C12 | PASS: the `(not observed in Phase 1)` mark is still in step 4 and the exempt reply (`SKILL.md:26`, `:43`). |
| qa-operator-actionability-report:C15 | PASS: stalled (proved) and fenced still cannot appear: `fenced_evidence` keeps its default `unreadable` and `worker_done_seen` its default None (`models.py:86-87`); grep finds no assignment of either in `probes.py`. |
| qa-operator-actionability-report:C16 | PASS: the failure argument concerns files outside the edit set. |
| qa-operator-actionability-report:C17 | PASS: tests, lint and sync pass on the sweep surface (re-run). |
| qa-evidence-quality-report:C1 | PASS: the join key read (`assigneeHandle`) is unchanged at `probes.py:438`; fixtures unchanged. |
| qa-evidence-quality-report:C2 | PASS: `dispatchedAt`, `completedAt` reads unchanged at `probes.py:439-440`. |
| qa-evidence-quality-report:C3 | PASS: page and cursor handling untouched. |
| qa-evidence-quality-report:C4 | PASS: unknown-Run handling untouched. |
| qa-evidence-quality-report:C5 | PASS: worktree path and version-file rules untouched. |
| qa-evidence-quality-report:C6 | PASS: the parser reads only fields present in captured fixtures (`projection.liveness.verdict`, `projection.outcome`, `dispatch.*`); it now reads one field fewer, `agentWait`. |
| qa-evidence-quality-report:C8 | PASS: the project-folder key rule is untouched. |
| qa-evidence-quality-report:C12 | PASS: disclosure of unobserved shapes untouched; the `agentWait` names are now disclosed as unread in code (`probes.py:432-434`). |
| qa-evidence-quality-report:C13 | PASS: `UNATTENDED_EXPECT` file not in the edit set. |
| qa-evidence-quality-report:C14 | PASS: the 168 count re-run now; 0 hits in the sweep primitives. |
| qa-evidence-quality-report:C15 | PASS: DESIGN and 1.0a-facts files unchanged (hash and edit-set check). |
| qa-evidence-quality-report:C16 | PASS: failure argument unchanged. |
| qa-evidence-quality-report:C17 | PASS: tests, `ruff check`, `ruff format --check` and `make verify-sync` re-run by me. |
| qa-numbers-metrics-report:C1 | PASS: never-as-worker list files not in the edit set. |
| qa-numbers-metrics-report:C2 | PASS: 10 templates, 7 verbs, 4 not called: unchanged (`probes.py:47-59`). |
| qa-numbers-metrics-report:C3 | PASS: `tests/skills/test_worker_contract.py` not in the edit set. |
| qa-numbers-metrics-report:C4 | PASS: routing rows untouched. |
| qa-numbers-metrics-report:C5 | PASS: still six modules. |
| qa-numbers-metrics-report:C6 | PASS: publish messages and exit codes are in `commands.py`, `sweep.md` and the skill, unchanged. |
| qa-numbers-metrics-report:C7 | PASS: DESIGN hash unchanged ("Total: 10 deviations."). |
| qa-numbers-metrics-report:C8 | PASS: DESIGN hash unchanged ("Total: 23 open items."). |
| qa-numbers-metrics-report:C9 | PASS: the byte limits are unchanged constants (`probes.py:69-75`). |
| qa-numbers-metrics-report:C10 | PASS: `Budget` defaults (50, 90 s, 10 s) unchanged. |
| qa-numbers-metrics-report:C11 | PASS: report-name limit is in `commands.py` (unchanged). |
| qa-numbers-metrics-report:C12 | PASS: window, Run id and timeout numbers unchanged in `sweep.md`, `SKILL.md:23-24` and the code. |
| qa-numbers-metrics-report:C13 | PASS: still eight classes, 6 package states, 9 rules (`classify.py:333-343`), ten dimensions. |
| qa-numbers-metrics-report:C14 | PASS (count drift): the inventory sizes were recorded before the fix (`final-inventory.md:139-143`); the new-file line total grew because the fix added lines, which does not make the recorded recount wrong at the time. |
| qa-numbers-metrics-report:C15 | PASS (count drift): the test counts grew (command tests 121 to 124, sweep modules 166, 51, 254, 94; scoped run 3220 to 3242); each added test is named in the fix log and exists. |
| qa-numbers-metrics-report:C16 | PASS: `pragmatic.md` not in the edit set, so the style counts are unchanged. |
| qa-numbers-metrics-report:C17 | PASS: the Phase 14 numbers are a dated record and are unchanged; the 168 grep count holds now. |
| qa-numbers-metrics-report:C18 | PASS: the saved live-check JSON and report are not in the edit set; no live run made. |
| qa-numbers-metrics-report:C19 | PASS: fixtures and `SOURCES.md` not in the edit set. |

Verdict and counts for the tables: 238 rows, 232 PASS, 6 FAIL.

## Self-audit

## Self-Audit

**(a) Reliance list: what I did not re-derive.**
- For the checks on files the fix did not touch (about 150 of the 238: `commands.py`, `models.py`, DESIGN, SPEC, `pragmatic.md`, `sweep.md`, WC-16, the guide and its plugin copy, fixtures, CHANGELOG, docs) I relied on the unchanged-file argument. My own evidence for it: `find -newer` over the repository lists only the nine fix files plus three files whose content equals HEAD; `sha256sum` of the four immutable inputs equals the fix log's sums; `cmp` of the two guide copies and of the skill source against `.claude/` is clean. I did not reproduce the orchestrator's 126-file sha256 baseline (not on disk), and I did not re-read each cycle-0 report's reasoning for those checks.
- Checks that describe cycle-0 scratch runs or saved artifacts (readonly C7, C19; fork C13; maintainability C17; test-traceability C21, C22 in part; design C23, C25; numbers C18) cannot be re-run. I confirmed that the files they relied on are unchanged, and I re-ran one of the mutations of test-traceability C22.

**(b) Independent semantic checks (tool evidence).**
- Live behaviour of all nine F_0 findings, read in `probes.py`, `classify.py`, `report.py` and `SKILL.md` and not taken from the fix log (FIN-F1 to FIN-F9 above).
- Two private-copy mutations under /tmp (deleted): three reads in `_stable` and no budget break; both caught by the named tests.
- DESIGN and addendum comparison found FIN-N1: `docs/designs/orchestrator-mode.md:662` and `design-addendum.md:29` against `SKILL.md:25`; no cycle-0 or fix-log text says so.
- `yaml.safe_load` experiments (colon in a plain scalar raises `ScannerError`; timing 1.7 s and 2.9 s on about 1 MB; 399 of 400 existing contracts parse) behind FIN-N4 and FIN-N5.
- Re-run gates: ruff check, ruff format list (same 12 files), 3242 passed, per-module counts (166, 51, 254, 94, 124) that match the five regenerated result files, `make verify-sync`, the two greps, the untracked-file `comm` against the baseline.

**Confidence (computed, rough counts):** Verified individually on live files this pass: about 83 of the 238 check rows plus the 9 findings, so 92 of 247 items | Unverifiable (scratch runs, cannot be re-run): 9 rows, each accounted for by the unchanged-input confirmation above | Unchecked: 0 | Confidence on individual re-checks: about 39% (92 of 238 rows plus findings, after taking out the 9 unverifiable). The other rows rest on the edit-set argument: "no change found", not a second review. By the lens's own rule (confirm from disk that nothing the check relied on changed) all 238 rows are accounted for. The verdict is FAIL because of FIN-F5, FIN-F7 and FIN-N1; more rounds could only add findings, so I did not run them.

**Tool engagement:** Read: about 45 | Grep: about 30 | Glob: 0 | Bash: 18 (each call targeted a row or finding above; the Read count exceeds the 9 findings plus the rows I judged individually, and the unchanged-file rows rest on the `find`, hash and `cmp` calls, not on one call per row).

No web research was done; Tavily was not needed.

## Result

- F_1 (open blocking findings): FIN-F5 (owner decision on the pinned banner), FIN-F7 (exempt reply, needs the owner of the output style and the addendum), FIN-N1 (skill step 3 against DESIGN 7.6 and the addendum). |F_1| = 3, down from |F_0| = 9. Seven of the nine F_0 findings are RESOLVED (FIN-F1, F2, F3, F4, F6, F8, F9); FIN-F5 and FIN-F7 are the two that stay OPEN.
- Six of the 238 cycle-0 PASS checks now FAIL (Checks table): three follow from the blocking FIN-N1 (`qa-design-conformance-report:C13`, `:C22`, `qa-completeness-report:C4`), two from FIN-N2 (`qa-design-conformance-report:C5`, `qa-test-traceability-report:C8`), one from FIN-N3 (`qa-maintainability-report:C9`). The two FIN-N2 rows and the FIN-N3 row are MINOR.
- Not blocking: FIN-N2 to FIN-N7.

Verdict: FAIL
Blocking count: 3
