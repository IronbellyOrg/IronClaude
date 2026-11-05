---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-devGuideFenceFix-20261104-204854
version: "1"
priority: Medium
created_date: "2026-11-04"
---

# Fix the nested code-fence rendering bugs in the developer guide

Source: ./source.md
Goal: the six example templates in `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` whose three-backtick outer fence is closed early by an inner block get four-backtick outer fences, so the fence-state script reports no inner fence closing an outer one, and no other line of the guide changes.

## Constraints

- Only `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` changes, and only on the twelve outer-fence lines the source lists (the opening and closing line of each of the six templates). No prose line, inner code block or other fence changes. Scripts and evidence go under this package's `./artifacts/`.
- Each opening line becomes four backticks followed by `markdown`; each closing line becomes four backticks and nothing else.
- The archived script `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-fence-check.py` is copied, never edited; the copy lives at `./artifacts/fence-check.py` and runs with `uv run python -I`.
- The earlier guide refactor is still uncommitted, so "the guide before this plan" means the copy `./artifacts/guide-before.md` saved before the first edit, not `HEAD`.
- No em dash and no en dash in changed lines.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included. Staging is not committing; commit only when the user asks.

## Phase 1: Fix the Quick Start template

## Task 1: Save the baseline and fix the 2.1 Quick Start command template fence

Before any edit, copy `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` byte for byte to `./artifacts/guide-before.md`, copy `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-fence-check.py` to `./artifacts/fence-check.py`, and save `uv run python -I ./artifacts/fence-check.py docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` output as `./artifacts/fence-before.txt`. Then, in section 2.1 "Create a Minimal Command", read the `/sc:hello` command template and change its outer opening fence (guide line 136 today, ```` ```markdown ````) to four backticks plus `markdown` and its outer closing fence (guide line 177 today, the bare fence just before `### 2.2 Create a Minimal Agent`) to four backticks. If either line number has moved, locate the pair by the template and record the actual lines in `./artifacts/t1-notes.txt`.

Acceptance criteria:
- `./artifacts/guide-before.md` is byte-identical to the guide as it was before this task's edit (`cmp` against the task's start snapshot of the guide passes), and `./artifacts/fence-before.txt` lists the 2.1 spot (outer fence opened at line 136).
- The guide's 2.1 command template opens with ````` ````markdown ````` and closes with ````` ```` `````; running the script on the edited guide shows `### 2.2 Create a Minimal Agent` outside any fence and no spot whose outer fence opened at line 136 or 177; that output is saved as `./artifacts/fence-t1.txt`.
- `diff ./artifacts/guide-before.md docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` shows exactly two changed lines, the two fence lines, saved as `./artifacts/t1-diff.txt`.

## Phase 2: Fix the section 10 example templates and check the whole change

## Task 2: Fix the five section 10 template fences

Depends on: Task 1

In section 10 "Complete Examples" of `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, read each of these templates and change its outer opening fence to four backticks plus `markdown` and its outer closing fence to four backticks (guide line numbers as of today): Example 1 command file (1322, 1379); Example 2 command file (1435, 1501); Example 2 skill file `src/superclaude/skills/sc-pr-review/SKILL.md` (1505, 1605); Example 3 command file `src/superclaude/commands/adversarial.md` (1615, 1674); Example 3 `src/superclaude/skills/sc-adversarial/refs/agent-specs.md` (1828, 1884). If a line number has moved, locate the pair by its `**File**:` line and template and record the actual lines in `./artifacts/t2-notes.txt`. Then run the whole-change checks below and save their outputs.

Acceptance criteria:
- `uv run python -I ./artifacts/fence-check.py docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, saved as `./artifacts/fence-after.txt`, prints `none` under "Inner fence closes outer fence"; shows `### 2.2 Create a Minimal Agent`, every `### Example N:` heading of section 10 and `## Appendix C: Agent Template` outside any fence; and shows `## Appendix B: Command Template`'s template headings inside its four-backtick fence, as in `./artifacts/fence-before.txt`.
- `diff ./artifacts/guide-before.md docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, saved as `./artifacts/guide-diff.txt`, changes exactly twelve lines, each a lone outer-fence line (```` ``` ```` to ````` ```` ````` or ```` ```markdown ```` to ````` ````markdown `````), and nothing else.
- The changed lines contain no em dash or en dash, checked with `LC_ALL=C grep -P '\xE2\x80[\x93\x94]'` over the `>` lines of `./artifacts/guide-diff.txt` (no output), saved as `./artifacts/dash-check.txt`.
- `uv run pytest tests/docs -q` passes, output saved as `./artifacts/pytest-docs.txt`.
- `git status --porcelain -- docs src plugins tests` shows no change outside the guide other than the already-staged `docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-Specs.md`, saved as `./artifacts/changed-files.txt`.
