# Draft notes

Leave a list empty (write "None") when there is nothing to report. The orchestrator asks the user one question only when either list has an item.

## New material

<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). -->

- Linux 6.8.0: supplied session environment, OS Version Linux 6.8.0-147-generic.
- Contract describes worker completion and preamble authority over heartbeat cadence: `src/superclaude/core/WORKER-CONTRACT.md:5-7`.
- Contract suppresses heartbeats during `ask` or `check --wait`, requires pulling follow-ups, and has the coordinator open the contract after completion: `src/superclaude/core/WORKER-CONTRACT.md:56-61,88`.
- Developer guide describes coordinator and worker roles and the orchestration discovery stub: `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:972-981`.
- Orchestration skill describes coordination, heartbeats and message waits: `~/.claude/skills/orchestration/SKILL.md:20-27`.
- #409 is a TUI dashboard for managing orchestration at scale; #331 is a task watcher and routing service; #394 concerns launch-level enforcement: `scout.md:27-31`.
- #315 concerns a launch-time session-name prompt: `gh issue view 315 --repo IronbellyOrg/IronClaude --json title,body`.
- #412 concerns selecting the wrong session launch action, not a demonstrated prompt: `gh issue view 412 --repo IronbellyOrg/IronClaude --json title,body`.
- Quick analysis used Grep and Read because codegraph and auggie tools were unavailable; no runtime reproduction was performed: this analysis session.
- High severity and all supervised worker runs as the potential blast radius are requested draft classifications, not independently verified incident measurements: task instructions.

## Contradictions

<!-- Each place where the description disagrees with the code, one per line, with path:line evidence. -->

- None
