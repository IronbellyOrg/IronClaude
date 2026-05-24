# Merge Log — Adversarial Run 2 Incorporation Roadmap

**Base**: Variant 2 (Quality Engineer).
**Merge target**: `merged-output.md` (the classification table) + `incorporation-report.md` (the actionable roadmap).
**Provenance**: 11 incorporated items + 6 explicit REJECT rationales + 3 DEFER rationales + 2 SHARED no-action items.

## Changes Applied

### Change #1 — Adopt QE base structure (5 INCORPORATE + 1 ADAPT)
- Source: Variant 2 base.
- Target: Spine of `incorporation-report.md` "Incorporation Roadmap" section.
- Rationale: Highest quant + qual score, broadest INCORPORATE list, defense-in-depth framing.
- Status: APPLIED.

### Change #2 — Adopt Architect's workload-mismatch framing for executive summary
- Source: Variant 1 §"Architectural verdict" + steelman section.
- Target: `incorporation-report.md` Executive Summary.
- Rationale: Architect's framing is the clearest articulation of "forensic and v2 solve different problems." Sets the right expectation that REJECT will dominate.
- Status: APPLIED.

### Change #3 — Adopt Analyzer's frequency-weighted prioritisation as the ordering rule
- Source: Variant 3 §"Concrete recommendations driven by eval evidence" + observed failure-mode enumeration.
- Target: `incorporation-report.md` "Incorporation Roadmap — Order of operations" section.
- Rationale: Analyzer's framing is the cleanest ordering principle. Items driven by observed eval failure modes ship first.
- Status: APPLIED.

### Change #4 — Audit-log schema absorbed into the schema-conformance INCORPORATE
- Source: Variant 3 #1 + Variant 2 #1 (broader scope).
- Target: `incorporation-report.md` INCORPORATE #4 (audit-log schema) + INCORPORATE #5 (hypothesis-card / REPORT.md schemas).
- Rationale: Split QE's monolithic "template schemas" into two distinct items because audit-log schema is driven by observed format variation (analyzer's evidence) while hypothesis-card / REPORT.md schemas are driven by general enforcement (QE's framing).
- Status: APPLIED.

### Change #5 — `test_is_wrong` recommendation unified
- Source: All three variants converged.
- Target: `incorporation-report.md` INCORPORATE #1 (top priority for asymmetric-cost mitigation).
- Rationale: All three advocates put it in INCORPORATE; analyzer made the asymmetric-cost argument explicit; QE made the additivity argument; architect made the trivial-cost argument.
- Status: APPLIED.

### Change #6 — MCP per-server concurrency cap unified
- Source: All three variants converged.
- Target: `incorporation-report.md` INCORPORATE #3.
- Rationale: Unanimous; cheap; latent-risk mitigation.
- Status: APPLIED.

### Change #7 — Repeat-failure detection upgraded from ADAPT to INCORPORATE
- Source: Architect Round 2 concession (upgraded from ADAPT) + Analyzer's eval-driven argument.
- Target: `incorporation-report.md` INCORPORATE #2.
- Rationale: Round 2 convergence shifted this to unanimous INCORPORATE.
- Status: APPLIED.

### Change #8 — Single-agent adversarial fallback as the one ADAPT
- Source: All three variants converged (architect: "single-agent intermediate retry only"; QE: "3-level → 2-level chain"; analyzer: "single-agent scoring fallback before 'pick highest-confidence'").
- Target: `incorporation-report.md` ADAPT #1.
- Rationale: Single unanimous ADAPT survived all of Round 2.
- Status: APPLIED.

### Change #9 — Three DEFER items explicitly enumerated
- Source: QE's deferred items (JSON Schema for output contract, stale-codebase detection, named degradation modes) accepted by all three in Round 2.
- Target: `incorporation-report.md` "Open Questions / Defer-Until" section.
- Rationale: Each item has merit but no observed failure mode driving it yet. Deferred until eval evidence shows the latent failure mode firing.
- Status: APPLIED.

### Change #10 — Five MEDIUM-severity invariant items as implementation gotchas
- Source: Round 2.5 invariant probe.
- Target: `incorporation-report.md` "Implementation Gotchas" section.
- Rationale: No HIGH-severity items block convergence, but 5 MEDIUM items must be addressed in change specs.
- Status: APPLIED.

### Change #11 — Comprehensive REJECT list with explicit rationale
- Source: Unanimous REJECT verdicts across all three variants.
- Target: `incorporation-report.md` "Explicit Rejects" section.
- Rationale: Honesty requires articulating *why* each forensic position is rejected, with workload-mismatch evidence. Prevents future "should we revisit this?" cycles.
- Status: APPLIED.

## Post-merge Validation

- All 31 substantive differences from `debate-1-differences/merged-output.md` have an explicit verdict (INCORPORATE / ADAPT / DEFER / REJECT / SHARED).
- All INCORPORATE / ADAPT items specify: WHICH v2 file changes, WHAT the change is, WHICH wave, WHY (with eval-evidence citation where applicable), COST, RISK.
- Implementation gotchas (Round 2.5 invariants) cross-referenced in incorporation report.
- DEFER items have explicit "defer-until" criteria.
- REJECT items have explicit rationale (workload mismatch / no audience / no observed failure mode).
- No new contradictions introduced by the merge (re-scanned `incorporation-report.md` for opposing claims; none found).

## Merge Status: SUCCESS

11 of 11 planned changes applied. Validation passes. Final deliverable `incorporation-report.md` ready.
