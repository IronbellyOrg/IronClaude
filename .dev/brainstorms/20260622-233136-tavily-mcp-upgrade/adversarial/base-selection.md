# Base Selection

## Quantitative Summary

| Variant | Coverage | Consistency | Specificity | Testability | Combined |
|---|---:|---:|---:|---:|---:|
| Variant 1 — Architect | 0.88 | 0.92 | 0.86 | 0.84 | 0.88 |
| Variant 2 — Refactorer | 0.86 | 0.94 | 0.90 | 0.86 | 0.89 |
| Variant 3 — QA | 0.90 | 0.90 | 0.88 | 0.98 | 0.92 |

## Selected Base

Variant 3 is selected as the base because it best satisfies the user's explicit verification requirements and keeps the `tavily-mcp@latest` target. Variant 1's source-of-truth and command-builder concerns and Variant 2's minimal-risk deletion/stale-migration framing are merged into the final artifact.

## Strengths Incorporated

- From Variant 1: keep remote HTTP default out of scope; test command-builder grammar; centralize the package token.
- From Variant 2: prefer deleting dormant Tavily JSON configs; scope stale migration to exact server name `tavily`.
- From Variant 3: adopt `tavily-mcp@latest`; add a comprehensive mocked test matrix; document optional live tool-surface verification for map/crawl.
