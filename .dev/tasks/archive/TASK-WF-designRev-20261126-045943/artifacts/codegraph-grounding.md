# Codegraph grounding

## Run state

- index_state: fresh (recorded by the first generation of this plan in the same run; no second readiness check, per the protocol)
- checked_at: 2026-11-26T04:11:48Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-290
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-290
- access: mcp (lookup tools listed)
- tokens: none
- Note: this is the regenerated plan (route: regenerate, after the review of the first plan). Every file it edits is Markdown, YAML or HTML, which the graph does not index, so structure and dependents come from Read and Grep (the floor). The first plan's grounding note is in `.dev/tasks/archive/TASK-WF-design-20261126-041053/artifacts/codegraph-grounding.md`.

## Resolved symbols

| Name | Kind | Location | Method |
|---|---|---|---|
| test_every_deck_command_and_flag_is_in_the_guide | function | tests/docs/test_onboarding_deck.py:83 | codegraph_search, then Read (first plan) |
| test_guide_is_ascii_except_the_ruling_example | function | tests/core/test_how_we_work_routing_table.py:329 | codegraph_search, then Grep and Read (first plan) |
| test_guide_and_plugin_twin_are_byte_equal | function | tests/skills/test_review_prompt_overrides.py:134 | codegraph_search, then Read (first plan) |

## Dependents

Unchanged from the first plan: the guide and its plugin copy are read by 14 test files; the PR template by `tests/core/test_default_branch_agreement.py`; the deck by `tests/docs/test_onboarding_deck.py`; `docs/developer-guide/contributing-code.md` is deep-linked from `docs/developer-guide/documentation-index.md` and `docs/developer-guide/README.md`; the two issue forms and `CONTRIBUTING.md` are read by no test. Task 8 runs all 16 test files. An empty graph answer is not used as evidence of absence.

## Pre-check

| Check | Result |
|---|---|
| Files named by Tasks 1 to 8 exist | The eight edit targets and 16 test files exist (checked in the first plan; the review did not change the file set). New artifacts are written under `./artifacts/` by the tasks |
| Review defects of the first plan fixed | Gate greps on this plan: no checkbox or numbered lines, no `.claude/` path, no absolute path; base commit recorded in Task 1; ASCII check expects no output; Task 8 has no item count; card HTML is pasted in Task 7 |
| Dependents of touched files that no task names | None found |
| Graph tokens | none |

Count: 8 tasks checked, 0 unresolved names, 0 unnamed dependents.
