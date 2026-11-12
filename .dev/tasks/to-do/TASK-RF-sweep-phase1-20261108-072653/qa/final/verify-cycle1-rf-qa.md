# Verify cycle 1 (rf-qa): final gate, fix_authorization false

Date: 2026-11-13. Verifier: rf-qa (cold read of the live files; the fix log was read but not trusted).
`T` = `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653`.

## Basis (what I ran and read; all findings below are judged on the live files)

- Inputs read in full: `consolidated-findings-cycle0.md` (F_0, lines 1-115), `fix-log-cycle1.md` (including "Repair pass after review 1"), `cycle-ledger.md` (238 PASS ids), the 14 cycle-0 reports' check rows.
- `uv run pytest tests/sweep tests/commands tests/core tests/skills tests/recommend -q`: 3242 passed, exit 0 (the fix log's 3249 includes the 7 tests of `tests/cli/test_verify_sync_hooks.py`, which I ran separately: 7 passed). `uv run ruff check .`: All checks passed. `uv run ruff format --check src/superclaude/cli/sweep tests/sweep tests/commands`: 25 files already formatted. `uv run ruff format --check src/ tests/`: 12 files would be reformatted (same count as item 14.3; all Markdown per the fix log, none of the nine edited files).
- `sha256sum` of DESIGN, SPEC, the design addendum and the revision BUILD-REQUEST equals the four sums recorded at the top of the fix log. `find ... -newer consolidated-findings-cycle0.md` over `src tests docs plugins CHANGELOG.md .gitignore`: the nine edited files plus three files (`src/superclaude/hooks/hooks.json`, `src/superclaude/hooks/scripts/auggie-flag-clear.sh`, `src/superclaude/cli/install_hooks.py`) that have a newer mtime but no diff against HEAD (`git diff HEAD --stat` and `git status --short` print nothing for them). Under the task folder only the six result files named in the fix log are newer. `pragmatic.md`, `WORKER-CONTRACT.md`, `HOW-WE-WORK.md`, `sweep.md`, `models.py` and `commands.py` are not newer.
- `cmp` of `src/superclaude/skills/sc-sweep-protocol/SKILL.md` with `.claude/skills/sc-sweep-protocol/SKILL.md`, `sweep.md` with `.claude/commands/sc/sweep.md`, and the two HOW-WE-WORK copies: all identical. `git diff --cached --name-only -- .claude/`: 0 lines. HEAD equals `artifacts/base-commit.txt` (`5dc29d23b15eb7db4ead50623bb409f696a0d7d3`).
- Step 1.28 scoped `grep -rn 'src/superclaude'` over the sweep primitives: no output (rc 1); full-tree count: 168 (unchanged). Grep over `cli/sweep`, `sweep.md`, `SKILL.md` for `gh`, `{owner}`, `{repo}`, `SuperClaude-Org`: 0. WC-9 and lock-retry grep: 0. `chat-summary|exempt|coordinator assignment` in `cli/sweep/*.py`: 0. Em or en dash in `SKILL.md`: 0.
- Saved result files vs live collection: 166 / 51 / 254 / 94 / 124 tests collected for test_classify / test_report / test_probes_allowlist / test_cli_contract / test_sweep_command, equal to the counts in `test-classify.txt`, `test-report.txt`, `test-probes-allowlist.txt`, `test-cli-contract.txt`, `test-sweep-command.txt`.
- Not re-run by me: the 16-minute full `uv run pytest` (I relied on the fix log for its 3 failures and re-checked the two ruff ones: `importlib.util.find_spec('ruff')` is None and both `-k ruff` tests fail; `git diff HEAD --stat` over `src/superclaude/cli/eval tests/cli/eval tests/hooks src/superclaude/hooks` is empty). The timing test `test_speed_large_commands` did not finish in a 180 s isolated run here, so I stopped it; the code it tests is unchanged.

## F_0 findings, judged by the live files

### FIN-F1 (BLOCKING): RESOLVED

- Live: `src/superclaude/cli/sweep/probes.py:431-435` (`parse_worker_show` reads no `agentWait` from either place and the comment says why). A grep over `src/` and `tests/` for `_WAIT_TIME_KEYS`, `_wait_since`, `_agent_wait_present` finds nothing. `agent_wait`, `agent_wait_present`, `agent_wait_since` are set by nothing in production code (only the defaults at `models.py:78-90`; readers at `classify.py:228` and `report.py:121-122`).
- Rule 5: `classify.py:251-257` `_rule_working` returns None with a comment naming DESIGN open item 6 (`docs/designs/orchestrator-mode.md:996`: "Rule 5 cannot match; rows fall to the fallback"), so no guessed string can class a row `working`. Rule 4(a) (`classify.py:226-236`) is kept (DESIGN `:481` and SPEC `:252` require the rule in the table) but with the lookup gone it cannot match from an agent-wait entry in a live run, so no guessed key can print a false `waiting on a person` row.
- Tests: `tests/sweep/test_probes_allowlist.py:1552-1566` (new pin: both guessed places hold a wait, nothing is read); `tests/sweep/test_classify.py:365-372`, `:436` (Rule 5 never matches, four broken-condition inputs kept).
- What is still open but does not keep the finding open: the live-capture alternative (needs a live Orca command, not allowed here), and no text says that `working` is also never printed (`SP24_LINE`, `report.py:36-39`, names only stalled and fenced). The cycle-0 evidence already showed Rule 5 could not match on captured data (`1.0a-facts.md` row 6), so the live output did not change; the missing caveat is a note, not a new defect.

### FIN-F2 (MAJOR): RESOLVED

- `report.py:425-426` prints `<terminal> / <worktree> (<reason>)` from `r.safe.reason` through the table cell path; `report.py:40-43` and `:400` print `SAFE_TO_CLOSE_LINE` once under the Sessions heading. The reason is always built at `classify.py:488-491`.
- Test `tests/sweep/test_report.py:1046-1077` asserts both cells byte for byte and the single line. Mutation B below fails it.

### FIN-F3 (MAJOR): RESOLVED

- `report.py:54-55` (`waiting_signal`: "read what the Evidence cell names: the Orca agent-wait entry and the worker's last transcript lines, the contract, or the ready Task in Orca task-list") and `:60-61` (`fallback`: "read the row's Evidence and Notes cells, then the sources marked unscanned in Source coverage (if none, the session's last transcript lines)"). Each is true for every outcome of its rule; the map is still keyed by rule name (DESIGN `:643`). "Source coverage" is a real section heading (`report.py:204`).
- Test `test_report.py:1035-1043`; the existing map test (`:1010-1016`) still passes. Note (minor): the frozen-plan row's Evidence cell (`classify.py:240-244`) names the STOP codes, not a contract path, so "the contract" is a coarse pointer for that outcome.

### FIN-F4 (MAJOR): RESOLVED

- `classify.py:86` (`NOTE_NO_CONTRACT`) and `:327-330` (fallback attaches it when the Orca row is settled and no contract is attached). Tests `test_classify.py:607` and `:634`. Mutation C below fails the first.

### FIN-F5 (MAJOR): OPEN

- The OPEN reason is valid. Unchanged and still wrong in the way cycle 0 described: `report.py:33` (`WORKTREES_LINE`, "Orca unavailable"), `report.py:163-166` (`_discovery_incomplete` is true for any unscanned `orca worktree ps` row), printed at `report.py:194`. The literal and the condition are pinned by DESIGN `docs/designs/orchestrator-mode.md:614`, `tests/sweep/test_report.py:66` and `tests/sweep/test_cli_contract.py:443`; DESIGN is immutable for the fix agent, so this needs an owner decision. Counts toward F_1.

### FIN-F6 (MAJOR): RESOLVED

- `report.py:513-516` now reads "Orca became unavailable; the Orca sources marked unscanned above were not read". When Orca drops, the failing source is recorded as unscanned (`probes.py:1040-1071` record/skip, `:1231-1237`), so the sentence is true. Test `test_report.py:1080-1091`; the old sentence appears nowhere (grep of `src`, `tests`, `docs`, `plugins`, `CHANGELOG.md`: only the negative assertion at `test_report.py:1091`).

### FIN-F7 (MAJOR): OPEN

- Ordinary reply fixed; the exempt reply stays open and that OPEN reason is valid.
- Fixed part: `SKILL.md:25` takes `report_path`, `summary` and `orca_available`; `SKILL.md:26` prints, in the ordinary reply only, `Orca was unavailable; the counts may be missing Orca data (see Source coverage in the report).` (the repaired, true wording; "Source coverage" exists). `orca_available` is a top-level key of the JSON (`report.py:621`). Tests `tests/commands/test_sweep_command.py:559-569` and the moved pin at `:436-440`.
- Open part: the exempt reply (`SKILL.md:35`, `:43`; `pragmatic.md:23` "it contains the summary counts and the report path, without a DONE / NEXT table ...") still carries counts and path alone, so an exit 0 outage run relayed under the exception does not say Orca was unavailable. Changing it needs `pragmatic.md` and the addendum, which are revision authority and unchanged (hash and mtime). Counts toward F_1.

### FIN-F8 (MAJOR): RESOLVED

- `probes.py:179-184` (`_remaining`, `spent`), `:540-554` (`_stable` stops after one read when the file changed and the budget is spent, then raises `conflict: inconsistent observation`), budget passed at `:572`, `:652`, `:720`, `:801`, `:922`, `:1251-1252`, `:1306`, `:1355`. This is DESIGN 7.2 `:511` and the NFR-007 row `:808`. Public readers keep the single unconditional re-read, so `test_a_contract_changed_between_two_reads_is_re_read_once` (`test_probes_allowlist.py:1690`) still holds.
- Test `test_probes_allowlist.py:1787-1818` (two cases through `collect`). Mutation A below fails the `spent` case. Note (minor): only the contract reader is tested; ledger and transcript use the same `_stable`.

### FIN-F9 (MAJOR): RESOLVED

- `probes.py:22` (`import yaml`), `:672-684` (`_yaml_top` uses `yaml.safe_load`, catches `YAMLError`, `RecursionError`, `ValueError`; a non-mapping gives `{}`), `:687-710` (only string values are read; `artifacts` keeps string items). `_unquote` and the line reader are gone. Test `test_probes_allowlist.py:1731-1784`: 8 cases including the three divergent inputs of the finding and the date `2026-13-45`.
- The DESIGN import-list line (`:211`) is still not updated; DESIGN does not forbid `yaml`, so nothing fails (documentation gap, owner edit).

## New findings introduced by the fix

No new BLOCKING or MAJOR finding. Three MINOR findings (notes; they do not fail the review):

### FIN-N1 (MINOR, follow-up candidate): the skill's steps 3 and 4 now depart from DESIGN 7.6 and the departure is not recorded

- DESIGN `docs/designs/orchestrator-mode.md:662` says "(3) on exit 0, parse the stdout JSON, take `report_path` and `summary` only ... (4) print the counts from `summary` and the report path". `SKILL.md:25-26` now also takes `orca_available` and prints an outage line in the ordinary reply. The fix log's FIN-F7 block does not list this as a departure (it lists open items for the exempt reply only). DESIGN is immutable for the fix agent, so the line needs an owner edit, naturally together with the owner's decision on the open part of FIN-F7. No wrong behaviour: the extra field is a boolean the command itself wrote, and the added line is a fact, not advice (no banned word; `test_sweep_command.py` passes).
- Effect on the check ledger: `qa-design-conformance-report:C13` and `qa-completeness-report:C4` both claim the skill matches DESIGN 7.6; that claim is false on this one literal, so both are marked FAIL below for this non-blocking reason (cycle-0 checks that failed only for a MINOR reason also counted as FAIL). They would return to PASS when DESIGN `:662` is updated or the skill text is reverted.

### FIN-N2 (MINOR, follow-up candidate): `yaml.safe_load` is slow on a large contract and is not under the time budget

- Measured on a private /tmp script (deleted) with the repo's PyYAML: a 1 MiB file of `kN: v` lines parsed in 5.20 s; a 1 MiB flow list in 3.35 s (the pure-Python `SafeLoader`; `CSafeLoader` exists in this environment but `safe_load` does not use it). `CONTRACT_LIMIT` (`probes.py:72`) is 1 MiB per file and the parse is not checked against the 90 s `Budget`, so a few oversized contract files could use most of the budget. The old line reader was linear and fast. Normal contracts are a few KB, and an alias bomb of 151 bytes parsed in 0.01 s (aliases share objects), so this is a performance weakness, not a safety issue.

### FIN-N3 (MINOR): two small leftovers

- `_contract_from_text` (`probes.py:687-710`) now ignores a number, boolean or date value that it used to read as text (the fix log says so); no test pins that choice (`grep` of `tests/sweep/test_probes_allowlist.py` for a numeric contract value finds none).
- `phase-outputs/test-results/test-sweep-command-summary.md:138` still says "Test case total: 14 + 74 + 15 + 12 + 6 = 121" while `:9` says 124 (the fix log discloses that the prose below the regenerated blocks was not rewritten).

## Do the new tests fail when the behaviour is removed, and is the module still read-only

Mutations ran on a private copy (`mktemp -d /tmp/verify-c1-mut.*` with `src`, `tests/sweep`, `pyproject.toml`; `PYTHONPATH` pointed at the copy and I printed `probes.__file__` to confirm the copy was imported; deleted afterwards). No repository file was changed.

| Mutation (read against the live code and test) | Result |
|---|---|
| A (FIN-F8): in `probes._stable` replace `if budget is not None and budget.spent():` with `if False:` | `test_a_changed_contract_is_re_read_only_while_the_budget_allows[spent]` FAILED (`assert 2 == 1`, reads `[1, 1]`); the `budget-left` case passed. 1 failed, 1 passed |
| B (FIN-F2): drop the `(reason)` suffix from the Safe to close cell in `report._sessions` | `test_sessions_safe_to_close_cell_carries_its_reason` FAILED (cell `could not determine / could not determine` against the expected reason text) |
| C (FIN-F4): `notes = ()` in `classify._rule_fallback` | `test_settled_orca_row_without_a_contract_names_the_missing_contract` FAILED (`N_NO_CONTRACT` not in the notes); my first selector (`-k no_contract`) missed that test by name, so I reran with `-k "no_contract or without_a_contract"`: 1 failed, 4 passed |
| D (FIN-F1): restore a read of `projection.agentWait` in `parse_worker_show` | `test_parse_worker_show_reads_no_agent_wait_field_until_its_names_are_captured` FAILED (`agent_wait` is the dict, not None) |

Read-only check of the sweep module after the fix:

- Process starts: `subprocess` is imported and used only in `probes.py` (two `subprocess.run` calls at `:257` and `:308`); nothing in `classify.py` or `report.py` starts a process.
- Allowlists unchanged: `ALLOWED_ORCA` still has the 10 templates (`probes.py:47-58`, comment "10 templates, 7 verbs") and `ALLOWED_GIT` the one `status --porcelain=v1 -z --branch --untracked-files=all` entry. The fix added no argv.
- Files: `open(` is at `probes.py:559`, `:792`, `:856`, all `"rb"`. A grep for `write_text|write_bytes|.write(|os.replace|os.rename|mkdir|unlink|shutil|Popen|os.system` over `probes.py`, `classify.py`, `report.py` finds nothing. `commands.py` (the only writer, report path only) is not newer than the cycle-0 ledger. The only new import is `yaml`, and `yaml.safe_load` works on a string already read and bounded by `CONTRACT_LIMIT`.
- `tests/sweep/test_readonly.py` and `tests/sweep/conftest.py` (the process and write guards) are unchanged and pass.

## Checks

Rule I applied: a check is PASS when the file state it describes still conforms (DESIGN counts as amended by its own open items, e.g. open item 6 at `:996`) or when only a line number or a count moved; it is FAIL only when its claim is now false. Checks about saved scratch runs or artifacts cannot be re-run; for those I confirmed that nothing the check relied on was changed by the fix and say so. 238 rows, one per id of the cycle-0 PASS set. Two rows are FAIL (design-conformance C13 and completeness C4), both through the one non-blocking departure FIN-N1.

| Check id | Result |
|---|---|
| qa-design-conformance-report:C1 | PASS: every DESIGN 7.1 name is still defined in its module; the fix added only `_remaining` and `spent` and removed private helpers DESIGN does not name |
| qa-design-conformance-report:C2 | PASS: signatures as before plus optional `budget` arguments and `Budget.spent()` (same kind of widening as the MINOR notes F2 and F4) |
| qa-design-conformance-report:C3 | PASS: `models.py` not edited (mtime older than the ledger) |
| qa-design-conformance-report:C4 | PASS: `models.py` not edited |
| qa-design-conformance-report:C5 | PASS: `RULES` order and names unchanged (`classify.py:333-343`); rule 5 now returns None as DESIGN open item 6 (`:996`) says, its four conditions kept in the comment at `classify.py:251-257` |
| qa-design-conformance-report:C6 | PASS: 10 templates, `ALLOWED_GIT`, limits unchanged (`probes.py:47-78`); allowlist tests pass |
| qa-design-conformance-report:C7 | PASS: `models.py` unchanged, `orca_available` still a top-level key (`report.py:621`); golden key-set test passes |
| qa-design-conformance-report:C8 | PASS: `SECTIONS` still 12 entries (`report.py:534-547`); one line added under Sessions, columns unchanged (DESIGN `:643` fixes columns, not text) |
| qa-design-conformance-report:C9 | PASS: `commands.py` not edited |
| qa-design-conformance-report:C10 | PASS: `subprocess` only in `probes.py`; no write call in `probes`, `classify`, `report`; the one new import (`yaml`) is in `probes.py` |
| qa-design-conformance-report:C11 | PASS: `__init__.py` not edited |
| qa-design-conformance-report:C12 | PASS: `main.py` not edited |
| qa-design-conformance-report:C13 | FAIL: skill step 3 now also takes `orca_available` and step 4 prints an outage line, while DESIGN 7.6 `:662` says `report_path` and `summary` only (FIN-N1, non-blocking) |
| qa-design-conformance-report:C14 | PASS: the DESIGN 7.6 test list (`:666`) still passes; one skill-only pin was renamed with its text (`test_sweep_command.py:436-440`) |
| qa-design-conformance-report:C15 | PASS: style, addendum and exempt-reply text unchanged (sha256, mtime); the new line is ordinary reply only (`SKILL.md:26`) |
| qa-design-conformance-report:C16 | PASS: `WORKER-CONTRACT.md` and `test_worker_contract.py` not edited |
| qa-design-conformance-report:C17 | PASS: guide and plugin copy not edited; `cmp` identical |
| qa-design-conformance-report:C18 | PASS: `.gitignore` not edited |
| qa-design-conformance-report:C19 | PASS: every `test_...` token in DESIGN that is a function name still has a `def` in `tests/` (the tokens not found are file names, a prefix and the pre-existing worker-contract rename) |
| qa-design-conformance-report:C20 | PASS: Phase 14 files unchanged; my re-run: 3242 passed, ruff check clean, the same two ruff-module failures |
| qa-design-conformance-report:C21 | PASS: `sweep-help-pipx.txt`, the decision file and `commands.py` unchanged |
| qa-design-conformance-report:C22 | PASS: no departure beyond MINOR; the one new departure (FIN-N1) is MINOR |
| qa-design-conformance-report:C23 | PASS: saved live-check JSON files not newer (cannot be re-run; nothing relied on changed) |
| qa-design-conformance-report:C24 | PASS: `frozen` and `removable` path not edited; rule 5 is now an explicit no-op per open item 6 |
| qa-design-conformance-report:C25 | PASS: 0 `.claude/` paths staged; `.gitignore` unchanged; my /tmp copies deleted |
| qa-test-traceability-report:C1 | PASS: DESIGN-named test functions still resolve (see design C19) |
| qa-test-traceability-report:C2 | PASS: `tests/sweep/conftest.py` not edited |
| qa-test-traceability-report:C3 | PASS: `test_readonly.py` not edited; the fix added no integration mark |
| qa-test-traceability-report:C4 | PASS: real-git test in `test_readonly.py` not edited |
| qa-test-traceability-report:C5 | PASS: `test_readonly.py` not edited |
| qa-test-traceability-report:C6 | PASS: allowlist, negative, argv and result-class tests still present; tests were added, none removed (254 collected, all pass) |
| qa-test-traceability-report:C8 | PASS: per-rule case and `CLASSES` coverage now pin rule 5 as fallback per DESIGN `:996` (`test_classify.py:365-372`, `:436`); other rows unchanged (166 pass) |
| qa-test-traceability-report:C9 | PASS: FR-010 fixtures unchanged in meaning; file passes |
| qa-test-traceability-report:C10 | PASS: D9, SP-29, R2-B1, R3 fixtures unchanged; file passes |
| qa-test-traceability-report:C11 | PASS: `test_report.py` rows present; three tests added (51 pass) |
| qa-test-traceability-report:C12 | PASS: `test_cli_contract.py` rows present; the ids-only waiting test now builds waiting (a) from a blocked contract and still pins both lists (`:1065-1095`) |
| qa-test-traceability-report:C13 | PASS: `test_cli_registration.py` not edited |
| qa-test-traceability-report:C14 | PASS: budget-exhaustion publish test not edited |
| qa-test-traceability-report:C15 | PASS: `test_worker_contract.py` not edited |
| qa-test-traceability-report:C16 | PASS: routing, parity and severity test files not edited |
| qa-test-traceability-report:C17 | PASS: the 14 original 7.6 assertions still in `test_sweep_command.py` (124 pass); NFR-011 grep rc 1; full-tree count 168 |
| qa-test-traceability-report:C18 | PASS: addendum positive cases map to the same pins (one `success-*` pin renamed with its text) |
| qa-test-traceability-report:C19 | PASS: negative and exclusion pins unchanged |
| qa-test-traceability-report:C20 | PASS: `pragmatic.md` not edited; the seven-site tests pass |
| qa-test-traceability-report:C21 | PASS: scratch mutation run of cycle 0 cannot be re-run; the style, command and the skill pins it mutated still exist and pass (124), and my own mutations A to D fail as expected |
| qa-test-traceability-report:C22 | PASS: scratch code mutations of cycle 0 cannot be re-run; the tests they relied on still exist (the "three reads" pin at `test_probes_allowlist.py:1707-1728` still asserts 2 reads) |
| qa-test-traceability-report:C23 | PASS: the two severity modules and the parity file not edited; they pass in my run |
| qa-test-traceability-report:C24 | PASS: re-checked: ruff module absent (`find_spec` None), both `-k ruff` tests fail, no diff in eval and hooks |
| qa-test-traceability-report:C25 | PASS: `tests/sweep/fixtures` not newer |
| qa-test-traceability-report:C26 | PASS: count moved to 3242 passed; ruff check clean; mirror copies identical; sync test 7 passed |
| qa-validation-evidence-report:C1 | PASS: `cmp` of SKILL.md and sweep.md with the `.claude` copies identical; verify-sync test passes (I did not run `make verify-sync`) |
| qa-validation-evidence-report:C2 | PASS: `uv run ruff check .` All checks passed |
| qa-validation-evidence-report:C3 | PASS: `ruff format --check src/ tests/` prints 12 files would be reformatted (same count) |
| qa-validation-evidence-report:C4 | PASS: none of the nine edited files is among them (the edited sweep folders report 25 files formatted) |
| qa-validation-evidence-report:C5 | PASS: `ruff format --check src/superclaude/cli/sweep tests/sweep tests/commands`: 25 files already formatted |
| qa-validation-evidence-report:C6 | PASS: count moved: 3242 passed, exit 0 |
| qa-validation-evidence-report:C7 | PASS: the Phase 14 files predate the fix edits, so they are superseded; the fix log re-checks and my run cover the current tree |
| qa-validation-evidence-report:C8 | PASS: re-checked, ruff absent from the venv and no diff on the two test files' code |
| qa-validation-evidence-report:C9 | PASS: code under test unchanged (empty diff for `tests/hooks`, `src/superclaude/hooks`); I did not re-run it in isolation (180 s) |
| qa-validation-evidence-report:C10 | PASS: re-run, no output, rc 1 |
| qa-validation-evidence-report:C11 | PASS: re-run, 168 |
| qa-validation-evidence-report:C12 | PASS: `sweep-help-pipx.txt` and the decision file not edited |
| qa-validation-evidence-report:C13 | PASS: `commands.py` (the help screen source) not edited |
| qa-validation-evidence-report:C14 | PASS: staged `.claude/` paths 0; `.claude/` stays ignored |
| qa-scope-report:C1 | PASS: the fix added and removed no file; the path set of the inventory is unchanged |
| qa-scope-report:C2 | PASS: the nine files the fix edited were already in the inventory |
| qa-scope-report:C3 | PASS: no new file from the fix |
| qa-scope-report:C4 | PASS: only the nine edited files and six result files are newer than the ledger (three hooks files have a newer mtime and no diff) |
| qa-scope-report:C5 | PASS: WC-9 and lock-retry grep returns 0 |
| qa-scope-report:C6 | PASS: `WORKER-CONTRACT.md` not newer |
| qa-scope-report:C7 | PASS: `test_worker_contract.py` not edited |
| qa-scope-report:C8 | PASS: `commands.py` not edited; no new option or abstraction |
| qa-scope-report:C9 | PASS: allowlist still 10 templates |
| qa-scope-report:C10 | PASS: the guessed-key heuristic (S-m2) is gone (`probes.py:431-435`); the only addition is an optional `budget` argument |
| qa-scope-report:C11 | PASS: `pragmatic.md` not edited |
| qa-scope-report:C12 | PASS: WC-16 files not edited |
| qa-scope-report:C13 | PASS: guide and plugin copy not edited; `cmp` identical |
| qa-scope-report:C14 | PASS: grep for `chat-summary`, `exempt`, `coordinator assignment` in `cli/sweep` returns 0 |
| qa-scope-report:C15 | PASS: DESIGN sha256 equals the recorded sum |
| qa-scope-report:C16 | PASS: count moved: scoped run now 3242 |
| qa-scope-report:C17 | PASS: argument re-checked (see test-traceability C24) |
| qa-scope-report:C18 | PASS: pipx files not edited |
| qa-scope-report:C19 | PASS: 0 staged `.claude/` paths; `.gitignore` not edited |
| qa-readonly-safety-report:C1 | PASS: `subprocess.run` only at `probes.py:257` and `:308`; no shell, Popen or os.system in any sweep file |
| qa-readonly-safety-report:C2 | PASS: the `_orca` seam is not in the fix's edited regions; the argv tests pass |
| qa-readonly-safety-report:C3 | PASS: `ALLOWED_ORCA` still the same 10 templates (`probes.py:47-58`) and the allowlist tests pass |
| qa-readonly-safety-report:C4 | PASS: forbidden-token tests pass; no template added |
| qa-readonly-safety-report:C5 | PASS: `orca_binary()` unchanged (`probes.py:200-202`) |
| qa-readonly-safety-report:C6 | PASS: `ALLOWED_GIT` is the one status entry; git argv and env tests in `test_readonly.py` pass |
| qa-readonly-safety-report:C7 | PASS: scratch experiment cannot be re-run; `_git`, `ALLOWED_GIT` and `test_readonly.py` unchanged |
| qa-readonly-safety-report:C8 | PASS: no write call in `probes`, `classify`, `report`; `commands.py` unchanged |
| qa-readonly-safety-report:C9 | PASS: `open(` at `probes.py:559`, `:792`, `:856`, all `"rb"`; the new code only parses a string |
| qa-readonly-safety-report:C10 | PASS: `commands.py` not edited |
| qa-readonly-safety-report:C11 | PASS: the new `except (..., ValueError)` at `probes.py:682` wraps `yaml.safe_load` only; the argv check cannot raise inside it |
| qa-readonly-safety-report:C12 | PASS: `main.py` not edited |
| qa-readonly-safety-report:C13 | PASS: tests, lint, sync re-run (counts moved) |
| qa-readonly-safety-report:C14 | PASS: `test_readonly.py` not edited |
| qa-readonly-safety-report:C15 | PASS: `allowed-tools` at `SKILL.md:4` unchanged; steps 1 and 2 are still the only commands (`SKILL.md:23-24`) |
| qa-readonly-safety-report:C18 | PASS: argument re-checked (see test-traceability C24) |
| qa-readonly-safety-report:C19 | PASS: my experiments used /tmp copies, deleted; no repository file changed by me |
| qa-fork-never-commit-report:C1 | PASS: HEAD equals `base-commit.txt` (`5dc29d23b...`) |
| qa-fork-never-commit-report:C2 | PASS: 0 `.claude/` paths staged |
| qa-fork-never-commit-report:C3 | PASS: `.gitignore` not edited; `.dev/tasks` not ignored |
| qa-fork-never-commit-report:C4 | PASS: grep for `gh` over `cli/sweep`, `sweep.md`, `SKILL.md` returns 0 |
| qa-fork-never-commit-report:C5 | PASS: same grep, no `{owner}` or `{repo}` |
| qa-fork-never-commit-report:C6 | PASS: no `SuperClaude-Org` or `SuperClaude_Framework` in those files |
| qa-fork-never-commit-report:C7 | PASS: the new skill text (`SKILL.md:25-26`) tells no one to stage or commit anything |
| qa-fork-never-commit-report:C8 | PASS: `conftest.py` guard not edited |
| qa-fork-never-commit-report:C9 | PASS: pipx files not edited (saved scratch run cannot be re-run; nothing relied on changed) |
| qa-fork-never-commit-report:C10 | PASS: argument re-checked (see test-traceability C24) |
| qa-fork-never-commit-report:C11 | PASS: `cmp` of the two edited primitives with the `.claude` copies identical; ruff clean |
| qa-fork-never-commit-report:C12 | PASS: scoped folders pass (3242) |
| qa-fork-never-commit-report:C13 | PASS: my runs changed no repository file (no commit; HEAD unchanged) |
| qa-fork-never-commit-report:C14 | PASS: nothing is gitignored under `.dev/tasks`; the staging note stays a MINOR close-out item |
| qa-coordinator-usefulness-report:C1 | PASS: `NO_RECORDS` (`report.py:29`) and the waiting sections unchanged |
| qa-coordinator-usefulness-report:C10 | PASS: coverage lines still stated (`report.py:513-525` and the lower-bound lines) |
| qa-coordinator-usefulness-report:C11 | PASS: exempt reply is still counts and path alone; the ordinary reply gains one fact when `orca_available` is false; no advice; Read to `Report complete` (`SKILL.md:25`); observations sentence at `:66` |
| qa-coordinator-usefulness-report:C12 | PASS: argument re-checked; sweep and command tests pass |
| qa-failure-clarity-report:C1 | PASS: `commands.py` not edited; its tests pass |
| qa-failure-clarity-report:C2 | PASS: `commands.py` not edited |
| qa-failure-clarity-report:C3 | PASS: no-binding exit 2 path not edited |
| qa-failure-clarity-report:C6 | PASS: `PAGE_LINE` and the lower-bound line unchanged (`report.py:32`, `:517-520`) |
| qa-failure-clarity-report:C8 | PASS: `call_failed` rows still unscanned and unknown; the fix only adds a note for a settled Orca row without a contract |
| qa-failure-clarity-report:C9 | PASS: transcript-missing handling not edited |
| qa-failure-clarity-report:C10 | PASS: `NOTE_TRANSCRIPT_UNREADABLE` unchanged |
| qa-failure-clarity-report:C11 | PASS: `commands.py` not edited |
| qa-failure-clarity-report:C12 | PASS: `commands.py` not edited |
| qa-failure-clarity-report:C15 | PASS: exit-code text in `commands.py` and `SKILL.md:27` unchanged |
| qa-failure-clarity-report:C16 | PASS: `sanitize` use unchanged; the new report lines are fixed text |
| qa-failure-clarity-report:C17 | PASS: header `READ ONLY` (`report.py:181`) and footer `Inspection only.` (`:531`) unchanged |
| qa-failure-clarity-report:C18 | PASS: failure-path tests pass |
| qa-failure-clarity-report:C19 | PASS: argument re-checked |
| qa-failure-clarity-report:C20 | PASS: ruff check clean; format check clean on the sweep and command test folders |
| qa-maintainability-report:C2 | PASS: `_remaining` is shared by `call_timeout` and `spent`; the budget is threaded by one optional argument, not copied logic |
| qa-maintainability-report:C3 | PASS: new constants live in one module each (`SAFE_TO_CLOSE_LINE`, `NOTE_NO_CONTRACT`); the outage sentence is pinned by its test |
| qa-maintainability-report:C4 | PASS: no new path or environment rule |
| qa-maintainability-report:C5 | PASS: the new comments give reasons (open item 6, NFR-007), not restatements |
| qa-maintainability-report:C6 | PASS: new comments point at DESIGN open item 6 and step 1.0a, which exist |
| qa-maintainability-report:C7 | PASS: the new decisions (no `agentWait` read, `RecursionError` and `ValueError` caught) carry one-line comments or docstrings (`probes.py:432-434`, `:673-679`) |
| qa-maintainability-report:C8 | PASS: new names say what they do |
| qa-maintainability-report:C9 | PASS: the `agent_wait*` fields are now set only by tests; explained at `probes.py:432-434` and `classify.py:251-257` |
| qa-maintainability-report:C10 | PASS: 8 `type: ignore` uses, none in the new code |
| qa-maintainability-report:C11 | PASS: `main.py` and package layout not edited |
| qa-maintainability-report:C12 | PASS: duplicated normative text still pinned; the new sentences are pinned (`test_sweep_command.py:526-569`) |
| qa-maintainability-report:C13 | PASS: helpers still shared (`conftest.py` not edited) |
| qa-maintainability-report:C14 | PASS: ruff check clean; 25 sweep and command test files formatted |
| qa-maintainability-report:C15 | PASS: `cmp` of skill and command with `.claude` identical; sync test passes |
| qa-maintainability-report:C16 | PASS: count moved: sweep and command tests pass |
| qa-maintainability-report:C17 | PASS: my copies were under /tmp and deleted |
| qa-cross-artifact-report:C1 | PASS: WC-16 files not edited |
| qa-cross-artifact-report:C2 | PASS: contract and DESIGN block unchanged (DESIGN hash equal) |
| qa-cross-artifact-report:C3 | PASS: `WORKER-CONTRACT.md` and `sweep.md` not edited |
| qa-cross-artifact-report:C4 | PASS: cadence text in the guide, contract and `sweep.md` not edited |
| qa-cross-artifact-report:C5 | PASS: four flags unchanged in `commands.py`, `sweep.md`, `SKILL.md:19` |
| qa-cross-artifact-report:C6 | PASS: flag limits and Run id regex unchanged |
| qa-cross-artifact-report:C7 | PASS: report location code and text unchanged |
| qa-cross-artifact-report:C8 | PASS: JSON keys unchanged (`report.py:610-639`); golden test passes |
| qa-cross-artifact-report:C9 | PASS: owner-decision files unchanged |
| qa-cross-artifact-report:C10 | PASS: style, addendum and the exempt-reply pins unchanged |
| qa-cross-artifact-report:C11 | PASS: common-rule sentences in style and skill unchanged; pin tests pass |
| qa-cross-artifact-report:C12 | PASS: style sites unchanged |
| qa-cross-artifact-report:C13 | PASS: exclusion text unchanged |
| qa-cross-artifact-report:C14 | PASS: authority text unchanged |
| qa-cross-artifact-report:C15 | PASS: no activation claim added (`SKILL.md:49-51` unchanged) |
| qa-cross-artifact-report:C16 | PASS: routing rows and plugin copy unchanged; `cmp` identical |
| qa-cross-artifact-report:C17 | PASS: `CHANGELOG.md` not edited |
| qa-cross-artifact-report:C18 | PASS: docs files not edited |
| qa-cross-artifact-report:C19 | PASS: never-as-worker copies not edited |
| qa-cross-artifact-report:C20 | PASS: reproduced pytest (3242), ruff, sync test |
| qa-cross-artifact-report:C21 | PASS: argument re-checked |
| qa-cross-artifact-report:C22 | PASS: the path set of the inventory is unchanged |
| qa-cross-artifact-report:C23 | PASS: skill failure handling (`SKILL.md:27-29`) unchanged and matches the code |
| qa-cross-artifact-report:C24 | PASS: pipx evidence not edited |
| qa-completeness-report:C1 | PASS: pre-step files not edited |
| qa-completeness-report:C2 | PASS: every DESIGN 7.1 name still on disk (see design C1) |
| qa-completeness-report:C3 | PASS: all test files on disk and DESIGN section-11 names resolve |
| qa-completeness-report:C4 | FAIL: the skill is on disk but its steps 3 and 4 no longer match DESIGN 7.6 `:662` (FIN-N1, non-blocking) |
| qa-completeness-report:C5 | PASS: step 1.16a record not edited |
| qa-completeness-report:C6 | PASS: WC-16 files not edited |
| qa-completeness-report:C7 | PASS: routing rows unchanged |
| qa-completeness-report:C8 | PASS: sync clean (`cmp`, sync test); 0 staged `.claude/` paths |
| qa-completeness-report:C9 | PASS: lint clean; the 12 format failures are unchanged Markdown files |
| qa-completeness-report:C10 | PASS: scoped run 3242 passed; failure argument re-checked |
| qa-completeness-report:C11 | PASS: re-run, no output |
| qa-completeness-report:C12 | PASS: pipx output not edited |
| qa-completeness-report:C13 | PASS: `.gitignore` not edited |
| qa-completeness-report:C14 | PASS: every file, constant set and JSON key still delivered |
| qa-completeness-report:C15 | PASS: style edit not touched |
| qa-completeness-report:C16 | PASS: skill still carries the rule (`SKILL.md:35-51`) |
| qa-completeness-report:C17 | PASS: no new test module, detector or hook |
| qa-completeness-report:C18 | PASS: evidence files exist; the regenerated result files match live counts |
| qa-completeness-report:C19 | PASS: approval and implementation records not edited |
| qa-completeness-report:C20 | PASS: contract and `sweep.md` edits not touched |
| qa-completeness-report:C21 | PASS: path set unchanged (the fix created no file) |
| qa-completeness-report:C22 | PASS: no recorded step lost an output file |
| qa-operator-actionability-report:C1 | PASS: guide, contract and `sweep.md` not edited |
| qa-operator-actionability-report:C2 | PASS: flags and defaults unchanged |
| qa-operator-actionability-report:C3 | PASS: report location unchanged |
| qa-operator-actionability-report:C7 | PASS: report cells now give a reason for `could not determine` and invite no close or message |
| qa-operator-actionability-report:C8 | PASS: assignment text in style and skill unchanged |
| qa-operator-actionability-report:C9 | PASS: exempt and ordinary rules unchanged; the outage line only adds visibility |
| qa-operator-actionability-report:C11 | PASS: no activation claim added |
| qa-operator-actionability-report:C12 | PASS: mark text unchanged in the skill (`SKILL.md:26`, `:43`) |
| qa-operator-actionability-report:C15 | PASS: rules 2 and 3 not edited (`classify.py:215-223`); no code reads a stalled or fenced signal |
| qa-operator-actionability-report:C16 | PASS: argument re-checked |
| qa-operator-actionability-report:C17 | PASS: 3242 passed, ruff clean, sync test passes |
| qa-evidence-quality-report:C1 | PASS: fixtures not edited; join fields in `parse_worker_show` unchanged (`probes.py:436-438`) |
| qa-evidence-quality-report:C2 | PASS: time fields still read as before (`probes.py:439-440`) |
| qa-evidence-quality-report:C3 | PASS: page and cursor handling not edited |
| qa-evidence-quality-report:C4 | PASS: unknown-Run handling not edited |
| qa-evidence-quality-report:C5 | PASS: worktree path and version reads not edited |
| qa-evidence-quality-report:C6 | PASS: every field the parser still reads exists in the fixtures; the removed `agentWait` read is no longer a read |
| qa-evidence-quality-report:C8 | PASS: project-folder key rule not edited |
| qa-evidence-quality-report:C12 | PASS: disclosures unchanged |
| qa-evidence-quality-report:C13 | PASS: `UNATTENDED_EXPECT` file not edited |
| qa-evidence-quality-report:C14 | PASS: re-run, 168 and 0 hits |
| qa-evidence-quality-report:C15 | PASS: DESIGN and 1.0a-facts anchors unchanged (DESIGN hash equal) |
| qa-evidence-quality-report:C16 | PASS: argument re-checked |
| qa-evidence-quality-report:C17 | PASS: re-ran pytest, ruff check, format check, sync test |
| qa-numbers-metrics-report:C1 | PASS: nine-entry list not edited |
| qa-numbers-metrics-report:C2 | PASS: 10 templates and 7 verbs (`probes.py:47-59`) |
| qa-numbers-metrics-report:C3 | PASS: `test_worker_contract.py` not edited |
| qa-numbers-metrics-report:C4 | PASS: routing rows not edited |
| qa-numbers-metrics-report:C5 | PASS: six sweep modules still (`ls` lists six) |
| qa-numbers-metrics-report:C6 | PASS: `commands.py` messages and exit codes unchanged |
| qa-numbers-metrics-report:C7 | PASS: DESIGN unchanged |
| qa-numbers-metrics-report:C8 | PASS: DESIGN unchanged |
| qa-numbers-metrics-report:C9 | PASS: limits unchanged (`probes.py:71-73`) |
| qa-numbers-metrics-report:C10 | PASS: 50-call cap, 90 s budget and 10 s per call unchanged; `spent` reuses the existing 1 s threshold |
| qa-numbers-metrics-report:C11 | PASS: `-99` limit in `commands.py` unchanged |
| qa-numbers-metrics-report:C12 | PASS: window, Run id and timeout numbers unchanged in `sweep.md` and `SKILL.md:23-24` |
| qa-numbers-metrics-report:C13 | PASS: 9 rules and 12 sections unchanged (`classify.py:333-343`, `report.py:534-547`) |
| qa-numbers-metrics-report:C14 | PASS: count drift only: the saved sizes (14069 lines for the 37 new files, `final-inventory.md:139`) described the tree at inventory time and the fix grew the sweep files |
| qa-numbers-metrics-report:C15 | PASS: counts moved (command test 124, scoped 3242); the structure holds |
| qa-numbers-metrics-report:C16 | PASS: style counts unchanged (`pragmatic.md` not edited) |
| qa-numbers-metrics-report:C17 | PASS: saved Phase 14 numbers are history; 168 and the sync result re-run |
| qa-numbers-metrics-report:C18 | PASS: saved live-check files not newer (cannot be re-run) |
| qa-numbers-metrics-report:C19 | PASS: fixtures not edited |

Check totals: 238 rows; 236 PASS, 2 FAIL (both FIN-N1); 0 cycle-0 PASS checks fail for a blocking reason.

## Verdict

- F_0 had 9 blocking-grade findings. Live files: 7 RESOLVED (FIN-F1, FIN-F2, FIN-F3, FIN-F4, FIN-F6, FIN-F8, FIN-F9) and 2 OPEN (FIN-F5, FIN-F7). F_1 = {FIN-F5, FIN-F7}, so `|F_1|` = 2, strictly fewer than `|F_0|` = 9.
- FIN-F5 (the pinned "Orca unavailable" banner) and the exempt-reply part of FIN-F7 stay open for valid reasons: each needs an edit of DESIGN, the output style or the revision addendum, none of which the fix agent may change. Both need an owner decision. When the owner decides, DESIGN `:662` (FIN-N1) and `:211` (the `yaml` import, FIN-F9) can be updated in the same pass.
- No new BLOCKING or MAJOR finding. Three MINOR notes (FIN-N1, FIN-N2, FIN-N3), plus the minor notes under FIN-F1, FIN-F3 and FIN-F8.
- Tests: 3242 passed in the scoped run, ruff check clean; four mutations fail the new tests as intended; the sweep module stays read-only (allowlists and write surface unchanged).
- Regression note for the controller: two cycle-0 PASS checks (design-conformance C13, completeness C4) now fail, both through the non-blocking FIN-N1; I did not treat them as blocking.

Verdict: FAIL
Blocking count: 2
