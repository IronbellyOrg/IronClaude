# Adversarial Debate Transcript — Porting SuperClaude Pipeline to Stack D (Mastra + Backlog.md + Beads)

**Moderation method:** Steelman-then-strongest-objection, with codebase verification of load-bearing structural claims.
**Date:** 2026-06-02
**Proposals under debate:** A (reference architecture), B (feasibility skeptic / defer), C (strangler-fig), D (reuse-maximizing seam swap).

---

## 0. Ground-truth verification (performed before critique)

Before steelmanning, the moderator verified the structural claims the four proposals stake their recommendations on. Results:

| Claim | Source proposal | Verification | Result |
|---|---|---|---|
| ClaudeProcess seam is small | A, B, C, D | `wc -l`: process.py **244**, sprint/process.py **385**, monitor.py **571** (~1.2K total) | CONFIRMED |
| pipeline runs against injected StepRunner Protocol | D | `class StepRunner(Protocol)` at executor.py:41; docstring: *"Launching the claude -p subprocess"* is the runner's sole responsibility | CONFIRMED |
| roadmap wraps runtime behind factory | D | `claude_process_factory=lambda: _ClaudeRunner(config)` at roadmap/executor.py:1364; `_ClaudeRunner` at :1253 | CONFIRMED |
| gates/convergence/audit have zero runtime coupling | A, C, D | grep subprocess/ClaudeProcess in roadmap/gates.py, roadmap/convergence.py, audit/wiring_gate.py → **0 matches each** | CONFIRMED |
| sprint has explicit `delegate_runner` substitution branch (line 1007) | D | line 1007 is a private `_subprocess_factory` test hook with hardcoded default to `_run_task_subprocess`; **no `delegate_runner` identifier exists** | PARTIALLY REFUTED — seam exists but is a narrower test hook, not a clean Protocol |

**Consequence:** D's "already built for substitution" thesis is *verified for pipeline and roadmap* but *overstated for the 2150-LOC sprint flagship*, where the seam is entangled with monitor/TUI/tmux/TurnLedger. This single correction reshapes the merge (sprint Phase 2 carries more rewrite than D implies).

---

## 1. Proposal A — Reference Architecture (HYBRID)

**Steelman.** The most intellectually honest proposal because it refuses to let the AcpAgent≈ClaudeProcess analogy inflate the recommendation. Its decisive move is the LOC stratification — verified above: ~1.2K coupled, ~60K runtime-agnostic — and it uses that number correctly to land on HYBRID, not rewrite. The port_matrix is the most disciplined: it assigns `reuse-as-is` to the ~12.7K-LOC FMEA/audit heuristic mass with the right rationale (rewriting subtle regex/AST heuristics to TS is high-risk/low-reward). It alone names the central strategic contradiction out loud: the entire reason for the port — multi-tenant RBAC — is Mastra-EE-paid and lives OUTSIDE the reuse story, so a technically successful port can still fail the business objective.

**Strongest objection.** It is structurally identical to C and D on the engineering plan yet scores itself with conflicting signals — likelihood 24/40 (below C's 28 and D's 29) while wearing the most confident "reference architecture" framing. The rhetoric and the number disagree. Substantively it over-centers Mastra: it makes Mastra the spine from Phase 1, when D shows (and the verified StepRunner + factory injection confirm) that a thin in-process Python ACP client could deliver multi-tool support in Phases 0-2 with ZERO Mastra dependency, deferring all Mastra API-churn and EE risk.

**Verdict.** STRONG on diagnosis, OVER-COMMITTED on sequencing. Best source for the port_matrix dispositions and risk taxonomy; not for phase ordering.

---

## 2. Proposal B — Feasibility Skeptic (DEFER)

**Steelman.** The indispensable adversary and the only proposal that keeps "do not port" genuinely live. Its core insight is unassailable and verified: Mastra replaces ONLY the ~1.2K-LOC seam; the other ~60K is domain intelligence Mastra never touches — so a like-for-like replatform spends most of its budget recreating what already works. It frames the decision as conditional (EE cost acceptable AND ACP parity proven for Claude + ≥1 tool AND hybrid preserves Python/Markdown IP) and closes with the strongest decision-theoretic framing in the set: an explicit "what would have to be true." Its worst-case VCLR (value 22, likelihood 16, risk 36) is the honest anchor that stops the other three drifting into optimism. Keeping the existing CLI as the live benchmark/fallback is operationally correct and underweighted elsewhere.

**Strongest objection.** It scores a strawman. Its VCLR is explicitly "for a full Stack D replatform, not a narrow ACP spike" — but NONE of the others recommend a big-bang replatform; all recommend the same hybrid strangler path B's own Phase 0-6 describes. So likelihood 16 measures a plan nobody proposed, making the "defer" headline misleading. The disagreement with A/C/D is largely semantic/temperamental. It also slightly over-weights Claude-native feature loss (freshness hooks, /sc:* loading) as first-tier strategic risk — those are dev ergonomics, not the moat; the moat (gate/convergence/FMEA/audit IP) is *preserved* by the port.

**Verdict.** ESSENTIAL as gate-setter, WEAK as a standalone recommendation. Its "defer" is really "hybrid with hard commercial+parity gates before any TS rewrite" — the consensus. Adopt its Phase-0 commercial stop/go, its benchmark discipline, and its "what would have to be true" criteria. Reject "defer" as the headline.

---

## 3. Proposal C — Strangler-Fig (HYBRID)

**Steelman.** The best-engineered execution plan. The strangler-fig framing fits a system whose coupling is a single isolated seam: <2-week spike (correctly the only proposal to size Phase 0 as **S**), then run the new Mastra sprint workflow IN PARALLEL with the existing Python CLI for 2-3 sprints under an explicit **identical-outcomes-within-5% acceptance gate**. That parallel-run-with-tolerance-gate is the single most valuable operational idea in the debate — it converts a high-blast-radius cutover into an evidence-gated, reversible transition, and no other proposal specifies a concrete threshold. Its file-by-file port_matrix (LOC + difficulty) is the most actionable for task generation, and it uniquely flags the Python→TS serialization-impedance risk at the MCP boundary.

**Strongest objection.** Most optimistic scorer (likelihood 28, risk 28) while inheriting every unverified parity risk, and its Beads disposition is internally inconsistent: it assigns Beads `adapt` ("start with embedded mode") while listing Beads Dolt instability and dual-source drift in its own top-risks — A, B, and the Beads research all conclude DROP/DEFER. C is the outlier, contradicted by its own evidence. Its VCLR also under-exposes the `value` anchor (buried in notes), and it front-loads Mastra Server in Phase 2, partially importing the vendor risk D defers more cleanly.

**Verdict.** STRONG; the best EXECUTION skeleton. Adopt parallel-run + 5%-tolerance gate, S-sized Phase 0, and file-level port_matrix. Override Beads `adapt` → DROP/DEFER.

---

## 4. Proposal D — Reuse-Maximizing Seam Swap (HYBRID)

**Steelman.** Contributes the most important — and VERIFIED — architectural insight: the codebase was already built for runtime substitution. The StepRunner Protocol docstring names launching the claude subprocess as the runner's sole job; roadmap uses `claude_process_factory` + `_ClaudeRunner`; pipeline callers are unchanged by a runner swap. This makes the seam swap a low-risk *adapt*, not a rewrite. Its sharpest move is decoupling Mastra from the seam swap entirely: Phases 0-2 need NO Mastra (a thin Python ACP/stdio client preserving the StepRunner contract delivers multi-tool support), so Mastra Server + the EE decision defer to Phases 4-5 where they are independently justifiable. Lowest-risk VCLR (risk 24, complexity 27) precisely because it minimizes new vendor surface. It also most precisely localizes the real risk: **monitor.py's stream-json→ACP event reconstruction**, not AcpAgent itself.

**Strongest objection.** It over-generalizes from the pipeline seam to the whole system. It claims the sprint flagship has an "explicit `delegate_runner` branch (line 1007)" — verification shows line 1007 is a private `_subprocess_factory` test hook with a hardcoded `_run_task_subprocess` default; the identifier `delegate_runner` does not exist. So "built for substitution" is solid for pipeline/roadmap but OVERSTATED for the 2150-LOC sprint flagship, where the seam is entangled with monitor/TUI/tmux/TurnLedger. Second, the permanent two-runtime (Python+Node) boundary it endorses is a real, under-priced operational tax. Third, deferring Mastra so late risks delivering multi-USER (SimpleAuth) but never the multi-TENANT company goal if momentum stalls at Phase 4.

**Verdict.** STRONG; the best ARCHITECTURE. Adopt "swap the seam not the stack," the verified reuse argument, the "monitor.py is the real risk" precision, and Mastra-late sequencing. Correct the sprint overstatement: sprint's seam is a private `_subprocess_factory`, not a clean Protocol.

---

## 5. Cross-Proposal Contradictions

1. **Beads** — A/B/research = DROP/DEFER; C = ADAPT (outlier, self-contradicting). Resolution: DROP/DEFER v1.
2. **Mastra sequencing** — A (early/spine) vs D (late/vendor-free first); C in between. Genuine architectural fork; cannot be averaged away.
3. **Headline label** — B "defer" vs A/C/D "hybrid," but B's Phase 0-6 *is* a gated strangler-fig. Semantic, not architectural.
4. **Sprint seam cleanliness** — D claims clean substitution branch; code shows private `_subprocess_factory`. Ground truth: sprint is harder than D implies; A/C correctly rate it very-high.
5. **Domain end-state** — D: permanent polyglot; A/C: transitional with eventual TS migration. Unresolved (org-dependent).
6. **Score calibration** — likelihood spread 16→29 for substantially the same plan reflects temperament, not different plans.

---

## 6. Convergence

**Score: 0.82.** All four converge on a HYBRID strangler-fig: Phase-0 ACP parity spike as hard gate → port sprint first → keep ~60K LOC Python domain logic (behind MCP or in-process) → Backlog.md as task-of-record → defer Beads → EE decision as a distinct late gate. The high agreement on *shape and plan* is what pushes the score above 0.8. It is held below ~0.9 by (a) the genuine Mastra-early-vs-late fork, (b) the permanent-vs-transitional polyglot disagreement, and (c) the fact that the empirical foundation (ACP parity for max_turns/permission/CLAUDE_WORK_DIR/TurnLedger-reconstruction, @mastra/acp license, per-tool parity) is UNVERIFIED across all four — consensus on the plan does not resolve the unrun spike.

---

## 7. Selected Base + Merge Guidance

**Architectural base: D.** **Execution base: C.** **Risk taxonomy + strategic framing: A.** **Conditionality gates + benchmark discipline: B.**

Merge spine:
1. Frame as D's verified seam-swap thesis (~1.2K LOC), with the sprint-seam correction (private `_subprocess_factory`, very-high difficulty).
2. Phase 0 = B's dual gate (commercial stop/go + semantic parity spike). Keep existing CLI as benchmark throughout.
3. Execution = C's S-sized Phase 0, sprint-first, parallel-run with 5%-tolerance gate, per-phase gates, file-level port_matrix.
4. State A's EE-strategic-mismatch as the canonical caveat; EE buy-vs-DIY is a distinct funded late gate.
5. Beads = DROP/DEFER v1 (override C). Backlog.md sole task-of-record behind existing checkpoint/TaskEntry models; live-probe its MCP decision/milestone tools first.
6. Name the Mastra-early-vs-late fork (A vs D) as an explicit Phase-1 decision with an owner; default to D's Mastra-late.
7. Preserve B's conditionality language and the five unresolved conflicts as named gates, not buried assumptions.

*End of transcript.*
