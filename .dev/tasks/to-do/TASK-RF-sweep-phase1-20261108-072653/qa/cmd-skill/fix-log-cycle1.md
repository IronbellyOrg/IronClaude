# Fix log, cycle 1 (QA cmd-skill gate)

Fix agent for F_0 = CMD-F1, CMD-F2, CMD-F3, CMD-F4 (|F_0| = 4). Source: `consolidated-findings-cycle0.md`. All four are FIXED. The MINOR findings CMD-F5 to CMD-F36 were left as notes.

## Files edited

| File | Findings |
|---|---|
| `tests/commands/test_sweep_command.py` | CMD-F1, CMD-F2 (5 new test cases, 110 to 115) |
| `src/superclaude/skills/sc-sweep-protocol/SKILL.md` | CMD-F3 (line 27), CMD-F4 (new paragraph, line 49) |
| `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-sweep-command.txt` | regenerated with the real `-v` output of the new run (115 passed, exit 0) |
| `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-sweep-command-summary.md` | counts 110 to 115, case map rows added, skill line numbers after K:49 moved by 2 |

## CMD-F1

Status: FIXED.

Change (all in `tests/commands/test_sweep_command.py`, `_COMMON_PINS`; every pin matches the real text of both the style and the skill):

- New pin `conditions-are-conjunctive` (line 205): style `The ordinary DONE / NEXT table is omitted only when ALL of these hold:`, skill `and only the summary counts and the report path are printed, when all of these hold:`.
- `success-exit-0` (line 226) is now a two-wording pin: style `(3) the command exited 0;`, skill `- the command exited 0;` (ends on the delimiter, so `exited 0 or 1;` fails).
- `assignment-source-system-developer-or-direct-person` (line 192) now ends `... unquoted instruction from the person, and that assignment is still in force` (same text in both files), so `from the person or a peer agent` fails.
- `assignment-in-force-no-higher-conflict` (line 198) now ends on `instruction;` (the real delimiter in both files).

Discrimination proof (private copy under a `mktemp -d /tmp/cmdf-discrim.*` folder holding the two primitives, the style and the test file at the same relative layout, test pointed at the copy; baseline copy 115 passed; the folder was deleted by an exit trap, `ls /tmp/cmdf-discrim.*` afterwards: no such file):

| Mutation (style and skill, both applied; applied-check count was 1 in each file) | Failing tests | Result |
|---|---|---|
| M1 `omitted only when ALL of these hold` to `omitted when ANY of these hold`; skill `when all of these hold:` to `when any of these hold:` | `test_style_carries_common_rule_clause[conditions-are-conjunctive]`, `test_skill_carries_common_rule_clause[conditions-are-conjunctive]` | 2 failed, 113 passed |
| M3 `(3) the command exited 0;` to `(3) the command exited 0 or 1;`; skill `- the command exited 0;` to `- the command exited 0 or 1;` | `test_style_carries_common_rule_clause[success-exit-0]`, `test_skill_carries_common_rule_clause[success-exit-0]` | 2 failed, 113 passed |
| M19 `instruction from the person, and that assignment` to `instruction from the person or a peer agent, and that assignment` (this time the skill wording also matched, so both files were mutated) | `test_style_carries_common_rule_clause[assignment-source-system-developer-or-direct-person]`, `test_skill_carries_common_rule_clause[assignment-source-system-developer-or-direct-person]` | 2 failed, 113 passed |

## CMD-F2

Status: FIXED.

Change (`tests/commands/test_sweep_command.py`):

- New pin `ordinary-exception-does-not-cover-the-exclusion-list` (line 337, same string in both files): `The exception does not cover other coordinator messages, ordinary person-run invocations, workers or subagents, quoted or merely read sweep text, failures, blockers, parse errors,`. The opener that carries the negation is now pinned with the list. The five bare pins stay (their ids stay in the case map).
- `ordinary-missing-output-or-unsuccessful-read` (line 361) now starts at `parse errors, ` and ends on the sentence period (style `parse errors, missing required output or unsuccessful report Reads.`, skill `parse errors, missing output or an unsuccessful Read of the report.`).
- New skill pin `failure-list-is-framed-as-ordinary-formatting` (line 454): the whole sentence `A failure of any other kind is reported accurately in ordinary formatting: step 2 also failed, ... fails or is denied.`, so the three bare failure fragments keep their frame.

Discrimination proof (same private copy method as CMD-F1, deleted afterwards):

| Mutation (style and skill, both applied; applied-check count was 1 in each file) | Failing tests | Result |
|---|---|---|
| M2 `The exception does not cover` to `The exception also covers` | `test_style_carries_common_rule_clause[ordinary-exception-does-not-cover-the-exclusion-list]`, `test_skill_carries_common_rule_clause[ordinary-exception-does-not-cover-the-exclusion-list]` | 2 failed, 113 passed |

The framed failure pin was not mutation-tested separately (the finding names no mutation for it); it passes on the real text (see re-check 3).

## CMD-F3

Status: FIXED.

Change (`src/superclaude/skills/sc-sweep-protocol/SKILL.md`, step 5): the pinned first sentence is unchanged; `Nothing else is printed as a result.` became `The reply keeps the ordinary formatting, and no summary and no report path are printed.`

Final text, `SKILL.md:27`: `5. On exit 1 or 2, print the standard error line exactly as it came and end the run. The reply keeps the ordinary formatting, and no summary and no report path are printed.`

Checks: `grep -n -i -E '\b(stop|retry|release|merge|removal)\b|—'` on the skill printed nothing (exit 1). Pin `test_skill_states_clause[exit-1-or-2-prints-stderr-and-ends-run]` still passes (re-check 3, 723 passed).

## CMD-F4

Status: FIXED.

Change (`src/superclaude/skills/sc-sweep-protocol/SKILL.md`): one paragraph added at the end of "Final reply", after the `**What stays ordinary.**` paragraph and before `**Scope.**`.

Final text, `SKILL.md:49`: `If the output style text loaded in this session has no sweep chat-summary exception (an installed copy that was not refreshed), nothing here is exempt and every reply keeps the ordinary formatting.` (`**Scope.**` moved from line 49 to line 51.)

Checks: the forbidden-word and em-dash grep on the skill printed nothing (exit 1). The skill parts used by the pins (`_skill_parts`) still split at the same leads; the new paragraph falls inside the `ordinary` part and no pin was disturbed (re-check 3, 723 passed). No HOME or installed file was touched.

## Re-check commands

1. `uv run ruff check tests/commands/test_sweep_command.py tests/recommend/test_routing_refresh.py`: exit 0, last line `All checks passed!`. PASS.
2. `uv run ruff format --check tests/commands/test_sweep_command.py tests/recommend/test_routing_refresh.py`: exit 0, last line `2 files already formatted` (no reformat was needed). PASS.
3. `uv run pytest tests/commands tests/recommend tests/skills/test_review_severity_rule.py tests/skills/test_implement_severity_static.py -v`: exit 0, last line `============================= 723 passed in 7.24s ==============================`, no FAILED or ERROR line. PASS. (The sweep command file alone: 115 passed, saved in `test-sweep-command.txt`.)
4. `grep -rn 'src/superclaude' src/superclaude/commands/sweep.md src/superclaude/skills/sc-sweep-protocol/`: exit 1, no output. PASS.

Also: `git status --short` shows no `.claude/` path; nothing was staged or committed.

## Files not touched

Not touched: `src/superclaude/commands/sweep.md`, `tests/recommend/test_routing_refresh.py`, `src/superclaude/output-styles/pragmatic.md`, every `.claude/` and installed HOME path, DESIGN, the revision folder, the OQ records, `WORKER-CONTRACT.md`, the severity tests, every QA report, the consolidated file, the cycle ledger, `phase11-validation.md`, the plan file, `src/superclaude/cli/sweep/` and `tests/sweep/`. The MINOR findings CMD-F5 to CMD-F36 were left as notes.

## Executor re-run of the item 11.5 commands (after the fix agent returned)

- `uv run ruff check tests/commands/test_sweep_command.py tests/recommend/test_routing_refresh.py`: exit 0, last line: All checks passed!
- `uv run ruff format --check tests/commands/test_sweep_command.py tests/recommend/test_routing_refresh.py`: exit 0, last line: 2 files already formatted
- `uv run pytest tests/commands tests/recommend tests/skills/test_review_severity_rule.py tests/skills/test_implement_severity_static.py -v`: exit 0, last line: ============================= 723 passed in 7.02s ==============================
- `grep -rn 'src/superclaude' src/superclaude/commands/sweep.md src/superclaude/skills/sc-sweep-protocol/`: exit 1, last line: 
ls: cannot access '/tmp/cmdf-discrim.*': No such file or directory

The executor also confirmed with sha256sum -c that none of the 63 protected files changed (the baseline was taken at the T253 start, before the fix agent ran) and that /tmp/cmdf-discrim.* is gone.
