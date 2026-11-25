---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-addTheGitHubBloc-20261125-201412
version: "1"
priority: Medium
created_date: "2026-11-25"
---

# Stop /sc:issue --claim while a GitHub blocked-by issue is open

Source: ./source.md
Goal: `/sc:issue --claim` reads the issue's GitHub "blocked by" links in Wave 2, before Wave 3 assigns anything. Any open blocker stops the claim with `E-BLOCKED` naming each one and writes nothing. No blockers, or only closed ones, leaves the claim running as today. A list that cannot be read lets the claim go ahead as today, and its final output says the check could not run. The protocol, the command description, the routing guide row and the plugin copy of the guide describe this, and regression tests pin it.

## Constraints

- Change only what the source asks: the blocker read and `E-BLOCKED` stop in the claim, their description in four places, and the tests. Not the issue watcher, not dependency links, and not any other claim behaviour.
- Edit only the canonical files under `src/superclaude/`, the plugin guide copy and the tests. Do not edit or stage anything under `.claude/`; the generated copies come from `make sync-dev`.
- Inside the skill files and the command file under `src/superclaude/skills/sc-issue-protocol/` and `src/superclaude/commands/issue.md`, never write the text `src/superclaude/` (two existing tests forbid it), never write `{owner}/{repo}`, and keep every `gh api` path spelled `repos/<R>/...`.
- Do not touch the paragraph that begins "Coordinator handoff for `--pipeline none`:"; it must stay identical in `refs/claim.md`, `SKILL.md` and `commands/issue.md`.
- Do not add fields to the claim return contract in `SKILL.md`; a test pins its exact keys. A failed read is reported as one line of the final output.
- `SKILL.md` must stay under 500 lines.

## Phase 1: Claim protocol reads the blockers

## Task 1: Add the blocker check to Wave 2 and its output line in refs/claim.md

Edit `src/superclaude/skills/sc-issue-protocol/refs/claim.md`, the section `## Wave 2: edge cases (orchestrator reads `<D>/scout.md`)`. Its items 1 to 4 are the pull request, closed and assignee checks and item 5 remembers earlier comment IDs. Insert a new item 5 after item 4 and renumber the old item 5 to 6. The new item is a read-only check: run `gh api --paginate repos/<R>/issues/<N>/dependencies/blocked_by --jq '.[] | select(.state == "open") | "#\(.number) \(.html_url)"'`. Any output line is an open blocker, and the claim STOPs `E-BLOCKED` with the message "Issue #N is blocked by open issue(s): <each #number and link>; not claimed." No output (no blockers, or only closed ones) means continue as today. A failed call (non-zero exit, for example no access or an endpoint that is not served) means continue as today and hold the line `Blocker check: could not run (<reason>); the claim went ahead without it.` for the final output. The item says it runs for a re-claim and for every `--pipeline` value. Change the sentence that opens the section from "every STOP here makes no GitHub or ClickUp write (B9)" to "every STOP here makes no GitHub, ClickUp or Orca write (B9)". In `## Final output`, extend item 4 (the warnings item) with the sentence: when the Wave 2 blocker check could not run, print the held `Blocker check: could not run (<reason>); the claim went ahead without it.` line, also for `--pipeline none`. Leave Waves 3 to 8 and the "Coordinator handoff" paragraph unchanged.

Acceptance criteria:
- `## Wave 2` in `src/superclaude/skills/sc-issue-protocol/refs/claim.md` contains `repos/<R>/issues/<N>/dependencies/blocked_by` and `E-BLOCKED`, and that item sits after the closed-issue item and the assignee item and before `## Wave 3`.
- `## Wave 3` still holds the only `--add-assignee` call and does not mention `dependencies/blocked_by`.
- The Wave 2 item states all three outcomes: an open blocker stops with `E-BLOCKED` naming each one, none or only closed continues as today, and an unreadable list continues and is reported in the final output.
- `## Final output` carries the `Blocker check: could not run` line rule.
- `grep -n "src/superclaude/" src/superclaude/skills/sc-issue-protocol/refs/claim.md` prints nothing and `grep -n "gh api" src/superclaude/skills/sc-issue-protocol/refs/claim.md` shows only `repos/<R>/...` or `user` paths.

## Task 2: Describe the blocker check and E-BLOCKED in SKILL.md

Depends on: Task 1

Edit `src/superclaude/skills/sc-issue-protocol/SKILL.md`. In `## Claim mode`, item 3 (`**Wave 2, edge cases**`), add after the existing text that a read-only blocker check follows: an open blocker is STOP `E-BLOCKED` naming each one with no write, none or only closed continues, and an unreadable list continues and the final output says the check could not run. In `## Error handling`, add two rows after the row `| Number or URL is a pull request | STOP `E-NOT-AN-ISSUE` |`: one for an open GitHub "blocked by" issue (STOP `E-BLOCKED` naming each open blocker by number and link, no writes) and one for a blocked-by list that cannot be read (continue as today; the final output says `Blocker check: could not run (<reason>)`). Leave the `## Return contract` block, the "Coordinator handoff" paragraph and the `## Will` and `## Will Not` lists unchanged.

Acceptance criteria:
- `SKILL.md` Claim mode item 3 and the `## Error handling` table both contain `E-BLOCKED`, and the table has a row for the unreadable list that includes `Blocker check: could not run`.
- `wc -l src/superclaude/skills/sc-issue-protocol/SKILL.md` prints fewer than 500 lines.
- `tests/skills/test_issue_protocol.py::test_st10_claim_return_contract_has_the_ten_fields_and_keeps_the_old_ones` and `::test_the_coordinator_handoff_is_the_same_paragraph_in_all_three_files` still pass.

## Phase 2: Command and routing guide describe it

## Task 3: Describe the blocker stop in the /sc:issue command file

Depends on: Task 1

Edit `src/superclaude/commands/issue.md`, the `--claim` bullet under "Two modes on the repository that `origin` points at" (the long bullet that begins "`--claim` takes an existing issue"). After the sentence that ends "Orca must be running (STOP `E-ORCA-REQUIRED` otherwise, before anything is assigned or posted)." add one sentence: the claim first reads the issue's GitHub "blocked by" links and stops with `E-BLOCKED`, naming each open blocker, while any is open (before anything is assigned or posted); a list that cannot be read does not stop the claim, and its final output says the check could not run. Add no new flag and change nothing else in the file, including the "Coordinator handoff" paragraph and the `## Boundaries` lists.

Acceptance criteria:
- `src/superclaude/commands/issue.md` contains `E-BLOCKED` in the `--claim` bullet and still contains no text `src/superclaude/`.
- The Options table and the STOP rules list of the file are unchanged, and `tests/commands/test_issue_command.py` and `tests/skills/test_issue_protocol.py::test_st11_no_source_tree_path_in_the_command_file` pass.

## Task 4: Update the /sc:issue row of the routing guide in HOW-WE-WORK.md

Edit `src/superclaude/core/HOW-WE-WORK.md`, the table row at line 296 that begins `| `/sc:issue` |`. In the claim description, change "it assigns the issue to you, checks its accuracy" so it reads that the claim first stops, naming each open blocker, while a GitHub "blocked by" issue is still open (a blocked-by list it cannot read does not stop the claim); otherwise it assigns the issue to you and checks its accuracy. Keep the rest of the row, including the `--pipeline` levels and the Create sentence, as it is. Do not touch any other line, the level table or the routing table.

Acceptance criteria:
- The `/sc:issue` row of `src/superclaude/core/HOW-WE-WORK.md` mentions the GitHub "blocked by" check and that an unreadable list does not stop the claim.
- `git diff --stat -- src/superclaude/core/HOW-WE-WORK.md` shows exactly one changed line.

## Task 5: Copy the guide byte for byte to its plugin copy

Depends on: Task 4

Copy `src/superclaude/core/HOW-WE-WORK.md` over `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` with `cp`, so the plugin copy is byte-identical. Change no other file in that plugin folder.

Acceptance criteria:
- `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing and exits 0.
- `uv run pytest tests/commands/test_routing_plugin_parity.py -q` passes.

## Phase 3: Regression tests

## Task 6: Pin the blocker check in tests/skills/test_issue_protocol.py

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5

Edit `tests/skills/test_issue_protocol.py` and add the checks at the end of the file, after `test_stage_claim_skips_recommend_and_plain_claim_keeps_it`, in the style of the existing `plan_section_problems` helper and its mutation tests. Reuse `_text`, `_wave`, `REFS`, `SKILL`, `COMMANDS` and `ROOT` from the top of the file. Add a helper `blocker_check_problems(claim: str) -> list[str]` that returns a list of what is wrong with the claim text: the Wave 2 section lacks `repos/<R>/issues/<N>/dependencies/blocked_by` or `E-BLOCKED`; the blocker item is not after the closed-issue item of Wave 2; the Wave 3 section contains `dependencies/blocked_by` or lacks `--add-assignee`; or the Final output section lacks `Blocker check: could not run`. Add these tests: one that asserts the helper returns an empty list for `REFS / "claim.md"`; one that removes the blocker item from a copy of the claim text (use `tmp_path` or string replacement, never edit the real file) and asserts the helper reports a problem; one that asserts Wave 2 states an open blocker stops with `E-BLOCKED` naming each one and "no GitHub, ClickUp or Orca write", that none or only closed continues as today, and that an unreadable list continues; one that asserts `SKILL.md` carries `E-BLOCKED` in its Claim mode list and in the `## Error handling` table together with the `Blocker check: could not run` row; and one that asserts `commands/issue.md` contains `E-BLOCKED` and that the `/sc:issue` row of `src/superclaude/core/HOW-WE-WORK.md` mentions "blocked by" and equals the same row of `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. These static tests pin the written contract; they do not show a live model following it, so name that limit in a one-line comment above the new tests.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_protocol.py tests/commands/test_routing_plugin_parity.py -q` passes with the new tests included.
- Reverting only Task 1's Wave 2 item in a scratch copy makes the helper test report a problem, shown by the mutation test passing.
- The other readers of the changed text still pass: `uv run pytest tests/commands/test_issue_command.py tests/issue_pipeline/test_brief.py tests/issue_watch/test_marker_contract.py tests/skills/test_issue_orca_worktree.py tests/skills/test_worker_contract.py tests/core/test_how_we_work_routing_table.py tests/cli/test_how_we_work_install.py -q` shows no new failure compared with the same run before Task 1.
- `make lint` reports no error for `tests/skills/test_issue_protocol.py`.
