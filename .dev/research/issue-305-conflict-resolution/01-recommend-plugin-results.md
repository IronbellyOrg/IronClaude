# Step 1: /sc:recommend --plugin results (issue #305)

Invocation: `/sc:recommend "best Claude Code / community agents or skills for resolving git merge conflicts in a PR workflow" --plugin`
Date: 2026-11-04
Mode: plugin (ecosystem search); `--minstar` omitted, so the default floor of 500 stars applies.
Search delegate: `deep-research` agent (SKILL.md Phase 3, search priority 2; `refs/plugin-ecosystem-sources.md`). Backends: Tavily search/extract (13 discovery queries), WebFetch fallback for some GitHub commit-date API calls. Star counts from `api.github.com/repos/<owner>/<repo>`, fetched 2026-11-04.

## Delegated search prompt

Find the best Claude Code plugins, skills and subagents that resolve git merge conflicts, ideally in a pull-request workflow (rebase/merge conflicts on a PR branch, lockfile/generated-file conflicts, semantic conflicts). Scope: Claude Code plugin marketplaces (claude-plugins-official and others), community skill repos (anthropics/skills, obra/superpowers, sammcj/agentic-tools, wshobson/agents, VoltAgent and awesome-claude-code lists) and standalone GitHub repos. Raw MCP servers out of scope. Per candidate: name, repo URL and file path, capability summary, install command as given, own-repo stars with source URL, last commit date, depth of conflict-resolution content with a quote, caveats, citations. Rank by depth and quality of conflict-resolution guidance.

## Ranked results

**Star floor:** No candidate met the >= 500 star floor; showing unranked credible matches below. Lower the floor with `--minstar <smaller>`. (The highly starred collections, VoltAgent 26,328 and mattpocock/skills 231,171 as parents, are either tangential or the skill was removed; their stars are not attributable to a conflict skill.)

**Bonus: not ranked by GitHub stars, ordered by depth of conflict-resolution guidance**

| Rank | Candidate | Source (file) | Own stars | Depth |
|---|---|---|---|---|
| 1 | git-conflict-resolver (Raudbjorn/conflict-of-interest) | https://github.com/Raudbjorn/conflict-of-interest (`SKILL.md`, `constitution.md`, `references/`, `scripts/`) | 0 | Full layered procedure: mergiraf, then deterministic per-category handling (9 categories, 16 lockfile types), intent statement per side, validation, semantic audit; halts when intent cannot be inferred |
| 2 | resolve-conflicts (haacked/dotfiles) | https://github.com/haacked/dotfiles/tree/main/ai/skills/resolve-conflicts | nested (parent 133) | Full procedure: diff3 markers, lockfile take-and-regenerate, migrations always ask, mergiraf pass, stacked-PR duplicate detection by similarity |
| 3 | git-merge-conflicts (Spardutti/claude-skills) | https://github.com/Spardutti/claude-skills/blob/main/skills/git-merge-conflicts/SKILL.md | 3 (nested in own collection) | Full procedure: resolve by intent against merge base, zdiff3, index stages, rebase ours/theirs inversion, unmarked semantic conflicts, migration chains |
| 4 | merge-conflicts (event4u-app/agent-config) | https://github.com/event4u-app/agent-config/blob/main/dist/agent-src/skills/merge-conflicts/SKILL.md | 18 (nested) | Full procedure: generated / remeasured / authored classes, written plan before edits, resolution log |
| 5 | merge (jsifalda/ai-project-rules) | https://github.com/jsifalda/ai-project-rules/blob/main/skills/merge/SKILL.md | 5 (nested) | Full PR-branch workflow: merge never rebase, no stash, no force-push, worktree-safe preflight, lockfile-only regeneration, stop-and-resume on product decisions |
| 6 | pr-babysitter (mblode/agent-skills) | https://github.com/mblode/agent-skills/blob/main/skills/pr-babysitter/references/merge-conflicts.md | 181 (nested) | PR-level: reads `mergeStateStatus`, auto-resolves only lockfiles/generated/changelogs, aborts and reports source/migration/API conflicts |
| 7 | git-merge-conflicts (kapicic) | https://github.com/kapicic/git-merge-conflict-skill | 0 | Five phases, safe / needs-context / ask-user triage |
| 8 | conflict-resolution (troykelly/claude-skills) | https://github.com/troykelly/claude-skills/blob/main/skills/conflict-resolution/SKILL.md | 12 (nested) | Generic five-step loop plus PR comment template |
| 9 | resolving-merge-conflicts (mattpocock/skills, removed) | https://github.com/mattpocock/skills/blob/main/docs/engineering/resolving-merge-conflicts.md | nested | Five lines of strong principles; archived |
| 10 | rebase command (webuild-ai/claude-toolkit) | https://github.com/webuild-ai/claude-toolkit/blob/main/commands/rebase.md | 8 (nested) | Per-file ask-user; whole-file ours/theirs; force-with-lease |
| 11-16 | raine.dev `/rebase`, olshansky resolver, motlin `git:conflicts`, CuriousLearner `conflict-resolver`, pponali `/resolve-conflicts` (anti-pattern), mcpmarket `git-conflict-resolver-2` | blog posts / listings | 0-29 or n/a | Short or heuristic-only |
| Tangential | VoltAgent `git-workflow-manager`, petry-projects `claude-rebase` CI job, TheVoskamps issue #29, wshobson/agents, claude-plugins-official | n/a | n/a | Conflicts mentioned once or nothing found |

Install commands (as given by the sources, not tested):
- Raudbjorn: `make install` (README)
- haacked: copy the folder into `~/.claude/skills/resolve-conflicts/` (https://haacked.com/archive/2026/03/25/resolve-merge-conflicts)
- Spardutti: `npx @spardutti/claude-skills`
- jsifalda: install instructions unclear from README for a single skill; check repo directly
- mblode: `npx skills add mblode/agent-skills -g --agent codex claude-code -y`

## Top 3 picked for /sc:analyze, with reasons

1. **Raudbjorn/conflict-of-interest `git-conflict-resolver`**: deepest guidance found, and its layered structure (cheap deterministic passes first, intent analysis and halts only for hard conflicts) is exactly the "layer complexity as conflict complexity rises" shape the issue asks for.
2. **Spardutti/claude-skills `git-merge-conflicts`**: the strongest intent-based resolution rules (merge base, index stages, the rebase ours/theirs inversion, conflicts git does not mark), which cover the semantic tier the others treat thinly.
3. **jsifalda/ai-project-rules `merge`**: the only full procedure built for an open PR branch with the same safety rules sc:pr-submit already has (merge never rebase, never force-push, never stash because worktrees share one stash stack, worktree-safe preflight); it answers how to publish a resolution without force-pushing.

Not picked: haacked `resolve-conflicts` (rank 2) because Raudbjorn closely mirrors its structure (categories, diff3, lockfile regeneration) and adds more, so analyzing both would mostly duplicate items; event4u (rank 4) and mblode (rank 6) contribute single ideas (the "remeasured" file class; reading `mergeStateStatus`), noted here for the design step rather than analyzed in full.

## Return contract

| Field | Value |
|---|---|
| status | plugin_search |
| mode | plugin |
| recommendation_kind | plugin_candidate |
| prompt_block | (delegated search prompt above) |
| verified_sources | `~/.claude/skills/sc-recommend/SKILL.md`, `~/.claude/skills/sc-recommend/refs/plugin-ecosystem-sources.md`, candidate SKILL.md/README files fetched by the delegate (URLs above) |
| auggie_status | skipped (plugin mode; local surface not enumerated) |
| degradation_notes | No candidate met the 500-star floor; all results are in the unranked bonus tier. Delegate fell back to WebFetch for some commit-date lookups. Install commands not tested. |
| guide_status | not_applicable |
| routing_row_id | (empty) |
