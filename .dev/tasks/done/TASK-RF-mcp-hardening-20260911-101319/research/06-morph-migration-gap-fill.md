# Morph MCP migration gap fill

**Status:** Complete

## Conclusion

Retain the existing client registration/key `morphllm-fast-apply`; replace only its launcher with:

```sh
npx -y @morphllm/morphmcp
```

Preserve `MORPH_API_KEY`. The Claude MCP registration name is independent from the command, and preserving it lets same-name exact-command reconciliation upgrade current registrations without cross-name cleanup. No project Morph tool namespace was found in initial scope research.

No Morph-specific CLI flag is required for normal stdio operation. Do not use `--prefer-offline`; current vendor documentation warns it can use stale metadata. Optional configuration includes `MORPH_API_URL` and `MORPH_WARP_GREP_TIMEOUT`; do not add them without a current use case.

**Confidence:** high for package command/environment and conditional migration strategy.

Sources:
- https://www.npmjs.com/package/@morphllm/morphmcp
- https://registry.npmjs.org/@morphllm%2Fmorphmcp/latest
- https://docs.morphllm.com/guides/claude-code
- https://docs.morphllm.com/mcpquickstart
- https://docs.anthropic.com/en/docs/claude-code/mcp#option-3-add-a-local-stdio-server
