---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-refactorTheScIss-20261118-054817
version: "1"
priority: Medium
created_date: "2026-11-18"
---

# Choose the default /sc:issue --claim level from the issue

Source: ./source.md
Goal: A `/sc:issue --claim` typed with no `--pipeline` picks its level from the issue: `full` for every bug and for a simple or medium feature of up to 16 hours, `worktree` for a complex feature, a feature over 16 hours, or an issue it cannot classify; an explicit `--pipeline` always wins, `--submit` still needs an explicit `--pipeline full`, and the issue watcher still passes `--pipeline none`.

## Constraints

- The rule is authored once, in `src/superclaude/skills/sc-issue-protocol/refs/claim.md` (Wave 5). `issue.md`, `SKILL.md`, the next-steps template, the docs and the routing guide state the outcome in one sentence, which may name the 16-hour line once per file, and do not restate the order of the rule's checks or its unreadable fallback as a second rule; the full rule lives only in `refs/claim.md`.
- The rule reads three lines of `<D>/issue-summary.md`, which Wave 4 already writes from `templates/issue-summary.md`: `Type`, `Complexity` and `Effort estimate`. A value that is missing or not one of the allowed words counts as unreadable and gives `worktree`.
- No new return-contract field. The claim return contract keeps its ten fields (a test pins them); `pipeline_level` carries the level actually used.
- An `already_launched` re-claim still reports the stored level from the `launch` entry of `worktree.json` or its mirror file; that path is not changed.
- `--submit` still stops with `E-SUBMIT-NEEDS-FULL` when `--pipeline full` is not written out, including when `--pipeline` is omitted. The rule text of that STOP and its quoted message "--submit needs --pipeline full" stay as they are.
- Do not edit `tests/issue_watch/`, `src/superclaude/cli/issue_watch/launch.py`, `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`, the launch-level guard text, or the ship-gate and OB-H paragraphs. The issue watcher keeps passing an explicit `--pipeline none` and never reaches the rule.
- Text added to installed skill, command and core files names no `src/superclaude/` path and no git or gh verb that `tests/skills/test_worker_contract.py` audits in new lines.
- Design and user-guide records keep their original text: this change only adds dated "Amended 2026-11-18" notes, and a note on a table row goes inside that row's last cell so the table stays a table.
- The new text is prose that a model follows, so the tests pin its wording and order, not an executable rule. Each task says which words are pinned.
- Never `git add` or `git add -f` any path under `.claude/`; `make sync-dev` writes those copies and they stay unstaged. `claim-handoff-planb` edits some of the same files, so rebase onto `origin/master` before any PR.

## Phase 1: The rule in the skill

## Task 1: Add the default-level step to Wave 5 of the claim reference

In `src/superclaude/skills/sc-issue-protocol/refs/claim.md`, Wave 5 (lines 75-83): insert one new step between the current step 2 (write `next-steps.md`) and the current step 3 (set the plan boundary), and renumber the later steps (the plan boundary becomes step 4, the launch prompt step 5, the do-not-run step 6). The new step resolves `<L>` and reads: when `--pipeline` was given, `<L>` is its value and no rule runs; when it was omitted, read `Type`, `Complexity` and `Effort estimate` from `<D>/issue-summary.md`; if any of the three cannot be read, `<L>` is `worktree` and no other check runs (this check comes first, so a bug whose hours cannot be read also gets `worktree`); otherwise `<L>` is `full` for a bug, `full` for a feature whose complexity is `simple` or `medium` and whose effort is 16 hours or less, and `worktree` for a feature whose complexity is `complex` or whose effort is over 16 hours. The step then prints one line, `Level: <L> (explicit)` for a given flag or `Level: <L> (default: <reason>)` with the reason one of `bug`, `simple or medium feature of 16 hours or less`, `complex feature`, `feature over 16 hours` or `could not read type, complexity or hours`; `--pipeline none` prints no level line. In the renumbered launch-prompt step (the old step 4, line 82) replace "where `<L>` is the `--pipeline` value, or `full` when the flag was omitted" with "where `<L>` is the level from the step above". In the final output (the `launched` item at line 144 and the `already_launched` item at line 145) add that the `Level:` line of Wave 5 is printed with the launch result for `launched` only; for `already_launched` the stored level (from the `launch` entry of `worktree.json` or its mirror file) is printed in its place; for a failed worktree or a failed launch no `Level:` line is printed, because the launch result names the failure. The new text must not contain the words "run the printed implement command": the test in Task 5 splits the `launched` item on "For `worktree`:" and "For `full`:". Keep every other word of the pinned Wave 5 text: the `<K>` rule, "Plan boundary: before step 1", "`--pipeline full` ignores the line", the `orca_worktree.py" prompt --template` command with `--out "<D>/launch-prompt.md"`, "not `none`" and "written before Wave 7"; keep Wave 8 unchanged, including "`<L>` is the same level as in Wave 5." (line 122). `refs/chains.md:27` names "claim Wave 5 step 1" (the recommend call); step 1 does not move.

Acceptance criteria:
- `src/superclaude/skills/sc-issue-protocol/refs/claim.md` Wave 5 holds the new step after the `next-steps.md` step and before the plan-boundary step, with the unreadable check first (giving `worktree`, also for a bug), then the three outcomes (bug, simple or medium feature of 16 hours or less, complex feature or over 16 hours), "explicit" winning, and the `Level:` line format; the final output states the `Level:` line for `launched` only, the stored level for `already_launched`, and no `Level:` line for a failed worktree or launch; the text "or `full` when the flag was omitted" no longer appears in that file.
- `uv run pytest tests/skills/test_issue_protocol.py -k "st7 or st9" -v` still passes (the worker-contract file is run by the next bullet): the pinned plan-boundary and launch-prompt words of Wave 5 and the Wave 8 words are unchanged. `test_default_level_is_full_and_only_worktree_waits_for_a_person` fails until Task 5 updates it, which is expected.
- `tests/skills/test_worker_contract.py` passes (the new lines add no audited git or gh verb), and `grep -n "src/superclaude" src/superclaude/skills/sc-issue-protocol/refs/claim.md` prints nothing.
- `launch.py`, `tests/issue_watch/` and `orca_worktree.py` are untouched; Wave 8 and its launch command line are byte for byte as before.

## Task 2: Point the skill summary, the contract paragraph and the template at the rule

Depends on: Task 1

In `src/superclaude/skills/sc-issue-protocol/SKILL.md`: at line 17 replace "`full` (default) also implements without a commit or a push" so the sentence says `worktree` plans and waits for approval and `full` also implements without a commit or a push, and add that with no `--pipeline` the claim picks the level from the issue as `refs/claim.md` Wave 5 says; at line 89 (the Wave 5 summary) add that the wave sets `<L>` from `--pipeline` or the default rule; at line 138 replace "`pipeline_level` holds the level requested in this run, `full` when `--pipeline` was omitted" with the level used in this run, that is the `--pipeline` value or, when it was omitted, the level the default rule picked; keep the `already_launched` sentence. In `src/superclaude/skills/sc-issue-protocol/templates/next-steps.md` line 7, replace "to the last step at the default level `full`" with "to the last step at level `full`", and keep "(up to the plan boundary at level `worktree`," and the "or you do after `--pipeline none`" ending. Line 92 (the Wave 8 summary) already ends with "`<L>` is the same level as in Wave 5." and stays unchanged on purpose, although the source names it. Do not add a return-contract field and do not touch the yaml block at lines 123-134.

Acceptance criteria:
- `src/superclaude/skills/sc-issue-protocol/SKILL.md` lines 17 and 138 describe the picked level and no longer call `full` the single default; the yaml block of ten fields is unchanged and `pipeline_level` is still its first line.
- `src/superclaude/skills/sc-issue-protocol/templates/next-steps.md` line 7 no longer contains "default level `full`" and still names the plan boundary at level `worktree`.
- `uv run pytest tests/skills/test_issue_protocol.py -k "skill or st10 or contract" -v` passes; `test_default_level_is_full_and_only_worktree_waits_for_a_person` still fails until Task 5, which is expected.

## Phase 2: The command file

## Task 3: Describe the picked default in the command file

Depends on: Task 1

In `src/superclaude/commands/issue.md`: at line 16 replace "`full` (the default)" so the levels list says `worktree` stops at a plan a human approves, `full` also implements without a commit or a push, and that without `--pipeline` the claim picks one of them from the issue; in the Options table row of `--pipeline` (line 43) replace the default cell `full` with "`full` or `worktree`, picked from the issue" and replace "Omitted means `full`." in the meaning cell with a pointer sentence: omitted means the level is picked from the issue (a bug or a simple or medium feature of 16 hours or less gets `full`; a complex feature, a feature over 16 hours or an issue that cannot be classified gets `worktree`; the rule is in the skill, `refs/claim.md`). Rewrite the paragraph under the table (line 48) to say that a person who types `--claim` with no `--pipeline` gets the picked level, that an explicit `--pipeline` always wins, that the issue watcher never relies on the default and always passes `--pipeline none`, and that `--submit` still needs an explicit `--pipeline full`. In line 44 (`--submit` row) drop the clause ", even though `full` is the default" and keep "an explicit `--pipeline full` is still required" (the paragraph rewritten at line 48 must not use that clause either). Keep the STOP rules at lines 52-59 with the quoted message "--submit needs --pipeline full" and the words "no `--pipeline`", and the examples at lines 64-69 as they are.

Acceptance criteria:
- `src/superclaude/commands/issue.md` states the picked default in the intro, the `--pipeline` row and the paragraph under the table, names the 16-hour line only once (in the row), and points to the skill for the rule.
- The paragraph still contains "always passes `--pipeline none`", the examples still contain the exact line `/sc:issue --claim 302 --pipeline worktree`, and the STOP rule line for `E-SUBMIT-NEEDS-FULL` is unchanged.
- `uv run pytest tests/commands/test_issue_command.py -v` fails only in `test_option_defaults` (its pinned default cell is updated in Task 4), and `grep -n "src/superclaude/" src/superclaude/commands/issue.md` prints nothing, and `grep -n "even though .full. is the default" src/superclaude/commands/issue.md` prints nothing.

## Phase 3: Tests

## Task 4: Pin the picked default in the command tests

Depends on: Task 3

In `tests/commands/test_issue_command.py`: in `test_option_defaults` (line 113) change the `--pipeline` default assertion from `` "`full`" `` to the new cell text of Task 3 (the `--pipeline` row default cell, "`full` or `worktree`, picked from the issue"); extend `test_default_level_is_for_a_person_and_the_watcher_stays_explicit` (line 182) with assertions that the command text says an explicit `--pipeline` wins and that it points to `refs/claim.md` for the rule, and that the text "even though `full` is the default" is gone from the command file; keep `test_submit_rule_stops_a_bare_submit_and_keeps_its_message` (line 188) unchanged. Do not edit `tests/issue_watch/`.

Acceptance criteria:
- `uv run pytest tests/commands/test_issue_command.py tests/issue_watch/test_launch.py tests/issue_watch/test_security_invariants.py -v` passes with `tests/issue_watch/` unchanged (`git status --short tests/issue_watch` prints nothing).
- Changing the default cell in `src/superclaude/commands/issue.md` back to `` `full` `` makes `test_option_defaults` fail, removing "always passes `--pipeline none`" makes the watcher test fail, and putting ", even though `full` is the default" back into `issue.md` makes the same test fail.

## Task 5: Pin the rule in the protocol tests

Depends on: Task 1, Task 2

In `tests/skills/test_issue_protocol.py`: in `test_default_level_is_full_and_only_worktree_waits_for_a_person` (line 681) replace the assertion on "or `full` when the flag was omitted" with assertions that `_wave(claim, 5)` contains the new step's words (the `Level:` line formats `(explicit)` and `(default: `, the unreadable case, and the 16-hour line), and change the check on `SKILL.md` to the new line 17 wording; keep its checks on Wave 8 ("`<L>` is the same level as in Wave 5."), the next-steps template (now "at level `full`"), and "run the printed implement command" appearing only in the `worktree` sentence of the `launched` item. Add one new test, `test_default_level_rule_is_bug_full_complex_feature_worktree`, that reads Wave 5 and asserts: the new step sits after the `next-steps.md` step and before the plan-boundary step (compare `index` of the three step phrases); it names `Type`, `Complexity` and `Effort estimate` of `issue-summary.md`; bug gives `full`; a simple or medium feature of 16 hours or less gives `full`; a complex feature or over 16 hours gives `worktree`; unreadable gives `worktree`; an explicit `--pipeline` wins. The same test also asserts that the unreadable sentence comes before the bug sentence (compare their `index` in Wave 5), and that the final-output `launched` item states the `Level:` line, the stored level for `already_launched` and no `Level:` line for a failed worktree or launch (pin one phrase for each of the three).

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_model_alias_policy.py tests/skills/test_worker_contract.py -v` passes.
- Removing the unreadable-gives-`worktree` sentence from Wave 5 of `refs/claim.md` makes the new test fail, moving the new step after the plan-boundary step makes it fail, swapping the unreadable sentence below the bug sentence makes it fail, and deleting the `Level:` instruction from the final-output `launched` item makes it fail.
- `tests/skills/test_issue_protocol.py` still pins the ten return-contract fields and `pipeline_level` is not renamed.

## Phase 4: User-facing documentation and routing guide

## Task 6: Update the user guide and the architecture reference

Depends on: Task 1

In `docs/user-guide/commands.md`: line 368 (the `--pipeline` row) set the default cell to "`full` or `worktree`, picked from the issue" and replace "omitted means `full`" with the one-sentence outcome (a bug or a simple or medium feature of 16 hours or less gets `full`; a complex feature, a feature over 16 hours or an unclassifiable issue gets `worktree`); line 371 keep the `E-SUBMIT-NEEDS-FULL` sentence and the watcher sentence but change "(write `--pipeline full --submit`, even though `full` is the default)" to "(write `--pipeline full --submit`)", and say an explicit `--pipeline` always wins; in the levels table move "(default)" off the `full` row (line 378) and say in the table's lead-in line that the default is picked from the issue; leave the example at line 388 and the guard and ship-gate paragraph (line 382) unchanged. In `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md`: line 1557 change the `--pipeline` default from `full` to "`full` or `worktree`, picked from the issue by `refs/claim.md` Wave 5 (an explicit value wins)" and keep the Impact cell, which already names the no `--pipeline` case; line 1635 is unchanged.

Acceptance criteria:
- `grep -n "(default)" docs/user-guide/commands.md` prints no line from the `/sc:issue` levels table, and the options row and the lead-in say the default is picked from the issue; `grep -n "even though .full. is the default" docs/user-guide/commands.md` prints nothing.
- The syntax block, the ClickUp table and the guard paragraph of `docs/user-guide/commands.md` are unchanged; line 1557 of the architecture reference shows the picked default and line 1635 is unchanged.

## Task 7: Add dated amendment notes to the two design records

Depends on: Task 1

In `docs/designs/sc-issue-claim-pipeline-flag.md` add a note "Amended 2026-11-18 (second)" saying the default is now picked from the issue (bug: `full`; simple or medium feature of 16 hours or less: `full`; complex feature, feature over 16 hours or unreadable: `worktree`; an explicit `--pipeline` wins; the issue watcher always passes `--pipeline none`), inside the last cell of the table rows at lines 21, 43, 45 (decision P4, "The default stop is an approved plan", which already carries an "Amended 2026-11-08" note), 66, 78 and 274 (each of the others already carries an "Amended 2026-11-18" note: append the new note after it, never edit the existing text), and at the prose sentence at line 87; leave line 85 as it is. In `docs/designs/sc-issue-command.md` add the same note inside the last cell of the B17 row (line 44) after its existing note, and as a new blockquote paragraph after the existing "Amended 2026-11-18" block at line 66. Keep every original word.

Acceptance criteria:
- Both files carry the new note at the places above (including the decision P4 row at line 45 of the flag record); `git diff docs/designs` shows only added text (no removed word of an existing decision or note except appending inside the same cell).
- No line without a leading `|` sits between two rows of any table in either file, and line 85 of `docs/designs/sc-issue-claim-pipeline-flag.md` is byte for byte unchanged.

## Task 8: Update the routing guide sentence and its mirror

Depends on: Task 1

In `src/superclaude/core/HOW-WE-WORK.md` line 328 replace "`full` by default when a person types the command: implement, with no commit or push; `worktree`: plan, then wait for approval;" with a sentence that says: with no `--pipeline` the level is picked from the issue (`full` for a bug or a simple or medium feature of 16 hours or less; `worktree` for a complex feature, one over 16 hours or one it cannot classify), `full` implements with no commit or push, `worktree` plans then waits for approval, and keep "`--submit` with `full`: also commit, push and open a PR; `none`: no worktree and no agent, you run the steps yourself) and never merges". Then copy the file byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. The level table is not touched, so `src/superclaude/core/CLAUDE.md` needs no change. If `claim-handoff-planb` has already changed `HOW-WE-WORK.md` on `origin/master`, rebase first and redo the edit and the copy on the rebased file.

Acceptance criteria:
- `diff src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing and line 328 states the picked default.
- `uv run pytest tests/commands/test_routing_plugin_parity.py tests/core/test_how_we_work_routing_table.py tests/core/test_claude_md_routing_block.py -v` passes.

## Phase 5: Dev copies and staging

## Task 9: Sync the dev copies and stage the changes

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8

Run `make sync-dev` so the gitignored `.claude/` copies of the edited command and skill files match `src/superclaude/`. Stage the `src/`, `tests/`, `docs/` and `plugins/` paths this plan changed and always `git add .dev/tasks`; never `git add` anything under `.claude/`.

Acceptance criteria:
- `make verify-sync` exits 0, and its result is saved under `./artifacts/t9-evidence.log`.
- `uv run pytest tests/commands/test_issue_command.py tests/skills/test_issue_protocol.py tests/skills/test_model_alias_policy.py tests/skills/test_worker_contract.py tests/issue_watch -v` passes, with its result in `./artifacts/t9-evidence.log`.
- `git status --short` lists no path under `.claude/` as staged and shows `.dev/tasks` staged.
