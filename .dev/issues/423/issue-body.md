<!-- /sc:issue feature template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. -->

## Feature Summary

**Orchestrator v2 - Proactive Holistic** gives each Orchestrator a catalogue and working knowledge of what all agents across all workspaces are doing, maintaining a holistic view and using it to inform and course-correct their work. This is a separate future release after the v1 orchestrator (#339) is complete.

## Problem Statement

Agents working across workspaces need relevant knowledge from one another's work, research, failures and lessons learned. The Orchestrator should identify shared problems, reusable functionality and work that benefits from coordination, rather than treating each agent's work in isolation.

## User Story

As an Orchestrator supervising agents across workspaces, I want an up-to-date catalogue of their work and regular cross-agent reviews, so that relevant knowledge is shared, duplicate effort is identified and overlapping work can be coordinated proactively.

## Proposed Solution

Start with `/sc:brainstorm --depth deep --handoff design`. Treat this as v2, a separate future release after completion of the v1 orchestrator (#339), not an expansion of the v1 delivery scope.

Each Orchestrator catalogues and uses knowledge of what all agents across all workspaces are doing. Update the catalogue through timer-based refreshes and child-session reports at checkpoints or accomplishments. Also consider cheaper, faster agents searching sessions or diffing logs and summarizing changes. Feed these updates into a process that determines their relevance to every other agent with work in progress or unmerged PRs.

Conduct regular reviews to identify:

- How agents' work impacts other agents.
- Duplicate functionality that could be reused or instanced/referenced directly.
- Research that could inform other agents and should be shared.
- Issues, bugs or failures whose fixes could inform others.
- Multiple agents solving the same issue.
- Overlapping work touching the same files that could be done better in a specific order.
- Proactive course corrections or changes resulting from lessons learned.

Run a dedicated `/tech-research` pass to find techniques used elsewhere for multi-agent memory and context, and how those techniques enrich or course-correct other agents. This research can be done ahead of the rest of the work and saved to this issue.

### Research findings (to be added)

Not known yet.

### Architecture and next steps

Keep the architecture flexible for harnesses outside Claude Code, including one like Mastra. Follow `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`.

Next steps: begin with `/sc:brainstorm --depth deep --handoff design`, then run the dedicated `/tech-research` pass and save its findings to this issue ahead of the remaining work. Do not begin implementation before the brainstorm and research are complete; v2 delivery follows completion of v1.

## Acceptance Criteria

- [ ] `/sc:brainstorm --depth deep --handoff design` has been run as the starting point, with its design handoff linked from this issue before implementation begins.
- [ ] A dedicated `/tech-research` pass examines multi-agent memory/context techniques used elsewhere and how they enrich or course-correct agents; its findings are saved to this issue. This research may be completed ahead of the remaining work.
- [ ] Each Orchestrator has a catalogue covering all agents across all workspaces; a timer refresh and a child-session checkpoint or accomplishment report each demonstrably update it.
- [ ] Catalogue updates are evaluated for relevance to other agents with work in progress or unmerged PRs, with a relevant update demonstrably used to inform their work.
- [ ] Regular reviews identify and record how agents' work impacts one another.
- [ ] Regular reviews identify duplicate functionality and record opportunities to reuse or instance/reference it directly.
- [ ] Regular reviews identify research relevant to other agents and share it with those agents.
- [ ] Regular reviews identify issues, bugs or failures whose fixes could inform others and share those lessons.
- [ ] Regular reviews identify multiple agents solving the same issue.
- [ ] Regular reviews identify overlapping work touching the same files and record a better execution order where appropriate.
- [ ] Regular reviews record proactive course corrections or changes arising from lessons learned and relay them to affected agents.
- [ ] The design documents how the architecture can support a harness outside Claude Code, including an option such as Mastra, without making the core approach Claude-Code-only.
- [ ] The design and resulting components are checked against `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, with the compliance review recorded.
- [ ] v2 is delivered as a separate future release after the v1 orchestrator (#339) is complete.

## Out of Scope

- v1 orchestrator work (#339).
- Implementation before the brainstorm and research are complete.

## Components Affected (from `/sc:analyze`)

Static discovery and architecture inspection followed `/sc:analyze` without a depth flag, using Glob, Grep and Read because Codegraph and Auggie tools were unavailable. These are existing integration/review surfaces, not a finalized implementation file list:

- `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` — required architecture guide; its Orca orchestration section describes the coordinator/worker separation.
- `src/superclaude/core/WORKER-CONTRACT.md` — existing coordinator, worker-report and cross-session follow-up rules to account for when designing v2.
- `src/superclaude/commands/pm.md` and `src/superclaude/skills/sc-pm-protocol/SKILL.md` — existing project-management orchestration and memory/checkpoint protocol to review for integration or reuse.
- `src/superclaude/commands/spawn.md` — existing task decomposition and delegation command to review for orchestration boundaries.
- `~/.claude/skills/orchestration/SKILL.md` — installed Orca orchestration discovery stub, which loads the version-matched guide from the Orca binary; this is an external integration surface, not a repository-owned implementation file.

The scoped repository discovery did not locate a dedicated v1/v2 orchestrator command or skill implementation. New implementation paths: Not known yet. This pass identified components only; it did not validate live Orca behavior or performance.

## Related Issues/PRs

- #339 — [Orchestrator - To Run and manage ALL sessions within a worktree](https://github.com/IronbellyOrg/IronClaude/issues/339): v1 prerequisite covering session supervision, child reporting and session recovery/cleanup; v2 follows its completion.
- #409 — [TUI Dashboard to Manage Orchestration at Scale](https://github.com/IronbellyOrg/IronClaude/issues/409): related read-only human-observation dashboard for orchestrators and sessions; distinct from v2's proactive knowledge sharing and course corrections.
- #331 — [Automated Github Issue / Task Watcher and Routing Service](https://github.com/IronbellyOrg/IronClaude/issues/331): related intake service proposal that would notify a project's Orchestrator about tagged, human-approved backlog issues.
- #326 — [Embed more Git and PM related workflows into skills](https://github.com/IronbellyOrg/IronClaude/issues/326): related effort to improve Git/GitHub communication and collaboration across commands and skills, rather than the cross-workspace knowledge catalogue itself.

<!-- sc:issue:create template=issue-feature-simple -->
