# sequential-thinking MCP removal (agent 1 of 4)

Stop documenting/shipping Sequential MCP in **owned** command/skill/agent files. SoT: `src/superclaude/`. Smallest diff. No commit. Never `git add .claude/`. Do not touch `.dev/worktrees/` or `.venv/`.

Retarget: keep multi-step reasoning as a concept; drop MCP name; use native Claude reasoning (already the fallback). Leave generic English "sequential" (ordering) alone.

Not this agent: files that also mention magic or chrome-devtools (`help.md`, `task.md`, `workflow.md`, `pm.md`); CLI installer/registry; MCP configs; `MCP.md`; `FLAGS.md`; CLAUDE.md MCP Servers table; docs/user-guide; gateway; `tests/cli/test_install_mcp_registry.py`.

## T1 — Commands: drop Sequential MCP

Remove `sequential` from `mcp-servers`. Delete Sequential MCP / `sequentialthinking` bullets. Where the concept remains, say native reasoning.

- [ ] `src/superclaude/commands/cli-eval.md`
- [ ] `src/superclaude/commands/validate-roadmap.md`
- [ ] `src/superclaude/commands/improve.md`
- [ ] `src/superclaude/commands/validate-tests.md` (only server was sequential — drop field or leave empty list)
- [ ] `src/superclaude/commands/brainstorm.md`
- [ ] `src/superclaude/commands/post-release.md`
- [ ] `src/superclaude/commands/auggie-review.md`
- [ ] `src/superclaude/commands/cleanup.md`
- [ ] `src/superclaude/commands/review-translation.md`
- [ ] `src/superclaude/commands/tasklist.md`
- [ ] `src/superclaude/commands/spec-panel.md`
- [ ] `src/superclaude/commands/tdd.md`
- [ ] `src/superclaude/commands/research.md`
- [ ] `src/superclaude/commands/cli-portify.md`
- [ ] `src/superclaude/commands/explain.md`
- [ ] `src/superclaude/commands/troubleshoot.md`
- [ ] `src/superclaude/commands/adversarial.md`
- [ ] `src/superclaude/commands/pr-submit.md`
- [ ] `src/superclaude/commands/release-split.md`
- [ ] `src/superclaude/commands/cleanup-audit.md`
- [ ] `src/superclaude/commands/reflect.md`
- [ ] `src/superclaude/commands/swarm-wizard.md` (only server was sequential)
- [ ] `src/superclaude/commands/index.md`

## T2 — Skills: drop Sequential MCP

Drop `sequential` from `mcp-servers` / `allowed-tools` (`mcp__sequential-thinking__*`). Drop Sequential MCP body. Retarget `mcp_integration.sequential` to native reasoning.

- [ ] `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
- [ ] `src/superclaude/skills/sc-reflect-protocol/SKILL.md`
- [ ] `src/superclaude/skills/sc-swarm-wizard-protocol/SKILL.md`
- [ ] `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (incl. MCP table row `sequential`)
- [ ] `src/superclaude/skills/sc-cli-eval-protocol/SKILL.md`
- [ ] `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md`
- [ ] `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md`
- [ ] `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`
- [ ] `src/superclaude/skills/sc-adversarial-protocol/SKILL.md` (`mcp_integration.sequential`)
- [ ] `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md`
- [ ] `src/superclaude/skills/sc-post-release-protocol/SKILL.md`
- [ ] `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`
- [ ] `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` (not `refs/auggie-prompts.md`)
- [ ] `src/superclaude/skills/sc-roadmap-protocol/SKILL.md`
- [ ] `src/superclaude/skills/sc-release-split-protocol/SKILL.md`

## T3 — Agents + persona table

- [ ] `src/superclaude/agents/deep-research.md` — drop sequential-thinking tool; native reasoning for synthesis
- [ ] `src/superclaude/agents/deep-research-agent.md` — drop tool
- [ ] `src/superclaude/agents/socratic-mentor.md` — `sequential_thinking_integration` → native reasoning
- [ ] `src/superclaude/core/CLAUDE.md` **Personas table only** (not MCP Servers table): remove sequential/`seq` from Primary MCP. sequential-only rows (security, refactorer, devops) → native / empty. Keep c7/playwright where present.

## T4 — Test + sync + leftover grep

- [ ] Update `tests/sc-roadmap/compliance/test_mcp_circuit_breakers.py` `test_sequential_referenced` only (skill will no longer name Sequential MCP)
- [ ] `make sync-dev` (skills/commands/agents under src)
- [ ] `uv run pytest tests/sc-roadmap/compliance/test_mcp_circuit_breakers.py -v`
- [ ] Grep owned files: no `sequential-thinking`, `Sequential MCP`, `mcp__sequential`, `--seq` as Sequential MCP flag

## Acceptance

Owned files no longer install/document sequential-thinking as an IronClaude MCP. Native reasoning remains where multi-step analysis is still the job. Generic "sequential" (order) unchanged. No commit.
