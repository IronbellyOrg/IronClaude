# Official command verification

**Retrieved:** 2026-09-11

| Server | Verified source | Decision |
|---|---|---|
| Tavily | https://www.npmjs.com/package/tavily-mcp/v/0.2.22 | npm reports `0.2.22`; use `npx -y tavily-mcp@0.2.22`. |
| Sequential Thinking | https://www.npmjs.com/package/@modelcontextprotocol/server-sequential-thinking/v/2026.8.31 | npm reports `2026.8.31`; pin `npx -y @modelcontextprotocol/server-sequential-thinking@2026.8.31`. |
| Serena | https://pypi.org/project/serena-agent/1.7.0/; https://oraios.github.io/serena/02-usage/030_clients.html | Distribution is `serena-agent==1.7.0`; retain the research-verified server command `uvx --from serena-agent==1.7.0 serena start-mcp-server --context claude-code --project-from-cwd --enable-web-dashboard false --enable-gui-log-window false`. |
| Auggie | https://www.npmjs.com/package/@augmentcode/auggie/v/0.36.0; https://docs.augmentcode.com/context-services/mcp/quickstart-claude-code | `0.36.0` is published; official MCP args are `auggie --mcp --mcp-auto-workspace`. Pin global guidance/install metadata to `@augmentcode/auggie@0.36.0`. |
| Morph | https://www.npmjs.com/package/@morphllm/morphmcp; https://docs.morphllm.com/guides/claude-code | Official successor package is `@morphllm/morphmcp`; current package guidance supports `npx -y @morphllm/morphmcp`. Retain local registration key/name `morphllm-fast-apply` and `MORPH_API_KEY` as an intentional project compatibility decision. |

No command was inferred from local documentation. The selected Morph registration name intentionally differs from the vendor example and is not claimed to be a vendor-required identity.
