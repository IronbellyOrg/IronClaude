---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-followUpForIssue-20261126-173307
version: "1"
priority: Medium
created_date: "2026-11-26"
---

# Write the six owner answers of issue 289 into the worktree guide, the deck, CLAUDE.md and the tests

Source: ./source.md
Goal: The "Worktrees and branches" section of the guide and its mirror state the six owner answers, slide 12 of the onboarding deck and the worktree examples of CLAUDE.md no longer call the topic open or show stale names, and the tests pin all of it.

## Constraints

- Test, guide, deck and CLAUDE.md edits only; no production code (nothing under `src/superclaude/cli/`, `scripts/`, hooks or skills changes).
- Never edit or stage anything under `.claude/`. `.dev/tasks/` stays staged.
- ASCII only in the guide section; keep every existing rule that the six answers do not change, in the owner's wording where the source quotes it.
- Decision recorded here: answer 2 says "never stop", so a name whose bare form `<login>/issue-<N>` is over 24 characters is kept and the work goes on. The sentence "create nothing and ask the owner", its key phrase and the "stop" test are replaced. A name that carries words over 24 characters is still an error: drop the words.
- Not in scope (MB-2): reading the digit-run pattern from scripts/worktree_cleanup.py. The user withdrew that item; the hand-copied _NUMBER_RUN of tests/core/test_how_we_work_worktree_policy.py stays as it is.
- The branch `clayphi/issue-289-rest` was created in the reused worktree with `git switch -c` on the owner's order; the guide's "never switch branches in a worktree" line is left as it is.

## Phase 1: Guide text and mirror

## Task 1: Rewrite the "Worktrees and branches" section in src/superclaude/core/HOW-WE-WORK.md

Replace the section that starts at the line `## Worktrees and branches` and ends before `## Orca coordination` in `src/superclaude/core/HOW-WE-WORK.md` with the text below (answers 1 to 4 and 6 of the source; answer 5 is Tasks 3 and 4). Do not change any other line of the file. The first paragraph, the new-work bullet and the reuse bullet stay exactly as they are today; read them from the file and keep them byte for byte. The three bullets that change are the claim bullet, the names bullet and the lessons bullet:

- Claim bullet, new text (one line in the file):

```text
- **Check before `/sc:issue --claim` or a Project Status change.** A claim reuses the worktree it finds and starts its agent at once; the watcher claims by itself. Neither refuses an issue that already has a worktree; the iteration start check asks the owner first. A re-run of the claim's own earlier run (no `launch` entry in its `worktree.json`) is exempt. A handoff of unfinished work after the first session has stopped skips only the already-claimed check: it must still match on repository, issue and branch, because that match proves it is the same work.
```

- Names bullet, new text (one line in the file):

```text
- **Names:** `<login>/issue-<N>[-<words>]`, at most 24 characters, no spaces; `<login>` is `gh api user --jq .login`. Create with `--name issue-<N>-<words>`; Orca adds the login (use `--branch` if it does not). Words are lowercase letters and digits with no run of 2 to 4 digits (cleanup reads it as an issue). Example: `clayphi/issue-289-wtrule` (24). When the words do not fit, drop them and keep `<login>/issue-<N>`; never stop on it, even when that is over 24. A login that has a run of 2 to 4 digits is left out: use `issue-<N>-<words>`. A worktree made by the claim launcher keeps the launcher's `issue-<N>` name. After creation the agent checks `git branch --show-current` and may run `git branch -m` before any push; never switch branches in a worktree.
```

- Lessons bullet: the current bullet with one sentence inserted before its last sentence (the one that starts `A person runs`):

```text
A worktree with no issue keeps its lessons in its own `.dev/` notes; `/sc:worktrees` saves them to the evidence repo before removal (issue 881 covers a worktree with no merged pull request).
```

The section must keep exactly one heading line `## Worktrees and branches`, contain no HTML comment, be pure ASCII, and have at most as many words as the new cap that Task 6 sets (measure it with `awk` over the section lines; expected about 540 to 560). The `/sc:worktrees` table row of the guide (which already points at the section) is left unchanged.

Acceptance criteria:
- `git diff -U0 src/superclaude/core/HOW-WE-WORK.md` shows changes only between the `## Worktrees and branches` and `## Orca coordination` lines, and only in the three bullets above.
- The section no longer contains the text `create nothing and ask the owner`, and contains each of `Neither refuses an issue that already has a worktree`, `iteration start check asks the owner first`, `skips only the already-claimed check`, `match on repository, issue and branch`, `drop them and keep`, `never stop on it`, `is left out: use`, `keeps the launcher's`, `own `.dev/` notes` and `issue 881` exactly once.
- The existing phrases `same repository, issue and branch`, `is exempt`, `handoff of unfinished work`, `after the first session has stopped` and `the watcher claims by itself` each still occur exactly once in the section.
- The section is pure ASCII (`LC_ALL=C grep -nP '[^\x00-\x7F]'` over its lines prints nothing).

## Task 2: Copy the guide byte for byte to the plugin mirror plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md

Depends on: Task 1

Copy `src/superclaude/core/HOW-WE-WORK.md` over `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` with `cp`. Do not edit the mirror by hand.

Acceptance criteria:
- `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing and exits 0.
- `uv run pytest tests/core/test_how_we_work_routing_table.py -q` passes (it reads the guide and the mirror; the `/sc:worktrees` row is unchanged).

## Phase 2: Onboarding deck

## Task 3: Update the slide 12 heading, eyebrow and introduction and the footer hash in docs/onboarding/ironclaude-onboarding.html

In `docs/onboarding/ironclaude-onboarding.html`, slide `s12` (lines about 515 to 530): change the eyebrow line (`<p class="eyebrow"><b>12</b> · Contributing and open topics · GitHub issues #289 and #290</p>`) to `<p class="eyebrow"><b>12</b> · Contributing and worktrees · HOW-WE-WORK "Worktrees and branches", GitHub issue #290</p>`, keeping the middle-dot characters the line already uses; change the heading `Contributing, and one open topic` to `Contributing and worktrees`; change the introduction paragraph (`The contributing rules are settled for now; the worktree topic is still open in its own issue. Until it is settled, ask your lead.`) to `Both rules are settled. The worktree rule is the left card and the guide section "Worktrees and branches"; the contributing rule is the right card, with its history in issue #290. If a case is not covered, ask your lead.` Keep the `Worktree and branch protocol` card and the `Contributing rules` card, including the link to issue 290, unchanged. Change the build footer `Built from HOW-WE-WORK.md at commit a98d7b42.` so that the hash is the output of `git rev-parse --short=8 HEAD` taken at the time of the edit (the commit before this change). No other line of the file changes.

Acceptance criteria:
- `grep -c -E 'one open topic|still open in its own issue|issues #289 and #290|open topics' docs/onboarding/ironclaude-onboarding.html` prints 0.
- (MB-1) The introduction paragraph of slide `s12` in `docs/onboarding/ironclaude-onboarding.html` is exactly `Both rules are settled. The worktree rule is the left card and the guide section "Worktrees and branches"; the contributing rule is the right card, with its history in issue #290. If a case is not covered, ask your lead.`, and the old sentence `the worktree topic is still open in its own issue` no longer occurs in the file.
- The file contains `Contributing and worktrees` (heading and eyebrow), the `Worktree and branch protocol` card, the `Contributing rules` card and `https://github.com/IronbellyOrg/IronClaude/issues/290`.
- The footer matches `Built from HOW-WE-WORK\.md at commit [0-9a-f]{8}\.` and the hash equals `git rev-parse --short=8 HEAD` at that moment.
- `uv run pytest tests/docs/test_onboarding_deck.py -q` passes.

## Phase 3: CLAUDE.md examples

## Task 4: Replace the stale worktree examples in CLAUDE.md

In the repository `CLAUDE.md`, section `### Parallel Development with Git Worktrees` (lines about 301 to 342): (a) add after the bullet that starts `- **Existing checkouts under the retired` one bullet: `- **Names:** a worktree and its branch are named as in \`src/superclaude/core/HOW-WE-WORK.md\`, section "Worktrees and branches": branch \`<login>/issue-<N>[-<words>]\`, at most 24 characters, no spaces; create the worktree with \`--name issue-<N>-<words>\` and Orca adds the login.` (plain backticks); (b) replace the example block (the comment line and the `orca worktree create --name pm-agent ...` line) with the comment `# Create a worktree for issue 289, based on origin/integration, with an agent in it (Orca adds the login: the branch is <login>/issue-289-wtrule)` and the line `orca worktree create --name issue-289-wtrule --base-branch origin/integration --agent claude --prompt "<task>"`; keep the `orca worktree list` example; (c) replace the two `Usage` bullets that name worktree `integration` and worktree `pm-agent` with `- Worktree \`issue-289-wtrule\` (branch \`<login>/issue-289-wtrule\`): created by session A with \`--agent claude\`; that agent works there (path from \`orca worktree list\`)` and `- Worktree \`issue-301-hooks\` (another issue): created by session A with \`--agent claude\`; that agent works there`; (d) change the cleanup line `orca worktree rm --worktree name:integration` to `orca worktree rm --worktree name:issue-289-wtrule`. Do not change the first bullet (ownership), the `ABSOLUTE RULE` text, or any line outside that section. `src/superclaude/core/CLAUDE.md` has no stale name example and is not changed.

Acceptance criteria:
- `grep -n 'pm-agent' CLAUDE.md` prints no line from the worktree section (lines 301 to 345); `grep -n 'name:integration' CLAUDE.md` prints nothing.
- Every `orca worktree create` line of the section still contains `--agent`.
- `uv run pytest tests/core/test_claude_md_worktree_rule.py -q` passes after Task 7 (before Task 7 it still passes: nothing it pins was removed).

## Phase 4: Tests

## Task 5: Rewrite the name checker in tests/core/test_how_we_work_worktree_policy.py to follow the answers

Edit `tests/core/test_how_we_work_worktree_policy.py` (top of file to the end of `test_budget_formula`, about lines 1 to 116). (b) Make the login optional in `_BRANCH_RE` so the bare form `issue-<N>[-<words>]` matches. (c) Rewrite `branch_errors`: no login (bare form): errors only for more than 24 characters in all and for a digit run in the words (`_NUMBER_RUN.search`); with a login: an error when the words are present and the whole name is over 24 characters ("drop the words"), an error for a digit run in the words, an error for a digit run in the login ("leave the login out and use issue-<N>-<words>"); a bare `<login>/issue-<N>` over 24 characters is no error (never stop). Because the cleanup pattern has a capture group, search with `.search` on the text only, never `.findall`. (d) Update the parametrized cases: accepts add `issue-289-wtrule`, `issue-289`, `averylonglogin/issue-289` (bare form over 24, kept), `dev1/issue-289`; rejects add `dev42/issue-289`, `dev42/issue-289-words`, `issue-289-py312`, `issue-0289`, `averylonglogin1/issue-289-x` (words do not fit); keep the other existing cases that still hold and remove none that still hold. (e) Replace `test_bare_form_over_the_limit_is_a_stop` by `test_bare_form_over_the_limit_is_kept` (accepted, no "stop" in any message) and update `test_budget_formula` so it no longer asserts a "stop" message: for words that fit it asserts `[]`, one character more asserts an error, and the bare form is always accepted.
Acceptance criteria:
- `uv run pytest tests/core/test_how_we_work_worktree_policy.py -q -k "checker or budget or bare"` passes, and the parametrized rejects include `dev42/issue-289` and the accepts include `averylonglogin/issue-289`.
- `uv run ruff check tests/core/test_how_we_work_worktree_policy.py` and `uv run ruff format --check tests/core/test_how_we_work_worktree_policy.py` pass.

## Task 6: Update the key phrases, the word cap and the deck assertions in tests/core/test_how_we_work_worktree_policy.py

Depends on: Task 1, Task 3, Task 5

Edit the section-pinning part of `tests/core/test_how_we_work_worktree_policy.py` (from `_KEY_PHRASES` to the end of the file). (a) In `_KEY_PHRASES` remove `create nothing and ask the owner` and add the phrases of Task 1 that state the new rules, each of which occurs exactly once in the section: `Neither refuses an issue that already has a worktree`, `iteration start check asks the owner first`, `skips only the already-claimed check`, `match on repository, issue and branch`, `drop them and keep`, `never stop on it`, `is left out: use`, `keeps the launcher's`, `own `.dev/` notes`, `issue 881`. No phrase may contain another phrase (the deletion test removes one phrase and expects only it to be reported). (b) Change the 400-word cap in `test_section_is_at_most_400_words` (rename to `test_section_is_within_the_word_cap`) to the measured word count of the new section rounded up to the next multiple of 10, no higher. (c) Update `test_deck_card_is_replaced_and_neighbours_untouched` to assert the new slide: `Contributing and worktrees` present, `Worktree and branch protocol` and `Contributing rules` cards present, `clayphi/issue-289-wtrule` present, the old strings `Contributing, and one open topic`, `still open in its own issue`, `issues #289 and #290`, `how they are named is being worked out` and `issues/289` all absent, the exact new introduction paragraph text of Task 3 present (MB-1), the words `still open` absent between `id="s12"` and `id="s13"` in the deck so that an introduction that still calls the topic open fails (MB-1), and the footer regex `Built from HOW-WE-WORK\.md at commit [0-9a-f]{7,40}\b` present. (d) Keep the mirror, pointer, backticked-example and ASCII tests as they are.

Acceptance criteria:
- `uv run pytest tests/core/test_how_we_work_worktree_policy.py -q` passes, with `test_section_states_each_rule` and `test_deletion_is_detected` collected for every phrase of the new list (the new phrases included) and no phrase reported twice.
- Deleting any one new phrase from a copy of the section makes the suite's `_missing_phrases` report exactly that phrase (the existing parametrized deletion test shows it).
- `uv run pytest tests/core tests/docs tests/commands/test_worktrees_command.py tests/worktree_cleanup -q` passes, `make lint` passes, and `uv run ruff format --check tests/core/test_how_we_work_worktree_policy.py tests/core/test_claude_md_worktree_rule.py` passes.

## Task 7: Pin the new CLAUDE.md examples in tests/core/test_claude_md_worktree_rule.py

Depends on: Task 4

Add two tests to `tests/core/test_claude_md_worktree_rule.py` using its existing `_section()`: `test_names_follow_the_guide_pattern` asserts the section contains the `Names:` bullet text `<login>/issue-<N>[-<words>]`, `at most 24 characters`, `no spaces`, `--name issue-<N>-<words>` and the words `Worktrees and branches`; `test_examples_use_issue_names` asserts the section no longer contains `pm-agent` or `name:integration`, that its `orca worktree create` example line contains `--name issue-` and `--agent`, and that the `orca worktree rm` example line names an `issue-` worktree. The three existing tests stay unchanged.

Acceptance criteria:
- `uv run pytest tests/core/test_claude_md_worktree_rule.py -q` passes with five tests.
- Reverting Task 4 on a scratch copy of the section text (re-inserting `pm-agent`) makes `test_examples_use_issue_names` fail.
- `uv run ruff check tests/core/test_claude_md_worktree_rule.py` and `uv run ruff format --check tests/core/test_claude_md_worktree_rule.py` pass.
