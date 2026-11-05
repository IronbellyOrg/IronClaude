# Request: close the saved-reviewer-prompt gaps in /sc:implement

## Why

The fence-fix run (`.dev/tasks/done/TASK-WF-devGuideFenceFix-20261104-204854/`) showed two gaps in the `/sc:implement` rule that compares each saved reviewer prompt with the closed reviewer template:

1. The comparison is byte-exact outside the slots. A hand-filled prompt that dropped one blank line (between "Saved-probe re-check hit locations (may be empty): " and "Do not trust the implementer's report.") blocked the managed archive twice, although no review criterion was added, removed or reworded.
2. There is no recovery path. A saved prompt may never be overwritten, so once a prompt differs from the template, every later FINAL returns `issues` and the package can only archive by an ad-hoc user instruction (here: moving the two prompts to `artifacts/superseded-prompts/` and an `ARCHIVE: Ruling:` line, ledger `progress.md` lines 7-11 of that package). The re-review that preceded the move (a second `complete` line per task with no new `start`, prompts named `prompt-1-2.md` with no repair file) is also not described by the protocol.
3. The earlier package `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/` holds nine saved prompts (`artifacts/retries/T1/` to `T9/`, each `prompt-1-1.md`) with the same missing blank line; its FINAL passed without noticing.

## What to change

Rule source: `src/superclaude/skills/sc-implement-protocol/refs/qa.md` ("## FINAL derived test", saved-prompts bullet; "## Managed FINAL review (archive gate)"; "Saved prompts and paperwork-only reviews" under "## Subagent prompt (when not inline)"), `refs/ledger.md` (record forms / Resume), `refs/managed-workspace.md` (Enforcement map row for saved reviewer prompts). The plugin mirror `plugins/superclaude/skills/sc-implement-protocol/` must stay byte-identical to `src/`.

A. Whitespace tolerance. When FINAL compares a saved prompt with the template outside the slots, differences only in the number of blank lines between lines or in trailing whitespace are not a template difference; FINAL records them as a note. Any other difference (a changed, added, removed or reordered non-blank line) stays `issues` (managed) or `FINAL:` evidence (legacy), as today.

B. Recovery path for a defective saved prompt. When a FINAL flags a saved prompt as differing from the template:
- the executor re-runs that task's review with a template-exact prompt saved as the next free `prompt-<k>-<j>.md` of the same `start` (pinning its reviewed tree as `r<k>-<j>`), without reopening or reverting the task;
- a re-review with no blocking finding appends the task's `complete` line again (same verdict grammar, no new `start` line); a re-review with a confirmed blocker appends `blocked` and follows the existing Resume rows;
- the defective prompt is then moved unchanged (never edited or deleted) to `<pkg>/artifacts/superseded-prompts/T<id>-prompt-<k>-<j>.md` (managed) or `.dev/implement/<slug>/superseded-prompts/` (legacy), with a `README.md` there naming each moved file, its old path, the FINAL line that flagged it and the replacing prompt; this move is part of the protocol and needs no separate user approval;
- FINAL treats files under `superseded-prompts/` as history and does not compare them, but returns `issues` when a superseded prompt's task has no later template-exact saved prompt in `<retries>/T<id>/` or the README is missing.

C. Earlier package. With rule A in place, check mechanically that each of the nine `prompt-1-1.md` files in `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T1..T9/` differs from the template outside the slots only in blank lines, save the check script and its output under the new plan package's `artifacts/`, and add a short note file `artifacts/prompt-template-check.md` to that earlier package recording the result and pointing at the saved evidence. Do not edit, move or delete its prompts, ledger or other files.

## Checks

- Regression tests in `tests/skills/` that fail if rule A or rule B wording is missing from `refs/qa.md`, `refs/ledger.md` or `refs/managed-workspace.md`, or if any of those three files differs between `src/` and `plugins/` copies.
- `make sync-dev`, `make verify-sync`, and `uv run pytest tests/skills -q` pass (output saved as evidence).

## Out of scope

- A prompt-builder script, any other lesson from `docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-Specs.md`, any other skill, command or agent.
- Changing the reviewer template text itself.

## Constraints

- Never stage `.claude/` contents; edit `src/superclaude/` and the `plugins/` mirror, then `make sync-dev`.
- Installed primitives must not tell an agent to read anything through a `src/superclaude/...` path.
- `.dev/tasks/` is always staged (`git add .dev/tasks`); staging is not committing.
