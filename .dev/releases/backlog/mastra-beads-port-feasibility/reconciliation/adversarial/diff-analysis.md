# Diff Analysis: Mastra/Beads Port Feasibility — HYBRID study vs DEFER review

## Metadata
- Generated: 2026-06-03
- Variants compared: 2
- Variant 1 (V1): `merged-requirements.md` — original feasibility study, recommendation **HYBRID (conditional go)**, V/C/L/R = 33/30/29/26
- Variant 2 (V2): `revised-recommendation.md` — adversarial red-team + re-synthesis, recommendation **DEFER**, V/C/L/R = 28/34/20/34
- **Relationship note:** V2 is not a peer variant — it is an explicit adversarial review *of* V1 (`reviews: ../merged-requirements.md`). The comparison is therefore a **thesis vs. antithesis reconciliation**, and several "contradictions" are V2 deliberately correcting V1 against re-verified source.
- Total differences found: 19 (structural 1, content/contradiction 10, unique 8, shared assumptions 4)
- Categories: structural (1), content+contradictions (10), unique (8), shared assumptions (4)

---

## Structural Differences

| # | Area | Variant 1 (HYBRID) | Variant 2 (DEFER) | Severity |
|---|------|--------------------|--------------------|----------|
| S-001 | Document genre & completeness | Full 12-section decision document: exec summary, current-state architecture, target-stack assessment, component port matrix, runtime seam, task-of-record, multi-tenancy/licensing, what-is-lost, 5-phase roadmap, risk register, open questions, recap | 5-section delta review: revised recommendation, claims survived/knocked-down, roadmap-after-triage, decision-gates-that-matter, what-changed | **High** — different genres. V1 is the standalone artifact; V2 is a diff against it. A merge must re-host V2's corrections *inside* V1's structure, not append them. |

---

## Content Differences & Contradictions

> X-NNN combines the content-diff and contradiction passes since nearly every content difference here is V2 actively contradicting/qualifying V1.

| # | Point of conflict | Variant 1 position | Variant 2 position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | **Top-line recommendation** | HYBRID — conditional go via strangler-fig, gated on a dual Phase-0 spike | **DEFER** — buy down load-bearing unknowns in a time-boxed Phase 0 *before* starting any multi-phase roadmap | **High** — the decision itself. |
| X-002 | **V/C/L/R scoring** | 33/30/29/26 → **V > R** (favorable inversion justifies momentum) | 28/34/20/34 → **V < R** (Value drops, Complexity+Risk rise, Likelihood 29→20). The flip is the quantitative basis for DEFER. | **High** — the scoring inversion *is* the argument. |
| X-003 | **"Only ~1.2K of ~73K LOC is Claude-coupled"** | Headline feasibility claim: seam swap of ~1.2K LOC, not a 65K rewrite | Arithmetic literally correct (244+385+571=1,200) **but KNOCKED DOWN as phrased** — behavioral coupling is broader: `shutil.which("claude")` preflight, `TurnLedger(initial_budget=max_turns*active_phases)`, `CLAUDE_WORK_DIR`, CLI permission flags (`commands.py` 88-117) | **High** — reframes the central feasibility headline from "tiny seam" to "narrow file seam + broad behavioral coupling". |
| X-004 | **roadmap/executor.py abstraction** | "Already wraps the runtime behind `claude_process_factory` + `_ClaudeRunner` (:1271-1279)" → the *easier* flagship | **PARTIAL** — only the semantic-layer/convergence path (1358-1365) is factory-wrapped; ordinary steps instantiate `ClaudeProcess(...)` directly at **1107-1118**. Not uniformly abstracted. | **High** — source-verified correction; changes flagship-readiness assessment. |
| X-005 | **Flagship sequencing (Phase 2 target)** | **Sprint first** — swap the seam on the sprint flagship + parallel-run gate | **Sprint last.** Order: pipeline `StepRunner` (the one verified-clean seam) → roadmap semantic-layer (factory-wrapped) → **sprint last**, gated on a telemetry-reconstruction report | **High** — V1 even concedes (§2) sprint is not substitution-clean yet still sequences it first; V2 fixes the resulting tension. |
| X-006 | **Backlog.md role** | **Sole task-of-record for v1** | **Derived mirror, NOT task-of-record**, until a lossless MDTM round-trip (gate/convergence/checkpoint schema) is demonstrated + single-authoritative-write-path enforced | **Medium-High** — guards against verified-plausible dual/triple-store drift. |
| X-007 | **Multi-tenant RBAC / EE decision placement** | Phase 5 — late, funded build-or-buy gate *after* Phases 0-4; "deliberately last and separate" | **Phase 5 KILLED as a sequencing defect.** EE-buy-vs-DIY + `@mastra/acp` licensing moves **into Phase 0 as a day-zero commercial blocker** — validate the commercially-gated driver before building 4 phases of sunk-cost momentum | **High** — opposite sequencing philosophy on the strategic driver. |
| X-008 | **Phase 1 scope (domain behind MCP)** | Wrap the **~62K LOC** portable Python as an MCP tool server (no logic change) | Do **NOT** wrap all 62K; expose **3-5 highest-value verified-pure gates/checkers first** (`gates.py`, `wiring_gate.py`, `fmea_classifier.py`), prove schema/error/latency/observability contracts before broad extraction | **Medium** — incremental-proof vs big-bang exposure. |
| X-009 | **Per-tool ACP parity (Cursor/Gemini/Copilot)** | Named as an open gate + risk (multi-tool half of the business case) | **De-prioritized** — front-loads uncertainty irrelevant to go/defer; **Claude + exactly one second tool** is sufficient to prove abstraction value | **Medium** — scope of the Phase-0 spike. |
| X-010 | **convergence.py coupling** | Implicitly counted within the adaptable/agnostic mass (reuse-as-is/adapt) | Explicitly defended as runtime-agnostic — constants (`CHECKER_COST=10`, etc.) are plain integers, `TurnLedger` is a *conditional* import; V2 concedes the skeptic *overreached* in calling it Claude-coupled | **Low** — both end up agreeing it is agnostic; notable as V2 calibrating *against* its own skeptic (honesty-both-ways). |

---

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | V1 | Full 5-phase roadmap with per-phase effort sizing (S/L/L/M/L/XL), explicit dependencies, and rollback paths | **High** — the executable scaffolding V2 only revises, never restates. |
| U-002 | V1 | Component Port Matrix — file-by-file disposition (reuse-as-is / adapt / rewrite / drop) across ~20 modules | **High** — the granular reuse map. |
| U-003 | V1 | "What is lost leaving Claude Code" table (freshness hooks, `/sc:*`, permission modes, telemetry, `CLAUDE_WORK_DIR`, verify-sync, tmux) with severity + mitigation | **Medium** |
| U-004 | V1 | "What would have to be true" decision-theoretic continuation frame (a-f) | **Medium-High** — explicit go/no-go preconditions. |
| U-005 | V2 | **Line-by-line source re-verification**: `StepRunner` Protocol (41-72), sprint test-only `_subprocess_factory` (927-955) vs hardcoded prod path (1320-1324), roadmap 1107 vs 1358, `monitor.py` F2/F4/F6 bindings (398-407, 434-442), `wc` totals (72,906 LOC) | **High** — the evidentiary spine that grounds the whole DEFER case. |
| U-006 | V2 | Decision gates **reordered by what decides go/defer/no-go**, with `@mastra/acp` licensing flagged as decidable *now* (procurement evidence, not architecture) | **High** |
| U-007 | V2 | "Claims that survived vs knocked down" triage, including conceding where the skeptic himself overreached (convergence.py) | **High** — calibration / anti-sycophancy. |
| U-008 | V2 | Flagship-order-reversal rationale tied to seam-cleanliness evidence (pipeline clean → roadmap partial → sprint not-clean) | **High** |

---

## Shared Assumptions (UNSTATED preconditions both variants depend on)

| A-NNN | Assumption | Source agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | **ACP (Agent Client Protocol) is itself stable/mature enough to be the substitution target.** Both treat ACP as the destination contract; neither verifies ACP's own version stability, governance, or spec churn — only Mastra's `@mastra/acp` wrapper and Mastra's churn are examined. | Both make ACP the seam target (V1 §5; V2 gates 2-4) | **High** — if ACP itself is immature, the entire "lossy lowest-common-denominator but stable" premise weakens. | UNSTATED → promote |
| A-002 | **The ~62K LOC Python can run behind an MCP/HTTP boundary at acceptable latency/throughput on orchestration hot-paths.** Both assume the boundary is performant enough for gate/convergence loops; neither benchmarks per-call latency under the convergence 3-cycle load. | V1 Phase 1 (wrap all); V2 Phase 1 (prove "latency contracts" but not as a go/defer gate) | **High** — a slow MCP boundary turns the "keep Python, don't rewrite" thesis into a perf regression. | UNSTATED → promote (V2 partially surfaces) |
| A-003 | **The org has durable TypeScript/Node competency to operate a permanent polyglot (Python+Node+MCP+HTTP) stack.** | V2 raises "permanent-polyglot commitment" as a gate (gate 5) but neither verifies staffing reality | **Medium-High** — "hybrid" collapses to rewrite-or-no-go if staffing absent. | STATED (V2) — documented, not promoted |
| A-004 | **The "5% tolerance acceptance gate" (V1 Phase 2) is operationally measurable.** What metric defines "identical outcomes within 5%" — final artifacts? token totals? gate pass/fail? turn counts? — is never specified, yet the whole parallel-run safety net depends on it. | V1 Phase 2 + §12; V2 inherits parallel-run framing | **Medium-High** — an undefined acceptance metric is an unfalsifiable gate. | UNSTATED → promote |

**Promoted [SHARED-ASSUMPTION] diff points:** A-001, A-002, A-004 (UNSTATED). A-003 documented (STATED in V2). These enter the convergence denominator.

---

## Summary

- Total structural differences: 1 (S-001, High)
- Total content differences / contradictions: 10 (X-001..X-010)
- Total unique contributions: 8 (4 per variant — balanced)
- Total shared assumptions surfaced: 4 (UNSTATED: 3 → promoted; STATED: 1)
- **Highest-severity items (High):** S-001, X-001, X-002, X-003, X-004, X-005, X-007, A-001, A-002
- **Convergence denominator (total diff points):** S(1) + X(10) + A(3 promoted) = **14**
- **Key dynamic:** V2 is a source-grounded correction of V1. The debate must adjudicate (a) which of V2's contradictions are *evidence-backed corrections* (likely sustained) vs (b) where V2 *over-rotated* from "the original under-counts risk" into "defer", potentially discarding V1's still-valid executable roadmap. The merge target is almost certainly **V2's corrected judgments + risk calibration grafted onto V1's structural completeness** — but base selection must be earned in debate, including independent re-check of V2's load-bearing source citations.
