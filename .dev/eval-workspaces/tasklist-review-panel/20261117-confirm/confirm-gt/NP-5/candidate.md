---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-analyzeCodegraph-20261111-193557
version: "1"
priority: Medium
created_date: "2026-11-11"
---

# Add conditional codegraph support to /sc:analyze

Source: ./source.md
Goal: `src/superclaude/commands/analyze.md` runs one codegraph readiness check per run and uses the codegraph lookup tools above the Glob/Grep/Read floor in Discover, Scan and Evaluate only when the index is fresh; in every other state it continues on Glob/Grep/Read, records a `graph:*` note and never halts.

## Constraints

- Edit only `src/superclaude/commands/analyze.md`; a test that pins that file may change only if one must. Do not create a skill for `/sc:analyze`.
- Do not edit `src/superclaude/core/CODEGRAPH.md`, any other command, skill or agent, or anything under `.claude/`; `.claude/` is gitignored sync output and is never staged.
- Keep every existing flag, behaviour, the Unattended mode section and every Boundary (Will, Will Not, Output, Next Step) of the command as written.
- Name the guide by its installed path `~/.claude/CODEGRAPH.md`; add no instruction that reads a `src/superclaude/...` path.
- No commit, no push, no PR. Leave staging and committing to the coordinator.

## Phase 1: Declare and gate codegraph in analyze.md

## Task 1: Declare the codegraph server and add the Codegraph rules section

In `src/superclaude/commands/analyze.md` change the frontmatter line `mcp-servers: []` to `mcp-servers: [codegraph]` (the way `src/superclaude/commands/reflect.md` declares it; add no `allowed-tools`). In `## Tool Coordination` keep the five existing bullets and add one **codegraph** bullet naming `mcp__codegraph__codegraph_status` (once) and `_search`, `_node`, `_callers`, `_callees`, `_impact`, `_files`, used only when `index_state: fresh` and always before the matching Glob/Grep/Read step, which stays the floor. Add a `## Codegraph (optional)` section between `## Key Patterns` and `## Examples` (source section 2.4), under about 25 lines, that states: the one readiness check per run follows section 2 of `~/.claude/CODEGRAPH.md`; codegraph is used only when `index_state: fresh`, otherwise Glob/Grep/Read with the matching `graph:*` token added to the report's Codegraph line, never halting and never asking; graph rows are leads, never citations (re-Read a `file:line` before citing, an empty result is not a "no callers" finding, confirm a call site per the guide's standing rules, a short caller list is `graph:truncated`); codegraph stays read-only (never `codegraph init`, `index`, `sync`, `explore` or `context`); exact tool names `mcp__codegraph__codegraph_<tool>` with `projectPath` set to `worktree_root`; any subagent brief carries `index_state`, `checked_at` and `worktree_root`, and the subagent calls codegraph only when `index_state: fresh`.

Acceptance criteria:
- The frontmatter of `src/superclaude/commands/analyze.md` contains `mcp-servers: [codegraph]` and no `allowed-tools` key.
- `grep -n 'index_state: fresh' src/superclaude/commands/analyze.md` matches in Tool Coordination and in the new Codegraph section, and the section names `graph:*`, `never halt` (or equivalent wording), `~/.claude/CODEGRAPH.md` and the read-only ban on `codegraph init`, `index`, `sync`, `explore` and `context`.
- `grep -n 'src/superclaude' src/superclaude/commands/analyze.md` prints no line that tells an agent to read a `src/superclaude/...` path.

## Task 2: Wire the readiness check and per-step codegraph use into the Behavioral Flow

Depends on: Task 1

In `## Behavioral Flow` of `src/superclaude/commands/analyze.md` keep the five numbered steps and their wording, and add the source section 2.2 text: one lead-in line before step 1 that runs the readiness check of `~/.claude/CODEGRAPH.md` section 2 exactly once per run, before Discover, keeping `index_state`, `checked_at` and `worktree_root` for the whole run with no repeat; in step 1 (Discover) `codegraph_files {format:"grouped", maxDepth:2}` and `codegraph_search` before the existing language detection; in step 2 (Scan) `codegraph_node` (symbol body with `includeCode:true`, file outline with `symbolsOnly:true`), `codegraph_callers` and `codegraph_callees` before the existing pattern matching; in step 3 (Evaluate) `codegraph_impact` and `codegraph_callers` as dependency and blast-radius evidence for architecture and quality findings (dead-code candidates as leads only). Each clause says "when `index_state: fresh`" and leaves the Glob/Grep/Read step in place. Steps 4 and 5 stay unchanged except that the report gains one line: `Codegraph: index_state=<state>, checked_at=<UTC>; degraded: <graph:* tokens or none>`.

Acceptance criteria:
- `src/superclaude/commands/analyze.md` contains exactly one readiness-check instruction, placed before step 1, and the Discover, Scan and Evaluate steps each name the codegraph tools they use and state they apply only when `index_state: fresh`.
- The five step names (Discover, Scan, Evaluate, Recommend, Report), the usage flags, `## Unattended mode` and `## Boundaries` are byte-identical to `git show HEAD:src/superclaude/commands/analyze.md` apart from the intended additions (check with `git diff` on that file).
- The report description includes the `Codegraph: index_state=..., checked_at=...; degraded: ...` line, and a missing or stale graph is stated to leave the run succeeded (report written).

## Phase 2: Sync the dev copy

## Task 3: Sync the dev copy and run the tests that cover command files

Depends on: Task 2

Run `make sync-dev` then `make verify-sync` in the repository root so `.claude/commands/sc/analyze.md` matches `src/superclaude/commands/analyze.md`. If `verify-sync` names files this plan does not own, run `make sync-dev` once more and re-check; never edit those files. Find the tests that cover command files or their install (`grep -rn 'commands' tests` for tests touching `src/superclaude/commands`, including `tests/unit/test_cli_install.py`) and run them with `uv run pytest <those paths>`. Do not stage anything under `.claude/`.

Acceptance criteria:
- `make sync-dev` and `make verify-sync` exit 0, or any remaining `verify-sync` output names only files owned by other sessions.
- The `uv run pytest` run over the tests that cover command files and their install passes; any failure not caused by `src/superclaude/commands/analyze.md` is reported as such and left unfixed.
- `git status --short` shows no staged path under `.claude/`.
