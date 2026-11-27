---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-design-20261126-134817
version: "1"
priority: Medium
created_date: "2026-11-26"
---

# Implement the worktree and branch protocol: guide section, mirror, onboarding card and policy tests

Source: ./source.md
Goal: IronClaude has one short, tested, written rule for when new work gets its own branch and worktree, when an existing worktree is reused, how worktrees are named, and that lessons are written before a worktree is removed. The rule lives in the shared how-we-work guide and its plugin mirror, the onboarding page shows it instead of "being worked out", and a new test file pins it.

## Constraints

- Scope is five deliverables: the new guide section and the removal-timing pointer in `src/superclaude/core/HOW-WE-WORK.md`, the byte-identical mirror `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, the worktree card and build footer of `docs/onboarding/ironclaude-onboarding.html`, and the new `tests/core/test_how_we_work_worktree_policy.py`. No production code changes.
- Out of scope: the claim launcher and its `issue-<N>` naming, the cleanup script and its rules, the issue watcher, the `CLAUDE.md` examples at lines 318-341, the issue 290 card, the slide introduction at lines 516-518, and any tool that extracts lessons. Section 1 of `./source.md` lists them.
- The open owner questions of section 7 of `./source.md` (dropping the words from a name, lessons of issue-less worktrees, whether the watcher or the claim should refuse an issue that already has a worktree, the slide introduction, the `CLAUDE.md` examples, the footer rule) are not decided by this plan and are not written into the guide. They belong in the pull request body.
- The guide is a shared file: the level-table, routing-table and other-commands marker comments and every other section stay as they are, and every line the change adds is ASCII (plain hyphens, no en dashes).
- The mirror is never edited by hand: it is a copy of the guide after the guide's last edit.
- Python and tests run through uv (`uv run pytest`, `uv run ruff`); never `python -m` or bare `pip`.
- The tasks run in a straight line and the new test file comes last (the design's section 6 puts it first) so that the acceptance criteria of every task can pass the moment that task is done.
- Stage the changed files and `.dev/tasks`; never stage anything under `.claude/` or `.dev/issues/`. Staging is not committing.

## Phase 1: Guide policy text

## Task 1: Add the "Worktrees and branches" section to the guide

In `src/superclaude/core/HOW-WE-WORK.md`, insert a new unnumbered heading `## Worktrees and branches` and its bullets between the closing routing-table marker comment (line 350) and the `## Orca coordination` heading (line 352), with one blank line before the heading and one blank line after the section. The content is the fenced text block of section 3 of `./source.md` (between the `guide-section:begin` and `guide-section:end` comments). Use it verbatim, or tighten the wording without dropping any rule, so that the section stays within 400 words. The section is bullets and short paragraphs only (no table), holds no HTML comment or marker, and does not contain the three phrases that `tests/commands/test_worktrees_command.py:124-137` bans: "Every verb is a dry run", "every verb is a dry run" and "Verbs (a dry run unless --apply is given)".

Dependents that read this file and must keep passing: `tests/core/test_how_we_work_routing_table.py` (each marker once and in order, numbered-heading reference check at `_HEADING_RE`, ASCII guard at lines 329-334), `tests/core/test_claude_md_routing_block.py` (the level table copy in `src/superclaude/core/CLAUDE.md` equals the guide's), `tests/commands/test_worktrees_command.py` (banned phrases), `tests/cli/test_how_we_work_install.py` (the installed copy equals the guide bytes), and `tests/commands/test_help_command.py`.

Acceptance criteria:
- `src/superclaude/core/HOW-WE-WORK.md` has exactly one line `## Worktrees and branches`, located after the closing routing-table marker comment line and before the `## Orca coordination` line, with no marker or HTML comment inside the section.
- The section, from its heading to the line before `## Orca coordination`, is at most 400 words by `len(text.split())` and is ASCII only (`text.isascii()` is true).
- The section contains each of these exact substrings: `new worktree and branch`, `One writer per worktree`, `original worktree while it still exists`, `--ff-only`, `stop and ask`, `/sc:issue --claim`, `at most 24 characters`, `no spaces`, `no run of 2 to 4 digits`, `create nothing and ask the owner`, `Lessons comment`, `pins the worktree`, `checks that comment first`.
- `uv run pytest tests/core/test_how_we_work_routing_table.py tests/core/test_claude_md_routing_block.py tests/commands/test_worktrees_command.py tests/cli/test_how_we_work_install.py tests/commands/test_help_command.py -q` passes.

## Task 2: Point the /sc:worktrees row at the new section

Depends on: Task 1

In the `/sc:worktrees` row of the other-commands table of `src/superclaude/core/HOW-WE-WORK.md` (line 299), replace the sentence `When to remove a worktree after its pull request merges (item 4 of issue 289): after the pull request merges and every rule of the cleanup holds.` with `When to remove a worktree: after its pull request merges, the lessons are written (see Worktrees and branches below) and every rule of the cleanup holds.` Keep the rest of the row unchanged. Only this guide and its mirror contain the old sentence, and no test pins it. The row must stay ASCII with the same two table cells.

Acceptance criteria:
- The `/sc:worktrees` row of `src/superclaude/core/HOW-WE-WORK.md` contains `Worktrees and branches` and does not contain `item 4 of issue 289`; the rest of the row is byte-identical to before.
- The row still has exactly two table cells and the file still has each marker exactly once.
- `uv run pytest tests/core/test_how_we_work_routing_table.py tests/commands/test_worktrees_command.py -q` passes.

## Phase 2: Plugin mirror

## Task 3: Copy the guide over the plugin mirror

Depends on: Task 2

Overwrite `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` with the final content of `src/superclaude/core/HOW-WE-WORK.md` by copying the file (never by editing the mirror). Do not touch anything under `.claude/`; the level table is unchanged, so `src/superclaude/core/CLAUDE.md` needs no recopy.

Dependents that read the mirror or compare it with the guide: `tests/skills/test_review_prompt_overrides.py` (byte equality at lines 134-135), `tests/commands/test_routing_plugin_parity.py` (file comparison at line 38), `tests/commands/test_worktrees_command.py` (banned phrases in both files, lines 129-130), `tests/skills/test_review_brief_placement.py`, `tests/skills/test_spec_panel_review_loop.py` and `tests/skills/test_issue_protocol.py` (texts that must stay in the guide and the mirror).

Acceptance criteria:
- `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing and exits 0.
- `uv run pytest tests/skills/test_review_prompt_overrides.py tests/commands/test_routing_plugin_parity.py tests/commands/test_worktrees_command.py tests/skills/test_review_brief_placement.py tests/skills/test_spec_panel_review_loop.py tests/skills/test_issue_protocol.py -q` passes.
- `git status --short` lists no path under `.claude/`.

## Phase 3: Onboarding page

## Task 4: Replace the worktree card on slide 12

Depends on: Task 3

In `docs/onboarding/ironclaude-onboarding.html`, replace lines 520-524, the `<div class="card">` whose heading is "Worktree and branch protocol" and whose paragraph says the topic "is being worked out in issue #289", with the HTML block of section 4 (K5) of `./source.md`. The new card keeps the heading, keeps the glossary line (`<div class="term">`) and has no `<code>` element that holds a command or flag (its two `<code>` elements hold the name pattern and the example name). Lines 515-519 (the slide opening, eyebrow, "Being worked out" heading, introduction and the grid opening) and lines 525-530 (the issue 290 card and the closing tags) stay byte-identical.

Dependents: `tests/docs/test_onboarding_deck.py`, whose test `test_every_deck_command_and_flag_is_in_the_guide` reads every `<code>` element of the page and requires each command and flag in it to be in the guide.

Acceptance criteria:
- The page holds the card text "Worktree and branch protocol" and the example `clayphi/issue-289-wtrule`, and no longer holds the phrase "is being worked out in".
- `git diff -U0 docs/onboarding/ironclaude-onboarding.html` shows one changed hunk, inside the former lines 520-524; the issue 290 card (heading "Contributing rules") and lines 516-518 are untouched.
- `uv run pytest tests/docs/test_onboarding_deck.py -q` passes.

## Task 5: Update the build footer of the onboarding page

Depends on: Task 4

In `docs/onboarding/ironclaude-onboarding.html` line 579, replace `f3c1ef06` in the footer `Built from HOW-WE-WORK.md at commit f3c1ef06.` with the 8-character hash printed by `git rev-parse --short=8 HEAD` at the time of this edit. The commit that will hold the guide change does not exist yet, so a person corrects the footer when the artifact is re-published after the merge; that is a known limit and it is written in the pull request body, not in the page. The page's own maintenance rule (lines 3-5 of the file) requires the footer to be updated in the same pull request as a guide change.

Acceptance criteria:
- Line 579 of `docs/onboarding/ironclaude-onboarding.html` reads `Built from HOW-WE-WORK.md at commit <hash>.`, where `<hash>` is 8 hexadecimal characters equal to the output of `git rev-parse --short=8 HEAD` run at the time of the edit, and it differs from `f3c1ef06`.
- No other line of the page changes in this task.
- `uv run pytest tests/docs/test_onboarding_deck.py -q` passes, including `test_deck_keeps_its_build_commit_footer`.

## Phase 4: Policy tests

## Task 6: Create the policy test file with the name checker and its tests

Depends on: Task 5

Create `tests/core/test_how_we_work_worktree_policy.py` following the contract of section 5 of `./source.md`. Imports are `re`, `pytest` and `pathlib.Path`; constants `_REPO = Path(__file__).resolve().parents[2]`, `_GUIDE`, `_TWIN` (the mirror) and `_DECK`. Define the helpers `_NUMBER_RUN` (the regular expression `(?<!\d)\d{2,4}(?!\d)`, the same bound as `scripts/worktree_cleanup.py:1462`), `branch_errors(branch)` (whole string matches `^[A-Za-z0-9]+(-[A-Za-z0-9]+)*/issue-[1-9][0-9]*(-[a-z0-9]+)*$`, `len(branch) <= 24`, the words part has no `_NUMBER_RUN` match, and when the bare form `<login>/issue-<N>` is itself over 24 the error text contains the word `stop`) and `max_words_length(login, digits)` (`16 - len(login) - digits`). Add the tests `test_checker_accepts`, `test_checker_rejects`, `test_bare_form_over_the_limit_is_a_stop` and `test_budget_formula`, parametrized with the names and values listed in the section 5 table of `./source.md`. The checker lives only in this test file; no production code is added.

Acceptance criteria:
- `tests/core/test_how_we_work_worktree_policy.py` exists and `uv run pytest tests/core/test_how_we_work_worktree_policy.py -q` passes.
- `branch_errors` accepts `clayphi/issue-289-wtrule` (24), `clayphi/issue-834-clean` (23), `ironbelly/issue-517-orca` (24), `clayphi/issue-1234-docs` (23), `clayphi/issue-289` (17), `longloginname/issue-289` (23), `Ab-c/issue-5` (12) and `a/issue-1-v12345` (16), and rejects `clayphi/issue-289-wtrules` (25), a name with a space, `clayphi/issue-0289`, `clayphi/issue-`, `clayphi/issue-289-`, `clayphi/issue-289-py312`, `clayphi/issue-289-v2024`, `a--b/issue-1`, `-a/issue-1` and `a/issue-1-x/y`.
- `branch_errors("averylonglogin1/issue-289")` returns an error containing `stop`; `max_words_length("clayphi", 3)` is 6, `max_words_length("clayphi", 4)` is 5 and `max_words_length("longloginname", 3)` is 0.
- `uv run ruff check tests/core/test_how_we_work_worktree_policy.py` and `uv run ruff format --check tests/core/test_how_we_work_worktree_policy.py` pass.

## Task 7: Add the guide, mirror and onboarding tests to the policy file

Depends on: Task 6

In `tests/core/test_how_we_work_worktree_policy.py` add the helper `_section()` (the text of the guide from the line `## Worktrees and branches` up to the next line that starts with `## `; it fails with a clear message when the heading is missing or appears more than once) and the tests of section 5 of `./source.md` that read the repository files: `test_section_exists_once_before_orca_coordination`, `test_section_is_at_most_400_words`, `test_section_is_pure_ascii_and_has_no_banned_phrase`, `test_section_states_each_rule` (parametrized over the thirteen key phrases listed in Task 1), `test_every_backticked_branch_example_in_the_section_passes` (at least one example exists), `test_deletion_is_detected` (removes one key phrase from a copy of the section and asserts the check reports it), `test_mirror_is_byte_identical`, `test_pointer_names_the_section` and `test_deck_card_is_replaced_and_neighbours_untouched`. These tests read `src/superclaude/core/HOW-WE-WORK.md`, the mirror and `docs/onboarding/ironclaude-onboarding.html` as changed by Tasks 1 to 5.

Acceptance criteria:
- `uv run pytest tests/core/test_how_we_work_worktree_policy.py -v` passes and lists the thirteen tests of section 5 of `./source.md` (the four from Task 6 and the nine added here, the parametrized ones counted once each).
- Removing any one of the thirteen key phrases from a copy of the guide section makes `test_section_states_each_rule`'s check report it, and `test_deletion_is_detected` proves that.
- `uv run pytest tests/core/test_how_we_work_worktree_policy.py tests/core/test_how_we_work_routing_table.py tests/core/test_claude_md_worktree_rule.py tests/core/test_orca_session_launch_guidance.py tests/core/test_claude_md_routing_block.py tests/docs/test_onboarding_deck.py tests/commands/test_worktrees_command.py tests/commands/test_help_command.py tests/commands/test_routing_plugin_parity.py tests/skills/test_review_prompt_overrides.py tests/skills/test_sc_recommend_routing_contract.py tests/skills/test_issue_protocol.py tests/skills/test_review_brief_placement.py tests/skills/test_spec_panel_review_loop.py tests/cli/test_how_we_work_install.py tests/recommend -q` passes.
- `uv run ruff check tests/core/test_how_we_work_worktree_policy.py` and `uv run ruff format --check tests/core/test_how_we_work_worktree_policy.py` pass.
- `git status --short` lists only the guide, the mirror, the onboarding page, the new test file and files under `.dev/tasks`; nothing under `.claude/` or `.dev/issues/` is staged.
