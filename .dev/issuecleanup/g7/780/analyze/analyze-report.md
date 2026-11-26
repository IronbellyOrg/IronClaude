# /sc:analyze report: pyproject.toml, focus architecture, depth quick (issue 780)

Codegraph: index_state=fresh, checked_at=2026-11-24T20:49:08Z; degraded: none
(No codegraph lookup was needed: the target is package metadata and Orca's own source, outside the indexed Python symbols.)

Target: `pyproject.toml` (plus `package.json` and `CLAUDE.md`, the other two places the issue names). Read-only run; no source changed.

## Findings

| # | Severity | Finding | Evidence |
|---|---|---|---|
| 1 | Medium | The issue's suspected cause (upstream URLs in package metadata) is not what drives Orca's project id. Orca builds the id from the repo record's stored `upstream` field, which is the GitHub fork parent. | `orca repo list --json`: IronClaude has `"upstream": {"owner":"SuperClaude-Org","repo":"SuperClaude_Framework"}`; `gh repo view IronbellyOrg/IronClaude --json isFork,parent` returns `isFork: true`, parent `SuperClaude-Org/SuperClaude_Framework`. Non-fork repos (Coder, PrivateRepoB, PrivateRepoC) have `"upstream": null`; the fork IronOrca has upstream `stablyai/orca`. |
| 2 | Medium | In Orca's source the stored `upstream` is checked first and wins over `origin`: `getProjectProviderIdentity` (`/home/coder/workspaces/IronOrca/src/shared/project-host-setup-projection.ts:26-61`) returns the upstream identity when owner and repo are set; the origin remote is read only as a last fallback (`:63-72`); the id is `github:<owner>/<repo>` (`:123-125`). | Read live. The IronOrca checkout may differ from the installed Orca 1.4.245-aidev02: UNVERIFIED. |
| 3 | Low | `pyproject.toml:64-67` and `package.json:18,22,25,27` name `SuperClaude-Org` URLs. They are wrong for a fork's own metadata but do not feed the Orca id (no Orca code path reads them in the file read above). | `grep -n` on both files. |
| 4 | Low | `CLAUDE.md:54` still records the wrong id and bans Orca link flags; that ban is the only guard today. | `grep -n` on CLAUDE.md. |
| 5 | Info | `orca repo` offers no verb to change or clear `upstream` (list, add, show, set (worktree visibility), set-base-ref, search-refs). Where Orca stamps `upstream` from GitHub: UNVERIFIED (not traced). | `orca repo --help`. |

## Architecture recommendation

Do not edit `pyproject.toml` or `package.json` to fix the id; that will not change it. The fix belongs in Orca (the IronOrca fork) or in the stored repo record: either make Orca prefer the `origin` remote for the project id when the user's own remote is the fork, or let the owner clear or override `upstream` for this repo. Keep the CLAUDE.md link-flag ban until `orca worktree current --json` shows `github:IronbellyOrg/IronClaude`.

## Roadmap

1. Trace where Orca stamps `repo.upstream` (fork-parent lookup) in the IronOrca source.
2. Owner decides: change Orca (IronOrca issue) or edit the stored record.
3. Re-check `orca worktree current --json`; then update the CLAUDE.md Orca paragraph (issue 769, decision 5).
