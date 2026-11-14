# Cycle-1 re-check verification (rf-qa, fix_authorization: false)

**Topic:** sweep Phase 1 final gate, cycle 1 re-check after the owner's halt resolution
**Date:** 2026-11-13
**Phase:** fix-cycle (re-check)
**Fix cycle:** 1 (re-check after halt)
**Live DESIGN sha256 at start:** 83816a69c6c21ad80cd11b7881bb6a54c67c9f3919361aa77e5057aaacc7d45d (equals the "Halt resolution" sum in fix-log-cycle1.md)

Status: COMPLETE (Verdict: FAIL, Blocking count: 2; the two open findings are FIN-F5 and FIN-F7, both expected)

---

`T` = `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653`. All paths are relative to the repository root. Every finding and check below is judged on the live files; the fix log, the halt-resolution record and the first verifier report (`T/qa/final/verify-cycle1-rf-qa.md`) were read as evidence and not trusted.

## Basis (what I read and ran)

- Read in full: `consolidated-findings-cycle0.md` (the F_0 block, FIN-F1 to FIN-F9), `fix-log-cycle1.md` (including "Repair pass after review 1" and "Halt resolution"), `cycle-ledger.md` (the 238-id cycle-0 PASS set), `FINAL-GATE-halt-resolution-decision.md`, the first verifier report, and the check rows of all 14 cycle-0 reports.
- Live files read: DESIGN `docs/designs/orchestrator-mode.md` `:205-216`, `:474-497`, `:608-647`, `:650-667`, `:754-765`, `:996`; addendum `design-addendum.md:20-46`; `pragmatic.md:18-29`; `SKILL.md` (whole); `sweep.md:10-21`; `probes.py` (`:1-83`, `:160-270`, `:395-465`, `:530-600`, `:660-730`, `:1018-1110`, `:1160-1240`, `:1290-1362`); `classify.py` (`:40-95`, `:150-365`, `:440-510`); `models.py:55-115`; `report.py` (`:26-75`, `:130-205`, `:392-437`, `:500-530`, `:555-600`); tests `test_report.py:1003-1095`, `test_probes_allowlist.py:1725-1825`, `test_cli_contract.py:1060-1096`, `test_classify.py:272-330`, `:356-386`, `:428-460`, `:600-660`.
- Commands run: `uv run pytest tests/sweep tests/commands tests/core tests/skills tests/recommend -q`: **3239 passed**, exit 0 (the first re-check saw 3242; the difference is exactly the three FIN-F7 tests the owner's revert removed; the fix log's 3246 adds the 7 tests of `tests/cli/test_verify_sync_hooks.py`, which I ran separately: 7 passed). `uv run ruff check .`: All checks passed. `ruff format --check src/superclaude/cli/sweep tests/sweep tests/commands`: 25 files already formatted. `ruff format --check src/ tests/`: 12 files would be reformatted, the same 12 Markdown files as `phase14-lint.md` (list diff: identical), none edited here.
- Collected counts equal the saved result files: `test_classify.py` 166, `test_report.py` 51, `test_probes_allowlist.py` 254, `test_cli_contract.py` 94, `test_sweep_command.py` 121 (`test-classify.txt`, `test-report.txt`, `test-probes-allowlist.txt`, `test-cli-contract.txt`, `test-sweep-command.txt`: 166, 51, 254, 94, 121 passed; `test-sweep-command-summary.md:9` and `:138` both say 121 again). Sweep tests plus command test: 713 (cycle 0 saved 694; counts moved because the fix added tests).
- Immutable sources: SPEC, addendum and revision `BUILD-REQUEST.md` `sha256sum` equal the sums at the top of the fix log; DESIGN `sha256sum` is `83816a69c6c21ad80cd11b7881bb6a54c67c9f3919361aa77e5057aaacc7d45d`, the owner-revised sum in "Halt resolution". HEAD equals `T/artifacts/base-commit.txt` (`5dc29d23b15eb7db4ead50623bb409f696a0d7d3`); 0 commits since; 0 staged paths outside `.dev/tasks/`; `git ls-files .claude` tracks only `.claude/cache/sc-recommend-lookup.yaml` and `.claude/settings.json`.
- `find ... -newer T/qa/final/consolidated-findings-cycle0.md` over `src tests docs plugins CHANGELOG.md .gitignore`: `probes.py`, `classify.py`, `report.py`, `models.py` (owner-approved comment change), `SKILL.md`, `test_sweep_command.py`, `test_report.py`, `test_classify.py`, `test_cli_contract.py`, `test_probes_allowlist.py`, DESIGN (owner edit), plus `src/superclaude/hooks/hooks.json`, `hooks/scripts/auggie-flag-clear.sh` and `cli/install_hooks.py` (newer mtime, empty `git diff HEAD`, not part of this work). Not newer: `commands.py`, `__init__.py`, `main.py`, `sweep.md`, `pragmatic.md`, `WORKER-CONTRACT.md`, `HOW-WE-WORK.md`, its plugin copy, `CHANGELOG.md`, `.gitignore`, `docs/`, fixtures, `conftest.py`, `test_readonly.py`, `test_cli_registration.py`, `tests/core`, `tests/recommend`, `tests/skills`. Under `T` the newer files are the QA/decision files, the task file and the six result files the fix log names. In the Checks table "UNCH" means: the file the check concerns is in the not-newer set (mtime evidence; the fix log's 126 sha256 baseline is a second source I did not re-run).
- `cmp` of `SKILL.md`, `sweep.md` and the two `HOW-WE-WORK.md` copies with their `.claude/` or plugin copies: identical. `grep -rn 'src/superclaude'` over the sweep primitives: no output (rc 1); the full-tree count is 168. Grep for `gh`, `SuperClaude-Org`, `SuperClaude_Framework`, `{owner}`, `{repo}` over `cli/sweep`, `sweep.md`, `SKILL.md`: 0. WC-9 and lock-retry grep: 0. `chat-summary|exempt|coordinator assignment` in `cli/sweep`: 0. Em or en dash in `SKILL.md`: 0.
- Not re-run: the 16-minute full `uv run pytest` (I rely on the fix log for its 3 failures and re-checked the two ruff ones: `importlib.util.find_spec('ruff')` is None; both `-k ruff` tests fail; `git diff HEAD --stat` over `src/superclaude/cli/eval tests/cli/eval tests/hooks src/superclaude/hooks` is empty). The timing test `test_speed_large_commands` was not re-run; the code it tests is unchanged. No live Orca, ccsession or Claude command was run.

## F_0 findings, judged by the live files

### FIN-F1 (BLOCKING): RESOLVED

- No guessed Orca names are read any more. `probes.py:431-435`: `parse_worker_show` builds the observation with no `agentWait` read from either place, and the comment says why (step 1.0a, open item 6). `grep` over `src/` and `tests/` for `_WAIT_TIME_KEYS`, `_wait_since`, `_agent_wait_present`, `_agent_wait`: no hit. `agent_wait`, `agent_wait_present` and `agent_wait_since` are set by no production code; `models.py:78-79` and `:90-91` mark them "Reserved: ... while the agentWait lookup is off (DESIGN open item 6)".
- Rule 5: `classify.py:251-257` `_rule_working` returns None and its comment lists the four conditions to restore; DESIGN `:491` (as the owner revised it) says the same ("Rule 5 is inert: it returns None and a row that would reach it falls to the fallback") and `:996` (open item 6) says "Rule 5 cannot match; rows fall to the fallback". Rule 4(a) (`classify.py:226-236`) is kept because DESIGN `:481` and the SPEC rule table require it; with the lookup gone nothing sets `agent_wait`, so no guessed key can print a false `waiting on a person` row.
- Pins: `test_probes_allowlist.py:1552-1566` (both guessed places hold a wait; nothing is read); `test_classify.py:320`, `:365-369` (the `working` case expects `fallback`), `:372-376`, `:436-454`; my mutations D and H (below) fail them.
- Parts that stay open but do not keep the finding open: the live-capture alternative needs a live Orca command (not allowed); see RC-N1 for the missing "working is not observed" caveat and RC-N2 for the one remaining `"live"` comparison (note only).

### FIN-F2 (MAJOR): RESOLVED

- `report.py:425-426` prints `<terminal> / <worktree> (<reason>)` from `r.safe.reason` and the cell goes through `_table` and `cell()` (`:130-138`, `:591-594`), so the reason is sanitized and cut at 200 characters like every cell. `report.py:40-43` and `:400` print `SAFE_TO_CLOSE_LINE` once under the Sessions heading. The reason is always built (`classify.py:488-492`), and the claim "never prints yes in Phase 1" is true: the terminal value is `no` or `could not determine` only (`classify.py:469-483`) and the worktree value comes from `removable` (`:443-464`), never `yes`.
- Test `test_report.py:1046-1077` asserts two cells byte for byte and that the line appears exactly once; mutation B below fails it.

### FIN-F3 (MAJOR): RESOLVED

- `report.py:54-55` (`waiting_signal`: "read what the Evidence cell names: the Orca agent-wait entry and the worker's last transcript lines, the contract, or the ready Task in Orca task-list") and `:60-61` (`fallback`: "read the row's Evidence and Notes cells, then the sources marked unscanned in Source coverage (if none, the session's last transcript lines)"). The three `waiting_signal` outcomes (`classify.py:236-247`: agent wait, frozen plan from a contract, ready Task) each name one of the listed objects in their Evidence text, and `## Source coverage` is a real heading (`report.py:204`). The map stays keyed by rule name as DESIGN `:643` says. Test `test_report.py:1035-1043`; the older map test (`:1010-1016`) still passes; mutation E fails the new test.

### FIN-F4 (MAJOR): RESOLVED

- `classify.py:86` (`NOTE_NO_CONTRACT`) and `:327-330` (the fallback rule attaches it when the Orca row is settled and no contract is attached; `_settled` accepts `None`, `:113`). Tests `test_classify.py:607-616` (the live shape: exited, completed, succeeded, no contract; also `partial` and `failed`) and `:619-635` (four negative cases); mutation C fails the first.

### FIN-F5 (MAJOR): OPEN

- The OPEN reason is valid and nothing changed. `report.py:33` (`WORKTREES_LINE`, "Orca unavailable"), `report.py:163-166` (`_discovery_incomplete` is true for any unscanned `orca worktree ps` row) and `:194-195` (printed). DESIGN `:614` pins the literal and the condition ("when discovery incomplete"); `tests/sweep/test_report.py` (`WORKTREES_BANNER`) and `tests/sweep/test_cli_contract.py` pin it again; DESIGN is immutable for the fix agent, so this needs an owner decision. Counts toward F_1.

### FIN-F6 (MAJOR): RESOLVED

- `report.py:513-516` reads "Orca became unavailable; the Orca sources marked unscanned above were not read". True: when Orca drops, the failing source and every later Orca source are recorded as unscanned (`probes.py:1019-1029` `record`, `:1034-1036`, `:1061-1062`, `:1070-1071`, `:1171-1173`), and those rows are printed first in the same section (`report.py:508-512`). Test `test_report.py:1080-1091`; mutation F fails it. The old sentence appears nowhere in `src`, `tests`, `docs`, `plugins` or `CHANGELOG.md` (only in the negative assertion `:1091` and the saved Phase 14 raw output).

### FIN-F7 (MAJOR): OPEN

- Open as a whole, and the OPEN reason is valid. The owner's revert is complete on disk: `SKILL.md:25` says "take only `report_path` and `summary`"; `SKILL.md:26` prints the counts, the lower-bound note and the path; no `orca_available`, outage or "disk sources only" text exists in `SKILL.md`, `sweep.md`, `.claude/` copies or `tests/commands/test_sweep_command.py` (grep: no match); the three FIN-F7 tests and the two sentence constants are gone; the step 3 pin reads `success-parse-takes-only-report-path-and-summary` (`test_sweep_command.py:436-437`).
- Why it stays open: an exit 0 outage run still prints counts and the path alone in both replies (`SKILL.md:26`, `:35`, `:43`; `pragmatic.md:23`). Relaying the outage needs a change to DESIGN `:662` ("take `report_path` and `summary` only"), the addendum `:29` ("only summary/report_path parsed") and `pragmatic.md:23` (exempt reply "summary counts and the report path"), all owner or revision authority. Counts toward F_1.

### FIN-F8 (MAJOR): RESOLVED

- `probes.py:179-184` (`_remaining`, `Budget.spent`: true when under 1 s of the total is left, the same threshold `call_timeout` uses at `:171-177`), `:540-554` (`_stable` stops after one read when the file changed and the budget is spent, then raises `conflict: inconsistent observation`); with no `budget` it keeps the two-read behaviour. The budget is passed through `_ledger` (`:572-577`), `_contract` (`:713-720`), `_read_contracts` (`:1306`) and `_read_transcripts` (`:1355`); the four public readers keep their signatures. This is DESIGN `:511` and the NFR-007 row. Test `test_probes_allowlist.py:1787-1818` (two cases through `collect`); mutation A fails the `spent` case. Only the contract reader is tested (RC-N4).

### FIN-F9 (MAJOR): RESOLVED

- `probes.py:22` (`import yaml`), `:672-684` (`_yaml_top` calls `yaml.safe_load`, catches `YAMLError`, `RecursionError` and `ValueError`, returns `{}` for a non-mapping), `:687-710` (only string values are read; `artifacts` keeps string items); the caller bounds the text to `CONTRACT_LIMIT` first (`:718`). The hand-written `_unquote` and line reader are gone. Test `test_probes_allowlist.py:1731-1775` (8 cases: the three divergent inputs of the finding, a flow list with a comment, invalid YAML, a non-mapping, 5000 nested brackets, the date `2026-13-45`); mutation G fails `nested-too-deep`. Neither DESIGN nor SPEC mentions YAML or a line reader (grep), so nothing departs from them; DESIGN `:211` does not list `yaml` (RC-N6).

## New findings introduced by the fix or by the three approved changes

No new BLOCKING or MAJOR finding. The three changes did not leave a test or a comment that pins the reverted text: grep for the removed test names, `_OUTAGE_SENTENCE`, `_EXEMPT_ALONE_SENTENCE`, the reverted step 3 and the old pin id finds only the saved Phase 14 raw output (history). Notes (MINOR; they never fail the review; RC-N1 and RC-N3 are the follow-up candidates):

- **RC-N1 (MINOR, follow-up candidate): a zero `working` count, and a zero waiting (a) count from an agent wait, are not evidence of none, and no report, command or skill text says so.** `SP24_LINE` (`report.py:36-39`), `sweep.md:16` and `SKILL.md:26` name only stalled and fenced; DESIGN `:491` documents the inert Rule 5 but no operator-facing text does, and Rule 4(a) (`classify.py:228`) has a live call site whose producer is switched off (`probes.py:431-435`). I applied the caller-liveness test: this is not a stub passing as live, because the behaviour is the one DESIGN `:996` specifies ("rows fall to the fallback"), the fallback never prints a false class, and the owner approved it on 2026-11-12. Changing `SP24_LINE` is pinned by DESIGN D7 and `sweep.md` is outside the fix agent's scope, so this needs an owner edit when the capture lands.
- **RC-N2 (MINOR): `classify.py:184` still compares `liveness_verdict == "live"`**, a value never captured (DESIGN `:996`). It only decides whether the decline note `NOTE_ASK_COORDINATOR` is attached (rule 1 declines either way, `:179-186`), so a wrong guess drops a note and never changes a class.
- **RC-N3 (MINOR, follow-up candidate): `yaml.safe_load` is not under the time budget.** Measured here on a private /tmp script (deleted): 5.11 s for a 1 MiB mapping, 2.82 s for a 1 MiB flow list (the pure-Python loader). `CONTRACT_LIMIT` (`probes.py:72`) allows 1 MiB per file and `_read_contracts` (`:1293-1306`) checks no time before a parse. Normal contracts are a few KB; about 24 oversized files would be needed to pass the skill's 120 s Bash timeout. A performance weakness, not a safety one.
- **RC-N4 (MINOR): three untested choices.** Non-string contract values now read as absent (no test for, say, `reason: 404`); the ledger and transcript budget threading has no test of its own (same `_stable` call); and the four broken-condition inputs of `test_rule_5_never_matches_while_the_agent_wait_names_are_uncaptured` (`test_classify.py:447-454`) assert `!= WORKING` and are vacuous while Rule 5 is inert (the first assertion `:445-446` pins the behaviour; mutation D fails it).
- **RC-N5 (MINOR): `final-inventory.md:139` and `:143` were not refreshed.** The 37 new-file paths still equal the inventory table, DESIGN is 1051 lines and the edited-file count is 12 files with 67 changed lines; the new-file line total is now 14254 (saved: 14069) and the sum 15372 (saved: 15187). "over 3000" still holds.
- **RC-N6 (MINOR): DESIGN `:211`** lists only `models, subprocess, os, json, time, datetime` for `probes.py`; `probes.py:12-22` also imports `re`, `collections.abc`, `dataclasses`, `pathlib` (all present at cycle 0) and now `yaml`. Nothing forbids it (`:211` bans `classify`, `report`, `click`). A documentation gap for an owner edit.
- **RC-N7 (MINOR): the DESIGN layout (`:628-629`) shows one line under the Sessions heading**; the report now prints a second (`SAFE_TO_CLOSE_LINE`, `report.py:400`). DESIGN `:643` fixes the columns, not the text; this is the smallest fix FIN-F2 asked for.

## Do the new and changed tests fail when the behaviour is removed, and is the module still read-only

Mutations ran on a private copy (`mktemp -d /tmp/verify-rc-mut.*` holding `src`, `tests/sweep`, `tests/commands/test_sweep_command.py`, `pyproject.toml`; `PYTHONPATH` pointed at the copy and the script printed `IMPORTED /tmp/verify-rc-mut.XwpzPQmJ/m/src/superclaude/cli/sweep/probes.py` before any run; baseline in the copy: 471 passed for `test_classify.py`, `test_report.py` and `test_probes_allowlist.py`; the copy and the path file were deleted, `ls -d /tmp/verify-rc-*` finds nothing, and `git status` shows no repository change from me). Each mutation was one `sed` edit, checked to change the copied file:

| Mutation (read against the live code and test) | Result |
|---|---|
| A (FIN-F8): `probes._stable` `if budget is not None and budget.spent():` replaced by `if False:` | `test_a_changed_contract_is_re_read_only_while_the_budget_allows[spent]` FAILED; the `budget-left` case passed (1 failed, 1 passed) |
| B (FIN-F2): the `(reason)` suffix of the Safe to close cell removed in `report._sessions` | `test_sessions_safe_to_close_cell_carries_its_reason` FAILED |
| C (FIN-F4): `notes = (NOTE_NO_CONTRACT,) if ... else ()` replaced by `notes = ()` in `_rule_fallback` | `test_settled_orca_row_without_a_contract_names_the_missing_contract` FAILED (1 failed, 8 passed) |
| D (FIN-F1): the four conditions of Rule 5 restored in `_rule_working` | 3 FAILED: `test_rule_case_per_rule_1_to_9[working]`, `test_every_class_name_but_working_is_reached`, `test_rule_5_never_matches_while_the_agent_wait_names_are_uncaptured` (3 failed, 163 passed) |
| E (FIN-F3): the `waiting_signal` text cut back to the agent-wait-only sentence | `test_next_inspection_waiting_signal_and_fallback_fit_every_outcome` FAILED |
| F (FIN-F6): the old "Orca was unavailable; Orca sources were not read" sentence restored | `test_orca_dropping_mid_run_is_not_reported_as_nothing_read` FAILED |
| G (FIN-F9): `RecursionError` removed from the `except` tuple of `_yaml_top` | `test_contract_fields_are_read_by_yaml_safe_load[nested-too-deep]` FAILED (1 failed, 7 passed) |
| H (FIN-F1): a read of `projection.agentWait` added to `parse_worker_show` | `test_parse_worker_show_reads_no_agent_wait_field_until_its_names_are_captured` FAILED |

Mutations A and D are the two fix-log proofs I read against the code and tests; the fix log's account of both matches what I observed.

Read-only check of the sweep module (grep over `src/superclaude/cli/sweep/*.py`): `subprocess.run` appears only at `probes.py:257` (`_orca`, after `check_orca_argv` at `:254`) and `:308` (`_git`); no `Popen`, `os.system`, `shutil`, `mkdir`, `write_text`, `write_bytes`, `os.replace` or `os.rename` anywhere; `os.open`, `os.write`, `os.link` and `os.unlink` appear only in `commands.py` (the report-path publication, not newer than cycle 0); `open(` appears at `probes.py:559`, `:792`, `:856`, all `"rb"`. `ALLOWED_ORCA` still holds the 10 templates (`probes.py:49-60`, "10 templates, 7 verbs"), `ALLOWED_GIT` the one `status --porcelain=v1 -z --branch --untracked-files=all` entry (`:65-67`), `FORBIDDEN_TOKENS` is `--include-remote` (`:62`). The `except ValueError` clauses (`probes.py:236`, `:392`, `:526`, `:682`, `:725`) wrap JSON parsing, time parsing, path resolution and `yaml.safe_load`, never `_call`, `_orca` or `check_orca_argv`. The new `yaml` import touches no file or process: `safe_load` runs on a string already read and bounded by `CONTRACT_LIMIT`. `tests/sweep/conftest.py` and `test_readonly.py` (the process and write guards) are not newer and pass.

## The six checks that failed in the first re-check, and the new finding FIN-N1

- **FIN-N1 (skill step 3 against DESIGN 7.6 `:662`): gone.** The FIN-F7 edit was reverted; `SKILL.md:25` now says "take only `report_path` and `summary`", the text of DESIGN `:662` and of the addendum `:29`.
- `qa-design-conformance-report:C5`: PASS (rule 5 is inert as DESIGN `:491` now says; `RULES` order, names and rule 1 and 2 notes unchanged; the test pins match DESIGN `:760`).
- `qa-design-conformance-report:C13`: PASS (the skill again matches DESIGN 7.6 `:662`).
- `qa-design-conformance-report:C22`: PASS (the new departures are all MINOR: RC-N6, RC-N7, the optional budget argument, string-only contract values; Rule 5 inertness is DESIGN's own text).
- `qa-test-traceability-report:C8`: PASS (`test_classify.py:365-376` and `:436-454` are the cases DESIGN `:760` now describes: the `working` case expects `fallback`, every class but `working` is reached, the Rule 5 case never matches).
- `qa-maintainability-report:C9`: PASS (the three `agent_wait*` fields are explained as reserved at `models.py:78`, `:90`, `classify.py:229` and `probes.py:432-435`; the stale comments are gone).
- `qa-completeness-report:C4`: PASS (command, skill and command test are on disk and match DESIGN 7.6).

## Checks

Rule applied: a check is PASS when the state it describes still conforms (DESIGN counts as the owner revised it, including open item 6 at `:996` and the new `:491` and `:760`) or when only a line number or a count moved; it is FAIL only when its claim is now false. Checks about saved scratch runs or live records cannot be re-run; for those the row says what I confirmed instead (the files they relied on are in the not-newer set). 238 rows, one per id of the cycle-0 PASS set in `cycle-ledger.md`. "UNCH" is defined in the Basis section.

| Check id | Result |
|---|---|
| qa-design-conformance-report:C1 | PASS: every DESIGN 7.1 name is still defined where DESIGN puts it; the fix added `_remaining` and `Budget.spent` (`probes.py:179-184`) and removed private helpers DESIGN does not name |
| qa-design-conformance-report:C2 | PASS: the public readers keep their signatures; optional `budget` arguments were added to `_stable`, `_contract`, `_ledger` and the private readers (`probes.py:540-543`, `:572-574`, `:713-715`), the same kind of MINOR widening as the cycle-0 notes F2 and F4 |
| qa-design-conformance-report:C3 | PASS: `models.py:55-115` read: field names, order and defaults intact, two comments added (`:78`, `:90`); golden and import tests pass |
| qa-design-conformance-report:C4 | PASS: `JSON_SCHEMA_VERSION`, `CLASSES`, `PACKAGE_STATES`, `SAFE_VALUES` at `models.py:17`, `:31`, `:43`, `:52` |
| qa-design-conformance-report:C5 | PASS: `RULES` has 9 names in DESIGN order (`classify.py:333-343`); rule 5 is inert exactly as DESIGN `:491` now says (`:251-257`, the four conditions kept in the comment); rule 1 and 2 notes (`:161-208`) and SP-26 tests pass; `test_rule_case_per_rule_1_to_9[working]` expects `fallback` as DESIGN `:760` says |
| qa-design-conformance-report:C6 | PASS: 10 templates, `FORBIDDEN_TOKENS`, `ALLOWED_GIT`, byte limits and id regexes read at `probes.py:46-78`; allowlist tests pass |
| qa-design-conformance-report:C7 | PASS: JSON v1 key set: golden key-set tests pass; the fix log's edit regions of `report.py` (`:40-62`, `:400`, `:425-426`, `:513-516`) do not touch `to_json`, and `orca_available` is still a top-level key |
| qa-design-conformance-report:C8 | PASS: `SECTIONS` has 12 entries, Sessions columns unchanged (`report.py:404-413`), every cell goes through `cell()` (`:130-138`); one extra line under the Sessions heading is RC-N7 (MINOR) |
| qa-design-conformance-report:C9 | PASS: UNCH (`commands.py`) |
| qa-design-conformance-report:C10 | PASS: `subprocess.run` only at `probes.py:257`, `:308`; writes only in `commands.py`; no write call in `classify.py` or `report.py` (grep); the one new import (`yaml`) is in `probes.py:22`, which DESIGN `:211` lets import everything but `classify`, `report`, `click`; import-purity AST tests pass |
| qa-design-conformance-report:C11 | PASS: UNCH (`__init__.py`) |
| qa-design-conformance-report:C12 | PASS: UNCH (`main.py`; `git diff HEAD --stat` still 4 lines) |
| qa-design-conformance-report:C13 | PASS: the skill matches DESIGN 7.6 `:662` again: `SKILL.md:25` takes only `report_path` and `summary`, no `orca_available` anywhere in skill, command or test (grep), frontmatter literals at `SKILL.md:4`, `sweep.md` UNCH |
| qa-design-conformance-report:C14 | PASS: the DESIGN 7.6 test list (`:666`) passes in the 121-test file; the skill-only pin is `success-parse-takes-only-report-path-and-summary` (`test_sweep_command.py:436-437`) again |
| qa-design-conformance-report:C15 | PASS: addendum `:29` ("only summary/report_path parsed") agrees with the live skill; `pragmatic.md:22-26` UNCH; exempt-reply text `SKILL.md:35-43` unchanged by the revert |
| qa-design-conformance-report:C16 | PASS: UNCH (`WORKER-CONTRACT.md`, `test_worker_contract.py`) |
| qa-design-conformance-report:C17 | PASS: UNCH (guide and plugin copy); `cmp` identical |
| qa-design-conformance-report:C18 | PASS: UNCH (`.gitignore`); `git check-ignore -v .dev/tasks .dev/tasks/to-do` prints nothing, rc 1 |
| qa-design-conformance-report:C19 | PASS: every `test_` function token in DESIGN has a `def` under `tests/` (46 tokens; the 13 without are 11 test file names, the `test_fr010` prefix and the retired old name `test_never_as_worker_list_names_all_seven_commands`, as in cycle 0); DESIGN `:760` names no renamed test |
| qa-design-conformance-report:C20 | PASS: re-ran: scoped pytest 3239 passed (count moved: tests added, three FIN-F7 tests removed), ruff check clean, the two `-k ruff` tests still fail because the venv has no ruff module, `git diff HEAD --stat` over eval and hooks is empty |
| qa-design-conformance-report:C21 | PASS: UNCH (`sweep-help-pipx*.txt`, `OQ-10-pipx-decision.md`, `commands.py`) |
| qa-design-conformance-report:C22 | PASS: departures after the fix are all MINOR (optional budget argument, `import yaml` outside the `:211` list, string-only contract values, a second Sessions line); rule 5 inertness is DESIGN's own text; no blocking departure |
| qa-design-conformance-report:C23 | PASS: the saved live-check JSON and MD files are not newer; they cannot be re-run (live Orca) and nothing they relied on (the key set) changed |
| qa-design-conformance-report:C24 | PASS: `removable` reads `worktree.frozen` (`classify.py:453`) and `_prepare_worktrees` sets it (`:828-842`, `:923-931`); rule 5 reachability is now explicit in DESIGN `:491` (see RC-N1) |
| qa-design-conformance-report:C25 | PASS: 0 staged `.claude/` paths, `.dev/tasks` not ignored, my /tmp copies deleted |
| qa-test-traceability-report:C1 | PASS: see design-conformance C19; the 33 resolvable function names still resolve |
| qa-test-traceability-report:C2 | PASS: UNCH (`tests/sweep/conftest.py`) |
| qa-test-traceability-report:C3 | PASS: UNCH (`test_readonly.py`); the fix added no `integration` mark |
| qa-test-traceability-report:C4 | PASS: UNCH (real-git test in `test_readonly.py`) |
| qa-test-traceability-report:C5 | PASS: UNCH (`test_readonly.py`, 24 tests collected) |
| qa-test-traceability-report:C6 | PASS: `test_probes_allowlist.py` has 254 tests (tests were added, none removed in the fix log), all pass; the ten-template pin and negatives are untouched |
| qa-test-traceability-report:C8 | PASS: `test_classify.py` rows still present; rule 5 and class coverage now pin the inert Rule 5 as DESIGN `:760` says (`:365-376`, `:436-454`); 166 pass |
| qa-test-traceability-report:C9 | PASS: FR-010 fixtures unchanged in meaning; file passes |
| qa-test-traceability-report:C10 | PASS: D9, SP-29, R2-B1, R3-B1 and R3-B2 fixtures unchanged; file passes |
| qa-test-traceability-report:C11 | PASS: `test_report.py` rows present, three tests added (`:1035`, `:1046`, `:1080`); 51 pass |
| qa-test-traceability-report:C12 | PASS: `test_cli_contract.py` rows present; `test_waiting_lists_hold_row_ids_only` (`:1065-1095`) now builds waiting (a) from a blocked contract and still pins both lists as row ids; 94 pass |
| qa-test-traceability-report:C13 | PASS: UNCH (`test_cli_registration.py`, 3 tests) |
| qa-test-traceability-report:C14 | PASS: the budget-exhaustion publish test is in `test_cli_contract.py` (passes); the MINOR note T317-F2 is unchanged |
| qa-test-traceability-report:C15 | PASS: UNCH (`test_worker_contract.py`) |
| qa-test-traceability-report:C16 | PASS: UNCH (routing, parity and severity test files) |
| qa-test-traceability-report:C17 | PASS: the 14 original DESIGN 7.6 assertions are in the restored `test_sweep_command.py` (121 tests, all pass); NFR-011 grep rc 1; full-tree count 168 |
| qa-test-traceability-report:C18 | PASS: addendum positive cases map to the same pins; the one `success-*` pin id is back to its cycle-0 name |
| qa-test-traceability-report:C19 | PASS: negative and exclusion pins unchanged by the revert; file passes |
| qa-test-traceability-report:C20 | PASS: UNCH (`pragmatic.md`); the seven-site tests pass |
| qa-test-traceability-report:C21 | PASS: the cycle-0 text-mutation run on private copies cannot be re-run; the style, command and skill pins it mutated still exist and pass (121), and my mutations A to H fail as expected |
| qa-test-traceability-report:C22 | PASS: the cycle-0 code-mutation run cannot be re-run; the tests it relied on still exist (the "three reads" pin and the one-re-read pin in `test_probes_allowlist.py` pass) |
| qa-test-traceability-report:C23 | PASS: UNCH (the two severity modules and the parity file); they pass in the scoped run |
| qa-test-traceability-report:C24 | PASS: re-checked: `find_spec('ruff')` is None, both `-k ruff` tests fail, `git diff HEAD --stat` over eval and hooks is empty |
| qa-test-traceability-report:C25 | PASS: UNCH (`tests/sweep/fixtures`, 19 files, none named `synthetic`) |
| qa-test-traceability-report:C26 | PASS: gates reproduced (counts moved): 3239 passed, ruff check clean, formatting clean on the edited folders, sync test 7 passed, `cmp` of mirrors identical |
| qa-validation-evidence-report:C1 | PASS: `cmp` of `SKILL.md` and `sweep.md` with the `.claude/` copies identical and `tests/cli/test_verify_sync_hooks.py` 7 passed (I did not run `make verify-sync` itself) |
| qa-validation-evidence-report:C2 | PASS: `uv run ruff check .` prints All checks passed |
| qa-validation-evidence-report:C3 | PASS: `ruff format --check src/ tests/` prints 12 files would be reformatted, 1823 already formatted; the list equals `phase14-lint.md` (diff identical) |
| qa-validation-evidence-report:C4 | PASS: none of the 12 is an edited file (all Markdown, same list) |
| qa-validation-evidence-report:C5 | PASS: `ruff format --check src/superclaude/cli/sweep tests/sweep tests/commands`: 25 files already formatted |
| qa-validation-evidence-report:C6 | PASS: count moved: scoped run 3239 passed, exit 0 |
| qa-validation-evidence-report:C7 | PASS: the Phase 14 records predate the fix and are superseded by this re-run and the fix log; the code they cover was re-tested here |
| qa-validation-evidence-report:C8 | PASS: re-checked: no ruff module in the venv; the two test files are not newer |
| qa-validation-evidence-report:C9 | PASS: code under test unchanged (`git diff HEAD --stat` over `tests/hooks` and `src/superclaude/hooks` empty); I did not re-run the timing test |
| qa-validation-evidence-report:C10 | PASS: re-run: no output, rc 1 |
| qa-validation-evidence-report:C11 | PASS: re-run: 168 |
| qa-validation-evidence-report:C12 | PASS: UNCH (`sweep-help-pipx.txt`, decision file) |
| qa-validation-evidence-report:C13 | PASS: UNCH (`commands.py`, the help source) |
| qa-validation-evidence-report:C14 | PASS: 0 staged `.claude/` paths; `.claude/` mirrors stay ignored |

| qa-scope-report:C1 | PASS: the 37 new-file paths still equal the inventory table (`git ls-files --others` minus `baseline-untracked.txt`: `diff` empty); the 12 edited tracked files are the same; the fix created no file (the line total moved, RC-N5) |
| qa-scope-report:C2 | PASS: UNCH for the 12 edited tracked files; the nine files the fix edited were already in the inventory |
| qa-scope-report:C3 | PASS: no new file from the fix (set equality above) |
| qa-scope-report:C4 | PASS: nothing changed outside the inventory areas: `git ls-files --others` outside `src tests docs plugins .dev` is covered by the same set check, the only newer source files are the nine edited ones, `models.py` and DESIGN (both inventory paths) |
| qa-scope-report:C5 | PASS: WC-9 and lock-retry grep over the sweep sources, command, skill, tests, `.gitignore`, `CHANGELOG.md`: 0 |
| qa-scope-report:C6 | PASS: UNCH (`WORKER-CONTRACT.md`) |
| qa-scope-report:C7 | PASS: UNCH (`test_worker_contract.py`) |
| qa-scope-report:C8 | PASS: UNCH (`commands.py`); the fix added no option or abstraction |
| qa-scope-report:C9 | PASS: `ALLOWED_ORCA` still 10 templates (`probes.py:49-60`) |
| qa-scope-report:C10 | PASS: the guessed-key heuristic (S-m2) is gone (`probes.py:431-435`); the fix adds only an optional `budget` argument and `Budget.spent` |
| qa-scope-report:C11 | PASS: UNCH (`pragmatic.md`) |
| qa-scope-report:C12 | PASS: UNCH (WC-16 files and `sweep.md`) |
| qa-scope-report:C13 | PASS: UNCH (guide and plugin copy); `cmp` identical |
| qa-scope-report:C14 | PASS: `chat-summary\|exempt\|coordinator assignment` in `cli/sweep`: 0; `src/superclaude` in `sweep.md` and the skill: 0 |
| qa-scope-report:C15 | PASS: the DESIGN diff against `design-base.md` has 65 hunks (64 read in cycle 0); the added one is `@@ -487 +491 @@`, the owner's Rule 5 line, and `:760` sits inside the existing hunk `@@ -738,3 +759,3 @@`; both are recorded in `FINAL-GATE-halt-resolution-decision.md`; DESIGN sha256 equals the "Halt resolution" sum |
| qa-scope-report:C16 | PASS: count moved: scoped run 3239 passed (cycle 0: 3220), ruff check clean |
| qa-scope-report:C17 | PASS: argument re-checked (see test-traceability C24) |
| qa-scope-report:C18 | PASS: UNCH (pipx files and decision file) |
| qa-scope-report:C19 | PASS: 0 staged `.claude/` paths; `.gitignore` UNCH; `.dev/sweeps/` ignored |
| qa-readonly-safety-report:C1 | PASS: `subprocess.run` only at `probes.py:257` and `:308`, list argv, no shell, no `Popen` or `os.system` in any sweep file |
| qa-readonly-safety-report:C2 | PASS: `_orca` calls `check_orca_argv(tuple(args))` first (`probes.py:254`) then `subprocess.run([binary, *args], ...)` (`:257-263`); `_call` is the only caller of `_orca` |
| qa-readonly-safety-report:C3 | PASS: 10 templates matched token for token with `re.fullmatch` placeholders (`probes.py:212-224`); allowlist tests pass |
| qa-readonly-safety-report:C4 | PASS: `FORBIDDEN_TOKENS` (`:62`) rejected first in any position (`:217`); tests pass |
| qa-readonly-safety-report:C5 | PASS: `orca_binary()` unchanged (`probes.py:200-202`) |
| qa-readonly-safety-report:C6 | PASS: `ALLOWED_GIT` has the one `status` entry (`:65-67`), `check_git_args` exact match (`:227-230`); git argv and env tests in `test_readonly.py` (UNCH) pass |
| qa-readonly-safety-report:C7 | PASS: the cycle-0 scratch experiment cannot be re-run; `_git`, `ALLOWED_GIT` and `test_readonly.py` are UNCH |
| qa-readonly-safety-report:C8 | PASS: no write call in `probes`, `classify`, `report` (grep); `commands.py` UNCH |
| qa-readonly-safety-report:C9 | PASS: `open(` at `probes.py:559`, `:792`, `:856`, all `"rb"`; `read_bytes` at `:720`, `read_text` at `:839`; the new code only parses a string already read |
| qa-readonly-safety-report:C10 | PASS: UNCH (`commands.py`) |
| qa-readonly-safety-report:C11 | PASS: the `except` clauses with `ValueError` (`probes.py:236`, `:392`, `:526`, `:682`, `:725`) wrap JSON, time, path and `yaml.safe_load` only, none wraps `_call`, `_orca` or `check_orca_argv` |
| qa-readonly-safety-report:C12 | PASS: UNCH (`main.py`, 4 added lines) |
| qa-readonly-safety-report:C13 | PASS: tests, lint and sync re-run (counts moved) |
| qa-readonly-safety-report:C14 | PASS: UNCH (`test_readonly.py`, `conftest.py`) |
| qa-readonly-safety-report:C15 | PASS: `allowed-tools` at `SKILL.md:4` unchanged; steps 1 and 2 are the only commands (`:23-24`); `Will Not` at `:59-64` forbids the rest |
| qa-readonly-safety-report:C18 | PASS: argument re-checked (see test-traceability C24) |
| qa-readonly-safety-report:C19 | PASS: my experiments used /tmp copies, deleted; no repository file changed by me (HEAD, staged set and the not-newer set intact) |
| qa-fork-never-commit-report:C1 | PASS: HEAD and `base-commit.txt` both print `5dc29d23b15eb7db4ead50623bb409f696a0d7d3`; 0 commits since |
| qa-fork-never-commit-report:C2 | PASS: 0 staged paths outside `.dev/tasks/`; `.claude/` mirrors ignored |
| qa-fork-never-commit-report:C3 | PASS: `git check-ignore -v .dev/tasks .dev/tasks/to-do` prints nothing, rc 1; `.gitignore` UNCH |
| qa-fork-never-commit-report:C4 | PASS: grep for `gh` over `cli/sweep`, `sweep.md`, `SKILL.md`: 0 |
| qa-fork-never-commit-report:C5 | PASS: no `{owner}` or `{repo}` in those files: 0 |
| qa-fork-never-commit-report:C6 | PASS: no `SuperClaude-Org` or `SuperClaude_Framework` in those files: 0 |
| qa-fork-never-commit-report:C7 | PASS: `SKILL.md` (read in full) never tells an agent to stage, force-add or commit anything (`:59-64` forbids staging); `sweep.md` UNCH |
| qa-fork-never-commit-report:C8 | PASS: UNCH (`conftest.py` process and write guard) |
| qa-fork-never-commit-report:C9 | PASS: pipx files UNCH; the saved scratch run cannot be re-run and nothing it relied on changed |
| qa-fork-never-commit-report:C10 | PASS: argument re-checked (see test-traceability C24) |
| qa-fork-never-commit-report:C11 | PASS: `cmp` of the two edited primitives with the `.claude/` copies identical, sync test 7 passed, ruff check clean |
| qa-fork-never-commit-report:C12 | PASS: scoped folders pass (3239) |
| qa-fork-never-commit-report:C13 | PASS: my runs changed no repository file (only this report was written); HEAD and the staged set are unchanged |
| qa-fork-never-commit-report:C14 | PASS: nothing under `.dev/tasks` is gitignored; many `.dev/tasks` files are still untracked (new QA, result and artifact files), the same close-out staging step as the cycle-0 MINOR note F1 (`git add .dev/tasks` is still to be run; I did not stage anything) |
| qa-coordinator-usefulness-report:C1 | PASS: `NO_RECORDS` (`report.py:29`) and the waiting sections unchanged |
| qa-coordinator-usefulness-report:C10 | PASS: coverage lines still stated: remote hosts, partial Messages, lower bounds (`report.py:517-525`), discovery line (`:194-195`) |
| qa-coordinator-usefulness-report:C11 | PASS: the skill (read in full) prints counts and the path, no advice, Reads to `Report complete` (`SKILL.md:25`), says safe/removable/next inspection are observations (`:66`); restored by the owner's revert, no outage line |
| qa-coordinator-usefulness-report:C12 | PASS: Phase 14 failure attribution re-checked; sweep and command tests all pass (713 collected) |
| qa-failure-clarity-report:C1 | PASS: UNCH (`commands.py`); its tests pass |
| qa-failure-clarity-report:C2 | PASS: UNCH (`commands.py`) |
| qa-failure-clarity-report:C3 | PASS: UNCH (`commands.py` no-binding path) |
| qa-failure-clarity-report:C6 | PASS: `PAGE_LINE` (`report.py:32`) and the lower-bound line (`:517-520`) unchanged |
| qa-failure-clarity-report:C8 | PASS: `call_failed` rows still unscanned with a reason (`probes.py:1019-1029`); rows fall to could not determine; the fix only adds a note for a settled Orca row with no contract |
| qa-failure-clarity-report:C9 | PASS: missing transcript folder still gives a `no folder` row (`probes.py:1344-1345`), no idle or finished claim |
| qa-failure-clarity-report:C10 | PASS: `NOTE_TRANSCRIPT_UNREADABLE` unchanged (`classify.py:83`) |
| qa-failure-clarity-report:C11 | PASS: UNCH (`commands.py` publish collision) |
| qa-failure-clarity-report:C12 | PASS: UNCH (`commands.py` pre-commit failures) |
| qa-failure-clarity-report:C15 | PASS: exit codes in `commands.py` UNCH and `SKILL.md:27` ("On exit 1 or 2 ...") unchanged by the revert |
| qa-failure-clarity-report:C16 | PASS: every table cell goes through `cell()` (`report.py:130-138`), so the new Safe to close reason and the new note are sanitized; the new report lines are fixed text |
| qa-failure-clarity-report:C17 | PASS: header `READ ONLY .` (`report.py:181`) and footer `Inspection only.` (`:531`) unchanged |
| qa-failure-clarity-report:C18 | PASS: failure-path tests pass |
| qa-failure-clarity-report:C19 | PASS: argument re-checked (see test-traceability C24) |
| qa-failure-clarity-report:C20 | PASS: `ruff check .` clean; format check clean on the sweep and command test folders (25 files) |
| qa-maintainability-report:C2 | PASS: `_remaining` is shared by `call_timeout` and `spent` (`probes.py:171-184`); the budget is threaded by one optional argument, not copied logic |
| qa-maintainability-report:C3 | PASS: each new constant lives in one module (`SAFE_TO_CLOSE_LINE`, `NOTE_NO_CONTRACT`); the test literals are pinned like the cycle-0 copies |
| qa-maintainability-report:C4 | PASS: no new path or environment rule |
| qa-maintainability-report:C5 | PASS: the new comments give reasons (open item 6, NFR-007, the rule-6 dependence at `classify.py:328`), not restatements |
| qa-maintainability-report:C6 | PASS: new comments point at DESIGN open item 6 (`:996`) and step 1.0a, both exist |
| qa-maintainability-report:C7 | PASS: the new decisions carry one-line why text (`probes.py:432-434`, `_yaml_top` docstring `:673-679`, `_stable` docstring `:543-545`) |
| qa-maintainability-report:C8 | PASS: new names say what they do (`spent`, `_remaining`, `NOTE_NO_CONTRACT`, `SAFE_TO_CLOSE_LINE`) |
| qa-maintainability-report:C9 | PASS: the three `agent_wait*` fields are set only by tests and are explained as reserved at `models.py:78`, `:90`, `classify.py:229` and `probes.py:432-435`; the stale "parse_worker_show sets the wait time" comments are gone (grep of `src`) |
| qa-maintainability-report:C10 | PASS: 8 `type: ignore` uses (`report.py` x6, `probes.py:811`, `classify.py:513`), the same count as cycle 0, none in the code the fix added |
| qa-maintainability-report:C11 | PASS: UNCH (`main.py`, package layout) |
| qa-maintainability-report:C12 | PASS: the duplicated style and skill text is pinned by the restored `test_sweep_command.py`; the new report sentences are pinned by tests (`test_report.py:1035-1091`) |
| qa-maintainability-report:C13 | PASS: UNCH (`conftest.py`); the new tests reuse the shared helpers (`crow`, `real`, `srow`, `obs`) |
| qa-maintainability-report:C14 | PASS: `ruff check .` clean; 25 sweep and command test files formatted |
| qa-maintainability-report:C15 | PASS: `cmp` of skill and command with the `.claude/` copies identical; sync test 7 passed |
| qa-maintainability-report:C16 | PASS: count moved: the sweep and command tests (713) all pass in the scoped run |
| qa-maintainability-report:C17 | PASS: my copies were under /tmp and deleted |

| qa-cross-artifact-report:C1 | PASS: UNCH (WC-16 files, guide, `sweep.md`, `.gitignore`, `CHANGELOG.md`) |
| qa-cross-artifact-report:C2 | PASS: re-run here: `diff` of `WORKER-CONTRACT.md` line 277 against DESIGN line 679 prints nothing (identical); the owner's DESIGN edits touch `:491` and `:760` only, so the block is unchanged |
| qa-cross-artifact-report:C3 | PASS: UNCH (`WORKER-CONTRACT.md`, `sweep.md`) |
| qa-cross-artifact-report:C4 | PASS: UNCH (cadence text in contract, guide, `sweep.md`, `CHANGELOG.md`) |
| qa-cross-artifact-report:C5 | PASS: UNCH (`commands.py`, `sweep.md`); `SKILL.md:19` still names the four flags |
| qa-cross-artifact-report:C6 | PASS: flag limits UNCH (`commands.py`); Run id regex still `run_[0-9a-f]{12}` (`probes.py:46`) |
| qa-cross-artifact-report:C7 | PASS: UNCH (report location code `commands.py`, `.gitignore`, `sweep.md`) |
| qa-cross-artifact-report:C8 | PASS: `JSON_SCHEMA_VERSION = 1` (`models.py:17`); golden key-set tests pass; DESIGN 7.4 not among the owner's two edits |
| qa-cross-artifact-report:C9 | PASS: UNCH (owner-decision files); `probes.py:49-60` still holds the 10 templates, `--include-remote` the only forbidden token |
| qa-cross-artifact-report:C10 | PASS: UNCH (`pragmatic.md`, addendum, decision records); skill and test restored to the cycle-0 text |
| qa-cross-artifact-report:C11 | PASS: the common-rule text in `pragmatic.md:23-26` and `SKILL.md:35-51` is unchanged; pin tests pass |
| qa-cross-artifact-report:C12 | PASS: UNCH (`pragmatic.md`, seven table sites) |
| qa-cross-artifact-report:C13 | PASS: exclusion text in `SKILL.md:45-47` unchanged |
| qa-cross-artifact-report:C14 | PASS: `report.py` has no chat DONE / NEXT text (the only `NEXT` hits are the `NEXT_INSPECTION` map and `_NEXT_DEFAULT`), still ends `Report complete` (`:531`, line moved from `:520`), 12 sections; `commands.py` UNCH |
| qa-cross-artifact-report:C15 | PASS: no activation claim added; `grep -c chat-summary ~/.claude/output-styles/pragmatic.md` is 0 (read-only grep); `SKILL.md:49-51` unchanged |
| qa-cross-artifact-report:C16 | PASS: UNCH (routing rows, plugin copy); `cmp` identical |
| qa-cross-artifact-report:C17 | PASS: UNCH (`CHANGELOG.md`); its skill and test claims are true of the restored files |
| qa-cross-artifact-report:C18 | PASS: UNCH (`docs/`) |
| qa-cross-artifact-report:C19 | PASS: UNCH (the never-as-worker copies) |
| qa-cross-artifact-report:C20 | PASS: reproduced pytest (3239, counts moved), ruff check, sync test (7 passed) |
| qa-cross-artifact-report:C21 | PASS: argument re-checked (see test-traceability C24) |
| qa-cross-artifact-report:C22 | PASS: the 37 new-file paths equal the inventory (`diff` empty), DESIGN is 1051 lines, the 12 edited files and their 67 changed lines match; the `cat` total of the new files moved from 14069 to 14254 because of the authorized fix edits (RC-N5) |
| qa-cross-artifact-report:C23 | PASS: `SKILL.md:27-29` failure handling unchanged and still matches `commands.py` exit codes |
| qa-cross-artifact-report:C24 | PASS: UNCH (pipx evidence) |
| qa-completeness-report:C1 | PASS: UNCH (the 1.0a and 1.0b pre-step output files) |
| qa-completeness-report:C2 | PASS: the six modules are on disk (`ls` lists 6) with every DESIGN 7.1 name (see design C1) |
| qa-completeness-report:C3 | PASS: all test files on disk; DESIGN function-name tokens resolve (see design C19) |
| qa-completeness-report:C4 | PASS: command, skill and command test are on disk and match DESIGN 7.6 (`:653-666`): skill step 3 takes only `report_path` and `summary`, 121 command tests pass |
| qa-completeness-report:C5 | PASS: UNCH (step 1.16a record) |
| qa-completeness-report:C6 | PASS: UNCH (WC-16 files); the paragraph equals DESIGN line 679 (cross-artifact C2) |
| qa-completeness-report:C7 | PASS: UNCH (routing rows, parity and level-table rule) |
| qa-completeness-report:C8 | PASS: `cmp` of skill and command with the `.claude/` copies identical, sync test 7 passed, 0 staged `.claude/` paths |
| qa-completeness-report:C9 | PASS: `ruff check .` clean; the 12 format failures are the same Markdown files, none in the change set |
| qa-completeness-report:C10 | PASS: scoped run 3239 passed; failure argument re-checked |
| qa-completeness-report:C11 | PASS: re-run: no output, rc 1 |
| qa-completeness-report:C12 | PASS: UNCH (pipx output and decision) |
| qa-completeness-report:C13 | PASS: UNCH (`.gitignore`) |
| qa-completeness-report:C14 | PASS: every file, constant set and JSON key still delivered (six modules, `models.py:17`, `:31`, `:43`, `:52`; golden tests) |
| qa-completeness-report:C15 | PASS: UNCH (`pragmatic.md`) |
| qa-completeness-report:C16 | PASS: the skill carries the same rule (`SKILL.md:31-51`) |
| qa-completeness-report:C17 | PASS: no new test module, detector or hook (the new set of untracked paths equals the inventory) |
| qa-completeness-report:C18 | PASS: `step-7.10-style-exception.md`, `test-sweep-command-summary.md`, `phase11-validation.md` and the Phase 14 files exist; the regenerated result files match the live counts (166, 51, 254, 94, 121) |
| qa-completeness-report:C19 | PASS: approval and implementation records not edited |
| qa-completeness-report:C20 | PASS: UNCH (the contract and `sweep.md` edits) |
| qa-completeness-report:C21 | PASS: the 37 new paths equal the inventory, the 12 edited files equal the diff (see cross-artifact C22) |
| qa-completeness-report:C22 | PASS: no recorded step lost an output file; the fix created and removed no file |
| qa-operator-actionability-report:C1 | PASS: UNCH (guide, contract, `sweep.md`) |
| qa-operator-actionability-report:C2 | PASS: UNCH (flags and defaults in `commands.py`, `sweep.md`); Run id regex `probes.py:46` |
| qa-operator-actionability-report:C3 | PASS: UNCH (report location code and text) |
| qa-operator-actionability-report:C7 | PASS: report cells now give the reason behind `could not determine` (`report.py:425-426`) and the Safe to close line says it never prints yes (`:40-43`); nothing invites closing or messaging a person-started session |
| qa-operator-actionability-report:C8 | PASS: UNCH (assignment text in `pragmatic.md:24` and `SKILL.md:45`) |
| qa-operator-actionability-report:C9 | PASS: exempt and ordinary rules unchanged by the revert (`SKILL.md:35-47`) |
| qa-operator-actionability-report:C11 | PASS: no activation claim added; the canonical-test limit stays stated in `step-7.10-style-exception.md` |
| qa-operator-actionability-report:C12 | PASS: the `(not observed in Phase 1)` mark is in `SKILL.md:26` and `:43` as at cycle 0 |
| qa-operator-actionability-report:C15 | PASS: nothing in `probes.py` sets `worker_done_seen` or `fenced_evidence` (`parse_worker_show` ends at `:465`; model defaults None and `unreadable`), so rules 2 and 3 cannot match; `sweep.md:16` and `SKILL.md:26` say so |
| qa-operator-actionability-report:C16 | PASS: argument re-checked (see test-traceability C24) |
| qa-operator-actionability-report:C17 | PASS: 3239 passed, ruff check clean, sync test passes |
| qa-evidence-quality-report:C1 | PASS: fixtures UNCH; `parse_worker_show` still reads `dispatch.assigneeHandle` (`probes.py:438`), present in 5 of 5 `captured-worker-show-*.json` |
| qa-evidence-quality-report:C2 | PASS: `dispatch.dispatchedAt` and `completedAt` read at `probes.py:439-440`; both keys present in 5 of 5 fixtures |
| qa-evidence-quality-report:C3 | PASS: UNCH (page and cursor handling; `page.hasMore` at `probes.py:1045`) |
| qa-evidence-quality-report:C4 | PASS: UNCH (unknown-Run handling) |
| qa-evidence-quality-report:C5 | PASS: UNCH (worktree path field `terminal.worktreePath`, version file `probes.py:69`) |
| qa-evidence-quality-report:C6 | PASS: every field the parser still reads is in the captured fixtures (`verdict`, `outcome`, `terminalState`, `nextAction` in 6 files; `worktreePath` in 5); the removed `agentWait` read is no longer a read |
| qa-evidence-quality-report:C8 | PASS: UNCH (project-folder key rule) |
| qa-evidence-quality-report:C12 | PASS: UNCH (disclosures) |
| qa-evidence-quality-report:C13 | PASS: UNCH (`UNATTENDED_EXPECT`, `test_worker_contract.py`) |
| qa-evidence-quality-report:C14 | PASS: re-run: 168 and 0 hits in the new primitives |
| qa-evidence-quality-report:C15 | PASS: the anchors are checked against the base copy `design-base.md`, unchanged; the live DESIGN differs from it only by the recorded revisions and the owner's two lines |
| qa-evidence-quality-report:C16 | PASS: argument re-checked (see test-traceability C24) |
| qa-evidence-quality-report:C17 | PASS: re-ran pytest, ruff check, format check and the sync test |
| qa-numbers-metrics-report:C1 | PASS: UNCH (the nine-entry list in contract, test, guide, `sweep.md`) |
| qa-numbers-metrics-report:C2 | PASS: 10 templates and 7 verbs (`probes.py:49-60`); 4 marked not called |
| qa-numbers-metrics-report:C3 | PASS: UNCH (`UNATTENDED_EXPECT` 31 entries) |
| qa-numbers-metrics-report:C4 | PASS: UNCH (routing rows) |
| qa-numbers-metrics-report:C5 | PASS: six sweep modules (`ls src/superclaude/cli/sweep/*.py` prints 6) |
| qa-numbers-metrics-report:C6 | PASS: UNCH (`commands.py` messages and exit codes) |
| qa-numbers-metrics-report:C7 | PASS: DESIGN `:839` still says `Total: 10 deviations.` (no section 13 edit) |
| qa-numbers-metrics-report:C8 | PASS: DESIGN `:1015` still says `Total: 23 open items.` |
| qa-numbers-metrics-report:C9 | PASS: limits unchanged (`probes.py:70-75`: 8 MiB, 1 MiB, 512 KiB, 256 KiB) |
| qa-numbers-metrics-report:C10 | PASS: 50 shows, 90 s total, 10 s per call (`probes.py:115-117`) unchanged; `spent` reuses the existing 1 s threshold |
| qa-numbers-metrics-report:C11 | PASS: UNCH (`-99` limit in `commands.py`) |
| qa-numbers-metrics-report:C12 | PASS: UNCH (window, Run id and timeout numbers in `sweep.md` and `SKILL.md:23-24`) |
| qa-numbers-metrics-report:C13 | PASS: 9 rules (`classify.py:333-343`), 12 sections, 8 classes, 6 package states unchanged; ten dimensions in `_SESSION_DIMENSIONS` unchanged |
| qa-numbers-metrics-report:C14 | PASS: count moved: file counts 37 and 12, DESIGN 1051 lines and 67 edited lines still recount; the new-file line total (14069) and the sum (15187) recount to 14254 and 15372 after the authorized fix edits (RC-N5); the "over 3000" row holds |
| qa-numbers-metrics-report:C15 | PASS: count moved: 713 sweep and command tests (saved 694), `121 = 14 + 74 + 15 + 12 + 6` holds again for the command test, scoped 3239 (saved 3220) |
| qa-numbers-metrics-report:C16 | PASS: UNCH (`pragmatic.md`: style counts) |
| qa-numbers-metrics-report:C17 | PASS: the saved Phase 14 numbers are history; 168 and the sync result were re-run |
| qa-numbers-metrics-report:C18 | PASS: the saved live-check files are not newer; they cannot be re-run (live Orca) and nothing they relied on changed |
| qa-numbers-metrics-report:C19 | PASS: UNCH (fixtures and `SOURCES.md`) |

Check totals: 238 rows; 238 PASS, 0 FAIL. None of the 238 cycle-0 PASS checks fails now, including the six that failed in the first re-check.

## Summary

- F_0 had 9 blocking-grade findings. On the live files 7 are RESOLVED (FIN-F1, FIN-F2, FIN-F3, FIN-F4, FIN-F6, FIN-F8, FIN-F9) and 2 are OPEN (FIN-F5, FIN-F7). `F_1` = {FIN-F5, FIN-F7}, so `|F_1|` = 2, strictly fewer than `|F_0|` = 9.
- FIN-F5 (the pinned "Orca unavailable" banner, DESIGN `:614`) and FIN-F7 (the chat reply that cannot relay an Orca outage: DESIGN `:662`, addendum `:29`, `pragmatic.md:23`) stay open for valid reasons: each needs an edit of DESIGN, the output style or the revision addendum, none of which the fix agent may change. Both need an owner decision, and they are the two items the owner's halt resolution sends to the follow-up issue.
- No regression: every id of the cycle-0 PASS set passes. The three owner-approved changes left no stale pin: the reverted skill and test match DESIGN `:662`, the DESIGN `:491` and `:760` edits match `classify.py` and `test_classify.py`, and the comments in `models.py` and `classify.py` no longer say `parse_worker_show` sets the wait time.
- No new BLOCKING or MAJOR finding. Seven MINOR notes (RC-N1 to RC-N7); RC-N1 (the missing caveat that a zero `working` count means nothing, and the inert Rule 4(a)) and RC-N3 (`yaml.safe_load` runs outside the time budget) are the follow-up candidates.
- Tests: 3239 passed in the scoped run, ruff check clean; eight mutations each fail the test that pins the behaviour; the sweep module stays read-only (allowlists and write surface unchanged, the only new import is `yaml` on an already-read string).

**Confidence:** Verified: 232/238 checks | Unverifiable: 6 | Unchecked: 0 | Confidence: 100.0% (232 / (238 - 6)). The six unverifiable rows are the checks about saved scratch runs or live records that cannot be re-run (qa-design-conformance-report:C23, qa-test-traceability-report:C21, qa-test-traceability-report:C22, qa-readonly-safety-report:C7, qa-fork-never-commit-report:C9, qa-numbers-metrics-report:C18); for each I confirmed from the files on disk that nothing the check relied on was changed. I also did not re-run the 16-minute full pytest or the timing test `test_speed_large_commands` (the checks that rely on them rest on "code unchanged" evidence, `git diff HEAD --stat` empty).
**Tool engagement:** Read: about 45 | Grep: about 34 | Glob: 1 | Bash: about 22 (counted from my own call log, approximate). Read + Grep + Glob (about 80) is below the 238 check ids, so by the agent rule this review is flagged as suspect on engagement alone; the mitigation is that most rows rest on one shared piece of evidence (the `find -newer` list, the set equality of the 37 paths, the scoped pytest and ruff runs, the grep set) which each row cites, and the nine findings plus the eight mutations got individual reads. No web research was done (tavily 0, WebSearch 0, WebFetch 0).

Limits of this review: the "UNCH" rows rest on mtime plus the fix log's sha256 baseline (not re-run); the live capture of Orca names needs a live command and was not attempted; whether any installed HOME copy of the style carries the exception is outside this gate (the read-only grep of `~/.claude/output-styles/pragmatic.md` shows 0 occurrences of `chat-summary`).

Verdict: FAIL
Blocking count: 2
