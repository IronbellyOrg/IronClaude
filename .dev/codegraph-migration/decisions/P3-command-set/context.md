# Decision context: which new codegraph commands Phase 3 adds (task P3, issue #323)

Question: which 2-3 new `/sc:` commands (or skills) built around codegraph should Phase 3 add, so that other skills can call them and users can run them standalone?

## Facts every option must respect

- codegraph v1.6.2 exposes 8 read-only MCP tools (`codegraph_explore`, `_search`, `_callers`, `_callees`, `_impact`, `_node`, `_files`, `_status`) and CLI verbs (`init`, `index`, `sync`, `status`, `query`, `explore`, `context`, `callers`, `callees`, `impact`, `affected [--stdin --json]`). Source: `.dev/codegraph-migration/research/codegraph-evaluation.md` §3.
- Gaps: no text search, no diagnostics, no type hierarchy, no edits, no memory; caller rows give the caller's definition line, not the call site; `affected` maps changed files to test files only (§5.5, §6).
- The index is per worktree; a new worktree is "not initialized" until `codegraph init --yes` (about 4.5 s for 500 files) (§4, §5.8).
- `codegraph_explore` answers can be large (24,913 characters in one sample) and pull in unrelated symbols (§5.6).
- Existing callable-skill convention: a thin `src/superclaude/commands/<name>.md` that says "invoke Skill sc:<name>-protocol"; callers pass `--caller <name>` and `--output-dir <path>`; machine result is `<output-dir>/return-contract.yaml` with `status: success|partial|blocked|failed` and absolute paths (see `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` Wave 5 step 4.5).
- Candidate callers: sc-implement-protocol (before each task's edit), sc-task-protocol STANDARD/STRICT impact step, sc-workflow-protocol (plan's touched files), sc-pr-submit-protocol and sc-auggie-review-protocol (review scope), sc-troubleshoot-protocol Tier 1, sc-reflect-protocol UC-2, sc-tasklist-protocol, `/sc:index-repo`, `/sc:explain`, `/sc:load`, sc-brainstorm-protocol codebase enrichment.
- Repo rules: smallest correct change, no speculative features (`~/.claude/CLAUDE.md` rule 7, ladder rung 1); new commands need a file-list update in `tests/unit/test_cli_install.py`, content tests, and plugin twins only where the plugin ships that command.
- Brainstorm output: `.dev/codegraph-migration/brainstorm/P3-codegraph-opportunities/` (ranked ideas and candidate commands).

## Evaluation criteria

1. Value to the callers above (how many call it, what it saves).
2. Token cost per call compared with the caller doing the same work inline.
3. Interface simplicity for callers (one obvious way to call; stable return contract).
4. Failure behaviour when codegraph or the index is missing (callers must keep working).
5. Implementation and test effort; maintenance surface (files, tests, docs).
6. Overlap with existing commands (`/sc:index-repo`, `/sc:test`, `/sc:explain`).
