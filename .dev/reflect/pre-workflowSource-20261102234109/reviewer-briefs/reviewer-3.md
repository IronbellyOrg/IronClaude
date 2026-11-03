# Reviewer 3 brief: persona refactorer (UC-1 pre, read-only)

Audit the plan `.dev/tasks/to-do/TASK-WF-workflowSource-20261102-233731/TASK-WF-workflowSource-20261102-233731.md` against its spec `.dev/tasks/to-do/TASK-WF-workflowSource-20261102-233731/source.md` and the itemized source `.dev/releases/current/v5.0.0/post-release/CONSOLIDATED-PLAN.md`. Read-only: use Read/Grep/Glob only. Return findings; each finding cites file:line or is tagged [INFERRED]; classify each divergence as Authorized expansion / Necessary deviation / Drift / Regression, and evidence-insufficient items as Grounding Gap.

## T1 card excerpt

### Structural / sequencing (refactorer slice)

- S1 [grounded: coverage-summary.yaml:20] Three link sub-items in CONSOLIDATED-PLAN are not named in task bodies: A-W22 links to `docs/user-guide/codegraph.md` from `commands.md` and `mcp-servers.md` (Task 17 names README and mcp-installation only); B-W22 pointer in `docs/developer-guide/git-standards-protocols.md` (no task touches that file); B-W12 links from `docs/developer-guide/README.md` to the four new notes, while Task 37 (B-W12) runs before Tasks 43-46 create them and has no dependency on them.
- S2 [grounded: plan Constraints bullet on installed primitives] S_domains = 3 (code, docs, tests): Tasks 6 and 26 edit installed primitives under `src/superclaude/` and require `make sync-dev` / `make verify-sync`; this is the only code-domain blast radius.


## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-02T23:41:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/post-release-v5.0.0 projectPath=/home/coder/workspaces/worktrees/IronClaude/post-release-v5.0.0

### .dev/tasks/to-do/TASK-WF-workflowSource-20261102-233731/TASK-WF-workflowSource-20261102-233731.md:13-30 (Constraints)

```markdown

Source: ./source.md
Goal: every in-scope gap (1-70) of `.dev/releases/current/v5.0.0/post-release/CONSOLIDATED-PLAN.md` is fixed in the named file, the seven new docs exist, and the 16 user and 2 sysop human-test guides plus their index exist under `docs/testing/v5.0.0/`, each statement traceable to the v5.0.0 code (tag v5.0.0 = d953b983).

## Constraints

- The item text for every task lives in `.dev/releases/current/v5.0.0/post-release/CONSOLIDATED-PLAN.md`: section "Writer worklist" (items A-W1 to A-W22, B-W1 to B-W22, C-W1 to C-W3, each with doc line, corrected statement and code evidence), section "Gap list" (gap numbers), and section "Test guide plan (D and E)". Read the named item before editing. Scan inventories with the detailed code evidence are in `.dev/releases/current/v5.0.0/post-release/scan/` (A1-core-user-docs.md, A2-feature-user-docs.md, B-technical-docs.md, C-install-surface.md, DE1-cli-surface.md, DE2-claude-surface.md).
- Line numbers in the plan are from d953b983. Read the target file first and match on the quoted text, not the number.
- Every new or corrected claim must agree with the code or `--help` output (`uv run superclaude <cmd> --help` from the repo root). If a planned correction turns out wrong when checked against code, do not write it: record the item, the planned text and the code evidence in `./artifacts/deviations.md` and write the code-true statement instead.
- Ground facts (verified): version 5.0.0 (`pyproject.toml:7`); new-user install `pipx install git+https://github.com/IronbellyOrg/IronClaude` then `superclaude install`; upgrade `pipx install --force git+https://github.com/IronbellyOrg/IronClaude` then `superclaude install --force` then restart Claude sessions; `superclaude install` options are only `--target`, `--force`, `--list`; there is no `python -m superclaude` / `python3 -m SuperClaude`; 45 commands, 45 agents, 38 skill folders, 11 core files; issues go to `https://github.com/IronbellyOrg/IronClaude/issues`.
- Do not edit `docs/releases/v5.0.0.md` or `CHANGELOG.md` (published record). Do not change code (`src/superclaude/cli/**`, hooks, scripts): code findings O1-O22 are out of scope. Deferred gaps 71-84 are out of scope.
- `src/superclaude/core/HOW-WE-WORK.md` and `src/superclaude/rules/core/changelog_maintenance.md` are installed primitives: after editing them run `make sync-dev` then `make verify-sync`; never stage `.claude/` (only `.claude/settings.json` is tracked); never add `src/superclaude/...` paths inside installed primitives.
- Every `gh` command written into a doc uses `--repo IronbellyOrg/IronClaude`. No link or instruction points users at SuperClaude-Org/SuperClaude_Framework as the place to install or file issues.
- Test guides are documents a human runs by hand, built from the templates `~/.claude/skills/sc-post-release-protocol/templates/user-test-guide.md` (D) and `~/.claude/skills/sc-post-release-protocol/templates/sysop-test-guide.md` (E): Read the template first, keep its structure (Preconditions, What you're verifying, Steps with Do / Expected result / Pass-Fail, Edge cases or Negative check, Cleanup, Overall result), remove its HTML comment. Every expected result cites code file:line, `--help` output or a line range of `docs/testing/v5.0.0/c-e2e-transcript.txt`; a result that cannot be derived is written as UNVERIFIED with the reason. Every step carries one cost tag: `[FREE]`, `[LOCAL-WRITE]`, `[CLAUDE-SESSION]`, `[API-LONG]`, `[PROXY]` or `[EXTERNAL]`. Any step that writes files does so in a throwaway `HOME` or `/tmp` path, never the tester's real `~/.claude`.
- Markdown check for every created or edited `.md` file: `npx --yes markdownlint-cli@0.38.0 -c .markdownlint.json <file>` exits 0 (pre-existing violations on untouched lines of an updated file may be recorded in `./artifacts/deviations.md` instead of fixed).
- Do not run installs against the real `~/.claude`, the real pipx environment or running ccsession shims. Commit nothing; the post-release orchestrator commits and opens the PR.

## Phase 1: Install and upgrade docs agree with the e2e-proven path (Workstream C)
```
### .dev/reflect/pre-workflowSource-20261102234109/artifacts/coverage-matrix.md

(Read this file; it carries the INF rows, item-to-task map and target-existence checks.)

## Coverage slice

| Requirement | Tasks | Status |
|---|---|---|
| Task ordering and dependencies | Depends on lines | Task 37 vs 43-46 ordering gap |
| Installed-primitive edits + sync | 6, 26 | carried |
