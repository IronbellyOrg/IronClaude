# Request: fix the nested code-fence rendering bugs in the developer guide

## What to change and why

In `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, six example file templates are wrapped in a three-backtick outer fence that holds three-backtick inner blocks. The first inner block's bare closing fence closes the outer fence instead, so the rest of the template renders as live Markdown, and the template's own closing fence then opens a new fence that swallows the text after it (for example the `### 2.2 Create a Minimal Agent` heading). The earlier guide refactor reported ten such spots without fixing them: `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-stale-fences.txt`.

The fix is the same one already applied to Appendix B: make each affected outer fence four backticks, opening and closing, so the inner three-backtick blocks nest correctly.

## The six outer fences (guide line numbers as of 2026-11-04, after the refactor)

| Template | Opening line (today) | Closing line (today) |
|---|---|---|
| 2.1 Quick Start command template (`src/superclaude/commands/hello.md` example) | 136 (```` ```markdown ````) | 177 (```` ``` ````) |
| Section 10, Example 1 command file | 1322 (```` ```markdown ````) | 1379 (```` ``` ````) |
| Section 10, Example 2 command file | 1435 (```` ```markdown ````) | 1501 (```` ``` ````) |
| Section 10, Example 2 skill file (`sc-pr-review/SKILL.md`) | 1505 (```` ```markdown ````) | 1605 (```` ``` ````) |
| Section 10, Example 3 command file (`adversarial.md`) | 1615 (```` ```markdown ````) | 1674 (```` ``` ````) |
| Section 10, Example 3 `refs/agent-specs.md` | 1828 (```` ```markdown ````) | 1884 (```` ``` ````) |

Each opening line becomes four backticks plus `markdown`; each closing line becomes four backticks. Confirm each pair by reading the guide before editing; if a line number has moved, find the pair by its template and say so in the task notes.

## Checks

- Re-use the existing fence-state script `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-fence-check.py` (copy it into this plan's package `./artifacts/`, do not edit the archived copy) and run it with `uv run python -I` on the guide before and after the edits. After the edits its "Inner fence closes outer fence" section prints `none`, the headings `### 2.2 Create a Minimal Agent`, `### Example 2: ...` and `### Example 3: ...` are outside any fence, and Appendix B and Appendix C keep the state they have today (Appendix B inside its four-backtick fence, Appendix C heading outside).
- The guide's diff against its state before this plan (the earlier refactor is still uncommitted, so compare with a copy saved before the first edit, not with `HEAD`) changes exactly the twelve fence lines above and nothing else; save that diff under `./artifacts/`.
- `uv run pytest tests/docs -q` passes.

## Out of scope

- Any other line of the guide, including prose and the inner code blocks.
- Any other file.

## Constraints

- Only `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` changes; scripts and evidence go under the plan package's `./artifacts/`.
- No em dash and no en dash in changed lines.
- `.dev/tasks/` is always staged (`git add .dev/tasks`); staging is not committing; commit only when the user asks.
