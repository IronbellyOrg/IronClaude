# Summary: #504 [FEATURE] Add codegraph to agents analyze, design, implement and workflow

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/504
- Type: feature
- Complexity: complex (rubric: `refs/claim.md`)
- Effort estimate: 18 hours

Complexity note: the issue's Complexity field was set to Simple when the issue was created at quick depth. This check sizes it complex: the change touches more than one subsystem (four slash commands, two protocol skills and ten agent files, about 16 files) and is estimated at more than 16 hours.

## What the issue asks for

Add a single Codegraph readiness check to each of `/sc:analyze`, `/sc:design`, `/sc:implement` and `/sc:workflow` (in the command file, and in the backing skill for implement and workflow). When the index is fresh, those runs use the Codegraph tools on top of the existing Grep/Read search; otherwise they keep using Grep/Read and record a fallback note. Ten general-purpose agent files also get the shared rule "use Codegraph only when the caller passes `index_state: fresh`, otherwise Grep/Read". Changes go in `src/superclaude/`, followed by `make sync-dev` and `make verify-sync`. `/sc:troubleshoot`, `/sc:reflect` and the Codegraph MCP server are out of scope.

## Relevant files and systems (cheatsheet)

| Path or system | Why it matters |
|---|---|
| `src/superclaude/commands/analyze.md` | Needs the readiness check; no backing skill; today only mentions `.codegraph/` as an excluded report directory (line 97). |
| `src/superclaude/commands/design.md` | Same as analyze; no backing skill; `.codegraph/` exclusion only (line 96). |
| `src/superclaude/commands/implement.md` | Thin wrapper that invokes `Skill sc:implement-protocol` (line 79). |
| `src/superclaude/commands/workflow.md` | Thin wrapper that invokes `Skill sc:workflow-protocol` (line 54). |
| `src/superclaude/skills/sc-implement-protocol/SKILL.md` | Backing protocol for implement; where the readiness check and agent briefs belong. |
| `src/superclaude/skills/sc-workflow-protocol/SKILL.md` | Backing protocol for workflow; same. |
| `src/superclaude/agents/{system-architect,root-cause-analyst,refactoring-expert,security-engineer,performance-engineer,python-expert,backend-architect,quality-engineer,self-review,technical-writer}.md` | The ten agents that need the `index_state: fresh` rule; none has it today. |
| `src/superclaude/core/CODEGRAPH.md` (installs to `~/.claude/CODEGRAPH.md`) | Defines the once-per-run readiness check (section 2), degraded tokens, tool table and the agent rule (line 24). |
| `src/superclaude/agents/{auggie-reviewer,reflect-reviewer,reuse-auditor,troubleshoot-analyst}.md` | Existing wording of the agent rule to copy. |
| `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`, `sc-reflect-protocol/SKILL.md`, `sc-auggie-review-protocol/SKILL.md` (step 7) | Existing readiness-check pattern, including `allowed-tools` entries for the `mcp__codegraph__*` tools. |
| `make sync-dev` / `make verify-sync` | Copy `src/` to `.claude/` and confirm the two match. |
| Local checkout | 49 commits behind `origin/master`; rebase or work from `origin/master` before editing. |

## Analysis

None: the accuracy check found the issue current, so no analysis ran.
