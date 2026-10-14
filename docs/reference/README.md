# Reference Documentation

This folder holds reference material: troubleshooting guides, diagnostic procedures, and format contracts. It does not tell you which command to use for a job; for that, read [How We Work](../user-guide/how-we-work.md), or run `/sc:recommend "<what you want to do>"`. For the syntax of each command, see the [Commands Reference](../user-guide/commands.md).

## Troubleshooting

| Document | Use it when |
|---|---|
| [common-issues.md](./common-issues.md) | You hit a frequent problem and want the quick fix |
| [troubleshooting.md](./troubleshooting.md) | The quick fixes did not work and you need a step-by-step diagnosis |
| [diagnostic-reference.md](./diagnostic-reference.md) | You need to check installed context files and configuration by hand |
| [mcp-server-guide.md](./mcp-server-guide.md) | An MCP server will not start, connect, or respond |

## Contracts and design notes

| Document | What it defines |
|---|---|
| [deviation-report-format.md](./deviation-report-format.md) | The deviation report schema that pipeline gates and CLI commands read |
| [nfr-conv-2-prose-determinism.md](./nfr-conv-2-prose-determinism.md) | Where task-builder output must be deterministic and where prose may vary |
| [pm-agent-autonomous-reflection.md](./pm-agent-autonomous-reflection.md) | How the PM agent reflects on its own work and saves tokens |
| [claude-code-history-management.md](./claude-code-history-management.md) | How Claude Code stores conversation history and how to rotate it |
