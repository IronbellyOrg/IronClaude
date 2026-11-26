# Cross-workspace sweep architecture analysis

Template: analysis structure registered in `.dev/issuecleanup/g1/362/report-template.md`, adapted to the selected source path.

## Scope and grounding
Command: `/sc:analyze src/superclaude/skills/sc-sweep-protocol --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g1/423/analyze`.

The selected directory contains one Markdown protocol file, the narrowest existing source entry point for the recurring cross-session observations that issue #423 would reuse. Supporting reads followed its CLI into `src/superclaude/cli/sweep/commands.py` and the read allowlist in `probes.py`, plus the coordinator contract and recorded owner decisions. This does not pretend a v2 implementation directory exists.

Codegraph: index_state=fresh, checked_at=2026-11-23T23:09:34Z; degraded: graph:empty, graph:ambiguous, graph:truncated.

Access: mcp. Markdown is not indexed, so the target layout lookup returned no files and fell back to Glob/Read. The supporting CLI outline was available; its generic `run` caller query aggregated unrelated names, and its callee query showed 12 of 13 results. These were discovery leads only; the cited pipeline was read directly.

## Architecture and metrics
- The scoped surface is one 66-line Markdown file. It forwards caller flags unchanged and defines one sweep invocation plus one command-not-found fallback, not a refresh scheduler (`src/superclaude/skills/sc-sweep-protocol/SKILL.md:15-25`).
- The supporting CLI path is argument checks, optional Run binding, collection, classification, rendering, report publication and JSON output (`src/superclaude/cli/sweep/commands.py:248-278`). The skill reads the resulting report and prints counts and its location. This is a reusable observation source, not the requested knowledge layer.
- The collection boundary allows only listed read operations and explicitly rejects remote inclusion (`src/superclaude/cli/sweep/probes.py:49-62`). Expanding from local observations to every workspace requires an explicit scope and trust design, not silently broadening that allowlist.
- The coordinator contract supplies periodic-read duties without a scheduler and keeps person-started sessions observational only (`src/superclaude/core/WORKER-CONTRACT.md:288-290`).
- No source change, dependency change, export change, configuration change or test change was made. No complexity score, performance measurement, runtime pass or test count is claimed by this static review.

## Severity-rated findings
1. **High, scope/safety mismatch in the issue, not a discovered sweep defect:** the body promises relaying course corrections to affected agents, whereas the recorded owner decision is report-only with explicit prerequisites for reopening direct delivery (`.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/owner-answers.md:259`). Treating read permission or a useful summary as authority to instruct another session would cross the declared boundary. Correct the future scope through the coordinator after the owner's go.
2. **Medium, missing feature rather than regression:** the existing protocol produces a one-time status report, not a durable knowledge catalogue, relevance evaluator, research-sharing process or duplicate-work/course-correction reviewer (`src/superclaude/skills/sc-sweep-protocol/SKILL.md:15-29`; `src/superclaude/cli/sweep/commands.py:267-278`). The sweep merge is groundwork, not grounds to close #423.
3. **Medium, stale sequencing in the issue:** the owner narrowed the start gate to the sweep merge plus recorded capture, with the classification code fix explicitly not a gate. The capture findings exist and #539 is merged (`owner-questions/owner-answers.md:258` and `owner-questions/Q24/capture-findings-20261116.md:28-29`, both beneath `.dev/brainstorms/20261113-orchestrator-tui-alignment/`). Waiting for the whole of #339 would add an unapproved dependency. Meeting that gate does not itself grant starting v2.

No newly verified source-code defect was found in the small selected protocol. That statement is limited to this architecture inspection; it is not a full code or security audit.

## Recommendations and roadmap
Keep #423 open as still relevant. The next smallest step is a coordinator-owned correction of its scope and sequencing after the owner grants it, followed by the issue's requested brainstorm/design handoff and dedicated memory/context research. Reuse the sweep's observation source where it fits; do not equate it with a knowledge store or add cross-session delivery without a new explicit decision. Define which workspaces are in scope, what must persist, who can read it and how usefulness will be demonstrated before estimating a concrete implementation plan. Follow the existing command/skill/agent separation in `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:51-75`.

## Verification limits
Static quick architecture analysis only. No live sweep, tests, external multi-agent-memory research or off-checkout branch inspection was run. Source searches for catalogue, knowledge, relevance and course-correction terms in the supporting sweep package returned no matches; that is a scoped negative result, not a repository-wide absence proof. GitHub event timeline is UNVERIFIED because the authorized CLI surface is limited to issue/PR view/list, which exposes the body, comments and current state but not a complete event stream. The main findings report records this limit.
