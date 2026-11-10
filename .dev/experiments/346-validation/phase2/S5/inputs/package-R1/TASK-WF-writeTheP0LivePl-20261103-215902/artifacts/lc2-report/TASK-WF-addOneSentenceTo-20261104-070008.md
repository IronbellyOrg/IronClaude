---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-addOneSentenceTo-20261104-070008
version: "1"
priority: Medium
created_date: "2026-11-04"
---

# Document superclaude install --force in the README Installation section

Source: ./source.md
Goal: README.md's Installation section contains one sentence telling readers that `superclaude install --force` overwrites files that already exist in `~/.claude`.

## Constraints

- Edit only `README.md`; change no other file, no code and no test.
- Add exactly one sentence; do not reword, move or delete any existing text in the Installation section.
- The sentence must match the code: in `src/superclaude/cli/main.py` the `install` command passes `force` to the core files, commands, agents, skills, hooks, templates and user-setup steps, but not to the codegraph phase (its docstring says "--force is not forwarded to it"), and `src/superclaude/cli/install_hooks.py` (`_SEED_FILES` and the comment above it) never overwrites the user data seed file `~/.claude/auggie-projects.txt`, even with `--force`. The sentence must not claim that every file in `~/.claude` is overwritten.

## Phase 1: README states what --force overwrites

## Task 1: Add the --force sentence to the README Installation section

In `README.md`, under `## Installation` > `### Install the current package/CLI`, add one sentence at the end of the paragraph that begins "This installs the package, then framework assets" (the paragraph directly after the `pipx install` / `superclaude install` code block). The sentence states that running `superclaude install --force` overwrites the IronClaude files that already exist in `~/.claude` (core files, commands, agents, skills, hook scripts and templates), while a plain `superclaude install` skips files that already exist; it keeps the qualification from the Constraints that the user data file `~/.claude/auggie-projects.txt` is never overwritten. Ground the wording in the skip messages in `src/superclaude/cli/install_core.py`, `src/superclaude/cli/install_commands.py`, `src/superclaude/cli/install_agents.py`, `src/superclaude/cli/install_skills.py`, `src/superclaude/cli/install_hooks.py` and `src/superclaude/cli/install_templates.py` ("use --force to overwrite" / "use --force to reinstall").

Acceptance criteria:
- `git diff -- README.md` shows exactly one added sentence inside `## Installation` > `### Install the current package/CLI` and no removed or changed lines elsewhere in the file.
- The added sentence contains the literal text `superclaude install --force` and `~/.claude`, and says that existing files there are overwritten.
- The added sentence does not say that every file in `~/.claude` is overwritten, and names `~/.claude/auggie-projects.txt` as kept.
- `git status --porcelain` lists `README.md` as the only changed path outside `.dev/tasks/`.
