# Draft notes

Leave a list empty (write "None") when there is nothing to report. The orchestrator asks the user one question only when either list has an item.

## New material

<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). -->

- Session wrapper accepts model selection, resolves tiers and can set a local proxy base URL: `src/superclaude/skills/ccsession-tag/ccsession:798`, `:1144`, `:1041`.
- The example environment file documents session proxy configuration: `src/superclaude/skills/ccsession-tag/ccsession.env.example:10-16`.
- The local gateway proxy documents model alias rewriting and tier request forwarding: `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:3-21`.
- Model profiles are defined in `src/superclaude/skills/ccsession-tag/ccsession-models.json:1-18`.
- Codegraph and auggie tools were unavailable in this worker; the quick static pass used Glob, Grep and Read.

## Contradictions

<!-- Each place where the description disagrees with the code, one per line, with path:line evidence. -->

- None
