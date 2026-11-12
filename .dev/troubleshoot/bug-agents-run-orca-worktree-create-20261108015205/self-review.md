# Self-review of merged fix proposal (Wave 4 step 4)

<!-- Returned by troubleshoot-analyst (lens self-review), persisted by parent on receipt 2026-11-08T02:20Z. Raw verdict FAIL; consumer mapping: documented blocker. -->

**Verdict: FAIL** (one blocking finding). **Consumer mapping:** documented blocker.

## Findings

**B-1 (blocking): pinned phrase "`orca terminal close --worktree`" would fail as written.**
- tests/core/test_orca_session_launch_guidance.py:14-31 does an exact substring check (`assert required in section`) on raw text, backticks included; section runs from `### Orca session launches` to the next `\n## ` (:15-16); existing pins put backticks inside the string (e.g. "`agent launch`" at :22).
- The proposed sentence (merged-output.md:16) wraps the whole command in one code span: `orca terminal close --worktree path:<path> --all` with the closing backtick after `--all`, so the literal "`orca terminal close --worktree`" (closing backtick included) does not appear. The new pin fails for both files.
- Same ambiguity for the new project test (merged-output.md:40) against the bullet at :18.
- Fix: pin "`orca terminal close --worktree path:<path> --all`", or pin "orca terminal close --worktree" without backticks.
- Second pin "worktree you did not just create" matches :16 exactly.

**M-1 (minor):** "Replace/insert" (merged-output.md:15) is ambiguous; replacing the section text would drop all 12 pinned phrases. Say "append after the existing paragraph" (core/CLAUDE.md ends :53, README.md :237; copies already differ at README :234-235 vs core :51).

**M-2 (minor):** three risk bullets (merged-output.md:29-31) describe the dropped list-then-handle method; remove or rewrite for `--all`.

**M-3 (minor):** guards do not cover repo default tabs; `--all` "stops every terminal process owned by that workspace and durably removes its terminal tabs, layouts, and resume records" (IronOrca src/cli/specs/terminal-close.ts:13). Risk (b) at :33 acknowledges it; add "and the repo has no default tabs".

**M-4 (minor):** project bullet says `(see "Orca session launches")` (merged-output.md:18) but the root CLAUDE.md has no such section; it is in the installed ~/.claude/CLAUDE.md. Name that file.

## Checks that passed
- Syntax: usage `--worktree <selector> --all` (terminal-close.ts:9); handler accepts `--all` with `--worktree`, rejects it only with `--terminal`/`--tab` (src/cli/handlers/terminal-close.ts:49-58); `path:<absolute-path>` is a valid selector (src/cli/format-recovery.test.ts:32); `--setup run|skip|inherit` exists (src/cli/specs/core.ts:71).
- No confirmation prompt: `destructive: true` only filters suggestions (src/cli/command-suggestion.ts:18,66).
- Agent's own shell safe: `path:<new path>` targets only the new worktree.
- Other tests: test_claude_md_routing_block.py checks the level table between markers (:28-32); `test_removed_sections_stay_removed` bans "make sync-dev" (:73) — proposed installed text does not contain it; test_codegraph_guide.py:170-177 bans "serena"/"codegraph_explore" — absent. No test pins the root CLAUDE.md worktree section or example block.
- Copy rules: no plugins/superclaude/**/CLAUDE.md or README.md copy; level-table rule does not apply.
- Constraints: Orca-only creation and no link flags met; /sc:issue and WC-13 (WORKER-CONTRACT.md:62) kept; no `src/superclaude/` path in the installed text.

## Follow-up after the fix
1. `make sync-dev`, `make verify-sync`.
2. `superclaude update` (reinstalls core with force=True, src/superclaude/cli/main.py:365; plain install skips, install_core.py:70-72); note `update` overwrites local edits to ~/.claude/*.md.
3. File the orca_worktree.py issue from ~/.claude/ISSUE-BACKLOG.md.
4. Live V-CLOSE (needs a real create); keep pending until observed.

Not done by reviewer: tests not run; merge-log/debate/refactor-plan not opened.
