# Diff Analysis (cross-proposal contradictions)

## Contradictions

- BEADS DISPOSITION: A says DROP (v1), B says DROP, the Beads research itself recommends DEFER/earn-its-place, but C says ADAPT (wire behind createTool, start embedded). C is the outlier and its own top-risks list (Dolt instability, dual-source drift) contradicts its 'adapt' choice. 3-of-4 + research = DROP/DEFER wins.
- MASTRA SEQUENCING: A centers Mastra as the spine from Phase 1; D defers Mastra entirely until Phase 4, arguing Phases 0-2 need a thin Python ACP client and NO Mastra. C is in between (Mastra workflow from Phase 1 but parallel-run safety). This is the sharpest genuine architectural disagreement: Mastra-early (import vendor/churn/EE risk sooner, get the durable-workflow engine sooner) vs Mastra-late (vendor-free seam swap first, defer EE decision).
- HEADLINE RECOMMENDATION LABEL: B says 'defer'; A/C/D say 'hybrid.' But B's own Phase 0-6 IS a strangler-fig hybrid with gates — the label conflict is largely semantic/temperamental, not architectural. The four agree on the PLAN and disagree mainly on the WORD.
- SPRINT SEAM CLEANLINESS: D claims the sprint flagship has a clean 'delegate_runner' substitution branch (built-for-substitution); codebase verification shows sprint's seam is a private `_subprocess_factory` test hook with a hardcoded ClaudeProcess default — narrower and more entangled than D's framing. A and C more accurately treat sprint/executor as very-high difficulty rewrite. Contradiction resolved by ground truth: sprint is harder than D implies.
- DOMAIN-LOGIC END STATE: D treats the Python-behind-MCP boundary as PERMANENT architecture; A and C treat it as a transitional hybrid with a latent 'finish the TS migration' debt (A explicitly, C in optional Phase 4). Disagreement on whether polyglot is the destination or a waystation.
- VALUE/LIKELIHOOD CALIBRATION: B scores likelihood 16 (full-replatform strawman); A 24; C 28; D 29 — for what is substantially the SAME hybrid plan. The 13-point likelihood spread reflects framing/temperament (skeptic vs reference-architect) more than different plans, since all four converge on seam-first strangler-fig.

## Recommendation spread

| Proposal | Rec | V | C | L | R |
|---|---|---|---|---|---|
| Reference architecture — maximize multi-tenant capability: M | `hybrid` | 34 | 33 | 24 | 30 |
| Feasibility skeptic: risk-first no-go/defer case for porting | `defer` | 22 | 35 | 16 | 36 |
| Strangler-fig incremental migration: replace the single Clau | `hybrid` | 34 | 32 | 28 | 28 |
| Reuse-maximizing: swap only the runtime seam. Keep the Pytho | `hybrid` | 32 | 27 | 29 | 24 |
