---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-addOneSentenceTo-20261105-204034
version: "1"
priority: Medium
created_date: "2026-11-05"
---

# Document that `superclaude install --force` overwrites existing files in ~/.claude

Source: ./source.md
Goal: The Installation section of README.md states, in one added sentence, that `superclaude install --force` overwrites files that already exist in `~/.claude`.

## Constraints

- Only README.md changes; add exactly one sentence and edit no other sentence, section or file.
- The sentence goes inside the `## Installation` section (README.md), not in Quick start or later sections.

## Phase 1: Document the --force behavior

## Task 1: Add the --force overwrite sentence to the README Installation section

In README.md, under `## Installation` > `### Install the current package/CLI`, add one sentence at the end of the paragraph that starts "This installs the package, then framework assets". The sentence says that `superclaude install --force` overwrites files that already exist in `~/.claude`. Use backticks around the command and the path, as the surrounding text does. Do not touch the `### Upgrading to 5.0.0` paragraph, which already mentions `--force` separately.

Acceptance criteria:
- README.md contains one new sentence in the `## Installation` section that names `superclaude install --force` and `~/.claude` and says it overwrites files that already exist there.
- `git diff -- README.md` shows only that sentence added (one changed line, no other hunks), and `git diff --stat` lists no file other than README.md.
