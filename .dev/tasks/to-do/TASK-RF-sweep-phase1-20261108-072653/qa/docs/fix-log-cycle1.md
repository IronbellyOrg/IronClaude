# Fix log, docs gate cycle 1

Findings fixed this cycle: DOC-F1 and DOC-F2 (F_0). MINOR findings DOC-F3 to DOC-F32 left alone.

## Files edited

- `src/superclaude/commands/sweep.md` (new paragraph at line 16, after the report-content paragraph at line 14)
- `src/superclaude/skills/sc-sweep-protocol/SKILL.md` (step 4 at line 26, the exempt-reply paragraph at line 43, a closing sentence of `## Boundaries` at line 66)
- `tests/commands/test_sweep_command.py` (6 new pins after `test_skill_states_clause`; no existing pin changed)
- `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-sweep-command.txt` (regenerated from the real `-v` run: 121 passed, exit 0)
- `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-sweep-command-summary.md` (counts 115 to 121, cycle-1 paragraph, new case map, `C:49`/`C:53` moved to `C:51`/`C:55`)

## DOC-F1: FIXED

- Change: one sentence added to `sweep.md` and to the `## Boundaries` section of `SKILL.md`, the same text in both: "The report also states, as facts to review, `Safe to close`, `Removable` and `Next inspection` (what to read next); these are observations, not advice, and the coordinator or person decides." The alternative (narrowing the WC-16 or routing wording) was not used and stays OPEN.
- After the change: `src/superclaude/commands/sweep.md:16`; `src/superclaude/skills/sc-sweep-protocol/SKILL.md:66`.
- Words: no stop, retry, release, merge or removal (whole word, case-insensitive; `Removable` is a different word); no em dash or en dash.
- Pins: `test_sweep_command_says_report_columns_are_observations_not_advice` (the sentence in the command text before `## Triggers`) and `test_sweep_skill_boundaries_say_report_columns_are_observations_not_advice` (the sentence inside the skill's `## Boundaries` section).
- Mutation proof (private copy under a `mktemp -d /tmp/ironclaude-batch.*` folder, the test file pointed at the copy by its own `parents[2]` path logic, copy deleted by an exit trap):
  - M1, sentence removed from the copy of `sweep.md`: `FAILED tests/commands/test_sweep_command.py::test_sweep_command_says_report_columns_are_observations_not_advice`, 1 failed, 120 passed.
  - M2, sentence removed from the copy of `SKILL.md`: `FAILED tests/commands/test_sweep_command.py::test_sweep_skill_boundaries_say_report_columns_are_observations_not_advice`, 1 failed, 120 passed.
  - Baseline copy without a mutation: 121 passed.

## DOC-F2: FIXED (command, step 4 and the exempt reply); the report's WC-16 alternative stays OPEN

- Change, command and step 4: "In Phase 1 the classes stalled (proved) and fenced are not observed, so a zero count there means nothing; the report says so." added to `sweep.md` (same new paragraph) and to step 4 of `SKILL.md`.
- Change, how the counts are printed: step 4 also says "Print each of those two counts with the mark `(not observed in Phase 1)` after the number, so the caveat travels with the counts." The number stays the genuine summary number (`stalled (proved): 0 (not observed in Phase 1)`).
- Change, exempt reply: one sentence at the end of the "Only the final successful reply" paragraph: "The counts in that reply are printed as step 4 prints them, so the `(not observed in Phase 1)` mark on stalled (proved) and fenced stays; the mark is part of the counts, not a gloss of a label and not advice." The caveat is defined as part of the counts line, so the list of facts the exempt reply prints (`only the summary counts and the report path are printed`) and every pinned common-rule phrase are unchanged; `pragmatic.md` was not edited.
- After the change: `sweep.md:16`; `SKILL.md:26` (step 4); `SKILL.md:43` (exempt reply).
- Residual note, not a defect found by the gate: `pragmatic.md:23` says the exempt reply "contains the summary counts and the report path" and does not mention the mark, so only the skill text states the mark; the style file stays as it was because this cycle may not edit it. The skill still says the mark is part of the counts and not a gloss, so the two texts agree on what is printed.
- Words: none of the five advice words; no em dash or en dash.
- Pins: `test_sweep_command_says_phase1_stalled_and_fenced_zero_means_nothing`, `test_sweep_skill_step4_says_phase1_stalled_and_fenced_zero_means_nothing`, `test_sweep_skill_step4_prints_the_phase1_mark_with_the_counts`, `test_sweep_exempt_reply_keeps_the_phase1_mark_on_the_counts` (the last one reads the exempt-reply part of `## Final reply`).
- Mutation proof (same private-copy method):
  - M3, sentence removed from the copy of `sweep.md`: `FAILED ...::test_sweep_command_says_phase1_stalled_and_fenced_zero_means_nothing`, 1 failed, 120 passed.
  - M4, sentence removed from step 4 of the copy of `SKILL.md`: `FAILED ...::test_sweep_skill_step4_says_phase1_stalled_and_fenced_zero_means_nothing`, 1 failed, 120 passed.
  - M5, the "Print each of those two counts with the mark" sentence removed from step 4: `FAILED ...::test_sweep_skill_step4_prints_the_phase1_mark_with_the_counts`, 1 failed, 120 passed.
  - M6, the exempt-reply sentence removed: `FAILED ...::test_sweep_exempt_reply_keeps_the_phase1_mark_on_the_counts`, 1 failed, 120 passed.
- OPEN (not edited, out of scope): the alternative of a WC-16 sentence telling the coordinator the two zeros carry no meaning (owner-approved text in `WORKER-CONTRACT.md`).

## Re-check commands

| # | Command | Exit | Last lines | Result |
|---|---|---|---|---|
| 1 | `uv run pytest tests/core tests/commands tests/recommend tests/skills -v` | 0 | `============================ 2647 passed in 54.83s =============================` | PASS |
| 2 | `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | 0 | no output | PASS |
| 3 | `uv run ruff check tests/core/test_how_we_work_routing_table.py tests/commands/test_sweep_command.py` | 0 | `All checks passed!` | PASS |
| 4 | `uv run ruff format --check tests/core/test_how_we_work_routing_table.py tests/commands/test_sweep_command.py` | 0 | `2 files already formatted` | PASS |
| 5 | `grep -rn 'src/superclaude' src/superclaude/commands/sweep.md src/superclaude/skills/sc-sweep-protocol/` | 1 | no output | PASS (expected exit 1) |
| 6 | `grep -n -i -w -E 'stop\|retry\|release\|merge\|removal' src/superclaude/skills/sc-sweep-protocol/SKILL.md` | 1 | no output | PASS (expected exit 1) |
| 7 | `grep -n -E '—\|–'` on both primitives (extra check) | 1 | no output | PASS |
| 8 | `uv run pytest tests/commands/test_sweep_command.py -v` (result file regenerated from it) | 0 | `============================= 121 passed in 1.20s ==============================` | PASS |

The test file needed no `ruff format` run: `uv run ruff format tests/commands/test_sweep_command.py` reported "1 file left unchanged".

## Files not touched

Not edited: `src/superclaude/output-styles/pragmatic.md`, `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/core/HOW-WE-WORK.md` and its plugin copy, `docs/`, `CHANGELOG.md`, the SPEC, the revision folder, the OQ records, the severity-test modules, `tests/skills/`, `tests/core/`, `tests/recommend/`, `tests/sweep/`, `src/superclaude/cli/sweep/`, any QA report, the consolidated findings file, the cycle ledger, the plan file, and any `.claude/` or installed HOME path. `make sync-dev` was not run. Nothing was staged or committed. No live Orca, ccsession or Claude command was run. The `/tmp` mutation copies were deleted by an exit trap (checked: the folder was gone afterwards); an unrelated older `/tmp/ironclaude-batch.ptdj0orr` folder (created 13:08, not by this run) was left alone.

## Executor re-run of the item 13.8 commands (after the fix agent returned)

- `uv run pytest tests/core tests/commands tests/recommend tests/skills -v`: exit 0, last line: ============================ 2647 passed in 54.25s =============================
- `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`: exit 0, last line: 
- `uv run ruff check tests/core/test_how_we_work_routing_table.py tests/commands/test_sweep_command.py`: exit 0, last line: All checks passed!
- `uv run ruff format --check tests/core/test_how_we_work_routing_table.py tests/commands/test_sweep_command.py`: exit 0, last line: 2 files already formatted
- `grep -rn 'src/superclaude' src/superclaude/commands/sweep.md src/superclaude/skills/sc-sweep-protocol/`: exit 1, last line: 
- `grep -n -i -w -E 'stop|retry|release|merge|removal' src/superclaude/skills/sc-sweep-protocol/SKILL.md`: exit 1, last line: 

The executor also confirmed with sha256sum -c that none of the 71 protected files changed (baseline taken at the T299 start, before the fix agent ran) and that only the five allowed files changed.
