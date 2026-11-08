# Codebase enrichment: issue watcher (#331)

- quality_tier: fallback_1 (the Auggie MCP tool is not available in this session; the Augment search tool returned BRANCH_NOT_FOUND for the default branch name; Glob, Grep and Read were used, plus the claim-time analysis report)
- Checked against: origin/master e8db2fe6, 2026-11-07

## Integration points that exist

| Area | Path | Fact |
|---|---|---|
| Command to start | `src/superclaude/commands/issue.md`, `src/superclaude/skills/sc-issue-protocol/refs/claim.md` | Claim takes a bare number or URL, resolves the repo from `origin`, assigns to `gh`'s `@me`, refuses if assigned to someone else, stops at `next-steps.md`, edits marked comments on re-run |
| Launch a session | `src/superclaude/skills/ccsession-tag/README.md` (lines ~228-272), `src/superclaude/core/CLAUDE.md` ("Orca session launches") | `orca agent launch` in an existing worktree with `--surface terminal`; a launch prompt names the session; command must be configured as `ccsession-orca` |
| Not a worker | `src/superclaude/core/WORKER-CONTRACT.md` | `/sc:issue` is on the never-as-worker list |
| Launch governance (design only) | `docs/designs/sc-issue-launch-level-hook.md`, `src/superclaude/hooks/scripts/launch-job-identity.sh` | `--claim --pipeline <level>` is not implemented; only the Bash job-identity hook exists |
| CI | `.github/workflows/test.yml`, `boundary-guard.yml`, `contract3-generator-constraint-lint.yml` | push / pull_request / workflow_dispatch only; no schedule, no issue events |
| Labels | `src/superclaude/skills/sc-issue-protocol/refs/labels.md`, `.github/ISSUE_TEMPLATE/*.yml` | `/sc:issue` never creates labels; only `enhancement` / `bug` are added by templates |

## House patterns a repo-side deliverable should follow

- A Python CLI group is registered in `src/superclaude/cli/main.py` with `main.add_command(<group>, name="<name>")` (existing groups: sprint, roadmap, cleanup-audit, tasklist, cli-portify, prd, eval, swarm, recommend, init-lite, reflect).
- Domain code lives in a package under `src/superclaude/cli/<name>/` or `src/superclaude/<name>/` (for example `src/superclaude/pr_submit/` with `models.py`, `fsm.py`, `run_log.py`, `ci.py`), with tests under `tests/<name>/`.
- CORRECTION (2026-11-07, research alignment check): `src/superclaude/pr_submit/ci.py` is NOT a `gh` subprocess wrapper. It imports only `re`, `.classifier` and `.models` and has no `subprocess` use; no Python file under `src/superclaude` builds a `["gh", ...]` call. The `gh` calls of this repo are issued by skill/command protocols through Bash. The nearest Python subprocess pattern is `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py` (git calls). A poller therefore needs its own small injectable runner around `subprocess.run(["gh", ...])` (mockable in tests); every `gh` call must still pass `--repo IronbellyOrg/IronClaude`.
- Design docs go to `docs/designs/<name>.md` (house format: `docs/designs/sc-issue-command.md`: Status, Issue, Branch, Source of truth, Produced by, then numbered sections).
- Source of truth is `src/superclaude/`; `.claude/` is a gitignored mirror made by `make sync-dev`.

## What does not exist

- No watcher, scheduler, listener, dispatch record, trigger label, approval gate, or GitHub Projects (GraphQL) code.
- No inbound network endpoint of any kind in the package.

## Constraints on a repo-side build

- Nothing may listen on a port, be installed on a real project, or call a real workspace from this task. A poller script/CLI with injectable `gh` and launch functions can be tested fully with mocks.
