---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-restoreTheSweepS-20261116-223216
version: "1"
priority: Medium
created_date: "2026-11-16"
---

# Restore the sweep's working class using the real Orca names

Source: ./source.md
Goal: A worker that Orca reports as running (liveness `live`, outcome `in_progress`, `agentWait` present and null) is classed `working` by `superclaude sweep run`, and the code, tests and design doc all use the names seen in the real Orca capture of 2026-11-16.

## Constraints

- The sweep stays read-only: add no Orca command to `ALLOWED_ORCA` in `src/superclaude/cli/sweep/probes.py`, change nothing about what the sweep may run, and leave the git protections for INV-008 (fsmonitor off on every git call, submodules ignored, `unscanned` for a worktree where a selected filter could run) untouched.
- Edit `src/superclaude/` and `tests/` and `docs/` only; never the `.claude/` mirrors. No skill, agent, command or hook is changed, so `make sync-dev` is not needed; run `make verify-sync` once at the end of Task 5.
- What a non-null `agentWait` looks like was never captured. Code comments and docs must label its meaning UNVERIFIED and must not invent its shape. A non-null `agentWait` stays with rule 4 (`waiting_signal`, class waiting on a person) exactly as today, and is never `working`.
- `orca.status == "ready"` at `src/superclaude/cli/sweep/classify.py` (rule 4, inside `_rule_waiting_signal`) is not a mismatch: the sweep itself sets `status="ready"` on the rows it builds from `task-list --ready` in `_run_rows` (`src/superclaude/cli/sweep/probes.py`). Leave it as it is.
- The report footnote constant `SP24` ("Stalled and fenced are not observed in Phase 1; a zero count does not mean none occurred.") in `src/superclaude/cli/sweep/report.py` and `tests/sweep/test_report.py` is a wording contract pinned by tests and it is about stalled and fenced, which stay unobserved. Do not change its wording. If the evidence shows a report wording change is needed, stop and report it as an owner decision.
- Real values the code must match, from the 2026-11-16 capture of a running worker (`/home/coder/captures/q24-orca-capture2-20261116.md`): `result.dispatch.status` is `dispatched`; `result.projection.outcome` is `in_progress`; `result.projection.liveness.verdict` is `live`; `agentWait` is present with value null at `result.observation.agentWait` and at `result.terminal.agentWait`. A finished worker shows `completed`, `succeeded`, `unverifiable`.
- Do not open `/home/coder/captures/q24-orca-capture-20261116.md` (it holds other sessions' private prompt text).
- Use `uv run` for every Python command.

## Phase 1: Real running-worker fixture

## Task 1: Add the sanitized running-worker fixture and record it in the fixtures source note

Create `tests/sweep/fixtures/captured-worker-show-running.json` as the full `worker-show` envelope (top-level keys `id`, `ok`, `result`, `_meta`, the same shape as `tests/sweep/fixtures/captured-worker-show-1.json`) copied from the JSON block under "worker-show output" in `/home/coder/captures/q24-orca-capture2-20261116.md`. Apply the sanitize rules already written in `tests/sweep/fixtures/SOURCES.md`: replace the home prefix `/home/coder` with `/home/user` and the account name `coder` with `user` (rules 1 and 2); replace every UUID (envelope id, runtime epoch, runtime id, pane key parts, incarnation id, terminal handle UUID part, worktree id) with a stable fake UUID `00000000-0000-4000-8000-<12 digits>` numbered after the highest number already used in the other fixtures (rule 3; find it with a Grep over `tests/sweep/fixtures`); keep the `ctx_`, `run_`, `task_` and `wtr_` ids as captured (rule 4); replace the two `[text omitted]` values (`terminal.title`, `terminal.preview`) with `<text removed>` (rule 5). Keep every field name and value type, in particular `dispatch.status` `dispatched`, `projection.outcome` `in_progress`, `projection.liveness.verdict` `live`, `terminal.agentWait` null and `observation.agentWait` null. Add one row for the new file to the Files table in `tests/sweep/fixtures/SOURCES.md` (source: the 2026-11-16 second Q24 read-only capture, command `orca-ide orchestration worker-show --dispatch ctx_6c922cf310da --json`, exit 0, rules beyond 1 to 3: text of title and preview removed, a running worker with no non-null `agentWait` seen) and update the file count sentence in the Notes section of that file. Grep `tests/` and `docs/` for a pinned fixture count or folder listing (for example "19 files" or a glob of `captured-*.json`) and update any such pin.

Acceptance criteria:
- `tests/sweep/fixtures/captured-worker-show-running.json` parses as JSON and `jq` shows `.result.dispatch.status` `"dispatched"`, `.result.projection.outcome` `"in_progress"`, `.result.projection.liveness.verdict` `"live"`, `.result.terminal.agentWait` and `.result.observation.agentWait` both `null` (key present).
- The file contains no `coder` account name, no `/home/coder`, no real UUID from the capture, and no prompt or message text: a Grep for `coder`, `/home/coder` and for each original UUID of the capture returns nothing in the new file.
- `tests/sweep/fixtures/SOURCES.md` lists the new file and its sentence about the number of files is correct; `uv run pytest tests/sweep -q` still has the same pass count as before this task (no test depends on the new file yet).

## Phase 2: Read agentWait from worker-show

## Task 2: Make parse_worker_show read agentWait presence and value, and replace the test that pinned it off

Depends on: Task 1

In `src/superclaude/cli/sweep/probes.py`, change `parse_worker_show` (the only production caller is `_run_rows`, same file; the other callers are tests in `tests/sweep/test_probes_allowlist.py`) so it sets `agent_wait` and `agent_wait_present` on the returned `OrcaObservation`. Read the key from `result.observation.agentWait` first (`_get(show, "observation")`), and fall back to `result.terminal.agentWait` (`_get(show, "terminal")`) only when the `observation` object has no `agentWait` key. `agent_wait_present` is True when the key exists in that object, even when its value is null (the existing `_get` returns None for both a missing key and a null value, so write a small helper that tests key membership in the dict). `agent_wait` is the value found (None for null). When there is no show, or neither object has the key, `agent_wait_present` stays False and `agent_wait` None. `agent_wait_since` stays unset (no captured field names a wait time); keep a short comment saying so and that the meaning of a non-null `agentWait` is UNVERIFIED. Replace the stale comment above the `return OrcaObservation(` call. In `src/superclaude/cli/sweep/models.py`, rewrite the three "Reserved: no code sets these ... DESIGN open item 6" comments on `agent_wait`, `agent_wait_present` and `agent_wait_since` (class `OrcaObservation`) to say that `agent_wait` and `agent_wait_present` are set by `parse_worker_show` from `observation.agentWait` then `terminal.agentWait`, and `agent_wait_since` is still set by nothing. In `tests/sweep/test_probes_allowlist.py`, replace `test_parse_worker_show_reads_no_agent_wait_field_until_its_names_are_captured` (near line 1639) with tests that use `_captured("captured-worker-show-running.json")["result"]`: present and null gives `agent_wait_present` True and `agent_wait` None; also `liveness_verdict` `live`, `status` `dispatched`, `outcome` `in_progress`; an observation-only key, a terminal-only key (fallback), a non-null value in `observation` (`agent_wait` equals that value and `agent_wait_present` True; build it inline and call the meaning UNVERIFIED in a comment), a show with neither key, and a non-dict `observation` all behave as described and raise nothing. Update the assertion `obs.agent_wait_present is False` in `test_a_list_row_with_no_show_keeps_the_show_only_fields_unknown` only if it no longer holds (it should still hold). Dependents that must keep working: `_run_rows` in `src/superclaude/cli/sweep/probes.py` (builds rows through `dataclasses.replace` on the result), `test_list_and_show_disagree_and_the_show_value_is_used`, `test_a_show_of_the_wrong_shape_raises_nothing`, `test_one_missing_and_one_extra_worker_show_key_raise_nothing` and the three `test_worker_show_dispatch_times_*` tests, all in `tests/sweep/test_probes_allowlist.py`.

Acceptance criteria:
- `parse_worker_show` on the running-worker fixture result returns `agent_wait_present` True, `agent_wait` None, `liveness_verdict` `live`, `status` `dispatched`, `outcome` `in_progress`; on `captured-worker-show-1.json` (a finished worker without an `agentWait` key) it returns `agent_wait_present` False.
- The fallback, non-null, missing and wrong-shape cases listed above each have a test that passes, and no call to `parse_worker_show` raises on any shape.
- `ALLOWED_ORCA` in `src/superclaude/cli/sweep/probes.py` is unchanged (`git diff` shows no change to that tuple) and `uv run pytest tests/sweep/test_probes_allowlist.py -q` passes.

## Phase 3: Rule 5 and its tests

## Task 3: Rewrite rule 5 (_rule_working) with the real names and update the classify tests

Depends on: Task 2

In `src/superclaude/cli/sweep/classify.py`, replace the body and comment of `_rule_working` (registered as `Rule("working", _rule_working)` in `RULES`, the only reference besides the module itself) so it returns a `working` classification with rule name `working` only when all four hold on `row.orca`: `liveness_verdict == "live"`, `outcome == "in_progress"` (the `projection.outcome` field; not `status`, which holds `dispatch.status` and is `dispatched` for a running worker), `agent_wait_present is True`, `agent_wait is None`. Use the same `_classification(...)` helper the neighbouring rules use; its evidence text states the four observed values in the style of the other rules (for example "liveness_verdict live, outcome in_progress, agentWait present and null"). A row with a non-null `agent_wait` never reaches here as working because `_rule_waiting_signal` (rule 4) runs first and returns waiting on a person; keep that order. The comment must state that a non-null `agentWait` was never captured and its meaning is UNVERIFIED. Do not change `orca.status == "ready"` in `_rule_waiting_signal`. Class name constant: `C_WORKING` if it exists in `classify.py` or `models.py`; otherwise use the string `working` the way the other rules use their constants (Read the file first). In `tests/sweep/test_classify.py`: in `_rule_cases` (near line 278) change `live_unwaiting` to `outcome="in_progress"` with `status="dispatched"` and make the `working` case expect class `working`, rule `working`, no waiting kind; in `test_rule_case_per_rule_1_to_9` delete the `matched = "fallback" if rule == "working"` special case; in `test_every_class_name_but_working_is_reached` (near line 376) expect every name in `CLASSES` and rename the test; replace `test_rule_5_never_matches_while_the_agent_wait_names_are_uncaptured` (near line 436) with tests that the four-condition row is `working` and that breaking each condition one at a time is not `working` (liveness `unverifiable` and `exited`, outcome `succeeded` and `None`, `agent_wait_present` False, a non-null `agent_wait` gives rule `waiting_signal`); add a test that `status="in_progress"` with `outcome=None` is not `working` (this pins the correction of the old field name). Check every other test in the file that builds `liveness_verdict="live"` with `status="in_progress"` or `outcome="in_progress"` (near lines 524, 537, 642, 660, 1065) and fix those whose expected class changes because rule 5 now matches. Dependents of `classify` to keep working: `src/superclaude/cli/sweep/report.py` (reads the class and `agent_wait` through `_age`), `tests/sweep/test_report.py` (builds classified rows directly, so it is expected to need no change) and `tests/sweep/test_cli_contract.py`.

Acceptance criteria:
- `classify` returns class `working`, rule `working` for an observation with `liveness_verdict="live"`, `outcome="in_progress"`, `agent_wait_present=True`, `agent_wait=None`, and returns something else for each single broken condition; a non-null `agent_wait` with the other three true gives rule `waiting_signal`.
- `git diff` shows `if orca is not None and orca.status == "ready":` in `src/superclaude/cli/sweep/classify.py` unchanged.
- `uv run pytest tests/sweep/test_classify.py tests/sweep/test_report.py -q` passes, and no test in `tests/sweep/test_classify.py` still says rule 5 is inert, open item 6 or "no row is working in Phase 1".

## Task 4: Add an end-to-end sweep test that a captured running worker is reported as working

Depends on: Task 1, Task 2, Task 3

In `tests/sweep/test_cli_contract.py`, add a test next to `test_waiting_lists_hold_row_ids_only` (near line 1085) that uses the same `env` fixture and `_canned(env, RUN, workers=[...], shows={dispatch: <running fixture result>}, ...)` helper and `_ps(env)` the neighbouring tests use (Read them first for exact signatures) to run the sweep over one worker whose `worker-show` is `_captured("captured-worker-show-running.json")["result"]` (its `dispatch.id` is `ctx_6c922cf310da`; set the worker-list row's `dispatchId` and `dispatchStatus` `dispatched` to match). Assert from the JSON output that the row's class is `working` and the Working section of the Markdown report lists it, and add the same run with a finished worker fixture (`captured-worker-show-1.json`) to show it is not `working`. Update the comment near line 1095 ("the live agentWait field is not read in Phase 1 (open item 6)") because it is no longer true. If the running fixture's `terminal.worktreePath` or other joined fields make the row land under `could not determine` for an unrelated reason (for example the join to a transcript), assert only what the sweep reports for the Orca row and say why in a comment; do not weaken any existing assertion. The worker-show command stays the one already in the allow list: assert the recorded argv list contains no template outside `ALLOWED_ORCA`.

Acceptance criteria:
- The new test passes and fails if `_rule_working` is changed back to `return None` (confirm once by temporarily reverting locally, then restore; do not commit the revert).
- `uv run pytest tests/sweep/test_cli_contract.py tests/sweep/test_readonly.py tests/sweep/test_probes_allowlist.py -q` passes.
- No existing assertion in the three files is removed or loosened except the stale comment.

## Phase 4: Design doc and final checks

## Task 5: Update the design doc and run the full checks

Depends on: Task 3

In `docs/designs/orchestrator-mode.md`, update every statement that says rule 5 is inert or the names are uncaptured, found with `git grep -n -i "open item 6\|Rule 5\|agentWait\|inert\|not yet captured" docs/designs/orchestrator-mode.md`, in particular: the section 7.2 "Rule 5 (SP-24), one condition per line" bullet (near line 493) restated as `liveness_verdict == "live"`, `outcome == "in_progress"` (the `projection.outcome` field; `dispatch.status` is `dispatched` for a running worker), `agent_wait_present is True`, `agent_wait is None`, with the field sources now captured (`worker-show` `projection.liveness.verdict`, `projection.outcome`, and `agentWait` from `observation` then `terminal`) and a sentence that the meaning of a non-null `agentWait` is UNVERIFIED and that such a row is rule 4; the D7 row (near line 841) and the SP-24 mapping row (near line 877) so they say the restore happened with the real names (record the date 2026-11-16 and the capture file name `q24-orca-capture2-20261116.md`); the step 1.0a item 4 row (near line 914) with the observed names and values; open item 6 (near line 1003) marked resolved for `agentWait` presence, `liveness.verdict` and the outcome value, and still open (UNVERIFIED) for the non-null `agentWait` shape; the `tests/sweep/test_classify.py` row of the test table (near line 767) so it no longer says the `working` case expects `fallback` or that the four-condition case returns when Rule 5 is restored; and a short note that `status == "ready"` in rule 4 is the sweep's own marker for `task-list --ready` rows, not a `dispatch.status` value. Do not change the wording of the SP24 report footnote text quoted in the doc. Then run the whole verification and record the real counts.

Acceptance criteria:
- A Grep of `docs/designs/orchestrator-mode.md` for "Rule 5 is inert", "inert" next to Rule 5, and "show `status` \"in_progress\"" style leftovers (`status == "in_progress"`) finds none, and every remaining mention of open item 6 says what is still UNVERIFIED.
- `uv run pytest tests/sweep -q` passes with no failures (record passed, failed and skipped counts) and `uv run ruff check src/superclaude/cli/sweep tests/sweep` reports no errors.
- `make verify-sync` passes, and `git diff --stat` shows no change under `.claude/`, none to `ALLOWED_ORCA` or `ALLOWED_GIT`, and none to the `SP24` text in `src/superclaude/cli/sweep/report.py`.
