# R7 check (item 12.4)

Run 2026-11-12. Guide file: `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` line 991. Contract file: `src/superclaude/core/WORKER-CONTRACT.md` line 23.

## Before (guide line 991 at HEAD)

```text
- The never-as-worker list (`~/.claude/WORKER-CONTRACT.md`, section 1): `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while decision D3 keeps it off workers. These commands are never dispatched as workers and get no `--unattended` mode.
```

## After (guide line 991 now)

```text
- The never-as-worker list (`~/.claude/WORKER-CONTRACT.md`, section 1): `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while decision D3 keeps it off workers. These commands are never dispatched as workers and get no `--unattended` mode.
```

## Contract line 23 now

```text
- **Never-as-worker list**: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers. These are never dispatched as workers and get no `--unattended` mode. The list changes only when the coordinator-only command set or D3 changes, never per phase. If D3 adds a worker route for pr-submit, D3 also states how that route passes the brief guard.
```

## Side by side: command order

| Source | Commands in order |
|---|---|
| Guide line 991 | /sc:agent /sc:git /sc:help /sc:issue /sc:pm /sc:spawn /sc:sweep /sc:swarm-wizard |
| Contract line 23 | /sc:agent /sc:git /sc:help /sc:issue /sc:pm /sc:spawn /sc:sweep /sc:swarm-wizard |

Result: the order in the guide line equals the order in the contract line (`equal`). PASS.

## Diff size

```text
$ git diff --stat -- docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
 .../SuperClaude-Developer-Guide-Commands-Skills-Agents.md               | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```
Result: 1 insertion and 1 deletion. PASS.
