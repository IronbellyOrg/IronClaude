# Draft notes

Leave a list empty (write "None") when there is nothing to report. The orchestrator asks the user one question only when either list has an item.

## New material

<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). -->

- The pipeline is a not-yet-implemented dependency being built in parallel; its proposed `pipeline.json` input may move to a location the agent cannot edit. Sources: `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/launch-levels-addendum.md:73`, `:97`; task instructions.
- Existing installed hook registration and Bash blocking example: `src/superclaude/hooks/hooks.json:75` and `src/superclaude/hooks/scripts/block-bare-python.sh:1`.
- Project hook registration exists in `.claude/settings.json:2`; hook sources live under `src/superclaude/hooks/`, synced with `make sync-dev`, and `.claude/settings.json` is the only tracked `.claude/` file. Source: `CLAUDE.md` project instructions.
- Current claim protocol and command entry points are `src/superclaude/skills/sc-issue-protocol/refs/claim.md:1` and `src/superclaude/commands/issue.md:11`; hook tests include `tests/hooks/test_block_bare_python.py` (Glob search).
- Related issue titles, states, reasons and absence of a true duplicate: `.dev/issues/draft-20261105-165641-hook-that-mechanically-enforces-the-laun/scout.md:21` and task instructions.
- Automated tests should cover each level and the listed edge cases, and evaluate speed; this makes the request's testability and edge cases observable. Source: `.dev/issues/draft-20261105-165641-hook-that-mechanically-enforces-the-laun/description.md:3` and task instructions.
- Codegraph and auggie tools were unavailable in this session. The quick codebase pass followed `.claude/commands/sc/analyze.md` using Glob, Grep and Read instead.

## Contradictions

<!-- Each place where the description disagrees with the code, one per line, with path:line evidence. -->

- None
