# Proposal C: Strangler-fig incremental migration: replace the single ClaudeProcess/stream-json seam first (Phase 0-1), run the new Mastra pipeline alongside the existing Python CLI for one full flagship workload (Phase 2), then decide on EE vs DIY RBAC at the business gate (Phase 3). Never touch the 50K LOC of portable domain logic until the runtime seam is proven.

**Recommendation:** `hybrid`

**Thesis:** Port the SuperClaude orchestration pipeline to Mastra+Backlog.md+Beads via strangler-fig: prove AcpAgent replaces ClaudeProcess in a 1-2 week spike, then port the sprint pipeline first as a Mastra workflow running parallel to the existing Python CLI, keep all 50K LOC of domain logic behind Python tool boundaries during transition, and only port domain logic to TypeScript after the runtime seam is proven. Multi-tenant RBAC requires a Phase 3 commercial decision on Mastra EE licensing vs DIY RBAC build.

**V/C/L/R:** Value 34 | Complexity 32 | Likelihood 28 | Risk 28

> The single seam replacement (ClaudeProcess -> AcpAgent) is a narrow, well-scoped target with strong Mastra documentation fit. The multi-tenant RBAC strategic driver is commercially gated on Mastra EE pricing, which is the primary uncertainty. The 50K LOC of portable domain logic de-risks the port because the bulk of the intelligence does not need rewriting in Phase 0-2 -- it runs behind a Python tool boundary. Phase 0 ACP spike is the decisive go/no-go gate: if AcpAgent cannot replicate ClaudeProcess semantics, the entire port stops with minimal sunk cost (< 2 weeks). Overall likelihood is medium-high because each phase has a clear gate and the parallel-run strategy prevents big-bang failure.

## Port Matrix

| Component | Disposition | Rationale |
|---|---|---|
| pipeline/process.py (ClaudeProcess) | `rewrite` | The single runtime seam. Must be replaced by Mastra AcpAgent adapter (~245 LOC -> Mastra createTool wrapping AcpAgent.stream()). Python process groups, stdin prompt delivery, and stream-json parsing have no direct TS equivalent. AcpAgent is the structural replacement. |
| pipeline/models.py | `adapt` | Pure dataclasses (Step, StepStatus, GateCriteria, etc.). Port to TypeScript Zod schemas or Python Pydantic models that Mastra steps consume. ~235 LOC, trivial port. |
| pipeline/gates.py | `reuse-as-is` | Pure Python gate validators with zero runtime coupling. Keep as Python service callable from Mastra via createTool (spawn uv run python ...) or port to TS later. No urgency to rewrite. |
| pipeline/executor.py (generic step sequencer) | `rewrite` | Composition-via-callable sequencer with retry/parallel/trailing-gate. Maps directly to Mastra createWorkflow with .parallel(), .then(), .branch(). ~470 LOC, medium port. |
| pipeline/trailing_gate.py | `rewrite` | Thread-based async gate evaluation with grace-period protocol. Mastra workflows handle this via .branch() + timeout steps. ~650 LOC, low port but needs workflow semantics rewrite. |
| pipeline/fmea suite (classifier, domains, invariants, passes, promotion) | `reuse-as-is` | Pure Python regex/text analysis with zero Claude coupling. Keep behind Mastra createTool or port to TS in low-priority wave. |
| pipeline/dataflow_graph + dataflow_pass | `reuse-as-is` | Pure Python DAG construction. Keep as Python callable; Mastra orchestrates. |
| pipeline/guard analyzer/pass/resolution | `reuse-as-is` | Pure Python analysis. Same reuse-as-is strategy as FMEA suite. |
| pipeline/conflict_detector + conflict_review | `reuse-as-is` | Pure Python. Reuse behind Mastra tool boundary. |
| pipeline/state_detector + mutation_inventory | `reuse-as-is` | Pure Python. Reuse. |
| pipeline/diagnostic_chain + combined_m2_pass | `reuse-as-is` | Pure Python. Reuse. |
| pipeline/contract_extractor + deliverables + verification_emitter | `reuse-as-is` | Pure Python. Reuse. |
| sprint/executor.py (2150 LOC main loop) | `rewrite` | The flagship orchestration logic. Phase sequencing, stall detection, TUI, KPI, retrospective, tmux, TurnLedger all need re-expression as Mastra workflow steps + Node.js event loop. Very-high port. Keep Python as MCP service for Phase 1-2 parallel run; full TS rewrite is Phase 3+. |
| sprint/process.py (Sprint ClaudeProcess subclass) | `rewrite` | Extends ClaudeProcess with build_prompt() and sprint-specific hooks. Entirely subsumed by AcpAgent adapter. ~385 LOC. |
| sprint/models.py (885 LOC domain types) | `adapt` | Pure data types. Port to TS interfaces/Zod schemas. TaskEntry, SprintConfig, TurnLedger, PhaseStatus FSM all straightforward. |
| sprint/checkpoints.py (410 LOC) | `adapt` | Checkpoint extraction from markdown + manifest. Port to TS or keep as Python tool. Mastra suspend/resume provides the checkpoint mechanism itself. |
| sprint/monitor.py (570 LOC stream-json parser) | `drop` | Parses NDJSON from claude --output-format stream-json. AcpAgent.stream() emits Mastra text-delta chunks -- a different wire format entirely. The stall detection and turn counting logic must be reimplemented against the new stream. |
| sprint/tmux.py (325 LOC) | `drop` | tmux session management is a deployment choice specific to the CLI-local workflow. Mastra Studio UI replaces this for the multi-user target. Drop or keep as optional legacy CLI shim. |
| sprint/tui.py (630 LOC Rich dashboard) | `drop` | Replaced by Mastra Studio UI + OTel traces. Drop. |
| sprint/commands.py (465 LOC Click CLI) | `rewrite` | Click CLI routes to executor. Replaced by Mastra Server HTTP endpoints + optional CLI wrapper. Medium port. |
| sprint/config.py (510 LOC phase discovery) | `reuse-as-is` | Markdown parsing. Keep as Python callable or port to TS. Low priority. |
| sprint/summarizer + retrospective + kpi + logging_ (~1.5K LOC) | `reuse-as-is` | Pure Python report generation. Keep behind Mastra tool boundary; port later if needed. |
| sprint/preflight + diagnostics + notify + debug_logger (~700 LOC) | `reuse-as-is` | Pure Python utilities. Reuse. |
| roadmap/executor.py (3700 LOC 8-step pipeline) | `rewrite` | The largest single file. Extract/generate/diff/debate/score/merge/remediate/certify with convergence loop. Maps to Mastra createWorkflow but the convergence engine integration is complex. Very-high port. Keep Python behind MCP for Phase 1-2. |
| roadmap/convergence.py (780 LOC) | `adapt` | DeviationRegistry, convergence loop, regression detection. Core algorithm is portable but tightly integrated with TurnLedger. Port to TS or keep as Python callable. |
| roadmap/gates.py (1440 LOC, 14 gates, 30+ checks) | `reuse-as-is` | Pure Python semantic checks. Keep as Python service. Port individually to TS over time. |
| roadmap/cosmetic_remediator.py (1100 LOC) | `reuse-as-is` | Deterministic regex transforms. Zero runtime coupling. Keep as Python. |
| roadmap/fidelity + structural + semantic checkers (~2.2K LOC) | `reuse-as-is` | Pure Python analysis. Keep behind Mastra tool boundary. |
| roadmap/spec_parser + fingerprint + spec_structural_audit (~975 LOC) | `reuse-as-is` | Pure Python markdown/AST parsing. Keep. |
| roadmap/obligation_scanner + integration_contracts (~1.3K LOC) | `reuse-as-is` | Pure Python text analysis. Keep. |
| roadmap/remediate* (5 files, ~2.1K LOC) | `reuse-as-is` | Remediation orchestration. Keep as Python callable from Mastra. |
| roadmap/prompts + validate_prompts + certify_prompts (~1.9K LOC) | `reuse-as-is` | LLM prompt templates. Runtime-agnostic. Keep as markdown/text resources consumed by either runtime. |
| roadmap/commands + validate_executor + templates + validate_gates (~840 LOC) | `reuse-as-is` | CLI + validation. Keep or port later. |
| tasklist/* (executor, models, gates, prompts, commands) | `reuse-as-is` | Small, pure Python. Keep behind Mastra tool boundary. |
| prd/* (executor, prompts, process, ~2.7K LOC) | `reuse-as-is` | PRD pipeline. Keep as Python service; port later if product priority demands. |
| audit/* (entire module, ~6.7K LOC) | `reuse-as-is` | Static analysis suite, pure Python, zero runtime coupling. Keep as callable Python services. Highest-LOC reusable block in the entire codebase. |
| skills/* (24 SKILL.md files) | `reuse-as-is` | Portable markdown. Mastra has skills.sh integration. Drop-in. |
| agents/* (39 .md files, ~8K LOC) | `reuse-as-is` | Portable markdown agent personas. Runtime-agnostic. |
| install_hooks + install_commands + install_agents + install_mcp (~1.4K LOC) | `drop` | Claude Code-specific installation pipelines. Irreducible Claude runtime coupling. Drop entirely; replaced by Mastra build/deploy. |
| cli_portify/* (~6K LOC) | `adapt` | Self-referential porting tool. Adapt for the Mastra target or drop after port completes. |
| eval/* (~8.5K LOC) | `adapt` | Eval harness with PTY driver. Adapt to drive Mastra AcpAgent instead of ClaudeProcess. Keep isolation model. |
| Backlog.md (external dependency) | `reuse-as-is` | MIT, built-in MCP server, markdown task-of-record. Plug into Mastra as MCP client for task create/update/query. |
| Beads (external dependency) | `adapt` | MIT, Dolt-backed issue graph. Wire behind Mastra createTool (bd CLI --json) for bd ready/dep cycles/prime. Flag Dolt ops risk; start with embedded mode. |

## Roadmap Phases

| Phase | Goal | Effort | Dependencies |
|---|---|---|---|
| Phase 0 -- ACP Spike | Prove AcpAgent drives Claude Code through ACP with max_turns/permission/model parity vs current ClaudeProcess. Drive one additional CLI (Codex or Gemini) to validate multi-tool claim. Deliver a single Mastra createTool that spawns AcpAgent, streams output, and produces a report matching the current stream-json parse. | `S` | Node >=22.13.0, @mastra/core >=1.34.0, @mastra/acp installed, Claude Code on PATH |
| Phase 1 -- Sprint Pipeline Dual-Run | Port sprint executor to Mastra createWorkflow with Postgres/LibSQL suspend/resume. Keep ALL Python domain logic behind Mastra createTool boundaries. Wire Backlog.md MCP as task-of-record. Run in PARALLEL with existing Python CLI for 2-3 sprints. Gate: identical phase outcomes within 5% tolerance. | `L` | Phase 0 gate passed, Postgres or LibSQL storage configured, Backlog.md init in project, Mastra Server running |
| Phase 2 -- Multi-User Server + SimpleAuth | Expose sprint + roadmap pipelines as Mastra Server HTTP endpoints. Add SimpleAuth (API-key->role) for basic multi-user access. Wire OTel observability for per-run traces and token/cost attribution. Replace tmux/TUI with Mastra Studio playground. | `M` | Phase 1 gate passed, Mastra Server deployed, OTel exporter configured |
| Phase 3 -- RBAC Decision Gate | The business decision: license Mastra EE for SSO+RBAC+Agent Builder multi-tenant, or build DIY RBAC on the Apache server layer. Wire Inngest for per-tenant concurrency if EE. Add Beads Dolt server mode if bd ready proved valuable. Gate: 3+ tenants, noisy-neighbor isolation verified. | `XL` | Phase 2 gate passed, Mastra EE license procured (path A) or DIY RBAC architecture approved (path B), Inngest account |
| Phase 4 -- Domain Logic Port (optional) | Incrementally port the ~50K LOC of reusable Python domain logic to TypeScript Mastra steps. Start with gates, checkpoints, convergence, cosmetic remediation. Audit suite and roadmap gates are lowest priority. | `XL` | Phase 3 gate passed, TypeScript team capacity, confidence in Mastra API stability |

## Top Risks

- Mastra EE licensing cost is unknown and non-negotiable without vendor engagement -- the strategic driver (multi-tenant RBAC) is commercially gated. Budget risk if EE pricing exceeds internal build cost.
- AcpAgent max_turns/permission-flag/model-parity is UNVERIFIED against Claude Code's actual CLI flags. If ACP normalizes away knobs like --max-turns or --dangerously-skip-permissions, the sprint TurnLedger budget model breaks and stall detection semantics change.
- Python-to-TypeScript boundary introduces serialization impedance: gate predicates return Python dataclasses that Mastra steps must parse from stdout JSON. Error propagation across the boundary is fragile until typed adapters exist.
- Beads Dolt-only backend carries operational instability risk (orphaned dolt sql-server, embedded panics, migration-induced pull failures are open issues). Betting the dependency graph on a moving target risks production incidents.
- Mastra API churn (1.0 -> 1.16 already broke getAgents->listAgents, telemetry config, pagination) means the ported workflow may need codemod updates every 2-3 months. Version-pinning is mandatory but delays security patches.
- Backlog.md official MCP server decision/milestone tool exposure is UNVERIFIED. If decision_create is not available, the obligation_scanner -> decision.add dependency in the roadmap pipeline cannot be satisfied without CLI text-parsing fragility.
- Dual-source-of-truth drift between Backlog.md (markdown work-of-record) and Beads (Dolt issue graph) during Phase 1-2. A sync adapter is required but not yet designed.
- The existing Python CLI must remain fully functional during the parallel run (Phase 1-2). Any changes to shared domain logic (gates, models, checkpoints) must be backward-compatible with both runtimes -- a hidden compatibility tax.

## Key Tradeoffs

["T1: Mastra EE license (paid RBAC/SSO now) vs DIY RBAC on Apache server (build cost 2-3 months, no vendor lock-in).", "T2: Port domain logic to TS (clean, but 3-6 months of rewrite risk) vs keep Python behind MCP/HTTP (faster, but introduces cross-language boundary).", "T3: Ship Backlog.md + Beads together (complete DAG + markdown, but dual-source-of-truth risk and Dolt ops burden) vs Backlog.md only (simpler, lose bd ready/agent-memory, approximate in harness).", "T4: AcpAgent for multi-tool today (Claude Code verified; Cursor/Gemini/Copilot unverified) vs waiting for ACP maturity (safer but loses first-mover advantage).", "T5: Full parallel run for 2-3 sprints before decommissioning old pipeline (safety, but doubles infra cost during transition) vs quicker cutover (faster but higher blast-radius if AcpAgent flags diverge)."]
