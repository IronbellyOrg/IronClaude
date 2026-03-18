# Diff Analysis: Branch Decision Comparison

## Metadata
- Generated: 2026-03-17
- Variants compared: 2
- Variant 1 (Architect): Branch (b) at 88% confidence
- Variant 2 (Analyzer): Branch (b), conditions stated
- Total differences found: 18
- Categories: structural (3), content (7), contradictions (2), unique contributions (4), shared assumptions (2)

---

## Structural Differences

| # | Area | Variant 1 (Architect) | Variant 2 (Analyzer) | Severity |
|---|------|----------------------|---------------------|----------|
| S-001 | Conclusion framing | "Spec can be amended; dead code cannot be safely activated" — documentation vs runtime risk framing | "Spec was written against a nonexistent execution substrate — deviation is a correction, not a compromise" — spec defect framing | Low |
| S-002 | Branch (b) conditions | 5 required actions listed (spec amendment, NR-1, TurnLedger deferral, P2b scope reduction, locked decision) | 6 conditions listed with more emphasis on forward compatibility (retain task-scope in spec as deferred, emit NR-1 field anyway, shadow mode for empirical evidence) | Low |
| S-003 | Counter-argument section | Not present | Present — addresses 3 challenges including "8-state is over-engineered" with analysis | Medium |

---

## Content Differences

| # | Topic | Variant 1 (Architect) | Variant 2 (Analyzer) | Severity |
|---|-------|----------------------|---------------------|----------|
| C-001 | NR-1 under Branch (b) | Phase-level aggregation — tasklist still emits per-task, runner aggregates | Optional forward compatibility — emit field but no runtime consumer; defer if needed | Low |
| C-002 | TurnLedger under Branch (b) | Defer resolution of reimbursement_rate — already dead, adding decision now adds no value | Not needed at all under (b); no budget contention | Low |
| C-003 | State machine size characterization | 8 states (milestone + release scopes) — sufficient | Analyzes all 4 state machines (PhaseStatus 12 + TaskStatus 4 + AuditWorkflowState 8 + GateDisplayState 7 = 27 vs 35 under branch (a)) — provides total system complexity view | Medium |
| C-004 | execute_phase_tasks() characterization | "Dead code with unbounded activation risk; zero production history" | More detailed: function is non-trivial (iterates TaskEntry, checks TurnLedger.can_launch(), has test factory injection) but has never run with real ClaudeProcess; 8-12 functions need modification | Low |
| C-005 | Branch (a) delivery estimate | No timeline estimate; "if activation reveals latent defects (likely), Phase 2 slips" | Estimates 2-3 weeks for core path + 5 additional integration items; characterizes as "a separate feature delivery" | Medium |
| C-006 | Spec deviation characterization | "Four of twelve audit states eliminated; override rules in §4.3 still apply at milestone scope" | "Deviates at exactly one point: §4.1 task-scope state machine. Affects 4 of 12 states and 6 of 18 legal transitions. Milestone and release are fully satisfiable." | Low |
| C-007 | Rollback safety | Single vs double-variable rollback mentioned briefly | Explicitly modeled: branch (a) requires reverting audit gates AND task-scope execution; branch (b) reverts audit gates only | Low |

---

## Contradictions

| # | Point | Variant 1 | Variant 2 | Impact |
|---|-------|-----------|-----------|--------|
| X-001 | Is 8-state machine sufficient? | Yes — minimum viable set for lease-based audit with retry | Raises and then resolves the question (4 states per scope is minimum; reducing further is unsafe) — converged answer but via different paths | Low |
| X-002 | Should task-scope state machine be retained in spec? | "SS 4.1 task-scope transitions must be marked as 'deferred to future release'" | "Do NOT delete the task-scope state machine — retain with [v1.3 — deferred] marker" — this is the same recommendation but Variant 1's phrasing could imply removal | Low |

---

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|-------------|-------|
| U-001 | Variant 2 (Analyzer) | Complete downstream consequence matrix — 9-row table comparing all concerns side-by-side under both branches | High |
| U-002 | Variant 2 (Analyzer) | Counter-arguments section: systematically addresses "spec says task-scope so we must", "activate anyway as good engineering", "phase-scope too coarse", "8-state is over-engineered" | High |
| U-003 | Variant 2 (Analyzer) | Shippability assessment with specific Phase 2 acceptance criterion reference (§10.3 criterion: "timeout/retry paths terminate deterministically") | Medium |
| U-004 | Variant 1 (Architect) | Cleaner summary of required actions under Branch (b) adoption — actionable decision checklist | Medium |

---

## Shared Assumptions

| # | Assumption | Classification | Promoted |
|---|-----------|----------------|----------|
| A-001 | execute_phase_tasks() is confirmed dead code (MF-1 CRITICAL from adversarial review) | STATED | No |
| A-002 | Phase-scope audit gates are sufficient for v1.2.1 operational value, with task-scope deferred | UNSTATED | Yes |

### Promoted Shared Assumptions

| # | Assumption | Impact | Status |
|---|-----------|--------|--------|
| A-002 | Neither variant challenges whether phase-scope gates deliver meaningful audit value in production; they both assume the 8-state machine delivers the goal | If phase-scope gates are insufficient (e.g., a phase contains 10 tasks of wildly varying quality), the entire Branch (b) justification weakens | UNVERIFIED |

---

## Summary
- Total structural differences: 3 (all Low/Medium)
- Total content differences: 7 (mostly Low)
- Total contradictions: 2 (both Low, easily resolved)
- Total unique contributions: 4
- Shared assumptions surfaced: 2 (1 stated, 1 unstated/promoted)
- **Both variants agree on Branch (b)** — convergence before debate begins
- Similarity score: ~87% — variants are substantially aligned; debate will refine conditions, not reverse the decision
