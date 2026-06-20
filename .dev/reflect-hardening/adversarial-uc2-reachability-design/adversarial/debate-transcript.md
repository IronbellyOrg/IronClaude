# Adversarial Debate Transcript

## Metadata
- Depth: deep (3 rounds eligible)
- Rounds completed: 2 + invariant probe + targeted Round 3 on residual point
- Convergence achieved: 0.86
- Convergence threshold: 0.80
- Focus: canonical ownership, contract packaging, safety
- Advocate count: 3 (C-canonical, B-canonical, Coexist)
- Mode: in-context adversarial reasoning (fallback_mode=true) — advocates steelmanned by a single evaluator, not separate Task agents (per concurrent --parallel session in this worktree)

## Taxonomy tagging of diff points
- L3 (state-mechanics): C-003 (verdict/gate force), X-003 (taxonomy mapping), X-004 (leakage guard), A-001/A-002 — **debate cannot bypass these**
- L2 (structural): C-001, C-004, C-005, X-001, X-002, U-001..U-003, A-003
- L1 (surface): C-006 (naming/ids), C-007 (maturity)

## Round 1: Advocate Statements

### Advocate — C-canonical
**Steelman of B:** B's broad recall is genuinely valuable — un-annotated durable effects exist, and B catches dead surfaces C never sees. B's fail-open discipline is principled. **Critique:** a *gate* (a verdict that blocks) must be high-precision; B is explicitly degrade-only and *does not force Tier 2* precisely because it cannot be trusted to block. The user asked for the canonical reachability **GATE** — that is the blocking role, which only C's real-boot bar can safely fill. C is also the only design complete enough to ship safely today (wrapper, docs parity, bounded cost, PRE reflect coverage 1.0).

### Advocate — B-canonical
**Steelman of C:** C's real-boot-only Regression is the gold standard for precision and directly kills false-PASS on claimed-but-unexecuted effects. **Critique:** C only inspects *explicitly annotated* `@sink` contracts — it is blind to the majority of code where no one wrote an annotation. As a "reachability" feature it has narrow coverage; B sees the whole production surface. B is the prior art and the original owner of the "uc2-reachability" name.

### Advocate — Coexist
**Steelman of both:** both detect real, distinct defects; discarding either loses signal. **Claim:** field names don't collide and both bumps are additive, so a single 1.6.0 union schema is mechanically valid — ship both, lose nothing. **Concession:** this requires rewriting C-040 and forces simultaneous landing into one SKILL.md.

## Round 2: Rebuttals

- **C → B (recall objection):** Conceded — C's narrow recall is real and *by design* (precision over recall for a blocking verdict). But this does not make B the gate; it makes B the **complementary advisory detector**. Recall belongs in an advisory lane that degrades, never blocks — which is exactly B's own posture. So B's strength argues for B-as-advisory, not B-as-gate.
- **B → C (naming/prior-art):** Conceded weak — naming and authorship order are not safety arguments. Withdrawn as decisive.
- **Coexist → both (union is valid):** Rebutted — mechanical validity ≠ safety. Co-locating B's degrade-only verdicts beside C's real-boot Regression in one report, one taxonomy, one status computation creates a precedence hazard (see INV-001) and forces a 3-way single-fix-agent merge (matrix M-016/M-047). Validity is necessary, not sufficient.
- **Shared-assumption A-002 surfaced:** B's `runtime_surface_*` need not be *stable contract* fields at all. B's whole posture is advisory/telemetry → its fields could be telemetry, requiring **no contract bump**, which dissolves the X-001/M-028 collision outright. Neither original task stated this.

## Round 2.5: Invariant Probe
See `invariant-probe.md`. Two HIGH-severity items (INV-001 precedence, INV-002 sufficiency) were raised against the emerging "C-canonical" consensus and were **incorporated as binding preconditions** in the decision (not left unaddressed).

## Round 3 (targeted): residual non-converged point
**Point:** B's packaging once C owns 1.6.0 — (a) rebase to additive `1.7.0` stable minor, or (b) reclassify `runtime_surface_*` as advisory telemetry (no bump).
- C-advocate: prefers (b) — matches B's advisory nature, removes all version contention, lightest footprint.
- B-advocate: (b) is acceptable IF telemetry still surfaces in the report/ledger; if downstream consumers need a *stable* field, (a) is required.
- **Not resolved** — depends on whether any consumer needs `runtime_surface_*` as a *stable* contract guarantee. Flagged `needs_human_decision` (B-task owner). Does not block the primary decision.

## Scoring Matrix

| Diff Point | Level | Winner | Confidence | Evidence |
|---|---|---|---|---|
| C-003 (gate vs degrade) | L3 | C | 88% | Only real-boot precision may safely block; B is degrade-only by its own design |
| X-001/X-004 (1.6.0 + leakage) | L3/L2 | C (owns 1.6.0); B refactored | 85% | C-040 + version collision resolved by sequencing, not union |
| C-001/C-002 (capability) | L3/L2 | Both (complementary) | 82% | A-001 CONTRADICTED — not redundant; keep both |
| U-001/U-003 (precision + maturity) | L2 | C | 90% | C ships gate-grade precision + full surface today |
| U-002 (recall) | L2 | B (advisory lane) | 80% | Real value, but advisory not gating |
| A-002 (telemetry option) | L3 | B-refactor | 70% | Open: telemetry vs stable field |

## Convergence Assessment
- Points resolved: 5 of 6 (A-002 packaging sub-point open)
- Alignment: 86% ≥ 80% threshold → **CONVERGED**
- Taxonomy coverage: L1 ✓ L2 ✓ L3 ✓ (no forced round needed)
- Invariant gate: 0 HIGH UNADDRESSED after incorporation → not blocked
- Unresolved: B packaging (1.7.0 stable minor vs advisory telemetry) → `needs_human_decision`
