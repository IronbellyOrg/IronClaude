# Agent architecture analysis

## Scope and method

Command: `/sc:analyze src/superclaude/agents --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g3/572/analyze`.

Read-only, quick architecture assessment of canonical agent definitions, with targeted checks of retained callers, installation inventory, release records and live issue #572. This triages the issue; it does not execute the full per-agent disposition exercise. No source, install, GitHub object or git index was changed. The brief guard passed: the installed analyze command has an Unattended mode section and the project command copy does not exist.

The graph is fresh but excludes Markdown: its target listing contains only `__init__.py`, which has no symbols. Agent definitions and prose callers were therefore checked with Glob, Grep and Read rather than graph call edges.

## Findings

1. **Medium: the historical blocker is cleared, but the evaluation was deliberately deferred.** The Part B dependency map exists at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/cleanup/bundle/dependency-map.md:158-168`; its agent decision retains all eight pending #572. The actual bundle removal merged in #656 (`a3edd84db5f4dfe8351b49ddd769f0e7ebe08ee6`) and the corrected release merged in #664 (`64dfc0e8622281a56d6c4e6826c63d50c6959da8`). `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/releases/v6.1.0.md:135-152` says no agent was removed and assigns leftover task-flow text to this issue. The older claim that the work must still wait for the map/removals is no longer current.
2. **Medium: retained agent instructions still assume the retired task-file route.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/agents/rf-task-executor.md:6-7` preloads `rf:task`, and `:150-168` tells the agent to execute a `.gfdoc` script. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/agents/rf-team-lead.md:38-48` describes the same builder/executor team. Glob found none of the nine removed skill entry points under canonical skills, and no `automated_qa_workflow.sh` under canonical source. This is a stale dependency, not proof that an independently installed PrivateRepoA project cannot provide that script. No runtime failure was tested.
3. **Medium: removing all rf agents would break retained review instructions.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-reflect-protocol/SKILL.md:614-627` still assigns `rf-qa` and `rf-qa-qualitative` review work. The recursive canonical-skills search (including `refs/`) found three rf-agent mentions, all in that skill. Agent-to-agent, template and test references also survive: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/unit/test_cli_install.py:53-66` pins the eight rf agents. A removed skill's old caller table is not a valid current removal map.
4. **Medium: the baseline inventory has grown.** Tracked source contains 49 agent definition Markdown files, plus README and `__init__.py`, rather than the issue's 48. The addition is `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/agents/workflow-reviser.md:1-24`, introduced by merged #705 (`1a6c8723fe9e6caa85bfffcdb97b2dc434978bf9`). Its read/edit-only tool grant and untrusted-report handling are part of its documented safety purpose and must be preserved in any later consolidation; runtime isolation was not exercised here.
5. **Note: the agent README's ownership guidance is stale.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/agents/README.md:5-21` lists three agents and says to edit the plugin copy first; the repository's governing instructions instead make canonical source authoritative. Do not use that README as the complete inventory or as editing authority.

## Metrics and limits

- Inventory: 49 canonical agent definition Markdown files (50 Markdown files minus README), including eight `rf-*`, five audit, three eval, three issue, seven original review/debug helpers, two adversarial, one business panel, two research, one PM, sixteen general specialists and the added workflow reviser. Count cross-checked with Glob and `git ls-files src/superclaude/agents`.
- No source changes, tests, builds, install runs, dependency installs, transcript analysis or agent execution. All behavior and security effectiveness at runtime remain UNVERIFIED.
- Live #572 contains the 2026-11-18 usage study and provisional recommendations for all eight rf agents. Its raw `.dev/research/agent-usage-572/` evidence was not found in this checkout, so the usage counts, cross-project rules and removal-candidate judgments are UNVERIFIED here, not re-measured facts.
- GitHub lookups used only issue view and PR list/view on IronbellyOrg/IronClaude. Numeric PR search includes irrelevant matches; no absence-of-PR proof is inferred. Open PR search for `agent` returned only #756, not an identified #572 implementation. Full GitHub dependency/timeline metadata is UNVERIFIED under this allowlist.
- Canonical source was checked; installed copies and plugin parity were not exhaustively checked. The project analyze-command copy is absent. No command or install was run to repair it.

## Recommendations

Keep #572 open as research in progress. Refresh its inventory and waiting note to the post-6.1.0 state, map every current agent to surviving users including skill `refs/`, and record one keep/refactor/simplify/remove decision with evidence per current definition. Treat the two low-use candidates as hypotheses, not approved deletions. Preserve the retained QA roles and restricted reviser permissions. Address #393 when evaluating the retry adviser, and retain the eval-agents decision gate unless the owner explicitly changes it. Any later removal needs its own authorized plan, reference/test updates and installer-retirement verification; this triage authorizes none of those writes.

## Grounding

Codegraph: index_state=fresh, checked_at=2026-11-24T13:17:57Z; degraded: graph:empty

Access: mcp. Worktree root: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup`. The empty-symbol result for `agents/__init__.py` and Markdown exclusion required native file/text checks; no graph initialization, synchronization or other mutation ran. Live reads included #572 and its two comments, #571's body and latest release follow-ups, #647's decisions and completion, #393's follow-ups, #536, #573 and the directly relevant PRs recorded in findings. PR #658 was verified as superseded by #662 and #664 rather than treated as the final release.
