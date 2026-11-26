# Findings: issue 769 "[FEATURE] Trim Startup token costs"

Checked 2026-11-24 against worktree HEAD a7ae3dd30 (branch ironbelly/Issuecleanup) and the live issue (OPEN, label enhancement, created 2026-11-24T18:20:09Z, 6 comments recording owner decisions 1 to 7 and 5b; decisions 8 to 12 still open).

## Verdict

**still-relevant** (planned, owner-approved in part, nothing implemented yet).

Evidence of current state (all read from this checkout):
- Tests do not exist: `tests/agents/test_agent_frontmatter_policy.py`, `tests/core/test_project_claude_md_absolute_rules.py`, `tests/skills/test_listing_invocability.py` are all missing. `tests/agents/` holds only test_codegraph_rosters.py, test_tavily_tool_parity.py, test_workflow_reviser_readonly.py.
- `memory: project` is still on line 4 of 8 rf agents in `src/superclaude/agents/` (rf-analyst, rf-assembler, rf-qa-qualitative, rf-qa, rf-task-builder, rf-task-executor, rf-task-researcher, rf-team-lead). The issue deletes it on six and keeps rf-task-builder and rf-task-researcher.
- No agent file has `disallowedTools` or `omitClaudeMd`. 20 agent files have no `tools:` line (README.md also lacks one but is not an agent).
- Project `CLAUDE.md` is still 27,339 bytes (wc -c); no trimming and no archive section yet.
- `.claude/settings.json` has only a `hooks` key: no `skillListingBudgetFraction` or `enableArtifact`.
- `src/superclaude/hooks/scripts/freshness-subagent-start.sh` has no `agent_type` handling; it always prints the Bash policy copy (about lines 29 to 34).
- No PR references this issue (searches for 769, disallowedTools, omitClaudeMd, skillListingBudgetFraction, startup found nothing related; #768 and #778 are unrelated Playwright fixes).
- Owner decisions in the comments supersede the issue body where they differ: (1, 2) Artifacts off approved in principle after a live test, settings go in the user file `~/.claude/settings.json`, which covers BOTH `enableArtifact` and `skillListingBudgetFraction`; (7) the installer (`superclaude install`) writes those keys, merging without overwriting other settings, shipped through the Coder template; (3) `omitClaudeMd` on 10 read-only reviewers only after paired before/after tests (130 runs); (4) one combined frontmatter PR in a fixed order; (5) the `integration` branch workflow stays and the project id paragraph is rewritten to `github:IronbellyOrg/IronClaude`; (5b) rebase `integration` on master then switch the PR rule and `/sc:pr-submit` base to `integration` (replay conflicts in 3 files; branch unchanged at 141e97fec, per the owner comment); (6) the 46 BMad skills get `skillOverrides` "name-only", written by the installer.
- The measured token figures (26.3 percent start-up share, 2.4 and 3.6 percent savings) come from transcripts in the Coordinator checkout and were not re-measured: UNVERIFIED.
- `/sc:analyze` on `src/superclaude/agents` (`.dev/issuecleanup/g7/769/analyze/analyze-report.md`) confirmed the same repository facts.

## Complexity and size

Complexity: **complex**. Size: **XL**. Reason: at least 7 pull requests (tests, frontmatter, two CLAUDE.md stages, hook and core file, installer settings including the BMad override, gated reviewer changes) plus live tests and a 130-run paired comparison, across agents, project CLAUDE.md, a hook, the installer and the plugin mirror.

## Priority

**P2**. Reason: a measured but modest saving (about 2.4 percent of the bill for the safe set), no data loss or broken gate, and it blocks nothing; the issue itself says Medium.

## Concrete next steps

1. PR 1: add the two new test files (frontmatter policy table test and project CLAUDE.md rule hashes); confirm the four existing agent-roster tests pass.
2. PR 2 (combined frontmatter, per decision 4): delete `memory: project` on six rf agents; add one merged `disallowedTools` line (Artifact trio first) on the 20 no-tools agents; mirror in `plugins/superclaude/agents/`; `make sync-dev`, `make verify-sync`. `Skill` only after its live first-request check. `omitClaudeMd` lines join only for agents whose pair already passed.
3. PR 3 and 4: trim project `CLAUDE.md` in two stages, archiving stage 1 text verbatim in `docs/developer-guide/technical-architecture.md`. Stage 1 must NOT delete the `integration` workflow section and must rewrite the Orca project-id paragraph to `github:IronbellyOrg/IronClaude` while keeping the ban on Orca link flags (decision 5). Follow-up: one agreed wording for the Git Workflow section and the PR rule.
4. PR 5: `agent_type` hook change with tests, plus the codegraph paragraph trim in `src/superclaude/core/CLAUDE.md`.
5. Installer PR (decisions 2, 6, 7): `superclaude install` merges `skillListingBudgetFraction` (after the disposable-session pilot passes), `enableArtifact:false` (after its live test) and `skillOverrides` "name-only" for the 46 BMad skills into `~/.claude/settings.json` without overwriting other keys, with a merge-safe write test. Open: whether it replaces a user-set value and whether there is an opt-out. The issue body's "tracked `.claude/settings.json`" placement is superseded.
6. Gated, each on an owner "yes": `omitClaudeMd` per agent after its paired test, rf allowlist narrowing. Resolve open decisions 8 to 12 first.
7. Re-run the measurement scripts after release and compare to the baseline.

## Dependencies

- Needs: owner decisions 8 to 12 (open, recorded in this issue); live tests for the gated keys; the `integration` rebase (decision 5b, not done, conflicts in 3 files) must be settled before it is known whether these PRs target `integration` or master.
- Blocks: nothing found.

## Related issues

- #757 (OPEN, run the coordinator sweep outside the session; source of the measurements).
- #766 (OPEN, read workers show as "could not determine"; no code overlap).
- #767 (OPEN, coordinator compacts too often; adjacent token cost).
- #575 and #580 (CLOSED, Bash-output pruner evaluation).

## Related PRs

- None open or merged for this work. Planned: at least seven PRs through `/sc:pr-submit --monitor 3`; base is master today, but decision 5b would change it to `integration` once that branch is rebased. #768 and #778 appeared in searches but are unrelated.
