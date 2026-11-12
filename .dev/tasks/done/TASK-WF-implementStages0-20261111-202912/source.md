Implement Stages 0 to 2 of the reflect Tier 2 review-panel design: offline measurement, dormant kernel extensions, pre-execution shadow mode behind --t2-engine (default legacy), as specified in .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md. Code: src/superclaude/cli/review, src/superclaude/cli/reflect, src/superclaude/skills/sc-reflect-protocol

---

Referenced specification (the inline prompt above names it; it is not copied here because of its size).

- Path (repo-relative): .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md
- sha256 at plan time: 54a8dce218d2540ae312d721c65b47e5329120905006e5d480931400cb8c4e45
- Size at plan time: 103145 bytes
- Sections that define the requested scope: "Staged migration" (Stages 0, 1, 2), "Q4. Engine" (K1 hard exclusion contract, Template set, Forbidden models, Executor-exclusion gates, Guards and counts), "Finding format" (findings-v2, Multi-file identity K4 cluster_v2, cluster_agreement, Evidence gate and citation pre-check), "Adapter sketches" (Execution contract, Pre-execution adapter, Shadow mode), "When the panel is called (depth x tier path)" (rules D1-D5), "Contract compatibility gate", "First measurement" (Stage 0a), "Open items", "Assumptions and UNVERIFIED items".
- Out of scope (later stages): Stage 3 pre panel opt-in, Stage 4 pre default, Stage 5 post panel dispatch, Stage 6 deferred candidate E'. Contract version stays 1.8.0 in every stage requested here.

Flags of the invocation: --depth standard --handoff none (strategy default: systematic).
