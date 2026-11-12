# QA Report - Coordinator-usefulness lens (final gate, T322)

**Date:** 2026-11-12
**Reviewer:** qa-coordinator-usefulness (rf-qa-qualitative, fix_authorization: false)
**Lens:** Does the sweep report answer "who needs me" and "what is safe to close" without opening each session, and does every unknown say what could not be determined and why?

## Method and evidence base

Read from disk now: `src/superclaude/cli/sweep/report.py` (lines 1-673), `models.py` (1-256), `classify.py` (120-500), `src/superclaude/commands/sweep.md`, `src/superclaude/skills/sc-sweep-protocol/SKILL.md`, WC-16 in `src/superclaude/core/WORKER-CONTRACT.md:277`, DESIGN 7.5 (`docs/designs/orchestrator-mode.md:601-647`), SPEC lines 270-274 and 342-392 (`.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md`), the live check record (`artifacts/sweep-live-check-1.4.md`, `-1.4.json`, `-rerun-9.14.md`) and the live report it names (`.dev/sweeps/20261112-031239-sweep.md`, 605 lines, 154 KB). Rendered the test fixture `full_result` to `/tmp/cu_full_render.md` (outside the repo) to see the layout when Waiting rows exist, because the live data has none. No live Orca, ccsession or Claude command was run. `uv run pytest tests/sweep tests/commands/test_sweep_command.py`: 694 passed.

What the live report actually says (from the JSON and the report): 180 of 180 rows are `could not determine`, rule `fallback`; Waiting (a), Waiting (b) and Ready Tasks are empty; Historical is empty; Safe to close is `could not determine / could not determine` on 175 rows and `no / no` on the 5 Orca rows; Next inspection is the same sentence on every row.

## Where a person still has to open a session (answer to the lens question)

| # | Place | Why the report does not settle it | Finding |
|---|---|---|---|
| 1 | Any row whose Safe to close is `could not determine` (175 of 180 live rows) | Phase 1 can never print `yes` for terminal or worktree (SPEC FR-012, `classify.py:483-496`), and the Markdown never says so or says why for that row | F1 |
| 2 | The 5 completed Orca workers (`outcome succeeded`, `exited`, terminal `released`) | Class is `could not determine`; the missing input (no contract read) is not named; Next inspection points at nothing | F2, F3 |
| 3 | Every `could not determine` row | Next inspection says to read sources "that were not scanned"; the live report has zero unscanned sources | F2 |
| 4 | A frozen-plan or ready-Task row under Waiting (b) | Next inspection tells the person to read an agent-wait entry and a worker transcript that these rows do not have | F2 |
| 5 | Every Waiting (a) row | Requested by and Decision owner are always `unknown`, with no stated reason | F4 |
| 6 | Any transcript row | The row id is `transcript:<uuid>` only; no project folder, worktree or transcript path | F5 |
| 7 | Reading the Shift Brief for "who needs me" | One merged count of waiting plus unknown; the report file has no per-class tally | F6 |

## Findings

### F1 - MAJOR - Safe to close prints the value but not the reason in the Markdown report

- Evidence: `report.py:417` renders `f"{r.safe.terminal} / {r.safe.worktree}"` and nothing else. `SafeToClose.reason` (`models.py:203`, built at `classify.py:492-496` as `terminal: <why>; worktree: <why>`) is used only in `to_json` (`report.py:633-635`). Live report lines 302 and 480: `no / no` and `could not determine / could not determine`, with the Notes column carrying join notes, not the safe-to-close reason. SPEC `merged-requirements.md:274` says Phase 1 "prints `could not determine (result read not observable)` plus the Orca values". No test pins the cell beyond the header (`tests/sweep/test_report.py:106`, `:205`; no assertion on a reason).
- What is wrong: the person who reads the report (the file in `.dev/sweeps/`, or the text the skill just Read) sees `could not determine` for what is safe to close and cannot tell what could not be determined (result read? terminal not observed? worktree not observed?) or why. For the 5 released workers it prints terminal `no`, which a reader takes as "keep it", while the JSON reason says `terminal_state=released, next_action=none` (already released); the Markdown hides that. This is the one question the issue asks ("what is safe to close") and its unknowns carry no reason.
- Smallest fix: add the reason to the Sessions row (a short text in the Safe to close cell or the Notes cell, from `r.safe.reason`, still through `cell()`), and add one assertion in `test_report.py` that the cell or notes text contains the reason. State once under the Sessions heading that Phase 1 never prints `yes`.

### F2 - MAJOR - Next inspection is wrong or a dead end for the rows that matter

- Evidence A (dead end): `report.py:53` maps `fallback` to "read the sources in Source coverage that were not scanned". Live report lines 302-481 print exactly that on all 180 rows, while the live JSON has no source with `unscanned` set and `artifacts/sweep-live-check-1.4.md:37` records "0 `unscanned` sources". The instruction sends the person to an empty list.
- Evidence B (wrong target): `classify.py:236-246` gives three different outcomes the same rule name `waiting_signal` (agent wait; frozen plan from a contract STOP code; ready Task). `report.py:48` maps `waiting_signal` to "read the Orca agent-wait entry and the worker's last transcript lines" and `report.py:419` looks it up by rule only. In the rendered fixture (`/tmp/cu_full_render.md` lines 78-79) the frozen-plan row B1 and the ready-Task row B2 both get that sentence, although B1's evidence is a contract and B2 is a Task with no Dispatch, worker or transcript (`classify.py:733` comment).
- What is wrong: DESIGN 7.5 and SPEC line 388 require a non-empty read-or-check value; they do not excuse a value that names something the row does not have. The test (`test_report.py:1010-1019`) checks that each rule has an entry and that the text names only a read, not that it fits the row.
- Smallest fix: key the map by rule plus waiting kind (or by evidence kind) so frozen plan reads "read the contract named in the row" and ready Task reads "read the Task in Orca task-list"; for `fallback`, name the real missing input per row (see F3) or say "no unscanned source; open the session's last transcript lines".

### F3 - MAJOR - A `could not determine` row for a completed worker does not name what is missing

- Evidence: the 5 live Orca rows (JSON `orca:ctx_4e3237d227c3` and four more) have `liveness_verdict exited, outcome succeeded, status completed` yet class `could not determine`. `classify.py:273-286` returns `finished` only with a parsed contract; with no contract it returns None silently, and none of the notes in `classify.py:54-85` says "no contract found". The live record (`sweep-live-check-1.4.md:19`) gives the real reason ("no contract was read for these Tasks and `worker_done_seen` is not observable"), but the report does not. The notes printed are `Orca: exited; fenced evidence not readable` (a stalled-rule note) and `session start not observable: transcript tail only` (a join note), neither of which explains why the row is not `finished`.
- What is wrong: for the only rows that Orca itself marks completed, the report cannot tell the coordinator what to check. The person opens the session or the Run to settle it.
- Smallest fix: add one note when an Orca row is settled and no contract was attached (for example "no contract read for this Task; finished needs a parsed contract"), and pin it with a fixture test.

### F4 - MINOR (follow-up candidate, Medium) - Unknown cells in Waiting (a) and the Sessions dimensions carry no reason

- `report.py:239-242` hard-codes `Requested by` and `Decision owner` to `unknown` on every row and `Question` to `unknown` when there is no contract question; no row or section text says why. Under the table, `Answered: could not determine` (`report.py:260`) has its reason only in the distant last section ("Messages coverage is partial: pending questions cannot be read without consuming them", live line 531). By contrast the Ready Tasks heading does say "(creator not observable in Phase 1)". In the Sessions table, 9 of 10 dimension columns are `unknown` on all 180 live rows with no statement that Phase 1 does not observe them (`SP24_LINE` covers only stalled and fenced). DESIGN/SPEC prescribe the columns and the `unknown` value, so this is not a conformance defect; one sentence per table would close it.

### F5 - MINOR (Medium) - No row locator for transcript sessions

- `to_json` rows (`report.py:620-639`) and the Markdown rows carry only `transcript:<uuid>`; the project folder and transcript path (`SessionRow.transcript_path`, `models.py:135`) are not printed, and the Sessions row does not say which worktree its Safe to close worktree value refers to. A person acting on a `could not determine` transcript row must search `~/.claude/projects/*/<uuid>.jsonl` themselves. Waiting (a) rows are better off: `Affected` prints Run and worktree for Orca rows (`report.py:227-234`).

### F6 - MINOR (Medium) - The Shift Brief and report file give no per-class tally

- `report.py:480-495` prints one set-union count of waiting (a or b) plus could-not-determine (live: 180). The per-class counts exist only in the JSON and in the skill's chat reply (`SKILL.md` step 4). A person who opens only the report file cannot tell from the brief whether anyone is waiting or all rows are unknown; they must read the Waiting sections. The union is by design (an unknown can hide a person-wait), but the brief should show the three numbers.

### F7 - MINOR (Medium) - Size and repetition bury the unknowns

- Live report: 605 lines, 154 KB. The same 71-source list appears three times (header Sources line, Source coverage table, footer list), and the 180 `could not determine` rows appear twice (Could not determine table, then the 17-column Sessions table). SKILL step 3 has the coordinator Read the whole report in chunks of 150 lines on every run, and WC-16 (`WORKER-CONTRACT.md:277`) runs it on every wake at most every 5 minutes. That is roughly 150 KB read per sweep to confirm counts the JSON already gave. Note as a cost, not a wrong answer.

### F8 - MINOR - Waiting (b) column `Policy reason` prints the rule id

- `report.py:274` prints `r.classification.rule`; for every real (b) row that is `waiting_signal` (`classify.py:243`, `:246`), so the column named "Policy reason" says `waiting_signal` instead of "frozen plan" or "ready Task". The real reason is in the Evidence column (rendered fixture line 37).

## What works for the lens (verified)

- Empty sections say `No matching records. This is not an all-clear.` (live lines 87, 94, 98, 520), so an empty Waiting (a) is not read as "nobody waits".
- The header, Source coverage and the closing section state remote hosts not scanned, partial Messages coverage, lower-bound totals and discovery gaps (`report.py:164-192`, `:498-515`); the rerun fixed `total_is_lower_bound` so the JSON agrees (`sweep-live-check-1.4-rerun-9.14.md`).
- Worktrees table gives a reason for every `no` and for `could not determine` (live lines 487-516), so "what is removable" is readable per worktree.
- Waiting (a) rows give Age, the blocked question and Affected (Run, worktree) for the rows the sweep can see (rendered fixture lines 25-26).
- The 3 full-run failures argument in `phase14-full-pytest.md` holds: `git diff --stat` against the base on `src/superclaude/cli/eval`, `tests/cli/eval`, `tests/hooks`, `src/superclaude/hooks` is empty, and `ruff` is not importable in the venv (`find_spec('ruff')` is False).
## Checks

| Check | What was checked | Result |
|---|---|---|
| C1 | Report names who needs a person (Waiting (a), (b), Could not determine) and prints "not an all-clear" when empty | PASS |
| C2 | Safe to close shows a reason for each unknown in the Markdown report | FAIL (F1) |
| C3 | Next inspection fits the row for every rule and outcome | FAIL (F2) |
| C4 | A `could not determine` row for a completed worker says what is missing | FAIL (F3) |
| C5 | Unknown cells in Waiting (a) and the dimension columns carry a reason | FAIL, minor (F4) |
| C6 | Each row can be located without a search | FAIL, minor (F5) |
| C7 | Shift Brief and report file answer "anyone waiting?" without reading the sections | FAIL, minor (F6) |
| C8 | Report size and repetition are workable for a 5-minute coordinator pass | FAIL, minor (F7) |
| C9 | Waiting (b) column labels match their content | FAIL, minor (F8) |
| C10 | Coverage gaps (remote hosts, partial Messages, lower bounds, discovery) are stated | PASS |
| C11 | Skill and command text: counts-only reply, no advice, report Read to `Report complete`, safe/removable labelled as observations | PASS |
| C12 | Phase 14 failure attribution (3 failures) holds; sweep and command tests pass (694) | PASS |

## Summary

- Checks passed: 4 / 12; failed: 8 (3 blocking, 5 minor).
- The live report answers neither "who needs me" nor "what is safe to close" for any of its 180 rows, which the design expects for Phase 1 evidence. The defects above are in how the unknowns are explained: reasons that exist in the data (JSON) never reach the Markdown, two Next inspection sentences point at things the row does not have, and the dominant unknown (completed workers) does not name its missing input.
- Follow-up candidates (minor, Medium): F4, F5, F6, F7.
- Not checked: live Orca behaviour with a real blocked worker (no live run allowed; the Waiting (a) layout was read from the test fixture render, not from live data), and the output-style chat exception adherence (out of this lens).

Verdict: FAIL
Blocking count: 3
