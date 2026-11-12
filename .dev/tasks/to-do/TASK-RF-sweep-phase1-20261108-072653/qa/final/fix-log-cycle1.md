# Fix log, cycle 1 (item 14.25)

## Immutable-source checksums before the fix agent (recorded by the orchestrator)

Command: sha256sum docs/designs/orchestrator-mode.md .dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/revisions/chat-output-exception-20261109-133150/design-addendum.md .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/revisions/chat-output-exception-20261109-133150/BUILD-REQUEST.md

```
404c426d1e14a11e662b13ee0f6afbc4775c73b3e2aa4569486485947ede288c  docs/designs/orchestrator-mode.md
283054b289e95e565220bd8a9efe0375f790af6788849321aed80cf285e33300  .dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md
8a6f665983af0536732adf596bca8e3a5df34fb9dcfe1634c2f131cfe2a493e0  .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/revisions/chat-output-exception-20261109-133150/design-addendum.md
2f0328495ed73da58619d7fd38649bbcd2fb21f67618326bcdea48bfd0652eca  .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/revisions/chat-output-exception-20261109-133150/BUILD-REQUEST.md
```

(The fix agent appends its sections below.)

## Files edited

Source (`src/superclaude/`): `cli/sweep/probes.py`, `cli/sweep/classify.py`, `cli/sweep/report.py`, `skills/sc-sweep-protocol/SKILL.md`.
Tests: `tests/sweep/test_classify.py`, `tests/sweep/test_report.py`, `tests/sweep/test_probes_allowlist.py`, `tests/sweep/test_cli_contract.py`, `tests/commands/test_sweep_command.py`.
Result files under `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/`: `test-classify.txt`, `test-report.txt`, `test-probes-allowlist.txt`, `test-cli-contract.txt`, `test-sweep-command.txt`, `test-sweep-command-summary.md` (see "Result files").
This log.

Not edited, though the brief allowed it: `models.py`, `commands.py`. Line numbers below are as of the end of this fix run.

## Per-finding blocks

### FIN-F1 (BLOCKING): PARTLY FIXED (Rule 5 and the guessed names are fixed; two parts stay OPEN)

- Change, probes: `parse_worker_show` no longer reads `agentWait` from anywhere, and `_agent_wait_present`, `_agent_wait`, `_WAIT_TIME_KEYS` and `_wait_since` are deleted. `agent_wait`, `agent_wait_present` and `agent_wait_since` keep their model defaults (None, False, None). After the change: `src/superclaude/cli/sweep/probes.py:422` (`parse_worker_show`), comment at `:432-434`.
- Change, classify: `_rule_working` (Rule 5) always returns None, with a comment naming DESIGN open item 6 and the four conditions to restore once a read-only capture records the names. After the change: `src/superclaude/cli/sweep/classify.py:251-257`. A row that would reach Rule 5 falls to the fallback rule (DESIGN `docs/designs/orchestrator-mode.md:996`: "Rule 5 cannot match; rows fall to the fallback").
- Tests: `tests/sweep/test_classify.py:320` (the `working` case now expects `could not determine` through `fallback`), `:365` `test_rule_case_per_rule_1_to_9` (the `working` case expects rule `fallback`), `:372` `test_every_class_name_but_working_is_reached` (was `test_every_class_name_is_reached`), `:436` `test_rule_5_never_matches_while_the_agent_wait_names_are_uncaptured` (was `test_rule_5_needs_all_four_conditions`; its four broken-condition inputs are kept and still must not be `working`). New `tests/sweep/test_probes_allowlist.py:1552` `test_parse_worker_show_reads_no_agent_wait_field_until_its_names_are_captured`. `tests/sweep/test_cli_contract.py:1065` `test_waiting_lists_hold_row_ids_only` got its waiting (a) row from a blocked contract the Task names (rule 1) instead of an invented `agentWait` object (`:1074-1081`); it still pins both waiting lists as row ids.
- Pins moved with the text they pin: the "reaches every name in CLASSES" pin and the "rule 5 four-condition case" now describe the Rule 5 fallback behaviour (DESIGN section 11 lists both in the `test_classify.py` row at line 760; the cause is open item 6 at `:996`).
- Rule 4(a): the match in `classify._rule_waiting_signal` (`classify.py:226-236`) is KEPT. Lines that require it: DESIGN `docs/designs/orchestrator-mode.md:481` (the rule table, rule 4 is "waiting on a person (a) or (b)") and SPEC `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:252` (rule 4 "(a) non-null `agent_wait`") and `:578` (OQ-2, "non-null `agentWait`" stands in for the question read). OPEN: that part. Effect: with the lookup deleted nothing sets `agent_wait`, so waiting (a) from an agent-wait entry cannot match in a live run until the names are captured, and no guessed key can produce a false `waiting on a person` row; a person must decide whether the rule stays in the table.
- OPEN: the live-capture alternative (record one live worker's `worker-show` and `worktree ps --agent-wait` output in `readonly-probe.md`, add a `captured-*` fixture, update `1.0a-facts.md` row 6, then restore Rule 5 and the lookup). It needs a live Orca command.
- OPEN (documentation gap): nothing says that `working` is also never printed now. The report caveat `SP24_LINE` (`report.py:36`) and `sweep.md` name only stalled and fenced; `SP24_LINE` is pinned by DESIGN D7 and by `test_report.py`, and `sweep.md` is not editable here.
- Mutation proof (private copy under `/tmp/fixlog-mut/`, deleted): restoring the original `_rule_working` body failed `test_every_class_name_but_working_is_reached`, `test_rule_5_never_matches_while_the_agent_wait_names_are_uncaptured` and `test_rule_case_per_rule_1_to_9[working]` (3 failed, 163 passed in `test_classify.py`). Restoring a lookup of `agentWait` in `parse_worker_show` failed `test_parse_worker_show_reads_no_agent_wait_field_until_its_names_are_captured` (1 failed, 252 passed in `test_probes_allowlist.py`).

### FIN-F2 (MAJOR): FIXED

- Change: the Safe to close cell of the Sessions row is `<terminal> / <worktree> (<reason>)`, from `r.safe.reason`, still through `cell()` (so it is cut at 200 characters like every cell); a row with no reason keeps the old cell. One line under the Sessions heading says it once: `SAFE_TO_CLOSE_LINE`, "Safe to close never prints yes in Phase 1: each cell gives the terminal value, the worktree value and, in parentheses, the reason for both." After the change: `src/superclaude/cli/sweep/report.py:40` (constant), `:400` (printed after `SP24_LINE`), `:425-426` (cell).
- Test: `tests/sweep/test_report.py:1046` `test_sessions_safe_to_close_cell_carries_its_reason` (a hand-built row and a classifier-built released row; asserts both cells byte for byte and that the line appears once).
- Mutation proof: removing the reason from the cell failed `test_sessions_safe_to_close_cell_carries_its_reason`; removing `SAFE_TO_CLOSE_LINE` from the section failed the same test (1 failed, 50 passed each).

### FIN-F3 (MAJOR): FIXED (the map stays keyed by rule name; no re-keying)

- Change: the `waiting_signal` entry reads "read what the Evidence cell names: the Orca agent-wait entry and the worker's last transcript lines, the contract, or the ready Task in Orca task-list" (true for an agent wait, a frozen plan and a ready Task). The `fallback` entry reads "read the row's Evidence and Notes cells, then the sources marked unscanned in Source coverage (if none, the session's last transcript lines)" (no longer an empty list when no source is unscanned). A comment above the map says why. After the change: `src/superclaude/cli/sweep/report.py:54-55` and `:60-61`.
- Test: `tests/sweep/test_report.py:1035` `test_next_inspection_waiting_signal_and_fallback_fit_every_outcome` (new). The existing `test_next_inspection_map_has_an_entry_per_rule_and_only_names_a_read` is unchanged and still passes: every rule has an entry and no entry holds stop, retry, release, merge or removal.
- Mutation proof: restoring the two original sentences failed `test_next_inspection_waiting_signal_and_fallback_fit_every_outcome` (1 failed, 50 passed).

### FIN-F4 (MAJOR): FIXED

- Change: a new note `NOTE_NO_CONTRACT` = "no contract read for this row; finished needs a parsed contract" is attached by the fallback rule when the Orca row is settled (outcome succeeded, partial or failed) and no contract is attached. After the change: `src/superclaude/cli/sweep/classify.py:86` (constant), `:327-330` (use in `_rule_fallback`). No existing exact note list changed: `tests/sweep` passed unchanged apart from the tests named here.
- Tests: `tests/sweep/test_classify.py:94` (`N_NO_CONTRACT`), `:607` `test_settled_orca_row_without_a_contract_names_the_missing_contract` (the live shape: exited, completed, succeeded, no contract; also `partial` and `failed`), `:634` `test_no_contract_note_is_only_for_a_settled_row_with_no_contract` (not settled, no Orca row, contract not settled, finished: no note).
- Mutation proof: removing the note from the fallback rule failed `test_settled_orca_row_without_a_contract_names_the_missing_contract` (1 failed, 165 passed).

### FIN-F5 (MAJOR): OPEN

Not edited. DESIGN `docs/designs/orchestrator-mode.md:614` pins the literal `[child worktrees not discovered: Orca unavailable; worktree count is a lower bound]` and the condition; `tests/sweep/test_report.py` (`WORKTREES_BANNER`) and `tests/sweep/test_cli_contract.py` pin it again. Changing the text or the condition needs an owner decision and an edit of DESIGN, which this agent never edits. When the owner decides: print the literal only when `result.orca_available` is false, otherwise `[child worktrees not discovered: orca worktree ps unscanned (<its reason>); worktree count is a lower bound]`, and move DESIGN `:614` and the two test pins with it.

### FIN-F6 (MAJOR): FIXED

- Change: the line is now "- Orca became unavailable; the Orca sources marked unscanned above were not read". After the change: `src/superclaude/cli/sweep/report.py:514-516`.
- Test: `tests/sweep/test_report.py:1080` `test_orca_dropping_mid_run_is_not_reported_as_nothing_read` (new; no test pinned the old sentence).
- Mutation proof: restoring the old sentence failed that test (1 failed, 50 passed).

### FIN-F7 (MAJOR): PARTLY FIXED (the ordinary reply is fixed; the exempt reply stays OPEN)

- Change: SKILL.md step 3 takes `orca_available` as well ("take only `report_path`, `summary` and `orca_available`"); step 4 adds "In the ordinary reply, when `orca_available` is false, also print the one line `Orca was unavailable; the counts come from disk sources only.` The exempt reply described below stays the counts and the path alone." After the change: `src/superclaude/skills/sc-sweep-protocol/SKILL.md:25` and `:26`. No em dash, en dash or banned word was added (the skill test for those passes).
- Tests (`tests/commands/test_sweep_command.py`): `:559` `test_sweep_skill_step3_takes_orca_available_from_the_json`, `:563` `test_sweep_skill_step4_prints_the_orca_outage_line_in_the_ordinary_reply`, `:567` `test_sweep_skill_step4_keeps_the_exempt_reply_counts_and_path_alone` (new, one per added sentence; sentences held in `_OUTAGE_SENTENCE` and `_EXEMPT_ALONE_SENTENCE` at `:526-531`). Pin moved with its text: the skill-only pin `success-parse-takes-only-report-path-and-summary` now reads `success-parse-takes-only-report-path-summary-and-orca-available` with the new step 3 wording (`:437`); the old wording no longer exists in the skill.
- OPEN: the exempt reply. An exit 0 outage run still prints the counts and the path alone there, so the outage is not relayed. Fixing it needs `src/superclaude/output-styles/pragmatic.md` and the addendum text ("counts and path alone") to allow one line, and both are revision authority. The new step 4 sentence says the exempt reply stays counts and path alone, so the skill matches the style as it stands.
- `make sync-dev` and `make verify-sync` were not run (the orchestrator runs them after the gate); the project `.claude/` copy of this skill is stale until then. Nothing under `.claude/` was staged or edited.
- Mutation proof (private copy of `src` and `tests`): reverting step 3 failed `test_sweep_skill_step3_takes_orca_available_from_the_json` and the moved pin `test_skill_states_clause[success-parse-takes-only-report-path-summary-and-orca-available]`; removing the two step 4 sentences failed `test_sweep_skill_step4_prints_the_orca_outage_line_in_the_ordinary_reply` and `test_sweep_skill_step4_keeps_the_exempt_reply_counts_and_path_alone` (2 failed, 122 passed each).

### FIN-F8 (MAJOR): FIXED through option (b); option (a) stays OPEN

- Change: `Budget.spent()` (true when under 1 s of the total is left, the same threshold `call_timeout` uses; `_remaining()` is the shared arithmetic) and an optional `budget` argument on `_stable`, which now stops after one read when the file changed and the budget is spent, giving the existing `conflict: inconsistent observation` reason. The budget is passed through the three readers that use `_stable`: contract (`_contract`, `_read_contracts`), ledger (`_ledger`, `_packages`, `_read_worktree`) and transcript (`_transcript`, `_read_transcripts`), all from `collect`. The public readers (`read_contract`, `read_ledger`, `read_packages`, `read_transcript_tail`) are unchanged and keep the unconditional single re-read. After the change: `src/superclaude/cli/sweep/probes.py:179-184` (`_remaining`, `spent`), `:540-554` (`_stable`), `:572` (`_ledger`), `:652`, `:719` (`_contract`), `:800`, `:921`, `:1250-1251`, `:1305`, `:1354`. DESIGN 7.1 shows no budget argument for these readers; the argument is optional, the same kind of widening as FIN-F11.
- Test: `tests/sweep/test_probes_allowlist.py:1782` `test_a_changed_contract_is_re_read_only_while_the_budget_allows` (two cases through `collect`: budget left gives two reads and the new value; budget spent gives one read and `conflict: inconsistent observation`). Only the contract reader is tested; the ledger and transcript threading rests on the same `_stable` call.
- OPEN: option (a), editing DESIGN 7.2 `:511` and the NFR-007 row `:808`.
- Mutation proof: removing the `budget.spent()` break failed `test_a_changed_contract_is_re_read_only_while_the_budget_allows[spent]` (1 failed, 252 passed).

### FIN-F9 (MAJOR): FIXED; the DESIGN import-list line stays OPEN

- Change: `_yaml_top` now calls `yaml.safe_load` inside `try/except` and treats a non-mapping result as `{}`; `_unquote` is deleted. `import yaml` was added to `probes.py`. Two choices go beyond the brief and are recorded here: the except clause also catches `RecursionError` (a contract nested too deep for the parser would otherwise stop the whole sweep, an unreadable file must be one unreadable row), and `_contract_from_text` now reads only string values (a number, boolean or date value is no longer turned into text; before, `reason: 404` read as "404", now it reads as absent) and keeps only string entries of `artifacts`. The reads stay bounded and read-only: the caller still enforces `CONTRACT_LIMIT` (1 MiB) before the parse and `safe_load` builds no object from a tag. After the change: `src/superclaude/cli/sweep/probes.py:22` (import), `:672-683` (`_yaml_top`), `:686-710` (`_contract_from_text`).
- Test: `tests/sweep/test_probes_allowlist.py:1769` `test_contract_fields_are_read_by_yaml_safe_load` (7 cases: the three divergent inputs of the finding as `trailing-comment`, `continued-plain-scalar` and `quoted-flow-item-with-comma`, plus `flow-list-with-comment`, `invalid-yaml`, `not-a-mapping` and `nested-too-deep`).
- OPEN (documentation gap): DESIGN `docs/designs/orchestrator-mode.md:211` does not list `yaml` among the imports of `probes.py`; DESIGN does not forbid it (the ban list in `tests/sweep/test_classify.py` has no `yaml`), so nothing fails, and the line needs an owner edit.
- Mutation proof: restoring a hand-written line reader with the original logic failed 5 cases (`trailing-comment`, `continued-plain-scalar`, `quoted-flow-item-with-comma`, `flow-list-with-comment`, `invalid-yaml`; 5 failed, 248 passed); removing `RecursionError` from the except clause failed `nested-too-deep` (1 failed, 252 passed). `not-a-mapping` passes under the old reader too; it pins the new `isinstance` guard only.

## Result files

The pytest stdout block of the five `.txt` files was replaced with the real new `-v` output of the same command (only the span from the `test session starts` banner to the final `N passed` line; every other line is unchanged), using a private script under `/tmp` that ran each command; the files were not edited by hand. The `pytest exit code: 0 (N passed)` line of `test-classify.txt` carries the new count. The case-to-test maps and prose below those blocks were not rewritten and still quote the earlier counts. `test-sweep-command-summary.md` was edited by hand (counts and one added paragraph).

## Re-check commands (in the order of the brief)

### 1. Immutable-source checksums

Command: `sha256sum docs/designs/orchestrator-mode.md .dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/revisions/chat-output-exception-20261109-133150/design-addendum.md .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/revisions/chat-output-exception-20261109-133150/BUILD-REQUEST.md`. Exit code 0.

```
404c426d1e14a11e662b13ee0f6afbc4775c73b3e2aa4569486485947ede288c  docs/designs/orchestrator-mode.md
283054b289e95e565220bd8a9efe0375f790af6788849321aed80cf285e33300  .dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md
8a6f665983af0536732adf596bca8e3a5df34fb9dcfe1634c2f131cfe2a493e0  .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/revisions/chat-output-exception-20261109-133150/design-addendum.md
2f0328495ed73da58619d7fd38649bbcd2fb21f67618326bcdea48bfd0652eca  .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/revisions/chat-output-exception-20261109-133150/BUILD-REQUEST.md
```

PASS: all four sums equal the four recorded at the top of this log.

### 2. Lint and format

Commands: `make lint ; uv run ruff check . ; uv run ruff format --check src/ tests/`.

- `make lint`: exit 0. Last lines: `Running linter...`, `uv run ruff check .`, `All checks passed!`. (Its architecture-policy step printed `PASS - architecture policy compliant (5 warning(s))`.) PASS.
- `uv run ruff check .`: exit 0, `All checks passed!`. PASS.
- `uv run ruff format --check src/ tests/`: exit 1, last line `12 files would be reformatted, 1823 files already formatted`. The 12 are the same pre-existing failures item 14.3 recorded, all Markdown files, none edited by this fix run: `src/superclaude/examples/release-spec-template.md`, `src/superclaude/skills/sc-cleanup-audit-protocol/rules/dynamic-use-checklist.md`, `src/superclaude/skills/sc-cli-portify-protocol/refs/code-templates.md`, `src/superclaude/skills/sc-cli-portify-protocol/refs/pipeline-spec.md`, `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`, `src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md`, `src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md`, `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md`, `src/superclaude/skills/sc-validate-tests-protocol/SKILL.md`, `src/superclaude/templates/documents/release-spec-template.md`, `tests/roadmap/fixtures/recurrence/dispatch_reachability/skipped_verification_step_case.md`, `tests/roadmap/fixtures/recurrence/retry_contract/retry_loop_no_terminal_case.md`. None is a file edited here (`sc-sweep-protocol/SKILL.md` is not among them). `uv run ruff format` was run on the eight edited Python files only (it reformatted `tests/sweep/test_probes_allowlist.py`: one signature joined onto one line). PASS for the edited files; FAIL (pre-existing, not mine) for the 12 files above.

### 3. Targeted pytest

Command: `uv run pytest tests/sweep tests/commands tests/core tests/skills tests/recommend -v`. Exit code 0. Last line: `======================= 3241 passed in 61.99s (0:01:01) =======================`. 0 failed, 0 errors. PASS.

### 4. Full pytest

Command: `uv run pytest` (Bash timeout 600000 ms; the harness moved it to the background after 600 s and it ran to the end). Pytest exit code 1 (the wrapping shell command printed `exit 0` for its `tail`). Last line: `= 3 failed, 25273 passed, 149 skipped, 2 xpassed, 32 warnings in 988.73s (0:16:28) =`. Failing ids:

```text
FAILED tests/cli/eval/test_claude_process_adapter.py::test_ruff_flags_synthetic_anthropic_import_under_cli_eval
FAILED tests/cli/eval/test_claude_process_adapter.py::test_ruff_passes_on_real_adapter_module
FAILED tests/cli/test_verify_sync_hooks.py::test_V1_clean_tree_exits_zero
```

- The two `test_ruff_*` failures are the pre-existing ones of item 14.4 (`phase14-full-pytest.md`): ruff is not importable in the venv.
- The timing test `tests/hooks/test_launch_level_guard.py::test_speed_large_commands[1MB-big]` that failed in item 14.4 passed in this run.
- `tests/cli/test_verify_sync_hooks.py::test_V1_clean_tree_exits_zero` is NEW and is caused by this fix run: its output says `DIFFERS: sc-sweep-protocol` (`src/superclaude/skills/sc-sweep-protocol/SKILL.md` and `.claude/skills/sc-sweep-protocol/SKILL.md` differ) and no other skill, agent or command differs. The cause is my FIN-F7 edit of `SKILL.md`; the brief forbids `make sync-dev` and `make verify-sync` for this agent. Not run, so not observed: the orchestrator's `make sync-dev` should clear it, after which `make verify-sync` and this test should pass.

Verdict: FAIL by pytest exit code. Two failures are pre-existing, one is mine and waits only for `make sync-dev`; no other failure.

### 5. Hardcoded source paths in the sweep primitives

Command: `grep -rn 'src/superclaude' src/superclaude/commands/sweep.md src/superclaude/skills/sc-sweep-protocol/ src/superclaude/core/WORKER-CONTRACT.md src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. Exit code 1 (no match), no output. PASS (expected no output).

### 6. Count of `src/superclaude` references in installed primitives

Command: `grep -rn 'src/superclaude' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core src/superclaude/hooks | wc -l`. Output: `168` (grep also warned that six `__pycache__` binary files match; they are in other skills and were not touched). PASS (expected 168).

## Files not touched

Not edited by this run: `docs/designs/orchestrator-mode.md` (DESIGN), `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md` (SPEC), the `revisions/` folder, the OQ decision files, `src/superclaude/output-styles/pragmatic.md`, `src/superclaude/core/WORKER-CONTRACT.md`, `HOW-WE-WORK.md` and its plugin copy, `CHANGELOG.md`, `.gitignore`, `docs/`, `src/superclaude/commands/sweep.md`, `tests/core`, `tests/recommend`, `tests/skills`, `tests/sweep/fixtures`, `tests/sweep/conftest.py`, `tests/sweep/test_readonly.py`, `tests/sweep/test_cli_registration.py`, `src/superclaude/cli/sweep/__init__.py`, `models.py`, `commands.py`, any QA report, the consolidated findings file, the cycle ledger, the plan file, and any `.claude/` or installed HOME path. Nothing was staged or committed. Open items for the orchestrator or owner: FIN-F5 (whole), the Rule 4(a) and live-capture parts of FIN-F1, the exempt-reply part of FIN-F7, option (a) of FIN-F8, the DESIGN import-list line of FIN-F9, and the documentation gap that nothing says `working` is no longer observed.

## Executor re-run after the fix agent (appended by the orchestrator)

The fix agent's brief forbade `make sync-dev` and `make verify-sync`; the orchestrator ran them after reading the log.

- `make sync-dev`: exit 0 (Agents 48, Commands 47, Hooks 16, Templates 52 files copied to the gitignored `.claude/`). PASS.
- `make verify-sync`: exit 0, "All components in sync." PASS.
- `git diff --cached --name-only -- .claude/`: no output (nothing under `.claude/` is staged). PASS.
- `uv run pytest tests/cli/test_verify_sync_hooks.py -q`: 7 passed. The `test_V1_clean_tree_exits_zero` failure noted in section 4 above is cleared. PASS.
- `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`: exit 0. PASS.
- Protected-file check (orchestrator, sha256 baseline of 126 files taken before the spawn): all 126 unchanged. PASS. Only the nine editable files listed above differ from their baselines (`models.py` and `commands.py` untouched).
- Pytest result of section 4 stands: 3 failed, of which 2 are pre-existing (ruff not importable in the venv) and 1 (sync) is cleared above; the timing test of item 14.4 passed this time.

## Repair pass after review 1 (orchestrator, three findings of the independent review)

The first independent review of this fix cycle raised three blocking findings in the fix agent's new text. The orchestrator fixed them in one pass; this section supersedes the wording of the FIN-F7 and FIN-F9 blocks above where they differ.

- F1.1 (FIN-F7 wording): the ordinary-reply line said "the counts come from disk sources only", which is false after a mid-run Orca drop (Orca calls made before the drop were read). It now reads `Orca was unavailable; the counts may be missing Orca data (see Source coverage in the report).` Changed in `src/superclaude/skills/sc-sweep-protocol/SKILL.md:26` and in `_OUTAGE_SENTENCE` at `tests/commands/test_sweep_command.py:526-529`. Mutation proof: restoring the old sentence in the skill failed `test_sweep_skill_step4_prints_the_orca_outage_line_in_the_ordinary_reply` (1 failed, 123 passed).
- F1.2 (FIN-F9): `yaml.safe_load` raises `ValueError`, not `YAMLError`, on a scalar such as the date `2026-13-45`. `_yaml_top` now also catches `ValueError` (`src/superclaude/cli/sweep/probes.py:682`, docstring `:673-679`) and a new case `rejected-date-scalar` (8 cases now) pins it in `test_contract_fields_are_read_by_yaml_safe_load`. Mutation proof: removing `ValueError` from the except tuple failed that case (1 failed, 253 deselected).
- F1.3 (stale result map): `test-classify.txt:190` and `:193` now name `test_every_class_name_but_working_is_reached` and `test_rule_5_never_matches_while_the_agent_wait_names_are_uncaptured`. The pytest blocks of `test-probes-allowlist.txt` (254 passed) and `test-sweep-command.txt` (124 passed) were regenerated from real `-v` runs.
- Re-checks: `make sync-dev` exit 0; `make verify-sync` exit 0; `uv run ruff check .` all checks passed; `ruff format --check` on `src/superclaude/cli/sweep`, `tests/sweep`, `tests/commands` clean; `uv run pytest tests/sweep tests/commands tests/core tests/skills tests/recommend tests/cli/test_verify_sync_hooks.py -q` 3249 passed; `cmp` of the two HOW-WE-WORK copies identical; nothing under `.claude/` staged; the 126 protected files unchanged. PASS.

## Halt resolution (owner decision of 2026-11-12; appended by the orchestrator)

Item 14.28 halted on its regression rule (six check ids that passed at cycle 0 failed in a cycle-1 verifier report). The owner decided "All 3 approved" (record: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/FINAL-GATE-halt-resolution-decision.md`). Changes made, in this order:

1. FIN-F7 edit reverted: `src/superclaude/skills/sc-sweep-protocol/SKILL.md` and `tests/commands/test_sweep_command.py` were restored byte for byte from the copies taken before this fix cycle (the only differences between those copies and the fixed files were the FIN-F7 edits). The three FIN-F7 tests, `_OUTAGE_SENTENCE` and `_EXEMPT_ALONE_SENTENCE` are gone, and the step 3 pin reads `success-parse-takes-only-report-path-and-summary` again. FIN-F7 is therefore OPEN as a whole; this supersedes the "PARTLY FIXED" status, the FIN-F7 block and the F1.1 line of the repair section above. `test-sweep-command.txt` (121 passed) and `test-sweep-command-summary.md` were updated.
2. DESIGN `docs/designs/orchestrator-mode.md` edited by the owner's decision: line 491 now says Rule 5 is inert until open item 6 closes (its four conditions stay listed, the `worker-show` names are marked NOT captured, UNVERIFIED), and line 760 (the `test_classify.py` row) now says the `working` case expects the fallback rule, every class but `working` is reached, and the rule 5 case never matches while the names are uncaptured. Section 13 is unchanged.
3. Comments: `src/superclaude/cli/sweep/models.py` (the three agent-wait fields are marked reserved) and `classify.py:229` no longer say `parse_worker_show` sets the wait time.
- New DESIGN sha256 (supersedes the DESIGN sum at the top of this log; the SPEC, addendum and revision request sums are unchanged): `83816a69c6c21ad80cd11b7881bb6a54c67c9f3919361aa77e5057aaacc7d45d  docs/designs/orchestrator-mode.md`.
- Re-checks after the repair: `make sync-dev` exit 0; `make verify-sync` exit 0 ("All components in sync."); `uv run ruff check .` all checks passed; `ruff format --check` clean on `src/superclaude/cli/sweep`, `tests/sweep`, `tests/commands`; `uv run pytest tests/sweep tests/commands tests/core tests/skills tests/recommend tests/cli/test_verify_sync_hooks.py -q` 3246 passed; `cmp` of the two HOW-WE-WORK copies identical; nothing under `.claude/` staged. PASS.
- The two cycle-1 verifiers are run again over the repaired tree; their reports are `verify-cycle1-rf-qa-recheck.md` and `verify-cycle1-rf-qa-qualitative-recheck.md`, and item 14.28 is evaluated on them. The halted decision is kept as `cycle1-decision-halted.md`.
