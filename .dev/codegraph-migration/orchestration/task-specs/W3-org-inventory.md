Task W3: IronbellyOrg-wide inventory of codebase-memory and Serena references (read-only).

First read /home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init/.dev/codegraph-migration/orchestration/README.md (shared rules; binding).

Target: every repository in the IronbellyOrg GitHub organization other than IronClaude.

Change: write `.dev/codegraph-migration/inventory/org-repos.md` with:
1. The list of org repos (`gh repo list IronbellyOrg --limit 200 --json name,isArchived,isFork,defaultBranchRef`).
2. For each of these search terms run `gh search code '<term> org:IronbellyOrg' --limit 100 --json repository,path` : codebase-memory, codebase_memory, DeusData, serena, mcp__serena, serena-agent. Note GitHub code search only indexes default branches and may cap results; record that limitation.
3. For each non-IronClaude repo with hits: a table of path, term, kind (live config / Dockerfile or installer / CI / test / doc / historical .dev or claudedocs artifact). Historical `.dev/`, `claudedocs/` and archived-task artifacts are listed separately as "keep (historical)".
4. For each repo with live (non-historical) hits: a one-paragraph scope estimate of what removal there would need, and which repo owns it. Do NOT investigate implementation details beyond what the hit lines show.
5. `## Decisions` section.

Constraints: strictly read-only (gh search/view/api GET only). No issues, PRs, comments or clones that write anywhere except /tmp.

Ownership: write only `.dev/codegraph-migration/inventory/org-repos.md`.

Observable acceptance: file exists with the exact gh commands used, per-term hit counts, and a per-repo live-versus-historical table.
