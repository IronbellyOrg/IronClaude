# Refactor Plan — Merging V2's judgments into V1's structure

## Overview
- **Base:** Variant 1 (`merged-requirements.md`) — full structure retained.
- **Incorporated from:** Variant 2 (`revised-recommendation.md`) — judgments, scoring, sequencing.
- **New material:** Round 2.5 invariant probe (3 new gates + 2 missing gates + Phase-0-authorizes-next-phase framing).
- **Change count:** 12 planned changes. **Risk:** Medium (changes the recommendation and resequences the roadmap; additive on structure).
- **Review status:** auto-approved (non-interactive run).

## Planned changes

| # | Change | Source | Target in base | Approach | Risk |
|---|--------|--------|----------------|----------|------|
| 1 | Flip top-line recommendation HYBRID → **DEFER**, reframed as a standalone time-boxed Phase-0 intelligence sprint (output = report, not a port). | V2 §1 + QA sufficiency challenge | §1 Executive Summary & §12 Recap | replace | Med |
| 2 | Replace V/C/L/R **33/30/29/26 → 28/34/20/34** with the inversion rationale (V<R). | V2 §1 table | §1 headline table | replace | Med |
| 3 | Reframe "only ~1.2K of ~73K coupled" → "narrow file seam (process+monitor, 1,200 LOC verified) **+ broad behavioral coupling**" (preflight, TurnLedger budget binding, CLAUDE_WORK_DIR, CLI permission flags). | V2 §2 knocked-down | §1, §2, §4 matrix, §12 | replace+annotate | Med |
| 4 | Correct roadmap abstraction claim → **PARTIAL** (1107 direct `ClaudeProcess` vs only 1358 factory-wrapped). | V2 §2 (source-confirmed) | §2 correction, §4 roadmap row | replace | Low |
| 5 | Reorder flagships: **pipeline (clean StepRunner) → roadmap (semantic-layer) → sprint LAST**, sprint gated on a `monitor.py` telemetry-reconstruction report. | V2 §3 Phase 2 | §9 Phase 2 | restructure | Med |
| 6 | Demote Backlog.md: **derived mirror, not task-of-record**, until lossless MDTM round-trip proven + single-write-path rule. | V2 §3 Phase 3 | §6 Task-of-Record, §9 Phase 3 | replace | Low |
| 7 | X-007 **synthesis**: move `@mastra/acp` licensing + EE-buy-vs-DIY **decision** to day-zero Phase 0; keep the multi-tenant RBAC **build** last. (Do NOT fully "kill Phase 5" — reframe it as a build-phase whose *decision* is pulled forward.) | V2 §3 Phase 5 + architect nuance | §7, §9 Phase 0 & Phase 5 | restructure | Med |
| 8 | Narrow Phase 1: expose **3–5 highest-value verified-pure gates first** (`gates.py`, `wiring_gate.py`, `fmea_classifier.py`) — prove schema/error/latency/observability before broad extraction. | V2 §3 Phase 1 | §9 Phase 1 | replace | Low |
| 9 | De-prioritize per-tool parity (Cursor/Gemini/Copilot) → **Claude + exactly one second tool**; record untested tools' ACP status as a procurement fact. | V2 §4 | §9 Phase 0, §10 risk | replace | Low |
| 10 | Add **3 new gates** G-A (ACP-spec maturity/version-pin/governance), G-B (MCP boundary latency under convergence load), G-C (typed differential spec replacing the unfalsifiable "5% tolerance"). | Invariant probe INV-003/INV-005, panel A-001/A-002/A-004 | §9 Phase 0 gates, §10 risk, §11 gates | insert | Low |
| 11 | Add **2 missing gates**: operating-model/staffing gate for durable polyglot ownership (promote A-003); end-to-end tenancy pilot/control-plane gate (isolation, noisy-neighbor, throughput-vs-baseline). | Invariant probe INV-002/INV-012/INV-014 | §9 (new Phase 0 gate + Phase 5), §11 | insert | Low |
| 12 | Add explicit framing: **Phase-0 success only authorizes the next bounded validation phase**, not full-port feasibility (gate G-A/B/C are necessary, not sufficient; test coupled, not independent). | Invariant probe INV-009/INV-011/INV-013 | §9 intro, §12 | insert | Low |

## Changes NOT being made (V2 considered, base/debate rejected)

| Diff point | V2 proposed | Why base/debate kept otherwise |
|---|---|---|
| X-007 (partial) | Outright **KILL Phase 5** | Rejected as overstated (architect, 78%). The *build* sequencing (tenancy last) was correct in V1; only the *decision timing* moves forward. Phase 5 is reframed, not deleted. |
| X-001 (framing) | Bare "DEFER" | Kept V1's "conditional / gated" spirit by reframing DEFER as a standalone Phase-0 sprint with pass/fail — avoids the org-friction failure mode (QA: DEFER needs a restart meeting). The *substance* is V2's; the *framing* preserves V1's continuity. |
| Scoring | V2's exact 27 Value | Adopted V2's adjusted **28** (V2 itself nudged 27→28 acknowledging pipeline is cleanly injectable) — already reconciled in V2. |

## Risk summary
Overall Medium. The recommendation flip and roadmap resequencing are the high-impact edits; both are well-evidenced (6/6 source confirmations) and rollback is trivial (the source docs are preserved untouched alongside the merged output).
